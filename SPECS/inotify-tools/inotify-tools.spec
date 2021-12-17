Summary:        Command line utility for i-node notifications and management.
Name:           inotify-tools
Version:        3.14
Release:        3%{?dist}
URL:            https://github.com/inotify-tools/inotify-tools/wiki
Source0:        https://github.com/downloads/rvoicilas/%{name}/%{name}-%{version}.tar.gz
License:        GPLv2
Group:          Applications/Systems
Vendor:         Microsoft Corporation
Distribution:   Mariner
Provides:       libinotifytools0

%description
inotify-tools is simple command line interface program for linux distributions
which is used to monitor inode specific filesystem events.

%package devel
Summary: Header files and libraries for building application using libinotify-tools.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q


%build
%configure
make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT
%makeinstall

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
/usr/bin
/usr/share
/%{_libdir}/libinotifytools.so.0.4.1

%files devel
%defattr(-,root,root)
/usr/include
/%{_libdir}/libinotifytools.a
/%{_libdir}/libinotifytools.so
/%{_libdir}/libinotifytools.so.0
/%{_libdir}/libinotifytools.la

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.14-3
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.14-2
- Added %%license line automatically

*   Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> 3.14-1
-   Update to 3.14. Update Source0 URL. Fix license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.13-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.13-2
-	GA - Bump release of all rpms
*       Mon Dec 14 2015 Kumar Kaushik <kaushikk@vmware.com> 3.13-1
-       Initial build.  First version
