import os
import socket

with open("/log.txt", 'a') as fd:
    fd.write(f"Wombat\n")
    fd.write(f"Working dir: {os.getcwd()}\n")

    # Verify DNS is working.
    addrinfos = socket.getaddrinfo("microsoft.com", None)
    fd.write(f"Found DNS address: {len(addrinfos)>0}\n")
