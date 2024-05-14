Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global provider_dir %{_libdir}/cmpi

Name:           sblim-cmpi-sysfs
Version:        1.2.0
Release:        24%{?dist}
Summary:        SBLIM sysfs instrumentation

License:        EPL
URL:            https://sblim.wiki.sourceforge.net/
Source0:        https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2

# Patch0: already upstream,
#         see https://sourceforge.net/tracker/index.php?func=detail&aid=2818227&group_id=128809&atid=712784
Patch0:         sblim-cmpi-sysfs-1.2.0-provider-segfault.patch
# Patch1: issue reported upstream, patch not accepted yet,
#         see https://sourceforge.net/tracker/index.php?func=detail&aid=2818223&group_id=128809&atid=712784
Patch1:         sblim-cmpi-sysfs-1.2.0-sysfs-links.patch
# Patch2: remove version from docdir
Patch2:         sblim-cmpi-sysfs-1.2.0-docdir.patch
# Patch3: use Pegasus root/interop instead of root/PG_Interop
Patch3:         sblim-cmpi-sysfs-1.2.0-pegasus-interop.patch
# Patch4: call systemctl in provider registration
Patch4:         sblim-cmpi-sysfs-1.2.0-prov-reg-sfcb-systemd.patch

BuildRequires:  sblim-cmpi-devel sblim-cmpi-base-devel
BuildRequires:  gcc
Requires:       sblim-cmpi-base cim-server

%description
Standards Based Linux Instrumentation Sysfs Providers

%package        test
Summary:        SBLIM Sysfs Instrumentation Testcases
Requires:       sblim-cmpi-sysfs = %{version}-%{release}
Requires:       sblim-testsuite

%description test
SBLIM Base Params Testcase Files for SBLIM Testsuite

%prep
%setup -q
%patch 0 -p1 -b .provider-segfault
%patch 1 -p1 -b .sysfs-links
%patch 2 -p1 -b .docdir
%patch 3 -p1 -b .pegasus-interop
%patch 4 -p1 -b .prov-reg-sfcb-systemd
sed -ri 's,-type d -maxdepth 1 -mindepth 1,-maxdepth 1 -mindepth 1 -type d,g' \
        ./test/system/linux/*.{sh,system}


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
mv $RPM_BUILD_ROOT/%{_libdir}/libLinux_SysfsAttributeUtil.so $RPM_BUILD_ROOT/%{provider_dir}
mv $RPM_BUILD_ROOT/%{_libdir}/libLinux_SysfsDeviceUtil.so $RPM_BUILD_ROOT/%{provider_dir}


%files
%doc AUTHORS COPYING DEBUG README README.TEST README.tog-pegasus sysfs.txt
%dir %{provider_dir}
%{provider_dir}/libLinux_Sysfs*
%{_datadir}/sblim-cmpi-sysfs
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files test
%{_datadir}/sblim-testsuite/sblim-cmpi-sysfs-test.sh
%{_datadir}/sblim-testsuite/cim/Linux_Sysfs*
%{_datadir}/sblim-testsuite/system/linux/Linux_Sysfs*


%global SCHEMA %{_datadir}/%{name}/Linux_SysfsAttribute.mof %{_datadir}/%{name}/Linux_SysfsBlockDevice.mof %{_datadir}/%{name}/Linux_SysfsBusDevice.mof %{_datadir}/%{name}/Linux_SysfsInputDevice.mof %{_datadir}/%{name}/Linux_SysfsNetworkDevice.mof %{_datadir}/%{name}/Linux_SysfsSCSIDevice.mof %{_datadir}/%{name}/Linux_SysfsSCSIHostDevice.mof %{_datadir}/%{name}/Linux_SysfsTTYDevice.mof

%global REGISTRATION %{_datadir}/%{name}/Linux_SysfsAttribute.registration %{_datadir}/%{name}/Linux_SysfsBlockDevice.registration %{_datadir}/%{name}/Linux_SysfsBusDevice.registration %{_datadir}/%{name}/Linux_SysfsInputDevice.registration %{_datadir}/%{name}/Linux_SysfsNetworkDevice.registration %{_datadir}/%{name}/Linux_SysfsSCSIDevice.registration %{_datadir}/%{name}/Linux_SysfsSCSIHostDevice.registration %{_datadir}/%{name}/Linux_SysfsTTYDevice.registration

%pre
%sblim_pre

%post
%sblim_post

%preun
%sblim_preun
 
%postun -p /sbin/ldconfig


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.0-19
- Add BuildRequires gcc
- Remove Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.0-12
- Update provider registration script to use systemctl to stop/start sfcb
- Use new macros for %%pre/%%post/%%preun from sblim-cmpi-devel

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.0-9
- Use Pegasus root/interop instead of root/PG_Interop
- Fix for unversioned docdir change
  Resolves: #994084

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.0-6
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.0-3
- Fix provider segfaults when enumerating instances of Linux_SysfsAttribute class
- Fix provider doesn't show much sysfs entries
- Add mofs registration for various CIMOMs

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct  4 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.0-1
- Update to sblim-cmpi-sysfs-1.2.0
- Remove CIMOM dependencies

* Wed Oct 14 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.9-1
- Initial support
