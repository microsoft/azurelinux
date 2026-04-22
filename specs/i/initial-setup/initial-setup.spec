# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enable X11 for RHEL 9 and older only
%bcond x11 %[0%{?rhel} && 0%{?rhel} < 10]

Name: initial-setup
Summary: Initial system configuration utility
URL: https://fedoraproject.org/wiki/InitialSetup
License: GPL-2.0-or-later
Version: 0.3.101
Release: 7%{?dist}

# This is a Red Hat maintained package which is specific to
# our distribution.
#
# The source is thus available only from within this SRPM
# or via direct git checkout:
# git clone https://github.com/rhinstaller/initial-setup
Source0: %{name}-%{version}.tar.gz

%define debug_package %{nil}
%define anacondaver 37.8-1

BuildRequires: gettext
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: systemd-units
BuildRequires: gtk3-devel
BuildRequires: glade-devel
BuildRequires: intltool
BuildRequires: make

Requires: %{__python3}
Requires: anaconda-tui >= %{anacondaver}
Requires: libxkbcommon
Requires: python3-simpleline >= 1.4
Requires: systemd >= 235
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: util-linux
Conflicts: firstboot < 19.2

%description
The initial-setup utility runs after installation.  It guides the user through
a series of steps that allows for easier configuration of the machine.

%post
%systemd_post initial-setup.service

%preun
%systemd_preun initial-setup.service

%postun
%systemd_postun initial-setup.service

