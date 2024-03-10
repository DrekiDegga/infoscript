import os
import socket
import uuid
import wmi
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
def get_mac_address():
    mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                         for i in range(0, 8*6, 8)][::-1])
    return mac_addr

# Function to copy to clipboard.
def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Copied", "Copied to clipboard!")

root = Tk()
root.geometry("500x500")

host_label = Label(root, text=f"Host Name: {get_host_name()}")
service_label = Label(root, text=f"Service Tag: {get_service_tag()}")
mac_label = Label(root, text=f"MAC Address: {get_mac_address()}")

host_button = Button(root, text="Copy", command=lambda: copy_to_clipboard(get_host_name()))
service_button = Button(root, text="Copy", command=lambda: copy_to_clipboard(get_service_tag()))
mac_button = Button(root, text="Copy", command=lambda: copy_to_clipboard(get_mac_address()))

host_label.pack(pady=10)
host_button.pack(pady=10)

service_label.pack(pady=10)
service_button.pack(pady=10)

mac_label.pack(pady=10)
mac_button.pack(pady=10)

root.mainloop()
