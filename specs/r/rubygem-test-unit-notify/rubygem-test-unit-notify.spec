# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	gem_name	test-unit-notify
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Test::Unit::Notify - A test result notify extension for Test::Unit
Name:		rubygem-%{gem_name}
Version:	1.0.4
Release: 23%{?dist}
# https://github.com/test-unit/test-unit-notify/issues/2
# https://cutter.osdn.jp/reference/readme.html
# LGPL-2.1-or-later: overall
# LGPL-3.0-or-later OR GFDL-1.3-or-later OR CC-BY-SA-3.0:
#      kinotan icons (data/icons/kinotan)
# SPDX confirmed
License:	LGPL-2.1-or-later AND (LGPL-3.0-or-later OR GFDL-1.3-or-later OR CC-BY-SA-3.0)
URL:		https://test-unit.github.io/#test-unit-notify
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:	https://cutter.osdn.jp/reference/readme.html

Requires:	ruby(release)
BuildRequires:	ruby(release)
Requires:	ruby(rubygems) 
BuildRequires:	rubygems-devel 
BuildArch:	noarch

%description
Test::Unit::Notify - A test result notify extension for Test::Unit.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%autosetup -n %{gem_name}-%{version} -p1
mv ../%{gem_name}-%{version}.gemspec .

%build
gem build ./%{gem_name}-%{version}.gemspec
%gem_install

# Permission
find . -type f -print0 | xargs --null chmod go-w

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/
cp -p %SOURCE1 %{buildroot}%{gem_instdir}/kinotan-readme.html

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -f  \
	Gemfile \
	Rakefile \
	.yardopts \
	%{nil}

# No test suite available currently

%files
%dir	%{gem_instdir}
%{gem_instdir}/lib/
%{gem_instdir}/data/
%{gem_spec}

%license	%{gem_instdir}/README.md
%license	%{gem_instdir}/kinotan-readme.html
%doc	%{gem_instdir}/doc/

%files doc
%doc	%{gem_docdir}/
%doc	%{gem_instdir}/screenshot/

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.4-17
- SPDX migration
- modernize spec file

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.4-1
- 1.0.4

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3-1
- 1.0.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-1
- 1.0.1

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.0-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.0-1
- Initial package
