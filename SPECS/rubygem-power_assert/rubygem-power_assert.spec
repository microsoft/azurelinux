%global gem_name power_assert
Summary:        Power Assert for Ruby
Name:           rubygem-%{gem_name}
Version:        2.0.3
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/power_assert/
Source0:        https://github.com/ruby/power_assert/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  ruby

# This package used to be bundled with older versions of Ruby.
Obsoletes:      ruby <= 3.1.2-2%{?dist}

Provides:       rubygem(power_assert) = %{version}-%{release}

%description
Power Assert shows each value of variables and method calls in the expression.
It is useful for testing, providing which value wasn't correct when the
condition is not satisfied.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/BSDL
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.3-1
- Auto-upgrade to 2.0.3 - Azure Linux 3.0 - package upgrades

* Mon Oct 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-4
- Adding 'Obsoletes: ruby <= 3.1.2-2'.

* Wed Jul 06 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.1-3
- Added missing lib files

* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.1-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.1-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
