Vendor:         Microsoft Corporation
Distribution:   Mariner
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
%if !%{use_systemd}
%global __python2 %{__python}
%global python2_sitelib %{python_sitelib}
%endif

%define use_python3 1
%if %{use_python3}
%global python_ver python3
%global python_exec %{__python3}
%global python_sitelib %{python3_sitelib}
%else
%global python_ver python
%global python_exec %{__python2}
%global python_sitelib %{python2_sitelib}
%endif

Name:           virt-who
Version:        0.24.2
Release:        2%{?dist}

Summary:        Agent for reporting virtual guest IDs to subscription-manager

License:        GPLv2+
URL:            https://github.com/candlepin/virt-who
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  %{python_ver}-devel
BuildRequires:  %{python_ver}-setuptools
# rhel 8 has different naming going forward
%if (0%{?rhel} && 0%{?rhel} >= 8)
Requires:      platform-python-setuptools
%else
Requires:      %{python_ver}-setuptools
%endif
# libvirt python required for libvirt support

Requires:       %{python_ver}-libvirt



# python-rhsm 1.20 has the M2Crypto wrappers needed to replace M2Crypto
# with the python standard libraries where plausible
%if %{use_python3}
Requires:       python3-subscription-manager-rhsm
%else
Requires:       subscription-manager-rhsm
%endif
# python-suds is required for vSphere support
Requires:       %{python_ver}-suds
# m2crypto OR python3-cryptography is required for Hyper-V support
%if %{use_python3}
Requires:       python3-cryptography
%else
Requires:       m2crypto
%endif
Requires:       %{python_ver}-requests
Requires:       %{python_ver}-six
# python-argparse is required for Python 2.6 on EL6
%{?el6:Requires: python-argparse}
Requires:       openssl

%if %{use_systemd}
%if %{use_python3}
Requires: python3-systemd
%else
Requires: systemd-python
%endif
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%endif

%description
Agent that collects information about virtual guests present in the system and
report them to the subscription manager.

%prep
%setup -q


%build
%{python_exec} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{python_exec} setup.py install --root %{buildroot}
%{python_exec} setup.py install_config --root %{buildroot}
%{python_exec} setup.py install_man_pages --root %{buildroot}
%if %{use_systemd}
%{python_exec} setup.py install_systemd --root %{buildroot}
%else
%{python_exec} setup.py install_upstart --root %{buildroot}
%endif

mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}/
touch %{buildroot}/%{_sharedstatedir}/%{name}/key

mkdir -p %{buildroot}/%{_datadir}/zsh/site-functions
install -m 644 virt-who-zsh %{buildroot}/%{_datadir}/zsh/site-functions/_virt-who

# Don't run test suite in check section, because it need the system to be
# registered to subscription-manager server

%post
%if %{use_systemd}
%systemd_post virt-who.service
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add virt-who
%endif


%preun
%if %{use_systemd}
%systemd_preun virt-who.service
%else
if [ $1 -eq 0 ] ; then
    /sbin/service virt-who stop >/dev/null 2>&1
    /sbin/chkconfig --del virt-who
fi
%endif

%postun
%if %{use_systemd}
%systemd_postun_with_restart virt-who.service
%else
if [ "$1" -ge "1" ] ; then
    /sbin/service virt-who condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%doc README.md LICENSE README.hyperv
