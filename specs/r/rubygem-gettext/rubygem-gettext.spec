# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global		gem_name	gettext

%global		locale_ver		2.0.5
%global		repoid			67096

Name:		rubygem-%{gem_name}
Version:	3.5.1
Release: 4%{?dist}
Summary:	RubyGem of Localization Library and Tools for Ruby

# Ruby OR LGPL-3.0-or-later:	gemspec
# Ruby:	lib/gettext/mo.rb
# SPDX confirmed
License:	(Ruby OR LGPL-3.0-or-later) AND Ruby
URL:		http://www.yotabanana.com/hiki/ruby-gettext.html?ruby-gettext
Source0:	http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
# For %%check

BuildRequires:	rubygem(erubi)
BuildRequires:	rubygem(locale) >= %{locale_ver}
BuildRequires:	rubygem(prime)
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
BuildRequires:	rubygem(test-unit-rr)
BuildRequires:	rubygem(text)
# test/tools/test_task.rb -> lib/gettext/tools/task.rb
BuildRequires:	rubygem(rake)
BuildRequires:	gettext

BuildRequires:	rubygem(racc)

Requires:	ruby(rubygems)
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

Obsoletes:	ruby-gettext-package <= %{version}-%{release}
Provides:	ruby-gettext-package = %{version}-%{release}

BuildArch:	noarch

%description
Ruby-GetText-Package is a GNU GetText-like program for Ruby.
The catalog file(po-file) is same format with GNU GetText.
So you can use GNU GetText tools for maintaining.

This package provides gem for Ruby-Gettext-Package.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.


%prep
%setup -q -n %{gem_name}-%{version}
mv ../%{gem_name}-%{version}.gemspec .

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

