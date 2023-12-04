%global debug_package %{nil}
%global gem_name fluent-plugin-kafka
Summary:        Kafka input and output plugin for Fluentd
Name:           rubygem-%{gem_name}
Version:        0.19.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-kafka
Source0:        https://github.com/fluent/fluent-plugin-kafka/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Patch0:         fix-file_list.patch
Requires:       rubygem-fluentd
Requires:       rubygem-ltsv
Requires:       rubygem-ruby-kafka < 2
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A fluentd plugin to both consume and produce data for Apache Kafka.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.19.0-1
- Auto-upgrade to 0.19.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.17.5-1
- Update to v0.17.5.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 0.13.0-1
- License verified
- Original version for CBL-Mariner
