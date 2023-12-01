# Add short alias to see trident's logs
alias tridentlog="journalctl -u trident -u trident-networking"

# Open journalctl immediately after autologin
journalctl -f -u trident -u trident-networking