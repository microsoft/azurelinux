# CBL-Mariner TBOOT

Platform Prerequisites: Real hardware platform that supports Intel TXT (Trusted Execution Technology) and TPM 2.0
--------------------------

Enabling TBOOT in CBL-Mariner:
1. Install the tboot rpm package

2. Check the cpu info of the platform and download the corresponding SINIT ACM module from: https://www.intel.com/content/www/us/en/developer/articles/tool/intel-trusted-execution-technology.html to /boot

3. Invoke create-drtm-policy.sh to generate the launch control policy (LCP) and verified launch control policy (VLP) and write them into the corresponding TPM NV Index

4. Modify the tboot menu entry in /boot/grub2/grub.cfg to load launch control policy and SINIT ACM bin

Eg. module2 /boot/7th_8th_gen_i5_i7-SINIT_81.bin

