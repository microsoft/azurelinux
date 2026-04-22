# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	gem_name minitest
# Use full EVR for provides
%global	__provides_exclude_from	%{gem_spec}

Summary:	Small and fast replacement for ruby's huge and slow test/unit

Name:		rubygem-%{gem_name}4
# With 4.7.5, some test fails, so for now use 4.7.0
Version:	4.7.0
Release: 28%{?dist}

License:	MIT
URL:		https://github.com/seattlerb/minitest
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# support ruby3.4 formatting change
Patch0:	minitest-4.7.0-ruby34-format.patch
BuildRequires:	rubygems-devel
BuildRequires:	ruby(release)
BuildArch:			noarch
Provides:			rubygem(%{gem_name}) = %{version}-%{release}
# Also provide this
Provides:			rubygem(%{gem_name}4) = %{version}-%{release}
Conflicts:			rubygem-minitest < 4.7.0-3

%description
minitest/unit is a small and fast replacement for ruby's huge and slow
test/unit. This is meant to be clean and easy to use both as a regular
test writer and for language implementors that need a minimal set of
methods to bootstrap a working unit test suite.

miniunit/spec is a functionally complete spec engine.

miniunit/mock, by Steven Baker, is a beautifully tiny mock object framework.

This is a compatibitity package for minitest version 4.x.y.

%package	doc
Summary:	Documentation for %{name}

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}
mv ../%{gem_name}-%{version}.gemspec .

# Fix for F-37
sed -i test/minitest/test_minitest_mock.rb \
	-e 's|assert_equal expected, e.message|assert_equal expected, e.message.lines(chomp: true)[0]|'
# Ruby 3.2 removes already deprecated Fixnum
sed -i test/minitest/test_minitest_mock.rb \
	-e 's|Fixnum|Integer|'
# Ruby 3.2 removes Object#=~
sed -i test/minitest/test_minitest_unit.rb -e 's|\(test_refute_match_matcher_object\)|\1; skip|'
# Ruby 3.4 formatting change
%patch -P0 -p1

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

find %{buildroot}%{gem_instdir}/lib -type f | \
	xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/ruby.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{gem_instdir} -type f | \
	xargs chmod 0644

# Cleanup
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest}
rm -f %{buildroot}%{gem_cache}
rm -rf %{buildroot}%{gem_instdir}/{Rakefile,test/}

%check
pushd .%{gem_instdir}

# spec test suite is unstable.
# https://github.com/seattlerb/minitest/issues/257
mv test/minitest/test_minitest_spec.rb{,.ignore}

for f in test/minitest/test_*.rb
do
	ruby -Ilib:.:./test $f
done

%files
%doc	%{gem_instdir}/History.txt
%doc	%{gem_instdir}/Manifest.txt
%license	%{gem_instdir}/README.txt
%dir	%{gem_instdir}
%{gem_libdir}/
%{gem_spec}

%files doc
%{gem_instdir}/design_rationale.rb
%doc	%{gem_docdir}/

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 15 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-25
- Support ruby34 formatting change for testsuite

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct  8 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-20
- Fix test failure with ruby3.2 (wrt removal of Fixnum, Object#=~)

* Sun Jul 24 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-19
- Fix FTBFS on F-37

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-4
- rpmlint fix
- Filter out redundant Provides
- Add Conflicts for older rubygem-minitest

* Mon Jun  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-3
- Rename to rubygem-minitest4
- Bump release number

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Josef Stribny <jstribny@redhat.com> - 4.7.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to minitest 4.7.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.10.1-1
- 2.10.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.6.0-3
- Removed Rake circular dependency.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-1
- Update to 1.6.0 (#586505)
- Patch0 removed

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-3
- Drop Requires on hoe, only used by Rakefile (#538303).
- Move Rakefile to -doc (#538303).

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-2
- Better Source (#538303).
- More standard permissions on files.

* Tue Nov 17 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-1
- Initial package
