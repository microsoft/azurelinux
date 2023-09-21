%global debug_package %{nil}
Summary:        A language for data analysis and graphics
Name:           R
Version:        4.1.0
Release:        4%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            https://www.r-project.org
Source0:        https://cran.r-project.org/src/base/R-4/R-%{version}.tar.gz
# This change is a best hunch fix as the limitation on curl version 7 was set
# in 2018. Given curl 8.0.0 is not an actual breaking change, this patch should be fine.
# We should drop this when R eventually gets official support for build with curl >= 8.0.0
Patch0:         0001-configure-fix-compilation-with-curl-8.0.0.patch
BuildRequires:  build-essential
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  gfortran
BuildRequires:  glibc-iconv
BuildRequires:  make
BuildRequires:  msopenjdk-11
BuildRequires:  pcre
BuildRequires:  pcre2
BuildRequires:  pcre2-devel
BuildRequires:  readline-devel
BuildRequires:  which
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
R is a language and environment for statistical computing and graphics.
It is a GNU project which is similar to the S language and environment
which was developed at Bell Laboratories (formerly AT&T, now Lucent
Technologies) by John Chambers and colleagues. R can be considered as a
different implementation of S. There are some important differences, but
much code written for S runs unaltered under R. R, like S, is designed
around a true computer language, and it allows users to add additional
functionality by defining new functions. Much of the system is itself
written in the R dialect of S, which makes it easy for users to follow
the algorithmic choices made. For computationally-intensive tasks, C,
C++ and Fortran code can be linked and called at run time. Advanced
users can write C code to manipulate R objects directly.

%package     core
Summary:        R
Requires:       bzip2-devel
Requires:       curl-devel
Requires:       gcc-c++
Requires:       gfortran
Requires:       xz-devel
Requires:       zlib-devel

%description core
R is a language and environment for statistical computing and graphics.
It is a GNU project which is similar to the S language and environment
which was developed at Bell Laboratories (formerly AT&T, now Lucent
Technologies) by John Chambers and colleagues. R can be considered as a
different implementation of S. There are some important differences, but
much code written for S runs unaltered under R. R, like S, is designed
around a true computer language, and it allows users to add additional
functionality by defining new functions. Much of the system is itself
written in the R dialect of S, which makes it easy for users to follow
the algorithmic choices made. For computationally-intensive tasks, C,
C++ and Fortran code can be linked and called at run time. Advanced
users can write C code to manipulate R objects directly.

%package     core-devel
Summary:        Core files for development of R packages
Requires:       %{name}-core = %{version}-%{release}

%description core-devel
Install R-core-devel if you are going to develop or compile R packages.

%prep
%autosetup -p1

%build
./configure --with-x=no --prefix=%{_prefix}/
%make_build

%install
%make_install
%ifarch x86_64
pushd %{buildroot}%{_lib64dir}/R
ln -s %{_includedir}/R include
popd
%endif

%check
# Tests do not all pass
# Upstream tests on intel architectures
%ifnarch aarch64
ulimit -s 16384
TZ="Europe/Paris" make check -k -i
%endif

%files core
%license COPYING
%{_bindir}/R
%{_bindir}/Rscript
%{_mandir}/man1/R*
%ifarch x86_64
%{_lib64dir}/R/*
%exclude %dir %{_lib64dir}/R/include/*
%exclude %{_prefix}/src/debug/R*
%exclude %dir %{_libdir}/debug/usr/lib64/R*
%endif
%ifarch aarch64
%{_libdir}/R/*
%exclude %dir %{_libdir}/R/include/*
%endif

%files core-devel
%ifarch x86_64
%{_lib64dir}/R/include/*
%endif
%ifarch aarch64
%{_libdir}/R/include/*
%endif

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.1.0-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Mar 31 2023 Muhammad Falak <mwani@microsoft.com> - 4.1.0-3
- Patch to fix build with curl >= 8.0.0

* Thu Dec 02 2021 Andrew Phelps <anphel@microsoft.com> - 4.1.0-2
- Build with JDK 11
* Wed Jun 16 2021 Rachel Menge <rachelmenge@microsoft.com> - 4.1.0-1
- Add R spec.
- License verified
- Original version for CBL-Mariner
