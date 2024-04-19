%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# No.  I have enough trouble already.
%undefine _auto_set_build_flags

Name:    pesign
Summary: Signing utility for UEFI binaries
Version: 116
Release: 3%{?dist}
License: GPL-2.0-only
URL:     https://github.com/rhboot/pesign

Vendor:        Microsoft Corporation
Distribution:  Azure Linux

Obsoletes: pesign-rh-test-certs <= 0.111-7
BuildRequires: efivar-devel >= 38-1
BuildRequires: gcc
BuildRequires: git
BuildRequires: libuuid-devel
BuildRequires: make
BuildRequires: mandoc
BuildRequires: nspr
BuildRequires: nspr-devel >= 4.9.2-1
BuildRequires: nss
BuildRequires: nss-devel >= 3.13.6-1
BuildRequires: nss-tools
BuildRequires: nss-util
BuildRequires: popt-devel
BuildRequires: python3
BuildRequires: python3-rpm-macros
BuildRequires: tar
BuildRequires: xz
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 17 || 0%{?azl}
BuildRequires: systemd-rpm-macros
%endif
Requires:      nspr
Requires:      nss
Requires:      nss-tools >= 3.53
Requires:      nss-util
Requires:      popt
Requires:      rpm
Requires(pre): shadow-utils
ExclusiveArch: %{ix86} x86_64 ia64 aarch64 %{arm}
%if 0%{?rhel} == 7
BuildRequires: rh-signing-tools >= 1.20-2
%endif

Source0: https://github.com/rhboot/pesign/releases/download/%{version}/pesign-%{version}.tar.bz2
Source1: certs.tar.xz
Source2: pesign.py
Source3: pesign.patches

# generate with tool
%include %{SOURCE3}

%description
This package contains the pesign utility for signing UEFI binaries as
well as other associated tools.

%prep
%setup -q -T -b 0
%setup -q -T -D -c -n pesign-%{version}/ -a 1
git init
git config user.email "azurelinux@microsoft.com"
git config user.name "Azure Linux"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
make PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
mkdir -p %{buildroot}/%{_libdir}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} \
	install
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 17 || 0%{?azl}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} \
	install_systemd
%endif

# there's some stuff that's not really meant to be shipped yet
rm -rf %{buildroot}/boot %{buildroot}/usr/include
rm -rf %{buildroot}%{_libdir}/libdpe*

