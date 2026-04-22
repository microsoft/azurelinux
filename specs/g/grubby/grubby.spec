# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# What?  No.
%define __brp_mangle_shebangs %{nil}

Name: grubby
Version: 8.40
Release: 86%{?dist}
Summary: Command line tool for updating bootloader configs
License: GPL-2.0-or-later
Source1: grubby-bls
# Source2: rpm-sort.c
Source3: COPYING
Source5: 95-kernel-hooks.install
Source6: 10-devicetree.install
Source7: grubby.8

BuildRequires: gcc
BuildRequires: glib2-devel
BuildRequires: libblkid-devel
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: popt-devel
BuildRequires: rpm-devel
BuildRequires: sed
%ifarch aarch64 x86_64 %{power64} riscv64
BuildRequires: grub2-tools-minimal
Requires: grub2-tools-minimal
Requires: grub2-tools
%endif
%ifarch s390 s390x
Requires: s390utils-core
%endif
Requires: findutils
Requires: util-linux

ExcludeArch: %{ix86}
Conflicts:	uboot-tools < 2021.01-0.1.rc2
Obsoletes:	%{name}-bls < %{version}-%{release}
Obsoletes:	%{name}-deprecated < %{version}-%{release}

%description
This package provides a grubby compatibility script that manages
BootLoaderSpec files and is meant to be backward compatible with
the previous grubby tool.

%prep
# Make sure the license can be found in mock
cp %{SOURCE3} . || true

%build
%set_build_flags

%install
mkdir -p %{buildroot}%{_sbindir}/
install -T -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}/grubby

install -D -m 0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE5}
install -D -m 0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE6}

mkdir -p %{buildroot}%{_mandir}/man8
install -m 0644 %{SOURCE7} %{buildroot}%{_mandir}/man8/

%post
if [ "$1" = 2 ]; then
    arch=$(uname -m)
    [[ $arch == "s390x" ]] && \
    zipl-switch-to-blscfg --backup-suffix=.rpmsave &>/dev/null || :
fi

%files
%license COPYING
%attr(0755,root,root) %{_sbindir}/grubby
%attr(0755,root,root) %{_prefix}/lib/kernel/install.d/10-devicetree.install
%attr(0755,root,root) %{_prefix}/lib/kernel/install.d/95-kernel-hooks.install
%{_mandir}/man8/grubby.8*

%changelog
* Wed Jul 30 2025 Leo Sandoval <lsandova@redhat.com> - 8.40-85
- Update cfg when setting a default kernel

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-84
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 20 2025 Leo Sandoval <lsandova@redhat.com> - 8.40-83
- grubby-bls: in s390* systems, run zipl on grub cfg update event
  Fixes previous commit and formats better the conditions that trigger grub cfg updates

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-82
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Nicolas Frayer <nfrayer@redhat.com> - 8.40-81
- Fixups to custom kernel targets

* Fri Dec 06 2024 Leo Sandoval <lsandova@redhat.com> - 8.40-80
- grubby-bls: on PPC systems, remove petiboot's version checks

* Fri Dec 06 2024 Leo Sandoval <lsandova@redhat.com> - 8.40-79
- grubby-bls: in s390* systems, run zipl on grub cfg update event

* Mon Dec 02 2024 David Abdurachmanov <davidlt@rivosinc.com> - 8.40-78
- Add riscv64 support

* Mon Nov 25 2024 Leo Sandoval <lsandova@redhat.com> - 8.40-77
- On grub cfg updates, run grub2-mkconfig for Xen systems

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-74
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marta Lewandowska <mlewando@redhat.com> - 8.40-73
- Do not overwrite all vars that start with GRUB_CMDLINE_LINUX

* Mon Sep 11 2023 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 8.40-72
- Drop installkernel so that it can be provided by systemd

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Marta Lewandowska <mlewando@redhat.com> - 8.40-70
- remove root= when not copying default

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-68
- Drop custom rpm-sort
- See-also: https://github.com/rpm-software-management/rpm/pull/2249

