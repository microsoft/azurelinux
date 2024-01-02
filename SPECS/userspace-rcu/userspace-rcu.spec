Summary:        user space RCU (read-copy-update)
Name:           userspace-rcu
Version:        0.14.0
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://liburcu.org
#Source0:       https://github.com/urcu/userspace-rcu/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  elfutils-devel
BuildRequires:  libxml2-devel
BuildRequires:  m4
BuildRequires:  popt-devel

%description
This data synchronization library provides read-side access which scales linearly with the number of cores.

%package devel
Summary:        Development Libraries for openssl
Group:          Development/Libraries
Requires:       userspace-rcu = %{version}-%{release}

%description devel
Library files for doing development with userspace-rcu.

%prep
%setup -q

%build
autoreconf -fiv
./configure \
    --prefix=%{_prefix} \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%files
%{_libdir}/*.so.*
%{_includedir}/*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%license LICENSE
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-1
- Auto-upgrade to 0.14.0 - Azure Linux 3.0 - package upgrades

* Wed Jan 12 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.13.0-1
- Update to version 0.13.0.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 0.10.1-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.10.1-4
- Added %%license line automatically

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> 0.10.1-3
- Update URL.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.10.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.10.1-1
- Updated to version 0.10.1.

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 0.9.3-1
- Updated to version 0.9.3.

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.9.1-4
- Modified %check

* Mon Jul 25 2016 Divya Thaluru <dthaluru@vmware.com> 0.9.1-3
- Added devel package and removed packaging of debug files

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.1-2
- GA - Bump release of all rpms

* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
- Initial build.  First version
