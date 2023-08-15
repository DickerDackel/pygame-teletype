import os.path
import importlib.resources
import json
import pygame

from teletype import Teletype


FPS = 60
SIZE = (1024, 768)


def create_box(w, h):
    canvas = pygame.Surface((w, h))
    canvas.fill(pygame.Color('peachpuff3'))
    pygame.draw.line(canvas, pygame.Color('peachpuff4'), (    0,     0), (w - 1,     0), width=3)
    pygame.draw.line(canvas, pygame.Color('peachpuff4'), (    0,     0), (    0, h - 1), width=3)
    pygame.draw.line(canvas, pygame.Color('papayawhip'), (    0, h - 1), (w - 1, h - 1), width=3)
    pygame.draw.line(canvas, pygame.Color('papayawhip'), (w - 1,     0), (w - 1, h - 1), width=3)
    return canvas


pygame.init()
pygame.display.set_caption('Teletype demo')
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

beep = importlib.resources.files('teletype.data').joinpath('beep.wav')
sound = pygame.mixer.Sound(beep) if os.path.isfile(beep) else None

with open(importlib.resources.files('teletype.data').joinpath('multidemo.json')) as f:
    boxes = json.load(f)

tt_list = []
for location, box_desc in boxes.items():
    tb = create_box(*box_desc['size'])
    tbr = tb.get_rect(center=box_desc['pos'])

    tt_list.append(Teletype(text=box_desc['text'],
                            rect=tbr,
                            margin=10,
                            ticker_speed=box_desc['tickerspeed'],
                            backdrop=tb,
                            font=pygame.font.SysFont('couriernew', 16),
                            font_color=pygame.Color('black'),
                            sound=sound,
                            random_delay=0.05))

sprite_group = pygame.sprite.Group()
sprite_group.add(tt_list)


def main():
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

        sprite_group.update(dt)
        sprite_group.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