#%%{__rm} -f .%{gem_instdir}/Rakefile
%{__rm} -f .%{gem_instdir}/%{gem_name}.gemspec
%{__rm} -rf .%{gem_instdir}/po/
%{__chmod} 0755 .%{gem_instdir}/bin/*
%{__chmod} 0644 .%{gem_dir}/cache/*.gem
find .%{gem_instdir}/ -name \*.po | xargs %{__chmod} 0644

# Cleanups for rpmlint
find .%{gem_instdir}/lib/ -name \*.rb | while read f
do
	%{__sed} -i -e '/^#!/d' $f
done

# fix timestamps
find . -type f -print0 | xargs -0 touch -r %{SOURCE0}

%install
%{__mkdir_p} %{buildroot}{%{gem_dir},%{_bindir}}

%{__cp} -a .%{_bindir}/* %{buildroot}/%{_bindir}/
%{__cp} -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
find %{buildroot}%{gem_dir} -name \*.rb.patch\* -delete


# For --short-circult
%{__rm} -f *.lang

# modify find-lang.sh to deal with gettext .mo files under
# %%{gem_instdir}/locale
#%%{__sed} -e 's|/share/locale/|/data/locale/|' \
#	/usr/lib/rpm/find-lang.sh \
#	> find-lang-modified.sh
#
#sh find-lang-modified.sh %{buildroot} gettext gettext-gem.lang
%find_lang gettext
mv gettext.lang gettext-gem.lang

%{__cat} *-gem.lang >> %{name}-gem.lang

# list directories under %%{gem_instdir}/locale/
find %{buildroot}%{gem_instdir}/locale -type d | while read dir
do
	echo "%%dir ${dir#%{buildroot}}" >> %{name}-gem.lang
done

# clean up
rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Rakefile \
	.yardopts \
	src/ \
	test/ \
	%{nil}
popd

%check
pushd .%{gem_instdir}
export LANG=C.UTF-8
export LANGUAGE=ja_JP.utf8
export RUBYLIB=$(pwd)/lib

# Umm...
pushd test/po
locales=$(ls -1d */ | sed -e 's|/||')
popd
catalogues=$(ls -1 test/po/ja/*.po | while read f ; do basename $f | sed -e 's|\.po||' ; done)
for l in $locales
do
	for d in $catalogues
	do
		if [ -f test/po/${l}/${d}.po ] ; then
			mkdir -p  test/locale/${l}/LC_MESSAGES/ || true
			bin/rmsgfmt -o test/locale/${l}/LC_MESSAGES/${d}.mo test/po/${l}/${d}.po
		fi
	done
done

pushd samples/po
locales=$(ls -1d */ | sed -e 's|/||')
popd
catalogues=$(ls -1 samples/po/ja/*.po | while read f ; do basename $f | sed -e 's|\.po||' ; done)
for l in $locales
do
	for d in $catalogues
	do
		if [ -f samples/po/${l}/${d}.po ] ; then
			mkdir -p  samples/locale/${l}/LC_MESSAGES/ || true
			bin/rmsgfmt -o samples/locale/${l}/LC_MESSAGES/${d}.mo samples/po/${l}/${d}.po
		fi
	done
done

pushd samples/cgi/po
locales=$(ls -1d */ | sed -e 's|/||')
popd
catalogues=$(ls -1 samples/cgi/po/ja/*.po | while read f ; do basename $f | sed -e 's|\.po||' ; done)
for l in $locales
do
	for d in $catalogues
	do
		if [ -f samples/cgi/po/${l}/${d}.po ] ; then
			mkdir -p  samples/cgi/locale/${l}/LC_MESSAGES/ || true
			bin/rmsgfmt -o samples/cgi/locale/${l}/LC_MESSAGES/${d}.mo samples/cgi/po/${l}/${d}.po
		fi
	done
done

ruby -Ilib:test test/run-test.rb

popd


%files	-f %{name}-gem.lang
%{_bindir}/rxgettext
%{_bindir}/rmsginit
%{_bindir}/rmsgcat
%{_bindir}/rmsgfmt
%{_bindir}/rmsgmerge

%dir %{gem_instdir}/
%doc %{gem_instdir}/[A-Z]*
%dir %{gem_instdir}/doc/
%dir	%{gem_instdir}/doc/text/
%license	%{gem_instdir}/doc/text/*txt
%doc	%{gem_instdir}/doc/text/news.md

%{gem_instdir}/bin/
%{gem_instdir}/lib/

%{gem_spec}

%files		doc
%{gem_docdir}/
%{gem_instdir}/samples/

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 27 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-1
- 3.5.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 04 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-1
- 3.5.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.9-1
- 3.4.9

* Fri Aug 18 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.7-1
- 3.4.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.6-1
- 3.4.6

* Sun Jun 11 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.4-1
- 3.4.4

* Tue May 23 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.3-5
- Fix license typo

* Sat May  6 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.3-4
- SPDX migration

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 25 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.3-1
- 3.4.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.2-1
- 3.4.2

* Thu Sep  9 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-1
- 3.4.1

* Fri Aug 27 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-1
- 3.4.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.7-1
- 3.3.7
- Remove irb dependency

* Sun Aug  9 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.6-1
- 3.3.6

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.5-1
- 3.3.5

* Fri Feb 14 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.4-1
- 3.3.4

* Fri Jan 31 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-2
- R,BR rubygem(racc)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-1
- 3.3.2

* Thu Jan  9 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-1
- 3.3.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.9-4
- Fix test failure with ruby 2.6

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.9-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar  9 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.9-1
- 3.2.9

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.6-1
- 3.2.6

* Mon Aug 14 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.4-1
- 3.2.4

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.3-1
- 3.2.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 20 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.2-1
- 3.2.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- 3.2.1

* Thu Dec 31 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-1
- 3.2.0

* Wed Dec 30 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.9-1
- 3.1.9

* Tue Sep 22 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.7-1
- 3.1.7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 21 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.6-1
- 3.1.6

* Mon Jan 19 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.5-1
- 3.1.5

* Sun Aug 31 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.4-1
- 3.1.4

* Fri Aug  1 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.3-1
- 3.1.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-1
- 3.1.2

* Thu Feb 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.1-1
- 3.1.1

* Mon Feb 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.0-1
- 3.1.0

* Mon Feb  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.6-1
- 3.0.6

* Tue Dec 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.3-1
- 3.0.3

* Tue Oct 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.2-6
- Patch from upstream git to remove memoization with
  coordination with rubygem-locale side change
- Patch from upstream git to fix test failure on arm

* Fri Oct 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.2-4
- Make test failure conditional

* Thu Oct 10 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.2-2
- F-21: rescue test failure for now

* Thu Oct 10 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.2-1
- 3.0.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.8-1
- 2.3.8

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.7-4
- Kill unneeded iconv call

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.7-3
- F-19: Rebuild for ruby 2.0.0
- F-19: Use GLib's iconv instead of iconv removed from ruby core

* Sun Feb 10 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.7-2
- Require levenshtein for fuzzy merging

* Thu Jan 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.7-1
- 2.3.7

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>  - 2.3.6-1
- 2.3.6

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>  - 2.2.1-3
- Clean up old stuff

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 30 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.2.1-1
- 2.2.1

* Mon Apr  7 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.2.0-2
- Fix test case

* Mon Apr  7 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.1.0-7
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1.0-6
- F-17: rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jun 25 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1.0-4
- Rescue Gem.all_load_paths when it is removed from rubygems

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.0-3
- F-15 mass rebuild

* Tue Jan 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- gems.rubyforge.org gem file seems old, changing Source0 URL for now

* Wed Nov 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.0-1
- 2.1.0

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-2
- F-12: Mass rebuild

* Wed May 28 2009 Mamoru Tasaka <mtasaka@ios.s.u-tokyo.ac.jp> - 2.0.4-1
- 2.0.4

* Mon May 11 2009 Mamoru Tasaka <mtasaka@ios.s.u-tokyo.ac.jp> - 2.0.3-2
- 2.0.3
- Add "BR: gettext" (not to Requires) for rake test

* Fri May  1 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-3
- Mark LICENSE etc as %%doc

* Wed Apr 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-2
- Bump ruby-locale Requires version

* Tue Apr 21 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- 2.0.1, drop patches already in upstream (all)

* Sat Mar 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-1
- Update to 2.0.0
- Now require rubygem(locale)
- Rescue NoMethodError on gem call on gettext.rb
- Reintroduce 4 args bindtextdomain() compatibility

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-8
- %%global-ize "nested" macro

* Thu Oct 23 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-7
- Handle gettext .mo files under %%{gem_instdir}/data/locale by
  modifying find-lang.sh

* Tue Oct  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-6
- Move sed edit section for lib/ files from %%install to %%build
  stage for cached gem file

* Tue Oct  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-5
- Recreate gettext .mo files (by using this itself)

* Mon Oct  6 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-3
- Some modification for spec file by Scott

* Tue Sep 23 2008 Scott Seago <sseago@redhat.com> - 1.93.0-2
- Initial package (of rubygem-gettext)
  Set at release 2 to supercede ruby-gettext-package-1.93.0-1

* Thu Sep 18 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-1
- 1.93.0

* Sat Aug  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.92.0-1
- 1.92.0

* Thu May 22 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.91.0-1
- 1.91.0

* Sun Feb  3 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.90.0-1
- 1.90.0
- Arch changed to noarch

* Wed Aug 29 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.10.0-1
- 1.10.0

* Wed Aug 22 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-2.dist.2
- Mass rebuild (buildID or binutils issue)

* Fri Aug  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-2.dist.1
- License update

* Mon May  7 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-2
- Create -doc subpackage

* Sat Apr 21 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-1
- Initial packaging
