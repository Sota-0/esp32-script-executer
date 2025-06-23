print("options / wifi / main.py executed")


import time
import sys

# Hardware‑specific imports
from machine import Pin
sys.path.append("/sd")

import init
from init import oled, button_up, button_down, button_confirm   # pre‑configured in init.py




#---------------------------
# Execution DEF
#---------------------------



def AP_Scan():
    sys.path.append("/sd/options/wifi/")
    from AP_Scan import scan_networks
    scan_networks()
    main()

def handshake():
    print("Action Two Executed")

def deauth():
    sys.path.append("/sd/options/wifi/")
    from Deauth import attack_menu
    attack_menu()
    main()

def action_four():
    print("Action Four Executed")

def action_five():
    print("Action Five Executed")

#---------------------------
# Options
#---------------------------

menu_items = [
    ("AP Scan", AP_Scan),
    ("Handshake", handshake),
    ("Deauth", deauth),
    ("Option 4", action_four),
    ("Option 5", action_five),
]

#---------------------------
# Menu State
#---------------------------

current_index   = 0
line_height     = 10                       # 8‑pixel font + 2‑pixel spacing
items_per_page  = oled.height // line_height

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
    global current_index
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

if __name__ == "__main__":
    main()
