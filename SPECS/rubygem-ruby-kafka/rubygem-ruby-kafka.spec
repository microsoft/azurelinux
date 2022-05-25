%global debug_package %{nil}
%global gem_name ruby-kafka
Summary:        A Ruby client library for Apache Kafka
Name:           rubygem-%{gem_name}
Version:        1.4.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/zendesk/ruby-kafka
Source0:        https://github.com/zendesk/ruby-kafka/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-digest-crc

%description
A Ruby client library for Apache Kafka, a distributed log and message
bus. The focus of this library will be operational simplicity,
with logging and metrics that can make debugging issues easier.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.txt file to buildroot from Source0
cp LICENSE.txt %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
