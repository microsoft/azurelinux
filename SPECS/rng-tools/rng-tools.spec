Summary:        RNG deamon and tools
Name:           rng-tools
Version:        5
Release:        5%{?dist}
License:        GPLv2
URL:            https://github.com/nhorman/rng-tools
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
# For some reason, this file downloads as rng-tools-rng-tools-5.tar.gz on Chrome, but wget is fine
Source0:        https://github.com/nhorman/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        rngd.service
Source2:        LICENSE.PTR
BuildRequires:  systemd
BuildRequires:  gcc
BuildRequires:  make

Requires:       systemd

%description
The rng-tools is a set of utilities related to random number generation in kernel.

%prep
%setup -q
cp %{SOURCE2} ./

%build
%configure \
        --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_libdir}/systemd/system
install -p -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/

%check
make  %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post rngd.service

%preun
%systemd_preun rngd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rngd.service

%files
%license LICENSE.PTR
%defattr(-,root,root)
%{_libdir}/systemd/*
%{_bindir}/rngtest
%{_sbindir}/rngd
%{_mandir}/*

%changelog
*  Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 5-5
-  Update BuildRequires
-  Add %%license macro
-  Replace ./configure with %%configure
*  Fri Apr 10 2020 Nick Samson <nisamson@microsoft.com> 5-4
-  Updated Source0, removed %%define sha1, confirmed license.
*  Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5-3
-  Initial CBL-Mariner import from Photon (license: Apache2).
*  Thu May 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5-2
-  Start rngd before cloud-init-local.service to speed up booting.
*  Wed Oct 26 2016 Alexey Makhalov <amakhalov@vmware.com> 5-1
-  Initial version.