%files -f %{name}.lang
%doc README.rst ChangeLog
%license COPYING
%{python3_sitelib}/initial_setup*
%exclude %{python3_sitelib}/initial_setup/gui
%{_libexecdir}/%{name}/run-initial-setup
%{_libexecdir}/%{name}/initial-setup-text
%{_libexecdir}/%{name}/reconfiguration-mode-enabled
%{_unitdir}/initial-setup.service
%{_unitdir}/initial-setup-reconfiguration.service
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/conf.d
%config %{_sysconfdir}/%{name}/conf.d/*
%{_sysconfdir}/pam.d/initial-setup

%ifarch s390 s390x
%{_sysconfdir}/profile.d/initial-setup.sh
%{_sysconfdir}/profile.d/initial-setup.csh
%endif

# --------------------------------------------------------------------------

%package gui
Summary: Graphical user interface for the initial-setup utility
Requires: gtk3
Requires: anaconda-gui >= %{anacondaver}
Requires: firstboot(gui-backend)
Requires: %{name} = %{version}-%{release}
Suggests: %{name}-gui-wayland-generic

%description gui
The initial-setup-gui package contains a graphical user interface for the
initial-setup utility.

%files gui
%{_libexecdir}/%{name}/initial-setup-graphical
%{python3_sitelib}/initial_setup/gui/

# --------------------------------------------------------------------------

%package gui-wayland-generic
Summary: Run the initial-setup GUI in Wayland
Requires: %{name}-gui = %{version}-%{release}
Requires: weston
Requires: xorg-x11-server-Xwayland

Provides:  firstboot(gui-backend)
Conflicts: firstboot(gui-backend)
RemovePathPostfixes: .guiweston

%description gui-wayland-generic
%{summary}.

%files gui-wayland-generic
%{_libexecdir}/%{name}/run-gui-backend.guiweston

# --------------------------------------------------------------------------

%if %{with x11}
%package gui-xorg
Summary: Run the initial-setup GUI in Xorg
Requires: %{name}-gui = %{version}-%{release}
Requires: xorg-x11-xinit
Requires: xorg-x11-server-Xorg
Requires: firstboot(windowmanager)

Provides:  firstboot(gui-backend)
Conflicts: firstboot(gui-backend)
RemovePathPostfixes: .guixorg

%description gui-xorg
%{summary}.

%files gui-xorg
%{_libexecdir}/%{name}/run-gui-backend.guixorg
%{_libexecdir}/%{name}/firstboot-windowmanager
%endif

# --------------------------------------------------------------------------

%prep
%autosetup -p 1

# remove upstream egg-info
rm -rf *.egg-info

%build
%make_build

%install
%make_install

# Remove the default link, provide subpackages for alternatives
rm %{buildroot}%{_libexecdir}/%{name}/run-gui-backend

%if ! %{with x11}
# We do not want to ship X11 support anymore
rm -v %{buildroot}%{_libexecdir}/%{name}/run-gui-backend.guixorg
rm -v %{buildroot}%{_libexecdir}/%{name}/firstboot-windowmanager
%endif

%find_lang %{name}

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.3.101-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.3.101-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.3.101-3
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Martin Kolman <mkolman@redhat.com> - 0.3.101-1
- Use threads.py submodule in favor of compatibility file threading.py (kkoukiou)

* Wed Jan 03 2024 Martin Kolman <mkolman@redhat.com> - 0.3.100-1
- spec: Disable shipping the X11 backend for all but RHEL < 10 (neal)
- spec: Restructure and modernize (neal)

* Wed Jan 03 2024 Martin Kolman <mkolman@redhat.com> - 0.3.99-1
- Default initial-setup-gui GDK to X11 for all display servers (ales.astone)
- Configure a seat session for running wayland compositors (ales.astone)
- Add support for generic Wayland support through Weston (neal)
- Allow running the graphical setup in graphic servers other than Xorg (ales.astone)
- windowmanager: Remove kwin (ales.astone)

* Mon Oct 09 2023 Martin Kolman <mkolman@redhat.com> - 0.3.98-1
- Fix Anaconda module startup (#2241274) (mkolman)

* Mon Feb 13 2023 Martin Kolman <mkolman@redhat.com> - 0.3.97-1
- Make it possible to run with no kickstart (mkolman)
- Fixup packit SRPM build deps (mkolman)

* Thu Jan 19 2023 Martin Kolman <mkolman@redhat.com> - 0.3.96-1
- SPDX compatible License: line (mkolman)
- Fixup version in setup.py (mkolman)

* Wed Jul 20 2022 Martin Kolman <mkolman@redhat.com> - 0.3.95-1
- Use Anaconda DBus read-write properties (vponcova)

* Tue Oct 12 2021 Martin Kolman <mkolman@redhat.com> - 0.3.94-1
- Remove the default_help_pages configuration option (vponcova)
- Add the configuration files to the updates image (vponcova)
- Remove the helpFile attribute (vponcova)
- Specify unique screen ids (vponcova)
- Apply suggestions from code review (martin.kolman)
- Fix ownership of the gui folder (#1812463) (mkolman)
- Don't show the EULA spoke if the license file doesn't exist (vponcova)

* Mon Jul 12 2021 Martin Kolman <mkolman@redhat.com> - 0.3.93-1
- Use profiles instead of product configuration files (vponcova)
- Change the Python version to 3.10 in the makeupdates script (vponcova)

* Thu Jun 24 2021 Martin Kolman <mkolman@redhat.com> - 0.3.92-1
- Fixup version in setup.py (mkolman)
- Add gnome-kiosk to window managers usable by initial-setup (rvykydal)
- Add copr builds also for branched Fedora (jkonecny)

* Tue Apr 27 2021 Martin Kolman <mkolman@redhat.com> - 0.3.91-1
- Disable multi TTY handler when running in SSH session (mkolman)
- Add CLI option to disable multi TTY handler (mkolman)

* Tue Mar 30 2021 Martin Kolman <mkolman@redhat.com> - 0.3.90-1
- Remove old failing pre scriptlet (mkolman)

* Tue Mar 23 2021 Martin Kolman <mkolman@redhat.com> - 0.3.89-1
- Include scripts in the updates image (vponcova)
- Drop build time dependency on the anaconda package (mkolman)

* Mon Feb 22 2021 Martin Kolman <mkolman@redhat.com> - 0.3.88-1
- Load the product configuration files (vponcova)
- Clean up the code (vponcova)

* Mon Feb 15 2021 Martin Kolman <mkolman@redhat.com> - 0.3.87-1
- Add BuildRequires: make (tstellar)
- Fixup version number in setup.py (mkolman)

* Fri Feb 12 2021 Martin Kolman <mkolman@redhat.com> - 0.3.86-1
- Drop python-nose from the dependencies (#1916799) (vponcova)
- Add the makeupdates script (vponcova)
- Remove deprecated support for add-ons (vponcova)
- Don't run installation tasks of add-ons in a meta task (vponcova)
- Migrate COPR builds from Jenkins to Packit (jkonecny)
- Add documentation for the new test solution (jkonecny)
- Add support for custom Anaconda COPR repository (jkonecny)
- Use `make test` to run TMT tests locally (jkonecny)
- Add TMT configuration to get Anaconda COPR build (jkonecny)
- Add Packit support for initial-setup (jkonecny)
- Update and use setup.py for archive creation (jkonecny)
- Fix ChangeLog generation in Makefile (jkonecny)

* Mon Dec 07 2020 Martin Kolman <mkolman@redhat.com> - 0.3.85-1
- Adapt to category title translation fix in Anaconda (mkolman)

* Tue Oct 27 2020 Martin Kolman <mkolman@redhat.com> - 0.3.84-1
- Adjust to logging command changes in Anaconda (#1891621) (mkolman)
- Make sure the output from custom_getpass() is serialized after stdout (lkundrak)

* Wed Aug 19 2020 Martin Kolman <mkolman@redhat.com> - 0.3.83-1
- Add PEP8 Speaks configuration (mkolman)
- Remove hard coded name of the translation repo in tmp (jkonecny)
- Update README.rst (mkolman)
- Add missing branch config to manifest file (jkonecny)
- Add COPR daily builds badge (jkonecny)

* Mon Jun 08 2020 Martin Kolman <mkolman@redhat.com> - 0.3.82-1
- Add translation badge to the README file (jkonecny)
- Remove unused PREFIX variable from Makefile (jkonecny)
- Use new po-push instead of Zanata (jkonecny)
- Add po-push using localization repository (jkonecny)
- Use translation repository to pull the translations (jkonecny)

* Fri May 22 2020 Martin Kolman <mkolman@redhat.com> - 0.3.81-1
- Use macro for Python 3 requirement in spec file (mkolman)
- Remove outdated dependency on python3-libreport (vslavik)
- Fix a typo in Zanata CLI invocation (mkolman)

* Tue Dec 10 2019 Martin Kolman <mkolman@redhat.com> - 0.3.80-1
- Do not call a task which has been moved into install keyboard task (rvykydal)
- Adapt to changes in localization module (rvykydal)
- Fix Zanata client detection in Makefile (mkolman)

* Mon Nov 18 2019 Martin Kolman <mkolman@redhat.com> - 0.3.79-1
- Fix import of the DBus launcher (vponcova)

* Tue Nov 12 2019 Martin Kolman <martin.kolman@gmail.com> - 0.3.78-1
- Revert "Fix import of the DBus launcher" (martin.kolman)
- Run the installation tasks of the DBus addons (vponcova)
- Run the installation tasks of the Timezone module (vponcova)
- Fix import of the DBus launcher (vponcova)

* Thu Oct 24 2019 Martin Kolman <mkolman@redhat.com> - 0.3.77-1
- Run the installation tasks of the Localization module (vponcova)
- Use new DBus support for reading a kickstart file (vponcova)
- Use autosetup instead of setup (mkolman)
- Bump Anaconda version due to networking changes (mkolman)

* Fri Oct 04 2019 Martin Kolman <mkolman@redhat.com> - 0.3.76-1
- Fix configuration of network hostname (#1757960) (rvykydal)

* Thu Oct 03 2019 Martin Kolman <mkolman@redhat.com> - 0.3.75-1
- Blacklist some USB consoles from multi-TTY handler (#1755580) (mkolman)

* Wed Sep 18 2019 Martin Kolman <mkolman@redhat.com> - 0.3.74-1
- Fix typo in reconfig mode detection (#1752554) (mkolman)

* Wed Jul 31 2019 Martin Kolman <mkolman@redhat.com> - 0.3.73-1
- Remove system root from DBus calls (vponcova)
- Correct the name for libreport Python3 require (mkutlak)

* Thu Jun 20 2019 Martin Kolman <mkolman@redhat.com> - 0.3.72-1
- Set physical and system roots in the configuration file (vponcova)
- Write Anaconda logs to journal (vponcova)
- Read configuration files from /etc/initial-setup/conf.d (#1713506) (vponcova)

* Thu Jun 13 2019 Martin Kolman <mkolman@redhat.com> - 0.3.71-1
- Don't initialize the screen access manager (vponcova)

* Wed May 15 2019 Martin Kolman <mkolman@redhat.com> - 0.3.70-1
- Adjust to changes in the Users DBus module (mkolman)

* Thu Apr 04 2019 Martin Kolman <mkolman@redhat.com> - 0.3.69-1
- Adapt to removal of ifcfg.log (#1695967) (rvykydal)

* Tue Mar 12 2019 Martin Kolman <mkolman@redhat.com> - 0.3.68-1
- Remove obsolete Group definition from the spec file (mkolman)
- Initialize network module (device configurations) (#1685992) (rvykydal)
- Specify the type of the installation system (#1685992) (vponcova)

* Tue Mar 12 2019 Martin Kolman <mkolman@redhat.com> - 0.3.67-1
- Update arguments of the execute methods (#1666849) (vponcova)

* Mon Jan 21 2019 Martin Kolman <mkolman@redhat.com> - 0.3.66-1
- Don't call initThreading (#1666849) (vponcova)

* Thu Jan 03 2019 Martin Kolman <mkolman@redhat.com> - 0.3.65-1
- Remove install classes from the initial setup (vponcova)

* Mon Nov 19 2018 Martin Kolman <mkolman@redhat.com> - 0.3.64-1
- Handle simpleline having an empty stack (mkolman)

* Mon Nov 05 2018 Martin Kolman <mkolman@redhat.com> - 0.3.63-1
- Disable modules in the configuration file (vponcova)
- Let the DBus launcher to set up the modules (vponcova)
- README.rst: update link to anaconda addon dev guide (kenyon)

* Fri Jul 27 2018 Martin Kolman <mkolman@redhat.com> - 0.3.62-1
- Make EULA spoke name compatible with three column hub (mkolman)
- Blacklist the ptmx console from multi-tty use (mkolman)
- Add support for showing an EULA spoke (mkolman)
- Add explicit dependency on X server for the GUI sub-package (mkolman)

* Wed May 09 2018 Martin Kolman <mkolman@redhat.com> - 0.3.61-1
- Fix the users module import (#1575650) (mkolman)

* Fri May 04 2018 Martin Kolman <mkolman@redhat.com> - 0.3.60-1
- Fix name of the Zanata Python client package (mkolman)
- Use the Anaconda default for DBUS module timeout (mkolman)

* Mon Apr 23 2018 Martin Kolman <mkolman@redhat.com> - 0.3.59-1
- Fix version number in setup.py (mkolman)

* Thu Apr 19 2018 Martin Kolman <mkolman@redhat.com> - 0.3.58-1
- Run only the supported kickstart modules (#1566621) (vponcova)

* Tue Apr 10 2018 Martin Kolman <mkolman@redhat.com> - 0.3.57-1
- Adapt to a new Simpleline input handling (jkonecny)

* Mon Mar 19 2018 Martin Kolman <mkolman@redhat.com> - 0.3.56-1
- Adjust to Hub behavior change (mkolman)
- Apply the Anaconda modularization changes (vponcova)

* Mon Mar 05 2018 Martin Kolman <mkolman@redhat.com> - 0.3.55-1
- Handle kickstart commands provided by DBUS modules (mkolman)
- Adapt to changes in starting Boss (mkolman)

* Wed Feb 28 2018 Martin Kolman <mkolman@redhat.com> - 0.3.54-1
- Start and stop Boss (mkolman)
- New version 0.3.53 (mkolman)
- Add common function for finding bugreport URL (riehecky)

* Fri Jan 19 2018 Martin Kolman <mkolman@redhat.com> - 0.3.53-1
- Fix imports after Anaconda refactoring (jkonecny)
- Return correct code at startup script success/failure (mkolman)

* Wed Nov 29 2017 Martin Kolman <mkolman@redhat.com> - 0.3.52-1
- Use getty-pre.target to prevent getty from running (mkolman)

* Thu Oct 05 2017 Martin Kolman <mkolman@redhat.com> - 0.3.51-1
- Don't print directory changes when outputting the changelog (mkolman)
- Automate release creation (mkolman)
- Don't include merges in the spec file changelog (mkolman)
- Update initial-setup-reconfiguration.service too, add another (mvebu) serial console (pbrobinson)
- Add some more serial console options for ARM (pbrobinson)

* Mon Sep 11 2017 Martin Kolman <mkolman@redhat.com> - 0.3.50-1
- Use constant+offset when turning systemd console logging on/off (mkolman)
- Add some more serial console options (pbrobinson)

* Wed Aug 30 2017 Martin Kolman <mkolman@redhat.com> - 0.3.49-1
- Use new Simpleline package (jkonecny)
- Remove unused import (jkonecny)
- add yet another ARM serial console (sjenning)

* Wed Jul 12 2017 Martin Kolman <martin.kolman@gmail.com> - 0.3.48-1
- Fix Anaconda threading import name (#1469776) (mkolman)

* Fri Jun 02 2017 Martin Kolman <mkolman@redhat.com> - 0.3.47-1
- Adapt to anaconda_log module name change (mkolman)

* Wed May 24 2017 Martin Kolman <mkolman@redhat.com> - 0.3.46-2
- Drop Anaconda version bump for now (mkolman)

* Wed May 24 2017 Martin Kolman <mkolman@redhat.com> - 0.3.46-1
- Add support for password entry from arbitrary consoles (#1438046) (mkolman)

* Wed May 17 2017 Martin Kolman <mkolman@redhat.com> - 0.3.45-1
- Remove stdin & stdout definition from unit files (#1438046) (mkolman)

* Mon May 15 2017 Martin Kolman <mkolman@redhat.com> - 0.3.44-1
- Run the Initial Setup TUI on all usable consoles (#1438046) (mkolman)

* Wed Sep 21 2016 Martin Kolman <mkolman@redhat.com> - 0.3.43-1
- Initialize SAM on startup (#1375721) (mkolman)
- Log unhandled exceptions to Journal (mkolman)
- Suppress logging to stdout when TUI is started by s390 startup scripts (mkolman)
- Fix path to TUI executable in the s390 startup scripts (#1366776) (mkolman)
- Canonicalize symlinks returned by readlink (mkolman)

* Fri Aug 05 2016 Martin Kolman <mkolman@redhat.com> - 0.3.42-1
- Fix a typo (mkolman)
- Don't run the GUI on text-only systems (#1360343) (mkolman)

* Wed Jun 08 2016 Martin Kolman <mkolman@redhat.com> - 0.3.41-1
- Fix reconfiguration service name (mkolman)
- Fix installation path for the reconfiguration-mode-enabled script (mkolman)
- Use the environs flag when setting the environment (mkolman)
- Some typo fixes and logging improvements (mkolman)
- Add a systemd service that enables Initial Setup if /.unconfigured exists (#1257624) (mkolman)
- Adapt to addon execute() signature change (mkolman)
- Replace hardcoded python3 call by a variable (mkolman)
- Nicer systemctl calls (mkolman)
- Use systemd-cat also for the run-initial-setup script (mkolman)
- Remove a redundant Requires: line (mkolman)
- Fix a typo (mkolman)
- Run correct systemd scriptlets (mkolman)
- Use systemd-cat for logging to the journal (mkolman)

* Thu Mar 24 2016 Martin Kolman <mkolman@redhat.com> - 0.3.40-1
- Use blank title for the Initial Setup window (mkolman)
- Start the window manager correctly (#1160891) (mkolman)
- Fix some rpmlint warnings (mkolman)

* Tue Feb 16 2016 Martin Kolman <mkolman@redhat.com> - 0.3.39-1
- Disable the correct service on successful completion (#1298725) (mkolman)

* Tue Dec 01 2015 Martin Kolman <mkolman@redhat.com> - 0.3.38-1
- Make Initial Setup startup more robust (mkolman)
- Move the s390 profile scripts to a subfolder (mkolman)
- Improve log messages for kickstart parsing error (mkolman)

* Wed Sep 30 2015 Martin Kolman <mkolman@redhat.com> - 0.3.37-1
- Stop any Initial Setup services before upgrading package (#1244394) (mkolman)
- Replace systemd_postun_with_restart with systemd_postun (#1244394) (mkolman)
- Fix 'bumpver' make target (vtrefny)
- Add archive target to Makefile (vtrefny)

* Mon Aug 31 2015 Martin Kolman <mkolman@redhat.com> - 0.3.36-1
- Setup the locale before starting the UI (dshea)
- Run the TUI service before hvc0.service (#1209731) (mkolman)
- Don't create /etc/sysconfig/initial-setup on s390 (#1181209) (mkolman)
- Use systemd service status for run detection on S390 console (#1181209) (mkolman)
- Read the kickstart from previous IS run, if available (#1110439) (mkolman)
- Add support for externally triggered reconfig mode (#1110439) (mkolman)
- Log the reason if GUI import fails (#1229747) (mkolman)

* Thu Jul 30 2015 Martin Kolman <mkolman@redhat.com> - 0.3.35-1
- Fix a typo in Makefile (#1244558) (mkolman)

* Thu Jul 30 2015 Martin Kolman <mkolman@redhat.com> - 0.3.34-1
- Switch Initial Setup to Python 3 (#1244558) (mkolman)

* Thu Apr 23 2015 Martin Kolman <mkolman@redhat.com> - 0.3.33-1
- Improve the Makefile (mkolman)
- Remove old GUI testing code from the Makefile (mkolman)
- Update upstream URL (#1213101) (mkolman)
- Update upstream Git repository URL (mkolman)

* Tue Mar 31 2015 Martin Kolman <mkolman@redhat.com> - 0.3.32-1
- Point out the err in case that ks parsing failed (#1145130) (fabiand)
- Switch to Zanata for translations (mkolman)

* Wed Mar 04 2015 Martin Kolman <mkolman@redhat.com> - 0.3.31-1
- Use kwin_x11 for kde/plasma spin (#1197135) (rdieter)

* Fri Feb 13 2015 Martin Kolman <mkolman@redhat.com> - 0.3.29-1
- Split scriptlets for the gui subpackage (mkolman)
- Use /usr/bin/python2 in scripts (mkolman)

* Thu Feb 05 2015 Martin Kolman <mkolman@redhat.com> - 0.3.28-1
- Fix breakage caused by README file rename (mkolman)

* Thu Feb 05 2015 Martin Kolman <mkolman@redhat.com> - 0.3.27-1
- Remove unneeded dependencies (mkolman)
- Add the rst suffix to the README file (mkolman)
- Update the link to the upstream source code repository (mkolman)
- Add AnacondaKSHandler no-member error to pylint-false-positives. (mulhern)
- Mark strings for translation when module is loaded. (mulhern)
- Fix easy pylint errors. (mulhern)
- Add pylint testing infrastructure. (mulhern)

* Mon Nov 3 2014 Martin Kolman <mkolman@redhat.com> - 0.3.26-1
- Explicitly require the main package in the GUI sub package (#1078917) (mkolman)

* Thu Oct 23 2014 Martin Kolman <mkolman@redhat.com> - 0.3.25-1
- Add syslog logging support (#1145122) (mkolman)

* Fri Oct 10 2014 Martin Kolman <mkolman@redhat.com> - 0.3.24-1
- Fix Initial Setup to correctly support the Anaconda built-in Help (#1072033) (mkolman)
- Populate README (#1110178) (master-log) (mkolman)
- Remove the --disable-overwrite parameter for the Transifex client (mkolman)

* Fri Aug 08 2014 Martin Kolman <mkolman@redhat.com> - 0.3.23-1
- Adapt to class changes in Anaconda (vpodzime)

* Fri Jul 04 2014 Martin Kolman <mkolman@redhat.com> - 0.3.22-1
- Update the initial-setup hub for the new HubWindow API (dshea)

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.3.21-2
- Only the GUI needs a window manager

* Wed May 28 2014 Martin Kolman <mkolman@redhat.com> - 0.3.21-1
- Adapt to python-nose API change (mkolman)

* Thu May 22 2014 Martin Kolman <mkolman@redhat.com> - 0.3.20-1
- Adapt Initial Setup to the new way Anaconda handles root path (#1099581) (vpodzime)

* Tue May 06 2014 Martin Kolman <mkolman@redhat.com> - 0.3.19-1
- Bump required Anaconda version due to TUI category handling change (mkolman)
- Override Hub collect methods also in TUI hub (mkolman)
- Translation update

* Mon Apr 28 2014 Martin Kolman <mkolman@redhat.com> - 0.3.18-1
- Remove debugging code that was left in the tarball by mistake (#1091470) (mkolman)
- Translation update

* Fri Apr 11 2014 Martin Kolman <mkolman@redhat.com> - 0.3.17-1
- Set initial-setup translation domain for the hub (#1040240) (mkolman)

* Thu Apr 03 2014 Martin Kolman <mkolman@redhat.com> - 0.3.16-1
- initial-setup-gui requires the initial-setup package (vpodzime)

* Wed Mar 19 2014 Martin Kolman <mkolman@redhat.com> - 0.3.15-1
- Import the product module (#1077390) (vpodzime)

* Tue Feb 11 2014 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.14-1
- Try to quit plymouth before running our X server instance (#1058329)
- Get rid of the empty debuginfo package (#1062738)

* Wed Feb 05 2014 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.13-1
- Make Initial Setup an arch specific package (#1057590) (vpodzime)

* Thu Nov 28 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.12-1
- Adapt to changes in anaconda tui spoke categories (#1035462) (vpodzime)
- Ignore the SIGINT (#1035590) (vpodzime)

* Wed Nov 20 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.11-1
- Fix how spokes are collected for the I-S main hub (vpodzime)
- Override distribution text in spokes (#1028370) (vpodzime)
- Get rid of the useless modules directory (vpodzime)
- Split GUI code into a separate package (#999464) (vpodzime)
- Fallback to text UI if GUI is not available (vpodzime)

* Tue Nov 05 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.10-1
- Do not try to kill unexisting process (vpodzime)
- Add some logging to our shell scripts (vpodzime)

* Thu Sep 26 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.9-1
- Yet another serial console in ARMs (#1007163) (vpodzime)
- Fix the base mask of initial_setup gui submodules (vpodzime)
- Specify and use environment of the main hub (vpodzime)

* Tue Sep 10 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.8-1
- Read /etc/os-release to get product title (#1000426) (vpodzime)
- Don't let product_title() return None (vpodzime)
- Apply the timezone and NTP configuration (#985566) (hdegoede)
- Make handling translations easier (vpodzime)
- Make translations work (vpodzime)
- Sync changelog with downstream (vpodzime)

* Tue Aug 27 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.7-1
- Prevent getty on various services killing us (#979174) (vpodzime)
- Initialize network logging for the network spoke (vpodzime)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.6-2
- Rebuild with dependencies available.

* Tue Jun 18 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.6-1
- Make serial-getty wait for us as well (#970719) (vpodzime)
- Disable the service only on successful exit (#967617) (vpodzime)

* Wed May 22 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.5-1
- Reference the new repository in the .spec file (vpodzime)
- Prevent systemd services from running on live images (#962196) (awilliam)
- Don't traceback if the expected kickstart file doesn't exist (#950796) (vpodzime)

* Mon Apr 8 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.4-3
- Rebuild with fixed spec that partly reverts the previous change

* Fri Apr 5 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.3.4-2
- Rebuild with fixed spec that enables services after installation

* Thu Mar 28 2013 Martin Sivak <msivak@euryale.brq.redhat.com> - 0.3.4-1
- Search for proper UI variant of addons
- Add addon directories to sys.path

* Tue Mar 26 2013 Martin Sivak <msivak@euryale.brq.redhat.com> - 0.3.3-1
- Systemd unit files improved

* Tue Mar 26 2013 Martin Sivak <msivak@euryale.brq.redhat.com> - 0.3.2-1
- Modify the ROOT_PATH properly
- Do not execute old ksdata (from anaconda's ks file)
- Save the resulting configuration to /root/initial-setup-ks.cfg

* Tue Mar 26 2013 Martin Sivak <msivak@euryale.brq.redhat.com> - 0.3.1-2
- Require python-di package

* Thu Mar 21 2013 Martin Sivak <msivak@euryale.brq.redhat.com> - 0.3.1-1
- Use updated Anaconda API
- Request firstboot environment spokes
- Initialize anaconda threading properly

* Wed Mar 13 2013 Martin Sivak <msivak@euryale.brq.redhat.com> - 0.3-1
- Use updated Anaconda API
- Fix systemd units
- Add localization spokes to TUI
- Write changes to disk
- Conflict with old firstboot

* Wed Feb 13 2013 Martin Sivak <msivak@redhat.com> 0.2-1
- Updates for package review
- Firstboot-windowmanager script

* Wed Feb 13 2013 Martin Sivak <msivak@redhat.com> 0.1-3
- Updates for package review

* Tue Jan 22 2013 Martin Sivak <msivak@redhat.com> 0.1-2
- Updates for package review

* Tue Nov 06 2012 Martin Sivak <msivak@redhat.com> 0.1-1
- Initial release
