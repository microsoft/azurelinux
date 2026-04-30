## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: nmap
Epoch: 4
Version: 7.92
#global prerelease TEST5
Release: %autorelease
Summary: Network exploration tool and security scanner
URL: http://nmap.org/
# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/thread/Q67UGCHSCKCLJOVOHSLYU4AERAHBS5YE/
# https://gitlab.com/fedora/legal/fedora-license-data/-/issues/543
License: LicenseRef-Nmap

Source0: http://nmap.org/dist/%{name}-%{version}%{?prerelease}.tar.bz2
Source1: https://nmap.org/dist/sigs/%{name}-%{version}.tar.bz2.asc
Source2: https://svn.nmap.org/nmap/docs/nmap_gpgkeys.txt

#prevent possible race condition for shtool, rhbz#158996
Patch1: nmap-4.03-mktemp.patch
#don't suggest to scan microsoft
Patch2: nmap-4.52-noms.patch
# upstream provided patch for rhbz#845005, not yet in upstream repository
Patch3: ncat_reg_stdin.diff
# TODO: review after GUI gets enabled again
#Patch4: nmap-6.25-displayerror.patch
# https://github.com/nmap/nmap/pull/2247
Patch7: nmap_resolve_config.patch
# backport of upstream pcre2 migration, rhbz#2128336
Patch8: nmap-pcre2.patch
# https://github.com/nmap/nmap/pull/2724
Patch9: nmap-ems-ssl-enum-ciphers.patch
# Fix build with libpcap 1.10.5
Patch10: nmap-libpcap.patch

BuildRequires: automake make
BuildRequires: autoconf
BuildRequires: gcc-c++
BuildRequires: gettext-devel
BuildRequires: libpcap-devel
%if 0%{?fedora} 
BuildRequires: libssh2-devel
%endif
BuildRequires: libtool
BuildRequires: lua-devel
BuildRequires: openssl-devel
BuildRequires: pcre2-devel
BuildRequires: zlib-devel
BuildRequires: gnupg2
Requires: %{name}-ncat = %{epoch}:%{version}-%{release}

Obsoletes: nmap-frontend < 7.70-1
Obsoletes: nmap-ndiff < 7.70-1

%define pixmap_srcdir zenmap/share/pixmaps

%description
Nmap is a utility for network exploration or security auditing.  It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, reverse-identd scanning, and more. In addition
to the classic command-line nmap executable, the Nmap suite includes a flexible
data transfer, redirection, and debugging tool (netcat utility ncat), a utility
for comparing scan results (ndiff), and a packet generation and response
analysis tool (nping). 

%package ncat
Summary: Nmap's Netcat replacement
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
Obsoletes: nc < 1.109.20120711-2
Obsoletes: nc6 < 1.00-22
Provides: nc = %{epoch}:%{version}-%{release}
Provides: nc6 = %{epoch}:%{version}-%{release}
Provides: ncat = %{epoch}:%{version}-%{release}

%description ncat
Ncat is a feature packed networking utility which will read and
write data across a network from the command line.  It uses both
TCP and UDP for communication and is designed to be a reliable
back-end tool to instantly provide network connectivity to other
applications and users. Ncat will not only work with IPv4 and IPv6
but provides the user with a virtually limitless number of potential
uses.


%prep
%{gpgverify} --keyring=%{SOURCE2} --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
autoconf -f

#TODO: stop using local copy of libdnet, once system distributed version
#supports sctp (grep sctp /usr/include/dnet.h)
#be sure we're not using tarballed copies of some libraries
#rm -rf liblua libpcap libpcre macosx mswin32 ###TODO###
rm -rf libpcap libpcre macosx mswin32 libssh2 libz

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
### TODO ## configure  --with-libpcap=/usr ###TODO###
%configure  --with-libpcap=yes --with-liblua=included \
  --without-zenmap --without-ndiff \
%if 0%{?fedora} 
  --with-libssh2=yes  \
%else
  --with-libssh2=no  \
%endif
  --enable-dbus 

%make_build

#fix man page (rhbz#813734)
sed -i 's/-md/-mf/' nping/docs/nping.1

%install
#prevent stripping - replace strip command with 'true'
make DESTDIR=%{buildroot} STRIP=true install

#do not include certificate bundle (#734389)
rm -f %{buildroot}%{_datadir}/ncat/ca-bundle.crt
rmdir %{buildroot}%{_datadir}/ncat

