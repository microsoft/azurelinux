%global debug_package %{nil}
%global gem_name semantic_puppet

Summary:        Useful tools for working with Semantic Versions
Name:           rubygem-%{gem_name}
Version:        1.1.0
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:	Mariner
URL:            https://github.com/puppetlabs/semantic_puppet
Source0:        https://github.com/puppetlabs/semantic_puppet/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Tools used by Puppet to parse, validate, and compare Semantic Versions and
Version Ranges and to query and resolve module dependencies.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gem_instdir}/lib
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.0-1
- Auto-upgrade to 1.1.0 - Azure Linux 3.0 - package upgrades

* Tue Jul 19 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.4-4
- Add provides, add missing files

* Tue May 03 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.4-3
- Add lib/ from source.

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.4-2
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.0.4-1
- Original version for CBL-Mariner
- License verified
