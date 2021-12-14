Vendor:         Microsoft Corporation
Distribution:   Mariner
%global	gem_name	test-unit

# svn repository
# http://test-unit.rubyforge.org/svn/trunk/

Summary:	Improved version of Test::Unit bundled in Ruby 1.8.x
Name:		rubygem-%{gem_name}
Version:	3.3.6
Release:	202%{?dist}
# lib/test/unit/diff.rb is under GPLv2 or Ruby or Python
# lib/test-unit.rb is under LGPLv2+ or Ruby
# Other file: GPLv2 or Ruby
License:	(GPLv2 or Ruby) and (GPLv2 or Ruby or Python) and (LGPLv2+ or Ruby)
URL:		http://test-unit.github.io/

Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems
BuildRequires:	rubygems-devel
# For %%check
#BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(hoe)
Requires:	ruby(release)
Requires:	rubygems
AutoReqProv: 0

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
%setup -q -c -T
# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

#find . -name \*.gem | xargs chmod 0644
find . -type f | xargs chmod ugo+r

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
#rake test --trace
ruby -Ilib ./test/run-test.rb
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%{gem_instdir}/lib/

%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%{gem_instdir}/doc/
# Keep below for this package
%{gem_instdir}/Rakefile
%{gem_instdir}/sample/
%{gem_instdir}/test/

%{gem_docdir}/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.6-202
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
