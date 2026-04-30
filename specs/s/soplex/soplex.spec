## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Architectures that have libquadmath
%ifarch %{x86_64} %{power64}
%global quadmath 1
%else
%global quadmath 0
%endif

Name:           soplex
Version:        7.1.6
Release:        %autorelease
Summary:        Sequential object-oriented simplex

%global upver   %(sed 's/\\.//g' <<< %{version})
%global giturl  https://github.com/scipopt/soplex

# Apache-2.0: the project as a whole
# LGPL-2.1-or-later: src/soplex/gzstream.{cpp,h}
# MIT: the bundled fmt project
License:        Apache-2.0 AND LGPL-2.1-or-later AND MIT
URL:            https://soplex.zib.de/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/release-%{upver}.tar.gz
# Elevate the shared library from second-class status to first-class
Patch:          %{name}-shared.patch
# Unbundle zstr
Patch:          %{name}-unbundle-zstr.patch

# See https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  cmake(papilo)
BuildRequires:  cmake(tbb)
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
%if %{quadmath}
BuildRequires:  libquadmath-devel
%endif
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(gmp)
BuildRequires:  pkgconfig(mpfr)
BuildRequires:  zstr-static

# Documentation
BuildRequires:  doxygen
BuildRequires:  php-cli
BuildRequires:  python3

Requires:       libsoplex%{?_isa} = %{version}-%{release}

%global _desc %{expand:
SoPlex is an optimization package for solving linear programming problems
(LPs) based on an advanced implementation of the primal and dual revised
simplex algorithm.  It provides special support for the exact solution of LPs
with rational input data.  It can be used as a standalone solver reading MPS
or LP format files via a command line interface as well as embedded into other
programs via a C++ class library.  The main features of SoPlex are:

- presolving, scaling, exploitation of sparsity, hot-starting from any regular
  basis,
- column- and row-oriented form of the simplex algorithm,
- an object-oriented software design written in C++,
- a compile-time option to use 80bit extended ("quad") precision for
  numerically difficult LPs,
- an LP iterative refinement procedure to compute high-precision solution, and
- routines for an exact rational LU factorization and continued fraction
  approximations in order to compute exact solutions.

SoPlex has been used in numerous research and industry projects and is the
standard LP solver linked to the mixed-integer nonlinear programming and
constraint integer programming solver SCIP.}

%description
%_desc

This package contains a command-line tool to access SoPlex
functionality.

%package -n     libsoplex
Summary:        Library for sequential object-oriented simplex

# The bundled version of fmt is incompatible with version 10 in Rawhide.
Provides:       bundled(fmt) = 7.1.3

%description -n libsoplex
%_desc

This package contains a library interface to SoPlex functionality.

%package -n     libsoplex-devel
Summary:        Headers and library links for libsoplex
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libsoplex%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}
Requires:       gmp-devel%{?_isa}
Requires:       libpapilo-devel%{?_isa}
%if %{quadmath}
Requires:       libquadmath-devel%{?_isa}
%endif
Requires:       mpfr-devel%{?_isa}
Requires:       zstr-devel

%description -n libsoplex-devel
This package contains headers and library links for developing
applications that use libsoplex.

%package -n     libsoplex-doc
# The content is licensed with Apache-2.0.  The other licenses are due to files
# added by doxygen.  Most such files are licensed with GPL-1.0-or-later, but
# the JavaScript files are licensed with MIT.
License:        Apache-2.0 AND GPL-1.0-or-later AND MIT
Summary:        API documentation for libsoplex
BuildArch:      noarch

%description -n libsoplex-doc
API documentation for libsoplex.

%prep
%autosetup -n %{name}-release-%{upver} -p1

%conf
# We want to know about overflow errors, as the compiler can do surprising
# things if we don't fix them!
sed -i 's/ -Wno-strict-overflow//' CMakeLists.txt Makefile

# Turn off HTML timestamps for repeatable builds
sed -i '/HTML_TIMESTAMP/s/YES/NO/' doc/soplex.dxy

# Ensure the bundled copy of zstr is not used
rm -fr src/soplex/external/zstr

%build
%cmake \
  -DMPFR:BOOL=ON \
  -DPAPILO:BOOL=ON \
  -DQUADMATH:BOOL=%{?quadmath:ON}%{!?quadmath:OFF}
%cmake_build

# Build documentation
cd doc
../%{_vpath_builddir}/bin/soplex --saveset=parameters.set
cd inc
python3 parser.py --linkext html
php localfaq.php > faq.inc
cd ..
doxygen soplex.dxy
cd ..

%install
%cmake_install

# Fix the papilo and clusol dependencies
sed -i 's/papilo;/papilo-core;clusol;/' \
    %{buildroot}%{_libdir}/cmake/soplex/soplex-targets.cmake

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%ctest

%files
%{_bindir}/soplex

%files -n libsoplex
%doc CHANGELOG README.md
%license LICENSE
%{_libdir}/libsoplex.so.7.1*

%files -n libsoplex-devel
%{_includedir}/soplex*
%{_libdir}/libsoplex.so
%{_libdir}/cmake/soplex/

%files -n libsoplex-doc
%doc doc/html
%license LICENSE

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 7.1.6-3
- test: add initial lock files

* Thu Dec 18 2025 Jerry James <loganjerry@gmail.com> - 7.1.6-2
- Fix the papilo and clusol dependencies

* Fri Nov 21 2025 Jerry James <loganjerry@gmail.com> - 7.1.6-1
- Version 7.1.6

* Tue Aug 19 2025 Jerry James <loganjerry@gmail.com> - 7.1.5-2
- Rebuild for tbb 2022.2.0

* Thu Aug 07 2025 Jerry James <loganjerry@gmail.com> - 7.1.5-1
- Version 7.1.5

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Apr 25 2025 Jerry James <loganjerry@gmail.com> - 7.1.4-1
- Version 7.1.4

* Fri Feb 14 2025 Jerry James <loganjerry@gmail.com> - 7.1.3-1
- Version 7.1.3

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Jerry James <loganjerry@gmail.com> - 7.1.2-2
- Move configuration steps to %%conf

* Tue Dec 03 2024 Jerry James <loganjerry@gmail.com> - 7.1.2-1
- Version 7.1.2

* Mon Sep 23 2024 Jerry James <loganjerry@gmail.com> - 7.1.1-1
- Version 7.1.1
- Use zlib-ng directly instead of via the compatibility interface

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jerry James <loganjerry@gmail.com> - 7.1.0-2
- Fix the VCS field

* Mon Jun 24 2024 Jerry James <loganjerry@gmail.com> - 7.1.0-1
- Version 7.1.0
- Drop upstreamed template-id patch

* Wed Jun 19 2024 Jerry James <loganjerry@gmail.com> - 7.0.1-1
- Version 7.0.1
- Drop upstreamed nondefinition, python3, and segfault patches
- Add patch for invalid C++ template IDs

* Wed Mar 13 2024 Jerry James <loganjerry@gmail.com> - 7.0.0-1
- Version 7.0.0
- Note that fmt is now bundled
- Add MIT to License for the bundled fmt
- Drop upstreamed invalid-array-assignment patch
- Add patch to avoid potential segfault

* Fri Feb 23 2024 Jerry James <loganjerry@gmail.com> - 6.0.4-1
- Initial RPM
## END: Generated by rpmautospec
