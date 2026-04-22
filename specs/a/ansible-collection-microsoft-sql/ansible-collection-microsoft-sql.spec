# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# NOTE: ansible-core is in rhel-8.6 and newer, but not installable
# in buildroot as it depended on modular Python.
# It has been installable at buildtime in 8.8 and newer.
%if 0%{?fedora}
BuildRequires: ansible-packaging
%else
%if 0%{?rhel} >= 8
BuildRequires: ansible-core >= 2.11.0
%endif
%endif

%bcond_with collection_artifact

Name: ansible-collection-microsoft-sql
Url: https://github.com/linux-system-roles/mssql
Summary: The Ansible collection for Microsoft SQL Server management
Version: 2.6.4
Release: 2%{?dist}

License: MIT

%global rolename mssql
%global collection_namespace microsoft
%global collection_name sql
%global collection_rolename server
%global collection_version %{version}
%global legacy_rolename %{collection_namespace}.sql-server
%global _pkglicensedir %{_licensedir}/%{name}

# be compatible with the usual Fedora Provides:
Provides: ansible-collection-%{collection_namespace}-%{collection_name} = %{collection_version}-%{release}

# ansible-core is in rhel 8.6 and later - default to ansible-core, but allow
# the use of ansible if present - we may revisit this if the automatic dependency
# generator is added to ansible-core in RHEL
# Fedora - the automatic generator will add this - no need to explicit declare
# it in the spec file
# EL7 - no dependency on ansible because there is no ansible in el7 - user is
# responsible for knowing they have to install ansible
%if 0%{?rhel} >= 8
Requires: (ansible-core >= 2.11.0 or ansible >= 2.9.0)
%endif

%if 0%{?rhel}
Requires: rhel-system-roles
%else
Requires: linux-system-roles
%endif

%global mainid eadd06cfa98d244b096cff24cd11b668428b1613
# Use either hash or tag for source1id
# %%global source1id 50edba099ab2c8b25b225fe760cb5a459b320030
%global source1id %{version}
%global parenturl https://github.com/linux-system-roles
Source: %{parenturl}/auto-maintenance/archive/%{mainid}/auto-maintenance-%{mainid}.tar.gz
Source1: %{parenturl}/%{rolename}/archive/%{source1id}/%{rolename}-%{source1id}.tar.gz

# EL only, includes macros available from ansible-packaging that is not available on EL
Source1002: ansible-packaging.inc
%include %{SOURCE1002}

BuildArch: noarch
# there is no ansible on i686, so when we get a builder that uses
# this arch, the build fails with
# No matching package to install: 'ansible-core >= 2.11.0'
ExcludeArch: i686

# Requirements for galaxy_transform.py
BuildRequires: python3
BuildRequires: python%{python3_pkgversion}-ruamel-yaml

%description
This RPM installs the %{collection_namespace}.%{collection_name} Ansible
collection that provides the %{collection_rolename} role for Microsoft SQL
Server management. This RPM also installs the %{legacy_rolename} role
in the legacy roles format for users of Ansible < 2.9.

%if %{with collection_artifact}
%package collection-artifact
Summary: Collection artifact to import to Automation Hub / Ansible Galaxy

%description collection-artifact
Collection artifact for %{name}. This package contains
%{collection_namespace}-%{collection_name}-%{collection_version}.tar.gz
%endif

%pretrans -p <lua>
path = "%{ansible_roles_dir}/%{legacy_rolename}"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%prep
%setup -q -a1 -n auto-maintenance-%{mainid}

mv %{rolename}-%{source1id} %{rolename}

# Remove symlinks in tests/roles
if [ -d %{rolename}/tests/roles ]; then
    find %{rolename}/tests/roles -type l -exec rm {} \;
    if [ -d %{rolename}/tests/roles/linux-system-roles.%{rolename} ]; then
        rm -r %{rolename}/tests/roles/linux-system-roles.%{rolename}
    fi
fi

%build
# Move a hidden .README.html to a not hidden README.html
mv %{rolename}/.README.html %{rolename}/README.html

mkdir .collections

