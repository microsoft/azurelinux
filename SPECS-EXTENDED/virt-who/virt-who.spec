%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%define use_python3 0%{?fedora} || (0%{?rhel} && 0%{?rhel} > 7)
%if %{use_python3}
%global python_ver python3
%global python_exec %{__python3}
%global python_sitelib %{python3_sitelib}
%else
%if !%{use_systemd}
%global __python2 %{__python}
%global python2_sitelib %{python_sitelib}
%endif
%global python_ver python
%global python_exec %{__python2}
%global python_sitelib %{python2_sitelib}
%endif
%global release_number 1

%global git_tag %{name}-%{version}-%{release_number}


Name:           virt-who
Version:        1.31.26
Release:        %{release_number}%{?dist}.3

Summary:        Agent for reporting virtual guest IDs to subscription-manager

Group:          System Environment/Base
# GPL for virt-who proper and LGPL for incorporated suds
License:        GPL-2.0-or-later AND LGPL-3.0-or-later
URL:            https://github.com/candlepin/virt-who
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  %{python_ver}-devel
BuildRequires:  %{python_ver}-setuptools
BuildRequires:  %{python_ver}-pyyaml

Requires:      %{python_ver}-setuptools
# libvirt python required for libvirt support
%if (0%{?rhel} && 0%{?rhel} > 7 || 0%{?fedora})
Requires:       %{python_ver}-libvirt
%else
Requires:       libvirt-python
%endif
# python-rhsm 1.20 has the M2Crypto wrappers needed to replace M2Crypto
# with the python standard libraries where plausible
%if %{use_python3}
Requires:       python3-subscription-manager-rhsm > 1.25.6
%else
Requires:       subscription-manager-rhsm > 1.25.6
%endif
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
Requires:       %{python_ver}-pyyaml

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
Provides: bundled(python-suds) = 0.8.4

%description
Agent that collects information about virtual guests present in the system and
report them to the subscription manager.

%prep
%setup -q

%build
%{python_exec} setup.py build --rpm-version=%{version}-%{release_number}

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
# This moves parameters from old config to remaining general config file
%if (0%{?fedora} > 33 || 0%{?rhel} > 8)
%{python_exec} %{python_sitelib}/virtwho/migrate/migrateconfiguration.py
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
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.26-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.31.26-1.2
- Rebuilt for Python 3.13

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.26-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Feb 01 2023 Jiri Hnidek <jhnidek@redhat.com> 1.31.26-1
- Fix stylish issue in migrateconfiguration.py (jhnidek@redhat.com)
- Added next rhel-9.x subversion to releasers.conf file. (jhnidek@redhat.com)
- 2158710: Migrated virt-who.conf, when necessary (jhnidek@redhat.com)
- Added documentation for the 'rhsm_insecure' option, for insecure connections
  (fernandez.santos.d@gmail.com)
- Added configuration for rhel-9.x into releasers.conf (jhnidek@redhat.com)

* Thu Oct 06 2022 William Poteat <wpoteat@redhat.com> 1.31.25-1
- 2099925: Drop support for RHEVM on RHEL 9 (jhnidek@redhat.com)
- Update virt-who-config.5 (s10w.1ife.31@gmail.com)
- Big optimization and refactoring of Nutanix code (jhnidek@redhat.com)

* Thu Sep 01 2022 William Poteat <wpoteat@redhat.com> 1.31.24-1
- 2118253: Nutanix: Gather information about VMs correctly (jhnidek@redhat.com)

* Thu Apr 21 2022 William Poteat <wpoteat@redhat.com> 1.31.23-1
- 2054504: Use usedforsecurity=False for md5() calls to make suds work on FIPS
  enabled systems (oalbrigt@redhat.com)

* Wed Mar 16 2022 William Poteat <wpoteat@redhat.com> 1.31.22-1
- 2060949: Indicate that virt-who provides python-suds in the spec file
  (wpoteat@redhat.com)
- Run complex tests as forked for consistent results (wpoteat@redhat.com)
- Update releasers for current needs (wpoteat@redhat.com)

* Tue Feb 08 2022 William Poteat <wpoteat@redhat.com> 1.31.21-1
- 1987247: The connection value shows null for kubevirt mode in virt-who status
  json (wpoteat@redhat.com)
