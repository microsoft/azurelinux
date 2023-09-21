Summary:	    Standard Linux utility for controlling network drivers and hardware
Name:		    ethtool
Version:        5.16
Release:        2%{?dist}
License:	    GPLv2
URL:		    https://www.kernel.org/pub/software/network/ethtool/
Group:		    Productivity/Networking/Diagnostic
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	    https://www.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.xz

BuildRequires: libmnl-devel

%description
ethtool is the standard Linux utility for controlling network drivers and hardware,
particularly for wired Ethernet devices

%prep
%setup -q

%build
autoreconf -fi
%configure --sbindir=/sbin
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%files
%doc AUTHORS COPYING NEWS README ChangeLog
%defattr(-,root,root)
%license LICENSE
/sbin/*
%{_mandir}
%{_datadir}/bash-completion/completions/ethtool

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.16-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

*   Mon Jan 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.16-1
-   Update version to 5.16

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0-3
-   Removing the explicit %%clean stage.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.0-2
-   Added %%license line automatically

*   Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> 5.0-1
-   Update to 5.0. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.18-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 4.18-1
-   Version update

*   Mon Apr 03 2017 Chang Lee <changlee@vmware.com> 4.8-1
-   Upgraded to version 4.8

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2-3
-   GA - Bump release of all rpms

*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.2-2
-   Change file packaging.

*   Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2-1
-   Initial build. First version
