print("options / wifi / main.py executed")


import time
import sys
import network

# Hardware‑specific imports
from machine import Pin
sys.path.append("/sd")

import init
from init import oled, button_up, button_down, button_confirm   # pre‑configured in init.py




#---------------------------
# Execution DEF
#---------------------------

def Deauth_Attack():
    
    pass

def attack_menu():

    def ALL_option():
        print("ALL Works")
        pass

    def Selected_option():
        print("SELECTED Works")
        pass



    #---------------------------
    # Options
    #---------------------------

    menu_items = [
        ("ALL", ALL_option),
        ("Selected", Selected_option),
    ]

    #---------------------------
    # Menu State
    #---------------------------

    current_index = 0
    line_height = 10                       # 8‑pixel font + 2‑pixel spacing
    items_per_page = oled.height // line_height

    last_press = {
        'up': 0,
        'down': 0,
        'confirm': 0
    }

    #---------------------------
    # Helper Functions
    #---------------------------

    def draw_menu():
        oled.fill(0)
        start = (current_index // items_per_page) * items_per_page
        end   = min(start + items_per_page, len(menu_items))

        for row, (label, _) in enumerate(menu_items[start:end]):
            idx = start + row
            text = f"{label} <" if idx == current_index else label
            oled.text(text, 0, row * line_height)
        oled.show()

    def debounce(pin_name: str, ms: int = 200) -> bool:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_press[pin_name]) > ms:
            last_press[pin_name] = now
            return True
        return False

    #---------------------------
    # Main Loop
    #---------------------------

    draw_menu()

    def main():
        nonlocal current_index
        draw_menu()

        while True:
            if not button_up.value() and debounce('up'):
                if current_index > 0:
                    current_index -= 1
                    draw_menu()

            if not button_down.value() and debounce('down'):
                if current_index < len(menu_items) - 1:
                    current_index += 1
                    draw_menu()

            if not button_confirm.value() and debounce('confirm'):
                _, action = menu_items[current_index]
                print(f"Selected index {current_index} - executing action")
                action()
                time.sleep(0.5)

            time.sleep(0.01)

    main()