- Addition of LGPLv3 license file from suds (wpoteat@redhat.com)
- 2000415: Nutanix config needs to handle bad server value (wpoteat@redhat.com)
- 1996942: Use cluster name instead of UUID for fabric consistency
  (wpoteat@redhat.com)
- 1990758: Virt-who always prints YAMLLoadWarning for kubevirt mode
  (wpoteat@redhat.com)
- 1990563: Move progress bar to stderr to keep stdout clean
  (wpoteat@redhat.com)

* Tue Feb 08 2022 William Poteat <wpoteat@redhat.com>
- 1987247: The connection value shows null for kubevirt mode in virt-who status
  json (wpoteat@redhat.com)
- Addition of LGPLv3 license file from suds (wpoteat@redhat.com)
- 2000415: Nutanix config needs to handle bad server value (wpoteat@redhat.com)
- 1996942: Use cluster name instead of UUID for fabric consistency
  (wpoteat@redhat.com)
- 1990758: Virt-who always prints YAMLLoadWarning for kubevirt mode
  (wpoteat@redhat.com)
- 1990563: Move progress bar to stderr to keep stdout clean
  (wpoteat@redhat.com)

* Mon Jan 10 2022 William Poteat <wpoteat@redhat.com> 1.31.19-1
- 1990562: Remove the redundant 'update_interval' option from ahv config
  (wpoteat@redhat.com)
- 1990561: rename configuration entry to show ahv specificity
  (wpoteat@redhat.com)

* Thu Dec 16 2021 William Poteat <wpoteat@redhat.com> 1.31.18-1
- 2000019: Convert non-latin1 username/password to bytes (jhnidek@redhat.com)
- 2018052: Fix virt-who -s, when Hyper-V with new API is used
  (jhnidek@redhat.com)
- ENT-4511: Remove six package from requirements (mhorky@redhat.com)
- ENT-4511: Drop Python 2 only tests (mhorky@redhat.com)
- ENT-4511: Drop six usage in suds tests (mhorky@redhat.com)
- ENT-4511: Drop six usage in tests (mhorky@redhat.com)
- ENT-4511: Drop six usage in virt-who code (mhorky@redhat.com)
- ENT-4511: Drop OrderedDict implementation (mhorky@redhat.com)
- Update for deprecation of MutableMapping (wpoteat@redhat.com)
- Only query the VM related taks in AHV hypervisors. (amir.eibagi@nutanix.com)
- Remove unused NTLM code as only basic auth is used (wpoteat@redhat.com)

* Tue Sep 14 2021 William Poteat <wpoteat@redhat.com> 1.31.17-1
- Bypass stylish check on suds code (wpoteat@redhat.com)
- 2000922: Add the suds code to virt-who in place of python3-suds package
  (wpoteat@redhat.com)
- ENT-4004: Fix flake8 issues for test files (mhorky@redhat.com)
- ENT-4004: Use four spaces for indentation (mhorky@redhat.com)
- ENT-4004: Fix flake8 issues (mhorky@redhat.com)
- ENT-4004: Add stylish tests (mhorky@redhat.com)
- Cannot use ESX where python3-suds is not available (wpoteat@redhat.com)
- 1981249: Stop using NTLM which requires MD4 (OpenSSL 3.0)
  (csnyder@redhat.com)
- 1989877: Status command does not reach actual credentials checking
  (wpoteat@redhat.com)
- Make changes to follow Conscious language initiative (mhorky@redhat.com)

* Fri Aug 06 2021 William Poteat <wpoteat@redhat.com> 1.31.16-1
- 1990550: Add the description for nutanix mode in man virt-who and man virt-
  who-config (wpoteat@redhat.com)
- 1990337: The guest state in mapping should be uniform with other hypervisors
  1990338: The guest shows wrong active value "0" in mapping when it's running
  (wpoteat@redhat.com)
- 1989646:  Get UnboundLocalError when configured hypervisor_id=hwuuid
  (wpoteat@redhat.com)
- 1989645: Add dmi.system.uuid to ahv facts (wpoteat@redhat.com)
- 1974624: proxy error with https (wpoteat@redhat.com)

