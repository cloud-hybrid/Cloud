"""
@Infrastructure
  ↳   Requirement - Description                           - Required  : (Type)

@Parameters
  ↳   Server      - Description                           - Required  : (Command-Line)

@Documentation
  [To-Do]     - Change object and file name(s) from Preseed to Injection.
  [To-Do]     - Update all preseeds to match that of the minimal.
"""

import textwrap

class Preseed(object):
  def __init__(self, user = "bionic", password = "bionic", IP = "192.168.0.255", hostname = "VPS-Bionic"):
    self.user = user
    self.password = password
    self.IP = IP
    self.hostname = Preseed.HOSTNAME

  @property
  def HOSTNAME(self):
    hostname = None
    return hostname

  @property
  def preseed(self):
    seed = textwrap.dedent(
      f"""
      #---------╔════════════════════╦═══════════════════════════════╗---------#
      #---------║      Developer     ║      © Vault Cipher LLC.      ║---------#
      #---------║   ──────────────   ║   ─────────────────────────   ║---------#
      #---------║  Jacob B. Sanders  ║    https://vaultcipher.com    ║---------#
      #---------╚════════════════════╩═══════════════════════════════╝---------#

      # --- Injection Priority --- #
      d-i debconf/priority string critical
      d-i auto-install/enable boolean true

      # --- Language Settings --- #
      d-i debian-installer/language string en
      d-i debian-installer/country string US
      d-i debian-installer/locale string en_US

      # --- Keyboard Overwrites --- #
      d-i console-setup/ask_detect boolean false
      d-i keyboard-configuration/xkb-keymap select us

      # --- Network Configuration --- #
      d-i netcfg/choose_interface select auto
      d-i netcfg/disable_autoconfig boolean true
      d-i netcfg/dhcp_failed note
      d-i netcfg/dhcp_options select Configure network manually
      # ------ > Static Network Settings
      d-i netcfg/get_ipaddress string 192.168.1.10
      d-i netcfg/get_netmask string 255.255.0.0
      d-i netcfg/get_gateway string 192.168.1.1
      d-i netcfg/get_nameservers string 192.168.1.1
      d-i netcfg/confirm_static boolean true
      # ------ > Hostname
      d-i netcfg/get_hostname string bionic-server
      d-i netcfg/get_domain string bionic-domain

      # --- Prevent Wireless Prompt --- #
      d-i netcfg/wireless_wep string

      # --- Mirrors --- #
      d-i mirror/country string manual
      d-i mirror/http/hostname string us.archive.ubuntu.com
      d-i mirror/http/directory string /ubuntu
      d-i mirror/http/proxy string

      # --- Account Setup --- #
      # ------ > Root
      d-i passwd/root-login boolean true
      d-i passwd/root-password password P@ssw0rd!
      d-i passwd/root-password-again password P@ssw0rd!
      # ------ > Default User
      d-i passwd/user-fullname string Ubuntu User
      d-i passwd/username string ubuntu
      d-i passwd/user-password password insecure
      d-i passwd/user-password-again password insecure
      # ------ > Allow Weak Password
      d-i user-setup/allow-password-weak boolean true
      # ------ > User Groups
      d-i passwd/user-default-groups sudo ubuntu adm cdrom dip plugdev lpadmin sambashare
      # ------ > Home Encryption
      d-i user-setup/encrypt-home boolean false

      # --- Time --- #
      d-i clock-setup/utc boolean true
      d-i time/zone string US/Eastern
      d-i clock-setup/ntp boolean true

      # --- Disk Partitioning --- #
      d-i partman-auto/method string lvm
      d-i partman-lvm/device_remove_lvm boolean true
      d-i partman-md/device_remove_md boolean true
      d-i partman-lvm/confirm boolean true
      d-i partman-lvm/confirm_nooverwrite boolean true
      d-i partman-auto/choose_recipe select atomic
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true
      d-i partman-md/confirm boolean true
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true

      # --- Package Installations --- #
      tasksel tasksel/first multiselect lamp-server
      d-i pkgsel/include string openssh-server net-tools software-properties-common build-essential curl ca-certificates
      # --- Update Policy --- #
      d-i pkgsel/update-policy select none

      # --- Post Setup Configuration --- #
      d-i grub-installer/only_debian boolean true
      d-i grub-installer/with_other_os boolean true
      d-i finish-install/reboot_in_progress note

      # --- Late-Stage Commands --- #
      debconf-set-selections <<< "postfix postfix/mailname string your.hostname.com"
      debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
      apt-get install -y postfix

      d-i preseed/late_command string \
        in-target sh -c 'sed -i "s/^#PermitRootLogin.*\$/PermitRootLogin yes/g" /etc/ssh/sshd_config'; \
        in-target sh -c 'curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash'; \
        in-target sh -c 'sudo EXTERNAL_URL="https://git.vaultcipher.com" apt-get install gitlab-ee';
      """.strip()
      )

    return seed

  @property
  def preseed_lamp(self):
    lamp = textwrap.dedent(
      f"""
      d-i debconf/priority string critical
      d-i auto-install/enable boolean true

      # --- Language Settings --- #
      d-i debian-installer/language string en
      d-i debian-installer/country string US
      d-i debian-installer/locale string en_US

      # --- Keyboard Overwrites --- #
      d-i console-setup/ask_detect boolean false
      d-i keyboard-configuration/xkb-keymap select us

      # --- Network Configuration --- #
      d-i netcfg/choose_interface select auto
      d-i netcfg/disable_autoconfig boolean true
      d-i netcfg/dhcp_failed note
      d-i netcfg/dhcp_options select Configure network manually
      # ------ > Static Network Settings
      d-i netcfg/get_ipaddress string {self.IP}
      d-i netcfg/get_netmask string 255.255.0.0
      d-i netcfg/get_gateway string 192.168.1.1
      d-i netcfg/get_nameservers string 192.168.1.1
      d-i netcfg/confirm_static boolean true
      # ------ > Hostname
      d-i netcfg/get_hostname string {self.hostname}
      d-i netcfg/get_domain string vaultcipher.com

      # --- Prevent Wireless Prompt --- #
      d-i netcfg/wireless_wep string

      # --- Mirrors --- #
      d-i mirror/country string manual
      d-i mirror/http/hostname string us.archive.ubuntu.com
      d-i mirror/http/directory string /ubuntu
      d-i mirror/http/proxy string

      # --- Account Setup --- #
      # ------ > Root
      d-i passwd/root-login boolean true
      d-i passwd/root-password password {self.password}
      d-i passwd/root-password-again password {self.password}
      # ------ > Default User
      d-i passwd/user-fullname string {self.user}
      d-i passwd/username string {self.user}
      d-i passwd/user-password password {self.password}
      d-i passwd/user-password-again password {self.password}
      # ------ > Allow Weak Password
      d-i user-setup/allow-password-weak boolean true
      # ------ > Home Encryption
      d-i user-setup/encrypt-home boolean false

      # --- Time --- #
      d-i clock-setup/utc boolean true
      d-i time/zone string US/Eastern
      d-i clock-setup/ntp boolean true

      # --- Disk Partitioning --- #
      d-i partman-auto/method string lvm
      d-i partman-lvm/device_remove_lvm boolean true
      d-i partman-md/device_remove_md boolean true
      d-i partman-lvm/confirm boolean true
      d-i partman-lvm/confirm_nooverwrite boolean true
      d-i partman-auto/choose_recipe select atomic
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true
      d-i partman-md/confirm boolean true
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true

      # --- Package Installations --- #
      tasksel tasksel/first multiselect lamp-server
      d-i pkgsel/include string openssh-server net-tools curl software-properties-common wget curl

      # --- Update Policy --- #
      d-i pkgsel/update-policy select none
      d-i pkgsel/updatedb boolean false

      # --- Post Setup Configuration --- #
      d-i grub-installer/only_debian boolean true
      d-i grub-installer/with_other_os boolean true

      # --- Reboot --- #
      d-i finish-install/reboot_in_progress note

      # --- Late-Stage Commands --- #

      d-i preseed/late_command string in-target sed -i "s/^#PermitRootLogin.*\$/PermitRootLogin yes/g" /etc/ssh/sshd_config; in-target wget -O /tmp/provision.sh "https://unixvault.com/provision_lamp.sh" --no-check-certificate; in-target chmod +x /tmp/provision.sh; in-target /bin/bash /tmp/provision.sh {self.user};
      """
    ).strip()
    return lamp

  @property
  def preseed_lamp_wordpress(self):
    lamp_wordpress = textwrap.dedent(
      f"""
      d-i debconf/priority string critical
      d-i auto-install/enable boolean true

      # --- Language Settings --- #
      d-i debian-installer/language string en
      d-i debian-installer/country string US
      d-i debian-installer/locale string en_US

      # --- Keyboard Overwrites --- #
      d-i console-setup/ask_detect boolean false
      d-i keyboard-configuration/xkb-keymap select us

      # --- Network Configuration --- #
      d-i netcfg/choose_interface select auto
      d-i netcfg/disable_autoconfig boolean true
      d-i netcfg/dhcp_failed note
      d-i netcfg/dhcp_options select Configure network manually
      # ------ > Static Network Settings
      d-i netcfg/get_ipaddress string {self.IP}
      d-i netcfg/get_netmask string 255.255.0.0
      d-i netcfg/get_gateway string 192.168.1.1
      d-i netcfg/get_nameservers string 192.168.1.1
      d-i netcfg/confirm_static boolean true
      # ------ > Hostname
      d-i netcfg/get_hostname string {self.hostname}
      d-i netcfg/get_domain string vaultcipher.com

      # --- Prevent Wireless Prompt --- #
      d-i netcfg/wireless_wep string

      # --- Mirrors --- #
      d-i mirror/country string manual
      d-i mirror/http/hostname string us.archive.ubuntu.com
      d-i mirror/http/directory string /ubuntu
      d-i mirror/http/proxy string

      # --- Account Setup --- #
      # ------ > Root
      d-i passwd/root-login boolean true
      d-i passwd/root-password password {self.password}
      d-i passwd/root-password-again password {self.password}
      # ------ > Default User
      d-i passwd/user-fullname string {self.user}
      d-i passwd/username string {self.user}
      d-i passwd/user-password password {self.password}
      d-i passwd/user-password-again password {self.password}
      # ------ > Allow Weak Password
      d-i user-setup/allow-password-weak boolean true
      # ------ > Home Encryption
      d-i user-setup/encrypt-home boolean false

      # --- Time --- #
      d-i clock-setup/utc boolean true
      d-i time/zone string US/Eastern
      d-i clock-setup/ntp boolean true

      # --- Disk Partitioning --- #
      d-i partman-auto/method string lvm
      d-i partman-lvm/device_remove_lvm boolean true
      d-i partman-md/device_remove_md boolean true
      d-i partman-lvm/confirm boolean true
      d-i partman-lvm/confirm_nooverwrite boolean true
      d-i partman-auto/choose_recipe select atomic
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true
      d-i partman-md/confirm boolean true
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true

      # --- Package Installations --- #
      tasksel tasksel/first multiselect lamp-server
      d-i pkgsel/include string openssh-server net-tools curl software-properties-common wget curl

      # --- Update Policy --- #
      d-i pkgsel/update-policy select none
      d-i pkgsel/updatedb boolean true

      # --- Post Setup Configuration --- #
      d-i grub-installer/only_debian boolean true
      d-i grub-installer/with_other_os boolean true

      # --- Reboot --- #
      d-i finish-install/reboot_in_progress note

      # --- Late-Stage Commands --- #

      d-i preseed/late_command string in-target sed -i "s/^#PermitRootLogin.*\$/PermitRootLogin yes/g" /etc/ssh/sshd_config; in-target wget -O /tmp/provision.sh "https://unixvault.com/provision_lamp_wordpress.sh" --no-check-certificate; in-target chmod +x /tmp/provision.sh; in-target /bin/bash /tmp/provision.sh {self.user} {self.hostname};
      """
    ).strip()
    return lamp_wordpress


  @property
  def preseed_basic(self):
    basic = textwrap.dedent(
      f"""
      #╔════════════════════╦═══════════════════════════════╗#
      #║      Developer     ║      © Vault Cipher LLC.      ║#
      #║   ──────────────   ║ ───────────────────────────── ║#
      #║  Jacob B. Sanders  ║    https://vaultcipher.com    ║#
      #╚════════════════════╩═══════════════════════════════╝#

      # --- Injection Priority --- #
      d-i debconf/priority string critical
      d-i auto-install/enable boolean true

      # --- Language Settings --- #
      d-i debian-installer/language string en
      d-i debian-installer/country string US
      d-i debian-installer/locale string en_US

      # --- Keyboard Overwrites --- #
      d-i console-setup/ask_detect boolean false
      d-i keyboard-configuration/xkb-keymap select us

      # --- Network Configuration --- #
      d-i netcfg/choose_interface select auto
      d-i netcfg/disable_autoconfig boolean true
      d-i netcfg/dhcp_failed note
      d-i netcfg/dhcp_options select Configure network manually
      # ------ > Static Network Settings
      d-i netcfg/get_ipaddress string {self.IP}
      d-i netcfg/get_netmask string 255.255.0.0
      d-i netcfg/get_gateway string 192.168.1.1
      d-i netcfg/get_nameservers string 192.168.1.1
      d-i netcfg/confirm_static boolean true
      # ------ > Hostname
      d-i netcfg/get_hostname string {self.hostname}
      d-i netcfg/get_domain string vaultcipher.com

      # --- Prevent Wireless Prompt --- #
      d-i netcfg/wireless_wep string

      # --- Mirrors --- #
      d-i mirror/country string manual
      d-i mirror/http/hostname string us.archive.ubuntu.com
      d-i mirror/http/directory string /ubuntu
      d-i mirror/http/proxy string

      # --- Account Setup --- #
      # ------ > Root
      d-i passwd/root-login boolean true
      d-i passwd/root-password password {self.password}
      d-i passwd/root-password-again password {self.password}
      # ------ > Default User
      d-i passwd/user-fullname string {self.user} User
      d-i passwd/username string {self.user}
      d-i passwd/user-password password {self.password}
      d-i passwd/user-password-again password {self.password}
      # ------ > Allow Weak Password
      d-i user-setup/allow-password-weak boolean true
      # ------ > User Groups
      d-i passwd/user-default-groups sudo {self.user} adm cdrom dip plugdev lpadmin sambashare
      # ------ > Home Encryption
      d-i user-setup/encrypt-home boolean false

      # --- Time --- #
      d-i clock-setup/utc boolean true
      d-i time/zone string US/Eastern
      d-i clock-setup/ntp boolean true

      # --- Disk Partitioning --- #
      d-i partman-auto/method string lvm
      d-i partman-lvm/device_remove_lvm boolean true
      d-i partman-md/device_remove_md boolean true
      d-i partman-lvm/confirm boolean true
      d-i partman-lvm/confirm_nooverwrite boolean true
      d-i partman-auto/choose_recipe select atomic
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true
      d-i partman-md/confirm boolean true
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true

      # --- Package Installations & Update --- #
      d-i pkgsel/include string openssh-server net-tools curl software-properties-common wget
      d-i pkgsel/upgrade select full-upgrade
      # --- Update Policy --- #
      d-i pkgsel/update-policy select none

      # --- Post Setup Configuration --- #
      d-i grub-installer/only_debian boolean true
      d-i grub-installer/with_other_os boolean true
      d-i finish-install/reboot_in_progress note

      # --- Late-Stage Commands --- #
      d-i preseed/late_command string \
        in-target sed -i "s/^#PermitRootLogin.*\$/PermitRootLogin yes/g" /etc/ssh/sshd_config; \
        in-target usermod -aG sudo {self.user};
      """
    )
    return basic

  @property
  def preseed_minimal(self):
    minimal = textwrap.dedent(
      f"""
      d-i debconf/priority string critical
      d-i auto-install/enable boolean true

      # --- Language Settings --- #
      d-i debian-installer/language string en
      d-i debian-installer/country string US
      d-i debian-installer/locale string en_US

      # --- Keyboard Overwrites --- #
      d-i console-setup/ask_detect boolean false
      d-i keyboard-configuration/xkb-keymap select us

      # --- Network Configuration --- #
      d-i netcfg/choose_interface select auto
      d-i netcfg/disable_autoconfig boolean true
      d-i netcfg/dhcp_failed note
      d-i netcfg/dhcp_options select Configure network manually
      # ------ > Static Network Settings
      d-i netcfg/get_ipaddress string {self.IP}
      d-i netcfg/get_netmask string 255.255.0.0
      d-i netcfg/get_gateway string 192.168.1.1
      d-i netcfg/get_nameservers string 192.168.1.1
      d-i netcfg/confirm_static boolean true
      # ------ > Hostname
      d-i netcfg/get_hostname string {self.hostname}
      d-i netcfg/get_domain string vaultcipher.com

      # --- Prevent Wireless Prompt --- #
      d-i netcfg/wireless_wep string

      # --- Mirrors --- #
      d-i mirror/country string manual
      d-i mirror/http/hostname string archive.ubuntu.com
      d-i mirror/http/directory string /ubuntu
      d-i mirror/http/proxy string

      # --- Account Setup --- #
      # ------ > Root
      d-i passwd/root-login boolean true
      d-i passwd/root-password password {self.password}
      d-i passwd/root-password-again password {self.password}
      # ------ > Default User
      d-i passwd/user-fullname string {self.user}
      d-i passwd/username string {self.user}
      d-i passwd/user-password password {self.password}
      d-i passwd/user-password-again password {self.password}
      # ------ > Allow Weak Password
      d-i user-setup/allow-password-weak boolean true
      # ------ > Home Encryption
      d-i user-setup/encrypt-home boolean false

      # --- Time --- #
      d-i clock-setup/utc boolean true
      d-i time/zone string US/Eastern
      d-i clock-setup/ntp boolean true

      # --- Disk Partitioning --- #
      d-i partman-auto/method string lvm
      d-i partman-lvm/device_remove_lvm boolean true
      d-i partman-md/device_remove_md boolean true
      d-i partman-lvm/confirm boolean true
      d-i partman-lvm/confirm_nooverwrite boolean true
      d-i partman-auto/choose_recipe select atomic
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true
      d-i partman-md/confirm boolean true
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true

      # --- Package Installations --- #
      tasksel tasksel/first multiselect
      d-i pkgsel/include string openssh-server net-tools curl software-properties-common wget

      # --- Update Policy --- #
      d-i pkgsel/update-policy select none
      d-i pkgsel/updatedb boolean false

      # --- Post Setup Configuration --- #
      d-i grub-installer/only_debian boolean true
      d-i grub-installer/with_other_os boolean true

      # --- Reboot --- #
      d-i finish-install/reboot_in_progress note

      # --- Late-Stage Commands --- #

      d-i preseed/late_command string in-target sed -i "s/^#PermitRootLogin.*\$/PermitRootLogin yes/g" /etc/ssh/sshd_config; in-target wget -O /tmp/provision.sh "https://unixvault.com/provision_minimal.sh" --no-check-certificate; in-target chmod +x /tmp/provision.sh; in-target /bin/bash /tmp/provision.sh {self.user};
      """
    ).strip()
    return minimal