# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name activesupport

#%%global prerelease 

Name: rubygem-%{gem_name}
Epoch: 1
Version: 8.0.2
Release: 3%{?dist}
Summary: A support libraries and Ruby core extensions extracted from the Rails framework
License: MIT
URL: https://rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# git clone http://github.com/rails/rails.git && cd rails/activesupport
# git archive -v -o activesupport-8.0.2-tests.tar.gz v8.0.2 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.tar.gz
# This is needed due to `force_skip` alias.
# https://github.com/rails/rails/blob/main/tools/test_common.rb
Source2: https://raw.githubusercontent.com/rails/rails/e25d738430bdc6bdd04cd28be705484ea953e74e/tools/test_common.rb

# Ruby package has just soft dependency on rubygem(json), while
# ActiveSupport always requires it.
Requires: rubygem(json)

# Runtime dependency, lot of build failures in other packages.
# https://fedoraproject.org/wiki/Changes/AllowRemovalOfTzdata
Requires: tzdata

# Let's keep Requires and BuildRequires sorted alphabeticaly
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 3.2.0
BuildRequires: rubygem(bigdecimal)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(concurrent-ruby)
BuildRequires: rubygem(connection_pool)
BuildRequires: rubygem(dalli)
BuildRequires: rubygem(drb)
BuildRequires: rubygem(i18n) >= 0.7
BuildRequires: rubygem(listen)
BuildRequires: rubygem(minitest) >= 5.0.0
BuildRequires: rubygem(msgpack)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(redis)
BuildRequires: rubygem(rexml)
BuildRequires: rubygem(tzinfo) >= 2.0
BuildRequires: memcached
%ifnarch %{ix86}
BuildRequires: %{_bindir}/valkey-server
%endif
BuildRequires: tzdata
BuildArch: noarch

%description
A toolkit of support libraries and Ruby core extensions extracted from the
Rails framework. Rich support for multibyte strings, internationalization,
time zones, and testing.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}%{?prerelease} -b1

%build
gem build ../%{gem_name}-%{version}%{?prerelease}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
( cd .%{gem_instdir}
# Move the tests into place
cp -a %{builddir}/test .

mkdir ../tools
ln -s %{SOURCE2} ../tools/
touch ../tools/strict_warnings.rb

sed -i '/require .bundler./ s/^/#/' test/abstract_unit.rb

# Start a testing Valkey (Redis) server instance
%ifnarch %{ix86}
VALKEY_DIR=$(mktemp -d)
valkey-server --dir $VALKEY_DIR --pidfile $VALKEY_DIR/valkey.pid --daemonize yes
%endif

# Start Memcached server
memcached &
mPID=$!
sleep 1

ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)' -- -v

# Shutdown Memcached
kill -15 $mPID

# Shutdown Valkey.
%ifnarch %{ix86}
kill -INT $(cat $VALKEY_DIR/valkey.pid)
%endif
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.rdoc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 02 2025 Vít Ondruch <vondruch@redhat.com> - 1:8.0.2-1
- Update to Active Support 8.0.2.
  Related: rhbz#2238177

* Thu Jan 23 2025 Vít Ondruch <vondruch@redhat.com> - 1:7.0.8-11
- Fix compatibility with concurrent-ruby 1.3.5+

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 26 2024 Vít Ondruch <vondruch@redhat.com> - 1:7.0.8-9
- Add extracted standard gems dependencies.

* Mon Nov 04 2024 Vít Ondruch <vondruch@redhat.com> - 1:7.0.8-8
- Ruby 3.4 compatibility fixes.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 24 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:7.0.8-6
- Backport upstream fix for test failure wrt ruby side
  Object#dup behavior change

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Vít Ondruch <vondruch@redhat.com> - 1:7.0.8-3
- Add explicit dependencies to avoid Ruby 3.3 warnings.

* Sun Sep 24 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.8-2
- Add tzdata as a runtime dependency.

* Sun Sep 10 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.8-1
- Update to activesupport 7.0.8.

* Mon Aug 28 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.7.2-1
- Update to activesupport 7.0.7.2.

* Thu Aug 10 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.7-1
- Update to activesupport 7.0.7.

