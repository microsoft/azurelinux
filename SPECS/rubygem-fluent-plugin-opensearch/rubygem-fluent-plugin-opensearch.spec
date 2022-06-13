%global debug_package %{nil}
%global gem_name fluent-plugin-opensearch
Summary:        OpenSearch Plugin for Fluentd
Name:           rubygem-%{gem_name}
Version:        1.0.4
Release:        1%{?dist}
License:        Apache 2.0
Vendor:	        Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/fluent/fluent-plugin-opensearch
Source0:        https://github.com/fluent/fluent-plugin-opensearch/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Opensearch output plugin for Fluent event collector

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.txt file to buildroot from Source0
cp LICENSE.txt %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.7.0-1
- License verified
- Original version for CBL-Mariner
