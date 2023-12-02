Summary:        Parallel Implementation of GZIP
Name:           pigz
Version:        2.8
Release:        1%{?dist}
License:        zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.zlib.net/pigz
Source0:        https://github.com/madler/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel

%description
pigz, which stands for parallel implementation of gzip, is a fully
functional replacement for gzip that exploits multiple processors and
multiple cores to the hilt when compressing data

%prep
%autosetup

%build
%make_build

%install
mkdir -p %{buildroot}%{_bindir}/
install -p -m 755 pigz %{buildroot}%{_bindir}/
install -p -m 755 unpigz %{buildroot}%{_bindir}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license README
%{_bindir}/pigz
%{_bindir}/unpigz

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.8-1
- Auto-upgrade to 2.8 - Azure Linux 3.0 - package upgrades

* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-2
- Fixing invalid source URL.
* Tue Feb 09 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.6-1
- Update pigz to 2.6
- Change source url to GitHub.
* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.5-1
- Add pigz spec
- License verified
- Original version for CBL-Mariner
