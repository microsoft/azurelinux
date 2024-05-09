Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:	Command line tool that displays bandwidth usage on an interface
Name:		iftop
Version:	1.0
Release:	1%{?dist}
License:	GPLv2+
URL:		https://www.ex-parrot.com/~pdw/%{name}/
Source:		https://www.ex-parrot.com/~pdw/%{name}/download/%{name}-%{version}pre4.tar.gz
Patch0:		iftop-1.0-ncursesw.patch
Patch1:		iftop-1.0-git20181003.patch
Patch2:		iftop-1.0-gcc10.patch
BuildRequires:	gcc, ncurses-devel, libpcap-devel

%description
iftop does for network usage what top(1) does for CPU usage. It listens to
network traffic on a named interface and displays a table of current bandwidth
usage by pairs of hosts. Handy for answering the question "why is our ADSL link
so slow?".

%prep
%setup -q -n %{name}-%{version}pre4
%patch 0 -p1 -b .ncursesw
touch -c -r configure.ac{.ncursesw,}
%patch 1 -p1 -b .git20181003
%patch 2 -p1 -b .gcc10

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%doc ChangeLog README TODO
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-1
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Sep 24 2021 Muhammad Falak <mwani@microsoft.com.> 1.0-0.24.pre4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Feb 02 2020 Robert Scheck <robert@fedoraproject.org> 1.0-0.23.pre4
- Added patch to declare variables as extern in header files

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.22.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Robert Scheck <robert@fedoraproject.org> 1.0-0.21.pre4
- Added patch from upstream to choose first "running" interface,
  rather than first "up" interface (#1403025)
- Added patch from upstream to support scales beyond 1 Gbps

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.20.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.19.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.18.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.17.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.16.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.15.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Robert Scheck <robert@fedoraproject.org> 1.0-0.14.pre4
- Added patch from upstream to fix DNS resolution (#1120254, #1309755)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.13.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Robert Scheck <robert@fedoraproject.org> 1.0-0.12.pre4
- Added patch to fix broken MAC address output (#1063298, #1165349)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.11.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.10.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.9.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Robert Scheck <robert@fedoraproject.org> 1.0-0.7.pre4
- Update to 1.0pre4 (#1047679, #1055277)

* Thu Dec 19 2013 Robert Scheck <robert@fedoraproject.org> 1.0-0.6.pre2
- Added patch to fix a memory leak in resolver.c (#782275, #861582)
- Run autoreconf to recognize aarch64 (#925579)
- Added patch to fix needlessly caused assertion failure when using
  nss-myhostname (#839750, #847124, #868065, #961236, #1007434)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.5.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.4.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.2.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011 Robert Scheck <robert@fedoraproject.org> 1.0-0.1.pre2
- Update to 1.0pre2 (#661448, #743535)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Robert Scheck <robert@fedoraproject.org> 0.17-12
- Updated man page patch to correct some further man page typos
- Added two patches to avoid two crashes on arm architectures
- Added patch to fix drives line going crazy if order is frozen
- Added a patch to turns off the bar display using -b option
- Fixed a segfault when using same argument repeatedly (#654343)
- Added patch from Mats Erik Andersson to add IPv6 support
- Added patch to use better hash algorithm in address pairs

* Sat Jul 10 2010 Robert Scheck <robert@fedoraproject.org> 0.17-11
- Corrected the wrong synopsis for -F/-N parameter (#601087 #c3)
- Added patch to avoid pointer with free(ed) memory (#601087 #c2)

* Thu Apr 01 2010 Robert Scheck <robert@fedoraproject.org> 0.17-10
- Link against ncursesw for lines with UTF-8 and PuTTY (#546032)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.17-8
- Rebuild against gcc 4.4 and rpm 4.6

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 0.17-7
- Rebuild against gcc 4.3

* Tue Aug 28 2007 Robert Scheck <robert@fedoraproject.org> 0.17-6
- Buildrequire %%{_includedir}/pcap.h instead of conditionals
- Patch to display top scale in bytes when measuring in bytes

* Sat Aug 25 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.17-5
- fix license tag
- rebuild for BuildID

* Wed Nov 29 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.17-4
- rebuild

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.17-3
- rebuild

* Thu Jun 15 2006 Aurelien Bompard <gauret[AT]free.fr> 0.17-2
- buildrequire libpcap-devel from FC6 on

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.17-1
- version 0.17

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.16-7
- rebuild for fc5

* Sun Nov 13 2005 Aurelien Bompard <gauret[AT]free.fr> 0.16-6
- rebuild for libpcap

* Sat Oct 22 2005 Aurelien Bompard <gauret[AT]free.fr> 0.16-5
- rebuild and add disttag

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Jun 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.16-0.fdr.3
- use make install

* Thu Jun 03 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.16-0.fdr.2
- remove useless BuildRequires: texinfo

* Sat May 22 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.16-0.fdr.1
- Initial RPM release.
