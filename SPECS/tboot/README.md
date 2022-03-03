# CBL-Mariner TBOOT

Platform Prerequisites: Real hardware platform that supports Intel TXT (Trusted Execution Technology) and TPM 2.0
--------------------------

Enabling TBOOT in CBL-Mariner:
1. Install the tboot rpm package

2. Check the cpu info of the platform and download the corresponding SINIT ACM module from: https://www.intel.com/content/www/us/en/developer/articles/tool/intel-trusted-execution-technology.html to /boot

3. Invoke create-drtm-policy.sh to generate the launch control policy (LCP) and verified launch control policy (VLP) and write them into the corresponding TPM NV Index

4. Add grub menu entry for booting with TBOOT DRTM using your specific settings (i.e. kernel and initramfs version, SINIT ACM module, launch control policy data file etc.), see the 
template below, which is the grub entry for TBOOT tested on a Lenovo ThinkStation for reference:

### BEGIN /etc/grub.d/20_linux_tboot ###
submenu "tboot 1.10.2" {
menuentry 'GNU/Linux, with tboot 1.10.2' --class gnu-linux --class gnu --class os --class tboot {
	insmod multiboot2
	insmod part_gpt
	insmod ext2
	set bootprefix={{.BootPrefix}}
	set bootID={{.BootUUID}}
	load_env -f $bootprefix/mariner.cfg
	if [ -f  $bootprefix/systemd.cfg ]; then
		load_env -f $bootprefix/systemd.cfg
	else
		set systemd_cmdline=net.ifnames=0
	fi
	search --no-floppy --fs-uuid --set=root $bootID
	echo	'Loading tboot 1.10.2 ...'
	multiboot2	/boot/tboot.gz logging=serial,memory
	echo	'Loading Linux kernel ...'
	module2 /boot/$mariner_linux root=UUID=$bootID ro intel_iommu=on noefi
	echo	'Loading initial ramdisk ...'
	module2 /boot/$mariner_initrd
	echo	'Loading LCP ...'
	module2 /boot/lists.data
	echo	'Loading sinit 7th_8th_gen_i5_i7-SINIT_81.bin ...'
	module2 /boot/7th_8th_gen_i5_i7-SINIT_81.bin
}
}
### END /etc/grub.d/20_linux_tboot ###

