%global debug_package %{nil}
%global gem_name async-http
Summary:        A HTTP client and server library
Name:           rubygem-%{gem_name}
Version:        0.63.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/async-http
Source0:        https://github.com/socketry/async-http/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-async
Requires:       rubygem-async-io
Requires:       rubygem-async-pool
Requires:       rubygem-protocol-http
Requires:       rubygem-protocol-http1
Requires:       rubygem-protocol-http2
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
An asynchronous client and server implementation of HTTP/1.0,
HTTP/1.1 and HTTP/2 including TLS. Support for streaming requests
and responses.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Jan 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.63.0-1
- Auto-upgrade to 0.63.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.56.5-1
- Update to v0.56.5.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 0.50.13-1
- License verified
- Original version for CBL-Mariner
