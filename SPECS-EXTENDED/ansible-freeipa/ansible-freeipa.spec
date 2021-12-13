Vendor:         Microsoft Corporation
Distribution:   Mariner
# Turn off automatic python byte compilation because these are Ansible
# roles and the files are transferred to the node and compiled there with
# the python version used in the node
%define __brp_python_bytecompile %{nil}

%global python %{__python3}

Summary: Roles and playbooks to deploy FreeIPA servers, replicas and clients
Name: ansible-freeipa
Version: 0.3.4
Release: 2%{?dist}
URL: https://github.com/freeipa/ansible-freeipa
License: GPLv3+
Source: https://github.com/freeipa/ansible-freeipa/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch: noarch

%description
ansible-freeipa provides Ansible roles and playbooks to install and uninstall
FreeIPA servers, replicas and clients. Also modules for management.

Note: The ansible playbooks and roles require a configured ansible environment
where the ansible nodes are reachable and are properly set up to have an IP
address and a working package manager.

Features

- Server, replica and client deployment
- Cluster deployments: Server, replicas and clients in one playbook
- One-time-password (OTP) support for client installation
- Repair mode for clients
- Backup and restore, also to and from controller
- Modules for config management
- Modules for delegation management
- Modules for dns config management
- Modules for dns forwarder management
- Modules for dns record management
- Modules for dns zone management
- Modules for group management
- Modules for hbacrule management
- Modules for hbacsvc management
- Modules for hbacsvcgroup management
- Modules for host management
- Modules for hostgroup management
- Modules for location management
- Modules for permission management
- Modules for privilege management
- Modules for pwpolicy management
- Modules for role management
- Modules for self service management
- Modules for service management
- Modules for sudocmd management
- Modules for sudocmdgroup management
- Modules for sudorule management
- Modules for topology management
- Modules fot trust management
- Modules for user management
- Modules for vault management

Supported FreeIPA Versions

FreeIPA versions 4.6 and up are supported by all roles.

The client role supports versions 4.4 and up, the server role is working with
versions 4.5 and up, the replica role is currently only working with versions
4.6 and up.

Supported Distributions

- RHEL/CentOS 7.4+
- Fedora 26+
- Ubuntu
- Debian 10+ (ipaclient only, no server or replica!)

Requirements

  Controller

  - Ansible version: 2.8+ (ansible-freeipa is an Ansible Collection)
    /usr/bin/kinit is required on the controller if a one time password (OTP)
    is used
  - python3-gssapi is required on the controller if a one time password (OTP)
    is used with keytab to install the client.

  Node

  - Supported FreeIPA version (see above)
  - Supported distribution (needed for package installation only, see above)

Limitations

External signed CA is now supported. But the currently needed two step process
is an issue for the processing in a simple playbook.
Work is planned to have a new method to handle CSR for external signed CAs in
a separate step before starting the server installation.


%package tests
Summary: ansible-freeipa tests
Requires: %{name} = %{version}-%{release}

%description tests
ansible-freeipa tests.

Please have a look at %{_datadir}/ansible-freeipa/requirements-tests.txt
to get the needed requrements to run the tests.


%prep
%setup -q
# Do not create backup files with patches

# Fix python modules and module utils:
# - Remove shebang
# - Remove execute flag
for i in roles/ipa*/library/*.py roles/ipa*/module_utils/*.py plugins/*/*.py; do
    sed -i '1{/\/usr\/bin\/python*/d;}' $i
    chmod a-x $i
done

