import socket
import wmi
import subprocess
from tkinter import *
from tkinter import messagebox
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

# Function to get MAC address.
def get_network_interfaces_and_mac_addresses():
    output = subprocess.check_output("ipconfig /all", universal_newlines=True)
    lines = output.split('\n')
    
    macs_and_interfaces = []
    current_interface = ''
    
    for line in lines:
        if 'adapter' in line.lower() and ':' in line:
            current_interface = line.split(':')[0].strip()
        elif 'physical address' in line.lower():
            mac_addr = line.split(':')[1].strip()
            macs_and_interfaces.append((current_interface, mac_addr))
            
    return macs_and_interfaces

# Function to copy to clipboard.
def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Copied", "Copied to clipboard!")

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

mac_addresses = get_network_interfaces_and_mac_addresses()
for (interface_name, mac_address) in mac_addresses:
    label_text = f"{interface_name} (MAC Address): {mac_address}"
    
    # Only copy the MAC address when button is clicked
    label_button_command=lambda x=mac_address:copy_to_clipboard(x)
    
    label = Label(root, text=label_text)
    button = Button(root, text="Copy", command=label_button_command)

    label.pack(pady=5)
    button.pack(pady=5)

root.mainloop()
