%global debug_package %{nil}
%global gem_name fluent-plugin-prometheus_pushgateway
Summary:        A fluent plugin for prometheus pushgateway
Name:           rubygem-fluent-plugin-prometheus_pushgateway
Version:        0.1.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-prometheus_pushgateway
Source0:        https://github.com/fluent/fluent-plugin-prometheus_pushgateway/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluent-plugin-prometheus < 2.0.0

%description
This is Fluentd's plugin for sending data collected by
fluent-plugin-prometheus plugin to Pushgateway.

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
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 0.0.2-1
- License verified
- Original version for CBL-Mariner
