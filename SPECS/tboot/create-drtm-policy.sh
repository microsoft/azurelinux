echo "1. Create hash for tboot module and store it in the mle_hash file"
sudo lcp2_mlehash --create --alg sha256 --cmdline "logging=serial,memory" /boot/tboot.gz > mle_hash

echo "2. Create the policy element for tboot"
sudo lcp2_crtpolelt --create --type mle2 --alg sha256 --ctrl 0x00 --minver 0 --out mle.elt mle_hash

echo "3. Create the policy element for the platform configuration (pconf)"
pcr0=$(sudo tpm2_pcrread | grep '0 :' | sed -n '2 p' | cut -c 9-)
pcr1=$(sudo tpm2_pcrread | grep '1 :' | sed -n '2 p' | cut -c 9-)

echo ${pcr0}
echo ${pcr1}

sudo lcp2_crtpolelt --create --type pconf2 --ctrl 0x00 --alg sha256 \
    --pcr0 ${pcr0} \
    --pcr1 ${pcr1} \
    --out pconf2.elt

echo "4. Create the unsigned policy list file list_unsig.lst, using mle_elt and pconf_elt"
sudo lcp2_crtpollist --create --listver 0x100 --out lists_unsig.lst pconf2.elt mle.elt
sudo lcp2_crtpol --create --type list --pol lists.pol --alg sha256 --sign 0x0A --ctrl 0x00 --data lists.data lists_unsig.lst

echo "5. Create an RSA key pair, and sign the policy list, list_sig.lst"
sudo openssl genrsa -out privkey.pem 2048
sudo openssl rsa -pubout -in privkey.pem -out pubkey.pem

sudo cp lists_unsig.lst lists_sig.lst
sudo lcp2_crtpollist --sign --sigalg rsa --pub pubkey.pem --priv privkey.pem --out lists_sig.lst

echo "6. Create the final LCP policy blobs from list_sig.lst, and generate the list_pol and list_data files"
sudo lcp2_crtpol --create --type list --alg sha256 --sign 0x0A --ctrl 0x00 --pol lists_sig.pol --data lists_sig.data lists_sig.lst

echo "7. Generate the tboot policy to control expected kernel and initrd"
sudo tb_polgen --create --type nonfatal --alg sha256 vl.pol

KERNEL_CMD_LINE=$(cat /proc/cmdline | cut -d ' ' -f 1 --complement)
KERNEL_IMG=$(ls /boot/ | grep vmlinuz | head -n1)
INITRD_IMG=$(ls /boot/ | grep initrd | head -n1)

echo ${KERNEL_CMD_LINE}
echo ${KERNEL_IMG}
echo ${INITRD_IMG}

sudo tb_polgen --add --num 0 --pcr none --hash image --cmdline "logging=serial,memory" --image /boot/tboot.gz vl.pol
sudo tb_polgen --add --num 1 --pcr 19 --hash image --cmdline "$KERNEL_CMD_LINE" --image /boot/${KERNEL_IMG} vl.pol
sudo tb_polgen --add --num 2 --pcr 19 --hash image --cmdline "" --image /boot/${INITRD_IMG} vl.pol

echo "8. Create the TPM NV Index for the LCP"
sudo tpm2_nvdefine 0x1c10106 -C o -s 70 -a 0x204000A

echo "9. Create the TPM NV index for the tboot policy"
sudo tpm2_nvdefine 0x1c10131 -C o -s 256 -a 0x204000A

echo "10. Write the LCP policy (lists_sig.pol) into the NV Index"
sudo tpm2_nvwrite 0x1c10106 -C o -i lists_sig.pol

echo "11. Write the VLP into the NV Index"
sudo tpm2_nvwrite 0x1c10131 -C o -i vl.pol

cp lists_sig.data /boot/lists.data
