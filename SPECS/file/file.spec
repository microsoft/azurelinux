Summary:        Contains a utility for determining file types
Name:           file
Version:        5.38
Release:        1%{?dist}
License:        BSD
URL:            https://www.darwinsys.com/file
Group:          Applications/File
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz

Requires:       %{name}-libs = %{version}-%{release}
Conflicts:      toybox

%description
The package contains a utility for determining the type of a
given file or files

%package        libs
Summary:        Library files for file
%description    libs
It contains the libraries to run the application.

%package        devel
Summary:        Header and development files for file
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q
%build
%configure \
    --disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*man1/*
%{_mandir}/*man4/*

%files  libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datarootdir}/misc/magic.mgc

%files  devel
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/*man3/*

%changelog
*   Mon Jun 08 2020 Joe Schmitt <joschmit@microsoft.com> 5.38-1
-   Update to version 5.38 to resolve CVE-2019-18218.
-   License verified.
-   Remove sha1 macro.
-   Update URL to use https.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 5.34-3
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5.34-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 5.34-1
-   Bump file version to 5.34
*   Fri Dec 15 2017 Divya Thaluru <dthaluru@vmware.com> 5.30-3
-   Added seperate package for libraries
-   Added toybox as conflict package
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 5.30-2
-   Add devel package.
*   Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 5.30-1
-   Updated to version 5.30
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.24-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 5.24-1
-   Updated to version 5.24
*   Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 5.22-1
-   Initial build. First version
