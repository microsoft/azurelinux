Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global provider_dir %{_libdir}/cmpi

Summary:        SBLIM fsvol instrumentation
Name:           sblim-cmpi-fsvol
Version:        1.5.1
Release:        27%{?dist}
License:        EPL
URL:            https://sourceforge.net/projects/sblim/
Source0:        https://downloads.sourceforge.net/project/sblim/providers/%{name}/%{version}/%{name}-%{version}.tar.bz2
Patch0:         sblim-cmpi-fsvol-1.5.0-ext4-support.patch
# Patch1: bz921487, backported from upstream
Patch1:         sblim-cmpi-fsvol-1.5.1-mounted-fs-shown-as-disabled.patch
# Patch2: remove version from docdir
Patch2:         sblim-cmpi-fsvol-1.5.1-docdir.patch
# Patch3: use Pegasus root/interop instead of root/PG_Interop
Patch3:         sblim-cmpi-fsvol-1.5.1-pegasus-interop.patch
# Patch4: call systemctl in provider registration
Patch4:         sblim-cmpi-fsvol-1.5.1-prov-reg-sfcb-systemd.patch
# Patch5: fixes  mounted filesystem is shown as disabled when device mapper is used
Patch5:         sblim-cmpi-fsvol-1.5.1-mounted-dm-fs-shown-as-disabled.patch

BuildRequires:  perl-generators
BuildRequires:  sblim-cmpi-base-devel sblim-cmpi-devel
BuildRequires:  gcc
Requires:       sblim-cmpi-base cim-server
Requires:       /etc/ld.so.conf.d
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Standards Based Linux Instrumentation Fsvol Providers

%package devel
Summary:        SBLIM Fsvol Instrumentation Header Development Files
Requires:       %{name} = %{version}-%{release}

%description devel
SBLIM Base Fsvol Development Package

%package test
Summary:        SBLIM Fsvol Instrumentation Testcases
Requires:       %{name} = %{version}-%{release}
Requires:       sblim-testsuite

%description test
SBLIM Base Fsvol Testcase Files for SBLIM Testsuite

%prep
%setup -q
%patch 0 -p1 -b .ext4-support
%patch 1 -p0 -b .mounted-fs-shown-as-disabled
%patch 2 -p1 -b .docdir
%patch 3 -p1 -b .pegasus-interop
%patch 4 -p1 -b .prov-reg-sfcb-systemd
%patch 5 -p1 -b .mounted-dm-fs-shown-as-disabled

%build
%ifarch s390 s390x ppc ppc64
export CFLAGS="$RPM_OPT_FLAGS -fsigned-char"
%else
export CFLAGS="$RPM_OPT_FLAGS" 
%endif
%configure \
        TESTSUITEDIR=%{_datadir}/sblim-testsuite \
        PROVIDERDIR=%{provider_dir}
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

%files
%doc AUTHORS COPYING DEBUG README README.TEST README.tog-pegasus
%{_libdir}/libcmpiOSBase_CommonFsvol*.so.*
%{provider_dir}/libcmpiOSBase_LocalFileSystemProvider.so
%{provider_dir}/libcmpiOSBase_NFSProvider.so
%{provider_dir}/libcmpiOSBase_BlockStorageStatisticalDataProvider.so
%{provider_dir}/libcmpiOSBase_HostedFileSystemProvider.so
%{provider_dir}/libcmpiOSBase_BootOSFromFSProvider.so
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%files devel
%{_libdir}/libcmpiOSBase_CommonFsvol*.so
%{_includedir}/sblim/*Fsvol.h

%files test
%{_datadir}/sblim-testsuite/test-cmpi-fsvol.sh
%{_datadir}/sblim-testsuite/cim/*FileSystem.cim
%{_datadir}/sblim-testsuite/cim/*FS.cim
%{_datadir}/sblim-testsuite/cim/*BlockStorageStatisticalData.cim
%{_datadir}/sblim-testsuite/system/linux/*FileSystem.*
%{_datadir}/sblim-testsuite/system/linux/*FileSystemEntries.*

%global SCHEMA %{_datadir}/%{name}/Linux_Fsvol.mof

%global REGISTRATION %{_datadir}/%{name}/Linux_Fsvol.registration

%pre
%sblim_pre

%post
%sblim_post

%preun
%sblim_preun

%postun -p /sbin/ldconfig

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.1-27
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-22
- Add BuildRequires gcc
- Remove Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 09 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-18
- Fix mounted filesystem is shown as disabled when device mapper is used

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-14
- Update provider registration script to use systemctl to stop/start sfcb
- Use new macros for %%pre/%%post/%%preun from sblim-cmpi-devel

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-11
- Use Pegasus root/interop instead of root/PG_Interop
- Fix for unversioned docdir change
  Resolves: #994078

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.5.1-9
- Perl 5.18 rebuild

* Thu Mar 14 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-8
- Fix mounted filesystem is shown as disabled when fstab entry uses link, UUID or LABEL

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-6
- Fix source URL

* Tue Sep 04 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-5
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-2
- Add better support of mofs registration for various CIMOMs

* Wed May 25 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.1-1
- Update to sblim-cmpi-fsvol-1.5.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.0-2
- Add ext4 support (without update of testcase files)
- Fix mofs registration for various CIMOMs

* Thu Nov  4 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.0-1
- Update to sblim-cmpi-fsvol-1.5.0
- Remove CIMOM dependencies

* Wed Oct 14 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.4-1
- Initial support
