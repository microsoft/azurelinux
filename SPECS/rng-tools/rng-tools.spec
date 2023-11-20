Summary:        RNG deamon and tools
Name:           rng-tools
Version:        6.14
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/nhorman/rng-tools
Source0:        https://github.com/nhorman/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        rngd.service
BuildRequires:  gcc
BuildRequires:  jansson-devel
BuildRequires:  libcurl-devel
BuildRequires:  libp11-devel
BuildRequires:  make
BuildRequires:  rtl-sdr-devel
BuildRequires:  systemd
Requires:       systemd

%description
The rng-tools is a set of utilities related to random number generation in kernel.

%prep
%setup -q

%build
./autogen.sh
%configure
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
%license COPYING
%defattr(-,root,root)
%{_libdir}/systemd/*
%{_bindir}/rngtest
%{_bindir}/randstat
%{_sbindir}/rngd
%{_mandir}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 6.14-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Feb 08 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 6.14-1
- Update to version 6.14.
- Remove LICENSE.PTR file
- License verified

* Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 5-5
- Update BuildRequires
- Add %%license macro
- Replace ./configure with %%configure

* Fri Apr 10 2020 Nick Samson <nisamson@microsoft.com> 5-4
- Updated Source0, removed %%define sha1, confirmed license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu May 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5-2
- Start rngd before cloud-init-local.service to speed up booting.

* Wed Oct 26 2016 Alexey Makhalov <amakhalov@vmware.com> 5-1
- Initial version.
