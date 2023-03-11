
import sys
import os.path
import importlib.resources
import json
import pygame

from teletype import Teletype
from cooldown import Cooldown


FPS = 60
SIZE = (1024, 768)

def create_box(w, h):
    textbox = pygame.Surface((w, h))
    textbox.fill(pygame.Color('peachpuff3'))
    pygame.draw.line(textbox, pygame.Color('peachpuff4'), (    0,     0), (w - 1,     0), width=3)
    pygame.draw.line(textbox, pygame.Color('peachpuff4'), (    0,     0), (    0, h - 1), width=3)
    pygame.draw.line(textbox, pygame.Color('papayawhip'), (    0, h - 1), (w - 1, h - 1), width=3)
    pygame.draw.line(textbox, pygame.Color('papayawhip'), (w - 1,     0), (w - 1, h - 1), width=3)
    return textbox

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
    tbr = tb.get_rect()

    tt_list.append(Teletype(pos=box_desc['pos'],
                            text=box_desc['text'],
                            margin=10,
                            ticker_speed=box_desc['tickerspeed'],
                            backdrop=tb,
                            font=pygame.font.SysFont('couriernew', 16),
                            font_color=pygame.Color('black'),
                            sound=sound,
                            random_delay=0.05))


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

        for tt in tt_list:
            tt.update(dt)
            tt.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
