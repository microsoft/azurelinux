Summary:	Tool to translate x86-64 CPU Machine Check Exception data
Name:		mcelog
Version:	168
Release:	3%{?dist}
License:	GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://github.com/andikleen/mcelog
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# note that this source OVERRIDES the one on the tarball above!
Source1:	mcelog.conf
ExclusiveArch:	i686 x86_64
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires:  gcc
BuildRequires: systemd

%description
mcelog is a utility that collects and decodes Machine Check Exception data
on x86-32 and x86-64 systems.

%prep
%autosetup

%build
%make_build CFLAGS="$RPM_OPT_FLAGS -fpie -pie"

%install
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{5,8}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
install -p -m755 mcelog $RPM_BUILD_ROOT/%{_sbindir}/mcelog
install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/mcelog.conf
install -p -m755 triggers/cache-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/cache-error-trigger
install -p -m755 triggers/dimm-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/dimm-error-trigger
install -p -m755 triggers/page-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/page-error-trigger
install -p -m755 triggers/socket-memory-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/socket-memory-error-trigger
install -p -m644 mcelog.service $RPM_BUILD_ROOT%{_unitdir}/mcelog.service
install -p -m644 mcelog*.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -p -m644 mcelog*.5 $RPM_BUILD_ROOT/%{_mandir}/man5/

%post
%systemd_post mcelog.service

%preun
%systemd_preun mcelog.service

%postun
%systemd_postun_with_restart mcelog.service

%files
%license LICENSE
%{_sbindir}/mcelog
%dir %{_sysconfdir}/mcelog
%{_sysconfdir}/mcelog/triggers
%config(noreplace) %{_sysconfdir}/mcelog/mcelog.conf
%{_unitdir}/mcelog.service
%{_mandir}/*/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 168-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3:168-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 24 2020 Nicolas Chauvet <kwizart@gmail.com> - 3:168-1
- Update to 168

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:153-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:153-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:153-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:153-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:153-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 21 2017 Prarit Bhargava <prarit@redhat.com> - 3:153-1
- Update to v153

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:137-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:137-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:137-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 26 2016 Adam Williamson <awilliam@redhat.com> - 3:137-1
- update to latest upstream release tag

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:119-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3:119-1
- Update to latest upstream tag
- Drop cron job (#1066659)
- Remove double starting of daemon

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:101-2.9bfaad8f92c5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 18 2014 Prarit Bhargava <prarit@redhat.com> 3:101-1.9bfaad8f92c5
- Update to 101 (#1175832)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2:1.0-0.13.f0d7654
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2:1.0-0.12.f0d7654
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.11.f0d7654
- remaining scriptlets replaced with new systemd macros (#850199)

* Mon Aug 12 2013 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.10.f0d7654
- updated to latest mcelog
- removed mcelog-fix-trigger-path-and-cacheing.patch. AFAICT triggers are
  correctly installed
- added mcelog-disable-cron-job.patch as mcelog runs in daemon mode by
  default in Fedora
* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.0-0.9.6e4e2a00
- Fix FBTFS, modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.8.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.7.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.6.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Jon Ciesla <limburgher@gmail.com> - 2:1.0-0.5.6e4e2a00
- Merge review fixes, BZ 226132.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.4.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.3.6e4e2a00
- Updated sources to deal with various warning issues [701083] [704302]
- Update URL for new location of Andi's mcelog tree
- Update n-v-r to include latest git hash

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.3.pre3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Jon Masters <jcm@redhat.com> 2:1.0-0.2.pre3
- Rework mcelog to use daemon mode and systemd.

* Tue Nov 09 2010 Jon Masters <jcm@redhat.com> 2:1.0-0.1.pre3
- Bump epoch and use standard Fedora Packaging Guidelines for NVR.
- Switch to using signed bz2 source and remove dead patch.

* Fri Sep 17 2010 Dave Jones <davej@redhat.com> 1:1.0pre3-0.1
- Update to upstream mcelog-1.0pre3

* Mon Oct 05 2009 Orion Poplawski <orion@cora.nwra.com> - 1:0.9pre1-0.1
- Update to 0.9pre1
- Update URL
- Add patch to update mcelog kernel record length (bug #507026)

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 0.7-5
- Fix %%install for new buildroot cleanout.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.7-2
- fix license tag
- clean this package up

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.7-1.22
- Autorebuild for GCC 4.3

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- Rebuild.

* Fri Jun 30 2006 Dave Jones <davej@redhat.com>
- Rebuild. (#197385)

* Wed May 17 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.7
- Change frequency to hourly instead of daily.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Wed Feb  8 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.6

* Mon Dec 19 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.5

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Wed Feb  9 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.4

* Thu Jan 27 2005 Dave Jones <davej@redhat.com>
- Initial packaging.

