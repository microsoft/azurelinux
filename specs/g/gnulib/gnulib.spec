# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit a8ac9f9ce50284c5ddeac8b4d50e9bc433eb42b4
# %%global tag 11 #disabled due to unarragment release line after mass rebuild.
%global githead %(printf %%.7s %commit)
%global gitdate 20251223

# epel7 compatibility mode
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# Module Sample: (Alpha Version)
# %% global moduleX %%name-of-module
#
# %% package -n %%{moduleX}
# Summary: %%{summary_of_moduleX}
# License: %%{license_of_moduleX}
#
# %% description -n %%{moduleX}
# %%description-of-module
#
# %% prep
# ./gnulib-tool --create-testdir --dir=build-%%{moduleX} %%{moduleX}
#
# %% build
# pushd build-%%{moduleX}
# %% configure --prefix=%%_prefix
# make %%{?_smp_mflags}
# popd
#
# %% install
# pushd build-%%{moduleX}
# %%make_install
# popd
# help2man -N --no-discard-stderr %%{buildroot}%%{_bindir}/%%{moduleX} | gzip -9c > %%{buildroot}%%{_mandir}/man1/%%{moduleX}.1.gz
#
# %% files -n %%{moduleX}
# %%{_bindir}/%%{moduleX}
# %%{_mandir}/*/%%{moduleX}.*

##################################
# LIST OF SINGLE MODULE PACKAGES :
# 1.git-merge-changelog
##################################

%global module1 git-merge-changelog
%global common_desc \
The GNU portability library is a macro system and C declarations and \
definitions for commonly-used API elements and abstracted system behaviors. \
It can be used to improve portability and other functionality in your programs.

Name:     gnulib
Version:  0
Release: 57.%{gitdate}git%{?dist}
Summary:  GNU Portability Library
License:  Public Domain and BSD and GPLv2+ and GPLv3 and GPLv3+ and LGPLv2 and LGPLv2+ and LGPLv3+
URL:      https://www.gnu.org/software/gnulib
Source0:  https://git.savannah.gnu.org/gitweb/?p=gnulib.git;a=snapshot;h=%{githead};sf=tgz;name=gnulib-%{githead}.tar.gz#/gnulib-%{githead}.tar.gz
Source1: https://erislabs.net/gitweb/?p=gnulib.git;a=blob_plain;hb=HEAD;f=debian/manpages/check-module.1#/check-module.1
Source2: https://erislabs.net/gitweb/?p=gnulib.git;a=blob_plain;hb=HEAD;f=debian/manpages/gnulib-tool.1#/gnulib-tool.1

#Patch0:   test-u8-strstr-alarm.diff

BuildRequires:		perl-generators
BuildRequires:		texinfo

# Java JDK dropped in i686
# https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs
%ifnarch %{ix86}
BuildRequires:		java-devel
Requires:           %{name}-javaversion
%endif

# For building Modules, all gnulib requires must be found, Modules BRs:
BuildRequires:		gettext-devel
BuildRequires:		bison
BuildRequires:		gperf
BuildRequires:		libtool
BuildRequires:		help2man
BuildRequires:		git
BuildRequires:      make
BuildRequires:      ncurses-devel
BuildRequires:      python3-devel


%description
%common_desc

%prep
%autosetup -n %{name}-%{githead} -p1 -Sgit

#modules not to be tested by direct import
toRemove="lib-symbol-visibility havelib .*-obsolete localcharset gettext-h gettext alloca-opt alloca "

list="$(./gnulib-tool --list)"
for item in $toRemove
do
   list="$(echo $list| sed "s:\b$item\b::g")"
done

#is necessary to avoid some modules to test prep pass
./gnulib-tool --create-testdir --with-tests --with-obsolete --avoid=alloca --avoid=lib-symbol-visibility --avoid=havelib --dir=build-tests $list

rm lib/javaversion.class
# MODULE #1 - git-merge-changelog
./gnulib-tool --create-testdir --dir=build-%{module1} %{module1}

%build
# MODULE #1 - git-merge-changelog
pushd build-%{module1}
%configure --prefix=%_prefix
make %{?_smp_mflags}
popd
#tests build
cp -p lib/timevar.def build-tests/gllib #Fix timevar.def not found
pushd build-tests

