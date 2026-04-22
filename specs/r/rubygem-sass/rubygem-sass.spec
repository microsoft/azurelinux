# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from sass-3.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sass

Name: rubygem-%{gem_name}
Version: 3.7.4
Release: 14%{?dist}
Summary: A powerful but elegant CSS compiler that makes CSS fun again
License: MIT
URL: http://sass-lang.com/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/sass/ruby-sass.git
# cd ruby-sass && git checkout 3.7.4
# tar czvf sass-3.7.4-tests.tgz test/ Rakefile
Source1: %{gem_name}-%{version}-tests.tgz

# Use listen as a depencency instead of sass-listen.
# sass-listen is a fork from original listen v3.0 branch to support Ruby <= 2.1.
# https://github.com/sass/ruby-sass/pull/65
Patch0: rubygem-sass-3.5.6-use-listen.patch
# Note that patches below are not going to be submitted upstream
# because rubygem-sass is obsoleted by the upstream
# Remove warnings for literal string being frozen in ruby3.4
Patch1: rubygem-sass-3.7.4-Remove-warnings-for-literal-string-being-frozen-in-r.patch
# Support caller format change in ruby3.4
Patch2: rubygem-sass-3.7.4-Support-caller-format-change-in-ruby3.4.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(listen)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Sass makes CSS fun again. Sass is an extension of CSS, adding
nested rules, variables, mixins, selector inheritance, and more.
It's translated to well-formatted, standard CSS using the
command line tool or a web-framework plugin.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -a 1

%gemspec_remove_dep -g sass-listen -s ../%{gem_name}-%{version}.gemspec
%gemspec_add_dep -g listen -s ../%{gem_name}-%{version}.gemspec
%patch 0 -p1
%patch 1 -p2
%patch 2 -p2

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Fix for rpmlint
find %{buildroot}%{gem_instdir}/bin -type f | \
  xargs sed -i 's|^#!/usr/bin/env ruby|#!/usr/bin/ruby|'

%check
cp -a test/ Rakefile .%{gem_instdir}
pushd .%{gem_instdir}

# Fix Minitest 5.19+ compatibility.
# The fix is not proposed upstream, because this package is deprecated.
grep -Rl MiniTest | xargs sed -i "/MiniTest::Test/ s/MiniTest/Minitest/"

ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/sass
%{_bindir}/sass-convert
%{_bindir}/scss
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/MIT-LICENSE
# Required on runtime from version.rb
%{gem_instdir}/REVISION
%{gem_instdir}/VERSION
%{gem_instdir}/VERSION_DATE
%{gem_instdir}/VERSION_NAME
%{gem_instdir}/bin
%{gem_instdir}/extra
%{gem_instdir}/init.rb
%{gem_libdir}
%{gem_instdir}/rails
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CODE_OF_CONDUCT.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 19 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.4-11
- Support ruby3.4 string literal being chilled
- Support ruby3.4 backtrace formatting change

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 04 2023 Vít Ondruch <vondruch@redhat.com> - 3.7.4-8
- Fix FTBFS due to Minitest 5.19+ incompatibility.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 30 15:48:14 CET 2020 Pavel Valena <pvalena@redhat.com> - 3.7.4-1
- Update to sass 3.7.4.
  Resolves: rhbz#1695981

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Pavel Valena <pvalena@redhat.com> - 3.7.3-1
- Update to Sass 3.7.3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 01 2018 Jun Aruga <jaruga@redhat.com> - 3.5.6-1
- Update to Sass 3.5.6.

* Mon May 28 2018 Adam Williamson <awilliam@redhat.com> - 3.4.25-4
- Backport fix for a parser error that affects bootstrap

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Jun Aruga <jaruga@redhat.com> - 3.4.25-1
- Update to Sass 3.4.25.

* Tue Feb 14 2017 Jun Aruga <jaruga@redhat.com> - 3.4.23-3
- Fix Fixnum/Bignum deprecated warning for Ruby 2.4.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Vít Ondruch <vondruch@redhat.com> - 3.4.23-1
- Update to Sass 3.4.23.

* Tue Apr 26 2016 Jun Aruga <jaruga@redhat.com> - 3.4.22-1
- Update to 3.4.22.
- Fix test suite for Ruby 2.3 compatibility. (rhbz#1308082)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Greg Hellings <greg.hellings@gmail.com> - 3.4.19-2
- Added explicit Provides for EPEL 7

* Mon Oct 12 2015 Vít Ondruch <vondruch@redhat.com> - 3.4.19-1
- Update to Sass 3.4.19.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 16 2014 Mo Morsi <mmorsi@redhat.com> - 3.4.4-1
- Update to 3.4.4
- Remove patch now included in upstream release

* Thu Jun 12 2014 Mo Morsi <mmorsi@redhat.com> - 3.3.8-1
- Update to latest upstream release
- Include patch updating test suite to minitest 5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Vít Ondruch <vondruch@redhat.com> - 3.2.14-1
- Update to sass 3.2.14.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.6-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to sass 3.2.6.
- Own extra and rails directories (rhbz#911648).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 3.2.3-2
- update to sass 3.2.3
- update changelog

* Thu Jul 26 2012 Vít Ondruch <vondruch@redhat.com> - 3.1.20-2
- Fix dependency rubygem(fssm) => rubygem(listen).

* Mon Jul 23 2012 Vít Ondruch <vondruch@redhat.com> - 3.1.20-1
- Update to sass 3.1.20.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.1.7-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Chris Lalancette <clalance@redhat.com> - 3.1.4-4
- Add patches to make sass work in Fedora

* Thu Jul 21 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.4-3
- changed ruby(fssm) dep to rubygem(fssm)

* Thu Jul 14 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.4-2
- corrected license, whitespace fixes

* Wed Jul 13 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.4-1
- Initial package
