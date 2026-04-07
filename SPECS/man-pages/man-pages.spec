## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Linux kernel and C library user-space interface documentation
Name: man-pages
Version: 6.13
Release: %autorelease
# List of all licenses - each with an example of a man-page that uses it
# (complete list of all man-pages per license would be too long)
# BSD-2-Clause: man5/elf.5
# BSD-3-Clause: man3/list.3
# BSD-4.3TAHOE: man5/resolv.conf.5
# BSD-4-Clause-UC: man2/accept.2
# GPL-1.0-or-later: man1/ldd.1
# GPL-2.0-only: man2/fallocate.2
# GPL-2.0-or-later: man1/getent.1
# LicenseRef-Fedora-Public-Domain: man2/nfsservctl.2
# LicenseRef-Fedora-UltraPermissive: man2/futex.2
# Linux-man-pages-1-para: man2/getcpu.2
# Linux-man-pages-copyleft: man2/chdir.2
# Linux-man-pages-copyleft-2-para: man2/move_pages.2
# Linux-man-pages-copyleft-var: man2/get_mempolicy.2
# MIT: man3/program_invocation_name.3
# Spencer-94: man7/regex.7
License: BSD-2-Clause AND BSD-3-Clause AND BSD-4.3TAHOE AND BSD-4-Clause-UC AND GPL-1.0-or-later AND GPL-2.0-only AND GPL-2.0-or-later AND LicenseRef-Fedora-Public-Domain AND LicenseRef-Fedora-UltraPermissive AND Linux-man-pages-1-para AND Linux-man-pages-copyleft AND Linux-man-pages-copyleft-2-para AND Linux-man-pages-copyleft-var AND MIT AND Spencer-94
URL: http://www.kernel.org/doc/man-pages/
# Verify signature:
# wget http://www.kernel.org/pub/linux/docs/man-pages/man-pages-%%{version}.tar.xz
# wget http://www.kernel.org/pub/linux/docs/man-pages/man-pages-%%{version}.tar.sign
# gpg --armour \
# 	--no-default-keyring \
#	--keyring ./man-pages.gpg --import ./man-pages.keyring
# gpg --no-default-keyring --keyring ./man-pages.gpg \
# 	--verify man-pages-%%{version}.tar.sign man-pages-%%{version}.tar.xz
# Verify "Good signature from" for the stored key.
Source0: http://www.kernel.org/pub/linux/docs/man-pages/man-pages-%{version}.tar.xz
Source1: http://www.kernel.org/pub/linux/docs/man-pages/man-pages-%{version}.tar.sign

BuildRequires: make
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives

# attr.5 man page was moved from attr to man-pages in attr-2.4.47-11
Conflicts: attr < 2.4.47-11

# keyrings.7, persistent-keyring.7, process-keyring.7, session-keyring.7,
# thread-keyring.7, user-keyring.7 and user-session-keyring.7 man pages
# were moved from keyutils-libs to man-pages in keyutils-libs-1.5.10
Conflicts: keyutils-libs < 1.5.10

Autoreq: false
BuildArch: noarch

## Patches ##

# Regular man pages
# resolves: #650985
# https://bugzilla.kernel.org/show_bug.cgi?id=53781
Patch21: man-pages-3.42-close.patch

# Add rtas.2, swapcontext.2 and cons.saver.8 man pages
Patch28: additional-man-pages.patch

%description
A large collection of manual pages from the Linux Documentation Project (LDP).

%prep
%setup -q

%patch -P 21 -p1
%patch -P 28 -p1

## Remove man pages we are not going to use ##

# deprecated
rm man2/pciconfig_{write,read,iobase}.2

# problem with db x db4 (#198597) - man pages are obsolete
rm man3/{db,btree,dbopen,hash,mpool,recno}.3

# we are not using SystemV anymore
rm man7/boot.7

# remove man pages deprecated by libxcrypt (#1610307)
rm man3/crypt{,_r}.3

