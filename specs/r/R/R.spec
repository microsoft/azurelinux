# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# We need +x on these files
%global __brp_mangle_shebangs_exclude_from %{_libdir}/R/bin/

# The additional linker flags break binary R- packages
# https://bugzilla.redhat.com/show_bug.cgi?id=2046246
%undefine _package_note_flags

# EPEL-only issues in some architectures (gcc < 12?)
%if 0%{?rhel} && "%{_arch}" != "x86_64"
%bcond_with tests
%else
%bcond_without tests
%endif

# We need at least gcc 10
%if 0%{?rhel} && 0%{?rhel} < 9
%global _lto_cflags %nil
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%global blasvar %{nil}
%else
%global blaslib openblas
%global blasvar o
%endif

# Should be the previous version, to make mass-rebuilds easier
%bcond_with bootstrap
%global bootstrap_abi 4.4

%global major_version 4
%global minor_version 5
%global patch_version 2

Name:           R
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release: 4%{?dist}
Summary:        A language for data analysis and graphics

License:        GPL-2.0-or-later
URL:            https://www.r-project.org
Source0:        https://cran.r-project.org/src/base/R-4/R-%{version}.tar.gz
# see https://bugzilla.redhat.com/show_bug.cgi?id=1324145
Patch0:         R-3.3.0-fix-java_path-in-javareconf.patch

BuildRequires:  gcc-gfortran
BuildRequires:  gcc-c++
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  readline-devel
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel
BuildRequires:  libcurl-devel
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  libdeflate-devel
BuildRequires:  libzstd-devel
BuildRequires:  tre-devel
BuildRequires:  %{blaslib}-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libICE-devel
BuildRequires:  libXt-devel
BuildRequires:  libXmu-devel
BuildRequires:  libicu-devel
BuildRequires:  libtirpc-devel
%ifarch %{valgrind_arches}
BuildRequires:  valgrind-devel
%endif
%ifarch %{java_arches}
BuildRequires:  java-devel
%endif
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  less
BuildRequires:  tex(latex)
BuildRequires:  texinfo-tex
BuildRequires:  tex(upquote.sty)
%if 0%{?fedora}
# No inconsolata on RHEL tex
BuildRequires:  tex(inconsolata.sty)
%endif

# R-devel will pull everything else
Requires:       R-devel%{?_isa} = %{version}-%{release}

%description
This is a metapackage that provides both core R userspace and
all R development components.

R is a language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package core
Summary:        The minimal R components necessary for a functional runtime
Requires:       libRmath%{?_isa} = %{version}-%{release}
Requires:       tzdata
Requires:       less
Requires:       xdg-utils
Requires:       zip, unzip

%ifnarch %{java_arches}
Provides:       R-java = %{version}-%{release}
Obsoletes:      R-java < 4.1.3-3
%endif

# This is our ABI provides to prevent mismatched installs.
# R packages should autogenerate a Requires: R(ABI) based on the R they were built against.
Provides:       R(ABI) = %{major_version}.%{minor_version}
%if %{with bootstrap}
Provides:       R(ABI) = %{bootstrap_abi}
%endif

# These are the submodules that R-core provides. Sometimes R modules say they
# depend on one of these submodules rather than just R. These are provided for
# packager convenience.
%define add_submodule() %{lua:
  local name = rpm.expand("%1")
  local version = rpm.expand("%2")
  local rpm_version = string.gsub(version, "-", ".")
  print("Provides: R-" .. name .. " = " .. rpm_version .. "\\n")
  print("Provides: R(" .. name .. ") = " .. rpm_version)
}
%add_submodule  base %{version}
%add_submodule  boot 1.3-32
%add_submodule  class 7.3-23
%add_submodule  cluster 2.1.8.1
%add_submodule  codetools 0.2-20
%add_submodule  compiler %{version}
%add_submodule  datasets %{version}
%add_submodule  foreign 0.8-90
%add_submodule  graphics %{version}
%add_submodule  grDevices %{version}
%add_submodule  grid %{version}
%add_submodule  KernSmooth 2.23-26
%add_submodule  lattice 0.22-7
%add_submodule  MASS 7.3-65
%add_submodule  Matrix 1.7-4
Obsoletes:      R-Matrix < 0.999375-7
%add_submodule  methods %{version}
%add_submodule  mgcv 1.9-3
%add_submodule  nlme 3.1-168
%add_submodule  nnet 7.3-20
%add_submodule  parallel %{version}
%add_submodule  rpart 4.1.24
%add_submodule  spatial 7.3-18
%add_submodule  splines %{version}
%add_submodule  stats %{version}
%add_submodule  stats4 %{version}
%add_submodule  survival 3.8-3
%add_submodule  tcltk %{version}
%add_submodule  tools %{version}
%add_submodule  translations %{version}
%add_submodule  utils %{version}

%description core
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package core-devel
Summary:        Core files for development of R packages (no Java)
Requires:       R-core%{?_isa} = %{version}-%{release}
Requires:       libRmath-devel%{?_isa} = %{version}-%{release}
# R inherits the compiler flags it was built with, hence we need this on hardened systems
Requires:       redhat-rpm-config
# You need all the BuildRequires for the development version
Requires:       gcc-gfortran
Requires:       gcc-c++
Requires:       make
Requires:       pkgconfig
Requires:       pcre2-devel
Requires:       bzip2-devel
Requires:       xz-devel
Requires:       zlib-devel
Requires:       libdeflate-devel
Requires:       libzstd-devel
Requires:       tre-devel
Requires:       %{blaslib}-devel
Requires:       libX11-devel
Requires:       libicu-devel
Requires:       libtirpc-devel
Recommends:     tex(latex)
Recommends:     texinfo-tex
Recommends:     tidy
Recommends:     devscripts-checkbashisms
%if 0%{?fedora}
# No inconsolata on RHEL tex
Recommends:     tex(inconsolata.sty)
# "‘qpdf’ is needed for checks on size reduction of PDFs"
# qpdf is not in epel, and since 99% of R doesn't use it, we'll let it slide.
Recommends:     qpdf
%endif

Provides:       R-Matrix-devel = 1.7.4
Obsoletes:      R-Matrix-devel < 0.999375-7

%ifarch %{java_arches}
%description core-devel
Install R-core-devel if you are going to develop or compile R packages.
This package does not configure the R environment for Java, install
R-java-devel if you want this.
%else
%description core-devel
Install R-core-devel if you are going to develop or compile R packages.
%endif

%package devel
Summary:        Full R development environment metapackage
Requires:       R-rpm-macros
Requires:       R-core-devel%{?_isa} = %{version}-%{release}
%ifarch %{java_arches}
Requires:       R-java-devel%{?_isa} = %{version}-%{release}
%else
Provides:       R-java-devel = %{version}-%{release}
Obsoletes:      R-java-devel < 4.1.3-3
%endif

%description devel
This is a metapackage to install a complete (with Java) R development
environment.

%ifarch %{java_arches}
%package java
Summary:        R with Fedora provided Java Runtime Environment
Requires(post): R-core%{?_isa} = %{version}-%{release}
Requires:       java-headless

%description java
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

This package also has an additional dependency on java, as provided by
Fedora's openJDK.

%package java-devel
Summary:        Development package for use with Java enabled R components
Requires:       R-java%{?_isa} = %{version}-%{release}
Requires(post): R-core-devel%{?_isa} = %{version}-%{release}
Requires(post): java-devel

%description java-devel
Install R-java-devel if you are going to develop or compile R packages
that assume java is present and configured on the system.
%endif

%package -n libRmath
Summary:        Standalone math library from the R project

%description -n libRmath
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the shared libRmath library.

%package -n libRmath-devel
Summary:        Headers from the R Standalone math library
Requires:       libRmath%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libRmath-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the libRmath header files.

%package -n libRmath-static
Summary:        Static R Standalone math library
Requires:       libRmath-devel%{?_isa} = %{version}-%{release}

%description -n libRmath-static
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the static libRmath library.

%prep
%setup -q
%patch -P0 -p1 -b .fixpath
# A bunch of macOS stuff in v4.5.2's archive
find . -name '._*' -delete

%build
# Comment out default R_LIBS_SITE (since R 4.2) and set our own as always
sed -i -e '/R_LIBS_SITE=/s/^/#/g' etc/Renviron.in
# Only packages which are needed as runtime dependencies are rebuilt for
# flatpaks in /app, build dependencies are from buildroot in /usr
echo 'R_LIBS_SITE=${R_LIBS_SITE-'"'/usr/local/lib/R/site-library:/usr/local/lib/R/library:%{_libdir}/R/library:%{_datadir}/R/library%{?flatpak::/usr/%{_lib}/R/library:/usr/share/R/library}'"'}' >> etc/Renviron.in
# No inconsolata on RHEL tex
%if 0%{?rhel}
export R_RD4PDF="times,hyper"
sed -i 's|inconsolata,||g' etc/Renviron.in
%endif
export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_BROWSER="%{_bindir}/xdg-open"

%ifarch %{java_arches}
export JAVA_HOME=%{_jvmdir}/jre
%endif

%configure \
  rdocdir=%{_pkgdocdir} \
  rincludedir=%{_includedir}/R \
  rsharedir=%{_datadir}/R \
  --with-system-tre \
  --with-blas=%{blaslib}%{blasvar} \
  --with-lapack \
  --with-tcl-config=/usr/%{_lib}/tclConfig.sh \
  --with-tk-config=/usr/%{_lib}/tkConfig.sh \
  --enable-R-shlib \
  --enable-prebuilt-html \
  --enable-R-profiling \
  --enable-memory-profiling \
  | tee CONFIGURE.log
