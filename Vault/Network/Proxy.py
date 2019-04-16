"""
@Infrastructure
  ↳   SSH-Keys    - SSH keys must be set from the         - Required  : (RSA-Key)
                  | - host --> client.
                  | - For testing purposes, add SSH
                  | - keys to and from localhost.
@Parameters
  ↳   Server      - The IP address or verified hostname   - Required  : (Command-Line)
                  | - of the target server hosting the
                  | - VPS. Defaults to localhost.
@Documentation
  [Note]    - When packaging the program, {script} may not work correct. The path relative
            - to its execution potentially could be the problem.
  [To-Do]   - Update @Parameters
"""

import os
import sys
import time
import textwrap

from Payload.Vault.Shell.Terminal import Terminal

DIRECTORY = "C:\\Windows\\Temp\\"

class Proxy(object):
  def __init__(self, user, address):
    self.user = user
    self.IP = address

  def updateProxy(self, VPS):
    script = DIRECTORY + "update-proxy.sh"

    script = open(script, "w+")

    if VPS.SSL == True or VPS.SSL == 1:
      script.write(self.proxy_script_ssl(VPS))
    else:
      script.write(self.proxy_script(VPS))

    script.close()

    Proxy(self.user, self.IP).ttyExecute("192.168.1.60", DIRECTORY + "update-proxy.sh")

  @staticmethod
  def proxy_script(VPS):
    open = "{"
    close = "}"

    script = textwrap.dedent(
    f"""
    #!/bin/bash
    HOST='\$host'
    URI='\$request_uri'
    cat << EOF > /etc/nginx/sites-enabled/{VPS.hostname}.conf
    server {open}
      listen 80;
      server_name {VPS.hostname};
      location / {open}
        proxy_pass http://{VPS.IP}:80;
        include proxy.conf;
      {close}
    {close}

    server {open}
      listen 443;
      server_name {VPS.hostname};
      location / {open}
        proxy_pass http://{VPS.IP}:443;
        include proxy.conf;
      {close}
    {close}
    EOF

    sudo nginx -s reload

    """
    ).strip()

    return script

  @staticmethod
  def proxy_script_ssl(VPS):
    open = "{"
    close = "}"

    script = textwrap.dedent(
    f"""
    #!/bin/bash
    HOST='$host'
    URI='$request_uri'
    cat << EOF > /etc/nginx/sites-enabled/{VPS.hostname}.conf
    server {open}
      listen 80;
      server_name {VPS.hostname};
      location / {open}
        proxy_pass http://{VPS.IP}:80;
        include proxy.conf;
      {close}
    {close}
    EOF

    sudo nginx -s reload

    sudo certbot certonly --nginx -d {VPS.hostname}
    cat << EOF > /etc/nginx/sites-enabled/{VPS.hostname}.conf
    server {open}
      listen 443;
      server_name {VPS.hostname};
      ssl_certificate /etc/letsencrypt/live/{VPS.hostname}/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/{VPS.hostname}/privkey.pem;
      include /etc/letsencrypt/options-ssl-nginx.conf;
      ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
      location / {open}
        proxy_pass http://{VPS.IP}:80;
        include proxy.conf;
      {close}
    {close}
    
    server {open}
      listen 80;
      server_name {VPS.hostname};
      return 301 https://$HOST$URI;
    {close}
    EOF

    sudo nginx -s reload

    """
    ).strip()

    return script

  @staticmethod
  def ttyExecute(server, script):
    """ 
    @Description
    ↳ Internal method that executes a installer()-related command on a remote location using a file either created or 
        stored locally. The the process is executed by puTTY. puTTY should be pre-installed (create check statement), and 
        password should be passed in by command line before program execution (when creating the Installer() object) and 
        then be hashed.
    @Parameters
    ↳ Script --> The [os.path.dirname(os.path.normpath(__file__)) + \ + location] of the script.
    """

    tty_command = textwrap.dedent(
    f"""
    putty -ssh -l snow -pw Kn0wledge! -m {script} {server}
    """.strip()
    )

    Terminal(tty_command).display()