Summary:        jq is a lightweight and flexible command-line JSON processor.
Name:           jq
Version:        1.7.1
Release:        4%{?dist}
Group:          Applications/System
Vendor:         Microsoft Corporation
License:        MIT
URL:            https://jqlang.github.io/jq/
Source0:        https://github.com/jqlang/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-53427.patch
Patch1:         CVE-2024-23337.patch
Patch2:         CVE-2025-48060.patch
Distribution:   Azure Linux
BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  oniguruma-devel
%if 0%{?with_check}
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
%autosetup -p1

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
%exclude %{_datadir}/doc/jq/COPYING
%{_libdir}/libjq.so.*
%{_libdir}/pkgconfig/libjq.pc

%files devel
%{_libdir}/libjq.so
%{_includedir}/*

%changelog
* Wed Jul 23 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.7.1-4
- Patch for CVE-2025-48060
- Updated files section to fix duplicated license files

* Mon May 26 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.7.1-3
- Patch CVE-2024-23337

* Wed Mar 05 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.7.1-2
- Patch CVE-2024-53427

* Fri Feb 02 2024 Thien Trung Vuong <tvuong@microsoft.com> - 1.7.1-1
- Upgrade to version 1.7.1

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