%{_bindir}/virt-who
%{_bindir}/virt-who-password
%{python_sitelib}/*
%if %{use_systemd}
%{_unitdir}/virt-who.service
%else
%{_sysconfdir}/rc.d/init.d/virt-who
%endif
%attr(600, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/virt-who
%attr(700, root, root) %dir %{_sysconfdir}/virt-who.d
%{_mandir}/man8/virt-who.8.gz
%{_mandir}/man8/virt-who-password.8.gz
%{_mandir}/man5/virt-who-config.5.gz
%attr(700, root, root) %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/key
%{_datadir}/zsh/site-functions/_virt-who
%{_sysconfdir}/virt-who.d/template.conf
%attr(600, root, root) %config(noreplace) %{_sysconfdir}/virt-who.conf


%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.24.2-2
- Switching to using full number for the 'Release' tag.

* Mon Jun 28 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.24.2-1.6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Switching to building with Python 3.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.2-1.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.24.2-1.4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.24.2-1.3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 21 2018 William Poteat <wpoteat@redhat.com> 0.24.2-1
- 1657104: Remove references to removed command line options
  (wpoteat@redhat.com)
- Fixing kubevirt config path argument (piotr.kliczewski@gmail.com)
- fix travis run (wpoteat@redhat.com)
- 1650133: setuptools naming change (wpoteat@redhat.com)
- 1638250: Proxy issue when https not specified (wpoteat@redhat.com)
- Update branch definition for RHEL 8.0 branch (wpoteat@redhat.com)
- ENT-896: Disable deprecated configuration options in python 3
  (wpoteat@redhat.com)
- 1637407: vCenter mapping info failure due to TypeError (wpoteat@redhat.com)

* Mon Oct 29 2018 William Poteat <wpoteat@redhat.com> 0.24.1-1
- Merge in changes from Fedora packaging (wpoteat@redhat.com)
- ENT-826 Added correlation id to virt-who reports (nmoumoul@redhat.com)
- Releaser addition for rhel-7.7 (wpoteat@redhat.com)
- Install subscription-manager, not python-rhsm which is deprecated: - Removed
  python-rhsm from the requirements, and added subscription-manager as
  dependency. - Added some dependencies that travis requires to install
  subscription-manager. (nmoumoul@redhat.com)

* Wed Sep 19 2018 William Poteat <wpoteat@redhat.com> 0.24.0-1
- Automatic commit of package [virt-who] release [0.22.2-1].
  (wpoteat@redhat.com)
- kubevirt: warn user that dependencies are missing
  (piotr.kliczewski@gmail.com)
- 1369634: Dont log proxy html errors for hyperv: - When hyperv gets an HTML
  page as error response from a proxy, don't log the whole html, but try to
  scrape the title off of it. - If scraping the title doesn't work, only log
  the http error code. - Changed all variables named 'xml' to 'xml_doc' in
  hyperv.py to avoid conflict with the new python keyword.
  (nmoumoul@redhat.com)
- 1599725: Handle job status report errors (nmoumoul@redhat.com)
- 1557296: Warn of commented out lines prefixed with space/tab (ENT-606) - When
  reading config files in python2, warn the user if a line continuation (starts
  with space/tab) is followed by '#' (nmoumoul@redhat.com)
- kubevirt: Ignore vmis in Scheduling (piotr.kliczewski@gmail.com)
- kubevirt: Update config (piotr.kliczewski@gmail.com)
- Print/log debug information about filtered hosts (jhnidek@redhat.com)
- 1577954: Added config option filter_type; ENT-580 (jhnidek@redhat.com)
- Changed info about how filter_host_parents/exclude_host_parents filters work
  (ktordeur@redhat.com)
- 1387800: set name of ESX cluster properly; ENT-793 (jhnidek@redhat.com)
- Add release entry for RHEL 8 (wpoteat@redhat.com)
- template update (wpinheir@iroman.home)
- template update (wpinheir@iroman.home)
- 1596041: Make python libvirt required (wpoteat@redhat.com)
- updating RHV/RHEV/XenServer information (wpinheir@iroman.home)
- 1581021: Decode error from unicode passwords (wpoteat@redhat.com)
- 1510920: Change the choreography for the job status check
  (wpoteat@redhat.com)
- ENT-493: Add option to command line to return version
  (adarshvritant@gmail.com)
- Update executor.py (all_bright@live.com)
- kubevirt: rename virtual machine instance (piotr.kliczewski@gmail.com)
- Update for build process (wpoteat@redhat.com)
- Fixed hyperv wmi query. Invalid response (500)
  (njmiller@lakemichigancollege.edu)
- 1432140: Log when a duplicate hypervisor id is detected [ENT-568]
  (wpoteat@redhat.com)
- 1368341: Warn that --sam/--satellite6 are unused & deprecated * Now logging a
  warning when --sam/--satellite6 are used. * man page and --help output
  updated to explaing that these options are unused and virt-who will report to
  either sam/satellite/stage candlepin regardless of their being there.
  (nmoumoul@redhat.com)
- 1455062: Partial fix of high CPU usage, when many conf files used
  (jhnidek@redhat.com)
- Correction to the spec file condition for python 3 (wpoteat@redhat.com)
- ENT-554 Host reports for libvirt and rhevm include the system hardware uuid
  (wpoteat@redhat.com)
- Add releaser for RHEL 7.6 (wpoteat@redhat.com)
- Remove f26 releaser (f26 is EOL) (csnyder@redhat.com)

* Wed Sep 19 2018 William Poteat <wpoteat@redhat.com>
- Automatic commit of package [virt-who] release [0.22.2-1].
  (wpoteat@redhat.com)
- kubevirt: warn user that dependencies are missing
  (piotr.kliczewski@gmail.com)
- 1369634: Dont log proxy html errors for hyperv: - When hyperv gets an HTML
  page as error response from a proxy, don't log the whole html, but try to
  scrape the title off of it. - If scraping the title doesn't work, only log
  the http error code. - Changed all variables named 'xml' to 'xml_doc' in
  hyperv.py to avoid conflict with the new python keyword.
  (nmoumoul@redhat.com)
- 1599725: Handle job status report errors (nmoumoul@redhat.com)
- 1557296: Warn of commented out lines prefixed with space/tab (ENT-606) - When
  reading config files in python2, warn the user if a line continuation (starts
  with space/tab) is followed by '#' (nmoumoul@redhat.com)
- kubevirt: Ignore vmis in Scheduling (piotr.kliczewski@gmail.com)
- kubevirt: Update config (piotr.kliczewski@gmail.com)
- Print/log debug information about filtered hosts (jhnidek@redhat.com)
- 1577954: Added config option filter_type; ENT-580 (jhnidek@redhat.com)
- Changed info about how filter_host_parents/exclude_host_parents filters work
  (ktordeur@redhat.com)
- 1387800: set name of ESX cluster properly; ENT-793 (jhnidek@redhat.com)
- Add release entry for RHEL 8 (wpoteat@redhat.com)
- template update (wpinheir@iroman.home)
- template update (wpinheir@iroman.home)
- 1596041: Make python libvirt required (wpoteat@redhat.com)
- updating RHV/RHEV/XenServer information (wpinheir@iroman.home)
- 1581021: Decode error from unicode passwords (wpoteat@redhat.com)
- 1510920: Change the choreography for the job status check
  (wpoteat@redhat.com)
- ENT-493: Add option to command line to return version
  (adarshvritant@gmail.com)
- Update executor.py (all_bright@live.com)
- kubevirt: rename virtual machine instance (piotr.kliczewski@gmail.com)
- Update for build process (wpoteat@redhat.com)
- Fixed hyperv wmi query. Invalid response (500)
  (njmiller@lakemichigancollege.edu)
- 1432140: Log when a duplicate hypervisor id is detected [ENT-568]
  (wpoteat@redhat.com)
- 1368341: Warn that --sam/--satellite6 are unused & deprecated * Now logging a
  warning when --sam/--satellite6 are used. * man page and --help output
  updated to explaing that these options are unused and virt-who will report to
  either sam/satellite/stage candlepin regardless of their being there.
  (nmoumoul@redhat.com)
- 1455062: Partial fix of high CPU usage, when many conf files used
  (jhnidek@redhat.com)
- Correction to the spec file condition for python 3 (wpoteat@redhat.com)
- ENT-554 Host reports for libvirt and rhevm include the system hardware uuid
  (wpoteat@redhat.com)
- Add releaser for RHEL 7.6 (wpoteat@redhat.com)
- Remove f26 releaser (f26 is EOL) (csnyder@redhat.com)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.22.2-1.1
- Rebuilt for Python 3.7

* Thu May 31 2018 William Poteat <wpoteat@redhat.com> 0.22.2-1
- Correct date ordering in changelog (wpoteat@redhat.com)
- 1575513: Re-add changelog entries that were merged out. (wpoteat@redhat.com)
- 1560598: Pass hostname to M2Crypto in STOMP client (khowell@redhat.com)
- Make vdsm respect RHSM_USE_M2CRYPTO var (khowell@redhat.com)
- Set up Travis CI to use Python 3 (jhnidek@redhat.com)
- Fixing python 2 -> 3 issue (wpoteat@redhat.com)
- kubevirt support (piotr.kliczewski@gmail.com)

* Mon May 07 2018 William Poteat <wpoteat@redhat.com> 0.22.1-1
- 1542652: When the -c option is used, don't parse the default files
  (nmoumoul@redhat.com)
- 1569299: try/exception needed for hypervisor_id check (wpoteat@redhat.com)
- Update tito releasers to include newer versions of fedora
  (csnyder@redhat.com)
- 1560461: Make env and owner options required for approprite cases
  (jhnidek@redhat.com)
- 1554228: Unicode issue on status update call (wpoteat@redhat.com)
- 1387800: [RFE] virt-who can report cluster in host-to-guest mapping
  (jhnidek@redhat.com)
- Updates for future builds based on changing environments (wpoteat@redhat.com)
- limit version of libvirt-python (wpoteat@redhat.com)
- 1447022: Log warning, when wrong filter is in config file
  (jhnidek@redhat.com)
- 1511644: Support running virt-who on python 3 (csnyder@redhat.com)
- 1520236: Do not log traceback, when server returns 429 http error
  (jhnidek@redhat.com)
- 1492074: Enable login to ESX using password with UTF-8 string
  (jhnidek@redhat.com)
- 1353119: Add JSON-RPC support for VDSM (khowell@redhat.com)
- 1509597: Enable to use virt-who wih VDSM again (jhnidek@redhat.com)
- 1522383: Remove global option background (jhnidek@redhat.com)
- 1523548: Options log_dir and log_file are not ignored (jhnidek@redhat.com)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Christopher Snyder <csnyder@redhat.com> 0.21.2-1
- 1510310: Ensure that owner and env are required where necessary
  (csnyder@redhat.com)
- 1512778: ESX should require username, password, and server values
  (csnyder@redhat.com)

* Tue Nov 28 2017 Kevin Howell <khowell@redhat.com> 0.21.1-1
- 1511308: Only ESX supports: exclude_host_parents and filter_host_parents.
  (jhnidek@redhat.com)
- 1509596: Use qemu+ssh transport if not provided (libvirt)
  (csnyder@redhat.com)
- 1511308: Xen and Hyper-V do not support some filter options
  (jhnidek@redhat.com)
- 1510760: Ensure virt-who exits properly (w/ no good conf)
  (csnyder@redhat.com)
- 1509606: Remove duplicate output of validation messages (csnyder@redhat.com)
- 1509597: Fix issue with cli consistancy check for vdsm (csnyder@redhat.com)
- 1509595: Only expect owner on HostGuestAssociationReports
  (csnyder@redhat.com)

* Mon Oct 30 2017 Christopher Snyder <csnyder@redhat.com> 0.21.0-1
- Update hypervisorCheckInAsync test for new config sections
  (csnyder@redhat.com)
- Update Config Refactor with changes from master (csnyder@redhat.com)
- Removed usage of old Config (not unit tests) (jhnidek@redhat.com)
- Further clean up of unit tests (jhnidek@redhat.com)
- Create Xen Config Subclass (jhnidek@redhat.com)
- Create Rhevm Config Subclass (jhnidek@redhat.com)
- Create VDSM config subclass (wpoteat@redhat.com)
- Clean up ConfigSection Unit tests (jhnidek@redhat.com)
- Adds FakeVirtConfigSection (csnyder@redhat.com)
- Configuration subclass for hyperv (wpoteat@redhat.com)
- Implement EsxConfigSection (khowell@redhat.com)
- Libvirtd ConfigSection Subclass (jhnidek@redhat.com)
- Adds EffectiveConfig, ConfigSection (csnyder@redhat.com)
- Adds warning message for deprecated env vars (csnyder@redhat.com)
- 1503700: Updates to the job polling frequency (csnyder@redhat.com)
- 1502821: Remove undocumented, broken env var "VIRTWHO_DISABLE_ASYNC"
  (csnyder@redhat.com)
- 1466015: Warn of deprecation of command line options in next release
  (wpoteat@redhat.com)
- remove non-existant variable fake_is_hypervisor (adarshvritant@gmail.com)
- 1485865: Do not replace /etc/virt-who.conf on rpm upgrade
  (csnyder@redhat.com)
- Utilize the owner from the first report seen, if we do not know the owner
  (csnyder@redhat.com)
- Updates based on review (use str.format) (csnyder@redhat.com)
- Fix example fake config in man docs (adarshvritant@gmail.com)
- Add m2crypto dependency (adarshvritant@gmail.com)
- 1211435: Don't send host-to-geust mapping, when env, owner are wrong
  (jhnidek@redhat.com)
- 1408556: Log which owner updated mappings are being sent to
  (csnyder@redhat.com)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 26 2017 Christopher Snyder <csnyder@redhat.com> 0.20.4-1
- Point Source0 to GitHub (csnyder@redhat.com)

* Thu Jul 13 2017 Christopher Snyder <csnyder@redhat.com> 0.20.2-1
- 1458184: better reading of environment variables (jhnidek@redhat.com)
- 1401867: Enable logging of rhsm module to rhsm.log (jhnidek@redhat.com)
- 1404117: Check parameter consistency and refactoring (jhnidek@redhat.com)
- Adds a patch number to virt-who versioning (csnyder@redhat.com)
- 1401420: xen supports only uuid/hostname as hypervisor_id
  (jhnidek@redhat.com)
- 1458674: Update use of result data to match the new async api
  (csnyder@redhat.com)
- 1452436: virt-who prints host-to-quest mapping everytime (jhnidek@redhat.com)
- 1357761: Do not check passwords to be in latin1 encoding (jhnidek@redhat.com)
- 1457101: Continue running despite malformed configs (csnyder@redhat.com)
- 1409984: Retry initial report retrieval on connection timeout
  (csnyder@redhat.com)

* Fri Jun 09 2017 Christopher Snyder <csnyder@redhat.com> 0.20-1
- 1389729: Add missing xml section for test (fran@caosdigital.com)
- 1389729: virt-who incorrectly reports 'name' instead of 'hostname' for RHEV
  hosts (fran@caosdigital.com)
- 1450747: Continue running destination threads on internal failure
  (csnyder@redhat.com)
- 1444718: Log name of config when duplicate reports are retrieved
  (csnyder@redhat.com)
- 1447264: Keep running on InvalidPasswordFormat given other valid configs
  (csnyder@redhat.com)
- 1448267: Fix polling behavior for oneshot, CTRL-C, 429 responses
  (csnyder@redhat.com)
- 1369107: Update docs and log messages to show the *.conf requirement
  (csnyder@redhat.com)
- 1436517: Fix api base detection for rhevm version 3 and 4
  (csnyder@redhat.com)
- 1442337: Send updates immediately the first run (csnyder@redhat.com)
- Do not join threads not started, fix up fake backend (csnyder@redhat.com)
- 1439317: Ensure reports are still sent despite duplicate configurations
  (csnyder@redhat.com)
- DestinationThreads now send all reports (csnyder@redhat.com)
- Adds IntervalThread base class and refactors Virt classes
  (csnyder@redhat.com)
- Remove reference to nonexistant method _set_option (csnyder@redhat.com)
- Update ConfigManager to produce destination and source mappings.
  (csnyder@redhat.com)
- Implemements a threadsafe datastore (csnyder@redhat.com)
- Move from using processes to threads (csnyder@redhat.com)
- 1436517: Set Version header for version detect (pcreech@redhat.com)
- 1403640: Fix syntax error in exception handling (pcreech@redhat.com)
- Update the spec file for builds on more downstream platforms
  (csnyder@redhat.com)
- Add releaser for rhel-7.4 (khowell@redhat.com)
- 1391512: Handle utf-8 within Xmlrpc transport (pcreech@redhat.com)

* Thu Mar 02 2017 Christopher Snyder <csnyder@redhat.com> 0.19-1
- 1415497: Support rhev4 auto detection and usage (pcreech@redhat.com)
- 1388577: Adding UTF-8 support (pcreech@redhat.com)
- 1410000: Include org_id in hv base channel (pcreech@redhat.com)
- 1400431: Fix AttributeError where val is missing (pcreech@redhat.com)
- 1405967: Filter host via glob or regex (pcreech@redhat.com)
- Adds --password option to virt-who-pasword (tstrachota@redhat.com)
- 1392390 Fix default interval handling (pcreech@redhat.com)
- BZ1405967  Add filter_hosts_regex, and exclude_hosts_regex to allow filtering
  large numbers of hosts easily (chris@chrisprocter.co.uk)
- 1369107: Only load files with .conf extension (pcreech@redhat.com)
- 1383436: Obey the interval setting (csnyder@redhat.com)
- 1299643: Update virt-who-config man page to include NO_PROXY
  (csnyder@redhat.com)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 11 2016 Radek Novacek <rnovacek@redhat.com> 0.18-1
- Version 0.18

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 24 2016 Radek Novacek <rnovacek@redhat.com> - 0.17-1
- Rebase to 0.17

* Tue May 17 2016 Radek Novacek <rnovacek@redhat.com> 0.17-1
- Version 0.17

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Radek Novacek <rnovacek@redhat.com> 0.16-1
- Version 0.16

* Tue Aug 04 2015 Devan Goodwin <dgoodwin@rm-rf.ca> 0.15-1
- Update spec for renamed README.md. (dgoodwin@redhat.com)
- Moves fakevirt._decode() to util.decode() (csnyder@redhat.com)
- Adds the report.config.name to log message when refusing to send a report due
  to lack of change (csnyder@redhat.com)
- VirtWho: Clears list of reports on reload (csnyder@redhat.com)
- Revises change detection tests to account for changes in master
  (csnyder@redhat.com)
- Libvirtd: Sends a report on start up, and on events (csnyder@redhat.com)
- Removes trailing line at the end of the file (csnyder@redhat.com)
- Test_Esx: Test Oneshot to ensure it queues a report (csnyder@redhat.com)
- Esx: only queue data if the version has changed (csnyder@redhat.com)
- Test_VirtWho:Patches manager.Manager.fromOptions, removes unnecessary mocks
  (csnyder@redhat.com)
- Removes unhelpful debug log message (csnyder@redhat.com)
- Fix spacing, remove unused imports (csnyder@redhat.com)
- Test_VirtWho: Adds test to show same report will not be sent twice
  (csnyder@redhat.com)
- VirtWho: Adds basic change detection using report hashs (csnyder@redhat.com)
- Adds hash property to config (csnyder@redhat.com)
- Adds hash property to DomainListReport and HypervisorGuestAssociationReport
  (csnyder@redhat.com)
- Hypervisor: Adds getHash class method (csnyder@redhat.com)
- Limits interval settings (wpoteat@redhat.com)
- Retry sending data to subscription manager multiple times before dropping
  (rnovacek@redhat.com)
- SubscriptionManager: nicely order keys in debug report (rnovacek@redhat.com)
- Fix serialization of guest list in print mode (rnovacek@redhat.com)
- Do not exit oneshot mode if any job exists (rnovacek@redhat.com)
- SubscriptionManager: check if report result has failedUpdate item
  (rnovacek@redhat.com)
- SubscriptionManager: minor logging fixes (rnovacek@redhat.com)
- SubscriptionManager: add env var to disable asynchronous reporting
  (rnovacek@redhat.com)
- Check jobs status in increasing interval (rnovacek@redhat.com)
- Esx: report host even if it doesn't have any guests (rnovacek@redhat.com)
- Hypervisors reported by hyperv now include hostname. (csnyder@redhat.com)
- Removes completed jobs. (csnyder@redhat.com)
- Fix output format in print mode (rnovacek@redhat.com)
- Fix using empty list as default parameter value (rnovacek@redhat.com)
- satellite: support new hypervisor format (rnovacek@redhat.com)
- Fix tests failures (rnovacek@redhat.com)
- Removes timeouts for jobs. All jobs in the list are now executed just before
  a new report is sent. (csnyder@redhat.com)
- The virtwho loop now blocks on the report queue with a one second timeout
  (csnyder@redhat.com)
- Removes unnecessary imports and queue (csnyder@redhat.com)
- Rewrite readme to markdown syntax (rnovacek@redhat.com)
- CI: install unittest2 from pypi (rnovacek@redhat.com)
- CI: add -y option to add-apt-repository (rnovacek@redhat.com)
- CI: another attempt on cloud archive for libvirt (rnovacek@redhat.com)
- CI: try to install newer version of libvirt from cloud archive
  (rnovacek@redhat.com)
- CI: add libvirt-dev dependency (rnovacek@redhat.com)
- CI: install libvirt-python via pip (rnovacek@redhat.com)
- CI: another attempt without site-packages (rnovacek@redhat.com)
- CI: install python-rhsm dependencies (rnovacek@redhat.com)
- Adds support for facts in Hypervisor profile. (csnyder@redhat.com)
- Adds count of unchanged mappings to the info logged for the result of an
  async job (csnyder@redhat.com)
- Adds tests for jobs in virtwho, removes unnecessary tests for managerprocess.
  (csnyder@redhat.com)
- Changes to ensure backwards compatibility with python-rhsm
  (csnyder@redhat.com)
- Fixes RhevM.getHostGuestMapping() as suggested by rnovacek
  (csnyder@redhat.com)
- Adds layer to hypervisorId. Removes completed TODO (csnyder@redhat.com)
- Moves all functionality of managerprocess into virtwho. (csnyder@redhat.com)
- CI: use python with system side packages enabled (rnovacek@redhat.com)
- CI: install m2crypto using apt instead of pip (rnovacek@redhat.com)
- CI: install python-libvirt using apt instead of pip (rnovacek@redhat.com)
- Add requirements.txt and .travis.yml for the CI (rnovacek@redhat.com)
- Adds tests to verify the hostGuestAssociation is generated correctly.
  (csnyder@redhat.com)
- Updates libvirtd and tests to add host name to hypervisor profile
  (csnyder@redhat.com)
- Updates managerprocess with better logging and changes for the new tests.~~
  (csnyder@redhat.com)
- Updates to use the new hypervisor class (csnyder@redhat.com)
- print mode: format debug message about found hypervisors
  (rnovacek@redhat.com)
- Removing uncesasary comments (csnyder@redhat.com)
- Removes unused dictionary of jobs and associated methods.
  (csnyder@redhat.com)
- Fixes tests data to include "status" key. (csnyder@redhat.com)
- Updates tests to make use of new Hypervisor class. (csnyder@redhat.com)
- Host name is now included in the hypervisor profile using the new Hypervisor
  class (csnyder@redhat.com)
- Adds new Hypervisor class. (csnyder@redhat.com)
- Adds new test for the updates to subscriptionmanager.py (csnyder@redhat.com)
- Updates fakevirt to make use of virt.Guest classes (csnyder@redhat.com)
- Changes to ensure proper execution post-merge (csnyder@redhat.com)
- Removing more unnecessary prints (csnyder@redhat.com)
- Fixes oneshot mode for work with new managerprocess (csnyder@redhat.com)
- Cleaning up unneeded prints and adding more useful debug log messages
  (csnyder@redhat.com)
- Adds async job status polling for use with the new report API
  (csnyder@redhat.com)
- This (along with python-rhsm/csnyder/new_report_api ee38f15, allows
  communication with new report api (csnyder@redhat.com)

* Tue Jun 23 2015 Radek Novacek <rnovacek@redhat.com> 0.14-1
- Version 0.14

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 17 2015 Radek Novacek <rnovacek@redhat.com> 0.13-1
- new package built with tito

* Fri Feb 27 2015 Radek Novacek <rnovacek@redhat.com> 0.12-1
- Version 0.12

* Tue Feb 03 2015 Radek Novacek <rnovacek@redhat.com> 0.8-11
- Fix permission of /etc/sysconfig/virt-who file
- Resolves: #1186034

* Mon Sep 08 2014 Radek Novacek <rnovacek@redhat.com> 0.11-1
- Version 0.11

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Radek Novacek <rnovacek@redhat.com> 0.10-1
- Add directory with configuration files
- Version 0.10

* Thu Mar 13 2014 Radek Novacek <rnovacek@redhat.com> 0.9-1
- Remove libvirt dependency
- Add dependency on m2crypto
- Version 0.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Radek Novacek <rnovacek@redhat.com> 0.8-8
- Increase ESXi compatibility
- Resolves: rhbz#923760

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Radek Novacek <rnovacek@redhat.com> 0.8-6
- Add systemd support
- specfile cleanup

* Thu Oct 25 2012 Radek Novacek <rnovacek@redhat.com> 0.8-5
- Fix adding https:// to ESX url

* Wed Oct 24 2012 Radek Novacek <rnovacek@redhat.com> 0.8-4
- Help and manpage improvements

* Wed Oct 17 2012 Radek Novacek <rnovacek@redhat.com> 0.8-3
- Fix bugs in Hyper-V support (patch rebased)
- Create PID file ASAP to prevent service stop fails

* Thu Oct 11 2012 Radek Novacek <rnovacek@redhat.com> 0.8-2
- Add support for accessing Hyper-V

* Wed Sep 26 2012 Radek Novacek <rnovacek@redhat.com> 0.8-1
- Upstream version 0.8
- RFE: command line improvements
- Add support for accessing RHEV-M
- Fix printing tracebacks on terminal

* Fri Sep 14 2012 Radek Novacek <rnovacek@redhat.com> 0.8-1
- Version 0.8

* Mon Jul 09 2012 Radek Novacek <rnovacek@redhat.com> 0.7-1
- Version 0.7

* Thu Apr 26 2012 Radek Novacek <rnovacek@redhat.com> 0.6-6
- Handle unknown libvirt event properly

* Wed Apr 18 2012 Radek Novacek <rnovacek@redhat.com> 0.6-5
- Enable debug output to be written to stderr
- Log guest list to log even in non-debug mode

* Tue Apr 17 2012 Radek Novacek <rnovacek@redhat.com> 0.6-4
- Fix regression in double fork patch

* Wed Mar 28 2012 Radek Novacek <rnovacek@redhat.com> 0.6-3
- Do double fork when daemon is starting

* Fri Mar 09 2012 Radek Novacek <rnovacek@redhat.com> 0.6-2
- Add python-suds require
- Requires python-rhsm >= 0.98.6

* Thu Mar 01 2012 Radek Novacek <rnovacek@redhat.com> 0.6-1
- Rebase to virt-who-0.6

* Mon Feb 13 2012 Radek Novacek <rnovacek@redhat.com> 0.6-1
- Version 0.6

* Fri Dec 09 2011 Radek Novacek <rnovacek@redhat.com> 0.5-1
- VSphere support
- Req: python-suds

* Wed Nov 30 2011 Radek Novacek <rnovacek@redhat.com> 0.4-1
- Version 0.4

* Wed Oct 12 2011 Radek Novacek <rnovacek@redhat.com> 0.3-3
- Use updateConsumer API instead of updateConsumerFact (fixes limit 255 chars of uuid list)
- Requires python-rhsm >= 0.96.13

* Thu Oct 06 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-2
- Requires python-rhsm >= 0.96.13 (contains fix for char limit in uuid list)

* Wed Sep 07 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-2
- Add upstream patch that prevents failure when server not implements /status/ command

* Thu Sep 01 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-1
- Add initscript and configuration file

* Mon Aug 22 2011 Radek Novacek <rnovacek@redhat.com> - 0.2-2
- Bump release because of tagging in wrong branch

* Mon Aug 22 2011 Radek Novacek <rnovacek@redhat.com> - 0.2-1
- Update to upstream version 0.2
- Add Requires: libvirt

* Fri Aug 19 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-2
- Add BuildRoot tag (the package will be in RHEL5)

* Wed Aug 10 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-1
- initial import
