Changelog
=========

[1.120.5] - 2026-02-23
---------------------

### Bug Fixes

- storage - fix: ensure libblockdev-loop package on EL7 for loop mounts (#591)

[1.120.4] - 2026-02-20
---------------------

### Other Changes

- no user-visible changes

[1.120.3] - 2026-02-18
---------------------

### Bug Fixes

- firewall - fix: el7 interface functionality requires NetworkManager (#323)
- firewall - fix: add set vars platform vars loader (#322)
- ha_cluster - fix: ostree - add dnf/dnf5 package, add firewall packages (#358)
- selinux - fix: when does not prevent template expansion in name with import_role (#331)

[1.120.2] - 2026-02-12
---------------------

### Bug Fixes

- timesync - fix: use ansible_facts timesync_ntp_provider_current (#331)

[1.120.1] - 2026-02-11
---------------------

### Bug Fixes

- vpn - fix: use host for dict key in tunnel - hostname is not a dict key (#236)

[1.120.0] - 2026-02-10
---------------------

### New Features

- selinux - feat: Add support for DCCP and SCTP protocols to selinux_port (#325)

[1.119.1] - 2026-02-07
---------------------

### Bug Fixes

- snapshot - fix: check create_snapshot_set function for boot parameter (#148)
- snapshot - fix: problem with bootable flag not getting passed properly to snapm (#138)
- storage - fix: Volume with no size is same as size 100% - fixes divide by zero error (#583)
- timesync - fix: check for existence of runlevel, chkconfig, service before using them (#325)

[1.119.0] - 2026-01-29
---------------------

### New Features

- postgresql - feat: Add support for postgresql 18 (#160)

[1.118.0] - 2026-01-22
---------------------

### New Features

- sshd - feat: Add systemd ephemeral authorized_keys to the instantiated service file on Fedora (#344)
- sshd - feat: New OpenSSH configuration option GSSAPIDelegateCredentials (#343)

[1.117.0] - 2026-01-21
---------------------

### New Features

- metrics - feat: add TLS certificate and key support for Grafana for HTTPS (#284)

[1.116.0] - 2026-01-18
---------------------

### New Features

- ha_cluster - feat: Support this role in container builds (#341)

[1.115.3] - 2026-01-14
---------------------

### Other Changes

- no user-visible changes

[1.115.2] - 2026-01-13
---------------------

### Bug Fixes

- storage - fix: add vdo package for Fedora OSTree (#579)

[1.115.1] - 2026-01-08
---------------------

### Other Changes

- no user-visible changes

[1.115.0] - 2026-01-06
---------------------

### New Features

- ssh - feat: Add new configuration option VersionAddendum (#214)

### Bug Fixes

- storage - fix: check for no disks specified and report correct error (#575)

[1.114.0] - 2025-12-17
---------------------

### New Features

- ha_cluster - feat: add support for fencing-watchdog-timeout (#335)
- kdump - feat: Ubuntu support (#265)

### Bug Fixes

- aide - fix: support new config file options, expose aide_version (#54)

[1.113.0] - 2025-11-17
---------------------

### New Features

- sshd - feat: add support for NetBSD (#338)

### Bug Fixes

- ad_integration - fix: cannot use community-general version 12 - no py27 and py36 support (#161)
- aide - fix: cannot use community-general version 12 - no py27 and py36 support (#52)
- bootloader - fix: cannot use community-general version 12 - no py27 and py36 support (#175)
- certificate - fix: cannot use community-general version 12 - no py27 and py36 support (#300)
- cockpit - fix: cannot use community-general version 12 - no py27 and py36 support (#245)
- crypto_policies - fix: cannot use community-general version 12 - no py27 and py36 support (#168)
- fapolicyd - fix: cannot use community-general version 12 - no py27 and py36 support (#83)
- firewall - fix: cannot use community-general version 12 - no py27 and py36 support (#307)
- gfs2 - fix: cannot use community-general version 12 - no py27 and py36 support (#70)
- ha_cluster - fix: cannot use community-general version 12 - no py27 and py36 support (#330)
- hpc - fix: cannot use community-general version 12 - no py27 and py36 support (#37)
- journald - fix: cannot use community-general version 12 - no py27 and py36 support (#129)
- kdump - fix: cannot use community-general version 12 - no py27 and py36 support (#262)
- kernel_settings - fix: cannot use community-general version 12 - no py27 and py36 support (#281)
- keylime_server - fix: cannot use community-general version 12 - no py27 and py36 support (#99)
- logging - fix: cannot use community-general version 12 - no py27 and py36 support (#475)
- metrics - fix: cannot use community-general version 12 - no py27 and py36 support (#274)
- nbde_client - fix: cannot use community-general version 12 - no py27 and py36 support (#224)
- nbde_server - fix: cannot use community-general version 12 - no py27 and py36 support (#205)
- network - fix: cannot use community-general version 12 - no py27 and py36 support (#824)
- podman - fix: cannot use community-general version 12 - no py27 and py36 support (#254)
- postfix - fix: cannot use community-general version 12 - no py27 and py36 support (#207)
- postgresql - fix: cannot use community-general version 12 - no py27 and py36 support (#150)
- rhc - fix: cannot use community-general version 12 - no py27 and py36 support (#248)
- selinux - fix: cannot use community-general version 12 - no py27 and py36 support (#312)
- snapshot - fix: cannot use community-general version 12 - no py27 and py36 support (#132)
- ssh - fix: cannot use community-general version 12 - no py27 and py36 support (#209)
- storage - fix: cannot use community-general version 12 - no py27 and py36 support (#571)
- sudo - fix: cannot use community-general version 12 - no py27 and py36 support (#85)
- systemd - fix: cannot use community-general version 12 - no py27 and py36 support (#113)
- timesync - fix: cannot use community-general version 12 - no py27 and py36 support (#312)
- tlog - fix: cannot use community-general version 12 - no py27 and py36 support (#191)
- vpn - fix: cannot use community-general version 12 - no py27 and py36 support (#219)

[1.112.0] - 2025-11-15
---------------------

### New Features

- sshd - feat: Add new configuration option CanonicalMatchUser on RHEL/CentOS (#332)

### Bug Fixes

- sshd - fix: Allow specifying OS vars from playbook_dir (#330)

[1.111.0] - 2025-11-13
---------------------

### New Features

- ha_cluster - feat: export cluster constraints (#326)
- hpc - New Role
- snapshot - feat: add support for "bootable" snapshots (#115)

### Bug Fixes

- firewall - fix: install python311-firewall on SLES 15 (#300)
- nbde_client - fix: idempotence issue when binding fails to be added (#196)

[1.110.1] - 2025-10-23
---------------------

### Other Changes

- no user-visible changes

[1.110.0] - 2025-10-21
---------------------

### New Features

- firewall - feat: add IPv6 ipset support, add support for ipset_options (#296)
- ha_cluster - feat: export cluster properties and resource defaults and resource operation defaults (#318)
- podman - feat: Support this role in container builds (#245)
- storage - feat: Add support for creating multiple partitions (#552)
- timesync - feat: support this role in container builds (#303)

### Bug Fixes

- network - fix: Skip the loopback profile when deleting all profiles except the ones explicitly included (#813)
- network - fix: allow use of built-in routing tables (#804)
- storage - fix: Allow running on systems without /etc/fstab present (#562)

[1.109.0] - 2025-09-07
---------------------

### New Features

- sshd - feat: Support for daemon reload, socket restart and systemd socket file to match Ubuntu 24.04 (#318)
- sshd - feat: add Debian 13 support (#315)

### Bug Fixes

- sshd - fix: include external config files first so they can override all options (#316)

[1.108.6] - 2025-08-20
---------------------

### Other Changes

- no user-visible changes

[1.108.5] - 2025-08-18
---------------------

### Other Changes

- no user-visible changes

[1.108.4] - 2025-08-08
---------------------

### Other Changes

- no user-visible changes

[1.108.3] - 2025-08-02
---------------------

### Other Changes

- no user-visible changes

[1.108.2] - 2025-08-01
---------------------

### Bug Fixes

- sshd - fix: New configuration option in CentOS 10 (#319)

[1.108.1] - 2025-08-01
---------------------

### Bug Fixes

- bootloader - fix: Fix Python 2.7.5 compatibility by using msg= in fail_json() calls (#154)
- bootloader - fix: boolean values and null values are not allowed (#153)
- ha_cluster - fix: crsmh corosync template wrongly used variable from run_once host (#299)
- keylime_server - fix: Add SLES_16 var file with required packages and ensure pyasn1 (#84)
- sudo - fix: Use the correct regular expression to parse Cmnd_Alias and other aliases (#68)

[1.108.0] - 2025-07-24
---------------------

### New Features

- metrics - feat: add metrics_optional_domains and metrics_optional_packages for users to configure optional domains (#245)

### Bug Fixes

- metrics - fix: add missing Spark import/export support for metrics - part 2 (#246)

[1.107.0] - 2025-07-24
---------------------

### New Features

- keylime_server - feat: add openSUSE Leap 15.6 to integration test matrix (#82)

### Bug Fixes

- ha_cluster - fix: use empty init to prevent old ansible issues (#294)
- podman - fix: do not mix facts with vars (#236)
- storage - fix: the encryption_key parameter should not be marked as no_log (#546)
- storage - fix: Show better error when trying to create RAID without enough disks  (#545)

[1.106.1] - 2025-07-15
---------------------

### Bug Fixes

- postfix - fix: configure postfix to listen only to IPv4 if IPv6 is disabled (#187)
- selinux - fix: tempdir path not defined in check mode; __selinux_item.path may be undefined (#289)

[1.106.0] - 2025-07-09
---------------------

### New Features

- ha_cluster - feat: export cluster resources (#288)
- journald - feat: Add MaxRetention configuration (#113)

### Bug Fixes

- sudo - fix: ensure single space before TYPE, ROLE, and correctly format those values (#65)

[1.105.0] - 2025-07-03
---------------------

### New Features

- ad_integration - feat: search for name of domain/realm in sssd.conf; merge settings if duplicates (#145)
- bootloader - feat: Add ability to configure default kernel (#147)
- cockpit - feat: add sles 16 support (#227)
- metrics - feat: Support this role in container builds (#243)

### Bug Fixes

- ha_cluster - fix: ensure /var/lib/pcsd exists (#285)

[1.104.1] - 2025-06-25
---------------------

### Bug Fixes

- bootloader - fix: Fix removing kernel options with values (#146)

[1.104.0] - 2025-06-23
---------------------

### New Features

- certificate - feat: Support this role in container builds (#277)
- crypto_policies - feat: Support this role in container environments and builds (#151)
- ha_cluster - feat: crmsh SLES 16 changes and introduction of zypper patterns (#283)
- nbde_server - feat: Support this role in container builds (#188)
- selinux - feat: Support selinux_modules during bootc builds (#284)
- selinux - feat: Support selinux_fcontexts during bootc builds (#283)
- ssh - feat: Support this role in container environments and builds (#185)

### Bug Fixes

- nbde_client - fix: Adjust for Ansible 2.19 (#206)
- postgresql - fix: Fix removing sql script from the host after inputting it (#131)
- ssh - fix: Avoid setting ansible_managed variable (#189)
- sudo - fix: Avoid append() in sudoers file template (#62)
- sudo - fix: Avoid setting ansible_managed variable (#61)

[1.103.0] - 2025-06-21
---------------------

### New Features

- sshd - feat: Add new options from OpenSSH 10.0 (#312)

### Bug Fixes

- sshd - fix: service: Add default Environment option (#308)

[1.102.0] - 2025-06-17
---------------------

### New Features

- aide - feat: add Suse support (#31)
- journald - feat: Add support for SystemKeepFree journald.conf option (#109)
- postgresql - feat: Support this role in container builds (#125)
- selinux - feat: Partially support this role in container builds (#277)

### Bug Fixes

- postgresql - fix: Fixes for Ansible 2.19 (#129)
- snapshot - fix: correct issues with LC_ALL and LVM_COMMAND_PROFILE and snapshot manager (#112)
- storage - fix: Fix getting PVs from raid_disks for RAID LVs (#536)
- tlog - fix: Set __is_system_running in check mode (#172)

[1.101.1] - 2025-05-31
---------------------

### Bug Fixes

- selinux - fix: Set the kernel command line selinux parameter correctly when changing selinux state (#275)

[1.101.0] - 2025-05-21
---------------------

### New Features

- cockpit - feat: Support this role in container builds (#212)
- firewall - feat: Support this role in container builds (#274)
- tlog - feat: Support this role in container builds (#164)

### Bug Fixes

- certificate - fix: update python package dependencies for SLE 16 (#270)
- cockpit - fix: Consider "degraded" systemd state as booted (#217)
- cockpit - fix: Ignore extra lines in dnf repoquery parsing (#214)
- firewall - fix: Fix "interface_pci_id" role option (#278)
- firewall - fix: Fix "helpers" service option (#277)
- tlog - fix: Consider "degraded" systemd state as booted (#166)

[1.100.1] - 2025-05-20
---------------------

### Other Changes

- no user-visible changes

[1.100.0] - 2025-05-19
---------------------

### New Features

- snapshot - feat: add support for snapshot manager backing the role (#97)

[1.99.1] - 2025-05-16
---------------------

### Bug Fixes

- storage - fix: Show error when trying to put LVM volume on partition pool (#531)
- storage - fix: Allow small size differences to match the device min size (#526)

[1.99.0] - 2025-05-15
---------------------

### New Features

- logging - feat: Support this role in container builds (#444)

### Bug Fixes

- logging - fix: Consider "degraded" systemd state as booted (#449)

[1.98.0] - 2025-05-06
---------------------

### New Features

- metrics - feat: add missing Spark import/export support for metrics (#233)

[1.97.3] - 2025-05-05
---------------------

### Other Changes

- no user-visible changes

[1.97.2] - 2025-05-02
---------------------

### Bug Fixes

- storage - fix: Correctly check PVs for grow_to_fill feature (#523)

[1.97.1] - 2025-04-29
---------------------

### Bug Fixes

- systemd - fix: files and templates in nested directories are not placed correctly (#89)

[1.97.0] - 2025-04-28
---------------------

### New Features

- ad_integration - feat: Introduced option to skip package installation (#131)

### Bug Fixes

- systemd - fix: unmask should run at the begin to allow the role to manage the units (#87)

[1.96.0] - 2025-04-23
---------------------

### New Features

- firewall - feat: support includes for services (#259)
- ha_cluster - feat: crmsh remove python3-rpm dependency (#270)
- ha_cluster - feat: export pcsd and OS configuration (#264)
- podman - feat: support TOML tables by using a real TOML formatter (#218)
- timesync - feat: add support for timesync_ntp_ip_family (#277)

### Bug Fixes

- cockpit - fix: Dynamically ignore cockpit-pcp (#206)
- cockpit - fix: Run Fedora 42 with dnf instead of default setup (#205)
- cockpit - fix: Ignore cockpit-pcp on RedHat 9 (#204)
- ha_cluster - fix: disable proxy when connecting to pcsd local socket (#265)
- ha_cluster - fix: restart qdevice when its certificates have been regenerated (#262)
- logging - fix: Only remove rsyslog* packages, remove packages with command line (#440)
- logging - fix: Add a variable for rsyslog base package on Debian (#436)
- network - fix: Correct attribute checks for routing rule validation (#774)
- network - fix: Remove MAC address matching from SysUtil.link_info_find() (#769)
- network - fix: Refine MAC validation using interface name (#768)
- podman - fix: Do not change the directory mode for the container parent path (#216)
- podman - fix: Do not restart logind unless absolutely necessary (#213)
- podman - fix: render boolean option values correctly in toml files (#209)
- timesync - fix: add default seccomp filters for el9/10 (#279)

[1.95.7] - 2025-03-06
---------------------

### Bug Fixes

- storage - fix: there is no kmod-kvdo on EL10 and later (#514)

[1.95.6] - 2025-02-26
---------------------

### Other Changes

- no user-visible changes

[1.95.5] - 2025-02-13
---------------------

### Other Changes

- no user-visible changes

[1.95.4] - 2025-02-11
---------------------

### Bug Fixes

- aide - fix: aide --check should not report changed (#19)

[1.95.3] - 2025-02-04
---------------------

### Other Changes

- no user-visible changes

[1.95.2] - 2025-02-04
---------------------

### Other Changes

- no user-visible changes

[1.95.1] - 2025-02-03
---------------------

### Bug Fixes

- storage - fix: ensure ostree has libblockdev and libblockdev-loop (#509)

[1.95.0] - 2025-02-01
---------------------

### New Features

- aide - feat: ensure role works on ostree systems (#15)

[1.94.2] - 2025-01-27
---------------------

### Bug Fixes

- ha_cluster - fix: update for EL10 (#254)
- rhc - fix: use the right systemd service for remediations in EL 10+ (#209)
- storage - fix: Fix PV grow_to_fill feature  (#502)

[1.94.1] - 2025-01-09
---------------------

### New Features

- aide - feat: Allow setup aide inside of cron job (#7)

### Bug Fixes

- network - fix: Prioritize find link info by permanent MAC address, with fallback to current address (#749)
- podman - fix: get user information for secrets (#198)
- ssh - fix: Workaround for CentOS 10 issues in openssh (#167)

[1.94.0] - 2025-01-07
---------------------

### New Features

- sshd - feat: Use sshd_config instead of sshd which has been deprecated (#299)
- sshd - feat: New options in OpenSSH + fixes for bugx in OpenSSH 9.9p1 (#304)

### Bug Fixes

- sshd - fix: Reload the service when needed (#303)
- sshd - fix: use quote with command, shell and validate with variable (#298)

[1.93.0] - 2024-12-13
---------------------

### New Features

- ha_cluster - feat: Remove python expect dependency in crmsh (#249)

[1.92.1] - 2024-12-09
---------------------

### Bug Fixes

- ha_cluster - fix: update constraints commands syntax for pcs-0.12 (#245)
- systemd - fix: Always become user we are managing (#73)

[1.92.0] - 2024-12-09
---------------------

### New Features

- ha_cluster - feat: export corosync configuration (#231)

### Bug Fixes

- ha_cluster - fix: list cloud agent packages by architecture (#244)

[1.91.0] - 2024-12-04
---------------------

### New Features

- postfix - feat: support postfix_default_database_type (#165)

### Bug Fixes

- certificate - fix: Workaround getcert issue when cert key-file is missing (#243)
- storage - fix: VDO tests and packages fixes for Fedora and RHEL 10 (#490)

[1.90.3] - 2024-11-20
---------------------

### Other Changes

- no user-visible changes

[1.90.2] - 2024-11-19
---------------------

### Bug Fixes

- gfs2 - fix: remove el10 support (#33)
- metrics - fix: Use correct syntax for keyserver port and test check
- metrics - fix: use __grafana_keyserver_datasource_type variable instead of its string value

[1.90.1] - 2024-11-13
---------------------

### Other Changes

- no user-visible changes

[1.90.0] - 2024-11-12
---------------------

### New Features

- aide - New Role
- logging - feat: support custom templates (#425)
- podman - feat: support for Pod quadlets (#190)
- systemd - feat: support user units (#67)

[1.89.1] - 2024-11-06
---------------------

### Other Changes

- no user-visible changes

[1.89.0] - 2024-10-31
---------------------

### New Features

- ha_cluster - feat: crmsh 4.6.0 support and stonith-enabled workflow update (#232)
- network - feat: Support `wait_ip` property (#741)
- network - feat: Support autoconnect_retries (#737)
- sudo - feat: Add variable that handles semantic check for sudoers (#22)

### Bug Fixes

- firewall - fix: Prevent interface definitions overriding 'changed' value when other elements are changed (#241)
- metrics - fix: add leading triple-hyphen to all github workflow files (#214)
- metrics - fix: add support for Valkey (#212)
- podman - fix: make role work on el 8.8 and el 9.2 and podman version less than 4.7.0 (#188)
- podman - fix: ignore pod not found errors when removing kube specs (#186)
- postgresql - fix: postgresql_cert_name didn't work properly, using this parameter (#102)

[1.88.9] - 2024-09-13
---------------------

### Other Changes

- no user-visible changes

[1.88.8] - 2024-09-11
---------------------

### Bug Fixes

- podman - fix: Cannot remove volumes from kube yaml - need to convert yaml to list (#180)

[1.88.7] - 2024-09-04
---------------------

### Bug Fixes

- podman - fix: subgid maps user to gids, not group to gids (#178)

[1.88.6] - 2024-08-30
---------------------

### Other Changes

- no user-visible changes

[1.88.5] - 2024-08-29
---------------------

### Bug Fixes

- fapolicyd - fix: use journalctl -t fapolicyd to get fapolicyd log messages (#41)
- storage - fix: Skip Stratis tests on RHEL 8 and document Stratis support (#482)
- storage - fix: Use blkid instead of lsblk in tests to get partition table (#480)

[1.88.4] - 2024-08-26
---------------------

### Bug Fixes

- kernel_settings - fix: detect profile parent directory (#222)

[1.88.3] - 2024-08-22
---------------------

### New Features

- gfs2 - feat: role does not work on el10, aarch64 (#25)

[1.88.2] - 2024-08-22
---------------------

### Bug Fixes

- storage - fix: add stratis to list of packages for ostree (#478)

[1.88.1] - 2024-08-22
---------------------

### Bug Fixes

- ha_cluster - fix: openssl is now required for password (#227)

[1.88.0] - 2024-08-20
---------------------

### New Features

- sshd - feat: Add new configuration options from OpenSSH 9.8

### Bug Fixes

- ha_cluster - fix: Fixes for new pcs and ansible (#223)

[1.87.2] - 2024-08-19
---------------------

### Other Changes

- no user-visible changes

[1.87.1] - 2024-08-16
---------------------

### Bug Fixes

- storage - fix: architecture is now a required fact (#473)

[1.87.0] - 2024-08-16
---------------------

### New Features

- podman - feat: Handle reboot for transactional update systems (#170)
- timesync - feat: Handle reboot for transactional update systems (#256)

[1.86.0] - 2024-08-09
---------------------

### New Features

- network - feat: Add the support for the optional route source parameter in nm provider (#714)

### Bug Fixes

- kernel_settings - fix: Use tuned files instead of using it as a module (#220)
- rhc - fix: drop usage of "auto_attach" of the "redhat_subscription" module (#189)
- storage - fix: Add libblockdev s390 and FS plugins to blivet dependencies list (#467)

[1.85.0] - 2024-08-01
---------------------

### New Features

- crypto_policies - Handle reboot for transactional update systems (#121)
- ha_cluster - feat: Add alerts support (#218)
- ha_cluster - feat: crmsh watchdog correction, remove obsolete assert for softdog (#217)
- kernel_settings - Handle reboot for transactional update systems (#215)
- ssh - Handle reboot for transactional update systems (#151)
- sudo - Handle reboot for transactional update systems (#16)

### Bug Fixes

- nbde_server - fix: Remove hard dependency on selinux and firewall roles (#154)
- podman - fix: Ensure user linger is closed on EL10 (#165)
- storage - fix: Remove partition table from disk removed from a VG (#464)

[1.84.0] - 2024-07-23
---------------------

### New Features

- logging - feat: add support for file and directory mode/owner/group for output files (#400)
- logging - feat: support custom config files with logging_custom_config_files (#399)
- logging - feat: add support for reopen_on_truncate for files input (#398)
- selinux - feat: add support for transactional update (#241)
- storage - feat: write storage role fingerprint to /etc/fstab (#458)

### Bug Fixes

- podman - fix: proper cleanup for networks; ensure cleanup of resources (#160)
- podman - fix: add support for EL10 (#159)
- sshd - fix: add support for EL10 (#293)

[1.83.1] - 2024-07-17
---------------------

### Bug Fixes

- network - fix: network_state must be defined in defaults/main.yml (#702)

[1.83.0] - 2024-07-15
---------------------

### New Features

- firewall - feat: Handle reboot for transactional update systems (#226)
- postfix - feat: Added postfix_files feature as a simple means to add extra files/maps to config (#129)
- snapshot - feat: rewrite snapshot.py as an Ansible module / add support for thin origins (#58)
- systemd - feat: add support for transactional update (#53)

### Bug Fixes

- metrics - fix: add support for EL10 (#200)
- metrics - fix: add configuration files for c10s and el10 (#199)
- postfix - fix: add support for EL10 (#134)
- snapshot - fix: add support for EL10 (#66)

[1.82.0] - 2024-07-02
---------------------

### New Features

- ha_cluster - feat: crmsh corosync jinja2 template rework (#212)
- nbde_client - feat: Allow initrd configuration to be skipped (#165)

### Bug Fixes

- ad_integration - fix: add support for EL10 (#102)
- bootloader - fix: add support for EL10 (#109)
- certificate - fix: add support for EL10 (#229)
- cockpit - fix: add support for EL10 (#163)
- cockpit - fix: wildcard package installation not working with dnf module (#161)
- crypto_policies - fix: add support for EL10 (#118)
- fapolicyd - fix: add support for EL10 (#28)
- firewall - fix: add support for EL10 (#224)
- gfs2 - fix: add support for EL10 (#17)
- journald - fix: add support for EL10 (#73)
- kdump - fix: add support for EL10 (#206)
- kdump - fix: el10 kdump role should depend on kdump-utils (#204)
- kernel_settings - fix: add support for EL10 (#207)
- keylime_server - fix: add support for EL10 (#46)
- logging - fix: add support for EL10 (#395)
- nbde_client - fix: add support for EL10 (#166)
- nbde_server - fix: add support for EL10 (#150)
- network - fix: add support for EL10 (#700)
- postgresql - fix: add support for EL10 (#93)
- rhc - fix: add support for EL10 (#184)
- selinux - fix: add support for EL10 (#239)
- ssh - fix: add support for EL10 (#149)
- storage - fix: add support for EL10 (#452)
- sudo - fix: add support for EL10 (#12)
- systemd - fix: add support for EL10 (#51)
- timesync - fix: Don't use chrony-dhcp sourcedir on EL8 systems (#246)
- timesync - fix: add support for EL10 (#245)
- tlog - fix: add support for EL10 (#133)
- vpn - fix: add support for EL10 (#160)

[1.81.0] - 2024-06-24
---------------------

### New Features

- sudo - New Role

[1.80.0] - 2024-06-22
---------------------

### New Features

- sshd - feat:  Ubuntu Noble support (#290)

### Bug Fixes

- sshd - fix: Ubuntu 22.04 PrintMotd set default to false (#290)

[1.79.0] - 2024-06-12
---------------------

### New Features

- ssh - feat: Add new configuration options and remove false positives in the test (#142)
- storage - feat: Stratis support (#439)
- storage - feat: PV resize support (#438)

### Bug Fixes

- bootloader - fix: Set user.cfg path to /boot/grub2/ on EL 9 UEFI (#101)
- logging - fix: Add check for "rsyslogd: error" in /var/log/messages in all tests (#388)
- podman - fix: grab name of network to remove from quadlet file (#155)
- postfix - fix: Reflect smtp-submission service rename in EL 10 and Fedora 40+ (#131)
- storage - fix: Fix expected error message in tests_misc.yml (#446)
- storage - fix: Get same sector size disks for multi device LVM tests (#441)
- storage - fix: Fix 'possibly-used-before-assignment' pylint issues (#440)

[1.78.2] - 2024-05-22
---------------------

### Bug Fixes

- logging - fix: Remove name="basics_imuxsock" parameter from imuxsock type input (#385)

[1.78.1] - 2024-04-26
---------------------

### Other Changes

- no user-visible changes

[1.78.0] - 2024-04-25
---------------------

### New Features

- gfs2 - New Role

[1.77.0] - 2024-04-23
---------------------

### New Features

- ha_cluster - feat: Add support for utilization (#202)
- ha_cluster - feat: crmsh enhancements, master slave, validations (#197)
- podman - feat: manage TLS cert/key files for registry connections and validate certs (#146)
- podman - feat: support podman_credential_files (#142)
- podman - feat: support registry_username and registry_password (#141)

### Bug Fixes

- bootloader - fix: Fail on the s390x architecture with a not supported msg (#96)
- ha_cluster - fix: make consistent approach for multiple node attributes sets (#201)
- podman - fix: make kube cleanup idempotent (#144)
- podman - fix: do not use become for changing hostdir ownership, and expose subuid/subgid info (#139)
- podman - fix: use correct user for cancel linger file name (#138)
- storage - fix: Fix recreate check for formats without labelling support (#435)

[1.76.2] - 2024-04-13
---------------------

### Other Changes

- no user-visible changes

[1.76.1] - 2024-04-07
---------------------

### Bug Fixes

- sshd - fix: Document and streamline the sshd_main_config_file (#281)

[1.76.0] - 2024-04-05
---------------------

### New Features

- ha_cluster - feat: ha_cluster_node_options allows per-node addresses and SBD options to be set (#196)
- ha_cluster - feat: easily install cloud agents (#194)
- ha_cluster - feat: Add support for ACL (#193)
- ha_cluster - feat: SLES15 enablement, HAE detection (#192)
- journald - feat: Add options for rate limit interval and burst (#64)

### Bug Fixes

- bootloader - fix: Add /etc/default/grub if missing (#93)
- network - fix: Allow network to restart when wireless or team connection is specified (#675)

[1.75.4] - 2024-04-04
---------------------

### Bug Fixes

- rhc - fix: Ignore ansible_host: "" (#169)

[1.75.3] - 2024-03-15
---------------------

### Bug Fixes

- podman - fix: Add support for --check flag (#134)

[1.75.2] - 2024-03-09
---------------------

### Bug Fixes

- ad_integration - fix: Sets domain name lower case in realmd.conf section header (#88)

[1.75.1] - 2024-02-27
---------------------

### Bug Fixes

- bootloader - fix: Fix bug with extra spaces in variables (#88)
- bootloader - fix: Fix the role for UEFI systems (#90)

[1.75.0] - 2024-02-22
---------------------

### New Features

- rhc - feat: Add a display name parameter (#166)

### Bug Fixes

- snapshot - fix: better error handling for all platforms and ansible versions (#47)

[1.74.0] - 2024-02-21
---------------------

### New Features

- snapshot - feat: add support for snapshot_lvm_vg_include (#39)

### Bug Fixes

- snapshot - fix: ensure role is idempotent and supports check mode (#41)
- snapshot - fix: ostree test failures - use /var/mnt (#37)

[1.73.3] - 2024-02-20
---------------------

### Bug Fixes

- sshd - fix: Fix service files generated on EL7 and workaround the tests for containers (#276)

[1.73.2] - 2024-02-16
---------------------

### Bug Fixes

- ad_integration - fix: Add default_ipv4 to required_facts to gather ansible_hostname (#84)
- nbde_server - fix: Allow tangd socket override directory to be managed outside of the role (#139)

[1.73.1] - 2024-02-15
---------------------

### Other Changes

- no user-visible changes

[1.73.0] - 2024-02-14
---------------------

### New Features

- ha_cluster - feat: crmsh workflow and SUSE support (#186)
- snapshot - feat: add support mounting/unmounting snapshots and origins (#34)
- snapshot - feat: add support for the "list" command (#31)
- snapshot - feat: add support to extending existing snapshots to required percentage (#22)

### Bug Fixes

- snapshot - fix: rename the clean command to remove (#24)

[1.72.2] - 2024-02-10
---------------------

### Bug Fixes

- bootloader - fix: Modify grub timeout in grub config directly (#86)

[1.72.1] - 2024-02-09
---------------------

### Bug Fixes

- podman - fix: ensure user linger is enabled and disabled correctly (#127)

[1.72.0] - 2024-02-08
---------------------

### New Features

- ha_cluster - feat: add support for configuring node attributes (#184)

[1.71.1] - 2024-02-01
---------------------

### Other Changes

- no user-visible changes

[1.71.0] - 2024-01-28
---------------------

### New Features

- storage - feat: Enable GFS2 support in blivet (#418)

[1.70.0] - 2024-01-27
---------------------

### New Features

- snapshot - feat: add support for reverting LV back to state of snapshot  (#15)

### Bug Fixes

- sshd - fix: Review and update service units and socket unit to include distribution defaults

[1.69.0] - 2024-01-24
---------------------

### New Features

- snapshot - New Role

[1.68.0] - 2024-01-24
---------------------

### New Features

- rhc - feat: add ansible host parameter to insights configuration (#155)

### Bug Fixes

- podman - fix: cast secret data to string in order to allow JSON valued strings (#122)

[1.67.0] - 2024-01-18
---------------------

### New Features

- network - feat: Support blackhole, prohibit and unreachable route types  (#662)

### Bug Fixes

- keylime_server - fix: add timeout for registrar service - use 30 second timeout for registrar and verifier
- postgresql - fix: Enable PostgreSQL stream selection for c9s and RHEL9 (#72)

[1.66.0] - 2024-01-17
---------------------

### New Features

- ad_integration - feat: add ad_integration_preserve_authselect_profile (#79)
- ad_integration - feat: Add SSSD parameters support (#76)

### Bug Fixes

- journald - fix: Compress applies to all storage modes, SyncInterval only to persistent (#58)
- podman - fix: name of volume quadlet service should be basename-volume.service (#119)

[1.65.1] - 2024-01-11
---------------------

### Bug Fixes

- journald - fix: ForwardToSyslog only set for volatile (#56)

[1.65.0] - 2024-01-09
---------------------

### New Features

- bootloader - New Role
- journald - feat: Adding support for ForwardToSyslog (#54)

[1.64.0] - 2023-12-13
---------------------

### New Features

- metrics - feat: support for ostree systems
- metrics - feat: sync with latest ansible-pcp (#178)
- rhc - feat: support again EL7 (#151)
- storage - feat: Added support for creating shared LVM setups (#388)

### Bug Fixes

- metrics - fix: add missing pmie webhook action configuration functionality (#183)
- podman - fix: add no_log: true for tasks that can log secret data (#113)
- ssh - fix: Fix warning for using jinja templates in assert (#131)

[1.63.0] - 2023-12-09
---------------------

### New Features

- fapolicyd - feat: several role improvements (#8)
- postgresql - feat: Enable support for Postgresql 16 (#68)

### Bug Fixes

- logging - fix: ansible-core-2.16 - only use to_nice_json for output formatting (#374)
- logging - fix: avoid conf of RatelimitBurst when RatelimitInterval is zero (#373)
- selinux - fix: Print an error message when module to be created doesn't exist (#218)
- selinux - fix: no longer use "item" as a loop variable (#217)

[1.62.1] - 2023-12-07
---------------------

### Bug Fixes

- ha_cluster - fix: set sbd.service timeout based on SBD_START_DELAY (#169)

[1.62.0] - 2023-12-05
---------------------

### New Features

- rhc - feat: support for ostree systems (#145)

[1.61.1] - 2023-12-02
---------------------

### Bug Fixes

- ha_cluster - fix: manage firewall on qnetd hosts (#166)

[1.61.0] - 2023-12-01
---------------------

### New Features

- ssh - feat: support for ostree systems (#124)
- sshd - feat: support for ostree systems (#270)

### Bug Fixes

- network - fix: Allow address 0.0.0.0/0 or ::/0 for 'from'/'to' in a routing rule (#649)
- sshd - fix: Avoid creation of runtime directories in home (#265)

[1.60.0] - 2023-11-30
---------------------

### New Features

- ad_integration - feat: support for ostree systems (#68)
- ad_integration - feat: Add sssd custom settings (#64)
- cockpit - feat: support for ostree systems (#133)
- crypto_policies - feat: support for ostree systems (#99)
- ha_cluster - feat: support for ostree systems (#159)
- journald - feat: support for ostree systems (#46)
- kernel_settings - feat: support for ostree systems (#180)
- keylime_server - feat: support for ostree systems (#24)
- nbde_server - feat: support for ostree systems (#124)
- podman - feat: support for ostree systems (#105)
- postgresql - feat: support for ostree systems (#62)
- systemd - feat: support for ostree systems (#29)
- timesync - feat: support for ostree systems (#224)
- tlog - feat: support for ostree systems (#111)
- vpn - feat: support for ostree systems (#134)

[1.59.0] - 2023-11-27
---------------------

### New Features

- fapolicyd - New Role

[1.58.1] - 2023-11-23
---------------------

### Bug Fixes

- selinux - fix: fix ansible-lint issues (#210)

[1.58.0] - 2023-11-10
---------------------

### New Features

- network - feat: support for ostree systems (#650)
- storage - feat: Support for creating volumes without a FS (#400)

[1.57.2] - 2023-11-09
---------------------

### Other Changes

- no user-visible changes

[1.57.1] - 2023-11-08
---------------------

### Other Changes

- no user-visible changes

[1.57.0] - 2023-11-07
---------------------

### New Features

- ha_cluster - feat: add an option to enable Resilient Storage rpm repository (#158)
- kdump - feat: support for ostree systems (#182)
- logging - feat: Add support for general queue and general action parameters (#364)
- logging - feat: Add support for the global config option preserveFQDN with a new logg… (#362)
- logging - feat: support for ostree systems (#360)
- metrics - feat: support for ostree systems (#175)
- postfix - feat: support for ostree systems (#110)
- storage - feat: support for ostree systems (#399)

### Bug Fixes

- ha_cluster - fix: cast sbd option value to string (#160)
- logging - fix: check that logging_max_message_size is set, not rsyslog_max_message_size (#361)

[1.56.0] - 2023-10-27
---------------------

### New Features

- certificate - feat: support for ostree systems (#203)
- firewall - feat: support for ostree systems (#191)
- selinux - feat: support for ostree systems (#206)

[1.55.1] - 2023-10-25
---------------------

### Bug Fixes

- network - fix: Add dhcp client package dependency for initscripts provider (#639)

[1.55.0] - 2023-10-24
---------------------

### New Features

- ha_cluster - feat: Add support for configuring stonith levels (#147)

### Bug Fixes

- selinux - fix: Use `ignore_selinux_state` module option (#194)
- sshd - fix: Symlink sub-directories under tests/roles/ansible-sshd to avoid recursive loop (#262)
- storage - fix: Do not remove swap at every run (#396)

[1.54.2] - 2023-09-27
---------------------

### Bug Fixes

- selinux - fix: make role work again on Suse - not officially supported (#195)

[1.54.1] - 2023-09-20
---------------------

### Other Changes

- no user-visible changes

[1.54.0] - 2023-09-14
---------------------

### New Features

- sshd - feat: manage ssh certificates (#252)

### Bug Fixes

- sshd - fix: Makes runtime dir relative (#249)
- sshd - fix: Support inject_facts_as_vars = false (#244)

[1.53.7] - 2023-09-13
---------------------

### Bug Fixes

- kdump - fix: retry read of kexec_crash_size (#169)

[1.53.6] - 2023-09-12
---------------------

### Other Changes

- no user-visible changes

[1.53.5] - 2023-09-09
---------------------

### Other Changes

- no user-visible changes

[1.53.4] - 2023-08-22
---------------------

### Bug Fixes

- ad_integration - fix: use command stdin for password, and do not log password (#51)

[1.53.3] - 2023-08-18
---------------------

### Bug Fixes

- firewall - fix: files: overwrite firewalld.conf on previous replaced (#176)
- kdump - fix: Ensure authorized_keys management works with multiple hosts (#165)
- kdump - fix: ensure .ssh directory exists for kdump_ssh_user on kdump_ssh_server (#164)
- storage - fix: use stat.pw_name, stat.gr_name instead of owner, group (#377)

[1.53.2] - 2023-08-17
---------------------

### Bug Fixes

- kdump - fix: Write new authorized_keys if needed is not idempotent (#162)
- kdump - fix: do not fail if authorized_keys not found (#161)

[1.53.1] - 2023-08-16
---------------------

### Other Changes

- no user-visible changes

[1.53.0] - 2023-08-12
---------------------

### New Features

- ad_integration - feat: Enable AD dynamic DNS updates (#48)

[1.52.2] - 2023-08-11
---------------------

### Bug Fixes

- podman - fix: user secret support (#91)

[1.52.1] - 2023-08-10
---------------------

### Other Changes

- no user-visible changes

[1.52.0] - 2023-08-09
---------------------

### New Features

- firewall - feat: define, modify, and remove ipsets (#166)

[1.51.2] - 2023-08-03
---------------------

### Other Changes

- no user-visible changes

[1.51.1] - 2023-08-02
---------------------

### Bug Fixes

- podman - fix: require the crun package on EL8 (#88)

[1.51.0] - 2023-08-01
---------------------

### New Features

- firewall - feat: add new arg firewalld_conf, subarg allow_zone_drifting (#162)

### Bug Fixes

- firewall - fix: firewall_lib: make try_set_zone_of_interface idempotent (#167)
- firewall - fix: error when running with check mode and previous: replaced (#163)
- rhc - fix: use rhc_organization and rhc_baseurl only when specified (#127)

[1.50.1] - 2023-07-31
---------------------

### Bug Fixes

- kdump - fix: use failure_action instead of default on EL9 and later (#155)

[1.50.0] - 2023-07-28
---------------------

### New Features

- podman - feat: allow not pulling images, continue if pull fails (#82)

### Bug Fixes

- podman - fix: support global options in config files (#83)

[1.49.1] - 2023-07-27
---------------------

### Bug Fixes

- systemd - fix: allow .j2 suffix for templates, strip off for file/service names (#12)

[1.49.0] - 2023-07-24
---------------------

### New Features

- keylime_server - New Role

[1.48.1] - 2023-07-22
---------------------

### Bug Fixes

- firewall - fix: reload on resetting to defaults (#159)

[1.48.0] - 2023-07-20
---------------------

### New Features

- systemd - New Role - manage systemd units

[1.47.1] - 2023-07-20
---------------------

### Bug Fixes

- network - fix: facts being gathered unnecessarily (#628)

[1.47.0] - 2023-07-20
---------------------

### New Features

- ha_cluster - feat: cluster and quorum can have distinct passwords (#134)
- podman - feat: add support for quadlet, secrets (#78)
- postgresql - feat: Enable support for Postgresql 15 (#44)

### Bug Fixes

- ad_integration - fix: facts being gathered unnecessarily (#46)
- certificate - fix: facts being gathered unnecessarily (#187)
- certificate - fix: Re-issue certificate if key size changes (#188)
- cockpit - fix: facts being gathered unnecessarily (#116)
- crypto_policies - fix: facts being gathered unnecessarily (#84)
- firewall - fix: facts being gathered unnecessarily (#156)
- firewall - fix: unmask firewalld on run, disable conflicting services (#154)
- firewall - fix: make enabling/disabling non-existent services not fail in check mode (#153)
- ha_cluster - fix: facts being gathered unnecessarily (#139)
- ha_cluster - fix: various minor fixes (#137)
- journald - fix: facts being gathered unnecessarily (#31)
- kdump - fix: facts being gathered unnecessarily (#152)
- kernel_settings - fix: facts being gathered unnecessarily (#163)
- logging - fix: facts being gathered unnecessarily (#341)
- nbde_client - fix: facts being gathered unnecessarily (#127)
- nbde_server - fix: facts being gathered unnecessarily (#110)
- podman - fix: facts being gathered unnecessarily (#80)
- postfix - fix: facts being gathered unnecessarily (#96)
- postgresql - fix: facts being gathered unnecessarily (#43)
- rhc - fix: facts being gathered unnecessarily (#124)
- rhc - fix: enable remediation only on RHEL >= 8.4 (#116)
- selinux - fix: facts being gathered unnecessarily (#180)
- ssh - fix: facts being gathered unnecessarily (#106)
- ssh - fix: Fix rendering Match/Host defaults when user provides their own (#104)
- storage - fix: facts being gathered unnecessarily (#374)
- storage - fix: RAID volume pre cleanup  (#169)
- timesync - fix: facts being gathered unnecessarily (#202)
- tlog - fix: facts being gathered unnecessarily (#97)
- vpn - fix: facts being gathered unnecessarily (#120)

[1.46.0] - 2023-07-11
---------------------

### New Features

- network - feat: Support "no-aaaa" DNS option (#619)
- network - feat: add AlmaLinux to RHEL compat distro list (#618)

[1.45.1] - 2023-07-09
---------------------

### Bug Fixes

- storage - fix: Test issue when creating fs /w invalid param (#367)

[1.45.0] - 2023-07-08
---------------------

### New Features

- certificate - feat: Allow setting certificate and key files mode (#175)

[1.44.0] - 2023-06-23
---------------------

### New Features

- ssh - feat: add ssh_backup option with default true (#91)

[1.43.0] - 2023-06-23
---------------------

### New Features

- storage - feat: Add support for filesystem online resize (#356)

[1.42.2] - 2023-06-22
---------------------

### Bug Fixes

- firewall - fix: Don't install python(3)-firewall it's a dependency of firewalld (#148)

[1.42.1] - 2023-06-21
---------------------

### Other Changes

- no user-visible changes

[1.42.0] - 2023-06-20
---------------------

### New Features

- sshd - feat: Fix alpine tests by adding a new configuration options (#240)
- sshd - feat: debian 12 support and small config fixes for debian (#238)

[1.41.1] - 2023-06-09
---------------------

### Other Changes

- no user-visible changes

[1.41.0] - 2023-06-07
---------------------

### New Features

- storage - feat: Add support for setting stripe size for LVM RAID (#357)

[1.40.0] - 2023-05-31
---------------------

### New Features

- network - feat: Support ipv4_ignore_auto_dns and ipv6_ignore_auto_dns settings
- storage - feat: User-specified mount point owner and permissions

### Bug Fixes

- nbde_server - fix: README.md headers should not be more than 72 characters
- storage - fix: Allow using raid_chunk_size for RAID pools and volumes

[1.39.0] - 2023-05-28
---------------------

### New Features

- kdump - feat: Add support for auto_reset_crashkernel and dracut_args
- selinux - feat: Use `restorecon -T 0` on Fedora and RHEL > 8

### Bug Fixes

- kdump - fix: do not use /etc/sysconfig/kdump
- kdump - fix: use grubby to update crashkernel=auto if needed
- metrics - fix: make role work on ansible-core 2.15
- podman - fix: make role work on ansible-core 2.15

[1.38.3] - 2023-05-27
---------------------

### Bug Fixes

- logging - fix: work with ansible-core 2.15

[1.38.2] - 2023-05-24
---------------------

### Bug Fixes

- rhc - fix: fix filename with insights-client tags
- tlog - fix: Switch SSSD files provider to Proxy Provider

[1.38.1] - 2023-05-04
---------------------

### Other Changes

- no user-visible changes

[1.38.0] - 2023-04-29
---------------------

### New Features

- sshd - feat: add support for FreeBSD, OpenBSD

[1.37.0] - 2023-04-28
---------------------

### New Features

- ad_integration - Add 'ad_integration_force_rejoin' role variable (#29)

### Bug Fixes

- podman - fix: graphroot required in storage.conf on Fedora 37
- podman - fix: Use match instead of in for test for jinja 2.7 support

[1.36.4] - 2023-04-18
---------------------

### Other Changes

- no user-visible changes

[1.36.3] - 2023-04-15
---------------------

### Bug Fixes

- rhc - Do not pass fake creds when activation keys are specified (#92)

[1.36.2] - 2023-04-12
---------------------

### Other Changes

- no user-visible changes

[1.36.1] - 2023-04-08
---------------------

### Bug Fixes

- sshd - Fedora 38 has no longer non-standard hostkey permissions

[1.36.0] - 2023-04-07
---------------------

### New Features

- ha_cluster - add support for resource and operation defaults
- ha_cluster - Add possibility to load SBD watchdog kernel modules (#82)

### Bug Fixes

- ha_cluster - use pcs to setup qdevice certificates if available
- kdump - Use ansible_os_family in template (#133)
- ssh - Proper indent when lists are used in block (#80)
- ssh - add vars files for Rocky 8/9 (links) (#81)
- timesync - Update chrony.conf location for Debian (#187)

[1.35.2] - 2023-03-17
---------------------

### Bug Fixes

- rhc - README: improve the role documentation a bit (#76)
- rhc - workaround insights-client issue with /usr/bin/python

[1.35.1] - 2023-02-21
---------------------

### Bug Fixes

- network - initscripts: Configure output device in routes

[1.35.0] - 2023-02-16
---------------------

### New Features

- rhc - Implement "rhc_state: reconnect" (#43)
- rhc - Implement "rhc_insights.remediation"
- rhc - Implement rhc_environments (#48)
- rhc - rhc_repository: setting default state of repo to enabled (#65)
- rhc - Implemented "rhc_insights.tags" parameter
- rhc - meta: stop supporting EL7 (#66)
- rhc - Added "rhc_insights.autoupdate" parameter (#67)

### Bug Fixes

- ad_integration - Add `state: up` for the network role to activate the connection (#20)
- rhc - Fix rhc_auth.activation_keys.keys (#54)
- rhc - Fix rhc_insights.remediation when absent (#70)

[1.34.5] - 2023-02-10
---------------------

### Bug Fixes

- selinux - use fileglob to lookup selinux module file - idempotency support (#155)

[1.34.4] - 2023-02-09
---------------------

### Bug Fixes

- ha_cluster - Fix stonith watchdog timeout; fix purging nodes from pacemaker (#105)
- selinux - Use stat on localhost with become: false for module idempotency (#152)

[1.34.3] - 2023-02-04
---------------------

### Bug Fixes

- selinux - Fix idempotency - Use lookup file + sha256 to get hash of local policy file

[1.34.2] - 2023-02-03
---------------------

### Bug Fixes

- ha_cluster - Fence agent firewall port is restricted to x86_64 architecture. (#106)
- selinux - Use selinux facts to compare module checksums before copying to a node (#144)

[1.34.1] - 2023-02-02
---------------------

### Other Changes

- no user-visible changes

[1.34.0] - 2023-01-27
---------------------

### New Features

- journald - new role

[1.33.12] - 2023-01-27
---------------------

### Bug Fixes

- nbde_server - fix some more Jinja constructs (#83)
- podman - fix typo in README (#46)
- selinux - Rewrite selinux_load_module.yml to use local_semodule  (#135)

[1.33.11] - 2023-01-26
---------------------

### Bug Fixes

- kernel_settings - Cleanup non-inclusive words.

[1.33.10] - 2023-01-25
---------------------

### Other Changes

- no user-visible changes

[1.33.9] - 2023-01-24
---------------------

### Bug Fixes

- selinux - ansible-lint 6.x fixes (#132)

[1.33.8] - 2023-01-24
---------------------

### Bug Fixes

- nbde_client - Fix nbde_client error handling (#101)
- postfix - fix issues with jinja, ansible-lint (#70)

[1.33.7] - 2023-01-22
---------------------

### Bug Fixes

- ssh - ansible-lint 6.x fixes (#60)

[1.33.6] - 2023-01-21
---------------------

### Bug Fixes

- ad_integration - ansible-lint 6.x fixes (#11)
- certificate - ansible-lint 6.x fixes
- cockpit - ansible-lint 6.x fixes
- crypto_policies - ansible-lint 6.x fixes (#55)
- firewall - ansible-lint 6.x fixes
- firewall - cannot use distutils; use custom version
- kernel_settings - ansible-lint 6.x fixes (#119)
- kernel_settings - Cleanup non-inclusive words.
- logging - ansible-lint 6.x fixes (#311)
- metrics - fix pimeconf rule filesys vfs_rules support
- metrics - ansible-lint 6.x fixes (#133)
- nbde_server - ansible-lint 6.x fixes (#75)
- podman - Ease permissions on kube spec dir and files (#44)
- postfix - ansible-lint 6.x fixes (#65)
- timesync - fixes for ansible-lint 6.x
- tlog - ansible-lint 6.x fixes (#71)
- vpn - Clean up non-inclusive words.
- vpn - ansible-lint 6.x fixes (#86)

[1.33.5] - 2023-01-20
---------------------

### Bug Fixes

- nbde_client - Do not report password in stacktrace or return value from module (#98)
- nbde_client - Use daemon_reload with askpass path service (#96)

[1.33.4] - 2023-01-19
---------------------

### Other Changes

- no user-visible changes

[1.33.3] - 2023-01-17
---------------------

### Other Changes

- no user-visible changes

[1.33.2] - 2023-01-14
---------------------

### Bug Fixes

- ha_cluster - Not request password to be specified when purging cluster (#92)


[1.33.1] - 2022-12-17
---------------------

[1.33.0] - 2022-12-15
---------------------

### New Features

- rhc - New Role


[1.32.1] - 2022-12-14
---------------------

### Bug Fixes

- ha_cluster - Allow enabled SBD on disabled cluster (#81)
- logging - tests: specify empty inputs, outputs, flows with purge (#308)
- tlog - Unconditionally enable the files provider. (#67)


[1.32.0] - 2022-12-13
---------------------

### New Features

- network - Support cloned MAC address
- podman - add checking for subuid, subgid

### Bug Fixes

- ha_cluster - command warn is not supported in ansible-core 2.14
- ha_cluster - fix ownership of cib.xml
- ha_cluster - update for upcoming pcs release
- ha_cluster - tests: add qnetd cleanup


[1.31.3] - 2022-12-07
---------------------

### New Features

- ad_integration - initial versioned release

### Bug Fixes

- storage - Thin pool test with large size volume fix (#310)


[1.31.2] - 2022-12-06
---------------------

### Bug Fixes

- logging - use logging_purge_confs in relp test (#303)


[1.31.1] - 2022-12-01
---------------------

### Bug Fixes

- ha_cluster - fix qnetd check mode
- nbde_client - use fedora.linux_system_roles.nbde_server for tests (#86)


[1.31.0] - 2022-11-29
---------------------

### Bug Fixes

- nbde_server - fix behavior of manage_firewall and manage_selinux; ansible-lint 6.x (#69)


[1.30.5] - 2022-11-22
---------------------

### Bug Fixes

- cockpit - ansible-core 2.14 support - remove another warn
- vpn - only check for firewall ipsec service if managing firewall (#76)


[1.30.4] - 2022-11-20
---------------------

### Bug Fixes

- logging - cert cleanup needs to use getcert stop-tracking (#300)


[1.30.3] - 2022-11-18
---------------------

### Bug Fixes

- podman - ensure role works with podman 4.3
- podman - ensure role works with ansible-core 2.14
- podman - ensure role passes ansible-lint 6.x


[1.30.2] - 2022-11-16
---------------------

### Bug Fixes

- cockpit - make role work with ansible-core 2.14 - fix ansible-lint 6.x issues (#81)


[1.30.1] - 2022-11-15
---------------------

[1.30.0] - 2022-11-02
---------------------

### New Features

- ad_integration - New Role
- cockpit - Use the firewall role and the selinux role from the cockpit role (#76)
- cockpit - Introduce cockpit_manage_firewall to use the firewall role to
- cockpit - Add the test check task tasks/check_port.yml for verifying the
- cockpit - Add meta/collection-requirements.yml.
- cockpit - Introduce cockpit_manage_selinux to use the selinux role to
- cockpit - Use the certificate role to create the cert and the key (#78)
- cockpit - Introduce a variable cockpit_certificates to set the certificate_requests.
- cockpit - Update README so that using the certificate role is recommended.
- network - Support looking up named route table in routing rule
- network - Support 'route_metric4' for initscripts provider
- network - Support the DNS priority
- podman - New Role

### Bug Fixes

- network - bond: improve the validation for setting peer_notif_delay
- network - bond: test arp_all_targets only when arp_interval is enabled
- network - bond: attach ports when creating the bonding connection


[1.29.0] - 2022-11-02
---------------------

### New Features

- ha_cluster - Use the firewall role and the selinux role from the ha_cluster role
- ha_cluster - Introduce ha_cluster_manage_firewall to use the firewall role to
- ha_cluster - Introduce ha_cluster_manage_selinux to use the selinux role to
- ha_cluster - Add the test check task tasks/check_firewall_selinux.yml for
- ha_cluster - Use the certificate role to create the cert and the key
- ha_cluster - Introduce a variable ha_cluster_pcsd_certificates to set the certificate_requests.
- ha_cluster - add support for configuring qnetd
- ha_cluster - add support for configuring qdevice
- ha_cluster - qdevice and qnetd documentation
- logging - Use the firewall role, the selinux role, and the certificate role from the logging role (#293)
- logging - Introduce logging_manage_firewall to use the firewall role to manage
- logging - Introduce logging_manage_selinux to use the selinux role to manage
- logging - Add the test check task check_firewall_selinux.yml for verify the
- logging - Use the certificate role to generate certificates in the logging role
- logging - Introduce logging_certificates variable to specify parameters for
- metrics - Use the firewall role and the selinux role from the metrics role
- metrics - Introduce metrics_manage_firewall to use the firewall role to
- metrics - Introduce metrics_manage_selinux to use the selinux role to
- metrics - Add the test check task check_firewall_selinux.yml for verify
- metrics - Skip calling the firewall role when the managed node is rhel-6.
- metrics - When metrics_manage_firewall and metrics_manage_selinux are set
- nbde_server - Add support for custom ports (#38)
- nbde_server - Introduce nbde_server_manage_firewall and nbde_server_manage_selinux
- nbde_server - If nbde_server_manage_firewall is set to true, use the firewall
- nbde_server - If nbde_server_manage_selinux is set to true, use the selinux
- postfix - Use the firewall role and the selinux role from the postfix role (#56)
- postfix - Introduce postfix_manage_firewall to use the firewall role to
- postfix - Introduce postfix_manage_selinux to use the selinux role to
- postfix - Add the test check task tasks/check_firewall_selinux.yml for
- postfix - Add meta/collection-requirements.yml.
- vpn - Use the firewall role and the selinux role from the vpn role (#70)
- vpn - Introduce vpn_manage_firewall to enable the firewall role to manage
- vpn - Introduce vpn_manage_selinux to enable the selinux role to manage
- vpn - Add the test check task check_firewall_selinux.yml for verify the
- vpn - Add meta/collection-requirements.yml

### Bug Fixes

- ha_cluster - fix decoding variables from an Ansible vault
- ha_cluster - add a test for vault-encrypted variables
- ha_cluster - adapt tests with vault-encrypted variables for CI
- ha_cluster - use a real temporary directory for test secrets
- ha_cluster - fix checking hacluster password
- ha_cluster - update sbd config file template
- ha_cluster - fix installing qnetd and pcs packages
- ha_cluster - fix auth for qnetd host
- metrics - grafana: small wording tweak to grafana v8/v9 action names
- metrics - grafana: include config file for Grafana v9
- metrics - grafana: update grafana.ini to permit all grafana-pcp plugin components
- nbde_client - correct clevis askpass unit conditional (#81)
- nbde_client - Add default clevis luks askpass unit (#79)
- nbde_client - use no_log: true where secrets might be revealed
- storage - Master thin support size fix (#299)
- storage - percent specified 'size' of thin pool volume is now properly
- storage - percentage size thin volume now correctly references its parent device
- storage - percentage values are now accepted size for thin pool size


[1.28.0] - 2022-10-31
---------------------

### New Features

- ssh - Add final version of the option RequiredRSASize (#53)
- sshd - Adding support for OpenWrt 21.03
- sshd - Add final version of RequiredRSASize

### Bug Fixes

- sshd - Update source template to match generated files


[1.27.0] - 2022-09-19
---------------------

### New Features

- selinux - add 'local' parameter to seport (#124)
- selinux - `local: true`:
- sshd - Make drop-in config file functionality configurable by user
- timesync - adding support fpr Oracle Linux 6,7,8 and 9
- vpn - Various improvements required to connect to a managed remote host (#65)

### Bug Fixes

- certificate - Move Debian to Python 3 packages
- ha_cluster - only install and setup fence-virt on x86_64 hosts (#64)
- ssh - cast value to string in jinja macro (#50)
- sshd - Allow user to override variables
- timesync - Update chrony.conf.j2
- timesync - Updated: type casting in overall timesync templates for testing
- timesync - Updated: type casting adjusted (timesync_max_distance <= int)
- vpn - Check for /usr/bin/openssl on controller - do not use package_facts (#66)


[1.26.1] - 2022-08-05
---------------------

### Bug Fixes

- network - network_state: improve state comparison for achieving idempotency
- network - argument_validator: fix IPRouteUtils.get_route_tables_mapping() for whitespace


[1.26.0] - 2022-08-03
---------------------

### New Features

- cockpit - Add customization of port (#67)
- firewall - feature - add/remove interfaces by PCI ID
- logging - Support startmsg.regex and endmsg.regex in the files inputs.
- network - Support the nmstate network state configuration
- selinux - Added setting of seuser and selevel for completeness (#108)
- ssh - add RSAMinSize parameter (#45)

### Bug Fixes

- ha_cluster - readme: describe limitations of udp transports (#56)
- kernel_settings - Set the kernel_settings_reboot_required when reboot needed (#93)
- metrics - docs: make minimum redis and grafana versions more clear
- metrics - restart pmie, pmlogger if changed, do not wait for handler
- nbde_client - Sets needed spacing for appended rd.neednet parameter (#68)
- network - IfcfgUtil: Remediate `connection_seems_active()` for controller
- sshd - Add CHANGELOG.md
- sshd - Add changelog_to_tag.yml to .github/workflows
- sshd - add parameter RSAMinSize
- sshd - Add parameter RSAMinSize to Match blocks
- storage - Update README.md with latest changes (#290)

[1.24.2] - 2022-06-15
---------------------

### Bug Fixes

- sshd - The role still supports 2.9

[1.24.1] - 2022-06-13
---------------------

### New Features

- storage - check for thinlv name before assigning to thinlv\_params

### Bug Fixes

- ha_cluster - s/ansible\_play\_hosts\_all/ansible\_play\_hosts/ where applicable
- logging - Fix including a var file in set\_vars.yml
- sshd - Fix various linting issues
- sshd - Addition notes about secondary variables

[1.24.0] - 2022-06-02
---------------------

### New Features

- network - IfcfgUtil: Remediate `connection_seems_active()` for controller
- storage - LVM RAID raid0 level support
- storage - Thin pool support

### Bug Fixes

- firewall - fix: state not required for masquerade and ICMP block inversion
- firewall - Fix deprecated syntax in Readme
- ha_cluster - If ansible\_hostname includes '\_' the role fails with `invalid characters in salt`
- sshd - Remove kvm from virtualization platforms

[1.23.0] - 2022-05-25
---------------------

### New Features

- network - infiniband: Add the setting description
- network - infiniband: Reject the interface name for the ipoib connection
- network - infiniband: Reject the invalid pkey value
- network - infiniband: Change the default value of `p_key` into `None`

### Bug Fixes

- network - infiniband: Fix the bug of wrongly checking whether the device exists

[1.22.1] - 2022-05-16
---------------------

### New Features

- metrics - Add CentOS 9 platform variables for each role
- sshd - Unbreak FIPS detection and stabilize failing tests and GH actions
- sshd - Make sure Include is in the main configuration file when drop-in directory is used
- sshd - Make the role FIPS-aware
- storage - add support for mount\_options

### Bug Fixes

- ha_cluster - additional fix for password\_hash salt length
- sshd - Fix runtime directory check condition
- sshd - README: fix meta/make\_option\_lists link

[1.22.0] - 2022-05-02
---------------------

### New Features

- firewall - Added ability to restore Firewalld defaults

[1.21.0] - 2022-04-27
---------------------

### New Features

- logging - support gather\_facts: false
- metrics - Add a metrics\_from\_postfix boolean flag for the metrics role
- network - support playbooks which use gather_facts: false

### Bug Fixes

- metrics - Resolve race condition with starting pmdapostfix
- metrics - Ensure a postfix log file exists for pmdapostfix to start
- postfix - fix ansible-lint issues

[1.20.0] - 2022-04-25
---------------------

### New Features

- firewall - support gather\_facts: false; support setup-snapshot.yml
- ha_cluster - Add support for SBD devices
- ha_cluster - support gather\_facts: false; support setup-snapshot.yml
- ha_cluster - add support for configuring bundle resources
- kdump - support gather\_facts: false; support setup-snapshot.yml
- kernel_settings - support gather\_facts: false; support setup-snapshot.yml
- metrics - Provide pcp_\single\_control option for control.d vs control files
- nbde_client - support gather\_facts: false; support setup-snapshot.yml
- nbde_server - support gather\_facts: false; support setup-snapshot.yml
- network - Add support for routing rules
- network - Util: Normalize address family value before getting prefix length
- postfix - support gather\_facts: false; support setup-snapshot.yml
- selinux - support gather\_facts: false; support setup-snapshot.yml
- ssh - support gather\_facts: false; support setup-snapshot.yml
- sshd - Ensure the ansible facts are available
- sshd - Move the common variables to separate file
- sshd - Clarify the magic number
- sshd - Reuse the list of skipped virtualization environments
- sshd - Update documentation with recent changes
- sshd - Introduce default hostkeys to check when using drop-in directory
- sshd - Add another virtualization platform exception
- sshd - Update templates to apply FIPS hostkeys filter
- storage - add xfsprogs for non-cloud-init systems
- storage - allow role to work with gather\_facts: false
- storage - add setup snapshot to install packages into snapshot
- timesync - support gather\_facts: false; support setup-snapshot.yml
- tlog - support gather\_facts: false; support setup-snapshot.yml
- vpn - support gather\_facts: false; support setup-snapshot.yml

### Bug Fixes

- ha_cluster - Pcs fixes
- network - fix: class Python26CompatTestCase broken by minor python versions
- sshd - Avoid unnecessary use of 'and' in 'when' conditions
- sshd - Unbreak FIPS detection and hostkey filtering
- sshd - Set explicit path to the main configuration file to work well with the drop-in directory
- sshd - Fix runtime directory check

[1.19.0] - 2022-04-06
---------------------

### New Features

- ha_cluster - add support for advanced corosync configuration
- logging - Add log handling in case the target Elasticsearch is unavailable
- logging - RFE - support template, severity and facility options
- logging - Add support for multiline logs in oVirt vdsm.log
- storage - Less verbosity by default
- tlog - Execute authselect to update nsswitch

[1.18.2] - 2022-03-31
---------------------

### Bug Fixes

- nbde_client - network-flush: reset autoconnect-priority to zero

[1.18.1] - 2022-03-29
---------------------

### New Features

- nbde_client - Add dracut module for disabling autoconnect within initrd

[1.18.0] - 2022-03-15
---------------------

### New Features

- metrics - Support metrics from postfix mail servers
- metrics - Add "follow: yes" to the template task in the mssql and elasticsearch subrole.
- network - Add support for Rocky Linux
- postfix - Remove outdated ansible managed header and use {{ ansible\_managed | comment }}
- postfix - Add "previous: replaced" functionality to postfix\_conf dict to reset postfix configuration

### Bug Fixes

- network - bond: Fix supporting the infiniband ports in active-backup mode
- postfix - Fix some issues in the role, more info in commits
- timesync - handle errors with stopping services

[1.17.0] - 2022-02-22
---------------------

### New Features

- firewall - ensure that changes to target take effect immediately
- firewall - Add ability to set the default zone
- ha_cluster - add SBD support

### Bug Fixes

- tlog - tlog does not own sssd.conf - so use ini\_file to manage it

[1.16.0] - 2022-02-15
---------------------

### New Features

- certificate - System Roles should consistently use ansible\_managed in configuration files it manages
- network - NetworkManager provider: Support all available bonding modes and options
- network - Support routing tables in static routes
- tlog - System Roles should consistently use ansible\_managed in configuration files it manages
- vpn - System Roles should consistently use ansible\_managed in configuration files it manages

### Bug Fixes

- certificate - fix python black errors
- ha_cluster - fix default pcsd permissions
- network - Fix setting DNS search settings when only one IP family is enabled
- network - Fix switching from initscripts to NetworkManager 1.18

[1.15.2] - 2022-02-08
---------------------

### New Features

- kdump - use kdumpctl reset-crashkernel on rhel9
- vpn - script to convert vpn\_ipaddr to FQCN

[1.15.1] - 2022-01-27
---------------------

### New Features

- firewall - Added implicit firewalld reload for when a custom zone is added or removed

### Bug Fixes

- cockpit - Skip/undocumented obsolete packages
- kernel_settings - make tuned.conf have correct ansible\_managed comment
- logging - make purge and reset idempotent
- metrics - Address PyYAML vulnerability

[1.15.0] - 2022-01-18
---------------------

### New Features

- logging - Refactor logging\_purge\_confs and logging\_restore\_confs.

[1.14.0] - 2022-01-17
---------------------

### New Features

- timesync - Initial version for Debian

### Bug Fixes

- nbde_client - Add network flushing before setting up network

[1.13.0] - 2022-01-11
---------------------

### New Features

- ha_cluster - add support for configuring resource constraints
- logging - Add logging\_restore\_confs variable to restore backup.
- metrics - Specify grafana username/password
- Changes - Support matching network interfaces by their device path such as PCI address
- storage - Add LVM RAID specific parameters to module\_args
- storage - Added support for LVM RAID volumes
- storage - Add support for creating and managing LVM cache volumes
- storage - Nested module params checking
- storage - Refined safe\_mode condition in create\_members
- vpn - use custom vpn\_ipaddr filter

### Bug Fixes

- Changes - Support ansible-core 2.11 and 2.12
- timesync - Fix an issue if a service is listed by service\_facts that does not have the 'status' property defined

[1.12.0] - 2021-12-06
---------------------

### New Features

- firewall - Added support for RHEL 7
- firewall - Added runtime and permanent flags to documentation.
- kdump - Add reboot required
- ssh - Add new configuration options from Openssh 8.7p1

[1.11.0] - 2021-12-03
---------------------

### New Features

- cockpit - Add option to use an existing certificate
- storage - add support for storage\_udevadm\_trigger
- storage - Add workaround for the service\_facts module for Ansible \< 2.12

### Bug Fixes

- timesync - evaluate is\_ntp\_default as boolean, not string
- timesync - reject services which have a status == not-found
- timesync - also reject masked and failed services

[1.10.1] - 2021-11-08
---------------------

### New Features

- kernel_settings - make role work with ansible-core-2.11 ansible-lint and ansible-test
- kernel_settings - support ansible-core 2.12; ansible-plugin-scan; py39
- logging - support python 39, ansible-core 2.12, ansible-plugin-scan
- metrics - support python 39, ansible-core 2.12, ansible-plugin-scan
- nbde_client - support python 39, ansible-core 2.12, ansible-plugin-scan
- nbde_client - add regenerate-all to the dracut command
- nbde_server - support python 39, ansible-core 2.12, ansible-plugin-scan
- postfix - support python 39, ansible-core 2.12, ansible-plugin-scan
- selinux - support python 39, ansible-core 2.12, ansible-plugin-scan
- ssh - support python 39, ansible-core 2.12, ansible-plugin-scan
- storage - support python 39, ansible-core 2.12, ansible-plugin-scan
- storage - Add support for Rocky Linux 8
- timesync - make role work with ansible-core-2.11 ansible-lint and ansible-test
- tlog - support python 39, ansible-core 2.12, ansible-plugin-scan
- vpn - support python 39, ansible-core 2.12, ansible-plugin-scan

### Bug Fixes

- ha_cluster - fix ansible-lint issues
- logging - missing quotes around immark module interval option
- nbde_server - fix python black issues
- selinux - fix ansible-lint issues

[1.10.0] - 2021-10-07
---------------------

### New Features

- ha_cluster - use firewall-cmd instead of firewalld module
- ha_cluster - replace rhsm\_repository with subscription-manager cli
- ha_cluster - Use the openssl command-line interface instead of the openssl module
- logging - Use {{ ansible\_managed | comment }} to fix multi-line ansible\_managed
- logging - Performance improvement
- logging - Replacing seport module with the semanage command line.
- logging - Add uid and pwd parameters
- logging - Use the openssl command-line interface instead of the openssl module
- sshd - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- storage - Replace crypttab with lineinfile
- storage - replace json\_query with selectattr and map
- timesync - replace json\_query with selectattr/map

### Bug Fixes

- cockpit - Use {{ ansible\_managed | comment }} to fix multi-line ansible\_managed
- cockpit - use apt-get install -y
- ha_cluster - fix password\_hash salt length
- kdump - Use {{ ansible\_managed | comment }} to fix multi-line ansible\_managed
- kdump - remove authorized\_key; use ansible builtins
- kernel_settings - Use {{ ansible\_managed | comment }} to fix multi-line ansible\_managed
- logging - Eliminate redundant loop.
- selinux - Fix version comparisons for ansible\_distribution\_major\_version
- ssh - Use {{ ansible\_managed | comment }} to fix multi-line ansible\_managed
- sshd - Use {{ ansible_managed | comment }} to fix multi-line ansible_managed
- sshd - FIX: indentation including tests
- timesync - Use {{ ansible\_managed | comment }} to fix multi-line ansible\_managed
- vpn - do not use json\_query - not needed here
- vpn - use wait\_for\_connection instead of wait\_for with ssh

[1.9.2] - 2021-08-24
---------------------

### New Features

- logging - Allowing the case, tls is false and key/certs vars are configured.

### Bug Fixes

- logging - Update copy tasks conditions with tls true

[1.9.1] - 2021-08-17
---------------------

### Bug Fixes

- metrics - bpftrace: follow bpftrace.conf symlink for latest PCP versions

[1.9.0] - 2021-08-12
---------------------

### New Features

- certificate - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- ha_cluster - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- kdump - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- kernel_settings - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- logging - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- metrics - Raise supported Ansible version to 2.9
- nbde_client - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- nbde_server - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- network - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- network - wifi: Add Simultaneous Authentication of Equals(SAE) support
- postfix - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- selinux - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- ssh - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- sshd - Add Debian 11 \(bullseye\) support
- sshd - Workaround namespace feature also for RHEL6
- storage - Raise supported Ansible version to 2.9
- timesync - Raise supported Ansible version to 2.9
- tlog - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9
- vpn - Drop support for Ansible 2.8 by bumping the Ansible version to 2.9

### Bug Fixes

- sshd - Fix wrong template file

[1.8.5] - 2021-08-08
---------------------

### New Features

- storage - use volume1\_size; check for expected error

[1.8.4] - 2021-08-06
---------------------

### New Features

- certificate - Instead of the unarchive module, use "tar" command for backup.

### Bug Fixes

- logging - do not warn about unarchive or leading slashes
- logging - python2 renders server\_host list incorrectly
- logging - FIX README false variable name
- logging - use correct python-cryptography package

[1.8.2] - 2021-08-03
---------------------

### New Features

- sshd - Add support for RHEL 9 and adjust tests for it

[1.8.1] - 2021-07-29
---------------------

### Bug Fixes

- storage - omit unnecessary conditional - deadcode reported by static scanner

[1.8.0] - 2021-07-28
---------------------

### New Features

- certificate - Instead of the archive module, use "tar" command for backup.
- logging - Add a support for list value to server\_host in the elasticsearch output
- logging - Instead of the archive module, use "tar" command for backup.
- storage - percentage-based volume size \(lvm only\)

### Bug Fixes

- network - fix yamllint issue - indentation
- network - connections: workaround DeprecationWarning for NM.SettingEthtool.set_feature()

[1.7.0] - 2021-07-15
---------------------

### New Features

- ha_cluster - add pacemaker cluster properties configuration
- network - Only show stderr_lines by default
- network - Add 'auto_gateway' option

### Bug Fixes

- ha_cluster - do not fail if openssl is not installed
- network - nm: Fix the incorrect change indication for dns option
- network - nm: Fix the incorrect change indication when apply the same config twice
- network - fix: dhclient is already running for `nm-bond`
- storage - Fixed volume relabeling

[1.6.0] - 2021-07-07
---------------------

### New Features

- crypto_policies - rename 'policy modules' to 'subpolicies'
- storage - LVMVDO support

[1.5.0] - 2021-06-21
---------------------

### New Features

- kdump - use localhost if no SSH\_CONNECTION env. var.
- sshd - Add configuration options from OpenSSH 8.6p1
- sshd - Rename sshd\_namespace\_append to sshd\_config\_namespace
- sshd - Support for appending a snippet to configuration file
- sshd - Update meta data and README
- sshd - use state: absent instead of state: missing
- sshd - \[FreeBSD\] Add Subsystem to \_sshd\_defaults
- sshd - UsePrivilegeSeparation is deprecated since 2017/OpenSSH 7.5 - https://www.openssh.com/txt/re
- sshd - examples: Provide simple example playbook

### Bug Fixes

- nbde_client - fix python black formatting errors
- ssh - Fix variable precedence for ssh\_drop\_in\_name
- sshd - Fix variable precedence when invoked through legacy "roles:"
- sshd - Fix issues found by linters - enable all tests on all repos - remove suppressions
- sshd - README: Document missing exported variable

[1.4.0] - 2021-06-04
---------------------

### New Features

- selinux - Update semanage task to not specify Fedora since it also runs on RHEL/CentOS 8
- sshd - Skip defaults when appending configuration
- sshd - README: Reword the option description and provide example
- sshd - Remove boolean comparison and regenerate templates
- sshd - Support for appending a snippet to configuration file
- sshd - Update source template files used to generate final template
- timesync - Add NTS support

### Bug Fixes

- metrics - \_\_pcp\_target\_hosts not defined so loop doesn't run

[1.3.0] - 2021-05-27
---------------------

### Initial Release
