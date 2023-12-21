Summary:        Utilities for managing the XFS filesystem
Name:           xfsprogs
Version:        6.5.0
Release:        1%{?dist}
License:        GPL+ and LGPLv2+
URL:            https://xfs.wiki.kernel.org/
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/%{name}-%{version}.tar.xz
BuildRequires:  gettext
BuildRequires:  readline-devel
BuildRequires:  inih-devel
BuildRequires:  userspace-rcu-devel

%description
The xfsprogs package contains administration and debugging tools for the
XFS file system.

%package devel
Summary: XFS filesystem-specific static libraries and headers
Group: Development/Libraries
Requires: xfsprogs = %{version}-%{release}

%description devel
Libraries and header files needed to develop XFS filesystem-specific programs.

%package lang
Summary: Additional language files for xfsprogs
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of xfsprogs.

%prep
%setup -q

%build
%configure \
    --enable-readline=yes \
    --enable-blkid=yes

make DEBUG=-DNDEBUG     \
     INSTALL_USER=root  \
     INSTALL_GROUP=root  %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_usr}/share/doc/%{name}-%{version} install
make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_usr}/share/doc/%{name}-%{version} install-dev

find %{buildroot}/%{_lib64dir} -name '*.la' -delete
find %{buildroot}/%{_lib64dir} -name '*.a' -delete

%find_lang %{name}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license debian/copyright LICENSES/*
%doc %{_docdir}/%{name}-%{version}/*
/sbin/*
/lib64/*.so.*.*
%{_libdir}/xfsprogs/xfs_scrub_all.cron
%{_mandir}/man2/*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_sbindir}/*
%{_datadir}/%{name}/mkfs/*.conf
%exclude %{_docdir}/%{name}-%{version}/CHANGES.gz

%files devel
%defattr(-,root,root)
%dir %{_includedir}/xfs
%{_includedir}/xfs/*
/lib64/*.so
/lib64/*.so.1
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Tue Dec 19 2023 Andrew Phelps <anphel@microsoft.com> - 6.5.0-1
- Upgrade to version 6.5.0

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.15.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jul 28 2023 Andy Zaugg <azaugg@linkedin.com> - 5.15-1
- Updated to version 5.15

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0.0-3
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.0.0-2
- Added %%license line automatically

*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 5.0.0-1
-   Update to 5.0.0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.18.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 4.18.0-1
-   Updated to latest version
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.10.0-3
-   Use standard configure macros
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.10.0-2
-   Ensure non empty debuginfo
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 4.10.0-1
-   Updated to version 4.10.0.
*   Fri Jan 6 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.0-1
-   Initial build.  First version
