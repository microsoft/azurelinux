%global debug_package %{nil}
%global gem_name serverengine
Summary:        a framework to implement robust multiprocess servers like Unicorn
Name:           rubygem-%{gem_name}
Version:        2.3.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/treasure-data/serverengine
Source0:        https://github.com/treasure-data/serverengine/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-sigdump
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
a framework to implement robust multiprocess servers like Unicorn.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.3.2-1
- Auto-upgrade to 2.3.2 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.2.5-1
- Update to v2.2.5.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.2.1-1
- License verified
- Original version for CBL-Mariner
