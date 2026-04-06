# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name mocha

Name: rubygem-%{gem_name}
Version: 2.6.1
Release: 4%{?dist}
Summary: Mocking and stubbing library
License: Ruby OR BSD-2-Clause OR MIT
URL: https://mocha.jamesmead.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/freerange/mocha.git && cd mocha
# git archive -v -o mocha-2.6.1-test.tar.gz v2.6.1 test/
Source1: %{gem_name}-%{version}-test.tar.gz
# Use single quote instead of backtick for Ruby 3.4 compatibility
# https://github.com/freerange/mocha/pull/688
Patch0: rubygem-mocha-2.6.1-Support-single-quote-instead-of-backtick-for-Ruby-3.4.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(introspection)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%global __requires_exclude ruby2_keywords

%description
Mocking and stubbing library with JMock/SchMock syntax, which allows mocking
and stubbing of methods on real (non-mock) classes.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

pushd %{builddir}
%patch 0 -p1
popd

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/test .

# Each part of test suite must be run separately, otherwise the test suite fails.
# https://github.com/freerange/mocha/issues/121
for kind in unit acceptance; do
  ruby -e "Dir.glob('./test/$kind/**/*_test.rb').each {|t| require t}"
done

MOCHA_RUN_INTEGRATION_TESTS=minitest ruby -rminitest -e "Dir.glob('./test/integration/**/minitest_test.rb').each {|t| require t}"
MOCHA_RUN_INTEGRATION_TESTS=test-unit ruby -rtest/unit -e "Dir.glob('./test/integration/**/test_unit_test.rb').each {|t| require t}"
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/COPYING.md
%license %{gem_instdir}/MIT-LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/RELEASE.md
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles/
%{gem_instdir}/mocha.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Vít Ondruch <vondruch@redhat.com> - 2.6.1-2
- Use single quote instead of backtick for Ruby 3.4 compatibility

* Tue Dec 03 2024 Vít Ondruch <vondruch@redhat.com> - 2.6.1-1
- Update to Mocha 2.6.1.
  Resolves: rhbz#2274314

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 Vít Ondruch <vondruch@redhat.com> - 2.1.0-1
- Update to Mocha 2.1.0.
  Resolves: rhbz#2135833

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.0-2
- Backport upstream fix for ruby3.2 Object#=~ removal

* Tue Oct 11 2022 Vít Ondruch <vondruch@redhat.com> - 1.15.0-1
- Update to Mocha 1.1.0.
  Resolves: rhbz#1778907

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 09 2019 Pavel Valena <pvalena@redhat.com> - 1.9.0-1
- Update to mocha 1.9.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Update to Mocha 1.1.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.14.0-1
- Update to 0.14.0
- Run unit and acceptance tests in a single process
- Patch test suite to work outside rake/bundler

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.13.1-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Vít Ondruch <vondruch@redhat.com> - 0.13.1-1
- Updated to the Mocha 0.13.1.

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.12.1-1
- Update to Mocha 0.12.1, as this version is needed by ActionPack 3.2.6 tests.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.11.0-1
- Updated to the Mocha 0.11.0.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.10.0-3
- Rebuild for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.10.0-1
- Updated to the Mocha 0.10.0.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 29 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.9.8-1
- Fixed odd naming in BR
- Updating to 0.9.8
- Breaking into -doc package as well
- Adding tests

* Thu Jul 23 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.7-1
- New upstream version

* Mon Apr 27 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.5-1
- New upstream version

* Sun Feb 01 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-4
- Mark files as %%doc

* Thu Oct 30 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-3
- Use gem instead of tgz

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-2
- Fix license

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-1
- New upstream version
- Fix license not being marked as %%doc

* Mon Sep 08 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.0-2
- Add ruby(abi) = 1.8 requirement

* Sat Aug 23 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.0-1
- New upstream version
- Initial package for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 0.5.6-1
- Initial package