# FIX ERROR CAN'T DETECT AC_LIB_PREPARE_PREFIX
mkdir m4
autoreconf -vfi


%configure --prefix=%_prefix
make %{?_smp_mflags}
popd

# Java JDK dropped in i686
# https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs
%ifnarch %{ix86}
# Rebuild removed java class
javac -d lib lib/javaversion.java
%endif

# This part is done with the original path

make %{?_smp_mflags} MODULES.html

sed -i -r 's#HREF="(lib|m4|modules)#HREF="%{_datadir}/%{name}/\1#g' MODULES.html
sed -i "/^[ ]*gnulib_dir=/s#\`[^\`]*\`#%{_datadir}/%{name}#" gnulib-tool
sed -i "/^[ ]*gnulib_dir=/s#\`[^\`]*\`#%{_datadir}/%{name}#" gnulib-tool.sh
sed -i "/^[ ]*gnulib_dir=/s#\`[^\`]*\`#%{_datadir}/%{name}#" gnulib-tool.py

# This part is done with the target path
make %{?_smp_mflags} info
make %{?_smp_mflags} html
# Removing unused files
rm -f */.cvsignore
rm -f */.gitignore
rm -f */.gitattributes
rm -f lib/.cppi-disable
rm -f lib/uniname/gen-uninames.lisp

%check
make -C build-tests check VERBOSE=1

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/info
mkdir -p %{buildroot}%{_pkgdocdir}
mkdir -p %{buildroot}%{_mandir}/man1

cp -p check-module %{buildroot}%{_bindir}
cp -p gnulib-tool gnulib-tool.sh gnulib-tool.py %{buildroot}%{_bindir}
cp -rp build-aux lib m4 modules config tests %{buildroot}%{_datadir}/%{name}/
cp -p .gnulib-tool.py %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_datadir}/%{name}/doc
cp -arv doc/relocatable.texi %{buildroot}%{_datadir}/%{name}/doc

cp -p doc/gnulib.info %{buildroot}%{_datadir}/info/
cp -p doc/gnulib.html MODULES.html NEWS COPYING ChangeLog HACKING users.txt doc/COPYING* %{buildroot}%{_pkgdocdir}/
cp -p %{SOURCE1} %{SOURCE2} %{buildroot}%{_mandir}/man1

cp -rp top %{buildroot}%{_datadir}/%{name}/

# Python Gnulib installing
mkdir -p %{buildroot}%{python3_sitelib}
cp -rp py%{name} %{buildroot}%{python3_sitelib}

# Module installing
%make_install -C build-%{module1}
help2man -N --no-discard-stderr %{buildroot}%{_bindir}/%{module1} | gzip -9c > %{buildroot}%{_mandir}/man1/%{module1}.1.gz

#-------------------------------------------------------------------------

%package docs
Summary: Documentation for %{name} modules
License: GFDL
Requires:			%{name}-devel = %{version}-%{release}
BuildArch: noarch

%description docs
%common_desc

This package contains documentation for %{name}.

%files docs
%{_datadir}/info/gnulib.info.gz
%{_pkgdocdir}/gnulib.html
%{_pkgdocdir}/MODULES.html
# license text is included directly in info and html files.

#-------------------------------------------------------------------------

# Java JDK dropped in i686
# https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs
%ifnarch %{ix86}
%package javaversion
Summary: javaversion built unit
License: GPLv3+
Requires:			%{name}-devel = %{version}-%{release}
%description javaversion
This package contains javaversion built unit of %{name}.

%files javaversion
%{_datadir}/%{name}/lib/javaversion.class
%endif

#-------------------------------------------------------------------------

%package devel
Summary: Devel files of %{name}
BuildArch: noarch
Provides: gnulib = %{version}-%{release}
Requires: gettext-devel
Requires: bison
Requires: coreutils
Requires: gperf
Requires: libtool
Requires: make
Requires: texinfo
Requires: diffutils
Requires: patch
Requires: m4
Requires: grep
Requires: autoconf
Requires: automake
Requires: gawk
Requires: gcc
Requires: gnulib-python

%description devel
%common_desc

This package contains devel files of %{name}.

