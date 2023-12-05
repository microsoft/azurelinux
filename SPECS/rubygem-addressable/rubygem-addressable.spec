%global debug_package %{nil}
%global gem_name addressable
Summary:        an alternative implementation to the URI implementation that is part of Ruby's standard library
Name:           rubygem-%{gem_name}
Version:        2.8.5
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/sporkmonger/addressable
Source0:        https://github.com/sporkmonger/addressable/archive/refs/tags/addressable-%{version}.tar.gz#/%{gem_name}-%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-public_suffix < 5.0
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Addressable is an alternative implementation to the URI implementation that is
part of Ruby's standard library. It offers heuristic parsing, and additionally 
provides extensive support for IRIs and URI templates.

%prep
%setup -q -n %{gem_name}-%{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.8.5-1
- Auto-upgrade to 2.8.5 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.8.0-2
- Build from .tar.gz source.

* Thu Aug 04 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 2.8.0-1
- Move to 2.8.0 to fix CVE-2021-32740

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.7.0-1
- License verified
- Original version for CBL-Mariner
