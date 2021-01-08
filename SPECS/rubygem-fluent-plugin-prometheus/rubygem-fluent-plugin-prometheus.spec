%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-prometheus

Name:           rubygem-fluent-plugin-prometheus
Version:        1.7.3
Release:        1%{?dist}
Summary:        A fluent plugin that collects metrics and exposes for Prometheus 
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-fluentd
Requires:       rubygem-prometheus-client < 0.10

%description
A fluent plugin that instruments metrics from records and exposes them via web interface. 
Intended to be used together with a Prometheus server.
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
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 1.7.3-1
-   Original version for CBL-Mariner.
-   License verified.