* Tue Aug 03 2021 William Poteat <wpoteat@redhat.com> 1.31.15-1
- 1986973: Take out AHV removal patch mechanism (wpoteat@redhat.com)
- Update AHV patch (wpoteat@redhat.com)

* Fri Jul 16 2021 William Poteat <wpoteat@redhat.com> 1.31.14-1
- Merge run data into report (wpoteat@redhat.com)
- Update the man page for the status mode (wpoteat@redhat.com)
- Status execution (wpoteat@redhat.com)
- Record last dates of succcess for sources and destinations
  (wpoteat@redhat.com)
- Update certs for complex tests (wpoteat@redhat.com)

* Thu Jun 03 2021 William Poteat <wpoteat@redhat.com> 1.31.13-1
- 1965320: Clear previous report hash when hypervisor count is zero
  (wpoteat@redhat.com)
- Added support for Packit service (jhnidek@redhat.com)
- Convert CI from Travis to Jenkins (wpoteat@redhat.com)

* Fri May 21 2021 William Poteat <wpoteat@redhat.com> 1.31.12-1
- 1951347: Update patch for xen removal (wpoteat@redhat.com)

* Thu May 20 2021 William Poteat <wpoteat@redhat.com> 1.31.11-1
- 1951347: Remove Xen from hypervisor types (wpoteat@redhat.com)
- Releaser for Centos (wpoteat@redhat.com)

* Mon May 17 2021 William Poteat <wpoteat@redhat.com> 1.31.10-1
- 1920322: Uncomment section header on migrate (wpoteat@redhat.com)
- Update CI link to use branch name main (wpoteat@redhat.com)
- Fedora master branch name changed to main (wpoteat@redhat.com)

* Thu Feb 18 2021 William Poteat <wpoteat@redhat.com> 1.31.9-1
- Man page update to describe the migration script (wpoteat@redhat.com)
- 1924572: Add insecure option to config template (wpoteat@redhat.com)
- Add Fedora 34 to releaser list (wpoteat@redhat.com)

* Thu Jan 28 2021 William Poteat <wpoteat@redhat.com> 1.31.8-1
- Update AHV patch for Kubevirt change (wpoteat@redhat.com)

* Mon Jan 25 2021 William Poteat <wpoteat@redhat.com> 1.31.7-1
- 1917645: handle not running vms (piotr.kliczewski@gmail.com)
- Fedora 31 is no longer a build target (wpoteat@redhat.com)

* Fri Jan 15 2021 William Poteat <wpoteat@redhat.com> 1.31.6-1
- 1910020: replace deprecated call (wpoteat@redhat.com)

* Mon Jan 04 2021 William Poteat <wpoteat@redhat.com> 1.31.5-1
- 1909145: [RFE] Use single json format for input/output data
  (wpoteat@redhat.com)
- 1855550: [Remote Libvirt] The Name in Stage Candlepin cannot update based on
  hypervisor_id configuration (wpoteat@redhat.com)
- 1879329: List possible values for type in man page (wpoteat@redhat.com)

* Tue Dec 08 2020 William Poteat <wpoteat@redhat.com> 1.31.4-1
- 1899652: Install script error when file does not exist (wpoteat@redhat.com)

* Fri Dec 04 2020 William Poteat <wpoteat@redhat.com> 1.31.3-1
- 1899652: Update to ahv patch file (wpoteat@redhat.com)

* Wed Dec 02 2020 William Poteat <wpoteat@redhat.com> 0.31.2-1
- 1896652: platform-python-setuptools is not in RHEL9 (wpoteat@redhat.com)

* Tue Nov 17 2020 William Poteat <wpoteat@redhat.com> 0.31.1-1
- 1658440: Remove the use of environment variables for configuration
  (wpoteat@redhat.com)
- Do not use deprecated isAlive() but use is_alive() (jhnidek@redhat.com)
- 1890421: New section of virt-who.conf file for environment variables
  (wpoteat@redhat.com)

* Thu Oct 22 2020 William Poteat <wpoteat@redhat.com> 0.31.0-1
- 1876927: virt-who fails to parse output from hypervisor (wpoteat@redhat.com)
- Additional copy of patch file needed for build Update of Fedora versions in
  releaser file (wpoteat@redhat.com)
