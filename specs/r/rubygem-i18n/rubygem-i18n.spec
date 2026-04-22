# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name i18n

%bcond_without tests

Name: rubygem-%{gem_name}
Version: 1.14.6
Release: 4%{?dist}
Summary: New wave Internationalization support for Ruby
# `BSD or Ruby` due to header of lib/i18n/gettext/po_parser.rb
License: MIT AND (BSD-2-Clause OR Ruby)
URL: https://github.com/ruby-i18n/i18n
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/ruby-i18n/i18n && cd i18n
# git archive -v -o i18n-1.14.6-tests.tar.xz v1.14.6 test
Source1: %{gem_name}-%{version}-tests.tar.xz
# Fix `NameError: uninitialized constant I18nLoadPathTest::Pathname` test
# errors.
# https://github.com/ruby-i18n/i18n/pull/708
Patch0: rubygem-i18n-1.14.6-Explicitly-require-pathname.patch
# Fix Ruby 3.4 `Hash#inspect` compatibility.
# https://github.com/ruby-i18n/i18n/pull/709
Patch1: rubygem-i18n-1.14.6-Ruby-3.4-Hash-inspect-compatibility.patch
Patch2: rubygem-i18n-1.14.6-Ruby-3.4-Hash-inspect-compatibility-test.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if %{with tests}
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(test_declarative)
BuildRequires: rubygem(concurrent-ruby)
BuildRequires: rubygem(activesupport)
BuildREquires: rubygem(racc)
%endif
BuildArch: noarch

%description
Ruby internationalization and localization solution.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

%patch 1 -p1

pushd %{builddir}
%patch 0 -p1
%patch 2 -p1
popd

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%if %{with tests}
%check
pushd .%{gem_instdir}
ln -s %{builddir}/test .

# Bundler just complicates everything in our case, remove it.
sed -i -e "/require 'bundler\/setup'/ s/^/#/" test/test_helper.rb

find ./test/ -type f -name '*_test.rb' | \
  xargs -n 1 ruby -Ilib:test
popd
%endif

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 09 2024 Vít Ondruch <vondruch@redhat.com> - 1.14.6-1
- Update to i18n 1.14.6.
  Resolves: rhbz#2268010

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-3
- Explicitly add rubygem(racc) for BuildRequires for %%check

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 07 2023 Vít Ondruch <vondruch@redhat.com> - 1.14.1-1
- Update to i18n 1.14.1.
  Resolves: rhbz#2054428

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jan 25 2022 Pavel Valena <pvalena@redhat.com> - 1.8.11-1
- Update to i18n 1.8.11.
  Resolves: rhbz#1923812

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Pavel Valena <pavel.valena@email.com> - 1.8.7-1
- Update to i18n 1.8.7.
  Resolves: rhbz#1911952

* Fri Oct 30 16:58:04 CET 2020 Pavel Valena <pvalena@redhat.com> - 1.8.5-1
- Update to i18n 1.8.5.
  Resolves: rhbz#1844286

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 22 2020 Vít Ondruch <vondruch@redhat.com> - 1.8.2-1
- Update to i18n 1.8.2.
  Resolves: rhbz#1788714

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Pavel Valena <pvalena@redhat.com> - 1.7.0-1
- Update to i18n 1.7.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.1-2
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Tue Nov 13 2018 Vít Ondruch <vondruch@redhat.com> - 1.1.1-1
- Update to i18n 1.1.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 16 2018 Pavel Valena <pvalena@redhat.com> - 1.0.0-1
- Update to i18n 1.0.0.
  Requires rubygem(concurrent-ruby)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.0-1
- Update to i18n 0.7.0.

* Tue Jul 22 2014 Josef Stribny <jstribny@redhat.com> - 0.6.11-1
- Update to i18n 0.6.11

* Wed Jun 18 2014 Josef Stribny <jstribny@redhat.com> - 0.6.9-4
- Fix test suite compatibility with minitest 5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 04 2014 Josef Stribny <jstribny@redhat.com> - 0.6.9-2
- Fix license: Ruby is now licensed under BSD or Ruby

* Mon Dec 09 2013 Vít Ondruch <vondruch@redhat.com> - 0.6.9-1
- Update to i18n 0.6.9.
  - Fix CVE-2013-4491.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Josef Stribny <jstribny@redhat.com> - 0.6.4-1
- Update to i18n 0.6.4.

* Tue Feb 26 2013 Vít Ondruch <vondruch@redhat.com> - 0.6.1-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Vít Ondruch <vondruch@redhat.com> - 0.6.1-1
- Update to I18n 0.6.1.

* Wed Jul 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-1
- Update to I18n 0.6.0.
- Removed unneeded %%defattr usage.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.5.0-3
- Rebuilt for Ruby 1.9.3.
- Enabled test suite.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 24 2011 Vít Ondruch <vondruch@redhat.com> - 0.5.0-1
- Update to i18n 0.5.0.
- Documentation moved into subpackage.
- Removed unnecessary cleanup.
- Preparetion for test suite execution during build.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.4.2-2
- Add GPLv2 or Ruby License
- Files MIT-LICENSE, geminstdir/lib/i18n.rb are non executable now

* Thu Nov 11 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.4.2-1
- Initial package
