%if 0%{?rhel} >= 8
%bcond_with php
%bcond_with guile
%else
# temporal drop of PHP support due to https://gitlab.com/graphviz/graphviz/-/issues/2277
%bcond_with php
%bcond_without guile
%endif
%bcond_with python2

# Macro for creating an option which enables bootstraping build without dependencies,
# which cause problems during rebuilds. Currently it is circular dependency of graphviz and
# doxygen - in case a dependency of graphviz/doxygen bumps SONAME and graphviz/doxygen
# has to be rebuilt, we can break the circular dependency by building with --with bootstrap.
%bcond_with bootstrap

%if 0%{?rhel} >= 10
%bcond_with gtk2
%else
%bcond_without gtk2
%endif

# Necessary conditionals
%ifarch %{mono_arches}
%global SHARP  1
%else
%global SHARP  0
%endif

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
%ifnarch %{ix86}
%global OCAML  1
%else
%global OCAML  0
%endif

%global DEVIL  1
%global ARRRR  1

# Build with QT applications (currently only gvedit)
# Disabled until the package gets better structuring, see bug #447133
%global QTAPPS 0

%global GTS    1
%global LASI   1

# Not in Fedora yet.
%global MING   0

%ifarch %{java_arches}
%global JAVA 1
%else
%global JAVA 0
%endif

%if 0%{?rhel}
%global SHARP  0
%global ARRRR  0
%global DEVIL  0
%global GTS    0
%global LASI   0
%endif

%if %{GTS} && %{with gtk2}
%global SMYRNA 1
%else
%global SMYRNA 0
%endif

%if %{with php}
%global PHP 1
%else
%global PHP 0
%endif

%if %{with guile}
%global GUILE 1
%else
%global GUILE 0
%endif

%ifarch %{golang_arches}
%global GOLANG 1
%else
%global GOLANG 0
%endif

# Plugins version
%global pluginsver 6

%global php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)

%if "%{php_version}" < "5.6"
%global ini_name     %{name}.ini
%else
%global ini_name     40-%{name}.ini
%endif

# Fix for the 387 extended precision (rhbz#772637)
%ifarch i386 i686
%global FFSTORE -ffloat-store
%endif

Name:			graphviz
Summary:		Graph Visualization Tools
Version:		9.0.0
Release:		10%{?dist}
# Add license:
License:		epl-1.0 AND cpl-1.0 AND bsd-3-clause AND mit AND gpl-3.0-or-later WITH bison-exception-2.2 AND apache-1.1 AND lgpl-2.0-or-later WITH libtool-exception AND smlnj AND hpnd-uc
URL:			http://www.graphviz.org/
#Source0:		https://gitlab.com/%%{name}/%%{name}/-/archive/%%{version}/%%{name}-%%{version}.tar.bz2
Source0:		https://gitlab.com/api/v4/projects/%{name}%2F%{name}/packages/generic/%{name}-releases/%{version}/%{name}-%{version}.tar.xz
BuildRequires:		gcc-g++
BuildRequires:		zlib-devel
BuildRequires:		libpng-devel
BuildRequires:		libjpeg-devel
BuildRequires:		expat-devel
BuildRequires:		freetype-devel >= 2
BuildRequires:		ksh
BuildRequires:		bison
BuildRequires:		m4
BuildRequires:		flex
BuildRequires:		tk-devel
BuildRequires:		tcl-devel >= 8.3
BuildRequires:		swig
BuildRequires:		sed
BuildRequires:		fontconfig-devel
BuildRequires:		libtool-ltdl-devel
BuildRequires:		ruby-devel
BuildRequires:		ruby
BuildRequires:		libXt-devel
BuildRequires:		libXmu-devel
%if %{GUILE}
BuildRequires:		guile22-devel
%endif
%if %{with python2}
BuildRequires:		python2-devel
%endif
BuildRequires:		python3-devel
BuildRequires:		libXaw-devel
BuildRequires:		libSM-devel
BuildRequires:		libXext-devel
%if %{JAVA}
BuildRequires:		java-devel
BuildRequires:		javapackages-tools
%endif
BuildRequires:		cairo-devel >= 1.1.10
BuildRequires:		pango-devel
BuildRequires:		gmp-devel
BuildRequires:		lua-devel
%if %{with gtk2}
BuildRequires:		gtk2-devel
%endif
BuildRequires:		gd-devel
BuildRequires:		perl-devel
BuildRequires:		swig >= 1.3.33
BuildRequires:		automake
BuildRequires:		autoconf
BuildRequires:		libtool
BuildRequires:		qpdf
# Temporary workaound for perl(Carp) not pulled
BuildRequires:		perl-Carp
%if %{PHP}
BuildRequires:		php-devel
%endif
%if %{SHARP}
BuildRequires:		mono-core
%endif
%if %{DEVIL}
BuildRequires:		DevIL-devel
%endif
%if %{ARRRR}
BuildRequires:		R-devel
%endif
%if %{OCAML}
BuildRequires:		ocaml
%endif
%if %{QTAPPS}
BuildRequires:		qt-devel
%endif
%if %{GTS}
BuildRequires:		gts-devel
%endif
%if %{LASI}
BuildRequires:		lasi-devel
%endif
BuildRequires:		urw-base35-fonts
BuildRequires:		perl-ExtUtils-Embed
BuildRequires:		perl-generators
BuildRequires:		librsvg2-devel
# for ps2pdf
BuildRequires:		ghostscript
BuildRequires:		libgs-devel
BuildRequires:		make
BuildRequires:		poppler-glib-devel
BuildRequires:		freeglut-devel
%if %{SMYRNA}
BuildRequires:		libglade2-devel
BuildRequires:		gtkglext-devel
%endif
%if %{without bootstrap}
BuildRequires:		doxygen
%endif
%if %{GOLANG}
BuildRequires:		golang
%endif
Requires:		urw-base35-fonts
# rhbz#1838679
Patch0:			graphviz-4.0.0-gvpack-neato-static.patch
# https://gitlab.com/graphviz/graphviz/-/issues/2448
Patch1:			graphviz-9.0.0-doxygen-fix.patch

