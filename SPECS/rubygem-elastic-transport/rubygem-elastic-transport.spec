%global debug_package %{nil}
%global gem_name elastic-transport
Summary:        Transport classes and utilities shared among Ruby Elastic client libraries
Name:           rubygem-%{gem_name}
Version:        8.2.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/elastic/elastic-transport-ruby
Source0:        https://github.com/elastic/elastic-transport-ruby/archive/refs/tags/v%{version}.tar.gz#/elastic-transport-ruby-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-faraday
Requires:       rubygem-multi_json
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem provides a low-level Ruby client for connecting to an Elastic cluster. It powers both the Elasticsearch client and the Elastic Enterprise Search client.

%prep
%autosetup -p1 -n %{gem_name}-ruby-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.2.2-1
- Auto-upgrade to 8.2.2 - Azure Linux 3.0 - package upgrades

* Tue May 31 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 8.0.1-1
- License verified
- Original version for CBL-Mariner
