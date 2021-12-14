Name:           perftest
Summary:        IB Performance Tests
Version:        4.4
Release:        4%{?dist}
License:        GPLv2 or BSD
Source:         https://github.com/linux-rdma/perftest/releases/download/4.4-0.29/perftest-4.4-0.29.g817ec38.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/linux-rdma/perftest

BuildRequires:  gcc
BuildRequires:  libibverbs-devel >= 1.2.0
BuildRequires:  librdmacm-devel >= 1.0.21
BuildRequires:  libibumad-devel >= 1.3.10.2
Obsoletes:      openib-perftest < 1.3
ExcludeArch:    s390 s390x %{arm}

%description
Perftest is a collection of simple test programs designed to utilize 
RDMA communications and provide performance numbers over those RDMA
connections.  It does not work on normal TCP/IP networks, only on
RDMA networks.

%prep
%setup -q
find src -type f -iname '*.[ch]' -exec chmod a-x '{}' ';'

%build
%configure
make V=1 %{?_smp_mflags}

%install
for file in ib_{atomic,read,send,write}_{lat,bw} raw_ethernet_{lat,bw}; do
	install -D -m 0755 $file %{buildroot}%{_bindir}/$file
done

%files
%doc README
%license COPYING
%_bindir/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun May 24 2020 Honggang Li <honli@redhat.com> - 4.4-3
- Rebase to upstream release perftest-4.4-0.29

* Sun Apr 12 2020 Honggang Li <honli@redhat.com> - 4.4-2
- Rebase to upstream release perftest-4.4-0.23

* Mon Feb 10 2020 Honggang Li <honli@redhat.com> - 4.4-1
- Rebase to upstream release perftest-4.4-0.11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018  Honggang Li <honli@redhat.com> - 4.2-3
- Rebase to latest upstream release v4.2-0.8
- BuildRequires gcc
- Resolves: bz1605400

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018  Honggang Li <honli@redhat.com> - 4.2-1
- Rebase to latest upstream release V4.2-0.5
- Resolves: bz1568309

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 29 2016 Honggang Li <honli@redhat.com> - 3.0-1
- Update to latest upstream

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.2-1
- Update to 2.2-17

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Doug Ledford <dledford@redhat.com> - 2.0-1
- Update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 1.3.0-2
- Update to latest upstream release
- Initial import into Fedora
- Remove runme from docs section (review item)
- Improve description of package (review item)

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.3.0-1
- Update to latest upstream release (1.2.3 -> 1.3.0)
- Strip rocee related code out of upstream update
- Add a buildrequires on libibumad because upstream needs it now
- Fix lack of build on i686
- Related: bz725016
- Resolves: bz724896

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2.3-3.el6
- More minor pkgwrangler cleanups
- Related: bz543948

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2.3-2.el6
- Fixes for pkgwrangler review
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 1.2.3-1.el5
- Update to latest upstream version
- Related: bz518218

* Mon Jun 22 2009 Doug Ledford <dledford@redhat.com> - 1.2-14.el5
- Rebuild against libibverbs that isn't missing the proper ppc wmb() macro
- Related: bz506258

* Sun Jun 21 2009 Doug Ledford <dledford@redhat.com> - 1.2-13.el5
- Update to ofed 1.4.1 final bits
- Rebuild against non-XRC libibverbs
- Related: bz506097, bz506258

* Sat Apr 18 2009 Doug Ledford <dledford@redhat.com> - 1.2-12.el5
- Update to ofed 1.4.1-rc3 version
- Remove dead patch
- Related: bz459652

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 1.2-11
- Upstream has updated the tarball without updating the version, so we
  grabbed the one from the OFED-1.3.2-20080728.0355 tarball
- Resolves: bz451481

* Wed Apr 09 2008 Doug Ledford <dledford@redhat.com> - 1.2-10
- Fix the fact that the itc clock on ia64 may be a multiple of the cpu clock
- Resolves: bz433659

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 1.2-9
- Update to OFED 1.3 final bits
- Related: bz428197

* Sun Jan 27 2008 Doug Ledford <dledford@redhat.com> - 1.2-8
- Split out to separate package (used to be part of openib package)
- Related: bz428197

