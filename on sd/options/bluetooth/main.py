print("options / bluetooth / main.py executed")

scripts
import time
import sys

# Hardware-specific imports (adjust as needed)
from machine import Pin
sys.path.append("/sd")
import init
from init import oled, button_up, button_down, button_confirm
