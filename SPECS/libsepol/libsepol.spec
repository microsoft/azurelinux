Summary:	    SELinux binary policy manipulation library
Name:		    libsepol
Version:	    2.9
Release:        5%{?dist}
License:	    LGPLv2+
Group:		    System Environment/Libraries
URL:		    http://www.selinuxproject.org
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20190315/%{name}-%{version}.tar.gz
Source1:        https://sourceforge.net/projects/cunit/files/CUnit-2.1-2-src.tar.bz2
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package	devel
Summary:	Header files and libraries used to build policy manipulation tools
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	pkgconfig(libsepol)

%description	devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%prep
%setup -qn %{name}-%{version}
sed  -i 's/int rc;/int rc = SEPOL_OK;/' ./cil/src/cil_binary.c
tar xf %{SOURCE1} --no-same-owner

%build
make clean
make %{?_smp_mflags} CFLAGS="%{build_cflags}"

%install
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man8
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" install
rm -f %{buildroot}%{_bindir}/genpolbools
rm -f %{buildroot}%{_bindir}/genpolusers
rm -f %{buildroot}%{_bindir}/chkcon
rm -rf %{buildroot}%{_mandir}/man8
rm -rf %{buildroot}%{_mandir}/ru/man8

%check
pushd CUnit-2.1-2/
./configure --prefix=/usr
make
make install
popd

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
[ -x /sbin/telinit ] && [ -p /dev/initctl ]  && /sbin/telinit U
exit 0

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root)
%license COPYING
%{_libdir}/libsepol.so
%{_libdir}/libsepol.a
%{_libdir}/pkgconfig/libsepol.pc
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h
%{_includedir}/sepol/*.h
%{_includedir}/sepol/cil/*.h
%{_mandir}/man3/*.3.gz

%files
%defattr(-,root,root)
%{_lib}/libsepol.so.1

%changelog
*   Tue Jun 09 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.9-5
-   Remove unused "systemd-bootstrap" from requires.
*   Fri May 29 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.9-4
-   Use "systemd-bootstrap" to break circular dependencies.
*   Sat May 09 00:21:36 PST 2020 Nick Samson <nisamson@microsoft.com> 2.9-3
-   Added %%license line automatically
*   Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 2.9-2
-   Add cflags to make to fix gcc9 compatibility.
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 2.9-1
-   Update to 2.9. Fix Source0 URL. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.8-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Aug 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.8-1
-   Update to version 2.8 to get it to build with gcc 7.3
*   Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.6-1
-   Updating version to 2.6
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-2
-	GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-1
-   Updated to version 2.5
*	Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> 2.4-1
-	Initial build.	First version
