Name:             powertop
Version:          2.13
Release:          3%{?dist}
Summary:          Power consumption monitor

License:          GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:              https://01.org/powertop/
Source0:          https://github.com/fenrus75/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:          powertop.service

# Sent upstream
Patch0:           powertop-2.7-always-create-params.patch
Patch1:           0001-ncurses.patch
BuildRequires:    gettext-devel, ncurses-devel, pciutils-devel, zlib-devel, libnl3-devel
BuildRequires:    automake, libtool, systemd, autoconf-archive
BuildRequires:    gcc, gcc-c++
Requires(post):   systemd, coreutils
Requires(preun):  systemd
Requires(postun): systemd
Provides:         bundled(kernel-event-lib)

%description
PowerTOP is a tool that finds the software component(s) that make your
computer use more power than necessary while it is idle.

%prep
%setup -q
%patch 0 -p1 -b .always-create-params
%patch 1 -p1

echo "v%{version}" > version-long
echo '"v%{version}"' > version-short

%build
# workaround for rhbz#1826935
autoreconf -fi || autoreconf -fi
%configure
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -Dd %{buildroot}%{_localstatedir}/cache/powertop
touch %{buildroot}%{_localstatedir}/cache/powertop/{saved_parameters.powertop,saved_results.powertop}
%find_lang %{name}

# Systemd
install -Dpm 644 %{SOURCE1} %{buildroot}%{_unitdir}/powertop.service

%preun
%systemd_preun powertop.service

%postun
%systemd_postun_with_restart powertop.service

%post
%systemd_post powertop.service
# Hack for powertop not to show warnings on first start
touch %{_localstatedir}/cache/powertop/{saved_parameters.powertop,saved_results.powertop} &> /dev/null || :

%files -f %{name}.lang
%doc COPYING README.md README.traceevent CONTRIBUTE.md TODO
%dir %{_localstatedir}/cache/powertop
%ghost %{_localstatedir}/cache/powertop/saved_parameters.powertop
%ghost %{_localstatedir}/cache/powertop/saved_results.powertop
%{_sbindir}/powertop
%{_mandir}/man8/powertop.8*
%{_unitdir}/powertop.service
%{_datadir}/bash-completion/completions/powertop

%changelog
* Thu Jun 23 2022 Ahmed Badawi <ahmedbadawi@microsoft.com> - 2.13-3
- Added patch to fix compilation with ncurses 6.3
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.13-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Jun 15 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.13-1
- New version
  Resolves: rhbz#1843773
- Dropped coverity-fixes patch (upstreamed)

* Wed May 13 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.12-2
- Fixed two new issues found by coverity

* Wed Apr 22 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.12-1
- New version
  Resolves: rhbz#1820409

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 10 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.11-2
- Fixed version display
  Resolves: rhbz#1760121

* Mon Sep 30 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.11-1
- New version
  Resolves: rhbz#1756322
- Changed source URL to github, which seems to be the most quickly updated source
- Used automake
- Dropped fix-vert-scrolling patch (upstreamed)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 21 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10-2
- Fixed vertical scrolling

* Mon Mar 18 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10-1
- New version
  Resolves: rhbz#1689490
- Updated URL
- Dropped upstreamed patches

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-10
- Fix -C and -r to take optional arguments

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-8
- Use intel_cpu only if APERF MSR is supported, it fixes powertop on KVM
  (by intel-cpu-check-aperf patch)

* Fri May  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-7
- Added support for Intel GLK platforms (by intel-glk-support patch)
- Added support for Intel CNL-U/Y platforms (by intel-cnluy-support patch)
- Fixed problem with some C-states overwriting others
  (by cstates-rewrite-fix patch)

* Fri Apr 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-6
- Made post scriptlet not to fail
  Resolves: rhbz#1569722

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.9-5
- Add gcc, gcc-c++ to BuildRequires

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-1
- New version
  Resolves: rhbz#1454519
- Dropped pthreads-cflags-fix and potential-segfaults patches (both upstreamed)
- Updated source URL

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 30 2016 Ondřej Lysoněk <olysonek@redhat.com> - 2.8-3
- Fixed some potential sources of segfaults
  Resolves: rhbz#1352708

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-1
- New version
  Resolves: rhbz#1279872
