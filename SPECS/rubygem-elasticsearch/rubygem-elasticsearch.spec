%global debug_package %{nil}
%global gem_name elasticsearch
Summary:        Ruby integrations for Elasticsearch
Name:           rubygem-elasticsearch
Version:        8.0.1
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/elastic/elasticsearch-ruby
Source0:        https://github.com/elastic/elasticsearch-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-elastic-transport
Requires:       rubygem-elasticsearch-api
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby integrations for Elasticsearch (client, API, etc.)

%prep
%setup -q -n %{gem_name}-ruby-%{version}

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
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 7.6.0-1
- License verified
- Original version for CBL-Mariner
