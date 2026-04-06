## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# From src/version.h:#define OCTAVE_API_VERSION
%global octave_api api-v60

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%global builddocs 1

%if 0%{?fedora} || 0%{?rhel} >= 9
%bcond_without flexiblas
%endif
%if %{with flexiblas}
%global blaslib flexiblas
%else
%global blaslib openblas
%endif

# No more Java on i686
%ifarch %{java_arches}
%bcond_without java
%else
%bcond_with java
%endif

# Compile with ILP64 BLAS - not yet working
%bcond_with blas64

# For rc versions, change release manually
#global rcver 2
%if 0%{?rcver:1}
%global rctag  -rc%{?rcver}
%global relsuf .rc%{?rcver}
%endif

%global optflags %{optflags}
%global build_ldflags %{build_ldflags} -flto

Name:           octave
Epoch:          6
Version:        10.2.0
Release:        %autorelease
Summary:        A high-level language for numerical computations
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:        GPL-3.0-or-later
URL:            http://www.octave.org

Source0:        https://ftp.gnu.org/gnu/octave/octave-%{version}.tar.lz
#Source0:        https://alpha.gnu.org/gnu/octave/octave-%{version}%{?rctag}.tar.lz
# RPM macros for helping to build Octave packages
Source1:        macros.octave
Source2:        xorg.conf
%if !%{builddocs}
Source3:        octave-%{version}-docs.tar.xz
%endif
# Add needed time.h header
Patch2:         octave-time.patch

Provides:       octave(api) = %{octave_api}
Provides:       bundled(gnulib)
Provides:       bundled(qterminal)
# From liboctave/cruft
Provides:       bundled(amos)
Provides:       bundled(blas-xtra)
Provides:       bundled(daspk)
Provides:       bundled(dasrt)
Provides:       bundled(dassl)
Provides:       bundled(faddeeva)
Provides:       bundled(lapack-xtra)
Provides:       bundled(odepack)
Provides:       bundled(ordered-qz)
Provides:       bundled(quadpack)
Provides:       bundled(ranlib)
Provides:       bundled(slatec-err)
Provides:       bundled(slatec-fn)

# For Source0
BuildRequires: make
BuildRequires:  lzip

# For autoreconf
BuildRequires:  automake
BuildRequires:  libtool
# For validating desktop and appdata files
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

BuildRequires:  arpack-devel
BuildRequires:  %{blaslib}-devel
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  fftw-devel
BuildRequires:  flex
BuildRequires:  fltk-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  ghostscript
BuildRequires:  gl2ps-devel
BuildRequires:  glpk-devel
BuildRequires:  gnuplot
BuildRequires:  gperf
BuildRequires:  GraphicsMagick-c++-devel
BuildRequires:  hdf5-devel
%if %{with java}
BuildRequires:  java-25-devel
%if 0%{?fedora}
BuildRequires:  javapackages-local-openjdk25
%endif
%endif
BuildRequires:  less
BuildRequires:  libsndfile-devel
BuildRequires:  libX11-devel
BuildRequires:  llvm-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel
BuildRequires:  portaudio-devel
BuildRequires:  qhull-devel
BuildRequires:  qrupdate-devel
BuildRequires:  qscintilla-qt6-devel
BuildRequires:  qt6-linguist
BuildRequires:  qt6-qttools-devel
BuildRequires:  pkgconfig(Qt6Core5Compat)
BuildRequires:  rapidjson-devel
BuildRequires:  readline-devel
%if %{with blas64}
BuildRequires:  suitesparse64-devel
%else
BuildRequires:  suitesparse-devel
%endif
# EPEL9 is missing sundials - https://bugzilla.redhat.com/show_bug.cgi?id=2063760
%if 0%{?fedora} || 0%{?rhel} != 9
BuildRequires:  sundials-devel
%endif
BuildRequires:  tex(dvips)
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
BuildRequires:  texlive-collection-fontsrecommended
%if 0%{?rhel}
BuildRequires:  texlive-ec
BuildRequires:  texlive-metapost
%endif
BuildRequires:  zlib-devel
# For check
BuildRequires:  mesa-libGL
%ifnarch s390 s390x
BuildRequires:  xorg-x11-drv-dummy
%endif
BuildRequires:  zip

Requires:       epstool
Requires:       gnuplot
Requires:       gnuplot-common
Requires:       hdf5 = %{_hdf5_version}
Requires:       hicolor-icon-theme
%if %{with java}
Requires:       java-25-headless
%endif
Requires:       less
%if %{undefined flatpak}
Requires:       info
Requires:       texinfo
# Rrom scripts/general/private/__publish_latex_output__.m
Requires:       tex(amssymb.sty)
Requires:       tex(fontenc.sty)
Requires:       tex(graphicx.sty)
Requires:       tex(hyperref.sty)
Requires:       tex(inputenc.sty)
Requires:       tex(listings.sty)
Requires:       tex(lmodern.sty)
Requires:       tex(mathtools.sty)
Requires:       tex(titlesec.sty)
Requires:       tex(xcolor.sty)
# Rrom scripts/plot/util/print.m:
Requires:       tex(color.sty)
Requires:       tex(epsfig.sty)
Requires:       tex(geometry.sty)
Requires:       tex(graphicx.sty)
%endif


%description
GNU Octave is a high-level language, primarily intended for numerical
computations. It provides a convenient command line interface for
solving linear and nonlinear problems numerically, and for performing
other numerical experiments using a language that is mostly compatible
with Matlab. It may also be used as a batch-oriented language. Octave
has extensive tools for solving common numerical linear algebra
problems, finding the roots of nonlinear equations, integrating
ordinary functions, manipulating polynomials, and integrating ordinary
differential and differential-algebraic equations. It is easily
extensible and customizable via user-defined functions written in
Octave's own language, or using dynamically loaded modules written in
C++, C, Fortran, or other languages.


%package devel
Summary:        Development headers and files for Octave
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       gcc-c++
Requires:       gcc-gfortran
Requires:       fftw-devel%{?_isa}
Requires:       hdf5-devel%{?_isa}
Requires:       %{blaslib}-devel%{?_isa}
Requires:       readline-devel%{?_isa}
Requires:       zlib-devel
Requires:       libappstream-glib

%description devel
The octave-devel package contains files needed for developing
applications which use GNU Octave.


%package doc
Summary:        Documentation for Octave
BuildArch:      noarch

%description doc
This package contains documentation for Octave.

%prep
%autosetup -p1 -n %{name}-%{version}%{?rctag}
%if %{with blas64}
sed -i -e 's/OCTAVE_CHECK_LIB(suitesparseconfig,/OCTAVE_CHECK_LIB(suitesparseconfig64,/' configure.ac
%endif

