import socket
import wmi
from tkinter import Tk, Label, Button, Frame, X, LEFT
import pyperclip

def get_system_info():
    info = {}

    # Get computer name
    info['Computer Name'] = socket.gethostname()

    # Get serial number/service tag and Model 
    c = wmi.WMI()
    
    try:
        for bios in c.Win32_BIOS():
            info['Serial Number'] = bios.SerialNumber  # On Dell machines this will be the service tag
        
        for system in c.Win32_ComputerSystem():
            info['Model'] = system.Model

    except Exception as e:
        info['Serial Number'] = "Error: " + str(e)

    # Get MAC address and Network Adapter Type 
    net_info_list=[]
    
    for interface in c.Win32_NetworkAdapter():
        if interface.MACAddress is not None:
            net_info_list.append((interface.NetConnectionID,':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1]),interface.AdapterType))
    
    info['Network Information']=net_info_list

    return info

def copy_to_clipboard(root,text):
   root.clipboard_clear()
   root.clipboard_append(text)

def create_gui(info):
   root=Tk()
   
   for key in ['Computer Name','Serial Number', 'Model']:
       row_frame=Frame(root)
       row_frame.pack(fill=X)
       
       label_key=Label(row_frame,text=key+": ")
       label_key.pack(side=LEFT)

       label_value=Label(row_frame,text=info[key])
       label_value.pack(side=LEFT)

       copy_button=Button(row_frame,text="Copy",command=lambda text=info[key]:copy_to_clipboard(root,text))
       copy_button.pack(side=LEFT)
   
   network_frame=Frame(root)
   network_frame.pack(fill=X)

   network_label_key=Label(network_frame,text='Network Information: ')
   network_label_key.pack()

   for adapter in info["Network Information"]:
      adapter_frame=Frame(network_frame)
      adapter_frame.pack(fill=X)

      adapter_name_label=Label(adapter_frame,text=str(adapter[0])+": ")
      adapter_name_label.pack(side=LEFT)
      
      mac_address_label_value=Label(adapter_frame,text=str(adapter[1]))
      mac_address_label_value.pack(side=LEFT)

      copy_button_network_adapter_mac_addresss_value_only_Button(adapter_frame,text="Copy",command=lambda text=str(adapter[1]):copy_to_clipboard(root,text))
      copy_button_network_adapter_mac_addresss_value_only_Button(packside_LEFT)
       
      type_of_adapter_label_Value_Labelnetwork_frametextstradapter2type_of_adapter_label_Value_LabelpacksideLEFT
   
   
root.mainloop()

if __name__ == "__main__":
   system_info=get_system_info()
   
create_gui(system_info)
