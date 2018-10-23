import board
from adafruit_slideshow import PlayBackOrder, SlideShow
import pulseio

# Create the slideshow object that plays through once alphabetically.
slideshow = SlideShow(board.DISPLAY, pulseio.PWMOut(board.TFT_BACKLIGHT),
					  folder="/images", loop=True,
					  order=PlayBackOrder.ALPHABETICAL, dwell=2.5)

while slideshow.update():
    pass
