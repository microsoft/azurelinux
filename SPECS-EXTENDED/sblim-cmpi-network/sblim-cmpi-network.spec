Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global provider_dir %{_libdir}/cmpi

Name:           sblim-cmpi-network
Version:        1.4.0
Release:        26%{?dist}
Summary:        SBLIM Network Instrumentation

License:        EPL
URL:            https://sblim.wiki.sourceforge.net/
Source0:        https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2

Patch0:         sblim-cmpi-network-1.4.0-network-devices-arbitrary-names-support.patch
# Patch1: remove version from docdir
Patch1:         sblim-cmpi-network-1.4.0-docdir.patch
# Patch2: use Pegasus root/interop instead of root/PG_Interop
Patch2:         sblim-cmpi-network-1.4.0-pegasus-interop.patch
# Patch3: call systemctl in provider registration
Patch3:         sblim-cmpi-network-1.4.0-prov-reg-sfcb-systemd.patch

BuildRequires:  perl-generators
BuildRequires:  sblim-cmpi-base-devel >= 1.5 sblim-cmpi-devel
BuildRequires:  gcc
Requires:       sblim-cmpi-base >= 1.5 cim-server cim-schema

%description
Standards Based Linux Instrumentation Network Providers

%package        devel
Summary:        SBLIM Network Instrumentation Header Development Files
Requires:       %{name} = %{version}-%{release}

%description    devel
SBLIM Base Network Development Package

%package        test
Summary:        SBLIM Network Instrumentation Testcases
Requires:       sblim-cmpi-network = %{version}-%{release}

%description    test
SBLIM Base Network Testcase Files for SBLIM Testsuite

%prep
%setup -q
%patch 0 -p1 -b .network-devices-arbitrary-names-support
%patch 1 -p1 -b .docdir
%patch 2 -p1 -b .pegasus-interop
%patch 3 -p1 -b .prov-reg-sfcb-systemd

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

%files
%doc AUTHORS COPYING DEBUG README README.TEST README.tog-pegasus
%{_datadir}/%{name}
%{_libdir}/*.so.*
%{provider_dir}/*.so
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%files devel
%{_includedir}/*
%{_libdir}/*.so

%files test
%{_datadir}/sblim-testsuite

%global SCHEMA %{_datadir}/%{name}/Linux_Network.mof

%global REGISTRATION %{_datadir}/%{name}/Linux_Network.registration

%pre
%sblim_pre

%post
%sblim_post

%preun
%sblim_preun

%postun -p /sbin/ldconfig

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.0-26
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.0-21
- Add BuildRequires gcc
- Remove Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.0-14
- Update provider registration script to use systemctl to stop/start sfcb
- Use new macros for %%pre/%%post/%%preun from sblim-cmpi-devel
- Fix packaging of -test

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.0-11
- Use Pegasus root/interop instead of root/PG_Interop
- Fix for unversioned docdir change
  Resolves: #994079

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.4.0-9
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.0-7
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.0-5
- Add support for arbitrary names of network devices in Linux_NetworkPortImplementsIPEndpoint
  association
  Resolves: #682386
- Remove macros from changelog, register to sfcb

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct  6 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.4.0-2
- de-registering the providers properly in %%pre and %%preun

* Wed Oct  6 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.0-1
- Update to sblim-cmpi-network-1.4.0
- Remove CIMOM dependencies

* Thu Aug 13 2009 Srinivas Ramanatha <srinivas_ramanatha@dell.com> - 1.3.8-2
- modified the spec file to fix some rpmlint warnings

* Tue May 26 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.8-1
- Initial support
