%global debug_package %{nil}
%global gem_name elasticsearch
Summary:        Ruby integrations for Elasticsearch
Name:           rubygem-%{gem_name}
Version:        8.9.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/elastic/elasticsearch-ruby
Source0:        https://github.com/elastic/elasticsearch-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-elastic-transport
Requires:       rubygem-elasticsearch-api
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby integrations for Elasticsearch (client, API, etc.)

%prep
%autosetup -p1 -n %{gem_name}-ruby-%{version}

%build
cd %{gem_name}
gem build %{gem_name}

%install
cd %{gem_name}
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.9.0-1
- Auto-upgrade to 8.9.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 8.3.0-1
- Update to v8.3.0.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 7.6.0-1
- License verified
- Original version for CBL-Mariner
