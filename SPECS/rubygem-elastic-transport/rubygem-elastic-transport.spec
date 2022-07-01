%global debug_package %{nil}
#%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name elastic-transport
Summary:        Ruby client for Elastic
Name:           rubygem-elastic-transport
Version:        8.0.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-faraday
Requires:       rubygem-multi_json

%description
Ruby client for Elastic.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Thu Jun 30 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.0.0-1
- License verified
- Original version for CBL-Mariner