Summary:        Utility to set/show the host name or domain name
Name:           hostname
Version:        3.23
Release:        8%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://packages.qa.debian.org/h/hostname.html
Source0:        https://ftp.de.debian.org/debian/pool/main/h/hostname/hostname_%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        gpl-2.0.txt
Source2:        nis-domainname
Source3:        nis-domainname.service
# NOTE: We are *not* requiring systemd on purpose, because we want to allow
#       hostname package to be installed in containers without the systemd.
# Initial changes
Patch1:         hostname-rh.patch
BuildRequires:  gcc
BuildRequires:  make

%description
This package provides commands which can be used to display the system's
DNS name, and to display or set its hostname or NIS domain name.

%prep
%setup -q -n hostname
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .
%patch 1 -p1

%build
make CFLAGS="%{optflags} $CFLAGS -D_GNU_SOURCE" LDFLAGS="$RPM_LD_FLAGS"

%install
make BASEDIR=%{buildroot} BINDIR=%{_bindir} install

install -m 0755 -d %{buildroot}%{_libexecdir}/%{name}
install -m 0755 -d %{buildroot}%{_libdir}/systemd/system
install -m 0755 nis-domainname         %{buildroot}%{_libexecdir}/%{name}
install -m 0644 nis-domainname.service %{buildroot}%{_libdir}/systemd/system

%post
if [ $1 -eq 1 ]; then
  # Initial installation...
  systemctl --no-reload preset nis-domainname.service &>/dev/null || :
fi

%preun
if [ $1 -eq 0 ]; then
  # Package removal, not upgrade...
  systemctl --no-reload disable --now nis-domainname.service &>/dev/null || :
fi

# NOTE: Nothing to do for upgrade (in postun), nis-domainname.service is oneshot.

%files
%doc COPYRIGHT
%license gpl-2.0.txt
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/systemd/system/*
%{_libexecdir}/%{name}

%changelog
* Tue Nov 01 2022 Riken Maharjan <rmaharjan@microsoft.com> - 3.23-8
- License verified
- Initial CBL-Mariner import from Fedora 37 (license: MIT).

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Pavel Zhukov <pzhukov@redhat.com> - 3.23-1
- New version 3.23 (#1771102)

* Fri Aug 30 2019 Pavel Zhukov <pzhukov@redhat.com> - 3.22-1
- New release v3.22 (#1747011)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr  3 2019 Pavel Zhukov <pzhukov@redhat.com> - 3.20-7
- Own whole libexec/hostname directory (#1695488)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 3.20-5
- nis-domainname.service moved here from initscripts package

* Wed Mar  7 2018 Pavel Zhukov <pzhukov@redhat.com> - 3.20-4
- Add gcc to BuildRequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 3.20-2
- Build with linker flags from redhat-rpm-config

* Thu Feb  1 2018 Pavel Zhukov <pzhukov@redhat.com> - 3.20-1
- New version 3.20

* Wed Jan 31 2018 Pavel Zhukov <landgraf@fedoraproject.org> - 3.19-2
- New version 3.19

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 10 2016 Pavel Šimerda <psimerda@redhat.com> - 3.18-1
- New version 3.18

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.15-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 3.15-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 04 2013 Jiri Popelka <jpopelka@redhat.com> - 3.15-1
- 3.15

* Wed Oct 16 2013 Jiri Popelka <jpopelka@redhat.com> - 3.14-3
- use BINDIR

* Mon Oct 14 2013 Jaromír Končický <jkoncick@redhat.com> - 3.14-2
- Install binaries into /usr/bin

* Sun Sep 08 2013 Jiri Popelka <jpopelka@redhat.com> - 3.14-1
- 3.14

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13-1
- 3.13: -v references removed upstream

* Tue Mar 26 2013 Jiri Popelka <jpopelka@redhat.com> - 3.12-4
- remove void -v option from --help

* Fri Mar 08 2013 Jiri Popelka <jpopelka@redhat.com> - 3.12-3
- do not ship outdated french man pages (#919198)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 07 2012  Jiri Popelka <jpopelka@redhat.com> - 3.12-1
- 3.12: man page improvements

* Fri Nov 30 2012  Jiri Popelka <jpopelka@redhat.com> - 3.11-4
- revert /usr move for now

* Fri Nov 30 2012  Jiri Popelka <jpopelka@redhat.com> - 3.11-3
- remove some rh-specific bits from rh.patch as they are no longer valid (#881913)
- remove outdated de & pt man pages
- /usr move: use _bindir macro

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012  Jiri Popelka <jpopelka@redhat.com> - 3.11-1
- 3.11

* Wed Jan 18 2012  Jiri Popelka <jpopelka@redhat.com> - 3.10-1
- 3.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011  Jiri Popelka <jpopelka@redhat.com> - 3.09-1
- 3.09

* Sat Dec 24 2011  Jiri Popelka <jpopelka@redhat.com> - 3.08-1
- 3.08

* Fri Dec 23 2011  Jiri Popelka <jpopelka@redhat.com> - 3.07-1
- 3.07

* Mon Mar 07 2011  Jiri Popelka <jpopelka@redhat.com> - 3.06-1
- 3.06

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 16 2010  Jiri Popelka <jpopelka@redhat.com> - 3.05-1
- 3.05

* Fri Apr 30 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.04-2
- Mark localized man pages with %%lang.

* Thu Mar 25 2010  Jiri Popelka <jpopelka@redhat.com> - 3.04-1
- 3.04

* Tue Feb 02 2010  Jiri Popelka <jpopelka@redhat.com> - 3.03-1
- 3.03

* Tue Nov 10 2009  Jiri Popelka <jpopelka@redhat.com> - 3.01-1
- Initial package. Up to now hostname has been part of net-tools package.
- This package is based on Debian's hostname because Debian has had hostname
  as separate package since 1997 and the code is much better then the old one
  contained in net-tools.
