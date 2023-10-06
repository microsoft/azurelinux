Summary:        Utilities for loading kernel modules
Name:           kmod
Version:        29
Release:        2%{?dist}
License:        LGPLv2.1+ AND GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.kernel.org/pub/linux/utils/kernel/kmod
Source0:        http://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
Requires:       xz
Provides:       module-init-tools
Provides:       /sbin/modprobe

%description
The Kmod package contains libraries and utilities for loading kernel modules

%package        devel
Summary:        Header and development files for kmod
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=/bin \
    --sysconfdir=%{_sysconfdir} \
    --with-rootlibdir=%{_libdir} \
    --disable-manpages \
    --with-xz \
    --with-zlib \
    --disable-silent-rules
make VERBOSE=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} pkgconfigdir=%{_libdir}/pkgconfig install
install -vdm 755 %{buildroot}/sbin
for target in depmod insmod lsmod modinfo modprobe rmmod; do
    ln -sv /bin/kmod %{buildroot}/sbin/$target
done
find %{buildroot} -type f -name "*.la" -delete -print

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
/bin/*
%{_libdir}/*.so.*
/sbin/*
%{_datadir}/bash-completion/completions/kmod

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 29-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Dec 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 29-1
- Updated to version 29
- Verified license.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 25-6
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 25-5
- Provide /sbin/modprobe and module-init-tools for base package

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 25-4
- Added %%license line automatically

* Tue Jan 21 2020 Andrew Phelps <anphel@microsoft.com> 25-3
- Fix changelog date

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 25-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Ankit Jain <ankitja@vmware.com> 25-1
- Updated to version 25

* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 24-3
- Add devel package.

* Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 24-2
- Remove %check

* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 24-1
- Updated to version 24

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 21-4
- GA - Bump release of all rpms

* Thu Apr 21 2016 Anish Swaminathan <anishs@vmware.com> 21-3
- Add patch for return code fix in error path

* Fri Mar 25 2016 Alexey Makhalov <amakhalov@vmware.com> 21-2
- /bin/lsmod -> /sbin/lsmod

* Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> 21-1
- Updated to version 21

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 16-1
- Initial build. First version