#we provide 'nc' replacement (#1653119)
touch %{buildroot}%{_mandir}/man1/nc.1.gz
touch %{buildroot}%{_bindir}/nc

%find_lang nmap --with-man

%post ncat
%{_sbindir}/alternatives --install %{_bindir}/nc nc %{_bindir}/ncat 10 \
  --slave %{_mandir}/man1/nc.1.gz nc-man %{_mandir}/man1/ncat.1.gz

%preun ncat
if [ $1 -eq 0 ]; then
  %{_sbindir}/alternatives --remove nc %{_bindir}/ncat
fi

%files -f nmap.lang
%license LICENSE
%doc docs/README
%doc docs/nmap.usage.txt
%{_bindir}/nmap
%{_bindir}/nping
%{_mandir}/man1/nmap.1.gz
%{_mandir}/man1/nping.1.gz
%{_datadir}/nmap

%files ncat 
%license LICENSE
%doc ncat/docs/AUTHORS ncat/docs/README ncat/docs/THANKS ncat/docs/examples
%ghost %{_bindir}/nc
%{_bindir}/ncat
%ghost %{_mandir}/man1/nc.1.gz
%{_mandir}/man1/ncat.1.gz

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 4:7.92-8
- test: add initial lock files

* Wed Aug 13 2025 František Hrdina <fhrdina@redhat.com> - 4:7.92-7
- Update of fmf plans

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:7.92-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:7.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 03 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 4:7.92-4
- Fix build with libpcap-1.10.5

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:7.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Martin Osvald <mosvald@redhat.com> - 4:7.92-2
- Support EMS in ssl-enum-ciphers

