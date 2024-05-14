Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global provider_dir %{_libdir}/cmpi

Summary:        SBLIM syslog instrumentation
Name:           sblim-cmpi-syslog
Version:        0.9.0
Release:        20%{?dist}
License:        EPL
URL:            https://sourceforge.net/projects/sblim/
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  cvs -z3 -d:pserver:anonymous@sblim.cvs.sourceforge.net:/cvsroot/sblim co -P cmpi-syslog
#  mv cmpi-syslog sblim-cmpi-syslog-0.8.0
#  tar -cJvf sblim-cmpi-syslog-0.8.0.tar.xz sblim-cmpi-syslog-0.8.0
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.bz2

# use Pegasus' root/interop instead of root/PG_Interop
Patch0:         sblim-cmpi-syslog-0.9.0-pegasus-interop.patch
Patch1:         sblim-cmpi-syslog-0.9.0-docdir.patch
# Patch2: call systemctl in provider registration
Patch2:         sblim-cmpi-syslog-0.9.0-prov-reg-sfcb-systemd.patch
# Patch3: fixes -Wformat-security build error when debug is enabled
Patch3:         sblim-cmpi-syslog-0.9.0-format-security.patch
# Patch4: fix possible buffer overflow, remove usage of obsolete tmpnam()
Patch4:         sblim-cmpi-syslog-0.9.0-buffer-overflow-remove-tmpnam.patch

BuildRequires:  perl-generators
BuildRequires:  sblim-cmpi-devel
BuildRequires:  sblim-cmpi-base-devel >= 1.5.4
BuildRequires:  libtool
Requires:       sblim-cmpi-base >= 1.5.4 cim-server
Requires:       /etc/ld.so.conf.d
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Standards Based Linux Instrumentation Syslog Providers

%package devel
# ^- currently a placeholder - no devel files shipped
Summary:        SBLIM Syslog Instrumentation Header Development Files
Requires:       %{name} = %{version}-%{release}

%description devel
SBLIM Base Syslog Development Package

%package test
Summary:        SBLIM Syslog Instrumentation Testcases
Requires:       %{name} = %{version}-%{release}
Requires:       sblim-testsuite

%description test
SBLIM Base Syslog Testcase Files for SBLIM Testsuite

%prep
%setup -q
%patch 0 -p1 -b .interop
%patch 1 -p1 -b .docdir
%patch 2 -p1 -b .prov-reg-sfcb-systemd
%patch 3 -p1 -b .format-security
%patch 4 -p1 -b .buffer-overflow-remove-tmpnam

%build
%ifarch s390 s390x ppc ppc64
export CFLAGS="$RPM_OPT_FLAGS -fsigned-char"
%else
export CFLAGS="$RPM_OPT_FLAGS"
%endif
%configure \
        TESTSUITEDIR=%{_datadir}/sblim-testsuite \
        PROVIDERDIR=%{provider_dir} \
        SYSLOG=rsyslog
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a
rm -f $RPM_BUILD_ROOT/%{provider_dir}/*a
# shared libraries
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/cmpi" > $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
# move libraries to provider dir
mv $RPM_BUILD_ROOT/%{_libdir}/lib[Ss]yslog*.so* $RPM_BUILD_ROOT/%{provider_dir}
# add shebang to the scripts
sed -i -e '1i#!/bin/sh' $RPM_BUILD_ROOT/%{_bindir}/syslog-service.sh \
$RPM_BUILD_ROOT/%{_datadir}/sblim-testsuite/runtest_pegasus.sh \
$RPM_BUILD_ROOT/%{_datadir}/sblim-testsuite/runtest_wbemcli.sh \
$RPM_BUILD_ROOT/%{_datadir}/sblim-testsuite/system/linux/logrecord.sh \
$RPM_BUILD_ROOT/%{_datadir}/sblim-testsuite/system/linux/msglogtest.sh \
$RPM_BUILD_ROOT/%{_datadir}/sblim-testsuite/system/linux/messagelog.sh

%files
%license COPYING
%doc AUTHORS ChangeLog INSTALL NEWS README
%{_bindir}/syslog-service.sh
%{provider_dir}/lib[Ss]yslog*.so*
%{_datadir}/%{name}
%docdir %{_datadir}/doc/%{name}
%{_datadir}/doc/%{name}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%files test
%{_datadir}/sblim-testsuite/runtest*
%{_datadir}/sblim-testsuite/test-cmpi-syslog*
%{_datadir}/sblim-testsuite/cim/Syslog*
%{_datadir}/sblim-testsuite/system/linux/Syslog*
%{_datadir}/sblim-testsuite/system/linux/logrecord.sh
%{_datadir}/sblim-testsuite/system/linux/messagelog.sh
%{_datadir}/sblim-testsuite/system/linux/msglogtest.sh
%{_datadir}/sblim-testsuite/system/linux/setting

%global SCHEMA %{_datadir}/sblim-cmpi-syslog/Syslog_Log.mof %{_datadir}/sblim-cmpi-syslog/Syslog_Service.mof  %{_datadir}/sblim-cmpi-syslog/Syslog_Configuration.mof
%global REGISTRATION %{_datadir}/sblim-cmpi-syslog/Syslog_Configuration.registration  %{_datadir}/sblim-cmpi-syslog/Syslog_Log.registration %{_datadir}/sblim-cmpi-syslog/Syslog_Service.registration

%pre
%sblim_pre

%post
%sblim_post

%preun
%sblim_preun

%postun -p /sbin/ldconfig

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-20
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 0.9.0-19
- Update Source0
- Add %%doc and %%license
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.9.0-8
- Fix -Wformat-security build fails when debug is enabled
- Fix possible buffer overflow and usage of obsolete tmpnam() function

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 05 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.9.0-6
- Update provider registration script to use systemctl to stop/start sfcb
- Use new macros for %%pre/%%post/%%preun from sblim-cmpi-devel

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 12 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.9.0-3
- Fix for unversioned docdir change
  Resolves: #994085

* Mon Aug  5 2013 Tomas Bzatek <tbzatek@redhat.com> - 0.9.0-2
- Use Pegasus root/interop instead of root/PG_Interop

* Fri Jul 26 2013 Tomas Bzatek <tbzatek@redhat.com> - 0.9.0-1
- Update to sblim-cmpi-syslog-0.9.0

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.8.0-11.20120315cvs
- Perl 5.18 rebuild

* Mon Jul 01 2013 Tomas Bzatek <tbzatek@redhat.com> - 0.8.0-10.20120315cvs
- Add support for rsyslog $IncludeConfig directive (#971807)
- Add support for filter definitions (#971807)
- Various rsyslog compatibility fixes (#971807)

* Thu May 30 2013 Tomas Bzatek <tbzatek@redhat.com> - 0.8.0-9.20120315cvs
- Update scriptlets to register with both sfcbd and pegasus

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-8.20120315cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.8.0-7.20120315cvs
- Set rsyslogd as default

* Thu Sep 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.8.0-6.20120315cvs
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5.20120315cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.8.0-4.20120315cvs
- Use latest upstream CVS (because of rsyslog support)
- Build against sblim-cmpi-devel and instead of tog-pegasus-devel
- Fix rsyslog support to work with systemd

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov  4 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.8.0-1
- Update to sblim-cmpi-syslog-0.8.0
- Remove CIMOM dependencies

* Fri Oct 23 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.7.11-1
- Initial support
