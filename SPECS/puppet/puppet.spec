%global nm_dispatcher_dir %{_libdir}/NetworkManager
%global puppet_libdir %{ruby_vendorlibdir}
%global puppet_vendor_mod_dir %{_datadir}/%{name}/vendor_modules

Summary:        Network tool for managing many disparate systems
Name:           puppet
Version:        7.12.1
Release:        5%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://puppet.com
Source0:        https://downloads.puppetlabs.com/puppet/%{name}-%{version}.tar.gz
# Get these by checking out the right tag from https://github.com/puppetlabs/puppet-agent and:
# sed 's|.\+puppetlabs/\([a-z_-]\+\).git.\+tags/\([0-9\.]\+\)"}|https://forge.puppet.com/v3/files/\1-\2.tar.gz|' configs/components/module-puppetlabs-*.json
Source3:        https://forge.puppet.com/v3/files/puppetlabs-augeas_core-1.1.2.tar.gz
Source4:        https://forge.puppet.com/v3/files/puppetlabs-cron_core-1.0.5.tar.gz
Source5:        https://forge.puppet.com/v3/files/puppetlabs-host_core-1.0.3.tar.gz
Source6:        https://forge.puppet.com/v3/files/puppetlabs-mount_core-1.0.4.tar.gz
Source7:        https://forge.puppet.com/v3/files/puppetlabs-scheduled_task-1.0.0.tar.gz
Source8:        https://forge.puppet.com/v3/files/puppetlabs-selinux_core-1.1.0.tar.gz
Source9:        https://forge.puppet.com/v3/files/puppetlabs-sshkeys_core-2.2.0.tar.gz
Source10:       https://forge.puppet.com/v3/files/puppetlabs-yumrepo_core-1.0.7.tar.gz
Source11:       https://forge.puppet.com/v3/files/puppetlabs-zfs_core-1.2.0.tar.gz
Source12:       https://forge.puppet.com/v3/files/puppetlabs-zone_core-1.0.3.tar.gz
Source13:       puppet-nm-dispatcher.systemd
Source14:       start-puppet-wrapper
Source15:       logrotate

BuildArch:      noarch

BuildRequires:  facter
BuildRequires:  gnupg2
BuildRequires:  hiera
# ruby-devel does not require the base package, but requires -libs instead
BuildRequires:  ruby
BuildRequires:  ruby-devel
BuildRequires:  rubygem-json
BuildRequires:  systemd
BuildRequires:  which

Requires:       augeas >= 1.10.1
Requires:       augeas-libs >= 1.10.1
Requires:       cpp-hocon >= 0.2.1
Requires:       facter >= 3.9.6
Requires:       hiera >= 3.3.1
Requires:       libselinux-utils
Requires:       ruby
Requires:       ruby-augeas >= 0.5.0
Requires:       rubygem(concurrent-ruby) >= 1.0.5
Requires:       rubygem(deep_merge) >= 1.0
Requires:       rubygem(facter) >= 3.9.6
Requires:       rubygem(multi_json) >= 1.10
Requires:       rubygem(puppet-resource_api) >= 1.5
Requires:       rubygem(semantic_puppet) >= 1.0.2

%description
Puppet lets you centrally manage every important aspect of your system using a
cross-platform specification language that manages all the separate elements
normally aggregated in different files, like users, cron jobs, and hosts,
along with obviously discrete elements like packages, services, and files.

%prep
%autosetup
cp -a %{sources} .
for f in puppetlabs-*.tar*; do
  tar xvf $f
done
# Puppetlabs messed up with default paths
find -type f -exec \
  sed -i \
    -e 's|/etc/puppetlabs/puppet|%{_sysconfdir}/%{name}|' \
    -e 's|/etc/puppetlabs/code|%{_sysconfdir}/%{name}/code|' \
    -e 's|/opt/puppetlabs/puppet/bin|%{_bindir}|' \
    -e 's|/opt/puppetlabs/puppet/cache|%{_sharedstatedir}/%{name}|' \
    -e 's|/opt/puppetlabs/puppet/public|%{_sharedstatedir}/%{name}/public|' \
    -e 's|/opt/puppetlabs/puppet/share/locale|%{_datadir}/%{name}/locale|' \
    -e 's|/opt/puppetlabs/puppet/modules|%{_datadir}/%{name}/modules|' \
    -e 's|/opt/puppetlabs/puppet/vendor_modules|%{_datadir}/%{name}/vendor_modules|' \
    -e 's|/var/log/puppetlabs/puppet|%{_localstatedir}/log/%{name}|' \
  '{}' +

