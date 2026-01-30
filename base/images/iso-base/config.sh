#!/bin/bash

set -euxo pipefail

#======================================
# Functions...
#--------------------------------------
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

#======================================
# Greeting...
#--------------------------------------
echo "Configure image: [$kiwi_iname]-[$kiwi_profiles]..."

#======================================
# Set SELinux booleans
#--------------------------------------
if [[ "$kiwi_profiles" != *"Container"* ]] && [[ "$kiwi_profiles" != *"FEX"* ]] && [[ "$kiwi_profiles" != *"WSL"* ]]; then
	## Fixes KDE Plasma, see rhbz#2058657
	if command -v setsebool >/dev/null 2>&1; then
		setsebool -P selinuxuser_execmod 1
	else
		echo "Warning: setsebool command not found, skipping SELinux configuration"
	fi
fi

#======================================
# Clear machine specific configuration
#--------------------------------------
## Clear machine-id on pre generated images
rm -f /etc/machine-id
echo 'uninitialized' > /etc/machine-id
## remove random seed, the newly installed instance should make its own
rm -f /var/lib/systemd/random-seed

#======================================
# Configure grub correctly
#--------------------------------------
if [[ "$kiwi_profiles" != *"Container"* ]] && [[ "$kiwi_profiles" != *"FEX"* ]] && [[ "$kiwi_profiles" != *"WSL"* ]]; then
	## Works around issues with grub-bls
	## See: https://github.com/OSInside/kiwi/issues/2198
	echo "GRUB_DEFAULT=saved" >> /etc/default/grub
	## Disable submenus to match Fedora
	echo "GRUB_DISABLE_SUBMENU=true" >> /etc/default/grub
	## Disable recovery entries to match Fedora
	echo "GRUB_DISABLE_RECOVERY=true" >> /etc/default/grub
	if [[ "$kiwi_profiles" == *"Disk"* ]]; then
		## Write `menu_auto_hide=1` into grubenv to match Fedora anaconda installs
		## Set boot_indeterminate to avoid displaying the grub menu on first boot
		if [[ "$kiwi_profiles" != *"Server"* ]] || [[ "$kiwi_profiles" != *"Cloud"* ]]; then
			grub2-editenv /boot/grub2/grubenv set menu_auto_hide=1 boot_indeterminate=1
		fi
	fi
fi

#======================================
# Resize root partition on first boot
#--------------------------------------

if [[ "$kiwi_profiles" == *"Disk"* ]]; then
	mkdir -p /etc/repart.d/
	cat > /etc/repart.d/50-root.conf << EOF
[Partition]
Type=root
EOF
fi

#======================================
# Delete & lock the root user password
#--------------------------------------
if [[ "$kiwi_profiles" == *"Cloud"* ]] || [[ "$kiwi_profiles" == *"Disk"* ]] || [[ "$kiwi_profiles" == *"Live"* ]] || [[ "$kiwi_profiles" == *"WSL"* ]]; then
	passwd -d root
	passwd -l root
fi

#======================================
# Setup default services
#--------------------------------------

if [[ "$kiwi_profiles" == *"Live"* ]]; then
	## Configure livesys session
	if [[ "$kiwi_profiles" == *"GNOME"* ]]; then
		echo 'livesys_session="gnome"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"KDE"* ]]; then
		echo 'livesys_session="kde"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"Budgie"* ]]; then
		echo 'livesys_session="budgie"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"Cinnamon"* ]]; then
		echo 'livesys_session="cinnamon"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"COSMIC"* ]]; then
		echo 'livesys_session="cosmic"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"i3"* ]]; then
		echo 'livesys_session="i3"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"LXDE"* ]]; then
		echo 'livesys_session="lxde"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"LXQt"* ]]; then
		echo 'livesys_session="lxqt"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"MATE_Compiz"* ]]; then
		echo 'livesys_session="mate"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"MiracleWM"* ]]; then
		echo 'livesys_session="miraclewm"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"Sway"* ]]; then
		echo 'livesys_session="sway"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"SoaS"* ]]; then
		echo 'livesys_session="soas"' > /etc/sysconfig/livesys
	fi
	if [[ "$kiwi_profiles" == *"Xfce"* ]]; then
		echo 'livesys_session="xfce"' > /etc/sysconfig/livesys
	fi
fi

#======================================
# Setup firstboot initial setup
#--------------------------------------

