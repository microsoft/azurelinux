Summary:        Math libraries
Name:           gmp
Version:        6.3.0
Release:        1%{?dist}
License:        GPLv2+ AND GPLv3+ AND LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.gnu.org/software/gmp
Source0:        http://ftp.gnu.org/gnu/gmp/%{name}-%{version}.tar.xz

%description
The GMP package contains math libraries. These have useful functions
for arbitrary precision arithmetic.

%package    devel
Summary:        Header and development files for gmp
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%autosetup -p1

%build
cp -v configfsf.guess config.guess
cp -v configfsf.sub   config.sub
./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules \
    --disable-static \
    --disable-assembly \
    --enable-cxx
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -v doc/{isa_abi_headache,configuration} doc/*.html %{buildroot}%{_defaultdocdir}/%{name}-%{version}
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING COPYING.LESSERv3 COPYINGv2 COPYINGv3
%{_libdir}/libgmp.so.*

%files devel
%{_includedir}/gmp.h
%{_includedir}/gmpxx.h
%{_libdir}/libgmp.so
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.so.*
%{_libdir}/pkgconfig/gmp.pc
%{_libdir}/pkgconfig/gmpxx.pc
%{_docdir}/%{name}-%{version}/tasks.html
%{_docdir}/%{name}-%{version}/projects.html
%{_docdir}/%{name}-%{version}/configuration
%{_docdir}/%{name}-%{version}/isa_abi_headache

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.3.0-1
- Auto-upgrade to 6.3.0 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 6.2.1-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jul 26 2023 Archana Choudhary <archana1@microsoft.com> - 6.2.1-3
- Added c++ support in gmp-devel package

* Fri Nov 19 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.2.1-2
- Adding a patch to fix CVE-2021-43618.
- Added missing licensing information.
- Using HTTPS in the 'URL' and 'Source0' tags.

* Mon Oct 11 2021 Andrew Phelps <anphel@microsoft.com> - 6.2.1-1
- Update to version 6.2.1
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 6.1.2-5
- Added %%license line automatically

* Fri Feb 14 2020 Andrew Phelps <anphel@microsoft.com> - 6.1.2-4
- Use generic config to help prevent illegal instruction errors

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 6.1.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Apr 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.1.2-2
- Disable cxx (do not build libgmpxx). Disable static.

* Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> - 6.1.2-1
- Update to 6.1.2

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 6.0.0a-3
- GA - Bump release of all rpms

* Thu Apr 14 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> - 6.0.0a-2
- Disable assembly and use generic C code

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> - 6.0.0a-1
- Updated to version 6.0.0

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 5.1.3-1
- Initial build. First version
