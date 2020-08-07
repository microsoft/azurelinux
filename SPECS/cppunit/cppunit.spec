Summary:	C++ port of Junit test framework
Name:		cppunit
Version:	1.12.1
Release:        5%{?dist}
License:	LGPLv2
URL:		https://sourceforge.net/projects/cppunit/
Source0:	https://sourceforge.net/projects/cppunit/files/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 cppunit=f1ab8986af7a1ffa6760f4bacf5622924639bf4a
Group:		Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool

%description
CppUnit is the C++ port of the famous JUnit framework for unit testing. Test
output is in XML or text format for automatic testing and GUI based for
supervised tests

%package devel
Summary:        cppunit devel
Group:          Development/Tools
%description devel
This contains headers and libs for development with cppunit.

%prep
%setup -n %{name}-%{version}

%build
export LDFLAGS="`echo " %{build_ldflags} " | sed 's/ -Wl,--as-needed//'`"
%configure \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/libcppunit-*so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/libcppunit.a
%{_libdir}/libcppunit.so
%{_libdir}/pkgconfig*
/usr/share/*

%changelog
*   Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.12.1-5
-   Disable link as-needed to fix compilation errors updated ldflags.
*   Sat May 09 00:21:26 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.12.1-4
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.12.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.12.1-2
-   Use standard configure macros
*   Sun Mar 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.12.1-1
-   Initial version of cppunit for Photon.
