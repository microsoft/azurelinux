%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name test-unit
Summary:        An xUnit family unit testing framework for Ruby
Name:           rubygem-test-unit
Version:        3.5.3
Release:        1%{?dist}
License:        PSF AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://test-unit.github.io/
Source0:        https://github.com/test-unit/test-unit/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem(power_assert)

%description
Test::Unit (test-unit) is unit testing framework for Ruby, based on xUnit
principles. These were originally designed by Kent Beck, creator of extreme
programming software development methodology, for Smalltalk's SUnit. It allows
writing tests, checking results and automated testing in Ruby.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add BSDL, COPYING and PSFL files to buildroot from Source0
cp BSDL %{buildroot}%{gem_instdir}/
cp COPYING %{buildroot}%{gem_instdir}/
cp PSFL %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/BSDL
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING
%license %{gemdir}/gems/%{gem_name}-%{version}/PSFL
%{gemdir}

%changelog
* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.5.3-1
- License verified
- Original version for CBL-Mariner