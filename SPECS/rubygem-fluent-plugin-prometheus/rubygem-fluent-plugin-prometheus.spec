%global debug_package %{nil}
%global gem_name fluent-plugin-prometheus
Summary:        A fluent plugin that collects metrics and exposes for Prometheus
Name:           rubygem-%{gem_name}
Version:        2.1.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-prometheus
Source0:        https://github.com/fluent/fluent-plugin-prometheus/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A fluent plugin that instruments metrics from records and exposes them via web interface.
Intended to be used together with a Prometheus server.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.0-1
- Auto-upgrade to 2.1.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.2-1
- Update to v2.0.2.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.7.3-1
- License verified
- Original version for CBL-Mariner
