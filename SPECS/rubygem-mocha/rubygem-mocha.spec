%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mocha
Summary:        Mocking and stubbing library
Name:           rubygem-mocha
Version:        1.13.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://mocha.jamesmead.org/
Source0:        https://github.com/freerange/mocha/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
BuildArch:      noarch

%description
Mocking and stubbing library with JMock/SchMock syntax, which allows mocking
and stubbing of methods on real (non-mock) classes.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add MIT-LICENSE.md and COPYING.md files to buildroot from Source0
cp MIT-LICENSE.md %{buildroot}%{gem_instdir}/
cp COPYING.md %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/MIT-LICENSE.md
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING.md
%{gemdir}

%changelog
* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.0-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
