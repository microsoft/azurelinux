Summary:        Compression and decompression routines
Name:           zlib
Version:        1.3
Release:        1%{?dist}
URL:            https://www.zlib.net/
License:        zlib
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/madler/zlib/releases/download/v%{version}/%{name}-%{version}.tar.xz
#Patch0:         CVE-2023-45853.patch
%description
Compression and decompression routines
%package    devel
Summary:    Header and development files for zlib
Requires:   %{name} = %{version}
Provides:   zlib-static = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%autosetup -p1

%build
./configure \
    --prefix=%{_prefix}
make V=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_libdir}
ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libz.so) %{buildroot}%{_libdir}/libz.so

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%license contrib/dotzlib/LICENSE_1_0.txt
%{_libdir}/libz.so.*

%files devel
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/pkgconfig/zlib.pc
%{_libdir}/libz.a
%{_libdir}/libz.so
%{_mandir}/man3/zlib.3.gz

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3-1
- Auto-upgrade to 1.3 - Azure Linux 3.0 - package upgrades

* Thu Oct 19 2023 Nan Liu <liunan@microsoft.com> - 1.2.13-2
- Add patch to address CVE-2023-45853
- Fix invalid source URL

* Thu Apr 27 2023 Muhammad Falak <mwani@microsoft.com> - 1.2.13-1
- Upgrade version to address java exception
- Drop un-needed patches

* Tue Aug 16 2022 Muhammad Falak <mwani@microsoft.com> - 1.2.12-2
- Introduce patches from upstream to address CVE-2022-37434

* Tue Apr 12 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.2.12-1
- Upgrade to 1.12.2 to fix CVE-2018-25032
- License verified

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.2.11-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 1.2.11-4
-   Add explicit provide for zlib-static
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.2.11-3
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.11-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.11-1
-   Updated to version 1.2.11.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.8-5
-   Moved man3 to devel subpackage.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.2.8-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.8-3
-   GA - Bump release of all rpms
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.2.8-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
-   Initial build. First version
