
%bcond autoreconf 1

Name:           arpwatch
Epoch:          14
Version:        3.7
Release:        10%{?dist}
Summary:        Network monitoring tools for tracking IP addresses on a network

# SPDX matching with BSD-3-Clause confirmed at
# https://gitlab.com/fedora/legal/fedora-license-data/-/issues/49
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Any files under different licenses are part of the build system and do not
# contribute to the license of the binary RPM:
#   - config.guess and config.sub are GPL-3.0-or-later
#   - configure is FSFUL
#   - install-sh is X11
#   - mkdep is BSD-4.3RENO
SourceLicense:  %{shrink:
                %{license} AND
                BSD-4.3RENO AND
                FSFUL AND
                GPL-3.0-or-later AND
                X11
                }
URL:            https://ee.lbl.gov/

Requires(pre):  shadow-utils

Requires:       /usr/sbin/sendmail
Requires:       python3

BuildRequires:  gcc
BuildRequires:  make
%if %{with autoreconf}
BuildRequires:  autoconf
%endif

BuildRequires:  /usr/sbin/sendmail
BuildRequires:  systemd-rpm-macros
%{?sysuser_requires_compat}
BuildRequires:  python3-devel
BuildRequires:  libpcap-devel

# Note that https://ee.lbl.gov/ may not link to the latest version; the
# directory listing at https://ee.lbl.gov/downloads/arpwatch/ shows all
# available versions.
Source0:        https://ee.lbl.gov/downloads/arpwatch/arpwatch-%{version}.tar.gz
# This file comes from https://standards-oui.ieee.org/oui/oui.csv; it is used
# to generate ethercodes.dat. Because it is unversioned (and frequently
# updated), we store the file directly in the repository with the spec file;
# see the update-oui-csv script.
#
# File oui.csv last fetched 2024-12-11T19:41:27+00:00.
Source1:        oui.csv
Source2:        arpwatch.service
Source3:        arpwatch.sysconfig
Source4:        arp2ethers.8
Source5:        massagevendor.8
Source6:        arpwatch.sysusers

# The latest versions of all “arpwatch-3.1-*” patches were sent upstream by
# email 2021-04-24.

# Fix section numbers in man page cross-references. With minor changes, this
# patch dates all the way back to arpwatch-2.1a4-man.patch, from RHBZ #15442.
Patch:          arpwatch-3.1-man-references.patch
# Add, and document, a -u argument to change to a specified unprivileged user
# after establishing sockets. This combines and improves multiple previous
# patches; see patch header and changelog for notes.
Patch:          arpwatch-3.2-change-user.patch
# Fix nonstandard sort flags in arp2ethers script.
Patch:          arpwatch-3.1-arp2ethers-sort-invocation.patch
# Fix stray rm (of an undefined variable) in example arpfetch script.
Patch:          arpwatch-3.1-arpfetch-stray-rm.patch
# Do not add /usr/local/bin or /usr/local/sbin to the PATH in any scripts
Patch:          arpwatch-3.2-no-usr-local-path.patch
# Do not attempt to search for local libpcap libraries lying around in the
# parent of the build directory, or anywhere else random. This is not expected
# to succeed anyway, but it is better to be sure.
Patch:          arpwatch-3.1-configure-no-local-pcap.patch
# RHBZ #244606: Correctly handle -n 0/32 to allow the user to disable reporting
# bogons from 0.0.0.0.
Patch:          arpwatch-3.1-all-zero-bogon.patch
# When arpwatch is terminated cleanly by a signal (INT/TERM/HUP) handler, the
# exit code should be zero for success instead of nonzero for failure.
Patch:          arpwatch-3.5-exitcode.patch
# When -i is not given, do not just try the first device found, but keep
# checking devices until a usable one is found, if any is available.
# Additionally, handle the case where a device provides both supported and
# unsupported datalink types.
Patch:          arpwatch-3.5-devlookup.patch

# Replace _getshort(), “a glibc function that hasn't been declared in the
# installed headers for many, many years,” with ns_get16(). Fixes C99
# compatibility (https://bugzilla.redhat.com/show_bug.cgi?id=2166336). Sent
# upstream by email 2023-02-01.
Patch:          arpwatch-3.3-c99.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