* Tue Oct 04 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-67
- Apply Marta's copy-default args fix

* Mon Aug 22 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-66
- Give up and just pull the config from BLS
- Suggested-by: Bojan Smojver <bojan@rexursive.com>

* Wed Aug 17 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-65
- Mark package as obsoleting -deprecated
- Resolves: #2117817

* Tue Aug 02 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-64
- Handle updating /etc/kernel/cmdline

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-63
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-62
- Clarify that grub files aren't used on s390x in man page

* Wed Jun 22 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-61
- Revert previous change

* Tue May 31 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-60
- Additionally write to /etc/kernel/cmdline

* Wed Apr 27 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-59
- Remove upstream and layers of indirection around -bls

* Thu Mar 10 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-58
- Remove grubby-deprecated

* Mon Feb 07 2022 Robbie Harwood <rharwood@redhat.com> - 8.40-57
- grubby-bls: wire up -h (help)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Javier Martinez Canillas <javierm@redhat.com> - 8.40-54
- Clarify package description
  Resolves: rhbz#1913299
- Update man page to not mention the GRUB config in the ESP anymore
  Resolves: rhbz#1958458

* Wed Jun 09 2021 Javier Martinez Canillas <javierm@redhat.com> - 8.40-53
- grubby-bls: expand only the kernelopts variable

* Mon Apr 26 2021 Javier Martinez Canillas <javierm@redhat.com> - 8.40-52
- grubby-bs: Fix changing kernel cmdline params not working on ppc64le

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 30 2020 Tom Stellard <tstellar@redhat.com> - 8.40-50
- Use make_build macro instead of plain make
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Fri Nov 20 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 8.40-49
- Add device tree kernel install option

* Mon Oct 26 2020 Josh Boyer <jwb@redhat.com> - 8.40-48
- Only require s390utils-core, not s390utils-base

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Javier Martinez Canillas <javierm@redhat.com> - 8.40-46
- fix build with rpm-4.16
- grubby-bls: fix --extra-initrd option not adding the correct path

* Wed May 13 2020 Javier Martinez Canillas <javierm@redhat.com> - 8.40-45
- grubby-bls: don't replace options with kernelopts if values are the same

* Wed May 06 2020 Javier Martinez Canillas <javierm@redhat.com> - 8.40-44
- Fix installed man page file mode bits

* Tue May 05 2020 Javier Martinez Canillas <javierm@redhat.com> - 8.40-43
- grubby-bls: always escape the delimiter character used in sed commands
- grubby-bls: add a --no-etc-grub-update option

* Wed Apr 29 2020 Javier Martinez Canillas <javierm@redhat.com> - 8.40-42
- grubby-bls: fix corner case when a kernel param value contains a '='
- grubby-bls: update man page to match options in current wrapper script

* Mon Mar 30 2020 Javier Martinez Canillas <javierm@redhat.com> - 8.40-41
- Make grubby to also update GRUB_CMDLINE_LINUX in /etc/default/grub
  Related: rhbz#1287854

* Mon Feb 10 2020 Javier Martinez Canillas <javierm@redhat.com> - 8.40-40
- Fix FTBFS
  Resolves: rhbz#1799496
- Fix wrong S-o-B tag in patch
- Fix warning about using unversioned Obsoletes

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-38
- grubby-bls: don't update grubenv when generating grub.cfg for ppc64le
  Related: rhbz#1726514

* Thu Nov 28 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-37
- grubby-bls: don't print rpm-sort error messages
  Resolves: rhbz#1731924
- grubby-bls: remove -o option and support -c for ppc64le grub config
  Resolves: rhbz#1758598
- grubby-bls: fix logic to check if the kernelopts var is defined in a BLS
  Resolves: rhbz#1726514

* Tue Aug 06 2019 Yuval Turgeman <yturgema@redhat.com> - 8.40-36
- grubby-bls: strip only /boot from paths

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-34
- Add a kernel-install plugin to execute hook scripts in /etc/kernel/
  Resolves: rhbz#1696202

