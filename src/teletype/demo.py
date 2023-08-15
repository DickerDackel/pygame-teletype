import sys
import os.path
import importlib.resources
import pygame

from teletype import Teletype


FPS = 60
SIZE = (1024, 768)

LIPSUM = """Press ESC any time to end the demo, but keep watching until scrolling starts.

Use UP and DOWN to change the ticker speed.  SPACE toggles random delay every now and then, PERIOD toggles pause after the end of each sentence...

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

Did I mention you can press ESC any time to end the demo?
"""


def main():
    pygame.init()
    pygame.display.set_caption('Teletype demo')
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    beep = importlib.resources.files('teletype.data').joinpath('beep.wav')
    sound = pygame.mixer.Sound(beep) if os.path.isfile(beep) else None

    textbox = pygame.Surface((384, 256))
    textbox.fill(pygame.Color('peachpuff3'))
    pygame.draw.line(textbox, pygame.Color('peachpuff4'), (  0,   0), (383,   0), width=3)
    pygame.draw.line(textbox, pygame.Color('peachpuff4'), (  0,   0), (  0, 255), width=3)
    pygame.draw.line(textbox, pygame.Color('papayawhip'), (  0, 255), (383, 255), width=3)
    pygame.draw.line(textbox, pygame.Color('papayawhip'), (383,   0), (383, 255), width=3)
    textbox_rect = textbox.get_rect()

    tt = Teletype(pos=screen.get_rect().center,
                  text=LIPSUM,
                  margin=10,
                  ticker_speed=0.05,
                  backdrop=textbox,
                  font=pygame.font.SysFont('couriernew', 16),
                  font_color=pygame.Color('black'),
                  sound=sound)

    running = True
    while running:
        dt = clock.get_time() / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_UP:
                    tt.cooldown.init *= 0.66
                elif e.key == pygame.K_DOWN:
                    tt.cooldown.init *= 1.333
                elif e.key == pygame.K_SPACE:
                    tt.random_delay = 0.05 - tt.random_delay
                elif e.key == pygame.K_PERIOD:
                    tt.pause_after_sentence = not tt.pause_after_sentence

        screen.fill(pygame.Color('aquamarine4'))

        tt.update(dt)
        tt.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
