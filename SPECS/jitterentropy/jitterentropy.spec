Summary:        Library implementing the jitter entropy source
Name:           jitterentropy
Version:        3.0.1
Release:        1%{?dist}
License:        BSD or GPLv2
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

%package devel
Summary:        Development libraries for jitterentropy-library
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers for jitterentropy-library

%package static
Summary:        Libraries for static linking of applications which will use jitterentropy library.
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
Libraries for static linking of applications which will use jitterentropy library.

%prep
%autosetup -n %{name}-library-%{version} -p1

%build
%set_build_flags
make

%install
mkdir -p %{buildroot}/usr/include/
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%license COPYING COPYING.bsd COPYING.gplv2
%{_libdir}/lib%{name}.so*

%files devel
%{_includedir}/*
%{_mandir}/man3/*

%files static
%{_libdir}/lib%{name}.a

%changelog
* Wed Apr 14 2021 Nicolas Ontiveros <niontive@microsoft.com> - 3.0.1-1
- Original version for CBL-Mariner. License verified.