%global debug_package %{nil}
%global gem_name rdkafka
Summary:        Modern Kafka client library for Ruby based on librdkafka
Name:           rubygem-%{gem_name}
Version:        0.15.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/appsignal/rdkafka-ruby
Source0:        https://github.com/appsignal/rdkafka-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  librdkafka-devel
BuildRequires:  librdkafka1
BuildRequires:  ruby
BuildRequires:  git
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
%gemspec_clear_signing
git init .
git add .

%build
gem build %{gem_name}

%install
export RDKAFKA_EXT_PATH="/usr/"
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license MIT-LICENSE
%{gemdir}

%changelog
* Mon Mar 25 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.15.1-1
- Upgrade to 0.15.1

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.12.0.beta.4-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.12.0.beta.4-1
- Update to v0.12.0.beta.4.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.7.0-1
- License verified
- Original version for CBL-Mariner
