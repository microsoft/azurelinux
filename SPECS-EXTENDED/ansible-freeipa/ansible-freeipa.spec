Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# Turn off automatic python byte compilation because these are Ansible
# roles and the files are transferred to the node and compiled there with
# the python version used in the node
%define __brp_python_bytecompile %{nil}

%global python %{__python3}

%global collection_namespace freeipa
%global collection_name ansible_freeipa
%global ansible_collections_dir %{_datadir}/ansible/collections/ansible_collections

Summary: Roles and playbooks to deploy FreeIPA servers, replicas and clients
Name: ansible-freeipa
Version: 1.13.2
Release: 2%{?dist}
URL: https://github.com/freeipa/ansible-freeipa
License: GPL-3.0-or-later
Source: https://github.com/freeipa/ansible-freeipa/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Source:  https://github.com/freeipa/ansible-freeipa/archive/refs/tags/v1.13.2.tar.gz
BuildArch: noarch
#Requires: ansible-core >= 1.15.0
#BuildRequires: ansible-core >= 1.15.0
BuildRequires: ansible
BuildRequires: python
BuildRequires: PyYAML

%description
Ansible roles to install and uninstall FreeIPA servers, replicas and clients,
roles for backups and SmartCard configuration, modules for management and also
playbooks for all roles and modules.

Note: The Ansible playbooks and roles require a configured Ansible environment
where the Ansible nodes are reachable and are properly set up to have an IP
address and a working package manager.

Features

- Server, replica and client deployment
- Cluster deployments: Server, replicas and clients in one playbook
- One-time-password (OTP) support for client installation
- Repair mode for clients
- Backup and restore, also to and from controller
- Smartcard setup for servers and clients
- Inventory plugin freeipa
- Modules for automembership rule management
- Modules for automount key management
- Modules for automount location management
- Modules for automount map management
- Modules for certificate management
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
- Modules for idoverridegroup management
- Modules for idoverrideuser management
- Modules for idp management
- Modules for idrange management
- Modules for idview management
- Modules for location management
- Modules for netgroup management
- Modules for permission management
- Modules for privilege management
- Modules for pwpolicy management
- Modules for role management
- Modules for self service management
- Modules for server management
- Modules for service management
- Modules for service delegation rule management
- Modules for service delegation target management
- Modules for sudocmd management
- Modules for sudocmdgroup management
- Modules for sudorule management
- Modules for topology management
- Modules for trust management
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
  - Ansible version: 2.13+

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

The tests for the collection are part of the collection sub package.

Please have a look at %{_datadir}/ansible-freeipa/requirements-tests.txt
to get the needed requrements to run the tests.


%package collection
Summary: %{collection_namespace}.%{collection_name} collection
Provides: ansible-collection-%{collection_namespace}-%{collection_name} = %{version}-%{release}

%description collection
The %{collection_namespace}.%{collection_name} collection, including tests.


%prep
%setup -q
# Do not create backup files with patches

# Fix python modules and module utils:
# - Remove shebang
# - Remove execute flag
for i in roles/ipa*/library/*.py roles/ipa*/module_utils/*.py plugins/*/*.py;
do
    sed -i '1{/\/usr\/bin\/python*/d;}' $i
    sed -i '1{/\/usr\/bin\/env python*/d;}' $i
    chmod a-x $i
done

