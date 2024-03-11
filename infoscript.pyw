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
    
    macs_and_interfaces_and_types = []
    
    for line in lines:
        if 'adapter' in line.lower() and ':' in line:
            current_interface = line.split(':')[0].strip()
            current_interface_type = categorize_network_adapter_type(current_interface)  # Categorize network adapter type
            macs_and_interfaces_and_types.append((current_interface_type, current_interface, None))
        elif 'physical address' in line.lower() and macs_and_interfaces_and_types:  # Ensure there's already an entry before assigning a MAC address
            mac_addr = line.split(':')[1].strip().replace('-', ':')  # Replace hyphens with colons
            (interface_type, interface_name, _) = macs_and_interfaces_and_types.pop()
            macs_and_interfaces_and_types.append((interface_type, interface_name, mac_addr))
            
    return macs_and_interfaces_and_types

# Function to copy to clipboard.
def copy_to_clipboard(text):
    pyperclip.copy(text)

# Function to get a command for a button. (New Test edit)
def get_button_command(mac_address):
    return lambda: copy_to_clipboard(mac_address)


root=Tk()
root.geometry("500x800")

canvas = Canvas(root, width=500, height=800, bg='white')

frame=Frame(canvas)
scrollbar=Scrollbar(root, orient="vertical", command=canvas.yview)

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left")
canvas.create_window((0,0), window=frame, anchor='nw')

host_label=Label(frame,text=f"Host Name: {get_host_name()}")
service_label=Label(frame,text=f"Service Tag: {get_service_tag()}")

host_button=Button(frame,text="Copy",command=lambda :copy_to_clipboard(get_host_name()))
service_button=Button(frame,text="Copy",command=lambda :copy_to_clipboard(get_service_tag()))

host_label.pack(pady=10)
host_button.pack(pady=10)

service_label.pack(pady=10)
service_button.pack(pady=10)

mac_addresses_interfaces_types=get_network_interfaces_and_mac_addresses()
for (interface_type, interface_name ,mac_address) in mac_addresses_interfaces_types:

   label_text=f"{interface_type}:\n{interface_name}: {mac_address}"
   
   button_command=lambda mac_address=mac_address :copy_to_clipboard(mac_address)
   
   color = 'green' if interface_type in ['Ethernet', 'Wi-Fi'] else 'black'
   
   label=Label(frame,text=label_text, fg=color)
   button=Button(frame,text="Copy",command=button_command)

   label.pack(pady=5)
   button.pack(pady=5)

frame.update()
canvas.configure(scrollregion=canvas.bbox("all"))

root.mainloop()
