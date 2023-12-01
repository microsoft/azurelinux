Summary:        A library for Perl-compatible regular expressions
Name:           pcre2
Version:        10.42
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/C and C++
URL:            https://www.pcre.org/
Source0:        https://github.com/PhilipHazel/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bzip2-devel
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
Requires:       %{name}-doc = %{version}-%{release}
Requires:       %{name}-tools = %{version}-%{release}
Requires:       libpcre2-8-0 = %{version}-%{release}
Requires:       libpcre2-posix2 = %{version}-%{release}

%description
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

%package        devel
Summary:        A library for Perl-compatible regular expressions
Group:          Development/Libraries/C and C++
Requires:       libpcre2-16-0 = %{version}-%{release}
Requires:       libpcre2-32-0 = %{version}-%{release}
Requires:       libpcre2-8-0 = %{version}-%{release}
Requires:       libpcre2-posix2 = %{version}-%{release}
Requires:       libstdc++-devel

%description    devel
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

%package        devel-static
Summary:        A library for Perl-compatible regular expressions
Group:          Development/Libraries/C and C++
Requires:       pcre2-devel = %{version}-%{release}

%description devel-static
The PCRE2 library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

PCRE2 is a re-working of the original PCRE library to provide an entirely new
API.

This package contains static versions of the PCRE2 libraries.

%package -n     libpcre2-8-0
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

%package -n     libpcre2-16-0
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries
Provides:       %{name}-utf16 = %{version}-%{release}

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
Provides:       %{name}-utf32 = %{version}-%{release}

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
       --enable-pcre2test-libreadline \
       --enable-unicode
%make_build

%install
%make_install
mkdir -p %{buildroot}/%{_defaultdocdir}
mv %{buildroot}%{_docdir}/pcre2 %{buildroot}/%{_defaultdocdir}/pcre2-doc
#empty dependecy_libs
find %{buildroot} -type f -name "*.la" -delete -print

%check
export LANG=POSIX
make check -j1

%ldconfig_scriptlets -n libpcre2-8-0
%ldconfig_scriptlets -n libpcre2-16-0
%ldconfig_scriptlets -n libpcre2-32-0
%ldconfig_scriptlets -n libpcre2-posix2

%files

%files -n libpcre2-8-0
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libpcre2-8.so.*

%files -n libpcre2-16-0
%license LICENCE
%{_libdir}/libpcre2-16.so.*

%files -n libpcre2-32-0
%license LICENCE
%{_libdir}/libpcre2-32.so.*

%files -n libpcre2-posix2
%license LICENCE
%{_libdir}/libpcre2-posix.so.*

%files tools
%license LICENCE
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_mandir}/man1/pcre2grep.1.gz
%{_mandir}/man1/pcre2test.1.gz

%files doc
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS README
%doc doc/html doc/*.txt
%doc %{_defaultdocdir}/pcre2-doc

%files devel
%license LICENCE
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
* Mon Jul 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.42-1
- Upgrading to v10.42 to address CVE-2022-41409.

* Thu May 26 2022 Cameron Baird <cameornbaird@microsoft.com> - 10.40-1
- Upgrading to v10.40 to address CVE-2022-1586, CVE-2022-1587

* Tue Feb 15 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 10.39-1
- Upgrading to v10.39
- Fixing source URL. 
- License verified.

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 10.34-2
- Unconditionally build with readline support
- Add compatibility provides for pcre2-utf{16,32}
- Require libpcre2-8-0, libpcre2-posix2 from base package

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
