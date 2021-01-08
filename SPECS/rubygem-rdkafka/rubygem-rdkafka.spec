%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rdkafka

Name:           rubygem-rdkafka
Version:        0.7.0
Release:        1%{?dist}
Summary:        Modern Kafka client library for Ruby based on librdkafka
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
Patch0:         librdkafka.patch
BuildRequires:  ruby > 2.1.0
BuildRequires:  rubygem-mini_portile2
BuildRequires:  librdkafka1
BuildRequires:  librdkafka-devel
BuildRequires:  git
Requires:       rubygem-mini_portile2
Requires:       rubygem-rake

%description
The rdkafka gem is a modern Kafka client library for Ruby based on librdkafka. 
It wraps the production-ready C client using the ffi gem and targets Kafka 1.0+ and Ruby 2.4+.

%prep
%setup -q -c -T
cp %{SOURCE0} .
gem unpack %{SOURCE0}
cd %{gem_name}-%{version}
patch -p1 < %{PATCH0}
gem build ./rdkafka.gemspec

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} ./%{gem_name}-%{version}/%{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 0.7.0-1
-   Original version for CBL-Mariner.
-   License verified.
