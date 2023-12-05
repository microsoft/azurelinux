%global debug_package %{nil}
%global gem_name digest-crc
Summary:        A Cyclic Redundancy Check (CRC) library for Ruby.
Name:           rubygem-digest-crc
Version:        0.6.5
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/postmodern/digest-crc
Source0:        https://github.com/postmodern/digest-crc/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-rake < 14.0.0
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Adds support for calculating Cyclic Redundancy Check (CRC) to the Digest module.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.6.5-1
- Auto-upgrade to 0.6.5 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.6.4-1
- Update to v0.6.4.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.6.1-1
- License verified
- Original version for CBL-Mariner
