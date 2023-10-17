Summary:        jq is a lightweight and flexible command-line JSON processor.
Name:           jq
Version:        1.6
Release:        2%{?dist}
Group:          Applications/System
Vendor:         Microsoft Corporation
License:        MIT
URL:            https://github.com/stedolan/jq
Source0:        https://github.com/stedolan/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Distribution:   Mariner
BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  oniguruma-devel
%if %{with_check}
BuildRequires:  which
%endif

%description
jq is a lightweight and flexible command-line JSON processor.

%package devel
Summary:    Development files for jq
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for jq

%prep
%setup -q

%build
%configure \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/*
%{_datadir}/*
%{_libdir}/libjq.so.*

%files devel
%{_libdir}/libjq.so
%{_includedir}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.6-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.6-1
- Update source to v1.6
- Remove CVE-2015-8863.patch, CVE-2016-4074.patch (changes found in this release)
- Move oniguruma BuildRequires outside of check block 

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5-7
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.5-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Nov 19 2018 Ashwin H<ashwinh@vmware.com> 1.5-4
- Add which for %check

* Tue Aug 22 2017 Chang Lee <changlee@vmware.com> 1.5-3
- Add oniguruma for %check

* Wed Jun 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5-2
- Fix for CVE-2015-8863 and CVE-2016-4074

* Mon May 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5-1
- Initial version
