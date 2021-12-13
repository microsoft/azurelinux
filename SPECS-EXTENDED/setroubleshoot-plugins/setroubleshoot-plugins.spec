Vendor:         Microsoft Corporation
Distribution:   Mariner
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0

Summary: Analysis plugins for use with setroubleshoot
Name: setroubleshoot-plugins
Version: 3.3.12
Release: 2%{?dist}
License: GPLv2+
URL: https://github.com/fedora-selinux/setroubleshoot
Source0: https://releases.pagure.org/setroubleshoot/%{name}-%{version}.tar.gz
# git format-patch -N setroubleshoot-plugins-<version> -- plugins
# i=1; for j in 00*patch; do printf "Patch%04d: %s\n" $i $j; i=$((i+1));done
BuildArch: noarch

# gcc is needed only for ./configure
# Remove it when the build process is fixed
BuildRequires: gcc
BuildRequires: perl-XML-Parser
BuildRequires: intltool gettext python3-devel
# Introduction of get_package_nvr functions
Requires: setroubleshoot-server >= 3.3.23

%description
This package provides a set of analysis plugins for use with
setroubleshoot. Each plugin has the capacity to analyze SELinux AVC
data and system data to provide user friendly reports describing how
to interpret SELinux AVC denials.

%prep
%autosetup -p 2

%build
%configure PYTHON=%{__python3}
make PYTHON=%{__python3}

%install 
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PYTHON=%{__python3} pkgdocdir=%{_pkgdocdir} install
%find_lang %{name}
# Manually invoke the python byte compile macro for each path that needs byte
# compilation.
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/setroubleshoot/plugins

%files -f %{name}.lang 
%doc %{_pkgdocdir}
%{_datadir}/setroubleshoot/plugins

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.12-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Apr 21 2020 Vit Mojzis <vmojzis@redhat.com> - 3.3.12-1
- Use get_package_nvr* functions instead of get_rpm_nvr*
- Update deprecated type references
- Update translations

* Thu Jan 30 2020 Vit Mojzis <vmojzis@redhat.com> - 3.3.11-1
- Add plugin which analyzes execmem denials
- Add missing "If " strings
- Update qemu_blk_image and qemu_file_image
- Update "xen_image" plugin
- Update "file" plugin
- Update "missing" scripts to automake-1.15

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec  8 2018 Petr Lautrbach <plautrba@redhat.com> - 3.3.10-1
- Handle no "allowed_target_types" properly
- bind_ports: Do not use when there are no allowed_target_types
- Fix summary and "if" text for AVCs with unknown target path
- plugins: Update translations

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.9-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 23 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.9-3
- Update translations

* Mon Nov 20 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.9-2
- Update translations

* Sat Nov 18 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.9-1
- Fix catchall plugin message for process2

