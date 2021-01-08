%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ruby-kafka

Name:           rubygem-ruby-kafka
Version:        1.0.0
Release:        1%{?dist}
Summary:        A Ruby client library for Apache Kafka
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.1.0
Requires:       rubygem-digest-crc

%description
A Ruby client library for Apache Kafka, a distributed log and message 
bus. The focus of this library will be operational simplicity, 
with good logging and metrics that can make debugging issues easier.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 1.0.0-1
-   Original version for CBL-Mariner.
-   License verified.
