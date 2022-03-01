Summary:       jq is a lightweight and flexible command-line JSON processor.
Name:          jq
Version:       1.5
Release:        7%{?dist}
Group:         Applications/System
Vendor:         Microsoft Corporation
License:       MIT
URL:           https://github.com/stedolan/jq
Source0:       https://github.com/stedolan/jq/releases/download/jq-1.5/jq-1.5.tar.gz
#https://github.com/stedolan/jq/commit/8eb1367ca44e772963e704a700ef72ae2e12babd
Patch0:        CVE-2015-8863.patch
#https://github.com/wmark/jq/commit/e6f32d647b180006a90e080ab61ce6f09c3134d7
Patch1:        CVE-2016-4074.patch
Distribution:   Mariner
%if %{with_check}
BuildRequires: which
BuildRequires: oniguruma-devel
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
%patch0 -p1
%patch1 -p1

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
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5-7
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.5-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*  Mon Nov 19 2018 Ashwin H<ashwinh@vmware.com> 1.5-4
-  Add which for %check
*  Tue Aug 22 2017 Chang Lee <changlee@vmware.com> 1.5-3
-  Add oniguruma for %check
*  Wed Jun 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5-2
-  Fix for CVE-2015-8863 and CVE-2016-4074
*  Mon May 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5-1
-  Initial version