%install
ruby install.rb --destdir=%{buildroot} \
 --bindir=%{_bindir} \
 --configdir=%{_sysconfdir}/%{name} \
 --codedir=%{_sysconfdir}/%{name}/code \
 --logdir=%{_localstatedir}/log/%{name} \
 --rundir=%{_rundir}/%{name} \
 --localedir=%{_datadir}/%{name}/locale \
 --vardir=%{_sharedstatedir}/%{name} \
 --publicdir=%{_sharedstatedir}/%{name}/public \
 --sitelibdir=%{puppet_libdir}

mkdir -p %{buildroot}%{_datadir}/%{name}/vendor_modules
for d in $(find -mindepth 1 -maxdepth 1 -type d -name 'puppetlabs-*'); do
  modver=${d#*-}
  mod=${modver%-*}
  cp -a $d %{buildroot}%{_datadir}/%{name}/vendor_modules/$mod
done

install -Dp -m0644 %{SOURCE15} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -d -m0755 %{buildroot}%{_unitdir}
install -Dp -m0644 ext/systemd/puppet.service %{buildroot}%{_unitdir}/%{name}.service

# Note(hguemar): Conflicts with config file from hiera package
rm %{buildroot}%{_sysconfdir}/%{name}/hiera.yaml

# Install a NetworkManager dispatcher script to pickup changes to
# /etc/resolv.conf and such (https://bugzilla.redhat.com/532085).
install -Dpv -m0755 %{SOURCE13} \
 %{buildroot}%{nm_dispatcher_dir}/dispatcher.d/98-%{name}

# Install the ext/ directory to %%{_datadir}/%%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -a ext/ %{buildroot}%{_datadir}/%{name}

# Install wrappers for SELinux
install -Dp -m0755 %{SOURCE14} %{buildroot}%{_bindir}/start-puppet-agent
sed -i 's|^ExecStart=.*/bin/puppet|ExecStart=%{_bindir}/start-puppet-agent|' \
 %{buildroot}%{_unitdir}/%{name}.service

# Setup tmpfiles.d config
mkdir -p %{buildroot}%{_tmpfilesdir}
echo "D %{_rundir}/%{name} 0755 %{name} %{name} -" > \
 %{buildroot}%{_tmpfilesdir}/%{name}.conf

# Unbundle
# Note(hguemar): remove unrelated OS/distro specific folders
# These mess-up with RPM automatic dependencies compute by adding
# unnecessary deps like /sbin/runscripts
# some other things were removed with the patch
rm -r %{buildroot}%{_datadir}/%{name}/ext/{debian,osx,solaris,suse,windows,systemd,redhat}
rm %{buildroot}%{_datadir}/%{name}/ext/{build_defaults.yaml,project_data.yaml}

%pre
getent group puppet &>/dev/null || groupadd -r puppet -g 52 &>/dev/null
getent passwd puppet &>/dev/null || \
useradd -r -u 52 -g puppet -s /sbin/nologin \
 -c "Puppet" puppet &>/dev/null

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%attr(-, puppet, puppet) %{_localstatedir}/log/%{name}
%attr(-, root, root) %{_datadir}/%{name}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%dir %{nm_dispatcher_dir}
%dir %{nm_dispatcher_dir}/dispatcher.d
%{nm_dispatcher_dir}/dispatcher.d/98-puppet

# Vendor modules
%doc %{_datadir}/%{name}/vendor_modules/*/*.md
%doc %{_datadir}/%{name}/vendor_modules/*/readmes
%license %{_datadir}/%{name}/vendor_modules/*/LICENSE
# Strip development files
%exclude %{_datadir}/%{name}/vendor_modules/*/.{github,puppet-lint.rc,sync.yml}
%exclude %{_datadir}/%{name}/vendor_modules/*/{CODEOWNERS,Gemfile,appveyor.yml,spec}

%doc README.md examples
%license LICENSE
%{ruby_vendorlibdir}/hiera
%{ruby_vendorlibdir}/hiera_puppet.rb
%{ruby_vendorlibdir}/puppet
%{ruby_vendorlibdir}/puppet_pal.rb
%{ruby_vendorlibdir}/puppet.rb
%{ruby_vendorlibdir}/puppet_x.rb
%{ruby_vendorlibdir}/puppet
%dir %{_sharedstatedir}/%{name}
%dir %{_sharedstatedir}/%{name}/public
%{_bindir}/puppet
%{_bindir}/start-puppet-agent
%{_mandir}/man5/puppet.conf.5*
%{_mandir}/man8/puppet-plugin.8*
%{_mandir}/man8/puppet-report.8*
%{_mandir}/man8/puppet-resource.8*
%{_mandir}/man8/puppet-script.8*
%{_mandir}/man8/puppet-ssl.8*
%{_mandir}/man8/puppet-agent.8*
%{_mandir}/man8/puppet.8*
%{_mandir}/man8/puppet-apply.8*
%{_mandir}/man8/puppet-catalog.8*
%{_mandir}/man8/puppet-config.8*
%{_mandir}/man8/puppet-describe.8*
%{_mandir}/man8/puppet-device.8*
%{_mandir}/man8/puppet-doc.8*
%{_mandir}/man8/puppet-epp.8*
%{_mandir}/man8/puppet-facts.8*
%{_mandir}/man8/puppet-filebucket.8*
%{_mandir}/man8/puppet-generate.8*
%{_mandir}/man8/puppet-help.8*
%{_mandir}/man8/puppet-lookup.8*
%{_mandir}/man8/puppet-module.8*
%{_mandir}/man8/puppet-node.8*
%{_mandir}/man8/puppet-parser.8*

%config(noreplace) %attr(-, root, root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(-, root, root) %dir %{_sysconfdir}/%{name}/code
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/%{name}/puppet.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}

%ghost %attr(755, puppet, puppet) %{_rundir}/%{name}

%changelog
* Thu Dec 21 2023 Sindhu Karri <lakarri@microsoft.com> - 7.12.1-5
- Promote package to Mariner Base repo

* Sun Apr 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.12.1-4
- Updating Ruby vendor lib path macro.

* Thu Apr 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.12.1-3
- Spec clean-up.

* Thu Dec 30 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 7.12.1-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Nov 18 2021 Breno Brand Fernandes <brandfbb@gmail.com> - 7.12.1-1
- Update to 7.12.1

* Tue Aug 17 2021 Ewoud Kohl van Wijngaarden <ewoud+fedora@kohlvanwijngaarden.nl> - 7.9.0-1
- Update to 7.9.0
- Revert paths to FHS standards

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Breno Brand Fernandes <brandfbb@gmail.com> - 7.7.0-2
- Updated puppet url

* Mon Jul 05 2021 Breno Brand Fernandes <brandfbb@gmail.com> - 7.7.0-2
- Cleaning up the spec file, adding suggestions from ekohl (Ewoud Kohl van Wijngaarden)

* Tue Jun 15 2021 Breno Brand Fernandes <brandfbb@gmail.com> - 7.7.0-1
- Update to 7.7.0 - latest version that supports ruby 3.0

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.5.20-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 02 2020 Terje Rosten <terje.rosten@ntnu.no> - 5.5.20-1
- 5.5.20
- Add patches to work (somewhat) with ruby 2.7

* Mon Feb 03 2020 Terje Rosten <terje.rosten@ntnu.no> - 5.5.18-1
- 5.5.18

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 04 2019 Alfrdo Moralejo <amoralej@redhat.com> - 5.5.10-9
- Add rubygem-multi_json as dependency.

* Sun Sep 22 2019 Terje Rosten <terje.rosten@ntnu.no> - 5.5.10-8
- Prefer /run over /var/run (rhbz#1710635)

* Sun Sep 22 2019 Terje Rosten <terje.rosten@ntnu.no> - 5.5.10-7
- Drop buildroot prefix in nm_dispatcher_dir macro
- Fix wrong path for gem in puppetet_gem.rb (rhbz#1751385),
  report and fix from Lucien Weller, thanks!

* Thu Aug 22 2019 Lubomir Rintel <lkundrak@v3.sk> - 5.5.10-6
- Move the NetworkManager dispatcher script out of /etc

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 13 2019 Terje Rosten <terje.rosten@ntnu.no> - 5.5.10-4
- Minor clean up

* Thu Mar 07 2019 Terje Rosten <terje.rosten@ntnu.no> - 5.5.10-3
- Move sysconfdirs to headless too

* Thu Mar 07 2019 Terje Rosten <terje.rosten@ntnu.no> - 5.5.10-2
- Move reqs to headless

* Thu Mar 07 2019 Terje Rosten <terje.rosten@ntnu.no> - 5.5.10-1
- 5.5.10

* Thu Mar 07 2019 Terje Rosten <terje.rosten@ntnu.no> - 5.5.6-6
- Split off headless subpackage, based on idea from Bogdan Dobrelya

* Sun Feb 17 2019 Bogdan Dobrelya <bdobreli@redhat.com> - 5.5.6-5
- Revert use of systemd_ordering macro

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Bogdan Dobrelya <bdobreli@redhat.com> - 5.5.6-3
- Use systemd_ordering macro

* Wed Oct 31 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 5.5.6-1
- Upstream 5.5.6
- Fix issues with RHEL > 7

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May  8 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 5.5.1-1
- Upstream 5.5.1
- Unmaintained editor extensions were removed upstream (PUP-7558)
- Deprecated commands were removed: inspect (PUP-893), extlookup2hiera (PUP-3478)
- Refreshed patches

* Thu Mar 15 2018 Terje Rosten <terje.rosten@ntnu.no> - 4.10.10-1
- Update to 4.10.10

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 James Hogarth <james.hogarth@gmail.com> - 4.10.1-3
- F28 facter3 change means puppet needs to require the ruby bindings for facter

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Dominic Cleal <dominic@cleal.org> - 4.10.1-1
- Update to 4.10.1

* Wed May 31 2017 Dominic Cleal <dominic@cleal.org> - 4.8.2-2
- Remove Fedora release restrictions from DNF package provider

* Thu May 25 2017 Dominic Cleal <dominic@cleal.org> - 4.8.2-1
- Update to 4.8.2

* Tue May 23 2017 Ville Skyttä <ville.skytta@iki.fi> - 4.6.2-5
- Move tmpfiles.d config to %%{_tmpfilesdir}
- Install LICENSE as %%license

* Tue May 23 2017 Dominic Cleal <dominic@cleal.org> - 4.6.2-4
- Fix remote code exec via YAML deserialization (BZ#1452654, CVE-2017-2295)

* Thu May 18 2017 Dominic Cleal <dominic@cleal.org> - 4.6.2-3
- Fix Ruby 2.4 compatibility, xmlrpc + OpenSSL errors (BZ#1443673, BZ#1440710)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 13 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 4.6.2-1
- Upstream 4.6.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 29 2015 Gael Chamoulaud <gchamoul@redhat.com> - 4.2.1-2
- Remove usage of vendored library safe_yaml (rhbz#1261091)

* Wed Jul 29 2015 Gael Chamoulaud <gchamoul@redhat.com> - 4.2.1-1
- Upstream 4.2.1

* Tue Jul 28 2015 Lukas Zapletal <lzap+rpm@redhat.com> 4.1.0-4
- 1246238 - systemd service type changed to 'simple'

* Tue Jul 21 2015 Lukas Zapletal <lzap+rpm@redhat.com> 4.1.0-3
- Puppet agent is started via exec rather than sub-process

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 23 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.0-1
- Upstream 4.1.0
- Fix Puppet belief that Fedora is OpenBSD (PUP-4491)

* Sun May 17 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 4.0.0-2
- Fix puppet paths and unit files (upstream #12185)

* Tue Apr 28 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 4.0.0-1
- Upstream 4.0.0

* Mon Apr 27 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 4.0.0-0.1rc1
- Upstream 4.0.0
- Fix issue codedir path
- Fix init provider for Fedora (systemd is default on all supported releases now)

* Wed Apr 22 2015 Orion Poplawski <orion@cora.nwra.com> - 3.7.5-4
- Do not unbundle puppet's semantic module

* Sun Apr 19 2015 Orion Poplawski <orion@cora.nwra.com> - 3.7.5-3
- Require rubygem(pathspec) and rubygem(semantic)

* Tue Mar 31 2015 Orion Poplawski <orion@cora.nwra.com> - 3.7.5-2
- Unbundle libs (bug #1198366)

* Tue Mar 31 2015 Orion Poplawski <orion@cora.nwra.com> - 3.7.5-1
- Update to 3.7.5

* Sat Feb 28 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 3.7.1-3
- Use systemd macros (RHBZ #1197239)

* Tue Sep 30 2014 Orion Poplawski <orion@cora.nwra.com> - 3.7.1-2
- Drop server deps and configuration changes (bug #1144298)

* Wed Sep 17 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 3.7.1-1
- Update to 3.7.1

* Tue Aug 19 2014 Lukas Zapletal <lzap+rpm@redhat.com> 3.6.2-3
- 1131398 - added start-puppet-ca SELinux wrapper binary

* Mon Jun 30 2014 Pádraig Brady <pbrady@redhat.com> - 3.6.2-2
- Allow yumrepo proxy attribute to be set to _none_

* Mon Jun 16 2014 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-1
- Update to 3.6.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Sam Kottler <skottler@fedoraproject.org> 3.6.0-1
- Remove logic specific to unsupported versions of Fedora
- Update to 3.6.0

* Mon Apr 28 2014 Sam Kottler <skottler@fedoraproject.org> 3.5.1-1
- Update to 3.5.1

* Tue Apr 08 2014 Lukas Zapletal <lzap+rpm@redhat.com> 3.4.3-3
- RHBZ#1070395 - fixed error in postun scriplet
- Reformatted all scriplets and corrected exit codes

* Tue Apr 08 2014 Lukas Zapletal <lzap+rpm@redhat.com> 3.4.3-2
- Fixed systemd unit files - wrappers are now in use and master starts
  with correct context

* Mon Feb 24 2014 Sam Kottler <skottler@fedoraproject.org> - 3.4.3-1
- Update to 3.4.3

* Wed Jan 29 2014 Sam Kottler <skottler@fedoraproject.org> - 3.4.2-5
- Add rubygem(rgen) runtime dependency

* Thu Jan 23 2014 Sam Kottler <skottler@fedoraproject.org> - 3.4.2-4
- Use localstatedir macro instead of /tmp

* Fri Jan 17 2014 Sam Kottler <skottler@fedoraproject.org> - 3.4.2-3
- Enable puppet.service during upgrade if puppetagent.service was previously enabled

* Thu Jan 16 2014 Sam Kottler <skottler@fedoraproject.org> - 3.4.2-2
- Remove F18 conditionals now that it's EOL

* Tue Jan 14 2014 Sam Kottler <skottler@fedoraproject.org> - 3.4.2-1
- Update to 3.4.2 to mitigate CVE-2013-4969 (BZ#1047792)

* Mon Nov 18 2013 Sam Kottler <skottler@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2 (BZ#1031810)

* Sat Nov 16 2013 Sam Kottler <skottler@fedoraproject.org> - 3.3.1-3
- Add patch to convert nil resource parameter values to undef (BZ#1028930)

* Fri Nov 1 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 3.3.1-2
- Added SELinux wrappers for daemon processes

* Mon Oct 7 2013 Orion Poplawski <orion@cora.nwra.com> - 3.3.1-1
- Update to 3.3.1

* Fri Sep 13 2013 Sam Kottler <skottler@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0 and remove the rundir-perms patch since it's no longer needed

* Fri Aug 30 2013 Sam Kottler <skottler@fedoraproject.org> - 3.2.4-1
- Update to 3.2.4 to fix CVE-2013-4761 and CVE-2013-4956

* Thu Aug 29 2013 Sam Kottler <skottler@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2

* Wed Aug 7 2013 Sam Kottler <skottler@fedoraproject.org> - 3.1.1-6
- Add tar as an installation requirement

* Tue Jul 30 2013 Orion Poplawski <orion@cora.nwra.com> - 3.1.1-5
- Use systemd semantics and name in NM dispatcher script

* Fri Jul 26 2013 Sam Kottler <skottler@fedoraproject.org> - 3.1.1-4
- Add hard dependency on ruby

* Tue Apr 16 2013 Orion Poplawski <orion@cora.nwra.com> - 3.1.1-3
- Add upstream patch for ruby 2.0 support
- Fix rhel ruby conditional

* Fri Mar 15 2013 Vít Ondruch <vondruch@redhat.com> - 3.1.1-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Mar 13 2013 Michael Stahnke <stahnma@puppetlabs.com> - 3.1.1-1
- Fixes for CVE-2013-1640 CVE-2013-1652 CVE-2013-1653 CVE-2013-1654
- CVE-2013-1655 CVE-2013-2274 CVE-2013-2275

* Thu Mar 07 2013 Michael Stahnke <stahnma@puppetlabs.com> - 3.1.0-4
- Disable systemd in F18 as per bz#873853
- Update Patch0 to work with 3.1

* Thu Mar  7 2013 Daniel Drake <dsd@laptop.org> - 3.1.0-2
- Improve server compatibility with old puppet clients (#831303)

* Mon Feb 11 2013 Sam Kottler <shk@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Tue Oct 30 2012 Moses Mendoza <moses@puppetlabs.com> - 3.0.2-1
- Update to 3.0.2
- Update new dependencies (ruby >= 1.8.7, facter >= 1.6.6, hiera >= 1.0.0)
- Update for manpage and file changes in upstream
- Add conditionals for systemd service management
- Remove 0001-Ruby-1.9.3-has-a-different-error-when-require-fails.patch
- Remove 0001-Preserve-timestamps-when-installing-files.patch

* Wed Jul 11 2012 Todd Zullinger <tmz@pobox.com> - 2.7.18-1
- Update to 2.7.17, fixes CVE-2012-3864, CVE-2012-3865, CVE-2012-3866,
  CVE-2012-3867
- Improve NetworkManager compatibility, thanks to Orion Poplawski (#532085)
- Preserve timestamps when installing files

* Wed Apr 25 2012 Todd Zullinger <tmz@pobox.com> - 2.7.13-1
- Update to 2.7.13
- Change license from GPLv2 to ASL 2.0
- Drop %%post hacks to deal with upgrades from 0.25
- Minor rpmlint fixes
- Backport patch to silence confine warnings in ruby-1.9.3

* Wed Apr 11 2012 Todd Zullinger <tmz@pobox.com> - 2.6.16-1
- Update to 2.6.16, fixes CVE-2012-1986, CVE-2012-1987, and CVE-2012-1988
- Correct permissions of /var/log/puppet (0750)

* Wed Feb 22 2012 Todd Zullinger <tmz@pobox.com> - 2.6.14-1
- Update to 2.6.14, fixes CVE-2012-1053 and CVE-2012-1054

* Mon Feb 13 2012 Todd Zullinger <tmz@pobox.com> - 2.6.13-3
- Move rpmlint fixes to %%prep, add a few additional fixes
- Bump minimum ruby version to 1.8.5 now that EL-4 is all but dead
- Update install locations for Fedora-17 / Ruby-1.9
- Use ruby($lib) for augeas and shadow requirements
- Only try to run 0.25.x -> 2.6.x pid file updates on EL

* Thu Jan 05 2012 Todd Zullinger <tmz@pobox.com> - 2.6.13-2
- Revert to minimal patch for augeas >= 0.10 (bz#771097)

* Wed Dec 14 2011 Todd Zullinger <tmz@pobox.com> - 2.6.13-1
- Update to 2.6.13
- Cherry-pick various augeas fixes from upstream (bz#771097)

* Sun Oct 23 2011 Todd Zullinger <tmz@pobox.com> - 2.6.12-1
- Update to 2.6.12, fixes CVE-2011-3872
- Add upstream patch to restore Mongrel XMLRPC functionality (upstream #10244)
- Apply partial fix for upstream #9167 (tagmail report sends email when nothing
  happens)

* Thu Sep 29 2011 Todd Zullinger <tmz@pobox.com> - 2.6.6-3
- Apply upstream patches for CVE-2011-3869, CVE-2011-3870, CVE-2011-3871, and
  upstream #9793

* Tue Sep 27 2011 Todd Zullinger <tmz@pobox.com> - 2.6.6-2
- Apply upstream patch for CVE-2011-3848

* Wed Mar 16 2011 Todd Zullinger <tmz@pobox.com> - 2.6.6-1
- Update to 2.6.6
- Ensure %%pre exits cleanly
- Fix License tag, puppet is now GPLv2 only
- Create and own /usr/share/puppet/modules (#615432)
- Properly restart puppet agent/master daemons on upgrades from 0.25.x
- Require libselinux-utils when selinux support is enabled
- Support tmpfiles.d for Fedora >= 15 (#656677)
- Apply a few upstream fixes for 0.25.5 regressions

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 17 2010 Todd Zullinger <tmz@pobox.com> - 0.25.5-1
- Update to 0.25.5
- Adjust selinux conditional for EL-6
- Apply rundir-perms patch from tarball rather than including it separately
- Update URL's to reflect the new puppetlabs.com domain

* Fri Jan 29 2010 Todd Zullinger <tmz@pobox.com> - 0.25.4-1
- Update to 0.25.4

* Tue Jan 19 2010 Todd Zullinger <tmz@pobox.com> - 0.25.3-2
- Apply upstream patch to fix cron resources (upstream #2845)

* Mon Jan 11 2010 Todd Zullinger <tmz@pobox.com> - 0.25.3-1
- Update to 0.25.3

* Tue Jan 05 2010 Todd Zullinger <tmz@pobox.com> - 0.25.2-1.1
- Replace %%define with %%global for macros

* Tue Jan 05 2010 Todd Zullinger <tmz@pobox.com> - 0.25.2-1
- Update to 0.25.2
- Fixes CVE-2010-0156, tmpfile security issue (#502881)
- Install auth.conf, puppetqd manpage, and queuing examples/docs

* Wed Nov 25 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.25.1-1
- New upstream version

* Tue Oct 27 2009 Todd Zullinger <tmz@pobox.com> - 0.25.1-0.3
- Update to 0.25.1
- Include the pi program and man page (R.I.Pienaar)

* Sat Oct 17 2009 Todd Zullinger <tmz@pobox.com> - 0.25.1-0.2.rc2
- Update to 0.25.1rc2

* Tue Sep 22 2009 Todd Zullinger <tmz@pobox.com> - 0.25.1-0.1.rc1
- Update to 0.25.1rc1
- Move puppetca to puppet package, it has uses on client systems
- Drop redundant %%doc from manpage %%file listings

* Fri Sep 04 2009 Todd Zullinger <tmz@pobox.com> - 0.25.0-1
- Update to 0.25.0
- Fix permissions on /var/log/puppet (#495096)
- Install emacs mode and vim syntax files (#491437)
- Install ext/ directory in %%{_datadir}/%%{name} (/usr/share/puppet)

* Mon May 04 2009 Todd Zullinger <tmz@pobox.com> - 0.25.0-0.1.beta1
- Update to 0.25.0beta1
- Make Augeas and SELinux requirements build time options

* Mon Mar 23 2009 Todd Zullinger <tmz@pobox.com> - 0.24.8-1
- Update to 0.24.8
- Quiet output from %%pre
- Use upstream install script
- Increase required facter version to >= 1.5

* Tue Dec 16 2008 Todd Zullinger <tmz@pobox.com> - 0.24.7-4
- Remove redundant useradd from %%pre

* Tue Dec 16 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 0.24.7-3
- New upstream version
- Set a static uid and gid (#472073, #471918, #471919)
- Add a conditional requirement on libselinux-ruby for Fedora >= 9
- Add a dependency on ruby-augeas

* Wed Oct 22 2008 Todd Zullinger <tmz@pobox.com> - 0.24.6-1
- Update to 0.24.6
- Require ruby-shadow on Fedora and RHEL >= 5
- Simplify Fedora/RHEL version checks for ruby(abi) and BuildArch
- Require chkconfig and initstripts for preun, post, and postun scripts
- Conditionally restart puppet in %%postun
- Ensure %%preun, %%post, and %%postun scripts exit cleanly
- Create puppet user/group according to Fedora packaging guidelines
- Quiet a few rpmlint complaints
- Remove useless %%pbuild macro
- Make specfile more like the Fedora/EPEL template

* Mon Jul 28 2008 David Lutterkort <dlutter@redhat.com> - 0.24.5-1
- Add /usr/bin/puppetdoc

* Thu Jul 24 2008 Brenton Leanhardt <bleanhar@redhat.com>
- New version
- man pages now ship with tarball
- examples/code moved to root examples dir in upstream tarball

* Tue Mar 25 2008 David Lutterkort <dlutter@redhat.com> - 0.24.4-1
- Add man pages (from separate tarball, upstream will fix to
  include in main tarball)

* Mon Mar 24 2008 David Lutterkort <dlutter@redhat.com> - 0.24.3-1
- New version

* Wed Mar  5 2008 David Lutterkort <dlutter@redhat.com> - 0.24.2-1
- New version

* Sat Dec 22 2007 David Lutterkort <dlutter@redhat.com> - 0.24.1-1
- New version

* Mon Dec 17 2007 David Lutterkort <dlutter@redhat.com> - 0.24.0-2
- Use updated upstream tarball that contains yumhelper.py

* Fri Dec 14 2007 David Lutterkort <dlutter@redhat.com> - 0.24.0-1
- Fixed license
- Munge examples/ to make rpmlint happier

* Wed Aug 22 2007 David Lutterkort <dlutter@redhat.com> - 0.23.2-1
- New version

* Thu Jul 26 2007 David Lutterkort <dlutter@redhat.com> - 0.23.1-1
- Remove old config files

* Wed Jun 20 2007 David Lutterkort <dlutter@redhat.com> - 0.23.0-1
- Install one puppet.conf instead of old config files, keep old configs
  around to ease update
- Use plain shell commands in install instead of macros

* Wed May  2 2007 David Lutterkort <dlutter@redhat.com> - 0.22.4-1
- New version

* Thu Mar 29 2007 David Lutterkort <dlutter@redhat.com> - 0.22.3-1
- Claim ownership of _sysconfdir/puppet (bz 233908)

* Mon Mar 19 2007 David Lutterkort <dlutter@redhat.com> - 0.22.2-1
- Set puppet's homedir to /var/lib/puppet, not /var/puppet
- Remove no-lockdir patch, not needed anymore

* Mon Feb 12 2007 David Lutterkort <dlutter@redhat.com> - 0.22.1-2
- Fix bogus config parameter in puppetd.conf

* Sat Feb  3 2007 David Lutterkort <dlutter@redhat.com> - 0.22.1-1
- New version

* Fri Jan  5 2007 David Lutterkort <dlutter@redhat.com> - 0.22.0-1
- New version

* Mon Nov 20 2006 David Lutterkort <dlutter@redhat.com> - 0.20.1-2
- Make require ruby(abi) and buildarch: noarch conditional for fedora 5 or
  later to allow building on older fedora releases

* Mon Nov 13 2006 David Lutterkort <dlutter@redhat.com> - 0.20.1-1
- New version

* Mon Oct 23 2006 David Lutterkort <dlutter@redhat.com> - 0.20.0-1
- New version

* Tue Sep 26 2006 David Lutterkort <dlutter@redhat.com> - 0.19.3-1
- New version

* Mon Sep 18 2006 David Lutterkort <dlutter@redhat.com> - 0.19.1-1
- New version

* Thu Sep  7 2006 David Lutterkort <dlutter@redhat.com> - 0.19.0-1
- New version

* Tue Aug  1 2006 David Lutterkort <dlutter@redhat.com> - 0.18.4-2
- Use /usr/bin/ruby directly instead of /usr/bin/env ruby in
  executables. Otherwise, initscripts break since pidof can't find the
  right process

* Tue Aug  1 2006 David Lutterkort <dlutter@redhat.com> - 0.18.4-1
- New version

* Fri Jul 14 2006 David Lutterkort <dlutter@redhat.com> - 0.18.3-1
- New version

* Wed Jul  5 2006 David Lutterkort <dlutter@redhat.com> - 0.18.2-1
- New version

* Wed Jun 28 2006 David Lutterkort <dlutter@redhat.com> - 0.18.1-1
- Removed lsb-config.patch and yumrepo.patch since they are upstream now

* Mon Jun 19 2006 David Lutterkort <dlutter@redhat.com> - 0.18.0-1
- Patch config for LSB compliance (lsb-config.patch)
- Changed config moves /var/puppet to /var/lib/puppet, /etc/puppet/ssl
  to /var/lib/puppet, /etc/puppet/clases.txt to /var/lib/puppet/classes.txt,
  /etc/puppet/localconfig.yaml to /var/lib/puppet/localconfig.yaml

* Fri May 19 2006 David Lutterkort <dlutter@redhat.com> - 0.17.2-1
- Added /usr/bin/puppetrun to server subpackage
- Backported patch for yumrepo type (yumrepo.patch)

* Wed May  3 2006 David Lutterkort <dlutter@redhat.com> - 0.16.4-1
- Rebuilt

* Fri Apr 21 2006 David Lutterkort <dlutter@redhat.com> - 0.16.0-1
- Fix default file permissions in server subpackage
- Run puppetmaster as user puppet
- rebuilt for 0.16.0

* Mon Apr 17 2006 David Lutterkort <dlutter@redhat.com> - 0.15.3-2
- Don't create empty log files in post-install scriptlet

* Fri Apr  7 2006 David Lutterkort <dlutter@redhat.com> - 0.15.3-1
- Rebuilt for new version

* Wed Mar 22 2006 David Lutterkort <dlutter@redhat.com> - 0.15.1-1
- Patch0: Run puppetmaster as root; running as puppet is not ready
  for primetime

* Mon Mar 13 2006 David Lutterkort <dlutter@redhat.com> - 0.15.0-1
- Commented out noarch; requires fix for bz184199

* Mon Mar  6 2006 David Lutterkort <dlutter@redhat.com> - 0.14.0-1
- Added BuildRequires for ruby

* Wed Mar  1 2006 David Lutterkort <dlutter@redhat.com> - 0.13.5-1
- Removed use of fedora-usermgmt. It is not required for Fedora Extras and
  makes it unnecessarily hard to use this rpm outside of Fedora. Just
  allocate the puppet uid/gid dynamically

* Sun Feb 19 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-4
- Use fedora-usermgmt to create puppet user/group. Use uid/gid 24. Fixed
problem with listing fileserver.conf and puppetmaster.conf twice

* Wed Feb  8 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-3
- Fix puppetd.conf

* Wed Feb  8 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-2
- Changes to run puppetmaster as user puppet

* Mon Feb  6 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-1
- Don't mark initscripts as config files

* Mon Feb  6 2006 David Lutterkort <dlutter@redhat.com> - 0.12.0-2
- Fix BuildRoot. Add dist to release

* Tue Jan 17 2006 David Lutterkort <dlutter@redhat.com> - 0.11.0-1
- Rebuild

* Thu Jan 12 2006 David Lutterkort <dlutter@redhat.com> - 0.10.2-1
- Updated for 0.10.2 Fixed minor kink in how Source is given

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-3
- Added basic fileserver.conf

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-1
- Updated. Moved installation of library files to sitelibdir. Pulled
initscripts into separate files. Folded tools rpm into server

* Thu Nov 24 2005 Duane Griffin <d.griffin@psenterprise.com>
- Added init scripts for the client

* Wed Nov 23 2005 Duane Griffin <d.griffin@psenterprise.com>
- First packaging
