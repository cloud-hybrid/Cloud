import os
import sys
import subprocess
import textwrap
import argparse
import time

from tkinter import *

from argparse import ArgumentParser
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
from subprocess import *

from Payload.Vault.Installation.Progress import Progress
from Payload.Vault.Installation.Preseed import Preseed
from Payload.Vault.Installation.Installer import Installer
from Payload.Vault.Shell.Terminal import Terminal
from Payload.Vault.Shell.Display import Display
from Payload.Vault.Shell.CMD import CMD
from Payload.Vault.Network.Host import Host
from Payload.Vault.Network.VPS import VPS
from Payload.Vault.Network.Gateway import Gateway
from Payload.Vault.Network.Proxy import Proxy
# from Payload.Vault.Database.Connection import Connection

vDIRECTORY = "/mnt/Virtual-Machines/"

def resource_path(relative_path):
  base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
  return os.path.join(base_path, relative_path)

def main():
  source = resource_path("Bionic-Server.iso")

  v_Host = Host(input.h_User, input.h_IP, input.h_OS, input.eMail)
  v_VPS = VPS(input.v_User, input.v_Password, input.v_IP, input.v_Type, input.v_RAM, input.v_CPU, input.Domain, input.SSL)
  v_VPS.hostname = v_VPS.name 
  v_Gateway = Gateway(input.g_User, input.g_IP)
  v_Proxy = Proxy(input.p_User, input.p_IP)
  v_Preseed = Preseed(v_VPS.user, v_VPS.password, v_VPS.IP, Preseed.HOSTNAME)
  Preseed.HOSTNAME = v_VPS.hostname
  sys.stdout.write(f"{Preseed.HOSTNAME}".center(os.get_terminal_size().columns))

  v_Installer = Installer(source, v_VPS.RAM, v_VPS.CPUs)
  v_Installer.install(v_VPS.type, v_VPS.user, v_VPS.password, v_VPS.IP)

  CMD().execute(f"""ssh snow@192.168.0.1 -t "sudo {vDIRECTORY}create-VPS.sh" """)

  Progress(750).display()

  if v_Host.OS == "linux":
    v_VPS.start(v_VPS.hostname)

  v_Gateway.updateDNS(v_VPS)
  v_Gateway.createUser(v_VPS)

  v_Proxy.updateProxy(v_VPS)

  if v_VPS.type == "Wordpress":
    v_Installer.install_wordpress_database(v_VPS.password, v_VPS.IP)

  if v_VPS.FQDN != "N/A" and v_VPS.FQDN != None:
    command = f"""ssh {v_Proxy.user}@{v_Proxy.IP} "sudo wget -O /tmp/add-domain.py 'https://unixvault.com/proxy/add-domain.py' --no-check-certificate && sudo chmod +x /tmp/add-domain.py && sudo /tmp/add-domain.py {v_VPS.hostname} {v_VPS.FQDN}" """
    Terminal(command).run()
  
  v_Host.email_private_key_windows(v_Host)

  sys.stdout.write("Payload(s) Delivered".center(os.get_terminal_size().columns))


