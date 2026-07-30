# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define _hardened_build 1

Name:           atop
Version:        2.12.1
Release: 2%{?dist}
Summary:        An advanced interactive monitor to view the load on system and process level

License:        GPL-2.0-or-later
URL:            https://www.atoptool.nl
Source0:        https://www.atoptool.nl/download/%{name}-%{version}.tar.gz
Source1:        atop.d

Patch0:         atop-sysconfig.patch

BuildRequires:  gcc
BuildRequires:  zlib-devel
BuildRequires:  ncurses-devel
BuildRequires:  glib2-devel
BuildRequires:  systemd
BuildRequires:  make

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
An advanced interactive monitor for Linux-systems to view the load on 
system-level and process-level.
The command atop has some major advantages compared to other
performance-monitors: 
   - Resource consumption by all processes
   - Utilization of all relevant resources
   - Permanent logging of resource utilization
   - Highlight critical resources
   - Watch activity only
   - Watch deviations only
   - Accumulated process activity per user
   - Accumulated process activity per program
 
%prep
%setup -q
%patch -P 0 -p0 -b .sysconfig

# Correct unit file path
sed -i "s|/etc/default/atop|/etc/sysconfig/atop|g" atop.service

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS $(pkg-config --cflags glib-2.0) -I. -std=gnu17"

%install
install -Dp -m 0755 atop $RPM_BUILD_ROOT%{_bindir}/atop
install -Dp -m 0755 atopconvert $RPM_BUILD_ROOT%{_bindir}/atopconvert
ln -s atop $RPM_BUILD_ROOT%{_bindir}/atopsar
install -Dp -m 0644 man/atop.1 $RPM_BUILD_ROOT%{_mandir}/man1/atop.1
install -Dp -m 0644 man/atopsar.1 $RPM_BUILD_ROOT%{_mandir}/man1/atopsar.1
install -Dp -m 0644 man/atopacctd.8 $RPM_BUILD_ROOT%{_mandir}/man8/atopacctd.8
install -Dp -m 0755 atop.daily $RPM_BUILD_ROOT%{_datadir}/atop/atop.daily
install -Dp -m 0644 atop.default $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/atop
install -Dp -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/atopd
install -Dp -m 0644 atop.service $RPM_BUILD_ROOT%{_unitdir}/atop.service
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/atop
install -Dp -m 0755 atopacctd $RPM_BUILD_ROOT%{_sbindir}/atopacctd
install -Dp -m 0644 atopacct.service $RPM_BUILD_ROOT%{_unitdir}/atopacct.service
#%%if 0%%{?rhel} >= 8 || 0%%{?fedora}
#install -Dp -m 0755 atopgpud $RPM_BUILD_ROOT%%{_sbindir}/atopgpud
#install -Dp -m 0644 atopgpu.service $RPM_BUILD_ROOT%%{_unitdir}/atopgpu.service
#%%endif
install -Dp -m 0644 atop-rotate.* $RPM_BUILD_ROOT%{_unitdir}/

%post
%systemd_post atop.service atopacct.service atop-rotate.timer
#%%if 0%%{?rhel} >= 8 || 0%%{?fedora}
#%%systemd_post atopgpu.service
#%%endif

%preun
%systemd_preun atop.service atopacct.service atop-rotate.timer
#%%if 0%%{?rhel} >= 8 || 0%%{?fedora}
#%%systemd_preun atopgpu.service
#%%endif

%postun
%systemd_postun_with_restart atop.service atopacct.service atop-rotate.timer
#%%if 0%%{?rhel} >= 8 || 0%%{?fedora}
#%%systemd_postun_with_restart atopgpu.service
#%%endif


%files
%if 0%{?rhel}
%doc COPYING
%else
%license COPYING
%endif
%doc README*
%config(noreplace) %{_sysconfdir}/sysconfig/atop
%{_bindir}/atopsar
%{_bindir}/atop
%{_bindir}/atopd
%{_bindir}/atopconvert
%{_mandir}/man1/atop.1.gz
%{_mandir}/man1/atopsar.1.gz
%{_mandir}/man8/atopacctd.8.gz
%attr(0755,root,root) %dir %{_localstatedir}/log/atop
%{_unitdir}/atop*.service
%{_unitdir}/atop*.timer
%{_datadir}/atop/atop.daily
%{_sbindir}/atopacctd
#%%if 0%%{?rhel} >= 8 || 0%%{?fedora}
#%%{_sbindir}/atopgpud
#%%endif

%changelog
* Tue Sep 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.12.1-1
- 2.12.1

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.12.0-1
- 2.12.0

* Mon Mar 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.11.1-1
- 2.11.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jul 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.11.0-1
- 2.11.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.10.0-1
- 2.10.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.9.0-1
- 2.9.0

* Sun Mar 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.8.1-3
- migrated to SPDX license

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.8.1-1
- 2.8.1

* Tue Jan 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.8.0-1
- 2.8.0

