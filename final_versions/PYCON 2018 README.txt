Welcome to CircuitPython!
#############################

Hello PyCon 2018 - we wanted to have a fun ~electronic~ swag-bag item, that
does more than just a sticker! What you have in your hand is a special 
edition Adafruit Gemma M0 with a super cool Python logo on the back.
This hardware is identical in functionality to the 'regular' Gemma M0, it's
just got a swanky custom look.

This hardware comes pre-loaded with CircuitPython! CircuitPython is Adafruit's
branch of MicroPython designed to simplify experimentation and education on 
low-cost microcontrollers. It makes it easier than ever to get prototyping 
by requiring no upfront desktop software downloads.

With CircuitPython you can write clean and simple Python 3 code to control 
hardware instead of having to use complex low-level languages like C or C++ 
(what Arduino uses for programming). It's great for beginners and is powerful
for experts.

The Gemma M0 does a lot on its own, but it will also work with just about 
every kind of sensor, LED/NeoPixel, robotic parts and more. If you need some 
fun electronics to go with your Gemma check out the Adafruit shop.

Enjoy PyCon 2018 and keep an eye out for CircuitPython open spaces and join 
us on the first day of sprints!

Thanks!
  - the Adafruit team

#############################

Visit the Gemma M0 product page here for more info: 
    https://adafruit.com/product/3501

To get started with CircuitPython, which comes built into your Gemma, visit:
    https://learn.adafruit.com/welcome-to-circuitpython

#############################

The Gemma has a very tiny disk drive so we have disabled Mac OS X indexing
which could take up that valuable space. 

So *please* do not remove the empty .fseventsd/no_log, .metadata_never_index 
or .Trashes files!

#############################

The pre-loaded demo shows off what your Gemma M0 can do with CircuitPython:
  * The built in DotStar LED can show any color, it will swirl through the 
    rainbow
  * Pin A0 is a true analog output, you will see the voltage slowly rise
  * Pin A1 is an analog input, the REPL will display the voltage on this pin 
    (0-3.3V is the max range)
  * Pin A2 is a capacitive input, when touched, it will turn on the red LED. 
    If you update main.py to uncomment the relevant lines, it will act as a 
    mini keyboard and emulate an 'a' key-press whenever A2 is touched.

For more details on how to use CircuitPython, visit 
https://adafruit.com/product/3501
and check out all the tutorials we have!

#############################
CircuitPython Quick Start:

Changing the code is as easy as editing main.py in your favorite text editor. 

Our recommended editor is Mu, which is great for simple projects, and comes
with a built in REPL serial viewer! It is available for Mac, Windows & Linux
https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor

After the file is saved, CircuitPython will automatically reload the latest 
code. Try enabling the capacitive keyboard 
(HINT: look for the "# optional! uncomment below..." text)

Connecting to the serial port will give you access to sensor information, 
better error messages and an interactive CircuitPython (known as the REPL). 
On Windows we recommend Mu, Tera Term or PuTTY. 
On Mac OSX and Linux, use Mu or 'screen' can be used from a terminal.