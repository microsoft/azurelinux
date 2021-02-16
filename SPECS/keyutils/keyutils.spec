Summary:        Linux Key Management Utilities
Name:           keyutils
Version:        1.5.10
Release:        5%{?dist}
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://people.redhat.com/~dhowells/keyutils/
Source0:        https://people.redhat.com/~dhowells/keyutils/keyutils-%{version}.tar.bz2

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
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} LIBDIR=/%{_libdir} USRLIBDIR=%{_libdir}
find %{buildroot} -name '*.a'  -delete

%clean
rm -rf %{buildroot}


%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENCE.GPL LICENCE.LGPL
%license LICENCE.GPL
%doc README
/sbin/*
/bin/*
%{_libdir}/*.so.*
%{_datadir}/keyutils
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/request-key.conf
%dir %{_sysconfdir}/request-key.d/

%files devel
%defattr(-,root,root)
%license LICENCE.GPL LICENCE.LGPL
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.5.10-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Jan 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.5.10-4
- Provide keyutils-libs and keyutils-libs-devel.

*   Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.5.10-3
-   Adding a license reference.
-   License verified.
-   Removed "sha1" macro.
-   Switched to HTTPS URLs.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.5.10-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.5.10-1
-   Updated to version 1.5.10

*   Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.5.9-1
-   Initial build. First version
