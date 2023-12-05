%global debug_package %{nil}
%global gem_name prometheus-client
Summary:        Prometheus instrumentation library for Ruby applications
Name:           rubygem-%{gem_name}
Version:        4.2.1
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/prometheus/client_ruby
Source0:        https://github.com/prometheus/client_ruby/archive/refs/tags/v%{version}.tar.gz#/client_ruby-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A suite of instrumentation metric primitives for Ruby that can be exposed through a HTTP interface.
Intended to be used together with a Prometheus server.

%prep
%setup -q -n client_ruby-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.2.1-1
- Auto-upgrade to 4.2.1 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 4.0.0-1
- Update to v4.0.0.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.9.0-1
- License verified
- Original version for CBL-Mariner