- Dropped tunable-overflow-fix, auto-tune-crash-fix, navigate-hint
  patches (all upstreamed)
- Dropped bytrail-no-c7 patch (following upstream)
- Fixed linkage with pthreads (by pthreads-cflags-fix patch)
- Added bundled(kernel-event-lib)
  Resolves: rhbz#1041323

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May  6 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-5
- Fixed crash on Baytrail CPUs (by bytrail-no-c7 patch)
  Resolves: rhbz#1208600

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.7-4
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 11 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-3
- Added hint how to navigate through panes, (by navigate-hint patch)
  Resolves: rhbz#1191112

* Fri Jan 30 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-2
- Fixed crash when running with --auto-tune (by auto-tune-crash-fix patch)
  Resolves: rhbz#1187452

* Tue Nov 25 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-1
- New version
  Resolves: rhbz#1167726
- De-fuzzified patches
- Dropped man-fix patch (upstreamed)
- Added powertop autotuner oneshot service

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.1-1
- New version
  Resolves: rhbz#1100724
- Dropped ondemand-check patch (upstream dropped the functionality)

* Tue Mar 25 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5-2
- Fixed buffer overflow in cpufreq tunables on systems with many CPUs
  (by tunable-overflow-fix patch)

* Mon Nov 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5-1
- New version
  Resolves: rhbz#1034113
- Dropped unlimit-fds, fd-limit-err, reg-net-params  patches (all upstreamed)

* Tue Oct 29 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4-6
- Fixed some possible unregistered parameters errors
  Resolves: rhbz#947425

* Thu Oct 10 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4-5
- New version of unlimit-fds patch
- Fixed error message if FDs limit is reached (by fd-limit-err patch)

* Fri Sep 20 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4-4
- Unlimit FDs (by unlimit-fds patch) and dropped the fd-limit-err patch

* Thu Sep 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4-3
- Printed friendly error message if the system is running out
  of FDs (by fd-limit-err patch)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4-1
- New version
  Resolves: rhbz#987404

* Fri Jun 28 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-4
- Added check if ondemand governor is applicable (by ondemand-check patch)
  Resolves: rhbz#697273

* Tue Jun 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-3
- Added workload option to the man page

* Wed Apr 10 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-2
- Added post requirements for coreutils

* Wed Mar 20 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-1
- New version
  Resolves: rhbz#923729
- Dropped fix-crash-on-readonly-fs, reduce-syscalls,
  gpu-wiggle-fix patches (upstreamed)
- Dropped version-fix patch (not needed)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dan Horák <dan@danny.cz> - 2.2-6
- rebuilt again for fixed soname in libnl3

* Sun Jan 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.2-5
- Rebuilt for libnl3

* Mon Jan 14 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-4
- Reduced number of useless syscalls (reduce-syscalls patch) and
  fixed gpu wiggle (gpu-wiggle-fix patch)
  Resolves: rhbz#886185

* Sun Dec  2 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-3
- Updated version to show 2.2 (by version-fix patch)

* Wed Nov 28 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-2
- Fixed crash when writing report on readonly filesystem
  (fix-crash-on-readonly-fs patch)

* Fri Nov 23 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-1
- New version
  Resolves: rhbz#877373
- Dropped html-escape patch (not needed)

* Thu Aug 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1-2
- Removed left over object files

* Thu Aug 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1-1
- New version
- Removed patches (all upstreamed): show-watts-only-if-discharging,
  valid-html-output, factor-out-powertop-init, catch-fstream-errors

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0-3
- Catch fstream exceptions
  Resolves: rhbz#832497

* Mon May 21 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0-2
- Fixed segfault during calibration
  Resolves: rhbz#823502
- Used macro optflags instead of variable RPM_OPT_FLAGS

* Wed May 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0-1
- New version
  Resolves: rhbz#821144
- Dropped patches: unknown-readings-fix (upstreamed), compile-fix (upstreamed),
  power-supply-add-power-now-support (upstreamed),
  html-print-commands (upstreamed), add-power-supply-class-support (obsoleted),
  power-supply-units-fix (obsoleted)
