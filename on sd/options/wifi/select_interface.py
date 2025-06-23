# TO CALL: select_network_interface()

print("options / wifi / select_interface.py executed")

import time
import sys
from machine import Pin

sys.path.append("/sd")
import init
from init import oled, button_up, button_down, button_confirm
import network




def select_network_interface():



    def get_all_network_interfaces():
        interfaces = []
        for iface_name in dir(network):
            if iface_name.endswith('_IF') and iface_name.isupper():
                try:
                    iface_const = getattr(network, iface_name)
                    wlan = network.WLAN(iface_const)
                    interfaces.append((iface_name, iface_const))
                except Exception:
                    pass
        return interfaces

    def display_menu(interfaces, selected_index):
        oled.fill(0)
        oled.text("Select interface:", 0, 0)

        max_lines = 3  # Adjust for OLED size
        start = max(0, selected_index - max_lines + 1)
        end = min(len(interfaces), start + max_lines)

        for i in range(start, end):
            name, _ = interfaces[i]
            prefix = ">" if i == selected_index else " "
            oled.text(f"{prefix} {name}", 0, 10 + (i - start) * 10)

        oled.show()

    def wait_for_release(pin):
        while not pin.value():
            time.sleep(0.01)

    interfaces = get_all_network_interfaces()
    if not interfaces:
        oled.fill(0)
        oled.text("No interfaces found", 0, 0)
        oled.show()
        time.sleep(2)
        return None

    selected_index = 0
    display_menu(interfaces, selected_index)

    while True:
        if not button_up.value():
            selected_index = (selected_index - 1) % len(interfaces)
            display_menu(interfaces, selected_index)
            wait_for_release(button_up)
            time.sleep(0.1)

        if not button_down.value():
            selected_index = (selected_index + 1) % len(interfaces)
            display_menu(interfaces, selected_index)
            wait_for_release(button_down)
            time.sleep(0.1)

        if not button_confirm.value():
            _, selected_const = interfaces[selected_index]
            wait_for_release(button_confirm)
            oled.fill(0)
            oled.text("Selected:", 0, 0)
            oled.text(interfaces[selected_index][0], 0, 10)
            oled.show()

            time.sleep(1)
            from main import main
            main()
        
