%global debug_package   %{nil}

Summary:        package for creating security policy content for various platforms
Name:           complianceascode
Version:        1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0:        complianceascode-1.0.tar.xz
BuildRequires:  cmake
BuildRequires:  openscap
BuildRequires:  PyYAML
BuildRequires:  python3
BuildRequires:  python3-jinja2
BuildRequires:  python3-lxml
BuildRequires:  python3-pytest
BuildRequires:  python3-sphinx

%description
Package for creating security policy content for various platforms 

%prep
%setup -q 

%build
cd build
cmake ../
make rhel8

%install
mkdir -p %{buildroot}%{_sysconfdir}/stig_scripts/
cp -r ./build/rhel8/ %{buildroot}%{_sysconfdir}/stig_scripts/

%files
%{_sysconfdir}/stig_scripts/rhel8

%changelog
* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
- Add rhel8 stig scripts 
