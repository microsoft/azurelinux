Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           sblim-cmpi-base
Version:        1.6.4
Release:        17%{?dist}
Summary:        SBLIM CMPI Base Providers

License:        EPL-1.0
URL:            https://sourceforge.net/projects/sblim/
Source0:        https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
Patch0:         sblim-cmpi-base-1.6.0-missing-fclose.patch
Patch1:         sblim-cmpi-base-1.6.0-methods-enable.patch
Patch2:         sblim-cmpi-base-1.6.1-double-fclose.patch
# Patch3: removes version from docdir
Patch3:         sblim-cmpi-base-1.6.2-docdir.patch
# Patch4: use Pegasus root/interop instead of root/PG_Interop
Patch4:         sblim-cmpi-base-1.6.2-pegasus-interop.patch
# Patch5: call systemctl in provider registration
Patch5:         sblim-cmpi-base-1.6.4-prov-reg-sfcb-systemd.patch
# Patch6: explicitly list library dependencies in Makefile.am, rhbz#1606302
Patch6:         sblim-cmpi-base-1.6.4-list-lib-dependencies.patch
# Patch7: don't install COPYING with license, included through %%license
Patch7:         sblim-cmpi-base-1.6.4-dont-install-license.patch
# Patch8: fixes getting of InstallDate property, improves it to work
#   on non en_US locales and updates support for Fedora
Patch8:         sblim-cmpi-base-1.6.4-fix-get-os-install-date.patch
# Patch9: fixes possible null pointer dereferences after strstr calls
Patch9:         sblim-cmpi-base-1.6.4-fix-possible-null-dereference.patch
Requires:       cim-server sblim-indication_helper
BuildRequires:  perl-generators
BuildRequires:  sblim-cmpi-devel sblim-indication_helper-devel
BuildRequires:  autoconf automake libtool pkgconfig


%description
SBLIM (Standards Based Linux Instrumentation for Manageability)
CMPI (Common Manageability Programming Interface) Base Providers
for System-Related CIM (Common Information Model) classes.

%package devel
Summary:        SBLIM CMPI Base Providers Development Header Files
Requires:       %{name} = %{version}-%{release}

%description devel
SBLIM (Standards Based Linux Instrumentation for Manageability)
CMPI (Common Manageability Programming Interface) Base Provider
development header files and link libraries.

%package test
Summary:        SBLIM CMPI Base Providers Test Cases
Requires:       %{name} = %{version}-%{release}
Requires:       sblim-testsuite

%description test
SBLIM (Standards Based Linux Instrumentation for Manageability)
CMPI (Common Manageability Programming Interface) Base Provider
Testcase Files for the SBLIM Testsuite.

%prep
%setup -q
autoreconf --install --force
%patch 0 -p0 -b .missing-fclose
%patch 1 -p0 -b .methods-enable
%patch 2 -p1 -b .double-fclose
%patch 3 -p1 -b .docdir
%patch 4 -p1 -b .pegasus-interop
%patch 5 -p1 -b .prov-reg-sfcb-systemd
%patch 6 -p1 -b .list-lib-dependencies
%patch 7 -p1 -b .dont-install-license
%patch 8 -p1 -b .fix-get-os-install-date
%patch 9 -p1 -b .fix-possible-null-dereference.patch

