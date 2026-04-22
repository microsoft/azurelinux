## README.fedora.md (mainly clamav-milter) 


Please note for Fedora and EPEL 7+ we use only systemd.

A clamav-milter setup consists of the following three components:

### The clamav-milter itself

  The main configuration is in /etc/mail/clamav-milter.conf and MUST
  be changed before first use.

  This can be enabled with: 'systemctl enable clamav-milter.service'

### A clamav scanner daemon

  The daemon is configured by /etc/clamd.d/scan.conf (which MUST be
  edited before first use).

  This can be enabled with: 'systemctl enable clamd@scan.service'

### The MTA (sendmail/postfix)

  --> you should know how to install this...

  When communicating across unix sockets with the clamav-milter, it is
  suggested to use the /run/clamav-milter/clamav-milter.socket
  path.  You have to add something like

    INPUT_MAIL_FILTER(`clamav', `S=local:/run/clamav-milter/clamav-milter.socket, F=, T=S:4m;R:4m')dnl

  to your sendmail.mc.

### Changing permissions of directory /var/lib/clamav  

  - Whenever ClamAV is upgraded by dnf, the permissions for the /var/lib/clamav directory change to user clamupdate  
  - If for some reason you need DatabaseOwner be another user, you may copy /usr/lib/systemd/system/clamav-freshclam.service to /etc/systemd/system/ and add ExecStartPre=+/usr/bin/chown youruser:yourgroup /var/lib/clamav and updates won't break your configuration ...
  - Please add comments to https://bugzilla.redhat.com/show_bug.cgi?id=2023371 if not work for you or if you have any suggestion.
  - Note: =+ on systemd.service (man 5 systemd.service, Special executable prefixes)  If the executable path is prefixed with "+" then the process is executed with full privileges.


EXAMPLE
=======

For clamav-milter, a possible setup might be created by

A)  On the MTA  (assumed hostname 'host-mta')

  1. Add to sendmail.mc

    | INPUT_MAIL_FILTER(`clamav', `S=inet:6666@host-milter, F=, T=S:4m;R:4m')dnl

  2. Rebuild sendmail.cf


B)  On the clamav-milter host (assumed hostname 'host-milter')

  1. Install clamav-milter + clamav-milter-upstart packages

  2. Set in /etc/mail/clamav-milter.conf

    | MilterSocket	inet:6666
    | ClamdSocket	tcp:host-scanner:6665

     and all the other options which are required on your system

  3. Enable clamav-milter.service:

    | systemctl enable clamav-milter.service

     Restart your system or execute

    | systemctl start clamav-milter.service

  4. Add something like

    | iptables -N IN-cmilt
    | iptables -A IN-cmilt -s host-mta -j ACCEPT
    | iptables -A IN-cmilt -j DROP

    | iptables -A INPUT -p tcp --dport 6666 -j IN-cmilt

     to your firewall setup

C)  On the clamav-scanner host (assumed hostname 'host-scanner')

  1. Install clamd

  2. Add to /etc/clamd.d/scan.conf

    | TCPSocket 6665
    | TCPAddr   host-scanner

     comment out possible 'LocalSocket' lines and set all the other
     options which are required on your system

  3. Enable clamd@scan.service:

    | systemctl enable clamd@scan.service

     Restart your system or execute

    | systemctl start clamd@scan.service

  4. Add something like

    | iptables -N IN-cscan
    | iptables -A IN-cscan -s host-milter -j ACCEPT
    | iptables -A IN-cscan -j DROP

    | iptables -A INPUT -p tcp --dport 6665 -j IN-csan

     to your firewall setup
