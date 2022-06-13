%global debug_package %{nil}
%global gem_name fluent-plugin-prometheus
Summary:        A fluent plugin that collects metrics and exposes for Prometheus
Name:           rubygem-fluent-plugin-prometheus
Version:        2.0.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-prometheus
Source0:        https://github.com/fluent/fluent-plugin-prometheus/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A fluent plugin that instruments metrics from records and exposes them via web interface.
Intended to be used together with a Prometheus server.

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
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.7.3-1
- License verified
- Original version for CBL-Mariner
