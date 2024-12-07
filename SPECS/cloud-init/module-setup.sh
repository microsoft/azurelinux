#!/usr/bin/bash
# called by dracut
check() {
   return 0
}
# called by dracut
depends() {
   return 0
}
# called by dracut to make sure 66-azure-ephemeral.rules is installed 
install() {
   inst_multiple cut readlink
   inst_rules 66-azure-ephemeral.rules
}

