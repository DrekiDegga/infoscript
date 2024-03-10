import socket
import wmi
import subprocess
from tkinter import *
import pyperclip

# Initialize the wmi constructor.
f = wmi.WMI()

# Function to get host name.
def get_host_name():
    return socket.gethostname()

# Function to get service tag.
def get_service_tag():
    for bios in f.Win32_SystemEnclosure():
        return bios.SerialNumber

# Function to categorize network adapter type.
def categorize_network_adapter_type(interface_name):
    interface_name_lower = interface_name.lower()
    if 'bluetooth' in interface_name_lower:
        return 'Bluetooth'
    elif 'wi-fi' in interface_name_lower or 'wifi' in interface_name_lower:
        return 'Wi-Fi'
    elif 'ethernet' in interface_name_lower:
        return 'Ethernet'
    else:
        return 'Other'

# Function to get MAC address.
def get_network_interfaces_and_mac_addresses():
    output = subprocess.check_output("ipconfig /all", universal_newlines=True)
    lines = output.split('\n')
    
    macs_and_types = []
    
    for line in lines:
        if 'adapter' in line.lower() and ':' in line:
            current_interface_type = categorize_network_adapter_type(line)  # Categorize network adapter type based on entire line text
        elif 'physical address' in line.lower():
            mac_addr = line.split(':')[1].strip().replace('-', ':')  # Replace hyphens with colons
            macs_and_types.append((current_interface_type, mac_addr))
            
    return macs_and_types

# Function to copy to clipboard.
def copy_to_clipboard(text):
    pyperclip.copy(text)

# Function to get a command for a button.
def get_button_command(mac_address):
    return lambda: copy_to_clipboard(mac_address)

root = Tk()
root.geometry("500x500")

host_label = Label(root, text=f"Host Name: {get_host_name()}")
service_label = Label(root, text=f"Service Tag: {get_service_tag()}")

host_button = Button(root, text="Copy", command=lambda: copy_to_clipboard(get_host_name()))
service_button = Button(root, text="Copy", command=lambda: copy_to_clipboard(get_service_tag()))

host_label.pack(pady=10)
host_button.pack(pady=10)

service_label.pack(pady=10)
service_button.pack(pady=10)

mac_addresses_and_types = get_network_interfaces_and_mac_addresses()
for (interface_type, mac_address) in mac_addresses_and_types:
    
   label_text = f"{interface_type}: {mac_address}"
    
   # Only copy the MAC address when button is clicked
   button_command=get_button_command(mac_address)
   
   label=Label(root, text=label_text)
   button=Button(root, text="Copy", command=button_command)

   label.pack(pady=5)
   button.pack(pady=5)

root.mainloop()
