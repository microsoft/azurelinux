Name:       btrfs-progs
Version:    6.8
Release:    2%{?dist}
Summary:    Userspace programs for btrfs
Group:      System Environment/Base
License:    GPLv2+
URL:        https://btrfs.wiki.kernel.org/index.php/Main_Page
Source0:    https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz#/%{name}-%{version}.tar.xz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildRequires:  lzo-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libacl-devel
BuildRequires:  systemd-devel
BuildRequires:  xmlto
BuildRequires:  asciidoc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-sphinx
BuildRequires:  pkgconfig(libgcrypt) >= 1.8.0
Requires:   e2fsprogs
Requires:   lzo

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
%configure CFLAGS="%{optflags} -fno-strict-aliasing" --with-crypto=libgcrypt --disable-python --disable-zstd
%make_build

%install
#disabled the documentation
make DISABLE_DOCUMENTATION=1 mandir=%{_mandir} bindir=%{_sbindir} libdir=%{_libdir} incdir=%{_includedir} install DESTDIR=%{buildroot}
# Nuke the static lib
rm -v %{buildroot}%{_libdir}/*.a

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
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfsutil.so
%{_libdir}/pkgconfig/libbtrfsutil.pc


%changelog
* Wed Mar 27 2024 Betty Lakes <bettylakes@microsoft.com> - 6.8-2
- Disable zstd

* Wed Mar 27 2024 Betty Lakes <bettylakes@microsoft.com> - 6.8-1
- Update to 6.8

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.16-102
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jan 13 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.16-1
- Update to 5.16

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