* Mon Jun 10 22:13:19 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.40-33
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:02 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.40-32
- Rebuild for RPM 4.15

* Fri May 03 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-31
- Use mountpoint command to check whether /boot is a mount point
  Resolves: rhbz#1706091

* Thu Mar 21 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-30
- grubby-bls: fix --add-kernel not working when using the --args option
  Resolves: rhbz#1691004

* Mon Mar 11 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-29
- Only switch to BLS config for s390x / zipl
  Related: rhbz#1652806

* Fri Mar 01 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-28
- grubby-bls: make --update-kernel ALL to update kernelopts var in grubenv

* Thu Feb 14 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-27
- grubby-bls: error if args or remove-args is used without update-kernel

* Tue Feb 05 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-26
- Fix GCC warnings about possible string truncations and buffer overflows
- grubby-bls: unset default entry if is the one being removed
- grubby-bls: show absolute path when printing error about incorrect param

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Javier Martinez Canillas <javierm@redhat.com> - 8.40-24
- Correctly set LDFLAGS to include hardened flags (pjones)
  Related: rhbz#1654936
- grubby-bls: expand all variables in options field when updating it
  Resolves: rhbz#1660700

* Tue Dec 11 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-23
- grubby-bls: lookup default entry by either id or title on grub2
  Related: rhbz#1654936

* Fri Nov 30 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-22
- grubby-bls: also print the absolute path in the --default-kernel option
  Resolves: rhbz#1649778
- grubby-bls: allow to specify the same kernel param multiple times
  Resolves: rhbz#1652486
- grubby-bls: expand kernel options if these are environment variables
  Resolves: rhbz#1649785
- grubby-bls: always generate the BLS snippets when adding new entries
  Resolves: rhbz#1653365
- Improve man page for --info option (jstodola)
  Resolves: rhbz#1651672
- Make the old grubby take precedence over grubby-bls if is installed
  Related: rhbz#165484

* Wed Nov 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-21
- installkernel-bls: remove unnecessary check for GRUB_ENABLE_BLSCFG=true
  Resolves: rhbz#1647721
- grubby-bls: use title field instead of version for zipl default entry
  Related: rhbz#1645200
- grubby-bls: print the absolute kernel and initramfs images paths
  Resolves: rhbz#1649778
- grubby-bls: make info print the root parameter if is present in cmdline
  Resolves: rhbz#1649791

* Tue Nov 13 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-20
- Switch to a BLS configuration on %%post

* Tue Nov 06 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-19
- Make the temporary config wrapper be what "grubby" contains, and put
  traditional grubby in grubby-deprecated (pjones)
- Re-enable debuginfo generation (pjones)
  Related: rhbz#1619344
- Install installkernel-bls here as well, not just in the grub2 package,
  since s390x doesn't have grubby packages (pjones)
  Related: rhbz#1619344
- Make grubby-bls execute grub2-mkconfig on ppc64
  Resolves: rhbz#1636039
- grubby-bls should only check if kernel exists and not if was installed
  Resolves: rhbz#1634740
- Use ! instead of , as sed delimiter in grubby-bls script
  Resolves: rhbz#1634744
- Print information about the entry set as default
  Resolves: rhbz#1636180
- grubby-bls: make "id" be the filename, and include it in --info=ALL (pjones)
  Related: rhbz#1638103
- grubby-bls: Make grubby-bls sort everything the same way grub2 does (pjones)
  Resolves: rhbz#1638103
- grubby-bls: Consistently use the filename as the bls id
  Related: rhbz#1638103
- grubby-bls: check if entry exists before attempting to print its info
  Resolves: rhbz#1634712
- grubby-bls: make a copy of the cmdline if is modified for an entry
  Resolves: rhbz#1629054
- grubby-bls: escape delimiter character before replacing the options field
  Resolves: rhbz#1640017
- grubby-bls: grubby-bls: use id instead of title to get the default entry
  Resolves: rhbz#1638103
