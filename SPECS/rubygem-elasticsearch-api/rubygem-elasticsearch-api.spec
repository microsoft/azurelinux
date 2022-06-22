%global debug_package %{nil}
%global gem_name elasticsearch-api
Summary:        Ruby API for Elasticsearch
Name:           rubygem-elasticsearch-api
Version:        8.0.1
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://www.elastic.co/guide/en/elasticsearch/client/ruby-api/current/index.html
Source0:        https://github.com/elastic/elasticsearch-ruby/archive/refs/tags/v%{version}.tar.gz#/elasticsearch-ruby-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-multi_json
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
The elasticsearch-api library provides a Ruby implementation 
of the Elasticsearch REST API.

%prep
%setup -q -n elasticsearch-ruby-%{version}

%build
cd %{gem_name}
gem build %{gem_name}

%install
cd %{gem_name}
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add lib files to buildroot from Source0
cp -r lib/ %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 8.0.1-1
- Update to v8.0.1.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 7.6.0-1
- License verified
- Original version for CBL-Mariner