Summary:        Tools and Utilities for interaction with SCSI devices.
Name:           sg3_utils
Version:        1.48
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Tools.
URL:            http://sg.danny.cz/sg/sg3_utils.html
Source0:        https://github.com/hreinecke/sg3_utils/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Provides:       sg_utils.
Provides:       %{name}-libs

%description
Linux tools and utilities to send commands to SCSI devices.

%package -n libsg3_utils-devel
Summary:        Devel package for sg3_utils.
Group:          Development/Library.
Provides:       %{name}-devel

%description -n libsg3_utils-devel
Package containing static library object for development.

%prep
%setup -q

%build
./autogen.sh
%configure

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%install
if [ "$RPM_BUILD_ROOT" != "/" ]; then
        rm -rf $RPM_BUILD_ROOT
fi

make install \
        DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING COVERAGE CREDITS INSTALL NEWS README README.sg_start
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/*

%files -n libsg3_utils-devel
%defattr(-,root,root)
%{_includedir}/scsi/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/libsgutils2-1.48.so.2
%{_libdir}/libsgutils2-1.48.so.2.0.0
%{_libdir}/libsgutils2.la


%changelog
* Thu Jan 25 2024 Dallas Delaney <dadelan@microsoft.com> - 1.48-1
- Upgrade to version 1.48

* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.46-2
- Fixing invalid source URL.

* Tue Jan 04 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.46-1
- Update to version 1.46

* Thu Dec 10 2020 Joe Schmitt <joschmit@microsoft.com> - 1.44-3
- Provide sg3_utils-devel and sg3_utils-libs.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.44-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 1.44-1
- Update to 1.44. Removed ctr patch (fixed upstream). Fix URL. Fix Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.43-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.43-2
- Fix compilation issue against glibc-2.28

* Tue Oct 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.43-1
- Update to v1.43

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.42-2
- GA - Bump release of all rpms

*   Thu Apr 14 2016 Kumar Kaushik <kaushikk@vmware.com> 1.42-1
-   Initial build. First version