# Copy galaxy.yml for the collection build
cp %{rolename}/.collection/galaxy.yml ./

%if 0%{?rhel}
# Ensure the correct entries in galaxy.yml
./galaxy_transform.py "%{collection_namespace}" "%{collection_name}" "%{collection_version}" \
                      "Ansible collection for Microsoft SQL Server management" \
                      "https://github.com/linux-system-roles/mssql" \
                      "https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/automating_system_administration_by_using_rhel_system_roles/assembly_configuring-microsoft-sql-server-using-microsoft-sql-server-ansible-role_automating-system-administration-by-using-rhel-system-roles" \
                      "https://access.redhat.com/articles/3050101" \
                      "https://issues.redhat.com/secure/CreateIssueDetails!init.jspa?pid=12332745&summary=Your%20request%20summary&issuetype=1&priority=10200&labels=Partner-Feature-Request&components=12377164" \
                      > galaxy.yml.tmp
%else
./galaxy_transform.py "%{collection_namespace}" "%{collection_name}" "%{collection_version}" \
                      "Ansible collection for Microsoft SQL Server management" \
                      > galaxy.yml.tmp
%endif
mv galaxy.yml.tmp galaxy.yml

%if 0%{?rhel}
# Replace "fedora.linux_system_roles" with "redhat.rhel_system_roles"
# This is for the "roles calling other roles" case
find . -type f -exec \
     sed -e "s/fedora\.linux_system_roles/redhat.rhel_system_roles/g" \
         -i {} \;
%endif

# Convert to the collection format
python3 lsr_role2collection.py --role "%{rolename}" \
    --src-path "%{rolename}" \
    --src-owner linux-system-roles \
    --dest-path .collections \
    --readme %{rolename}/.collection/README.md \
    --namespace %{collection_namespace} \
    --collection %{collection_name} \
    --new-role "%{collection_rolename}" \
    --meta-runtime lsr_role2collection/runtime.yml

# Replace remnants of "linux-system-roles.mssql" with collection FQDN
find .collections/ansible_collections/%{collection_namespace}/%{collection_name}/ -type f -exec \
     sed -e "s/linux-system-roles[.]%{rolename}\\>/%{collection_namespace}.%{collection_name}.%{collection_rolename}/g" \
         -i {} \;

# removing dot files/dirs
rm -r .collections/ansible_collections/%{collection_namespace}/%{collection_name}/.[A-Za-z]*
rm -r .collections/ansible_collections/%{collection_namespace}/%{collection_name}/tests/%{collection_rolename}/.[A-Za-z]*

# Copy CHANGELOG.md from collection role to parent collection dir
cp .collections/ansible_collections/%{collection_namespace}/%{collection_name}/roles/%{collection_rolename}/CHANGELOG.md \
    .collections/ansible_collections/%{collection_namespace}/%{collection_name}

# Copy galaxy.yml to the collection directory
cp -p galaxy.yml .collections/ansible_collections/%{collection_namespace}/%{collection_name}

# Build collection
pushd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
%ansible_collection_build
popd

%install
mkdir -p %{buildroot}%{ansible_roles_dir}

# Step 1: Install the role in legacy format
# Copy role in legacy format and rename rolename in tests
cp -pR "%{rolename}" "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}"
find %{buildroot}%{ansible_roles_dir}/%{legacy_rolename} -type f -exec \
     sed -e "s/%{collection_namespace}\.%{collection_name}\.%{collection_rolename}/%{legacy_rolename}/g" \
         -i {} \;

# Copy README, COPYING, CHANGELOG and LICENSE files to the corresponding directories
mkdir -p %{buildroot}%{_pkglicensedir}
mkdir -p "%{buildroot}%{_pkgdocdir}/%{legacy_rolename}"
ln -sr "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/README.md" \
    "%{buildroot}%{_pkgdocdir}/%{legacy_rolename}"
ln -sr "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/README.html" \
    "%{buildroot}%{_pkgdocdir}/%{legacy_rolename}"
ln -sr "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/CHANGELOG.md" \
    "%{buildroot}%{_pkgdocdir}/%{legacy_rolename}"
