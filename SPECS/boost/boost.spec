Summary:	Boost
Name:		boost
Version:	1.66.0
Release:        4%{?dist}
License:	Boost Software License V1
URL:		http://www.boost.org/
Group:		System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://downloads.sourceforge.net/boost/boost_1_66_0.tar.bz2
Patch0:    CVE-2018-14040.patch
%define sha1 boost=b6b284acde2ad7ed49b44e856955d7b1ea4e9459
BuildRequires:	bzip2-devel

%description
Boost provides a set of free peer-reviewed portable C++ source libraries. It includes libraries for
linear algebra, pseudorandom number generation, multithreading, image processing, regular expressions and unit testing.

%package        devel
Summary:        Development files for boost
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The boost-devel package contains libraries, header files and documentation
for developing applications that use boost.

%package        static
Summary:        boost static libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
The boost-static package contains boost static libraries.

%prep
%setup -qn boost_1_66_0
%patch0 -p1

%build
./bootstrap.sh --prefix=%{buildroot}%{_prefix}
./b2 %{?_smp_mflags} stage threading=multi

%install
./b2 install threading=multi

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE_1_0.txt
%{_libdir}/libboost_*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/boost/*
%{_libdir}/libboost_*.so

%files static
%defattr(-,root,root)
%{_libdir}/libboost_*.a

%changelog
* Mon Feb 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.66.0-4
- Add patch for CVE-2018-14040

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.66.0-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.66.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Sep 11 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.66.0-1
-   Update to version 1.66.0
*   Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 1.63.0-1
-   Upgraded to version 1.63.0
*   Thu Mar 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.60.0-3
-   Build static libs in additon to shared.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.60.0-2
-   GA - Bump release of all rpms
*   Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 1.60.0-1
-   Update to version 1.60.0.
*   Thu Oct 01 2015 Xiaolin Li <xiaolinl@vmware.com> 1.56.0-2
_   Move header files to devel package.
*   Tue Feb 10 2015 Divya Thaluru <dthaluru@vmware.com> 1.56.0-1
-   Initial build. First version