* Wed Jul 10 2024 Martin Osvald <mosvald@redhat.com> - 4:7.92-1
- Downgrade Nmap to 7.92 to fix NPSL license issue (rhbz#2296006)

* Tue Apr 23 2024 Martin Osvald <mosvald@redhat.com> - 3:7.95-1
- New version 7.95 (rhbz#2276542)

* Tue Feb 27 2024 Martin Osvald <mosvald@redhat.com> - 3:7.94-1
- New version 7.94 (rhbz#2208804)
- Provide ncat in nmap-ncat for convenience (rhbz#2214073)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.93-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.93-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 17 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3:7.93-4
- Use pcre2 instead of deprecated pcre (rhbz#2128336)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 02 2022 Martin Osvald <mosvald@redhat.com> - 3:7.93-1
- New version 7.93 (rhbz#2123556)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 10 2022 Martin Osvald <mosvald@redhat.com> - 3:7.92-4
- Reverting the last change as it would do more harm than good

* Thu May 05 2022 Martin Osvald <mosvald@redhat.com> - 3:7.92-3
- ncat: close on EOF by default, new --no-terminate option
  for backward compatibility (#2082270)

* Tue Feb 22 2022 Martin Osvald <mosvald@redhat.com> - 3:7.92-1
- New version 7.92

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.91-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3:7.91-9
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May  5 2021 Pavel Zhukov <pzhukov@redhat.com> - 3:7.91-7
- Fix crash with unix sockets

* Fri Apr 16 2021 Pavel Zhukov <pzhukov@redhat.com> - 3:7.91-6
- Bumping release because brew doesn't work with Epoch

* Thu Apr  8 2021 Pavel Zhukov <pzhukov@redhat.com> - 3:7.91-1
- Bring 7.91 back

* Sun Mar 07 2021 Robert Scheck <robert@fedoraproject.org> - 3:7.80-11
- Manage nc symlink using alternatives (#1653119)

* Wed Feb 10 2021 Pavel Zhukov  <pzhukov@redhat.com> - 3:7.80-10
- Do not listen on ipv6 if it's disabled

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:7.80-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Pavel Zhukov  <pzhukov@redhat.com> - 3:7.80-8
- Replace FD_ functions with safe implementation (#1914734)

* Sun Jan 10 2021 Pavel Zhukov <pzhukov@redhat.com> - 3:7.80-7
- Drop nmap >= 7.90

* Thu Aug 20 2020 Pavel Zhukov <pzhukov@redhat.com> - 2:7.80-6
- Drop libssh from eln

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 19 2020 Pavel Zhukov <pzhukov@redhat.com> - 2:7.80-4
- Do not assert on unsolicited ARP response (#1836989)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2:7.80-2
- Re-provide nc, clearly 7 years isn't enough

* Mon Aug 12 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2:7.80-1
- Update to 7.80
- Drop features conditionals from old releases
- Use %%license, package cleanups

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May  2 2019  Pavel Zhukov <pzhukov@redhat.com> - 2:7.70-7
- Fix double free when ssh connections fails

* Tue Feb  5 2019 Pavel Zhukov <pzhukov@redhat.com> - 2:7.70-6
- Fix ipv6 literals parsing in proxy connection

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 10 2018 Pavel Zhukov <pzhukov@redhat.com> - 2:7.70-4
- Obsolete frontend packages in f29+ (#1626804)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Pavel Zhukov <pzhukov@redhat.com> - 2:7.70-2
- Do not build zenmap and ndiff because of python2 deprecation

* Wed Mar 21 2018 Pavel Zhukov <pzhukov@redhat.com> - 2:7.70-1
- New version 7.70 (#1558770)

* Tue Feb 27 2018 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-14
- Add appdata file (#1476506)

* Mon Feb 19 2018 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-12
- add gcc-c++ BR

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.60-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-10
- Print source address in UDP mode

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:7.60-9
- Remove obsolete scriptlets

* Mon Aug 21 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-8
- Fix memory leaks on error

* Thu Aug  3 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-7
- Use upstream patch

* Thu Aug  3 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-6
- Fix library version for non-included libraries

* Thu Aug  3 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-4
- Keep nmap specific libssh and libz headers
- Drop unused libssh2 patch

* Thu Aug  3 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-4
- Delete bundled libssh2
- Delete bundled zlib

* Wed Aug 02 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.60-1
- New release 7.60 (#1477387)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.50-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.50-9
- Don't ship ndiff in nmap package

* Wed Jul 19 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.50-8
- change ndiff arch to noarch
- Move nmap to Requires (was in BR)

* Tue Jul 18 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.50-6
- Add missed py[co] files

* Tue Jul 18 2017 Pavel Zhukov <pzhukov@redhat.com> - 2:7.50-5
- Move ndiff to subpackage (#1471999)
- Specify python version

* Fri Jun 30 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 2:7.50-3
- Add provides for nc6 (#1348348)
- Fix rpmlint errors

* Wed Jun 21 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 2:7.50-1
- New release (7.50)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Michal Hlavinka <mhlavink@redhat.com> - 2:7.40-1
- nmap updated to 7.40

* Mon Oct 24 2016 Michal Hlavinka <mhlavink@redhat.com> - 2:7.31-1
- nmap updated to 7.31

* Mon Oct 03 2016 Michal Hlavinka <mhlavink@redhat.com> - 2:7.30-1
- nmap updated to 7.30

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.12-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 31 2016 Michal Hlavinka <mhlavink@redhat.com> - 2:7.12-1
- nmap updated to 7.12

* Wed Mar 23 2016 Michal Hlavinka <mhlavink@redhat.com> - 2:7.11-1
- nmap updated to 7.11

* Fri Mar 18 2016 Michal Hlavinka <mhlavink@redhat.com> - 2:7.10-1
- nmap updated to 7.10

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Michal Hlavinka <mhlavink@redhat.com> - 2:7.01-1
- nmap updated to 7.01

* Tue Sep 01 2015 Michal Hlavinka <mhlavink@redhat.com> - 2:6.47-5
- fix FTBFS

* Mon Aug 31 2015 Michal Hlavinka <mhlavink@redhat.com> - 2:6.47-4
- ncat should try to connect to all resolved addresses, not only the first one (#978964)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:6.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 Michal Hlavinka <mhlavink@redhat.com> - 2:6.47-2
- do not own icons/hicolor/<size>/apps directory (#1171813)

* Mon Aug 25 2014 Michal Hlavinka <mhlavink@redhat.com> - 2:6.47-1
- nmap updated to 6.47

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:6.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:6.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Michal Hlavinka <mhlavink@redhat.com> - 2:6.46-1
- nmap updated to 6.46

* Mon Apr 14 2014 Michal Hlavinka <mhlavink@redhat.com> - 2:6.45-1
- nmap updated to 6.45

* Wed Apr 09 2014 Michal Hlavinka <mhlavink@redhat.com> - 2:6.40-6
- fix unexpected crash when too much paralelism is used (#1057912)

* Wed Apr 09 2014 Michal Hlavinka <mhlavink@redhat.com> - 2:6.40-5
- update license tag (#1055861)

* Tue Mar 04 2014 Michal Hlavinka <mhlavink@redhat.com> - 2:6.40-4
- use _hardened_build

* Thu Oct 17 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.40-3
- ncat should support UNIX sockets correctly, drop wrapper with socat

* Thu Aug 08 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.40-2
- do not print debug messages during normal use (#994376)

* Tue Jul 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.40-1
- nmap updated to 6.40

* Mon Jul 22 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.25-7
- bundled lua no longer required

* Mon Jun 24 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.25-6.20130624svn
- use svn snapshot that contains all necessary UDP patches

* Fri May 24 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.25-5
- fix man page typo

* Thu May 23 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.25-4
- zenamp: fix icon symlink (#957381)

* Thu May 23 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.25-3
- zenmap: do not traceback when there si no display, just exit nicely (#958240)

* Thu Mar 28 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.25-2
- fix aarch64 support (#926241)

* Fri Mar 08 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.25-1
- nmap updated to 6.25

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:6.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-10
- use select as default nsock engine

* Thu Nov 29 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-9
- do not use strict aliasing

* Thu Nov 29 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-8
- call shutdown also in listen mode

* Tue Oct 02 2012 Petr Šabata <contyk@redhat.com> - 2:6.01-7
- Move the socat dependency to the ncat subpackage (#858733)

* Wed Sep 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-6
- shutdown socket on EOF (#845075)

* Mon Aug 13 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-5
- ncat did not work when file was used as input (#845005)

* Tue Jul 24 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-4
- add nc wrapper with socat as a fallback for unix sockets

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:6.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-2
- provide ncat in extra package as replacement for nc

* Mon Jun 18 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.01-1
- nmap updated to 6.01

* Tue Jun 05 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.00-2
- prevent stripping binaries

* Tue Jun 05 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:6.00-1
- updated to 6.00

* Wed Mar 14 2012 Michal Hlavinka <mhlavink@redhat.com> - 2:5.61-0.1.TEST5
- updated to 5.61TEST5

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2:5.51-5
- Rebuild against PCRE 8.30

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2:5.51-4
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:5.51-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Michal Hlavinka <mhlavink@redhat.com> - 2:5.51-2
- do not use bundled certificates, use only system ones (#734389)

* Mon Feb 14 2011 Michal Hlavinka <mhlavink@redhat.com> - 2:5.51-1
- nmap updated to 5.51

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:5.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 2:5.50-1
- updated to 5.50

* Tue Oct 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.21-10
- add workaround for zenmap crash (#637403)

* Wed Sep 29 2010 jkeating - 2:5.21-9
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.21-8
- fix location of ja man page (#632104)

* Thu Aug 19 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.21-7
- update icon cache only after gui install

* Wed Aug 11 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.21-6
- update icon cache after package install

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2:5.21-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 21 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.21-4
- build -frontend as noarch

* Fri Jun 18 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.21-3
- fix multilib issue

* Fri Apr 30 2010 Ville Skyttä <ville.skytta@iki.fi> - 2:5.21-2
- Mark localized man pages with %%lang.

* Mon Feb 01 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.21-1
- updated to 5.21

* Tue Jan 12 2010 Michal Hlavinka <mhlavink@redhat.com> - 2:5.00-6
- use sqlite3 (instead of sqlite2)

* Tue Dec 01 2009 Michal Hlavinka <mhlavink@redhat.com> - 2:5.00-5
- spec cleanup

* Mon Nov 02 2009 Michal Hlavinka <mhlavink@redhat.com> - 2:5.00-4
- spec cleanup

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2:5.00-3
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:5.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Michal Hlavinka <mhlavink@redhat.com> - 2:5.0-1
- updated to 5.0

* Wed Jul 15 2009 Michal Hlavinka <mhlavink@redhat.com> - 2:4.90-0.RC1
- updated to 4.90RC1

* Thu Jun 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 2:4.85-0.BETA10
- updated to 4.85beta10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:4.76-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2:4.76-3
- rebuild with new openssl

* Mon Dec 15 2008 Michal Hlavinka <mhlavink@redhat.com> - 2:4.77-2
- bump release for rebuild

* Mon Dec 15 2008 Michal Hlavinka <mhlavink@redhat.com> - 2:4.76-1
- new upstream version 4.76
- use consolehelper for root auth

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2:4.68-4
- Rebuild for Python 2.6

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:4.68-3
- add missing BuildRequires to use system libs rather than local copies
- really fix license tag

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:4.68-2
- fix license tag

* Thu Jul 24 2008 Tomas Smetana <tsmetana@redhat.com> - 2:4.68-1
- new upstream version

* Mon May 12 2008 Tomas Smetana <tsmetana@redhat.com> - 2:4.62-1
- new upstream version

* Mon Feb 04 2008 Tomas Smetana <tsmetana@redhat.com> - 2:4.53-1
- new upstream version

* Mon Jan 07 2008 Tomas Smetana <tsmetana@redhat.com> - 2:4.52-2
- bump release because of build error

* Mon Jan 07 2008 Tomas Smetana <tsmetana@redhat.com> - 2:4.52-1
- new upstream version

* Wed Dec 05 2007 Tomas Smetana <tsmetana@redhat.com> - 2:4.20-6.1
- rebuild

* Wed Aug 22 2007 Harald Hoyer <harald@redhat.com> - 2:4.20-6
- changed license tag

* Fri Mar 23 2007 Harald Hoyer <harald@redhat.com> - 2:4.20-5
- fixed changelog versions

* Thu Mar 15 2007 Karsten Hopp <karsten@redhat.com> 2:4.20-4
- rebuild with current gtk2 to add png support (#232013)

* Tue Feb 27 2007 Harald Hoyer <harald@redhat.com> - 2:4.20-3
- specfile cleanup
- fixed Florian La Roche's patch

* Tue Jan 30 2007 Florian La Roche <laroche@redhat.com> - 2:4.20-2
- do not strip away debuginfo

* Tue Jan 09 2007 Florian La Roche <laroche@redhat.com> - 2:4.20-1
- version 4.20

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:4.11-1.1
- rebuild

* Tue Jun 27 2006 Harald Hoyer <harald@redhat.com> - 2:4.11-1
- version 4.11

* Wed May 17 2006 Harald Hoyer <harald@redhat.de> 4.03-2
- added more build requirements (bug #191932)

* Wed May 10 2006 Karsten Hopp <karsten@redhat.de> 4.03-1
- update to 4.03, this fixes #184286
- remove duplicate menu entry in 'Internet' (#183056)
- fix possible tmpdir race condition during build (#158996)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:4.00-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:4.00-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Harald Hoyer <harald@redhat.com> - 2:4.00-1
- version 4.00

* Mon Dec 19 2005 Harald Hoyer <harald@redhat.com> - 2:3.95-1
- version 3.95

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Harald Hoyer <harald@redhat.com> - 2:3.93-3
- fixed wrong __attribute__ test

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> - 2:3.93-2
- rebuilt against new openssl

* Tue Sep 13 2005 Harald Hoyer <harald@redhat.com> - 2:3.93-1
- version 3.93

* Wed Aug 03 2005 Harald Hoyer <harald@redhat.com> - 2:3.81-4
- removed references how to scan microsoft.com (bz #164962)
- finally got rid of gtk+-devel dependency

* Thu Apr 21 2005 Harald Hoyer <harald@redhat.com> - 2:3.81-3
- removed gtk+ requirement

* Thu Apr 21 2005 Harald Hoyer <harald@redhat.com> - 2:3.81-2
- fixed desktop file and added icons (bug #149157)

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> - 2:3.81-1
- version 3.81

* Wed Feb 02 2005 Harald Hoyer <harald@redhat.com> - 2:3.78-2
- evil port of nmapfe to gtk2

* Fri Dec 17 2004 Harald Hoyer <harald@redhat.com> - 2:3.78-1
- version 3.78

* Mon Sep 13 2004 Harald Hoyer <harald@redhat.com> - 2:3.70-1
- version 3.70

* Tue Jul 13 2004 Harald Hoyer <harald@redhat.com> - 2:3.55-1
- new version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Harald Hoyer <harald@redhat.com> - 2:3.50-2
- added BuildRequires: openssl-devel, gtk+-devel, pcre-devel, libpcap

* Thu Jan 22 2004 Harald Hoyer <harald@redhat.com> - 2:3.50-1
- version 3.50

* Wed Oct  8 2003 Harald Hoyer <harald@redhat.de> 2:3.48-1
- version 3.48

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow disabling frontend if gtk1 is not available

* Wed Jul 30 2003 Harald Hoyer <harald@redhat.de> 2:3.30-1
- version 3.30

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 26 2003 Harald Hoyer <harald@redhat.de> 2:3.27-1
- version 3.27

* Mon May 12 2003 Harald Hoyer <harald@redhat.de> 2:3.20-2
- changed macro comments to double %% for changelog entries

* Mon Apr 14 2003 Harald Hoyer <harald@redhat.de> 2:3.20-1
- version 3.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Harald Hoyer <harald@redhat.de> 3.0-3
- nmap-3.00-nowarn.patch added

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches
- remove old desktop file from $$RPM_BUILD_ROOT so rpm won't complain

* Thu Aug  1 2002 Harald Hoyer <harald@redhat.de>
- version 3.0

* Mon Jul 29 2002 Harald Hoyer <harald@redhat.de> 2.99.2-1
- bumped version

* Fri Jul 26 2002 Harald Hoyer <harald@redhat.de> 2.99.1-2
- bumped version to 2.99RC1

* Fri Jul 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add an epoch

* Mon Jul  1 2002 Harald Hoyer <harald@redhat.de> 2.54.36-1
- removed desktop file
- removed "BETA" name from version
- update to BETA36

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Harald Hoyer <harald@redhat.de> 2.54BETA34-1
- update to 2.54BETA34

* Mon Mar 25 2002 Harald Hoyer <harald@redhat.com>
- more recent version (#61490)

* Mon Jul 23 2001 Harald Hoyer <harald@redhat.com>
- buildprereq for nmap-frontend (#49644)

* Sun Jul 22 2001 Heikki Korpela <heko@iki.fi>
- buildrequire gtk+

* Tue Jul 10 2001 Tim Powers <timp@redhat.com>
- fix bugs in desktop file (#48341)

* Wed May 16 2001 Tim Powers <timp@redhat.com>
- updated to 2.54BETA22

* Mon Nov 20 2000 Tim Powers <timp@redhat.com>
- rebuilt to fix bad dir perms

* Fri Nov  3 2000 Tim Powers <timp@redhat.com>
- fixed nmapdatadir in the install section, forgot lto include
  $RPM_BUILD_ROOT in the path

* Thu Nov  2 2000 Tim Powers <timp@redhat.com>
- update to nmap-2.54BETA7 to possibly fix bug #20199
- use the desktop file provided by the package instead of using my own
- patches in previous version are depreciated. Included in SRPM for
  reference only

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jun 28 2000 Tim Powers <timp@redhat.com>
- rebuilt package

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fixed man pages so that they are in an FHS compliant location
- use %%makeinstall
- use predefined RPM macros wherever possible

* Tue May 16 2000 Tim Powers <timp@redhat.com>
- updated to 2.53
- using applnk now
- use %%configure, and %%{_prefix} where possible
- removed redundant defines at top of spec file

* Mon Dec 13 1999 Tim Powers <timp@redhat.com>
- based on origional spec file from
    http://www.insecure.org/nmap/index.html#download
- general cleanups, removed lots of commenrts since it madethe spec hard to
    read
- changed group to Applications/System
- quiet setup
- no need to create dirs in the install section, "make
    prefix=$RPM_BUILD_ROOT&{prefix} install" does this.
- using defined %%{prefix}, %%{version} etc. for easier/quicker maint.
- added docs
- gzip man pages
- strip after files have been installed into buildroot
- created separate package for the frontend so that Gtk+ isn't needed for the
    CLI nmap
- not using -f in files section anymore, no need for it since there aren't that
    many files/dirs
- added desktop entry for gnome

* Sun Jan 10 1999 Fyodor <fyodor@dhp.com>
- Merged in spec file sent in by Ian Macdonald <ianmacd@xs4all.nl>

* Tue Dec 29 1998 Fyodor <fyodor@dhp.com>
- Made some changes, and merged in another .spec file sent in
  by Oren Tirosh <oren@hishome.net>

* Mon Dec 21 1998 Riku Meskanen <mesrik@cc.jyu.fi>
- initial build for RH 5.x

## END: Generated by rpmautospec