- Correction in patch builder for directory location (wpoteat@redhat.com)
- Update releasers (wpoteat@redhat.com)
- 1878136: Deprecation comment in config file (wpoteat@redhat.com)
- 1854829: rhsm_port and rhsm_password are missing in template.conf
  (wpoteat@redhat.com)

* Thu Oct 01 2020 William Poteat <wpoteat@redhat.com> 0.30.0-1
- Add patch to remove AHV bits for RHEL builds (wpoteat@redhat.com)
- 1878136: Deprecation warning for environment variables (wpoteat@redhat.com)
- 184506: virt-who should send its version in the User-Agent header
  (wpoteat@redhat.com)
- 1806572: RHEVM API url needs version specified (wpoteat@redhat.com)
- 1847792: [ESX] Virt-who is failed when run with
  "filter/exclude_host_parents=" option (wpoteat@redhat.com)
- 1809098: Convert UUID to big-endian for certain esx hardware versions
  (wpoteat@redhat.com)
- 1835132: support milicpus (piotr.kliczewski@gmail.com)

* Thu May 21 2020 William Poteat <wpoteat@redhat.com> 0.29.2-1
- NTLM: Fix compatibility issue with Python3.8 (jhnidek@redhat.com)
- 1806572: RHEVM should only use version 4 (wpoteat@redhat.com)
- Update to tests to match changes in Subscription Manager (jhnidek@redhat.com)
- 1461272: Filter virt-who hosts based on host_parents using wildcard
  (wpoteat@redhat.com)

* Fri May 08 2020 William Poteat <wpoteat@redhat.com> 0.29.1-1
- 1806572: virt-who using V3 APIs for communication with RHEVM which is
  deprecated (wpoteat@redhat.com)
- Update Fedora releases (wpoteat@redhat.com)

* Fri Apr 03 2020 William Poteat <wpoteat@redhat.com> 0.29.0-1
- Update releasers for RHEL-8.3 (wpoteat@redhat.com)
- 1775535: config option to override api version (piotr.kliczewski@gmail.com)
- 1780467: Validate rhevm password when unicode is not allowed
  (wpoteat@redhat.com)
- 1727203: Validate server name for ASCII only in ESX (wpoteat@redhat.com)
- 1757985: better behavior of --config option; ENT-1713 (jhnidek@redhat.com)
- 1751441: Add command line path parameter (piotr.kliczewski@gmail.com)
- 1762780: fix bug, when reporter_id is empty; ENT-1706 (jhnidek@redhat.com)
- 1759869: Version file needs updating on rpm (wpoteat@redhat.com)
- 1776084 - Failed to run virt-who with Hyper-V (wpoteat@redhat.com)
- Proper placeholder (wpoteat@redhat.com)
- 1751441: remove strict need for kubeconfig (piotr.kliczewski@gmail.com)
- Update for 8.2 (wpoteat@redhat.com)
- 1748677: Improved timeout for esx (wpoteat@redhat.com)
- 1727130: Correct man page for default interval (wpoteat@redhat.com)
- 1743589: Content type header null coverage (wpoteat@redhat.com)
- 1751624: Allow unicode username only if python-requests allows it
  (wpoteat@redhat.com)
- 1745768: Make message unicode safe (wpoteat@redhat.com)
- 1516209: Proper handling for empty server entry (wpoteat@redhat.com)
- 1733286: add connection/request timeout (piotr.kliczewski@gmail.com)
- Remove vdsm capability (wpoteat@redhat.com)
- 1720048: Template for general configuration not properly formatted
  (wpoteat@redhat.com)
- Add AHV v3 lenght and offset for the API calls. (amir.eibagi@nutanix.com)
- 1530254: Update checking on environment variables (wpoteat@redhat.com)
- 1714456: Update description of 'print_' config option (wpoteat@redhat.com)
- 1499679: Check for duplicates in conf file; ENT-249 (jhnidek@redhat.com)
- 1720154: Provide SYSTEM_UUID_FACT (piotr.kliczewski@gmail.com)
- 1516120: Handling for incorrect config section headers (wpoteat@redhat.com)
- 1722560: Make heartbeat more robust (jhnidek@redhat.com)
- Update spec for build system (wpoteat@redhat.com)
- 1416298: Use unique guest attribute for state tracking (wpoteat@redhat.com)

