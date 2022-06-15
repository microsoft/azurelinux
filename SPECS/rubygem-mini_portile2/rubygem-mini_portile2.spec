%global debug_package %{nil}
%global gem_name mini_portile2
Summary:        Simplistic port-like solution for developers
Name:           rubygem-mini_portile2
Version:        2.8.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/flavorjones/mini_portile
Source0:        https://github.com/flavorjones/mini_portile/archive/refs/tags/v%{version}.tar.gz#/mini_portile-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This project is a minimalistic implementation of a port/recipe system for developers.

%prep
%setup -q -n mini_portile-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.txt file to buildroot from Source0
cp LICENSE.txt %{buildroot}%{gem_instdir}/
#add lib and test folders to buildroot from Source0
cp -r lib/ %{buildroot}%{gem_instdir}/
cp -r test/ %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.5.0-1
- License verified
- Original version for CBL-Mariner
