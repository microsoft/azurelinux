%global debug_package %{nil}
%global gem_name protocol-http2
Summary:        A low level implementation of the HTTP/2 protocol
Name:           rubygem-%{gem_name}
Version:        0.15.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/protocol-http2
Source0:        https://github.com/socketry/protocol-http2/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-protocol-hpack
Requires:       rubygem-protocol-http
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Provides a low-level implementation of the HTTP/2 protocol.

%prep
%setup -q -n %{gem_name}-%{version}
%gemspec_clear_signing

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Feb 01 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.15.1-1
- Update to v0.15.1

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.14.2-1
- Update to v0.14.2.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.13.2-1
- License verified
- Original version for CBL-Mariner
