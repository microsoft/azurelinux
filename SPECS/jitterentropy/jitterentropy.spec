%define         debug_package %{nil}
Summary:        Library implementing the jitter entropy source
Name:           jitterentropy
Version:        3.0.2
Release:        1%{?dist}
License:        BSD OR GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/smuellerDD/jitterentropy-library
#Source0:       https://github.com/smuellerDD/%%{name}-library/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-library-%{version}.tar.gz
Patch0:         makefile.patch
BuildRequires:  gcc
BuildRequires:  make

%description
The Jitter RNG provides a noise source using the CPU execution timing jitter.
It does not depend on any system resource other than a high-resolution time stamp.
It is a small-scale, yet fast entropy source that is viable in almost all environments and on a lot of CPU architectures.

%prep
%autosetup -n %{name}-library-%{version} -p1

%build
export CFLAGS='-DOPENSSL -DOPENSSL_FIPS'
make

%install
mkdir -p %{buildroot}%{_includedir}
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

# Rename static library to libjitterentropy-openssl
mv %{buildroot}/%{_libdir}/lib%{name}.a %{buildroot}/%{_libdir}/lib%{name}-openssl.a

%files
%doc README.md
%license COPYING COPYING.bsd COPYING.gplv2
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/lib%{name}-openssl.a

%changelog
* Wed Apr 14 2021 Nicolas Ontiveros <niontive@microsoft.com> - 3.0.2-1
- Original version for CBL-Mariner. License verified.