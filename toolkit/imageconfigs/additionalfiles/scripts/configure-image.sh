#!/bin/bash -x

echo "AKS image build-time configuration script"

# set boot script
chmod 744 /etc/rc.d/init.d/post-boot.sh
chmod +x /etc/rc.d/init.d/post-boot.sh

systemctl enable post-boot.service

# Disable linux agent console log
echo Logs.Console=n >> /etc/waagent.conf
echo Extensions.Enabled=y >> /etc/waagent.conf
rm /var/log/waagent.log

echo Done!
