%global gem_name faraday-httpclient
Summary:        Faraday adapter for HTTPClient
Name:           rubygem-%{gem_name}
Version:        2.0.1
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/lostisland/faraday-httpclient
Source0:        https://github.com/lostisland/faraday-httpclient/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem is a Faraday adapter for the HTTPClient library. Faraday is an HTTP client library that provides a common interface over many adapters. Every adapter is defined into its own gem. This gem defines the adapter for HTTPClient.

%prep
%autosetup -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license LICENSE
%{gemdir}

%changelog
* Wed Jan 31 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-1
- Upgrading to the latest version.
- Updated the license.

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
