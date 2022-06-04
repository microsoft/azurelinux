%global gem_name power_assert
Summary:        Power Assert for Ruby
Name:           rubygem-%{gem_name}
Version:        2.0.1
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/power_assert/
Source0:        https://github.com/ruby/power_assert/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(power_assert) = %{version}-%{release}
BuildArch:      noarch

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
#add BSDL and COPYING files to buildroot from Source0
cp BSDL %{buildroot}%{gem_instdir}/
cp COPYING %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/BSDL
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING
%{gemdir}

%changelog
* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.1-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.1-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