if [ -f "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/COPYING" ]; then
    ln -sr "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/COPYING" \
        "%{buildroot}%{_pkglicensedir}/%{legacy_rolename}.COPYING"
fi
if [ -f "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/LICENSE" ]; then
    ln -sr "%{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/LICENSE" \
        "%{buildroot}%{_pkglicensedir}/%{legacy_rolename}.LICENSE"
fi

# Remove dot files
rm -r %{buildroot}%{ansible_roles_dir}/*/.[A-Za-z]*
rm -r %{buildroot}%{ansible_roles_dir}/%{legacy_rolename}/tests/.[A-Za-z]*

# Step 2: Remove molecule directory from all roles under ansible_roles_dir
rm -r %{buildroot}%{ansible_roles_dir}/*/molecule

# Step 3: Install the role in collection format
pushd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
%ansible_collection_install
popd

mkdir -p %{buildroot}%{_pkgdocdir}/collection/roles

# Link collection README to /usr/share/doc/ansible-collection-microsoft-sql/collection.
ln -sr %{buildroot}%{ansible_collection_files}%{collection_name}/README.md \
   %{buildroot}%{_pkgdocdir}/collection

# Link role READMEs to /usr/share/doc/ansible-collection-microsoft-sql/collection/roles/server
mkdir -p %{buildroot}%{_pkgdocdir}/collection/roles/%{collection_rolename}
ln -sr %{buildroot}%{ansible_collection_files}%{collection_name}/roles/%{collection_rolename}/README.md \
    %{buildroot}%{_pkgdocdir}/collection/roles/%{collection_rolename}
ln -sr %{buildroot}%{ansible_collection_files}%{collection_name}/roles/%{collection_rolename}/README.html \
    %{buildroot}%{_pkgdocdir}/collection/roles/%{collection_rolename}

# Link role CHANGELOG.md to /usr/share/doc/ansible-collection-microsoft-sql/collection/roles/server
ln -sr %{buildroot}%{ansible_collection_files}%{collection_name}/roles/%{collection_rolename}/CHANGELOG.md \
    %{buildroot}%{_pkgdocdir}/collection/roles/%{collection_rolename}

# Step 4: Copy collection artifact to /usr/share/ansible/collections/ for collection-artifact
%if %{with collection_artifact}
pushd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
if [ -f %{collection_namespace}-%{collection_name}-%{collection_version}.tar.gz ]; then
    mv %{collection_namespace}-%{collection_name}-%{collection_version}.tar.gz \
       %{buildroot}%{_datadir}/ansible/collections/
fi
popd
%endif