mkdir -p %{buildroot}%{_sysconfdir}/pki/pesign/
mkdir -p %{buildroot}%{_sysconfdir}/pki/pesign-rh-test/
cp -a etc/pki/pesign/* %{buildroot}%{_sysconfdir}/pki/pesign/
cp -a etc/pki/pesign-rh-test/* %{buildroot}%{_sysconfdir}/pki/pesign-rh-test/

if [ %{macrosdir} != %{_sysconfdir}/rpm ]; then
	mkdir -p %{buildroot}%{macrosdir}
	mv %{buildroot}%{_sysconfdir}/rpm/macros.pesign \
		%{buildroot}%{macrosdir}
	rmdir %{buildroot}%{_sysconfdir}/rpm
fi
rm -vf %{buildroot}/usr/share/doc/pesign-%{version}/COPYING

# and find-debuginfo.sh has some pretty awful deficencies too...
cp -av libdpe/*.[ch] src/

install -d -m 0755 %{buildroot}%{python3_sitelib}/mockbuild/plugins/
install -m 0755 %{SOURCE2} %{buildroot}%{python3_sitelib}/mockbuild/plugins/

%pre
getent group pesign >/dev/null || groupadd -r pesign
getent passwd pesign >/dev/null || \
	useradd -r -g pesign -d /run/pesign -s /sbin/nologin \
		-c "Group for the pesign signing daemon" pesign
exit 0

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 17 || 0%{?azl}
%post
%systemd_post pesign.service

%preun
%systemd_preun pesign.service

%postun
%systemd_postun_with_restart pesign.service

%posttrans
certutil -d %{_sysconfdir}/pki/pesign/ -X -L > /dev/null

# this is disabled currently because it breaks the fedora kernel build root
# generation - because we don't currently have a good way of populating
# /etc/pesign/{users,groups} before the buildroot is installed, or
# populating them and re-running pesign-authorize afterwards but before the
# package build of e.g. kernel
#%%{_libexecdir}/pesign/pesign-authorize
%endif

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md TODO
%{_bindir}/authvar
%{_bindir}/efikeygen
%{_bindir}/pesigcheck
%{_bindir}/pesign
%{_bindir}/pesign-client
%{_bindir}/pesum
%dir %{_libexecdir}/pesign/
%dir %attr(0770,pesign,pesign) %{_sysconfdir}/pki/pesign/
%config(noreplace) %attr(0660,pesign,pesign) %{_sysconfdir}/pki/pesign/*
%dir %attr(0775,pesign,pesign) %{_sysconfdir}/pki/pesign-rh-test/
%config(noreplace) %attr(0664,pesign,pesign) %{_sysconfdir}/pki/pesign-rh-test/*
%{_libexecdir}/pesign/pesign-authorize
%{_libexecdir}/pesign/pesign-rpmbuild-helper
%config(noreplace)/%{_sysconfdir}/pesign/users
%config(noreplace)/%{_sysconfdir}/pesign/groups
%{_sysconfdir}/popt.d/pesign.popt
%{macrosdir}/macros.pesign
%{_mandir}/man*/*
%dir %attr(0770, pesign, pesign) %{_rundir}/%{name}
%ghost %attr(0660, -, -) %{_rundir}/%{name}/socket
%ghost %attr(0660, -, -) %{_rundir}/%{name}/pesign.pid
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 17 || 0%{?azl}
%{_tmpfilesdir}/pesign.conf
%{_unitdir}/pesign.service
%endif
%{python3_sitelib}/mockbuild/plugins/*/pesign.*
%{python3_sitelib}/mockbuild/plugins/pesign.*

%changelog
* Thu Feb 08 2024 Dan Streetman <ddstreet@ieee.org> - 116-3
- Initial Azure Linux import from Fedora 39 (license: MIT).
- license verified

* Mon Feb 20 2023 Nicolas Frayer <nfrayer@redhat.com> - 116-2
- cms_common: Fixed Segmentation fault

* Tue Jan 31 2023 Robbie Harwood <rharwood@redhat.com> - 116-1
- New upstream release (116)
- Resolves: CVE-2022-3560

* Wed Aug 31 2022 Robbie Harwood <rharwood@redhat.com> - 115-9
- Roll up to pjones's smartcard/cms fixes

* Tue Aug 02 2022 Robbie Harwood <rharwood@redhat.com> - 115-8
- Rebuild for python bytecode change
- See-also: #2107826

* Thu Jul 07 2022 Robbie Harwood <rharwood@redhat.com> - 115-6
- Fix formatting of man pages
- Resolves: #2104778

* Mon Apr 04 2022 Robbie Harwood <rharwood@redhat.com> - 115-5
- Detect presence of rpm-sign when checking for rhel-ness

* Fri Apr 01 2022 Robbie Harwood <rharwood@redhat.com> - 115-4
- Correctly handle rhel and centos macros

* Fri Mar 25 2022 Robbie Harwood <rharwood@redhat.com> - 115-3
- Add -D_GLIBCXX_ASSERTIONS to CPPFLAGS

* Thu Mar 24 2022 Robbie Harwood <rharwood@redhat.com> - 115-2
- Add support for non-koji signing in macros
- Resolves: #1880858

* Tue Mar 08 2022 Robbie Harwood <rharwood@redhat.com> - 115-1
- New upstream version (115)

* Mon Feb 14 2022 Robbie Harwood <rharwood@redhat.com> - 114-4
- Disable -fanalyzer since it's broken and pragmas don't work
- See-also: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=104370

* Mon Feb 14 2022 Robbie Harwood <rharwood@redhat.com> - 114-3
- Fix explicit NULL deref when daemonizing

* Wed Feb 02 2022 Robbie Harwood <rharwood@redhat.com> - 114-2
- Attempt to fix signing parsing by dropping pesign_args

* Tue Feb 01 2022 Robbie Harwood <rharwood@redhat.com> - 114-1
- New upstream version (114)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 113-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 113-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 113-16
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 113-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Jeff Law <law@redhat.com> - 113-14
- Turn off -Wfree-nonheap-object

* Mon Aug 03 2020 Peter Jones <pjones@redhat.com> - 113-13
- Add the rundir related stuff that was staged on my f32 checkout.

* Mon Aug 03 2020 Peter Jones <pjones@redhat.com> - 113-12
- Try to make kernel and fwupd both work at the same time.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 113-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Peter Jones <pjones@redhat.com> - 113-10
- I really cannot figure out why bkernel01 thinks the certificate nickname
  starts with /CN=, but it does, so I'm gonna stop fighting with the sand.

* Thu Jul 16 2020 Peter Jones <pjones@redhat.com> - 113-9
- Even more kernel build debugging...

* Tue Jul 07 2020 Peter Jones <pjones@redhat.com> - 113-8
- More kernel build debugging...

* Tue Jul 07 2020 Peter Jones <pjones@redhat.com> - 113-6
- Disable the pesign-authorize call in posttrans, until we can figure out a
  better way to deal with that in the fedora kernel builder chroot setup

* Tue Jul 07 2020 Peter Jones <pjones@redhat.com> - 113-5
- Make pesign require nss-tools for the posttrans scriptlet
- Move most of macros.pesign to /usr/libexec/pesign/pesign-rpmbuild-helper

* Mon Jul 06 2020 Peter Jones <pjones@redhat.com> - 113-4
- Attempt to fix kernel signing failures caused by -3...

* Fri Jun 12 2020 Peter Jones <pjones@redhat.com> - 113-3
- Fix the signer name for fedora and some other minor nits
  Related: rhbz#1708773
  Related: rhbz#1678146

* Thu Jun 11 2020 Peter Jones <pjones@redhat.com> - 113-2
- Fix a signing protocol bug we introduced in 113 that makes the fedora
  kernel builders fail.
  Related: rhbz#1708773

* Thu Jun 11 2020 Javier Martinez Canillas <javierm@redhat.com> - 113-1
- Update to 113 release
  Resolves: rhbz#1708773

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.112-32
- Making binaries paths compatible with CBL-Mariner's paths.

* Mon Jun 08 2020 Javier Martinez Canillas <javierm@redhat.com> - 0.112-31
- Switch default NSS database to SQLite format (pjones)
  Resolves: rhbz#1827902

* Wed Dec 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.112-31
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Set -Werror=format-security to avoid build break from warnings.

* Mon Feb 24 2020 Peter Jones <pjones@redhat.com> - 0.112-30
- Make sure the patch for -29 is actually in the build in f32, and
  synchronize with master.

* Tue Feb 18 2020 Peter Jones <pjones@redhat.com> - 0.112-29
- Rebuild to match OpenSC's token name mangling change.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Peter Jones <pjones@redhat.com> - 0.112-27
- Rebuild to fix an NSS API issue.	

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar  6 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.112-25
- Fix build (#1675653)
- Add missing closing quote in macro (#1651020)
- Update obsolete /var/run/ path (#1678146)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.112-22
- Minor spec cleanups, fix arm conditional

* Fri Oct 06 2017 Troy Dawson <tdawson@redhat.com> - 0.112-21
- Cleanup spec file conditionals

* Tue Aug 15 2017 Peter Jones <pjones@redhat.com> - 0.112-20
- Maybe fewer typoes would be better.

* Tue Aug 15 2017 Peter Jones <pjones@redhat.com> - 0.112-19
- Update to match f26's build so new kernel builds will work.

* Thu Aug 10 2017 Peter Jones <pjones@redhat.com> - 0.112-10
- Try to fix the db problem nirik is seeing trying to upgrade the builders.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Peter Jones <pjones@redhat.com> - 0.112-7
- Rebuild for efivar-31-1.fc26
  Related: rhbz#1468841

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 06 2017 Peter Jones <pjones@redhat.com> - 0.112-5
- Don't Req: or BuildReq: coolkey or opensc; those belong in system deploy
  scripts.
  Related: rhbz#1349073

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 0.112-4
- Build as -4 to make bodhi happy.

* Fri Aug 12 2016 Adam Williamson <awilliam@redhat.com> - 0.112-3
- backport fix for command line parsing from upstream master

* Wed Aug 10 2016 Peter Jones <pjones@redhat.com> - 0.112-2
- Build with newer efivar.

* Wed Apr 20 2016 Peter Jones <pjones@redhat.com> - 0.112-1
- Update to 0.112
- Also fix up some spec file woes:
  - dumb things in %%setup
  - find-debuginfo.sh not working right for some source files...

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.111-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Peter Jones <pjones@redhat.com> - 0.111-7
- Obsolete pesign-rh-test-certs, it was in -1's update.
  Resolves: rhbz#1283475

* Wed Dec 02 2015 Peter Jones <pjones@redhat.com> - 0.111-6
- *Don't* use --certdir if we're using the socket.
  Related: rhbz#1283475
  Related: rhbz#1284063
  Related: rhbz#1284561

* Tue Dec 01 2015 Peter Jones <pjones@redhat.com> - 0.111-5
- Actually do a better job of choosing which cert to use when, so people will
  stop seeing any of this problem.  (Thanks for the thought, jforbes.)
  Resolves: rhbz#1283475
  Resolves: rhbz#1284063
  Resolves: rhbz#1284561

* Mon Nov 30 2015 Peter Jones <pjones@redhat.com> - 0.111-5
- setfacl even harder.
  Related: rhbz#1283475
  Related: rhbz#1284063
  Related: rhbz#1284561

* Fri Nov 20 2015 Peter Jones <pjones@redhat.com> - 0.111-3
- Better ACL setting code.
  Related: rhbz#1283475

* Thu Nov 19 2015 Peter Jones <pjones@redhat.com> - 0.111-2
- Allow the mockbuild user to read the nss database if the account exists.

* Wed Oct 28 2015 Peter Jones <pjones@redhat.com> - 0.111-1
- Rebase to 0.111
- Split test certs out into a "Recommends" subpackage.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar  4 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.110-2
- Install macros in %%{_rpmconfigdir}/macros.d where available (#1074281)

* Fri Oct 24 2014 Peter Jones <pjones@redhat.com> - 0.110-1
- Update to pesign-0.110

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Peter Jones <pjones@redhat.com> - 0.108-2
- Fix a networking problem nirik observed when reinstalling builders.

* Sat Aug 10 2013 Peter Jones <pjones@redhat.com> - 0.108-1
- Remove errant result files and raise an error from %%pesign 

* Tue Aug 06 2013 Peter Jones <pjones@redhat.com> - 0.106-3
- Add code for signing in RHEL 7

* Mon Aug 05 2013 Peter Jones <pjones@redhat.com> - 0.106-2
- Fix for new %%doc rules.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.106-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Peter Jones <pjones@redhat.com> - 0.106-1
- Update to 0.106
- Hopefully fix the segfault dgilmore was seeing.

* Mon May 20 2013 Peter Jones <pjones@redhat.com> - 0.105-1
- Various bug fixes.

* Wed May 15 2013 Peter Jones <pjones@redhat.com> - 0.104-1
- Make sure alignment is correct on signature list entries
  Resolves: rhbz#963361
- Make sure section alignment is correct if we have to extend the file

* Wed Feb 06 2013 Peter Jones <pjones@redhat.com> - 0.103-2
- Conditionalize systemd bits so they don't show up in RHEL 6 builds

* Tue Feb 05 2013 Peter Jones <pjones@redhat.com> - 0.103-1
- One more compiler problem.  Let's expect a few more, shall we?

* Tue Feb 05 2013 Peter Jones <pjones@redhat.com> - 0.102-1
- Don't use --std=gnu11 because we have to work on RHEL 6 builders.

* Mon Feb 04 2013 Peter Jones <pjones@redhat.com> - 0.101-1
- Update to 0.101 to fix more "pesign -E" issues.

* Fri Nov 30 2012 Peter Jones <pjones@redhat.com> - 0.100-1
- Fix insertion of signatures from a file.

* Mon Nov 26 2012 Matthew Garrett <mjg59@srcf.ucam.org> - 0.99-9
- Add a patch needed for new shim builds

* Fri Oct 19 2012 Peter Jones <pjones@redhat.com> - 0.99-8
- Get the Fedora signing token name right.

* Fri Oct 19 2012 Peter Jones <pjones@redhat.com>
- Add coolkey and opensc modules to pki database during %%install.

* Fri Oct 19 2012 Peter Jones <pjones@redhat.com> - 0.99-7
- setfacl u:kojibuilder:rw /var/run/pesign/socket
- Fix command line checking in client
- Add client stdin pin reading.

* Thu Oct 18 2012 Peter Jones <pjones@redhat.com> - 0.99-6
- Automatically select daemon as signer when using rpm macros.

* Thu Oct 18 2012 Peter Jones <pjones@redhat.com> - 0.99-5
- Make it work on the -el6 branch as well.

* Wed Oct 17 2012 Peter Jones <pjones@redhat.com> - 0.99-4
- Fix some more bugs found by valgrind and coverity.
- Don't build utils/ ; we're not using them and they're not ready anyway. 

* Wed Oct 17 2012 Peter Jones <pjones@redhat.com> - 0.99-3
- Fix daemon startup bug from 0.99-2

* Wed Oct 17 2012 Peter Jones <pjones@redhat.com> - 0.99-2
- Fix various bugs from 0.99-1
- Don't make the database unreadable just yet.

* Mon Oct 15 2012 Peter Jones <pjones@redhat.com> - 0.99-1
- Update to 0.99
- Add documentation for client/server mode.
- Add --pinfd and --pinfile to server mode.

* Fri Oct 12 2012 Peter Jones <pjones@redhat.com> - 0.98-1
- Update to 0.98
- Add client/server mode.

* Mon Oct 01 2012 Peter Jones <pjones@redhat.com> - 0.10-5
- Fix missing section address fixup.

* Wed Aug 15 2012 Peter Jones <pjones@redhat.com> - 0.10-4
- Make macros.pesign even better (and make it work right for i686 packages)

* Tue Aug 14 2012 Peter Jones <pjones@redhat.com> - 0.10-3
- Only sign things on x86_64; all else ignore gracefully.

* Tue Aug 14 2012 Peter Jones <pjones@redhat.com> - 0.10-2
- Make macros.pesign more reliable

* Mon Aug 13 2012 Peter Jones <pjones@redhat.com> - 0.10-1
- Update to 0.10
- Include rpm macros to support easy custom signing of signed packages.

* Fri Aug 10 2012 Peter Jones <pjones@redhat.com> - 0.9-1
- Update to 0.9
- Bug fix from Gary Ching-Pang Lin
- Support NSS Token selection for use with smart cards.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 0.8-1
- Update to 0.8
- Don't open the db read-write
- Fix permissions on keystore (everybody can sign with test keys)

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 0.7-2
- Include test keys.

* Mon Jul 30 2012 Peter Jones <pjones@redhat.com> - 0.7-1
- Update to 0.7
- Better fix for MS compatibility.

* Mon Jul 30 2012 Peter Jones <pjones@redhat.com> - 0.6-1
- Update to 0.6
- Bug-for-bug compatibility with signtool.exe .

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Peter Jones <pjones@redhat.com> - 0.5-1
- Rebase to 0.5
- Do more rigorous bounds checking when hashing a new binary.

* Tue Jul 10 2012 Peter Jones <pjones@redhat.com> - 0.3-2
- Rebase to 0.4

* Fri Jun 22 2012 Peter Jones <pjones@redhat.com> - 0.3-2
- Move man page to a more reasonable place.

* Fri Jun 22 2012 Peter Jones <pjones@redhat.com> - 0.3-1
- Update to upstream's 0.3 .

* Thu Jun 21 2012 Peter Jones <pjones@redhat.com> - 0.2-4
- Do not build with smp flags.

* Thu Jun 21 2012 Peter Jones <pjones@redhat.com> - 0.2-3
- Make it build on i686, though it's unclear it'll ever be necessary.

* Thu Jun 21 2012 Peter Jones <pjones@redhat.com> - 0.2-2
- Fix compile problem with f18's compiler.

* Thu Jun 21 2012 Peter Jones <pjones@redhat.com> - 0.2-1
- Fix some rpmlint complaints nirik pointed out
- Add popt-devel build dep

* Fri Jun 15 2012 Peter Jones <pjones@redhat.com> - 0.1-1
- First version of SRPM.
