%global debug_package %{nil}
%global gem_name faraday
Summary:        HTTP/REST API client library
Name:           rubygem-faraday
Version:        2.7.10
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
AutoReq:        no

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

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.10-1
- Auto-upgrade to 2.7.10 - Azure Linux 3.0 - package upgrades

* Wed Sep 07 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.5.2-1
- Update to v2.5.2.

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.10.0-1
- Update to v1.10.0.
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.1.0-1
- License verified
- Original version for CBL-Mariner