%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export F77=gfortran
# TODO: some items appear to be bundled in libcruft..
#   gl2ps.c is bundled.  Anything else?
%if !%{builddocs}
%global disabledocs --disable-docs
%endif
%if %{with java}
# Find libjvm.so for this architecture in generic location
libjvm=$(find %{_jvmdir}/jre/lib -name libjvm.so -printf %h)
export JAVA_HOME=%{java_home}
%endif
# JIT support is still experimental, and causes a segfault on ARM.
# --enable-float-truncate - https://savannah.gnu.org/bugs/?40560
# sundials headers need to know where to find suitesparse headers
export CPPFLAGS=-I%{_includedir}/suitesparse
# Disable _GLIBCXX_ASSERTIONS for now
# https://savannah.gnu.org/bugs/?55547
export CXXFLAGS="$(echo %optflags | sed s/-Wp,-D_GLIBCXX_ASSERTIONS//)"

verstr=$(%{__cxx} --version | head -1)
if [[ "$verstr" == *"GCC"* ]]; then
  CXXFLAGS="$CXXFLAGS -flto=auto"
else
  CXXFLAGS="$CXXFLAGS -flto"
fi

%configure --enable-shared --disable-static \
 --enable-float-truncate \
 %{?disabledocs} \
 --disable-silent-rules \
 --with-blas=%{blaslib}%{?with_blas64:64}  \
%if %{with java}
 --with-java-includedir=%{_jvmdir}/java/include \
 --with-java-libdir=$libjvm \
%endif
 --with-qrupdate \
 --with-amd --with-umfpack --with-colamd --with-ccolamd --with-cholmod \
 --with-cxsparse

# Check that octave_api is set correctly (autogenerated file)
make liboctave/version.h
if ! grep -q '^#define OCTAVE_API_VERSION "%{octave_api}"' liboctave/version.h
then
  echo "octave_api variable in spec does not match liboctave/version.h"
  exit 1
fi

%make_build OCTAVE_RELEASE="Fedora %{version}%{?rctag}-%{release}"

%install
%make_install

# Docs - In case we didn't build them and to explicitly install pre-built docs
make install-data install-html install-info install-pdf DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_pkgdocdir}
cp -ar AUTHORS BUGS ChangeLog examples NEWS README %{buildroot}%{_pkgdocdir}/
cp -a doc/refcard/*.pdf %{buildroot}%{_pkgdocdir}/
%if !%{builddocs}
tar xvf %SOURCE3 -C %{buildroot}
%endif

find %{buildroot}%{_libdir} -name \*.la -delete

# No info directory
rm -f %{buildroot}%{_infodir}/dir

# Make library links
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/octave/%{version}%{?rctag}" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/octave-%{_arch}.conf

# Remove RPM_BUILD_ROOT from ls-R files
perl -pi -e "s,%{buildroot},," %{buildroot}%{_libdir}/%{name}/ls-R
perl -pi -e "s,%{buildroot},," %{buildroot}%{_datadir}/%{name}/ls-R
# Make sure ls-R exists
touch %{buildroot}%{_datadir}/%{name}/ls-R

desktop-file-validate %{buildroot}%{_datadir}/applications/org.octave.Octave.desktop
# RHEL9 appstream does not know url type
%{?el9:sed -i -e '/url type=/d' %{buildroot}/%{_datadir}/metainfo/org.octave.Octave.metainfo.xml}
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/org.octave.Octave.metainfo.xml

# Create directories for add-on packages
HOST_TYPE=`%{buildroot}%{_bindir}/octave-config -p CANONICAL_HOST_TYPE`
mkdir -p %{buildroot}%{_libdir}/%{name}/site/oct/%{octave_api}/$HOST_TYPE
mkdir -p %{buildroot}%{_libdir}/%{name}/site/oct/$HOST_TYPE
mkdir -p %{buildroot}%{_datadir}/%{name}/packages
mkdir -p %{buildroot}%{_libdir}/%{name}/packages
touch %{buildroot}%{_datadir}/%{name}/octave_packages

# Fix multilib installs
for include in octave-config defaults
do
   mv %{buildroot}%{_includedir}/%{name}-%{version}%{?rctag}/%{name}/${include}.h \
      %{buildroot}%{_includedir}/%{name}-%{version}%{?rctag}/%{name}/${include}-%{__isa_bits}.h
   cat > %{buildroot}%{_includedir}/%{name}-%{version}%{?rctag}/%{name}/${include}.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "${include}-32.h"
#elif __WORDSIZE == 64
#include "${include}-64.h"
#else
#error "Unknown word size"
#endif
EOF
done
for script in octave-config-%{version}%{?rctag} mkoctfile-%{version}%{?rctag}
do
   mv %{buildroot}%{_bindir}/${script} %{buildroot}%{_libdir}/%{name}/%{version}%{?rctag}/${script}
   cat > %{buildroot}%{_bindir}/${script} <<EOF
#!/bin/bash
ARCH=\$(uname -m)

case \$ARCH in
x86_64 | ia64 | s390x | aarch64 | ppc64 | ppc64le | riscv64) LIB_DIR=%{_libdir}
                       SECONDARY_LIB_DIR=%{_prefix}/lib
                       ;;
* )
                       LIB_DIR=%{_prefix}/lib
                       SECONDARY_LIB_DIR=%{_prefix}/lib64
                       ;;
esac

if [ ! -x \$LIB_DIR/%{name}/%{version}%{?rctag}/${script} ] ; then
  if [ ! -x \$SECONDARY_LIB_DIR/%{name}/%{version}%{?rctag}/${script} ] ; then
    echo "Error: \$LIB_DIR/%{name}/%{version}%{?rctag}/${script} not found"
    if [ -d \$SECONDARY_LIB_DIR ] ; then
      echo "   and \$SECONDARY_LIB_DIR/%{name}/%{version}%{?rctag}/${script} not found"
    fi
    exit 1
  fi
  LIB_DIR=\$SECONDARY_LIB_DIR
fi
exec \$LIB_DIR/%{name}/%{version}%{?rctag}/${script} "\$@"
EOF
   chmod +x %{buildroot}%{_bindir}/${script}
done
%if %{builddocs}
# remove timestamp from doc-cache
sed -i -e '/^# Created by Octave/d' %{buildroot}%{_datadir}/%{name}/%{version}%{?rctag}/etc/doc-cache
%else
cp -p doc/interpreter/macros.texi %{buildroot}%{_datadir}/%{name}/%{version}/etc/macros.texi
%endif

# rpm macros
mkdir -p %{buildroot}%{macrosdir}
cp -p %SOURCE1 %{buildroot}%{macrosdir}


%check
cp %SOURCE2 .
if [ -x /usr/libexec/Xorg ]; then
   Xorg=/usr/libexec/Xorg
else
   Xorg=/usr/libexec/Xorg.bin
fi
$Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xorg.log -config ./xorg.conf :99 &
sleep 2
export DISPLAY=:99
export FLEXIBLAS=netlib
%ifarch ppc64le riscv64
# liboctave/array/dMatrix.cc-tst segfaults
# riscv: image/getframe.m ...............................................LLVM ERROR: Relocation type not implemented yet!
make check || :
%else
make check
%endif

%ldconfig_scriptlets

%files
%license COPYING
%dir %{_pkgdocdir}
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/BUGS
%{_pkgdocdir}/ChangeLog
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/README
# FIXME: Create an -emacs package that has the emacs addon
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/octave-*.conf
%{_bindir}/octave*
%dir %{_libdir}/octave/
%dir %{_libdir}/octave/%{version}
%{_libdir}/octave/%{version}/liboctave.so.12*
%{_libdir}/octave/%{version}/liboctgui.so.13*
%{_libdir}/octave/%{version}/liboctinterp.so.13*
%{_libdir}/octave/%{version}/liboctmex.so.1*
%{_libdir}/octave/%{version}/mkoctfile-%{version}
%{_libdir}/octave/%{version}/oct/
%{_libdir}/octave/%{version}/octave-config-%{version}
%{_libdir}/octave/%{version}/site/
%{_libdir}/octave/packages/
%{_libdir}/octave/site/
%{_libexecdir}/octave/
%{_mandir}/man1/octave*.1.*
%{_infodir}/liboctave.info*
%{_infodir}/octave.info*
%{_datadir}/applications/org.octave.Octave.desktop
%{_datadir}/icons/hicolor/*/apps/octave.png
%{_datadir}/icons/hicolor/scalable/apps/octave.svg
%{_datadir}/metainfo/org.octave.Octave.metainfo.xml
# octave_packages is %ghost, so need to list everything else separately
%dir %{_datadir}/octave
%{_datadir}/octave/%{version}%{?rctag}/
%{_datadir}/octave/ls-R
%ghost %{_datadir}/octave/octave_packages
%{_datadir}/octave/packages/
%{_datadir}/octave/site/