- grubby-bls: use ~debug instead of -debug as suffix to sort correctly
  Related: rhbz#1638103
- grubby-bls: allow to add many BLS entries for the same kernel image
  Resolves: rhbz#1634752
- grubby-bls: fix --default-* options for s390x
  Resolves: rhbz#1644608
- grubby-bls: only compare using relative paths if /boot is a mount point
  Resolves: rhbz#1642078

* Fri Aug 10 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-18
- Make installkernel to use kernel-install scripts on BLS configuration

* Tue Jul 24 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-17
- Fix grubby wrapper paths
  Resolves: rhbz#1607981

* Tue Jul 24 2018 Peter Jones <pjones@redhat.com> - 8.40-16
- Fix permissions on /usr/sbin/grubby

* Fri Jul 13 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-15
- Add a grubby-bls package that conflicts with grubby

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Peter Jones <pjones@redhat.com> - 8.40-13
- Use standard Fedora linker flags (rhbz#1543502) (rdossant)
- Switch zipl config to BLS configuration on %%postun for s390x (javierm)

* Tue Apr 10 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-12
- Use .rpmsave as backup suffix when switching to BLS configuration

* Fri Apr 06 2018 Javier Martinez Canillas <javierm@redhat.com> - 8.40-11
- Switch grub2 config to BLS configuration on %%postun

* Sat Mar 03 2018 Nathaniel McCallum <npmccallum@redhat.com> - 8.40-10
- Add support for /boot on btrfs subvolumes

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Peter Robinson <pbrobinson@fedoraproject.org> 8.40-8
- Drop u-boot uImage generation on ARMv7
- Minor cleanups

* Tue Sep 12 2017 Peter Jones <pjones@redhat.com> - 8.40-7
- Explicitly require grub2-tools on platforms that need grub2-editenv
- Minor packaging cleanups

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Peter Jones <pjones@redhat.com> - 8.40-1
- Update to 8.40
- More work on the thing that went to testing in 8.39
  Resolves: rhbz#1211887

* Tue Apr 14 2015 Peter Jones <pjones@redhat.com> - 8.39-1
- Update to 8.39
- Fix title extraction with some config file types
  Resolves: rhbz#1204353
  Resolves: rhbz#1204888
  Resolves: rhbz#1206943

* Tue Apr 14 2015 Peter Jones <pjones@redhat.com> - 8.38-1
- Update to 8.38
- Fix title extraction with some config file types
  Resolves: rhbz#1204353
  Resolves: rhbz#1204888
  Resolves: rhbz#1206943

* Tue Mar 17 2015 Peter Jones <pjones@redhat.com> - 8.37-1
- Update to 8.37
- Fix test case from 8.35 on ppc64
  Resolves: rhbz#1202876

* Thu Nov 13 2014 Peter Jones <pjones@redhat.com> - 8.35-9
- Disable "make check" on arm builds; right now the test suite is broken
  there and raises false positives constantly.

* Mon Oct 27 2014 Peter Jones <pjones@redhat.com> - 8.35-8
- Treat kernel and kernel-core as identical in terms of --make-default
  Resolves: rhbz#1141414

* Thu Oct 16 2014 Peter Jones <pjones@redhat.com> - 8.35-7
- Revert "debug" image creation for now
  Resolves: rhbz#1153410
- Fix minor quoting errors in dtbdir code
  Resolves: rhbz#1088933

* Wed Oct 15 2014 Peter Jones <pjones@redhat.com> - 8.35-6
- Update grubby to support device tree options for arm.  Again.
  Resolves: rhbz#1088933

* Fri Sep 26 2014 Peter Jones <pjones@redhat.com> - 8.35-5
- See if what people are seeing in 1141414 is actually 957681
  Related: rhbz#957681
  Related: rhbz#1141414

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 8.35-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Peter Jones <pjones@redhat.com> - 8.35-1
- Fix a minor test case error that causes koji builds to fail.
  Related: rhbz#1096358

* Wed May 21 2014 Peter Jones <pjones@redhat.com> - 8.34-1
- Make grub2 "--copy-default --add-kernel=foo --initrd=bar" work when default
  has no initrd line.
  Resolves: rhbz#1099627
  Related: rhbz#1096358

* Tue Apr 01 2014 Peter Jones <pjones@redhat.com> - 8.33-1
- Fix --devtree test in new-kernel-pkg even harder (#1082318)

* Mon Mar 31 2014 Peter Jones <pjones@redhat.com> - 8.32-1
- Fix --devtree test in new-kernel-pkg (#1082318)
- Fix aarch64 #define test.

* Fri Mar 28 2014 Peter Jones <pjones@redhat.com> - 8.31-1
- Update to 8.31
- Fold in patches from Fedora and RHEL 7 trees

* Mon Jan 20 2014 Lubomir Rintel <lkundrak@v3.sk> - 8.28-2
- Fix extlinux default

* Fri Aug 02 2013 Peter Jones <pjones@redhat.com> - 8.28-1
- More work on grub's "saved_entry" system. 
  Resolves: rhbz#768106
  Resolves: rhbz#736188

* Tue Jul 30 2013 Peter Jones <pjones@redhat.com> - 8.27-1
- Make grubby understand grub's "saved_entry" system
  Resolves: rhbz#768106
  Resolves: rhbz#736188
- BuildRequire grub2 on appropriate platforms, for the test suite.

* Fri Jun 07 2013 Dennis Gilmore <dennis@ausil.us> - 8.26-2
- add patch to update extlinux.conf file on arm if it exists

* Fri May 10 2013 Peter Jones <pjones@redhat.com> - 8.26-1
- Conditionally call arm-boot-config's boot.scr generator if available
  Resolves: rhbz#952428

* Tue Apr 09 2013 Peter Jones <pjones@redhat.com> - 8.25-1
- Error instead of segfaulting if we can't find any working config
  Resolves: rhbz#912873
  Resolves: rhbz#751608

* Tue Mar 19 2013 Peter Jones <pjones@redhat.com> - 8.24-1
- Fix module remove code from Harald (#923441)

* Mon Mar 11 2013 Peter Jones <pjones@redhat.com> - 8.23-1
- Update to 8.23
- Fix empty root device in case of an empty /etc/fstab (lemenkov)
- General refactoring and cleanup (harald)
- Don't clean up modules.* so aggressively (harald)

* Wed Feb 20 2013 Peter Jones <pjones@redhat.com> - 8.22-3
- Add --debug style logging (for both success and failures) to /var/log/grubby

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Peter Jones <pjones@redhat.com> - 8.22-1
- Revert test case for rhbz#742885 - it's a work in progress that isn't
  ready yet.

* Fri Jan 04 2013 Peter Jones <pjones@redhat.com> - 8.21-1
- Use systemd vconsole.conf and locale.conf if present
  Resolves rhbz#881908
- Avoid unnecessary stat calls (from Ville Skyttä)
  Resolves rhbz#741135
- Spelling fixes (Ville Skyttä)
- Add a test case for rhbz#742885
- Handle case-insensitive extlinux config files properly (from Johannes Weiner)

* Tue Oct 02 2012 Peter Jones <pjones@redhat.com> - 8.20-1
- Handle linuxefi initrd and removal correctly.
  Resolves: rhbz#859285

* Wed Sep 26 2012 Peter Jones <pjones@redhat.com> - 8.19-1
- Don't accidentally migrate from linuxefi back to linux
  Related: rhbz#859285

* Fri Sep 21 2012 Peter Jones <pjones@redhat.com> - 8.18-1
- Change the way the kernel load address is determined for ARM U-Boot.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 8.17-1
- Update to 8.17
- Fixes a "make test" failure.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 8.16-1
- Update to 8.16
- Handle "linuxefi" directive on grub2/uefi machines.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Peter Jones <pjones@redhat.com> - 8.15-1
- Update to 8.15
- Revert dirname change from 8.13; it was wrong.

* Thu Jun 14 2012 Peter Jones <pjones@redhat.com> - 8.14-1
- Update to 8.14 to fix a build problem.

* Thu Jun 14 2012 Peter Jones <pjones@redhat.com> - 8.13-1
- Update to 8.13
- Add some more ARM tweaks (dmartin)
- Better support for other distros (crosa)

* Tue Jun 12 2012 Peter Jones <pjones@redhat.com> - 8.12-2
- Support UBOOT_IMGADDR override on ARM (blc)

* Thu May 31 2012 Peter Jones <pjones@redhat.com> - 8.12-1
- Update to 8.12
- Preserve trailing indentation when splitting line elements (mads)
  Resolves: rhbz#742720
- Pick last device mounted on / (pjones,bcl)
  Related: rhbz#820340
  Related: rhbz#820351

* Wed Mar 21 2012 Peter Jones <pjones@redhat.com> - 8.11-1
- Update to 8.11
  Resolves: rhbz#805310

* Thu Mar 15 2012 Peter Jones <pjones@redhat.com> - 8.10-1
- Update to 8.10
- Use "isquote" where appropriate
- Make --remove-kenrel support titles in grub2 (jianzhong.huang)
- Use grub2 if it's there on ppc.

* Fri Mar 02 2012 Peter Jones <pjones@redhat.com> - 8.9-1
- Refactor grub2 title extraction, making it a function (Cleber Rosa)
- Include prefix when printing kernel information (Cleber Rosa)
- Implement support for "default saved" for grub2 (Cleber Rosa)
- Try to display title when printing information with '--info' (Cleber Rosa)
- new-kernel-pkg fails to find U-Boot. (D. Marlin)
- Add support to new-kernel-pkg to recognize ARCH == armv5tel needed for Kir
  (D.Marlin)
- Include a / when one is missing in paths (#769641)
- Fix hard coded paths so kernel's "make install" will DTRT.
- Fix endswith() to correctly test its input for validity.

* Tue Feb 07 2012 Dennis Gilmore <dennis@ausil.us> - 8.8-3
- add uboot-tools requires on arm arches
- add uboot config file on arm arches

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Peter Jones <pjones@redhat.com> - 8.8-1
- Fix test cases from 8.7 to work on a system without /boot mounted.

* Tue Dec 20 2011 Peter Jones <pjones@redhat.com> - 8.7-1
- Add a --debug to try to help diagnose "No suitable template". (sandeen,pjones)

* Mon Dec 19 2011 Peter Jones <pjones@redhat.com> - 8.6-1
- Fix a "make test" errors introduced in 8.4-1

* Sat Dec 17 2011 Peter Jones <pjones@redhat.com> - 8.5-1
- Don't hardcode dracut path
  Resolves: #768645

* Thu Dec 08 2011 Adam Williamson <awilliam@redhat.com> - 8.4-1
- Update to 8.4:
  + fix Loading... line for updated kernels
  + Add new '--default-title' feature
  + Add new '--default-index' feature
  + add feature for testing the output of a grubby command
  + Fix detection when comparing stage1 to MBR
  + do not link against glib-2.0
  + Don't crash if grubConfig not found
  + Adding extlinux support for new-kernel-pkg
  + Look for Debian / Ubuntu grub config files (#703260)
  + Make grubby recognize Ubuntu's spin of Grub2 (#703260)

* Thu Sep 29 2011 Peter Jones <pjones@redhat.com> - 8.3-1
- Fix new-kernel-pkg invocation of grubby for grub (patch from Mads Kiilerich)
  Resolves: rhbz#725185

* Wed Sep 14 2011 Peter Jones <pjones@redhat.com> - 8.2-1
- Fixes for xen (from Michael Petullo)
  Resolves: rhbz#658387

* Fri Jul 22 2011 Peter Jones <pjones@redhat.com> - 8.1-1
- Update to 8.1
- Fix miss-spelled variable name in new-kernel-pkg

* Thu Jul 21 2011 Peter Jones <pjones@redhat.com> - 8.0-1
- Add support for grub2.

* Tue Jun 07 2011 Brian C. Lane <bcl@redhat.com> - 7.0.18-1
- Bump version to 7.0.18 (bcl)
- Fixup new-kernel-pkg errors (#711493) (bcl)

* Mon Jun 06 2011 Peter Jones <pjones@redhat.com> - 7.0.17-1
- Fix references to wrong program name in new-kernel-pkg.8
  Resolves: rhbz#663981

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 7.0.16-2
- add BR utils-linux-ng for getopt

* Tue Jul 13 2010 Brian C. Lane <bcl@redhat.com> - 7.0.16-1
- Update to 7.0.16
- Add patch to check the return value of getuuidbydev
- Resolves: rhbz#592294

* Wed Apr 14 2010 Peter Jones <pjones@redhat.com> - 7.0.15-1
- Update to 7.0.15
- Add man pages for installkernel and new-kernel-pkg
  Resolves: rhbz#529333

* Wed Apr 14 2010 Peter Jones <pjones@redhat.com> - 7.0.14-1
- Update to 7.0.14

* Thu Feb 11 2010 Peter Jones <pjones@redhat.com> - 7.0.13-1
- Strip boot partition prefix from initrd path if present during --update.
  Related: rhbz#557922
- add host only support for local kernel compiles (airlied)

* Mon Feb 08 2010 Peter Jones <pjones@redhat.com> - 7.0.12-1
- compare rootdev using uuid instead of stat, for better btrfs support (josef)
  Resolves: rhbz#530108

* Mon Feb 08 2010 Peter Jones <pjones@redhat.com> - 7.0.11-1
- Make it possible to update the initrd without any other change.
  Related: rhbz#557922

* Fri Feb 05 2010 Peter Jones <pjones@redhat.com> - 7.0.10-1
- Make --update able to add an initramfs.
  Related: rhbz#557922

* Mon Nov 30 2009 Peter Jones <pjones@redhat.com> - 7.0.9-3
- Use s390utils-base as the s390 dep, not s390utils
  Related: rhbz#540565

* Tue Nov 24 2009 Peter Jones <pjones@redhat.com> - 7.0.9-2
- Add s390utils dep when on s390, since new-kernel-package needs it.
  Resolves: rhbz#540565

* Fri Oct 30 2009 Peter Jones <pjones@redhat.com> - 7.0.9-1
- Add support for dracut to installkernel (notting)

* Thu Oct  1 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.8-1
- Stop using nash

* Fri Sep 11 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.7-1
- Remove writing rd_plytheme=$theme to kernel args in dracut mode (hansg)
- Add a couple of test cases for extra initrds (rstrode)
- Allow tmplLine to be NULL in getInitrdVal (rstrode)

* Fri Sep 11 2009 Peter Jones <pjones@redhat.com> - 7.0.6-1
- Fix test case breakage from 7.0.5 (rstrode)

* Fri Sep 11 2009 Peter Jones <pjones@redhat.com> - 7.0.5-1
- Add support for plymouth as a second initrd. (rstrode)
  Resolves: rhbz#520515

* Wed Sep 09 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.4-1
- Add --dracut cmdline argument for %%post generation of dracut initrd

* Wed Aug 26 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.3-1
- Silence error when no /etc/sysconfig/keyboard (#517187)

* Fri Aug  7 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.2-1
- Add --add-dracut-args new-kernel-pkg cmdline option

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Jeremy Katz <katzj@redhat.com> - 7.0.1-1
- Fix blkid usage (#124246)

* Wed Jun 24 2009 Jeremy Katz <katzj@redhat.com> - 7.0-1
- BR libblkid-devel now instead of e2fsprogs-devel
- Add bits to switch to using dracut for new-kernel-pkg

* Wed Jun  3 2009 Jeremy Katz <katzj@redhat.com> - 6.0.86-2
- add instructions for checking out from git

* Tue Jun  2 2009 Jeremy Katz <katzj@redhat.com> - 6.0.86-1
- initial build after splitting out from mkinitrd