if [[ "$kiwi_profiles" == *"Disk"* ]]; then
	if [[ "$kiwi_profiles" != *"GNOME"* ]] && [[ "$kiwi_profiles" != *"KDE"* ]] && [[ "$kiwi_profiles" != *"COSMIC"* ]]; then
		## Enable initial-setup
		systemctl enable initial-setup.service
		## Enable reconfig mode
		touch /etc/reconfigSys
	fi
fi

#======================================
# Setup default target
#--------------------------------------
if [[ "$kiwi_profiles" != *"Container"* ]] && [[ "$kiwi_profiles" != *"FEX"* ]]; then
	if [[ "$kiwi_profiles" == *"Desktop"* ]]; then
		systemctl set-default graphical.target
	else
		systemctl set-default multi-user.target
	fi
fi

#======================================
# Setup default customizations
#--------------------------------------

if [[ "$kiwi_profiles" == *"Disk"* ]]; then
	# Find the architecture we are on
	installarch=$(uname -m)
	# Setup Raspberry Pi firmware
	if [[ $installarch == "aarch64" ]]; then
		cp -a /usr/share/uboot/rpi_arm64/u-boot.bin /boot/efi/rpi-u-boot.bin
	fi
fi

if [[ "$kiwi_profiles" == *"Server"* ]]; then
	# Trigger lvm-devices-import.path and .service to create
	# a new /etc/lvm/devices/system.devices for the root VG.
	rm -f /etc/lvm/devices/system.devices
	touch /etc/lvm/devices/auto-import-rootvg
fi

if [[ "$kiwi_profiles" == *"Azure"* ]]; then
cat > /etc/ssh/sshd_config.d/50-client-alive-interval.conf << EOF
ClientAliveInterval 120
EOF

cat >> /etc/chrony.conf << EOF
# Azure's virtual time source:
# https://docs.microsoft.com/en-us/azure/virtual-machines/linux/time-sync#check-for-ptp-clock-source
refclock PHC /dev/ptp_hyperv poll 3 dpoll -2 offset 0
EOF

# Support Azure's accelerated networking feature; without this the network fails
# to come up. It may need adjustments for additional drivers in the future.
cat > /etc/NetworkManager/conf.d/99-azure-unmanaged-devices.conf << EOF
# Ignore SR-IOV interface on Azure, since it's transparently bonded
# to the synthetic interface
[keyfile]
unmanaged-devices=driver:mlx4_core;driver:mlx5_core
EOF

# Configure DHCP timeout for Azure to retry indefinitely during VM provisioning
cat > /etc/NetworkManager/conf.d/99-azure-dhcp-timeout.conf << EOF
# Azure requires VMs to attempt DHCP for at least 300 seconds during provisioning,
# as that's the upper bound of how long Azure waits to make networking available.
# NetworkManager's ipv4.dhcp-timeout setting accepts 2147483647 as a special value
# representing infinity, which ensures DHCP keeps retrying indefinitely. This is
# more robust than a fixed timeout and matches systemd-networkd's default behavior.
# Both IPv4 and IPv6 are configured to prepare for IPv6-only scenarios.
# Reference: https://networkmanager.dev/docs/api/latest/nm-settings-nmcli.html
[connection]
ipv4.dhcp-timeout=2147483647
ipv6.dhcp-timeout=2147483647
EOF
fi

if [[ "$kiwi_profiles" == *"GCE"* ]]; then
cat <<EOF > /etc/NetworkManager/conf.d/gcp-mtu.conf
# In GCP it is recommended to use 1460 as the MTU.
# Set it to 1460 for all connections.
# https://cloud.google.com/network-connectivity/docs/vpn/concepts/mtu-considerations
[connection]
ethernet.mtu = 1460
EOF
fi

if [[ "$kiwi_profiles" == *"Vagrant"* ]]; then
sed -e 's/.*UseDNS.*/UseDNS no/' -i /etc/ssh/sshd_config
mkdir -m 0700 -p ~vagrant/.ssh
cat > ~vagrant/.ssh/authorized_keys << EOKEYS
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key
EOKEYS
chmod 600 ~vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant ~vagrant/.ssh/

cat > /etc/sudoers.d/vagrant << EOSUDOER
## Ensure the vagrant user always can use sudo
Defaults:vagrant !requiretty
vagrant ALL=(ALL) NOPASSWD: ALL
EOSUDOER
chmod 600 /etc/sudoers.d/vagrant

