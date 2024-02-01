Summary:        TPM2 Access Broker & Resource Management Daemon implementing the TCG spec
Name:           tpm2-abrmd
Version:        3.0.0
Release:        3%{?dist}
License:        BSD 2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/tpm2-software/tpm2-abrmd/releases/
Source0:        https://github.com/tpm2-software/tpm2-abrmd/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  dbus-devel
BuildRequires:  glib-devel
BuildRequires:  tpm2-tss-devel
BuildRequires:  which
Requires:       dbus
Requires:       glib
Requires:       tpm2-tss

%description
TPM2 Access Broker & Resource Management Daemon implementing the TCG spec

%package devel
Summary:        The libraries and header files needed for TSS2 ABRMD development.
Requires:       %{name} = %{version}-%{release}

%description devel
The libraries and header files needed for TSS2 ABRMD development.

%prep
%setup -q

%build
%configure \
    --disable-static \
    --with-systemdsystemunitdir=%{_libdir}/systemd/system \
    --with-dbuspolicydir=%{_sysconfdir}/dbus-1/system.d

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_sysconfdir}/dbus-1/system.d/tpm2-abrmd.conf
%{_sbindir}/tpm2-abrmd
%{_libdir}/libtss2-tcti-tabrmd.so.0.0.0
%{_libdir}/systemd/system/tpm2-abrmd.service
%{_libdir}/systemd/system-preset/tpm2-abrmd.preset
%{_datadir}/dbus-1/*
%{_mandir}/man8

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/libtss2-tcti-tabrmd.la
%{_libdir}/libtss2-tcti-tabrmd.so
%{_libdir}/libtss2-tcti-tabrmd.so.0
%{_mandir}/man3
%{_mandir}/man7

%changelog
* Thu Jan 25 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 3.0.0-3
- Increment version to rebuild with new tpm2-tss

* Thu Jan 25 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 3.0.0-2
- Increment version to rebuild with new tpm2-tss

* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.0-1
- Auto-upgrade to 3.0.0 - Azure Linux 3.0 - package upgrades

* Tue Jan 18 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.4.0-1
- Update to version 2.4.0

* Sun Sep 27 2020 Daniel McIlvaney <damcilva@microsoft.com> 2.3.3-1
- Update to 2.3.3 to solve incompatibility with tpm2-tss 2.4.0

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.1.1-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 2.1.1-1
- Update to 2.1.1. Fix URL. Fix Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.1.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.0-1
- Initial build. First version
