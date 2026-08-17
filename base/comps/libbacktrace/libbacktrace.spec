%global commit 6f8310e238fc3ce68f42f391cbe93fd156bb2c23
%global shortcommit 6f8310e238fc
%global snapshotdate 20260816

# Static-only library: no shared objects or executables are shipped, so there is
# nothing for a debuginfo package to contain.
%global debug_package %{nil}

# LTO localizes the test's `int global` symbol, which the mtest_minidebug
# mini-symtab recipe then drops, failing %check; LTO also just bloats this
# small static archive.
%global _lto_cflags %{nil}

Name:           libbacktrace
Version:        0^%{snapshotdate}git%{shortcommit}
Release:        %autorelease
Summary:        C library for producing symbolic backtraces
License:        BSD-3-Clause
URL:            https://github.com/ianlancetaylor/libbacktrace
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libbacktrace is a C library that may be linked into C/C++ programs to produce
symbolic backtraces.

%package        static
Summary:        Static library and development headers for libbacktrace
Provides:       libbacktrace-devel = %{version}-%{release}

%description    static
This package contains the libbacktrace static library (libbacktrace.a) and its
public headers: backtrace.h and the generated backtrace-supported.h.

%prep
%autosetup -n %{name}-%{commit}

%build
# Build position-independent so the archive can also be linked into shared
# objects (e.g. Boost's boost_stacktrace_backtrace).
export CFLAGS="%{optflags} -fPIC"
%configure --disable-shared --enable-static
%make_build

%install
%make_install
# Only the static library and headers are shipped; drop the libtool archive.
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files static
%license LICENSE
%{_includedir}/backtrace.h
%{_includedir}/backtrace-supported.h
%{_libdir}/libbacktrace.a

%changelog
%autochangelog
