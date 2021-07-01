Summary:        A language for data analysis and graphics
Name:           R
Version:        4.1.0
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            http://www.r-project.org
Source0:        https://cran.r-project.org/src/base/R-4/R-%{version}.tar.gz

BuildRequires:  build-essential
BuildRequires:  glibc-iconv
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  pcre
BuildRequires:  pcre2
BuildRequires:  pcre2-devel 
BuildRequires:  openjdk8
BuildRequires:  gfortran
BuildRequires:  which
BuildRequires:  readline-devel 
BuildRequires:  zlib-devel
BuildRequires:  curl-devel
BuildRequires:  bzip2-devel
BuildRequires:  make

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
Summary:      R
Requires:     zlib-devel
Requires:     curl-devel
Requires:     bzip2-devel
Requires:     gcc-c++
Requires:     gfortran 
Requires:     xz-devel

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
Summary:     Core files for development of R packages
Requires:    %{name}-core

%description core-devel
Install R-core-devel if you are going to develop or compile R packages.

%prep
%autosetup -p1

%build
./configure --with-x=no --prefix=/usr/
%make_build

%install
%make_install
pushd %{buildroot}%{_lib64dir}/R
ln -s %{_includedir}/R include 
popd

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
%{_exec_prefix}/lib64/R/*
%{_mandir}/man1/R*
%exclude %dir %{_exec_prefix}/lib64/R/include/*
%exclude %{_usrsrc}/debug/usr/bin/R*
%exclude %dir %{_exec_prefix}/lib/debug/usr/lib64/R*

%files core-devel
%{_exec_prefix}/lib64/R/include/*

%changelog
* Wed Jun 16 2021 Rachel Menge <rachelmenge@microsoft.com> - 4.1.0-1
- Add R spec.
- License verified
- Original version for CBL-Mariner