%global pkgstatedir %{_sharedstatedir}/arpwatch

%description
The arpwatch package contains arpwatch and arpsnmp. Arpwatch and arpsnmp are
both network monitoring tools. Both utilities monitor Ethernet or FDDI network
traffic and build databases of Ethernet/IP address pairs, and can report
certain changes via email.

Install the arpwatch package if you need networking monitoring devices which
will automatically keep track of the IP addresses on your network.


%prep
%autosetup -p1

# Substitute absolute paths to awk scripts in shell scripts
sed -r -i 's|(-f *)([^[:blank:]+]\.awk)|\1%{_datadir}/arpwatch/\2|' arp2ethers

# Fix default directory in man pages to match ARPDIR in build section. This was
# formerly done by arpwatch-dir-man.patch. For thoroughness, do the same
# replacement in update-ethercodes.sh.in and bihourly.sh, even though they are
# not installed.
sed -r -i 's|/usr/local/arpwatch|%{pkgstatedir}|g' *.8.in *.sh.in *.sh

# Fix Python interpreter path (but note that this script is not installed)
sed -r -i 's|/usr/local/bin/python|%{python3}|g' update-ethercodes.sh.in

# Emailed upstream requesting a separate LICENSE/COPYING file 2022-07-30.
# For now, we extract it from the main source file’s “header” comment.
awk '/^ \* / { print substr($0, 4); } /^ \*\// { exit }' arpwatch.c |
  tee LICENSE


%conf
%if %{with autoreconf}
autoreconf --force --install --verbose
%endif

# Prior to version 3.4, this was handled by the configure script. If it is not
# defined, the build fails because time.h is not included in report.c. This
# regregression was reported upstream by email to arpwatch@ee.lbl.gov on
# 2023-09-06.
export CPPFLAGS="${CPPFLAGS-} -DTIME_WITH_SYS_TIME=1"

%configure --with-sendmail=/usr/sbin/sendmail PYTHON=%{python3}


%build
%make_build ARPDIR=%{pkgstatedir}


%install
install -p -D -m 0644 %{SOURCE6} '%{buildroot}%{_sysusersdir}/arpwatch.conf'

# The upstream Makefile does not create the directories it requires, so we must
# do it manually. Additionally, it attempts to comment out the installation of
# the init script on non-FreeBSD platforms, but this does not quite work as
# intended. We just let it install the file, then remove it afterwards.
install -d %{buildroot}%{_mandir}/man8 \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_datadir}/arpwatch \
    %{buildroot}%{pkgstatedir} \
    %{buildroot}%{_unitdir} \
    %{buildroot}%{_prefix}/etc/rc.d

%make_install

# Make install uses mode 0555, which is unconventional, and which can interfere
# with debuginfo generation since the file is not writable by its owner.
chmod -v 0755 %{buildroot}%{_sbindir}/arpwatch %{buildroot}%{_sbindir}/arpsnmp

install -p -t %{buildroot}%{_datadir}/arpwatch -m 0644 *.awk
install -p -t %{buildroot}%{_sbindir} arp2ethers
install -p massagevendor.py %{buildroot}%{_sbindir}/massagevendor

install -p -t %{buildroot}%{pkgstatedir} -m 0644 *.dat
touch %{buildroot}%{pkgstatedir}/arp.dat- \
    %{buildroot}%{pkgstatedir}/arp.dat.new

install -p -t %{buildroot}%{_unitdir} -m 0644 %{SOURCE2}
%{python3} massagevendor.py < %{SOURCE1} \
    > %{buildroot}%{pkgstatedir}/ethercodes.dat
touch -r %{SOURCE1} ethercodes.dat

# Add an environment/sysconfig file:
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/arpwatch

# Add extra man pages not provided upstream:
install -p -t %{buildroot}%{_mandir}/man8 -m 0644 %{SOURCE4} %{SOURCE5}

# Remove legacy init scripts:
rm -rvf %{buildroot}%{_prefix}/etc/rc.d


%check
# Verify the sed script in the prep section did not miss fixing the ARPDIR
# anywhere
if grep -FrnI '/usr/local/arpwatch' .
then
  echo 'Missed fixing ARPDIR in at least one file' 1>&2
  exit 1
fi

