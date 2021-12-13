Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		edac-utils
Version:	0.16
Release:	23%{?dist}
Summary:	Userspace helper for kernel EDAC drivers

License:	GPLv2+
URL:		https://github.com/grondo/edac-utils

ExclusiveArch:	%{ix86} x86_64 %{arm} aarch64 %{power64}
# Source0: https://github.com/grondo/edac-utils/archive/refs/tags/0.16.tar.gz
Source0:	https://github.com/grondo/edac-utils/archive/refs/tags/%{name}-%{version}.tar.bz2
Source1:	edac.service

%ifarch %{ix86} x86_64
Requires:	dmidecode
%endif
Requires:	hwdata
Requires:	sysfsutils
Requires:	systemd
BuildRequires:  gcc
BuildRequires:	libsysfs-devel
BuildRequires:	perl-generators
BuildRequires:  systemd
BuildRequires:	systemd-devel

%description 
EDAC is the current set of drivers in the Linux kernel that handle
detection of ECC errors from memory controllers for most chipsets
on i386 and x86_64 architectures. This userspace component consists
of an init script which makes sure EDAC drivers and DIMM labels
are loaded at system startup, as well as a library and utility
for reporting current error counts from the EDAC sysfs files.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development headers and libraries
for %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags} 

%install
make install-exec install-data DESTDIR="$RPM_BUILD_ROOT"
# Remove libtool archive
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

install -D -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/edac.service
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/edac

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable edac.service > /dev/null 2>&1 || :
    /bin/systemctl stop edac.service > /dev/null 2>&1 || :
fi

%postun
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart edac.service >/dev/null 2>&1 || :
fi

%triggerun -- edac-utils < 0.9-14
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply edac
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save edac >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del edac >/dev/null 2>&1 || :
/bin/systemctl try-restart edac.service >/dev/null 2>&1 || :

%files 
%doc COPYING README NEWS ChangeLog DISCLAIMER
%{_sbindir}/edac-ctl
%{_bindir}/edac-util
%{_libdir}/*.so.*
%{_mandir}/*/*
%dir %attr(0755,root,root) %{_sysconfdir}/edac
%config(noreplace) %{_sysconfdir}/edac/*
%{_unitdir}/edac.service

%files devel
%{_libdir}/*.so
%{_includedir}/edac.h

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 23 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.16-13
- BR: systemd (Fix F23FTBFS, RHBZ#1239443).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.16-11
- edac supported in the kernel for ppc64/aarch64 too

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.16-7
- Minor spec cleanups to fix FTBFS

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.16-5
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.16-3
- ARM has support for EDAC so enable the utils

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Aristeu Rozanski <aris@redhat.com> - 0.16-1
- New upstream release 0.16

* Wed Mar 14 2012 Jon Ciesla <limburgher@gmail.com> - 0.9-14
- Migrate to systemd, BZ 767784.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.9-9
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-8
- Autorebuild for GCC 4.3

* Wed Jul 18 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-7
- including missing .patch file

* Tue Jul 17 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-6
- building FC7 package

* Thu Jul 09 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-5
- Fixed start/stop message, missing echo
- Fixed status command to use edac-util

* Thu Jun 15 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-4
- Removed debug code left by mistake on initrd file
- Fixed model comparing in edac-ctl script

* Wed Jun 13 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-3
- Adding COPYING to documents
- Fixing Requires to use a single equal sign, instead of two

* Wed Jun 13 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-2
- Multiple updates in spec file to conform to the standards pointed by
  Jarod Wilson

* Wed Jun 06 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-1
- Updated version to 0.9, separate project now
- Updated spec file based on upstream edac-utils spec file
- Removed driver loading portion in a separate patch, it'll be removed from
  upstream too
- Fixed init script to use functions and daemon function

* Thu Apr 19 2007 Aristeu Rozanski <arozansk@redhat.com> 20061222-3
- Updated initrd script to start after syslogd, otherwise if the board isn't
  supported, the user will never know.

* Thu Apr 19 2007 Aristeu Rozanski <arozansk@redhat.com> 20061222-2
- Changing this package to noarch and preventing the build on ia64, ppc64,
  s390 and s390x

* Thu Mar 12 2007 Aristeu Rozanski <arozansk@redhat.com> 20061222-1
- Package created