%if ! %{JAVA}
Obsoletes:              graphviz-java < %{version}-%{release}
%endif

%description
A collection of tools for the manipulation and layout of graphs (as in nodes
and edges, not as in barcharts).

%package devel
Summary:		Development package for graphviz
Requires:		%{name} = %{version}-%{release}, pkgconfig
Requires:		%{name}-gd = %{version}-%{release}

%description devel
A collection of tools for the manipulation and layout of graphs (as in nodes
and edges, not as in barcharts). This package contains development files for
graphviz.

%if %{DEVIL}
%package devil
Summary:		Graphviz plugin for renderers based on DevIL
Requires:		%{name} = %{version}-%{release}

%description devil
Graphviz plugin for renderers based on DevIL. (Unless you absolutely have
to use BMP, TIF, or TGA, you are recommended to use the PNG format instead
supported directly by the cairo+pango based renderer in the base graphviz rpm.)
%endif

%package doc
Summary:		PDF and HTML documents for graphviz

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%if %{SMYRNA}
%package smyrna
Summary:		Graphviz interactive graph viewer

%description smyrna
Smyrna is a viewer for graphs in the DOT format.
%endif

%package gd
Summary:		Graphviz plugin for renderers based on gd
Requires:		%{name} = %{version}-%{release}

%description gd
Graphviz plugin for renderers based on gd.  (Unless you absolutely have to use
GIF, you are recommended to use the PNG format instead because of the better
quality anti-aliased lines provided by the cairo+pango based renderer.)

%if %{with gtk2}
%package gtk2
Summary:		Graphviz plugin for renderers based on gtk2
Requires:		%{name} = %{version}-%{release}

%description gtk2
Graphviz plugin for renderers based on gtk2.
%endif

%package graphs
Summary:		Demo graphs for graphviz

%description graphs
Some demo graphs for graphviz.

%if %{GUILE}
%package guile
Summary:		Guile extension for graphviz
Requires:		%{name} = %{version}-%{release}

%description guile
Guile extension for graphviz.
%endif

%if %{JAVA}
%package java
Summary:		Java extension for graphviz
Requires:		%{name} = %{version}-%{release}

%description java
Java extension for graphviz.
%endif

%package lua
Summary:		Lua extension for graphviz
Requires:		%{name} = %{version}-%{release}, lua

%description lua
Lua extension for graphviz.

%if %{MING}
%package ming
Summary:		Graphviz plugin for flash renderer based on ming
Requires:		%{name} = %{version}-%{release}

%description ming
Graphviz plugin for -Tswf (flash) renderer based on ming.
%endif

%if %{OCAML}
%package ocaml
Summary:		Ocaml extension for graphviz
Requires:		%{name} = %{version}-%{release}

%description ocaml
Ocaml extension for graphviz.
%endif

%package perl
Summary:		Perl extension for graphviz
Requires:		%{name} = %{version}-%{release}

%description perl
Perl extension for graphviz.

%if %{PHP}
%package php
Summary:		PHP extension for graphviz
Requires:		%{name} = %{version}-%{release}
Requires:	php(zend-abi) = %{?php_zend_api}%{?!php_zend_api:UNDEFINED}
Requires:	php(api) = %{?php_core_api}%{?!php_core_api:UNDEFINED}

%description php
PHP extension for graphviz.
%endif

%if %{with python2}
%package python2
Summary:		Python extension for graphviz
Requires:		%{name} = %{version}-%{release}
# Manually add provides that would be generated automatically if .egg-info was present
Provides: python2dist(gv) = %{version}
Provides: python%{python2_version}dist(gv) = %{version}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < 2.40.1-25
Obsoletes: python2-%{name} < 2.40.1-25

%description python2
Python extension for graphviz.
%endif

%package python3
Summary:		Python 3 extension for graphviz
Requires:		%{name} = %{version}-%{release}
# Manually add provides that would be generated automatically if .egg-info was present
Provides: python3dist(gv) = %{version}
Provides: python%{python3_version}dist(gv) = %{version}

%description python3
Python 3 extension for graphviz.

%if %{ARRRR}
%package R
Summary:		R extension for graphviz
Requires:		%{name} = %{version}-%{release}, R-core

%description R
R extension for graphviz.
%endif

