#!/usr/bin/env python
#title           :Net_GUI.py
#description     :This script do Ansible job in GUI interface using Netmiko library.
#author          :Rachid
#date            :20220301
#version         :0.1
#usage           :python Net_GUI.py
#notes           :this script needs more improvement to do fully Ansible job
#python_version  :2.7 
#==============================================================================


# Import the modules needed to run the script.
import tkinter as tk
from tkinter.messagebox import showinfo
from datetime import date
import time
import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException  


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        
        
        self.title('My Awesome App')
        self.geometry('500x500')
     
        self.listbox = tk.Listbox(self, height = 10, 
                  width = 15, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "yellow")
        self.listbox.pack()

        
        dev_t = tk.Label(self, text="device type")
        dev_t.pack()
        self.deviceType = tk.Entry(self)
        self.deviceType.pack()

        ip_t = tk.Label(self, text="Device ip")
        ip_t.pack()
        self.host = tk.Entry(self)
        self.host.pack()

        user_t = tk.Label(self, text="Device username")
        user_t.pack()
        self.username = tk.Entry(self)
        self.username.pack()

        self.check_1 = tk.IntVar()
        self.check_conf = tk.Checkbutton(self,text="Go to config Terminal", variable=self.check_1)
        self.check_conf.pack(side="bottom")
         

        pass_t = tk.Label(self, text="Device password")
        pass_t.pack()
        self.password = tk.Entry(self)
        self.password.pack()

        self.cmd_txt = tk.Label(self, text="command")
        self.cmd_txt.pack()
        self.cmd = tk.Entry(self)
        self.cmd.pack()

        # button
        self.button = tk.Button(self, text='Execute command')
        self.button['command'] = self.Excute_clicked
        self.button.pack()

        self.show_btn = tk.Button(self, text='Load devices')
        self.show_btn['command'] = self.Load_Clicked
        self.show_btn.pack()

        self.add_dev = tk.Button(self, text='show data Device')
        self.add_dev['command'] = self.show_dev_data_Clicked
        self.add_dev.pack()


    def Load_Clicked(self):
        with open("devices.yaml", 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            for index, line in enumerate(data_loaded) :
                self.listbox.insert(index,line)

    def show_dev_data_Clicked(self):
        #for i in 
           selected = self.listbox.curselection() 
           res = self.listbox.get(selected)
           stream = open("devices.yaml", 'r') 
           yl = yaml.load(stream,Loader=yaml.FullLoader)
           self.host.delete(0,tk.END)
           self.host.insert(0,yl[res]['ip'])
           self.deviceType.delete(0,tk.END)
           self.deviceType.insert(0,yl[res]['device_type'])
           self.username.delete(0,tk.END)
           self.username.insert(0,yl[res]['username'])
           self.password.delete(0,tk.END)
           self.password.insert(0,yl[res]['password'])

    def Excute_clicked(self):
        res = {
             "device_type": self.deviceType.get(),
             "ip": self.host.get(),
             "username": self.username.get(), 
             "password": self.password.get()
        }
        
        try:
            print('Starting SSH to Device:  ' + res['ip'])
            net_connect = ConnectHandler(**res)
            net_connect.enable()
            if self.check_1.get()==1:
                output = net_connect.send_config_set(self.cmd.get())
            else:   
                output = net_connect.send_command(self.cmd.get())
            showinfo(message=output,title="Info")
            Date = time.strftime('%Y%m%d', time.localtime())

            # Creating a log file to save the output.
            with open("SW_BK_" + res["ip"] + "_V" + str(Date) + ".log", "a", newline="") as saveoutput:
                saveoutput.write(str(output) + "\n\n")

# When SSH time-out, bypass the device and create a doc 'Unreachable_IP_vyyyymmdd.log' to log this IP.
        except NetMikoTimeoutException:
                    print("Device is not reachable: " + res["ip"] + "\n")
                    with open("Unreachable_IP.log", "a", newline="") as unreach:
                        unreach.write(res["ip"] + "\n")

 # When SSH Authentication Failed, bypass the device and create a doc 'Auth_Failed.log_vyyyymmdd' to log this IP.
        except NetMikoAuthenticationException:
                    print("Authentication Failed: " + res["ip"] + "\n")
                    with open("Auth_Failed.log", "a", newline="") as auth_f:
                        auth_f.write(res["ip"] + "\n")
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
