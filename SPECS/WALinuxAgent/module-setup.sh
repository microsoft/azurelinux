#!/usr/bin/bash
# called by dracut
check() {
    return 0
}
 
# called by dracut
depends() {
    return 0
}
 
# called by dracut
install() {
    inst_multiple chmod cut readlink
    inst_rules 66-azure-storage.rules 99-azure-product-uuid.rules
}