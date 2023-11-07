Summary:        Libcap
Name:           libcap
Version:        2.69
Release:        1%{?dist}
License:        GPLv2+
Group:          System Environment/Security
URL:            https://www.gnu.org/software/hurd/community/gsoc/project_ideas/libcap.html
Source0:        https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
The libcap package implements the user-space interfaces to the POSIX 1003.1e capabilities available
in Linux kernels. These capabilities are a partitioning of the all powerful root privilege
into a set of distinct privileges.

%package        devel
Summary:        Development files for libcap
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libcap-devel package contains libraries, header files and documentation
for developing applications that use libcap.

%prep
%autosetup -p1

%build
sed -i 's:LIBDIR:PAM_&:g' pam_cap/Makefile
make %{?_smp_mflags}
%install
make prefix=%{_prefix}	SBINDIR=%{_sbindir} PAM_LIBDIR=%{_libdir} RAISE_SETFCAP=no DESTDIR=%{buildroot} LIBDIR=%{_libdir} install
chmod -v 755 %{buildroot}%{_libdir}/libcap.so

%check
cd progs
sed -i "s|pass_capsh --chroot=\$(/bin/pwd) ==||g" quicktest.sh
./quicktest.sh

%files
%defattr(-,root,root)
%license License
%{_libdir}/libcap.so.*
%{_libdir}/libpsx.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%exclude %{_libdir}/libcap.a
%exclude %{_libdir}/libpsx.a
%{_libdir}/pkgconfig/*
%{_libdir}/libcap.so
%{_libdir}/libpsx.so
%{_mandir}/man3/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.69-1
- Auto-upgrade to 2.69 - Azure Linux 3.0 - package upgrades

* Thu Jun 15 2023 Henry Li <lihl@microsoft.com> - 2.60-2
- Add patch to resolve CVE-2023-2602 and CVE-2023-2603
- Use autosetup

* Sat Nov 20 2021 Chris Co <chrco@microsoft.com> - 2.60-1
- Update version to 2.60

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.26-2
- Added %%license line automatically

* Mon Mar 16 2020 Andrew Phelps <anphel@microsoft.com> - 2.26-1
- Update version to 2.26. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.25-9
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.25-8
- Aarch64 support

* Wed Aug 09 2017 Danut Moraru <dmoraru@vmware.com> - 2.25-7
- Remove capsh test that runs chroot already in chroot, failing due to expected environment/dependencies not available

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.25-6
- Remove attr deps.

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.25-5
- Moved man3 to devel subpackage.

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.25-4
- BuildRequired attr-devel.

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 2.25-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.25-2
- GA - Bump release of all rpms

* Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> - 2.25-1
- Updating Version.

* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> - 2.24-2
- Moving static lib files to devel package.

* Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> - 2.24-1
- Initial version
