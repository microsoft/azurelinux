Name:       btrfs-progs
Version:    4.19
Release:        4%{?dist}
Summary:    Userspace programs for btrfs
Group:      System Environment/Base
License:    GPLv2+
URL:        http://btrfs.wiki.kernel.org/index.php/Main_Page
Source0:    https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz
%define sha1 btrfs-progs=df4d34b8ecf5eaac177a0b121b41e67fce9612e1
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  lzo-devel
BuildRequires:  e2fsprogs-devel,libacl-devel
BuildRequires:  xmlto
BuildRequires:  asciidoc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:   e2fsprogs, lzo

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package devel
Summary:    btrfs filesystem-specific libraries and headers
Group:      Development/Libraries
Requires:   btrfs-progs = %{version}-%{release}

%description devel
btrfs-progs-devel contains the libraries and header files needed to
develop btrfs filesystem-specific programs.

You should install btrfs-progs-devel if you want to develop
btrfs filesystem-specific programs.

%prep
%setup -q -n %{name}-v%{version}

%build
./autogen.sh
%configure \
	--disable-zstd
make DISABLE_DOCUMENTATION=1 %{?_smp_mflags}

%install
#disabled the documentation
make DISABLE_DOCUMENTATION=1 mandir=%{_mandir} bindir=%{_sbindir} libdir=%{_libdir} incdir=%{_includedir} install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%license COPYING
%doc COPYING
%{_libdir}/libbtrfs.so.0*
%{_libdir}/libbtrfsutil.so.1*
%{_sbindir}/btrfsck
%{_sbindir}/fsck.btrfs
%{_sbindir}/mkfs.btrfs
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-convert
%{_sbindir}/btrfstune
%{_sbindir}/btrfs
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-find-root
%{_sbindir}/btrfs-select-super

%files devel
%{_includedir}/*
%{_libdir}/libbtrfs.a
%{_libdir}/libbtrfsutil.a
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfsutil.so

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.19-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.19-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.19-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Nov 19 2018 Sujay G <gsujay@vmware.com> 4.19-1
-   Bump btrfs-progs version to 4.19
*   Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.10.2-2
-   Fix compilation issue againts e2fsprogs-1.44
*   Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  4.10.2-1
-   Upgrade to 4.10.2
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.4-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  4.4-1
-   Upgrade to 4.4
*   Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 3.18.2-1
-   Initial version
