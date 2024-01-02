%global debug_package %{nil}
%global gem_name elasticsearch-api
Summary:        Ruby API for Elasticsearch
Name:           rubygem-%{gem_name}
Version:        8.9.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://www.elastic.co/guide/en/elasticsearch/client/ruby-api/current/index.html
Source0:        https://github.com/elastic/elasticsearch-ruby/archive/refs/tags/v%{version}.tar.gz#/elasticsearch-ruby-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-multi_json
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
The elasticsearch-api library provides a Ruby implementation 
of the Elasticsearch REST API.

%prep
%autosetup -p1 -n elasticsearch-ruby-%{version}

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

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 7.6.0-1
- License verified
- Original version for CBL-Mariner