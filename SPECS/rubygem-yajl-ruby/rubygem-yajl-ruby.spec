%global debug_package %{nil}
%global gem_name yajl-ruby
Summary:        A streaming JSON parsing and encoding library for Ruby
Name:           rubygem-yajl-ruby
Version:        1.4.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/brianmario/yajl-ruby
Source0:        https://github.com/brianmario/yajl-ruby/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
a C binding to the YAJL JSON parsing and generation library.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.1-1
- Auto-upgrade to 1.4.1 - Azure Linux 3.0 - package upgrades

* Tue Aug 23 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.3.1-2
- Fix CVE-2022-24795.

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.3.1-1
- Downgrade to v1.3.1.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.4.1-1
- License verified
- Original version for CBL-Mariner
