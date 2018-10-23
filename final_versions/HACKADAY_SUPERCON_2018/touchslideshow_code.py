import board
from adafruit_slideshow import SlideShow, PlayBackDirection, PlayBackOrder
import touchio
import pulseio

forward_button = touchio.TouchIn(board.TOUCH4)
back_button = touchio.TouchIn(board.TOUCH1)

brightness_up = touchio.TouchIn(board.TOUCH3)
brightness_down = touchio.TouchIn(board.TOUCH2)

slideshow = SlideShow(board.DISPLAY, pulseio.PWMOut(board.TFT_BACKLIGHT),
		      folder="/images", auto_advance=False,
		      order=PlayBackOrder.ALPHABETICAL, dwell=0)

while True:
    if forward_button.value:
        slideshow.direction = PlayBackDirection.FORWARD
        slideshow.advance()
    if back_button.value:
        slideshow.direction = PlayBackDirection.BACKWARD
        slideshow.advance()

    if brightness_up.value:
        slideshow.brightness += 0.001
    elif brightness_down.value:
        slideshow.brightness -= 0.001
