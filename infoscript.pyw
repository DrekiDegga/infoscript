import os
import subprocess
import re
from tkinter import *
import pyperclip

def get_system_info():
    # Computer name
    computer_name = os.environ['COMPUTERNAME']

    # Manufacturer 
    manufacturer = subprocess.check_output('wmic csproduct get vendor', shell=True).decode().split('\n')[1].strip()

    # Serial number or Service tag in case of Dell machines
    if manufacturer.lower() == "dell inc.":
        service_tag = subprocess.check_output('wmic bios get servicetag', shell=True).decode().split('\n')[1].strip()
        unique_id = f"Dell Service Tag: {service_tag}"
    else:
        serial_number = subprocess.check_output('wmic bios get serialnumber', shell=True).decode().split('\n')[1].strip()
        unique_id = f"Serial Number: {serial_number}"

    # Network interfaces info using getmac command
    network_info = subprocess.check_output('getmac /V /FO list', shell=True).decode()
    
    return (computer_name, unique_id, network_info)

def copy_to_clipboard(text):
   pyperclip.copy(text)

def display_info(info):
    root = Tk()
    
    Label(root, text="Computer Name: ").pack(side=LEFT)
    Label(root, text=info[0]).pack(side=LEFT)
    Button(root, text="Copy", command=lambda: copy_to_clipboard(info[0])).pack(side=LEFT)
    
     Label(root, text=info[1].split(':')[0] + ': ').pack(side=LEFT)
     Label(root, text=info[1].split(':')[1]).pack(side=LEFT)
     Button(root, text="Copy", command=lambda: copy_to_clipboard(info[1].split(':')[1])).pack(side=LEFT)

     net_info_lines = info[2].split("\n")
     mac_addresses = []
     
     for i in range(len(net_info_lines)):
         if "Physical Address:" in net_info_lines[i]:
             mac_address = re.findall("..-..-..-..-..-..", net_info_lines[i])[0]
             connection_name = re.findall(":.+", net_info_lines[i-2])[0][2:]
             transport_type = re.findall(":.+", net_info_lines[i+2])[0][2:]

             if 'Wi-Fi' in connection_name or 'Wireless' in connection_name:
                 device_type = "WiFi"
             elif 'Ethernet' in connection_name:
                 device_type = "Ethernet"
             else:
                 device_type ="Unknown"
                 
             mac_addresses.append(mac_address)
             
             Label(root, text=f"Network Device: {device_type}").pack()
             Label(root, text=f"Connection Name: {connection_name}").pack()
             
              Frame_mac=root.Frame()
              Frame_mac.pack()
              
              Label(Frame_mac, text=f"MAC Address: ").pack(side=LEFT)
              Label(Frame_mac, text=mac_address).pack(side=LEFT)
              Button(Frame_mac, text="Copy", command=lambda: copy_to_clipboard(mac_address)).pack(side=LEFT)

     Button(root, text="Copy All MAC Addresses", command=lambda: copy_to_clipboard('\n'.join(mac_addresses))).pack()
     
     root.mainloop()

if __name__ == "__main__":
   info = get_system_info()
   display_info(info)
