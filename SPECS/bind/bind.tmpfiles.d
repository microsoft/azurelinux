# vim: ft=conf:
d /run/named 0755 named named -
d /var/named 01770 root named -
d /var/named/slaves  0770 named named -
d /var/named/data    0770 named named -
d /var/named/dynamic 0770 named named -
L /var/named/named.ca        0640 named named - ../../../etc/named.ca
L /var/named/named.localhost 0640 named named - ../../../usr/share/named/named.localhost
L /var/named/named.loopback  0640 named named - ../../../usr/share/named/named.loopback
L /var/named/named.empty     0640 named named - ../../../usr/share/named/named.empty
