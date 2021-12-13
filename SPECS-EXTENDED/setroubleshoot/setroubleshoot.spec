Vendor:         Microsoft Corporation
Distribution:   Mariner
# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0

Summary: Helps troubleshoot SELinux problems
Name: setroubleshoot
Version: 3.3.24
Release: 3%{?dist}
License: GPLv2+
URL: https://pagure.io/setroubleshoot
Source0: https://releases.pagure.org/setroubleshoot/%{name}-%{version}.tar.gz
Source1: %{name}.tmpfiles
# git format-patch -N setroubleshoot-3.3.24 -- framework
# i=1; for j in 00*patch; do printf "Patch%04d: %s\n" $i $j; i=$((i+1));done
Patch0001: 0001-framework-Update-translations.patch
BuildRequires: gcc
BuildRequires: libcap-ng-devel
BuildRequires: intltool gettext python3 python3-devel
BuildRequires: desktop-file-utils dbus-glib-devel gtk2-devel libnotify-devel audit-libs-devel libselinux-devel polkit-devel
BuildRequires: python3-libselinux python3-pydbus python3-gobject gtk3-devel
Requires: %{name}-server = %{version}-%{release}
Requires: gtk3, libnotify
Requires: libreport-gtk >= 2.2.1-2, python3-libreport
Requires: python3-gobject, python3-pydbus
Requires(post): desktop-file-utils
Requires(post): dbus
Requires(postun): desktop-file-utils
Requires(postun): dbus

BuildRequires: xdg-utils
Requires: xdg-utils

%global pkgpythondir  %{python3_sitelib}/%{name}
%global pkgguidir     %{_datadir}/%{name}/gui
%global pkgdatadir    %{_datadir}/%{name}
%global pkglibexecdir %{_prefix}/libexec/%{name}
%global pkgvardatadir %{_localstatedir}/lib/%{name}
%global pkgconfigdir  %{_sysconfdir}/%{name}
%global pkgdatabase   %{pkgvardatadir}/setroubleshoot_database.xml
%global username      setroubleshoot

%description
setroubleshoot GUI. Application that allows you to view setroubleshoot-server
messages.
Provides tools to help diagnose SELinux problems. When AVC messages
are generated an alert can be generated that will give information
about the problem and help track its resolution. Alerts can be configured
to user preference. The same tools can be run on existing log files.