cat > /etc/ssh/sshd_config.d/10-vagrant-insecure-rsa-key.conf <<EOF
# For now the vagrant insecure key is an rsa key
# https://github.com/hashicorp/vagrant/issues/11783
PubkeyAcceptedKeyTypes=+ssh-rsa
EOF

# Further suggestion from @purpleidea (James Shubin) - extend key to root users as well
mkdir -m 0700 -p /root/.ssh
cp /home/vagrant/.ssh/authorized_keys /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
chown -R root:root /root/.ssh
fi

# https://bugzilla.redhat.com/show_bug.cgi?id=2356069
if [[ "$kiwi_profiles" == *"Container"* ]] && [[ "$kiwi_profiles" != *"Init"* ]]; then
	if [[ -f /usr/lib/tmpfiles.d/rootfiles.conf ]]; then
		systemd-tmpfiles --create /usr/lib/tmpfiles.d/rootfiles.conf
	fi
fi

if [[ "$kiwi_profiles" == *"Container"* ]] || [[ "$kiwi_profiles" == *"FEX"* ]]; then
	# Set install langs macro so that new rpms that get installed will
	# only install langs that we limit it to.
	LANG="en_US"
	echo "%_install_langs $LANG" > /etc/rpm/macros.image-language-conf

	# https://bugzilla.redhat.com/show_bug.cgi?id=1727489
	echo 'LANG="C.UTF-8"' >  /etc/locale.conf

	# https://bugzilla.redhat.com/show_bug.cgi?id=1400682
	echo "Import RPM GPG key"
	releasever=$(rpm --eval '%{?fedora}')

	# When building ELN containers, we don't have the %{fedora} macro
	if [ -z $releasever ]; then
		releasever=eln
	fi

	rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-primary

	echo "# fstab intentionally empty for containers" > /etc/fstab

	# Remove machine-id on pre generated images
	rm -f /etc/machine-id
	touch /etc/machine-id

	echo "# resolv placeholder" > /etc/resolv.conf
	chmod 644 /etc/resolv.conf

	# Remove extraneous files
	rm -rf /tmp/*

	# https://pagure.io/atomic-wg/issue/308
	printf "tsflags=nodocs\n" >>/etc/dnf/dnf.conf

	if [[ "$kiwi_profiles" == *"Base-Generic-Minimal"* ]]; then
		# remove some random help txt files
		rm -fv /usr/share/gnupg/help*.txt

		# Pruning random things
		rm /usr/lib/rpm/rpm.daily
		rm -rfv /usr/lib64/nss/unsupported-tools/  # unsupported

		# Statically linked crap
		rm -fv /usr/sbin/{glibc_post_upgrade.x86_64,sln}
		ln /usr/bin/ln usr/sbin/sln

		# Remove some dnf info
		rm -rfv /var/lib/dnf

		# don't need icons
		rm -rfv /usr/share/icons/*

		#some random not-that-useful binaries
		rm -fv /usr/bin/pinky

		# we lose presets by removing /usr/lib/systemd but we do not care
		rm -rfv /usr/lib/systemd
	fi
	if [[ "$kiwi_profiles" == *"Toolbox"* ]]; then
		# Remove macros.image-language-conf file
		rm -f /etc/rpm/macros.image-language-conf

		# Remove 'tsflags=nodocs' line from dnf.conf
		sed -i '/tsflags=nodocs/d' /etc/dnf/dnf.conf
	fi
fi

if [[ "$kiwi_profiles" == *"Jam"* ]]; then
# Override boot configuration in Anaconda to enable threaded IRQs
cat > /usr/share/anaconda/post-scripts/85-jam-threadirqs.ks << THREADIRQS_EOF
%post

echo "Enable threaded IRQs"
grubby --update-kernel=ALL --args="threadirqs"
%end
THREADIRQS_EOF

# Override new user configuration to add audio groups
sed -e "s/UserGroups=.*/UserGroups=wheel,jackuser,audio/" -i /etc/xdg/plasmasetuprc

# Override livesys-kde settings
cat >> /var/lib/livesys/livesys-session-extra << EOF

#setup kickoff favorites
/bin/mkdir -p /etc/skel/.config

