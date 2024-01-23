%global debug_package %{nil}
%global gem_name protocol-http
Summary:        Provides abstractions to handle HTTP protocols
Name:           rubygem-%{gem_name}
Version:        0.24.7
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/protocol-http
Source0:        https://github.com/socketry/protocol-http/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Provides abstractions for working with the HTTP protocol.

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
* Mon Jan 22 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.24.7-1
- Update to v0.24.7.

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.22.5-1
- Update to v0.22.5.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.17.0-1
- License verified
- Original version for CBL-Mariner
