print("Main.py Executed")

import time
import sys

# Hardware-specific imports (adjust as needed)
from machine import Pin
sys.path.append("/sd")
import init
from init import oled, button_up, button_down, button_confirm




#---------------------------
# option add / edit
#---------------------------


options = [1, 2, 3]

option_names = {
    1: 'scripts',
    2: 'wifi',
    3: 'bluetooth',

}

def scripts_run():
    with open("sd/options/scripts/main.py") as f:
        code = f.read()
    exec(code)

def wifi_run():
    with open("sd/options/wifi/main.py") as f:
        code = f.read()
    exec(code)

def bluetooth_run():
    with open("sd/options/bluetooth/main.py") as f:
        code = f.read()
    exec(code)


option_functions = {
    1: scripts_run,
    2: wifi_run,
    3: bluetooth_run,

}

#---------------------------
# menu
#---------------------------



current_index = 1 # start at option 2

def wrap_index(index, length):
    return (index + length) % length

def update_display():
    num_options = len(options)

    first_option = options[wrap_index(current_index - 1, num_options)]
    curr_option = options[current_index]
    third_option = options[wrap_index(current_index + 1, num_options)]

    oled.fill(0)
    oled.text("   " + option_names[first_option], 5, 20)
    oled.text("> " + option_names[curr_option] + "", 10, 30)  # highlight current
    oled.text("   " + option_names[third_option], 5, 40)
    oled.show()


#---------------------------
# file exec
#---------------------------




def check_buttons():
    global current_index

    if button_down.value() == 0:
        current_index = wrap_index(current_index + 1, len(options))
        update_display()
        time.sleep(0.2)  

    elif button_up.value() == 0:
        current_index = wrap_index(current_index - 1, len(options))
        update_display()
        time.sleep(0.2) 

    elif button_confirm.value() == 0:
        selected_option = options[current_index]
        time.sleep(0.2)
        option_functions[selected_option]()  # call function
        update_display()  

# Initial display
update_display()

#---------------------------
# START
#---------------------------


while True:
    check_buttons()
    time.sleep(0.1)