# Verify we did not miss any PATH alterations in
# arpwatch-no-usr-local-path.patch.
if grep -ErnI --exclude=mkdep --exclude='config.*' '^[^#].*/usr/local/s?bin' .
then
  echo 'Probably missed an uncommented PATH alteration with /usr/local' 1>&2
  exit 1
fi


%post
%systemd_post arpwatch.service

%pre
%sysusers_create_compat %{SOURCE6}

%postun
%systemd_postun_with_restart arpwatch.service

%preun
%systemd_preun arpwatch.service

%files
%license LICENSE
%doc README
%doc CHANGES
%doc arpfetch

%{_sbindir}/arpwatch
%{_sbindir}/arpsnmp
# manually-installed scripts
%{_sbindir}/arp2ethers
%{_sbindir}/massagevendor

%dir %{_datadir}/arpwatch
%{_datadir}/arpwatch/*.awk

# make install uses mode 0444, which is unconventional
%attr(0644,-,-) %{_mandir}/man8/*.8*

%{_unitdir}/arpwatch.service
%{_sysusersdir}/arpwatch.conf
%config(noreplace) %{_sysconfdir}/sysconfig/arpwatch

%attr(1775,-,arpwatch) %dir %{pkgstatedir}
%attr(0644,arpwatch,arpwatch) %verify(not md5 size mtime) %config(noreplace) %{pkgstatedir}/arp.dat
%attr(0644,arpwatch,arpwatch) %verify(not md5 size mtime) %config(noreplace) %{pkgstatedir}/arp.dat-
%attr(0600,arpwatch,arpwatch) %verify(not md5 size mtime) %ghost %{pkgstatedir}/arp.dat.new
%attr(0644,-,arpwatch) %verify(not md5 size mtime) %config(noreplace) %{pkgstatedir}/ethercodes.dat

%changelog
* Fri Mar 14 2025 Akhila Guruju <v-guakhila@microsoft.com> - 14:3.7-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Wed Dec 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-9
- Add a SourceLicense field

* Wed Dec 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-8
- Generate ethercodes.dat from latest oui.csv

* Tue Nov 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-7
- Generate ethercodes.dat from latest oui.csv

* Tue Nov 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-6
- Invoke autoreconf and configure in %%conf rather than in %%build

* Tue Nov 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-5
- By default, re-generate the configure script

* Tue Nov 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-4
- Fix arpwatch/arpsnmp permissions in %%install, not in %%files
- Works around an issue extracting debuginfo

* Thu Oct 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-3
- Fix a trivial typo in the spec file

* Thu Oct 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-2
- Generate ethercodes.dat from latest oui.csv

* Fri Oct 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.7-1
- Update to 3.7 (close RHBZ#2316380)

* Sat Sep 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.6-8
- Generate ethercodes.dat from latest oui.csv

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.6-6
- Generate ethercodes.dat from latest oui.csv

* Fri May 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.6-5
- Generate ethercodes.dat from latest oui.csv

* Thu Mar 28 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.6-4
- Generate ethercodes.dat from latest oui.csv

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.6-1
- Update to 3.6 (close RHBZ#2259459)

* Mon Jan 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.5-5
- Generate ethercodes.dat from latest oui.csv

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.5-3
- Generate ethercodes.dat from latest oui.csv

* Mon Dec 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.5-2
- Switch to dynamically-allocated service user/group ID’s

* Mon Dec 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.5-1
- Update to 3.5 (close RHBZ#2252673)

* Mon Dec 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.4-4
- Generate ethercodes.dat from latest oui.csv

* Fri Nov 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.4-3
- Generate ethercodes.dat from latest oui.csv

* Wed Oct 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.4-2
- Generate ethercodes.dat from latest oui.csv

* Wed Sep 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.4-1
- Update to 3.4 (close RHBZ#2237532)

* Wed Sep 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-21
- Generate ethercodes.dat from latest oui.csv

* Wed Sep 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-20
- Generate ethercodes.dat from latest oui.csv

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-18
- Generate ethercodes.dat from latest oui.csv

* Wed May 24 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-17
- Generate ethercodes.dat from latest oui.csv

* Tue Apr 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-16
- Generate ethercodes.dat from latest oui.csv

* Sun Mar 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-15
- Generate ethercodes.dat from latest oui.csv

* Wed Feb 15 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-14
- Generate ethercodes.dat from latest oui.csv

* Wed Feb 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-13
- C99 compatibility patch (fix RHBZ#2166336)

* Wed Feb 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-12
- Stop numbering patches

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-10
- Generate ethercodes.dat from latest oui.csv

* Mon Dec 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-9
- Generate ethercodes.dat from latest oui.csv

* Mon Dec 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-8
- Leaf package: remove i686 support

* Wed Aug 03 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-7
- Generate ethercodes.dat from latest oui.csv

* Mon Aug 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-6
- Update License field to SPDX
- Additionally, the license is corrected; it should have been “BSD” rather
  than “BSD with advertising” under the old system.

* Sun Jul 31 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-5
- Generate ethercodes.dat from latest oui.csv

* Sun Jul 31 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-4
- Extract a LICENSE file from arpwatch.c’s comment header

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-2
- Generate ethercodes.dat from latest oui.csv

* Mon Mar 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.3-1
- Update to 3.3 (close RHBZ#2068925)

* Mon Mar 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.2-7
- Generate ethercodes.dat from latest oui.csv

* Thu Mar 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.2-6
- Generate ethercodes.dat from latest oui.csv

* Thu Mar 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.2-5
- Switch OUI URL from HTTP to HTTPS

* Mon Feb 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.2-4
- Allow fsync in systemd sandbox (fix RHBZ#2051521)

* Tue Feb 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.2-3
- Generate ethercodes.dat from latest oui.csv

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.2-1
- Update to 3.2 (close RHBZ#2033095)

* Thu Dec 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-38
- Generate ethercodes.dat from latest oui.csv

* Thu Dec 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-37
- Do not use path macros in file dependencies

* Thu Dec 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-36
- Generate ethercodes.dat from latest oui.csv

* Sun Dec 05 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-35
- Generate ethercodes.dat from latest oui.csv

* Mon Nov 15 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-34
- Allow timer syscalls in systemd sandboxing (fix RHBZ#2023139)

* Mon Nov 15 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-33
- Generate ethercodes.dat from latest oui.csv

* Thu Nov 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-32
- Generate ethercodes.dat from latest oui.csv

* Thu Nov 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-31
- Trivial spec file reformatting

* Thu Nov 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-30
- Change BR on python3 to python3-devel

* Thu Nov 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-29
- Reduce macro indirection in the spec file

* Mon Oct 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-28
- Use %%%%python3 macro instead of %%%%__python3

* Thu Sep 30 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-27
- Generate ethercodes.dat from latest oui.csv

* Sun Aug 01 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-26
- Add “Wants=network-online.target” to systemd unit file (fixes
  RHBZ#1988849)

* Sun Aug 01 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-25
- Generate ethercodes.dat from latest oui.csv

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-22
- Generate ethercodes.dat from latest oui.csv

* Fri Jul 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-14
- generate ethercodes.dat from latest oui.csv

* Mon May 03 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-13
- Fix systemd sandboxing syntax in unit file
- generate ethercodes.dat from latest oui.csv

* Sat Apr 24 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-12
- Fix an error in arpwatch-devlookup.patch that could cause a null pointer
  dereference on startup. Implements the suggestion of PR#1, “Update
  arpwatch-devlookup.patch to correctly open a named interface”.
- generate ethercodes.dat from latest oui.csv

* Tue Apr 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-11
- Do not use %%exclude for unpackaged files (RPM 4.17 compatibility)
- generate ethercodes.dat from latest oui.csv

* Mon Mar 29 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-10
- generate ethercodes.dat from latest oui.csv

* Wed Mar 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-9
- generate ethercodes.dat from latest oui.csv

* Tue Mar 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-8
- generate ethercodes.dat from latest oui.csv

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 14:3.1-7
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Sun Jan 31 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-6
- generate ethercodes.dat from latest oui.csv

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14:3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-4
- Fix changelog date

* Sat Jan  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-3
- Generate ethercodes.dat from latest oui.csv
- Change systemd BR to systemd-rpm-macros
- Drop Requires on systemd for scriptlets per current guidelines

* Wed Dec 16 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-2
- Add BR on make for
  https://fedoraproject.org/wiki/Changes/Remove_make_from_BuildRoot
- generate ethercodes.dat from latest oui.csv

* Wed Nov 11 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 14:3.1-1
- new upstream version 3.1
- generate ethercodes.dat from latest oui.csv
- improve systemd unit file, including hardening
- add sysconfig (environment) file
- drop arpwatch-2.1a4-fhs.patch: version 3.1 no longer attempts to set
  user/group for installed binaries, and permissions for binaries and man pages
  are now adjusted in the files section of the spec file
- rebase arpwatch-2.1a10-man.patch against version 3.1 as
  arpwatch-man-references.patch, fixing some additional cross-references
- rebase against version 3.1 and combine arpwatch-drop.patch, which provided
  -u; arpwatch-drop-man.patch, which documented it; and
  arpwatch-2.1a15-dropgroup.patch, which fixed CVE-2012-2653 (RHBZ #825328) in
  the original arpwatch-drop.patch, into a single combined
  arpwatch-change-user.patch; remove an unnecessary and unchecked strdup() in
  the original patch that could have theoretically led to a null pointer
  dereference
- drop arpwatch-addr.patch; the -e and -s arguments are now present in upstream
  version 3.1 as -w and -W, respectively
- replace arpwatch-dir-man.patch with a sed invocation
- replace arpwatch-2.1a15-extraman.patch with additional source files
  arp2ethers.8 and massagevendor.8; reformat the contents to match the upstream
  arpwatch.8 and arpsnmp.8 man pages; remove references to Debian; and rewrite
  massagevendor.8 to match the new Python-based massagevendor script
- split arpwatch-scripts.patch into arpwatch-arp2ethers-sort-invocation.patch,
  arpwatch-arpfetch-stray-rm.patch, and arpwatch-no-usr-local-path.patch,
  removing some additional PATH alterations in the last
- rebase arpwatch-2.1a15-nolocalpcap.patch against the version 3.1 configure script
  and rename it as arpwatch-configure-no-local-pcap.patch
- rebase arpwatch-2.1a15-bogon.patch against version 3.1 and rename it as
  arpwatch-all-zero-bogon.patch
- rebase arpwatch-exitcode.patch against version 3.1
- rewrite, combine, and simplify arpwatch-2.1a15-devlookup.patch and
  arpwatch-2.1a15-lookupiselect.patch, which fixed RHBZ #842660, as
  arpwatch-devlookup.patch; upstream version 3.1 will now try the first
  interface when -i is not given, but we still need a patch to search for
  another usable interface if the first one is not usable; additionally, the
  patch now handles the case where a device provides both supported and
  unsupported datalink types.
- drop arpwatch-201301-ethcodes.patch; upstream no longer distributes
  ethercodes.dat anyway, and we are generating it from oui.csv
- drop arpwatch-pie.patch; we are passing in hardened CFLAGS/LDFLAGS the normal
  way
- drop arpwatch-aarch64.patch, as upstream now has a more up-to-date
  config.guess
- drop arpwatch-promisc.patch; the -p flag is now upstream
- drop arpwatch-2.1a15-buffer-overflow-bz1563939.patch, which was a backport
  from this version

* Sat Oct 31 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 14:2.1a15-52
- add rpmlintrc file to suppress expected rpmlint errors

* Sat Oct 31 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 14:2.1a15-51
- touch ghost file arp.dat.new (ghost files should exist in the buildroot)

* Sat Oct 31 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 14:2.1a15-50
- use autosetup macro to apply patches

* Fri Oct 30 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 14:2.1a15-49
- drop explicit _hardened_build macro (default in all current Fedora releases)
- replace _vararpwatch macro with pkgstatedir, and define in terms of
  _sharedstatedir instead of _localstatedir
- use buildroot macro instead of RPM_BUILD_ROOT variable
- use package name macro more widely
- create macros for unprivileged service user and group names
- adjust whitespace throughout the spec file
- update URLs
- remove unnecessary BR on systemd
- use make_build and make_install macros; as a consequence, we now preserve
  timestamps when installing files (install -p)
- since we do not package the massagevendor-old script, do not prep it with the
  others
- instead of embedding awk scripts in the shell scripts that use them, install
  the awk scripts and use their absolute paths in the shell scripts; drop BR on
  perl, which was used to quote the awk scripts
- tidy up manual install steps
- remove user/group renaming code from pre-install script, and replace it with
  the suggested implementation for soft static allocation from
  https://fedoraproject.org/wiki/Packaging:UsersAndGroups;
  the pcap user and group were renamed to arpwatch in 2007
  (https://src.fedoraproject.org/rpms/arpwatch/c/f1b7b51), and we have no need
  to handle such ancient installations anymore

* Tue Oct 27 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 14:2.1a15-48
- fix arpwatch buffer overflow (#1563939)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar  5 2018 Jan Synáček <jsynacek@redhat.com> - 14:2.1a15-42
- make sure arpwatch starts after network devices are up (#1551431)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 20 2017 Jan Synáček <jsynacek@redhat.com> - 14:2.1a15-38
- fix FTBFS (#1423238)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 14:2.1a15-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Jan Synáček <jsynacek@redhat.com> - 14:2.1a15-35
- fix arpwatch buffer overflow (#1301880)
- add -p option that disables promiscuous mode (#1301853)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb  3 2014 Jan Synáček <jsynacek@redhat.com> 14:2.1a15-31
- reference documentation in the service file
- remove redundant sysconfig-related stuff

* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 14:2.1a15-30
- Fix FTBFS

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Jan Synáček <jsynacek@redhat.com> 14:2.1a15-28
- harden the package (#954336)
- support aarch64 (#925027)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Ales Ledvinka <aledvink@redhat.com> - 14:2.1a15-26
- fix permissions related to collected database
- update ethcodes defaults to current public IEEE OUI-32

* Mon Oct 15 2012 Ales Ledvinka <aledvink@redhat.com> - 14:2.1a15-25
- fix -i with invalid interface specified (#842660)

* Mon Oct 15 2012 Ales Ledvinka <aledvink@redhat.com> - 14:2.1a15-24
- fix devlookup to start with -i interface specified (#842660)

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 14:2.1a15-23
- Add system-rpm macros (#850032)

* Tue Jul 24 2012 Jan Synáček <jsynacek@redhat.com> - 14:2.1a15-22
- add devlookup patch: search for suitable default interface, if -i is not
  specified (#842660)

* Thu Jul 19 2012 Jan Synáček <jsynacek@redhat.com> - 14:2.1a15-21
- make spec slightly more fedora-review-friendly

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 31 2012 Aleš Ledvinka <aledvink@redhat.com> 14:2.1a15-20
- fix supplementary group list (#825328) (CVE-2012-2653)

* Thu Jan 19 2012 Jan Synáček <jsynacek@redhat.com> 14:2.1a15-19
- Turn on PrivateTmp=true in service file (#782477)

* Thu Jan 05 2012 Jan Synáček <jsynacek@redhat.com> 14:2.1a15-18
- Rebuilt for GCC 4.7

* Fri Jul 08 2011 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-17
- exit with zero error code (#699285)
- change service type to forking (#699285)

* Thu Jul 07 2011 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-16
- replace SysV init script with systemd service (#699285)
- update ethercodes.dat

* Mon Mar 28 2011 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-15
- update ethercodes.dat (#690948)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 30 2010 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-13
- update ethercodes.dat (#577552)
- mark ethercodes.dat as noreplace
- fix init script LSB compliance
- include Debian arp2ethers and massagevendor man pages (#526160)
- don't include massagevendor-old script anymore

* Wed Sep 02 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-12
- update ethercodes.dat

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:2.1a15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 16 2008 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-9
- update ethercodes.dat (#462364)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 14:2.1a15-8
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-7
- rebuild

* Thu Aug 09 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-6
- improve init script (#246869)
- allow -n 0/32 to disable reporting bogons from 0.0.0.0 (#244606)
- update license tag
- update ethercodes.dat

* Wed Jun 13 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-5
- update ethercodes.dat

* Thu May 24 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-4
- fix return codes in init script (#237781)

* Mon Jan 15 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-3
- rename pcap user to arpwatch

* Tue Nov 28 2006 Miroslav Lichvar <mlichvar@redhat.com> 14:2.1a15-2
- split from tcpdump package (#193657)
- update to 2.1a15
- clean up files in /var
- force linking with system libpcap

