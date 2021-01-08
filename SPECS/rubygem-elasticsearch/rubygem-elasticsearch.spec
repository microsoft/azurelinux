%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name elasticsearch

Name:           rubygem-elasticsearch
Version:        7.6.0
Release:        1%{?dist}
Summary:        Ruby integrations for Elasticsearch 
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.4.0
Requires:       rubygem-elasticsearch-api
Requires:       rubygem-elasticsearch-transport

%description
Ruby integrations for Elasticsearch (client, API, etc.)

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
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 7.6.0-1
-   Original version for CBL-Mariner.
-   License verified.
