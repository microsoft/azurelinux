Summary:        Command line utility for i-node notifications and management.
Name:           inotify-tools
Version:        3.22.1.0
Release:        1%{?dist}
URL:            https://github.com/inotify-tools/inotify-tools/wiki
Source0:        https://github.com/inotify-tools/inotify-tools/archive/%{version}/inotify-tools-%{version}.tar.gz
License:        GPLv2
Group:          Applications/Systems
Vendor:         Microsoft Corporation
Distribution:   Mariner
Provides:       libinotifytools0
BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  make
BuildRequires:  libtool

%description
inotify-tools is simple command line interface program for linux distributions
which is used to monitor inode specific filesystem events.

%package        devel
Summary:        Headers and libraries for building apps that use libinotifytools
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1

%build
./autogen.sh
%configure \
        --disable-dependency-tracking \
        --disable-static \
        --enable-doxygen
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
# We'll install documentation in the proper place
rm -rf %{buildroot}/%{_datadir}/doc/

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets

%files
%doc AUTHORS COPYING
%license COPYING
%{_bindir}/inotifywait
%{_bindir}/inotifywatch
%{_libdir}/libinotifytools.so.*
%{_mandir}/man1/inotifywait.1*
%{_mandir}/man1/inotifywatch.1*
%{_mandir}/man1/fsnotifywait.1*
%{_mandir}/man1/fsnotifywatch.1*

%files devel
%doc libinotifytools/src/doc/html/*
%dir %{_includedir}/inotifytools/
%{_includedir}/inotifytools/inotify.h
%{_includedir}/inotifytools/inotify-nosys.h
%{_includedir}/inotifytools/inotifytools.h
%{_includedir}/inotifytools/fanotify-dfid-name.h
%{_includedir}/inotifytools/fanotify.h
%{_libdir}/libinotifytools.so

%changelog
* Thu Jan 27 2022 Rachel Menge <rachelmenge@microsoft.com> - 3.22.1.0-1
- Update to 3.22.1.0

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.14-3
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.14-2
- Added %%license line automatically

* Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> 3.14-1
- Update to 3.14. Update Source0 URL. Fix license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.13-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.13-2
- GA - Bump release of all rpms

* Mon Dec 14 2015 Kumar Kaushik <kaushikk@vmware.com> 3.13-1
- Initial build.  First version
