Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           iw
Version:        6.7
Release:        1%{?dist}
Summary:        A nl80211 based wireless configuration tool

License:        ISC
URL:            https://wireless.kernel.org/en/users/Documentation/iw
Source0:        https://www.kernel.org/pub/software/network/iw/iw-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  kernel-headers >= 2.6.24 
BuildRequires:  libnl3-devel
BuildRequires:  pkgconfig      

%description
iw is a new nl80211 based CLI configuration utility for wireless devices.
Currently you can only use this utility to configure devices which
use a mac80211 driver as these are the new drivers being written - 
only because most new wireless devices being sold are now SoftMAC.


%prep
%setup -q


%build
export CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}


%files
%license COPYING
%{_sbindir}/%{name}
%{_datadir}/man/man8/iw.*


%changelog
* Thu Feb 22 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.7-1
- Auto-upgrade to 6.7 - Azure Linux 3.0 Upgrades

* Tue Oct 18 2022 Henry Li <lihl@microsoft.com> - 5.9-1
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 05 2019 John W. Linville <linville@redhat.com> - 5.4-1
- Update to 5.4 from upstream

* Fri Aug 16 2019 John W. Linville <linville@redhat.com> - 5.3-1
- Update to 5.3 from upstream

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 John W. Linville <linville@redhat.com> - 5.0.1-1
- Update to 5.0.1 from upstream

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 John W. Linville <linville@redhat.com> - 4.14-6
- Update URL for package header

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14-5
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 4.14-3
- Build with linker flags from redhat-rpm-config

* Fri Jan 05 2018 John W. Linville <linville@redhat.com> - 4.14-2
- Fixup bogus date in the changelog...

* Fri Jan 05 2018 John W. Linville <linville@redhat.com> - 4.14-1
- Update to 4.14

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 02 2017 Michael Cronenworth <mike@cchtml.com> - 4.9-1
- Update to 4.9

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Apr 04 2016 John W. Linville <linville@redhat.com> - 4.3-1
- Update to 4.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jul 18 2015 Adel Gadllah <adel.gadllah@gmail.com> - 4.1-1
- Update to 4.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb  4 2015 John W. Linville <linville@redhat.com> 3.15-3
- Use %%license instead of %%doc for file containing license information

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 John W. Linville <linville@redhat.com> 3.15-1
- Update to 3.15
- Move /sbin/iw to /usr/sbin/iw

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 John W. Linville <linville@redhat.com> 3.14-1
- Update to 3.14
- Correct some bogus dates in the changelog

* Tue Nov 12 2013 Adel Gadllah <adel.gadllah@gmail.com> 3.11-1
- Update to 3.11

* Sat Nov 09 2013 Xose Vazquez Perez <xose.vazquez@gmail.com> 3.10-3
- Link with libnl3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May  6 2013 John W. Linville <linville@redhat.com> 3.10-2
- Update URL for source download

* Mon May  6 2013 John W. Linville <linville@redhat.com> 3.10-1
- Update to 3.10

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 John W. Linville <linville@redhat.com> 3.8-1
- Update to 3.8

* Wed Oct 17 2012 John W. Linville <linville@redhat.com> 3.7-1
- Update to 3.7

* Mon Aug 13 2012 John W. Linville <linville@redhat.com> 3.6-1
- Update to 3.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 John W. Linville <linville@redhat.com> 3.5-1
- Update to 3.5

* Wed Jun 13 2012 John W. Linville <linville@redhat.com> 3.4-1
- Update to 3.4

* Wed Jan 18 2012 John W. Linville <linville@redhat.com> 3.3-1
- Update to 3.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 John W. Linville <linville@redhat.com> 3.2-1
- Update to 3.2

* Wed Sep 14 2011 John W. Linville <linville@redhat.com> 3.1-1
- Update to 3.1

* Sun Mar 13 2011 Adel Gadllah <adel.gadllah@gmail.com> 0.9.22-1
- Update to 0.9.22

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.9.21-2
- Rebuilt for gcc bug 634757

* Sun Sep 26 2010 Adel Gadllah <adel.gadllah@gmail.com> 0.9.21-1
- Update to 0.9.21

* Wed Jul 14 2010 John W. Linville <linville@redhat.com> 0.9.20-1
- Update to 0.9.20

* Thu Jan 14 2010 John W. Linville <linville@redhat.com> 0.9.19-2
- Correct license tag from BSD to ISC

* Thu Jan 14 2010 John W. Linville <linville@redhat.com> 0.9.19-1
- Update to 0.9.19

* Mon Dec 21 2009 John W. Linville <linville@redhat.com> 0.9.18-4
- Remove unnecessary explicit Requires of libnl -- oops!

* Mon Dec 21 2009 John W. Linville <linville@redhat.com> 0.9.18-3
- Add libnl to Requires

* Fri Dec 18 2009 John W. Linville <linville@redhat.com> 0.9.18-2
- BuildRequires kernels-headers instead of kernel-devel

* Wed Dec  2 2009 John W. Linville <linville@redhat.com> 0.9.18-1
- Update to 0.9.18

* Thu Oct  1 2009 John W. Linville <linville@redhat.com> 0.9.17-3
- Install in /sbin

* Fri Sep  4 2009 John W. Linville <linville@redhat.com> 0.9.17-2
- Revert "separate commands into sections", section type conflicts on ppc64

* Fri Sep  4 2009 John W. Linville <linville@redhat.com> 0.9.17-1
- Update to 0.9.17

* Mon Aug 17 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.16-1
- Update to 0.9.16

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.15-1
- Update to 0.9.15

* Wed May 13 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.14-1
- Update to 0.9.14

* Sat May  2 2009 John W. Linville <linville@redhat.com> 0.9.13-1
- Update to 0.9.13

* Wed Apr 15 2009 John W. Linville <linville@redhat.com> 0.9.12-1
- Update to 0.9.12

* Mon Apr  6 2009 John W. Linville <linville@redhat.com> 0.9.11-1
- Update to 0.9.11

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.7-1
- Update to 0.9.7

* Sun Oct 26 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.6-1
- Update to 0.9.6

* Sun Sep 28 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.5-3
- Use offical tarball

* Sun Sep 28 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.5-2
- Fix BuildRequires

* Sun Sep 28 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.5-1
- Update to 0.9.5

* Tue Jul 22 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.0-0.3.20080703gitf6fc7dc
- Add commitid to version
- Use versioned buildrequires for kernel-devel

* Thu Jul 3 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.0-0.2.20080703git
- Add tarball instructions
- Fix install
- Fix changelog

* Thu Jul 3 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.0-0.1.20080703git
- Initial build
