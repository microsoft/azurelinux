# Initially generated from hpricot-0.6.164.gem by gem2rpm -*- rpm-spec -*-
%define	gem_name		hpricot

# See bug 1402582
# Currently colm (dependency for ragel) has difficulty on
# armv7hl
%global	force_regenerate_from_rl	0

Summary:	A Fast, Enjoyable HTML Parser for Ruby
Name:		rubygem-%{gem_name}
Version:	0.8.6
Release:	34%{?dist}
# ext/fast_xs/FastXsService.java is licensed under ASL 2.0
License:	MIT AND ASL 2.0
Vendor:	        Microsoft Corporation
Distribution:	Mariner
URL:		http://github.com/hpricot/hpricot
# Non-free file removed, see Source10
# Source0:	http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Source0:	https://src.fedoraproject.org/repo/pkgs/rubygem-hpricot/hpricot-0.8.6-modified.gem/5d737234720f3847cc5def6c0047f2e4/hpricot-0.8.6-modified.gem
Source10:	rubygem-hpricot-create-free-gem.sh

Requires:	ruby(release)
BuildRequires:	ruby(release)

BuildRequires:	gcc
BuildRequires:	rubygems-devel
# Recompile
%if %{force_regenerate_from_rl}
BuildRequires:	ruby
BuildRequires:	ragel
%endif
# Others
BuildRequires:	rubygem(rake-compiler)
BuildRequires:	ruby-devel
BuildRequires:  rubygem(test-unit)
BuildRequires:  ruby
Requires:	ruby(rubygems)
Provides:	rubygem(%{gem_name}) = %{version}-%{release}
Provides:	ruby-%{gem_name} = %{version}-%{release}

%description
Hpricot is a very flexible HTML parser, based on Tanaka Akira's
HTree and John Resig's JQuery, but with the scanner recoded in C
(using Ragel for scanning.)

%package	doc
Summary:	Documentation for %{name}
# Directory ownership issue
Requires:	%{name} = %{version}-%{release}
Requires:	ruby(rubygems)

%description	doc
This package contains documentation for %{name}.

%package	-n ruby-%{gem_name}
Summary:	Non-Gem support package for %{gem_name}
Requires:	%{name} = %{version}-%{release}
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description	-n ruby-%{gem_name}
This package provides non-Gem support for %{gem_name}.

%prep
%setup -q -T -c

# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}*

# ??
find . -type f | xargs chmod ugo+r

sed -i Rakefile -e '\@require.*bundler/setup@d'
mkdir tmpbin
ln -sf /bin/true tmpbin/git
export PATH=$(pwd)/tmpbin:$PATH

%if %{force_regenerate_from_rl}
rm -f ext/hpricot_scan/*.c
rake ext/hpricot_scan/extconf.rb
%endif

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd

%gem_install

pushd .%{gem_instdir}/test
# Kill tests related to BOINGBOING, licensed under CC-BY-NC
grep -rl BOING . | \
	xargs sed -i '/BOING/s|^\([ \t][ \t]*\)\(.*\)$|\1# This test is intentionally killed\n\1return true\n\1\2|'
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}

mkdir -p %{buildroot}%{gem_extdir_mri}/lib
mv %{buildroot}%{gem_libdir}/*.so %{buildroot}%{gem_extdir_mri}/lib

for f in $(find %{buildroot}%{gem_instdir} -name \*.rb)
do
	sed -i -e '/^#!/d' $f
	chmod 0644 $f
done

# clean
rm -rf %{buildroot}%{gem_instdir}/tmp/
rm -rf %{buildroot}%{_libdir}/ruby/gems/extensions

# Kill unneeded files
find %{buildroot}%{gem_instdir}/ext \
	-type f \
	-not -name \*.java \
	-print0 | \
	xargs -0 rm -f
rm -f %{buildroot}%{gem_instdir}/.require_paths
DIR=%{buildroot}%{gem_libdir}/universal-java*
[ -d $DIR ] && rmdir $DIR


pushd %{buildroot}
find . -type f '(' -name '[A-Z]*' -or -name '*.java' -or -name '*.rb' -or -name '*gem*' ')' \
	-print0 | xargs -0 chmod 0644
popd

%check
pushd .%{gem_instdir}

# problem reported here: https://github.com/hpricot/hpricot/issues/52
LANG=C.UTF-8
ruby \
	-Ilib:.:ext/hpricot_scan:ext/fast_xs:test \
	-e "gem 'test-unit' ; Dir.glob('test/test_*.rb').each { |f| require f }"

popd

%files
%{gem_extdir_mri}
%dir	%{gem_instdir}/
%doc	%{gem_instdir}/[A-Z]*
%exclude %{gem_instdir}/Rakefile
%{gem_instdir}/[a-l]*/
%{gem_cache}
%{gem_spec}

%files	doc
%{gem_instdir}/Rakefile
%{gem_instdir}/extras/
%{gem_instdir}/test/
%{gem_docdir}/

%changelog
* Thu Dec 30 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.8.6-34
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Sun Jul 25 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-33
- Rebuild for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-31
- F-34: rebuild against ruby 3.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-28
- F-32: rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-25
- F-30: rebuild against ruby26

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8.6-24
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.8.6-21
- Rebuilt for switch to libxcrypt

* Wed Jan 03 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-20
- F-28: rebuild for ruby25

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-16
- Bump release
- Kill ragel BR for now due to armv7hl difficulty (ref: bug 1402582)

* Tue Jan 17 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-14
- Explicitly regenerate C source from .rl (bug 1412841)

* Wed Jan 11 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-13
- F-26: rebuild for ruby24

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-11
- F-24: rebuild against ruby23

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-9
- F-22: Rebuild for ruby 2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-6
- F-21: rebuild for ruby 2.1 / rubygems 2.2
- End up with using test-unit for testsuite

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.6-4
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.8.6-1
- 0.8.6

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.8.5-4
- F-17: kill compat ruby-%%{gem_name} package

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.5-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.8.5-1
- 0.8.5

* Wed Mar  2 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.8.4-1
- 0.8.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.3-2
- Fix segfault on GC (bug 672169, patch suggested by TAGOH Akira)

* Sat Nov  6 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.3-1
- 0.8.3

* Mon Nov  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.2-1
- 0.8.2
- Kill BOINGBOING test properly

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.1-3
- F-12: Mass rebuild

* Sat Jun 27 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.1-2
- Readd Rakefile
- Enable check

* Wed Apr  8 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.1-1
- 0.8.1

* Thu Mar 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7-1
- 0.7

* Sat Feb 28 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-5
- Fix permission (bug 487654)

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-4
- F-11: Mass rebuild

* Thu Jan 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-3
- Fix license tag, removing non-free file (thanks to
  Michael Stahnke)

* Fri Dec 26 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-2
- Kill unneeded files more

* Sun Dec 21 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-1
- Switch to Gem

* Sat Dec 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6-3
- Fix build error related to Windows constant, detected
  by Matt's mass build
  (possibly due to rubygems 1.3.1 change)

* Wed Feb 13 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6-2
- Rebuild against gcc43
- Patch for Rakefile to skip unneeded commands call for ragel 6.0+
  (bug 432186, Thanks Jeremy Hinegardner !!)

* Tue Nov  6 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6-1
- 0.6

* Sat Nov  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.150-2
- Use rubygem(rake) for rebuild

* Fri Jun  8 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.150-1
- Initial packaging