* Sun Jul 23 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.6-1
- Update to activesupport 7.0.6.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.5-1
- Update to activesupport 7.0.5.

* Tue Mar 14 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.4.3-1
- Update to activesupport 7.0.4.3.

* Wed Jan 25 2023 Pavel Valena <pvalena@redhat.com> - 1:7.0.4.2-1
- Update to activesupport 7.0.4.2.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:7.0.4-2
- Backport upstream fix for test failure with ruby3.2 wrt class_serial removal

* Thu Sep 15 2022 Pavel Valena <pvalena@redhat.com> - 1:7.0.4-1
- Update to activesupport 7.0.4.

* Tue Aug 02 2022 Vít Ondruch <vondruch@redhat.com> - 1:7.0.2.3-3
- Fix Minitest 5.16+ compatibility.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavel Valena <pvalena@redhat.com> - 1:7.0.2.3-1
- Update to activesupport 7.0.2.3.

* Wed Feb 09 2022 Pavel Valena <pvalena@redhat.com> - 1:7.0.2-1
- Update to activesupport 7.0.2.

* Thu Feb 03 2022 Pavel Valena <pvalena@redhat.com> - 1:7.0.1-1
- Update to activesupport 7.0.1.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 1:6.1.4.1-1
- Update to activesupport 6.1.4.1.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Pavel Valena <pvalena@redhat.com> - 1:6.1.4-1
- Update to activesupport 6.1.4.

* Tue May 18 2021 Pavel Valena <pvalena@redhat.com> - 1:6.1.3.2-1
- Update to activesupport 6.1.3.2.

* Fri Apr 09 2021 Pavel Valena <pvalena@redhat.com> - 1:6.1.3.1-1
- Update to activesupport 6.1.3.1.

* Thu Feb 18 2021 Pavel Valena <pvalena@redhat.com> - 1:6.1.3-1
- Update to activesupport 6.1.3.

* Mon Feb 15 2021 Pavel Valena <pvalena@redhat.com> - 1:6.1.2.1-1
- Update to activesupport 6.1.2.1.

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 1:6.1.1-1
- Update to activesupport 6.1.1.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Vít Ondruch <vondruch@redhat.com> - 1:6.0.3.4-2
- Fix FTBFS due to Ruby 3.0 update.

* Thu Oct  8 10:45:37 CEST 2020 Pavel Valena <pvalena@redhat.com> - 1:6.0.3.4-1
- Update to activesupport 6.0.3.4.
  Resolves: rhbz#1886136

* Fri Sep 18 17:58:30 CEST 2020 Pavel Valena <pvalena@redhat.com> - 1:6.0.3.3-1
- Update to activesupport 6.0.3.3.
  Resolves: rhbz#1877502

* Thu Sep 10 08:42:03 GMT 2020 Vít Ondruch <vondruch@redhat.com> - 1:6.0.3.2-3
- Fix evaluator test from web-console.

* Tue Sep 01 2020 Vít Ondruch <vondruch@redhat.com> - 1:6.0.3.2-2
- Properly fix flaky `FileStoreTest#test_filename_max_size` test case.

* Mon Aug 17 04:41:17 GMT 2020 Pavel Valena <pvalena@redhat.com> - 1:6.0.3.2-1
- Update to activesupport 6.0.3.2.
  Resolves: rhbz#1742797

* Mon Aug 03 07:01:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.1-1
- Update to ActiveSupport 6.0.3.1.
  Resolves: rhbz#1742797

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 16 2020 Vít Ondruch <vondruch@redhat.com> - 1:5.2.3-4
- Ruby 2.7 compatibility.
  Resolves: rhbz#1799093
- TZInfo 2.0 compatibility.
  Resolves: rhbz#1805531

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Pavel Valena <pvalena@redhat.com> - 1:5.2.3-1
- Update to Active Support 5.2.3.

* Thu Mar 14 2019 Pavel Valena <pvalena@redhat.com> - 1:5.2.2.1-1
- Update to Active Support 5.2.2.1.

* Mon Feb 04 2019 Vít Ondruch <vondruch@redhat.com> - 1:5.2.2-3
- Fix Range and BigDecimal compatibility with Ruby 2.6.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Pavel Valena <pvalena@redhat.com> - 1:5.2.2-1
- Update to Active Support 5.2.2.