%build
# nothing to build

%install
make -R install prefix=/usr DESTDIR=$RPM_BUILD_ROOT

# The man.7 manual page is empty and references groff_man.7, but we
# don't want to explicitly require installing groff to make the set
# of man pages complete.
#
# rename files for alternative usage
mv %{buildroot}%{_mandir}/man7/man.7 %{buildroot}%{_mandir}/man7/man.%{name}.7
touch %{buildroot}%{_mandir}/man7/man.7

# Remove binaries we don't use and their man pages.
rm %{buildroot}%{_bindir}/diffman-git
rm %{buildroot}%{_bindir}/mansect
rm %{buildroot}%{_bindir}/pdfman
rm %{buildroot}%{_bindir}/sortman
rm %{buildroot}%{_mandir}/man1/mansect.1
rm %{buildroot}%{_mandir}/man1/diffman-git.1
rm %{buildroot}%{_mandir}/man1/pdfman.1
rm %{buildroot}%{_mandir}/man1/sortman.1

%pre
# remove alternativized files if they are not symlinks
[ -L %{_mandir}/man7/man.7.gz ] || rm -f %{_mandir}/man7/man.7.gz >/dev/null 2>&1 || :

%post
# set up the alternatives files
%{_sbindir}/update-alternatives --install %{_mandir}/man7/man.7.gz man.7.gz %{_mandir}/man7/man.%{name}.7.gz 300 \
    >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove man.7.gz %{_mandir}/man7/man.%{name}.7.gz >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ]; then
    if [ "$(readlink %{_sysconfdir}/alternatives/man.7.gz)" == "%{_mandir}/man7/man.%{name}.7.gz" ]; then
        %{_sbindir}/update-alternatives --set man.7.gz %{_mandir}/man7/man.%{name}.7.gz >/dev/null 2>&1 || :
    fi
fi

