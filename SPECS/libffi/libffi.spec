Summary:    A portable, high level programming interface to various calling conventions
Name:       libffi
Version:    3.2.1
Release:    10%{?dist}
License:    BSD
URL:        http://sourceware.org/libffi/
Group:      System Environment/GeneralLibraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:    ftp://sourceware.org/pub/libffi/%{name}-%{version}.tar.gz
Provides:   pkgconfig(libffi)
#%if %{with_check}
#BuildRequires:  dejagnu
#%endif

%description
The libffi library provides a portable, high level programming interface
to various calling conventions. This allows a programmer to call any
function specified by a call interface description at run time.

%package    devel
Summary:    Header and development files for libffi
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
sed -e '/^includesdir/ s:$(libdir)/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:$(includedir):' \
    -i include/Makefile.in &&
sed -e '/^includedir/ s:${libdir}/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:@includedir@:' \
    -e 's/^Cflags: -I${includedir}/Cflags:/' \
    -i libffi.pc.in        &&
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
rm -rf %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_lib64dir}/*.la
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*

#%check
#make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
%ifarch aarch64
%{_libdir}/*.so*
%endif
%ifarch x86_64
%{_libdir}/*.so*
%endif

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datarootdir}/licenses/libffi/LICENSE
%{_mandir}/man3/*

%changelog
*   Tue Jul 07 2020 Henry Beberman <henry.beberman@microsoft.com> 3.2.1-10
-   Comment out dejagnu dependency and check to prevent a rebuild.
*   Wed May 13 2020 Nick Samson <nisamson@microsoft.com> 3.2.1-9
-   Added %%license line automatically
*   Wed Jan 29 2020 Andrew Phelps <anphel@microsoft.com> 3.2.1-8
-   Fixing build issues for multiple architectures
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.2.1-7
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-6
-   Aarch64 support
*   Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-5
-   Get tcl, expect and dejagnu from packages
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-4
-   Added -devel subpackage
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.2.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 3.2.1-1
-   Updated to version 3.2.1
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.1-1
-   Initial build.	First version
