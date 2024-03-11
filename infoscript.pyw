# Section 1: Importing necessary libraries

# socket and wmi are used to get system information like hostname and service tag.
import socket
import wmi

# subprocess is used to execute shell commands, which we will use to get network interface details.
import subprocess

# tkinter and ttk are used for creating the GUI.
from tkinter import *
from tkinter import ttk

# pyperclip is used for copying text to clipboard.
import pyperclip 

# qrcode and pillow are used for generating and displaying QR codes.
import qrcode
from PIL import ImageTk

# Section 2: Functions for fetching system and network information

# The wmi constructor is initialized.
f = wmi.WMI()

# Function to get host name using socket library's gethostname method.
def get_host_name():
    return socket.gethostname()

# Function to get service tag using wmi. It queries Win32_SystemEnclosure class for SerialNumber (which is the service tag).
def get_service_tag():
    for bios in f.Win32_SystemEnclosure():
        return bios.SerialNumber

# Function to categorize network adapter type based on its name. Returns 'Bluetooth', 'Wi-Fi', 'Ethernet' or 'Other'.
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

# Function to get MAC address of each network interface. This uses subprocess module to execute "ipconfig /all" command and parse its output.
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

# Section 3: Functions for copying text to clipboard and generating QR codes

# Function to copy input text to clipboard using pyperclip library.
def copy_to_clipboard(text):
    pyperclip.copy(text)

# Function to generate QR Code using qrcode library. The generated QR code has high error correction level and a white background with black data pixels.
def generate_qr_code(text):
   qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_H,
      box_size=10,
      border=4,
   )
   qr.add_data(text)
   qr.make(fit=True)

   img = qr.make_image(fill='black', back_color='white')
   return ImageTk.PhotoImage(img)

# Section 4: Initializing GUI and setup

# Create a new Tk root widget - this is the main window.
root = Tk()
# Set the size of the window.
root.geometry("600x800")

# Create a tab control with two tabs, one for copy operations and another for QR codes.
tabControl = ttk.Notebook(root) 
copy_tab = Frame(tabControl)
qr_tab = Frame(tabControl)

# Create canvases in each tab where we will place our content. Set their width and height, and background color to white.
canvas1 = Canvas(copy_tab, width=500, height=800, bg='white')
canvas2 = Canvas(qr_tab, width=500, height=800, bg='white')

# Create frames within each canvas where we will place our labels and buttons.
frame1=Frame(canvas1)
frame2=Frame(canvas2)

# Create scrollbars for each tab and link them with corresponding canvases. This allows us to scroll if content exceeds visible area.
scrollbar1=Scrollbar(copy_tab, orient="vertical", command=canvas1.yview)
scrollbar2=Scrollbar(qr_tab, orient="vertical", command=canvas2.yview)

canvas1.configure(yscrollcommand=scrollbar1.set)
canvas2.configure(yscrollcommand=scrollbar2.set)

# Pack scrollbar on right side of each tab and canvas on left side. This makes sure scrollbars are always visible on right side of content.
scrollbar1.pack(side="right", fill="y")
scrollbar2.pack(side="right", fill="y")

canvas1.pack(side="left")
canvas2.pack(side="left")

# Add tabs to the notebook (tab control) with appropriate labels ("Copy" and "QR codes").
tabControl.add(copy_tab, text ='Copy') 
tabControl.add(qr_tab, text ='QR codes')

# Pack the notebook into root widget. With expand set to 1 and fill set to "both", it will expand and shrink with window resizing.
tabControl.pack(expand = 1, fill ="both")

# Section 5: Populating GUI with labels and buttons

# Get host name, service tag and network interface details.
host_name = get_host_name()
service_tag = get_service_tag()
macs_and_interfaces_and_types = get_network_interfaces_and_mac_addresses()

# Create labels and buttons for each network interface and add them to the "Copy" tab frame.
for i, (interface_type, interface_name, mac_addr) in enumerate(macs_and_interfaces_and_types):
    # Create a label with network interface details.
    Label(frame1, text=f"{interface_type}: {interface_name} - MAC Address: {mac_addr if mac_addr else 'N/A'}").grid(row=i*2, column=0)
    # Create a button that copies MAC address to clipboard when clicked.
    Button(frame1, text="Copy", command=lambda mac_addr=mac_addr: copy_to_clipboard(mac_addr if mac_addr else '')).grid(row=i*2+1, column=0)

# For each label/button pair in the "Copy" tab frame, also create a label and QR code image in the "QR codes" tab frame.
for i, (interface_type, interface_name, mac_addr) in enumerate(macs_and_interfaces_and_types):
    # Create a label with network interface details.
    Label(frame2, text=f"{interface_type}: {interface_name} - MAC Address: {mac_addr if mac_addr else 'N/A'}").grid(row=i*2,column=0)
    # Generate QR code from MAC address (if it exists), otherwise from empty string. Then create an image label from this QR code image.
    qr_img_label = Label(frame2)
    qr_img_label.grid(row=i*2+1,column=0)
    qr_img_label.imgtk = generate_qr_code(mac_addr if mac_addr else '')
    qr_img_label.configure(image=qr_img_label.imgtk)

# The main event loop is started by calling the Tkinter widget's mainloop method. 
root.mainloop()
