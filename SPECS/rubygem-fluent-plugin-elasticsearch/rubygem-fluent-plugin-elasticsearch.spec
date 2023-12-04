%global debug_package %{nil}
%global gem_name fluent-plugin-elasticsearch
Summary:        Elasticsearch output plugin for Fluent event collector
Name:           rubygem-fluent-plugin-elasticsearch
Version:        5.3.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/uken/fluent-plugin-elasticsearch
Source0:        https://github.com/uken/fluent-plugin-elasticsearch/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-elasticsearch
Requires:       rubygem-excon
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Elasticsearch output plugin for Fluent event collector

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.3.0-1
- Auto-upgrade to 5.3.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.2.2-1
- Update to v5.2.2.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 4.0.7-1
- License verified
- Original version for CBL-Mariner