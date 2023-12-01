Summary:        C++ port of Junit test framework
Name:           cppunit
Version:        1.15.1
Release:        1%{?dist}
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://sourceforge.net/projects/cppunit/
Source0:        https://dev-www.libreoffice.org/src/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool
BuildRequires:  make

%description
CppUnit is the C++ port of the famous JUnit framework for unit testing. Test
output is in XML or text format for automatic testing and GUI based for
supervised tests

%package devel
Summary:        cppunit devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description devel
This contains headers and libs for development with cppunit.

%prep
%setup -q

%build
export LDFLAGS="`echo " %{build_ldflags} " | sed 's/ -Wl,--as-needed//'`"
%configure \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

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
%{_datadir}/*

%changelog
* Wed Mar 16 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.15.1-1
- Update to v1.15.1.

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.12.1-7
- Remove unused `%%define sha1` lines
- License verified

* Mon Feb 08 2021 Henry Li <lihl@microsoft.com> - 1.12.1-6
- Add cppunit as Requires for cppunit-devel

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.12.1-5
- Disable link as-needed to fix compilation errors updated ldflags.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.12.1-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.12.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.12.1-2
- Use standard configure macros

* Sun Mar 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.12.1-1
- Initial version of cppunit for Photon.
