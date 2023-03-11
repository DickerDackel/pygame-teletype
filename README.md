# pygame-teleprinter

## Usage
A textbox with a teleprinter text effect as in old adventure games

![alt text for screen reaScreen recording of demoders](/path/to/image.png "Text to show on mouseover").
![Screen recording of demo](https://github.com/DickerDackel/pygame-teleprinter/blob/main/demo.gif)

    tt = Teleprinter(pos=screen.get_rect().center,
		     text='Lorem ipsum dolor',
		     margin=10,
		     ticker_speed=0.05,
		     font=pygame.font.SysFont('couriernew', 16),
		     font_color=pygame.Color('black'),
		     sound=pygame.mixer.Sound('beep.wav'))

    ...

    tt.update(dt)
    tt.draw(screen)

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

Additionally, a short but usefull class for cooldown events has been added.

    clock = pygame.time.Clock()
    delay = Cooldown(5)

    ...

    dt = clock.get_time() / 1000.0
    delay(delta_time)
    if delay.cold:
	# do stuff
	# Reset the timer to wait again
	delay.reset()

Parameters:

	temp: float - "temperature" in seconds to cool down from 

    The delta_time that's usually calculated at the beginning of a pygame main
    loop will be used as a factor while counting down.

    See Teleprinter code for how it is used.


## Licensing stuff

    Beep sound, used in demo from https://opengameart.org/content/beep-tone-sound-sfx
    It's CC0, but still

