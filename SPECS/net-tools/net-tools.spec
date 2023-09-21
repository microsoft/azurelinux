Summary:        Networking Tools
Name:           net-tools
Version:        2.10
Release:        3%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://sourceforge.net/projects/net-tools/
Source0:        https://downloads.sourceforge.net/project/%{name}/%{name}-%{version}.tar.xz
Conflicts:      toybox
Obsoletes:      inetutils
Provides:       hostname = %{version}-%{release}

%description
The Net-tools package is a collection of programs for controlling the network subsystem of the Linux kernel.

%prep
%autosetup -p1

%build
yes "" | make config
sed -i -e 's|HAVE_IP_TOOLS 0|HAVE_IP_TOOLS 1|g' \
       -e 's|HAVE_AFINET6 0|HAVE_AFINET6 1|g' \
       -e 's|HAVE_MII 0|HAVE_MII 1|g' config.h
sed -i -e 's|#define HAVE_HWSTRIP 1|#define HAVE_HWSTRIP 0|g' \
       -e 's|#define HAVE_HWTR 1|#define HAVE_HWTR 0|g' config.h
sed -i -e 's|# HAVE_IP_TOOLS=0|HAVE_IP_TOOLS=1|g' \
       -e 's|# HAVE_AFINET6=0|HAVE_AFINET6=1|g' \
       -e 's|# HAVE_MII=0|HAVE_MII=1|g' config.make
sed -i 's|#include <netinet/ip.h>|//#include <netinet/ip.h>|g' iptunnel.c
make

%install
make BASEDIR=%{buildroot} install

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
/bin/*
/sbin/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.10-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Apr 04 2022 Rachel Menge <rachelmenge@microsoft.com> - 2.10-2
- Remove ifconfig mv command

* Thu Feb 17 2022 Rachel Menge <rachelmenge@microsoft.com> - 2.10-1
- Update to 2.10

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.60-16
- Removing the explicit %%clean stage.

* Fri Dec 11 2020 Joe Schmitt <joschmit@microsoft.com> - 1.60-15
- Provide hostname.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.60-14
- Added %%license line automatically

* Mon Apr 13 2020 Eric Li <eli@microsoft.com> 1.60-13
- Update Source0: and delete sha1. Verified license. Fixed URL.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.60-12
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 1.60-11
- Added conflicts toybox

* Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-10
- Fix compilation issue with linux-4.9

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-9
- Remove iputils deps.

* Tue Oct 04 2016 ChangLee <changLee@vmware.com> 1.60-8
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.60-7
- GA - Bump release of all rpms

* Thu Feb 4 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-6
- Apply all patches from 1.60-26ubuntu1.

* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-5
- Added net-tools-1.60-manydevs.patch

* Fri Nov 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.60-4
- Added ipv6 support. Include hostname and dnshostname.

* Thu Oct 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.60-3
- Added changes to replace inetutils with net-tools

* Thu Jul 30 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-2
- Disable building with parallel threads

* Mon Jul 13 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-1
- Initial build. First version
