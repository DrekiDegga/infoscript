import tkinter as tk
import subprocess
import getmac

def get_system_info():
    # Fetching system info using subprocess
    computer_name = subprocess.check_output('hostname', shell=True).decode().strip()
    model_name = subprocess.check_output('wmic csproduct get name', shell=True).decode().split('\n')[1].strip()
    serial_num = subprocess.check_output('wmic bios get serialnumber', shell=True).decode().split('\n')[1].strip()

    # Fetching MAC addresses using getmac package
    mac_info = []
    mac_addresses = getmac.get_mac_address(interface="all", nics=True)
    for interface in mac_addresses:
        mac_info.append((interface[0], interface[2]))

    return computer_name, model_name, serial_num, mac_info

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)

root = tk.Tk()

# Fetching system info
computer_name, model_name, serial_num, mac_info = get_system_info()

# Displaying fetched info in GUI window
tk.Label(root, text=f"Computer Name: {computer_name}").pack()
tk.Button(root, text="Copy", command=lambda: copy_to_clipboard(computer_name)).pack()

tk.Label(root, text=f"Model Name: {model_name}").pack()
tk.Button(root, text="Copy", command=lambda: copy_to_clipboard(model_name)).pack()

tk.Label(root, text=f"Serial Number / Service Tag: {serial_num}").pack()
tk.Button(root, text="Copy", command=lambda: copy_to_clipboard(serial_num)).pack()

for interface in mac_info:
  tk.Label(root,text=f"{interface[0]} MAC Address: {interface[1]}").pack()
  tk.Button(root,text="Copy",command=lambda i=interface[1]:copy_to_clipboard(i)).pack()

root.mainloop()
