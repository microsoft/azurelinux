# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from pg-0.11.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name pg

Name: rubygem-%{gem_name}
Version: 1.6.1
Release: 2%{?dist}
Summary: Pg is the Ruby interface to the PostgreSQL RDBMS
License: (BSD-2-Clause OR Ruby) AND PostgreSQL
URL: https://github.com/ged/ruby-pg
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/ged/ruby-pg.git
# git archive -v -o pg-1.6.1-spec.tar.gz v1.6.1 spec/
Source1: %{gem_name}-%{version}-spec.tar.gz
# Disable RPATH.
# https://github.com/ged/ruby-pg/issues/183
Patch0: rubygem-pg-1.3.0-remove-rpath.patch
# lib/pg/text_{de,en}coder.rb
Requires: rubygem(json)
# This is optional dependency now.
# https://github.com/ged/ruby-pg/pull/556
Suggests: rubygem(bigdecimal)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc

BuildRequires: postgresql-server libpq-devel
# This is optional dependency now.
# https://github.com/ged/ruby-pg/pull/556
BuildRequires: rubygem(bigdecimal)
BuildRequires: rubygem(rspec)

%description
Pg is the Ruby interface to the PostgreSQL RDBMS. It works with PostgreSQL 10
and later.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%patch 0 -p1


%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/


%check
pushd .%{gem_instdir}
ln -s %{_builddir}/spec .

# Assign a random port to consider a case of multi builds in parallel in a host.
# https://github.com/ged/ruby-pg/pull/39
export PGPORT="$((54321 + ${RANDOM} % 1000))"
# Since RPM 4.20, the build path becomes too long and therefore the
# "Unix-domain socket path" hits the limit. Use some shorter path to prevent
# the issue (/tmp could be also possibility).
export RUBY_PG_TEST_DIR=%{_builddir}/tmp
# Set --verbose to show detail log by $VERBOSE.
# See https://github.com/ged/ruby-pg/blob/master/spec/helpers.rb $VERBOSE
if ! ruby -S --verbose rspec -I$(dirs +1)%{gem_extdir_mri} -f d spec -E "${EXAMPLE_MATCHES}"; then
  echo "==== [setup.log start ] ===="
  cat ${RUBY_PG_TEST_DIR}/tmp_test_specs/setup.log
  echo "==== [setup.log end ] ===="
  false
fi
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/BSDL
%license %{gem_instdir}/LICENSE
%license %{gem_instdir}/POSTGRES
%{gem_libdir}
%exclude %{gem_instdir}/ports
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/Contributors.rdoc
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README-OS_X.rdoc
%doc %{gem_instdir}/README-Windows.rdoc
%lang(ja) %doc %{gem_instdir}/README.ja.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/certs
%{gem_instdir}/misc
%{gem_instdir}/pg.gemspec
%{gem_instdir}/rakelib
%{gem_instdir}/sample

%changelog
* Tue Aug 12 2025 Vít Ondruch <vondruch@redhat.com> - 1.6.1-1
- Update to pg 1.6.1.
  Resolves: rhbz#2383782
  Resolves: rhbz#2385765

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 1.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Mon Nov 25 2024 Vít Ondruch <vondruch@redhat.com> - 1.5.9-2
- Fix test compatibility with Linux 6.10+.
  Resolves: rhbz#2324182

* Fri Nov 08 2024 Vít Ondruch <vondruch@redhat.com> - 1.5.9-1
- Update to pg 1.5.9.
  Resolves: rhbz#2310465

* Fri Nov 08 2024 Vít Ondruch <vondruch@redhat.com> - 1.5.7-2
- Disable some test cases failing with kernel 6.10+.

* Wed Aug 07 2024 Vít Ondruch <vondruch@redhat.com> - 1.5.7-1
- Update to pg 1.5.7.
  Resolves: rhbz#2264429

