%global debug_package %{nil}
%global gem_name fluent-plugin-calyptia-monitoring
Summary:        Monitoring Fluentd via Calyptia Cloud
Name:           rubygem-%{gem_name}
Version:        0.1.3
Release:        1%{?dist}
License:        Apache 2.0
Vendor:	        Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/calyptia/fluent-plugin-calyptia-monitoring
Source0:        https://github.com/calyptia/fluent-plugin-calyptia-monitoring/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Fluentd input plugin to ingest metrics into Calyptia Cloud.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE file to buildroot from Source0
cp LICENSE %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.1.3-1
- License verified
- Original version for CBL-Mariner