%package ruby
Summary:		Ruby extension for graphviz
Requires:		%{name} = %{version}-%{release}, ruby

%description ruby
Ruby extension for graphviz.

%if %{SHARP}
%package sharp
Summary:		C# extension for graphviz
Requires:		%{name} = %{version}-%{release}, mono-core

%description sharp
C# extension for graphviz.
%endif

%package tcl
Summary:		Tcl extension & tools for graphviz
Requires:		%{name} = %{version}-%{release}, tcl >= 8.3, tk

%description tcl
Various tcl packages (extensions) for the graphviz tools.

%if %{GOLANG}
%package go
Summary:		Go extension for graphviz
Requires:		%{name} = %{version}-%{release}, golang

%description go
Go extension for graphviz.
%endif

%prep
%autosetup -p1

# Attempt to fix rpmlint warnings about executable sources
find -type f -regex '.*\.\(c\|h\)$' -exec chmod a-x {} ';'

%build
autoreconf -fi

%if %{JAVA}
# Hack in the java includes we need
sed -i 's|for try_java_include in|& %{java_home}/include/ %{java_home}/include/linux/|' configure
%endif
# Rewrite config_ruby.rb to work with Ruby 2.2
sed -i 's|expand(|expand(RbConfig::|' config/config_ruby.rb
sed -i 's|sitearchdir|vendorarchdir|' config/config_ruby.rb

# get the path to search for ruby/config.h to CPPFLAGS, so that configure can find it
export CPPFLAGS=-I`ruby -e "puts File.join(RbConfig::CONFIG['includedir'], RbConfig::CONFIG['sitearch'])" || echo /dev/null`
%configure --with-x --disable-static --disable-dependency-tracking \
%if ! %{JAVA}
--enable-java=no \
%endif
	--without-mylibgd --with-ipsepcola --with-pangocairo \
	--with-gdk-pixbuf --with-visio --disable-silent-rules --enable-lefty \
%if ! %{LASI}
	--without-lasi \
%endif
%if %{without gtk2}
	--without-gtk \
	--without-gtkgl \
	--without-gtkglext \
	--without-glade \
%endif
%if ! %{GTS}
	--without-gts \
%endif
%if ! %{SMYRNA}
	--without-smyrna \
%endif
%if ! %{SHARP}
	--disable-sharp \
%endif
%if ! %{OCAML}
	--disable-ocaml \
%endif
%if ! %{MING}
	--without-ming \
%endif
%if ! %{ARRRR}
	--disable-r \
%endif
%if ! %{DEVIL}
	--without-devil \
%endif
%if ! %{QTAPPS}
	--without-qt \
%endif
%if %{GUILE}
	--enable-guile=yes \
%else
	--enable-guile=no \
%endif
%if %{GOLANG}
	--enable-go=yes
%else
	--enable-go=no
%endif

# drop rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fno-strict-overflow %{?FFSTORE}" \
  CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fno-strict-overflow %{?FFSTORE}"

%if %{without bootstrap}
make doxygen
%endif

%install
%make_install docdir=%{_docdir}/%{name} \
	pkgconfigdir=%{_libdir}/pkgconfig
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# Install README
install -m0644 README %{buildroot}%{_docdir}/%{name}

%if %{PHP}
# PHP configuration file
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} << __EOF__ > %{buildroot}%{_sysconfdir}/php.d/%{ini_name}
; Enable %{name} extension module
extension=gv.so
__EOF__
%endif

# Remove executable modes from demos
find %{buildroot}%{_datadir}/%{name}/demo -type f -exec chmod a-x {} ';'

# Move demos to doc
mv %{buildroot}%{_datadir}/%{name}/demo %{buildroot}%{_docdir}/%{name}/

# Rename python demos to prevent byte compilation
find %{buildroot}%{_docdir}/%{name}/demo -type f -name "*.py" -exec mv {} {}.demo ';'

# Remove dot_builtins, on demand loading should be sufficient
rm -f %{buildroot}%{_bindir}/dot_builtins

# Remove metadata from generated PDFs
pushd %{buildroot}%{_docdir}/%{name}
for f in prune gvgen.1 gc.1 dot.1 cluster.1
do
  if [ -f $f.pdf ]
  then
# ugly, but there is probably no better solution
    qpdf --empty --static-id --pages $f.pdf -- $f.pdf.$$
    mv -f $f.pdf.$$ $f.pdf
  fi
done
popd

%if %{with python2}
install -pD tclpkg/gv/.libs/libgv_python2.so %{buildroot}%{python2_sitearch}/_gv.so
install -p tclpkg/gv/gv.py %{buildroot}%{python2_sitearch}/gv.py
%endif

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

# Explicitly create examples directory to always have it.
# At the moment there are only examples dependant on smyrna. I.e. if smyrna is not
# built this directory is empty.
mkdir -p %{buildroot}%{_datadir}/%{name}/examples

%check
%if %{PHP}
# Minimal load test of php extension
LD_LIBRARY_PATH=%{buildroot}%{_libdir} \
php --no-php-ini \
    --define extension_dir=%{buildroot}%{_libdir}/graphviz/php/ \
    --define extension=libgv_php.so \
    --modules | grep gv
