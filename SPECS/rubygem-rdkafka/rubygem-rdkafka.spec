%global debug_package %{nil}
%global gem_name rdkafka
Summary:        Modern Kafka client library for Ruby based on librdkafka
Name:           rubygem-rdkafka
Version:        0.12.0.beta.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/appsignal/rdkafka-ruby
Source0:        https://github.com/appsignal/rdkafka-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
Patch0:         librdkafka.patch
BuildRequires:  git
BuildRequires:  librdkafka-devel
BuildRequires:  librdkafka1
BuildRequires:  ruby
BuildRequires:  rubygem-mini_portile2
BuildRequires:  rubygem-rake
Requires:       rubygem-mini_portile2
Requires:       rubygem-rake
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
The rdkafka gem is a modern Kafka client library for Ruby based on librdkafka.
It wraps the production-ready C client using the ffi gem and targets Kafka 1.0+ and Ruby 2.4+.

%prep
%setup -q -n rdkafka-ruby-%{version}
patch -p1 < %{PATCH0}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE file to buildroot from Source0
cp LICENSE %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.7.0-1
- License verified
- Original version for CBL-Mariner