%files devel
%{_datadir}/%{name}/
%{_bindir}/gnulib-tool
%{_bindir}/gnulib-tool.sh
%{_bindir}/gnulib-tool.py
%{_bindir}/check-module
%{_mandir}/*/check-module.*
%{_mandir}/*/gnulib-tool.*
%{_pkgdocdir}/
%exclude %{_pkgdocdir}/MODULES.html
%exclude %{_pkgdocdir}/gnulib.html
# Java JDK dropped in i686
# https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs
%ifnarch %{ix86}
# Remove built java class, goes to javaversion sub-package
%exclude %{_datadir}/%{name}/lib/javaversion.class
%endif

#-------------------------------------------------------------------------
%package -n python3-%{name}
Summary: Python Implement of Gnulib
BuildArch: noarch
Requires: gnulib = %{version}-%{release}
Provides: gnulib-python = %{version}-%{release}
Requires: python3

%description -n python3-%{name}
Python Implement of Gnulib

%files -n python3-%{name}
%{python3_sitelib}/py%{name}

#-------------------------------------------------------------------------

# MODULE #1 - git-merge-changelog
%package -n %{module1}
Summary: Git merge driver for ChangeLog files
License: GPLv2+

%description -n %{module1}
Git Merge Changelog is a git merge driver for changelogs that combines
parallel additions to the changelog without generating merge conflicts.
It can be enabled for specific files by setting appropriate git attributes.

