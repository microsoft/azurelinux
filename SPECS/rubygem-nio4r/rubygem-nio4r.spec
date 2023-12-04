%global debug_package %{nil}
%global gem_name nio4r
Summary:        Cross-platform asynchronous I/O primitives for scalable network clients and servers
Name:           rubygem-%{gem_name}
Version:        2.5.9
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/nio4r
Source0:        https://github.com/socketry/nio4r/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
cross-platform asynchronous I/O primitives for scalable network clients and servers.
Modeled after the Java NIO API, but simplified for ease-of-use.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.5.9-1
- Auto-upgrade to 2.5.9 - Azure Linux 3.0 - package upgrades

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.5.8-1
- Update to v2.5.8.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 2.5.4-1
- License verified
- Original version for CBL-Mariner