- Updated patches: show-watts-only-if-discharging patch (sent upstream),
  html-escape patch
- Added patch: valid-html-output (sent upstream)

* Tue Apr 17 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-9
- Show power consumption only if discharging
  Resolves: rhbz#811949

* Tue Apr 03 2012 Jan Kaluza <jkaluza@redhat.com> - 1.98-8
- Escape scripts in HTML output

* Mon Mar 26 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-7
- Print commands which reproduce the tunings into html log (html-print-commands patch)

* Wed Mar  7 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-6
- Fixed power_supply units
  Resolves: rhbz#800814

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98-5
- Rebuilt for c++ ABI breakage

* Fri Feb 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-4
- Backported support for power_supply class
  (add-power-supply-class-support patch)
- Added support for POWER_NOW readings
  (power-supply-add-power-now-support patch)
  Resolves: rhbz#796068

* Tue Jan 10 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-3
- Fixed 'unknown' readings from ACPI meters
  Resolves: rhbz#770289
- Fixed compilation on f17

* Fri Dec  2 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-2
- Always create params file
  Resolves: rhbz#698020
- Added cache files

* Wed May 25 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-1
- New version

* Wed Mar 23 2011 Dan Horák <dan[at]danny.cz> - 1.97-2
- csstoh should return 0

* Tue Feb 15 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.97-1
- New version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.13-2
- Fixed sigwinch handling (#644800)
- Readded strncpy patch as strncpy is safer than strcpy
- Print all P-states in dump mode
- Added explicit requires for pcituils (#653560)
- Output error in interactive mode if there is no tty (#657212)
- Do not suggest ondemand when p4-clockmod scaling driver is used (#497167)
- Fixed rpmlint warning about mixed tabs and spaces

* Wed Aug 25 2010 Adam Jackson <ajax@redhat.com> 1.13-1
- powertop 1.13

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Adam Jackson <ajax@redhat.com> 1.11-1
- powertop 1.11

* Thu Nov 20 2008 Adam Jackson <ajax@redhat.com>
- Spec only change, fix URL.

* Thu Nov  6 2008 Josh Boyer <jwboyer@gmail.com> - 1.10-1
- Update to latest release
- Drop upstreamed patch

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.9-4
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.9-3
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Adam Jackson <ajax@redhat.com> 1.9-2
- Use full path when invoking hciconfig. (Ville Skyttä, #426721)

* Mon Dec 10 2007 Josh Boyer <jwboyer@gmail.com> 1.9-1
- Update to latest release

* Mon Aug 20 2007 Josh Boyer <jwboyer@jdub.homelinux.org> 1.8-1
- Update to latest release

* Mon Jul 23 2007 Bill Nottingham <notting@redhat.com> 1.7-4
- add patch to allow dumping output to stdout

* Mon Jul 09 2007 Adam Jackson <ajax@redhat.com> 1.7-3
- powertop-1.7-strncpy.patch: Use strncpy() to avoid stack smash. Patch from
  Till Maas. (#246796)

* Thu Jul 05 2007 Adam Jackson <ajax@redhat.com> 1.7-2
- Don't suggest disabling g-p-m.  Any additional power consumption is more
  than offset by the ability to suspend.

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.7-1
- powertop 1.7.

* Mon Jun 11 2007 Adam Jackson <ajax@redhat.com> 1.6-1
- powertop 1.6.

* Tue May 29 2007 Adam Jackson <ajax@redhat.com> 1.5-1
- powertop 1.5.

* Mon May 21 2007 Adam Jackson <ajax@redhat.com> 1.3-1
- powertop 1.3.

* Tue May 15 2007 Adam Jackson <ajax@redhat.com> 1.2-1
- powertop 1.2.  Fixes power reports on machines that report power in Amperes
  instead of Watts.

* Sun May 13 2007 Adam Jackson <ajax@redhat.com> 1.1-1
- powertop 1.1.

* Fri May 11 2007 Adam Jackson <ajax@redhat.com> 1.0-1
- Initial revision.
