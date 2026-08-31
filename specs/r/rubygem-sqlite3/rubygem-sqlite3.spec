# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name sqlite3

Name: rubygem-%{gem_name}
Version: 2.5.0
Release: 2%{?dist}
Summary: Allows Ruby scripts to interface with a SQLite3 database
License: BSD-3-Clause
URL: https://github.com/sparklemotion/sqlite3-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/sparklemotion/sqlite3-ruby.git && cd sqlite3-ruby
# git archive -v -o sqlite3-2.5.0-test.tar.gz v2.5.0 test/
Source1: %{gem_name}-%{version}-test.tar.gz
# Fix (s390x) big endian tees failure.
# https://github.com/sparklemotion/sqlite3-ruby/pull/616
Patch0: rubygem-sqlite3-2.5.0-fix-tests-pass-on-bigendian-architecture.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: sqlite-devel
BuildRequires: rubygem(minitest) >= 5.0.0
BuildRequires: gcc

%description
SQLite3/Ruby is a module to allow Ruby scripts to interface with a SQLite3
database.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

# Remove bundled SQLite right away.
rm -rf ports
%gemspec_remove_file "ports/archives/sqlite-autoconf-3470200.tar.gz"

( cd %{builddir}
%patch 0 -p1
)

# This is not really runtime dependency, neither it is needed by official
# prebuild platform specific packages.
%gemspec_remove_dep -g mini_portile2 "~> 2.8.0"

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# Build against system SQLite3.
CONFIGURE_ARGS="--enable-system-libraries"

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,sqlite3} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/test test

# Fedora SQLite does not support URI.
# https://github.com/sparklemotion/sqlite3-ruby/issues/611
mv test/test_database_uri.rb{,.disable}

ruby -I$(dirs +1)%{gem_extdir_mri}:lib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/FAQ.md
%doc %{gem_instdir}/INSTALLATION.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/dependencies.yml

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Feb 03 2025 Vít Ondruch <vondruch@redhat.com> - 2.5.0-1
- Update to SQLite3 2.5.0.
  Resolves: rhbz#2182100

* Thu Jan 30 2025 Vít Ondruch <vondruch@redhat.com> - 2.0.2-1
- Update to sqlite 2.0.2.
  Resolves: rhbz#2182100

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.6.1-7
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.1-5
- Backport upstream fix for test with sqlite 3.46 error message change

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Vít Ondruch <vondruch@redhat.com> - 1.6.1-1
- Update to sqlite 1.6.1.
  Resolves: rhbz#2096351

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 1.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 12 2022 Vít Ondruch <vondruch@redhat.com> - 1.4.2-9
- Fix compatibility with SQLite 3.37.0+.

* Wed Jan 26 2022 Vít Ondruch <vondruch@redhat.com> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2 (to make test pass for ruby 27)
- F-32: rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 27 2019 Vít Ondruch <vondruch@redhat.com> - 1.4.1-1
- Update to sqlite3 1.4.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 1.3.13-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Fri Jul 27 2018 Vít Ondruch <vondruch@redhat.com> - 1.3.13-9
- Add "BR: gcc" to fix FTBFS (rhbz#1606268).

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.13-7
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.13-6
- F-28: rebuild for ruby25

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Vít Ondruch <vondruch@redhat.com> - 1.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Thu Jan 05 2017 Vít Ondruch <vondruch@redhat.com> - 1.3.13-1
- Update to sqlite3 1.3.13.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Vít Ondruch <vondruch@redhat.com> - 1.3.11-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3
- Update to sqlite3 1.3.11.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 1.3.10-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Update to sqlite3 1.3.10.

* Tue Oct 07 2014 Josef Stribny <jstribny@redhat.com> - 1.3.9-3
- Fix: Big Endian for Power

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Josef Stribny <jstribny@redhat.com> - 1.3.9-1
- Update to sqlite3 1.3.9

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 1.3.8-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Update to 1.3.8

* Wed Nov 27 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.7-3
- Prevent dangling symlink in -debuginfo.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.7-1
- Update to sqlite3 1.3.7.
- Fix -doc license (rhbz#969963).

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.5-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.5-1
- Updated to sqlite3 1.3.5.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.4-3
- Rebuilt for Ruby 1.9.3.
- Drop ruby-sqlite3 subpackage.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.4-1
- Updated to sqlite3 1.3.4.
- Use the upstream big endian fix.

* Wed Jun 22 2011 Dan Horák <dan[at]danny.cz> - 1.3.3-5
- fix build on big endian arches (patch by Vít Ondruch)

* Fri Jun 03 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.3-4
- The subdirectory of ruby_sitearch has to be owned by package.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.3-2
- Updated links.
- Removed obsolete BuildRoot.
- Removed unnecessary cleanup.

* Wed Feb 02 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.3-1
- Package renamed from rubygem-sqlite3-ruby to rubygem-sqlite3.
- Test suite executed upon build.
- Documentation moved into separate package.
- Removed clean section which is not necessary.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-4
- F-12: Rebuild to create valid debuginfo rpm again (ref: #505774)

* Tue Jun 16 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-3
- Create ruby-sqlite3 as subpackage (ref: #472621, #472622)
- Use gem as source

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.2.4-1
- Fix items from review (#459881)
- New upstream version

* Sun Aug 31 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.2.2-2
- Fix items from review (#459881)

* Sun Jul 13 2008 Matt Hicks <mhicks@localhost.localdomain> - 1.2.2-1
- Initial package
