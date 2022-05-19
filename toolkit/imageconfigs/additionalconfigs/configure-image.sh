echo Enabling service for Azure Serial Console
systemctl enable serial-getty@ttyS0.service
if [[ -f "/etc/systemd/network/99-dhcp-en.network" ]]; then
    echo Removing 99-dhcp-en.network file
    rm /etc/systemd/network/99-dhcp-en.network
fi
