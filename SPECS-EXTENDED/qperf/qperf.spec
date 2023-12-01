Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           qperf
Summary:        Measure socket and RDMA performance
Version:        0.4.9
Release:        18%{?dist}
License:        GPLv2 or BSD
Source:         http://www.openfabrics.org/downloads/%{name}/%{name}-%{version}.tar.gz
Url:            http://www.openfabrics.org
BuildRequires:  gcc
BuildRequires:  libibverbs-devel >= 1.2.0
BuildRequires:  librdmacm-devel >= 1.0.21
BuildRequires:  perl-interpreter
BuildRequires:  perl-diagnostics
BuildRequires:  perl-POSIX
# RDMA is not currently built on 32-bit ARM: #1484155
ExcludeArch:    %{arm}

%description
Measure socket and RDMA performance.

%prep
%setup -q

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%license COPYING
%_bindir/qperf
%_mandir/man1/qperf.1*

%changelog
* Fri May 28 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.4.9-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add BR: perl-diagnostics, perl-POSIX

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 28 2017 Honggang Li <honli@redhat.com> - 0.4.9-12
- Disable support for ARM32
- Resolves: bz1484155

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 20 2017 Michal Schmidt <mschmidt@redhat.com> - 0.4.9-9
- BuildRequire perl
- Resolves: bz1424224

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 30 2016 Honggang Li <honli@redhat.com> - 0.4.9-7
- Minor fixes.
- Rebuild against latest libibverbs and librdmacm

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Doug Ledford <dledford@redhat.com> - 0.4.9-1
- Update to latest upstream release

* Mon Feb 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.6-8
- Build on ARM, modernise spec

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Doug Ledford <dledford@redhat.com> - 0.4.6-6
- Fix the fact that qperf was using the wrong PF_RDS define now that RDS
  is integrated upstream and its assigned number is no longer temporary

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 0.4.6-4
- Initial import into Fedora

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 0.4.6-3.el6
- Fix failure to build on i686
- Resolves: bz724899

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 0.4.6-2.el6
- Cleanups for pkgwrangler import
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 0.4.6-1.el5
- Update to latest upstream version
- Related: bz518218

* Mon Jun 22 2009 Doug Ledford <dledford@redhat.com> - 0.4.4-3.el5
- Rebuild against libibverbs that isn't missing the proper ppc wmb() macro
- Related: bz506258

* Sun Jun 21 2009 Doug Ledford <dledford@redhat.com> - 0.4.4-2.el5
- Build against non-XRC libibverbs
- Update to ofed 1.4.1 final bits
- Related: bz506097, bz506258

* Sat Apr 18 2009 Doug Ledford <dledford@redhat.com> - 0.4.4-1.el5
- Update to ofed 1.4.1-rc3 version
- Related: bz459652

* Thu Sep 18 2008 Doug Ledford <dledford@redhat.com> - 0.4.1-2
- Add a build flag to silence some warnings

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 0.4.1-1
- Update to the qperf tarball found in the OFED-1.4-beta1 tarball
- Resolves: bz451483

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 0.4.0-1
- Initial import to Red Hat repo management
- Related: bz428197

* Sat Oct 20 2007 - johann@georgex.org
- Initial package
