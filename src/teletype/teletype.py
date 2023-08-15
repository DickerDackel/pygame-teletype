import pygame
import random

from pgcooldown import Cooldown


class Teletype(pygame.sprite.Sprite):
    """A textbox with a teletype text effect as in old adventure games.

    This is a pygame.sprite.Sprite subclass, so pygame.sprite.Group features
    are available.

    Parameters
    ----------
        text: str
            the text to teletype

        rect: pygame.rect.Rect
            dimensions and position of the teletype image

        *groups:
            sprite groups to add this instance to

        ticker_speed: float
            delay in seconds between letters

        margin: int
            margin around the text within the text box

        backdrop: pygame.Surface
            optional.  e.g. a paper texture

        font: pygame.font.SysFont
            Falls back to couriernew, 16pt

        font_color: pygame.Color
            defaults to white

        sound: pygame.mixer.Sound = None
            audio to play at every character

        random_delay: float = 0
            randomly add pauses, faking transmission delays

        pause_after_sentence: bool = True
            Make a longer pause after ./!/?/;

    The rect of the background also gives the size of the box.  If you don't
    need a background, just pass a transparent surface.

    The process shouldn't be too resource intensive, since every letter is
    blitted onto a surface that's kept in the class.  Line breaks as well as
    scrolling are implemented.

    Run and look into teleprinter-demo for an example.
    """
    RANDOM_PAUSE_FACTOR = 5
    SENTENCE_PAUSE_FACTOR = 10

    def __init__(self, text, rect, *groups, margin=10, ticker_speed=0.1,
                 backdrop=None, font=None, font_color=None, sound=None,
                 random_delay=0, pause_after_sentence=True):
        super().__init__(*groups)

        # Yes, I know, this all should be a dataclass...
        self.text = self.gen_text(text)
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=rect.center)
        self.ticker_speed = ticker_speed
        self.ticker = Cooldown(ticker_speed)
        self.margin = margin
        self.backdrop = backdrop
        self.font = font if font else pygame.font.SysFont('couriernew')
        self.font_color = font_color if font_color else pygame.Color('white')
        self.line_height = self.font.get_linesize()
        self.sound = sound
        self.random_delay = random_delay
        self.pause_after_sentence = pause_after_sentence

        w, h = self.backdrop.get_size()
        w -= 2 * margin
        h -= 2 * margin
        self.textbox = pygame.Surface((w, h), pygame.SRCALPHA)
        self.textbox_rect = self.textbox.get_rect(topleft=(margin, margin))

        self.cursor = [0, 0]

        self.done = False

    def gen_text(self, text):
        """Generator to return the text character by character"""
        for c in text:
            yield c

    def update(self, dt):
        """Call update with delta time to generate the text

        Parameters
        ----------
        dt: float
            delta time in seconds

        Returns
        -------
        None
        """
        if not self.ticker.cold or self.done:
            return False

        self.ticker.reset(self.ticker_speed)

        try:
            char = next(self.text)
        except StopIteration:
            self.done = True
            return False

        def eol():
            self.cursor[0] = 0
            if self.cursor[1] + 2 * self.line_height >= self.textbox_rect.height:
                self.textbox.scroll(0, -self.line_height)

                # Scroll doesn't clear the freed area. Fill it with transparent.
                fill = pygame.Rect(0, self.cursor[1],
                                   self.textbox_rect.width, self.line_height)
                self.textbox.fill((255, 255, 255, 0), fill)
            else:
                self.cursor[1] += self.line_height

        if char == '\n':
            eol()
        else:
            cell = self.font.render(char, True, self.font_color)
            r = cell.get_rect()

            wrapped = False
            if self.cursor[0] + r.width > self.textbox_rect.width:
                eol()
                wrapped = True

            # Don't print a space at the beginning of a line after a wrap.
            if not (wrapped and char == ' '):
                self.textbox.blit(cell, self.cursor)
                self.cursor[0] += r.width

                if self.sound:
                    self.sound.play()

            # Extended delay if a sentence ends
            if self.pause_after_sentence and char in '.!?;':
                self.ticker.reset(self.ticker_speed * Teletype.SENTENCE_PAUSE_FACTOR)

            elif self.random_delay and random.random() < self.random_delay:
                self.ticker.reset(self.ticker_speed * Teletype.RANDOM_PAUSE_FACTOR)

        self.image.blit(self.backdrop, (0, 0))
        self.image.blit(self.textbox, self.textbox_rect)
