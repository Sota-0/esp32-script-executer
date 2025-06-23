from machine import Pin, SPI
import sys

sys.path.append("/sd/lib/")
import sh1106


# ---------------------------------------------------------------
# Initialize OLED Display (SH1106)
# ---------------------------------------------------------------

spi = SPI(1, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23))
dc = Pin(21)
res = Pin(19)
cs = Pin(22)

oled = sh1106.SH1106_SPI(128, 64, spi, dc, res, cs)




# ---------------------------------------------------------------
# Initialize Buttons
# ---------------------------------------------------------------

button_up = Pin(27, Pin.IN, Pin.PULL_UP)
button_confirm = Pin(25, Pin.IN, Pin.PULL_UP)
button_down = Pin(26, Pin.IN, Pin.PULL_UP)











