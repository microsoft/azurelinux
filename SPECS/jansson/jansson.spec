Summary:        Jansson json parser
Name:           jansson
Version:        2.14
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
# digip.org now redirects to https://github.com/akheron/jansson
URL:            http://www.digip.org/jansson
Source0:        https://github.com/akheron/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

%description
Jansson is a C library for encoding, decoding and manipulating JSON data.

%package devel
Summary:        Development files for jansson
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for jansson

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name '*.la' -delete -print

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%files
%license LICENSE
%doc CHANGES
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Feb 10 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.14-1
- Update source to v2.14

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.11-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.11-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.11-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 2.11-1
- Updated to version 2.11

* Thu Mar 30 2017 Divya Thaluru <dthaluru@vmware.com> 2.10-1
- Updated to version 2.10

* Thu Jan 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-1
- Initial
