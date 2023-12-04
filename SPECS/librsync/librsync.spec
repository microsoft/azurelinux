Summary:        Rsync libraries
Name:           librsync
Version:        2.3.4
Release:        1%{?dist}
License:        LGPLv2+ AND CC0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://librsync.github.io/
#Source0:       https://github.com/librsync/librsync/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
%if %{with_check}
BuildRequires:  which
%endif

%description
librsync implements the "rsync" algorithm, which allows remote
differencing of binary files.  librsync computes a delta relative to a
file's checksum, so the two files need not both be present to generate
a delta.

This library was previously known as libhsync up to version 0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

%package devel
Summary:        Headers and development libraries for librsync
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
librsync implements the "rsync" algorithm, which allows remote
differencing of binary files.  librsync computes a delta relative to a
file's checksum, so the two files need not both be present to generate
a delta.

This library was previously known as libhsync up to version 0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

This package contains header files necessary for developing programs
based on librsync.

%prep
%setup -q

%build
mkdir -p build
cd build
%cmake -DCMAKE_SKIP_RPATH:BOOL=YES \
         -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
         -DENABLE_STATIC:BOOL=NO ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%if %{with_check}
# install outside of DESTDIR to resolve test error:
# /usr/src/mariner/BUILD/librsync-2.0.2/build/rdiff: error while loading shared libraries: librsync.so.2: cannot open shared object file: No such file or directory
make install
%endif

%check
cd build
make test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS
%{_bindir}/rdiff
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/*.so

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.3.4-1
- Auto-upgrade to 2.3.4 - Azure Linux 3.0 - package upgrades

* Thu Jan 13 2022 Henry Li <lihl@microsoft.com> - 2.3.2-1
- Upgrade to version 2.3.2

*   Wed Dec 09 2020 Andrew Phelps <anphel@microsoft.com> 2.0.2-4
-   Fix check tests

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.0.2-3
-   Added %%license line automatically

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 2.0.2-3
-   Verified license. Removed sha1. Fixed Source0 URL comment.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 2.0.2-1
-   Update to 2.0.2

*   Wed Jun 28 2017 Chang Lee <changlee@vmware.com>  2.0.0-2
-   Updated %check

*   Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  2.0.0-1
-   Initial build. First version
