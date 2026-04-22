# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1

# this is a correct if, bcond_with actually means without and vice versa
%if 0%{?rhel} && 0%{?rhel} >= 9
%bcond_with    pkcs11
%bcond_with    rtlsdr
%else
%bcond_without pkcs11
%bcond_without rtlsdr
%endif

Summary:        Random number generator related utilities
Name:           rng-tools
Version:        6.17
Release: 8%{?dist}
License:        GPL-2.0-or-later
URL:            https://github.com/nhorman/rng-tools
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        rngd.service
Source2:        rngd.sysconfig

BuildRequires: gcc make binutils
BuildRequires: gettext
BuildRequires: systemd systemd-rpm-macros
BuildRequires: autoconf >= 2.57, automake >= 1.7
BuildRequires: libgcrypt-devel libcurl-devel
BuildRequires: libxml2-devel openssl-devel
BuildRequires: jitterentropy-devel
BuildRequires: jansson-devel
BuildRequires: libcap-devel
%if %{with rtlsdr}
BuildRequires: rtl-sdr-devel
%endif
%if %{with pkcs11}
BuildRequires: libp11-devel
Suggests: opensc
%endif

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# This ensures that the selinux-policy package and all its dependencies
# are not pulled into containers and other systems that do not use SELinux.
Requires: (selinux-policy >= 36.5 if selinux-policy)

Patch0: 1-rt-comment-out-have-aesni.patch
Patch1: 2-rt-revert-build-randstat.patch

%description
This is a random number generator daemon and its tools. It monitors
a set of entropy sources present on a system (like /dev/hwrng, RDRAND,
TPM, jitter) and supplies entropy from them to a kernel entropy pool.

%prep
%autosetup -p0

%build
%if !%{with pkcs11}
%define _without_pkcs11 --without-pkcs11
%endif
%if !%{with rtlsdr}
%define _without_rtlsdr --without-rtlsdr
%endif

./autogen.sh
# a dirty hack to force PIC for a PIC-aware assembly code for i686
# /usr/lib/rpm/redhat/redhat-hardened-cc1 in Koji/Brew does not
# force PIC for assembly sources as of now
%ifarch i386 i686
sed -i -e '/^#define RDRAND_RETRY_LIMIT\t10/a#define __PIC__ 1' rdrand_asm.S
%endif
# a dirty hack so libdarn_impl_a_CFLAGS overrides common CFLAGS
sed -i -e 's/$(libdarn_impl_a_CFLAGS) $(CFLAGS)/$(CFLAGS) $(libdarn_impl_a_CFLAGS)/' Makefile.in
%configure %{?_without_pkcs11} %{?_without_rtlsdr}
%make_build

%install
%make_install

# install systemd unit file
install -Dt %{buildroot}%{_unitdir} -m0644 %{SOURCE1}
# install sysconfig file
install -D %{SOURCE2} -m0644 %{buildroot}%{_sysconfdir}/sysconfig/rngd

%post
%systemd_post rngd.service

%preun
%systemd_preun rngd.service

