Summary:        A tool for configuring certain Intel baseband devices
Name:           intel-pf-bb-config
Version:        22.03
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Tools
URL:            https://github.com/intel/pf-bb-config
Source0:        https://github.com/intel/pf-bb-config/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
This application provides a means to configure certain Intel baseband devices by
accessing their configuration space and setting parameters via MMIO.

%prep
%autosetup -n pf-bb-config-%{version}

%build
./build.sh

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 pf_bb_config %{buildroot}%{_bindir}/pf_bb_config

%ldconfig_scriptlets

%files

%license LICENSE

%{_bindir}/pf_bb_config

%changelog
* Wed Jul 06 2022 Sriram Nambakam <snambakam@microsoft.com> - 22.03-1
- Upgrade to 22.03

* Thu Feb 17 2022 Vince Perri <viperri@microsoft.com> - 21.11-1
- Original version for CBL-Mariner.
- License verified
