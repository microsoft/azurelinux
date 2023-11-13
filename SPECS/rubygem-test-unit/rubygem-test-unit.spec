%global gem_name test-unit
Summary:        An xUnit family unit testing framework for Ruby
Name:           rubygem-%{gem_name}
Version:        3.6.1
Release:        1%{?dist}
License:        PSF AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://test-unit.github.io/
Source0:        https://github.com/test-unit/test-unit/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  ruby

Requires:       rubygem-power_assert

# This package used to be bundled with older versions of Ruby.
Obsoletes:      ruby <= 3.1.2-2%{?dist}

Provides:       rubygem(test-unit) = %{version}-%{release}

%description
Test::Unit (test-unit) is unit testing framework for Ruby, based on xUnit
principles. These were originally designed by Kent Beck, creator of extreme
programming software development methodology, for Smalltalk's SUnit. It allows
writing tests, checking results and automated testing in Ruby.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.6.1-1
- Auto-upgrade to 3.6.1 - Azure Linux 3.0 - package upgrades

* Mon Oct 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5.3-3
- Adding 'Obsoletes: ruby <= 3.1.2-2'.

* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.5.3-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.5.3-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