JAMFAVORITES=/usr/share/applications/firefox.desktop,/usr/share/applications/mozilla-thunderbird.desktop,/usr/share/applications/studio-controls.desktop,/usr/share/applications/ardour6.desktop,/usr/share/applications/carla.desktop,/usr/share/applications/org.kde.konsole.desktop,/usr/share/applications/org.kde.dolphin.desktop,/usr/share/applications/systemsettings.desktop
JAMFAVORITESLIVE=/usr/share/applications/liveinst.desktop,\$JAMFAVORITES

cat <<FOE  >> /etc/skel/.config/kickoffrc
[Favorites]
FavoriteURLs=\$JAMFAVORITES
FOE

/usr/sbin/usermod -a -G jackuser,audio liveuser
EOF
fi

if [[ "$kiwi_profiles" == *"Robotics"* ]]; then

# Extend the post-configuration from the live-desktop, set default shortcuts to IDEs
cat >> /var/lib/livesys/livesys-session-extra << EOF
# disable screensaver locking
cat >> /usr/share/glib-2.0/schemas/org.gnome.desktop.screensaver.gschema.override << FOE
[org.gnome.desktop.screensaver]
lock-enabled=false
FOE

# and hide the lock screen option
cat >> /usr/share/glib-2.0/schemas/org.gnome.desktop.lockdown.gschema.override << FOE
[org.gnome.desktop.lockdown]
disable-lock-screen=true
FOE

# make the installer show up
if [ -f /usr/share/applications/liveinst.desktop ]; then
  # Show harddisk install in shell dash
  sed -i -e 's/NoDisplay=true/NoDisplay=false/' /usr/share/applications/liveinst.desktop ""
  # need to move it to anaconda.desktop to make shell happy
  mv /usr/share/applications/liveinst.desktop /usr/share/applications/anaconda.desktop

  cat >> /usr/share/glib-2.0/schemas/org.gnome.shell.gschema.override << FOE
[org.gnome.shell]
favorite-apps=['org.mozilla.firefox.desktop', 'org.qt-project.qtcreator.desktop', 'arduino.desktop', 'gnome-terminal.desktop','nautilus.desktop', 'anaconda.desktop']
FOE

fi

# rebuild schema cache with any overrides we installed
glib-compile-schemas /usr/share/glib-2.0/schemas

EOF

fi

if [[ "$kiwi_profiles" == *"Design_suite"* ]]; then
# Add link to lists of tutorials
cat >> /usr/share/applications/list-design-tutorials.desktop << FOE
[Desktop Entry]
Name=List of design tutorials
GenericName=List of Tutorials for Designers
Comment=Reference of Design Related Tutorials
Exec=xdg-open https://fedoraproject.org/wiki/Design_Suite/Tutorials
Type=Application
Icon=applications-graphics
Categories=Graphics;Documentation;
FOE
chmod a+x /usr/share/applications/list-design-tutorials.desktop

# Add information about Fedora Design Suite
cat >> /usr/share/applications/fedora-design-suite.desktop << FOE
[Desktop Entry]
Name=Design Suite Info
GenericName=About Design Suite
Comment=Wiki page of Design Suite
Exec=xdg-open https://fedoraproject.org/wiki/Design_Suite
Type=Application
Icon=applications-internet
Categories=Documentation;
FOE
chmod a+x /usr/share/applications/fedora-design-suite.desktop

# Add information about Fedora Design Team
cat >> /usr/share/applications/fedora-design-team.desktop << FOE
[Desktop Entry]
Name=Design Team Info
GenericName=About Design Team
Comment=Wiki page of Design Team
Exec=xdg-open https://fedoraproject.org/wiki/Design
Type=Application
Icon=applications-internet
Categories=Documentation;
FOE
chmod a+x /usr/share/applications/fedora-design-team.desktop

# Use Powerline in bash
cat >>  $HOME/.bashrc << FOE
# Enable powerline daemon
if [ -f `which powerline-daemon` ]; then
  powerline-daemon -q
  POWERLINE_BASH_CONTINUATION=1
  POWERLINE_BASH_SELECT=1
  . /usr/share/powerline/bash/powerline.sh
fi
FOE
# End powerline override

#Override the favorite desktop application in Dash
sed -i "s/favorite-apps=."'*'"/favorite-apps=['org.mozilla.firefox.desktop', 'shotwell.desktop', 'gimp.desktop', 'darktable.desktop','krita.desktop', 'inkscape.desktop', 'blender.desktop', 'libreoffice-writer.desktop', 'scribus.desktop', 'pitivi.desktop', 'nautilus.desktop', 'bijiben.desktop', 'anaconda.desktop', 'list-design-tutorials.desktop']/" /usr/libexec/livesys/sessions.d/livesys-gnome