# Step 5: Generate the %%files section in files_section.txt
# Bulk files inclusion is not possible because roles store doc and licence
# files together with other files
format_item_for_files() {
    # $1 is directory or file name in buildroot
    # $2 - if true, and item is a directory, use %%dir
    local item
    local files_item
    item="$1" # full path including buildroot
    files_item=${item##"%{buildroot}"} # path with cut buildroot to be added to %%files
    if [ -L "$item" ]; then
        echo "$files_item"
    elif [ -d "$item" ]; then
        if [[ "$item" == */doc* ]]; then
            echo "%doc $files_item"
        elif [ "${2:-false}" = true ]; then
            echo "%dir $files_item"
        else
            echo "$files_item"
        fi
    elif [[ "$item" == */README.md ]] || [[ "$item" == */README.html ]] || [[ "$item" == */CHANGELOG.md ]]; then
        if [[ "$item" == */private_* ]]; then
            # mark as regular file, not %%doc
            echo "$files_item"
        else
            echo "%doc $files_item"
        fi
    elif [[ "$item" == */COPYING* ]] || [[ "$item" == */LICENSE* ]]; then
        echo "%""%""license" "$files_item"
    else
        echo "$files_item"
    fi
}

files_section=files_section.txt
rm -f $files_section
touch $files_section
# Dynamically generate files section entries for %%{ansible_collection_files}
find %{buildroot}%{ansible_collection_files}%{collection_name} -mindepth 1 -maxdepth 1 | \
    while read item; do
        if [[ "$item" == */roles ]]; then
            format_item_for_files "$item" true >> $files_section
            find "$item" -mindepth 1 -maxdepth 1 | while read roles_dir; do
                format_item_for_files "$roles_dir" true >> $files_section
                find "$roles_dir" -mindepth 1 -maxdepth 1 | while read roles_item; do
                    format_item_for_files "$roles_item" >> $files_section
                done
            done
        else
            format_item_for_files "$item" >> $files_section
        fi
    done

# Dynamically generate files section entries for %%{ansible_roles_dir}
find %{buildroot}%{ansible_roles_dir} -mindepth 1 -maxdepth 1 | \
    while read item; do
        if [ -d "$item" ]; then
            format_item_for_files "$item" true >> $files_section
            find "$item" -mindepth 1 -maxdepth 1 | while read roles_item; do
                format_item_for_files "$roles_item" >> $files_section
            done
        else
            format_item_for_files "$item" >> $files_section
        fi
    done

%files -f files_section.txt
%dir %{_datadir}/ansible
%dir %{ansible_roles_dir}
%dir %{ansible_collection_files}
%dir %{ansible_collection_files}%{collection_name}
%doc %{_pkgdocdir}
%license %{_pkglicensedir}

%if %{with collection_artifact}
%files collection-artifact
%{_datadir}/ansible/collections/%{collection_namespace}-%{collection_name}-%{collection_version}.tar.gz
%endif

%changelog
* Wed Aug 13 2025 Packit <hello@packit.dev> - 2.6.4-1
- Update to version 2.6.4

* Mon Jul 28 2025 Packit <hello@packit.dev> - 2.6.3-1
- Update to version 2.6.3

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 27 2024 Packit <hello@packit.dev> - 2.5.2-1
- Update to version 2.5.2

* Mon Nov 25 2024 Packit <hello@packit.dev> - 2.5.1-1
- Update to version 2.5.1

* Wed Nov 20 2024 Sergei Petrosian <spetrosi@redhat.com> - 2.5.0-1
- Add mssql_tools_versions, mssql_tls_self_sign to allow installing different versions of mssql-tools

* Fri Nov 15 2024 Sergei Petrosian <spetrosi@redhat.com> - 2.4.0-1
- Support OpenSUSE/SLES
- Fail on RHEL or CentOS 10 because it's not supported
- Use new adutil functionality to enable AES encryption
- Add support for Fedora

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Sergei Petrosian <spetrosi@redhat.com> - 2.2.3-2
- Use downstream ansible-packaging.inc to fix eln build

* Tue Mar 12 2024 Sergei Petrosian <spetrosi@redhat.com> - 2.2.3-1
- Add support for running SQL Server as a SELinux unconfined application with SELinux in enforcing mode on RHEL 9
  Resolves: RHEL-17080
- ExcludeArch: i686

* Fri Feb 9 2024 Sergei Petrosian <spetrosi@redhat.com> - 2.2.2-1
- Update role to version 2.2.2 to fix HA
- CHANGELOG.md was missing in some places
- In legacy role, sed repalced unexpected strings at some places

* Wed Jan 31 2024 Sergei Petrosian <spetrosi@redhat.com> - 2.2.1-1
- Support installing SQL Server 2022 on RHEL 9 and running as a selinux-confined application
- Remove unnecessary variable and RPM requirements for read-scale clusters
- Add the mssql_ha_prep_for_pacemaker variable to configure SQL Server for Pacemaker
- Deprecate `mssql_ha_cluster_run_role` for `mssql_manage_ha_cluster`

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Sergei Petrosian <spetrosi@redhat.com> - 2.1.0-1
- Update role to 2.1.0 to add support for installing mssql on RHEL 9

* Mon Sep 18 2023 Sergei Petrosian <spetrosi@redhat.com> - 2.0.2-2
- Use latest auto-maintenance for updates in lsr_role2collection.py

* Wed Aug 16 2023 Sergei Petrosian <spetrosi@redhat.com> - 2.0.2-1
- Update role to version 2.0.2 to improve collection readme
- Remove with_html, instead use built-in .README.html
- Update galaxy fields

* Fri Jul 28 2023 Sergei Petrosian <spetrosi@redhat.com> - 2.0.1-1
- Update role to version 2.0.1 to fix issue in IDM CI

* Thu Jul 27 2023 Sergei Petrosian <spetrosi@redhat.com> - 2.0.0-1
- Update role to version 2.0.0 to enhance AD integration
Resolves: RHEL-877
Resolves: RHEL-878
Resolves: RHEL-879
Resolves: RHEL-880

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Sergei Petrosian <spetrosi@redhat.com> - 1.4.1-1
- Update BuiildRequires to use ansible-core on RHEL > 8.8
- Update role to version 1.4.1 to add customizable storage paths

* Tue May 30 2023 Sergei Petrosian <spetrosi@redhat.com> - 1.3.0-4
- Move RHEL related code into an include for spec readability

* Mon Feb 27 2023 Sergei Petrosian <spetrosi@redhat.com> - 1.3.0-3
- Spec: add functionality to build from a commit hash
- Use latest 1.3.0 to add flexibility to AD integration functionality
  Resolves: rhbz#2163709

* Fri Feb 3 2023 Sergei Petrosian <spetrosi@redhat.com> - 1.3.0-1
- On SQL Server Enterprise Edition, support configuring asynchronous replication
  Resolves: rhbz#2144820
- Support configuring a read-scale SQL server availability group (without pacemaker
  Resolves: rhbz#2144821
- Use the certificate role to create the cert and the key
  Resolves: rhbz#2144852
- Support SQL Server version 2022
  Resolves: rhbz#2153427
- Support integrating with AD Server for authentication
  Resolves: rhbz#2163696
- md2html.sh - use -t to generate TOC
- Replace installbase with ansible_roles_dir in pretrans scriplet

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 11 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.2.4-4
- Keep spec consistent with linux-system-roles
  - Return conditionals related to EL to keep up- and downstream consistent
  - Add pretrans scriplet to remove symlinks if exist to fix issue with update
  - Instead of copying doc and license files create symlinks
  - Dynamically generate %%files section

* Thu Sep 22 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.2.4-3
- Further simplify spec file
  - Do not install roles to /usr/share/microsoft and then create symlinks
    to /usr/share/ansible/roles/, instead install directly to
    /usr/share/ansible/roles/
  - Remove unused removal of ambiguous python shebangs

* Tue Sep 20 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.2.4-2
- Remove all code unrelated to Fedora to siplify the file
  - Remove bcond_with ansible because Fedora always have ansible
  - Replace the ansible_build_dep macro with simple ansible-packaging
  - Remove %%bcond_with html because Fedora always can convert md to html
  - Remove conditions related to RHEL
  - Replace ansible_collection_build_install with biult-in build & install
  - Remove unrelated to Fedora Provides
  - Remove all loops because this RPM contains only one role
  - Remove definition of ansible_collection_files as its part of ansible-packaging
  - Clean up %%files section
    - Use ansible_collection_files in %%files section
    - Remove duplicated lines and wildcards
  - Remove defsource - simply define the source for mssql
  - Escape macros in comments with a second %
  - 's|$RPM_BUILD_ROOT|%%{buildroot}|' for consistency
  -  Remove getarchivedir for simplicity
  - Wrap description by 80 symbols and clarify it
  - Remove tests/.fmf dir from the RPM
  Resolves: rhbz#2126901

* Thu Sep 1 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.2.4-1
- Replicate all provided databases
  - This change fixes the bug where only the first database provided with
mssql_ha_db_names got replicated
  - Clarify that the role does not remove not listed databases
  Resolves: rhbz#2066337
- Input multiple sql scripts
  - Allow _input_sql_file vars to accept list of files
  - Flush handlers prior to inputting post sql script
  Resolves: rhbz#2120712
- Note that ha_cluster is not idempotent
- SPEC: Do not update dates in CHANGELOG.md

* Thu Aug 25 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.2.3-1
- Use firewall role to configure firewall for SQL Server
  Resolves: rhbz#2120709
- Add mssql_ha_virtual_ip
  Replace mssql_ha_db_name with mssql_ha_db_names to let users replicate multiple DBs
  Resolves: rhbz#2066337

- Replace simple `mssql_input_sql_file` with `pre` and `post` variables
  Resolves: rhbz#2120712
- Add Requires: linux-system-roles or rhel-system-roles
- Replace fedora.linux_system_roles:redhat.rhel_system_roles on RHEL
- Add downstream values to galaxy.yml
- Change defcommit to defsource that takes both tags and commits
- Update CHANGELOG.md with the current date and copy it to collection dir

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 21 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.1.1-3
- Fix inserting ansible_managed
  Resolves: rhbz#2057651 (EL8)
  Resolves: rhbz#2064690 (EL9)
- Users now can provide a custom URLs to pull packages and RPM key from
  Resolves: rhbz#2038256 (EL8)
  Resolves: rhbz#2064648 (EL9)

* Fri Mar 18 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.1.1-2
- RHEL8.6, 9 - add "Requires: ansible-core or ansible"
  Resolves: rhbz#2065664 (EL8)
  Resolves: rhbz#2065669 (EL8)

* Thu Mar 17 2022 Sergei Petrosian <spetrosi@redhat.com> - 1.1.1-1
- Insert the "Ansible managed" comment to the /var/opt/mssql/mssql.conf file
  Resolves rhbz#2057651 (EL8)
  Resolves rhbz#2064690 (EL9)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Sergei Petrosian <spetrosi@redhat.com> - 1.1.0-1
- Add support for Microsoft SQL Server 2017

* Mon Jul 19 2021 Sergei Petrosian <spetrosi@redhat.com> - 1.0.12-2
- Copy fix for RHEL 7 builds from rhel-system-roles
  Link to the original fix:
  https://src.fedoraproject.org/rpms/linux-system-roles/c/093981119f99ac51a6e06a2714b587e4e2fe287c

* Tue Jul 13 2021 Sergei Petrosian <spetrosi@redhat.com> - 1.0.12-1
- Add the meta-runtime option from the latest auto-maintenance
- Use the latest mssql that ships fixes for issues #24,#25,#26,#27,#28,35

* Tue Jun 29 2021 Sergei Petrosian <spetrosi@redhat.com> - 1.0.11-3
- Add a missing slash at the {ansible_collection_files} definition for rhel 7

* Thu Jun 17 2021 Sergei Petrosian <spetrosi@redhat.com> - 1.0.11-2
- Make the ansible_collection_files macro defined in Fedora automatically and
  in RHEL manually consistent - having slash at the end to clean double-slashes

* Thu Jun 17 2021 Sergei Petrosian <spetrosi@redhat.com> - 1.0.11-1
- Update the version to be consistent with the Galaxy collection at
  https://galaxy.ansible.com/microsoft/sql

* Wed Jun 16 2021 Sergei Petrosian <spetrosi@redhat.com> - 0.0.1-5
- Update commit hash for mssql

* Wed Jun 16 2021 Sergei Petrosian <spetrosi@redhat.com> - 0.0.1-4
- Generate symlinks for roles in /usr/share/ansible/roles

* Wed Jun 16 2021 Sergei Petrosian <spetrosi@redhat.com> - 0.0.1-3
- Copy changes made to linux-system-roles in this PR:
  https://src.fedoraproject.org/rpms/linux-system-roles/pull-request/13#
- Make spec file available for older versions of OSes.
- Drop python3-six dependency which was used by lsr_role2collection.py.
- Drop html files from rpm if the version has no markdown parser.
- Drop unnecessary python scripts which include python3 only code, e.g.,
  f-strings.
  Resolves rhbz#1970165

* Mon Jun 14 2021 Sergei Petrosian <spetrosi@redhat.com> - 0.0.1-2
- Fix long description lines
- Fix incorrect role includes in microsoft/sql-server/tests/

* Thu Jun 3 2021 Sergei Petrosian <spetrosi@redhat.com> - 0.0.1-1
- Initial release
