%global debug_package %{nil}
%global gem_name fluent-plugin-windows-exporter
Summary:        Fluentd plugin to collect Windows metrics
Name:           rubygem-%{gem_name}
Version:        1.0.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:	        Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/fluent-plugins-nursery/fluent-plugin-windows-exporter
Source0:        https://github.com/fluent-plugins-nursery/fluent-plugin-windows-exporter/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
BuildRequires:  rubygem-rake
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Fluentd plugin to collect Windows metrics. This is a Fluentd port of Prometheus' Windows exporter. This plugin emits metrics as event stream, so can be used in combination with any output plugins.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
