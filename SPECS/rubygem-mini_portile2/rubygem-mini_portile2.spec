%global debug_package %{nil}
%global gem_name mini_portile2
Summary:        Simplistic port-like solution for developers
Name:           rubygem-mini_portile2
Version:        2.8.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/flavorjones/mini_portile
Source0:        https://github.com/flavorjones/mini_portile/archive/refs/tags/v%{version}.tar.gz#/mini_portile-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This project is a minimalistic implementation of a port/recipe system for developers.

%prep
%autosetup -p1 -n mini_portile-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.8.4-1
- Auto-upgrade to 2.8.4 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.8.0-1
- Update to v2.8.0.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.5.0-1
- License verified
- Original version for CBL-Mariner