for i in utils/*.py utils/ansible-ipa-*-install utils/new_module \
         utils/changelog utils/ansible-doc-test;
do
    sed -i '{s@/usr/bin/python*@%{python}@}' $i
done


%build

%install
install -m 755 -d %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipaserver %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipaserver/README.md README-server.md
cp -rp roles/ipareplica %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipareplica/README.md README-replica.md
cp -rp roles/ipaclient %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipaclient/README.md README-client.md
cp -rp roles/ipabackup %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipabackup/README.md README-backup.md
install -m 755 -d %{buildroot}%{_datadir}/ansible/plugins/
cp -rp plugins/* %{buildroot}%{_datadir}/ansible/plugins/

install -m 755 -d %{buildroot}%{_datadir}/ansible-freeipa
cp requirements*.txt %{buildroot}%{_datadir}/ansible-freeipa/
cp -rp utils %{buildroot}%{_datadir}/ansible-freeipa/
install -m 755 -d %{buildroot}%{_datadir}/ansible-freeipa/tests
cp -rp tests %{buildroot}%{_datadir}/ansible-freeipa/

%files
%license COPYING
%{_datadir}/ansible/roles/ipaserver
%{_datadir}/ansible/roles/ipareplica
%{_datadir}/ansible/roles/ipaclient
%{_datadir}/ansible/roles/ipabackup
%{_datadir}/ansible/plugins/module_utils
%{_datadir}/ansible/plugins/modules
%doc README*.md
%doc playbooks
%{_datadir}/ansible-freeipa/requirements.txt
%{_datadir}/ansible-freeipa/requirements-dev.txt
%{_datadir}/ansible-freeipa/utils

%files tests
%{_datadir}/ansible-freeipa/tests
%{_datadir}/ansible-freeipa/requirements-tests.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.4-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Mon Jan 18 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.4-1
- Update to version 0.3.4
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.4
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.2

* Wed Dec  2 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.1-1
- Update to version 0.3.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.1
- ipabackup: Fix undefined vars for conditions in shell tasks without else

* Tue Dec  1 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.0-2
- Ship ipabackup role for backup and restore

* Thu Nov 26 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.0-1
- Update to version 0.3.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.0

* Fri Oct 09 2020 Thomas Woerner <twoerner@redhat.com> - 0.2.1-1
- Update to version 0.2.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.2.1
- Update to version 0.2.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.2.0
- New tests sub package providing upstream tests
- Utils in /usr/share/ansible-freeipa/utils

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 15 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-1
- Update to version 0.1.12 bug fix only release

* Thu Jun 11 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.11-1
- Update to version 0.1.11
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.11

* Mon Apr 27 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.10-1
- Update to version 0.1.10 with fixes and additional modules
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.10

* Mon Mar 16 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.9-1
- Update to version 0.1.8 with lots of fixes and additional modules
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.8-1
- Update to version 0.1.8 with lots of fixes and additional modules
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.8
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.7

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.6-1
- Update to version 0.1.6
  - Lots of documentation updates in READMEs and modules
  - library/ipaclient_get_otp: Enable force mode for host_add call (fixes #74)
  - Flake8 and pylint reated fixes
  - Fixed wrong path to CheckedIPAddress class in ipareplica_test
  - Remove unused ipaserver/library/ipaserver.py
  - No not use wildcard imports for modules
  - ipareplica: Add support for pki_config_override
  - ipareplica: Initialize dns.ip_addresses and dns.reverse_zones for dns setup
  - ipareplica_prepare: Properly initialize pin and cert_name variables
  - ipareplica: Fail with proper error messages
  - ipaserver: Properly set settings related to pkcs12 files
  - ipaclient: RawConfigParser is not always provided by six.moves.configparser
  - ipaclient_setup_nss: paths.GETENT is not available before
    freeipa-4.6.90.pre1
  - ipaserver_test: Initialize value from options.zonemgr
  - ipareplica_setup_custodia: create_replica only available in newer releases
  - ipaclient: Fix typo in dnsok assignment for ipaclient_setup_nss
  - ipa[server,replica]: Set _packages_adtrust for Ubuntu
  - New build script for galaxy release
  - New utils script to update module docs

* Tue Jul  9 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.5-2
- Update README-user.md: Fixed examples, new example
- ipauser example playbooks: Fixed actions, new example

* Tue Jul  9 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.5-1
- Update to version 0.1.5
  - Support for IPA 4.8.0
  - New user management module
  - New group management module
  - ipaserver: Support external signed CA
  - RHEL-8 specific vars files to be able to install needed modules
    automatically
  - ipareplica: Fixes for certmonger and kra setup
  - New tests folder
  - OTP related updates to README files
- Updates of version 0.1.4
  - ipatopologysegment: Use commands, not command
- Updates of version 0.1.3
  - ipaclient_test: Fix Python2 decode use with Python3
  - Fixed: #86 (AttributeError: 'str' object has no attribute 'decode')
  - ipaclient_get_otp: Remove ansible_python_interpreter handling
  - ipaclient: Use omit (None) for password, keytab, no string length checks
  - ipaclient_join: Support to use ipaadmin_keytab without ipaclient_use_otp
  - ipaclient: Report error message if ipaclient_get_otp failed
  - Fixes #17 Improve how tasks manage package installation
  - ipareplica: The dm password is not needed for ipareplica_master_password
  - ipareplica: Use ipareplica_server if set
  - ipatopologysegment: Allow domain+ca suffix, new state: checked
  - Documentation updates
  - Cleanups
- Update of version 0.1.2
  - Now a new Ansible Collection
  - Fix gssapi requirement for OTP: It is only needed if keytab is used with
    OTP now.
  - Fix wrong ansible argument types
  - Do not fail on textwrap for replica deployments with CA
  - Ansible lint and galaxy fixes
  - Disable automatic removal of replication agreements in uninstall
  - Enable freeipa-trust service if adtrust is enabled
  - Add support for hidden replica
  - New topology managament modules
  - Add support for pki_config_override
  - Fix host name setup in server deployment
  - Fix errors when ipaservers variable is not set
  - Fix ipaclient install role length typo
  - Cleanups

* Mon May  6 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.1-1
- Initial package
