Summary:        Hardware identification and configuration data
Name:           hwdata
Version:        0.378
Release:        1%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/vcrhonek/hwdata
#WARNING: the source file downloads as 'v%%{version}.tar.gz' and MUST be re-named to match the 'Source0' tag.
#Source0:       %%{url}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

%description
hwdata contains various hardware identification and configuration data,
such as the pci.ids and usb.ids databases.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
 
%description    devel
The %{name}-devel package contains files for developing applications that use
%{name}.

%prep
%setup -q
%configure

%build
# nothing to build

%install
make install DESTDIR=%{buildroot} libdir=%{_libdir}

%files
%license COPYING LICENSE
%dir %{_datadir}/%{name}
%{_libdir}/modprobe.d/dist-blacklist.conf
%{_datadir}/%{name}/*

%files devel
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Thu Feb 02 2024 Nan Liu <liunan@microsoft.com> - 0.378-1
- Upgrade to 0.373
- Update License
- Add devel package with pkgconfig file

* Fri Feb 18 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.356-1
- Update source to v0.356

* Fri May 28 2021 Thomas Crain <thcrain@microsoft.com> - 0.341-4
- Replace improper %%{_lib} macro usage with %%{_libdir}

* Mon Mar 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.341-3
- Changed source tarball name.

* Fri Dec 18 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.341-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.

* Tue Nov 03 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.341-1
- Update pci and vendor ids

* Mon Oct 05 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.340-1
- Update pci and vendor ids

* Tue Sep 01 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.339-1
- Update pci, usb and vendor ids

* Tue Aug 04 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.338-1
- Update pci, usb and vendor ids

* Thu Jul 02 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.337-1
- Update pci, usb and vendor ids

* Mon Jun 01 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.336-1
- Update pci and vendor ids

* Mon May 04 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.335-1
- Update pci and vendor ids

* Wed Apr 01 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.334-1
- Updated pci, usb and vendor ids.

* Mon Mar 02 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.333-1
- Updated pci, usb and vendor ids.

* Mon Feb 03 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.332-1
- Updated pci, usb and vendor ids.

* Thu Jan 02 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.331-1
- Updated pci, usb and vendor ids.

* Mon Dec 02 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.330-1
- Updated pci, usb and vendor ids.

* Mon Nov 04 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.329-1
- Updated pci, usb and vendor ids.

* Tue Oct 01 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.328-1
- Updated pci, usb and vendor ids.

* Tue Sep 03 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.327-1
- Updated pci, usb and vendor ids.

* Thu Aug 01 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.326-1
- Updated pci, usb and vendor ids.

* Thu Jun 27 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.325-1
- Updated pci, usb and vendor ids.

* Mon Jun 03 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.324-1
- Updated pci, usb and vendor ids.

* Thu May 02 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.323-1
- Updated pci, usb and vendor ids.

* Tue Apr 02 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.322-1
- Updated pci, usb and vendor ids.

* Tue Mar 05 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.321-1
- Updated pci, usb and vendor ids.

* Mon Feb 04 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.320-1
- Updated pci, usb and vendor ids.

* Wed Jan 02 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.319-1
- Updated pci, usb and vendor ids.

* Mon Dec 03 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.318-1
- Updated pci, usb and vendor ids.

* Thu Nov 01 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.317-1
- Updated pci, usb and vendor ids.

* Mon Oct 01 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.316-1
- Updated pci, usb and vendor ids.

* Mon Sep 03 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.315-1
- Updated pci, usb and vendor ids.

* Thu Aug 02 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.314-1
- Updated pci, usb and vendor ids.

* Mon Jul 02 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.313-1
- Updated pci, usb and vendor ids.

* Wed May 02 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.312-1
- Updated pci, usb and vendor ids.

* Mon Mar 05 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.311-1
- Remove %%clean section
- Remove Group tag
- Updated pci, usb and vendor ids.

* Mon Mar 05 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.310-1
- Updated pci, usb and vendor ids.

* Mon Feb 05 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.309-1
- Updated pci, usb and vendor ids.

* Tue Jan 02 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.308-1
- Updated pci, usb and vendor ids.

* Mon Dec 04 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.307-1
- Updated pci, usb and vendor ids.

* Thu Nov 02 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.306-1
- Updated pci, usb and vendor ids.

* Mon Oct 02 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.305-1
- Updated pci, usb and vendor ids.

* Mon Sep 04 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.304-1
- Updated pci, usb and vendor ids.

* Tue Aug 01 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.303-1
- Updated pci, usb and vendor ids.

* Mon Jul 03 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.302-1
- Updated pci, usb and vendor ids.

* Mon Jun 05 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.301-1
- Updated pci, usb and vendor ids.

* Tue May 09 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.300-1
- Updated pci, usb and vendor ids.

* Mon Apr 03 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.299-1
- Updated pci, usb and vendor ids.

* Mon Mar 06 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.298-1
- Updated pci, usb and vendor ids.

* Mon Feb 06 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.297-1
- Updated pci, usb and vendor ids.

* Tue Jan 03 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.296-1
- Updated pci, usb and vendor ids.

* Mon Dec 12 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.295-1
- Updated pci, usb and vendor ids.

* Wed Nov 02 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.294-1
- Updated pci, usb and vendor ids.

* Tue Oct 04 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.293-1
- Updated pci, usb and vendor ids.

* Mon Aug 29 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.292-1
- Updated pci, usb and vendor ids.

* Tue Jul 26 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.291-1
- Updated pci and vendor ids.

* Wed Jun 22 2016 Michal Minar <miminar@redhat.com> 0.290-1
- Updated pci and vendor ids.

* Wed May 18 2016 Michal Minar <miminar@redhat.com> 0.289-1
- Updated pci and vendor ids.

* Mon Apr 18 2016 Michal Minar <miminar@redhat.com> 0.288-1
- Updated pci, usb and vendor ids.

* Tue Mar 22 2016 Michal Minar <miminar@redhat.com> 0.287-1
- Updated pci, usb and vendor ids.

* Thu Feb 18 2016 Michal Minar <miminar@redhat.com> 0.286-1
- Updated pci, usb and vendor ids.

* Tue Jan 19 2016 Michal Minar <miminar@redhat.com> 0.285-2
- Updated pci, usb and vendor ids.

* Wed Nov 18 2015 Michal Minar <miminar@redhat.com> 0.284-1
- Updated pci and vendor ids.

* Fri Oct 23 2015 Michal Minar <miminar@redhat.com> 0.283-1
- Updated pci, usb and vendor ids.

* Fri Sep 18 2015 Michal Minar <miminar@redhat.com> 0.282-1
- Updated pci, usb and vendor ids.

* Tue Aug 18 2015 Michal Minar <miminar@redhat.com> 0.281-1
- Updated pci, usb and vendor ids.

* Mon Jul 20 2015 Michal Minar <miminar@redhat.com> 0.280-1
- Updated pci and vendor ids.

* Wed Jun 24 2015 Michal Minar <miminar@redhat.com> 0.279-1
- Updated pci, usb and vendor ids.

* Wed May 20 2015 Michal Minar <miminar@redhat.com> 0.278-1
- Update pci, usb and vendor ids.

* Wed Apr 29 2015 Michal Minar <miminar@redhat.com> 0.277-1
- Updated pci, usb and vendor ids.

* Tue Mar 24 2015 Michal Minar <miminar@redhat.com> 0.276-1
- Updated pci, usb and vendor ids.

* Wed Feb 18 2015 Michal Minar <miminar@redhat.com> 0.275-1
- Updated pci, usb and vendor ids.

* Mon Jan 26 2015 Michal Minar <miminar@redhat.com> 0.274-2
- Removed bad entry from usb ids file.

* Mon Jan 19 2015 Michal Minar <miminar@redhat.com> 0.274-1
- Updated pci, usb and vendor ids.

* Thu Dec 18 2014 Michal Minar <miminar@redhat.com> 0.273-1
- Updated pci, usb and vendor ids.

* Tue Nov 25 2014 Michal Minar <miminar@redhat.com> 0.272-1
- Updated pci and vendor ids.

* Sun Oct 26 2014 Michal Minar <miminar@redhat.com> 0.271-1
- Updateed pci and vendor ids.

* Wed Sep 17 2014 Michal Minar <miminar@redhat.com> 0.270-2
- Recreated pnp.ids.

* Wed Sep 17 2014 Michal Minar <miminar@redhat.com> 0.270-1
- Updated pci, usb and vendor ids.

* Mon Aug 18 2014 Michal Minar <miminar@redhat.com> 0.269-1
- Updated pci, usb and vendor ids.

* Mon Jul 21 2014 Michal Minar <miminar@redhat.com> 0.268-1
- Updated pci, usb and vendor ids.

* Mon Jun 16 2014 Michal Minar <miminar@redhat.com> 0.267-1
- Updated pci, and vendor ids.

* Tue May 27 2014 Michal Minar <miminar@redhat.com> 0.266-1
- Updated pci, usb and vendor ids

* Tue Apr 22 2014 Michal Minar <miminar@redhat.com> 0.265-1
- Updated pci, usb and vendor ids.

* Thu Mar 27 2014 Michal Minar <miminar@redhat.com> 0.264-1
- Updated pci and vendor ids.

* Thu Mar 20 2014 Michal Minar <miminar@redhat.com> 0.263-1
- Added Individual Address Blocks file (iab.txt).

* Tue Mar 18 2014 Michal Minar <miminar@redhat.com> 0.262-1
- Update of pci and vendor ids.

* Tue Feb 25 2014 Michal Minar <miminar@redhat.com> 0.261-1
- Update of pci, usb and vendor ids.

* Sun Jan 19 2014 Michal Minar <miminar@redhat.com> 0.260-1
- Update of pci, usb and vendor ids.

* Tue Dec 31 2013 Michal Minar <miminar@redhat.com> 0.259-1
- Update of pci, usb and vendor ids.

* Fri Nov 29 2013 Michal Minar <miminar@redhat.com> 0.258-1
- Update of pci and oui ids.

* Tue Oct 29 2013 Michal Minar <miminar@redhat.com> 0.257-1
- Update of pci, oui and usb ids.

* Sun Sep 22 2013 Michal Minar <miminar@redhat.com> 0.256-1
- Update of pci, oui and usb ids.

* Wed Aug 21 2013 Michal Minar <miminar@redhat.com> 0.255-1
- Update of pci, oui and usb ids.

* Wed Aug 07 2013 Michal Minar <miminar@redhat.com> 0.254-1
- Update of vendor ids.

* Mon Jul 29 2013 Michal Minar <miminar@redhat.com> 0.253-1
- Changelog fix and oui.ids update.

* Sun Jul 21 2013 Michal Minar <miminar@redhat.com> 0.252-1
- Data files update.

* Sat Jul 06 2013 Michal Minar <miminar@redhat.com> 0.250-1
- Data files update.

* Thu Jun 20 2013 Michal Minar <miminar@redhat.com> 0.249-1
- Data files update, pnp.ids included.

* Thu Apr 18 2013 Michal Minar <miminar@redhat.com> 0.248-1
- Data files update

* Wed Mar 27 2013 Michal Minar <miminar@redhat.com> 0.247-1
- Moved blacklist.conf from /etc/modprobe.d to /usr/lib/modprobe.d.
- Renamed it to dist-blacklist.conf.
- Data files update

* Mon Mar 18 2013 Michal Minar <miminar@redhat.com> 0.245-1
- Data files update

* Mon Feb 18 2013 Michal Minar <miminar@redhat.com> 0.244-1
- Data files updated

* Fri Jan 18 2013 Michal Minar <miminar@redhat.com> 0.243-1
- Data files updated

* Fri Dec 07 2012 Michal Minar <miminar@redhat.com> 0.242-1
- Update data files

* Wed Nov 07 2012 Michal Minar <miminar@redhat.com> 0.241-1
- Update data files

* Wed Sep 26 2012 Michal Minar <miminar@redhat.com> 0.240-1
- made use of configure script in prep

* Tue Sep 25 2012 Michal Minar <miminar@redhat.com> 0.239-1
- Update data files

* Thu Aug 23 2012 Adam Jackson <ajax@redhat.com> 0.238-1
- Fix reference specfile to current Fedora style

* Thu Aug 23 2012 Adam Jackson <ajax@redhat.com> 0.235-1
- Update data files
- Remove upgradelist, not needed since kudzu-ectomy

* Mon Aug 08 2011 Karsten Hopp <karsten@redhat.com> 0.233-7.3
- update pci.ids, usb. ids

* Mon May 02 2011 Karsten Hopp <karsten@redhat.com> 0.233-7.2
- update pci.ids with a fix for QLogic Infiniband adapter

* Wed Apr 27 2011 Karsten Hopp <karsten@redhat.com> 0.233-7.1
- update to latest pci.ids, usb.ids

* Fri Jan 28 2011 Karsten Hopp <karsten@redhat.com> 0.233-7
- bump release
- update oui.txt URL
- fix tarball name in spec file
- update usb.ids, out.txt and pci.ids

* Wed Aug 25 2010 Karsten Hopp <karsten@redhat.com> 0.233-1
- update usb.ids, out.txt and pci.ids

* Thu Aug 05 2010 Karsten Hopp <karsten@redhat.com> 0.232-1
- update usb.ids, out.txt and pci.ids (#550020, #611860)
- fix incorrect syntax doc/comment in blacklist.conf (Ville Skyttä, #532802)
- add Acer B243HL and BenQ G2420HDBL (Ville Skyttä, #590787)
- add HP LP2475w and Samsung 2494HM (Ville Skyttä, #595059)

* Tue May 25 2010 Phil Knirsch <pknirsch@redhat.com> 0.230-1
- update usb.ids, out.txt and pci.ids
- Resolves: #584788

* Mon Mar 29 2010 Karsten Hopp <karsten@redhat.com> 0.229-1
- update usb.ids, out.txt and pci.ids for F-13 (#571914)

* Wed Mar 17 2010 Phil Knirsch <pknirsch@redhat.com> 0.228-1
- Blacklist chsc_sch for s390x
- Resolves: #563228

* Tue Feb 23 2010 Dave Airlie <airlied@redhat.com> 0.227-1
- add viafb to blacklist

* Mon Feb 22 2010 Karsten Hopp <karsten@redhat.com> 0.227-1
- update usb.ids, pci.ids, oui.txt
- update license

* Fri Jan 15 2010 Karsten Hopp <karsten@redhat.com> 0.226-1
- update release number

* Fri Jan 15 2010 Karsten Hopp <karsten@redhat.com> 0.225-4
- update usb.ids pci.ids oui.txt

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.225-3.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.225-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Adam Jackson <ajax@redhat.com> 0.225-2
- pnp-dell.patch: Fix Dell's entry in pnp.ids

* Thu Apr 09 2009 Adam Jackson <ajax@redhat.com> 0.224-1
- Update pci.ids, usb.ids, and oui.txt
- Add pnp.ids

* Thu Mar 19 2009 Karsten Hopp <karsten@redhat.com> 0.223-1
- update usb.ids pci.ids oui.txt
- rename /etc/modprobe.d/blacklist to /etc/modprobe.d/blacklist.conf

* Wed Jan 28 2009 Karsten Hopp <karsten@redhat.com> 0.222-1
- update usb.ids pci.ids oui.txt and build for all current releases
  Fixes p.e. #465440

* Wed Jan 21 2009 Karsten Hopp <karsten@redhat.com> 0.221-1
- update usb.ids pci.ids oui.txt

* Tue Dec 02 2008 Karsten Hopp <karsten@redhat.com> 0.220-1
- add new monitor entries from Mandriva hardware database (Thierry Vignaud)
- make generic entries have properly formated frequencies (Thierry Vignaud)
- remove duplicate Dell monitor entries (Thierry Vignaud)
- more vendor name fixes
- fix extra field in 'Compudyne KD-1500N' definition (Thierry Vignaud)
- make Dell monitors case consistent (Thierry Vignaud)
- make all GoldStar monitors have the same vendor name (Thierry Vignaud)
- add URL of git repository
- fix spacing (Thierry Vignaud)
- sort MonitorDB file with LANG=C sort -f -t ";" -k1,2
- add Samsung SyncMaster 2443BWX (Marc van den Dikkenberg)
- add some Lenovo monitors (Im Sza)

* Wed Jul 23 2008 Karsten Hopp <karsten@redhat.com> 0.220-1
- update pci.ids, usb.ids, oui.txt
- MonitorsDB: add some Samsung monitors (Ronald Warsow)
- MonitorsDB: add Dell E1609W (Matt Domsch)
- MonitorsDB: add 7 Dell monitors (Matt Domsch)
- MonitorsDB: add a bunch of Hyundai and ImageQuest monitors

* Mon Jun 09 2008 Karsten Hopp <karsten@redhat.com> 0.219-1
- add BenQ FP2091 monitor (Peter Williams)
- add a bunch of Hyundai and ImageQuest monitors

* Mon Jun 02 2008 Karsten Hopp <karsten@redhat.com> 0.219-1
- update pci.ids, usb.ids, oui.txt
- blacklist snd-pcsp (#448425)

* Mon May 19 2008 Karsten Hopp <karsten@redhat.com> 0.218-1
- add some Acer monitors (Im Sz)

* Tue Apr 01 2008 Karsten Hopp <karsten@redhat.com> 0.217-1
- update pci.ids, oui.txt
- update usb.ids, fixes #439963
- add HP w1907 LCD monitor, fixes #431359
- fix many monitor entries (Stanislav Ievlev, #430276)

* Mon Mar 03 2008 Karsten Hopp <karsten@redhat.com> 0.216-1
- update pci.ids, usb.ids (#431658)

* Tue Jan 29 2008 Phil Knirsch <pknirsch@redhat.com> 0.215-1
- Pull new upstream pci.ids

* Wed Jan 23 2008 Karsten Hopp <karsten@redhat.com> 0.215-1
- add HP W2207 monitor
- add oui.txt, a list of bluetooth device makers

* Fri Jan 18 2008 Karsten Hopp <karsten@redhat.com> 0.214-1
- remove MonitorsDB.generic as it isn't used anywhere
- drop RHEL-5 blacklist patch in -devel

* Tue Jan 15 2008 Karsten Hopp <karsten@redhat.com> 0.213-1
- add many monitor entries (Im Sza, #367111)

* Fri Jan 11 2008 Karsten Hopp <karsten@redhat.com> 0.212-1
- pull new upstream pci.ids, usb.ids
- Resolves: #300831
- added HP TFT5600 LCD Monitor
- Resolves: #250569
- added Acer AL1916W, Eizo L568/L568D, Samsung 795DF
- Resolves: #250582
- Add Samsung 205BW/206BW/225BW/226BW
- Resolves: #250584
- Add Samsung 931BF
- Resolves: #250587

* Sat Dec 22 2007 Karsten Hopp <karsten@redhat.com> 0.209-1
- add Proview 926w monitor (#363091)

* Sat Dec 22 2007 Karsten Hopp <karsten@redhat.com> 0.208-1
- new release
- drop dell-monitors patch, already included in tarball

* Thu Dec 13 2007 Karsten Hopp <karsten@redhat.com> 0.207-3
- fix License tag
- add empty %%build section for fedora-review

* Thu Oct 25 2007 Matt Domsch <Matt_Domsch@dell.com> 0.207-2
- MonitorsDB: add 20 new Dell monitors

* Wed Sep 26 2007 Karsten Hopp <karsten@redhat.com> 0.211-1
- pull new upstream pci.ids, usb.ids

* Thu Sep 20 2007 Karsten Hopp <karsten@redhat.com> 0.210-1
- add pci.id for Chelsio 10GbE Ethernet Adapter
- Resolves: bz #296811

* Wed Sep 19 2007 Karsten Hopp <karsten@redhat.com> 0.209-1
- pull new upstream pci.ids, usb.ids

* Wed Aug 29 2007 Karsten Hopp <karsten@redhat.com> 0.207-1
- update license tag

* Wed Aug 15 2007 Karsten Hopp <karsten@redhat.com> 0.207-1
- pull new upstream pci.ids and rebuild
- Resolves: bz #251732
- Resolves: bz #251734
- Resolves: bz #252195
- Resolves: bz #252196
- Resolves: bz #241274

* Tue Aug 14 2007 Karsten Hopp <karsten@redhat.com> 0.205-1
- add HP TFT5600        #229370

* Mon Jul 09 2007 Karsten Hopp <karsten@redhat.com> 0.205-1
- enable iwl4965 blacklist
- Resolves: bz#245379

* Mon Jun 25 2007 Karsten Hopp <karsten@redhat.com> 0.205-1
- really update pci.ids, update-pciids downloaded an old file
- disable iwl4965 blacklist as it is not approved yet (#245379)

* Mon Jun 25 2007 Karsten Hopp <karsten@redhat.com> 0.202-1
- don't load iwl4965 module automatically
- Resolves: #245379

* Tue Jun 19 2007 Karsten Hopp <karsten@redhat.com> 0.201-1
- add some monitors
- Resolves: #224511
- update pci.ids
- Related: #223105

* Tue Jan 02 2007 Karsten Hopp <karsten@redhat.com> 0.194-1
- Update to latest pci.ids/usb.ids for RHEL5
- Resolves: #220182
  Add some Dell monitors to MonitorDB

* Mon Oct 09 2006 Phil Knirsch <pknirsch@redhat.com> - 0.191-1
- Update to latest pci.ids for RHEL5

* Thu Sep 21 2006 Adam Jackson <ajackson@redhat.com> - 0.190-1
- Add a description for the 'intel' driver.

* Mon Sep 18 2006 Phil Knirsch <pknirsch@redhat.com> - 0.189-1
- Updated usb.ids for FC6

* Mon Sep 11 2006 Phil Knirsch <pknirsch@redhat.com> - 0.188-1
- Update of pci.ids for FC6

* Thu Aug 31 2006 Adam Jackson <ajackson@redhat.com> - 0.187-1
- Fix sync ranges for Samsung SyncMaster 710N (#202344)

* Thu Aug 03 2006 Phil Knirsch <pknirsch@redhat.com> - 0.186-1
- Updated pci.ids once more.

* Tue Jul 25 2006 Phil Knirsch <pknirsch@redhat.com> - 0.185-1
- Added the 17inch Philips LCD monitor entry (#199828)

* Mon Jul 24 2006 Phil Knirsch <pknirsch@redhat.com> - 0.184-1
- Added one more entry for missing Philips LCD monitor (#199828)

* Tue Jul 18 2006 Phil Knirsch <pknirsch@redhat.com> - 0.183-1
- Updated pci.ids before FC6 final (#198994)
- Added several missing Samsung monitors (#197463)
- Included a new inf2mondb.py from Matt Domsch (#158723)

* Tue Jul 11 2006 Adam Jackson <ajackson@redhat.com> - 0.182-1
- Added ast driver description to videodrivers
- Numerous Dell monitor additions (#196734)
- Numerous Belinea monitor additions (#198087)

* Sat Jul  8 2006 Adam Jackson <ajackson@redhat.com> - 0.181-1
- Updated videodrivers to mention i945
- New monitors: Sony CPD-G420 (#145902), Compaq P1110 (#155120).

* Thu May 11 2006 Phil Knirsch <pknirsch@redhat.com> - 0.180-1
- Updated and added some MonitorsDB entries

* Tue May 02 2006 Phil Knirsch <pknirsch@redhat.com> - 0.179-1
- Updated PCI ids from upstream (#180402)
- Fixed missing monitor entry in MonitorsDB (#189446)

* Wed Mar 01 2006 Phil Knirsch <pknirsch@redhat.com> - 0.178-1
- Commented out the VT lines at the end of usb.ids as our tools don't handle
  them properly.

* Fri Feb 24 2006 Bill Nottingham <notting@redhat.com> - 0.177-1
- remove stock videoaliases in favor of driver-specific ones in
  the X driver packages

* Wed Feb 22 2006 Phil Knirsch <pknirsch@redhat.com> - 0.176-1
- More entries from Dell to MonitorsDB (#181008)

* Fri Feb 10 2006 Phil Knirsch <pknirsch@redhat.com> - 0.175-1
- Added a few more entries to MonitorsDB

* Wed Feb 01 2006 Phil Knirsch <pknirsch@redhat.com> - 0.174-1
- Some cleanup and adds to the MonitorDB which closes several db related bugs.

* Tue Dec 13 2005 Bill Nottingham <notting@redhat.com> - 0.173-1
- add some IDs to the generic display entries for matching laptops

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> - 0.172-1
- ditto for radeon

* Fri Nov 18 2005 Jeremy Katz <katzj@redhat.com> - 0.171-1
- r128 -> ati.  should fix the unresolved symbol and kem says its more 
  generally the "right" thing to do

* Wed Nov 16 2005 Bill Nottingham <notting@redhat.com> - 0.170-1
- handle mptsas for migration as well
- move videoaliases file to a subdir

* Fri Sep 16 2005 Bill Nottingham <notting@redhat.com>
- add Iiyama monitor (#168143)

* Tue Sep 13 2005 Bill Nottingham <notting@redhat.com>
- add IBM monitor (#168080)

* Thu Sep  8 2005 Bill Nottingham <notting@redhat.com> - 0.169-1
- remove Cards, pcitable. Add videodrivers

* Fri Sep  2 2005 Dan Williams <dcbw@redhat.com> - 0.168-1
- Add more Gateway monitors

* Fri Sep  2 2005 Dan Williams <dcbw@redhat.com> - 0.167-1
- Add some ADI monitors, one BenQ, and and DPMS codes for two Apples

* Fri Sep  2 2005 Bill Nottingham <notting@redhat.com> - 0.166-1
- add videoaliases file
- remove CardMonitorCombos, as nothing uses it

* Thu Aug 25 2005 Dan Williams <dcbw@redhat.com> - 0.165-1
- Add a bunch of Acer monitors

* Tue Aug  9 2005 Jeremy Katz <katzj@redhat.com> - 0.164-1
- migrate sk98lin -> skge

* Sat Jul 30 2005 Bill Nottingham <notting@redhat.com>
- migrate mpt module names (#161420)
- remove pcitable entries for drivers in modules.pcimap
- switch lone remaining 'Server' entry - that can't work right

* Tue Jul 26 2005 Bill Nottingham <notting@redhat.com>
- add Daytek monitor (#164339)

* Wed Jul 13 2005 Bill Nottingham <notting@redhat.com> - 0.162-1
- remove /etc/pcmcia/config, conflict with pcmcia-cs

* Thu Jul  7 2005 Bill Nottingham <notting@redhat.com> - 0.160-1
- move blacklist to /etc/modprobe.d, require new module-init-tools
- add LG monitors (#162466, #161734)
- add orinoco card (#161696)
- more mptfusion stuff (#107088)

* Thu Jun 23 2005 Bill Nottingham <notting@redhat.com>
- add Samsung monitor (#161013)

* Wed Jun 22 2005 Bill Nottingham <notting@redhat.com> - 0.159-1
- pcitable: make branding happy (#160047)
- Cards: add required blank line (#157972)
- add some monitors
- add JVC CD-ROM (#160907, <richard@rsk.demon.co.uk>)
- add hisax stuff to blacklist (#154799, #159068)

* Mon May 16 2005 Bill Nottingham <notting@redhat.com> - 0.158-1
- add a orinoco card (#157482)

* Thu May  5 2005 Jeremy Katz <katzj@redhat.com> - 0.157-1
- add 20" Apple Cinema Display

* Sun Apr 10 2005 Mike A. Harris <mharris@redhat.com> 0.156-1
- Update SiS entries in Cards/pcitable to match what Xorg X11 6.8.2 supports

* Wed Mar 30 2005 Dan Williams <dcbw@redhat.com> 0.155-1
- Add a boatload of BenQ, Acer, Sony, NEC, Mitsubishi, and Dell monitors

* Wed Mar 30 2005 Dan Williams <dcbw@redhat.com> 0.154-1
- Add Typhoon Speednet Wireless PCMCIA Card mapping to atmel_cs driver

* Mon Mar 28 2005 Bill Nottingham <notting@redhat.com> 0.153-1
- update the framebuffer blacklist

* Wed Mar  9 2005 Bill Nottingham <notting@redhat.com> 0.152-1
- fix qlogic driver mappings, add upgradelist mappings for the modules
  that changed names (#150621)

* Wed Mar  2 2005 Mike A. Harris <mharris@redhat.com> 0.151-1
- Added one hundred billion new nvidia PCI IDs to pcitable and Cards to
  synchronize it with X.Org X11 6.8.2.  (#140601)

* Tue Jan 11 2005 Dan Williams <dcbw@redhat.com> - 0.150-1
- Add Dell UltraSharp 1704FPV (Analog & Digital)

* Sun Nov 21 2004 Bill Nottingham <notting@redhat.com> - 0.148-1
- add Amptron monitors (#139142)

* Wed Nov 10 2004 Bill Nottingham <notting@redhat.com> - 0.147-1
- update usb.ids (#138533)
- migrate dpt_i2o to i2o_block (#138603)

* Tue Nov  9 2004 Bill Nottingham <notting@redhat.com> - 0.146-1
- update pci.ids (#138233)
- add Apple monitors (#138481)

* Wed Oct 20 2004 Bill Nottingham <notting@redhat.com> - 0.145-1
- remove ahci mappings, don't prefer it over ata_piix

* Tue Oct 19 2004 Kristian Høgsberg <krh@redhat.com> - 0.144-1
- update IDs for Cirrus, Trident, C&T, and S3

* Tue Oct 12 2004 Bill Nottingham <notting@redhat.com> - 0.143-1
- add ahci mappings to prefer it over ata_piix
- map davej's ancient matrox card to vesa (#122750)

* Thu Oct  7 2004 Dan Williams <dcbw@redhat.com> - 0.141-1
- Add Belkin F5D6020 ver.2 (802.11b card based on Atmel chipset)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> - 0.140-1
- include /etc/hotplug/blacklist here

* Thu Sep 30 2004 Bill Nottingham <notting@redhat.com> - 0.136-1
- add S3 UniChrome (#131403)
- update pci.ids

* Thu Sep 23 2004 Bill Nottingham <notting@redhat.com> - 0.135-1
- megaraid -> megaraid_mbox

* Wed Sep 22 2004 Bill Nottingham <notting@redhat.com> - 0.134-1
- map ncr53c8xx to sym53c8xx (#133181)

* Fri Sep 17 2004 Bill Nottingham <notting@redhat.com> - 0.132-1
- fix 3Ware 9000 mapping (#132851)

* Tue Sep 14 2004 Kristian Høgsberg <krh@redhat.com> - 0.131-1
- Add python script to check sorting of pci.ids

* Thu Sep  9 2004 Kristian Høgsberg <krh@redhat.com> 0.131-1
- Add pci ids and cards for new ATI, NVIDIA and Intel cards

* Sat Sep  4 2004 Bill Nottingham <notting@redhat.com> 0.130-1
- trim pcitable - now just ids/drivers

* Wed Sep  1 2004 Bill Nottingham <notting@redhat.com> 0.125-1
- pci.ids updates
- remove updsftab.conf.*

* Sun Aug 29 2004 Mike A. Harris <mharris@redhat.com>  0.124-1
- Updates to pcitable/Cards for 'S3 Trio64 3D' cards. (#125866,59956)

* Fri Jul  9 2004 Mike A. Harris <mharris@redhat.com>  0.123-1
- Quick pcitable/Cards update for ATI Radeon and FireGL boards

* Mon Jun 28 2004 Bill Nottingham <notting@redhat.com>
- add Proview monitor (#125853)
- add ViewSonic monitor (#126324)
- add a Concord camera (#126673)

* Wed Jun 23 2004 Brent Fox <bfox@redhat.com> - 0.122-1
- Add Vobis monitor to MonitorsDB (bug #124151)

* Wed Jun 09 2004 Dan Williams <dcbw@redhat.com> - 0.121-1
- add Belkin F5D5020 10/100 PCMCIA card (#125581)

* Fri May 28 2004 Bill Nottingham <notting@redhat.com>
- add modem (#124663)

* Mon May 24 2004 Bill Nottingham <notting@redhat.com> - 0.120-1
- mainly:
  fix upgradelist module for CMPci cards (#123647)
- also:
  add another wireless card (#122676)
  add wireless card (#122625)
  add 1280x800 (#121548)
  add 1680x1050 (#121148)
  add IntelligentStick (#124313)

* Mon May 10 2004 Jeremy Katz <katzj@redhat.com> - 0.119-1
- veth driver is iseries_veth in 2.6

* Wed May  5 2004 Jeremy Katz <katzj@redhat.com> - 0.118-1
- add a wireless card (#122064)
- and a monitor (#121696)

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> 0.117-1
- fix makefile

* Thu Apr 15 2004 Bill Nottingham <notting@redhat.com> 0.116-1
- move updfstab.conf here
- add wireless card (#116865)
- add laptop display panel (#117385)
- add clipdrive (#119928)
- add travelling disk (#119143)
- add NEXDISK (#106782)

* Thu Apr 15 2004 Brent Fox <bfox@redhat.com> 0.115-1
- replace snd-es1960 driver with snd-es1968 in pcitable (bug #120729)

* Mon Mar 29 2004 Bill Nottingham <notting@redhat.com> 0.114-1
- fix entries pointing to Banshee (#119388)

* Tue Mar 16 2004 Bill Nottingham <notting@redhat.com> 0.113-1
- add a Marvell sk98lin card (#118467, <64bit_fedora@comcast.net>)

* Fri Mar 12 2004 Brent Fox <bfox@redhat.com> 0.112-1
- add a Sun flat panel to MonitorsDB (bug #118138)

* Fri Mar  5 2004 Brent Fox <bfox@redhat.com> 0.111-1
- add Samsung monitor to MonitorsDB (bug #112112)

* Mon Mar  1 2004 Mike A. Harris <mharris@redhat.com> 0.110-1
- Added 3Dfx Voodoo Graphics and Voodoo II entries to the Cards database, both
  pointing to Alan Cox's new "voodoo" driver which is now included in XFree86
  4.3.0-62 and later builds in Fedora development.  Mapped their PCI IDs to
  the new Cards entry in pcitable.
- Updated the entries for 3Dfx Banshee

* Mon Feb 23 2004 Bill Nottingham <notting@redhat.com> 0.109-1
- pci.ids and other updates

* Thu Feb 19 2004 Mike A. Harris <mharris@redhat.com> 0.108-1
- Added Shamrock C407L to MonitorsDB for bug (#104920)

* Thu Feb 19 2004 Mike A. Harris <mharris@redhat.com> 0.107-1
- Massive Viewsonic monitor update for MonitorsDB (#84882)

* Fri Feb 13 2004 John Dennis <jdennis@finch.boston.redhat.com> 0.106-1
- fix typo, GP should have been HP

* Thu Jan 29 2004 Bill Nottingham <notting@redhat.com> 0.105-1
- many monitor updates (#114260, #114216, #113993, #113932, #113782,
  #113685, #113523, #111203, #107788, #106526, #63005)
- add some PCMCIA cards (#113006, #112505)

* Tue Jan 20 2004 Bill Nottingham <notting@redhat.com> 0.104-1
- switch sound module mappings to alsa drivers

* Mon Jan 19 2004 Brent Fox <bfox@redhat.com> 0.103-1
- fix tab spacing

* Fri Jan 16 2004 Brent Fox <bfox@redhat.com> 0.102-1
- added an entry for ATI Radeon 9200SE (bug #111306)

* Sun Oct 26 2003 Jeremy Katz <katzj@redhat.com> 0.101-1
- add 1920x1200 Generic LCD as used on some Dell laptops (#108006)

* Thu Oct 16 2003 Brent Fox <bfox@redhat.com> 0.100-1
- add entry for Sun (made by Samsung) monitor (bug #107128)

* Tue Sep 23 2003 Mike A. Harris <mharris@redhat.com> 0.99-1
- Added entries for Radeon 9600/9600Pro/9800Pro to Cards
- Fixed minor glitch in pcitable for Radeon 9500 Pro

* Tue Sep 23 2003 Jeremy Katz <katzj@redhat.com> 0.98-1
- add VMWare display adapter pci id and map to vmware X driver

* Thu Sep 11 2003 Bill Nottingham <notting@redhat.com> 0.97-1
- bcm4400 -> b44

* Sun Sep  7 2003 Bill Nottingham <notting@redhat.com> 0.96-1
- fix provided Dell tweaks (#103892)

* Fri Sep  5 2003 Bill Nottingham <notting@redhat.com> 0.95-1
- Dell tweaks (#103861)

* Fri Sep  5 2003 Bill Nottingham <notting@redhat.com> 0.94-1
- add adaptec pci id (#100844)

* Thu Sep  4 2003 Brent Fox <bfox@redhat.com> 0.93-1
- add an SGI monitor for bug (#74870)

* Wed Aug 27 2003 Bill Nottingham <notting@redhat.com> 0.92-1
- updates from sourceforge.net pci.ids, update pcitable accordingly

* Mon Aug 18 2003 Mike A. Harris <mharris@redhat.com> 0.91-1
- Added HP monitors for bug (#102495)

* Fri Aug 15 2003 Brent Fox <bfox@redhat.com> 0.90-1
- added a sony monitor (bug #101550)

* Tue Jul 15 2003 Bill Nottingham <notting@redhat.com> 0.89-1
- updates from modules.pcimap

* Sat Jul 12 2003 Mike A. Harris <mharris@redhat.com> 0.88-1
- Update MonitorsDB for new IBM monitors from upstream XFree86 bugzilla:
  http://bugs.xfree86.org/cgi-bin/bugzilla/show_bug.cgi?id=459

* Mon Jun  9 2003 Bill Nottingham <notting@redhat.com> 0.87-1
- fusion update

* Mon Jun  9 2003 Jeremy Katz <katzj@redhat.com> 0.86-1
- pci id for ata_piix

* Wed Jun  4 2003 Brent Fox <bfox@redhat.com> 0.85-1
- correct entry for Dell P991 monitor

* Tue Jun  3 2003 Bill Nottingham <notting@redhat.com> 0.84-1
- fix qla2100 mapping (#91476)
- add dell mappings (#84069)

* Mon Jun  2 2003 John Dennis <jdennis@redhat.com>
- Add new Compaq and HP monitors - bug 90570, bug 90707, bug 90575, IT 17231

* Wed May 21 2003 Brent Fox <bfox@redhat.com> 0.81-1
- add an entry for SiS 650 video card (bug #88271)

* Wed May 21 2003 Michael Fulbright <msf@redhat.com> 0.80-1
- Changed Generic monitor entries in MonitorsDB to being in LCD and CRT groups

* Tue May 20 2003 Bill Nottingham <notting@redhat.com> 0.79-1
- pci.ids and usb.ids updates

* Tue May  6 2003 Brent Fox <bfox@redhat.com> 0.78-1
- added a Samsung monitor to MonitorsDB

* Fri May  2 2003 Bill Nottingham <notting@redhat.com>
- add Xircom wireless airo_cs card (#90099)

* Fri Apr 18 2003 Jeremy Katz <katzj@redhat.com> 0.77-1
- add generic framebuffer to Cards

* Mon Mar 17 2003 Mike A. Harris <mharris@redhat.com> 0.76-1
- Updated MonitorsDb for Dell monitors (#86072)

* Tue Feb 18 2003 Mike A. Harris <mharris@redhat.com> 0.75-1
- Change savage MX and IX driver default back to "savage" for the 1.1.27t
  driver update

* Tue Feb 18 2003 Brent Fox <bfox@redhat.com> 0.74-1
- Use full resolution description for Dell laptop screens (bug #80398)

* Thu Feb 13 2003 Mike A. Harris <mharris@redhat.com> 0.73-1
- Updated pcitable and Cards database to fix Savage entries up a bit, and
  change default Savage/MX driver to 'vesa' as it is hosed and with no sign
  of working in time for 4.3.0.  Fixes (#72476,80278,80346,80423,82394)

* Wed Feb 12 2003 Brent Fox <bfox@redhat.com> 0.72-1
- slightly alter the sync rates for the Dell 1503FP (bug #84123)

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 0.71-1
- large pcitable and pci.ids updates
- more tg3, e100

* Mon Feb 10 2003 Mike A. Harris <mharris@redhat.com> 0.69-1
- Updated pcitable and Cards database for new Intel i852/i855/i865 support

* Mon Feb 10 2003 Mike A. Harris <mharris@redhat.com> 0.68-1
- Massive update of all ATI video hardware PCI IDs in pcitable and a fair
  number of additions and corrections to the Cards database as well

* Wed Jan 29 2003 Brent Fox <bfox@redhat.com> 0.67-1
- change refresh rates of sny0000 monitors to use a low common denominator

* Wed Jan 29 2003 Bill Nottingham <notting@redhat.com> 0.66-1
- don't force DRI off on R200 (#82957)

* Fri Jan 24 2003 Mike A. Harris <mharris@redhat.com> 0.65-1
- Added Card:S3 Trio64V2 (Unsupported RAMDAC) entry to pcitable, pci.ids, and
  Cards database to default this particular variant to "vesa" driver (#81659)

* Thu Jan  2 2003 Bill Nottingham <notting@redhat.com> 0.64-1
- pci.ids and associated pcitable updates

* Sun Dec 29 2002 Mike A. Harris <mharris@redhat.com> 0.63-1
- Updates for GeForce 2 Go, GeForce 4 (#80209)

* Thu Dec 12 2002 Jeremy Katz <katzj@redhat.com> 0.62-2
- fix Cards for NatSemi Geode

* Thu Dec 12 2002 Jeremy Katz <katzj@redhat.com> 0.62-1
- use e100 instead of eepro100 for pcmcia

* Mon Nov 25 2002 Mike A. Harris <mharris@redhat.com>
- Complete reconstruction of all Neomagic hardware entries in Cards
  database to reflect current XFree86, as well as pcitable update,
  and submitted cleaned up entries to sourceforge

* Mon Nov  4 2002 Bill Nottingham <notting@redhat.com> 0.61-1
- move pcmcia config file here
- sort MonitorsDB, add some entries, remove dups
- switch some network driver mappings

* Tue Sep 24 2002 Bill Nottingham <notting@redhat.com> 0.48-1
- broadcom 5704 mapping
- aic79xx (#73781)

* Thu Sep  5 2002 Bill Nottingham <notting@redhat.com> 0.47-1
- pci.ids updates
- add msw's wireless card

* Tue Sep  3 2002 Jeremy Katz <katzj@redhat.com> 0.46-1
- Card entries in pcitable need matching in Cards

* Sun Sep  1 2002 Mike A. Harris <mharris@redhat.com> 0.45-1
- Update G450 entry in Cards

* Tue Aug 13 2002 Bill Nottingham <notting@redhat.com> 0.44-1
- fix some of the Dell entries
- add cardbus controller id (#71198)
- add audigy mapping
- add NEC monitor (#71320)

* Tue Aug 13 2002 Preston Brown <pbrown@redhat.com> 0.43-1
- pci.id for SMC wireless PCI card (#67346)

* Sat Aug 10 2002 Mike A. Harris <mharris@redhat.com> 0.42-1
- Change default driver for old S3 based "Miro" card for bug (#70743)

* Fri Aug  9 2002 Preston Brown <pbrown@redhat.com> 0.41-1
- fix tabs in pci.ids
- Change pci ids for the PowerEdge 4 series again...

* Tue Aug  6 2002 Preston Brown <pbrown@redhat.com> 0.39-1
- Dell PERC and SCSI pci.id additions

* Tue Aug  6 2002 Mike A. Harris <mharris@redhat.com> 0.38-1
- Removed and/or invalid entries from Cards database BLOCKER (#70802)

* Mon Aug  5 2002 Mike A. Harris <mharris@redhat.com> 0.37-1
- Changed Matrox G450 driver default options to fix bug (#66697)
- Corrected S3 Trio64V2 bug in Cards file (#66492)

* Tue Jul 30 2002 Bill Nottingham <notting@redhat.com> 0.36-1
- tweaks for Dell Remote Assisstant cards (#60376)

* Fri Jul 26 2002 Mike A. Harris <mharris@redhat.com> 0.35-1
- Updated Cards db for CT69000
- Various ATI cleanups and additions to Cards and pcitable
- Updated S3 Trio3D to default to "vesa" driver (#59956)

* Tue Jul 23 2002 Bill Nottingham <notting@redhat.com> 0.33-1
- Eizo monitor updates (#56080, <triad@df.lth.se>)
- pci.ids updates, corresponding pcitable updates
- pcilint for pcitable 

* Fri Jun 28 2002 Bill Nottingham <notting@redhat.com> 0.32-1
- switch de4x5 back to tulip

* Mon Jun 24 2002 Mike A. Harris <mharris@redhat.com> 0.31-1
- Modified ATI entries in pcitable to be able to autodetect the FireGL 8700
  and FireGL 8800 which both have the same ID, but different subdevice ID's.
  Added entries to Cards database for the 8700/8800 as well.

* Tue May 28 2002 Mike A. Harris <mharris@redhat.com> 0.30-1
- Reconfigured Cards database to default to XFree86 4.x for ALL video
  hardware, since 3.3.6 support is being removed.  Video cards not
  supported natively by 4.x will be changed to use the vesa or vga
  driver, or completely removed as unsupported.

* Wed Apr 17 2002 Michael Fulbright <msf@redhat.com> 0.14-1
- another megaraid variant

* Mon Apr 15 2002 Michael Fulbright <msf@redhat.com> 0.13-1
- fix monitor entry for Dell 1600X Laptop Display Panel

* Fri Apr 12 2002 Bill Nottingham <notting@redhat.com> 0.13-1
- more aacraid

* Tue Apr  9 2002 Bill Nottingham <notting@redhat.com> 0.12-1
- another 3ware, another megaraid

* Fri Apr  5 2002 Mike A. Harris <mharris@redhat.com> 0.11-1
- Added commented out line for some Radeon 7500 cards to Cards database.

* Tue Apr  2 2002 Mike A. Harris <mharris@redhat.com> 0.10-1
- Fixed i830 entry to use driver "i810" not "i830" which doesn't exist

* Mon Apr  1 2002 Bill Nottingham <notting@redhat.com> 0.9-1
- fix rebuild (#62459)
- SuperSavage ids (#62101)
- updates from pci.ids

* Mon Mar 18 2002 Bill Nottingham <notting@redhat.com> 0.8-2
- fix errant space (#61363)

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 0.8-1
- nVidia updates

* Wed Mar 13 2002 Bill Nottingham <notting@redhat.com> 0.7-1
- lots of pcitable updates

* Tue Mar  5 2002 Mike A. Harris <mharris@redhat.com> 0.6-1
- Updated Cards database

* Mon Mar  4 2002 Mike A. Harris <mharris@redhat.com> 0.5-1
- Built new package with updated database files for rawhide.

* Fri Feb 22 2002 Bill Nottingham <notting@redhat.com> 0.3-1
- return of XFree86-3.3.x

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com> 0.1-1
- initial build
