Summary:        Libxslt is the XSLT C library developed for the GNOME project. XSLT is a an XML language to define transformation for XML.
Name:           libxslt
Version:        1.1.34
Release:        1%{?dist}
License:        MIT
URL:            http://xmlsoft.org/libxslt/
Group:          System Environment/General Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://xmlsoft.org/sources/%{name}-%{version}.tar.gz
Requires:       libxml2-devel
BuildRequires:  libxml2-devel
%description
The libxslt package contains XSLT libraries used for extending libxml2 libraries to support XSLT files.

%package devel
Summary:        Development Libraries for libxslt
Group:          Development/Libraries
Requires:       libxslt = %{version}-%{release}
%description devel
Header files for doing development with libxslt.

%prep
%setup -q
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
find %{buildroot} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
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
%{_includedir}/*
%{_docdir}/*
%{_datadir}/aclocal/*
%{_mandir}/man3/*

%changelog
*   Mon Jun 08 2020 Joe Schmitt <joschmit@microsoft.com> 1.1.34-1
-   Update to version 1.1.34 to resolve CVE-2019-11068.
-   Remove patch for CVE-2019-5815 since it is fixed in 1.1.34.
-   License verified.
*   Tue May 12 2020 Paul Monson <paulmon@microsoft.com> 1.1.32-4
-   Add patch for CVE-2019-5815
*   Sat May 09 00:21:44 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.1.32-3
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
