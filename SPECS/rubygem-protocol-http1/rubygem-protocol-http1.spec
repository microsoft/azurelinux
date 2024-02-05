%global debug_package %{nil}
%global gem_name protocol-http1
Summary:        A low level implementation of the HTTP/1 protocol
Name:           rubygem-protocol-http1
Version:        0.18.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/protocol-http1
Source0:        https://github.com/socketry/protocol-http1/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove-pem.patch
BuildRequires:  ruby
Requires:       rubygem-protocol-http
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Provides a low-level implementation of the HTTP/1 protocol.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Feb 01 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.18.0-1
- Update to v0.18.0

* Mon Aug 21 2023 Dallas Delaney <dadelan@microsoft.com> - 0.15.1-1
- Update to v0.15.1 to fix CVE-2023-38697

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.14.2-1
- Update to v0.14.2.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.11.1-1
- License verified
- Original version for CBL-Mariner