* Wed Nov 14 2018 Vít Ondruch <vondruch@redhat.com> - 1:5.2.1-2
- Update I18n fallbacks configuration to be compatible with i18n 1.1.0.

* Wed Aug 08 2018 Pavel Valena <pvalena@redhat.com> - 1:5.2.1-1
- Update to Active Support 5.2.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 23 2018 Pavel Valena <pvalena@redhat.com> - 1:5.2.0-1
- Update to Active Support 5.2.0.

* Mon Apr 16 2018 Vít Ondruch <vondruch@redhat.com> - 1:5.1.5-3
- Fix test suite issue caused by fix of CVE-2018-6914 in Ruby.

* Wed Feb 21 2018 Pavel Valena <pvalena@redhat.com> - 1:5.1.5-2
- Allow rubygem-i18n ~> 1.0
  https://github.com/rails/rails/pull/31991

* Fri Feb 16 2018 Pavel Valena <pvalena@redhat.com> - 1:5.1.5-1
- Update to Active Support 5.1.5.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Vít Ondruch <vondruch@redhat.com> - 1:5.1.4-2
- Fix MiniTest 5.11 compatibility.

* Mon Sep 11 2017 Pavel Valena <pvalena@redhat.com> - 1:5.1.4-1
- Update to Active Support 5.1.4.

* Tue Aug 22 2017 Vít Ondruch <vondruch@redhat.com> - 1:5.1.3-2
- Explicitly require rubygem(json).
- Once again disable unstable test.

* Tue Aug 08 2017 Pavel Valena <pvalena@redhat.com> - 1:5.1.3-1
- Update to Active Support 5.1.3.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Pavel Valena <pvalena@redhat.com> - 1:5.1.2-1
- Update to Active Support 5.1.2.
- Run tests that need memcached

* Mon May 22 2017 Pavel Valena <pvalena@redhat.com> - 1:5.1.1-1
- Update to Active Support 5.1.1.

* Thu Mar 02 2017 Pavel Valena <pvalena@redhat.com> - 1:5.0.2-1
- Update to Active Support 5.0.2.

* Mon Feb 13 2017 Jun Aruga <jaruga@redhat.com> - 1:5.0.1-4
- Fix Fixnum/Bignum deprecated warning for Ruby 2.4.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Jun Aruga <jaruga@redhat.com> - 1:5.0.1-2
- Fix Ruby 2.4.0 compatibility.

* Mon Jan 02 2017 Pavel Valena <pvalena@redhat.com> - 1:5.0.1-1
- Update to Active Support 5.0.1.
  - Remove Patch0: rubygem-activesupport-5.0.0-Do-not-depend-on-Rails-git-repository-layout-in-Acti.patch; subsumed
- Fix warnings: Fixnum and Bignum are deprecated in Ruby trunk

* Mon Aug 15 2016 Pavel Valena <pvalena@redhat.com> - 1:5.0.0.1-1
- Update to Activesupport 5.0.0.1

* Wed Jul 27 2016 Vít Ondruch <vondruch@redhat.com> - 1:5.0.0-2
- Fix missing epoch in -doc subpackage.

* Fri Jul 01 2016 Vít Ondruch <vondruch@redhat.com> - 1:5.0.0-1
- Update to ActiveSupport 5.0.0.

* Fri Apr 08 2016 Vít Ondruch <vondruch@redhat.com> - 1:4.2.6-2
- Explicitly set rubygem(bigdecimal) dependency.

* Tue Mar 08 2016 Pavel Valena <pvalena@redhat.com> - 1:4.2.6-1
- Update to activesupport 4.2.6

* Tue Mar 01 2016 Pavel Valena <pvalena@redhat.com> - 1:4.2.5.2-1
- Update to activesupport 4.2.5.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Pavel Valena <pvalena@redhat.com> - 1:4.2.5.1-1
- Update to activesupport 4.2.5.1

* Wed Nov 18 2015 Pavel Valena <pvalena@redhat.com> - 1:4.2.5-1
- Update to activesupport 4.2.5

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.4-1
- Update to activesupport 4.2.4

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.3-1
- Update to activesupport 4.2.3

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.2-1
- Update to activesupport 4.2.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.1-2
- Fix tests

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.1-1
- Update to activesupport 4.2.1

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.0-1
- Update to activesupport 4.2.0

