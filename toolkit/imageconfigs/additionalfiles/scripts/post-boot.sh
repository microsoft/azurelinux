#!/bin/bash -x

echo "post-boot script"

# create and init ~/.profile
touch /root/.profile
echo "export TERM=linux" >> /root/.profile

# Fix for coredns crash
rm /etc/resolv.conf
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf

systemctl enable waagent
systemctl start waagent
