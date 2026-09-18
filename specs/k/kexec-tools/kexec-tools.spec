# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: kexec-tools
Version: 2.0.32
Release: 1%{?dist}
URL: https://kernel.org/pub/linux/utils/kernel/kexec
License: GPL-2.0-only
Summary: The kexec/kdump userspace component

Source0: https://kernel.org/pub/linux/utils/kernel/kexec/%{name}-%{version}.tar.xz
Recommends: kdump-utils

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gcc
BuildRequires: xz-devel
BuildRequires: zlib-devel
BuildRequires: libzstd-devel

#START INSERT

#
# Patches 0 through 100 are meant for x86 kexec-tools enablement
#

#
# Patches 101 through 200 are meant for x86_64 kexec-tools enablement
#

#
# Patches 301 through 400 are meant for ppc64 kexec-tools enablement
#

#
# Patches 401 through 500 are meant for s390 kexec-tools enablement
#

#
# Patches 501 through 600 are meant for ARM kexec-tools enablement
#

#
# Patches 601 onward are generic patches


%description
kexec-tools provides /sbin/kexec binary that facilitates a new
kernel to boot using the kernel's kexec feature either on a
normal or a panic reboot. This package contains the /sbin/kexec
binary and ancillary utilities that together form the userspace
component of the kernel's kexec feature.

%prep
%autosetup -p1

%build
autoreconf
%configure \
%ifarch ppc64
    --host=powerpc64-redhat-linux-gnu \
    --build=powerpc64-redhat-linux-gnu \
%endif
%ifarch ppc64le
    --host=powerpc64le-redhat-linux-gnu \
    --build=powerpc64le-redhat-linux-gnu \
%endif
    --sbindir=%{_sbindir}

%make_build

%install
%make_install
rm -f %{buildroot}/%{_libdir}/kexec-tools/kexec_test


%files
%{_sbindir}/kexec
%{_mandir}/man8/kexec.8*
%{_sbindir}/vmcore-dmesg
%{_mandir}/man8/vmcore-dmesg.8*
%doc News
%license COPYING
%doc TODO

%changelog
* Thu Oct 16 2025 Packit <hello@packit.dev> - 2.0.32-1
- Update to version 2.0.32
- Resolves: rhbz#2404365

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May 21 2025 Coiby Xu <coxu@redhat.com> - 2.0.31-2
- Add BuildRequires libzstd-devel to support loading zstd-compressed kernel

* Tue Apr 22 2025 Packit <hello@packit.dev> - 2.0.31-1
- Update to version 2.0.31
- Resolves: rhbz#2359477

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.30-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Mon Dec 02 2024 Packit <hello@packit.dev> - 2.0.30-1
- Update to version 2.0.30
- Resolves: rhbz#2326470

* Tue Aug 06 2024 Coiby Xu <coxu@redhat.com> - 2.0.29-1
- Update to version 2.0.29
- Resolves: 2297928

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.28-13
- Rebuilt for the bin-sbin merge (again)

* Thu Jul 11 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-12
- Re-add missing build dependencies

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.28-11
- Rebuilt for the bin-sbin merge

* Thu Apr 25 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-10
- Split out kdump-utils and makedumpfile

* Thu Apr 25 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-9
- Update to makedumpfile-1.7.5

* Tue Apr 09 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-8
- Add a kdump-utils subpackage

* Sun Apr 07 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-7
- Release 2.0.28-7

* Sat Mar 16 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-6
- let kexec-tools depends on makedumpfile

* Fri Feb 23 2024 Carl George <carlwgeorge@fedoraproject.org> - 2.0.28-5
- Add a makedumpfile subpackage

* Fri Feb 02 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-4
- kexec: don't use kexec_file_load on XEN
- Fix building on x86_64 with binutils 2.41

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Coiby Xu <coxu@redhat.com> - 2.0.28-1
- kexec-tools 2.0.28 (Simon Horman)
- Use the same /etc/resolve.conf in kdump initrd if it's managed manually
- dracut-module-setup: consolidate s390 network device config

* Mon Dec 11 2023 Coiby Xu <coxu@redhat.com> - 2.0.27-5
- Let %post scriptlet always exits with the zero exit status

* Wed Nov 08 2023 Coiby Xu <coxu@redhat.com> - 2.0.27-4
- update to makedumpfile-1.7.4
- kdump-lib.sh: add extra 64M to default crashkernel if sme/sev is active
- Allow _crashkernel_add to address larger memory ranges

* Tue Oct 17 2023 Coiby Xu <coxu@redhat.com> - 2.0.27-3
- Only try to reset crashkernel when kdump.service is enabled

* Fri Oct 13 2023 Coiby Xu <coxu@redhat.com> - 2.0.27-2
- update to latest upstream kexec-tools

* Tue Oct 10 2023 Coiby Xu <coxu@redhat.com> - 2.0.27-1
- kexec-tools 2.0.27 (Simon Horman)

* Thu Aug 31 2023 Coiby Xu <coxu@redhat.com> - 2.0.27-1
- kexec-tools 2.0.27 (Simon Horman)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Coiby <coxu@redhat.com> - 2.0.26-7
- kdumpctl: Fix the matching of plus symbol by grep's EREs
- kdump-lib: Evaluate the memory consumption by smmu and mlx5 separately
- kdump-lib: add support for 64K aarch64
- kdump-lib: Introduce parse_kver_from_path() to get kernel version from its path name
- kdump-lib: Introduce a help function _crashkernel_add()

* Fri Jun 02 2023 Timothée Ravier <tim@siosm.fr> - 2.0.26-6
- Make binutils a recommend as it's only needed for UKI support

* Mon May 29 2023 Coiby <coxu@redhat.com> - 2.0.26-5
- Simplify the management of the kernel parameter crashkernel
- Let _update_kernel_cmdline return the correct return code
- mkdumprd: call dracut with --add-device to install the drivers needed by /boot partition automatically for FIPS
- kdump-lib: fix the matching pattern for debug-kernel

* Tue May 16 2023 Coiby <coxu@redhat.com> - 2.0.26-4
- kdumpctl: Add support for systemd-boot paths
- mkdumprd: add --aggressive-strip as default dracut args
- kdumpctl: Add basic UKI support
- kdumpctl: Move temp file in get_kernel_size to global temp dir
- kdumpctl: Move get_kernel_size to kdumpctl
- kdumpctl: fix is_dracut_mod_omitted
- kdump-lib: move is_dracut_mod_omitted to kdumpctl
- kdump-lib: remove get_nmcli_connection_apath_by_ifname
- kdump-lib: remove get_nmcli_field_by_conpath
- dracut-module-setup: remove dead source_ifcfg_file
- kdump-lib-initramfs: remove is_fs_dump_target
- kdump-lib-initramfs: harden is_mounted
- Show how much time kdump has waited for the network to be ready
- Tell nmcli to not escape colon when getting the path of connection profile
- kdumpctl: lower the log level in reset_crashkernel_for_installed_kernel
- Install nfsv4-related drivers when users specify nfs dumping via dracut_args
- sysconfig: add zfcp.allow_lun_scan to KDUMP_COMMANDLINE_REMOVE on s390
- Use the correct command to get architecture

* Mon Jan 30 2023 Coiby <coxu@redhat.com> - 2.0.26-3
- kdumpctl: make do_estimate more robust
- kdumpctl: refractor check_rebuild
- kdumpctl: cleanup 'stop'
- kdumpctl: cleanup 'start'
- kdump-lib: fix prepare_cmdline
- kdumpctl: move aws workaround to kdump-lib
- unit tests: add tests for prepare_cmdline
- kdump-lib: always specify version in is_squash_available
- mkfadumprd: drop unset globals from debug output
- kdumpctl: merge check_current_{kdump,fadump}_status
- dracut-early-kdump: explicitly use bash
- dracut-early-kdump: fix shellcheck findings
- kdumpctl: simplify check_failure_action_config
- makedumpfile: Fix wrong exclusion of slab pages on Linux 6.2-rc1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Coiby <coxu@redhat.com> - 2.0.26-1
- Update kexec-tools to 2.0.25
- Don't try to update crashkernel when bootloader is not installed
- dracut-module-setup.sh: also install the driver of physical NIC for Hyper-V VM with accelerated networking
- dracut-module-setup.sh: skip installing driver for the loopback interface

* Wed Dec 07 2022 Coiby <coxu@redhat.com> - 2.0.25-4
- dracut-module-setup.sh: stop overwriting dracut's trap handler
- fadump: avoid status check while starting in fadump mode
- fadump: add a kernel install hook to clean up fadump initramfs
- fadump: fix default initrd backup and restore logic
- fadump: use 'zstd' as the default compression method

* Fri Nov 25 2022 Coiby <coxu@redhat.com> - 2.0.25-3
- kdumpctl: Optimize _find_kernel_path_by_release regex string
- unit tests: adapt check_config to gen-kdump-conf.sh
- kdump.conf: use a simple generator script to maintain
- Don't run kdump_check_setup_iscsi in a subshell in order to collect needed network interfaces
- Simplify setup_znet by copying connection profile to initrd
- Wait for the network to be truly ready before dumping vmcore
- Address the cases where a NIC has a different name in kdump kernel
- Reduce kdump memory consumption by only installing needed NIC drivers
- Reduce kdump memory consumption by not letting NetworkManager manage unneeded network interfaces
- Set up kdump network by directly copying NM connection profile to initrd
- Stop dracut 35network-manager from running nm-initrd-generator
- Apply the timeout configuration of nm-initrd-generator
- Determine whether IPv4 or IPv6 is needed
- Add functions to copy NetworkManage connection profiles to the initramfs
- Fix error for vlan over team network interface
- Skip reset_crashkernel_after_update during package install
- Don't check fs modified when dump target is lvm2 thinp
- tests: use .nmconnection to set up test network
- fadump: preserve file modification time to help with hardlinking
- fadump: do not use squash to reduce image size
- selftest: Add lvm2 thin provision for kdump test
- selftest: Only iterate the .sh files for test execution
- Add dependency of dracut lvmthinpool-monitor module
- lvm.conf should be check modified if lvm2 thinp enabled
- Add lvm2 thin provision dump target checker

* Thu Oct 27 2022 Coiby <coxu@redhat.com> - 2.0.25-2
- Update makedumpfile to 1.7.2
- Skip reading /etc/defaut/grub for s390x
- Include the memory overhead cost of cryptsetup when estimating the memory requirement for LUKS-encrypted target
- Choosing the most memory-consuming key slot when estimating the memory requirement for LUKS-encrypted target
- Fix grep warnings "grep: warning: stray \ before -"
- Only try to reset crashkernel for osbuild during package install
- Prefix reset-crashkernel-{for-installed_kernel,after-update} with underscore
- Seperate dracut and dracut-squash compressor for zstd
- Fix the sync issue for dump_fs
- virtiofs support for kexec-tools
- fadump: avoid non-debug kernel use for fadump case
- mkdumprd: Improve error messages on non-existing NFS target directories
- kdumpctl: make the kdump.log root-readable-only
- sysconfig: use a simple generator script to maintain

* Wed Aug 03 2022 Coiby <coxu@redhat.com> - 2.0.25-1
- Update kexec-tools to 2.0.25
- remind the users to run zipl after calling grubby on s390x
- remove useless --zipl when calling grubby to update kernel command line
- skip updating /etc/default/grub for s390x
- use /run/ostree-booted to tell if scriptlet is running on OSTree system
- Allow to update kexec-tools using virt-customize for cloud base image
- KDUMP_COMMANDLINE: remove irqpoll parameter on aws aarch64 platform

* Thu Jul 21 2022 Coiby <coxu@redhat.com> - 2.0.24-4
- Checking the existence of 40-redhat.rules before modifying
- kdump-lib: Add the CoreOS kernel dir to the boot_dirlist
- kdump-lib: attempt to fix BOOT_IMAGE detection
- kdump-lib: change how ostree based systems are detected
- kdump-lib: clear up references to Atomic/CoreOS
- crashkernel: optimize arm64 reserved size if PAGE_SIZE=4k
- kdump-lib: use non-debug kernels first

* Mon May 23 2022 Coiby <coxu@redhat.com> - 2.0.24-3
- Update makedumpfile to 1.7.1
- unit tests: add tests for get_system_size and get_recommend_size
- improve get_recommend_size
- fix a calculation error in get_system_size
- logger: save log after all kdump progress finished

* Sun Apr 24 2022 Coiby <coxu@redhat.com> - 2.0.24-2
- remove the upper bound of default crashkernel value example
- update fadump-howto
- update kexec-kdump-howto
- update crashkernel-howto
- add man documentation for kdumpctl get-default-crashkernel
- unit tests: add check_config with with the default kdump.conf
- unit tests: add tests for kdump_get_conf_val in kdump-lib-initramfs.sh
- unit tests: add tests for "kdumpctl reset-crashkernel"
- unit tests: add tests for _{update,read}_kernel_arg_in_grub_etc_default in kdumpctl
- unit tests: add tests for kdumpctl read_proc_environ_var and _is_osbuild
- unit tests: add tests for get_dump_mode_by_fadump_val
- unit tests: add tests for get_grub_kernel_boot_parameter
- unit tests: prepare for kdumpctl and kdump-lib.sh to be unit-tested