* Fri Sep 15 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.8-1
- Do not split If sentences to framework and plugins - requires
  setroubleshoot 3.3.13 at least - (rhbz#1210243, rhbz#1322734, rhbz#1115510)
- Update translations

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Petr Lautrbach <plautrba@redhat.com> - 3.3.7-1
- cvs_data: Add "fix_cmd" and enable "fix" button
- chrome: Update "fix_cmd" and enable "fix" button
- automount_exec_config: Update messages and enable "fix" button
- allow_ftpd_use_*: Update messages and enable "fix" button
- allow_execmod: Update messages and enable "fix" button
- catchall_boolean: fix import of boolean_desc (#1444549)
- restorecon: fix "then" text
- Spelling fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 01 2016 Petr Lautrbach <plautrba@redhat.com> 3.3.6-1
- Fix catchall plugin message for capability2 (#1360392)
- Stop executing restorecon plugin on specified path prefixes (#1270778)
- Update translations

* Wed Jun 22 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.5.1-1
- Catch all subprocess exceptions
- Use subprocess.check_output() with a sequence of program arguments
- Fix location of selinuxfs mount point

* Fri May 06 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.4-1
- Suggest my-<command>.pp modules instead of mypol.pp (#1329037)
- Suggest priority 300 for modules created by audit2allow

* Mon Apr 04 2016 Petr Lautrbach <plautrba@redhat.com> - 3.3.3-1
- Fix sshd_root.py setroubleshoot plugin to cover only /root/.ssh path as intended.
- Suggest to use ausearch instead of grep
- Update translations

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 06 2015 Petr Lautrbach <plautrba@redhat.com> 3.3.2-1
- Update restorecon plugin to to identify a mislabeling of executable (BZ#1257682)

* Tue Aug 18 2015 Petr Lautrbach <plautrba@redhat.com> 3.3.1-0.1
- port setroubleshoot-plugins to Python 3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 16 2015 Miroslav Grepl <mgrepl@redhat.com> - 3.0.61-1
- Fix catchall_boolean plugin to show correct man page for source type.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Dan Walsh <dwalsh@redhat.com> - 3.0.60-1
- Change file.py plugin to handle alias between file_t and unlabeled_t

* Wed Dec 4 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.59-1
- Update Translations

* Thu Aug 22 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.58-1
- Update Translations

* Fri Aug 16 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.57-1
- Add restorecon_source plugin, to check the source program is labeled correclty.
- Fix restorecon.py to handle customized_files properly.
- Update Translations

* Fri Jul 26 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.0.55-2
- Install docs to %%{_pkgdocdir} where available.

* Sun Jul 21 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.55-1
- Fix debug message in sandbox-connect plugin
- Update Translations

* Thu Jun 27 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.54-1
- Add sandbox-connect plugin
- Update Translations

* Mon Jun 24 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.53-1
- Update Translations
- Add sandbox_connect plugin to point out the use of alternate types with the sandbox -X command.

* Tue May 7 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.52-1
- Update Translations
- Only translate catchall_boolean descritpions if the are not unicode to start with.

* Fri Apr 19 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.51-1
- Update Translations

* Wed Mar 6 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.50-1
- Add chrome.py and update mozplugger.py to indicate how to disable plugin protection

* Tue Mar 5 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.49-1
- Fix restorecon plugin to check customizable types

* Fri Feb 15 2013 Dan Walsh <dwalsh@redhat.com> - 3.0.48-1
- Fix connect_ports and bind_ports to specify semanage command if only 1 port is available rather then to suggest user choices
- Update translations

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 7 2013  <dwalsh@redhat.com> - 3.0.47-1
- Update translations
- Fix sys_resource.py to mention all types of resources
- Fix unicode calls so catchall_booleans.py does not crash sealert

* Mon Nov 5 2012  <mgrepl@redhat.com> - 3.0.46-1
- Fix catchall_boolean.py to refer to correct SELinux man page

* Fri Sep 28 2012  <dwalsh@redhat.com> - 3.0.45-1
- Update translations
- Update mozplugger plugins to handle spice-xpi

* Thu Sep 20 2012  <dwalsh@redhat.com> - 3.0.44-1
- Update translations
- Add two new mozplugger plugins

* Mon Aug 13 2012  <dwalsh@redhat.com> - 3.0.43-1
- Update translations
- Use system setroubleshoot check_for_man

* Thu Jun 14 2012  <dwalsh@redhat.com> - 3.0.42-1
- Fix leaks plugin to only fire or write and append

* Fri Jun 8 2012  <dwalsh@redhat.com> - 3.0.41-1
- Update-translations

* Sat May 12 2012  <dwalsh@redhat.com> - 3.0.40-1
- Update-translations

* Wed May 9 2012  <dwalsh@redhat.com> - 3.0.39-1
- Update-translations

* Thu Apr 26 2012  <dwalsh@redhat.com> - 3.0.38-1
- Update-translations
- Have catchall_booleans report the correct man page if it exists

* Wed Mar 28 2012  <dwalsh@redhat.com> - 3.0.36-1
- Update-translations
- Fix leaks and catchall_labels to better detect leaks

* Mon Mar 19 2012  <dwalsh@redhat.com> - 3.0.35-1
- Update-translations

* Sat Mar 17 2012  <dwalsh@redhat.com> - 3.0.34-1
- Add associate.py plugin
- Update-translations

* Thu Mar 8 2012  <dwalsh@redhat.com> - 3.0.33-1
- Update-translations

* Thu Mar 1 2012  <dwalsh@redhat.com> - 3.0.30-1
- Update-translations

* Wed Feb 22 2012  <dwalsh@redhat.com> - 3.0.28-1
- Update-translations

* Tue Feb 14 2012  <dwalsh@redhat.com> - 3.0.27-1
- Update-translations

* Tue Feb 7 2012  <dwalsh@redhat.com> - 3.0.24-1
- Update-translations, 

* Wed Feb 1 2012  <dwalsh@redhat.com> - 3.0.23-1
- Update-translations, 
- Fix a couple of typos

* Fri Jan 27 2012  <dwalsh@redhat.com> - 3.0.22-1
- Update-translations, 
- Fix a couple of typos

* Mon Jan 23 2012  <dwalsh@redhat.com> - 3.0.21-1
- Change catchall_booleans to include reference to man page if available
- Update trans

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011  <dwalsh@redhat.com> - 3.0.18-1
- connect_port and bind_ports should handle unreserved_port_t
	
* Wed Nov 9 2011  <dwalsh@redhat.com> - 3.0.17-1
- restorecon plugin should not fire on nfs_t or cifs_t directories

* Tue Apr 19 2011  <dwalsh@redhat.com> - 3.0.16-1
- Update translations
- Change allow_execmod plugin to only fire if target_path is lib_t
- Ignore errors from disabled IPv6
Resolves: #674770

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 4 2011  <dwalsh@redhat.com> - 3.0.14-1
- Fix spelling mistakes, patch from Yuri Chornoivan
- Update translations

* Wed Feb 2 2011  <dwalsh@redhat.com> - 3.0.13-1
- Update Translations
- Fix allow_execstack plugin to be backwards compatable

* Mon Jan 24 2011  <dwalsh@redhat.com> - 3.0.12-1
- Update translations

* Tue Jan 18 2011  <dwalsh@redhat.com> - 3.0.11-1
- Update translations
- Add findexecstack to allow_execstack to find offending libraries

* Wed Jan 12 2011  <dwalsh@redhat.com> - 3.0.10-1
- Add dac_override plugin and update po

* Mon Jan 3 2011  <dwalsh@redhat.com> - 3.0.9-1
- Change catchall plugin to use just the SOURCE not the Full path for the grep example

* Mon Dec 13 2010  <dwalsh@redhat.com> - 3.0.8-1
- Update Translations 

* Thu Dec 2 2010  <dwalsh@redhat.com> - 3.0.7-1
- Update translations
- Fix Restorecon plugin

* Tue Nov 30 2010  <dwalsh@redhat.com> - 3.0.6-1
- Update translations
- Fix openvpn plugin

* Mon Nov 29 2010  <dwalsh@redhat.com> - 3.0.5-1
- Add plugin openvpn that looks for mislabeled cert files in homedir
- Update translations

* Tue Nov 23 2010  <dwalsh@redhat.com> - 3.0.4-1
- Update translations
- Fix boolean descriptions

* Mon Nov 22 2010  <dwalsh@redhat.com> - 3.0.3-1
- Update translations
- Fix catchall plugin to give better messages on capabilities and process avcs

* Mon Nov 15 2010  <dwalsh@redhat.com> - 3.0.2-1
- Fix crash in restorecon plugin

* Mon Nov 1 2010  <dwalsh@redhat.com> - 3.0.1-1
- Fix file_t to bring back multiple solutions

* Wed Oct 27 2010  <dwalsh@redhat.com> - 3.0.0-1
- Redesign of setroubleshoot

* Mon Jul 26 2010  <dwalsh@redhat.com> - 2.1.55-1
- Update translations

* Tue Jun 29 2010  <dwalsh@redhat.com> - 2.1.54-1
- Update translations
Resolves: #589181

* Fri May 21 2010  <dwalsh@redhat.com> - 2.1.52-1
- Remove allow_mount_anyfile boolean plugin

* Mon May 10 2010  <dwalsh@redhat.com> - 2.1.51-1
- Update translations
Resolves: #575686

* Mon Apr 26 2010  <dwalsh@redhat.com> - 2.1.50-1
- Change use_nfs_home_dirs priority to happen after catchall_boolean
- Update translations

* Tue Apr 6 2010  <dwalsh@redhat.com> - 2.1.49-1
- Update translations

* Wed Mar 24 2010  <dwalsh@redhat.com> - 2.1.47-1
- Fix disable_ipv6 and update po

* Tue Mar 23 2010  <dwalsh@redhat.com> - 2.1.46-1
- add restorecon_source_context.py
- add sys_resource.py

* Mon Mar 15 2010  <dwalsh@redhat.com> - 2.1.45-1
- Add disable_ipv6 plugin
- Update translations

* Mon Mar 8 2010  <dwalsh@redhat.com> - 2.1.43-1
- Change priority on httpd_bad_labels

* Fri Mar 5 2010  <dwalsh@redhat.com> - 2.1.42-1
- Update  translations
- Add sshd_root plugin

* Mon Feb 22 2010  <dwalsh@redhat.com> - 2.1.41-1
- Update translations

* Thu Feb 4 2010  <dwalsh@redhat.com> - 2.1.40-1
- Update translations

* Fri Jan 29 2010  <dwalsh@redhat.com> - 2.1.39-1
- Add Fuzzy translations

* Wed Jan 27 2010  <dwalsh@redhat.com> - 2.1.38-1
- Remove audit2why from catchall_booleans

* Mon Jan 18 2010  <dwalsh@redhat.com> - 2.1.37-1
- Fix FAQ pointer 
- Fix handling of translations

* Mon Nov 30 2009  <dwalsh@redhat.com> - 2.1.35-1
- Remove plugin httpd_unified and httpd_tmp_bad_labels.
- Change priority on restorecon plugin

* Fri Nov 20 2009  <dwalsh@redhat.com> - 2.1.33-1
- Remove report bugzilla button on lots of sealerts where there is a boolean to set.

* Tue Nov 17 2009  <dwalsh@redhat.com> - 2.1.32-1
- Remove httpd_connect_all plugin

* Mon Nov 9 2009  <dwalsh@redhat.com> - 2.1.30-1
- Update-po
- Add privoxy_connect_any plugin

* Mon Oct 26 2009  <dwalsh@redhat.com> - 2.1.29-1
- Update-po
- Add httpd_write_content plugin

* Thu Oct 15 2009  <dwalsh@redhat.com> - 2.1.28-1
- Update-po

* Tue Oct 13 2009  <dwalsh@redhat.com> - 2.1.27-1
- Add vbetool plugin

* Thu Oct 8 2009  <dwalsh@redhat.com> - 2.1.26-1
- Add wine plugin

* Thu Oct 8 2009  <dwalsh@redhat.com> - 2.1.25-1
- Fix http_can_senmail to look for "sendmail" in command

* Thu Oct 1 2009  <dwalsh@redhat.com> - 2.1.24-2
- Add support for Green Plugins

* Mon Sep 28 2009  <dwalsh@redhat.com> - 2.1.23-1
- Fix translations

* Tue Sep 22 2009  <dwalsh@redhat.com> - 2.1.22-1
- Remove allow_daemon_user_term plugin

* Thu Sep 17 2009  <dwalsh@redhat.com> - 2.1.21-1
- Remove allow_execmem plugin
- Add Firefox Plugin

* Fri Sep 11 2009  <dwalsh@redhat.com> - 2.1.20-1
- Fix priority on allow_execmod
- Update po

* Thu Sep 10 2009  <dwalsh@redhat.com> - 2.1.19-1
- Change summary to use full path for source

* Thu Sep 10 2009  <dwalsh@redhat.com> - 2.1.18-1
- Update po
- Fix "compromized plugins" to report more data in summary

* Tue Sep 1 2009  <dwalsh@redhat.com> - 2.1.17-1
- Plugin cleanup

* Sat Aug 22 2009  <dwalsh@redhat.com> - 2.1.16-1
- Fix subject to not include types

* Wed Aug 19 2009  <dwalsh@redhat.com> - 2.1.15-1
  - Fix mislabeled_file.py

* Tue Aug 18 2009  <dwalsh@redhat.com> - 2.1.14-1
  - Change priority on mmap_zero to happen after catchall_booleans

* Tue Aug 11 2009  <dwalsh@redhat.com> - 2.1.13-1
  - Change priority on restorecon and leaks

* Thu Jul 30 2009  <dwalsh@redhat.com> - 2.1.12-1
- Add leaks.py and tftpd_write_content.py plugin
- Check execmod protection

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009  <dwalsh@redhat.com> - 2.1.11-1
- Remove allow_default_t boolean
- Fix global_ssp.py to report boolean name

* Thu Jul 9 2009  <dwalsh@redhat.com> - 2.1.9-1
  - Add Scott Radvan. doc cleanup

* Tue Jul 7 2009  <dwalsh@redhat.com> - 2.1.8-1
  - Add avc.source=sendmail to httpd_can_sendmail

* Mon Jul 6 2009  <dwalsh@redhat.com> - 2.1.7-1
  - Remove stunnel_is_daemon plugin
  - Add httpd_can_sendmail

* Mon Jun 29 2009  <dwalsh@redhat.com> - 2.1.5-1
	- Add open calls
	- Fix restorecon plugin
	- Fix qemu calls to include checking for write

* Wed Jun 24 2009  <dwalsh@redhat.com> - 2.1.3-1
- Add sesearch capability to plugins

* Sat Jun 20 2009  <dwalsh@redhat.com> - 2.1.2-1
- Fix Makefile

* Fri Jun 19 2009  <dwalsh@redhat.com> - 2.1.1-1
- Add first plugins which will launch Red Star
- Add Thomas Liu change to allow restorecon to execute fixit button  
  *   2009-06-19 Dan Walsh <dwalsh@redhat.com>
	- Add setenforce.py from Thomas Liu
	- Add sys_module.py, mmap_zero.py, kernel_modules.py, selinuxpolicy.py
	- Allow restorecon to execute fixit command
      	  
* Fri Jun 5 2009  <dwalsh@redhat.com> - 2.0.18-1
	- Execute catchall_boolean.py before allow_daemons_use_tty
	- Fix chcon lines to match current policy

* Mon Apr 13 2009  <dwalsh@redhat.com> - 2.0.16-1
- Change priority on restorecon plugin to happen before public_content

* Fri Apr 3 2009  <dwalsh@redhat.com> - 2.0.15-1
- Update po files

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009  <dwalsh@redhat.com> - 2.0.14-1
- Fix allow_smbd_anon_write typo
- Remove catchall_file plugin

* Wed Dec 3 2008  <dwalsh@redhat.com> - 2.0.12-1
- Fix restorecon plugin

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.11-2
- Rebuild for Python 2.6

* Wed Nov 5 2008  <dwalsh@redhat.com> - 2.0.11-1
- Fix catchall_booleans
- Fix priority on samba plugins

* Thu Oct 23 2008  <dwalsh@redhat.com> - 2.0.10-1
- Add qemu plugins for real

* Wed Oct 15 2008  <dwalsh@redhat.com> - 2.0.9-1
- Fix catchall_plugin

* Wed Sep 10 2008  <dwalsh@redhat.com> - 2.0.8-1
- Add qemu plugins

* Tue Sep 9 2008  <dwalsh@redhat.com> - 2.0.7-1
- Add catchall_booleans plugin, fix spelling

* Fri Apr  4 2008 John Dennis <jdennis@redhat.com> - 2.0.4-5
	- bump rev for build

* Mon Mar  3 2008 John Dennis <jdennis@redhat.com> - 2.0.4-4
	- Resolve bug #435644: change requires setroubleshoot to requires setroubleshoot-server

* Fri Feb 22 2008  <jdennis@redhat.com> - 2.0.4-3
	- bump rev for build

* Mon Feb 18 2008 John Dennis <jdennis@redhat.com> - 2.0.4-2
	- Fix policycoreutils dependency, should only be F-9

* Thu Jan 31 2008  <jdennis@redhat.com> - 2.0.4-1
	- Resolve bug #416351: setroubleshoot does not escape regex chars in suggested cmds
	- add new template substitution $SOURCE, a friendly name, $SOURCE_PATH still exists
	  and is the full path name of $SOURCE

* Tue Jan 15 2008  <dwalsh@redhat.com> - 2.0.2-1
	- Add catchall_boolean.py plugin

* Fri Jan 11 2008  <jdennis@redhat.com> - 2.0.1-1
	- Resolve bug #332281: remove obsolete translation
	- Resolve bug #426586: Renaming translation po file from sr@Latn to sr@latin

* Fri Dec 28 2007  <jdennis@redhat.com> - 2.0.0-1
	- prepare for v2 test release

* Tue Nov 13 2007 Dan Walsh <dwalsh@redhat.com> - 1.10.4-1
	- Add allow_postfix_local_write_mail_spool plugin
	- Fix execute typo

* Wed Oct 10 2007 John Dennis <jdennis@redhat.com> - 1.10.3-1
	- rewrite all plugins to use new v2 audit data

* Mon Sep 24 2007 John Dennis <jdennis@redhat.com> - 1.10.3-1
	- Resolves bug #231762: Original PO strings bugs

* Thu Sep  6 2007 Dan Walsh <dwalsh@redhat.com> - 1.10.2-1
	- Change priority on use_nfs_home_dir to 55

* Thu Aug 23 2007 John Dennis <jdennis@redhat.com> - 1.10.1-1
	- add BuildRequires perl-XML-Parser

* Fri Jul 20 2007 John Dennis <jdennis@redhat.com> - 1.10.0-1
        - move all plugins and their translations from setroubleshoot-server
          package to this new independent package to allow easier updating
          of just the plugins

