%global debug_package %{nil}
%global gem_name async-io
Summary:        Concurrent wrappers for native Ruby IO & Sockets
Name:           rubygem-%{gem_name}
Version:        1.35.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/async-io
Source0:        https://github.com/socketry/async-io/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-async
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Async::IO provides builds on async and provides asynchronous
wrappers for IO, Socket, and related classes.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.35.0-1
- Auto-upgrade to 1.35.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.33.0-1
- Update to v1.33.0.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.30.1-1
- License verified
- Original version for CBL-Mariner