* Mon Apr 11 2022 Coiby <coxu@redhat.com> - 2.0.24-1
- Update kexec-tools to 2.0.24
- kdumpctl: remove kdump_get_conf_val in save_raw
- kdumpctl: drop DUMP_TARGET variable
- kdumpctl: drop SSH_KEY_LOCATION variable
- kdumpctl: drop SAVE_PATH variable
- kdumpctl: reduce file operations on kdump.conf
- kdumpctl: merge check_ssh_config into check_config
- kdumpctl: simplify propagate_ssh_key
- kdumpctl: forbid aliases from ssh config
- kdumpctl: fix comment in check_and_wait_network_ready
- kdump-lib-initramfs: merge definitions for default ssh key
- kdumpctl: remove unnecessary uses of $?
- kdump-lib: fix typo in variable name
- kdump-capture.service: switch to journal for stdout
- kdumpctl/estimate: Fix unnecessary warning
- kdumpctl: sync the $TARGET_INITRD after rebuild
- try to update the crashkernel in GRUB_ETC_DEFAULT after kexec-tools updates the default crashkernel value
- address the case where there are multiple values for the same kernel arg
- update kernel crashkernel in posttrans RPM scriptlet when updating kexec-tools
- kdump-lib.sh: Check the output of blkid with sed instead of eval

* Mon Feb 14 2022 Coiby <coxu@redhat.com> - 2.0.23-5
- fix incorrect usage of _get_all_kernels_from_grubby
- fix the mistake of swapping function parameters of read_proc_environ_var

* Wed Jan 26 2022 Coiby <coxu@redhat.com> - 2.0.23-4
- fix broken kdump_get_arch_recommend_size
- remove the upper bound of 102400T for the range in default crashkernel
- fix the error of parsing the container environ variable for osbuild
- s390: handle R_390_PLT32DBL reloc entries in machine_apply_elf_rel()
- Revert "Remove trace_buf_size and trace_event from the kernel bootparameters of the kdump kernel"
- spec: only install mkfadumprd for ppc
- selftest: Add early kdump test
- selftest: run-test.sh: wait for subprocess instead of kill it

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Coiby <coxu@redhat.com> - 2.0.23-2
- fix "kdump: Invalid kdump config option auto_reset_crashkernel" error
- use grep -s to suppress error messages about nonexistent or unreadable files
- kdump-lib.sh: Escape '|' for 'failure_action|default' in is_dump_to_rootfs
- Set zstd as the default compression method for kdump initrd
- (origin/auto_reset_crashkernel, auto_reset_crashkernel) update crashkernel-howto
- set up kernel crashkernel for osbuild in kernel hook
- reset kernel crashkernel for the special case where the kernel is updated right after kexec-tools
- try to reset kernel crashkernel when kexec-tools updates the default crashkernel value
- introduce the auto_reset_crashkernel option to kdump.conf
- rewrite reset_crashkernel to support fadump and to used by RPM scriptlet
- fix incorrect usage of rpm-ostree to update kernel command line parameters
- add helper functions to get kernel path by kernel release and the path of current running kernel
- add helper functions to get dump mode
- add a helper function to read kernel cmdline parameter from grubby --info
- provide kdumpctl get-default-crashkernel for kdump_anaconda_addon and RPM scriptlet
- factor out kdump_get_arch_recommend_crashkernel
- update default crashkernel value
- kdumpctl: remove some legacy code
- dracut-early-kdump-module-setup.sh: install xargs and kdump-lib-initramfs.sh
- ppc64/ppc64le: drop cpu online rule in 40-redhat.rules in kdump initramfs
- kdump/ppc64: suppress the error message "Could not find a registered notification tool" from servicelog_notify
- add keytuils as a weak dependency for POWER
- Document/kexec-kdump-howto.txt: improve notes for kdump_pre and kdump_post scripts
- sysconfig: make kexec_file_load as default option on ppc64le
- sysconfig: make kexec_file_load as default option on aarch64
- Enable zstd compression for makedumpfile in kexec-tools.spec

* Thu Nov 18 2021 Coiby <coxu@redhat.com> - 2.0.23-1
- Update kexec-tools to 2.0.23
- Rebase makedumpfile to 1.7.0
- fix broken extra_bins when installing multiple binaries
- mkdumprd: drop mountaddr/mountproto nfs mount options
- selftest: kill VM reliably by recursively kill children processes

* Thu Sep 16 2021 Kairui Song <kasong@redhat.com> - 2.0.22-8
- 92-crashkernel.install: fix exit code
- dracut-early-kdump.sh: make it POSIX compatible
- Add header comment for POSIX compliant scripts
- mkdumprd: allow using dash
- kdump-logger.sh: make it POSIX compatible
- kdump-lib.sh: reformat with shfmt
- kdump-lib.sh: declare and assign separately
- kdump-lib.sh: fix variable quoting issue
- kdump-lib.sh: fix a few ambiguous or redundant code
- kdump-lib.sh: fix arithmetic operation syntax
- kdump-lib.sh: remove useless echo and cat
- kdump-lib.sh: rework nmcli related functions
- kdump-lib.sh: replace '[ ]' with '[[ ]]' and get rid of legacy ``
- kdump-lib-initramfs.sh: make it POSIX compatible
- dracut-kdump.sh: reformat with shfmt
- dracut-kdump.sh: make it POSIX compatible
- dracut-kdump.sh: POSIX doesn't support pipefail
- dracut-kdump.sh: Use stat instead of ls to get vmcore size
- dracut-kdump.sh: simplify dump_ssh
- dracut-kdump.sh: remove add_dump_code
- dracut-kdump.sh: don't put KDUMP_SCRIPT_DIR in PATH
- kdump-lib-initramfs.sh: move dump related functions to kdump.sh
- Merge kdump-error-handler.sh into kdump.sh
- kdump-lib-initramfs.sh: prepare to be a POSIX compatible lib
- bash scripts: reformat with shfmt
- bash scripts: declare and assign separately
- bash scripts: fix redundant exit code check
- bash scripts: fix variable quoting issue
- bash scripts: replace '[ ]' with '[[ ]]' for bash scripts
- bash scripts: use $(...) notation instead of legacy `...`
- bash scripts: always use "read -r"
- bash scripts: get rid of unnecessary sed calls
- bash scripts: get rid of expr and let
- bash scripts: remove useless cat
- dracut-module-setup.sh: remove surrounding $() for subshell
- dracut-module-setup.sh: make iscsi check fail early if cd failed
- dracut-module-setup.sh: fix a loop over ls issue
- dracut-module-setup.sh: fix a ambiguous variable reference
- dracut-module-setup.sh: use "*" to expend array as string
- dracut-module-setup.sh: fix _bondoptions wrong references
- dracut-module-setup.sh: remove an unused variable
- dracut-module-setup.sh: rework kdump_get_ip_route_field
- mkfadumprd: make _dracut_isolate_args an array
- mkdumprd: use array to store ssh arguments in mkdir_save_path_ssh
- mkdumprd: remove an awk call in get_fs_size
- mkdumprd: fix multiple issues with get_ssh_size
- mkdumprd: remove some redundant echo
- mkdumprd: make dracut_args an array again
- mkdumprd: use kdump_get_conf_val to read config values
- kdumpctl: refine grep usage
- kdumpctl: fix fragile loops over find output
- kdumpctl: use kdump_get_conf_val to read config values
- kdump-lib.sh: use kdump_get_conf_val to read config values
- kdump-lib.sh: add a config value retrive helper
- kdump-lib.sh: add a config format and read helper
- Add a .editorconfig file

* Tue Aug 31 2021 Adam Williamson <awilliam@redhat.com> - 2.0.22-7
- Don't exit 1 from 92-crashkernel.install if zipl is absent (#1993505)

