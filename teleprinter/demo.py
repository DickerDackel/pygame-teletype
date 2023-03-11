import pygame

from teleprinter import Teleprinter, Cooldown


FPS = 60
SIZE = (1024, 768)

LIPSUM = """Press ESC any time to end the demo, but keep watching until scrolling starts.

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.

Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.

Did I mention you can press ESC any time to end the demo?
"""


def main():
    pygame.init()
    pygame.display.set_caption('Teleprinter demo')
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    sound = pygame.mixer.Sound('beep.wav')

    textbox = pygame.Surface((384, 256))
    textbox.fill(pygame.Color('peachpuff3'))
    pygame.draw.line(textbox, pygame.Color('peachpuff4'), (  0,   0), (383,   0), width=3)
    pygame.draw.line(textbox, pygame.Color('peachpuff4'), (  0,   0), (  0, 255), width=3)
    pygame.draw.line(textbox, pygame.Color('papayawhip'), (  0, 255), (383, 255), width=3)
    pygame.draw.line(textbox, pygame.Color('papayawhip'), (383,   0), (383, 255), width=3)
    textbox_rect = textbox.get_rect()

    tt = Teleprinter(pos=screen.get_rect().center,
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

        screen.fill(pygame.Color('aquamarine4'))

        tt.update(dt)
        tt.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
