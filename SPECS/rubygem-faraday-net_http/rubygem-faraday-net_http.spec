%global debug_package %{nil}
%global gem_name faraday-net_http
Summary:        Faraday adapter for Net::HTTP
Name:           rubygem-%{gem_name}
Version:        2.0.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/lostisland/faraday-net_http
Source0:        https://github.com/lostisland/faraday-net_http/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(faraday-net_http) = %{version}-%{release}
BuildArch:      noarch

%description
This gem is a Faraday adapter for the Net::HTTP library. Faraday is an HTTP client library that provides a common interface over many adapters. Every adapter is defined into it's own gem. This gem defines the adapter for Net::HTTP the HTTP library that's included into the standard library of Ruby.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.md file to buildroot from Source0
cp LICENSE.md %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.3-1
- License verified
- Original version for CBL-Mariner