%files
%{pkgguidir}
%config(noreplace) %{_sysconfdir}/xdg/autostart/*
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/dbus-1/services/sealert.service
%{_datadir}/icons/hicolor/*/*/*
%dir %attr(0755,root,root) %{pkgpythondir}
%{pkgpythondir}/browser.py
%{pkgpythondir}/__pycache__/browser.cpython*
%{pkgpythondir}/gui_utils.py
%{pkgpythondir}/__pycache__/gui_utils.cpython*
%{_bindir}/seapplet


%prep
%autosetup -p 2

%build
autoreconf -f
%configure PYTHON=%{__python3} --enable-seappletlegacy=yes --with-auditpluginsdir=/etc/audit/plugins.d
make

%install
%make_install PREFIX=/usr
desktop-file-install --vendor="" --dir=%{buildroot}%{_datadir}/applications %{buildroot}/%{_datadir}/applications/%{name}.desktop
mkdir -p %{buildroot}%{pkgvardatadir}
mkdir -p %{buildroot}%{_rundir}/setroubleshoot
touch %{buildroot}%{pkgdatabase}
touch %{buildroot}%{pkgvardatadir}/email_alert_recipients
rm -rf %{buildroot}/usr/share/doc/
# create /run/setroubleshoot on boot
install -m644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf


%find_lang %{name}

%package server
Summary: SELinux troubleshoot server

Requires: %{name}-plugins >= 3.3.10
Requires: audit >= 3
Requires: audit-libs-python3
Requires: libxml2-python3
Requires: python3-rpm
Requires: libselinux-python3  >= 2.1.5-1
Requires: policycoreutils-python-utils
BuildRequires: intltool gettext python3
BuildRequires: python3-devel
Requires: python3-slip-dbus systemd-python3 >= 206-1
Requires: python3-gobject-base >= 3.11
Requires: dbus
Requires: python3-dbus python3-pydbus
Requires: polkit
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description server
Provides tools to help diagnose SELinux problems. When AVC messages
are generated an alert can be generated that will give information
about the problem and help track its resolution. Alerts can be configured
to user preference. The same tools can be run on existing log files.

%pre server
getent passwd %{username} >/dev/null || useradd -r -U -s /usr/sbin/nologin -d %{pkgvardatadir} %{username}

%post server
/sbin/service auditd reload >/dev/null 2>&1 || :

%postun server
/sbin/service auditd reload >/dev/null 2>&1 || :

%triggerun server -- %{name}-server < 3.2.24-4
chown -R setroubleshoot:setroubleshoot %{pkgvardatadir}

%files server -f %{name}.lang
%{_bindir}/sealert
%{_sbindir}/sedispatch
%{_sbindir}/setroubleshootd
%{python3_sitelib}/setroubleshoot*.egg-info
%dir %attr(0755,root,root) %{pkgconfigdir}
%dir %{pkgpythondir}
%dir %{pkgpythondir}/__pycache__
%{pkgpythondir}/Plugin.py
%{pkgpythondir}/__init__.py
%{pkgpythondir}/access_control.py
%{pkgpythondir}/analyze.py
%{pkgpythondir}/audit_data.py
%{pkgpythondir}/avc_audit.py
%{pkgpythondir}/config.py
%{pkgpythondir}/email_alert.py
%{pkgpythondir}/errcode.py
%{pkgpythondir}/html_util.py
%{pkgpythondir}/rpc.py
%{pkgpythondir}/serverconnection.py
%{pkgpythondir}/rpc_interfaces.py
%{pkgpythondir}/server.py
%{pkgpythondir}/signature.py
%{pkgpythondir}/util.py
%{pkgpythondir}/uuid.py
%{pkgpythondir}/xml_serialize.py
%{pkgpythondir}/__pycache__/Plugin.cpython*
%{pkgpythondir}/__pycache__/__init__.cpython*
%{pkgpythondir}/__pycache__/access_control.cpython*
%{pkgpythondir}/__pycache__/analyze.cpython*
%{pkgpythondir}/__pycache__/audit_data.cpython*
%{pkgpythondir}/__pycache__/avc_audit.cpython*
%{pkgpythondir}/__pycache__/config.cpython*
%{pkgpythondir}/__pycache__/email_alert.cpython*
%{pkgpythondir}/__pycache__/errcode.cpython*
%{pkgpythondir}/__pycache__/html_util.cpython*
%{pkgpythondir}/__pycache__/rpc.cpython*
%{pkgpythondir}/__pycache__/rpc_interfaces.cpython*
%{pkgpythondir}/__pycache__/server.cpython*
%{pkgpythondir}/__pycache__/serverconnection.cpython*
%{pkgpythondir}/__pycache__/signature.cpython*
%{pkgpythondir}/__pycache__/util.cpython*
%{pkgpythondir}/__pycache__/uuid.cpython*
%{pkgpythondir}/__pycache__/xml_serialize.cpython*
%dir %{pkgdatadir}
%{pkgdatadir}/SetroubleshootFixit.py
%{pkgdatadir}/SetroubleshootPrivileged.py
%config(noreplace) %{pkgconfigdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.fedoraproject.Setroubleshootd.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.fedoraproject.SetroubleshootPrivileged.conf
%attr(0700,setroubleshoot,setroubleshoot) %dir %{pkgvardatadir}
%ghost %attr(0600,setroubleshoot,setroubleshoot) %{pkgdatabase}
%ghost %attr(0644,setroubleshoot,setroubleshoot) %{pkgvardatadir}/email_alert_recipients
%{_mandir}/man1/seapplet.1.gz
%{_mandir}/man8/sealert.8.gz
%{_mandir}/man8/sedispatch.8.gz
%{_mandir}/man8/setroubleshootd.8.gz
%config /etc/audit/plugins.d/sedispatch.conf
%{_datadir}/dbus-1/system-services/org.fedoraproject.Setroubleshootd.service
%{_datadir}/dbus-1/system-services/org.fedoraproject.SetroubleshootPrivileged.service
%{_datadir}/polkit-1/actions/org.fedoraproject.setroubleshootfixit.policy
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.fedoraproject.SetroubleshootFixit.conf
%{_datadir}/dbus-1/system-services/org.fedoraproject.SetroubleshootFixit.service
%attr(0644,root,root) %{_tmpfilesdir}/%{name}.conf
%attr(0711,setroubleshoot,setroubleshoot) %dir %{_rundir}/setroubleshoot
%doc AUTHORS COPYING ChangeLog DBUS.md NEWS README TODO

%package legacy
Summary: SELinux troubleshoot legacy applet

Requires: gtk2
Requires: %{name} = %{version}-%{release}

%description legacy
SELinux troubleshoot legacy applet

%files legacy
%{_bindir}/seappletlegacy

%changelog
* Tue Jun 22 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.24-3
- Replacing dependency on 'rpm-python3' with 'python3-rpm'.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.24-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Tue Oct 13 2020 Petr Lautrbach <plautrba@redhat.com> - 3.3.24-1
 - Add 'fur' into shipped locales
 - Update translations
 - Log full reports with correct syslog identifier
 - Cancel pending alarm during AVC analyses

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 3.3.23-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Apr 21 2020 Vit Mojzis <vmojzis@redhat.com> - 3.3.23-1
- browser: Check return value of Gdk.Screen().get_default()
- Improve and unify error messages
- setroubleshoot.util: Catch exceptions from sepolicy import
- Add dpkg support
- Do not refer to hardcoded selinux-policy rpm in signature
- Make date/time format locale specific
- Improve speed of plugin evaluation

* Wed Mar  4 2020 Petr Lautrbach <plautrba@redhat.com> - 3.3.22-6
- Do not try to report a bug on None package (#1809801)

* Fri Feb 28 2020 Petr Lautrbach <plautrba@redhat.com> - 3.3.22-5
- root user doesn't need to use SetroubleshootPrivileged API

* Thu Feb 27 2020 Petr Lautrbach <plautrba@redhat.com> - 3.3.22-4
- sealert to report a bug on a package which owns the related SELinux domain
  https://pagure.io/setroubleshoot/issue/18

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 11 2020 Petr Lautrbach <plautrba@redhat.com> - 3.3.22-2
- Log plugin exception traceback when log level is DEBUG
- sepolicy.info() returns a generator, not a list (#1784564)

* Thu Jan  2 2020 Petr Lautrbach <plautrba@redhat.com> - 3.3.22-1
- sepolicy.info() returns a generator, not a list (#1784564)

* Wed Dec 11 2019 Vit Mojzis <vmojzis@redhat.com> - 3.3.21-1
- Fix AVC.__typeMatch to handle aliases properly
- Handle sockets with abstract path properly (#1775135)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.20-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Aug 27 2019 Petr Lautrbach <plautrba@redhat.com> - 3.3.20-3
- Use dbus.mainloop.glib.DBusGMainLoop() instead of dbus.glib

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.20-2
- Rebuilt for Python 3.8

* Wed Jul 17 2019 Vit Mojzis <vmojzis@redhat.com> - 3.3.20-1
- Update "missing" scripts to automake-1.15
- Add active polling for acquiring policy file
- Fix translation of hex values in AVCs
- require initscripts to ensure that "service" call works properly
- Add man page for seapplet
- setroubleshoot-server: only require gobject-base

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec  8 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.19-1
- Require plugins >= 3.3.10

* Thu Nov 29 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.18-3
- Update scriptlets to reload auditd after install or uninstall

* Thu Sep 20 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.18-2
- Update translations
- Improve myplatform detection in get_os_environment()

* Wed Jul 18 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.18-1
- Move sedispatch.conf to /etc/audit/plugins.d/
- Fix summary and "if" text for AVCs with unknown target path

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.17-2
- Rebuilt for Python 3.7

* Mon Feb 26 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.17-1
- Set auto_save_interval to 5 (#1548913,#1523406,#1539180)
- seapplet: Try send and close notifications (#1541624,#1541719,#1544222,#1539367)

* Tue Feb 20 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.16-1
- Do not show status_icon when there's no alert (#1543758)
- Run seapplet only on SELinux enabled system (#1541631)
- Use context in Gio.AppInfo.launch (#1542156)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.3.15-3
- Escape macros in %%changelog

* Fri Jan 19 2018 Björn Esser <besser82@fedoraproject.org> - 3.3.15-2
- Fix runtime dependency: 's!lipreport!libreport!g' (#1536580)
- Prefer %%global over %%define
- Remove obsolete %%defattr(-,root,root,-)

* Fri Jan 19 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.15-1
- Rewrite seapplet to Python3 to use Notify and Gtk 3.0
- Add setroubleshoot-seappletlegacy with legacy seappletlegacy based on Gtk 2
- sealert: Finish dbus communication after error

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.3.14-4
- Remove obsolete scriptlets

* Thu Nov 23 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.14-3
- Update translations

* Mon Nov 20 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.14-2
- Update translations

* Sat Nov 18 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.14-1
- Increase the space for suggested solutions in sealert
- Highlight suggestions with the highest confidence
- Remove additional "If " string from plugin messages
- Fix sealert message for process2 (#1507909)
- Do not change if_string[0] to lowercase

* Fri Sep 15 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.13-1
- Don't stop when the plugin directory is empty
- Fix missing margins on Troubleshoot window
- Resize all solutions panels horizontally
- Fix missing priority color for proposed solutions
- Do not split If sentences to framework and plugins - requires
  setroubleshoot-plugins 3.3.8 at least (rhbz#1210243, rhbz#1322734, rhbz#1115510)
- Set translation domain for Gtk.Builder() object to have strings
  correctly translated
- Make labels on GtkButtons translatable
- Handla all exceptions from do_analyze_logfile()
- Fix semi-translated messages
- Update translations
- Do not catch POSIX signals (rhbz#1366004, rhbz#1419245)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.12-1
- Remove "Report bug" button when mozplugger plugin is used (#1290135)
- Change "check_for_man" return value upon failure (#1431191)
- Fix "plugin details" message content
- Add "init_args" function to Plugin
- Fix sealert crash when setroubleshootd fails to start (#1405003)
- Improve obtaining AVC object path
- Fix setroubleshootd.8
- Fix report problem summary string
- sealert - provide a better error message when SELinux is disabled
- Spelling fixes
- Python 3.6 invalid escape sequence deprecation fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.3.11-2
- Rebuild for Python 3.6

* Wed Aug 31 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.11-1
- Fix "list all alerts" in sealert gui (#1370272, #1332485)
- Fix sealert message for capability2 (#1360392)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.10-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Jul 16 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.10-1
- setroubleshootd fixed to catch all subprocess exceptions
- Translations updated

* Tue Jun 21 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.9.1-1
- Do not use dangerous shell=True
- Use subprocess.check_output() with a sequence of program arguments

* Thu Jun 02 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.8.1-1
- fixed get_all_alerts_ignored()

* Thu Jun 02 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.8-1
- added setroubleshootd_log.log_full=True|False directive
- setroubleshootd_log.level and sealert_log.level can be set to
  different values
- get_alert() and get_all_alerts_since() DBUS APIs change to use
  number of microseconds instead of date string
- setroubleshoot.conf cleanup

* Wed May 18 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.7-1
- Added new methods to DBUS API:
  set_filter(), get_all_alerts_ignored(), delete_alert()

* Fri May 06 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.6-1
- Translations updated (#1322654)
- Suggest my-<command>.pp modules instead of mypol.pp (#1329037)

* Thu Apr 14 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.5-3
- Drop unwanted debug message in sedispatch (#1326985)

* Thu Apr 07 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.5-2
- setroubleshoot: Ensure that dbus string param isn't null

* Mon Apr 04 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.5-1
- get_alert() DBUS API extended with more parameters
- sedispatch uses a timeout when collecting audit events (#1322771)
- Use correct packaging for byte compiled files (#1321047)

* Thu Feb 11 2016 Petr Lautrbach <plautrba@redhat.com> 3.3.4-1
- fixed traceback in SetroubleshootFixit.py (#1279396)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Petr Lautrbach <plautrba@redhat.com> 3.3.3-1
- fixed few UI browser problems
- extended DBUS API, see DBUS.md
- import MIMEText from the right module (#1297111)
- Fix several GTK deprecated warnings

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 16 2015 Richard Hughes <rhughes@redhat.com> - 3.3.1-0.3
- Move the AppData file to the right subpackage so it gets used.

* Fri Aug 28 2015 Michal Srb <msrb@redhat.com> - 3.3.1-0.2
- Sanitize requires for Python 3

* Tue Aug 18 2015 Petr Lautrbach <plautrba@redhat.com> 3.3.1-0.1
- port setroubleshoot to Python 3

* Mon Jul 27 2015 Petr Lautrbach <plautrba@redhat.com> 3.2.24-3
- setroubleshoot-server depends on policycoreutils-python-utils (#1246625)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Petr Lautrbach <plautrba@redhat.com> 3.2.24-1
- translations updated from https://fedora.zanata.org/project/view/setroubleshoot
- setroubleshoot_database.xml and email_alert_recipients are %%ghost again

* Thu Apr 09 2015 Petr Lautrbach <plautrba@redhat.com> 3.2.23-1
- setroubleshootd is set to be run as setroubleshoot user instead of root user
- several bugfixes

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 3.2.22-2
- Add an AppData file for the software center

* Thu Mar 26 2015 Petr Lautrbach <plautrba@redhat.com> 3.2.22-1
- Ship a symbolic setroubleshoot icon (#1182652)
- Fix get_rpm_nvr_*_temporary functions - CVE-2015-1815 (#1203352)

* Tue Feb 10 2015 Petr Lautrbach <plautrba@redhat.com> 3.2.21-1
- Provide the policy rpm in Bugzilla bug reports by jfilak@redhat.com

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 3.2.20-3
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.20-1
- Fix handling of target paths that decode screws up

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.19-1
- Remove at_console lines from policykit so cockpit can use dbus interfaces.

* Thu Apr 10 2014 Miroslav Grepl <mgrepl@redhat.com> - 3.2.18-1.1
- Add the policy rpm string to the user comments of an already reported bug from jfilak@redhat.com

* Tue Mar 25 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.18-1
- Stop sending syslog.LOG_DEBUG Messages unless loglevel is set to debug

* Tue Mar 25 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.18-1
- Stop sending syslog.LOG_DEBUG Messages unless loglevel is set to debug

* Mon Jan 20 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.17-1
- Fix unicode settings

* Tue Jan 7 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.16-2
- Remove requires for notify-python and yum

* Thu Jan 2 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.16-1
- Don't error out on no policy installed
- Update translations.

* Thu Jan 2 2014 Dan Walsh <dwalsh@redhat.com> - 3.2.15-2
- Eliminate requirement on service script.

* Tue Dec 3 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.15-1
- Update Lanquages
- Use setup.py in Makefile for setroubleshoot dir

* Wed Nov 20 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.14-2
- Add requires for libreport-python

* Mon Sep 16 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.14-1
- Remove "the the" typo from code.
- Update Translations

* Tue Sep 10 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.13-2
- Move some of the Requires block down to -server package

* Thu Aug 1 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.13-1
- Fix typo again in audit_data.py
- Make setroubleshoot less noicy in logs

* Thu Aug 1 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.12-1
- Fix typo in audit_data.py

* Thu Aug  1 2013 Adam Williamson <awilliam@redhat.com> - 3.2.11-2
- fix systemd-python requirement versioning

* Wed Jul 31 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.11-1
- Add journald support for OBJECT_ID when logging journal messages
- Update Translations.

* Tue May 21 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.10-1
- Make audit2allow optional, only requre policycoreutils-python not -devel.
- Update Translations.

* Tue May 7 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.9-1
- On update cp instead of rename, since there could be a situation where
someone has ~/.config on a different file sytem then ~.  It has happened.
- Fix --password spelling error
- Remove --quit option from sealert
- Update translations

* Fri Apr 19 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.8-1
- Fix handling of timeout attempt #2

* Fri Apr 19 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.7-1
- Fix translations to show in browser

* Fri Apr 19 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.6-1
- Fix handling of timeout
- Update Translations

* Mon Apr 8 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.5-1
- Remove old options from setroubleshoot usage statement.
- Update Translations

* Wed Mar 27 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.4-1
- Fix usage of "it's" versus its in man pages.
- Update Translations
 
* Tue Mar 26 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.3-2
- Remove requirement for setools-libs-python, no longer needed.

* Fri Feb 15 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.3-1
- Update Translations
- Fix audit2allow -R output to actually work.

* Fri Feb 15 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.2-1
- Fix handling of sesearch data

* Thu Jan 31 2013 Dan Walsh <dwalsh@redhat.com> - 3.2.1-1
- Remove sesearch from package and start using sepolicy from policycoreutils-python
- Fix retrieval of writable types to translate attributes into the group of types available, and not return non file types.

* Fri Jan 25 2013 Dan Walsh <dwalsh@redhat.com> - 3.1.21-2
- Need to add a requires for systemd-python

* Mon Jan 14 2013 Dan Walsh <dwalsh@redhat.com> - 3.1.21-1
- Update translations.
- Restart auditd service on install and removal

* Mon Jan 14 2013 Dan Walsh <dwalsh@redhat.com> - 3.1.20-1
- Update translations.

* Wed Dec 5 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.19-2
- Require policycoreutils-devel to pull in audit2allow

* Wed Dec 5 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.19-1
- Update Translations

* Tue Oct 9 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.18-1
- Update Translations
- Add keywords to desktop file

* Tue Oct 9 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.17-2
- Update Translations

* Thu Sep 20 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.17-1
- Update Translations

* Mon Aug 13 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.16-1
- Fix sealert to handle avc's in /var/log/messages which will be numbered 1400 and 1107 rather then AVC and USER_AVC
- Update Translations
- Fix hostname substitution to only effect hostnames

* Wed Jul 25 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.15-1
- More translation fixes.

* Wed Jul 25 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.14-1
- Fix Translations code to actually show translations

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 7 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.12-3
- Change requires to libreport-gtk instead of report-gtk

* Fri May 11 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.12-1
- Update translations
- Remove /var/log/setroubleshoot /run/setroubleshoot which are no longer used

* Wed May 9 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.11-1
- Update translations
- Only check for rpm on target process if is still exists

* Sat Mar 17 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.9-1
- Add file_types as a param to setroubleshoot.utils
- Update translations

* Thu Mar 8 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.8-1
- Add missing lanquages, using lang supported by gtk

* Thu Mar 8 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.7-1
- Add missing lanquages

* Thu Mar 8 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.6-1
- Remove gnome-keyring requirement

* Thu Mar 8 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.5-1
- Fix potential memory leak in setools
- Update to latest translations

* Thu Mar 1 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.4-1
- Update to latest translations

* Tue Feb 14 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.3-1
- Update to latest translations
- Fix handling of avc messages, missing \n
- Default to check for AVC's on login

* Mon Jan 23 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.2-1
- Fix crash caused by switching to syslog, and update trans

* Fri Jan 20 2012 Dan Walsh <dwalsh@redhat.com> - 3.1.1-1
- remove specific logging and move to syslog
- Fix handling of AVC messages broken by fix for memory leaks

* Tue Jan 17 2012 Dan Walsh <dwalsh@redhat.com> - 3.0.47-1
- Fixup for memory leaks

* Fri Jan 6 2012 Dan Walsh <dwalsh@redhat.com> - 3.0.45-1
- Update to latest translations

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 3.0.45-2
- optimize/update scriptlets
- don't own icons/hicolor
- drop %%config tag on applications/*.desktop

- Patch from Mgrepl to stop printable from crashing if None is passed in
- Update to latest translations

* Thu Dec 8 2011  <dwalsh@redhat.com> - 3.0.44-1
- Update to latest translations
- Fix memory leak in sedispatch

* Mon Dec 5 2011  <dwalsh@redhat.com> - 3.0.43-1
- Update to latest translations

* Fri Nov 11 2011  <dwalsh@redhat.com> - 3.0.42-1
- Set the gobject prg_name for better integration into the desktop

* Fri Nov 4 2011  <dwalsh@redhat.com> - 3.0.41-1
- Don't report to syslog when sedispatch gets an signal to exit.

* Wed Oct 26 2011  <dwalsh@redhat.com> - 3.0.40-1
- Apply Miroslav patch that rewrites sealert option handling with using optparse. Fixing conflicting options problems.

* Fri Aug 26 2011  <dwalsh@redhat.com> - 3.0.38-3
- Fix requires to include pygtk2-libglade

* Mon Aug 8 2011  <dwalsh@redhat.com> - 3.0.38-2
- Fix path to setroubleshoot xml in spec file

* Wed Jul 13 2011  <dwalsh@redhat.com> - 3.0.38-1
- Remove dependancy on X from sedispatch

* Fri Jun 24 2011  <dwalsh@redhat.com> - 3.0.37-1
- Move serverconnection.py and FixIt commands from setroubleshoot to setroubleshoot-server
- Remove run_cmd.py

* Tue May 24 2011  <dwalsh@redhat.com> - 3.0.35-1
- Make work on RHEL6
- Fix if Button to allow user to select full button

* Mon Apr 18 2011  <dwalsh@redhat.com> - 3.0.33-1
- Stop translating strings into bogus hex strings

* Mon Apr 11 2011  <dwalsh@redhat.com> - 3.0.31-1
- Allow browser to close even if windows are still open
- Cleanup imports in gui_utils.py

* Tue Mar 1 2011  <dwalsh@redhat.com> - 3.0.30-1
- Change seapplet to only check for AVCs on login, if checkonlogin flag is turned on in ~/.setroubleshoot file
- Fix list_all_alerts bug causing crash on bad type

* Mon Feb 21 2011  <dwalsh@redhat.com> - 3.0.29-1
- Fix handling of "/" in alert list
- Update translations

* Fri Feb 18 2011  <dwalsh@redhat.com> - 3.0.28-1
- Tighten up screen to fit on little screens

* Wed Feb 16 2011  <dwalsh@redhat.com> - 3.0.27-1
- Remove dependance on gnome python modules
- Update translations

* Wed Feb 9 2011  <dwalsh@redhat.com> - 3.0.26-1
- Cleanup handling of  current_alert
- Change Details button to say Plugin\nDetails

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011  <dwalsh@redhat.com> - 3.0.25-1
-  Turn off sensitivity of details button when no AVC's exist

* Mon Jan 24 2011  <dwalsh@redhat.com> - 3.0.24-1
- Add ProtocolError from xmlrpclib so Bugzilla reporting throwing an error will work.

* Tue Jan 18 2011  <dwalsh@redhat.com> - 3.0.23-1
- Fixup for allow_execstack have to add pid to avc struct

* Tue Jan 18 2011  <dwalsh@redhat.com> - 3.0.22-1
- Fix email_alerts to work with new infrastructure

* Fri Jan 7 2011  <dwalsh@redhat.com> - 3.0.20-1
- Added details button and context as tooltips to gui on front end for advanced users

* Thu Jan 6 2011  <dwalsh@redhat.com> - 3.0.19-1
- Fix man page to reflect change in gui
- Fix sealert -fixit call to import load_plugins
- update translations
- Fix handling of empty tpath in gui

* Thu Dec 23 2010  <dwalsh@redhat.com> - 3.0.17-1
- Fix dbus Introspect handling
- Make sealert use terminal for errors when in terminal mode

* Wed Dec 22 2010  <dwalsh@redhat.com> - 3.0.16-1
- Update Translations

* Thu Dec 2 2010  <dwalsh@redhat.com> - 3.0.15-1
- Fix Details Button
- Fix table display
- Handle situations when you have no spath and tpath

* Mon Nov 29 2010  <dwalsh@redhat.com> - 3.0.14-1
- Fix dbus config file to allow console to use sealert

* Mon Nov 29 2010  <dwalsh@redhat.com> - 3.0.13-1
- setroubleshoot will create /var/run/setroubleshoot if it does not exist

* Wed Nov 24 2010  <dwalsh@redhat.com> - 3.0.12-2
- Ghost /var/run/setroubleshoot

* Tue Nov 23 2010  <dwalsh@redhat.com> - 3.0.12-1
- Update translations
- Allow seapplet to check for updates

* Mon Nov 22 2010  <dwalsh@redhat.com> - 3.0.11-1
- Better handling of tracebacks in terminal mode
- Fix up messages on process and capability avc messages
- Update translations

* Fri Nov 19 2010  <dwalsh@redhat.com> - 3.0.9-1
- Fix config name

* Wed Nov 17 2010  <dwalsh@redhat.com> - 3.0.8-1
- Fix crash in sealert with missing log_*
- Report bugzillas in english

* Fri Nov 12 2010  <dwalsh@redhat.com> - 3.0.7-1
- Apply patch from Yuri Chornoivan to fix spelling mistakes
- Remove py files that are no longer used
- Add details button

* Wed Nov 10 2010  <dwalsh@redhat.com> - 3.0.6-1
- Fix handling of report_count and ignore button

* Mon Mar 15 2010  Dan Walsh <dwalsh@redhat.com> - 2.2.69-1
- Add white level, so plugins can tell setroubleshoot to ignore avc

* Mon Mar 8 2010  Dan Walsh <dwalsh@redhat.com> - 2.2.67-1
- Fix browser to handle ignore flag
- Remove tpath for signature 
- Fix audit2why handling for sealert and setroubleshoot
- Fix sort order selection
- Fix dontnotify handling

* Fri Mar 5 2010  Dan Walsh <dwalsh@redhat.com> - 2.2.66-1
- Update translations

* Mon Feb 22 2010  Dan Walsh <dwalsh@redhat.com> - 2.2.65-1
- Fix saving last position exception

* Sun Feb 14 2010  Dan Walsh <dwalsh@redhat.com> - 2.2.64-1
- Fix seapplet infinite loop from Tim Eliseo

* Wed Feb 10 2010  Dan Walsh <dwalsh@redhat.com> - 2.2.63-2
- Fix requires setools-libs-python line

* Thu Feb 4 2010  Dan Walsh <dwalsh@redhat.com> - 2.2.63-1
- Fix setroubleshoot seapplet to not show ignored avc

* Tue Feb 2 2010 Dan Walsh <dwalsh@redhat.com> - 2.2.62-1
- Remove packagekit dependancy

* Tue Jan 26 2010 Dan Walsh <dwalsh@redhat.com> - 2.2.61-1
- Add Gavin Romig-Koch report patch
- Cleanup Browser window
- Remove avc messages that are allowed or dontaudited in current poilcy

* Fri Jan 22 2010 Dan Walsh <dwalsh@redhat.com> - 2.2.60-1
- Remove untest attachfile code
- Catch ProtocolError

* Wed Jan 20 2010 Dan Walsh <dwalsh@redhat.com> - 2.2.58-1
- Fix remembering of bugzilla username/password 

* Tue Jan 19 2010 Dan Walsh <dwalsh@redhat.com> - 2.2.57-1
- Remove send_interface from Setroubleshootd.conf

* Mon Jan 18 2010 Dan Walsh <dwalsh@redhat.com> - 2.2.56-1
- Don't crash on missing inode
- Fix up default_encoding an translations

* Wed Jan 13 2010 Dan Walsh <dwalsh@redhat.com> - 2.2.55-2
- Cleanup spec file
- Add default_encoding
- Fix wording in bug report window

* Thu Dec 3 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.52-1
- Fix ignore button
- Add delete button

* Mon Nov 30 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.50-1
- Exit with error code if you run sealert as root and try to connect to session bus
- Fix Crash when ino is not defined

* Wed Nov 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.48-1
- Fix bug in substitute code

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.47-1
- Fix semanage fcontext lines to substitute "." for " " in path
- Update po

* Tue Nov 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.46-1
- Fix bugzilla reporting to work on RHEL6

* Tue Nov 3 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.45-1
- Do not translate hex files
- Catch exception on non dbus system

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.44-1
- Get version correct for both RHEL and Fedora

* Fri Oct 30 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.43-1
- Fix crash on selinux disabled and bad /etc/redhat-release reporing of bugzillas

* Mon Oct 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.42-1
- Update po
- Fix bugzilla reporting to handle LoadError exception
 
* Thu Oct 15 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.41-1
- Add icon to browser

* Thu Oct 15 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.40-1
- Fix up browser button handling when there are 0, 1 or more alerts

* Tue Oct 13 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.39-1
- Catch additional bugzilla exception

* Thu Oct 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.38-1
- Show that the application is starting.
- Fix ignore sealert button

* Wed Oct 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.37-1
- Don't throw up an error box if yum cache is not setup

* Mon Oct 5 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.36-1
- Fix Fix It button
- Remove Setroubleshoot: from every heading

* Thu Oct 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.35-1
- Fix translations, plurals and glade
  - Update Po
  - Fix plural form
  - Add support for Green Plugins

* Mon Sep 28 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.33-1
- Fix translations, plurals and glade

* Fri Sep 25 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.32-1
- Fix browser bug handling

* Thu Sep 24 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.31-1
- Fix translations

* Tue Sep 22 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.30-1
  - Update po and fix translation line
  
* Fri Sep 11 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.28-1
  -  Fix permissive domain check

* Thu Sep 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.27-1
- Close open file descriptors on exec

* Thu Sep 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.26-1
- Fix setroubleshoot error dialog and hash to catch more dups on reportbug

* Tue Sep 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.25-1
- Fix pipe and socket plugins to return tclass as path

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.24-1
- Fix permissive fix

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.23-3
- Add PackageKit requires

* Thu Aug 27 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.23-2
- Move  python-slip-dbus requirement to server package

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.23-1
- Fix Permissive Domain reporting

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.22-2
- Turn on libcap-ng-devel

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.22-1
- Differentiate between permissive domains and permissive mode

* Thu Aug 20 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.21-2
- Turn on libpcap

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.21-1
- Turn on copy to clipboard button

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.20-1
-Update to upstream 
        - 2009-8-18 Thomas Liu <tliu@redhat.com>
        - Added check for new policy.

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.19-1
- Default syscall field in audit_data

* Thu Aug 13 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.18-2
- Add buildrequires python-slip-dbus

* Thu Jul 30 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.18-1
- Add sgrubb drop capabilities, patch
- Fix infiniteloop

* Mon Jul 27 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.17-1
- Fix handling of mountpoints that the kernel reports as "/"

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.16-1
- Fix sesearch handling

* Sun Jul 19 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.15-1
- Fix a1 handling

* Mon Jul 13 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.14-1
- Update to upstream
  2009-7-15 Dan Walsh <dwalsh@redhat.com> 
  - Fix handling of syscall record a1 field
  - Translate "/" to mountpoint when returned by kernel

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.13-1
- Update to upstream
  2009-7-07 Thomas Liu <tliu@redhat.com> 
  - Fixed detail doc not clearing when deleting all alerts
  - Hid notify check when deleting all alerts.

* Wed Jul 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.12-1
- Fix locate code to use os.lstat

* Wed Jul 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.11-1
- Update to upstream
  2009-7-01 Thomas Liu <tliu@redhat.com> 
  - Fixed browser behavior when there are no alerts
  - Fixed seapplet behavior when there are no alerts
  - Made delete all button delete alerts on server side and on local side

* Mon Jun 29 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.10-1
- Add open access to audit_data.py define statements

* Fri Jun 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.9-1
- Update to upstream
  2009-6-25  Thomas Liu <tliu@redhat.com>
  - Added a "Copy to Clipboard" button to the browser GUI.

* Wed Jun 24 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.8-1
- Add sesearch 

* Mon Jun 22 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.1-1
- Fix handling of last seen
- Add open_with_write check

* Thu Jun 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.1-1
- Update to upstream
  * Thomas Liu <tliu@redhat.com>
  Bug fixes to GUI, added Delete All Alerts menu item.

* Tue Jun 16 2009 Dan Walsh <dwalsh@redhat.com> - 2.2.1-1
- Update to upstream
  * New Gui

* Wed Jun 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.13-2
- Fix handling of PATH with locatepwd

* Mon Jun 8  2009 Thomas Liu <tliu@redhat.com> - 2.1.12-2
- Redesign of GUI

* Wed Jun 3 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.12-1
- Fix handling of PATH 

* Thu May 21 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.11-1
- Fix crash when gathering stats

* Wed May 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.10-1
- Make sure setroubleshoot exists after 10 seconds 

* Mon May 4 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.9-1
- Change multiple signatures from exception to warning
- Update links on fedorahosted.org

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.8-1
- Fix sealert segfault

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.7-1
- Stop sending messages with scon or tcon == setroubleshootd_t

* Thu Mar 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.6-2
- Split out documentation

* Fri Feb 27 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.6-1
- Stop logging on normal shutdown of sedispatch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.5-1
- Fix cpu utilization problems
- Save database on exit

* Tue Feb 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.4-1
- make sure setroubleshoot is running when using sealert -l

* Tue Feb 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.3-1
- sedispatch needs to connect to dbus on avc arrival, 
  instead of startup, since the dbus daemon is not started 
  when sedispatch starts

* Wed Jan 21 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.2-1
- Fixes missing dbus config files

* Fri Jan 16 2009 Dan Walsh <dwalsh@redhat.com> - 2.1.1-1
- Switch to C Based applet
- Use dbus for messaging.  Only run setroubleshoot when 

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.12-2
- Rebuild for Python 2.6

* Wed Oct 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.12-1
- Update to upstream
  - 2008-10-06  Dan Walsh <dwalsh@redhat.com>
  - remove .png from desktop files

* Mon Sep 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.11-1
- Update to upstream
  - 2008-10-22    <jdennis@redhat.com>
    - Fix pruning code
    - Fix time stamps

* Wed Sep 10 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.10-2
- Fix requires line to gnome-python2-gnome

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.10-1
- Fix startup problems

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.8-2
- Fix setroubleshoot init to rely on messagebus being running

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.8-1
- Fix spelling mistakes
- Update translations

* Thu Feb 21 2008  <jdennis@redhat.com> - 2.0.6-1
  - add dialog to run a command in the background, capture it's stdout & stderr
    report it's status, kill it, and pass it a pseudo terminal for password prompts
    - separate the fix command into it's own section in formatted alerts
    - add UI for running the fix command, enable only if there is a single selection
      and the selected alert has a fix command
      - add a config parameters 'run_fix_cmd_enable' to control if fix commands
      can be run, defaults to False
      - Resolve bug 431380: prevent notify popups while setroubleshoot is open

* Wed Feb  6 2008 John Dennis <jdennis@redhat.com> - 2.0.5-1
- allow sealert -l lookup to accept * wildcard
- add a few more audit fields needing special decode handling

* Thu Jan 31 2008  <jdennis@redhat.com> - 2.0.4-1
- Resolve bug 430421: audit_listener_database.xml:3029: parser error in xmlParseDoc()
  rewrite the audit_msg_decode logic to beaware of specific audit fields
- add new template substitution $SOURCE, a friendly name, $SOURCE_PATH still exists
  and is the full path name of $SOURCE, also add 'source' attribute in AVC class,
  fix how source and source_path are computed from audit's comm and exe fields
- fix the computation of tpath to also look at the audit name field, formerly
  it had only been looking at path, fixes <Unknown> showing up for many targets
- add exception handling around xml file writes (Alan Cox reports problem when /var is full)
- add testing documentation
- Resolve bug 430845: obsolete URL in setroubleshoot package description
- Resolve bug 428960: Permissive message makes no sense.
- init script now allows extra test options
- show_browser() now opens and raises the window (e.g. presents) rather than just
  assuring it's realized (e.g. iconified, or hidden)
- sealert -l message in syslog converts from html before writing to syslog
- Resolve bug 320881: export setroubleshoot_selinux_symposium in PDF format
- add code to verify all async rpc's have been cleared from the async rpc cache
- add code to set a default rpc method return if the interface does not define a callbak
  (methods which did not have a callback were not returning anything and hence were no
   getting cleared from the cache)

* Fri Jan 11 2008  <jdennis@redhat.com> - 2.0.2-1
- Resolve bug 428252: Problem with update/remove old version
- Add code to validate xml database version, if file is incompatible it is not read,
   the next time the database is written it will be in the new version format.
   This means the database contents are not preserved across database version upgrades.
- Remove postun trigger from spec file used to clear database between incompatible versions
   the new database version check during database read will handle this instead
- bullet proof exit status in init script and rpm scriptlets
- Resolve bug 247302: setroubleshoot's autostart .desktop file fails to start under a KDE session
- Resolve bug 376041: Cannot check setroubleshoot service status as non-root
- Resolve bug 332281: remove obsolete translation
- Resolve bug 344331: No description in gnome-session-properties
- Resolve bug 358581: missing libuser-python dependency
- Resolve bug 426586: Renaming translation po file from sr@Latn to sr@latin
- Resolve bug 427260: German Translation
- enhance the sealert man page

* Fri Jan  4 2008  <jdennis@redhat.com> - 2.0.1-1
- make connection error message persist instead of timeout in browser
- updated Brazilian Portuguese translation: Igor Pires Soares <igor@fedoraproject.org>
- implement uid,username checks
- rpc methods now check for authenticated state
- fix html handling of summary string
- add 'named' messages to status bar, make sure all messages either timeout or are named
- fix ordering of menus, resolves bug 427418
- add 'hide quiet' to browser view filtering, resolves bug 427421
- tweak siginfo text formatting
- add logon to SECommandLine so that sealert -l <local_id> works
 
* Fri Dec 28 2007  <jdennis@redhat.com> - 2.0.0-1
- prepare for v2 test release
- Completed most work for version 2 of setroubleshoot, prepare for test release
- import Dan's changes from the mainline
   primarily allow_postfix_local_write_mail_spool plugin
- escape html, fix siginfo.format_html(), siginfo.format_text()
- add async-error signal
- change identity to just username
- make sure set_filter user validation works and reports error in browser
- fix generation of line numbers and host when connected to audispd
- add permissive notification, resolves bug 231334: Wording doesn't change for permissive mode
- resolves bug 244345: avc path information incomplete
- get the uid,gid when a client connects to the server
- set_filter now verifies the filter is owned by the user,
- resolves bug 288261: setroubleshoot lack of user authentication
- remove filter options which weren't being used
- change '@' in audit data hostname to '.'
- remove restart dialog
   resolves bug 321171: sealert's dialog after update is higly confusing
- fix rpc xml arg
- fix handling of host value
- tweak what fields are in signature
- move data items which had been in 'avc' object into siginfo
- clean up siginfo format
- large parts of new audit data pipeline working, checkpoint
- fix duplicate xml nodes when generating xml tree
- audit event can now be xml serialized
- switch from using int's for audit record types to strings
- avoid conversion headaches and possibilty of not being
   able to convert a new unknown type
- add logic to allow XmlSerialize to be subclassed and init_from_xml_node to be overridden
- add support to xml serialize classes AuditEventID, AuditEvent, AuditRecord
- use metaclass for xml class init
- start adding xml support to audit data classes
- Use metaclass to wrap class init
- move xml serialization code from signature.py to xml_serialize.py
- simplify aspect of the serialization code
- add unstructured xml mapping, each xml element name has its content mapped to obj.name
- modify xml serialization to be driven by xml contents
- general clean up
- checkpoint conversion of serialization to use metaclasses
- clean up class/data specifications for XmlSerializable
- add support for client rpc testing
- add changelog entry
- add SubProcess class to setroubleshootd in preparation to
- run daemon as subprocess so we can gather results and
   compare them to the expected data we sent
- rewrite all plugins to use new v2 audit data
- add SubProcess class to setroubleshootd in preparation to 
          run daemon as subprocess so we can gather results and
          compare them to the expected data we sent
- add new test support: add config section 'test', add boolean 'analyze' to
   config test section, add class TestPluginReportReceiver which is installed
   if test.analyze is True, it prints analysis report. In test_setroubleshootd
   send AUDIT_EOE to assure sequential event processing so analysis results
   have same ordering as events that are sent by test_setroubleshootd
- alert signatures now include host information, alerts will be grouped by host

* Tue Oct  2 2007 John Dennis <jdennis@redhat.com> - 1.10.7-1
- Fix spec file requires for opening an HTML page
   In configure.ac search for xdg-open and htmlview in priority order,
   set variable html_browser_open to the one found, in spec file require
   xdg-utils for fedora and htmlview for RHEL.

- add "Host" column in browser
   add "Toggle Column Visibility" menu to toggle display of any column on/off

- Resolves bug 310261: setroubleshoot notifications aren't throttled

- add support for AUDIT_EOE, end-of-event, if AUDIT_EOE immediately
   emit cached event. Disable timeouts used to flush events if
   AUDIT_EOE has been seen.
 
* Wed Sep 26 2007 John Dennis <jdennis@redhat.com> - 1.10.6-1
- make selinx-policy requires in spec file specific to dist tag

* Mon Sep 24 2007 John Dennis <jdennis@redhat.com> - 1.10.5-1
- update code for command line log file scanning to work with
   new log file scanning code introduced for the browser.

- update Bulgarian translation (Doncho N. Gunchev (gunchev@gmail.com))

- update Polish translation (Piotr Drąg (raven@pmail.pl))

- Resolves bug 239893: sealert wakes up very often
   This was caused by the use of threads and pygtk's thread signal
   handling.  The only use of threads in sealert was for log file
   scanning so that the UI would remain responsive during a
   scan. Threads in sealert have now been completely
   removed. Instead the scanning work is performed in a gobject idle
   function called from the main loop. The idle function is written
   as a python generator function which allows for the function to
   perform a small amount of work, save it's execution state and
   return. The next time the idle function is called from the main
   loop it resumes execution from it's last state until it decides
   to yield control again. This way the long running scan/analysis
   can be performed in small successive units of work during the
   time the application is otherwise idle and it does not interfere
   with the rest of the GUI event processing. Everything now occurs
   in an event loop, think of it as the applications process/thread
   scheduler whose event handlers execute time slices.

- rewrote parts of the audit input pipeline to use generators
   instead of callbacks, thus permitting the logfile scanning code
   to yield control with more granularity. Also updated
   test_setroubleshootd and audisp_listen to use the new
   generator/yield logic.

- rewrote the dialog used for scanning log files, progress bar
   updates are now in the dialog, the scan can be terminated part
   way through, errors from the scan are reported in pop-up dialog,
   one can only dismiss the dialog with success if the scan had
   been successfully run to completion, otherwise the user is only
   left with the option to cancel.

- Relates bug 252035  bug 247469, setroubleshootd and sealert should
   exit if SELinux is disabled.

- add utility functions escape_html() and unescape_html()

- fix initial sort order in browser, track sort order in browser

- modify AVC.get_path() to only return a value if the 'path' field is
   set, formerly it also considered the fields 'name' & 'file' which were
   incorrect. get_path() now also looks to see if the string begins with a
   slash for a fully qualified path, if not it looks to see if its a 
   pseudo path such as 'pipe[12345]' or 'socket[12345]' and if so strips out
   the instance information inside the brackets and returns just the type of 
   the pseudo path. This is done because we do not want path information
   in the signature to be unique for each instance of the denial.

- modify the TimeStamp class to hide it's internal datetime member,
   remove the cmp() method, the internal __cmp__ will be automatically invoked.

- require selinux policy version in spec file to allow system dbus use
 
- Resolves bug 256601: audit2allow generates incorrect syntax when comma "," in
   denied list

- update po i18n files

- Add support for pruning database by age and size


* Sat Sep  8 2007 John Dennis <jdennis@redhat.com> - 1.10.4-1
- fix init script

* Sat Sep  8 2007 John Dennis <jdennis@redhat.com> - 1.10.3-1
- modify avc_audit.py to use new audit_data.py implementation

- can listen for audit events on either /var/run/audit_events
   in bindary protocol mode or /var/run/audisp_events in
   text protocol mode

* Thu Sep  6 2007 John Dennis <jdennis@redhat.com> - 1.10.2-1
- remove all copied code from test_setroubleshootd, now we import
   from setroubleshoot
 
- export ClientConnectionHandler from rpc.py as a base class.
   Derive SetroubleshootdClientConnectionHandler and
   AuditClientConnectionHandler from ClientConnectionHandler.

- add audisp_listen as test program

- create setroubleshoot sym link in top devel directory pointing
   to src so import setroubleshoot.foo if PYTHONPATH=topdir

- add get_option, convert_cfg_type to config.py.in so that one
   can pass optional dict to override config file settings

- rewrite log_init() so it's easier for other programs to use it,
   fix the import logic concering log & config

- remove log code from test_setroubleshoot, now just does import
   from setroubleshoot.
 
- test_setroubleshootd can now handle audit records in both text
   and binary formats, can be selected by command line arg. It can now
   either output to clients connecting on a socket or to stdout. Can
   now optionally exit after N socket client connections.

- remove non audit record lines from test data

- remove config_init() and log_init() from package __init__.py
   It was the wrong place to call them, now call them when the
   process initializes before the first setroubleshoot imports

- add parse_config_setting() and set_config() to config module
- setroubleshootd now accepts -c --config command line arg
- test_sectroubleshoot: add err defines & program_error exception
   add is_valid() tests to assure we read a valid audit record
   log the unrecognized line if not valid, clean up socket close()

- Relates Bug #247056, update initscript to LSB standards
   Note: LSB initscripts in Fedora is not yet a resolved issue,
   the changes implemented were to add an LSB block and support
   the new LSB try-restart and force-reload commands. However
   the new /lib/lsb/init-functions are NOT currently used as this
   is the unstable part.

* Thu Aug 23 2007 John Dennis <jdennis@redhat.com> - 1.10.1-1
- add BuildRequires perl-XML-Parser

* Thu Aug 23 2007 John Dennis <jdennis@redhat.com> - 1.10.0-1

- move all plugins and their translations to independent package
- wrap XML generation inside try/except
- correct how access list is obtained in avc_auparse.py
- add try/except around top level of AnalyzeThread.run so exceptions
   in the thread get reported and the analysis thread does not just die.
- also add try/except around LogfileThread.process_logfile
- add new function assure_file_ownership_permissions()
- server now forces it's database file permissions/ownership to be 0600 root:root
- rpm now forces the server's database file permissions/ownership to be 0600 root:root
- Resolves Bug #251545: Review Request: setroubleshoot-plugins - analysis plugins for setroubleshoot
- clean up some other rpmlint warnings in setroubleshoot.spec
- fix missing install of setroubleshoot icon and sym link to it
- Resolves Bug #251551, setroubleshoot shows up in in wrong desktop menu
   also run desktop-file-install in rpm install
- add /etc/dbus-1/system.d/setroubleshootd.conf dbus configuration file
- Resolves Bug #250979, Bug #250932 Missing dependencies
- Restore plugins/Makefile.am which got nuked somehow
- remove dus.dbus_bindings.bus_name_has_owner(), deprecated as of F7
- wrap rpm transactions in try/except

* Tue Jun 12 2007 John Dennis <jdennis@redhat.com> - 1.9.7-1
- Resolves Bug# 241739, this bug is the lead bug for several bug reports,
   all consequences of the same problem, setroubleshootd/sealert when run
   in a non latin language environment because of incompatibilities in
   i18n encoding between components.

* Wed May 30 2007 John Dennis <jdennis@redhat.com> - 1.9.6-1
- add avc_auparse.py, now has option to use audit parsing library instead of
   built-in audit parsing.
- fix bug in log file scanning and detail display update
- Resolves Bug# 238516, python pkg directory not owned

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> - 1.9.5-1
- Update translations
- Fix mislabeled file

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> - 1.9.4-1
- Remove disable_trans boolean
- Check for paths in filesystem before suggesting chcon -R 
- Remove default to listen on local ports

* Mon Mar  5 2007 John Dennis <jdennis@redhat.com> - 1.9.3-1
- install icon in /usr/share/icons, refer to icon by name using standard API
- Fix performance problems in setroubleshoot browser log file scanning
- Significant rewrite of data/view management code in setroubleshoot
   browser. data and view now cleanly separated, can easily switch
   between data views while maintaining selections, view state, with
   proper update of status information in status area
- Resolves Bug# 227806: right click context menu resets selection
- Logfile scans now operate in independent thread, proper asynchronous
   updates of browser during scan, browser used to appear to hang
- Resolves Bug# 224340: Rewrite Menu/Toobar/Popup to use UIManger instead of glade
- Add toobar support
- Implement GUI to edit email recipient list in setroubleshoot browser
- Added user help to setroubleshoot browser
- Related Bug# 224343: Fix setroubleshoot browser to respond to desktop theme changes
- improve traceback error reporting in sealert
- rewrite AboutDialog, replacing glade version
- Resolves bug 229849  Bug# 230115, Relates bug 221850: fix uuid code to resolve
   '_uuid_generate_random' is not defined error
 
* Thu Feb  22 2007 Dan Walsh <dwalsh@redhat.com> - 1.9.2-1
- Suck in AuditMsg since audit libs are dropping support

* Fri Feb  16 2007 Dan Walsh <dwalsh@redhat.com> - 1.9.1-1
- Split into server and gui packages

* Fri Feb  16 2007 Dan Walsh <dwalsh@redhat.com> - 1.8.19-1
- Remove use of ctypes in uuid, which is causing bad avc messages

* Fri Feb  9 2007 Dan Walsh <dwalsh@redhat.com> - 1.8.18-1
- Remove avc from Plugin.py

* Wed Feb  7 2007 Dan Walsh <dwalsh@redhat.com> - 1.8.17-1
- Remove tempfile handling in util.py.  Causes lots of avc's and is not used

* Fri Feb  2 2007 John Dennis <jdennis@redhat.com> - 1.8.16-1
    [John Dennis <jdennis@redhat.com>]
- Fixes Bug# 224343 sealert's "Aditional Info:" text should be in white box
- Fixes Bug# 224336 sealert should have GtkRadioButtons in menu View
- Related: bug 224351
   Rewrite parts of logging support to better support changing output
   categories, output destinations. Now -v -V verbose works in sealert.
- Resolves bug 225161, granted AVC's incorrectly identified as a denial
- add alert count to status bar
- add "Help" command to Help menu, opens web browser on wiki User FAQ
    [Dan Walsh  <dwalsh@redhat.com>]
- Make setroubleshoot.logrotate correctly

* Fri Jan 12 2007 Dan Walsh <dwalsh@redhat.com> - 1.8.15-1
- Update po
- Additional Plugins
- Cleanup Plugins

* Thu Jan 11 2007 John Dennis <jdennis@redhat.com> - 1.8.14-1
- Fixes 221850
   plugin module loading was failing in python 2.5 with the message
   "SystemError: Parent module 'plugins' not loaded". This is due to a
   change in behavior between python 2.4 and 2.5, in python 2.4 the lack
   of a parent module was silently ignored. The fix is to load
   plugins.__init__ first.
 
* Sat Jan  6 2007 John Dennis <jdennis@redhat.com> - 1.8.13-1
- update translations

- change SETroubleshootDatabase so it is optional if it's backed
   by a file, this fixes the problem of us littering temporary files
   when scanning logfiles which does not require persistence.

- disable the view logfile menu item if no logfile has been opened

- fix redundant log messages for case where there is no log file and
   the console flag is set. When there is no log file the logging
   module opens a console stream, thus the console stream produced
   by the console flag was redundant.

- add username and password command line arguments
   rework startup logic so that all command line args are processed
   before we do any real work
 
- rework the email preferences so that each email address can
   have a filter type associated with it.

   add a new filter_type "Ignore After First Alert" which filters
   after the first alert has been delivered

- add UI for setting the email addresses alerts are sent to.
   Add menu item to edit email list, add email list dialog.
   Remove 'recipient' config file entry, now list is stored
   in seperate file. Add rpc to query and set the email list,
   the GUI calls this to get the current list from the server
   and set it in the server, it is the server which reads and 
   writes the file. Add 'enable' flag to each email entry.
   Modify how the server iterates over the email list when it
   receives an alert. When marking an alert as having been sent
   the username is the email address but with 'email:' prepended so
   as not to collide with non-email filtering options for the same user.

* Wed Dec 20 2006 John Dennis <jdennis@redhat.com> - 1.8.12-1
- remove obsolte requires for python element tree 

* Mon Dec 18 2006 John Dennis <jdennis@redhat.com> - 1.8.11-1
- Fixes 216575, more translations
- Replace delete and expunge menu labels with something more intuitive
- add ability for browser to be restarted with identical window
   position and state
- add pkg version and protocol version to logon handshake, test for
   compatibility between clint and server, prompt for restart
- add non-modal restart dialog
- add dialog to display traceback if sealert faults with an uncaught
   exception, try to limit invisible errors
- fix return args on rpc method
- add instance id to server

* Wed Dec 13 2006 Dan Walsh <dwalsh@redhat.com> - 1.8.10-1
- Improve quality of plugins
- Make matching easier
- Fixes 216575

* Wed Dec 13 2006 Dan Walsh <dwalsh@redhat.com> - 1.8.9-1
- Additional Translations
- Fixes 216575

* Sat Dec  9 2006 Dan Walsh <dwalsh@redhat.com> - 1.8.8-1
- Additional Translations
- Change sealert to be able to run without X-Windows
- Fixes 216575

* Fri Dec 8 2006 Dan Walsh <dwalsh@redhat.com> - 1.8.7-1
- Additional Translations
- Change avc_audit.py to allow it to analyze /var/log/messages

* Mon Dec  4 2006 John Dennis <jdennis@redhat.com> - 1.8.6-1
- Fixes 218150,
   "If view is set to "hide delete" you cannot filter new entries"
   Actually, the bug was toggle cell renderer was connected to the
   base model instead of the model attached to the view, the sort
   model, this meant the toggle was occuring on the wrong row if
   the view was sorted differently than the base model.

* Fri Dec  1 2006 John Dennis <jdennis@redhat.com> - 1.8.5-1
- fix bug, "could not convert path to a GtkTreePath" when database 
   is initially empty, caused by last_selected_row == None

* Thu Nov 30 2006 John Dennis <jdennis@redhat.com> - 1.8.3-1
- Fixes 217961, sealert needs pygtk2-libglade
- more i18n translations
- Fixes 217710, date representation did not respect locale,
   at the same time remove old date formatting code, now cruft since
   we can't use it because it was specific to US English.
- fix how selections are handled when rows are expunged.
- add Copy to Edit menu, for copying selection from detail pane,
   unfortunately gtkhtml2 widget does not preserve line breaks between
   table rows.

* Tue Nov 28 2006 John Dennis <jdennis@redhat.com> - 1.8.1-1
- Fixes 216936, bug 215290, add 'Copy Alert' edit menu item
- clean up menu items, add tooltips
- fix printing so it will work with multiple alerts, force font to
   monospace 10pt, display error dialog if printing fails.
- Fixes 216908, platform and raw audit messages were not wrapped
   to fit on page.
- Related: 216575, update i18n po files
- Fixes 216941, set default folder for save operation, also set
   default filename
- Fixes 216327 add menu items "toggle hide deleted", "select none". Add model
   filter to control visibility of alerts
- Fixes 214218, sealert with no command line
   arguments induces startup as dbus service, this had been a
   regression.
- Fixes 216327, rework how deletes are performed in browser. Delete
   now marks each seleted siginfo with a delete flag, expunge
   permanently deletes siginfo's marked for deletion, also add undelete
   command, removed delete confirmation dialog. Modify how text
   attributes in cell renderer are computed to allow for
   strike-throughs of alerts marked for deletion.
- multiple alerts can now be selected, add select all command, 

* Thu Nov 23 2006 Dan Walsh <dwalsh@redhat.com> - 1.7.1-1
- New Icon and translations

* Tue Nov 21 2006 Dan Walsh <dwalsh@redhat.com> - 1.7-1
    [John Dennis <jdennis@redhat.com>]
- Add command line utilities
- logfile scanning finally seems to work connected to browser
- Additional Information section of report now includes line
   number information (if alert was generated from logfile)
- replace database update_callback() with notify interface, a more
   generic solution more easily shared between components
- object implementing rpc method is now explicitly attached via
   connect_rpc_interface() instead of walking the MRO chain with
   magic exclusions. explicitly connecting is more flexible and
   robust (no getting the wrong object by mistake)
- fix handling of return args in local rpc case
- fix signal connections between audit and logfile
- split databae and database_properties for audit and logfile
- fix initial connection state
- fix lookup_local_id

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> - 1.5-1
- Speed up startup of service

* Tue Nov 7 2006 Dan Walsh <dwalsh@redhat.com> - 1.4-1
- Many fixes
- Changed the api

* Tue Oct 24 2006 Dan Walsh <dwalsh@redhat.com> - 1.3-1
- Speed enhancments
    [John Dennis <jdennis@redhat.com>]
- log file parsing now approx 4 times faster
- greatly enhance the statistics reporting capability in attempt
   to diagnose slow log file parsing performance
- make gathering of environmenatal information optional,
   environment information is only relevant at the time the
   alert fires, not in a post processing scenario
- clean up several places where environmental information was
   assumed and/or was always gathered, or gathered in the wrong place.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.2-1
- Fix signature for PORT_NUMBER src command

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> - 1.1-1
- Additional Plugins for port_t and device_t and mislabled files.

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> - 1.0-1
- Release of first version
- Fix icon
    [John Dennis <jdennis@redhat.com>]
- Memory leak fixes
- Substitution fixes
- File names in hex fixes

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> - 0.48-1
- Sealert only notify dropped connection once
- setroubleshoot shutdown cleanly
    [John Dennis <jdennis@redhat.com>]
- Gui cleanups

* Wed Sep 27 2006 Dan Walsh <dwalsh@redhat.com> - 0.47-1
- Change close key binding to ctrl-w

* Tue Sep 26 2006 Dan Walsh <dwalsh@redhat.com> - 0.46-1
- Add new plugins cvs_data, rsync_data, xen_image, swapfile, samba_share
    [John Dennis <jdennis@redhat.com>]
- clear the GUI of old data before loading new data,
   fix the code used to display the filter icon in the filter column

* Tue Sep 26 2006 Dan Walsh <dwalsh@redhat.com> - 0.45-1
    [John Dennis <jdennis@redhat.com>]
- Major rewrite of the client/server RPC code,

* Sat Sep 16 2006 Dan Walsh <dwalsh@redhat.com> - 0.44-1
- Fix Affected RPMS handling

* Fri Sep 15 2006 Dan Walsh <dwalsh@redhat.com> - 0.43-1
- Fix mail handling
- fix bugs related to recording per user per signature filtering
    [John Dennis <jdennis@redhat.com>]
- fix bugs related to recording per user per signature filtering
    [Karl MacMillan <kmacmill@redhat.com>]
- Add signal handling to client and server.
- Fix minor plugin bugs.

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> - 0.42-1
    [Karl MacMillan <kmacmill@redhat.com>]
- Add rpm information for target.
- Add hostname and uname to signature info
- Add display of the full AVC
- Add display of the analysis id
- Change html generation to be separated out and us elemmenttree
    [John Dennis <jdennis@redhat.com>]
- add CommunicationChannel class to encapsulate data transfer
   operations, in particular to provide an object threads can lock
   during data transfer.
- checkpoint the logfile scanning code, somewhat working

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 0.41-1
- Fix printing

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 0.40-1
- Fix notification window problems.  Now dissappears and does not regenerate if
it has already been seen

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 0.39-1
- Add Icon
    [John Dennis <jdennis@redhat.com>]
- dispatcher.py: rework how audit messages injected into the
   system and processed. Much of this work was in support of log file
   scanning which should be coupled to the exact same processing code
   as audit messages arriving from the audit socket. In essence log
   file scanning synthesizes an audit message and we inject it into
   the system the same way socket messages are injected. This was
   also an excellent moment correctly handle out of order audit
   messages, something we were not able to handle previously. This
   may have been contributing to splitting what should have been a
   single alert into two or more separate alerts because we didn't
   recongize the incoming audit events as a single event. Correctly
   assembling out of order messages introduced a fair amount of extra
   complexity as we now maintain a cache of recent audit events, this
   is fully documented in dispatcher.py
- Turn notifications back on by default.
    [Karl MacMillan <kmacmill@redhat.com>]
- Separated out HTML rendering and made it easier to translate.

* Wed Aug 30 2006 Dan Walsh <dwalsh@redhat.com> - 0.38-1
    [Dan  Walsh]
- Hook up the rest of the menu bars on browser window
- Add public_content.py plugin
    [John Dennis <jdennis@redhat.com>]
- add delete_signatures() method to AlertClient class
- start using the AppBar in the browser.
- "open logfile" now connected all the way from browser menu
   to server rpc, still needs implementation, but "plumbing" is working.
- fixes for the date/time dialog
- remove install of setroubleshoot.glade, we now only use
   setroubleshoot_browser.glade
- some fixed to DateTimeDialog

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> - 0.37-1
- Add back in the status icon

* Thu Aug 24 2006 John Dennis <jdennis@redhat.com> - 0.36-1
- change dbclear trigger to 0.35

* Thu Aug 24 2006 John Dennis <jdennis@redhat.com> - 0.35-1
- add sorting on category column and seen column in browser,
   fix reference to my_draw() in print function.

- make browser window hidden by default so it does not flash
   when it's first realized, connect to the "realize" signal to
   initially position the vpane, add signal handlers to track
   when the browser is visible, the presentation of the status
   icon now checks if the browser is visible, the status icon is
   not presented if the browser is already displayed.

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> - 0.34-1
- Standardize on the browser. remove alert window
    [John Dennis <jdennis@redhat.com>]
- remove all vestiges of popup alert, now browser is the only
   UI game in town
- restore the automatic updating of the browser window which had
   been a regression, the AlertClient class now emits signals which
   the GUI classes can connect to receive signals from the fault server,
   also fix the "mark seen" regression
- browser.py: restore mark_seen timeout

* Tue Aug 22 2006 Dan Walsh <dwalsh@redhat.com> - 0.33-1
- Spell check plugins
- fix dbus instantiation

* Tue Aug 22 2006 Dan Walsh <dwalsh@redhat.com> - 0.32-1
- Add avc_syslog to syslog translated avc message
- Fix submitbug button
    [John Dennis <jdennis@redhat.com>]
- fix signature inflation, all data attached to a signature is now
   encapsulated in a SEFaultSignatureInfo (siginfo) class. The GUI no
   longer reaches into a signature looking for information, it looks
   in the siginfo. The Plugin class now defines the method
   get_signature() which report() calls to obtain the signature. The
   default signature provided by the Plugin class includes the
   analysisID, an AVC with just the src & target contexts, and the
   object_path. All data accesses and parameters which had been "sig
   and solution" are now done via the unified siginfo class. There is
   still a bit more work to be done on this but this represents a
   reasonble point to checkpoint the code in CVS.

* Tue Aug 22 2006 Dan Walsh <dwalsh@redhat.com> - 0.31-1
- Fix desktop

* Tue Aug 22 2006 John Dennis <jdennis@redhat.com> - 0.30-1
- fix bug 203479, missing requires of audit-libs-python
- add support to sealert to listen on a dbus session signal to display
   the gui. This is needed for when the status icon is not visible and
   the user wants to see the UI. There is now a seperate program
   setroubleshoot_launch_gui which emits the signal.

* Tue Aug 22 2006 Dan Walsh <dwalsh@redhat.com> - 0.29-1
- Add Requires: audit-libs-python
- Add translations

* Mon Aug 21 2006 Dan Walsh <dwalsh@redhat.com> - 0.28-1
- Fix allow_execmem.py file
- Add translations

* Mon Aug 21 2006 John Dennis <jdennis@redhat.com> - 0.27-1
- load_plugins() now catches exceptions when a plugin won't load,
   reports the traceback in the log file, and continues with the next
   plugin. Previously a bad plugin caused the entire plugin loading
   to abort and no plugins were loaded.
- Add "daemon_name" to automake variables, change pid file to match
- turn off "noreplace" on config file till things settle down a bit
- browser.py now validates data, also test for missing column data in the
   cell_data function to avoid exceptions.
- add stub for analyzie_logfile() rpc call
- turn off balloon notifications by default in config file,
   libnotify is just plain busted at this point :-(
- only the setroubleshootd daemon creates it's log file
   under /var/log now, the user app's do it in /tmp, change file
   permissions on /var/log/setroubleshoot back to 0644.
- sealert now looks up the username rather than hardcoding it to "foo"
- CamelCase to lowercase_underscore clean up

* Mon Aug 21 2006 Dan Walsh <dwalsh@redhat.com> - 0.26-1
- Zero out datbase.xml for updated browser

* Mon Aug 21 2006 Dan Walsh <dwalsh@redhat.com> - 0.25-1
- Fix 64 bit issue that caused runaway problem

* Sun Aug 20 2006 Dan Walsh <dwalsh@redhat.com> - 0.24-1
- add missing runcmd

* Thu Aug 17 2006 John Dennis <jdennis@redhat.com> - 0.23-1

- fix for bug 202206, require correct version of audit,
   fixes for audit connection.

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> - 0.20-1
- add html support
- remove setroubleshoot_dispatcher

* Tue Aug 8 2006 Dan Walsh <dwalsh@redhat.com> - 0.19-1

2006-08-08  Dan Walsh <dwalsh@redhat.com>
- Fix up handling of mls ranges in context
- Cleanup some pychecker errors

2006-08-07  John Dennis <jdennis@redhat.com>
- add first seen, last seen, and report count to alert detail view
- make the seen icon work, if the alert has been displayed more
   than N seconds, mark the alert as having been seen by the user
   and update the icon is the list view
- change the schema for the xml data; the database now has a version,
   there is a local id attached to each signature, the filter list in
   the siginfo was replaced by a list of per user data, the per user
   data now contains the filter, seen_flag. Modify all the code which
   was operating on the filter information to use the new model.
- fix the xml serialization so that booleans can be used as a basic
   type and also so that non-string types can be used in element
   attributes (e.g. int, bool) and the serialization code will
   automatically convert between python types and strings.

* Mon Aug 7 2006 Dan Walsh <dwalsh@redhat.com> - 0.18-1
- Add dispatcher.py

* Sat Aug 5 2006 Dan Walsh <dwalsh@redhat.com> - 0.17-1
    [John Dennis <jdennis@redhat.com>]
- clean up and rework the timestamp code in util.py so that
   time zones are handled properly, there were a number of bugs.
   Hopefully it's correct now because timezone handling is a pain.
- change the time format in the browser so all times are displayed
   identically, the friendly time relative format was hard to compare.
- modify the plugin 'make install' to delete all existing plugin's
   prior to installing the new ones
- add popup menu to status icon to choose between browser and
   alert GUI (not fully connected yet). Several bug fixes related
   to changing the filter_type from a string to an int.
- add filter selection to bottom pane, change filter_type from
   string to integer constant. Enhance how columns are handled.
   Get init_combo_box to work. Remove unused RPM and Bugzilla
   fields from bottom pane. Modify the default size of the browser
   window. Fix missing import in util.py.
- add ability in broswer to sort on columns, initially the report
   count column and the last seen date column. The date column now
   stores a TimeStamp object instead of a string. Add new method
   to TimeStamp to return a friendly string relative to the current
   time. The date column in the browser now has a cell data function
   which invokes the friendly format method of the TimeStamp object.
- add ability fo serialize to/from xml for classes which can
   inititialized from strings and serialized as strings (e.g. numbers,
   TimeStamps, etc.)
- add count of how many times a signature is reported, the date
   when first and last reported, add columns for report count and
   last date count to browser.
- checkpoint browser code, list pane and detail pane now working.
- add initial support for browser applet, move some functions which
   kept getting reused to util.py
- add reporting of environment to email alert (email alerts still
   need work)
    [Dan  Walsh <dwalsh@redhat.com>]
- Fix disable_trans.py set_boolean call
- Complete all boolean plugins except disable
- Change interface to use audit unix domain socket

* Fri Jul 28 2006 Dan Walsh <dwalsh@redhat.com> - 0.16-1
    [John Dennis <jdennis@redhat.com>]
- modify SetFilter in server to return errors instead of
   throwing an exception. Default the filter list on each alert display.
- minor tweaks to alert queue handling
- fix analyze() parameter list in ftp_is_daemon.py plugin
- sealert now responds to pending alerts more correctly, it shows
   how many pending alerts are in the queue, if you filter the pending
   alert status is updated, the next alert button will advance you
   to the next alert in the queue
- simplify major pieces of sealert by coalescing common code
   into subroutines.
    [Dan  Walsh <dwalsh@redhat.com>]
- Complete all boolean plugins except disable
- Make Close button work.
- Make setroubleshoot_dispatcher exit if it gets an avc about itself

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> - 0.15-1
    [Karl MacMillan <kmacmill@redhat.com>]
- Add generic templating mechanism to Plugin
- Ported all plugins to use templating mechanism

* Sat Jul 22 2006 Dan Walsh <dwalsh@redhat.com> - 0.13-1
- Fixes to plugins
- Fixes to dispatcher

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> - 0.12-1
- Fix problem in dispatcher

* Fri Jul 21 2006 John Dennis <jdennis@redhat.com> - 0.11-1
- add email alerts
- stop the status icon from blinking, add notification balloon.

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> - 0.10-1
- Fix startup order for setrobleshoot
- Fix Plugins

* Thu Jul 20 2006 Dan Walsh <dwalsh@redhat.com> - 0.9-1
- Additional Plugins plus a lot of cleanup

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> - 0.8-1
- Added a bunch more plugins
    [Karl MacMillan <kmacmill@redhat.com>]
- Add allow_cvs_read_shadow.py, allow_ftp_use_cifs, allow_ftp_use_nfs, and allow_gssd_read_tmp.
- Change AVC to have additional helpers for matching messages.
- Change Plugin to work better with more than one solution.

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> - 0.7-1
- Fix setroubleshoot_dispatcher to catch all information from
   avc. Much cleaner interface and no longer uses audit2allow cruft.
- Remove toolbar from popup window since it did nothing, and I
   think it looks better without it.
- fix allow_execmod plugin to report better data.

* Mon Jun 26 2006 John Dennis <jdennis@redhat.com> - 0.3-1
- add missing /var/log directory files section in spec file,
   and add logrotate script

* Mon Jun 26 2006 John Dennis <jdennis@redhat.com> - 0.2-1
- clean up spec file, reduce rpmlint complaints

* Fri May 19 2006 John Dennis <jdennis@redhat.com> - 0.1-1
- Initial build.

