%global gem_name mocha
Summary:        Mocking and stubbing library
Name:           rubygem-mocha
Version:        1.13.0
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://mocha.jamesmead.org/
Source0:        https://github.com/freerange/mocha/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove-missing-devdeps.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(mocha) = %{version}-%{release}
BuildArch:      noarch

%description
Mocking and stubbing library with JMock/SchMock syntax, which allows mocking
and stubbing of methods on real (non-mock) classes.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

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
* Thu Apr 21 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.0-4
- Cleanup

* Thu Apr 21 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.0-3
- Adding patch to remove missing development_dependencies from .gemspec

* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.0-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.0-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
