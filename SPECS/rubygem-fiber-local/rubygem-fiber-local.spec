%global debug_package %{nil}
%global gem_name fiber-local
Summary:        A module to simplify fiber-local state
Name:           rubygem-fiber-local
Version:        1.0.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/fiber-local
Source0:        https://github.com/socketry/fiber-local/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Provides a class-level mixin to make fiber local state easy.

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
* Tue Jul 19 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-3
- Add provides, add missing files

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-2
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