* Wed Aug 07 2024 Vít Ondruch <vondruch@redhat.com> - 1.5.4-5
- Fix FTBFS caused by RPM 4.20+ deeper nesting.
  Resolves: rhbz#2301255

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Mon Oct 23 2023 Jarek Prokop <jprokop@redhat.com> - 1.5.4-1
- Upgrade to pg 1.5.4.
  Resolves: rhbz#2173399

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Thu Dec 15 2022 Vít Ondruch <vondruch@redhat.com> - 1.4.5-1
- Update to pg 1.4.5.
  Resolves: rhbz#2099059

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 12 2022 Jarek Prokop <jprokop@redhat.com> - 1.3.5-1
- Update to pg 1.3.5.
  Resolves: rhbz#1814862

* Thu Feb 17 2022 Pavel Valena <pvalena@redhat.com> - 1.3.2-1
- Update to pg 1.3.2.
  Resolves: rhbz#1814862

* Fri Jan 28 2022 Vít Ondruch <vondruch@redhat.com> - 1.3.0-1
- Update to pg 1.3.0.
  Resolves: rhbz#1814862

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 1.2.3-5
- rebuild for libpq ABI fix rhbz#1908268

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 19 2020 Jun Aruga <jaruga@redhat.com> - 1.2.3-1
- Update to pg 1.2.3.

* Fri Mar 06 2020 Jun Aruga <jaruga@redhat.com> - 1.2.2-1
- Update to pg 1.2.2.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Vít Ondruch <vondruch@redhat.com> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.7

* Mon Jan 06 2020 Jun Aruga <jaruga@redhat.com> - 1.2.1-1
- Update to pg 1.2.1.

* Thu Jan 02 2020 Jun Aruga <jaruga@redhat.com> - 1.2.0-1
- Update to pg 1.2.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Thu Jan 10 2019 Vít Ondruch <vondruch@redhat.com> - 1.1.4-1
- Update to pg 1.1.4.

* Wed Jan 09 2019 Vít Ondruch <vondruch@redhat.com> - 1.1.3-2
- Fix PostgreSQL 11 compatibility.

* Tue Sep 18 2018 Jun Aruga <jaruga@redhat.com> - 1.1.3-1
- Update to pg 1.1.3.
- Update to output log when tests fail.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 13 2018 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Update to pg 1.0.0.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.21.0-4
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Vít Ondruch <vondruch@redhat.com> - 0.21.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.5

* Fri Dec 08 2017 Jun Aruga <jaruga@redhat.com> - 0.21.0-2
- Fix failed tests for PostgreSQL-10.

* Thu Aug 17 2017 Vít Ondruch <vondruch@redhat.com> - 0.21.0-1
- Update to pg 0.21.0.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Vít Ondruch <vondruch@redhat.com> - 0.20.0-1
- Update to pg 0.20.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.18.4-3
- F-26: rebuild for ruby24
- Patch from the upstream for test failure with integer unification

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Vít Ondruch <vondruch@redhat.com> - 0.18.4-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3
- Update to pg 0.18.4.

* Wed Aug 26 2015 Vít Ondruch <vondruch@redhat.com> - 0.18.2-1
- Update to pg 0.18.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.18.1-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Update to pg 0.18.1.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Vít Ondruch <vondruch@redhat.com> - 0.17.1-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Update to pg 0.17.1.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 0.14.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to pg 0.14.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 0.12.2-2
- Obsolete ruby-postgress, which was retired.

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 0.12.2-1
- Rebuilt for Ruby 1.9.3.
- Upgrade to pg 0.12.2.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-5
- Pass CFLAGS to extconf.rb.

* Fri Jun 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-4
- Binary extension moved into ruby_sitearch dir.
- -doc subpackage made architecture independent.

* Wed Jun 01 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-3
- Quoted upstream license clarification.

* Mon May 30 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-2
- Removed/fixed shebang in non-executables.
- Removed sources.

* Thu May 26 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-1
- Initial package
