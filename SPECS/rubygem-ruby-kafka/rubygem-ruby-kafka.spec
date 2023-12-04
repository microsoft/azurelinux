%global debug_package %{nil}
%global gem_name ruby-kafka
Summary:        A Ruby client library for Apache Kafka
Name:           rubygem-%{gem_name}
Version:        1.5.1
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/zendesk/ruby-kafka
Source0:        https://github.com/zendesk/ruby-kafka/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-digest-crc
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A Ruby client library for Apache Kafka, a distributed log and message
bus. The focus of this library will be operational simplicity,
with logging and metrics that can make debugging issues easier.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.1-1
- Auto-upgrade to 1.5.1 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.4.0-1
- Update to v1.4.0.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