* Wed Dec 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.7.1-4
- Include atopacctd man page

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.7.1-1
- 2.7.1
- Drop atopgpud as it requires proprietary NVIDIA drivers.

* Mon Dec 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.7.0-1
- 2.7.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.6.0-6
- Upstream patch to fix service file.

* Tue Mar 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.6.0-5
- Use upstream sysconfig file.

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.0-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.6.0-3
- Don't ship atopgpud on EL-7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 2.6.0-1
- 2.6.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 2.5.1-1
- Fix unit file path.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 03 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.5.0-1
- 2.5.0

* Thu Sep 05 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.0-4
- Package atopacctd.

* Wed Aug 28 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.0-3
- Fix LOGINTERVAL in sysconfig.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.0-1
- 2.4.0: omitting atopgpud until nvidia-ml-py is in Fedora.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 14 2018 Filipe Rosset <rosset.filipe@gmail.com> - 2.3.0-12
- Fix FTBFS rhbz #1603433

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.3.0-10
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 29 2017 Gwyn Ciesla  <limburgher@gmail.com> - 2.3.0-8
- Apply the patch from the previous ENVR.

* Mon Dec 11 2017 Gwyn Ciesla  <limburgher@gmail.com> - 2.3.0-7
- try-restart in cron, not restart, BZ 1524436.

* Fri Dec 08 2017 Gwyn Ciesla  <limburgher@gmail.com> - 2.3.0-6
- Drop obsolete README.fedora.

* Fri Dec 08 2017 Gwyn Ciesla <limburgher@gmail.com> - 2.3.0-5
- Patch to support nvme disks, BZ 1523419.
- Patch to support /etc/sysconfig/atop, BZ 1520475.

* Tue Nov 07 2017 Gwyn Ciesla <limburgher@gmail.com> - 2.3.0-4
- Move from logrotate to upstream script.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Gwyn Ciesla <limburgher@gmail.com> - 2.3.0-1
- 2.3.0, BZ 1436833.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Jon Ciesla <limburgher@gmail.com> - 2.2-1
- Fix logrotate, 1247869
- 2.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May  7 2015 Richard Shaw <hobbes1069@gmail.com> - 2.1-1
- Update to latest upstream release.
- Fixes segmentation faults (BZ#1147145).
- Update spec file to use licence macro where appropriate.
- Modernize spec file and convert to new systemd scriptlets.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Jon Ciesla <limburgher@gmail.com> - 2.0.2-1
- Latest upstream, BZ 916908.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Jon Ciesla <limburgher@gmail.com> - 1.26-8
- Unit file fix, BZ 840942.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Jon Ciesla <limburgher@gmail.com> - 1.26-6
- Fix cron patch for systemd, BZ 821104.

* Fri May 11 2012 Jon Ciesla <limburgher@gmail.com> - 1.26-5
- Re-add atop.log logrotate section.
- Modify cron setup per BZ 445174 comment #6.

* Wed May 09 2012 Jon Ciesla <limburgher@gmail.com> - 1.26-4
- Dropped logrotate, conflicts with atop's logging, BZ 542598.
- Corrected cron config, BZ 819523.

* Fri Apr 13 2012 Jon Ciesla <limburgher@gmail.com> - 1.26-3
- Add hardened build.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Jon Ciesla <limb@jcomserv.net> - 1.26-1
- New upstream, BZ 657207.
- Migrated from sysv to systemd, BZ 659629.
- Modified to respect sysconfig settings, BZ 609124.
- Dropped explicit Requires for ncurses.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 21 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-8
- add bug fixes for #455223 and #455375
  logrotate output error:
  error: atop:prerotate or postrotate without endscript

* Mon May  5 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-7
- add bug fixes for #445174

* Thu Apr  3 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-6
- removed variable DATALIFE from atop.d and atop.crondaily

* Wed Apr  2 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-5
- improved atop.d and atop.crondaily (Manuel Wolfshant)

* Mon Mar 31 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-4
- logical bash bug on atop.d and atop.crondaily 
- implemented security on atop.d and atop.crondaily
- common script for init and cron.daily

* Sat Mar 29 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-3
- deleted duplicate "-p" on spec file (install)
- modified comment about interval on atop.d and atop.crondaily
- removed check atop.log on atop.d and atop.crondaily
- created new section on atop.crondaily

* Thu Mar 27 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-2
- removed atop start on %%post
- atop.crondaily with exit after checking
- created atop.sysconfig with variables
- created atop.d (removed atop.crondaily call from cron.init)

* Thu Mar 27 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.23-1
- update 1.23
- bug on source2 (init file)

* Sun Jan 27 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.22-3
- removed minimal version from requires/build-requires
- corrected variable in atop.crondaily
- corrected comentary in atop.crondaily

* Sun Jan 27 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.22-2
- corrected license tag to GPLv2+
- replaced references to atop (init file)
- rebuild with Fedora mandatory flags (make %%{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS")
- chkconfig and service added at pre/post scriptlets
- improved name in logrotate file configuration
- corrected english description

* Sat Jan 26 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.22-1
- Initial RPM release
