%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fiber-local
Summary:        A module to simplify fiber-local state
Name:           rubygem-fiber-local
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/fiber-local
#Source0:        https://github.com/socketry/fiber-local/archive/refs/tags/v%{version}.tar.gz
Source0:        %{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
Provides a class-level mixin to make fiber local state easy.

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
* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner