#
# spec file for package graphviz
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

# Plugins version
%global pluginsver 6

Summary:        Graph Visualization Tools
Name:           graphviz
Version:        9.0.0
Release:        1%{?dist}
License:        EPL-1.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.graphviz.org/
Source0:        https://gitlab.com/api/v4/projects/%{name}%2F%{name}/packages/generic/%{name}-releases/%{version}/%{name}-%{version}.tar.xz
BuildRequires:       gcc-g++
BuildRequires:       zlib-devel
BuildRequires:       libpng-devel
BuildRequires:       libjpeg-devel
BuildRequires:       expat-devel
BuildRequires:       freetype-devel >= 2
BuildRequires:       ksh
BuildRequires:       bison
BuildRequires:       m4
BuildRequires:       flex
BuildRequires:       tcl-devel >= 8.3
BuildRequires:       swig
BuildRequires:       sed
BuildRequires:       fontconfig-devel
BuildRequires:       libtool-ltdl-devel
BuildRequires:       ruby-devel
BuildRequires:       ruby
BuildRequires:       libXt-devel
BuildRequires:       libXmu-devel
BuildRequires:       python3-devel
BuildRequires:       libXaw-devel
BuildRequires:       libSM-devel
BuildRequires:       libXext-devel
BuildRequires:       cairo-devel >= 1.1.10
BuildRequires:       pango-devel
BuildRequires:       gmp-devel
BuildRequires:       lua-devel
BuildRequires:       gd-devel
BuildRequires:       perl-devel
BuildRequires:       swig >= 1.3.33
BuildRequires:       automake
BuildRequires:       autoconf
BuildRequires:       libtool
#BuildRequires:       qpdf
# Temporary workaound for perl(Carp) not pulled
BuildRequires:       perl-Carp
BuildRequires:       perl-ExtUtils-Embed
BuildRequires:       perl-generators
#BuildRequires:       librsvg2-devel
# for ps2pdf
#BuildRequires:       libgs-devel
BuildRequires:       make


Requires:       freefont

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A collection of tools for the manipulation and layout of graphs (as in nodes
and edges, not as in barcharts).

%package devel
Summary:        Development package for graphviz
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-gd = %{version}-%{release}

%description devel
A collection of tools for the manipulation and layout of graphs (as in nodes
and edges, not as in barcharts). This package contains development files for
graphviz.

%package ruby
Summary:		Ruby extension for graphviz
Requires:		%{name} = %{version}-%{release}, ruby
 
%description ruby
Ruby extension for graphviz.

%package doc
Summary:        PDF and HTML documents for graphviz

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%package gd
Summary:        Graphviz plugin for renderers based on gd
Requires:       %{name} = %{version}-%{release}
Requires:       freefont
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description gd
Graphviz plugin for renderers based on gd.  (Unless you absolutely have to use
GIF, you are recommended to use the PNG format instead because of the better
quality anti-aliased lines provided by the cairo+pango based renderer.)

%package graphs
Summary:        Demo graphs for graphviz

%description graphs
Some demo graphs for graphviz.

%package lua
Summary:        Lua extension for graphviz
Requires:       %{name} = %{version}-%{release}
Requires:       lua

%description lua
Lua extension for graphviz.

%package perl
Summary:        Perl extension for graphviz
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description perl
Perl extension for graphviz.

%package python3
Summary:        Python 3 extension for graphviz
Requires:       %{name} = %{version}-%{release}
# Manually add provides that would be generated automatically if .egg-info was present
Provides:       python3dist(gv) = %{version}
Provides:       python%{python3_version}dist(gv) = %{version}

%description python3
Python 3 extension for graphviz.

%package tcl
Summary:        Tcl extension & tools for graphviz
Requires:       %{name} = %{version}-%{release}
Requires:       tcl >= 8.3

%description tcl
Various tcl packages (extensions) for the graphviz tools.

%prep
%autosetup -p1

# Attempt to fix rpmlint warnings about executable sources
find -type f -regex '.*\.\(c\|h\)$' -exec chmod a-x {} ';'

%build
autoreconf -fi

%configure --with-x --disable-static --disable-dependency-tracking \
    --without-mylibgd --with-ipsepcola --with-pangocairo \
    --without-gdk-pixbuf --with-visio --disable-silent-rules \
    --without-ruby --without-python2 \
    --with-freetypeincludedir=%{_includedir}/freetype2 --with-freetypelibdir=%{_libdir}/lib \
    --without-lasi \
    --without-gts \
    --disable-sharp \
    --disable-ocaml \
    --without-ming \
    --disable-r \
    --without-devil \
    --without-qt

# drop rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build CFLAGS="%{optflags} -fno-strict-aliasing -fno-strict-overflow %{?FFSTORE}" \
  CXXFLAGS="%{optflags} -fno-strict-aliasing -fno-strict-overflow %{?FFSTORE}"

%install
%make_install DESTDIR=%{buildroot} \
	docdir=%{_docdir}/%{name} \
	pkgconfigdir=%{_libdir}/pkgconfig 

find %{buildroot} -type f -name "*.la" -delete -print

# Move docs to the right place
#mkdir -p %{buildroot}%{_docdir}/%{name}
#mv %{buildroot}%{_datadir}/%{name}/doc/* %{buildroot}%{_docdir}/%{name}

# Install README
install -m0644 README %{buildroot}%{_docdir}/%{name}

# Remove executable modes from demos
find %{buildroot}%{_datadir}/%{name}/demo -type f -exec chmod a-x {} ';'

# Move demos to doc
mv %{buildroot}%{_datadir}/%{name}/demo %{buildroot}%{_docdir}/%{name}/

# Rename python demos to prevent byte compilation
find %{buildroot}%{_docdir}/%{name}/demo -type f -name "*.py" -exec mv {} {}.demo ';'

# Remove dot_builtins, on demand loading should be sufficient
rm -f %{buildroot}%{_bindir}/dot_builtins

# These are part of gnome subpkg
rm -f %{buildroot}%{_libdir}/graphviz/libgvplugin_pango*
rm -f %{buildroot}%{_libdir}/graphviz/libgvplugin_xlib*
# This is part of the x11 subpkg only
rm -rf %{buildroot}%{_datadir}/graphviz/lefty
rm -f %{buildroot}%{_mandir}/man1/{lefty.1*}

# python 3
install -pD tclpkg/gv/.libs/libgv_python3.so %{buildroot}%{python3_sitearch}/_gv.so
install -p tclpkg/gv/gv.py %{buildroot}%{python3_sitearch}/gv.py

# Ghost plugins config
touch %{buildroot}%{_libdir}/graphviz/config%{pluginsver}

# Fix lua file placement for flatpak
if [ "%{_prefix}" != "/usr" ]; then
  cp -ru %{buildroot}/usr/* %{buildroot}%{_prefix}/
  rm -rf %{buildroot}/usr/*
fi

%check
# upstream test suite
# testsuite seems broken, disabling it for now
# cd rtest
# make rtest

%post
%{?ldconfig}
%{_bindir}/dot -c 2>/dev/null || :

%{ldconfig_postun}

# run "dot -c" to generate plugin config in %%{_libdir}/graphviz/config*
%post gd
%{_bindir}/dot -c 2>/dev/null || :
%{?ldconfig}

%postun gd
%{_bindir}/dot -c 2>/dev/null || :
%{?ldconfig}

%files
%license COPYING
%doc %{_docdir}/%{name}
%{_bindir}/*
%dir %{_libdir}/graphviz
%{_libdir}/*.so.*
%{_libdir}/graphviz/*.so.*
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*
%dir %{_datadir}/graphviz
%exclude %{_docdir}/%{name}/*.html
%exclude %{_docdir}/%{name}/*.pdf
%exclude %{_docdir}/%{name}/demo
%{_datadir}/graphviz/gvpr
%ghost %{_libdir}/graphviz/config%{pluginsver}

%exclude %{_libdir}/graphviz/*/*
%exclude %{_libdir}/graphviz/libgvplugin_gd.*

%files devel
%{_includedir}/graphviz
%{_libdir}/*.so
%{_libdir}/graphviz/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

%files doc
%doc %{_docdir}/%{name}/*.html
%doc %{_docdir}/%{name}/*.pdf
%doc %{_docdir}/%{name}/demo

%files gd
%{_libdir}/graphviz/libgvplugin_gd.so.*

%files graphs
%dir %{_datadir}/graphviz
%{_datadir}/graphviz/graphs

%files lua
%{_libdir}/graphviz/lua/
%{_prefix}/lib64/lua*/*
%{_mandir}/man3/gv.3lua*

%files perl
%{_libdir}/graphviz/perl/
%{_libdir}/perl*/*
%{_mandir}/man3/gv.3perl*

%files python3
%{python3_sitearch}/*
%{_mandir}/man3/gv.3python*

%files ruby
%{_libdir}/graphviz/ruby/
%{_libdir}/*ruby*/*
%{_mandir}/man3/gv.3ruby*

%files tcl
%{_libdir}/graphviz/tcl/
%{_prefix}/lib64/tcl*/*
# hack to include gv.3tcl only if available
# always includes tcldot.3tcl, gdtclft.3tcl
%{_mandir}/man3/*.3tcl*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.42.4-9
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jun 22 2023 Osama Esmail <osamaesmail@microsoft.com> - 2.42.4-8
- Trying some more `freefont` fixes (added Requires to gd)
- Added freetype option to build
- `dot` complains about not having URW1 fonts, but works anyway

* Wed Mar 08 2023 Osama Esmail <osamaesmail@microsoft.com> - 2.42.4-7
- Add `freefont` to BuildRequires to provide default font for graphviz

* Thu Apr 21 2022 Minghe Ren <mingheren@microsoft.com> - 2.42.4-6
- Add patch for CVE-2020-18032

* Mon Jan 31 2022 Thomas Crain <thcrain@microsoft.com> - 2.42.4-5
- Remove option to build with python2

* Wed Jan 26 2022 Henry Li <lihl@microsoft.com> - 2.42.4-4
- Add perl as BR
- License Verified
- Fix linting
- Remove usage of {?ext_man}, which is not supported in CBL-Mariner

* Tue Jun 22 2021 Thomas Crain <thcrain@microsoft.com> - 2.42.4-3
- Use pkgconfig(cairo) instead of cairo-devel build requirement

* Thu Dec 17 2020 Joe Schmitt <joschmit@microsoft.com> - 2.42.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove X11 dependencies and extra language bindings.
- Use `/usr/lib` instead of `/usr/lib64`

* Mon Apr  6 2020 Jaroslav �karvada <jskarvad@redhat.com> - 2.42.4-1
- New version
  Resolves: rhbz#1821045
- Switched to bz2 archives
- Dropped ocaml-allow-const-cast patch (upstreamed)

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 2.42.2-10
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 2.42.2-9
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.42.2-7
- F-32: rebuild against ruby27

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 2.42.2-6
- Bump release and rebuild.

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 2.42.2-5
- OCaml 4.10.0+beta1 rebuild.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 2.42.2-4
- OCaml 4.09.0 (final) rebuild.

* Thu Oct 31 2019 Miro Hroncok <mhroncok@redhat.com> - 2.42.2-3
- Remove Python 2 package on Fedora 32+

* Fri Oct 04 2019 Remi Collet <remi@remirepo.net> - 2.42.2-2
- rebuild for https://fedoraproject.org/wiki/Changes/php74

* Wed Oct  2 2019 Jaroslav �karvada <jskarvad@redhat.com> - 2.42.2-1
- New version
  Resolves: rhbz#1753061
- Dropped visio, python3, CVE-2018-10196, CVE-2019-11023, and
  swig4-updated-language-options patches (all upstreamed)
- Simplified python bindings build process

* Wed Oct 02 2019 Orion Poplawski <orion@nwra.com> - 2.40.1-58
- Rebuild for lasi 1.1.3 soname bump

* Mon Aug 19 2019 Miro Hroncok <mhroncok@redhat.com> - 2.40.1-57
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-56
- OCaml 4.08.1 (final) rebuild.

* Fri Aug 09 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.40.1-55
- Glob remaining man pages.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-54
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-52
- OCaml 4.08.0 (final) rebuild.

* Tue Jun 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.40.1-51
- Perl 5.30 re-rebuild updated packages

* Mon Jun  3 2019 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-50
- Fixed FTBFS with python-3.8

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.40.1-49
- Perl 5.30 rebuild

* Tue May  7 2019 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-48
- Fixed FTBFS caused by swig-4.0.0
  Resolves: rhbz#1707435

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-47
- OCaml 4.08.0 (beta 3) rebuild.

* Wed Apr 24 2019 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-46
- Updated CVE-2019-11023 patch
  Related: CVE-2019-11023

* Wed Apr 24 2019 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-45
- Fixed null pointer dereference in function agroot()
  Resolves: CVE-2019-11023

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 V�t Ondruch <vondruch@redhat.com> - 2.40.1-43
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Mon Jan 14 2019 Bj�rn Esser <besser82@fedoraproject.org> - 2.40.1-42
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Dec  7 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-41
- Fixed some issues found by coverity scan

* Thu Oct 18 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-40
- Clarified license tag

* Mon Oct 15 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-39
- Dropped rpath

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 2.40.1-38
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Wed Sep 26 2018 Kevin Fenzi <kevin@scrye.com> - 2.40.1-37
- Don't fail on post scriptlet failures.

* Wed Jul 18 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-36
- Fixed ghostscript requirements

* Wed Jul 18 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-35
- Conditionalized php support

* Tue Jul 17 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-34
- Fixed menu in dotty
  Resolves: rhbz#1505230

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-32
- Updated source URL

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-31
- OCaml 4.07.0 (final) rebuild.

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2.40.1-30
- Perl 5.28 rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.40.1-29
- Perl 5.28 rebuild

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-28
- OCaml 4.07.0-rc1 rebuild.

* Tue Jun 19 2018 Miro Hroncok <mhroncok@redhat.com> - 2.40.1-27
- Rebuilt for Python 3.7

* Thu May 17 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-26
- Fixed CVE-2018-10196

* Thu May  3 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-25
- Made python2 package optional

* Wed May  2 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-24
- Added support for python3

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-23
- OCaml 4.07.0-beta2 rebuild.

* Sat Apr 14 2018 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.1-22
- Rename python2 subpackage to graphviz-python2, because
  there is intent to package python-graphviz, which is a separate project
  from graphviz.

* Thu Mar  8 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-21
- Dropped libgnomeui-devel requirement, libgnomeui support has been
  dropped long time ago in upstream

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-19
- Rebuilt with urw-base35-fonts

* Sat Jan 20 2018 Bj�rn Esser <besser82@fedoraproject.org> - 2.40.1-18
- Rebuilt for switch to libxcrypt

* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.40.1-17
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Jan 15 2018 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-16
- Switched to libgs-devel
  Resolves: rhbz#1534666
- Made the build verbose (without silent rules)

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.40.1-15
- F-28: rebuild for ruby25

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-14
- OCaml 4.06.0 rebuild.

* Wed Oct 04 2017 Remi Collet <remi@fedoraproject.org> - 2.40.1-13
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Sun Aug 20 2017 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.1-12
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.1-11
- Python 2 binary package renamed to python2-graphviz
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-10
- OCaml 4.05.0 rebuild.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-7
- OCaml 4.04.2 rebuild.

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.40.1-6
- Perl 5.26 rebuild

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-5
- OCaml 4.04.1 rebuild.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-3
- Re-enabled PHP support

* Thu Jan 12 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.40.1-2
- F-26: rebuild for ruby24

* Mon Jan  2 2017 Jaroslav �karvada <jskarvad@redhat.com> - 2.40.1-1
- New version
  Resolves: rhbz#1406954
- Dropped rtest-fix, find-fix, ocaml-fix-ints, format-string,
  vimdot-vi, rbconfig, gs-9.18-fix patches (all upstreamed)
- Defuzzified visio patch

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-40
- Rebuild for OCaml 4.04.0.

* Fri Oct 14 2016 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-39
- Fixed build with ghostscript-9.18+
  Resolves: rhbz#1384016

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-38
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-37
- Conditionalized php support and disabled it due to rhbz#1356985

* Fri Jul 15 2016 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-36
- Rebuilt for php

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.38.0-35
- Perl 5.24 rebuild

* Fri Feb 26 2016 Than Ngo <than@redhat.com> - 2.38.0-34
- rebuilt

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 V�t Ondruch <vondruch@redhat.com> - 2.38.0-32
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Tue Dec  1 2015 Tom Callaway <spot@fedoraproject.org> - 2.38.0-31
- rebuild for libvpx 1.5.0

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-30
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-29
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-28
- ocaml-4.02.2 rebuild.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-26
- Fixed built with visio (by visio patch)
- Enabled visio support
  Resolves: rhbz#1231896

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.38.0-25
- Perl 5.22 rebuild

* Fri May 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.38.0-24
- Fix mono directive orders

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.38.0-23
- Rebuild (mono4)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.38.0-22
- Rebuilt for GCC 5 C++11 ABI change

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 2.38.0-21
- rebuild for libvpx 1.4.0

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-20
- ocaml-4.02.1 rebuild.

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.38.0-19
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Fix obsolete Config:: usage

* Fri Jan 16 2015 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-18
- Make vimdot to work with vi, dropped explicit vim-ehnanced requirement
  Resolves: rhbz#1182764

* Tue Nov 25 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-17
- Fixed format string vulnerability
  Resolves: rhbz#1167868

* Tue Nov 11 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-16
- Added ISO8859-1 fonts as requirement
  Resolves: rhbz#1058323
- Fixed spurious whitespaces

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.38.0-15
- Perl 5.20 rebuild

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-14
- ocaml-4.02.0 final rebuild.
- Add patch to fix build with OCaml > 4.02.0 and Fedora 22.

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.38.0-12
- Perl 5.20 rebuild

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-11
- ocaml-4.02.0+rc1 rebuild.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-9
- Rebuilt for new ocaml

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 2.38.0-8
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file
- cleanup filter (no more needed in F20+)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.38.0-6
- Re-enable R bindings on aarch64, we now have it

* Wed May 28 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-5
- Fixed crash by adding additional check to findVertical/Horizontal functions
  (by find-fix patch provided by Mattias Ellert <mattias.ellert@fysast.uu.se>)
  Resolves: rhbz#1095419

* Tue May 20 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-4
- Rebuilt for tcl/tk8.6

* Thu Apr 24 2014 V�t Ondruch <vondruch@redhat.com> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-2
- Remove ocaml_arches macro (RHBZ#1087794).

* Mon Apr 14 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.38.0-1
- New version
  Resolves: rhbz#1052160
- Dropped testsuite-sigsegv-fix, rtest-errout-fix, lefty-getaddrinfo,
  CVE-2014-0978-CVE-2014-1235, CVE-2014-1236, ppc64le-support
  patches (all upstreamed)
- Added rtest-fix patch (sent upstream)
- Disabled test suite (for now)

* Wed Mar 19 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.34.0-9
- Added ppc64le support
  Resolves: rhbz#1078464

* Thu Jan  9 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.34.0-8
- Prevent possible buffer overflow in yyerror()
  Resolves: CVE-2014-1235
- Fix possible buffer overflow problem in chkNum of scanner
  Resolves: CVE-2014-1236

* Tue Jan  7 2014 Jaroslav �karvada <jskarvad@redhat.com> - 2.34.0-7
- Fixed overflow in yyerror
  Resolves: CVE-2014-0978

* Sat Dec 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.34.0-6
- Disable R bindings on aarch64 for the moment

* Thu Dec 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.34.0-5
- No mono on aarch64

* Thu Oct 31 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.34.0-4
- Removed metadata from generated PDFs
  Related: rhbz#881173

* Thu Oct 31 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.34.0-3
- Fixed multilib conflicts
  Rewrote lefty IO lib to use getaddrinfo instead of gethostbyname
  (by lefty-getaddrinfo patch)
  Resolves: rhbz#881173

* Mon Sep 16 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.34.0-2
- Added explicit dependency on vim (required by vimdot)

* Mon Sep 16 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.34.0-1
- New version
  Resolves: rhbz#1005957
- Dropped perl-fix patch (upstreamed)

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 2.32.0-2
- Rebuild for OCaml 4.01.0.

* Mon Aug 19 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.32.0-1
- New version
  Resolves: rhbz#991752
- Dropped guile2-fix, cgraph, lua-52, smyrna-doc-opt, gv2gml-options-fix,
  lefty-help, prune-help, man-fix patches (all upstreamed)

* Tue Aug  6 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.1-14
- Used unversioned doc directory
  Resolves: rhbz#993803

* Mon Aug  5 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.1-13
- Fixed FTBFS related to perl config
  Resolves: rhbz#991915

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.30.1-11
- Perl 5.18 rebuild

* Fri Jul 12 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.1-10
- Various man and built-in help fixes

* Tue Jun 25 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.1-9
- Fixed handling of the libdir/graphviz directory

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.30.1-8
- rebuild for new GD 2.1.0

* Wed May 15 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-7
- rebuild for lua 5.2

* Tue Apr 23 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-6
- patch libgvc.pc.in to refer to -lcgraph (-lgraph is dead and gone)

* Thu Apr 11 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-5
- rebuild for R3 (may not be needed, but better safe than sorry)

* Mon Mar 25 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.1-4
- Added support for aarch64
  Resolves: rhbz#925487

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 2.30.1-3
- rebuild for http://fedoraproject.org/wiki/Features/Php55
- add explicit BuildRequires: perl-Carp (workaround)

* Thu Mar 14 2013 V�t Ondruch <vondruch@redhat.com> - 2.30.1-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Feb 15 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.1-1
- New version
  Resolves: rhbz#911520
  Resolves: rhbz#704529

* Thu Jan 24 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.0-3
- Used ocaml_arches macros to enable ocaml on supported arches

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.30.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Mon Jan 14 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.30.0-1
- New version
  Resolves: rhbz#895027
- Dropped guile-detect, ocaml4 patches (not needed)
- Fixed bogus date in changelog (guessing)

* Wed Jan  9 2013 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-26
- Rebuilt with -fno-strict-overflow to workaround the overflow problem
  (upstream ticket: http://www.graphviz.org/mantisbt/view.php?id=2244)
- The dot_builtins was removed rather then excluded to fix the dangling
  symlinks problem in debuginfo

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.28.0-25
- rebuild against new libjpeg

* Wed Oct 17 2012 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-24
- Rebuilt for new ocaml

* Fri Aug 17 2012 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-23
- Silenced 'dot -c' errors/warnings in post/postun
- Do not remove dot config in plugins post/postun

* Fri Aug 17 2012 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-22
- dot_builtins no longer installed (lowers implicit deps)
- Fixed post/postuns for plugins
- Removed -ffast-math, added -ffloat-store (on i386) to fix arithmetic on i386

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 2.28.0-20
- Perl 5.16 rebuild

* Sat Jun  9 2012 Richard W.M. Jones <rjones@redhat.com> - 2.28.0-19
- Rebuild for OCaml 4.00.0.
- Enable OCaml on arm and ppc64, since there are working native compilers
  for both.

* Wed May 23 2012 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-18
- Improved docs handling code in spec to be backward compatible with older RPM

* Tue May 22 2012 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-17
- All docs are now installed into /usr/share/doc/graphviz-%%{version}
- Demos packaged as docs not to automatically bring in unnecessary deps

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-16
- Rebuilt for c++ ABI breakage

* Thu Feb 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.28.0-15
- fix CPPFLAGS export so it doesn't cause issues on ARM

* Mon Feb 06 2012 V�t Ondruch <vondruch@redhat.com> - 2.28.0-14
- Rebuilt for Ruby 1.9.3.

* Wed Jan 18 2012 Remi Collet <remi@fedoraproject.org> - 2.28.0-13
- build against php 5.4.0
- add filter to fix private-shared-object-provides
- add %%check for php extension

* Sun Jan 08 2012 Richard W.M. Jones <rjones@redhat.com> - 2.28.0-12
- Rebuild for OCaml 3.12.1.

* Thu Dec  8 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-11
- Added conditionals for ARRRR, DEVIL, QTAPPS (gvedit), GTS, LASI
- Fixed conditionals for SHARP, OCAML
- Built with gts, ghostscript, rsvg and lasi
  Resolves: rhbz#760926
- Disabled gvedit
  Resolves: rhbz#751807
- Fixed rpmlint warnings about executable sources

* Wed Nov  9 2011 Tom Callaway <spot@fedoraproject.org> - 2.28.0-10
- rebuild for R 2.14.0

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.28.0-9
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.28.0-8
- Perl mass rebuild

* Thu Jul 07 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-7
- Added gd as devel requirement

* Fri Jun 17 2011 Marcela Ma�l�nov� <mmaslano@redhat.com> - 2.28.0-6
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Ma�l�nov� <mmaslano@redhat.com> - 2.28.0-5
- Perl 5.14 mass rebuild

* Thu May 19 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-4
- Fixed detection of guile 2.x
  Resolves: rhbz#704529

* Fri May 13 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-3
- Corrected license tag, the graphviz license is now EPL

* Fri May 13 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-2
- Recompiled with -fno-strict-aliasing in CXXFLAGS

* Tue May 10 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.28.0-1
- New version 2.28.0
- Added perl-ExtUtils-Embed to BuildRequires, it is now required
- Fixed build failure due to change in php_zend_api macro type
- Removed sparc64, gtk-progname, doc-index-fix, ppc-darwinhack
  patches (all were upstreamed)

* Thu Mar 03 2011 Oliver Falk <oliver@linux-kernel.at> - 2.26.3-5
- Disable mono and ocaml on alpha

* Tue Feb 22 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.26.3-4
- Added urw-fonts to requires (#677114)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Karsten Hopp <karsten@redhat.com> 2.26.3-2
- fix hack for powerpc-darwin8 in configure

* Thu Jan 06 2011 Jaroslav �karvada <jskarvad@redhat.com> - 2.26.3-1
- New version (#580017)
- Fixed gtk plugin program-name (#640671, gtk-progname patch)
- Fixed broken links in doc index (#642536, doc-index-fix patch)
- Fixed SIGSEGVs on testsuite (#645703, testsuite-sigsegv-fix patch)
- Testsuite now do diff check also in case of err output (#645703,
  rtest-errout-fix patch)
- Testsuite enabled on all arches (#645703)
- Added urw-fonts to BuildRequires
- Compiled with -fno-strict-aliasing
- Fixed rpmlint warnings on spec file
- Removed unused patches

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.26.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.26.0-3
- Mass rebuild with perl-5.12.0

* Mon Jan 04 2010 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.26.0-2
- Rebuild for updated ocaml
- Happy new year, Fedora!

* Fri Dec 18 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.26.0-1
- Updated to latest release
- Removed patches that have been applied upstream
- Fixed man page paths (mann -> man3)
- Disabled mono and ocaml for ARM (Jitesh Shah, BZ#532047)
- Disabled regression tests on sparc64 as well as ppc/ppc64 (Dennis Gilmore)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.3-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 2.20.3-4.1
- fix mistake in make rtest fix

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 2.20.3-4
- rebuild for new PHP 5.3.0 ABI (20090626)
- add PHP ABI check
- use php_extdir (and don't own it)
- add php configuration file (/etc/php.d/graphviz.ini)

* Mon Mar  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.20.3-3
- this spec makes baby animals cry... massively clean it up
- hack in java includes to build against openjdk
- add ruby as a BuildRequires (configure checks for /usr/bin/ruby)

* Wed Feb 25 2009 John Ellson <ellson@graphviz.org> 2.20.3-2.2
- fixes for swig changes

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.3-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Karsten Hopp <karsten@redhat.com> 2.20.3-.2
- make it build on s390, s390x (#469044)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.20.3-1.1
- Rebuild for Python 2.6

* Mon Nov 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.20.3-1
- update to 2.20.3

* Sat Nov 22 2008 Rex Dieter <rdieter@fedoraproject.org> 2.16.1-0.7
- respin (libtool)

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.16.1-0.6
- fix conditional comparison

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.16.1-0.5
- add Requires for versioned perl (libperl.so)

* Tue Mar 04 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16.1-0.4
- Disable R support

* Mon Mar 03 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16.1-0.2
- New upstream release (fixes BZ#433205, BZ#427376)
- Merged spec changes in from upstream
- Added patch from BZ#432683

* Tue Feb 12 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-3.3
- Added upstream-provided patch for building under GCC 4.3 (thanks John!)

* Thu Jan  3 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-3.2
- Re-added tcl/tk 8.5 patch
- Tweaked ming stuff

* Thu Jan  3 2008 Alex Lancaster <alexlan[AT]fedoraproject.org> - 2.16-3.1
- Rebuild against new Tcl 8.5

* Wed Dec 12 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-2
- What the heck?  Can't BR stuff that hasn't even gotten reviewed yet.

* Wed Nov 28 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-1
- New upstream release
- Remove arith.h patch

* Tue Sep 04 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.14.1-3
- Patch to resurrect arith.h

* Thu Aug 23 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.14.1-2
- Added perl-devel to BR for F7+

* Wed Aug 15 2007 John Ellson <ellson@research.att.com>
- release 2.14.1 - see ChangeLog for details

* Thu Aug 2 2007 John Ellson <ellson@research.att.com>
- release 2.14 - see ChangeLog for details

* Fri Mar 16 2007 Stephen North <north@research.att.com>
- remove xorg-X11-devel from rhel >= 5

* Mon Dec 11 2006 John Ellson <john.ellson@comcast.net>
- fix graphviz-lua description (Fedora BZ#218191)

* Tue Sep 13 2005 John Ellson <ellson@research.att.com>
- split out language bindings into their own rpms so that 
  main rpm doesn't depend on (e.g.) ocaml

* Sat Aug 13 2005 John Ellson <ellson@research.att.com>
- imported various fixes from the Fedora-Extras .spec by Oliver Falk <oliver@linux-kernel.at>

* Wed Jul 20 2005 John Ellson <ellson@research.att.com>
- release 2.4
