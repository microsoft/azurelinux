%global debug_package %{nil}
%global gem_name faraday-httpclient
Summary:        Faraday adapter for HTTPClient
Name:           rubygem-%{gem_name}
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/lostisland/faraday-httpclient
Source0:        https://github.com/lostisland/faraday-httpclient/archive/refs/tags/v1.0.tar.gz#/%{gem_name}-1.0.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem is a Faraday adapter for the HTTPClient library. Faraday is an HTTP client library that provides a common interface over many adapters. Every adapter is defined into its own gem. This gem defines the adapter for HTTPClient.

%prep
%setup -q -n %{gem_name}-1.0

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
