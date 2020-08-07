Name:           pcre2
Version:        10.34
Release:        1%{?dist}
Summary:        A library for Perl-compatible regular expressions
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
URL:            https://www.pcre.org/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.pcre.org/pub/pcre/%{name}-%{version}.tar.bz2
BuildRequires:  libgcc
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  bzip2-devel
%if %{with pcre2_enables_readline}
BuildRequires:  readline-devel
%endif

Requires: %{name}-tools
Requires: %{name}-doc

%description
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

%package        devel
Summary:        A library for Perl-compatible regular expressions
Group:          Development/Libraries/C and C++
Requires:       libpcre2-16-0 = %{version}
Requires:       libpcre2-32-0 = %{version}
Requires:       libpcre2-8-0 = %{version}
Requires:       libpcre2-posix2 = %{version}
Requires:       libstdc++-devel

%description devel
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

%package        devel-static
Summary:        A library for Perl-compatible regular expressions
Group:          Development/Libraries/C and C++
Requires:       pcre2-devel = %{version}

%description devel-static
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

This package contains static versions of the PCRE2 libraries.

%package -n libpcre2-8-0
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries

%description -n libpcre2-8-0
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

This PCRE2 library variant supports 8-bit and UTF-8 strings.
(See also libpcre2-16 and libpcre2-32)

%package -n libpcre2-16-0
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries

%description -n libpcre2-16-0
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

libpcre2-16 supports 16-bit and UTF-16 strings.

%package -n libpcre2-32-0
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries

%description -n libpcre2-32-0
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

libpcre2-32 supports 32-bit and UTF-32 strings.

%package -n libpcre2-posix2
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries

%description -n libpcre2-posix2
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

pcre2-posix provides a POSIX-compatible API to the PCRE2 engine.

%package doc
Summary:        A library for Perl-compatible regular expressions
Group:          Documentation/HTML
BuildArch:      noarch

%description doc
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

%package tools
Summary:        A library for Perl-compatible regular expressions
Group:          Productivity/Text/Utilities
Recommends:     %{name}-doc

%description tools
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

%prep
%setup -q

%build
# Available JIT archs see sljit/sljitConfig.h
autoreconf -fiv
export LDFLAGS="-Wl,-z,relro,-z,now"
%configure \
%ifarch %{ix86} x86_64 %{arm} ppc ppc64 ppc64le mips sparc
       --enable-jit \
       --enable-jit-sealloc \
%endif
       --enable-static \
       --with-link-size=2 \
       --with-match-limit=10000000 \
       --enable-newline-is-lf \
       --enable-pcre2-16 \
       --enable-pcre2-32 \
       --enable-pcre2grep-libz \
       --enable-pcre2grep-libbz2 \
       --disable-pcre2test-libedit \
%if %{with pcre2_enables_readline}
       --enable-pcre2test-libreadline \
%else
       --disable-pcre2test-libreadline \
%endif
       --enable-unicode
%if 0%{?do_profiling}
  make %{?_smp_mflags} CFLAGS="%{optflags} %{cflags_profile_generate}" V=1
  export LANG=POSIX
  # do not run profiling in parallel for reproducible builds (boo#1040589 boo#1102408)
  make CFLAGS="%{optflags} %{cflags_profile_generate}" check
  make %{?_smp_mflags} clean
  make %{?_smp_mflags} CFLAGS="%{optflags} %{cflags_profile_feedback}" V=1
%else
  make %{?_smp_mflags} CFLAGS="%{optflags}"
%endif

%install
%make_install
mkdir -p %{buildroot}/%{_defaultdocdir}
mv %{buildroot}%{_datadir}/doc/pcre2 %{buildroot}/%{_defaultdocdir}/pcre2-doc
#empty dependecy_libs
find %{buildroot} -type f -name "*.la" -delete -print

%check
export LANG=POSIX
make check -j1

%post -n libpcre2-8-0 -p /sbin/ldconfig
%postun -n libpcre2-8-0 -p /sbin/ldconfig
%post -n libpcre2-16-0 -p /sbin/ldconfig
%postun -n libpcre2-16-0 -p /sbin/ldconfig
%post -n libpcre2-32-0 -p /sbin/ldconfig
%postun -n libpcre2-32-0 -p /sbin/ldconfig
%post -n libpcre2-posix2 -p /sbin/ldconfig
%postun -n libpcre2-posix2 -p /sbin/ldconfig

%files

%files -n libpcre2-8-0
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libpcre2-8.so.*

%files -n libpcre2-16-0
%doc LICENCE
%{_libdir}/libpcre2-16.so.*

%files -n libpcre2-32-0
%doc LICENCE
%{_libdir}/libpcre2-32.so.*

%files -n libpcre2-posix2
%doc LICENCE
%{_libdir}/libpcre2-posix.so.*

%files tools
%doc LICENCE
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_mandir}/man1/pcre2grep.1.gz
%{_mandir}/man1/pcre2test.1.gz

%files doc
%license COPYING
%doc AUTHORS ChangeLog LICENCE NEWS README
%doc doc/html doc/*.txt
%doc %{_defaultdocdir}/pcre2-doc

%files devel
%doc LICENCE
%{_bindir}/pcre2-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpcre2-8.pc
%{_libdir}/pkgconfig/libpcre2-16.pc
%{_libdir}/pkgconfig/libpcre2-32.pc
%{_libdir}/pkgconfig/libpcre2-posix.pc
%{_mandir}/man1/pcre2-config.1.gz
%{_mandir}/man3/*.gz

%files devel-static
%{_libdir}/*.a

%changelog
* Tue May 18 2020 Andrew Phelps <anphel@microsoft.com> - 10.34-1
- Update to version 10.34

* Tue Mar 31 2020 Joe Schmitt <joschmit@microsoft.com> - 10.32-3
- Generate pcre2 package

* Mon Mar 30 2020 Joe Schmitt <joschmit@microsoft.com> - 10.32-2
- Update Vendor and Distribution tags
- Update source url
- Remove sha1 macro

* Thu Feb 13 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 10.32-1
- Original version for CBL-Mariner.