%files devel
%{macrosdir}/macros.octave
%{_bindir}/mkoctfile
%{_bindir}/mkoctfile-%{version}%{?rctag}
%{_includedir}/octave-%{version}%{?rctag}/
%{_libdir}/octave/%{version}/liboctave.so
%{_libdir}/octave/%{version}/liboctgui.so
%{_libdir}/octave/%{version}/liboctinterp.so
%{_libdir}/octave/%{version}/liboctmex.so
%{_libdir}/pkgconfig/octave.pc
%{_libdir}/pkgconfig/octinterp.pc
%{_libdir}/pkgconfig/octmex.pc
%{_mandir}/man1/mkoctfile.1.*

%files doc
%{_pkgdocdir}/examples/
%{_pkgdocdir}/liboctave.html/
%{_pkgdocdir}/liboctave.pdf
%{_pkgdocdir}/octave.html
%{_pkgdocdir}/octave.pdf
%{_pkgdocdir}/refcard*.pdf

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 6:10.2.0-2
- Latest state for octave

* Thu Aug 07 2025 Orion Poplawski <orion@nwra.com> - 6:10.2.0-1
- Update to 10.2.0

* Thu Aug 07 2025 Orion Poplawski <orion@nwra.com> - 6:9.4.0-8
- Build with flexiblas on RHEL 9+

* Mon Jul 28 2025 Jiri Vanek <jvanek@redhat.com> - 6:9.4.0-7
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6:9.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu May 08 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 6:9.4.0-5
- Fix flatpak build

* Mon Apr 28 2025 Antonio Trande <sagitter@fedoraproject.org> - 6:9.4.0-4
- Rebuild for petsc-3.23.0

* Fri Feb 14 2025 Orion Poplawski <orion@nwra.com> - 6:9.4.0-2
- Rebuild with hdf5 1.14.6

* Fri Feb 07 2025 Orion Poplawski <orion@nwra.com> - 6:9.4.0-1
- Update to 9.4.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6:9.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 01 2025 Orion Poplawski <orion@nwra.com> - 6:9.3.0-1
- Update to 9.3.0

* Mon Nov 11 2024 Orion Poplawski <orion@nwra.com> - 6:9.2.0-1
- Update to 9.2.0
- Build with Qt6

* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 6:8.4.0-11
- Rebuild for hdf5 1.14.5

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 6:8.4.0-10
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6:8.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 01 2024 Antonio Trande <sagitter@fedoraproject.org> - 6:8.4.0-8
- Rebuild for sundials-6.7.0

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 6:8.4.0-7
- Rebuilt for java-21-openjdk as system jdk

* Mon Feb 26 2024 David Abdurachmanov <davidlt@rivosinc.com> - 6:8.4.0-6
- Add support for riscv64

