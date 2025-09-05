# Deploy PXE Server

#### Create The VMs

- Create two network switches:
  - One connected to the internet. We'll call it `External`.
  - One for use only between the VMs we create. We'll call it `Private`.
- Create the PXE server VM
  - Use a Mariner 2.0 - Baremetal vhdx.
  - Add two network adapters: `External` and `Private`.
  - Add cloud-init data iso to provision a username/password.
  - Expand disk to 10GB.
  - Start the VM.
- Create the PXE client VM
  - Assign 8GB of RAM (it will download the iso unto the RAM).
  - Add a network adapter for `Private`.
  - Do not attach any disks.

#### Install The PXE Components

- There is currently a bug where SELinux does not allow the partition to grow
  on first boot. To work around that, we disable SELinux.
  ```bash
  # Install pre-reqs
  tdnf install cloud-utils-growpart vim

  # In /boot/grub2/grub.cfg, remove selinux= and security= kernel command line
  # parameters.
  chmod 644 /boot/grub2/grub.cfg
  vim /boot/grub2/grub.cfg
  chmod 400 /boot/grub2/grub.cfg

  # In /etc/selinux/config, changing `enforcing` to `permissive`.
  vim /etc/selinux/config

  # reset cloud-init and reboot.
  cloud-init clean
  reboot

  # log-in an verify that the root partition has been expanded.
  df -h
  ```

- Enable ssh
  ```bash
  tdnf install openssh
  systemctl daemon-reload
  systemctl enable sshd
  systemctl start sshd

  # note the ips associated with the two network adapters:
  ip a
  ```

- Install PXE packages
  ```bash
  tdnf install dhcp-server atftp xinetd httpd syslinux
  systemctl daemon-reload
  ```

- Configure the network adapter connected to the private network:
  ```bash
  cat <<EOF > /etc/systemd/network/10-eth1.network 
  # Config file for eth1 second network -- /etc/systemd/network/10-eth1.network 
  [Match] 
  Name=eth1 
  [Network] 
  Address=192.168.0.1/24 
  EOF

  chmod 644 /etc/systemd/network/10-eth1.network 

  # change adapter name from e* to eth1
  vim /etc/systemd/network/99-dhcp-en.network
  ```

- Configure the DHCP server
  ```bash
  cat <<EOF > /etc/dhcp/dhcpd.conf
  # ISC dhcpd configuration file -- /etc/dhcp/dhcpd.conf
  authoritative;
  ignore client-updates;
  allow booting;
  allow bootp;
  allow unknown-clients;
  option arch code 93 = unsigned integer 16;
  option configfile code 209 = text;
  subnet 192.168.0.0 netmask 255.255.255.0 {
      range 192.168.0.8 192.168.0.254;
      # options for enabling DNS forwarding/proxying:
      # option routers 192.168.0.1;
      # option domain-name-servers 192.168.0.1;
      # option domain-name-servers 10.50.10.50;
      # option root-path "<rfs_dir>";
      ignore-client-uids true;

      class "pxeclients" {
          match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
          next-server 192.168.0.1;
          if option arch = 00:07 {
              filename "bootx64.efi";
          } else {
              filename "pxelinux.0";
          }
      }
  }
  EOF

  chmod 644 /etc/dhcp/dhcpd.conf
  systemctl enable dhcp
  systemctl start dhcp
  ```

- Configure atftpd
  ```bash
  cat <<EOF > /etc/sysconfig/atftpd
  ATFTPD_USER=tftp
  ATFTPD_GROUP=tftp
  ATFTPD_OPTIONS=--verbose=7
  ATFTPD_USE_INETD=false
  ATFTPD_DIRECTORY=/var/lib/tftpboot
  ATFTPD_BIND_ADDRESSES=192.168.0.1
  EOF

  systemctl daemon-reload 

  systemctl enable atftpd.socket 
  systemctl start atftpd.socket 

  systemctl enable atftpd.service 
  systemctl start atftpd.service 
  ```

- Disable firewall
  ```bash
  iptables -P INPUT ACCEPT
  iptables -P OUTPUT ACCEPT
  iptables -P FORWARD ACCEPT
  ```

- Configure the httpd daemon to serve additional artifacts
  ```bash
  systemctl enable httpd
  systemctl start httpd
  systemctl status httpd

  mkdir /etc/httpd/marineros
  # copy all artifacts
  # touch /etc/httpd/marineros/index.html
  # vim /etc/httpd/marineros/index.html
  chmod -R 755 /etc/httpd/marineros/

  vim /etc/httpd/conf/httpd.conf
  # right below `ServerName localhost:80`

  Alias /marineros /etc/httpd/marineros 
  <Directory /etc/httpd/marineros> 
      Options Indexes FollowSymLinks 
      AllowOverride None 
      Require all granted 
  </Directory> 

  # restart the daemons
  systemctl restart httpd
  systemctl restart atftpd

  systemctl status httpd
  systemctl status atftpd
  ```