%files -n %{module1}
%{_bindir}/%{module1}
%{_mandir}/*/%{module1}.*
%license doc/COPYINGv2

#-------------------------------------------------------------------------
%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0-56.20251223git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Dec 23 2025 Mosaab Alzoubi <mosaab[AT]ruya[DOT]systems> - 0-55.20251223git
- Update on 2025-12-23
- Use stable branch instead of master
- Add next generation of Gnulib the python release of Gnulib
- Fix building tests
- Re-struct for gnulib ng with python base
- Update dependencies

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-54.20250704git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Mosaab Alzoubi <mosaab[AT]ruya[DOT]systems> - 0-53.20250704git
- Update on 2025-07-04

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-52.20230709git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-51.20230709git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-49.20230709git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-48.20230709git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jul 09 2023 Mosaab Alzoubi <moceap[AT]fedoraproject[DOT]com> - 0-47.20230709git
- Update on 2023-07-09
- Fix can't build on aarch64  (https://bugzilla.redhat.com/show_bug.cgi?id=2220874)
- Fix can't build on epel8 (https://koji.fedoraproject.org/koji/buildinfo?buildID=2227816)

* Thu Jul 06 2023 Mosaab Alzoubi <moceap[AT]fedoraproject[DOT]com> - 0-46.20230706git
- Update on 2023-07-06
- General clean-ups
- Move built javaversion to new sub-package
- Drop built javaversion from i686

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-45.20220212git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-44.20220212git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Feb 18 2022 Peter Lemenkov <lemenkov@gmail.com> - 0-43.20220212git
- Update (required for PSPP 1.4.1+, grub2, etc)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0-42.20200827git
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-41.20200827git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-40.20200827git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 25 2021 Florian Weimer <fweimer@redhat.com> - 0-39.20200827git
- Rebuild with new binutils to fix ppc64le corruption (#1960730)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-38.20200827git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 16 2020 Peter Lemenkov <lemenkov@gmail.com> - 0-37.20200827git
- Fix FTBFS

* Wed Sep 16 2020 Peter Lemenkov <lemenkov@gmail.com> - 0-36.20200809git
- Update (required for PSPP 1.4.1+)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-35.20200107git
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-34.20200107git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0-33.20200107git
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-32.20200107git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Mosaab Alzoubi <moceap[AT]hotmail[DOT]com> - 0-31.20200107git
- Update on 2020-01-07
- CVE-2018-17942

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-30.20180720git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 0-29.20180720git%{?dist}
- Remove obsolete requirements for post/preun scriptlets

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-28.20180720git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 16 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-27.20180720git
- Also include /usr/share/gnulib/top/GNUmakefile (#1607163)

* Sun Jul 22 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-26.20180720git
- Update on 20180720

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-25.20170217git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-24.20170217git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-23.20170217git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Peter Lemenkov <lemenkov@gmail.com> - 0-22.20170217git
- Install relocatable.texi file as well (required sometimes)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-21.20170217git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-20.20170217git
- Update on 20170217.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-19.20161109git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 12 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-18.20161109git
- Update on 20161109.

* Wed May 11 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-17.20160508git
- Update on 20160511.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-16.20150928git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 28 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-15.20150928git
- Update on 20150928.

* Mon Jul  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-15.20150706git
- Update on 20150706.
- Fixes #1239538.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-15.20150325git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Mosaab Alzoubi <moceap@hotmail.com> - 0-14.20150325git
- Update on 20150325.

* Sun Dec 14 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0-13.20141214git
- Update on 20141214.

* Tue Oct 21 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0-12.20141021git
- Update on 20141021.

* Wed Sep 17 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0-11.20140910git
- Disable varible tag number.

* Thu Sep 11 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-9.20140910git
- Update to latest git.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-10.20140710git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0-9.20140710git
- Update on 20140710.
- Fix unneed numbers of release line after (FRE).

* Fri Jun 27 2014 Jakub Čajka <jcajka@redhat.com> - 0-8.20140504git.2
- Added tests

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-8.20140504git.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 4 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0-8.20140504git
- Update on 20140504.

* Mon Mar 03 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0-7.20140225git
- Update to latest git.

* Mon Jan 27 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0-6.20140127git
- Update on 20140127.

* Thu Jan 9 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0-5.20140109git
- Update on 20140109.

* Thu Dec 19 2013 Mosaab Alzoubi <moceap@hotmail.com> - 0-4.20131219git
- Update.
- General tweaks.
- Remove META main package.
- Rename -core into -devel.
- Remove main package from other packages requires.
- -docs requires -devel.
- Move main requires to -devel ones.
- -devel provides main package.
- Remove un-need-to-list-BRs diffutils make coreutils patch.
- United path for documents for all packages.

* Sun Dec 1 2013 Mosaab Alzoubi <moceap@hotmail.com> - 0-3.20131201git
- Update.

* Thu Nov 14 2013 Mosaab Alzoubi <moceap@hotmail.com> - 0-2.20131112git
- Fix tag method to 0-$rel.$gitdategit instead of $ver.git$gitdate-$rel.
- Release number will increas by new git snapshot.

* Tue Nov 12 2013 Mosaab Alzoubi <moceap@hotmail.com> - 0.1.git20131112-1
- After more 6 years in 0.0, GnuLib 0.1 released.
- Replace version method to $ver.git$gitdate instead of $gitdate.git$githead.
- Update to 0.1.git20131112.

* Fri Nov 1 2013 Mosaab Alzoubi <moceap@hotmail.com> - 20131030.git5c508f6-2
- Decrease description of git-merge-changelog
- Add license file to git-merge-changelog

* Wed Oct 30 2013 Mosaab Alzoubi <moceap@hotmail.com> - 20131030.git5c508f6-1
- Update to 20131030.git5c508f6
- Create -core noarch package, because rpmbuild can't drive arched subpackage from nonarched main one.
- Some General Fixes.
- Add 1st sample form - Module Sample: (Alpha Version)
- Add 1st module single package - git-merge-changelog

* Mon Oct 28 2013 Mosaab Alzoubi <moceap@hotmail.com> - 20131027.git5191b35-2
- Fixes after Zbigniew Jędrzejewski-Szmek revision:
- Remove prebuilt java class.
- gnulib-docs require gnulib.
- List all licenses.
- Replace define by global.

* Sun Oct 27 2013 Mosaab Alzoubi <moceap@hotmail.com> - 20131027.git5191b35-1
- Update.

* Sat Oct 26 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20131022.git25fb29a-4
- Spec file tweaks.
- Package MODULES.html.

* Thu Oct 24 2013 Mosaab Alzoubi <moceap@hotmail.com> - 20131022.git25fb29a-3
- Many Fixes.

* Thu Oct 24 2013 Mosaab Alzoubi <moceap@hotmail.com> - 20131022.git25fb29a-2
- Many Fixes.

* Tue Oct 22 2013 Mosaab Alzoubi <moceap@hotmail.com> - 20131022.git25fb29a-1
- Initial build.