cat CONFIGURE.log | grep -A30 'R is now' - > CAPABILITIES
make V=1
(cd src/nmath/standalone; make)
make pdf
make compact-pdf
make info

# Convert to UTF-8
for i in doc/manual/R-intro.info doc/manual/R-FAQ.info doc/FAQ doc/manual/R-admin.info doc/manual/R-exts.info-1; do
  iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
  mv $i{.utf8,}
done

%install
make DESTDIR=%{buildroot} install install-pdf install-info

rm -f %{buildroot}%{_infodir}/dir
mkdir -p %{buildroot}%{_pkgdocdir}
install -p CAPABILITIES %{buildroot}%{_pkgdocdir}

# Install libRmath files
(cd src/nmath/standalone; make install DESTDIR=%{buildroot})

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/R/lib" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p %{buildroot}%{_datadir}/R/library

# Fix multilib
touch -r README %{buildroot}%{_pkgdocdir}/CAPABILITIES
touch -r README doc/manual/*.pdf
touch -r README %{buildroot}%{_bindir}/R

# Fix html/packages.html
# We can safely use RHOME here, because all of these are system packages.
sed -i 's|\..\/\..|%{_libdir}/R|g' %{buildroot}%{_pkgdocdir}/html/packages.html

for i in %{buildroot}%{_libdir}/R/library/*/html/*.html; do
  sed -i 's|\..\/\..\/..\/doc|%{_pkgdocdir}|g' $i
done

# Fix exec bits
chmod +x %{buildroot}%{_datadir}/R/sh/echo.sh
chmod +x %{buildroot}%{_libdir}/R/bin/*
chmod -x %{buildroot}%{_libdir}/R/library/mgcv/CITATION %{buildroot}%{_pkgdocdir}/CAPABILITIES

# Symbolic link for convenience
if [ ! -d "%{buildroot}%{_libdir}/R/include" ]; then
	pushd %{buildroot}%{_libdir}/R
	ln -s ../../include/R include
	popd
fi

# Symbolic link for LaTeX
%{!?_texdir:  %global _texdir  %{_datadir}/texlive}
%{!?_texdist: %global _texdist %{_texdir}/texmf-dist}
for i in tex/latex bibtex/bib bibtex/bst; do
  mkdir -p %{buildroot}%{_texdist}/$i
  (cd %{buildroot}%{_texdist}/$i && ln -s %{_datadir}/R/texmf/$i R)
done

%if 0%{?flatpak}
# keep compatibility with shebang dependencies
mkdir -p %{buildroot}/usr/bin
ln -s /app/bin/Rscript %{buildroot}/usr/bin/Rscript
%endif

%check
%if %{with tests}
# Needed by tests/ok-error.R, which will smash the stack on PPC64.
# This is the purpose of the test.
ulimit -s 16384
TZ="Europe/Paris" make check
%endif

%files
# Metapackage

%files core
%{_bindir}/R
%{_bindir}/Rscript
%{_datadir}/R/
# Links to LaTeX stuff
%dir %{_texdir}
%dir %{_texdist}
%dir %{_texdist}/tex/
%dir %{_texdist}/tex/latex/
%{_texdist}/tex/latex/R
%dir %{_texdist}/bibtex/
%dir %{_texdist}/bibtex/bib/
%{_texdist}/bibtex/bib/R
%dir %{_texdist}/bibtex/bst/
%{_texdist}/bibtex/bst/R
# Have to break this out for the translations
%dir %{_libdir}/R/
%{_libdir}/R/bin/
%dir %{_libdir}/R/etc
%config %{_libdir}/R/etc/Makeconf
%config %{_libdir}/R/etc/javaconf
%config(noreplace) %{_libdir}/R/etc/Renviron
%config(noreplace) %{_libdir}/R/etc/ldpaths
%config(noreplace) %{_libdir}/R/etc/repositories
%{_libdir}/R/lib/
%dir %{_libdir}/R/library/
%dir %{_libdir}/R/library/translations/
%{_libdir}/R/library/translations/DESCRIPTION
%lang(ar) %{_libdir}/R/library/translations/ar/
%lang(bn) %{_libdir}/R/library/translations/bn/
%lang(ca) %{_libdir}/R/library/translations/ca/
%lang(da) %{_libdir}/R/library/translations/da/
%lang(de) %{_libdir}/R/library/translations/de/
%lang(en) %{_libdir}/R/library/translations/en*/
%lang(es) %{_libdir}/R/library/translations/es/
%lang(fa) %{_libdir}/R/library/translations/fa/
%lang(fr) %{_libdir}/R/library/translations/fr/
%lang(hi) %{_libdir}/R/library/translations/hi/
%lang(hu) %{_libdir}/R/library/translations/hu/
%lang(id) %{_libdir}/R/library/translations/id/
%lang(it) %{_libdir}/R/library/translations/it/
%lang(ja) %{_libdir}/R/library/translations/ja/
%lang(ko) %{_libdir}/R/library/translations/ko/
%lang(lt) %{_libdir}/R/library/translations/lt/
%lang(ne) %{_libdir}/R/library/translations/ne/
%lang(nn) %{_libdir}/R/library/translations/nn/
%lang(pl) %{_libdir}/R/library/translations/pl/
%lang(pt) %{_libdir}/R/library/translations/pt*/
%lang(ru) %{_libdir}/R/library/translations/ru/
%lang(sq) %{_libdir}/R/library/translations/sq/
%lang(tr) %{_libdir}/R/library/translations/tr/
%lang(ur) %{_libdir}/R/library/translations/ur/
%lang(zh) %{_libdir}/R/library/translations/zh*/
# base
%dir %{_libdir}/R/library/base/
%{_libdir}/R/library/base/CITATION
%{_libdir}/R/library/base/demo/
%{_libdir}/R/library/base/DESCRIPTION
%{_libdir}/R/library/base/help/
%doc %{_libdir}/R/library/base/html/
%{_libdir}/R/library/base/INDEX
%{_libdir}/R/library/base/Meta/
%{_libdir}/R/library/base/R/
# boot
%dir %{_libdir}/R/library/boot/
%{_libdir}/R/library/boot/bd.q
%{_libdir}/R/library/boot/CITATION
%{_libdir}/R/library/boot/data/
%{_libdir}/R/library/boot/DESCRIPTION
%{_libdir}/R/library/boot/help/
%doc %{_libdir}/R/library/boot/html/
%{_libdir}/R/library/boot/INDEX
%{_libdir}/R/library/boot/Meta/
%{_libdir}/R/library/boot/NAMESPACE
%dir %{_libdir}/R/library/boot/po/
%lang(de) %{_libdir}/R/library/boot/po/de/
%lang(en) %{_libdir}/R/library/boot/po/en*/
%lang(fr) %{_libdir}/R/library/boot/po/fr/
%lang(it) %{_libdir}/R/library/boot/po/it/
%lang(ko) %{_libdir}/R/library/boot/po/ko/
%lang(pl) %{_libdir}/R/library/boot/po/pl/
%lang(ru) %{_libdir}/R/library/boot/po/ru/
%{_libdir}/R/library/boot/R/
# class
%dir %{_libdir}/R/library/class/
%{_libdir}/R/library/class/CITATION
%{_libdir}/R/library/class/DESCRIPTION
%{_libdir}/R/library/class/help/
%doc %{_libdir}/R/library/class/html/
%{_libdir}/R/library/class/INDEX
%{_libdir}/R/library/class/libs/
%{_libdir}/R/library/class/Meta/
%{_libdir}/R/library/class/NAMESPACE
%doc %{_libdir}/R/library/class/NEWS
%dir %{_libdir}/R/library/class/po/
%lang(de) %{_libdir}/R/library/class/po/de/
%lang(en) %{_libdir}/R/library/class/po/en*/
%lang(fr) %{_libdir}/R/library/class/po/fr/
%lang(it) %{_libdir}/R/library/class/po/it/
%lang(ko) %{_libdir}/R/library/class/po/ko/
%lang(pl) %{_libdir}/R/library/class/po/pl/
%{_libdir}/R/library/class/R/
# cluster
%dir %{_libdir}/R/library/cluster/
%{_libdir}/R/library/cluster/CITATION
%{_libdir}/R/library/cluster/data/
%{_libdir}/R/library/cluster/DESCRIPTION
%{_libdir}/R/library/cluster/help/
%doc %{_libdir}/R/library/cluster/html/
%{_libdir}/R/library/cluster/INDEX
%{_libdir}/R/library/cluster/libs/
%{_libdir}/R/library/cluster/Meta/
%{_libdir}/R/library/cluster/NAMESPACE
%doc %{_libdir}/R/library/cluster/NEWS.Rd
%dir %{_libdir}/R/library/cluster/po/
%lang(de) %{_libdir}/R/library/cluster/po/de/
%lang(en) %{_libdir}/R/library/cluster/po/en*/
%lang(fr) %{_libdir}/R/library/cluster/po/fr/
%lang(it) %{_libdir}/R/library/cluster/po/it/
%lang(ko) %{_libdir}/R/library/cluster/po/ko/
%lang(lt) %{_libdir}/R/library/cluster/po/lt/
%lang(pl) %{_libdir}/R/library/cluster/po/pl/
%{_libdir}/R/library/cluster/R/
%{_libdir}/R/library/cluster/test-tools.R
# codetools
%dir %{_libdir}/R/library/codetools/
%{_libdir}/R/library/codetools/DESCRIPTION
%{_libdir}/R/library/codetools/help/
%doc %{_libdir}/R/library/codetools/html/
%{_libdir}/R/library/codetools/INDEX
%{_libdir}/R/library/codetools/Meta/
%{_libdir}/R/library/codetools/NAMESPACE
%{_libdir}/R/library/codetools/R/
# compiler
%dir %{_libdir}/R/library/compiler/
%{_libdir}/R/library/compiler/DESCRIPTION
%{_libdir}/R/library/compiler/help/
%doc %{_libdir}/R/library/compiler/html/
%{_libdir}/R/library/compiler/INDEX
%{_libdir}/R/library/compiler/Meta/
%{_libdir}/R/library/compiler/NAMESPACE
%{_libdir}/R/library/compiler/R/
# datasets
%dir %{_libdir}/R/library/datasets/
%{_libdir}/R/library/datasets/data/
%{_libdir}/R/library/datasets/DESCRIPTION
%{_libdir}/R/library/datasets/help/
%doc %{_libdir}/R/library/datasets/html
%{_libdir}/R/library/datasets/INDEX
%{_libdir}/R/library/datasets/Meta/
%{_libdir}/R/library/datasets/NAMESPACE
# foreign
%dir %{_libdir}/R/library/foreign/
%license %{_libdir}/R/library/foreign/COPYRIGHTS
%{_libdir}/R/library/foreign/DESCRIPTION
%{_libdir}/R/library/foreign/files/
%{_libdir}/R/library/foreign/help/
%doc %{_libdir}/R/library/foreign/html/
%{_libdir}/R/library/foreign/INDEX
%{_libdir}/R/library/foreign/libs/
%{_libdir}/R/library/foreign/Meta/
%{_libdir}/R/library/foreign/NAMESPACE
%dir %{_libdir}/R/library/foreign/po/
%lang(de) %{_libdir}/R/library/foreign/po/de/
%lang(en) %{_libdir}/R/library/foreign/po/en*/
%lang(fr) %{_libdir}/R/library/foreign/po/fr/
%lang(it) %{_libdir}/R/library/foreign/po/it/
%lang(pl) %{_libdir}/R/library/foreign/po/pl/
%{_libdir}/R/library/foreign/R/
# graphics
%dir %{_libdir}/R/library/graphics/
%{_libdir}/R/library/graphics/demo/
%{_libdir}/R/library/graphics/DESCRIPTION
%{_libdir}/R/library/graphics/help/
%doc %{_libdir}/R/library/graphics/html/
%{_libdir}/R/library/graphics/INDEX
%{_libdir}/R/library/graphics/libs/
%{_libdir}/R/library/graphics/Meta/
%{_libdir}/R/library/graphics/NAMESPACE
%{_libdir}/R/library/graphics/R/
# grDevices
%dir %{_libdir}/R/library/grDevices/
%{_libdir}/R/library/grDevices/afm/
%{_libdir}/R/library/grDevices/demo/
%{_libdir}/R/library/grDevices/DESCRIPTION
%{_libdir}/R/library/grDevices/enc/
%{_libdir}/R/library/grDevices/fonts/
%{_libdir}/R/library/grDevices/help/
%doc %{_libdir}/R/library/grDevices/html/
%{_libdir}/R/library/grDevices/icc/
%{_libdir}/R/library/grDevices/INDEX
%{_libdir}/R/library/grDevices/libs/
%{_libdir}/R/library/grDevices/Meta/
%{_libdir}/R/library/grDevices/NAMESPACE
%{_libdir}/R/library/grDevices/R/
# grid
%dir %{_libdir}/R/library/grid/
%{_libdir}/R/library/grid/DESCRIPTION
%doc %{_libdir}/R/library/grid/doc/
%{_libdir}/R/library/grid/help/
%doc %{_libdir}/R/library/grid/html/
%{_libdir}/R/library/grid/INDEX
%{_libdir}/R/library/grid/libs/
%{_libdir}/R/library/grid/Meta/
%{_libdir}/R/library/grid/NAMESPACE
%{_libdir}/R/library/grid/R/
# KernSmooth
%dir %{_libdir}/R/library/KernSmooth/
%{_libdir}/R/library/KernSmooth/DESCRIPTION
%{_libdir}/R/library/KernSmooth/help/
%doc %{_libdir}/R/library/KernSmooth/html/
%{_libdir}/R/library/KernSmooth/INDEX
%{_libdir}/R/library/KernSmooth/libs/
%{_libdir}/R/library/KernSmooth/Meta/
%{_libdir}/R/library/KernSmooth/NAMESPACE
%dir %{_libdir}/R/library/KernSmooth/po/
%lang(de) %{_libdir}/R/library/KernSmooth/po/de/
%lang(en) %{_libdir}/R/library/KernSmooth/po/en*/
%lang(fr) %{_libdir}/R/library/KernSmooth/po/fr/
%lang(it) %{_libdir}/R/library/KernSmooth/po/it/
%lang(ko) %{_libdir}/R/library/KernSmooth/po/ko/
%lang(pl) %{_libdir}/R/library/KernSmooth/po/pl/
%{_libdir}/R/library/KernSmooth/R/
# lattice
%dir %{_libdir}/R/library/lattice/
%{_libdir}/R/library/lattice/CITATION
%{_libdir}/R/library/lattice/data/
%{_libdir}/R/library/lattice/demo/
%{_libdir}/R/library/lattice/DESCRIPTION
%doc %{_libdir}/R/library/lattice/doc/
%{_libdir}/R/library/lattice/help/
%doc %{_libdir}/R/library/lattice/html/
%{_libdir}/R/library/lattice/INDEX
%{_libdir}/R/library/lattice/libs/
%{_libdir}/R/library/lattice/Meta/
%{_libdir}/R/library/lattice/NAMESPACE
%doc %{_libdir}/R/library/lattice/NEWS.md
%dir %{_libdir}/R/library/lattice/po/
%lang(de) %{_libdir}/R/library/lattice/po/de/
%lang(en) %{_libdir}/R/library/lattice/po/en*/
%lang(fr) %{_libdir}/R/library/lattice/po/fr/
%lang(it) %{_libdir}/R/library/lattice/po/it/
%lang(ko) %{_libdir}/R/library/lattice/po/ko/
%lang(pl) %{_libdir}/R/library/lattice/po/pl*/
%{_libdir}/R/library/lattice/R/
# MASS
%dir %{_libdir}/R/library/MASS/
%{_libdir}/R/library/MASS/CITATION
%{_libdir}/R/library/MASS/data/
%{_libdir}/R/library/MASS/DESCRIPTION
%{_libdir}/R/library/MASS/help/
%doc %{_libdir}/R/library/MASS/html/
%{_libdir}/R/library/MASS/INDEX
%{_libdir}/R/library/MASS/libs/
%{_libdir}/R/library/MASS/Meta/
%{_libdir}/R/library/MASS/NAMESPACE
%doc %{_libdir}/R/library/MASS/NEWS
%dir %{_libdir}/R/library/MASS/po
%lang(de) %{_libdir}/R/library/MASS/po/de/
%lang(en) %{_libdir}/R/library/MASS/po/en*/
%lang(fr) %{_libdir}/R/library/MASS/po/fr/
%lang(it) %{_libdir}/R/library/MASS/po/it/
%lang(ko) %{_libdir}/R/library/MASS/po/ko/
%lang(pl) %{_libdir}/R/library/MASS/po/pl/
%{_libdir}/R/library/MASS/R/
%{_libdir}/R/library/MASS/scripts/
# Matrix
%dir %{_libdir}/R/library/Matrix/
%{_libdir}/R/library/Matrix/data/
%{_libdir}/R/library/Matrix/DESCRIPTION
%doc %{_libdir}/R/library/Matrix/doc/
%{_libdir}/R/library/Matrix/external/
%{_libdir}/R/library/Matrix/help/
%doc %{_libdir}/R/library/Matrix/html/
%{_libdir}/R/library/Matrix/include/
%{_libdir}/R/library/Matrix/INDEX
%{_libdir}/R/library/Matrix/libs/
%license %{_libdir}/R/library/Matrix/LICENCE
%{_libdir}/R/library/Matrix/Meta/
%{_libdir}/R/library/Matrix/NAMESPACE
%doc %{_libdir}/R/library/Matrix/NEWS.Rd
%dir %{_libdir}/R/library/Matrix/po/
%lang(de) %{_libdir}/R/library/Matrix/po/de/
%lang(en) %{_libdir}/R/library/Matrix/po/en*/
%lang(fr) %{_libdir}/R/library/Matrix/po/fr/
%lang(it) %{_libdir}/R/library/Matrix/po/it/
%lang(ko) %{_libdir}/R/library/Matrix/po/ko/
%lang(lt) %{_libdir}/R/library/Matrix/po/lt/
%lang(pl) %{_libdir}/R/library/Matrix/po/pl/
%{_libdir}/R/library/Matrix/R/
%{_libdir}/R/library/Matrix/scripts/
%{_libdir}/R/library/Matrix/test-tools.R
%{_libdir}/R/library/Matrix/test-tools-1.R
%{_libdir}/R/library/Matrix/test-tools-Matrix.R
# methods
%dir %{_libdir}/R/library/methods/
%{_libdir}/R/library/methods/DESCRIPTION
%{_libdir}/R/library/methods/help/
%doc %{_libdir}/R/library/methods/html/
%{_libdir}/R/library/methods/INDEX
%{_libdir}/R/library/methods/libs/
%{_libdir}/R/library/methods/Meta/
%{_libdir}/R/library/methods/NAMESPACE
%{_libdir}/R/library/methods/R/
# mgcv
%dir %{_libdir}/R/library/mgcv/
%{_libdir}/R/library/mgcv/CITATION
%{_libdir}/R/library/mgcv/data/
%{_libdir}/R/library/mgcv/DESCRIPTION
%{_libdir}/R/library/mgcv/help/
%doc %{_libdir}/R/library/mgcv/html/
%{_libdir}/R/library/mgcv/INDEX
%{_libdir}/R/library/mgcv/libs/
%{_libdir}/R/library/mgcv/Meta/
%{_libdir}/R/library/mgcv/NAMESPACE
%dir %{_libdir}/R/library/mgcv/po/
%lang(de) %{_libdir}/R/library/mgcv/po/de/
%lang(en) %{_libdir}/R/library/mgcv/po/en*/
%lang(fr) %{_libdir}/R/library/mgcv/po/fr/
%lang(ko) %{_libdir}/R/library/mgcv/po/ko/
%lang(pl) %{_libdir}/R/library/mgcv/po/pl/
%{_libdir}/R/library/mgcv/R/
# nlme
%dir %{_libdir}/R/library/nlme/
%{_libdir}/R/library/nlme/CITATION
%{_libdir}/R/library/nlme/data/
%{_libdir}/R/library/nlme/DESCRIPTION
%{_libdir}/R/library/nlme/help/
%doc %{_libdir}/R/library/nlme/html/
%{_libdir}/R/library/nlme/INDEX
%{_libdir}/R/library/nlme/libs/
%{_libdir}/R/library/nlme/Meta/
%{_libdir}/R/library/nlme/mlbook/
%{_libdir}/R/library/nlme/NAMESPACE
%dir %{_libdir}/R/library/nlme/po/
%lang(de) %{_libdir}/R/library/nlme/po/de/
%lang(en) %{_libdir}/R/library/nlme/po/en*/
%lang(fr) %{_libdir}/R/library/nlme/po/fr/
%lang(ko) %{_libdir}/R/library/nlme/po/ko/
%lang(pl) %{_libdir}/R/library/nlme/po/pl/
%{_libdir}/R/library/nlme/R/
%{_libdir}/R/library/nlme/scripts/
# nnet
%dir %{_libdir}/R/library/nnet/
%{_libdir}/R/library/nnet/CITATION
%{_libdir}/R/library/nnet/DESCRIPTION
%{_libdir}/R/library/nnet/help/
%doc %{_libdir}/R/library/nnet/html/
%{_libdir}/R/library/nnet/INDEX
%{_libdir}/R/library/nnet/libs/
%{_libdir}/R/library/nnet/Meta/
%{_libdir}/R/library/nnet/NAMESPACE
%doc %{_libdir}/R/library/nnet/NEWS
%dir %{_libdir}/R/library/nnet/po
%lang(de) %{_libdir}/R/library/nnet/po/de/
%lang(en) %{_libdir}/R/library/nnet/po/en*/
%lang(fr) %{_libdir}/R/library/nnet/po/fr/
%lang(it) %{_libdir}/R/library/nnet/po/it/
%lang(ko) %{_libdir}/R/library/nnet/po/ko/
%lang(pl) %{_libdir}/R/library/nnet/po/pl/
%{_libdir}/R/library/nnet/R/
# parallel
%dir %{_libdir}/R/library/parallel/
%{_libdir}/R/library/parallel/DESCRIPTION
%doc %{_libdir}/R/library/parallel/doc/
%{_libdir}/R/library/parallel/help/
%doc %{_libdir}/R/library/parallel/html/
%{_libdir}/R/library/parallel/INDEX
%{_libdir}/R/library/parallel/libs/
%{_libdir}/R/library/parallel/Meta/
%{_libdir}/R/library/parallel/NAMESPACE
%{_libdir}/R/library/parallel/R/
# rpart
%dir %{_libdir}/R/library/rpart/
%{_libdir}/R/library/rpart/data/
%{_libdir}/R/library/rpart/DESCRIPTION
%doc %{_libdir}/R/library/rpart/doc/
%{_libdir}/R/library/rpart/help/
%doc %{_libdir}/R/library/rpart/html/
%{_libdir}/R/library/rpart/INDEX
%{_libdir}/R/library/rpart/libs/
%{_libdir}/R/library/rpart/Meta/
%{_libdir}/R/library/rpart/NAMESPACE
%doc %{_libdir}/R/library/rpart/NEWS.Rd
%dir %{_libdir}/R/library/rpart/po
%lang(de) %{_libdir}/R/library/rpart/po/de/
%lang(en) %{_libdir}/R/library/rpart/po/en*/
%lang(fr) %{_libdir}/R/library/rpart/po/fr/
%lang(ko) %{_libdir}/R/library/rpart/po/ko/
%lang(pl) %{_libdir}/R/library/rpart/po/pl/
%lang(ru) %{_libdir}/R/library/rpart/po/ru/
%{_libdir}/R/library/rpart/R/
# spatial
%dir %{_libdir}/R/library/spatial/
%{_libdir}/R/library/spatial/CITATION
%{_libdir}/R/library/spatial/DESCRIPTION
%{_libdir}/R/library/spatial/help/
%doc %{_libdir}/R/library/spatial/html/
%{_libdir}/R/library/spatial/INDEX
%{_libdir}/R/library/spatial/libs/
%{_libdir}/R/library/spatial/Meta/
%{_libdir}/R/library/spatial/NAMESPACE
%doc %{_libdir}/R/library/spatial/NEWS
%dir %{_libdir}/R/library/spatial/po
%lang(de) %{_libdir}/R/library/spatial/po/de/
%lang(en) %{_libdir}/R/library/spatial/po/en*/
%lang(fr) %{_libdir}/R/library/spatial/po/fr/
%lang(it) %{_libdir}/R/library/spatial/po/it/
%lang(ko) %{_libdir}/R/library/spatial/po/ko/
%lang(pl) %{_libdir}/R/library/spatial/po/pl/
%{_libdir}/R/library/spatial/ppdata/
%{_libdir}/R/library/spatial/PP.files
%{_libdir}/R/library/spatial/R/
# splines
%dir %{_libdir}/R/library/splines/
%{_libdir}/R/library/splines/DESCRIPTION
%{_libdir}/R/library/splines/help/
%doc %{_libdir}/R/library/splines/html/
%{_libdir}/R/library/splines/INDEX
%{_libdir}/R/library/splines/libs/
%{_libdir}/R/library/splines/Meta/
%{_libdir}/R/library/splines/NAMESPACE
%{_libdir}/R/library/splines/R/
# stats
%dir %{_libdir}/R/library/stats/
%license %{_libdir}/R/library/stats/COPYRIGHTS.modreg
%{_libdir}/R/library/stats/demo/
%{_libdir}/R/library/stats/DESCRIPTION
%doc %{_libdir}/R/library/stats/doc/
%{_libdir}/R/library/stats/help/
%doc %{_libdir}/R/library/stats/html/
%{_libdir}/R/library/stats/INDEX
%{_libdir}/R/library/stats/libs/
%{_libdir}/R/library/stats/Meta/
%{_libdir}/R/library/stats/NAMESPACE
%{_libdir}/R/library/stats/R/
%{_libdir}/R/library/stats/SOURCES.ts
# stats4
%dir %{_libdir}/R/library/stats4/
%{_libdir}/R/library/stats4/DESCRIPTION
%{_libdir}/R/library/stats4/help/
%doc %{_libdir}/R/library/stats4/html/
%{_libdir}/R/library/stats4/INDEX
%{_libdir}/R/library/stats4/Meta/
%{_libdir}/R/library/stats4/NAMESPACE
%{_libdir}/R/library/stats4/R/
# survival
%dir %{_libdir}/R/library/survival/
%{_libdir}/R/library/survival/CITATION
%license %{_libdir}/R/library/survival/COPYRIGHTS
%{_libdir}/R/library/survival/data/
%{_libdir}/R/library/survival/DESCRIPTION
%doc %{_libdir}/R/library/survival/doc/
%{_libdir}/R/library/survival/help
%doc %{_libdir}/R/library/survival/html/
%{_libdir}/R/library/survival/INDEX
%{_libdir}/R/library/survival/libs/
%{_libdir}/R/library/survival/Meta/
%{_libdir}/R/library/survival/NAMESPACE
%doc %{_libdir}/R/library/survival/NEWS.Rd*
%{_libdir}/R/library/survival/R/
# tcltk
%dir %{_libdir}/R/library/tcltk/
%{_libdir}/R/library/tcltk/demo/
%{_libdir}/R/library/tcltk/DESCRIPTION
%{_libdir}/R/library/tcltk/exec/
%{_libdir}/R/library/tcltk/help/
%doc %{_libdir}/R/library/tcltk/html/
%{_libdir}/R/library/tcltk/INDEX
%{_libdir}/R/library/tcltk/libs/
%{_libdir}/R/library/tcltk/Meta/
%{_libdir}/R/library/tcltk/NAMESPACE
%{_libdir}/R/library/tcltk/R/
# tools
%dir %{_libdir}/R/library/tools/
%{_libdir}/R/library/tools/DESCRIPTION
%{_libdir}/R/library/tools/help/
%doc %{_libdir}/R/library/tools/html/
%{_libdir}/R/library/tools/INDEX
%{_libdir}/R/library/tools/libs/
%{_libdir}/R/library/tools/Meta/
%{_libdir}/R/library/tools/NAMESPACE
%{_libdir}/R/library/tools/R/
%{_libdir}/R/library/tools/wre.txt
# utils
%dir %{_libdir}/R/library/utils/
%{_libdir}/R/library/utils/DESCRIPTION
%doc %{_libdir}/R/library/utils/doc/
%{_libdir}/R/library/utils/help/
%doc %{_libdir}/R/library/utils/html/
%{_libdir}/R/library/utils/iconvlist
%{_libdir}/R/library/utils/INDEX
%{_libdir}/R/library/utils/libs/
%{_libdir}/R/library/utils/Meta/
%{_libdir}/R/library/utils/misc/
%{_libdir}/R/library/utils/NAMESPACE
%{_libdir}/R/library/utils/R/
%{_libdir}/R/library/utils/Sweave/
# end of packages
%{_libdir}/R/modules
%license %{_libdir}/R/COPYING
# %%doc %%{_libdir}/R/NEWS*
%{_libdir}/R/SVN-REVISION
%{_infodir}/R-*.info*
%{_mandir}/man1/*
%{_pkgdocdir}
%docdir %{_pkgdocdir}
%{_sysconfdir}/ld.so.conf.d/*
%if 0%{?flatpak}
/usr/bin/Rscript
%endif

%files core-devel
%{_libdir}/pkgconfig/libR.pc
%{_includedir}/R
# Symlink to %%{_includedir}/R/
%{_libdir}/R/include

%files devel
# Nothing, all files provided by R-core-devel

%ifarch %{java_arches}
%files java
# Nothing, all files provided by R-core

%files java-devel
# Nothing, all files provided by R-core-devel
%endif

%files -n libRmath
%license doc/COPYING
%{_libdir}/libRmath.so

%files -n libRmath-devel
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc

%files -n libRmath-static
%{_libdir}/libRmath.a

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Oct 31 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.5.2-1
- Update to 4.5.2

* Tue Aug 05 2025 František Zatloukal <fzatlouk@redhat.com> - 4.5.1-3
- Rebuilt for icu 77.1

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.5.1-1
- Update to 4.5.1

* Wed Apr 23 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 4.5.0-4
- Fix flatpak build

* Fri Apr 18 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.5.0-3
- Add libzstd-devel to Requires

* Fri Apr 18 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.5.0-2
- Add tzdata to Requires

* Fri Apr 18 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.5.0-1
- Update to 4.5.0

* Fri Feb 28 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.3-1
- Update to 4.4.3

* Thu Feb 27 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.2-5
- Remove requirement on tck/tk devel packages

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.2-3
- Depend on compat tcl/tk 8 for now
- Apply upstream patch for gcc15 compatibility

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 4.4.2-2
- Rebuild for ICU 76

* Fri Nov 01 2024 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.2-1
- Update to 4.4.2

* Mon Jul 22 2024 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.1-5
- Add less back as default PAGER

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.1-3
- Add libdeflate to Requires too

* Thu Jul 04 2024 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.1-2
- Enable libdeflate

* Mon Jun 17 2024 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.1-1
- Update to 4.4.1

* Thu Apr 25 2024 Iñaki Úcar <iucar@fedoraproject.org> - 4.4.0-1
- Update to 4.4.0

* Thu Feb 29 2024 Iñaki Úcar <iucar@fedoraproject.org> - 4.3.3-1
- Update to 4.3.3

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 4.3.2-5
- Rebuild for ICU 74

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 01 2023 Iñaki Úcar <iucar@fedoraproject.org> - 4.3.2-2
- Revert adding flexiblas to LAPACK_LIBS as per discussion with Tomas Kalibera

* Tue Oct 31 2023 Iñaki Úcar <iucar@fedoraproject.org> - 4.3.2-1
- Update to 4.3.2

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 4.3.1-2
- Rebuilt for ICU 73.2

* Fri Jun 16 2023 Iñaki Úcar <iucar@fedoraproject.org> - 4.3.1-1
- Update to 4.3.1

* Fri Apr 21 2023 Iñaki Úcar <iucar@fedoraproject.org> - 4.3.0-1
- Update to 4.3.0
- Enable LTO (except for EPEL8)
- Drop some tools from Requires for R-core
- Move latex-stuff to Recommends for R-core-devel
- Mark all html and doc folders as documentation

* Thu Mar 23 2023 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.3-2
- Enable libcurl > 7

* Wed Mar 15 2023 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.3-1
- Update to 4.2.3
- Adapt license tag to SPDX
- Disable tests for non x86_64 architectures in EPEL

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 4.2.2-6
- Rebuild for ICU 72

* Sun Nov 06 2022 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.2-5
- Revert inadvertent change to BLAS condition

* Sat Nov 05 2022 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.2-4
- Remove FlexiBLAS workaround, now officially supported
- Re-enable tests in all platforms
- Fix LTO flag once and for all (thanks, Mattias)

* Sat Nov 05 2022 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.2-3
- Let R find its way into Java instead of specifying too many possible paths

* Fri Nov 04 2022 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.2-2
- Move Java configuration to the build phase
- Remove javareconf from posttrans scriptlets
- Remove noreplace from javaconf file
- Rename LTO flag to avoid conflicts with bcond
- Simplify default R_LIBS_SITE cleanup
- Update old _pkgdocdir specification

* Mon Oct 31 2022 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.2-1
- Update to 4.2.2
- Run new compact-pdf target
- Remove obsolete MAKEINFO and texinfo hack
- Re-enable tests

* Fri Sep 23 2022 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.1-5
- Add flexiblas to LAPACK_LIBS
- Remove java_arches backport, already available in EPEL 8

* Tue Aug 23 2022 Iñaki Úcar <iucar@fedoraproject.org> - 4.2.1-4
- Remove ancient (RHEL 5/6) zlibhack
- Remove conditional paths for ancient RHEL (< 8) and Fedora (< 32)
- Simplify Java and LTO handling
- Simplify BLAS configuration, use openblas-openmp if flexiblas is not available
- Cleanup Requires and BuildRequires + sorting + indentation
- Remove unused files and patches
- Remove redundant flags

* Mon Aug  8 2022 Tom Callaway <spot@fedoraproject.org> - 4.2.1-3
- fix issue where Renviron was setting R_LIBS_SITE to an empty string, which makes it hard to find Fedora's noarch
  packages being installed into /usr/share.

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 4.2.1-2
- Rebuilt for ICU 71.1

* Wed Jul 27 2022 Tom Callaway <spot@fedoraproject.org> - 4.2.1-1
- update to 4.2.1
- disable the R test suite due to unknown failures on i686/x86_64 in koji (and only in koji)

* Mon Jul 25 2022 Tom Callaway <spot@fedoraproject.org> - 4.1.3-3
- add new "usejava" conditional
- do not "usejava" when Fedora >= 37 and i686

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Mar 19 2022 Tom Callaway <spot@fedoraproject.org> - 4.1.3-1
- update to 4.1.3

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.1.2-4
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 26 2022 Tom Callaway <spot@fedoraproject.org> - 4.1.2-3
- disable _package_note_flags because it breaks R modules

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov  3 2021 Tom Callaway <spot@fedoraproject.org> - 4.1.2-1
- update to 4.1.2

* Fri Oct 29 2021 Iñaki Úcar <iucar@fedoraproject.org> - 4.1.1-2
- Move javareconf to posttrans (bz 2009974)

* Sat Aug 14 2021 Tom Callaway <spot@fedoraproject.org> - 4.1.1-1
- update to 4.1.1

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun  7 2021 Tom Callaway <spot@fedoraproject.org> - 4.1.0-1
- update to 4.1.0

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 4.0.5-2
- Rebuild for ICU 69

* Mon May  3 2021 Tom Callaway <spot@fedoraproject.org> - 4.0.5-1
- update to 4.0.5

* Mon Feb 15 2021 Tom Callaway <spot@fedoraproject.org> - 4.0.4-1
- update to 4.0.4

* Wed Feb 03 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 4.0.3-3
- Always provide normalized versions of R submodules
- Fixes rhbz#1924565

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 12 2020 Tom Callaway <spot@fedoraproject.org> - 4.0.3-1
- update to 4.0.3

* Tue Sep  8 2020 Tom Callaway <spot@fedoraproject.org> - 4.0.2-5
- make cups a "Recommends" instead of a "Requires" (bz1875165)
- even though f31 uses a forked spec file, reflect the systemlapack change there here

* Fri Aug 07 2020 Iñaki Úcar <iucar@fedoraproject.org> - 4.0.2-4
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Tom Callaway <spot@fedoraproject.org> - 4.0.2-2
- add additional paths to find libjvm.so (OpenJDK 11+)

* Mon Jun 22 2020 Tom Callaway <spot@fedoraproject.org> - 4.0.2-1
- update to 4.0.2

* Tue Jun 16 2020 Tom Callaway <spot@fedoraproject.org> - 4.0.1-1
- update to 4.0.1

* Mon Jun 15 2020 Pete Walter <pwalter@fedoraproject.org> - 4.0.0-3
- Rebuild for ICU 67

* Tue Jun 2 2020 Tom Callaway <spot@fedoraproject.org> - 4.0.0-2
- apply upstream fix for ppc64 infinite loop

* Fri May 8 2020 Tom Callaway <spot@fedoraproject.org> - 4.0.0-1
- update to 4.0.0
  NOTE: This major release update requires all installed R modules to be rebuilt in order to work.
  To help with this, we've added an R(ABI) Provides/Requires setup.

* Mon Mar  2 2020 Tom Callaway <spot@fedoraproject.org> - 3.6.3-1
- update to 3.6.3
- conditionalize lapack changes from previous commits to Fedora 32+ and EPEL-8

* Tue Feb 18 2020 Tom Callaway <spot@fedoraproject.org> - 3.6.2-5
- fix openblas conditionals, openblas has wider arch support everywhere except el7

* Tue Feb 18 2020 Tom Callaway <spot@fedoraproject.org> - 3.6.2-4
- fix conditionals so that Fedora builds against system openblas for lapack/blas
  and we only generate the R lapack/blas libs on RHEL 5-6-7 (where system lapack/openblas
  is not reliable). Thanks to Dirk Eddelbuettel for pointing out the error.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Tom Callaway <spot@fedoraproject.org> - 3.6.2-2
- adjust ppc64 patch to reflect upstream fix

* Thu Dec 12 2019 Tom Callaway <spot@fedoraproject.org> - 3.6.2-1
- update to 3.6.2
- disable tests on all non-intel arches
- fix powerpc64

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 3.6.1-3
- Rebuild for ICU 65

* Fri Aug 30 2019 Tom Callaway <spot@fedoraproject.org> - 3.6.1-2
- conditionalize macro usage so that it only happens on Fedora 31+ and EPEL-8

* Fri Aug 16 2019 Tom Callaway <spot@fedoraproject.org> - 3.6.1-1
- update to 3.6.1

* Sun Aug 11 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.6.0-5
- Remove unused and nonfunctional macros and helper script

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.6.0-3
- Add automated dependency generator to R-devel
- Add standard Provides for bundled libraries

* Thu Jun 13 2019 Tom Callaway <spot@fedoraproject.org> - 3.6.0-2
- use devtoolset toolchain to compile on el6/el7 for C++11 support

* Wed May 29 2019 Tom Callaway <spot@fedoraproject.org> - 3.6.0-1
- update to 3.6.0
- use --no-optimize-sibling-calls for gfortran to work around issues

* Mon Mar 11 2019 Tom Callaway <spot@fedoraproject.org> - 3.5.3-1
- update to 3.5.3

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.2-5
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 3.5.2-3
- Rebuild for ICU 63

* Tue Jan  8 2019 Tom Callaway <spot@fedoraproject.org> - 3.5.2-2
- handle pcre2 use/detection

* Mon Jan  7 2019 Tom Callaway <spot@fedoraproject.org> - 3.5.2-1
- update to 3.5.2

* Fri Dec  7 2018 Tom Callaway <spot@fedoraproject.org> - 3.5.1-2
- use absolute path in symlink for latex dir (bz1594102)

* Mon Sep 10 2018 Tom Callaway <spot@fedoraproject.org> - 3.5.1-1
- update to 3.5.1
- update bundled curl to 7.61.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 3.5.0-5
- Rebuild for ICU 62

* Tue Jun  5 2018 Tom Callaway <spot@fedoraproject.org> - 3.5.0-4
- only own /usr/share/texmf/tex/latex/R ... not /usr/share/texmf

* Fri May 18 2018 Tom Callaway <spot@fedoraproject.org> - 3.5.0-3
- do not run javareconf on el6/ppc64 EVEN in the java subpackages

* Fri May 18 2018 Tom Callaway <spot@fedoraproject.org> - 3.5.0-2
- do not run javareconf on el6/ppc64

* Mon May 14 2018 Tom Callaway <spot@fedoraproject.org> - 3.5.0-1
- update to 3.5.0
- update xz bundle (rhel6 only)
- disable tests on armv7hl
- disable info builds on rhel 6

* Sun May 13 2018 Stefan O'Rear <sorear2@gmail.com> - 3.4.4-3
- Add riscv* to target CPU specs

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 3.4.4-2
- Rebuild for ICU 61.1

* Wed Mar 28 2018 Tom Callaway <spot@fedoraproject.org> - 3.4.4-1
- update to 3.4.4
- update pcre and curl bundles (rhel6 only)

* Mon Feb 12 2018 Tom Callaway <spot@fedoraproject.org> - 3.4.3-6
- undefine %%__brp_mangle_shebangs (we need +x on files in %%{_libdir}/R/bin/)

* Wed Feb  7 2018 Tom Callaway <spot@fedoraproject.org> - 3.4.3-5
- fix exec permissions on files in %%{_libdir}/R/bin/

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb  2 2018 Tom Callaway <spot@fedoraproject.org> - 3.4.3-3
- rebuild for new gfortran

* Fri Dec 01 2017 Pete Walter <pwalter@fedoraproject.org> - 3.4.3-2
- Rebuild once more for ICU 60.1

* Thu Nov 30 2017 Tom Callaway <spot@fedoraproject.org> - 3.4.3-1
- update to 3.4.3

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 3.4.2-3
- Rebuild for ICU 60.1

* Mon Oct 30 2017 Tom Callaway <spot@fedoraproject.org> - 3.4.2-2
- conditionalize Requires on perl-interpreter for fedora only

* Fri Oct 27 2017 Tom Callaway <spot@fedoraproject.org>- 3.4.2-1
- update to 3.4.2

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 3.4.1-2
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Fri Jun 30 2017 Tom Callaway <spot@fedoraproject.org> - 3.4.1-1
- update to 3.4.1

* Fri May 12 2017 José Matos <jamatos@fedoraproject.org> - 3.4.0-2
- add TZ="Europe/Paris" to please make check

* Sat Apr 22 2017 Tom Callaway <spot@fedoraproject.org> - 3.4.0-1
- update to 3.4.0

* Wed Mar  8 2017 Tom Callaway <spot@fedoraproject.org> - 3.3.3-1
- update to 3.3.3

* Tue Feb 14 2017 Tom Callaway <spot@fedoraproject.org> - 3.3.2-8
- disable tests on ppc64/ppc64le (no real way to debug them)

* Tue Feb 14 2017 Björn Esser <besser82@fedoraproject.org> - 3.3.2-7
- Add Patch2 to fix detection of zlib

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Björn Esser <besser82@fedoraproject.org> - 3.3.2-5
- Rebuilt for GCC-7

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.3.2-4
- Rebuild for readline 7.x

* Wed Dec 14 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.2-3
- openblas-Rblas provides libRblas.so now

* Mon Oct 31 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.2-2
- fix provides for openblas hack
- fix version for recommended components that are included

* Mon Oct 31 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.2-1.1
- disable readline support for el5

* Mon Oct 31 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.2-1
- update to 3.3.2

* Fri Oct 28 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.1-5
- add false Provides in openblas case

* Fri Oct 28 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.1-4
- use -Wl,--as-needed on zlibhack targets (bz 1389715)
- use openblas on architectures where it exists, keep R reference blas as "libRrefblas.so"

* Mon Aug 29 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.1-3
- fix use of _isa to be conditionalized on its existence (looking at you el5)

* Mon Aug  8 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.1-2
- add Requires: libmath to R-core

* Tue Jul  5 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.1-1
- update to 3.3.1

* Sat Jun 11 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-10
- fix CAPABILITIES pathing

* Sat Jun 11 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-9
- fix ldpaths for zlibhack
- clean libtool
- clean CAPABILITIES

* Thu Jun  9 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-8
- fix FLIBS cleanup for el5

* Thu Jun  9 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-7
- clean up zlibhack from FLIBS

* Tue Jun  7 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-6
- fix sed invocations to cover both el5 and el6 (thanks again to Mattias Ellert)

* Mon Jun  6 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-5
- fix sed invocations to fully cleanup zlibhack (thanks to Mattias Ellert)

* Wed Jun  1 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-4
- fixup libR.pc for zlibhack (el5/el6)

* Fri May 13 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-3
- we no longer need Requires: blas-devel, lapack-devel for R-core-devel

* Wed May 11 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-2.1
- implement "zlibhack" to build R against bundled bits too old in RHEL 5 & 6

* Tue May 10 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-2
- RHEL 6 ppc64 doesn't have libicu-devel. :P

* Tue May 10 2016 Tom Callaway <spot@fedoraproject.org> - 3.3.0-1
- update to 3.3.0
- fix R-java Requires (bz1324145)
- fix JAVA_PATH definition in javareconf (bz1324145)
- use bundled BLAS and LAPACK, create shared library for Rblas

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 3.2.4-2
- rebuild for ICU 57.1

* Fri Mar 18 2016 Tom Callaway <spot@fedoraproject.org> - 3.2.4-1
- move to 3.2.4-revised

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Tom Callaway <spot@fedoraproject.org> - 3.2.3-4
- if texi2any is set to 0, then copy in prebuilt html manuals (RHEL 5 & 6 only)

* Tue Jan 26 2016 Tom Callaway <spot@fedoraproject.org> - 3.2.3-3
- use global instead of define

* Fri Jan 15 2016 Tom Callaway <spot@fedoraproject.org> - 3.2.3-2
- Requires: redhat-rpm-config on hardened systems (all Fedora and RHEL 7+)

* Fri Dec 11 2015 Tom Callaway <spot@fedoraproject.org> - 3.2.3-1
- update to 3.2.3

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 3.2.2-3
- rebuild for ICU 56.1

* Tue Oct 13 2015 Tom Callaway <spot@fedoraproject.org> - 3.2.2-2
- apply patches from upstream bug 16497 to fix X11 hangs

* Fri Aug 14 2015 Tom Callaway <spot@fedoraproject.org> - 3.2.2-1
- update to 3.2.2

* Fri Jul 10 2015 Tom Callaway <spot@fedoraproject.org> - 3.2.1-2
- BR: libcurl-devel

* Thu Jun 18 2015 Tom Callaway <spot@fedoraproject.org> - 3.2.1-1
- update to 3.2.1

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Jakub Čajka <jcajka@redhat.com> - 3.2.0-2
- valgrind is available only on selected arches, fixes build on s390

* Thu Apr 30 2015 Tom Callaway <spot@fedoraproject.org>
- conditionalize MAKEINFO for ancient things (rhel 6 or older)

* Sun Apr 26 2015 Tom Callaway <spot@fedoraproject.org> - 3.2.0-1
- update to 3.2.0

* Mon Mar  9 2015 Tom Callaway <spot@fedoraproject.org> - 3.1.3-1
- update to 3.1.3

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 3.1.2-2
- rebuild for ICU 54.1

* Fri Oct 31 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.2-1
- update to 3.1.2

* Wed Oct 29 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.1-8
- rebuild for new tcl/tk
- mark Makeconf as config (not config(noreplace) so that we get proper updated tcl/tk libs)

* Mon Sep 29 2014 Orion Poplawski <orion@cora.nwra.com> - 3.1.1-7
- Just BR/R java instead of java-1.5.0-gcj (bug #1110684)

* Tue Sep 16 2014 David Sommerseth <davids@redhat.com> - 3.1.1-6
- Setting ulimit when running make check, to avoid segfault due to too small stack (needed on PPC64)

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 3.1.1-5
- rebuild for ICU 53.1

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug  8 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.1-3
- add "unzip" to Requirements list for R-core

* Fri Aug  8 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.1-2
- add "make" to Requirements list for R-core (thanks R config)

* Thu Jul 10 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.1-1
- update to 3.1.1

* Mon Jul  7 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.0-10
- disable lto everywhere (breaks debuginfo) (bz 1113404)
- apply fix for ppc64 (bz 1114240 and upstream bug 15856)
- add make check (bz 1059461)
- use bundled blas/lapack for RHEL due to bugs in their BLAS
- enable Rblas shared lib (whether using bundled BLAS or not)
- add explicit requires for new lapack

* Tue Jun 24 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.0-9
- mark files in %%{_libdir}/R/etc as config(noreplace), resolves 1098663

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Thu May 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.1.0-6
- Add aarch64 to target CPU specs

* Wed May  7 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.0-5
- add blas-devel and lapack-devel as Requires for R-devel/R-core-devel
  to ease rebuild pain

* Tue Apr 29 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.0-4
- unified spec file for all targets

* Tue Apr 29 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.0-3
- epel fixes

* Fri Apr 25 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.0-2
- fix core-devel Requires

* Mon Apr 21 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.0-1
- update to 3.1.0

* Mon Mar 24 2014 Brent Baude <baude@us.ibm.com> - 3.0.3-2
- add ppc64le support
- rhbz #1077819

* Thu Mar 20 2014 Tom Callaway <spot@fedoraproject.org> - 3.0.3-1
- update to 3.0.3
- switch to java-headless

* Fri Feb 14 2014 David Tardon <dtardon@redhat.com> - 3.0.2-7
- rebuild for new ICU

* Sat Feb  8 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.0.2-6
- Install macros to %%{_rpmconfigdir}/macros.d where available.
- Fix rpmlint spaces vs tabs warnings.

* Fri Feb  7 2014 Tom Callaway <spot@fedoraproject.org> - 3.0.2-5
- add support for system tre (f21+, rhel 7+)

* Fri Feb  7 2014 Orion Poplawski <orion@cora.nwra.com> - 3.0.2-4
- Use BR java

* Fri Jan 24 2014 Tom Callaway <spot@fedoraproject.org> - 3.0.2-3
- disable lto on non-modern targets (not just ppc)

* Fri Dec 20 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.2-2
- add --with-blas, --enable-lto to configure

* Tue Oct 15 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.2-1
- update to 3.0.2

* Mon Aug 12 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.1-4
- add support for unversioned docdir in F20+
- fix compile on arm (thanks Debian, wish you'd upstreamed that patch)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 18 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.1-2
- conditionalize the ugly hack for fedora 19+

* Fri May 17 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.1-1
- update to 3.0.1

* Sat Apr 13 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.0-2
- add Requires: tex(inconsolata.sty) to -core-devel to fix module PDF building

* Fri Apr  5 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.0-1
- update to 3.0.0

* Wed Feb 27 2013 Tom Callaway <spot@fedoraproject.org> - 2.15.2-7
- add BuildRequires: xz-devel (for system xz/lzma support)
- create R-core-devel

* Sat Jan 26 2013 Kevin Fenzi <kevin@scrye.com> - 2.15.2-6
- Rebuild for new icu

* Sun Jan 20 2013 Tom Callaway <spot@fedoraproject.org> - 2.15.2-5
- apply upstream fix for cairo issues (bz 891983)

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.15.2-4
- rebuild due to "jpeg8-ABI" feature drop

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.2-3
- add Requires: tex(cm-super-ts1.enc) for R-devel

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.2-2
- add additional TeX font requirements to R-devel for Fedora 18+ (due to new texlive)

* Mon Oct 29 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.2-1
- update to 2.15.2
- R now Requires: R-java (for a more complete base install)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.1-1
- update to 2.15.1

* Mon Jul  2 2012 Jindrich Novy <jnovy@redhat.com> - 2.15.0-4
- fix LaTeX and dvips dependencies (#836817)

* Mon May  7 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.0-3
- rebuild for new libtiff

* Tue Apr 24 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.0-2
- rebuild for new icu

* Fri Mar 30 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.0-1
- Update to 2.15.0

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.14.1-3
- Rebuild against PCRE 8.30

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan  4 2012 Tom Callaway <spot@fedoraproject.org> - 2.14.1-1
- update to 2.14.1

* Tue Nov  8 2011 Tom Callaway <spot@fedoraproject.org> - 2.14.0-3
- No inconsolata for EL

* Mon Nov  7 2011 Tom Callaway <spot@fedoraproject.org> - 2.14.0-2
- add texinfo-tex to Requires for -devel package

* Wed Nov  2 2011 Tom Callaway <spot@fedoraproject.org> - 2.14.0-1
- update to 2.14.0

* Fri Oct  7 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.2-1
- update to 2.13.2

* Mon Sep 12 2011 Michel Salim <salimma@fedoraproject.org> - 2.13.1-5
- rebuild for libicu 4.8.x

* Tue Aug  9 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.1-4
- fix salimma's scriptlets to be on -core instead of the metapackage

* Tue Aug  9 2011 Michel Salim <salimma@fedoraproject.org> - 2.13.1-3
- Symlink LaTeX files, and rehash on package change when possible (# 630835)

* Mon Aug  8 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.1-2
- add BuildRequires: less

* Mon Jul 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.1-1
- update to 2.13.1

* Tue Apr 12 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.0-1
- update to 2.13.0
- add convenience symlink for include directory (bz 688295)

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 2.12.2-2
- rebuild for icu 4.6

* Sun Feb 27 2011 Tom Callaway <spot@fedoraproject.org> - 2.12.2-1
- update to 2.12.2

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Tom Callaway <spot@fedoraproject.org> - 2.12.1-1
- update to 2.12.1

* Wed Oct 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12.0-1
- update to 2.12.0

* Wed Jul  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-4
- include COPYING in libRmath package

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-3
- move libRmath static lib into libRmath-static subpackage

* Thu Jun  3 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-2
- overload R_LIBS_SITE instead of R_LIBS

* Tue Jun  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-1
- update to 2.11.1

* Thu Apr 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.0-1
- update to 2.11.0

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 2.10.1-2
- rebuild for icu 4.4

* Mon Dec 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.1-1
- update to 2.10.1
- enable static html pages

* Mon Nov  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.0-2
- get rid of index.txt scriptlet on R-core (bz 533572)
- leave macro in place, but don't call /usr/lib/rpm/R-make-search-index.sh equivalent anymore
- add version check to see if we need to run R-make-search-index.sh guts

* Wed Nov  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.0-1
- update to 2.10.0
- use correct compiler for ARM

* Thu Oct 15 2009 Karsten Hopp <karsten@redhat.com> 2.9.2-2
- s390 (not s390x) needs the -m31 compiler flag

* Mon Aug 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.2-1
- Update to 2.9.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.1-2
- don't try to make the PDFs in rawhide/i586

* Thu Jul  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.1-1
- update to 2.9.1
- fix versioned provides

* Mon Apr 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.0-2
- properly Provide/Obsolete R-Matrix

* Fri Apr 17 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.0-1
- update to 2.9.0, change vim dep to vi

* Tue Apr  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-9
- drop profile.d scripts, they broke more than they fixed
- minimize hard-coded Requires based on Martyn Plummer's analysis

* Sat Mar 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-8
- fix profile scripts for situation where R_HOME is already defined
  (bugzilla 492706)

* Tue Mar 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-7
- bump for new tag

* Tue Mar 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-6
- add profile.d scripts to set R_HOME
- rpmlint cleanups

* Mon Mar 23 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-5
- add R-java and R-java-devel "dummy" packages, so that we can get java dependent R-modules
  to build/install

* Wed Mar  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-4
- update post scriptlet (bz 477076)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan  5 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.1-2
- add pango-devel to BuildRequires (thanks to Martyn Plummer and Peter Dalgaard)
- fix libRmath requires to need V-R (thanks to Martyn Plummer)

* Mon Dec 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.1-1
- update javareconf call in %%post (bz 477076)
- 2.8.1

* Sun Oct 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.0-2
- enable libtiff interface

* Sun Oct 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.0-1
- Update to 2.8.0
- New subpackage layout: R-core is functional userspace, R is metapackage
  requiring everything
- Fix system bzip2 detection

* Thu Oct 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-2
- fix sh compile (bz 464055)

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-1
- update to 2.7.2
- fix spec for alpha compile (bz 458931)
- fix security issue in javareconf script (bz 460658)

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.1-1
- update to 2.7.1

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-5
- add cairo-devel to BR/R, so that cairo backend gets built

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-4
- fixup sed invocation added in -3
- make -devel package depend on base R = version-release
- fix bad paths in package html files

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-3
- fix poorly constructed file paths in html/packages.html (bz 442727)

* Tue May 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-2
- add patch from Martyn Plummer to avoid possible bad path hardcoding in
  /usr/bin/Rscript
- properly handle ia64 case (bz 446181)

* Mon Apr 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-1
- update to 2.70
- rcompgen is no longer a standalone package
- redirect javareconf to /dev/null (bz 442366)

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.2-1
- properly version the items in the VR bundle
- 2.6.2
- don't use setarch for java setup
- fix R post script file

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-4
- multilib handling (thanks Martyn Plummer)
- Update indices in the right place.

* Mon Jan  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-3
- move INSTALL back into R main package, as it is useful without the
  other -devel bits (e.g. installing noarch package from CRAN)

* Tue Dec 11 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-2
- based on changes from Martyn Plummer <martyn.plummer@r-project.org>
- use configure options rdocdir, rincludedir, rsharedir
- use DESTDIR at installation
- remove obsolete generation of packages.html
- move header files and INSTALL R-devel package

* Mon Nov 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-1
- bump to 2.6.1

* Tue Oct 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-3.1
- fix missing perl requires

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-3
- fix multilib conflicts (bz 343061)

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-2
- add R CMD javareconf to post (bz 354541)
- don't pickup bogus perl provides (bz 356071)
- use xdg-open, drop requires for firefox/evince (bz 351841)

* Thu Oct  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-1
- bump to 2.6.0

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-3
- fix license tag
- rebuild for ppc32

* Thu Jul  5 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-2
- add rpm helper macros, script

* Mon Jul  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-1
- drop patch, upstream fixed
- bump to 2.5.1

* Mon Apr 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.0-2
- patch from Martyn Plummer fixes .pc files
- add new BR: gcc-objc

* Wed Apr  25 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.0-1
- bump to 2.5.0

* Tue Mar  13 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-4
- get rid of termcap related requires, replace with ncurses
- use java-1.5.0-gcj instead of old java-1.4.2
- add /usr/share/R/library as a valid R_LIBS directory for noarch bits

* Sun Feb  25 2007 Jef Spaleta <jspaleta@gmail.com> 2.4.1-3
- rebuild for reverted tcl/tk

* Fri Feb  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-2
- rebuild for new tcl/tk

* Tue Dec 19 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-1
- bump to 2.4.1
- fix install-info invocations in post/preun (bz 219407)

* Fri Nov  3 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.0-2
- sync with patched 2006-11-03 level to fix PR#9339

* Sun Oct 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.0-1
- bump for 2.4.0

* Tue Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.1-2
- bump for FC-6

* Fri Jun  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.1-1
- bump to 2.3.1

* Tue Apr 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.0-2
- fix ppc build for FC-4 (artificial bump for everyone else)

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.0-1
- bump to 2.3.0 (also, bump module revisions)

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-5
- now BR is texinfo-tex, not texinfo in rawhide

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-4
- bump for FC-5

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-3
- fix BR: XFree86-devel for FC-5

* Sat Dec 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-2
- missing BR: libXt-devel for FC-5

* Tue Dec 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-1
- bump to 2.2.1

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.0-2
- use fixed system lapack for FC-4 and devel

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.0-1
- bump to 2.2.0

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.1-2
- fix version numbers on supplemental package provides

* Mon Jun 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.1-1
- bugfix update

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-51
- proper library handling

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-50
- 2.1.0, fc4 version.
- The GNOME GUI is unbundled, now provided as a package on CRAN

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-50
- big bump. This is the fc4 package, the fc3 package is 2.0.1-11
- enable gnome gui, add requires as needed

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-10
- bump for cvs errors

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-9
- fix URL for Source0

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-8
- spec file cleanup

* Fri Apr  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-7
- use evince instead of ggv
- make custom provides for R subfunctions

* Wed Mar 30 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-6
- configure now calls --enable-R-shlib

* Thu Mar 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-5
- cleaned up package for Fedora Extras

* Mon Feb 28 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.4
- Fixed file ownership in R-devel and libRmath packages

* Wed Feb 16 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.3
- R-devel package is now a stub package with no files, except a documentation
  file (RPM won't accept sub-packages with no files). R now conflicts
  with earlier (i.e 0:2.0.1-0.fdr.2) versions of R-devel.
- Created libRmath subpackage with shared library.

* Mon Jan 31 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.2
- Created R-devel and libRmath-devel subpackages

* Mon Nov 15 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.1
- Built R 2.0.1

* Wed Nov 10 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.3
- Set R_PRINTCMD at configure times so that by default getOption(printcmd)
  gives "lpr".
- Define macro fcx for all Fedora distributions. This replaces Rinfo

* Tue Oct 12 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.2
- Info support is now conditional on the macro Rinfo, which is only
  defined for Fedora 1 and 2.

* Thu Oct 7 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.1
- Built R 2.0.0
- There is no longer a BUGS file, so this is not installed as a
  documentation file.

* Mon Aug  9 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.4
- Added gcc-g++ to the list of BuildRequires for all platforms.
  Although a C++ compiler is not necessary to build R, it must
  be present at configure time or R will not be correctly configured
  to build packages containing C++ code.

* Thu Jul  1 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.3
- Modified BuildRequires so we can support older Red Hat versions without
  defining any macros.

* Wed Jun 23 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.2
- Added libtermcap-devel as BuildRequires for RH 8.0 and 9. Without
  this we get no readline support.

* Mon Jun 21 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.1
- Build R 1.9.1
- Removed Xorg patch since fix is now in R sources

* Mon Jun 14 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.4
- Added XFree86-devel as conditional BuildRequires for rh9, rh80

* Tue Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.3
- Corrected names for fc1/fc2/el3 when using conditional BuildRequires
- Configure searches for C++ preprocessor and fails if we don't have
  gcc-c++ installed. Added to BuildRequires for FC2.

* Tue Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.2
- Added patch to overcome problems with X.org headers (backported
  from R 1.9.1; patch supplied by Graeme Ambler)
- Changed permissions of source files to 644 to please rpmlint

* Mon May 03 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.1
- R.spec file now has mode 644. Previously it was unreadable by other
  users and this was causing a crash building under mach.
- Changed version number to conform to Fedora conventions.
- Removed Provides: and Obsoletes: R-base, R-recommended, which are
  now several years old. Nobody should have a copy of R-base on a
  supported platform.
- Changed buildroot to Fedora standard
- Added Requires(post,preun): info
- Redirect output from postinstall/uninstall scripts to /dev/null
- Added BuildRequires tags necessary to install R with full
  capabilities on a clean mach buildroot. Conditional buildrequires
  for tcl-devel and tk-devel which were not present on RH9 or earlier.

* Thu Apr 01 2004 Martyn Plummer <plummer@iarc.fr>
- Added patch to set environment variable LANG to C in shell wrapper,
  avoiding warnings about UTF-8 locale not being supported

* Mon Mar 15 2004 Martyn Plummer <plummer@iarc.fr>
- No need to export optimization flags. This is done by %%configure
- Folded info installation into %%makeinstall
- Check that RPM_BASE_ROOT is not set to "/" before cleaning up

* Tue Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Removed tcl-devel from BuildRequires

* Tue Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Changes from James Henstridge <james@daa.com.au> to allow building on IA64:
- Added BuildRequires for tcl-devel tk-devel tetex-latex
- Use the %%configure macro to call the configure script
- Pass --with-tcl-config and --with-tk-config arguments to configure
- Set rhome to point to the build root during "make install"

* Wed Jan 07 2004 Martyn Plummer <plummer@iarc.fr>
- Changed obsolete "copyright" field to "license"

* Fri Nov 21 2003 Martyn Plummer <plummer@iarc.fr>
- Built 1.8.1
