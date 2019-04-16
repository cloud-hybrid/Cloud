"""
@Parameters
  ↳   User       - Username	         - Required	: (String)      - Default:  None
      Password   - Password          - Required	: (String)      - Default:  "Knowledge"
        ↳	Note: self.password is used for the preseeding. Default should remain the same. 
                Change the provisioning script(s) to change the user's password after 
                installation.
      IP         - IP Address        - Required	: (String)      - Default:  None
      Type       - Preseed Type      - Required	: (String)      - Default:  "minimal"
      RAM        - RAM Allocation    - Required	: (Integer)     - Default:  512
      CPUs       - vCPU Allocation   - Required	: (String)      - Default:  1
      Hostname   - Server Name       - Required	: (String)      - Default:  VPS().hostname
      Domain     - FQDN              - Optional : (String)      - Default:  None

@Documentation
  [Function]    - "VPS().hostname" will print out the actual function return hostname.
                - The @property returns a true object property, but is not static
                - accross all VPS() objects. 
"""

import time
import hashlib

from Payload.Vault.Shell.Terminal import Terminal

class VPS(object):
  def __init__(self, user, password, address, type, ram, cpu, domain, SSL):
    self.user = user
    self.password = password
    self.IP = address
    self.type = type
    self.RAM = ram 
    self.CPUs = cpu
    self.FQDN = domain
    self.SSL = SSL
    
    self.hostname = None

  @staticmethod
  def start(hostname):
    command = f"virsh start {hostname}"
    Terminal(command).execute()

  @staticmethod
  def remoteStart(hostname, user, client):
    command = f"""ssh {user}@{client} -t "sudo virsh start {hostname}" """
    Terminal(command).execute()

  @property
  def name(self):
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    hash_decoded = hash.hexdigest()
    hash_decoded = hash.hexdigest()[:-30]

    # name = ("vault-" + hash_decoded + ".vps.vaultcipher.com")
    name = ("virtual-" + hash_decoded + ".vps.vaultcipher.com")
    return name
