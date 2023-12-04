Summary:        Log for C++
Name:           log4cpp
Version:        1.1.4
Release:        1%{?dist}
License:        LGPLv2+
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            http://log4cpp.sourceforge.net/
Source:         https://sourceforge.net/projects/%{name}/files/%{name}-1.1.x%20%28new%29/%{name}-1.1/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

%description
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

%package devel
Summary: development tools for Log for C++
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %name-devel package contains the static libraries and header files
needed for development with %name.


%prep
%{__rm} -rf $RPM_BUILD_ROOT

%setup -q -n log4cpp
CC=%{__cc} CXX=%{__cxx} ./configure --prefix=%{_prefix}

%build
%{__make}

%install
%{__rm} -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%_prefix/lib/lib*.so.*

%files devel
%defattr(-,root,root)
%_prefix/include/*
%_prefix/bin/log4cpp-config
%_prefix/lib/lib*.so
%_prefix/lib/*.*a
%_prefix/lib/pkgconfig/log4cpp.pc
%_prefix/share/aclocal/*.m4

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4-1
- Auto-upgrade to 1.1.4 - Azure Linux 3.0 - package upgrades

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.3-7
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.3-6
- Added %%license line automatically

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 1.1.3-5
-   Replace BuildArch with ExclusiveArch
*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.1.3-4
-   Fixed "Source0" tag.
-   License verified and "License" tag updated.
-   Removed "%%define sha1".
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.3-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.1.3-2
-   Adding BuildArch
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.1.3-1
-   Upgrade to latest version
*   Mon Oct 23 2017 Benson Kwok <bkwok@vmware.com> 1.1.1-1
-   Initial build. First version
