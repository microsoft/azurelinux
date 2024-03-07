Summary:        Linux Key Management Utilities
Name:           keyutils
Version:        1.6.3
Release:        1%{?dist}
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git/about/
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git/snapshot/%{name}-%{version}.tar.gz

%if %{with_check}
BuildRequires: lsb-release
%endif

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to user space to get a key
instantiated.

%package   devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Provides:       %{name}-libs = %{version}-%{release}
Provides:       %{name}-libs-devel = %{version}-%{release}

%description   devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%make_build

%install
%make_install           \
    BINDIR=%{_bindir}   \
    LIBDIR=%{_libdir}   \
    SBINDIR=%{_sbindir} \
    USRLIBDIR=%{_libdir}
find %{buildroot} -name '*.a'  -delete

%check
# Installing keyutils binaries to be available for the tests to use.
%make_install DESTDIR=/
%make_build -k test

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENCE.GPL LICENCE.LGPL
%doc README
%{_bindir}/*
%{_datadir}/keyutils
%{_libdir}/*.so.1
%{_libdir}/*.so.1.*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/request-key.conf
%dir %{_sysconfdir}/request-key.d/

%files devel
%defattr(-,root,root)
%license LICENCE.GPL LICENCE.LGPL
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Fri Oct 13 2023 Thien Trung Vuong <tvuong@microsoft.com> - 1.6.3-1
- Update to version 1.6.3
- Update URL and Source0

* Wed Nov 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.1-1
- Update to version 1.6.1.
- Enabled tests.
- License verified.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.5.10-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Jan 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.5.10-4
- Provide keyutils-libs and keyutils-libs-devel.

* Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.10-3
- Adding a license reference.
- License verified.
- Removed "sha1" macro.
- Switched to HTTPS URLs.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.5.10-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> - 1.5.10-1
- Updated to version 1.5.10

* Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> - 1.5.9-1
- Initial build. First version
