%global debug_package %{nil}
%global gem_name faraday-excon
Summary:        Faraday adapter for Excon
Name:           rubygem-%{gem_name}
Version:        2.1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/lostisland/faraday-excon
Source0:        https://github.com/lostisland/faraday-excon/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem is a Faraday adapter for the Excon library. Faraday is an HTTP client library that provides a common interface over many adapters. Every adapter is defined into its own gem. This gem defines the adapter for Excon.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.0-1
- Auto-upgrade to 2.1.0 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.0-1
- License verified
- Original version for CBL-Mariner
