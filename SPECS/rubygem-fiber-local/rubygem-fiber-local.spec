%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fiber-local

Name:           rubygem-fiber-local
Version:        1.0.0
Release:        1%{?dist}
Summary:        A module to simplify fiber-local state
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.5.0

%description
Provides a class-level mixin to make fiber local state easy.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 1.0.0-1
-   Original version for CBL-Mariner.
-   License verified.
