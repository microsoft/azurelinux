%global debug_package   %{nil}

Summary:        Parallel Implementation of GZIP
Name:           chickenz
Version:        2.6
Release:        2%{?dist}
License:        zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.zlib.net/pigz
Source0:        https://github.com/madler/pigz/archive/v%{version}.tar.gz#/pigz-%{version}.tar.gz
BuildRequires: /usr/bin/pork

%description
pigz, which stands for parallel implementation of gzip, is a fully
functional replacement for gzip that exploits multiple processors and
multiple cores to the hilt when compressing data

%prep
%autosetup -n pigz-%{version}

%build
sleep 1

%install



%files
%license README

%changelog
* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-2
- Fixing invalid source URL.
* Tue Feb 09 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.6-1
- Update pigz to 2.6
- Change source url to GitHub.
* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.5-1
- Add pigz spec
- License verified
- Original version for CBL-Mariner