for i in utils/*.py utils/new_module utils/changelog utils/ansible-doc-test;
do
    sed -i '{s@/usr/bin/python*@%{python}@}' $i
    sed -i '{s@/usr/bin/env python*@%{python}@}' $i
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
cp -rp roles/ipasmartcard_server %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipasmartcard_server/README.md README-smartcard_server.md
cp -rp roles/ipasmartcard_client %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipasmartcard_client/README.md README-smartcard_client.md
install -m 755 -d %{buildroot}%{_datadir}/ansible/plugins/
cp -rp plugins/* %{buildroot}%{_datadir}/ansible/plugins/

install -m 755 -d %{buildroot}%{_datadir}/ansible-freeipa
cp requirements*.txt %{buildroot}%{_datadir}/ansible-freeipa/
cp -rp utils %{buildroot}%{_datadir}/ansible-freeipa/
install -m 755 -d %{buildroot}%{_datadir}/ansible-freeipa/tests
cp -rp tests %{buildroot}%{_datadir}/ansible-freeipa/

# Create collection and install to %{buildroot}%{ansible_collections_dir}
# ansible-galaxy collection install creates ansible_collections directory
# automatically in given path, therefore /..
utils/build-galaxy-release.sh -o "%{version}" -p %{buildroot}%{ansible_collections_dir}/.. %{collection_namespace} %{collection_name}

%files
%license COPYING
%{_datadir}/ansible/roles/ipaserver
%{_datadir}/ansible/roles/ipareplica
%{_datadir}/ansible/roles/ipaclient
%{_datadir}/ansible/roles/ipabackup
%{_datadir}/ansible/roles/ipasmartcard_server
%{_datadir}/ansible/roles/ipasmartcard_client
%{_datadir}/ansible/plugins/doc_fragments
%{_datadir}/ansible/plugins/module_utils
%{_datadir}/ansible/plugins/modules
%{_datadir}/ansible/plugins/inventory
%doc README*.md
%doc playbooks
%{_datadir}/ansible-freeipa/requirements.txt
%{_datadir}/ansible-freeipa/requirements-dev.txt
%{_datadir}/ansible-freeipa/utils

%files tests
%{_datadir}/ansible-freeipa/tests
%{_datadir}/ansible-freeipa/requirements-tests.txt

%files collection
%dir %{ansible_collections_dir}/%{collection_namespace}
%{ansible_collections_dir}/%{collection_namespace}/%{collection_name}

%changelog
* Tue Nov 12 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.13.2-2
- Update to 1.13.2

* Mon Jul  1 2024 Thomas Woerner <twoerner@redhat.com> - 1.13.2-1
- Update to version 1.13.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.13.2
  - Support for FreeIPA 4.12
  - Idempotency fixes
  - Minimum supported ansible-core version: 2.15.0
  - Fixes for ansible-test 2.17.1

* Tue May 28 2024 Thomas Woerner <twoerner@redhat.com> - 1.13.1-1
- Update to version 1.13.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.13.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.13.1
  Highlights:
  - New inventory plugin
  - Use batch command internally for ipahost, ipaservice and ipauser
  - Fix idempotency issues in ipahost, ipaservice and ipauser
  - Fix idempotency in ipaclient_dns_resolver
  - Documentation fixes

* Tue Apr  2 2024 Thomas Woerner <twoerner@redhat.com> - 1.12.1-2
- New -collection sub package providing the freeipa.ansible_freeipa
  collection
- New build requires for ansible-core and python

* Mon Feb 12 2024 Thomas Woerner <twoerner@redhat.com> - 1.12.1-1
- Update to version 1.12.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.12.1
  Highlights:
  - Fix ipaserver deployment on CentOS 8 Stream
  - Fix ipaclient deployment with automount
  - Fix ipaclient OTP error reporting
  - Add missing support for renaming groups and users
  - Idempotency fixes in several modules

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Thomas Woerner <twoerner@redhat.com> - 1.12.0-1
- Update to version 1.12.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.12.0
  Highlights:
  - New idoverridegroup management module.
  - New idoverrideuser management module.
  - New idview management module.
  - New idp management module.
  - Bug fixes and CI improvements.

* Mon Jul 24 2023 Thomas Woerner <twoerner@redhat.com> - 1.11.1-1
- Update to version 1.11.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.11.1
  Highlights:
  - Support for GECOS, street, smb and idp attributes in ipauser module
  - Support for indirect maps in ipaautomountmap module
  - Update of user_auth_type choices in ipaconfig and ipauser modules
  - Update of auth_ind choices in ipahost and ipaservice modules
  - Upstream test and environment enhancements
  - Documentation updates

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 12 2023 Thomas Woerner <twoerner@redhat.com> - 1.11.0-1
- Update to version 1.11.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.11.0
  Highlights:
  - Multiple service management with ipaservice module
  - New ipacert module for certificate management
  - Action group support for the Ansible collections on Ansible Galaxy and
    Ansible AutomationHub
  - Fixed maxsequence handling in ipapwpolicy module
  - Even more Ansible lint driven changes

* Wed Apr  5 2023 Thomas Woerner <twoerner@redhat.com> - 1.10.0-1
- Update to version 1.10.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.10.0
  Highlights:
  - ipagroup: Allow multiple group management.
  - ipaclient: Add subid option to select the sssd profile with-subid.
  - ipaclient: Fix allow_repair with removed krb5.conf and DNS lookup.
  - ipaclient: Keep server affinity while deploying by deferring the
    creation the final krb5.conf.
  - ipaserver: Allow deployments with random serial numbers.
  - ipareplica/server: Enable removal from domain with undeployment.
  - More Ansible lint fixes.

* Fri Mar 10 2023 Rafael Jeffman <rjeffman@redhat.com> - 1.9.2-2
- Migrate to SPDX license

* Tue Jan 31 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.2-1
- Update to version 1.9.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.2

* Mon Jan 30 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.1-1
- Update to version 1.9.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.1
  Highlights:
  - Ansible 2.14 test and lint fixes
  - pwpolicy: Allow clearing policy values
  - More bug fixes

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec  6 2022 Thomas Woerner <twoerner@redhat.com> - 1.9.0-1
- Update to version 1.9.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.0
  Highlights:
  - New netgroup management module
  - sudorule: Add support for 'hostmask' parameter
  - pwpolicy: Add support for password check and grace limit
  - ipaclient: No kinit on controller for deployment using OTP
  - ipaclient: Configure DNS resolver
  - Support for ansible-core 2.14 tests

* Mon Sep 12 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.4-1
- Update to version 1.8.4
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.4

* Tue Aug 16 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.3-1
- Update to version 1.8.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.3

* Thu Jul 28 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.2-1
- Update to version 1.8.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.2

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul  7 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.1-1
- Update to version 1.8.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.1

* Fri Jun 24 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.0-1
- Update to version 1.8.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.0

* Fri Apr 29 2022 Thomas Woerner <twoerner@redhat.com> - 1.7.0-1
- Update to version 1.7.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.7.0
- Update to version 1.6.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.3

* Wed Jan 26 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.2-1
- Update to version 1.6.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.2

* Fri Jan 21 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.1-1
- Update to version 1.6.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.1
- Update to version 1.6.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.0

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 28 2021 Thomas Woerner <twoerner@redhat.com> - 1.5.3-1
- Update to version 1.5.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.3
- Update to version 1.5.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.2
- Update to version 1.5.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.1

* Tue Dec  7 2021 Thomas Woerner <twoerner@redhat.com> - 1.5.0-1
- Update to version 1.5.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.0

* Wed Oct  6 2021 Thomas Woerner <twoerner@redhat.com> - 0.4.0-1
- Update to version 0.4.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.4.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.8-1
- Update to version 0.3.8
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.8
- Update to version 0.3.7
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.7

* Tue Jun  1 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.6-1
- Update to version 0.3.6
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.6

* Wed Mar  3 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.5-1
- Update to version 0.3.5
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.5

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