%endif

# upstream test suite
# testsuite seems broken, disabling it for now
# cd rtest
# make rtest

%transfiletriggerin -- %{_libdir}/graphviz
%{_bindir}/dot -c 2>/dev/null || :

%transfiletriggerpostun -- %{_libdir}/graphviz
%{_bindir}/dot -c 2>/dev/null || :

%files
%doc %{_docdir}/%{name}
%if %{SMYRNA}
%exclude %{_bindir}/smyrna
%exclude %{_mandir}/man1/smyrna.1*
%endif
%{_bindir}/*
%dir %{_libdir}/graphviz
%{_libdir}/*.so.*
%{_libdir}/graphviz/*.so.*
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*
%dir %{_datadir}/%{name}
%exclude %{_docdir}/%{name}/*.html
%exclude %{_docdir}/%{name}/*.pdf
%exclude %{_docdir}/%{name}/demo
%{_datadir}/%{name}/gvpr
%{_datadir}/%{name}/examples
%ghost %{_libdir}/%{name}/config%{pluginsver}

%if %{QTAPPS}
%{_datadir}/%{name}/gvedit
%endif

%exclude %{_libdir}/graphviz/*/*
%exclude %{_libdir}/graphviz/libgvplugin_gd.*
%if %{with gtk2}
%exclude %{_libdir}/graphviz/libgvplugin_gtk.*
%exclude %{_libdir}/graphviz/libgvplugin_gdk.*
%endif
%if %{DEVIL}
%exclude %{_libdir}/graphviz/libgvplugin_devil.*
%endif
%if %{MING}
%exclude %{_libdir}/graphviz/libgvplugin_ming.*
%exclude %{_libdir}/graphviz/*fdb
%endif

%files devel
%{_includedir}/graphviz
%{_libdir}/*.so
%{_libdir}/graphviz/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3.*

%if %{DEVIL}
%files devil
%{_libdir}/graphviz/libgvplugin_devil.so.*
%endif

%files doc
%doc %{_docdir}/%{name}/*.html
%doc %{_docdir}/%{name}/*.pdf
%doc %{_docdir}/%{name}/demo

%if %{SMYRNA}
%files smyrna
%{_bindir}/smyrna
%{_datadir}/%{name}/smyrna
%{_mandir}/man1/smyrna.1*
%endif

%files gd
%{_libdir}/graphviz/libgvplugin_gd.so.*

%if %{with gtk2}
%files gtk2
%{_libdir}/graphviz/libgvplugin_gtk.so.*
%{_libdir}/graphviz/libgvplugin_gdk.so.*
%endif

%files graphs
%dir %{_datadir}/graphviz
%{_datadir}/graphviz/graphs

%if %{GUILE}
%files guile
%{_libdir}/graphviz/guile/
%{_mandir}/man3/gv.3guile*
%endif

%if %{JAVA}
%files java
%{_libdir}/graphviz/java/
%{_mandir}/man3/gv.3java*
%endif

%files lua
%{_libdir}/graphviz/lua/
%{_libdir}/lua*/*
%{_mandir}/man3/gv.3lua*

%if %{MING}
%files ming
%{_libdir}/graphviz/libgvplugin_ming.so.*
%{_libdir}/graphviz/*fdb
%endif

%if %{OCAML}
%files ocaml
%{_libdir}/graphviz/ocaml/
%{_mandir}/man3/gv.3ocaml*
%endif

%files perl
%{_libdir}/graphviz/perl/
%{_libdir}/perl*/*
%{_mandir}/man3/gv.3perl*

%if %{PHP}
%files php
%config(noreplace) %{_sysconfdir}/php.d/%{ini_name}
%{_libdir}/graphviz/php/
%{php_extdir}/gv.so
%{_datadir}/php*/*
%{_mandir}/man3/gv.3php*
%endif

%if %{with python2}
%files python2
%{python2_sitearch}/*
%{_mandir}/man3/gv.3python*
%endif

%files python3
%{python3_sitearch}/*
%{_mandir}/man3/gv.3python*

%if %{ARRRR}
%files R
%{_libdir}/graphviz/R/
%{_mandir}/man3/gv.3r.*
%endif

%files ruby
%{_libdir}/graphviz/ruby/
%{_libdir}/*ruby*/*
%{_mandir}/man3/gv.3ruby*

%if %{SHARP}
%files sharp
%{_libdir}/graphviz/sharp/
%{_mandir}/man3/gv.3sharp*
%endif

