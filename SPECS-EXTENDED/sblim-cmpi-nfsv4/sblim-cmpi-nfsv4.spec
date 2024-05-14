Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global provider_dir %{_libdir}/cmpi

Name:           sblim-cmpi-nfsv4
Summary:        SBLIM nfsv4 instrumentation
Version:        1.1.0
Release:        24%{?dist}
License:        EPL
URL:            https://sourceforge.net/projects/sblim/
Source0:        https://downloads.sourceforge.net/project/sblim/providers/%{name}/%{version}/%{name}-%{version}.tar.bz2

# Patch0: remove version from docdir
Patch0:         sblim-cmpi-nfsv4-1.1.0-docdir.patch
# Patch1: use Pegasus root/interop instead of root/PG_Interop
Patch1:         sblim-cmpi-nfsv4-1.1.0-pegasus-interop.patch
# Patch2: call systemctl in provider registration
Patch2:         sblim-cmpi-nfsv4-1.1.0-prov-reg-sfcb-systemd.patch

BuildRequires:  sblim-cmpi-base-devel sblim-cmpi-devel
BuildRequires:  gcc
Requires:       sblim-cmpi-base cim-server cim-schema
Requires:       /etc/ld.so.conf.d
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Standards Based Linux Instrumentation Nfsv4 Providers

%package devel
# ^- currently a placeholder - no devel files shipped
Summary:        SBLIM Nfsv4 Instrumentation Header Development Files
Requires:       %{name} = %{version}-%{release}

%description devel
SBLIM Base Nfsv4 Development Package

%package test
Summary:        SBLIM Nfsv4 Instrumentation Testcases
Requires:       %{name} = %{version}-%{release}
Requires:       sblim-testsuite

%description test
SBLIM Base Fsvol Testcase Files for SBLIM Testsuite

%prep
%setup -q
%patch 0 -p1 -b .docdir
%patch 1 -p1 -b .pegasus-interop
%patch 2 -p1 -b .prov-reg-sfcb-systemd

%build
%ifarch s390 s390x ppc ppc64
export CFLAGS="$RPM_OPT_FLAGS -fsigned-char"
%else
export CFLAGS="$RPM_OPT_FLAGS" 
%endif
%configure \
        --disable-static \
        TESTSUITEDIR=%{_datadir}/sblim-testsuite \
        PROVIDERDIR=%{provider_dir}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{provider_dir}/*.la
# shared libraries
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/cmpi" > $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
mv $RPM_BUILD_ROOT/%{_libdir}/libLinux_NFSv4SystemConfigurationUtil.so $RPM_BUILD_ROOT/%{provider_dir}

%files
%doc AUTHORS COPYING DEBUG README README.TEST README.tog-pegasus
%dir %{provider_dir}
%{provider_dir}/*.so
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%files test
%{_datadir}/sblim-testsuite

%global SCHEMA %{_datadir}/%{name}/Linux_NFSv4SystemSetting.mof %{_datadir}/%{name}/Linux_NFSv4SystemConfiguration.mof

%global REGISTRATION %{_datadir}/%{name}/Linux_NFSv4SystemSetting.registration %{_datadir}/%{name}/Linux_NFSv4SystemConfiguration.registration

%pre
%sblim_pre

%post
%sblim_post

%preun
%sblim_preun

%postun -p /sbin/ldconfig

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.0-19
- Add BuildRequires gcc
- Remove Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.0-12
- Update provider registration script to use systemctl to stop/start sfcb
- Use new macros for %%pre/%%post/%%preun from sblim-cmpi-devel

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.0-9
- Use Pegasus root/interop instead of root/PG_Interop
- Fix for unversioned docdir change
  Resolves: #994081

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.0-6
- Fix Source0 URL

* Wed Sep 05 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.0-5
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct  6 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.0-1
- Update to sblim-cmpi-nfsv4-1.1.0
- Remove CIMOM dependencies

* Wed Oct 14 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.0.12-1
- Initial support
