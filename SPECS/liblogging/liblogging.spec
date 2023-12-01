Summary:        Logging Libraries
Name:           liblogging
Version:        1.0.6
Release:        4%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            http://www.liblogging.org/
Source0:        https://download.rsyslog.com/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  gcc

%description
liblogging (the upstream project) is a collection of several components: stdlog, journalemu and rfc3195.
The stdlog component of liblogging can be viewed as an enhanced version of the
syslog(3) API. It retains the easy semantics, but makes the API more
sophisticated "behind the scenes" with better support for multiple threads
and flexibility for different log destinations (e.g. syslog and systemd
journal).

%package devel
Summary:        Development libraries and header files for liblogging
Requires:       liblogging

%description devel
The package contains libraries and header files for
developing applications that use liblogging.

%prep
%setup -q

%build
%configure --disable-journal
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/*.a

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/liblogging/*.h

%changelog
* Wed Oct 28 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.0.6-4
- Address source RPM publishing issue on packages.microsoft.com

* Mon Oct 12 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.0.6-3
- Remove .la files
- Lint to Mariner style
- License verified, %%license added

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.0.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.0.6-1
- Updated to version 1.0.6

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.5-2
- GA - Bump release of all rpms

* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> - 1.0.5-1
- Initial build. First version