%build
%configure TESTSUITEDIR=%{_datadir}/sblim-testsuite --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
cp -fp *OSBase_UnixProcess.h $RPM_BUILD_ROOT/%{_includedir}/sblim
chmod 644 $RPM_BUILD_ROOT/%{_includedir}/sblim/*OSBase_UnixProcess.h
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/cmpi/*a

%files
%license COPYING
%doc AUTHORS DEBUG README README.INDICATION README.TEST README.tog-pegasus
%{_datadir}/%{name}
%{_libdir}/*.so.*
%{_libdir}/cmpi/*.so*

%files devel
%{_includedir}/*
%{_libdir}/*.so

%files test
%dir %{_datadir}/sblim-testsuite/cim
%dir %{_datadir}/sblim-testsuite/system
%dir %{_datadir}/sblim-testsuite/system/linux
%{_datadir}/sblim-testsuite/test-cmpi-base.sh
%{_datadir}/sblim-testsuite/cim/*.cim
%{_datadir}/sblim-testsuite/system/linux/*.system
%{_datadir}/sblim-testsuite/system/linux/*.sh
%{_datadir}/sblim-testsuite/system/linux/*.pl

%global SCHEMA %{_datadir}/%{name}/Linux_Base.mof %{_datadir}/%{name}/Linux_BaseIndication.mof

%global REGISTRATION %{_datadir}/%{name}/Linux_BaseIndication.registration

%pre
%sblim_pre

%post
%sblim_post

%preun
%sblim_preun

%postun -p /sbin/ldconfig

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.4-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Feb 04 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.4-16
- Fix possible null pointer dereferences after strstr calls

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.4-14
- Fix getting of InstallDate property, improve it to work on non en_US locales
  and update support for recent Fedora distributions

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.4-12
- Fix URL

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 22 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.4-10
- Fix docdir patch (patch Makefile.am, not Makefile.in)
- Use correct short name for Eclipse Public License 1.0
- Use %%license
- Add explicit dependencies for libraries in Makefile.am (fixes FTBFS)
  Resolves: #1606302

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.4-2
- Update provider registration script to use systemctl to stop/start sfcb
- Use new macros for %%pre/%%post/%%preun from sblim-cmpi-devel

* Wed Oct 29 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.4-1
- Update to sblim-cmpi-base-1.6.4

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-8
- Support aarch64
  Resolves: #926474

* Wed Aug 07 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-7
- Use Pegasus root/interop instead of root/PG_Interop
- Fix unversioned docdir change
  Resolves: #994073

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.6.2-5
- Perl 5.18 rebuild

* Mon Jun 17 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-4
- Fix wrong UserModeTime and KernelModeTime
- Fix bogus date in %%changelog

* Thu Jun 06 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-3
- Fix incorrect max cpu frequency

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-1
- Update to sblim-cmpi-base-1.6.2

* Tue Sep 04 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.1-8
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.1-6
- Fix double fclose() call (patch by Roman Rakus <rrakus@redhat.com>)
  Resolves: #820315

* Wed Feb 15 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.1-5
- Enable indications and method providers

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 27 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.1-3
- Fix/enhance mofs registration for various CIMOMs (patch by Masatake Yamato)
  Resolves: #695626

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.1-1
- Update to sblim-cmpi-base-1.6.1

* Mon Dec 13 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.0-2
- Fix license, mofs registration for various CIMOMs, sblim-sfcb init script
  path in provider-register.sh, rpmlint warnings

* Wed Oct  6 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.6.0-1
- Updated to 1.6.0
- removed the CIMOM dependencies
- following the upstream packaging obsolete, sblim-cmpi-base-test pkg.
- Added the patches from upstream packaging
- fix to restart tog-pegasus properly

* Thu Aug 27 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.9-1
- Update to 1.5.9

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.7-2
- Fix %%files (to be able build -devel dependent packages)
- Remove rpath from libraries
- Spec file cleanup, rpmlint check

* Fri Oct 24 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.7-1
- Update to 1.5.7
  Resolves: #468325

* Wed Jul  2 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.5-2
- Fix testsuite dependency

* Tue Jul  1 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.5-1
- Update to 1.5.5
- Spec file revision

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.4-8
- Autorebuild for GCC 4.3

* Tue Dec 05 2006 Mark Hamzy <hamzy@us.ibm.com> - 1.5.4-7
- Ignore failures when running provider-register.sh.  cimserver may be down

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.5.4-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Nov 10 2005  <mihajlov@de.ibm.com> - 1.5.4-3
- suppress error output in post scriptlets

* Wed Oct 26 2005  <mihajlov@de.ibm.com> - 1.5.4-2
- went back to original provider dir location as FC5 pegasus 2.5.1 support
  /usr/lib[64]/cmpi

* Wed Oct 12 2005  <mihajlov@de.ibm.com> - 1.5.4-1
- new spec file specifically for Fedora/RedHat

* Wed Jul 20 2005 Mark Hamzy <hamzy@us.ibm.com> - 1.5.3-1
- initial support
