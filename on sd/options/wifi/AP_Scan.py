
# TO CALL: scan_networks()

print("options / wifi / AP_Scan.py executed")


import time
import sys

# Hardware‑specific imports
from machine import Pin
sys.path.append("/sd")

import init
from init import oled, button_up, button_down, button_confirm
import network




def select_ssid():
    # Read saved networks
    with open("/sd/options/wifi/Recent_Scan.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    networks = []
    for line in lines:
        parts = line.split(',')
        if len(parts) == 3:
            ssid, bssid, channel = parts
            networks.append({'ssid': ssid, 'bssid': bssid, 'channel': channel})

    if not networks:
        oled.fill(0)
        oled.text("No networks", 0, 0)
        oled.show()
        return None

    index = 0
    lines_per_page = 5

    prev_down = 0
    prev_up = 0
    prev_confirm = 0

    while True:
        oled.fill(0)
        oled.text("Select SSID:", 0, 0)

        page = index // lines_per_page
        start = page * lines_per_page
        end = min(start + lines_per_page, len(networks))

        for i, net in enumerate(networks[start:end]):
            actual_idx = start + i
            prefix = ">" if actual_idx == index else " "
            display_name = net['ssid'] if net['ssid'] else "<hidden>"
            oled.text(f"{prefix} {display_name}", 0, 10 + i*10)  # Display SSID or <hidden>



        oled.show()

        curr_down = button_down.value()
        curr_up = button_up.value()
        curr_confirm = button_confirm.value()

        if curr_down == 1 and prev_down == 0:
            index = (index + 1) % len(networks)
        elif curr_up == 1 and prev_up == 0:
            index = (index - 1) % len(networks)
        elif curr_confirm == 1 and prev_confirm == 0:
            return networks[index]

        prev_down = curr_down
        prev_up = curr_up
        prev_confirm = curr_confirm

        time.sleep(0.05)






def scan_networks( duration=20):
    oled.fill(0)
    oled.text("Scanning...", 0, 0)
    oled.text("takes some", 0, 20)
    oled.text("time", 0, 40)
    oled.show()

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    start_time = time.time()
    found_networks = []  # list of dicts

    print("--------- SCANNING NETWORKS ---------")
    while time.time() - start_time < duration:
        try:
            networks = sta_if.scan()
            for net in networks:
                raw_ssid = net[0]
                ssid = raw_ssid.decode('utf-8') if raw_ssid else "<hidden>"
                bssid = ':'.join('{:02x}'.format(b) for b in net[1])
                channel = net[2]

                # Avoid duplicates based on ssid + bssid
                if not any(n['ssid'] == ssid and n['bssid'] == bssid for n in found_networks):
                    found_networks.append({'ssid': ssid, 'bssid': bssid, 'channel': channel})
                    print(f"SSID: {ssid}, BSSID: {bssid}, Channel: {channel}")
        except Exception as e:
            print("Scan failed:", e)
        time.sleep(1)

    print("---------------------------------")

    # Save to file: you can save as CSV or formatted string
    with open("/sd/options/wifi/Recent_Scan.txt", "w") as f:
        for net in found_networks:
            f.write(f"{net['ssid']},{net['bssid']},{net['channel']}\n")


    # Now call selection
    global ssid_saved
    ssid_saved = select_ssid()
    print("Selected network:", ssid_saved)


    with open("/sd/options/wifi/Target/current.txt", "w") as file:
        file.write(f"{ssid_saved['ssid']}|{ssid_saved['bssid']}|{ssid_saved['channel']}\n")


