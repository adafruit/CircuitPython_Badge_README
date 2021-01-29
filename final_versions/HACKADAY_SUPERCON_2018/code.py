import board
from adafruit_slideshow import PlayBackOrder, SlideShow
import pwmio

# Create the slideshow object that plays through once alphabetically.
slideshow = SlideShow(board.DISPLAY, pwmio.PWMOut(board.TFT_BACKLIGHT),
					  folder="/images", loop=True,
					  order=PlayBackOrder.ALPHABETICAL, dwell=2.5)

while slideshow.update():
    pass
