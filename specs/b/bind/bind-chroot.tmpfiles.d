# vim: ft=conf:
# TODO: these definitions are in different form in rpm spec %files chroot section
# find a way to have it defined only once
#defattr(0664,root,named,-)
c /var/named/chroot/dev/null    0664 root named - 1:3
c /var/named/chroot/dev/random  0664 root named - 1:8
c /var/named/chroot/dev/urandom 0664 root named - 1:9
c /var/named/chroot/dev/zero    0664 root named - 1:5
#defattr(0640,root,named,0750)
d /var/named/chroot             0750 root named -
d /var/named/chroot/dev         0750 root named -
d /var/named/chroot/etc         0750 root named -
d /var/named/chroot/etc/named   0750 root named -
d /var/named/chroot/etc/pki     0750 root named -
d /var/named/chroot/etc/pki/dnssec-keys 0750 root named -
d /var/named/chroot/etc/crypto-policies 0750 root named -
d /var/named/chroot/etc/crypto-policies/back-ends 0750 root named -
d /var/named/chroot/var         0750 root named -
d /var/named/chroot/run         0750 root named -
#defattr(-,root,root,-)
d /var/named/chroot/usr             - root root -
d /var/named/chroot/usr/lib64       - root root -
d /var/named/chroot/usr/lib64/bind  - root root -
d /var/named/chroot/usr/lib64/named - root root -
d /var/named/chroot/usr/share/GeoIP - root root -
d /var/named/chroot/usr/share/named - root root -
d /var/named/chroot/proc            - root root -
d /var/named/chroot/proc/sys        - root root -
d /var/named/chroot/proc/sys/net    - root root -
d /var/named/chroot/proc/sys/net/ipv4 - root root -
#defattr(0660,root,named,01770)
d /var/named/chroot/var/named   01770 root named -
#defattr(0660,named,named,0770)
d /var/named/chroot/var/tmp      0770 named named -
d /var/named/chroot/var/log      0770 named named -
#defattr(-,named,named,-)
d /var/named/chroot/run/named       - named named -
L /var/named/chroot/var/run         - named named - ../run