# rebuild schema cache with any overrides we installed
glib-compile-schemas /usr/share/glib-2.0/schemas
fi

if [[ "$kiwi_profiles" == *"SoaS"* ]]; then
# Get proper release naming in the control panel
cat >> /boot/olpc_build << EOF
Sugar on a Stick
EOF
cat /etc/fedora-release >> /boot/olpc_build

# Set the default Plymouth theme to the Sugar Desktop one
/usr/sbin/plymouth-set-default-theme sugar

# Fix https://bugzilla.redhat.com/show_bug.cgi?id=2239137
cat > /etc/xdg/autostart/xfce-polkit.desktop <<EOF
[Desktop Entry]
Type=Application
Name=xfce-polkit
Exec=/usr/libexec/xfce-polkit
EOF

fi

#======================================
# Set the WSL name for ELN
#--------------------------------------
if [[ "$kiwi_profiles" == *"WSL"* ]] && [[ "$kiwi_iname" == *"ELN"* ]]; then
wsl-setup --name Fedora-ELN
fi

#======================================
# Finalization steps
#--------------------------------------
# Inhibit the ldconfig cache generation unit, see rhbz2348669
touch -r "/usr" "/etc/.updated" "/var/.updated"

if [[ "$kiwi_profiles" == *"FEX"* ]]; then
	# Remove most things except libraries used by FEX and wine stuff.
	# Most binaries that are present in non-x86 architectures should be removed,
	# so they do not run under emulation.

	# rm mingw static libs and headers
	rm -rf /usr/{x86_64,i686}-w64-mingw32/sys-root/mingw/{lib,include}

	# rm everything in libexec
	rm -rf /usr/libexec

	# rm everything in /usr/share except wine and mesa related stuff
	find /usr/share -mindepth 1 -maxdepth 1 \
		\! -name wine -a \
		\! -name mesa-demos -a \
		\! -name drirc.d -a \
		\! -name vulkan \
		\! -name licenses \
		-exec rm -rf {} \;

	# rm everything in /etc except /etc/alternatives and ld stuff
	find /etc -mindepth 1 -maxdepth 1 \
		\! -name alternatives -a \
		\! -name 'ld.so*' -a \
		\! -name '*.kiwi' \
		-exec rm -rf {} \;

	# rm non-libs in lib/lib64
	rm -rf /usr/{lib,lib64}/{locale,tmpfiles.d,systemd,modprobe.d,kbd,cmake}
	rm -rf /usr/{lib,lib64}/python*

	# lib/clc and lib64/clc are identical, replace with a symlink
	rm -rf /usr/lib/clc
	ln -s ../lib64/clc /usr/lib/clc

	# rm sbin except for ldconfig, we don't even have root in some setups
	find /usr/sbin -mindepth 1 -maxdepth 1 \
		\! -name 'ldconfig' \
		-exec rm -rf {} \;

	# rm misc stuff
	rm -rf /usr/{include,games,local,src,tmp}

	# Finally, remove most binaries except Wine stuff, Mesa stuff, the shell,
	# path-related stuff, and system info tools.
	find /usr/bin -mindepth 1 -maxdepth 1 \
		\! -name 'wine*' -a \
		\! -name 'mango*' -a \
		\! -name notepad -a \
		\! -name 'msi*' -a \
		\! -name regedit -a \
		\! -name regsvr32 -a \
		\! -name 'vulkan*' -a \
		\! -name 'vk*' -a \
		\! -name clinfo -a \
		\! -name eglinfo -a \
		\! -name glxinfo -a \
		\! -name ulimit -a \
		\! -name ldd -a \
		\! -name env -a \
		\! -name sh -a \
		\! -name bash -a \
		\! -name ls -a \
		\! -name stat -a \
		\! -name dirname -a \
		\! -name realpath -a \
		\! -name readlink -a \
		\! -name basename -a \
		\! -name nproc -a \
		\! -name uname -a \
		\! -name arch -a \
		\! -name rm \
		-exec rm -rf {} \;

	# Do this last for obvious reasons.
	rm /usr/bin/rm
fi

exit 0
