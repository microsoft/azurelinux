%define         debug_package %{nil}
Summary:        Library implementing the jitter entropy source
Name:           jitterentropy
# NOTE: this package should be used only by OpenSSL
# Since OpenSSL has a static link to this package,
# OpenSSL release must be bumped when this package is updated.
Version:        3.0.2
Release:        1%{?dist}
License:        BSD OR GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/smuellerDD/jitterentropy-library
#Source0:       https://github.com/smuellerDD/%%{name}-library/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-library-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
The Jitter RNG provides a noise source using the CPU execution timing jitter.
It does not depend on any system resource other than a high-resolution time stamp.
It is a small-scale, yet fast entropy source that is viable in almost all environments and on a lot of CPU architectures.

%package devel
Summary:        Development Libraries for jitterentropy
Group:          Development/Libraries

%description devel
The jitterentropy-devel package contains include files and shared libraries
needed to develop applications that use jitterentropy.

%package static
Summary:        Libraries for static linking of applications which will use jitterentropy
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
The jitterentropy-static package contains static libraries needed for static linking of
applications which use jitterentropy.

%prep
%autosetup -n %{name}-library-%{version} -p1

%build
export CFLAGS='-DOPENSSL -DOPENSSL_FIPS'
make

%install
mkdir -p %{buildroot}%{_includedir}
make install-static install-includes install-shared DESTDIR=%{buildroot} PREFIX=%{_prefix}

# Rename static library to libjitterentropy-openssl
mv %{buildroot}/%{_libdir}/lib%{name}.a %{buildroot}/%{_libdir}/lib%{name}-openssl.a

%files
%doc README.md
%license COPYING COPYING.bsd COPYING.gplv2
%{_libdir}/libjitterentropy.so.3*

%files devel
%{_libdir}/libjitterentropy.so
%{_includedir}/*

%files static
%{_libdir}/lib%{name}-openssl.a

%changelog
* Wed Apr 14 2021 Nicolas Ontiveros <niontive@microsoft.com> - 3.0.2-1
- Original version for CBL-Mariner. License verified.
