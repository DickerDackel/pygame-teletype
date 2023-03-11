# pygame-teletype

A textbox with a teletype text effect as in old adventure games.

![Screen recording of demo](https://github.com/DickerDackel/pygame-teletype/blob/main/demo.gif)

## Installation

**Never do this without a virtual env!**

    pip install git+https://github.com/dickerdackel/pygame-teletype

## Usage

### Teletype()

    tt = Teletype(pos=screen.get_rect().center,
		  text='Lorem ipsum dolor',
		  margin=10,
		  ticker_speed=0.05,
		  font=pygame.font.SysFont('couriernew', 16),
		  font_color=pygame.Color('black'),
		  sound=pygame.mixer.Sound('beep.wav'),
		  random_delay=0,
		  pause_after_sentence=True)

    ...

    tt.update(dt)
    tt.draw(screen)

Parameters:

	pos: Vector2 - *center* position of the text box
	backdrop: pygame.Surface - background to draw the text on.
	text: the text to teletype
	margin: int - margin around the text within the text box
	ticket_speed: float - delay in seconds between letters
	backdrop: pygame.Surface - optional.  e.g. a paper texture
	font: pygame.font.SysFont - Falls back to couriernew, 16pt
	font_color: pygame.Color - defaults to white
        random_delay: float = 0: randomly add pauses, faking transmission delays
        pause_after_sentence: bool = True - Make a longer pause after ./!/?/;

The rect of the background also gives the size of the box.  If you don't need a background, just pass a transparent surface.

The process shouldn't be too resource intensive, since every letter is blitted onto a surface that's kept in the class.  Line breaks as well as scrolling are implemented.

Run and look into eleprinter-demo for an example.

### Cooldown()

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

The delta_time that's usually calculated at the beginning of a pygame main loop will be used as a factor while counting down.

See Teletype code for how it is used.


## How it's done

The class works on 3 surfaces.  

1st backdrop.  You hand the main surface, e.g. a paper texture, with proper
dimensions to the constructor.

The class itself has a main surface the same size as the backdrop.

Additionally, there's the text canvas.  This is filled letter by letter after each cooldown delay.

Then first the backdrop is blitted onto the main surface, followed by the text canvas.

## TODO

Proper word wrapping and text justification would be nice.  Right now, words
simply break in the middle, when the border is reached.  But this requires a
form of lookahead and this was implemented in about 2 hours, with 2 more for
documentation and making a github project.


## Licensing stuff

This lib is under the MIT license.

Beep sound, used in demo from https://opengameart.org/content/beep-tone-sound-sfx
It's CC0, but still