%files tcl
%{_libdir}/graphviz/tcl/
%{_libdir}/tcl*/*
# hack to include gv.3tcl only if available
#  always includes tcldot.3tcl, gdtclft.3tcl
%{_mandir}/man3/*.3tcl*

%if %{GOLANG}
%files go
%{_libdir}/graphviz/go/
%{_mandir}/man3/gv.3go.*
%endif

%changelog
* Thu Jan 25 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 9.0.0-10
- Added hpnd-uc license

* Wed Jan 24 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 9.0.0-9
- Converted license to SPDX

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 9.0.0-7
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Wed Dec 27 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 9.0.0-6
- Use transaction file triggers to configure plugins 

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 9.0.0-5
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 9.0.0-4
- OCaml 5.1.1 rebuild for Fedora 40

* Tue Oct 31 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 9.0.0-3
- Fixed %%java_home detection, patch by Yaakov Selkowitz

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 9.0.0-2
- OCaml 5.1 rebuild for Fedora 40

* Mon Sep 25 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 9.0.0-1
- New version
  Resolves: rhbz#2238427

* Tue Aug 22 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 8.1.0-6
- Dropped unused xserver fonts dependency

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Jitka Plesnikova <jplesnik@redhat.com> - 8.1.0-4
- Perl 5.38 re-rebuild updated packages

* Wed Jul 12 2023 Richard W.M. Jones <rjones@redhat.com> - 8.1.0-3
- OCaml 5.0 rebuild for Fedora 39

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 8.1.0-2
- Perl 5.38 rebuild

* Tue Jul 11 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 8.1.0-1
- New version
  Resolves: rhbz#2221142

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 8.0.5-3
- OCaml 5.0.0 rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 8.0.5-2
- Rebuilt for Python 3.12

* Tue May  2 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 8.0.5-1
- New version
  Resolves: rhbz#2192232

* Wed Apr 26 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 8.0.4-1
- New version
  Related: rhbz#2187116

* Wed Apr 26 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 8.0.3-1
- New version
  Resolves: rhbz#2187116

* Fri Apr 21 2023 Iñaki Úcar <iucar@fedoraproject.org> - 8.0.2-2
- R-maint-sig mass rebuild

* Tue Apr 11 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 8.0.2-1
- New version
  Resolves: rhbz#2185659

* Tue Mar 28 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 8.0.1-1
- New version
  Resolves: rhbz#2182174

* Tue Jan 24 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 7.1.0-2
- Release bump to handle gs update

* Tue Jan 24 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 7.1.0-1
- New version
  Resolves: rhbz#2162906

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 7.0.6-4
- Rebuild OCaml packages for F38

* Mon Jan 23 2023 Zdenek Dohnal <zdohnal@redhat.com> - 7.0.6-3
- add %%bcond_with bootstrap to break circular dependency with doxygen if needed

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 7.0.6-1
- New version
  Resovles: rhbz#2158703

* Fri Jan 06 2023 Tomas Popela <tpopela@redhat.com> - 7.0.5-3
- Don't build GTK 2 bits on ELN/RHEL 10 as GTK 2 won't be available there

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 7.0.5-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Thu Dec 29 2022 Tom Callaway <spot@fedoraproject.org> - 7.0.5-1
- update to 7.0.5
- patch out distutils usage to build with Python 3.12

* Thu Dec 15 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 7.0.4-1
- New version
  Resolves: rhbz#2150535

* Thu Dec  1 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 7.0.3-1
- New version
  Resolves: rhbz#2148597

* Mon Nov 21 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 7.0.2-1
- New version
  Resolves: rhbz#2144128

* Mon Nov 14 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 7.0.1-1
- New version
  Resolves: rhbz#2141409

* Tue Nov  1 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 7.0.0-2
- Temporally drop PHP support due to graphviz issue #2277
  Resolves: rhbz#2137832

* Mon Oct 24 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 7.0.0-1
- New version
  Resolves: rhbz#2137071

* Fri Oct 14 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 6.0.2-3
- More fixes for conditional build of smyrna

* Fri Oct 14 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 6.0.2-2
- Made smyrna dependant on GTS

* Thu Oct 13 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 6.0.2-1
- New version
  Resolves: rhbz#2133932

* Wed Oct 05 2022 Remi Collet <remi@remirepo.net> - 6.0.1-2
- rebuild for https://fedoraproject.org/wiki/Changes/php82

* Thu Sep 22 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 6.0.1-1
- New version
  Resolves: rhbz#2125817

* Tue Aug 23 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 5.0.1-1
- New version
  Resolves: rhbz#2119990

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 5.0.0-3
- Only build go subpackage on %%golang_arches (i.e. the architectures where
  golang is available).

* Fri Jul 15 2022 Jiri Vanek <jvanek@redhat.com> - 5.0.0-2
- adapted to removal of java on i686
- finsihing merged https://src.fedoraproject.org/rpms/graphviz/pull-request/9#request_diff
- ifed out on i686 recomanded rm -v...
- set --enable-java=no for non java arches
- added changelog entry, bumped release
- https://bugzilla.redhat.com/show_bug.cgi?id=2104225

* Tue Jul 12 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 5.0.0-1
- New version
  Resolves: rhbz#2105006

* Sun Jul 10 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 4.0.0-9
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Mon Jun 20 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.0.0-8
- Rebuilt for ocaml
  Resolves: rhbz#2098719

* Sun Jun 19 2022 Python Maint <python-maint@redhat.com> - 4.0.0-7
- Rebuilt for Python 3.11

* Sun Jun 19 2022 Robert-André Mauchin <zebob.m@gmail.com> - 4.0.0-6
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 4.0.0-5
- OCaml 4.14.0 rebuild

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 4.0.0-4
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.0.0-3
- Rebuilt for Python 3.11

* Thu Jun  9 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.0.0-2
- Used lm fix patch from upstream

* Mon Jun  6 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.0.0-1
- New version
  Resolves: rhbz#2091383

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.0-2
- Perl 5.36 rebuild

* Wed Mar  2 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.0-1
- New version
  Resolves: rhbz#2058892

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.50.0-6
- Rebuilt for java-17-openjdk as system jdk

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.50.0-5
- OCaml 4.13.1 rebuild to remove package notes

* Wed Jan 26 2022 Vít Ondruch <vondruch@redhat.com> - 2.50.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.50.0-2
- GTK2 stuff Split to the gtk2 subpackage
  Resolves: rhbz#2032671

* Mon Dec  6 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.50.0-1
- New version
  Resolves: rhbz#2029089

* Tue Nov 23 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.49.3-3
- Fixed gvpack to run
  Resolves: rhbz#1838679

* Thu Oct 28 2021 Remi Collet <remi@remirepo.net> - 2.49.3-2
- rebuild for https://fedoraproject.org/wiki/Changes/php81

* Mon Oct 25 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.49.3-1
- New version
  Resolves: rhbz#2016728

* Mon Oct 18 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.49.2-1
- New version
  Resolves: rhbz#2014784

* Wed Oct 06 2021 Richard W.M. Jones <rjones@redhat.com> - 2.49.1-2
- Rebuild for OCaml 4.13.1

* Tue Oct  5 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.49.1-1
- New version
  Resolves: rhbz#2007059

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 2.49.0-3
- OCaml 4.13.1 build

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.49.0-2
- Rebuilt with OpenSSL 3.0.0

* Mon Sep  6 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.49.0-1
- New version
  Resolves: rhbz#1998765

* Fri Jul 23 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 2.48.0-3
- Dropped unused runtime dependency from guile 2.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.48.0-1
- New version
  Resolves: rhbz#1983328

* Tue Jun 22 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.3-1
- New version
  Resolves: rhbz#1973976

* Tue Jun  8 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.2-3
- Fixed possible races during docs build which could lead to empty pdf files

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.47.2-2
- Rebuilt for Python 3.10

* Thu May 27 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.2-1
- New version
  Resolves: rhbz#1965146

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.47.1-5
- Perl 5.34 rebuild

* Wed May 12 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.1-4
- Dropped unneeded tmsize10.clo file

* Fri May  7 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.1-3
- Added build requirement for gcc-g++

* Fri May  7 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.1-2
- Conditionalized guile support
- Updated RHEL macros

* Mon Apr 19 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.1-1
- New version
  Resolves: rhbz#1950691

* Tue Mar 23 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.0-2
- Re-enabled PHP support
  Resolves: rhbz#1934996

* Tue Mar 16 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.47.0-1
- New version
  Resolves: rhbz#1939299

* Mon Mar  8 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.46.1-3
- Temporary disabled PHP support
  Resolves: rhbz#1935859

* Thu Mar  4 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.46.1-2
- Built against guile22

* Wed Mar  3 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.46.1-1
- New version
  Related: rhbz#1933722

* Tue Mar  2 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.46.0-1
- New version
  Resolves: rhbz#1933722

* Mon Mar  1 13:11:59 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.44.0-18
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.44.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.44.0-16
- F-34: rebuild against ruby 3.0

* Wed Nov 25 2020 Miro Hrončok <mhroncok@redhat.com> - 2.44.0-15
- Disable Python 2 in ELN

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 2.44.0-14
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.44.0-13
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.44.0-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.44.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.44.0-10
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.44.0-9
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.44.0-8
- Rebuilt for Python 3.9

* Wed May 20 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.44.0-7
- Also fixed man page typo

* Wed May 20 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.44.0-6
- Fixed man pages according to man page scan

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 2.44.0-5
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.44.0-4
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 2.44.0-3
- OCaml 4.11.0 pre-release

* Wed Apr  8 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.44.0-2
- Fixed multiple packaging of manual pages

* Wed Apr  8 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.44.0-1
- New version
  Resolves: rhbz#1822101

* Mon Apr  6 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.42.4-1
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

* Thu Oct 31 2019 Miro Hrončok <mhroncok@redhat.com> - 2.42.2-3
- Remove Python 2 package on Fedora 32+

* Fri Oct 04 2019 Remi Collet <remi@remirepo.net> - 2.42.2-2
- rebuild for https://fedoraproject.org/wiki/Changes/php74

* Wed Oct  2 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.42.2-1
- New version
  Resolves: rhbz#1753061
- Dropped visio, python3, CVE-2018-10196, CVE-2019-11023, and
  swig4-updated-language-options patches (all upstreamed)
- Simplified python bindings build process

* Wed Oct 02 2019 Orion Poplawski <orion@nwra.com> - 2.40.1-58
- Rebuild for lasi 1.1.3 soname bump

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.40.1-57
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

* Mon Jun  3 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-50
- Fixed FTBFS with python-3.8

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.40.1-49
- Perl 5.30 rebuild

* Tue May  7 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-48
- Fixed FTBFS caused by swig-4.0.0
  Resolves: rhbz#1707435

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-47
- OCaml 4.08.0 (beta 3) rebuild.

* Wed Apr 24 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-46
- Updated CVE-2019-11023 patch
  Related: CVE-2019-11023

* Wed Apr 24 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-45
- Fixed null pointer dereference in function agroot()
  Resolves: CVE-2019-11023

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Vít Ondruch <vondruch@redhat.com> - 2.40.1-43
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.40.1-42
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Dec  7 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-41
- Fixed some issues found by coverity scan

* Thu Oct 18 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-40
- Clarified license tag

* Mon Oct 15 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-39
- Dropped rpath

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 2.40.1-38
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Wed Sep 26 2018 Kevin Fenzi <kevin@scrye.com> - 2.40.1-37
- Don't fail on post scriptlet failures.

* Wed Jul 18 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-36
- Fixed ghostscript requirements

* Wed Jul 18 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-35
- Conditionalized php support

* Tue Jul 17 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-34
- Fixed menu in dotty
  Resolves: rhbz#1505230

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-32
- Updated source URL

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-31
- OCaml 4.07.0 (final) rebuild.

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2.40.1-30
- Perl 5.28 rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.40.1-29
- Perl 5.28 rebuild

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-28
- OCaml 4.07.0-rc1 rebuild.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.40.1-27
- Rebuilt for Python 3.7

* Thu May 17 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-26
- Fixed CVE-2018-10196

* Thu May  3 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-25
- Made python2 package optional

* Wed May  2 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-24
- Added support for python3

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-23
- OCaml 4.07.0-beta2 rebuild.

* Sat Apr 14 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.1-22
- Rename python2 subpackage to graphviz-python2, because
  there is intent to package python-graphviz, which is a separate project
  from graphviz.

* Thu Mar  8 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-21
- Dropped libgnomeui-devel requirement, libgnomeui support has been
  dropped long time ago in upstream

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-19
- Rebuilt with urw-base35-fonts

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.40.1-18
- Rebuilt for switch to libxcrypt

* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.40.1-17
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Jan 15 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-16
- Switched to libgs-devel
  Resolves: rhbz#1534666
- Made the build verbose (without silent rules)

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.40.1-15
- F-28: rebuild for ruby25

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 2.40.1-14
- OCaml 4.06.0 rebuild.

* Wed Oct 04 2017 Remi Collet <remi@fedoraproject.org> - 2.40.1-13
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.1-12
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.1-11
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

* Mon Jan 16 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-3
- Re-enabled PHP support

* Thu Jan 12 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.40.1-2
- F-26: rebuild for ruby24

* Mon Jan  2 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.40.1-1
- New version
  Resolves: rhbz#1406954
- Dropped rtest-fix, find-fix, ocaml-fix-ints, format-string,
  vimdot-vi, rbconfig, gs-9.18-fix patches (all upstreamed)
- Defuzzified visio patch

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-40
- Rebuild for OCaml 4.04.0.

* Fri Oct 14 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-39
- Fixed build with ghostscript-9.18+
  Resolves: rhbz#1384016

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-38
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-37
- Conditionalized php support and disabled it due to rhbz#1356985

* Fri Jul 15 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-36
- Rebuilt for php

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.38.0-35
- Perl 5.24 rebuild

* Fri Feb 26 2016 Than Ngo <than@redhat.com> - 2.38.0-34
- rebuilt

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 2.38.0-32
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

* Mon Jun 15 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-26
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

* Fri Jan 16 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-18
- Make vimdot to work with vi, dropped explicit vim-ehnanced requirement
  Resolves: rhbz#1182764

* Tue Nov 25 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-17
- Fixed format string vulnerability
  Resolves: rhbz#1167868

* Tue Nov 11 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-16
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

* Mon Jul 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-9
- Rebuilt for new ocaml

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 2.38.0-8
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file
- cleanup filter (no more needed in F20+)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.38.0-6
- Re-enable R bindings on aarch64, we now have it

* Wed May 28 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-5
- Fixed crash by adding additional check to findVertical/Horizontal functions
  (by find-fix patch provided by Mattias Ellert <mattias.ellert@fysast.uu.se>)
  Resolves: rhbz#1095419

* Tue May 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-4
- Rebuilt for tcl/tk8.6

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.38.0-2
- Remove ocaml_arches macro (RHBZ#1087794).

* Mon Apr 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.38.0-1
- New version
  Resolves: rhbz#1052160
- Dropped testsuite-sigsegv-fix, rtest-errout-fix, lefty-getaddrinfo,
  CVE-2014-0978-CVE-2014-1235, CVE-2014-1236, ppc64le-support
  patches (all upstreamed)
- Added rtest-fix patch (sent upstream)
- Disabled test suite (for now)

* Wed Mar 19 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.34.0-9
- Added ppc64le support
  Resolves: rhbz#1078464

* Thu Jan  9 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.34.0-8
- Prevent possible buffer overflow in yyerror()
  Resolves: CVE-2014-1235
- Fix possible buffer overflow problem in chkNum of scanner
  Resolves: CVE-2014-1236

* Tue Jan  7 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.34.0-7
- Fixed overflow in yyerror
  Resolves: CVE-2014-0978

* Sat Dec 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.34.0-6
- Disable R bindings on aarch64 for the moment

* Thu Dec 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.34.0-5
- No mono on aarch64

* Thu Oct 31 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.34.0-4
- Removed metadata from generated PDFs
  Related: rhbz#881173

* Thu Oct 31 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.34.0-3
- Fixed multilib conflicts
  Rewrote lefty IO lib to use getaddrinfo instead of gethostbyname
  (by lefty-getaddrinfo patch)
  Resolves: rhbz#881173

* Mon Sep 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.34.0-2
- Added explicit dependency on vim (required by vimdot)

* Mon Sep 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.34.0-1
- New version
  Resolves: rhbz#1005957
- Dropped perl-fix patch (upstreamed)

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 2.32.0-2
- Rebuild for OCaml 4.01.0.

* Mon Aug 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.32.0-1
- New version
  Resolves: rhbz#991752
- Dropped guile2-fix, cgraph, lua-52, smyrna-doc-opt, gv2gml-options-fix,
  lefty-help, prune-help, man-fix patches (all upstreamed)

* Tue Aug  6 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.1-14
- Used unversioned doc directory
  Resolves: rhbz#993803

* Mon Aug  5 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.1-13
- Fixed FTBFS related to perl config
  Resolves: rhbz#991915

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.30.1-11
- Perl 5.18 rebuild

* Fri Jul 12 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.1-10
- Various man and built-in help fixes

* Tue Jun 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.1-9
- Fixed handling of the libdir/graphviz directory

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.30.1-8
- rebuild for new GD 2.1.0

* Wed May 15 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-7
- rebuild for lua 5.2

* Tue Apr 23 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-6
- patch libgvc.pc.in to refer to -lcgraph (-lgraph is dead and gone)

* Thu Apr 11 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-5
- rebuild for R3 (may not be needed, but better safe than sorry)

* Mon Mar 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.1-4
- Added support for aarch64
  Resolves: rhbz#925487

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 2.30.1-3
- rebuild for http://fedoraproject.org/wiki/Features/Php55
- add explicit BuildRequires: perl-Carp (workaround)

* Thu Mar 14 2013 Vít Ondruch <vondruch@redhat.com> - 2.30.1-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Feb 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.1-1
- New version
  Resolves: rhbz#911520
  Resolves: rhbz#704529

* Thu Jan 24 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.0-3
- Used ocaml_arches macros to enable ocaml on supported arches

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.30.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Mon Jan 14 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.30.0-1
- New version
  Resolves: rhbz#895027
- Dropped guile-detect, ocaml4 patches (not needed)
- Fixed bogus date in changelog (guessing)

* Wed Jan  9 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-26
- Rebuilt with -fno-strict-overflow to workaround the overflow problem
  (upstream ticket: http://www.graphviz.org/mantisbt/view.php?id=2244)
- The dot_builtins was removed rather then excluded to fix the dangling
  symlinks problem in debuginfo

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.28.0-25
- rebuild against new libjpeg

* Wed Oct 17 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-24
- Rebuilt for new ocaml

* Fri Aug 17 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-23
- Silenced 'dot -c' errors/warnings in post/postun
- Do not remove dot config in plugins post/postun

* Fri Aug 17 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-22
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

* Wed May 23 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-18
- Improved docs handling code in spec to be backward compatible with older RPM

* Tue May 22 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-17
- All docs are now installed into /usr/share/doc/graphviz-%%{version}
- Demos packaged as docs not to automatically bring in unnecessary deps

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-16
- Rebuilt for c++ ABI breakage

* Thu Feb 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.28.0-15
- fix CPPFLAGS export so it doesn't cause issues on ARM

* Mon Feb 06 2012 Vít Ondruch <vondruch@redhat.com> - 2.28.0-14
- Rebuilt for Ruby 1.9.3.

* Wed Jan 18 2012 Remi Collet <remi@fedoraproject.org> - 2.28.0-13
- build against php 5.4.0
- add filter to fix private-shared-object-provides
- add %%check for php extension

* Sun Jan 08 2012 Richard W.M. Jones <rjones@redhat.com> - 2.28.0-12
- Rebuild for OCaml 3.12.1.

* Thu Dec  8 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-11
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

* Thu Jul 07 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-7
- Added gd as devel requirement

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.28.0-6
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.28.0-5
- Perl 5.14 mass rebuild

* Thu May 19 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-4
- Fixed detection of guile 2.x
  Resolves: rhbz#704529

* Fri May 13 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-3
- Corrected license tag, the graphviz license is now EPL

* Fri May 13 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-2
- Recompiled with -fno-strict-aliasing in CXXFLAGS

* Tue May 10 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28.0-1
- New version 2.28.0
- Added perl-ExtUtils-Embed to BuildRequires, it is now required
- Fixed build failure due to change in php_zend_api macro type
- Removed sparc64, gtk-progname, doc-index-fix, ppc-darwinhack
  patches (all were upstreamed)

* Thu Mar 03 2011 Oliver Falk <oliver@linux-kernel.at> - 2.26.3-5
- Disable mono and ocaml on alpha

* Tue Feb 22 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.26.3-4
- Added urw-fonts to requires (#677114)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Karsten Hopp <karsten@redhat.com> 2.26.3-2
- fix hack for powerpc-darwin8 in configure

* Thu Jan 06 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.26.3-1
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