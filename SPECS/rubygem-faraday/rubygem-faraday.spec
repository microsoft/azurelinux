%global debug_package %{nil}
%global gem_name faraday
Summary:        HTTP/REST API client library
Name:           rubygem-faraday
Version:        1.10.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://lostisland.github.io/faraday/
Source0:        https://github.com/lostisland/faraday/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-multipart-post < 3
Requires:       rubygem-ruby2_keywords
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Faraday is an HTTP client library that provides a common interface over
many adapters (such as Net::HTTP) and embraces the concept of Rack middleware
when processing the request/response cycle.

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
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.1.0-1
- License verified
- Original version for CBL-Mariner
