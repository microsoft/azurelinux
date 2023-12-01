Summary:        Fedora-specific CMake modules and release scripts
Name:           cmake-fedora
Version:        2.9.3
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pagure.io/%{name}
Source0:        https://releases.pagure.org/%{name}/%{name}-%{version}-Source.tar.gz
BuildRequires:  cmake
BuildArch:      noarch

%description
cmake-fedora consists a set of scripts and cmake modules that simply the release software packages to RHEL and Fedora.

%prep
%autosetup -n %{name}-%{version}-Source

%build
%cmake .
%cmake_build

%install
%cmake_install
# We don't need any of the release scripts for Fedora-specific infrastructure
rm -rf %{buildroot}%{_bindir}/*
# We don't need anything in the docs folder
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_datadir}/cmake/Modules/*
%{_datadir}/cmake/Templates/*

%changelog
* Thu Jun 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.9.3-1
- Original version for CBL-Mariner (license: MIT)
- License verified