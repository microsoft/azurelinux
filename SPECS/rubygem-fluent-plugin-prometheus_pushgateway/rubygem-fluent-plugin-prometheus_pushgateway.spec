%global debug_package %{nil}
%global gem_name fluent-plugin-prometheus_pushgateway
Summary:        A fluent plugin for prometheus pushgateway
Name:           rubygem-%{gem_name}
Version:        0.1.1
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-prometheus_pushgateway
Source0:        https://github.com/fluent/fluent-plugin-prometheus_pushgateway/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This is Fluentd's plugin for sending data collected by
fluent-plugin-prometheus plugin to Pushgateway.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.1.1-1
- Auto-upgrade to 0.1.1 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.1.0-1
- Update to v0.1.0.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 0.0.2-1
- License verified
- Original version for CBL-Mariner