* Fri Aug 20 2021 Kairui Song <kasong@redhat.com> - 2.0.22-6
- Remove hard requirement on grubby
- Clear old crashkernl=auto in comment and doc
- kdump/ppc64: migration action registration clean up
- Check the existence of /sys/bus/ccwgroup/devices/*/online beforehand
- Make `dump_to_rootfs` wait for 90s for real
- Update crashkernel-howto.txt
- kdump/ppc64: rebuild initramfs image after migration
- kdump.sysconfig.s390: Remove "prot_virt" from kdump kernel cmdline
- kdumpctl: fix a typo
- Remove references to systemd-sysv-convert
- kdump-lib.sh: kdump_get_arch_recommend_size uses crashkernel.default
- Revert "Revert "x86_64: enable the kexec file load by default""
- Cleanup dead systemd services before start sysroot.mount
- Add a crashkernel-howto.txt doc
- Add a new hook: 92-crashkernel.install
- kdumpctl: Add kdumpctl reset-crashkernel
- Revert "kdump-lib.sh: Remove is_atomic"
- fadump-init: clean up mount points properly
- fadump: kdumpctl should check the modules used by the fadump initramfs
- fadump: isolate fadump initramfs image within the default one

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Kairui Song <kasong@redhat.com> - 2.0.22-4
- fix format issue in find_online_znet_device
- check the existence of /sys/bus/ccwgroup/devices before trying to find online network device
- check for invalid physical address of /proc/kcore when making ELF dumpfile
- check for invalid physical address of /proc/kcore when finding max_paddr
- Increase SECTION_MAP_LAST_BIT to 5

* Sun Jun 20 2021 Kairui Song <kasong@redhat.com> - 2.0.22-3
- selftest: Make test_base_image depends on EXTRA_RPMS
- selftest: fix the error of misplacing double quotes
- mkdumprd: display the absolute path of dump location in the check_user_configured_target()
- Iterate /sys/bus/ccwgroup/devices to tell if we should set up rd.znet
- Use a customized emergency shell
- Remove the kdump error handler isolation wrapper
- Don's try to restart dracut-initqueue if it's already there
- kdump-lib.sh: fix a warning in prepare_kdump_bootinfo()
- kdump-lib.sh: fix the case if no enough total RAM for kdump in get_recommend_size()
- kdumpctl: Add kdumpctl estimate
- mkdumprd: make use of the new get_luks_crypt_dev helper
- kdump-lib.sh: introduce a helper to get all crypt dev used by kdump
- kdump-lib.sh: introduce a helper to get underlying crypt device

* Thu May 13 2021 Kairui Song <kasong@redhat.com> - 2.0.22-2
- Disable CMA in kdump 2nd kernel
- Warn the user if network scripts are used
- Set up bond cmdline by "nmcli --get-values"
- Set up dns cmdline by parsing "nmcli --get-values"
- Set up s390 znet cmdline by "nmcli --get-values"
- Add helper to get nmcli connection show cmd by ifname
- Add helper to get nmcli connection apath by ifname
- Add helper to get value by field using "nmcli --get-values"
- Update makedumpfile to 1.6.9

* Tue May 11 2021 Kairui Song <kasong@redhat.com> - 2.0.22-1
- Update kexec-tools to 2.0.22
- rd.route should use the name from kdump_setup_ifname
- get kdump ifname once in kdump_install_net
- Fix incorrect file permissions of vmcore-dmesg-incomplete.txt
- Revert "Always set vm.zone_reclaim_mode = 3 in kdump kernel"
- kdumpctl: fix check_config error when kdump.conf is empty

* Wed Apr 28 2021 Kairui Song <kasong@redhat.com> - 2.0.21-9
- Make dracut-squash required for kexec-tools
- Show write byte size in report messages
- Add shorthand --show-stats option to show report stats
- Add --dry-run option to prevent writing the dumpfile
- fadump: fix dump capture failure to root disk
- Write to `/var/lib/kdump` if $KDUMP_BOOTDIR not writable
- Drop dependency on ipcalc
- Implement IP netmask calculation to replace "ipcalc -m"
- Don't use die in dracut-module-setup.sh
- Don't iterate the whole /sys/devices just to find drm device

* Sat Apr 03 2021 Kairui Song <kasong@redhat.com> - 2.0.21-8
- Update eppic to latest upstream snapshot
- mkdumprd: prompt the user to install nfs-utils when mounting NFS fs failed
- Fix incorrect permissions on kdump dmesg file
- Fix incorrect vmcore permissions when dumped through ssh
- (origin/main) Stop reloading kdump service on CPU hotplug event for FADump
- Rebuilt for updated systemd-rpm-macros
- fadump: improve fadump-howto.txt about remote dump target setup
- kdumpctl: enable secure boot on ppc64le LPARs
- add dependency on ipcalc

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.21-7
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 08 2021 Kairui Song <kasong@redhat.com> - 2.0.21-6
- Remove trace_buf_size and trace_event from the kernel bootparameters of the kdump kernel
- kdump-lib.sh: introduce functions to return recommened mem size

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Kairui Song <kasong@redhat.com> - 2.0.21-4
- dracut-module-setup.sh: enable ForwardToConsole=yes in fadump mode
- kdump.conf: add ipv6 example for nfs and ssh dump
- fix kdump failure of saving vmcore with the scp + ipv6 method

* Wed Jan 20 2021 Kairui Song <kasong@redhat.com> - 2.0.21-3
- module-setup.sh: don't polute the namespace unnecessarily
- module-setup.sh: don't source $dracutfunctions
- logger: source the logger file individually
- Fix dump_fs mount point detection and fallback mount
- Revert "Don's try to restart dracut-initqueue if it's already failed"
- Revert "Append both nofail and x-systemd.before to kdump mount target"
- Doc: Improve the kdump sysconfig document
- kdump.conf: Update doc about core_collector for ssh target
- Merge #4 `Make dracut-squash a weak dep`
- Fix a date error in the change log

* Fri Jan 08 2021 Kairui Song <kasong@redhat.com> - 2.0.21-2
- makedumpfile: make use of 'uts_namespace.name' offset in VMCOREINFO
- kdumpctl: fix a variable expansion in check_fence_kdump_config()
- Add BuildRequires: make
- Save the final failure information to log file if saving vmcore failed

* Wed Dec 23 2020 Kairui Song <kasong@redhat.com> - 2.0.21-1
- makedumpfile: printk: use committed/finalized state values
- makedumpfile: printk: add support for lockless ringbuffer
- dracut-module-setup.sh: Use systemctl call to replace ln_r
- Doc: improve mkdumprd man page
- Don's try to restart dracut-initqueue if it's already failed
- dracut-module-setup.sh: use auto6 for ipv6

* Mon Nov 30 2020 Kairui Song <kasong@redhat.com> - 2.0.20-21
- Rebase makedumpfile to 1.6.8
- fadump-howto: update about 'nocma' and 'off' options for 'fadump=' parameter
- module-setup.sh: enable vlan on team interface
- kdump-lib: Fix get_bind_mount_source to support btrfs and fstab
- Make get_mount_info work with bind mount
- Set watchdog's pretimeout to zero in kdump kernel
- kdump-lib.sh: Use a more generic helper to detect omitted dracut module
- Fix the watchdog drivers detection code
- Add a helper for detecting watchdog drivers
- Remove a redundant nfs check
- kdumpctl: split the driver detection from fs dection function

* Thu Nov 19 2020 Kairui Song <kasong@redhat.com> - 2.0.20-20
- selftest: Fix several test issue with Fedora 33
- selftest: add more detailed log and fix a test failure issue
- selftest: Update test base image to Fedora 33
- selftest: Fix qcow2 image format detect
- selftest: Always use the get_image_fmt helper
- Doc: improve the usage documentation of the logger
- Update the kdump sysconfig
- Capitalize the configuration name of log level
- Add the rd.kdumploglvl option to control log level in the second kernel
- Appropriately converts logger numeric level to syslog log level
- Remove unused log levels for kdump logger
- Add sanity checks for the log levels
- Move watchdog detect and install code to module-setup.sh
- Add a helper to omit non-mandatory dracut module
- Move some dracut module dependencies checks to module-setup.sh
- Add code comments to help better understanding

* Thu Nov 05 2020 Kairui Song <kasong@redhat.com> - 2.0.20-19
- Fix comment about ssh dump target
- mkdumprd: Ensure kdumpbase is added
- kdump.service: use ConditionKernelCommandLine=crashkernel
- Revert "Revert "s390x: enable the kexec file load by def
- increase makdumpfile default message level to 7
- Fix error when using raw target with opalcore
- module-setup.sh: Instead of drop journalctl log, just don't read kmsg
- Doc: add a documentation for the usage of logger
- Improve debugging in the kdump kernel
- kdumpctl: add the '-d' option to enable the kexec loading debugging messages
- kdump.sysconfig: add the kdump logger configurations
- enable the logger for kdump
- introduce the kdump logger from the dracut
- Rework check_config and warn on any duplicated option
- (watchdog) kdump-lib.sh: detect secure boot on s390
- Don't drop journalctl content if failure action is "shell"
- dracut-module-install: Move systemd conf install code to a function
- selftest: Show the path of dumped vmcore on test end
- selftest: Add document for selftests
- selftest: Add basic test framework
- selftest: Add basic infrastructure to build test image

* Thu Aug 27 2020 Kairui Song <kasong@redhat.com> - 2.0.20-18
- mkdumprd: Improve the warning message when using encrypted target
- kdump-lib.sh: Remove is_atomic
- Refactor kernel image and initrd detection code
- early-kdump: Use consistent symbol link for kernel and initramfs
- Add a kernel install hook to clean up kdump initramfs

* Tue Aug 04 2020 Kairui Song <kasong@redhat.com> - 2.0.20-17
- Drop static lib dependencies
- Revert "x86_64: enable the kexec file load by default"
- Revert "s390x: enable the kexec file load by default"
- kdumpctl: exit if either pre.d or post.d is missing
- kdump_pre: make notes more precise
- dracut-kdump.sh: exit shell when machine reboot
- kdumpctl: detect modification of scripts by its directory's timestamp
- module-setup.sh: suppress false alarm
- kexec-tools.spec: make the existence of pre.d and post.d mandatory
- ppc64/kdump: use kexec_file_load when secureboot is enabled

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-16
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 1 2020 Kairui Song <kasong@redhat.com> - 2.0.20-14
- s390x: enable the kexec file load by default
- x86_64: enable the kexec file load by default
- Revert "s390x: add kdump sysconfig option to use the kexec_file_load() syscall"
- Revert "kdump-lib: switch to the kexec_file_load() syscall on x86_64 by default"
- kdump.conf: fix a grammar issue
- man: improve description about /etc/kdump/{pre.d,post.d}interface
- mkdumprd: Improve the error message for umounted dump target
- mkdumprd: Fix nfs detection in to_mount
- Always wrap up call to dracut get_persistent_dev function
- s390x: add kdump sysconfig option to use the kexec_file_load() syscall
- mkdumprd: Fix dracut error on multiple extra_modules
- Fix kdump failure when mount target specified by dracut_args
- kdump.conf: Specify /etc/kdump/{pre.d,post.d}interface
- dracut-kdump.sh: Execute the binary and script filesin /etc/kdump/{pre.d,post.d}
- kdumpctl: Check the update of the binary and script files in /etc/kdump/{pre.d,post.d}
- dracut-module-setup.sh: Install files under /etc/kdump/{pre.d,post.d} into kdump initramfs
- Drop switch root capability for non fadump initramfs
- fadump: update fadump-howto.txt with some more troubleshooting help
- fadump-howto.txt: source it in spec file
- Don't inherit swiotlb parameter form 1st kernel by default
- module-setup.sh: Add "rd.neednet" parameter if network is needed
- Revert "Add a hook to wait for kdump target in initqueue"
- kdump.sysconfig: Remove the option 'log_buf_len' from kdump command line

* Fri May 22 2020 Kairui Song <kasong@redhat.com> - 2.0.20-13
- Update docs for the new noauto dump target support
- kexec-kdump-howto.txt: Add some format to the document
- mkdumprd: generate usable kdump initramfs even target is not mounted
- User get_mount_info to replace findmnt calls
- kdump-lib.sh: add fstab failback helper for getting mount info
- Allow calling mkdumprd from kdumpctl even if targat not mounted
- Add a is_mounted helper
- Introduce get_kdump_mntpoint_from_target and fix duplicated /
- Append both nofail and x-systemd.before to kdump mount target
- Fix the problem that kdump prints redundant /
- Partially Revert "Don't mount the dump target unless needed"
- fadump: update fadump-howto.txt with some troubleshooting help
- Add a new option 'rd.znet_ifname' in order to use it in udev rules
- Don't unmount the dump target just after saving vmcore
- dracut-module-setup.sh: fix breakage in get_pcs_fence_kdump_nodes()
- dracut-module-setup.sh: ensure cluster info is ready before query

* Thu Apr 2 2020 Kairui Song <kasong@redhat.com> - 2.0.20-12
- Remove adjust_bind_mount_path call
- No longer treat atomic/silverblue specially
- mkdumprd: Simplify handling of user specified target
- mkdumprd: Use get_save_path instead of parsing config
- Remove is_dump_target_configured
- dracut-module-setup.sh: improve get_alias()

* Tue Mar 24 2020 Kairui Song <kasong@redhat.com> - 2.0.20-11
- Fix a potential syntax error
- Use read_strip_comments to filter the installed kdump.conf
- kdumpctl: fix driver change detection on latest Fedora
- kdumpctl: check hostonly-kernel-modules.txt for kernel module
- dracut-module-setup.sh: Ensure initrd.target.wants dir exists
- mkdumprd: Use DUMP_TARGET which printing error message during ssh
- kdump-lib.sh: Fix is_user_configured_dump_target()
- mkdumprd: Use makedumpfile --check-params option
- makedumpfile: Introduce --check-params option
- Improves the early-kdump-howto.txt document in several points:

* Thu Feb 13 2020 Kairui Song <kasong@redhat.com> - 2.0.20-10
- Add --force option to step 2 in early-kdump-howto.txt
- Fix typo in early-kdump-howto.txt
- kexec-tools/module-setup: Ensure eth devices get IP address for VLAN
- powerpc: enable the scripts to capture dump on POWERNV platform
- kdump-lib: switch to the kexec_file_load() syscall on x86_64 by default

* Wed Jan 29 2020 Kairui Song <kasong@redhat.com> - 2.0.20-9
- Fix building failure

* Wed Jan 29 2020 Kairui Song <kasong@redhat.com> - 2.0.20-8
- Update makedumpfile to 1.6.7
- Add a hook to wait for kdump target in initqueue
- Always install sed and awk
- Fix potential ssh/nfs kdump failure of missing "ip" command
- kdump-lib.sh: Fix is_nfs_dump_target
- Always use get_save_path to get the 'path' option
- kdump-lib: Don't abuse echo, and clean up

* Sun Dec 29 2019 Kairui Song <kasong@redhat.com> - 2.0.20-7
- Fix building failure due to makedumpfile's compile flag
- mkdumprd: Fix dracut args parsing

* Thu Nov 28 2019 Kairui Song <kasong@redhat.com> - 2.0.20-6
- kdump-error-handler.service: Remove ExecStopPost
- mkdumprd: simplify dracut args parsing
- Always set vm.zone_reclaim_mode = 3 in kdump kernel
- kdumpctl: make reload fail proof
- spec: move binaries from /sbin to /usr/sbin
- Don't execute final_action if failure_action terminates the system
- module-setup.sh: Simplify the network setup code
- mkdumprd: ensure ssh path exists before check size
- module-setup: re-fix 99kdumpbase network dependency
- kdumpctl: bail out immediately if host key verification failed

* Tue Oct 15 2019 Kairui Song <kasong@redhat.com> - 2.0.20-5
- Don't mount the dump target unless needed
- kdump-lib: strip grub device from kdump_bootdir
- Add systemd-udev require.

* Tue Sep 24 2019 Kairui Song <kasong@redhat.com> - 2.0.20-4
- kdumpctl: echo msg when waiting for connection
- makedumpfile: Fix inconsistent return value from find_vmemmap()
- makedumpfile: Fix exclusion range in find_vmemmap_pages()
- makedumpfile: x86_64: Fix incorrect exclusion by -e option with KASLR
- kdumpctl: distinguish the failed reason of ssh
- kexec-kdump-howto.txt: Add notes about device dump
- Disable device dump by default
- dracut-module-setup: fix bond ifcfg processing
- dracut-module-setup: filter out localhost for generic_fence_kdump
- dracut-module-setup: get localhost alias by manual

* Mon Aug 12 2019 Kairui Song <kasong@redhat.com> - 2.0.20-3
- kdumpctl: wait a while for network ready if dump target is ssh
- makedumpfile: Increase SECTION_MAP_LAST_BIT to 4
- makedumpfile: Do not proceed when get_num_dumpable_cyclic() fails
- Don't forward and drop journalctl logs for fadump

* Fri Aug 02 2019 Kairui Song <kasong@redhat.com> - 2.0.20-2
- x86: Fix broken multiboot2 buliding for i386
- dracut-module-setup.sh: skip alias of localhost in get_pcs_fence_kdump_nodes()

* Wed Jul 31 2019 Kairui Song <kasong@redhat.com> - 2.0.20-1
- Update makedumpfile to 1.6.6
- dracut-module-setup.sh: Don't use squash module for fadump
- Forward logs in kdump kernel to console directly
- kdump.sysconfig/x86_64: Disable HEST by default
- dracut-kdump-capture.service: Use OnFailureJobMode instead of deprecated OnFailureIsolate
- makedumpfile: x86_64: Add support for AMD Secure Memory Encryption
- aarch64/kdump.sysconfig: Make config options similar to x86_64
- Add aarch64 specific kdump.sysconfig and use 'nr_cpus' instead of 'maxcpus'
- kdumpctl: check for ssh path availability when rebuild
- kdumpctl: Check kdump.conf for error when rebuild is called

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Kairui Song <kasong@redhat.com> - 2.0.19-2
- kdumpctl: don't always rebuild when extra_modules is set
- kdumpctl: follow symlink when checking for modified files
- Get rid of duplicated strip_comments when reading config
- earlykdump: provide a prompt message after the rebuilding of kdump initramfs.
- kexec-kdump-howto.txt: Add document about encrypted targets
- kexec-kdump-howto.txt: Add document about initramfs rebiuld
- kdumpctl: Detect block device driver change for initramfs rebuild
- Revert "kdumpctl: Rebuild initramfs if loaded kernel modules changed"
- kexec.rules: create dedicated udev rules for ppc64
- kexec-kdump-howto: Add note on setting correct value of kptr_restrict
- Update man page for new kdumpctl command: reload / rebuild
- kdumpctl: add rebuild support
- mkdumprd: Improve the config reading logic

* Fri Mar 22 2019 Kairui Song <kasong@redhat.com> - 2.0.19-1
- Update eppic to latest snapshot
- fadump: leverage kernel support to re-regisgter FADump
- fadump: use the original initrd to rebuild fadump initrdfrom

* Fri Feb 22 2019 Kairui Song <kasong@redhat.com> - 2.0.18-5
- Update eppic to latest upstream snapshot
- Enable building with hardening flags
- Remove unused patches
- Remove obsolete Group tag
- mkdumprd: refine regex on dropping mount options

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Kairui Song <kasong@redhat.com> - 2.0.18-3
- earlykdump: Add a note of final_action option to avoid crash loop
- Add final_action option to kdump.conf
- Add failure_action as alias of default and make default obsolete
- mkdumprd: force drop earlykdump module
- earlykdump: warn when installed kernel version differs from dracut target
- earlykdump: add more sanity check when generating initramfs
- earlykdump: generate symlink with stable name to kernel image and iniramfs
- earlykdump: fix kexec fails to load the early kdump kernel
- mkdumprd: allow spaces after 'path' config phrase with network dump setting
- dracut-module-setup: Don't build squashed image if required modules are missing
- kdump-lib-initramfs.sh: using -force option when poweroff

* Fri Dec 7 2018 Kairui Song <kasong@redhat.com> - 2.0.18-2
- Update makedumpfile 1.6.5
- Make udev reload rules quiet during bootup
- dracut-module-setup: Fix routing failure on multipath route
- mkdumprd: drop some nfs mount options when reading from kernel
- doc/kdump.conf: Local dump path should be <mnt>/<path>/%HOST_IP-%DATE
- As /etc/kdump.conf timestamp is updated do not compare it when doing rpm --verify
- Add missing usage info

* Mon Nov 5 2018 Kairui Song <kasong@redhat.com> - 2.0.18-1
- Update to kexec-tools 2.0.18

* Thu Nov 1 2018 Kairui Song <kasong@redhat.com> - 2.0.17-12
- Throttle kdump reload request triggered by udev event
- Rewrite kdump's udev rules
- kdumpctl: Add reload support

* Mon Oct 15 2018 Kairui Song <kasong@redhat.com> - 2.0.17-11
- Enable dracut squash module
- kdumpctl: Print warning in case the raw device is formatted and contains filesystem
- kdump-lib-initramfs.sh: Add check to remount to rw mode only if dump target is ro

* Wed Aug 22 2018 Kairui Song <kasong@redhat.com> - 2.0.17-10
- kexec: fix for "Unhandled rela relocation: R_X86_64_PLT32" error
- kdumpctl: Error out if path is set more than once
- Always drop nofail or nobootwait options

* Tue Aug 07 2018 Kairui Song <kasong@redhat.com> - 2.0.17-9
- Remove redundant kdump-anaconda-addon source codes
- dracut-module-setup: Fix DRM module inclusion test for hyper-v
- Remove kdump-anaconda subpackage

* Thu Jul 26 2018 Dave Young <dyoung@redhat.com> - 2.0.17-8
- Fix armv7hl build failure

* Thu Jul 26 2018 Dave Young <dyoung@redhat.com> - 2.0.17-7
- Remove koji build workaround patch
- kexec-tools.spec: Drop kexec-tools-2.0.3-disable-kexec-test.patch
- Remove obsolete kdump tool
- dracut-module-setup.sh: don't include multipath-hostonly
- kdumpctl: Rebuild initramfs if loaded kernel modules changed

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 9 2018 Dave Young <dyoung@redhat.com> - 2.0.17-5
- Update makedumpfile 1.6.4
- dracut-module-setup.sh: pass ip=either6 param for ipv6
- dracut-module-setup.sh: install /etc/hosts when using fence_kdump

* Wed Jun 27 2018 Dave Young <dyoung@redhat.com> - 2.0.17-4
- kdump anaconda addon fix for rhbz1594827

* Wed May 30 2018 Dave Young <dyoung@redhat.com> - 2.0.17-3
- Add early kdump support in initramfs.
- move some common functions from kdumpctl to kdump-lib.sh
- Fix kdumpctl showmem
- kdumpctl: Remove 'netroot' and 'iscsi initiator' entries from kdump
- kdumpctl: add showmem cmd
- Revert "dracut-module-setup.sh: pass correct ip= param for ipv6"

* Sat Apr 28 2018 Dave Young <dyoung@redhat.com> - 2.0.17-2
- pull in makedumpfile 1.6.3

* Sat Apr 28 2018 Dave Young <dyoung@redhat.com> - 2.0.17-1
- pull in 2.0.17

* Sun Apr 08 2018 Dave Young <dyoung@redhat.com> - 2.0.16-6
- kdump.sysconfig.ppc64(le): remove "root=" param from ppc64(le) 2nd kernel
- kdumpctl: Check the modification time of core_collector
- dracut-module-setup.sh: pass correct ip= param for ipv6

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.16-5
- Escape macros in %%changelog

* Wed Feb 7 2018 Dave Young <dyoung@redhat.com> - 2.0.16-4
- update anaconda addon migrate with Anaconda changes.

* Fri Dec 8 2017 Dave Young <dyoung@redhat.com> - 2.0.16-3
- workaround koji build failure (rhbz1520805)

* Mon Dec 4 2017 Dave Young <dyoung@redhat.com> - 2.0.16-2
- dracut-module-setup.sh: check whether to include multipath-hostonly or not
- Revert "kdumpctl: sanity check of nr_cpus for x86_64 in case running out of vectors"
- kdumpctl: skip selinux-relabel for dracut_args --mount dump target

* Tue Nov 21 2017 Dave Young <dyoung@redhat.com> - 2.0.16-1
- update to kexec-tools 2.0.16

* Thu Nov 9 2017 Dave Young <dyoung@redhat.com> - 2.0.15-15
- Use absolute path /usr/bin/dracut in mkdumprd

* Wed Oct 11 2017 Dave Young <dyoung@redhat.com> - 2.0.15-14
- kdumpctl: Error out in case there are white spaces before an option name

* Wed Sep 6 2017 Dave Young <dyoung@redhat.com> - 2.0.15-13
- dracut-module-setup.sh: eliminate redundant kdump_get_mac_addr call
- mkdumprd: use --quiet dracut argument to speedup initramfs build
- mkdumprd: fix patterns to modify mount options
- fadump: rebuild default initrd with dump capture capability
- module-setup: remove software iscsi cmdline generated by dracut
- kdumpctl: remove some cmdline inheritage from 1st kernel
- mkdumprd: apply dracut "--hostonly-cmdline" and "--no-hostonly-default-device"
- Change dump_to_rootfs to use "--mount" instead of "root=X"
- kdumpctl: move is_fadump_capable() to kdump-lib.sh
- Revert "kdumpctl: use generated rd.lvm.lv=X"
- Revert "mkdumprd: omit crypt when there is no crypt kdump target"
- Revert "mkdumprd: omit dracut modules in case of no dm target"
- Revert "mkdumprd: omit dracut modules in case of network dumping"
- update bogus date in rpm spec

* Thu Aug 17 2017 Dave Young <dyoung@redhat.com> - 2.0.15-12
- makedumpfile: fix 4.13 kernel larget vmcore bug
- Revert "Improve 'cpu add' udev rules"

* Tue Aug 15 2017 Dave Young <dyoung@redhat.com> - 2.0.15-11
- Own the /usr/share/makedumpfile dir
- Mark COPYING as %%license

* Tue Aug 8 2017 Dave Young <dyoung@redhat.com> - 2.0.15-10
- Improve 'cpu add' udev rules
- module-setup: suppress the early iscsi error messages
- mkdumprd: use 300s as the default systemd unit timeout for kdump mount

* Mon Aug 7 2017 Dave Young <dyoung@redhat.com> - 2.0.15-9
- fix makedumpfile bug 1474706

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.0.15-7
- Rebuild with binutils fix for ppc64le (#1475636)

* Fri Jul 28 2017 Dave Young <dyoung@redhat.com> - 2.0.15-6
- update upstream makedumpfile 1.6.2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Dave Young <dyoung@redhat.com> - 2.0.15-4
- mkdumprd: remove useless "x-initrd.mount"
- kdumpctl: use "apicid" other than "initial apicid"

* Fri Jul 14 2017 Dave Young <dyoung@redhat.com> - 2.0.15-3
- module-setup: fix 99kdumpbase network dependency
- mkdumprd: omit dracut modules in case of network dumping
- mkdumprd: omit dracut modules in case of no dm target
- mkdumprd: omit crypt when there is no crypt kdump target
- kdumpctl: use generated rd.lvm.lv=X
- mkdumprd: change for_each_block_target() to use get_kdump_targets()
- kdump-lib.sh: introduce get_kdump_targets()
- kdump-lib.sh: fix improper get_block_dump_target()
- kdumpctl: fix infinite loop caused by running under bash

* Wed Jun 28 2017 Dave Young <dyoung@redhat.com> - 2.0.15-2
- enable makedumpfile for arm64

* Fri Jun 23 2017 Dave Young <dyoung@redhat.com> - 2.0.15-1
- rebase kexec-tools-2.0.15

* Thu Jun 15 2017 Dave Young <dyoung@redhat.com> - 2.0.14-13
- kexec-tools.spec: Fix whitespace errors
- dracut-module-setup: Fix test for inclusion of DRM modules
- kdump.conf.5: clarify the fence_kdump_nodes option

* Thu May 18 2017 Dave Young <dyoung@redhat.com> - 2.0.14-12
- kdumpctl: for fence_kdump, the ipaddr of this node should be excluded

* Fri May 12 2017 Dave Young <dyoung@redhat.com> - 2.0.14-11
- kdumpctl: change the shebang header to use /bin/bash
- kdumpctl: call strip_comments only when necessary to speedup
- Revert "kdumpctl: improve "while read" time for /etc/kdump.conf" (rhbz1449801)

* Fri May 5 2017 Dave Young <dyoung@redhat.com> - 2.0.14-10
- kdumpctl: improve "while read" time for /etc/kdump.conf
- kdumpctl: update check_dump_fs_modified() to use "lsinitrd -f"
- kdumpctl: improve check_wdt_modified()
- kdumpctl: remove is_mode_switched()
- kdumpctl: bail out earlier in case of no reserved memory

* Thu Apr 27 2017 Dave Young <dyoung@redhat.com> - 2.0.14-9
- kdump: Introduce 'force_no_rebuild' option
- kdump-lib-initramfs.sh: ignore the failure of echo
- kdump.sysconfig/x86_64: Add nokaslr to kdump kernel cmdline

* Tue Apr 11 2017 Dave Young <dyoung@redhat.com> - 2.0.14-8
- kdumpctl: fix status check when CONFIG_CRASH_DUMP is not enabled in kernel
- kdumpctl: fix a bug in remove_cmdline_param()
- kdumpctl: remove "root=X" for kdump boot
- Revert "kdumpctl: filter 'root' kernel parameter when running in live images"

* Fri Mar 31 2017 Dave Young <dyoung@redhat.com> - 2.0.14-7
- kdump-emergency: fix "Transaction is destructive" emergency failure
- mkdumprd: reduce lvm2 memory under kdump

* Fri Mar 17 2017 Dave Young <dyoung@redhat.com> - 2.0.14-6
- Fix kernel kaslr caused regressions (kexec -p and makedumpfile --mem-usage)

* Thu Mar 9 2017 Dave Young <dyoung@redhat.com> - 2.0.14-5
- kdump-lib.sh: fix incorrect usage with pipe as input for grep -q in is_pcs_fence_kdump()
- Document: fix incorrect link in fadump-how.txt

* Mon Jan 23 2017 Dave Young <dyoung@redhat.com> - 2.0.14-4
- drop kdump script rhcrashkernel-param in kexec-tools repo
- kdumpctl: sanity check of nr_cpus for x86_64 in case running out of vectors
- kdumpctl: change prepare_cmdline() to operate KDUMP_COMMANDLINE directly
- use --hostonly-i18n for dracut

* Wed Jan 4 2017 Dave Young <dyoung@redhat.com> - 2.0.14-3
- Rebase makedumpfile 1.6.1
- Delete unused patches

* Tue Dec 20 2016 Dave Young <dyoung@redhat.com> - 2.0.14-2
- rebase upstream kexec-tools 2.0.14
- update kdump anaconda addon
- cleanup sources file

* Mon Nov 28 2016 Dave Young <dyoung@redhat.com> - 2.0.14-1
- kexec-tools 2.0.14-1

* Mon Nov 28 2016 Dave Young <dyoung@redhat.com> - 2.0.13-9
- rename function kdump_to_udev_name
- Raw dump: use by-id as persistent policy in 2nd kernel
- drop dracut duplicate functions
- dracut-kdump: use POSIX shell syntax
- Correct two typos in kdumpctl and kdump.conf

* Fri Nov 11 2016 Dave Young <dyoung@redhat.com> - 2.0.13-8
- kexec/arch/i386: Add support for KASLR memory randomization
- Update kdump anaconda addon
- fadump: restore default initrd when fadump mode is disabled
- kdump/fadump: fix network interface name when switching from fadump to kdump
- kdumpctl: filter 'root' kernel parameter when running in live images
- Documentation: step by step guide on confiuring kdump in live images

* Thu Oct 27 2016 Dave Young <dyoung@redhat.com> - 2.0.13-7
- fix wrong page_offset added in 2.0.13-6

* Wed Oct 26 2016 Dave Young <dyoung@redhat.com> - 2.0.13-6
- add kexec support for arm64
- support x86 kaslr which is enabled by default in F25 kernel

* Fri Sep 16 2016 Dave Young <dyoung@redhat.com> - 2.0.13-5
- Fix bug 1373958 for system boot without initrd
- Do not depend on /etc/fstab in kdumpctl in case it does not exist

* Fri Aug 26 2016 Dave Young <dyoung@redhat.com> - 2.0.13-4
- Add special dump target "--mount" in dracut_args

* Tue Aug 9 2016 Dave Young <dyoung@redhat.com> - 2.0.13-3
- Fix armv7 build failure

* Tue Aug 9 2016 Dave Young <dyoung@redhat.com> - 2.0.13-2
- Drop old patches for 2.0.12

* Tue Aug 9 2016 Dave Young <dyoung@redhat.com> - 2.0.13-1
- Rebase kexec-tools 2.0.13

* Thu Jul 21 2016 Dave Young <dyoung@redhat.com> - 2.0.12-10
- kdump.conf manpage and kdump.conf comments fixes.
- kdump watchdog support.

* Wed Jul 13 2016 Dave Young <dyoung@redhat.com> - 2.0.12-9
- Update kdump anaconda addon
- makedumpfile: Support _count -> _refcount rename in struct page
- module-setup: Don't handle iBFT in kdump

* Wed Jul 6 2016 Dave Young <dyoung@redhat.com> - 2.0.12-8
- Rebase makedumpfile 1.6.0

* Mon Jun 27 2016 Dave Young <dyoung@redhat.com> - 2.0.12-7
- Fix date format in spec file.

* Mon Jun 27 2016 Dave Young <dyoung@redhat.com> - 2.0.12-6
- get_persistent_dev(): fix name contention with dracut's similar function

* Mon Jun 6 2016 Dave Young <dyoung@redhat.com> - 2.0.12-5
- kdump-lib: Add get_ifcfg_filename() to get the proper ifcfg file
- module-setup: Use get_ifcfg_filename() to get the proper ifcfg file

* Mon May 30 2016 Dave Young <dyoung@redhat.com> - 2.0.12-4
- update kdump anaconda addon to add mem range in tui
- .gitignore: Update to make it more generic
- kdumpctl: check_rebuild improvement
- kdumpctl: Do not rebuild initramfs when $KDUMP_BOOTDIR is read only

* Tue Mar 29 2016 Dave Young <dyoung@redhat.com> - 2.0.12-3
- update kdump anaconda addon to adapt to blivet-2.0 API

* Thu Mar 24 2016 Dave Young <dyoung@redhat.com> - 2.0.12-2
- Release 2.0.12-2
- ppc64le: fix kexec hang due to ppc64 elf abi breakage

* Tue Mar 22 2016 Dave Young <dyoung@redhat.com> - 2.0.12-1
- Rebase kexec-tools to 2.0.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Dave Young <dyoung@redhat.com> - 2.0.11-3
- use "systemctl reboot -f" for reboot action
- Remove kernel param "quiet" from kdump kernel cmdline
- kdump.sysconfig: add KDUMP_COMMANDLINE_REMOVE
- Add missing prefixes in default sysconfig file
- fix bogus date in changelog

* Thu Nov 19 2015 Dave Young <dyoung@redhat.com> - 2.0.11-2
- Rebase to upstream makedumpfile 1.5.9

* Mon Nov 9 2015 Dave Young <dyoung@redhat.com> - 2.0.11-1
- Rebase to upstream kexec-tools 2.0.11

* Mon Oct 19 2015 Dave Young <dyoung@redhat.com> - 2.0.10-9
- kexec-kdump-howto:Add introduction of parallel dumping
- Remove duplicate prefix path ${initdir}

* Tue Sep 8 2015 Dave Young <dyoung@redhat.com> - 2.0.10-8
- update kdump addon to fix a kickstart installationi issue

* Wed Aug 19 2015 Dave Young <dyoung@redhat.com> - 2.0.10-7
- add man page for kdumpctl

* Thu Aug 13 2015 Baoquan He <bhe@redhat.com> - 2.0.10-6
- mkdumprd: Remove ifcfg from dracut's modules
- module-setup: Choose the first matched gateway in kdump_static_ip
- module-setup: Add permanent option to detect static ip address or not

* Tue Aug 4 2015 Dave Young <dyoung@redhat.com> - 2.0.10-5
- Update kdump addon to fix an installation hang issue.

* Tue Jul 28 2015 Dave Young <dyoung@redhat.com> - 2.0.10-4
- ipv6 support (except for link scope addresses)
- Apply the manual DNS to the 2nd kernel
- load iTCO_wdt early in cmdline hook

* Thu Jul 23 2015 Dave Young <dyoung@redhat.com> - 2.0.10-3
- Update kdump addon icon
- Revert static route corner case patches per bhe. He discussed with Marc
  it is just a corner case.

* Mon Jul 13 2015 Dave Young <dyoung@redhat.com> - 2.0.10-2
- update kdump addon icon

* Thu Jul 9 2015 Dave Young <dyoung@redhat.com> - 2.0.10-1
- Rebase kexec-tools 2.0.10
- Rebase eppic git tree 050615
- Enhance kdump.conf "default" parameters check

* Thu Jul 2 2015 Dave Young <dyoung@redhat.com> - 2.0.9-2
- Resolve bug 1236456, kexec load fail because koji add extra gcc flags.
- Remove -FPIC for makedumpfile since it is not necessary without harden build

* Tue Jun 23 2015 Dave Young <dyoung@redhat.com> - 2.0.9-1
- Rebase kexec-tools 2.0.9
- Rebase makedumpfile 1.5.8
- revert 6347630 since ipv6 patches has not been reviewed.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dave Young <dyoung@redhat.com> -2.0.8-13
- Update kdump anaconda addon icon again.

* Wed Jun 10 2015 Dave Young <dyoung@redhat.com> -2.0.8-12
- Update kdump anaconda addon, change an icon.

* Wed Jun 03 2015 Baoquan He <bhe@redhat.com> -2.0.8-11
- make kdump work when kernel crash after shutdown
- Disable transparent hugepages in second kernel
- Filtered out "noauto" options in 2nd kernel fstab

* Tue Apr 21 2015 Baoquan He <bhe@redhat.com> -2.0.8-10
- add fPIC to makefumpfile CFLAGS to support hardening
- dracut-module-setup: Enhance kdump to support the bind mounted feature in Atomic
- Fix the warning if the target path is bind mount in Atomic
- Get the mount point correctly, if the device has several mount point
- kdump-lib: Add new function to judge the system is Atomic or not
- kdump-lib: Add the new function to enhance bind mounted judgement
- Remove duplicate slash in save path

* Thu Apr 09 2015 Baoquan He <bhe@redhat.com> -2.0.8-9
- Revert "execute kdump_post after do_default_action"
- dracut-module-setup.sh: change the insecure use of /tmp/*$$* filenames
- make kdump saving directory name consistent with RHEL6

* Sun Feb 15 2015 Dave Young <dyoung@redhat.com> - 2.0.8-8
- execute kdump_post after do_default_action
- update kdump anaconda addon (translations/help text issus)

* Fri Jan 30 2015 Baoquan He <bhe@redhat.com> - 2.0.8-7
- kdumpctl: adjust the boot dir if kernel is put in sub dir of /boot

* Tue Jan 13 2015 WANG Chao <chaowang@redhat.com> - 2.0.8-6
- mount fail if its mount point doesn't exist in /sysroot
- rebuild initrd dependency during kdump restart
- fix a dump path issue

* Tue Jan 06 2015 WANG Chao <chaowang@redhat.com> - 2.0.8-5
- remove panic_on_warn kernel param in 2nd kernel
- remove sysctl.conf to restore sysctl default values in 2nd kernel
- fix a core_collector issue in ssh and raw dump case
- update to kdump-anaconda-addon-005-2-g86366ae.tar.gz
- some cleanups

* Tue Nov 04 2014 WANG Chao <chaowang@redhat.com> - 2.0.8-4
- Fix ppc64le installation issue
- Fix get_option_value function

* Tue Oct 28 2014 WANG Chao <chaowang@redhat.com> - 2.0.8-3
- fix static route corner case
- fadump fix

* Tue Oct 21 2014 WANG Chao <chaowang@redhat.com> - 2.0.8-2
- Fix build issue on ARM

* Mon Oct 20 2014 WANG Chao <chaowang@redhat.com> - 2.0.8-1
- Rebase kexec-tools-2.0.8
- Remove subpackage kexec-tools-eppic
- Rebase kdump-anaconda-addon-005

* Fri Sep 26 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-11
- Fix build failure on ppc64le
- Fix an issue on iscsi boot environment

* Tue Sep 23 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-10
- Enable ppc64le arch.
- Rebase makedumpfile-1.5.7
- add sample eppic scripts to kexec-tools-eppic package
- Restart kdump service on cpu ADD/REMOVE events

* Wed Sep 10 2014 Baoquan He <bhe@redhat.com> - 2.0.7-9
- kdumpctl: Use kexec file based syscall for secureboot enabled machines
- kdumpctl: Use kexec file based mode to unload kdump kernel
- kdumpctl: Do not redirect error messages to /dev/null
- kexec: Provide an option to use new kexec system call

* Fri Aug 29 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-8
- use absolute path for executable in systemd service
- update to kdump-anaconda-addon-003
- remove dead kdump firstboot module and po files

* Thu Aug 21 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-7
- install 98-kexec.rules to /usr/lib/
- update kdump-anaconda-addon-0.2

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-5
- rework of kdump error handling
- add fadump support
- add static route support
- systemd will take care of shutdown and umount filesystems

* Thu Jul 24 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-4
- update to kdump-anaconda-addon-001-4-g03898ef.tar.gz
- prefix "kdump-" to eth name

* Mon Jul 21 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-3
- update to kdump-anaconda-addon-20140721.tar.gz

* Wed Jul 16 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-2
- Fix makedumpfile OOM issue

* Tue Jun 10 2014 WANG Chao <chaowang@redhat.com> - 2.0.7-1
- Rebase kexec-tools-2.0.7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 WANG Chao <chaowang@redhat.com> - 2.0.6-8
- re-construct anaconda-addon file hierarchy

* Wed May 21 2014 WANG Chao <chaowang@redhat.com> - 2.0.6-7
- fix a typo in kexec-tools.spec

* Tue May 20 2014 WANG Chao <chaowang@redhat.com> - 2.0.6-6
- New package kdump-anaconda-addon
- fixes for udev event based service restart

* Wed Apr 30 2014 WANG Chao <chaowang@redhat.com> - 2.0.6-5
- Remove nofail mount option
- Rebase makedumpfile-1.5.6

* Thu Apr 17 2014 WANG Chao <chaowang@redhat.com> - 2.0.6-4
- generate kdump service dependencies on the fly
- kdump.conf: a standalone path directive becomes a relative path to it's backed disk.

* Wed Apr 02 2014 WANG Chao <chaowang@redhat.com> - 2.0.6-3
- Add README to git repo
- Add fence_kdump support for generic clusters

* Thu Mar 27 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.6-2
- Exclude AArch64

* Wed Mar 26 2014 WANG Chao <chaowang@redhat.com> - 2.0.6-1
- Rebase kexec-tools-2.0.6
- fix an issue when dump path is mounted on nfs
- vmcore-dmesg: stack smashing fix
- get_ssh_size fix for localized df output

* Mon Mar 10 2014 WANG Chao <chaowang@redhat.com> - 2.0.5-2
- Warn about save vmcore patch mounted by another disk
- Omit dracut resume module

* Tue Mar 04 2014 WANG Chao <chaowang@redhat.com> - 2.0.5-1
- Rebase kexec-tools-2.0.5
- backport several patches from upstream for i386 build

* Mon Mar 03 2014 WANG Chao <chaowang@redhat.com> - 2.0.4-25
- Pass disable_cpu_apicid to kexec of capture kernel
- Relax restriction of dumping on encrypted target
- regression fix on wdt kernel drivers instal

* Mon Feb 17 2014 WANG Chao <chaowang@redhat.com> - 2.0.4-24
- add kdump-in-cluster-environment.txt to rpm pkg
- Secure Boot status check warning
- Some watchdog driver support

* Wed Jan 29 2014 WANG Chao <chaowang@redhat.com> - 2.0.4-23
- ssh dump: create random-seed manually
- makedumpfile: memset() in cyclic bitmap initialization introduce segment fault.
- Add acpi_no_memhotplug to kdump kernel
- Add fence kdump support

* Tue Jan 28 2014 WANG Chao <chaowang@redhat.com> - 2.0.4-22
- Rebase makedumpfile-1.5.5

* Wed Jan 22 2014 WANG Chao <chaowang@redhat.com> - 2.0.4-21
- makedumpfile: Improve progress information for huge memory system
- s390: use nr_cpus=1 instead of maxcpus=1

* Fri Jan 17 2014 WANG Chao <chaowang@redhat.com> - 2.0.4-20
- vmcore-dmesg: fix timestamp error in vmcore-dmesg.txt
- makedumpfile: re-enable mmap() and introduce --non-mmap
- kdump.conf uncomment default core_collector line
- fix an issue when 'ssh' directive appearing in kdump.conf, the rest part of
  lines in this file are ignored

* Tue Dec 24 2013 WANG Chao <chaowang@redhat.com> - 2.0.4-18
- update translation files
- makedumpfile: default to lzo compression
- makedumpfile: add makedumpfile.conf.sample and its manpage

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.0.4-15
- Fix Tamil (India) locale subdir name.
- Fix bogus date in %%changelog.

* Tue Dec 03 2013 WANG Chao <chaowang@redhat.com> - 2.0.4-14
- Add rd.memdebug in kdump module
- kdumpctl: Avoid leaking fd to subshell
- makedumpfile: Understand >= v3.11-rc4 dmesg
- makedumpfile, ppc: Support to filter dump for kernels that use CONFIG_SPARSEMEM_VMEMMAP.

* Fri Nov 15 2013 WANG Chao <chaowang@redhat.com> - 2.0.4-13
- makedumpfile: disable mmap()

* Tue Oct 29 2013 WANG Chao <chaowang@redhat.com> - 2.0.4-12
- fix sadump format phys_base calculating error
- kdump, x86: Process multiple Crash kernel in /proc/iomem
- makedumpfile: wrong cyclic buffer size recalculation causes bitmap data corruption
- Fix max_mapnr issue on system has over 44-bit addressing.

* Sat Oct 12 2013 Baoquan He <bhe@redhat.com> -2.0.4-11
- kdump-lib.sh: strip_comments is not implemented correcty

* Fri Sep 27 2013 Baoquan He <bhe@redhat.com> - 2.0.4-10
- Back port 2 revert commits
- kdump.sysconfig: default to "nofail" mount

* Fri Sep 27 2013 Baoquan He <bhe@redhat.com> - 2.0.4-9
- Strip inline comments from the kdump config file before use
- kdump-lib.sh: add common function strip_comments
- Introduce kdump-lib.sh for kdump shared functions
- kdump.service: Start kdump after network is online and remote fs is mounted
- dracut-module-setup: _dev to be a local variable
- kdumpctl: Run multiple kdumpctl instances one by one in serial order

* Wed Aug 21 2013 Baoquan He <bhe@redhat.com> - 2.0.4-8
- remove 98selinux dependency

* Fri Aug 2  2013 Baoquan He <bhe@redhat.com> - 2.0.4-7
- dracut-kdump.sh: add do_dump() and error out if dump vmcore fails
- dracut-module-setup.sh: setup correct system time and time zone in 2nd kernel.
- kernel cmdline: Remove hugepage allocations
- Use /lib/dracut/no-emergency-shell to control action on fail
- Revert: kdump.sysconfig: Add option action_on_fail and set its default as continue
- dracut-kdump.sh: Redirect kdump script stdout/stderr to /dev/console
- makedumpfile: Add vmap_area_list definition for ppc/ppc64.

* Fri Jul 12 2013 Baoquan He <bhe@redhat.com> - 2.0.4-6
- add snappy build
- add lzo build
- pull makedumpfile-1.5.4
- mkdumprd: check return value of subshell
- mkdumprd: get_persistent_dev() return original dev if no persistent dev exists.
- dracut-kdump.sh: Merge dump_to_rootfs() to dump_fs()
- dracut-kdump.sh: explicitly sync after each dump
- Correct wrong weekday of changelog
- kexec-tools.spec: Remove incorrect description in changelog

* Tue Jun 25 2013 Baoquan He <bhe@redhat.com> - 2.0.4-5
- monitor-dd-progress fix
- rawdump: only show dd progress bar when core_collector is not makedumpfile
- kexec-tools.spec: replaces scriptlets with new systemd macros
- dracut-kdump.sh: umount fs right before kdump exit
- dracut-kdump.sh: recursively umount fs and its submounts
- dracut-kdump.sh: cleanup - using local variable names instead of $1/$2 in functions
- dracut-kdump.sh: name the invalid vmcore to vmcore-incomplete
- dracut-kdump.sh: Output top level information about the kdump progress.
- kexec-kdump-howto: Add a section for debugging tips

* Tue Jun 18 2013 Baoquan He <bhe@redhat.com> - 2.0.4-4
- dracut-module-setup.sh: improve the approach to get a bridged interface list
- dracut-module-setup.sh: cleanup - use kdump_get_mac_addr() function
- dracut-module-setup.sh: use kernel exported mac address in kdump_get_mac_addr()
- dracut-module-setup.sh: use perm addr of slaves to setup bonding network
- kdump: Do not output debug messages by default
- dracut-module-setup.sh: kdump module depends on drm module
- mkdumprd: return error if no write permission on save path of server for ssh

* Thu Jun 13 2013 Baoquan He <bhe@redhat.com> - 2.0.4-3
- mkdumprd: remove -M option for dracut
- kdumpctl: add selinux relabel when service startup
- depends on dracut selinux module
- dracut-kdump.sh: umount rootfs after dump_to_rootfs
- kdump.sysconfig: append "panic=10" to kdump cmdline
- kexec-kdump-howto: grubby is suggested modifing kernel cmdline
- kexec-tools.spec: removes kexec udev rules for s390
- kdump.sysconfig: Add option action_on_fail and set its default as continue
- Add tab key as delimiter for core_collector in kdump.conf
- redirect stdout to stderr

* Tue May 14 2013 Baoquan He <bhe@redhat.com> - 2.0.4-2
- kdump: Save vmcore-dmesg.txt before saving vmcore
- Remove "ip=" overwrite to 40ip.conf
- Add support for bridge over bond/team/vlan.
- Fix bonding options syntax and get all specified options from ifcfg file.
- add dracut_args option to kdump.conf
- kexec-tools.spec: Add ethtool to dependency.
- error out if dump target is encrypted

* Wed Apr  3 2013 Baoquan He <bhe@redhat.com> - 2.0.4-1
- Delete several patches which have been merged into kexec-tools-2.0.4
- Revert: Release 2.0.3-72
- Release 2.0.3-72
- Pull kexec-tools-2.0.4
- Check if block device as dump target is resettable
- mkdumprd: add function perror_exit
- Deprecate blacklist option

* Wed Mar 27 2013 Baoquan He <bhe@redhat.com> - 2.0.3-71
- Remove eppic support on ppc and s390 arch

* Mon Mar 18 2013 Baoquan He <bhe@redhat.com> - 2.0.3-70
- Change rules related to eppic in kexec-tools.spec

* Thu Mar 14 2013 Baoquan He <bhe@redhat.com> - 2.0.3-69
- Support for eppic language as a subpackage

* Thu Mar 14 2013 Baoquan He <bhe@redhat.com> - 2.0.3-68
- tune sysconfig to save memory usage
- Remove useless codes related to LOGGER in kdumpctl
- kdumpctl:print out the service status
- Return to start() function when check_ssh_target failed
- use findmnt instead of blkid in mkdumprd
- check dump target mounting earlier
- kdumpctl: rename function name check_config
- add function to check kdump config file
- dracut-module-setup.sh: remove UUID/LABEL quotes before using it
- Change dump_to_rootfs to be a default option and reboot to be default action
- Remove "-F" in CORE_COLLECTOR when dump_to_rootfs

* Tue Feb 19 2013 Baoquan He <bhe@redhat.com> - 2.0.3-67
- Remove comma which is redundant
- Modify codes related to dump dir to make it clearer
- Rectify the get_host_ip implementation
- Revert: Merge an upstream patch for fix a ppc64 makedumpfile bug with with CONFIG_SPARSEMEM_EXTREME
- pull makedumpfile 1.5.3

* Tue Feb 5 2013 Dave Young <ruyang@redhat.com> - 2.0.3-66
- Spec: remove kdump image when a corresponding kernel is removed
- Merge an upstream patch for fix a ppc64 makedumpfile bug

* Mon Jan 28 2013 Dave Young <ruyang@redhat.com> - 2.0.3-65
- Add support for team devices
- Update translation file po/it.po
- remove wait for net ok function
- add bootdev cmdline param
- kdumpnic cmdline file name cleanup

* Fri Jan 4 2013 Dave Young <ruyang@redhat.com> - 2.0.3-64
- fix issue of exec on stack for ppc32

* Fri Dec 21 2012 Dave Young <ruyang@redhat.com> - 2.0.3-63
- revert explictly handling of PIPESTATUS
- enable pipefail bash option
- wrong ssh key fix
- build fix: Update 3 po files: po/gu.po po/or.po po/zh_CN.po

* Fri Dec 21 2012 Dave Young <ruyang@redhat.com> - 2.0.3-62
- Pull translated po files from zanata
- Optimize redundent code fetching server of network dump
- change the dump dir format to be more readable

* Wed Dec 12 2012 Dave Young <ruyang@redhat.com> - 2.0.3-61
- firstboot:fix reserve mem ui spinbox step size
- handle readonly mounted filesystem

* Mon Dec 10 2012 Dave Young <ruyang@redhat.com> - 2.0.3-60
- makedumpfile 1.5.1
- Update po tar.gz
- Add a notes for zanata process
- Add two xmls file for po zanata translation
- Cleanup and recreate po files

* Fri Nov 16 2012 Dave Young <ruyang@redhat.com> - 2.0.3-59
- Enable kdump service after installation
- get MEM_RESERVED from sysfs attribute
- get_ssh_size: use -n to redirect stdin from /dev/null
- add random feeding code for ssh dump
- kdump option space checking improvement
- kdumpctl: multi dump target checking fix

* Thu Oct 25 2012 Dave Young <ruyang@redhat.com> - 2.0.3-58
- pull in two upstream patches

* Thu Oct 11 2012 Dave Young <ruyang@redhat.com> - 2.0.3-57
- improve persistent name handling

* Sat Sep 29 2012 Dave Young <ruyang@redhat.com> - 2.0.3-56
- Pull vmcore-dmesg patches from vivek
- ppc/ppc64: compile purgatory with gcc option msoft-float
- Update to support f18 grub2 efi config file
- pass persistent name to dracut --device
- pass persistent name to dracut --mount
- use persistent name in kdump.conf of initramfs
- mkdumprd: add function get_persistent_dev
- remove useless uuid and label handling

* Thu Sep 06 2012 Dave Young <ruyang@redhat.com> - 2.0.3-55
- doc fix for mount dump target before mkdumprd
- pull makedumpfile 1.5.0

* Wed Aug 29 2012 Dave Young <ruyang@redhat.com> - 2.0.3-54
- pass raw device as dracut argument
- iscsi setup fix
- firstboot: add automatic and manual memory reservation for rhel
- firstboot: remove unnecessary underline shortkey
- firstboot: fix gtk warning about non-zero page size
- firstboot: update all kernels config in grubbyCmd
- firstboot: add actual reserved memory widget
- firstboot code cleanup
- rhcrashkernel-param: echo crashkernel=auto for rhel7
- Remove the kernel-kdump handling
- s390x firstboot fix
- remove elilo support
- grub2 fix in firstboot
- Take closing the reboot dialog as no
- Handle new crashkernel= syntax in firstboot
- Fix a localized string in firstboot
- Configure kdump in firstboot
- fix firstboot to ensure kdump svc is disabled properly
- firstboot text domain fix
- Update to use systemctl instead of sysv chkconfig
- port force_rebuild kdump.conf option
- Change return value to indicate the result of dump_raw() correctly.
- call dracut function for default shell

* Mon Jul 23 2012 Dave Young <ruyang@redhat.com> - 2.0.3-53
- refactor net option
- use fstab-sys to mount nfs
- rename function dump_localfs
- dump_localfs error path fix
- update kexec-kdump-howto.txt about systemctl commands
- ssh propagate alert message fix
- remove useless dracut cmdline '-c /dev/null'
- remove useless dracut cmdline for kernel-modules and kdumpbase
- install core_collector in module-setup.sh
- install extra_bins in module-setup.sh
- remove busybox dependency
- improve warning message of space checking
- do not mount root twice
- do not add fstab-sys module in dracut cmdline
- omit dash module
- network dns config fix
- shell exit value fix

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 5 2012 Dave Young <ruyang@redhat.com> - 2.0.3-51
- add s390x netdev setup
- Add s390x support
- Cleanup temp file leaved at /tmp/
- add check_size function for fs dump
- add ssh check_size
- blacklist patch apply fix
- Respect bonding mode
- Support dump over vlan tagged bonding

* Fri Jun 22 2012 Dave Young <ruyang@redhat.com> - 2.0.3-50
- add blacklist option, Resolves: bz805774
- Add kdump_post and kdump_pre support, Resolves: bz805773
- Port check_config from rhel6, Resolves: bz805778
- raw core_collector fix
- ssh core_collector fix
- drcut-kdump.sh: cleanup kdump.conf check

* Tue Jun 12 2012 Dave Young <ruyang@redhat.com> - 2.0.3-49
- cleanup DUMP_INSTRUCTION handling
- final reboot behavior fix
- dump_rootfs for default target fix
- add vlan support
- fix and refactor bond handling code
- fix and refactor bridge handling code
- core_collector doc basic fix
- omit plymouth module, Resolves: bz821997
- mkdumprd manpage cleanup manpage
- mkdumprd: remove --debug
- mkdumprd: remove noconf
- makedumprd: remove -d
- kdump.conf add sshkey
- kdump.conf remove disk_timeout
- kdump.conf make path uncommented
- kdump.conf.5 add default poweroff
- kdump.conf default shell fix
- kdump.conf default default action fix
- kdump.conf.5 remove module option
- kdump.conf remove kdump_pre/kdump_post
- kdump.conf: remove link_delay

* Mon May 28 2012 Dave Young <ruyang@redhat.com> - 2.0.3-48
- do_default_action cleanup, Resolves: bz805773
- add rhcrashkernel-param for anaconda use, Resolves: bz707441
- Basic iscsi target dump support (software initiator), Resolves bz822701
- Static ip configuratio support, Resolves: bz822739
- udev rules fix, Resolves: bz808817

* Thu May 3 2012 Dave Young <ruyang@redhat.com> - 2.0.3-47
- remove dracut-files.tgz2

* Wed May 2 2012 Dave Young <ruyang@redhat.com> - 2.0.3-46
- mkdumprd: Start using --hostonly and --add kdumpbase while calling dracut
- get_mp function cleanup
- move kdump script order to the end of pre pivot
- port raw dump from rhel6
- remove multi dump

* Mon Apr 23 2012 Dave Young <ruyang@redhat.com> - 2.0.3-45
- update dracut-files.tbz2

* Thu Apr 19 2012 Dave Young <dyoung@redhat.com> - 2.0.3-44
- update ppc64 sysconfig, resolve bug 811449
- deal with nic rename issue, resolve bug 810107
- update x86_64 sysconfig, resolve bug 813711

* Wed Apr 11 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.3-43
- variable name fix from Dave Young.

* Fri Mar 30 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.3-42
- get ip addr with getent
- spec: depends on dracut-network
- Handle net option for nfs in kdump.conf correctly

* Mon Feb 27 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.3-41
- Bump this version.

* Wed Feb 22 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-40
- Fixup sysytemd service file.

* Wed Feb 22 2012 Dave Young <ruyang@redhat.com> - 2.0.2-39
- Add ssh dump support, resolve bug 789253.

* Fri Jan 27 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-38
- Pull the latest makedumpfile release, 1.4.2.

* Fri Jan 27 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-37
- Add initial NFS dump support, experimental.

* Wed Jan 25 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-36
- Really upload the dracut module.

* Wed Jan 25 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-35
- Fix various bugs for nfs dump.

* Wed Jan 25 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-34
- kdump.sh cleanup for fstab handling, from Dave Young.

* Wed Jan 25 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-33
- Handle rootfs correctly.

* Tue Jan 10 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-32
- Fix add_dracut_arg in mkdumprd.

* Tue Jan 10 2012 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-31
- Update kdump dracut module with the latest dracut kdump branch.

* Fri Dec 16 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-30
- Update kdump dracut module to use the latest dracut feature.

* Fri Sep 9 2011 Tom Callaway <spot@fedoraproject.org> - 2.0.2-29
- fix systemd scriptlets

* Wed Sep 7 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-28
- Rename mkdumprd2 to mkdumpramfs.

* Wed Aug 31 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-27
- Add debug_mem_level debugging option, from Jan Stancek.
  Resolve Bug 731395.

* Mon Aug 15 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-26
- Fix several issues caused by the previous revert.

* Mon Aug 15 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-25
- Switch back to old mkdumprd and also keep the new one.

* Tue Aug 2 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-24
- Fix default action handling.

* Tue Aug 2 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-23
- Install modified kdump.conf in initrd.

* Tue Aug 2 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-22
- Handle lvm in pre-pivot hook.

* Tue Aug 2 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-21
- Fix udev rules in module-setup.sh

* Mon Aug 1 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-20
- Generate udev rules in module-setup.sh

* Mon Aug 1 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-19
- Generate udev rules to handle device names.

* Mon Aug 1 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-18
- Fix dump to local filesystem and raw dump.

* Mon Aug 1 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-17
- Depend on dracut-network.

* Mon Aug 1 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-16
- Move dracut module detection code to module-setup.sh.

* Thu Jul 28 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-15
- Use shutdown module of dracut to handle reboot/shutdown/halt.

* Wed Jul 27 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-14
- Wait for loginit.

* Wed Jul 27 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-13
- Use absolute path of reboot/halt/poweroff.

* Wed Jul 27 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-12
- Don't use consolehelper, use real reboot/halt/poweroff.

* Wed Jul 27 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-11
- Rename initrd to initramfs.

* Wed Jul 27 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-10
- Don't depend on busybox, as it doesn't save much space.

* Tue Jul 26 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-9
- Parse default action.

* Mon Jul 25 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-8
- Move path/core_collector/default parsing code to initrd.

* Mon Jul 25 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-7
- Remove obsolete code in kdumpctl.

* Mon Jul 25 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-6
- Support core_collector and extran_bins.

* Thu Jul 21 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-5
- Bypass '-d' option.

* Thu Jul 21 2011 Cong Wang <xiyou.wangcong@gmail.com> - 2.0.2-4
- Update initramfs infrastructure to make it working
  with dracut.

* Wed Jul 06 2011 Neil Horman <nhorman@redhat.com> - 2.0.2-3
- Removed sysv init script from package

* Mon Jul 04 2011 Neil Horman <nhorman@redhat.com> - 2.0.2-2
- Added systemd unit file (bz 716994)

* Fri Jun 24 2011 Neil Horman <nhorman@redhat.com> - 2.0.2-1
- Updated to upstream version 2.0.2

* Thu Jun 02 2011 Neil Horman <nhorman@redhat.com> - 2.0.0-47
- Fixed misuse of readlink command after directory change (bz 710744)

* Tue Apr 26 2011 Neil Horman <nhorman@redhat.com> - 2.0.0-46
- Fix some grammer in man page (bz 673817)

* Mon Mar 28 2011 Neil Horman <nhorman@redhat.com> - 2.0.0-45
- Fix misuse of basename in mkdumprd (bz 683769)

* Thu Mar 10 2011 Neil Horman <nhorman@redhat.com> - 2.0.0-44
- Fix build break in purgatory makefile

* Thu Mar 10 2011 Neil Horman <nhorman@redhat.com> - 2.0.0-43
- Remove vestigual emitdms code and call from mkdumprd

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 22 2010 Neil Horman <nhorman@redhat.com> - 2.0.0-41
- Fixed dhcp retry mechanism (bz 645734)

* Wed Sep 29 2010 jkeating - 2.0.0-40
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Neil Horman <nhorman@redhat.com> - 2.0.0-39
- fix finding modalias/mkdumprd hang (bz 635893)

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.0-38
- recompiling .py files against Python 2.7 (rhbz#623327)

* Sun Jun 13 2010 Lubomir Rintel <lkundrak@v3.sk> - 2.0.0-37
- Fix a syntax error in kdump init script

* Sun Jun 13 2010 Lubomir Rintel <lkundrak@v3.sk> - 2.0.0-36
- Cosmetic mkdumprd fixes (drop an unused function, streamline another)

* Sat May 29 2010 CAI Qian <caiqian@redhat.com> - 2.0.0-35
- Forward-port from F13
- Fixed kernel text area search in kcore (bz 587750)

* Sat May 29 2010 CAI Qian <caiqian@redhat.com> - 2.0.0-34
- Massive forward-port from RHEL6
- Update kexec-kdump-howto.txt
- Update docs to reflect use of ext4
- Update mkdumprd to pull in all modules needed
- Fix mkdumprd typo
- Removed universal add of ata_piix from mkdumprd
- Fix infinite loop from modprobe changes
- Fixed kexec-kdump-howto.doc for RHEL6
- Update makedumpfile to 1.3.5
- Improved mkdumprd run time
- Cai's fix for broken regex
- Fixing crashkernel syntax parsing
- Fix initscript to return proper LSB return codes
- Fixed bad call to resolve_dm_name
- Added poweroff option to mkdumprd
- Fixed readlink issue
- Fixed x86_64 page_offset specifictaion
- Fixed lvm setup loop to not hang
- Added utsname support to makedumpfile for 2.6.32
- Fix critical_disks list to exclude cciss/md
- Add help info for -b option
- Add ability to handle firmware hotplug events
- Update mkdumprd to deal with changes in busybox fsck
- Vitaly's fix to detect need for 64 bit elf
- Fix major/minor numbers on /dev/rtc
- Fix ssh id propogation w/ selinux
- Add blacklist feature to kdump.conf
- Removed rhpl code from firstboot
- Fixed firstboot enable sense
- Remove bogus debug comment from mkdumprd.
- Handle SPARSEMEM properly
- Fix scp monitoring script
- Fix firstboot to find grub on EFI systems
- Fixed mkdumprd to remove dup insmod
- Fixed kdump fsck pause
- Fixed kdump option handling
- fixed raid5 module detection

* Thu Mar 11 2010 Neil Horman <nhorman@redhat.com> - 2.0.0-33
- Remove nash references from mkdumprd

* Wed Feb 17 2010 Neil Horman <nhorman@redhat.com> - 2.0.0-32
- Fixed spec file error

* Wed Feb 17 2010 Neil Horman <nhorman@redhat.com> - 2.0.0-31
- Adding kdump.conf man page
- Adding disk timeout parameter (bz 566135)

* Tue Dec 01 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-30
- Fix raid support in mkdumprd (bz 519767)

* Mon Nov 23 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-29
- Updating firstboot script to RHEL-6 version (bz 539812)

* Fri Nov 06 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-28
- Added abrt infrastructure to kdump init script (bz 533370)

* Tue Sep 15 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-27
- Fixing permissions on dracut module files

* Fri Sep 11 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-26
- Rebuild for translation team (bz 522415)

* Thu Sep 10 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-25
- Fix dracut module check file (bz 522486)

* Thu Aug 13 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-24
- update kdump adv conf init script & dracut module

* Wed Jul 29 2009 Neil Horman <nhorman@redhat.com> - 2.0,0-23
- Remove mkdumprd2 and start replacement with dracut

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Neil Horman <nhorman@redhat.com> 2.0.0-21
- Fixed build break

* Mon Jul 06 2009 Neil Horman <nhorman@redhat.com> 2.0.0-20
- Make makedumpfile a dynamic binary

* Mon Jul 06 2009 Neil Horman <nhorman@redhat.com> 2.0.0-19
- Fix build issue

* Mon Jul 06 2009 Neil Horman <nhorman@redhat.com> 2.0.0-18
- Updated initscript to use mkdumprd2 if manifest is present
- Updated spec to require dash
- Updated sample manifest to point to correct initscript
- Updated populate_std_files helper to fix sh symlink

* Mon Jul 06 2009 Neil Horman <nhorman@redhat.com> 2.0.0-17
- Fixed mkdumprd2 tarball creation

* Tue Jun 23 2009 Neil Horman <nhorman@redhat.com> 2.0.0-16
- Fix up kdump so it works with latest firstboot

* Mon Jun 15 2009 Neil Horman <nhorman@redhat.com> 2.0.0-15
- Fixed some stat drive detect bugs by E. Biederman (bz505701)

* Wed May 20 2009 Neil Horman <nhorman@redhat.com> 2.0.0-14
- Put early copy of mkdumprd2 out in the wild (bz 466392)

* Fri May 08 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-13
- Update makedumpfile to v 1.3.3 (bz 499849)

* Tue Apr 07 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-12
- Simplifed rootfs mounting code in mkdumprd (bz 494416)

* Sun Apr 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.0.0-11
- Install the correct configuration for i586

* Fri Apr 03 2009 Neil Horman <nhorman@redhat.com> - 2.0.0-10
- Fix problem with quoted CORE_COLLECTOR string (bz 493707)

* Thu Apr 02 2009 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-9
- Add BR glibc-static

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.0-7
- Rebuild for Python 2.6

* Mon Dec 01 2008 Neil Horman <nhorman@redhat.com> - 2.0.0.6
- adding makedumpfile man page updates (bz 473212)

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.0-5
- Rebuild for Python 2.6

* Wed Nov 05 2008 Neil Horman <nhorman@redhat.com> - 2.0.0-3
- Correct source file to use proper lang package (bz 335191)

* Wed Oct 29 2008 Neil Horman <nhorman@redhat.com> - 2.0.0-2
- Fix mkdumprd typo (bz 469001)

* Mon Sep 15 2008 Neil Horman <nhorman@redhat.com> - 2.0.0-2
- Fix sysconfig files to not specify --args-linux on x86 (bz 461615)

* Wed Aug 27 2008 Neil Horman <nhorman@redhat.com> - 2.0.0-1
- Update kexec-tools to latest upstream version

* Wed Aug 27 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-16
- Fix mkdumprd to properly use UUID/LABEL search (bz 455998)

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.102pre-15
- fix license tag

* Mon Jul 28 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-14
- Add video reset section to docs (bz 456572)

* Fri Jul 11 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-13
- Fix mkdumprd to support dynamic busybox (bz 443878)

* Wed Jun 11 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-12
- Added lvm to bin list (bz 443878)

* Thu Jun 05 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-11
- Update to latest makedumpfile from upstream
- Mass import of RHEL fixes missing in rawhide

* Thu Apr 24 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-10
- Fix mkdumprd to properly pull in libs for lvm/mdadm (bz 443878)

* Wed Apr 16 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-9
- Fix cmdline length issue

* Tue Mar 25 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-8
- Fixing ARCH definition for bz 438661

* Mon Mar 24 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-7
- Adding patches for bz 438661

* Fri Feb 22 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-6
- Bringing rawhide up to date with bugfixes from RHEL5
- Adding patch to prevent kexec buffer overflow on ppc (bz 428684)

* Tue Feb 19 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-5
- Modifying mkdumprd to include dynamic executibles (bz 433350)

* Tue Feb 12 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-4
- bumping rev number for rebuild

* Wed Jan 02 2008 Neil Horman <nhorman@redhat.com> - 1.102pre-3
- Fix ARCH placement in kdump init script (bz 427201)
- Fix BuildRequires
- Fix Makedumpfile to build with new libelf

* Mon Oct 01 2007 Neil Horman <nhorman@redhat.com> - 1.102pre-2
- Fix triggerpostun script (bz 308151)

* Thu Aug 30 2007 Neil Horman <nhorman@redhat.com> - 1.102pre-1
- Bumping kexec version to latest horms tree (bz 257201)
- Adding trigger to remove initrds when a kernel is removed

* Wed Aug 22 2007 Neil Horman <nhorman@redhat.com> - 1.101-81
- Add xen-syms patch to makedumpfile (bz 250341)

* Wed Aug 22 2007 Neil Horman <nhorman@redhat.com> - 1.101-80
- Fix ability to determine space on nfs shares (bz 252170)

* Tue Aug 21 2007 Neil Horman <nhorman@redhat.com> - 1.101-79
- Update kdump.init to always create sparse files (bz 253714)

* Fri Aug 10 2007 Neil Horman <nhorman@redhat.com> - 1.101-78
- Update init script to handle xen kernel cmdlnes (bz 250803)

* Wed Aug 01 2007 Neil Horman <nhorman@redhat.com> - 1.101-77
- Update mkdumprd to suppres notifications /rev makedumpfile (bz 250341)

* Thu Jul 19 2007 Neil Horman <nhorman@redhat.com> - 1.101-76
- Fix mkdumprd to suppress informative messages (bz 248797)

* Wed Jul 18 2007 Neil Horman <nhorman@redhat.com> - 1.101-75
- Updated fr.po translations (bz 248287)

* Tue Jul 17 2007 Neil Horman <nhorman@redhat.com> - 1.101-74
- Fix up add_buff to retry locate_hole on segment overlap (bz 247989)

* Mon Jul 09 2007 Neil Horman <nhorman@redhat.com> - 1.101-73
- Fix up language files for kexec (bz 246508)

* Thu Jul 05 2007 Neil Horman <nhorman@redhat.com> - 1.101-72
- Fixing up initscript for LSB (bz 246967)

* Tue Jun 19 2007 Neil Horman <nhorman@redhat.com> - 1.101-71
- Fixed conflict in mkdumprd in use of /mnt (bz 222911)

* Mon Jun 18 2007 Neil Horman <nhorman@redhat.com> - 1.101-70
- Fixed kdump.init to properly read cmdline (bz 244649)

* Wed Apr 11 2007 Neil Horman <nhorman@redhat.com> - 1.101-69
- Fixed up kdump.init to enforce mode 600 on authorized_keys2 (bz 235986)

* Tue Apr 10 2007 Neil Horman <nhorman@redhat.com> - 1.101-68
- Fix alignment of bootargs and device-tree structures on ppc64

* Tue Apr 10 2007 Neil Horman <nhorman@redhat.com> - 1.101-67
- Allow ppc to boot ppc64 kernels (bz 235608)

* Tue Apr 10 2007 Neil Horman <nhorman@redhat.com> - 1.101-66
- Reduce rmo_top to 0x7c000000 for PS3 (bz 235030)

* Mon Mar 26 2007 Neil Horman <nhorman@redhat.com> - 1.101-65
- Fix spec to own kexec_tools directory (bz 219035)

* Wed Mar 21 2007 Neil Horman <nhorman@redhat.com> - 1.101-64
- Add fix for ppc memory region computation (bz 233312)

* Thu Mar 15 2007 Neil Horman <nhorman@redhat.com> - 1.101-63
- Adding extra check to avoid oom kills on nfs mount failure (bz 215056)

* Tue Mar 06 2007 Neil Horman <nhorman@redhat.com> - 1.101-62
- Updating makedumpfile to version 1.1.1 (bz 2223743)

* Thu Feb 22 2007 Neil Horman <nhorman@redhat.com> - 1.101-61
- Adding multilanguage infrastructure to firstboot_kdump (bz 223175)

* Mon Feb 12 2007 Neil Horman <nhorman@redhat.com> - 1.101-60
- Fixing up file permissions on kdump.conf (bz 228137)

* Fri Feb 09 2007 Neil Horman <nhorman@redhat.com> - 1.101-59
- Adding mkdumprd man page to build

* Thu Jan 25 2007 Neil Horman <nhorman@redhat.com> - 1.101-58
- Updating kdump.init and mkdumprd with most recent RHEL5 fixes
- Fixing BuildReq to require elfutils-devel-static

* Thu Jan 04 2007 Neil Horman <nhorman@redhat.com> - 1.101-56
- Fix option parsing problem for bzImage files (bz 221272)

* Fri Dec 15 2006 Neil Horman <nhorman@redhat.com> - 1.101-55
- Wholesale update of RHEL5 revisions 55-147

* Tue Aug 29 2006 Neil Horman <nhorman@redhat.com> - 1.101-54
- integrate default elf format patch

* Tue Aug 29 2006 Neil Horman <nhorman@redhat.com> - 1.101-53
- Taking Viveks x86_64 crashdump patch (rcv. via email)

* Tue Aug 29 2006 Neil Horman <nhorman@redhat.com> - 1.101-52
- Taking ia64 tools patch for bz 181358

* Mon Aug 28 2006 Neil Horman <nhorman@redhat.com> - 1.101-51
- more doc updates
- added patch to fix build break from kernel headers change

* Thu Aug 24 2006 Neil Horman <nhorman@redhat.com> - 1.101-50
- repo patch to enable support for relocatable kernels.

* Thu Aug 24 2006 Neil Horman <nhorman@redhat.com> - 1.101-49
- rewriting kcp to properly do ssh and scp
- updating mkdumprd to use new kcp syntax

* Wed Aug 23 2006 Neil Horman <nhorman@redhat.com> - 1.101-48
- Bumping revision number

* Tue Aug 22 2006 Jarod Wilson <jwilson@redhat.com> - 1.101-47
- ppc64 no-more-platform fix

* Mon Aug 21 2006 Jarod Wilson <jwilson@redhat.com> - 1.101-46
- ppc64 fixups:
  - actually build ppc64 binaries (bug 203407)
  - correct usage output
  - avoid segfault in command-line parsing
- install kexec man page
- use regulation Fedora BuildRoot

* Fri Aug 18 2006 Neil Horman <nhorman@redhat.com> - 1.101-45
- fixed typo in mkdumprd for bz 202983
- fixed typo in mkdumprd for bz 203053
- clarified docs in kdump.conf with examples per bz 203015

* Tue Aug 15 2006 Neil Horman <nhorman@redhat.com> - 1.101-44
- updated init script to implement status function/scrub err messages

* Wed Aug 09 2006 Jarod Wilson <jwilson@redhat.com> - 1.101-43
- Misc spec cleanups and macro-ifications

* Wed Aug 09 2006 Jarod Wilson <jwilson@redhat.com> - 1.101-42
- Add %%dir /var/crash, so default kdump setup works

* Thu Aug 03 2006 Neil Horman <nhorman@redhat.com> - 1.101-41
- fix another silly makefile error for makedumpfile

* Thu Aug 03 2006 Neil Horman <nhorman@redhat.com> - 1.101-40
- exclude makedumpfile from build on non-x86[_64] arches

* Thu Aug 03 2006 Neil Horman <nhorman@redhat.com> - 1.101-39
- exclude makedumpfile from build on non-x86[_64] arches

* Thu Aug 03 2006 Neil Horman <nhorman@redhat.com> - 1.101-38
- updating makedumpfile makefile to use pkg-config on glib-2.0

* Thu Aug 03 2006 Neil Horman <nhorman@redhat.com> - 1.101-37
- updating makedumpfile makefile to use pkg-config

* Thu Aug 03 2006 Neil Horman <nhorman@redhat.com> - 1.101-36
- Removing unneeded deps after Makefile fixup for makedumpfile

* Thu Aug 03 2006 Neil Horman <nhorman@redhat.com> - 1.101-35
- fixing up FC6/RHEL5 BuildRequires line to build in brew

* Wed Aug 02 2006 Neil Horman <nhorman@redhat.com> - 1.101-34
- enabling makedumpfile in build

* Wed Aug 02 2006 Neil Horman <nhorman@redhat.com> - 1.101-33
- added makedumpfile source to package

* Mon Jul 31 2006 Neil Horman <nhorman@redhat.com> - 1.101-32
- added et-dyn patch to allow loading of relocatable kernels

* Thu Jul 27 2006 Neil Horman <nhorman@redhat.com> - 1.101-30
- fixing up missing patch to kdump.init

* Wed Jul 19 2006 Neil Horman <nhorman@redhat.com> - 1.101-30
- add kexec frontend (bz 197695)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.101-29
- rebuild

* Fri Jul 07 2006 Neil Horman <nhorman@redhat.com> 1.101-27.fc6
- Buildrequire zlib-devel

* Thu Jun 22 2006 Neil Horman <nhorman@redhat.com> -1.101-19
- Bumping rev number

* Thu Jun 22 2006 Neil Horman <nhorman@redhat.com> -1.101-17
- Add patch to allow ppc64 to ignore args-linux option

* Wed Mar 08 2006 Bill Nottingham <notting@redhat.com> - 1.101-16
- fix scriptlet - call chkconfig --add, change the default in the
  script itself (#183633)

* Wed Mar 08 2006 Thomas Graf <tgraf@redhat.com> - 1.101-15
- Don't add kdump service by default, let the user manually add it to
  avoid everyone seeing a warning.

* Tue Mar 07 2006 Thomas Graf <tgraf@redhat.com> - 1.101-14
- Fix kdump.init to call kexec from its new location

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 1.101-13
- proper requires for scriptlets

* Mon Mar 06 2006 Thomas Graf <tgraf@redhat.com> - 1.101-12
- Move kexec and kdump binaries to /sbin

* Thu Mar 02 2006 Thomas Graf <tgraf@redhat.com> - 1.101-11
- Fix argument order when stopping kexec

* Mon Feb 27 2006 Thomas Graf <tgraf@redhat.com> - 1.101-10
- kdump7.patch
   o Remove elf32 core headers support for x86_64
   o Fix x86 prepare elf core header routine
   o Fix ppc64 kexec -p failure for gcc 4.10
   o Fix few warnings for gcc 4.10
   o Add the missing --initrd option for ppc64
   o Fix ppc64 persistent root device bug
- Remove --elf32-core-headers from default configuration, users
  may re-add it via KEXEC_ARGS.
- Remove obsolete KEXEC_HEADERS
* Wed Feb 22 2006 Thomas Graf <tgraf@redhat.com> - 1.101-9
- Remove wrong quotes around --command-line in kdump.init

* Fri Feb 17 2006 Jeff Moyer <jmoyer@redhat.com> - 1.101-8
- Fix the service stop case.  It was previously unloading the wrong kernel.
- Implement the "restart" function.
- Add the "irqpoll" option as a default kdump kernel commandline parameter.
- Create a default kernel command line in the sysconfig file upon rpm install.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.101-7.1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Thomas Graf <tgraf@redhat.com> - 1.101-7.1
- Add patch to enable the kdump binary for x86_64
* Wed Feb 01 2006 Thomas Graf <tgraf@redhat.com>
- New kdump patch to support s390 arch + various fixes
- Include kdump in x86_64 builds
* Mon Jan 30 2006 Thomas Graf <tgraf@redhat.com>
- New kdump patch to support x86_64 userspace

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Nov 16 2005 Thomas Graf <tgraf@redhat.com> - 1.101-5
- Report missing kdump kernel image as warning

* Thu Nov  3 2005 Jeff Moyer <jmoyer@redhat.com> - 1.101-4
- Build for x86_64 as well.  Kdump support doesn't work there, but users
  should be able to use kexec.

* Fri Sep 23 2005 Jeff Moyer <jmoyer@redhat.com> - 1.101-3
- Add a kdump sysconfig file and init script
- Spec file additions for pre/post install/uninstall

* Thu Aug 25 2005 Jeff Moyer <jmoyer@redhat.com>
- Initial prototype for RH/FC5