%files
%doc README Changes
%ghost %{_mandir}/man7/man.7.gz
%{_mandir}/man*/*

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 6.13-3
- Latest state for man-pages

* Mon Dec 01 2025 Carlos O'Donell <carlos@redhat.com> - 6.13-2
- Fix "%%setup -q" and remove "-a 0" (#2417800)

* Wed Nov 19 2025 Carlos O'Donell <carlos@redhat.com> - 6.13-1
- Update to 6.13 upstream release

* Wed Nov 19 2025 Carlos O'Donell <carlos@redhat.com> - 6.9.1-7
- Break up man-pages-additional-20140218.tar.xz
- Add rtas.2, swapcontext.2 and cons.saver.8 man pages as a patch.

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 28 2025 Lukas Javorsky <ljavorsk@redhat.com> - 6.9.1-4
- Disable the staging packit bot

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 17 2024 Packit <hello@packit.dev> - 6.9.1-1
- Update to 6.9.1 upstream release
- Resolves: rhbz#2292469

* Mon Jun 17 2024 Lukas Javorsky <ljavorsk@redhat.com> - 6.9-2
- Add issue_repository to Packit config

* Fri Jun 14 2024 Packit <hello@packit.dev> - 6.9-1
- Update to 6.9 upstream release
- Resolves: rhbz#2292469

* Wed May 22 2024 Lukas Javorsky <ljavorsk@redhat.com> - 6.8-1
- Update to 6.8 upstream release
- Resolves: rhbz#2281488

* Wed Mar 20 2024 Lukas Javorsky <ljavorsk@redhat.com> - 6.7-1
- Rebase to version 6.7

* Mon Feb 12 2024 Lukas Javorsky <ljavorsk@redhat.com> - 6.06-1
- Rebase to version 6.06

* Tue Jan 30 2024 Packit <hello@packit.dev> - 6.05.01-1
- [packit] 6.05.01 upstream release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 21 2023 Nikola Forró <nforro@redhat.com> - 6.05-5
- unix.7: SO_PEERCRED: Mention listen(2)

* Thu Aug 10 2023 Nikola Forró <nforro@redhat.com> - 6.05-4
- Enable Packit staging instance

* Thu Aug 03 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.05-3
- Upstream has removed the unapproved license in man5/dir_colors.5

* Wed Aug 02 2023 Nikola Forró <nforro@redhat.com> - 6.05-2
- Configure upstream tag template

* Wed Aug 02 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.05-1
- Rebase to version 6.05

* Wed Aug 02 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.04-7
- Add upstream_project_url to packit config

* Tue Jul 25 2023 Adam Dobeš <adobes@redhat.com> - 6.04-6
- migrated to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Nikola Forró <nforro@redhat.com> - 6.04-4
- Remove dir_colors.5 man page with unallowed license

* Tue Apr 18 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.04-3
- Enable pull_from_upstream packit action

* Mon Apr 03 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.04-2
- Trigger bodhi build for Fedora branched

* Mon Apr 03 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.04-1
- Rebase to version 6.04

* Tue Feb 14 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.03-3
- Add allowed PR authors for Packit job

* Tue Feb 14 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.03-2
- Enable Packit koji_build and bodhi_update for man-pages

* Mon Feb 13 2023 Lukas Javorsky <ljavorsk@redhat.com> - 6.03-1
- Rebase to version 6.03

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Nikola Forró <nforro@redhat.com> - 6.02-1
- Rebase to version 6.02
  resolves: #2155908

* Fri Oct 21 2022 Lukas Javorsky <ljavorsk@redhat.com> - 6.01-1
- Rebase to version 6.01

* Fri Oct 14 2022 Lukas Javorsky <ljavorsk@redhat.com> - 6.00-1
- Rebase to version 6.00
- Patch 22 upstreamed

* Tue Aug 23 2022 Nikola Forró <nforro@redhat.com> - 5.13-5
- nsswitch.conf.5: Mention subid database

* Tue Aug 09 2022 Nikola Forró <nforro@redhat.com> - 5.13-4
- Remove POSIX man pages due to disallowed license
  resolves: #2116859

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 27 2021 Nikola Forró <nforro@redhat.com> - 5.13-1
- update to 5.13
  resolves: #1998442

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Nikola Forró <nforro@redhat.com> - 5.12-1
- update to 5.12
  resolves: #1974538

* Mon Mar 22 2021 Nikola Forró <nforro@redhat.com> - 5.11-1
- update to 5.11
  resolves: #1941571

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 24 2020 Nikola Forró <nforro@redhat.com> - 5.10-1
- update to 5.10
  resolves: #1909987

* Fri Nov 06 2020 Nikola Forró <nforro@redhat.com> - 5.09-2
- update POSIX man pages to 2017-a
  resolves: #1691808

* Mon Nov 02 2020 Nikola Forró <nforro@redhat.com> - 5.09-1
- update to 5.09
  resolves: #1893576

* Mon Aug 17 2020 Nikola Forró <nforro@redhat.com> - 5.08-1
- update to 5.08
  resolves: #1868674

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 21 2020 Nikola Forró <nforro@redhat.com> - 5.07-1
- update to 5.07

* Thu Apr 16 2020 Nikola Forró <nforro@redhat.com> - 5.06-3
- Fix another typo in postun scriptlet

* Thu Apr 16 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 5.06-2
- Fix typo in postun scriptlet

* Tue Apr 14 2020 Nikola Forró <nforro@redhat.com> - 5.06-1
- update to 5.06
  resolves: #1823161

* Sun Mar 01 2020 Nikola Forró <nforro@redhat.com> - 5.04-6
- fix %pre scriptlet

* Fri Feb 28 2020 Nikola Forró <nforro@redhat.com> - 5.04-5
- fix upgrades from non-alternativized versions

* Thu Feb 27 2020 Nikola Forró <nforro@redhat.com> - 5.04-4
- use alternatives for man.7

* Mon Feb 03 2020 Nikola Forró <nforro@redhat.com> - 5.04-3
- add kernel_lockdown.7 man page
  resolves: #1797591

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 20 2019 Nikola Forró <nforro@redhat.com> - 5.04-1
- update to 5.04
  resolves #1774584

* Wed Oct 16 2019 Nikola Forró <nforro@redhat.com> - 5.03-1
- update to 5.03
  resolves #1761010

* Thu Oct 10 2019 Nikola Forró <nforro@redhat.com> - 5.02-2
- resolv.conf.5: update information about search list
  resolves #1758515

* Tue Aug 06 2019 Nikola Forró <nforro@redhat.com> - 5.02-1
- update to 5.02

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Nikola Forró <nforro@redhat.com> - 5.01-1
- update to 5.01
  resolves #1708251

* Wed Mar 06 2019 Nikola Forró <nforro@redhat.com> - 5.00-1
- update to 5.00
  resolves #1686085

* Tue Feb 26 2019 Nikola Forró <nforro@redhat.com> - 4.16-5
- socket.2: fix dead link in AF_ALG note
  resolves #1679505

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 03 2018 Nikola Forró <nforro@redhat.com> - 4.16-3
- remove man pages deprecated by libxcrypt
  resolves #1610307

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 03 2018 Nikola Forró <nforro@redhat.com> - 4.16-1
- update to 4.16
  resolves #1574060

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Nikola Forró <nforro@redhat.com> - 4.15-1
- update to 4.15
  resolves #1541376

* Wed Nov 29 2017 Nikola Forró <nforro@redhat.com> - 4.14-1
- update to 4.14

* Mon Sep 18 2017 Nikola Forró <nforro@redhat.com> - 4.13-1
- update to 4.13
  resolves #1492258

* Tue Aug 01 2017 Nikola Forró <nforro@redhat.com> - 4.12-1
- update to 4.12
  resolves #1473875

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 04 2017 Nikola Forró <nforro@redhat.com> - 4.11-1
- update to 4.11
  resolves #1447816

* Wed Mar 15 2017 Nikola Forró <nforro@redhat.com> - 4.10-2
- add conflict with keyutils-libs versions containing conflicting man pages
  resolves #1432546

* Wed Mar 15 2017 Nikola Forró <nforro@redhat.com> - 4.10-1
- update to 4.10
  resolves #1432268

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Nikola Forró <nforro@redhat.com> - 4.09-2
- pthread_once.3p: fix return type of initialize_random() function
  resolves #1415757

* Tue Dec 13 2016 Nikola Forró <nforro@redhat.com> - 4.09-1
- update to 4.09
  resolves #1403813

* Mon Oct 10 2016 Nikola Forró <nforro@redhat.com> - 4.08-1
- update to 4.08
  resolves #1382985

* Thu Oct 06 2016 Richard W.M. Jones <rjones@redhat.com> - 4.07-2
- Bump release version and rebuild.

* Thu Jul 28 2016 Nikola Forró <nforro@redhat.com> - 4.07-1
- update to 4.07
  resolves #1358060

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 4.06-2
- remove non-free man-pages (bz#1334279)

* Tue May 10 2016 Nikola Forró <nforro@redhat.com> - 4.06-1
- update to 4.06
  resolves #1334727

* Tue May 10 2016 Nikola Forró <nforro@redhat.com> - 4.05-3
- popen.3: RETURN VALUE: describe successful case
  resolves #1331312

* Tue May 10 2016 Nikola Forró <nforro@redhat.com> - 4.05-2
- clone.2, fork.2: document ERESTARTNOINTR error code
  resolves #1330663

* Wed Mar 16 2016 Nikola Forró <nforro@redhat.com> - 4.05-1
- update to 4.05
  resolves #1317877

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Nikola Forró <nforro@redhat.com> - 4.04-1
- updated to 4.04
  resolves #1294723

* Mon Dec 07 2015 Nikola Forró <nforro@redhat.com> - 4.03-1
- updated to 4.03
  resolves #1288782

* Thu Oct 22 2015 Nikola Forró <nforro@redhat.com> - 4.02-2
- added conflict with attr versions containing attr.5 man page
  resolves #1273702

* Mon Aug 10 2015 Nikola Forró <nforro@redhat.com> - 4.02-1
- updated to 4.02
  resolves #1251780
  resolves #1249444

* Fri Jul 24 2015 Nikola Forró <nforro@redhat.com> - 4.01-1
- updated to 4.01
  resolves #1246298

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 jchaloup <jchaloup@redhat.com> - 4.00-2
- rtld-audit.7: use the correct format character
  resolves: #1222719

* Thu May 07 2015 jchaloup <jchaloup@redhat.com> - 4.00-1
- updated to 4.00
  resolves: #1219478

* Mon Apr 20 2015 jchaloup <jchaloup@redhat.com> - 3.83-1
- updated to 3.83
  resolves: #1213147

* Tue Mar 31 2015 jchaloup <jchaloup@redhat.com> - 3.82-1
- updated to 3.82
  resolves: #1207665

* Tue Mar 03 2015 jchaloup <jchaloup@redhat.com> - 3.81-1
- updated to 3.81
  resolves: #1197926

* Sun Feb 22 2015 jchaloup <jchaloup@redhat.com> - 3.80-1
- updated to 3.80
  resolves: #1194974

* Mon Feb 02 2015 jchaloup <jchaloup@redhat.com> - 3.79-1
- updated to 3.79
  resolves: #1188036

* Fri Jan 23 2015 jchaloup <jchaloup@redhat.com> - 3.78-1
- updated to 3.78
  resolves: #1185309

* Thu Jan 15 2015 jchaloup <jchaloup@redhat.com> - 3.77-1
- updated to 3.77
  resolves: #1181496

* Mon Jan 05 2015 jchaloup <jchaloup@redhat.com> - 3.76-1
- updated to 3.76
  resolves: #1178355

* Sat Oct 18 2014 jchaloup <jchaloup@redhat.com> - 3.75-1
- updated to 3.75
  resolves: #1154261

* Wed Oct 08 2014 jchaloup <jchaloup@redhat.com> - 3.74-1
  updated to 3.74
- resolves: #1150489

* Mon Sep 22 2014 jchaloup <jchaloup@redhat.com> - 3.73-1
- resolves: #1145003
  updated to 3.73

* Mon Sep 08 2014 jchaloup <jchaloup@redhat.com> - 3.72-1
- resolves: #1139140
  updated to 3.72

* Fri Aug 22 2014 jchaloup <jchaloup@redhat.com> - 3.71-1
- resolves: #1132845
  updated to 3.71

* Fri Jul 11 2014 jchaloup <jchaloup@redhat.com> - 3.70-1
- resolves: #1118632
  updated to 3.70

* Mon Jun 16 2014 jchaloup <jchaloup@redhat.com> - 3.69-1
- resolves: #1111836
  updated to 3.69

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 jchaloup <jchaloup@redhat.com> - 3.68-1
- resolves: #1103158
  updated to 3.68

* Tue May 27 2014 jchaloup <jchaloup@redhat.com> - 3.67-1
- resolves: #1100444
  updated to 3.67

* Fri May 09 2014 Peter Schiffer <pschiffe@redhat.com> - 3.66-1
- resolves: #1095840
  updated to 3.66

* Wed Apr 23 2014 Peter Schiffer <pschiffe@redhat.com> - 3.65-1
- resolves: #1071305
  updated to 3.65
- resolves: #1082566
  install *xattr.2 man pages

* Tue Feb 18 2014 Peter Schiffer <pschiffe@redhat.com> - 3.60-1
- updated to 3.60

* Tue Feb 18 2014 Peter Schiffer <pschiffe@redhat.com> - 3.59-1
- resolves: #1066332
  updated to 3.59
- cleaned .spec file

* Tue Feb 11 2014 Peter Schiffer <pschiffe@redhat.com> - 3.58-1
- resolves: #1063754
  updated to 3.58

* Wed Feb  5 2014 Peter Schiffer <pschiffe@redhat.com> - 3.57-2
- removed invalid patch for man(1p) man page

* Wed Jan 29 2014 Peter Schiffer <pschiffe@redhat.com> - 3.57-1
- resolves: #1058001
  updated to 3.57
- resolves: #1056781
  updated to POSIX.1 2013

* Wed Jan 15 2014 Peter Schiffer <pschiffe@redhat.com> - 3.56-1
- resolves: #1051765
  updated to 3.56

* Mon Dec 16 2013 Peter Schiffer <pschiffe@redhat.com> - 3.55-1
- resolves: #1043074
  updated to 3.55

* Wed Dec  4 2013 Peter Schiffer <pschiffe@redhat.com> - 3.54-2
- resolves: #1031703
  removed pt_chown(5) man page

* Wed Oct  9 2013 Peter Schiffer <pschiffe@redhat.com> - 3.54-1
- resolves: #1009535
  updated to 3.54

* Wed Jul 31 2013 Peter Schiffer <pschiffe@redhat.com> - 3.53-1
- resolves: #990459
  updated to 3.53

* Mon Jul 22 2013 Peter Schiffer <pschiffe@redhat.com> - 3.52-1
- resolves: #981385
  updated to 3.52
- fixed broken sentence on the futex(7) man page
- resolves: #885740
  documented O_PATH flag on the open(2) man page

* Tue Apr 23 2013 Peter Schiffer <pschiffe@redhat.com> - 3.51-1
- resolves: #921911
  updated to 3.51

* Thu Mar  7 2013 Peter Schiffer <pschiffe@redhat.com> - 3.48-1
- resolves: #918417
  updated to 3.48

* Tue Feb 12 2013 Peter Schiffer <pschiffe@redhat.com> - 3.47-1
- resolves: #910268
  updated to 3.47

* Fri Feb  1 2013 Peter Schiffer <pschiffe@redhat.com> - 3.46-2
- related: #858703
  moved killpgrp(8) man page to the amanda-client package

* Mon Jan 28 2013 Peter Schiffer <pschiffe@redhat.com> - 3.46-1
- resolves: #904950
  updated to 3.46

* Wed Jan 16 2013 Peter Schiffer <pschiffe@redhat.com> - 3.45-2
- dropped some outdated patches, few patches updated

* Fri Dec 21 2012 Peter Schiffer <pschiffe@redhat.com> - 3.45-1
- resolves: #889446
  updated to 3.45

* Wed Nov 21 2012 Peter Schiffer <pschiffe@redhat.com> - 3.44-1
- resolves: #874650
  updated to 3.44

* Thu Oct 25 2012 Peter Schiffer <pschiffe@redhat.com> - 3.43-1
- resolves: #866874
  updated to 3.43
- added description of the TCP_CONGESTION on the tcp(7) man page
- added description of the IP_MULTICAST_ALL on the ip(7) man page
- updated additional man pages

* Wed Sep 19 2012 Peter Schiffer <pschiffe@redhat.com> - 3.42-1
- resolves: #847941
  update to 3.42
- updated additional man pages
- cleaned patches
- cleaned .spec file, fixed minor encoding issue
- resolves: #837090
  updated example on inet(3) man page - use fprintf(stderr,..) instead of perror
- resolves: #751429
  included initgroups database in the nsswitch.conf(5) man page
- removed the sccs-related man pages (#203302)
- added description of single-request-reopen to the resolv.conf(5) man page (#717770)
- added missing EIDRM error code description to the shmop(2) man page (#800256)
- added documentation of several source-specific multicast socket options to the ip(7) man page (#804003)
- improved explanation about calling listen or connect on the ip(7) man page (#787567)
- added information about incorrect use of getdents(2) call to the man page (#809490)
- removed man-pages-3.22-sched_setaffinity.patch because the problem it describes was fixed in the kernel. see #533811 for more info
- documented why to use shutdown() before close() when dealing with sockets on close(2) man page (#650985)
- updated description of /proc/sys/fs/file-nr file in proc(5) man page (#497197)
- updated zdump(8) man page to match current zdump usage (#517309)
- fixed one incorrect error code on connect(2) man page (#392431)
- fixed typo in sysconf(3) man page (#202092)
- removed additional uuname(1) man page - was moved to the uucp package (#858642)
- removed obsolete additional userisdnctl(8) man page

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 Peter Schiffer <pschiffe@redhat.com> - 3.41-1
- resolves: #820901
  update to 3.41

* Fri Apr 27 2012 Peter Schiffer <pschiffe@redhat.com> - 3.40-2
- related: #797857
  fixed broken source file

* Fri Apr 27 2012 Peter Schiffer <pschiffe@redhat.com> - 3.40-1
- resolves: #797857
  update to 3.40

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Peter Schiffer <pschiffe@redhat.com> - 3.35-1
- resolves: #751620
  update to 3.35
- resolves: #723578
  typo in readlink(3p)

* Fri May 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-14
- resolves: #705888
  the man page for proc is missing an explanation for /proc/[pid]/cgroup

* Fri Apr 22 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-13
- resolves: #698149
  Remove documentation for "order" keyword in /etc/host.conf manpage

* Fri Apr 22 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-12
- resolves: #680214
  manpage for fallocate(2) is wrong

* Fri Mar 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-11
- resolves: #681781
  snprintf man page is wrong

* Wed Mar  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-10
- resolves: #675544
  perfmonctl(2) typo manpage fix

* Thu Feb 24 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-9
- resolves: #679899
  add scopev4 to gai.conf man page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.32-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-7
- resolves: #673586
  fix the sed pages parsing

* Thu Jan 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-6
- resolves: #652869
  fix the necessary buffer limit in the man page for readdir_r

* Thu Jan 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-5
- resolves: #672348
  problems with the encoding of characters set man-pages
  thanks Denis Barbier for a patch

* Tue Jan 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-4
- resolves: #672377
  fix man-pages-2.48-passwd.patch remove trailing dots

* Tue Jan 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-3
- resolves: #652870
  fix strtol man-page

* Mon Jan  3 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-2
- update to 3.32

* Wed Nov 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-2
- resolves: #655961
  add the conflict tag

* Fri Nov 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-1
- update to 3.31

* Thu Nov 18 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.30-3
- resolves: #647269
  PR_SET_SECCOMP and _exit, documentation bug

* Thu Nov 11 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.30-2
- Resolves: #650257
  fix open.2 O_EXCL description

* Fri Nov  5 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.30-1
- update to 3.30

* Mon Oct 25 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.29-1
- update 3.29
  several bug fixes

* Wed Oct  6 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.28-3
- don't remove numa_maps, now the man page is not in numactl
- don't remove getipnodeby{name,addr}.3 and freehostent.3
  they are not more part of glibc-devel
- fix typo in gai_{error,suspend,cancel} pages

* Wed Oct  6 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.28-2
- add quotactl.2 to man-pages (the package was removed from quota - #640590)

* Wed Oct  6 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.28-1
- update to 3.28
- move all additional man-pages to one source
    (man-pages-additional-20101006.tar.bz2)
- remove additional man-pages without the info about license

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.27-3
- Resolves: #634626
  remove link to non-existing man page

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.27-2
- Resolves: #635869
  remove the link to removed man page

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.27-1
- Update to 3.27
- remove obsolete patch

* Wed Sep  8 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.26-1
- Update to 3.26
- Resolves: 624399 (rresvport man entry misleading)

* Thu Jul  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.25-1
- Update to 3.25

* Thu Jun 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-7
- resolves: #606038
  filesystems.5 makes no mention of ext4

* Fri Jun  4 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-6
- Resolves: #596666
  Man page for mmap64 is confusing

* Mon May 31 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-5
- Resolves: #597429
  remove the duplicate info about error output (recv(2) man page)

* Mon May 10 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-4
- Resolves: #588620
  Typo in sysconf(3) Manual page

* Mon May  3 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-3
- fix atanh man-page bug in glibc was fixed so removed the info about it

* Fri Mar 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-2
- Resolves: #570703
  fix getnameinfo prototype

* Tue Mar  2 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-1
- update to 3.24
  Resolves: #569451

* Mon Feb 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-7
- Resolves: #564528
  Man page and "info" information on snprintf incomplete

* Wed Jan 27 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-6
- Resolves: #556199
  update iconv.1 man page

* Tue Jan 26 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-5
- Resolves: #557971
  remove unnecessary man-pages from man-pages_syscalls and man-pages_add

* Thu Dec  3 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-4
- fix typo in sched_setaffinity(2) patch

* Wed Dec  2 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-3
- fix sched_setaffinity(2) page - add an EXAMPLE and new NOTES

* Wed Nov 18 2009 Ivana Varekova <varekova@redhat.com> - 3.23-2
- fix ld.so man-page (#532629)

* Mon Oct  5 2009 Ivana Varekova <varekova@redhat.com> - 3.23-1
- update to 3.23
- fix proc description

* Wed Sep 16 2009 Ivana Varekova <varekova@redhat.com> - 3.22-6
- fix nsswitch.conf(5) man page

* Mon Sep 14 2009 Ivana Varekova <varekova@redhat.com> - 3.22-5
- fix strcpy.3 man page
- remove statfc64 man page from syscalls tarball

* Tue Aug 11 2009 Ivana Varekova <varekova@redhat.com> - 3.22-4
- fix gai.conf an page (#515347)

* Mon Jul 27 2009 Ivana Varekova <varekova@redhat.com> - 3.22-3
- update to 3.22

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Ivana Varekova <varekova@redhat.com> - 3.21-2
- fix major.3 man page

* Tue Apr 21 2009 Ivana Varekova <varekova@redhat.com> - 3.21-1
- update to 3.21

* Tue Mar 31 2009 Ivana Varekova <varekova@redhat.com> - 3.20-1
- update to 3.20

* Tue Mar 10 2009 Ivana Varekova <varekova@redhat.com> - 3.19-1
- update to 3.19

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Ivana Varekova <varekova@redhat.com> - 3.16-1
- update to 3.16

* Mon Dec  8 2008 Ivana Varekova <varekova@redhat.com> - 3.15-1
- update to 3.15

* Thu Nov 13 2008 Ivana Varekova <varekova@redhat.com> - 3.13-2
- fix relative path in proc.5
- not build yet

* Thu Nov 13 2008 Ivana Varekova <varekova@redhat.com> - 3.13-1
- update to 3.13

* Mon Sep 15 2008 Ivana Varekova <varekova@redhat.com> - 3.09-2
- remove numa_maps.5 man page (part of numactl)

* Fri Sep 12 2008 Ivana Varekova <varekova@redhat.com> - 3.09-1
- update to 3.09

* Thu Aug 14 2008 Ivana Varekova <varekova@redhat.com> - 3.07-1
- update to 3.07
- remove ncsa_auth.8 (#458498)

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.04-2
- fix license tag

* Tue Jul 22 2008 Ivana Varekova <varekova@redhat.com> - 3.04-1
- update to 3.04
- remove mmap, sched_setaffinity, crypt and prctl patches
- remove -f from rm commands
- remove unnecessary/bogus rm commands

* Wed Jun 18 2008 Ivana Varekova <varekova@redhat.com> - 3.00-1
- update to 3.00
- source files changes

## END: Generated by rpmautospec
