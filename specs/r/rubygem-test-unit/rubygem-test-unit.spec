# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	gem_name	test-unit

# svn repository
# http://test-unit.rubyforge.org/svn/trunk/

Summary:	Improved version of Test::Unit bundled in Ruby 1.8.x
Name:		rubygem-%{gem_name}
# 3.6.0 and above is for F-39+ only as 3.5.8 and above
# changes default progress style
# (For 3.5.8 and 3.5.9, F-38 and below reverted this change)
Version:	3.7.0
Release:	101%{?dist}
# SPDX confirmed
# lib/test/unit/diff.rb is under (BSD-2-Clause OR Ruby) AND Python-2.0.1
# lib/test-unit.rb changed to BSD-2-Clause or Ruby (from 3.3.7)
# Other file: BSD-2-Clause or Ruby
License:	((BSD-2-Clause OR Ruby) AND Python-2.0.1) AND (BSD-2-Clause OR Ruby)
URL:		http://test-unit.github.io/

Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:	%{gem_name}-%{version}-tests.tar.gz
# Source1 is created by bash %%SOURCE2
Source2:	test-unit-create-missing-files.sh

BuildRequires:	ruby(release)
BuildRequires:	rubygems
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(power_assert)
# For %%check
#BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(hoe)
BuildRequires:	rubygem(bigdecimal)
BuildRequires:	rubygem(csv)
Requires:	ruby(release)
Requires:	rubygems

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
Test::Unit 2.x - Improved version of Test::Unit bundled in
Ruby 1.8.x.
Ruby 1.9.x bundles minitest not Test::Unit. Test::Unit
bundled in Ruby 1.8.x had not been improved but unbundled
Test::Unit (Test::Unit 2.x) will be improved actively.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -a 1

mv ../%{gem_name}-%{version}.gemspec .

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install
cp -a %{gem_name}-%{version}/test ./%{gem_instdir}

#find . -name \*.gem | xargs chmod 0644
find . -type f | xargs chmod ugo+r

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_cache}
# Keep undeleted the following files (now)??
# Needs investigation
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Rakefile \
	test/ \
	%{nil}
popd

%check
pushd .%{gem_instdir}
#rake test --trace
ruby -Ilib ./test/run.rb
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/BSDL
%license	%{gem_instdir}/COPYING
%license	%{gem_instdir}/PSFL
%doc	%{gem_instdir}/README.md

%{gem_libdir}
%{gem_instdir}/bin/
%{gem_spec}

%files	doc
%{gem_instdir}/doc/
%{gem_instdir}/sample/

%{gem_docdir}/

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 06 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-100
- 3.7.0

* Thu Apr 10 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.8-100
- 3.6.8

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.7-100
- 3.6.7

* Fri Nov 01 2024 Vít Ondruch <vondruch@redhat.com> - 3.6.2-202
- Add `rubygem(csv)` build dependency needed by Ruby 3.4

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 16 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.2-200
- 3.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.1-200
- 3.6.1

* Sun Jun 11 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-200
- 3.6.0

* Thu May 25 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.9-200
- 3.5.9

* Sat May 13 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.8-200
- 3.5.8
- F-38 and below: Keep progress style as mark as before instead of upstream-chosen
  inplace style

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.7-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 15 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.7-200
- 3.5.7

* Tue Oct  4 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.5-200
- 3.5.5

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.3-200
- 3.5.3

* Fri Dec 10 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.2-200
- 3.5.2

* Wed Nov 10 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-200
- 3.5.1

* Tue Oct 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-200
- 3.5.0

* Tue Oct 12 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.8-200
- 3.4.8

* Wed Sep 15 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.7-200
- 3.4.7

* Sun Sep  5 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.5-200
- 3.4.5

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.4-200
- 3.4.4

* Thu Apr 22 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-200
- 3.4.1

* Mon Feb  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-200
- 3.4.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.9-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 29 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.9-200
- 3.3.9

* Sat Dec 26 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.8-200
- 3.3.8

* Wed Dec 23 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.7-201
- Update license tag

* Wed Nov 25 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.7-200
- 3.3.7

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 12 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.6-200
- 3.3.6

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.5-200
- 3.3.5

* Tue Oct  1 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.4-200
- 3.3.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.3-200
- 3.3.3

* Tue Apr 23 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-200
- 3.3.2

* Mon Apr  1 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.1-200
- 3.3.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-200
- 3.3.0

* Fri Dec 14 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.9-200
- 3.2.9

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.8-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun  4 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.8-200
- 3.2.8
- Bump release number

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.7-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.7-100
- 3.2.7

* Fri Sep 22 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.6-100
- 3.2.6

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.5-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.5-100
- 3.2.5

* Fri May 26 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.4-100
- 3.2.4

* Fri May  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.3-103
- Follow up power_assert 1.0.0 change

* Thu Feb 16 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.3-102
- Fix test failure for ruby24 wrt integer unification

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  1 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.3-100
- 3.2.3

* Tue Nov 15 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.2-100
- 3.2.2

* Sun Jul 31 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-100
- 3.2.1

* Fri Jun 24 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-100
- 3.2.0

* Tue May 24 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.9-100
- 3.1.9

* Wed Mar 23 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.8-100
- 3.1.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.7-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.7-100
- 3.1.7

* Mon Oct 12 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.5-100
- 3.1.5

* Mon Sep 28 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.4-100
- 3.1.4

* Mon Jul 27 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.3-100
- 3.1.3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-100
- 3.1.2

* Fri May 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.1-100
- 3.1.1

* Fri May 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.0-100
- 3.1.0

* Tue Jan 13 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.9-101
- Kill 2-year-old testrb2 support on F-22+

* Wed Dec 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.9-100
- 3.0.9

* Sun Dec 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.8-100
- Bump release massively (for ruby srpm)

* Sun Dec 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.8-1
- 3.0.8

* Thu Dec  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.7-1
- 3.0.7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.5-1
- 2.5.5

* Thu Feb 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.4-3
- Patch for CSV support (patch by upstream)

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.4-2
- Rebuild for ruby 2.0.0

* Sun Feb  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.4-1
- 2.5.4

* Wed Jan  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.3-1
- 2.5.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.5-3
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.5-2
- 2.4.5

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.4-1
- 2.4.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-2
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.3-1
- 2.4.3

* Sun Nov 27 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.2-1
- 2.4.2

* Wed Nov 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.1-1
- 2.4.1

* Mon Sep 19 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.0-1
- 2.4.0

* Thu Aug 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.2-1
- 2.3.2

* Sun Aug 14 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.1-1
- 2.3.1

* Sun Apr 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0-1
- 2.3.0

* Fri Feb 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.2-2
- F-15 mass rebuild

* Thu Nov 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.2-1
- 2.1.2

* Sun Sep 19 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.1-2
- Fix up license tag

* Sat Sep 18 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.1-1
- Initial package