%postun
%systemd_postun_with_restart rngd.service

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS README.md
%{_bindir}/rngtest
%{_sbindir}/rngd
%{_mandir}/man1/rngtest.1.*
%{_mandir}/man8/rngd.8.*
%attr(0644,root,root)    %{_unitdir}/rngd.service
%config(noreplace) %attr(0644,root,root)    %{_sysconfdir}/sysconfig/rngd

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Vladis Dronov <vdronov@redhat.com> - 6.17-6
- Disable jitter entropy source by default

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 6.17-4
- Rebuild for Jansson 2.14
  (https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Vladis Dronov <vdronov@redhat.com> - 6.17-2
- Add Intel CET IBT instrumentation to assembly code
- Update to the upstream v6.17 @ ac43f912

* Wed Jun 05 2024 Vladis Dronov <vdronov@redhat.com> - 6.17-1
- Update to the upstream v6.17 @ 2160b9c3

* Tue Apr 09 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 6.16-8
- Rebuilt for new rtl-sdr

* Sat Mar 30 2024 Vladis Dronov <vdronov@redhat.com> - 6.16-7
- Update to the upstream v6.16 + tip of origin/master @ 98cf8d63

* Thu Feb 08 2024 Vladis Dronov <vdronov@redhat.com> - 6.16-6
- Use proper SPDX license identifiers

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Florian Weimer <fweimer@redhat.com> - 6.16-3
- Fix C compatibility issue in configure script

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 02 2023 Vladis Dronov <vdronov@redhat.com> - 6.16-1
- Update to the upstream v6.16 + tip of origin/master @ 0e560296
- Get rid of text relocations in -fPIE build
- Add a hint for opensc package (bz 1845854)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 27 2022 Vladis Dronov <vdronov@redhat.com> - 6.15-5
- Update to the upstream v6.15 + tip of origin/master @ cb8cc624

* Wed Sep 21 2022 Vladis Dronov <vdronov@redhat.com> - 6.15-4
- Update to the upstream v6.15 + tip of origin/master @ 6dcc9ec2
- Do not require selinux-policy if it is not present

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 16 2022 Vladis Dronov <vdronov@redhat.com> - 6.15-2
- Update to the upstream v6.15 + tip of origin/master @ 172bf0e3
- Add a requirement for selinux-policy of a certain version
- Fix an error building with jitterentropy-3.4.0

* Tue Feb 22 2022 Vladis Dronov <vdronov@redhat.com> - 6.15-1
- Update to the upstream v6.15 + tip of origin/master @ 3009fdd5
- Allow rngd process to drop privileges

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.14-3.git.b2b7934e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Vladis Dronov <vdronov@redhat.com> - 6.14-2.git.b2b7934e
- Update to the upstream v6.14 + tip of origin/master @ b2b7934e

* Mon Sep 20 2021 Vladis Dronov <vdronov@redhat.com> - 6.14-1.git.56626083
- Update to the upstream v6.14 + tip of origin/master @ 56626083
- Add an important 82f665c4 and a revert of 2ce93190
- Add a fix for covscan unused variable warning
- Add a config file for storing rngd options

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 6.13-4.git.d207e0b6
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.13-3.git.d207e0b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Vladis Dronov <vdronov@redhat.com> - 6.13-2.git.d207e0b6
- Update sources to incorporate the latest chages
- Add more fixes for the onecpu branch

* Tue Jul 06 2021 Vladis Dronov <vdronov@redhat.com> - 6.13.git.d207e0b6-1
- Update to the upstream v6.13 + tip of origin/master + onecpu
  branch + revert of 2ce93190
- Rebuild rng-tools against the latest jitterentropy library
  3.0.2.git.d18d5863 with fixes for an important issue:
  https://github.com/nhorman/rng-tools/pull/123
  https://github.com/smuellerDD/jitterentropy-library/issues/37
- Add important upstream fixes for the one CPU case (bz 1974132)
- Revert introducing a new but mostly useless randstat binary
- A couple of minor code and test fixes

* Fri Jun 18 2021 Vladis Dronov <vdronov@redhat.com> - 6.13-2
- Rewrite init_kernel_rng() to ensure proper logging
- Adjust Source0 to a more proper one
- Adjust wrong date in a changelog
- Remove Provides: jitterentropy-rngd as it was retired in f29

* Wed Jun 16 2021 Vladis Dronov <vdronov@redhat.com> - 6.13-1
- Update the sources to 6.13
- Add important fixes from the upstream

* Mon May 24 2021 Vladis Dronov <vdronov@redhat.com> - 6.12-3
- Update the rngd.service file
- Add 3 small upstream patches fixing issues

* Wed Apr 28 2021 Vladis Dronov <vdronov@redhat.com> - 6.12-2
- There is no need to hardcode _sbindir anymore, also the old value is incorrect

* Fri Mar 12 2021 Vladis Dronov <vdronov@redhat.com> - 6.12-1
- Update to 6.12
- Drop libsysfs dependency since it is not used anymore
- Remove jitterentropy-remove-install.patch since we depend on a system jitterentropy library now
- Remove rngd-shutdown.patch since it is the upstream commit 62fbff0a
- Remove rngd-exit-code-for-list.patch since it is the upstream commit fb46dc48
- Remove pkcs11-path.patch since it is the upstream commit 1993eca9

* Tue Mar 02 2021 Vladis Dronov <vdronov@redhat.com> - 6.11-3
- Replace outdated systemd-units

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.11-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583

* Fri Jan 29 2021 Dan Horák <dan[at]danny.cz> - 6.11-1
- Update to 6.11

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Vladis Dronov <vdronov@redhat.com> - 6.10-7
- Make rtl-sdr optional
- For RHEL9 and above, do not build with rtl-sdr

* Mon Oct 05 2020 Troy Dawson <tdawson@redhat.com> - 6.10-6
- Make pkcs11 optional
- For RHEL9 and above, do not build with pkcs11

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 27 2020 Neil Horman <nhorman@redhat.com> - 6.10-3
- Fix missing buildrequires

* Fri Mar 27 2020 Neil Horman <nhorman@redhat.com> - 6.10-2
- Fix missing buildrequires

* Fri Mar 27 2020 Neil Horman <nhorman@redhat.com> - 6.10-1
- Update to latest upstream

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Neil Horman <nhorman@redhat.com> - 6.9-2
- Correct default pkcs11 path on 32 bit arch (bz 1788083)

* Tue Dec 17 2019 Neil Horman <nhorman@redhat.com> - 6.9-1
- update to latest upstream

* Mon Aug 05 2019 Volker Froehlich <volker27@gmx.at> - 6.7-4
- Remove explicit Requires for libraries

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Neil Horman <nhorman@redhat.com> -6.7-2
- Fix race in shutdown leading to hang (bz 1690364)
- bump version number

* Thu Feb 14 2019 Neil Horman <nhorman@redhat.com> - 6.7-1
- Update to latest upstream

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Neil Horman <nhorman@redhat.com> - 6.3.1-2
- Add Provides for jitterentropy-rngd (bz 1634788)

* Mon Jul 16 2018 Neil Horman <nhorman@redhat.com> - 6.3.1-1
- Update to latest upstream

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Neil Horman <nhorman@redhat.com> - 6.3-1
- update to latest upstream (#1598608)

* Thu May 10 2018 Neil Horman <nhorman@redhat.com>
- Update to latest upstream

* Thu Feb 15 2018 Adam Williamson <awilliam@redhat.com> - 6.1-4
- Drop all attempts to 'fix' #1490632, revert spec to same as 6.1-1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 02 2017 Neil Horman <nhorman@redhat.com> - 6.1-2
- Enable rngd on entropy src availability (bz 1490632)

* Tue Oct 10 2017 Neil Horman <nhorman@redhat.com> - 6.1-1
- update to latest upstream

* Fri Jul 28 2017 Neil Horman <nhorman@redhat.com> - 6-1
- Update to latest upstream

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 18 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5-8
- If device is not found exit immediately (#892178)

* Sun Mar  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5-7
- Use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5-4
- Build with hardening flags (#1051344)
- Fail nicely if no hardware generator is found (#892178)
- Drop unneeded dependency

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Luke Macken <lmacken@redhat.com> - 5-1
- Update to release version 5.
- Remove rng-tools-man.patch

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Jaromir Capik <jcapik@redhat.com> - 4-2
- Migration to new systemd macros

* Mon Aug 6 2012 Jeff Garzik <jgarzik@redhat.com> - 4-1
- Update to release version 4.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Jiri Popelka <jpopelka@redhat.com> - 3-4
- 2 patches from RHEL-6
- systemd service
- man page fixes
- modernize spec file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul  3 2010 Jeff Garzik <jgarzik@redhat.com> - 3-2
- comply with renaming guidelines, by Providing rng-utils = 1:2.0-4.2

* Sat Jul  3 2010 Jeff Garzik <jgarzik@redhat.com> - 3-1
- Update to release version 3.

* Fri Mar 26 2010 Jeff Garzik <jgarzik@redhat.com> - 2-3
- more minor updates for package review

* Thu Mar 25 2010 Jeff Garzik <jgarzik@redhat.com> - 2-2
- several minor updates for package review

* Wed Mar 24 2010 Jeff Garzik <jgarzik@redhat.com> - 2-1
- initial revision (as rng-tools)