* Tue Aug 19 2014 Josef Stribny <jstribny@redhat.com> - 4.1.5-1
- Update to activesupport 4.1.5

* Fri Jul 04 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.4-1
- Update to ActiveSupport 4.1.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.1-1
- Update to ActiveSupport 4.1.1

* Thu Apr 17 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.0-1
- Update to ActiveSupport 4.1.0

* Wed Feb 26 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.3-1
- Update to ActiveSupport 4.0.3

* Thu Dec 05 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-1
- Update to ActiveSupport 4.0.2

* Fri Aug 09 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.1-1
- Update to ActiveSupport 4.0.1

* Fri Aug 09 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.0-2
- Fix: add minitest to requires

* Tue Jul 30 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.0-1
- Update to ActiveSupport 4.0.0.

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.13-1
- Update to ActiveSupport 3.2.13.

* Fri Mar 01 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Feb 12 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-1
- Update to ActiveSupport 3.2.12.

* Wed Jan 09 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.11-1
- Update to ActiveSupport 3.2.11.

* Thu Jan 03 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.10-1
- Update to ActiveSupport 3.2.10.

* Mon Aug 13 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.8-1
- Update to ActiveSupport 3.2.8.

* Mon Jul 30 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.7-1
- Update to ActiveSupport 3.2.7.

* Wed Jul 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.2.6-1
- Update to ActiveSupport 3.2.6.
- Removed unneeded BuildRoot tag.
- Tests no longer fail with newer versions of Mocha, remove workaround.

* Fri Jun 15 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.15-1
- Update to ActiveSupport 3.0.15.

* Fri Jun 01 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.13-1
- Update to ActiveSupport 3.0.13.

* Wed Apr 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-5
- Add the bigdecimal dependency to gemspec.

* Fri Mar 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-4
- The CVE patch name now contains the CVE id.

* Mon Mar 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-3
- Patch for CVE-2012-1098

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-1
- Rebuilt for Ruby 1.9.3.
- Update to ActiveSupport 3.0.11.

* Mon Aug 22 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.10-1
- Update to ActiveSupport 3.0.10

* Fri Jul 01 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.9-1
- Update to ActiveSupport 3.0.9
- Changed %%define into %%global
- Removed unnecessary %%clean section

* Thu Jun 16 2011 Mo Morsi <mmorsi@redhat.com> - 1:3.0.5-3
- Reverting accidental change adding a few gem flags

* Thu Jun 16 2011 Mo Morsi <mmorsi@redhat.com> - 1:3.0.5-2
- Include fix for CVE-2011-2197

* Thu Mar 24 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.5-1
- Update to ActiveSupport 3.0.5
- Remove Rake dependnecy

* Mon Feb 14 2011 Mohammed Morsi <mmorsi@redhat.com> - 1:3.0.3-4
- fix bad dates in the spec changelog

* Thu Feb 10 2011 Mohammed Morsi <mmorsi@redhat.com> - 1:3.0.3-3
- include i18n runtime dependency

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Mohammed Morsi <mmorsi@redhat.com> - 1:3.0.3-1
- update to rails 3

* Wed Aug 25 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-2
- bumped version

* Wed Aug 04 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8
- Added check section with rubygem-mocha dependency
- Added upsteam Rakefile and test suite to run tests

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Mon Sep 7 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4 (bug 520843, CVE-2009-3009)

* Sun Jul 26 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.3-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.2.2-1
- New upstream version

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-1
- New version (fixes CVE-2008-4094)

* Thu Jul 31 2008 Michael Stahnke <stahnma@fedoraproject.org> - 2.1.0-1
- New Upstream

* Mon Apr 07 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-1
- New version

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 2.0.1-1
- New version

* Wed Nov 28 2007 David Lutterkort <dlutter@redhat.com> - 1.4.4-3
- Fix buildroot

* Tue Nov 13 2007 David Lutterkort <dlutter@redhat.com> - 1.4.4-2
- Install README and CHANGELOG in _docdir

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.4.4-1
- Initial package
