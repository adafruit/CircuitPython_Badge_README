# The MIT License (MIT)
#
# Copyright (c) 2018 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`adafruit_slideshow`
====================================================
CircuitPython helper library for displaying a slideshow of images on a display.

* Author(s): Kattni Rembor, Carter Nelson, Roy Hooper

Implementation Notes
--------------------

**Hardware:**

 * `Adafruit Hallowing M0 Express <https://www.adafruit.com/product/3900>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""
import time
import os
import random
import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Slideshow.git"


class PlayBackOrder:
    """Defines possible slideshow playback orders."""
    # pylint: disable=too-few-public-methods
    ALPHABETICAL = 0
    """Orders by alphabetical sort of filenames"""

    RANDOM = 1
    """Randomly shuffles the images"""
    # pylint: enable=too-few-public-methods


class PlayBackDirection:
    """Defines possible slideshow playback directions."""
    # pylint: disable=too-few-public-methods
    BACKWARD = -1
    """The next image is before the current image. When alphabetically sorted, this is towards A."""

    FORWARD = 1
    """The next image is after the current image. When alphabetically sorted, this is towards Z."""
    # pylint: enable=too-few-public-methods


class SlideShow:
    # pylint: disable=too-many-instance-attributes
    """
    Class for displaying a slideshow of .bmp images on displays.

    :param str folder: Specify the folder containing the image files, in quotes. Default is
                       the root directory, ``"/"``.

    :param PlayBackOrder order: The order in which the images display. You can choose random
                                (``RANDOM``) or alphabetical (``ALPHABETICAL``). Default is
                                ``ALPHABETICAL``.

    :param bool loop: Specify whether to loop the images or play through the list once. `True`
                 if slideshow will continue to loop, ``False`` if it will play only once.
                 Default is ``True``.

    :param int dwell: The number of seconds each image displays, in seconds. Default is 3.

    :param bool fade_effect: Specify whether to include the fade effect between images. ``True``
                        tells the code to fade the backlight up and down between image display
                        transitions. ``False`` maintains max brightness on the backlight between
                        image transitions. Default is ``True``.

    :param bool auto_advance: Specify whether to automatically advance after dwell seconds. ``True``
                 if slideshow should auto play, ``False`` if you want to control advancement
                 manually.  Default is ``True``.

    :param PlayBackDirection direction: The playback direction.

    Example code for Hallowing Express. With this example, the slideshow will play through once
    in alphabetical order:

    .. code-block:: python

        from adafruit_slideshow import PlayBackOrder, SlideShow
        import board
        import pulseio

        slideshow = SlideShow(board.DISPLAY, pulseio.PWMOut(board.TFT_BACKLIGHT), folder="/",
                              loop=False, order=PlayBackOrder.ALPHABETICAL)

        while slideshow.update():
            pass

    Example code for Hallowing Express. Sets ``dwell`` to 0 seconds, turns ``auto_advance`` off,
    and uses capacitive touch to advance backwards and forwards through the images and to control
    the brightness level of the backlight:

    .. code-block:: python

        from adafruit_slideshow import PlayBackOrder, SlideShow, PlayBackDirection
        import touchio
        import board
        import pulseio

        forward_button = touchio.TouchIn(board.TOUCH4)
        back_button = touchio.TouchIn(board.TOUCH1)

        brightness_up = touchio.TouchIn(board.TOUCH3)
        brightness_down = touchio.TouchIn(board.TOUCH2)

        slideshow = SlideShow(board.DISPLAY, pulseio.PWMOut(board.TFT_BACKLIGHT), folder="/",
                              auto_advance=False, dwell=0)

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
    """

    def __init__(self, display, backlight_pwm, *, folder="/", order=PlayBackOrder.ALPHABETICAL,
                 loop=True, dwell=3, fade_effect=True, auto_advance=True,
                 direction=PlayBackDirection.FORWARD):
        self.loop = loop
        """Specifies whether to loop through the images continuously or play through the list once.
        ``True`` will continue to loop, ``False`` will play only once."""

        self.dwell = dwell
        """The number of seconds each image displays, in seconds."""

        self.direction = direction
        """Specify the playback direction.  Default is ``PlayBackDirection.FORWARD``.  Can also be
        ``PlayBackDirection.BACKWARD``."""

        self.auto_advance = auto_advance
        """Enable auto-advance based on dwell time.  Set to ``False`` to manually control."""

        self.fade_effect = fade_effect
        """Whether to include the fade effect between images. ``True`` tells the code to fade the
           backlight up and down between image display transitions. ``False`` maintains max
           brightness on the backlight between image transitions."""

        # Load the image names before setting order so they can be reordered.
        self._img_start = None
        self._file_list = [folder+"/"+f for f in os.listdir(folder) if (f.endswith(".bmp") and not f.startswith("._"))]
        self._order = None
        self.order = order
        """The order in which the images display. You can choose random (``RANDOM``) or
           alphabetical (``ALPHA``)."""

        self._current_image = -1
        self._image_file = None
        self._brightness = 0.5

        # Setup the display
        self._group = displayio.Group()
        self._display = display
        display.show(self._group)

        self._backlight_pwm = backlight_pwm

        # Show the first image
        self.advance()

    @property
    def current_image_name(self):
        """Returns the current image name."""
        return self._file_list[self._current_image]

    @property
    def order(self):
        """Specifies the order in which the images are displayed. Options are random (``RANDOM``) or
        alphabetical (``ALPHABETICAL``). Default is ``RANDOM``."""
        return self._order

    @order.setter
    def order(self, order):
        if order not in [PlayBackOrder.ALPHABETICAL, PlayBackOrder.RANDOM]:
            raise ValueError("Order must be either 'RANDOM' or 'ALPHABETICAL'")

        self._order = order
        self._reorder_images()

    def _reorder_images(self):
        if self.order == PlayBackOrder.ALPHABETICAL:
            self._file_list = sorted(self._file_list)
        elif self.order == PlayBackOrder.RANDOM:
            self._file_list = sorted(self._file_list, key=lambda x: random.random())

    def _set_backlight(self, brightness):
        full_brightness = 2 ** 16 - 1
        self._backlight_pwm.duty_cycle = int(full_brightness * brightness)

    @property
    def brightness(self):
        """Brightness of the backlight when an image is displaying. Clamps to 0 to 1.0"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        if brightness < 0:
            brightness = 0
        elif brightness > 1.0:
            brightness = 1.0
        self._brightness = brightness
        self._set_backlight(brightness)

    def _fade_up(self):
        if not self.fade_effect:
            self._set_backlight(self.brightness)
            return
        steps = 100
        for i in range(steps):
            self._set_backlight(self.brightness * i / steps)
            time.sleep(0.01)

    def _fade_down(self):
        if not self.fade_effect:
            self._set_backlight(self.brightness)
            return
        steps = 100
        for i in range(steps, -1, -1):
            self._set_backlight(self.brightness * i / steps)
            time.sleep(0.01)

    def update(self):
        """Updates the slideshow to the next image."""
        now = time.monotonic()
        if not self.auto_advance or now - self._img_start < self.dwell:
            return True

        return self.advance()

    def advance(self):
        """Displays the next image. Returns True when a new image was displayed, False otherwise.
        """
        if self._image_file:
            self._fade_down()
            self._group.pop()
            self._image_file.close()
            self._image_file = None

        self._current_image += self.direction

        # Try and load an OnDiskBitmap until a valid file is found or we run out of options. This
        # loop stops because we either set odb or reduce the length of _file_list.
        odb = None
        while not odb and self._file_list:
            if 0 <= self._current_image < len(self._file_list):
                pass
            elif not self.loop:
                return False
            else:
                image_count = len(self._file_list)
                if self._current_image < 0:
                    self._current_image += image_count
                elif self._current_image >= image_count:
                    self._current_image -= image_count
                self._reorder_images()

            image_name = self._file_list[self._current_image]
            self._image_file = open(image_name, "rb")
            try:
                odb = displayio.OnDiskBitmap(self._image_file)
            except ValueError:
                self._image_file.close()
                self._image_file = None
                del self._file_list[self._current_image]

        if not odb:
            raise RuntimeError("No valid images")

        sprite = displayio.Sprite(odb, pixel_shader=displayio.ColorConverter(), position=(0, 0))
        self._group.append(sprite)
        self._display.wait_for_frame()

        self._fade_up()
        self._img_start = time.monotonic()

        return True
