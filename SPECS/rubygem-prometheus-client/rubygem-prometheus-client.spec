%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name prometheus-client

Name:           rubygem-prometheus-client
Version:        0.9.0
Release:        1%{?dist}
Summary:        Prometheus instrumentation library for Ruby applications 
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
A suite of instrumentation metric primitives for Ruby that can be exposed through a HTTP interface. 
Intended to be used together with a Prometheus server.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 0.9.0-1
-   Original version for CBL-Mariner.
-   License verified.
