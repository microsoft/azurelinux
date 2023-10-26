# The goal of this script is to patch all the security vulnerabilities from asc baseline test result
# Below are patches for each FAIL case

# Security patch for CCE-14847-8, msid: 29
# The default umask for all users should be set to 077 in login.defs
sed -i "s/UMASK  .*/UMASK  077/g" /etc/login.defs

# Security patch for CCE-14063-2, msid: 157.7, 157.11
# Encryption must be used in shadow file
# Patched in Souce code

# Security patch for msid: 157.12
# Ensure minimum days between password changes is 7 or more
# Patched in Souce code

# Security patch for CCE-14118-4, msid: 6.6 
# Disable the installation and use of file systems that are not required (squashfs)
touch /etc/modprobe.d/squashfs.conf
echo "install squashfs /bin/true" > /etc/modprobe.d/squashfs.conf

# Security patch for msid: 66 (TO BE DONE)
# Logs should be sent to a remote loghost (using mdsd service)
# This rule can be ignore after discussing with ASC team as in C + AI we have AMA+ASA and AutoConfig instead

# Security patch for msid: 1.1.21.1 
# Ensure mounting of USB storage devices is disabled
# (Maybe patch it only for Azure) 
touch /etc/modprobe.d/usb-storage.conf
echo "install usb-storage /bin/true" > /etc/modprobe.d/usb-storage.conf

# Security patch for msid: 6.1 
# Disable the installation and use of file systems that are not required (cramfs)
touch /etc/modprobe.d/cramfs.conf
echo "install cramfs /bin/true" > /etc/modprobe.d/cramfs.conf

# Security patch for msid: 6.2 
# Disable the installation and use of file systems that are not required (freevxfs)
touch /etc/modprobe.d/freevxfs.conf
echo "install freevxfs /bin/true" > /etc/modprobe.d/freevxfs.conf

# Security patch for msid: 6.3 
# Disable the installation and use of file systems that are not required (hfs)
touch /etc/modprobe.d/hfs.conf
echo "install hfs /bin/true" > /etc/modprobe.d/hfs.conf

# Security patch for msid: 6.4 
# Disable the installation and use of file systems that are not required (hfsplus)
touch /etc/modprobe.d/hfsplus.conf
echo "install hfsplus /bin/true" > /etc/modprobe.d/hfsplus.conf

# Security patch for msid: 6.5 
# Disable the installation and use of file systems that are not required (jffs2)
touch /etc/modprobe.d/jffs2.conf
echo "install jffs2 /bin/true" > /etc/modprobe.d/jffs2.conf

# Security patch for CCE-15047-4, msid: 21
# Access to the root account via su should be restricted to the 'root' group
# Patched in Souce code

# Security patch for CCE-3818-2, msid: 31 
# All bootloaders should have password protection enabled 
# Notes: superuser=root, password=p@ssw0rd
#sed -i '$a set superusers=root' /etc/grub.d/40_custom
sed -i '$a password_pbkdf2 root grub.pbkdf2.sha512.10000.62B8C246D0B7794404AD87A2D0D56AB02DC99B42CB1F24B9743CF00E04DD67151357903842DEE1A3467138687E58FED468A55B330D3E45860916EC98FE600A23.80498C575072B93DBF272381BE4C6B6E4B0E3DDDC316A5DD5B6528E4819602474FC9B7C531AA66E5C7BF90E8679B229AEC394E0504E7F1346BD668E3B4188B3D' /boot/grub2/grub.cfg
#old='CLASS="--class gnu-linux --class gnu --class os"'
#new='CLASS="--class gnu-linux --class gnu --class os --unrestricted"'
#sed -i "s%$old%$new%g" /etc/grub.d/10_linux
#grub2-mkconfig -o /boot/grub2/grub.cfg

# Security patch for msid: 31.1
# Ensure permissions on bootloader config are configured
# Patched in Souce code

# Security patch for CCE-4186-3, msid: 38.4
# Sending ICMP redirects should be disabled for all interfaces. (net.ipv4.conf.default.accept_redirects = 0)
sysctl -w net.ipv4.conf.default.accept_redirects=0
sysctl -w net.ipv4.conf.all.accept_redirects=0
sysctl -w net.ipv6.conf.default.accept_redirects=0
sysctl -w net.ipv6.conf.all.accept_redirects=0