* Wed Jun 12 2019 William Poteat <wpoteat@redhat.com> 0.25.4-1
- 1718304: Fix issue when instance["BIOSGUID"] returns None
  (phess@users.noreply.github.com)
- 1652549: Add heartbeat call to virt-who cycle (wpoteat@redhat.com)
- 1472727: Log error, when encrypted password is missing; ENT-1344
  (jhnidek@redhat.com)
- 1714133: can't set data property (piotr.kliczewski@gmail.com)
- Add Nutanix AHV support for RHSS + UTs. (amir00018@gmail.com)

* Fri May 24 2019 William Poteat <wpoteat@redhat.com> 0.25.3-1
- 1530290: Remove enviroment as an input variable for the hypervisor check in
  (wpoteat@redhat.com)
- 1523482: 1519704: Interval value set to empty string will revert to default
  value (wpoteat@redhat.com)
- 1522384: Log at debug level when config uses default entries
  (wpoteat@redhat.com)
- 1708524: update man page with kubevirt backend information
  (piotr.kliczewski@gmail.com)
- 1708534: add kubeconfig to template (piotr.kliczewski@gmail.com)
- 1516209: Configuration should be deemed invalid when server is not specified
  (wpoteat@redhat.com)
- 1640967: Add xen type listing in /etc/virt-who.d/template.conf
  (wpoteat@redhat.com)

* Tue May 14 2019 William Poteat <wpoteat@redhat.com> 0.25.2-1
- Update to spec for pyyaml package (wpoteat@redhat.com)

* Tue May 14 2019 William Poteat <wpoteat@redhat.com>
- Update to spec for pyyaml package (wpoteat@redhat.com)

* Mon May 13 2019 William Poteat <wpoteat@redhat.com> 0.25.0-1
- Update releasers (wpoteat@redhat.com)
- 1641953: Virt-who fails if one hypervisor has wrong encrypted password
  (wpoteat@redhat.com)
- 1506167: Ignore new SIGHUP signals during signal handling
  (jhnidek@redhat.com)
- 1522661: Constrict is_hypervisor field to fake virt (wpoteat@redhat.com)
- 1695538: Provide support for hypervisor_id option
  (piotr.kliczewski@gmail.com)
- 1695519: use correct uuid in kubevirt report (piotr.kliczewski@gmail.com)

* Mon May 13 2019 William Poteat <wpoteat@redhat.com>
- Update releasers (wpoteat@redhat.com)
- 1641953: Virt-who fails if one hypervisor has wrong encrypted password
  (wpoteat@redhat.com)
- 1506167: Ignore new SIGHUP signals during signal handling
  (jhnidek@redhat.com)
- 1522661: Constrict is_hypervisor field to fake virt (wpoteat@redhat.com)
- 1695538: Provide support for hypervisor_id option
  (piotr.kliczewski@gmail.com)
- 1695519: use correct uuid in kubevirt report (piotr.kliczewski@gmail.com)

* Wed Apr 03 2019 William Poteat <wpoteat@redhat.com> 0.24.4-1
- 1667522: Omit ESX host from report when no hostname is present
  (wpoteat@redhat.com)
- 1693858: Send hardware uuid on every check in for system reconcilliation
  (wpoteat@redhat.com)
- kubevirt: provide user authentication (piotr.kliczewski@gmail.com)
- 1486270: pass no_proxy from config files (wpoteat@redhat.com)
- kubevirt: drop kubernetes and kubevirt dependencies
  (piotr.kliczewski@gmail.com)
- 1638250: Improved fix for http proxy issue (wpoteat@redhat.com)
- Update releaser (wpoteat@redhat.com)

* Wed Apr 03 2019 William Poteat <wpoteat@redhat.com>
- 1667522: Omit ESX host from report when no hostname is present
  (wpoteat@redhat.com)
- 1693858: Send hardware uuid on every check in for system reconcilliation
  (wpoteat@redhat.com)
- kubevirt: provide user authentication (piotr.kliczewski@gmail.com)
- 1486270: pass no_proxy from config files (wpoteat@redhat.com)
- kubevirt: drop kubernetes and kubevirt dependencies
  (piotr.kliczewski@gmail.com)
- 1638250: Improved fix for http proxy issue (wpoteat@redhat.com)
- Update releaser (wpoteat@redhat.com)

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