class GUI(Frame):
  def __init__(self):
    super().__init__()

    self.master.title("Vault Development")
    self.pack(fill = BOTH, expand = True)

    self.columnconfigure(1, weight = 1)
    self.columnconfigure(2, pad = 1)
    
    self.user_label = Label(self, text = "VPS Username")
    self.user_label.grid(row = 0, column = 0, pady = 5, padx = 5)
    self.user_entry = Entry(self, justify = "center")
    self.user_entry.grid(row = 1, column = 0, pady = 5, padx = 5)

    self.password_label = Label(self, text = "VPS Password")
    self.password_label.grid(row = 0, column = 1, pady = 5, padx = 5)
    self.password_entry = Entry(self, show = "*", justify = "center")
    self.password_entry.grid(row = 1, column = 1, pady = 5, padx = 5)
    self.password_entry.insert(0, "Knowledge")
    self.password_button = Button(self, text = "Show", command = self.showPassword)
    self.password_button.grid(row = 1, column = 3, pady = 5, padx = 5)

    self.server_menu_label = Label(self, text = "VPS Injection")
    self.server_menu_label.grid(row = 0, column = 4, pady = 5, padx = 5)
    self.server_menu_selection = StringVar(self)
    self.server_menu_selection.set("Minimal")
    self.server_menu = OptionMenu(self, self.server_menu_selection, "Minimal", "Basic", "LAMP", "Wordpress")
    self.server_menu.grid(row = 1, column = 4, pady = 5, padx = 5)

    self.IP_label = Label(self, text = "VPS IP-Address")
    self.IP_label.grid(row = 2, column = 0, pady = 5, padx = 5)
    self.IP_entry = Entry(self, justify = "center")
    self.IP_entry.grid(row = 3, column = 0, pady = 5, padx = 5)

    self.CPU_label = Label(self, text = "vCPU(s)")
    self.CPU_label.grid(row = 2, column = 1, pady = 5, padx = 5)
    self.CPU_entry = Entry(self, justify = "center")
    self.CPU_entry.grid(row = 3, column = 1, pady = 5, padx = 5)
    self.CPU_entry.insert(0, 1)

    self.RAM = Label(self, text = "vRAM")
    self.RAM.grid(row = 2, column = 4, pady = 5, padx = 5)
    self.RAM_entry = Entry(self, justify = "center")
    self.RAM_entry.grid(row = 3, column = 4, pady = 5, padx = 5)
    self.RAM_entry.insert(0, 512)

    self.domain_label = Label(self, text = "FQDN")
    self.domain_label.grid(row = 4, column = 0, pady = 5, padx = 5)
    self.domain_entry = Entry(self, justify = "center")
    self.domain_entry.insert(0, "N/A")
    self.domain_entry.grid(row = 5, column = 0, pady = 5, padx = 5)

    self.SSL = IntVar()
    self.SSL.set(0)
    self.check_SSL = Checkbutton(self, text = "SSL", variable = self.SSL, onvalue = 1, offvalue = 0)
    self.check_SSL.grid(row = 5, column = 1, pady = 5, padx = 5)  

    self.email_label = Label(self, text = "eMail")
    self.email_label.grid(row = 4, column = 4, pady = 5, padx = 5)
    self.email_entry = Entry(self, justify = "center")
    self.email_entry.grid(row = 5, column = 4, pady = 5, padx = 5)

    self.activate = Button(self, text = "Execute", command = self.execute)
    self.activate.grid(row = 25, column = 10, pady = 5, padx = 5)

    self.close = Button(self, text = "Close", command = self.master.destroy)
    self.close.grid(row = 25, column = 11, pady = 5, padx = 5)
    
    self.help_button = Button(self, text = "Help")
    self.help_button.grid(row = 25, column = 0, pady = 5, padx = 5)

  def showPassword(self):
    text = self.password_entry.get()

    self.password_entry = Entry(self, justify = "center")
    self.password_entry.insert(0, f"{text}")
    self.password_entry.grid(row = 1, column = 1, columnspan = 1, padx = 5)

  def execute(self):
    # connection = Connection("root", "Kn0wledge!", "192.168.1.75", "V_PAYLOAD")
    # result = connection.queryAll()
    # subnet = connection.incrementIP()
    # VPS_IP = connection.network + str(subnet)
    # input.v_IP = VPS_IP

    input.v_User = self.user_entry.get()
    input.v_Password = self.password_entry.get()
    input.v_IP = self.IP_entry.get()
    input.v_Type = self.server_menu_selection.get()
    input.v_CPU = self.CPU_entry.get()
    input.v_RAM = self.RAM_entry.get()

    input.Domain = self.domain_entry.get()
    input.SSL = self.SSL.get()

    input.eMail[2] = self.email_entry.get()

    # connection.addVPS("test2", "Knowledge", "Wordpress", VPS_IP, 512, 1, "N/A", 0, "jsanders4129@gmail.com")
    # connection.addVPS(input.v_User, input.v_Password, input.v_Type, input.v_IP, input.v_RAM, input.v_CPU, input.Domain, input.SSL, input.eMail[2])

    main()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog = "Vault Payload", argument_default = argparse.SUPPRESS)

  parser.add_argument("-D", "--Domain", type = str, default = None, required = False)
  parser.add_argument("--SSL", type = int, default = False, required = False)

  parser.add_argument("--v_User", type = str, default = "bionic",  required = False)
  parser.add_argument("--v_Password", type = str, default = "Knowledge", required = False)
  parser.add_argument("--v_IP", type = str, default = "169.254.0.1", required = False)
  parser.add_argument("--v_Type", type = str, default = "minimal", required = False)
  parser.add_argument("--v_RAM", type = int, default = 512, required = False)
  parser.add_argument("--v_CPU", type = int, default = 1, required = False)

  parser.add_argument("--h_User", type = str, default = "snow", required = False)
  parser.add_argument("--h_IP", type = str, default = "192.168.1.99", required = False)
  parser.add_argument("--h_OS", default = "windows", type = str, required = False)

  parser.add_argument("--p_User", type = str, default = "snow", required = False)
  parser.add_argument("--p_IP", type = str, default = "192.168.1.60", required = False)

  parser.add_argument("--g_User", type = str, default = "snow", required = False)
  parser.add_argument("--g_IP", type = str, default = "192.168.0.5", required = False)

  parser.add_argument("--eMail", nargs = "+", type = str, default = ["development.cloudhybrid@gmail.com", "Kn0wledge!", "development.cloudhybrid@gmail.com"], required = False)

  parser.add_argument("--GUI", type = str, default = True, required = False)

  input = parser.parse_args()

  if input.GUI == True:
    Display().header()
    Display().copyright()

    interface = Tk()
    logo = resource_path("Vault.ico")
    interface.iconbitmap(logo)
    display = GUI()
    interface.mainloop()
  else:
    if input.v_IP or input.v_User == None:
      print("Invalid Input")
      quit()
    else:
      print("Executing Injections".center(os.get_terminal_size().columns))
      main()
