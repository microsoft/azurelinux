Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global provider_dir %{_libdir}/cmpi

Name:           sblim-cmpi-params
Version:        1.3.0
Release:        24%{?dist}
Summary:        SBLIM params instrumentation

License:        EPL
URL:            https://sblim.wiki.sourceforge.net/
Source0:        https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
Patch0:         sblim-cmpi-params-1.2.4-no-abi-params.patch
# Patch1: remove version from docdir
Patch1:         sblim-cmpi-params-1.3.0-docdir.patch
# Patch2: use Pegasus root/interop instead of root/PG_Interop
Patch2:         sblim-cmpi-params-1.3.0-pegasus-interop.patch
# Patch3: call systemctl in provider registration
Patch3:         sblim-cmpi-params-1.3.0-prov-reg-sfcb-systemd.patch

BuildRequires:  sblim-cmpi-devel sblim-cmpi-base-devel
BuildRequires:  gcc
Requires:       sblim-cmpi-base cim-server cim-schema

%description
Standards Based Linux Instrumentation Params Providers

%package        test
Summary:        SBLIM Params Instrumentation Testcases
Requires:       sblim-cmpi-params = %{version}-%{release}
Requires:       sblim-testsuite

%description -n sblim-cmpi-params-test
SBLIM Base Params Testcase Files for SBLIM Testsuite

%prep
%setup -q
%patch 0 -p1 -b .no-abi-params
%patch 1 -p1 -b .docdir
%patch 2 -p1 -b .pegasus-interop
%patch 3 -p1 -b .prov-reg-sfcb-systemd

%build
%configure \
        --disable-static \
        TESTSUITEDIR=%{_datadir}/sblim-testsuite \
        PROVIDERDIR=%{provider_dir}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{provider_dir}/*.la

%files
%doc AUTHORS COPYING DEBUG README README.TEST README.tog-pegasus
%{provider_dir}/*.so
%{_datadir}/%{name}

%files test
%{_datadir}/sblim-testsuite

%global SCHEMA %{_datadir}/%{name}/*.mof
%global REGISTRATION %{_datadir}/%{name}/*.registration

%pre
%sblim_pre

%post
%sblim_post

%preun
%sblim_preun

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-19
- Add BuildRequires gcc
- Remove Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 05 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-12
- Update provider registration script to use systemctl to stop/start sfcb
- Use new macros for %%pre/%%post/%%preun from sblim-cmpi-devel

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-9
- Use Pegasus root/interop instead of root/PG_Interop
- Fix for unversioned docdir change
  Resolves: #994082

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-6
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-3
- Add mofs registration for various CIMOMs

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct  6 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-1
- Update to sblim-cmpi-params-1.3.0
- Remove CIMOM dependencies

* Mon Jun  1 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.6-1
- Initial support
