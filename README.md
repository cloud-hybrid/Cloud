# Vault Payload
Welcome to the Vault Cipher Provisioning Payload repository.

Payload is an automated infrastructure provisioning tool that creates, configures, and provisions reverse proxies, web-servers, clouds, SQL databases, SSH gateways, and other types of production servers. Sub-configurations include SSH keys, VPS users, Wordpress sites, Nginx & Apache backends, remote repositories, server preseeds, etc. Payload utilizes Python, Bash, and PHP as the primary programming languages, and various networking and front-end development concepts and packages. 

Please visit [Vault Cipher LLC.](https://vaultcipher.com) and read the package's documentation for additional details and information.

# Development

## Critical
- [ ] Fix Initial Wordpress settings where themes can't be downloaded
- [ ] Update php.ini wordpress vps settings to increased RAM limit
- [ ] 
- [ ] Permissions
  - Create permissions object that changes localhost permissions for tmp, tmp.mesi, etc
- [x] Fix Login Redirect
- [x] Style ftp-registration-pending.php 
- [ ] Add period to account confirmation email after the activation code
- [ ] Provisioning
  - [ ] Gateway Server
  - [ ] Shared Webserver (Apache)
  - [ ] Webserver (NginX)
  - [ ] Reverse Proxy (NginX)
  - [x] VPS
- [ ] SSH-Key Validation
  - Create SSH-Key validation script to check if keys are created. If they're not, use sshpass & ssh-keygen to create and provision a new set of keys
- [ ] CGI-Directory Dashboard Control
  - Create a dashboard button that sets the correct execution & access permissions
- [ ] DNS Record Object
  - Develop a DNS program that takes in input and creates the desired dns records
- [ ] puTTY SSH Keys
  - Figure out how to convert current SSH-Keys to a .pem format for puTTY use
- [ ] Decommissioning Script
- [ ] XML Map
- [ ] Backup Utilization
  - Implement backup scripts in all locations where file(s) change
  - Create the backup directories
  - [ ] Reverse Proxy
    - [x] FQDN Additions
    - [ ] Certificate Renewels
    - [ ] Wildcard Changes
  - [ ] DNS Records
- [x] Reverse Proxy FQDN Provisioning
- [x] SSL Redirections
- [x] Mail Server
## Important
- [ ] Services
  - [ ] Shared Hosting Registration Page
    - [ ] Free 
    - [ ] Paid
  - [ ] VPS Registration Page
  - [ ] Development Contact Page
  - [x] General Services Page
- [ ] Payload SQL
  - Create tables based off of objects --> such as VPS()
    - Attributes such as VPS().IP should be automatically incremented
    - Attributes such as VPS().user should be checked for duplicates
    - [ ] VPS Users
    - [ ] VPS IP Addresses
    - [ ] Shared-Hosted Users
    - [ ] Shared-Hosted Domains
- [ ] DNS-Record.py
  - Use to check if DNS record(s) point to Master-DNS before provisioning VPS FQDNs
- [ ] Homepage's Divided Header Padding
- [ ] Dashboard Margins & Padding
- [x] Python Email Function 
- [x] mySQL Root password
  - Fix string arguments
- [x] gitHub Repository
## Minor
- [ ] Check if True == 1 for SSL Input
- [ ] Debugging
  - [ ] Gateway
    - Check if port 22 is open to Internet before setting up as Jump-Host
  - [ ] Proxy
    - Check if ports 80, 443 are open
- [ ] Python DocStrings
  - [ ] Payload
  - [ ] Network
  - [ ] Installation
  - [ ] Shell
- [ ] Shared-Hosting Guide
  - [ ] Email Attachment
  - [ ] Tutorial
  - [ ] Blog Post
  - [ ] Shared-Hosting Services Reference Link
- [ ] VPS Guide
  - Include SSH, SSH w/puTTY, adding FQDN, how to point Google DNS Nameservers to Master-DNS, how to change default user password, Wordpress setup, SSH key disclaimers
  - [ ] Email Attachment
  - [ ] Tutorial
  - [ ] Blog Post
  - [ ] VPS Services Reference Link
- [ ] Embed PDFs
- [ ] vPanel Sidebar
  - Edit or remove
- [ ] Login Page
  - Style
- [ ] Knowledge Sidebar
  - Ensure of consistency with styling and margins for all pages
- [x] Remove gitLab from Infrastructure
## Indeterminate
- [ ] VPS().password
  - Update to VPS().__password --> a private attribute
- [ ] Network Map
  - Use Google's open-source cloud icons
- [ ] Company Documents
  - Update company name and update dates

# Support & Documentation

## Languages
- [Python3.6+](https://docs.python.org/3/) - Programming Language
- [Bash](https://www.tldp.org/LDP/abs/abs-guide.pdf) - Scripting Language
- [PHP 7.2+](http://php.net/manual/en/install.php) - Front/Backend Development Language

## Infrastructure
* [Nginx](https://docs.python.org/3/) - Reverse Proxy, SSL Encryption, SSH Jump-Server
* [Apache 2.4+](https://httpd.apache.org/docs/2.4/) - Backend Webserver, PHP 7.2 FPM Proxy
  * [CGI](https://httpd.apache.org/docs/2.4/mod/mod_cgi.html) - Apache2 Scripting Module

## Author(s) & Acknowledgments

* **Jacob B. Sanders** - *Project Creator, Owner of Vault Cipher LLC.* - [Vault Cipher LLC.](https://vaultcipher.com/team/jacob-sanders)

* [Contributors & Contributions](https://github.com/vaultcipher/Payload/Contributors)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

virt-install \
    --name=Windows
    --ram=8192 \
    --cpu=host
    --vcpus=2 \
    --os-type=windows \
    --disk /dev/mapper/vms-win10,bus=virtio \
    --disk /tmp/en_windows_10_enterprise_x64_dvd_6851151.iso,device=cdrom,bus=ide \
    --disk /usr/share/virtio-win/virtio-win.iso,device=cdrom,bus=ide \
    --graphics vnc,listen=0.0.0.0 