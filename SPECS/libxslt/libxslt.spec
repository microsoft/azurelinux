%define majminorver %(echo %{version} | cut -d. -f 1,2)
Summary:        Libxslt is the XSLT C library developed for the GNOME project. XSLT is a an XML language to define transformation for XML.
Name:           libxslt
Version:        1.1.39
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/General Libraries
URL:            http://xmlsoft.org/libxslt/
Source0:        https://download.gnome.org/sources/libxslt/%{majminorver}/%{name}-%{version}.tar.xz
BuildRequires:  libgcrypt-devel
BuildRequires:  libxml2-devel
Requires:       libgcrypt
Requires:       libxml2-devel
Provides:       %{name}-tools = %{version}-%{release}

%description
The libxslt package contains XSLT libraries used for extending libxml2 libraries to support XSLT files.

%package devel
Summary:        Development Libraries for libxslt
Group:          Development/Libraries
Requires:       libxslt = %{version}-%{release}
Provides:       %{name}-devel%{?_isa} = %{version}-%{release}

%description devel
Header files for doing development with libxslt.

%prep
%autosetup -p1

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --disable-static \
    --without-python
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
%{_fixperms} %{buildroot}/*

%check
# Disable fuzz testing as it has compile error for the released version.
sed -i 's/ fuzz//g' tests/Makefile
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/*.sh
%{_libdir}/libxslt-plugins
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/cmake/libxslt/FindGcrypt.cmake
%{_libdir}/cmake/libxslt/libxslt-config.cmake
%{_includedir}/*
%{_docdir}/*
%{_datadir}/gtk-doc/*
%{_datadir}/aclocal/*
%{_mandir}/man3/*



%changelog
* Tue Nov 28 2023 Andrew Phelps <anphel@microsoft.com> - 1.1.39-1
- Upgrade to version 1.1.39

* Tue May 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.1.34-7
- Applying patch for CVE-2021-30560.

* Fri Mar 04 2022 Muhammad Falak <mwani@microsoft.com> - 1.1.34-6
- Drop fuzz testing to enable ptest

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.34-5
- Removing the explicit %%clean stage.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.1.34-4
- Provide libxslt-devel%%{?_isa}

* Tue Dec 01 2020 Joe Schmitt <joschmit@microsoft.com> - 1.1.34-3
- Provide libxslt-tools.

*   Wed Aug 19 2020 Henry Beberman <henry.beberman@microsoft.com> 1.1.34-2
-   Add dependency on libgcrypt

*   Mon Jun 08 2020 Joe Schmitt <joschmit@microsoft.com> 1.1.34-1
-   Update to version 1.1.34 to resolve CVE-2019-11068.
-   Remove patch for CVE-2019-5815 since it is fixed in 1.1.34.
-   License verified.

*   Tue May 12 2020 Paul Monson <paulmon@microsoft.com> 1.1.32-4
-   Add patch for CVE-2019-5815

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.32-3
-   Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.32-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.1.32-1
-   Update to version 1.1.32.

*   Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 1.1.29-4
-   Applied patches for CVE-2015-9019 and CVE-2017-5029.

*   Tue May 23 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1.29-3
-   Build does not requires python.

*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.29-2
-   Moved man3 to devel subpackage.

*   Fri Oct 21 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.29-1
-   Fix CVEs 2016-1683, 2016-1684, 2015-7995 with version 1.1.29

*   Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 1.1.28-4
-   Modified check

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.28-3
-   GA - Bump release of all rpms

*   Tue Jan 19 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.28-2
-   Add a dev subpackage.

*   Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.28-1
-   Initial build.  First version