* Sun Feb 04 2024 Orion Poplawski <orion@nwra.com> - 6:8.4.0-5
- Rebuild with suitesparse 7.6.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6:8.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6:8.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 20 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 6:8.4.0-2
- Rebuilt for sundials-6.6.2 (fix RHBZ#2249025)

* Tue Nov 07 2023 Orion Poplawski <orion@nwra.com> - 6:8.4.0-1
- Update to 8.4.0

* Mon Oct 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 6:8.3.0-2
- Rebuild for sundials-6.6.1

* Sun Aug 13 2023 Orion Poplawski <orion@nwra.com> - 6:8.3.0-1
- Update to 8.3.0

* Thu Aug 10 2023 Tom Callaway <spot@fedoraproject.org> - 6:8.2.0-4
- rebuild for new qhull

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6:8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 25 2023 Orion Poplawski <orion@nwra.com> - 6:8.2.0-2
- Rebuild for sundials 6.5.1

* Mon Apr 17 2023 Orion Poplawski <orion@nwra.com> - 6:8.2.0-1
- Update to 8.2.0

* Sat Apr 08 2023 Orion Poplawski <orion@nwra.com> - 6:8.1.0-1
- Update to 8.1.0
- Build with pcre2 (bz#2128340)

* Fri Mar 17 2023 Orion Poplawski <orion@nwra.com> - 6:7.3.0-4
- Add upstream patch to fix doc builds

* Sun Feb 26 2023 Orion Poplawski <orion@nwra.com> - 6:7.3.0-3
- Disable building docs due to texinfo 7 incompatibility

* Fri Feb 10 2023 FeRD (Frank Dana> <ferdnyc@gmail.com> - 6:7.3.0-3
- Build with rapidjson to enable built-in json{decode,encode}

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6:7.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Orion Poplawski <orion@nwra.com> - 6:7.3.0-1
- Update to 7.3.0

* Sun Oct 02 2022 Orion Poplawski <orion@nwra.com> - 6:7.2.0-2
- Disable qscintilla and sundials support on EPEL9 for now (bz#2122390)

* Tue Aug 02 2022 Orion Poplawski <orion@nwra.com> - 6:7.2.0-1
- Update to 7.2.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6:7.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Orion Poplawski <orion@nwra.com> - 6:7.1.0-2
- Drop java for i686 (bz#2104081)

* Thu Apr 07 2022 Orion Poplawski <orion@nwra.com> - 6:7.1.0-1
- Update to 7.1.0

* Mon Feb 07 2022 Orion Poplawski <orion@nwra.com> - 6:6.4.0-5
- Update gnulib cdefs.h for gcc12 support on ppc64le

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 6:6.4.0-4
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6:6.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 6:6.4.0-2
- Rebuild for hdf5 1.12.1

* Wed Nov 03 2021 Orion Poplawski <orion@nwra.com> - 6:6.4.0-1
- Update to 6.4.0

* Wed Oct 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 6:6.3.0-2
- Rebuild for sundials-5.8.0

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 6:6.3.0-1
- Update to 6.3.0

* Mon Aug 09 2021 Orion Poplawski <orion@nwra.com> - 6:6.2.0-1
- Update to 6.2.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6:5.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 30 2021 Orion Poplawski <orion@nwra.com> - 6:5.2.0-13
- Use brp-strip instead of brp-strip-shared (bz#1955380)

* Tue Apr 06 2021 Orion Poplawski <orion@nwra.com> - 6:5.2.0-12
- Backport readline 8.1 support (bz#1946773)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6:5.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Orion Poplawski <orion@nwra.com> - 6:5.2.0-10
- Rebuild for sundials 5.6.1

* Sun Nov 22 2020 Orion Poplawski <orion@nwra.com> - 6:5.2.0-9
- Rebuild for sundials 5.5.0

* Mon Oct 05 2020 Orion Poplawski <orion@nwra.com> - 6:5.2.0-8
- Rebuild for sundials 5.4.0

* Thu Aug 13 2020 Iñaki Úcar <iucar@fedoraproject.org> - 5.2.0-7
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Tue Jul 28 2020 Adam Jackson <ajax@redhat.com> - 5.2.0-6
- Drop unnecessary (apparently unused) BuildRequires: xorg-x11-apps

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6:5.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 6:5.2.0-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 6:5.2.0-3
- Rebuild for hdf5 1.10.6

* Mon Apr 13 2020 Orion Poplawski <orion@nwra.com> - 6:5.2.0-2
- Rebuild for sundials 5.2.0

* Mon Feb 03 2020 Orion Poplawski <orion@nwra.com> - 6:5.2.0-1
- Update to 5.2.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6:5.1.0-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov  2 2019 Orion Poplawski <orion@nwra.com> - 6:5.1.0-4
- Enable 64-bit array indexes

* Sat Nov  2 2019 Orion Poplawski <orion@nwra.com> - 6:5.1.0-3
- Enable LTO optimisations

* Mon Oct 14 2019 Orion Poplawski <orion@nwra.com> - 6:5.1.0-2.1
- Rebuild for suitesparse 5.4.0

* Wed Jul 31 2019 Orion Poplawski <orion@nwra.com> - 6:5.1.0-2
- Drop use of %%buildarch in macros.octave (bugz#1733898)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6:5.1.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 16 2019 Orion Poplawski <orion@nwra.com> - 6:5.1.0-1
- Update to 5.1.0

* Mon May  6 2019 Orion Poplawski <orion@nwra.com> - 6:4.4.1-8
- Backport upstream patch for proper EOF handling (bugz#1705129)

* Tue Apr 23 2019 Björn Esser <besser82@fedoraproject.org> - 6:4.4.1-7
- rebuilt (sundials)

* Sat Mar 16 2019 Orion Poplawski <orion@nwra.com> - 6:4.4.1-6
- Rebuild for hdf5 1.10.5

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 6:4.4.1-5
- Remove obsolete requirements for post/preun scriptlets

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6:4.4.1-4
- Rebuild for readline 8.0

* Sat Feb 16 2019 Björn Esser <besser82@fedoraproject.org> - 6:4.4.1-3
- rebuilt (qscintilla)

* Tue Feb 12 2019 Björn Esser <besser82@fedoraproject.org> - 6:4.4.1-2
- rebuilt (qscintilla)
- Fix pre-release tag

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6:4.4.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 11 2018 Orion Poplawski <orion@nwra.com> - 6:4.4.1-1
- Update to 4.4.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6:4.2.2-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Colin B. Macdonald <cbm@m.fsf.org> - 6:4.2.2-6
- macros: support other names for appdata .metainfo.xml files

* Thu Jun 28 2018 Colin B. Macdonald <cbm@m.fsf.org> - 6:4.2.2-5
- macros: support dependencies in octave_pkg_check

* Thu Jun 21 2018 Orion Poplawski <orion@nwra.com> - 6:4.2.2-4
- Add patch to fix crash with Ctrl-D (bug #1589460)

* Sun Jun 17 2018 Orion Poplawski <orion@nwra.com> - 6:4.2.2-3
- Add requires hicolor-icon-theme
- Use make macros

* Sat Jun  2 2018 Jerry James <loganjerry@gmail.com> - 6:4.2.2-2
- Rebuild for glpk 4.65
- Use ldconfig macros
- Add -qbuttongroup patch to fix FTBFS

* Wed Mar 14 2018 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.2-1
- Update to 4.2.2
- Fail build again if make check fails

* Wed Feb 21 2018 Orion Poplawski <orion@nwra.com> - 6:4.2.1-5
- Add BR gcc-c++

* Thu Feb 08 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6:4.2.1-4.5
- Rebuild for hdf5 1.8.20

* Mon Feb 05 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6:4.2.1-4.4
- Rebuild for new gfortran

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6:4.2.1-4.3
- Remove obsolete scriptlets

* Sun Aug 13 2017 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.1-4.2
- Make octave-devel require libappstream-glib

* Sat Aug 12 2017 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.1-4.1
- Run appstream-util validate-relax on metainfo.xml files

* Fri Aug 11 2017 Orion Poplawski <orion@nwra.com> - 6:4.2.1-4
- Use openblas on Fedora 27+

* Thu Aug 10 2017 Orion Poplawski <orion@nwra.com> - 6:4.2.1-4
- Install metainfo.xml files in %%octave_pkg_install

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6:4.2.1-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6:4.2.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.1-3
- Use Qt5 on Fedora 26+

* Wed Apr  5 2017 Jerry James <loganjerry@gmail.com> - 6:4.2.1-2
- Rebuild for glpk 4.61

* Fri Feb 24 2017 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.1-1
- Update to 4.2.1

* Mon Feb 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 6:4.2.0-16
- rebuild (qscintilla)

* Wed Feb 08 2017 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-15
- Have %%octave_pkg_check re-strip shared objects

* Tue Feb 07 2017 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-14
- Rebuild with fixed pkgconf (bug #1419685)

* Sat Jan 28 2017 Björn Esser <besser82@fedoraproject.org> - 6:4.2.0-13
- Rebuilt for GCC-7

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 6:4.2.0-12.1
- Rebuild for readline 7.x

* Thu Dec 29 2016 Kalev Lember <klember@redhat.com> - 6:4.2.0-12
- Fix license in appdata file (bug #1293561)

* Fri Dec 09 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-11
- Handle noarch package tarball names

* Fri Dec 09 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-10
- Patch gzip from upstream bug report

* Thu Dec 08 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-9
- Disable more segfaulting tests

* Thu Dec 08 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-8
- Add patch to prevent gzip from deleting target file, instead emit warning
- Drop debug code
- Disable segfaulting osmesa_print and pltopt tests

* Thu Dec 08 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-7
- Fix version option

* Wed Dec 07 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-6
- A desparate attempt to debug octave package building

* Wed Dec 07 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-5
- Build in a build sub-directory

* Wed Dec 07 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-4
- Use 'octave-config -p CANONICAL_HOST_TYPE' in macros

* Wed Dec 07 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-3
- Use %%_host in macros

* Tue Dec 06 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-2
- Rework pkg build/install macros

* Tue Dec 06 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.2.0-1
- Update to 4.2.0
- Drop texinfo5 patch
- Use autoreconf -i
- Add requires for latex packages
- Add implicit patch

* Tue Dec 06 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.3-3
- Rebuild for hdf5 1.8.18

* Fri Sep 9 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.3-2
- Add upstream patch to fix build with texinfo 5 on <=EL7

* Sun Jul 3 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.3-1
- Update to 4.0.3

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.2-3
- Rebuild for hdf5 1.8.17

* Fri Apr 29 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 6:4.0.2-2
- Rebuild for qhull-2015.2-1.

* Thu Apr 21 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.2-1
- Update to 4.0.2

* Sun Apr 10 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.1-6
- Add upstream patch to fix setting TERM variable (bug #1325548)

* Mon Apr 4 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.1-5
- Arm tests appear to be running okay now (bug #1149953)

* Thu Mar 24 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.1-4
- Swap quoting in octave macros to make set -x output a little cleaner
- Stop trying to turn octave warnings off in macros

* Wed Mar 23 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.1-3
- Update signbit patch from gnulib upstream to work with older compilers
- Only munge headers for gnulib on Fedora 24+

* Tue Mar 22 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.1-2
- libappstream-glib is not in EL6

* Tue Mar 22 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.1-1
- Update to 4.0.1
- Drop upstream texinfo patch

* Fri Mar 11 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-14
- Rebuild for glpk 4.59

* Sun Feb 21 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-13
- Fix build with gcc 6

* Thu Feb 18 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-12
- Rebuild for glpk 4.58

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6:4.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-10
- Rebuild for poppler-0.40.0

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-9
- Rebuild for hdf5 1.8.16

* Tue Dec 29 2015 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-8
- Validate and fix appdata file (bug #1293561)

* Wed Nov 11 2015 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-7
- Add BR libsndfile-devel and portaudio-devel for audio support (bug #1279924)

* Tue Oct 6 2015 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-6
- Remove unused fftpack code, note bundled libraries

* Sun Oct 04 2015 Rex Dieter <rdieter@fedoraproject.org> - 6:4.0.0-5
- rebuild (GraphicsMagick)

* Fri Jul 31 2015 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-4
- Add octave_pkg_check rpm macro, other macro cleanup

* Tue Jul 14 2015 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-3
- Add patch to fix build with texinfo 6.0

* Mon Jul 13 2015 Dan Horák <dan[at]danny.cz> - 6:4.0.0-2
- build without the dummy Xorg driver on s390(x)

* Mon Jul 6 2015 Orion Poplawski <orion@cora.nwra.com> - 6:4.0.0-1
- Update to 4.0.0
- Rebase pkgbuilddir patch
- Drop suitesparse patch
- Run X server for tests

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.8.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Nils Philippsen <nils@redhat.com> - 6:3.8.2-19
- rebuild for suitesparse-4.4.4

* Thu May 28 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-18
- Fix doc install (bug #799662)

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-17
- Rebuild for hdf5 1.8.15

* Mon Apr 20 2015 Rex Dieter <rdieter@fedoraproject.org> - 6:3.8.2-16
- rebuild (qscintilla)

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 6:3.8.2-15
- Add an AppData file for the software center

* Tue Mar 10 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-14
- Build with --enable-float-truncate (https://savannah.gnu.org/bugs/?40560)
- Re-enable parallel builds

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 6:3.8.2-13
- rebuild (GraphicsMagick)

* Fri Feb 20 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-12
- Rebuild for rebuilt swig

* Wed Feb 18 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-11
- Rebuild for fltk 1.3.3

* Tue Feb 17 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-10
- Rebuild for gcc 5 C++11 ABI

* Sun Feb 08 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-9
- Use a generic location for libjvm.so, require java-headless (bug #1190523)

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-8
- Rebuild for hdf5 1.8.14

* Mon Oct 6 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-7
- Disable test failure on arm for now (bug #1149953)

* Mon Sep 15 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-6
- Add patch for suitesparse 4.3.1 support

* Fri Sep 12 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-5
- Rebuild for libcholmod soname bump

* Sat Aug 23 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-4
- No info scripts when not building docs

* Fri Aug 22 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-3
- Install macros.texi by hand if not building docs

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.2-1
- Update to 3.8.2 final

* Thu Jul 03 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 6:3.8.2-0.2.rc2
- Modernize rest of specfile.
- Update to 3.8.2-rc2.

* Tue Jun 10 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 6:3.8.2-0.1.rc1
- Update to 3.8.2-rc1.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar  7 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 6:3.8.1-1
- Update to 3.8.1.

* Sat Feb  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 6:3.8.0-6
- Add PPC64 and aarch64 to the 64 bit architectures

* Sat Feb 1 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-5
- Fix rpm macro install location

* Tue Jan 14 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-4
- Also fix base-list.h include

* Thu Jan 9 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-3
- Really fix config.h include

* Wed Jan 8 2014 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-2
- Fix config.h include

* Sat Dec 28 2013 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-1
- Update to 3.8.0 final

* Sat Dec 28 2013 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-0.4.rc2
- Rebase pkgbuilddir patch

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-0.3.rc2
- Rebuild for hdf5 1.8.12

* Sat Dec 21 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 6:3.8.0-0.2.rc2
- Update to 3.8.0-rc2.

* Fri Dec 6 2013 Orion Poplawski <orion@cora.nwra.com> - 6:3.8.0-0.1.rc1
- Update to 3.8.0-rc1
- Drop patches
- Add BR gl2ps-devel, qscintilla-devel, java-devel, llvm-devel

* Fri Dec 06 2013 Nils Philippsen <nils@redhat.com> - 6:3.6.4-9
- rebuild (suitesparse)

* Thu Oct 3 2013 Orion Poplawski - 6:3.6.4-8
- Re-enable atlas on arm

* Sun Sep 22 2013 Orion Poplawski - 6:3.6.4-7
- Rebuild for atlas 3.10
- Disable atlas on arm

* Thu Sep 12 2013 Dan Horák <dan[at]danny.cz> - 6:3.6.4-6
- Rebuilt to resolve broken deps on s390(x)

* Tue Jul 30 2013 Orion Poplawski <orion@cora.nwra.com> - 6:3.6.4-5
- Rebuild for glpk 4.52.1

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 6:3.6.4-4
- Rebuild for hdf5 1.8.11

* Thu Mar 28 2013 Jaromir Capik <jcapik@redhat.com> - 6:3.6.4-3
- aarch64 support (#926264)

* Fri Mar 08 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 6:3.6.4-2
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Sat Feb 23 2013 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.4-1
- Update to 3.6.4 final

* Tue Feb 12 2013 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.4-0.7.rc2
- Update to 3.6.4-rc2

* Tue Feb 12 2013 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.4-0.6.rc1
- Drop vendor from desktop file

* Sun Feb 03 2013 Kevin Fenzi <kevin@scrye.com> - 6:3.6.4-0.5.rc1
- Rebuild for broken deps in rawhide

* Fri Jan 4 2013 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.4-0.4.rc1
- Update to 3.6.4-rc1
- Drop gets patch

* Fri Dec 21 2012 Orion Poplawski <orion@cora.nwra.com> - 6:3.6.4-0.3.rc0
- Add patch to ignore deps when building packages for now (bug 733615)

* Wed Dec 05 2012 Orion Poplawski <orion@cora.nwra.com> - 6:3.6.4-0.2.rc0
- Restore gets patch
- Rebuild for hdf5 1.8.10

* Wed Oct 17 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.4-0.1.rc0
- Update to 3.6.4-rc0
- Drop sparse patch applied upstream

* Thu Sep 6 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.3-2
- Add upstream patch to fix sparse matrix test crash

* Wed Sep 5 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.3-1
- Update to 3.6.3
- Drop gets patch fixed upstream

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 5 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.6.2-2
- Build against OpenGL libraries.

* Mon Jun 4 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.2-1
- Update to 3.6.2 final

* Thu May 24 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.2-0.4.rc2
- Update to 3.6.2-rc2
- Add patch to update gnulib to handle gets removal

* Tue May 15 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.2-0.3.rc0
- Rebuild with hdf5 1.8.9

* Tue May 15 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.2-0.2.rc0
- Add Provides bundled(gnulib) (bug 821781)

* Sat May 12 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.2-0.1.rc0
- Update to 3.6.2-rc0.

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.6.1-2
- Rebuilt for c++ ABI breakage

* Wed Feb 22 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.1-1
- Update to 3.6.1.

* Thu Feb 9 2012 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.6.0-2
- Rebuild with pcre 8.30

* Sun Jan 15 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.6.0-1
- Update to 3.6.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.3-2
- Rebuild for hdf5 1.8.8

* Mon Oct 24 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.3-1
- Update to 3.4.3
- Drop upstreamed patches

* Wed Aug 24 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.4.2-3
- Place rpm macros in -devel.

* Thu Aug 11 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.2-2
- Drop smp build - seems to be failing
- Add patch to fix tar argument handling
- Add patch to fix xzip

* Sat Aug 06 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.4.2-1
- Update to 3.4.2.

* Fri May 27 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.0-8
- Add patch to fix Fl_File_Chooser.H location
- Add BR tex(dvips)

* Thu May 26 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.0-7
- Rebuild for fltk 1.3.0

* Tue May 17 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.0-6
- Rebuild for hdf5 1.8.7

* Fri Mar 18 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.0-5
- Use libdir instead of libexecdir
- Rename octave_pkg_preun macro
- Fix multilib installs
- Re-enable prelinking, seems to work
- Add patch to enable building packages from directories

* Wed Feb 23 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.0-4
- Update rpm macros per FPC comments

* Mon Feb 14 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.0-3
- Add rpm macros
- Rebuild should pick up fixed suitesparse
- Disable parallel builds

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 8 2011 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.4.0-1
- Update to 3.4.0
- Drop run-octave patch fixed upstream
- Add patch to support gcc 4.6

* Thu Dec 16 2010 Orion Poplawski <orion[AT]cora.nwra com> - 6:3.3.54-1
- Update to 3.3.54
- Add patch to prevent run-octave from getting installed
- Drop -DH5_USE_16_API
- Enable parallel builds
- Cleanup doc instal

* Sun Feb 28 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.2.4-3
- Temporarily disable %%check to enable build to complete and ensure
  upgrade path works.  This works around a crash in the imread.m image test
  script, this may be the same problem as described by upstream here:
  https://www-old.cae.wisc.edu/pipermail/octave-maintainers/2010-January/014891.html

* Fri Feb 26 2010 Michal Schmidt <mschmidt@redhat.com> 6:3.2.4-2
- Fix the prelink workaround to work with any version.
- Use _sysconfdir macro instead of /etc.

* Thu Jan 28 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.2.4-1
- Update to 3.2.4 with a few rpmlint fixes.

* Sun Jan 17 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.2.3-4
- Fix compilation against ARPACK.

* Wed Jan 6 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.2.3-3
- Really build against ATLAS instead of reference BLAS (#513381).

* Sun Nov 15 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.2.3-2
- Workaround broken pre-linking (#524493)

* Tue Sep 29 2009 Orion Poplawski <orion@cora.nwra.com> - 6:3.2.3-1
- Update to 3.2.3
- Re-add make check

* Tue Sep 22 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 6:3.2.2-5
- Added categories to desktop file: Education, DataVisualization, NumericalAnalysis

* Mon Sep  7 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.2.2-4
- Rebuild against new ATLAS

* Sun Sep  6 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.2.2-3
- Disable make check temporarily to get a build against newly fixed lapack

* Wed Sep 2 2009 Orion Poplawski <orion@cora.nwra.com> - 6:3.2.2-2
- Add make check

* Fri Jul 31 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.2.2-1
- Update to latest upstream (3.2.2).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.2.0-2
- Added BR: ftgl-devel for native graphics.
- Dropped obsolete X-Fedora category from desktop file.
- Macro use unifications.
- Branch documentation into its own subpackage.

* Sat Jul 11 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 6:3.2.0-1
- Update to latest upstream (3.2.0).

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 6:3.0.5-1
- Updated to latest upstream (3.0.5)

* Mon Feb 23 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.3-2
- Add patches from upstream for compiling against GCC 4.4
  http://hg.savannah.gnu.org/hgweb/octave/rev/93cf10950334
  http://hg.tw-math.de/release-3-0-x/rev/712d9e045b1e

* Wed Dec 10 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.3-1
- Update to latest upstream (3.0.3)

* Thu Oct 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 6:3.0.2-2
- patch for sh arch: it adds '-little' flag

* Mon Sep 8 2008 Orion Poplawski <orion@cora.nwra.com> 6:3.0.2-1
- Update to 3.0.2

* Mon Apr 21 2008 Quentin Spencer <qspencer@users.sf.net> 6:3.0.1-1
- New release of octave. Remove gcc 4.3 patch.

* Mon Mar  3 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.0-6
- Re-enable patch, but change cstring -> string.h so it works for C as
  well as C++.  Hopefully this will #435600 for real.

* Sun Mar  2 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.0-5
- Backout GCC 4.3 patch temporarily, causes trouble for octave-forge and
  may not be necessary (#435600)

* Fri Feb 29 2008 Orion Poplawski <orion@cora.nwra.com> 3.0.0-4
- Rebuild for hdf5 1.8.0 using compatability API define
- Add gcc43 patch

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6:3.0.0-3
- Autorebuild for GCC 4.3

* Wed Jan  9 2008 Quentin Spencer <qspencer@users.sf.net> 3.0.0-2
- Add curl-devel and pcre-devel as build dependencies. Closes bug 302231.

* Fri Dec 21 2007 Quentin Spencer <qspencer@users.sf.net> 3.0.0-1
- Update to 3.0.0.

* Wed Dec 12 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.19-1
- Update to 2.9.19 and update octave_api.

* Wed Dec  5 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.18-1
- Update to 2.9.18 and update octave_api.

* Wed Nov 28 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.17-1
- Update to 2.9.17 and update octave_api.

* Mon Nov  5 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.16-1
- Update to 2.9.16, remove old patch.
- Update licencse from GPLv2+ to GPLv3+.
- Detection of glpk no longer needs special CPPFLAGS.

* Tue Oct 16 2007 Orion Poplawski <orion@ora.nwra.com> 2.9.15-2
- Updated pkg.m patch

* Mon Oct 15 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.15-1
- New release. Remove old patch.

* Tue Sep 25 2007 Orion Poplawski <orion@ora.nwra.com> 2.9.14-2
- Add /usr/share/octave/packages for add on packages and %%ghost
  /usr/share/octave/octave_packages
- Add patch for octave package manager that will be going upstream

* Tue Sep 18 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.14-1
- New release.
- Remove redundant menu category in desktop file (bug 274431).
- Update license tag.
- Add qhull-devel as new build dependency.

* Thu Jul 26 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.13-1
- New release.
- Changed ufsparse-devel dependency to suitesparse-devel.
- Add configure flag to close bug 245562.
- Add directories for add-on packages (bug 234012).
- Since texinfo is now separate from tetex, it is a build requirement.

* Wed May 23 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.12-1
- New release.

* Tue Feb 20 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.9-2
- Fix install-info bug (Bug 219404).
- Add dependency on octave API so that breakages will be detected. (Bug 224050).
- Remove libtermcap-devel as build dependency (Bug 226768).

* Tue Oct 03 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.9-1
- New release. Remove old patch.

* Fri Sep 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.8-2
- Fix this bug:
  https://www.cae.wisc.edu/pipermail/bug-octave/2006-September/000687.html

* Fri Aug 25 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.8-1
- New release. Remove old patch. This fixes bug #203676.

* Tue Aug 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.7-3
- Add ghostscript as a build dependency.

* Tue Aug 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.7-2
- Update patch to fix several small bugs, including #201087.

* Fri Jul 28 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.7-1
- New release. Remove old patches and add one new one.

* Tue Jul 11 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.6-2
- Patch for some erroneous warnings and a file path bug.

* Mon Jul 10 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.6-1
- New release. Remove old patches.
- Disable 64-bit extensions (some libraries don't support 64-bit indexing yet).
- Add gcc-gfortran to -devel dependencies (mkoctfile fails without it).
- Move octave-bug and octave-config from devel to main package.
- Fix categorization of info files (bug 196760).

* Thu Apr 27 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-6
- Add patch for bug #190481
- Manual stripping of .oct files is no longer necessary.

* Wed Apr 19 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-5
- Add new patch to configure script (breaks octave-forge without it).

* Fri Mar 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-4
- Change patch again (suggested by the author on Octave mailing list).

* Fri Mar 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-3
- Fix broken patch.

* Fri Mar 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-2
- Add more changes to sparse patch.

* Thu Mar 23 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-1
- New upstream release; remove old patches; add sparse patch.
- Add gcc-c++ as dependency for devel package.
- Add more docs; cleanup extra files in docs.
- Simplify configure command.
- Install desktop file.

* Fri Feb 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-8
- Rebuild for new hdf5.
- Remove obsolete configure options.
- Make sure /usr/libexec/octave is owned by octave.

* Wed Feb 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-7
- Rebuild for Fedora Extras 5.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-6
- Change dependency from fftw3 to fftw.

* Thu Jan 26 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-5
- Rebuild for new release of hdf5.

* Mon Dec 19 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-4
- Rebuild for gcc 4.1.

* Thu Dec  1 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-3
- Make sure patch applies correctly before building!

* Thu Dec  1 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-2
- Patch to enable compilation on x86_64.

* Fri Nov 11 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-1
- New upstream release.
- Patch to make sure all headers are included in -devel.
- PKG_ADD file now needs %%{buildroot} stripped from it.
- Cleanup errors in dependencies.

* Tue Oct 25 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-6
- Add lapack-devel and blas-devel dependencies to devel package.

* Mon Oct 03 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-5
- Change umfpack-devel dependency to the new ufsparse-devel package.

* Thu Sep 22 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-5
- Change lapack and blas dependencies to lapack-devel and blas-devel

* Mon Aug 08 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-4
- Cleanup: remove redefinition of __libtoolize, ExcludeArch of two platforms,
  old s390 workarounds, and LC_ALL setting. None of these appear to be
  necessary any longer, even if the platforms were supported.
- Add --enable-64 to configure to enable 64-bit array indexing on x86_64.
- Add support for GLPK (new build dependency and CPPFLAGS for configure).

* Wed Jul 27 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-3
- Add fftw3-devel to dependencies for devel

* Tue Jul 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-2
- Add dependencies (hdf5-devel and zlib-devel) for devel

* Tue Jul 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-1
- Move to new 2.9.x development tree.
- Add umfpack-devel as new build dependency.

* Tue Jul 05 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-12
- Require hdf5-devel for build.

* Wed Jun 22 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-11
- Force octave-devel to require readline-devel.
- Add _libdir to configure command (fixes broken mkoctfile on x86_64).

* Tue Jun 21 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-10
- Add epoch to BuildRequires in octave-devel.

* Mon Jun 20 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-9
- Rebuild.

* Sat Jun 18 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-8
- Force octave-devel to require octave.

* Wed Jun  8 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-7
- Fix configure command again. The prefix isn't used for the install step
  but it is used to calculate internal variables in octave.

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 2.1.71-6
- disable explicit gcc-c++/libstdc++-devel BR and bump for another
  rebuild attempt

* Wed Jun  1 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-4
- Fix configure command. Remove irrelevant files from docs.

* Fri May 27 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-3
- Added patch for http://www.octave.org/mailing-lists/bug-octave/2005/617

* Thu May 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-2
- Added dist tag.

* Fri May 20 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-1
- Imported 2.1.71 from upstream, removed 2.1.70 patches (in upstream).
- Begin cleanup of spec file, including the big configure command
  (some options are obsolete, others appear unneeded if rpm configure
  macro is used).

* Tue May 03 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.70-1
- Imported 2.1.70 from upstream, removed old patches (resolved in new version)
- Changed g77 dependency to gfortran.
- Added fftw3 to BuildRequires.
- Added patches (from maintainer) to fix build problems.

* Wed Feb 23 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-13
- fix typo in spec 149420

* Mon Feb 21 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-12
- Fix problem with symlinks using ldconfig (bug 147922)

* Wed Feb 16 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-11
- add $RPM_OPT_FLAGS

* Tue Feb 15 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-10
- Fix bug 142477 - problem with signbit definition (Patch2)

* Wed Jan 19 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-9
- Fix bug #142440 - change octave.spec: autoconf is BuildPrereq
- Fix bug #142631 - change octave.spec: mkoctfile.1.gz is part of octave-devel not octave

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.1.57-8
- Rebuilt for new readline.

* Mon Oct 18 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-7
- Don't forget default attributes for -devel package

* Mon Oct 18 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-6
- Remove old lib/lib64 badness.

* Wed Oct 13 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-5
- Split into octave and octave-devel

* Thu Jun 24 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-4
- Remove RPM_BUILD_ROOT from preun section (#119112)

* Thu Jun 24 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-3
- Er, typo in patch (thanks Nils)

* Thu Jun 24 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-2
- Fix for #113852 - signbit broken

* Tue Jun 15 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-1
- Import 2.1.57 from upstream; this fixes #126074

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 30 2004 Karsten Hopp <karsten@redhat.de> 2.1.50-9
- remove builddir references from file list (#119112)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-7
- Add requirement for texinfo. #101299, round 3!

* Tue Sep 09 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-6
- Disable s390x again

* Tue Sep 09 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-5
- Disable ppc64

* Tue Sep 09 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-4
- Rebuild for Taroon

* Wed Jul 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-3
- Fix for Bugzilla #101299, round 2.  Include a patch to
quell sterr from info; it gives us funny messages if $HOME/.info
does not exist.

* Wed Jul 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-2
- Fix for Bugzilla #101299

* Mon Jun 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-1
- Import 2.1.50 from upstream
- Fix for Bugzilla #100682; try ppc64 again

* Mon Jun 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.49-6
- Rebuild; disabling ppc64

* Mon Jun 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.49-4
- Added link generation to /usr/lib so that munging
/etc/ld.so.conf isn't required to get octave to work.
(#98226)

* Thu Jun 05 2003 Lon Hohberger <lhh@redhat.com> 2.1.49-2
- Import from upstream; rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 16 2003 Lon Hohberger <lhh@redhat.com> 2.1.46-2
- Rebuilt

* Tue Apr 15 2003 Lon Hohberger <lhh@redhat.com> 2.1.46-1
- Import from upstream: 2.1.46.  Disabled s390x.

* Mon Mar 10 2003 Lon Hohberger <lhh@redhat.com> 2.1.40-5
- Enabled s390[x]

* Fri Feb 7 2003 Lon Hohberger <lhh@redhat.com> 2.1.40-4
- Disabled s390 and s390x builds for now.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 2 2003 Lon Hohberger <lhh@redhat.com> 2.1.40-2
- Fixed readline-devel build-rereq line. (#80673)

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> 2.1.40-1
- update to 2.1.40, fix matrix plotting (#77906).

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 2.1.39-2
- build on x86_64.

* Sun Nov 10 2002 Jeff Johnson <jbj@redhat.com> 2.1.39-1
- update to 2.1.39.

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Aug  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-7
- Rebuild

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-6
- Rebuild

* Thu Jul 11 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Rebuild with new readline

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-3
- Get rid of 0 size doc files (#66116)

* Thu May 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-2
- Rebuild
- Patch C++ code gcc changed its opinion of the last 3 weeks

* Wed May  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-1
- 2.1.36
- Disable patch

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.35-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 27 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.1.35-2
- Add patch for kpathsea to avoid segfaults

* Tue Nov  6 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.1.35-1
- 2.1.35
- s/Copyright/License/

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Wed Jun 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add more dependencies in BuildPrereq (#45184)

* Fri Jun 08 2001 Trond Eivind Glomsrød <teg@redhat.com>
- No longer exclude ia64

* Mon Apr 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.34

* Tue Mar 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- set LC_ALL to POSIX before building, otherwise the generated paths.h is bad

* Wed Jan 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.33

* Mon Jan 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require compat-egcs-c++, but gcc-c++
- add some libtoolize calls to add newest versions

* Fri Dec 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.32, no longer use CVS as our needed fixes are in now
- add Prereq for info

* Thu Dec 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use a development version, as they have now been fixed
  to compile with the our current toolchain.

* Thu Aug 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.0.16, with compat C++ compiler and new C and f77 compilers
  The C++ code is too broken for our new toolchain (C++ reserved
  words used as enums and function names, arcane macros), but
  plotting works here and not in the beta (#16759)
- add epoch to upgrade the betas

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- make sure #line commands are not output within macro arguments

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.31

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- no longer disable optimizations, sparc excepted

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Mon Jul  3 2000 Matt Wilson <msw@redhat.com>
- added missing %% before {_infodir} in the %%post

* Fri Jun 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.30 - the old version contains invalid C++ code
  accepted by older compilers.

* Fri Jun 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable optimization for C++ code

* Thu Jun 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add "Excludearch: " for Alpha - it triggers compiler bugs

* Thu Jun 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%configure, %%makeinstall, %%{_infodir}. %%{_mandir}
- remove prefix

* Tue May 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- upgraded to 2.0.16
- removed "--enable-g77" from the configure flags - let autoconf find it

* Thu Jan 20 2000 Tim Powers <timp@redhat.com>
- bzipped source to conserve space.

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- update to 2.0.15.

* Tue Jul 20 1999 Tim Powers <timp@redhat.com>
- rebuit for 6.1

* Wed Apr 28 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.0.14.

* Fri Oct 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.0.13.90

* Thu Jul  9 1998 Jeff Johnson <jbj@redhat.com>
- repackage in powertools.

* Thu Jun 11 1998 Andrew Veliath <andrewtv@usa.net>
- Add %%attr, build as user.

* Mon Jun 1 1998 Andrew Veliath <andrewtv@usa.net>
- Add BuildRoot, installinfo, require gnuplot, description from
  Octave's web page, update to Octave 2.0.13.
- Adapt from existing spec file.

* Tue Dec  2 1997 Otto Hammersmith <otto@redhat.com>
- removed libreadline stuff from the file list

* Mon Nov 24 1997 Otto Hammersmith <otto@redhat.com>
- changed configure command to put things in $RPM_ARCH-rehat-linux,
  rather than genereated one... was causing problems between building
  on i686 build machine.

* Mon Nov 17 1997 Otto Hammersmith <otto@redhat.com>
- moved buildroot from /tmp to /var/tmp

* Mon Sep 22 1997 Mike Wangsmo <wanger@redhat.com>
- Upgraded to version 2.0.9 and built for glibc system

* Thu May 01 1997 Michael Fulbright <msf@redhat.com>
- Updated to version 2.0.5 and changed to build using a BuildRoot

## END: Generated by rpmautospec
