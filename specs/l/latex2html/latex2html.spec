# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define enable_japanese 1

Summary: Converts LaTeX documents to HTML
Name: latex2html
Version: 2023.2
Release: 9%{?dist}
License: GPL-2.0-or-later
URL: https://github.com/latex2html/latex2html/releases
# main latex2html source
Source0: https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1: cfgcache.pm
Source2: %{name}-manpages.tar.gz
# support for Japanese
# http://takeno.iee.niit.ac.jp/~shige/TeX/latex2html/
Source3: http://takeno.iee.niit.ac.jp/~shige/TeX/latex2html/data2/l2h-2023-jp3.2b1.37.tar.gz
Patch1: latex2html-2018.2-teTeX-l2h-config.patch
Patch2: latex2html-2002-2-1-SHLIB.patch
Requires: tex(latex), tex(dvips), tex(url.sty), tex(preview.sty), netpbm-progs, poppler-utils
BuildRequires: tex(latex), tex(dvips), tex(url.sty), tex(preview.sty), netpbm-progs, poppler-utils
BuildRequires: perl-interpreter >= 5.003, perl-generators, ghostscript >= 4.03
BuildRequires: perl(Carp), perl(Config), perl(Cwd), perl(DB), perl(Exporter),
BuildRequires: perl(File::Copy), perl(FindBin), perl(IO::File), perl(Sys::Hostname)
BuildRequires: perl(Unicode::Collate::Locale), perl(lib), perl(strict), perl(vars)
BuildRequires: make
BuildArch: noarch

%description
LATEX2HTML is a converter written in Perl that converts LATEX
documents to HTML. This way e.g. scientific papers - primarily typeset
for printing - can be put on the Web for online viewing.

LATEX2HTML does also a good job in rapid web site deployment. These
pages are generated from a single LATEX source.

%prep
%setup -q -c -a 0

pushd %{name}-%{version}
# Patch from Oliver Paukstadt <oliver.paukstadt@millenux.com>
%patch -P1 -p2 -b .config

# fix SHLIBDIR
%patch -P2 -p1 -b .shlib

# remove all platforms we don't need
for i in Dos Mac OS2 Win32; do
  rm -f L2hos/${i}.pm
done
rm -rf cweb2html
rm -f readme.hthtml
popd

%if %{enable_japanese}
cp -a %{name}-%{version} %{name}-%{version}JA
pushd %{name}-%{version}JA
tar fxz %{SOURCE3}
popd
%endif

%build
pushd %{name}-%{version}
cp %{SOURCE1} cfgcache.pm
tar fxz %{SOURCE2}

./configure	--program-prefix=%{?_program_prefix} \
		--prefix=%{_prefix} \
		--exec-prefix=%{_exec_prefix} \
		--bindir=%{_bindir} \
		--sbindir=%{_sbindir} \
		--sysconfdir=%{_sysconfdir} \
		--datadir=%{_datadir} \
		--includedir=%{_includedir} \
		--libdir=%{_datadir}/latex2html \
		--libexecdir=%{_libexecdir} \
		--localstatedir=%{_localstatedir} \
		--sharedstatedir=%{_sharedstatedir} \
		--mandir=%{_mandir} \
		--infodir=%{_infodir} \
		--shlibdir=%{_datadir}/latex2html \
		--with-texpath=%{_datadir}/texmf/tex/latex/html

perl -pi -e "s,/usr/(share/)?lib,%{_datadir}," cfgcache.pm
make
popd

%if %{enable_japanese}
pushd %{name}-%{version}JA
sed s/latex2html/jlatex2html/g < %{SOURCE1} > cfgcache.pm
perl -pi -e "s,/usr/bin/dvips,/usr/bin/pdvips," cfgcache.pm
perl -pi -e "s,/usr/bin/latex,/usr/bin/platex," cfgcache.pm

./configure	--program-prefix=%{?_program_prefix} \
		--prefix=%{_prefix} \
		--exec-prefix=%{_exec_prefix} \
		--bindir=%{_bindir} \
		--sbindir=%{_sbindir} \
		--sysconfdir=%{_sysconfdir} \
		--datadir=%{_datadir} \
		--includedir=%{_includedir} \
		--libdir=%{_datadir}/jlatex2html \
		--libexecdir=%{_libexecdir} \
		--localstatedir=%{_localstatedir} \
		--sharedstatedir=%{_sharedstatedir} \
		--mandir=%{_mandir} \
		--infodir=%{_infodir} \
		--shlibdir=%{_datadir}/jlatex2html \
		--with-texpath=%{_datadir}/texmf/tex/latex/html

perl -pi -e "s,/usr/(share/)?lib,%{_datadir},;
	    s,%{_datadir}/latex2html,%{_datadir}/jlatex2html," cfgcache.pm
make
perl -pi -e "s,\\\$\{dd}pstoimg,\\\$\{dd}jpstoimg, ;
	    s,\\\$\{dd}texexpand,\\\$\{dd}jtexexpand," l2hconf.pm

for i in latex2html pstoimg texexpand ; do
	mv ${i} j${i}
done
popd
%endif

%install
pushd %{name}-%{version}
sed -i "s,%{_prefix},%{buildroot}%{_prefix}," cfgcache.pm
sed -i "s,%{buildroot},," l2hconf.pm

perl -pi -e "s,/.*\\\$\{dd}texexpand,%{_bindir}/texexpand,;
	    s,/.*\\\$\{dd}pstoimg,%{_bindir}/pstoimg,;
	    s,/.*\\\$\{dd}*icons,\\\$\{LATEX2HTMLDIR}/icons,;
	    s,/.*\\\$\{dd}rgb.txt,\\\$\{LATEX2HTMLDIR}/styles/rgb.txt,;
	    s,/.*\\\$\{dd}styles\\\$\{dd}crayola.txt,\\\$\{LATEX2HTMLDIR}/styles/crayola.txt," latex2html

make install
rm -rf %{buildroot}%{_datadir}/latex2html/versions/table.pl.orig \
       %{buildroot}%{_datadir}/latex2html/docs/ \
       %{buildroot}%{_datadir}/latex2html/example/
sed -i "s,/usr/local/bin/perl,/usr/bin/perl," %{buildroot}%{_datadir}/latex2html/makeseg/makeseg
sed -i "s,/usr/local/bin/perl,/usr/bin/perl," %{buildroot}%{_datadir}/latex2html/makemap
sed -i "s,###\!.*,," %{buildroot}%{_datadir}/latex2html/makemap
sed -i "s,###\!.*,," %{buildroot}%{_datadir}/latex2html/makeseg/makeseg
sed -i "s,%{buildroot},," %{buildroot}%{_bindir}/pstoimg
sed -i "s,%{buildroot},," %{buildroot}%{_bindir}/texexpand
sed -i "s,%{buildroot},," cfgcache.pm
sed -i "s,$cfg{'srcdir'}.*,$cfg{'srcdir'} = q'%{name}-%{version}';," cfgcache.pm
perl -pi -e "s,$cfg{'GS_LIB'} = q'';,$cfg{'GS_LIB'} = q'%{_datadir}/ghostscript/`ghostscript --version`';," cfgcache.pm
install -m0644 *.pm %{buildroot}%{_datadir}/latex2html
chmod +x %{buildroot}%{_datadir}/latex2html/makeseg/makeseg %{buildroot}%{_datadir}/latex2html/makemap

# install man pages
mkdir -p %{buildroot}%{_mandir}/man1
install -m0644 *.1 %{buildroot}%{_mandir}/man1
popd

# install japanese version
%if %{enable_japanese}
pushd %{name}-%{version}JA
sed -i "s,%{_prefix},%{buildroot}%{_prefix}," cfgcache.pm
perl -pi -e "s,latex2html pstoimg texexpand,jlatex2html jpstoimg jtexexpand," config/install.pl
perl -pi -e "s,/.*\\\$\{dd}texexpand,%{_bindir}/jtexexpand,;
	    s,/.*\\\$\{dd}pstoimg,%{_bindir}/jpstoimg,;
	    s,/.*\\\$\{dd}icons,\\\$\{LATEX2HTMLDIR}/icons,;
	    s,/.*\\\$\{dd}styles\\\$\{dd}rgb.txt,\\\$\{LATEX2HTMLDIR}/styles/rgb.txt,;
	    s,/.*\\\$\{dd}styles\\\$\{dd}crayola.txt,\\\$\{LATEX2HTMLDIR}/styles/crayola.txt," jlatex2html
sed -i "s,%{buildroot},," l2hconf.pm

make install
rm -rf %{buildroot}%{_datadir}/jlatex2html/versions/table.pl.orig \
       %{buildroot}%{_datadir}/jlatex2html/docs/ \
       %{buildroot}%{_datadir}/jlatex2html/example/
sed -i "s,/usr/local/bin/perl,/usr/bin/perl," %{buildroot}%{_datadir}/jlatex2html/makeseg/makeseg
sed -i "s,/usr/local/bin/perl,/usr/bin/perl," %{buildroot}%{_datadir}/jlatex2html/makemap
sed -i "s,###\!.*,," %{buildroot}%{_datadir}/jlatex2html/makemap 
sed -i "s,###\!.*,," %{buildroot}%{_datadir}/jlatex2html/makeseg/makeseg
sed -i "s,%{buildroot},," %{buildroot}%{_bindir}/jpstoimg
sed -i "s,%{buildroot},," %{buildroot}%{_bindir}/jtexexpand
sed -i "s,%{buildroot},," cfgcache.pm
sed -i "s,$cfg{'srcdir'}.*,$cfg{'srcdir'} = q'%{name}-%{version}JA';," cfgcache.pm
perl -pi -e "s,$cfg{'GS_LIB'} = q'';,$cfg{'GS_LIB'} = q'%{_datadir}/ghostscript/`ghostscript --version`';," cfgcache.pm
install -m0644 *.pm %{buildroot}%{_datadir}/jlatex2html
chmod +x %{buildroot}%{_datadir}/jlatex2html/makeseg/makeseg %{buildroot}%{_datadir}/jlatex2html/makemap
popd
%endif

# do not clash with texlive, prefer url.sty from texlive instead
rm -f %{buildroot}%{_datadir}/texmf/tex/latex/html/url.sty

%post
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :

%check
make -C %{name}-%{version} check
%if %{enable_japanese}
make -C %{name}-%{version}JA check
%endif

%files
%doc latex2html-%{version}/{LICENSE,README.md,FAQ,BUGS,docs,example}
%{_bindir}/latex2html
%{_bindir}/pstoimg
%{_bindir}/texexpand
%dir %{_datadir}/latex2html
%{_datadir}/latex2html/*
%dir %{_datadir}/texmf/tex/latex/html
%{_datadir}/texmf/tex/latex/html/*

%if %{enable_japanese}
%{_bindir}/jlatex2html
%{_bindir}/jpstoimg
%{_bindir}/jtexexpand
%dir %{_datadir}/jlatex2html
%{_datadir}/jlatex2html/*
%endif

%{_mandir}/man1/latex2html.*
%{_mandir}/man1/texexpand.*
%{_mandir}/man1/pstoimg.*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Than Ngo <than@redhat.com> - 2023.2-6
- Remove .orig files

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Than Ngo <than@redhat.com> - 2023.2-1
- update to 2023.2

* Mon Jan 30 2023 Ben Cotton <bcotton@fedoraproject.org> - 2020.2-8
- Update License field to match SPDX formatting

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Jindrich Novy <jnovy@redhat.com> - 2020.2-1
- update to 2020.2 and l2h-2020

* Tue Mar 24 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2019.2-5
- Add perl dependencies needed for build

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Than Ngo <than@redhat.com> - 2019.2-3
- add Requirement on tex(preview.sty)

* Wed Sep 11 2019 Than Ngo <than@redhat.com> - 2019.2-2
- update URL

* Wed Sep 11 2019 Than Ngo <than@redhat.com> - 2019.2-1
- update to v2019.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Ben Cotton <bcotton@fedoraproject.org> - 2018.3-1
- Update to latest upstream version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Ben Cotton <bcotton@fedoraproject.org> - 2018.2-3
- Add patch to fix bz#1582267 (upstream issue 48) until next upstream release

* Fri Jun 22 2018 Than Ngo <than@redhat.com> - 2018.2-2
- update l2h-2017-jp20180308

* Fri Jun 22 2018 Than Ngo <than@redhat.com> - 2018.2-1
- update to 2018.2
- add check

* Thu Jun 14 2018 Than Ngo <than@redhat.com> - 2017.2-6
- fixed bz#1591144, buildroot issue

* Fri May 11 2018 Than Ngo <than@redhat.com> - 2017.2-5
- fixed FTBFS

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Ben Cotton <bcotton@fedoraproject.org> 2017.2-2
- Update Perl commands in spec file to use valid syntax

* Mon Jun 26 2017 Tom Callaway <spot@fedoraproject.org> 2017.2-1
- update to 2017.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2012-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2012-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2012-3
- Perl 5.18 rebuild

* Tue Jan 29 2013 Jindrich Novy <jnovy@redhat.com> 2012-2
- prefer url.sty from texlive (#904888)

* Wed Nov 21 2012 Jindrich Novy <jnovy@redhat.com> 2012-1
- update to latex2html 2012
- update URL

* Thu Nov 15 2012 Jindrich Novy <jnovy@redhat.com> 2008-8
- BR: netpbm-progs to fix build

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 11 2009 Jindrich Novy <jnovy@redhat.com> 2008-4
- require netpbm-progs
- review fixes (#225980):
  - include documentation
  - set executable bit for makeseg and makemap scripts
  - white-space spec correction
  - move docs and example directory to %%doc
  - nuke duplicated stuff

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 02 2009 Jindrich Novy <jnovy@redhat.com> 2008
- update to latex2html-2008
- license changed to GPL
- update japanese support to l2h-2K8-jp20081220
- update cfgcache.pm
- fix BR

* Mon Jan 07 2008 Jindrich Novy <jnovy@redhat.com> 2002.2.1-8
- fix post/postun scriptlets

* Wed Nov 29 2006 Jindrich Novy <jnovy@redhat.com> 2002.2.1-7
- add dist tag, fix BuildRoot
- fix typo in description

* Tue Jun 27 2006 Jindrich Novy <jnovy@redhat.com> 2002.2.1-6
- remove .pdvips patch
- man pages are now stored in tar.gz
- rebuilt

* Sun Jun 25 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- fix BuildRequires to be rebuilt with mock (#191762)
- fix spec file scripts.
- update source files (use tar.gz with the date 20041025 and 2.1b1.6 Japanese patch)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 24 2005 Jindrich Novy <jnovy@redhat.com> 2002.2.1-5
- fix path to rgb.txt, thanks to Ville Skyttä (#174089)

* Tue Jun 21 2005 Jindrich Novy <jnovy@redhat.com> 2002.2.1-4
- remove '\n' causing that pstoimg generates gray images
  (#161186, #127010), solution from Julius Smith

* Wed May  4 2005 Jindrich Novy <jnovy@redhat.com> 2002.2.1-3
- add latex2html, texexpand, pstoimg man pages (#60308)

* Tue May  3 2005 Jindrich Novy <jnovy@redhat.com> 2002.2.1-2
- run texhash in the %%post and %%postun phase (#156660)

* Tue Mar 15 2005 Jindrich Novy <jnovy@redhat.com> 2002.2.1-1
- create backups for patches
- update Source1
- BuildArchitectures -> BuildArch
- remove direct RPM_BUILD_ROOT links from l2hconf.pm
- fix bad interpreter name path in pstoimg, texexpand
- define --with-texpath explicitely
- remove Dos.pm, Mac.pm, OS2.pm, Win32.pm
- don't require the font directory to be ended with PATH/fonts

* Wed Dec 15 2004 MATSUURA Takanori <t-matsuu@sx-lx3.protein.net>
- Initial build.
