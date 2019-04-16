import os
import sys
import time
import textwrap
import tempfile
import subprocess
import pkgutil

import threading as Threading
from multiprocessing import Process, Queue

from Payload.Vault.Shell.Terminal import Terminal
from Payload.Vault.Shell.CMD import CMD
from Payload.Vault.Installation import Source

from Payload.Vault.Installation.Progress import Progress
from Payload.Vault.Installation.Preseed import Preseed

EXECUTIONS = {
  "VPS" : "Installer(self).VPS(self)", 
  "ISO" : "Installer(self).ISO(self)", 
  "PRESEED" : "Installer(self).PRESEED(self)"
}

class Installer(object): 
  def __init__(self, source, ram = 512, cpu = 1):
    self.source = source
    self.RAM = ram
    self.vCores = cpu

  def install(self, vps_type, vps_user, vps_password, vps_ip):
    #Installer(self).aSYNCHRONIZE(self)
    Installer(self).ISO(self)
    Installer(self).VPS(self)
    Installer(self).PRESEED(self, vps_type, vps_user, vps_password, vps_ip)
    Installer(self).PERMISSIONS(self)

  @staticmethod
  def aSYNCHRONIZE(self):
    queue = Queue()

    for index, execution in EXECUTIONS.items():
      queue.put(execution)
      vThread = Threading.Thread(target = eval(execution), args = ())
      vThread.daemon = True
      vThread.start()

  @staticmethod
  def VPS(self):
    directory = str(Installer(self).windowsTEMP)
    file = "create-VPS.sh"
    script = directory + file

    script = open(script, "w+")
    script.write(self.kernal)
    script.close()

    if os.path.exists(str(directory + file)[:-3] + ".backup"):
      os.remove(str(directory + file)[:-3] + ".backup")

    with tempfile.NamedTemporaryFile(delete = False) as conversion:
      for line in open(str(directory + file), "rb") :
        line = line.rstrip()
        conversion.write(line + "\n".encode())

    conversion.close()

    os.rename(str(directory + file), str(f"{directory + file}"[:-3] + ".backup"))
    os.rename(conversion.name, f"{str(directory + file)}")

    Installer(self).SCP(f"{directory + file}", "snow", "192.168.0.1", "/mnt/Virtual-Machines/")

  @staticmethod
  def ISO(self):
    Installer(self).SCP(self.source, "snow", "192.168.0.1", "/mnt/Virtual-Machines/")

  @staticmethod
  def PRESEED(self, vps_type, vps_user, vps_password, vps_ip):
    directory = "C:\\Temp\\"
    file = "preseed.cfg"
    script = str(directory + file)

    script = open(script, "w+")

    if vps_type == "Basic":
      script.write(Preseed(vps_user, vps_password, vps_ip, Preseed.HOSTNAME).preseed_basic)
    elif vps_type == "LAMP":
      script.write(Preseed(vps_user, vps_password, vps_ip, Preseed.HOSTNAME).preseed_lamp)
    elif vps_type == "Wordpress":
      script.write(Preseed(vps_user, vps_password, vps_ip, Preseed.HOSTNAME).preseed_lamp_wordpress)
    else:
      script.write(Preseed(vps_user, vps_password, vps_ip, Preseed.HOSTNAME).preseed_minimal)
    
    script.close()
  
    Installer(self).SCP(f"{directory + file}", "snow", "192.168.0.1", "/mnt/Virtual-Machines/")

  @staticmethod
  def PERMISSIONS(self):
    CMD().execute(f"""ssh snow@192.168.0.1 -t "sudo chown snow -R /mnt/Virtual-Machines/" """)
    CMD().execute(f"""ssh snow@192.168.0.1 -t "sudo chmod 755 /mnt/Virtual-Machines/" """)
    CMD().execute(f"""ssh snow@192.168.0.1 -t "sudo chmod a+x /mnt/Virtual-Machines/create-VPS.sh" """)

  @staticmethod
  def SCP(source, user, client, directory):
    command = f"""scp {source} {user}@{client}:{directory}"""
    CMD().execute(command)

  @property
  def kernal(self):
    RAM = self.RAM
    CPU = self.vCores

    PRESEED = "preseed.cfg"
    ISO = "Bionic-Server.iso"
    MIRROR = "us.archive.ubuntu.com"

    slash = "\\"

    command = textwrap.dedent(
      f"""sudo virt-install {slash}
      --nographics {slash}
      --name {Preseed.HOSTNAME} {slash}
      --ram {RAM} {slash}
      --disk path={"/mnt/Virtual-Machines/"}{Preseed.HOSTNAME}.qcow2,size=10 {slash}
      --location "{"/mnt/Virtual-Machines/"}{ISO}" {slash}
      --initrd-inject={"/mnt/Virtual-Machines/"}{PRESEED} {slash}
      --vcpus {CPU} {slash}
      --os-type linux {slash}
      --os-variant ubuntu18.04 {slash}
      --autostart {slash}
      --extra-args="console=ttyS0,19200"
      """
    ).strip()

    return command

  @staticmethod
  def install_wordpress_database(vps_password, vps_ip):
    tty_command = textwrap.dedent(
    f"""
    echo y | plink -ssh {vps_ip} -l root -pw {vps_password} "exit"
    """.strip()
    )
    Terminal(tty_command).execute()

    time.sleep(1)

    tty_command = textwrap.dedent(
    f"""
    echo y | plink -ssh {vps_ip} -l root -pw {vps_password} "sudo /var/www/database.sh"
    """.strip()
    )
    Terminal(tty_command).execute()

  @property
  def vmDirectory(self):
    directory = "/mnt/Virtual-Machines/"
    return directory

  @property
  def windowsTEMP(self):
    directory = "C:\\Temp\\"
    return directory

  @property
  def linuxTEMP(self):
    directory = "/tmp/"
    return directory  