import pygame

class Cooldown:
    """A cooldown class, counting down to zero, optionally repeating.

        temp: float - "temperature" to cool down from
    """

    def __init__(self, temp=1):
        self.temp = self._temp = temp

    def __call__(self, dt):
        """cooldown(dt) -> float

        reduces and returns the cooldown
        """
        self.temp -= dt
        if self.temp < 0:
            self.temp = 0

    def reset(self):
        """cooldown.reset()

        reset the cooldown to its initial temperature to use it again
        """
        self.temp = self._temp

    @property
    def cold(self):
        """if cooldown.cold: ...

        the cooldown is cold, if it is down to zero.  From here, you can either
        act on it and/or reset.
        """

        if self.temp == -1:
            return False
        elif self.temp == 0:
            return True
        else:
            return False


class Teleprinter:
    """Simulate a teleprinter effect.  Text flows letter by letter into a box

    Parameters:

        pos: Vector2 - *center* position of the text box
        backdrop: pygame.Surface - background to draw the text on.
        text: the text to teleprint
        margin: int - margin around the text within the text box
        ticket_speed: float - delay in seconds between letters
        backdrop: pygame.Surface - optional.  e.g. a paper texture
        font: pygame.font.SysFont - Falls back to couriernew, 16pt
        font_color: pygame.Color - defaults to white

    The rect of the background also gives the size of the box.  If you don't
    need a background, just pass a transparent surface.

    The process shouldn't be too resource intensive, since every letter is
    blitted onto a surface that's kept in the class.  Line breaks as well as
    scrolling are implemented.

    Run and look into eleprinter-demo for an example.

    """
    def __init__(self, pos, text, margin=10, ticker_speed=0.1,
                 backdrop=None, font=None, font_color=None, sound=None):
        self.surface = pygame.Surface(backdrop.get_size(), pygame.SRCALPHA)
        self.backdrop = backdrop
        self.pos = self.surface.get_rect()
        self.pos.center = pos
        self.font = font if font else pygame.font.SysFont('couriernew')
        self.font_color = font_color if font_color else pygame.Color('white')
        self.margin = margin
        self.text = self.gen_text(text)
        self.line_height = self.font.get_linesize()
        self.cooldown = Cooldown(ticker_speed)
        self.sound = sound

        w, h = self.backdrop.get_size()
        w -= 2 * margin
        h -= 2 * margin
        self.textbox = pygame.Surface((w, h), pygame.SRCALPHA)
        self.textbox_rect = self.textbox.get_rect()
        self.textbox_rect.center = self.backdrop.get_rect().center

        self.cursor = [0, 0]

        self.done = False

    def gen_text(self, text):
        """Generator to return the text character by character
        """
        for c in text:
            yield c

    def update(self, dt):
        """Call this with delta time from the main loop

            tt.update(dt) -> bool

        Returns false when the text is exhausted.
        """
        self.cooldown(dt)
        if not self.cooldown.cold or self.done:
            return False

        self.cooldown.reset()

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
            if char in '.!?;':
                self.cooldown.temp = 1.5

        return True

    def draw(self, screen):
        """Call this from the main loop

            tt.draw(screen) -> bool

        Returns false when the text is exhausted.
        """
        self.surface.blit(self.backdrop, (0, 0))
        self.surface.blit(self.textbox, (self.margin, self.margin))
        screen.blit(self.surface, self.pos)