# Security patch for CCE-4151-7, msid: 38.5
# Sending ICMP redirects should be disabled for all interfaces. (net.ipv4.conf.default.secure_redirects = 0)
sysctl -w net.ipv4.conf.default.secure_redirects=0
sysctl -w net.ipv4.conf.all.secure_redirects=0

# Security patch for msid: 54
# Ensure DCCP is disabled
# Patched in Souce code

# Security patch for msid: 55
# Ensure SCTP is disabled
# Patched in Souce code

# Security patch for msid: 56
# Disable support for RDS
# Patched in Souce code

# Security patch for msid: 57
# Ensure TIPC is disabled
# Patched in Souce code

# Security patch for CCE-18095-0, msid: 63
# File permissions for all rsyslog log files should be set to 640 or 600
# Patched in Souce code

# Security patch for CCE-17857-4, msid: 65
# All rsyslog log files should be owned by the syslog user
# Patched in Souce code

# Security patch for CCE-4304-2, msid: 91
# File permissions for /etc/anacrontab should be set to root:root 600
# Patched in Souce code

# Security patch for msid: 93
# Ensure permissions on /etc/cron.d are configured
# Patched in Souce code

# Security patch for msid: 94
# Ensure permissions on /etc/cron.daily are configured
# Patched in Souce code

# Security patch for msid: 95
# Ensure permissions on /etc/cron.hourly are configured
# Patched in Souce code

# Security patch for msid: 96
# Ensure permissions on /etc/cron.monthly are configured
# Patched in Souce code

# Security patch for msid: 97
# Ensure permissions on /etc/cron.weekly are configured
# Patched in Souce code

# Security patch for msid: 157.5
# Ensure password reuse is limited
sed -i 's/\(try_first_pass\)/\1 remember=5/' /etc/pam.d/system-password
sed -i "/# End /d" /etc/pam.d/system-password
sed -i -e '$a# Password complexity must be enforced' /etc/pam.d/system-password
sed -i -e '$apassword requisite pam_cracklib.so ucredit=-1 lcredit=-2 dcredit=-1 ocredit=-1 retry=3 minlen=10\n' /etc/pam.d/system-password
sed -i -e '$a# End /etc/pam.d/system-password' /etc/pam.d/system-password

# Security patch for msid: 1.5.1
# Ensure core dumps are restricted
sed -i "/# End of/d" /etc/security/limits.conf
sed -i -e '$a*                hard    core            0\n' /etc/security/limits.conf
sed -i -e '$a# End of file' /etc/security/limits.conf
sysctl -w fs.suid_dumpable=0

# Security patch for msid: 5.3.1
# Ensure password creation requirements are configured
sed -i "s/# minclass = 0/minclass = 4/g" /etc/security/pwquality.conf

# Security patch for msid: 5.3.2
# Ensure lockout for failed password attempts is configured
# Patched in Souce code

# Security patch for msid: 106.11
# Ensure SSH access is limited
echo "" >> /etc/ssh/sshd_config
sed -i '$a# Ensure SSH access is limited' /etc/ssh/sshd_config
sed -i '$a#AllowUsers <userlist>' /etc/ssh/sshd_config
sed -i '$aDenyUsers <userlist>' /etc/ssh/sshd_config
sed -i '$a#DenyGroups <grouplist>' /etc/ssh/sshd_config

# Security patch for msid: 110.1
# Ensure SSH Idle Timeout Interval is configured
# Patched in Souce code

# Security patch for msid: 110.2
# Ensure SSH LoginGraceTime is set to one minute or less
# Patched in Souce code

# Security patch for CCE-4431-3, msid: 111.2
# SSH warning banner should be enabled
# Patched in Souce code

# Security patch for CCE-3932-1, msid: 12.3
# /etc/passwd- file permissions should be set to 0600
chmod 600 /etc/passwd-

# Below are patches for some SKIP cases:
# Security patch for CCE-4220-0, msid: 15
# All setgid/setuid programs on a system are owned by a package whose metadata indicates that the program's setgid bit should be set.
# Patched in Souce code

# Security patch for CCE-4220-0, msid: 18.1
# The daemon umask should be set to 027, only applied for Azure
# sed -i '$aumask 027' /etc/init/azuremonitoragent.conf

# Security patch for CCE-3762-2, msid: 157.6
# Password complexity must be enforced
# Patched in Souce code

