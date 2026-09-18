# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:             ansible-pcp
Version:          2.4.2
Release:          1%{?dist}
Summary:          Ansible Metric collection for Performance Co-Pilot
License:          MIT
URL:              https://github.com/performancecopilot/ansible-pcp
Source:           https://github.com/performancecopilot/ansible-pcp/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:        noarch

%if %{defined rhel}
%global collection_namespace redhat
%global collection_name rhel_metrics
%global ansible_collection_files %{_datadir}/ansible/collections/ansible_collections/%{collection_namespace}
%else
%global collection_namespace performancecopilot
%global collection_name metrics
%endif

%if 0%{?rhel} >= 8
Requires: (ansible-core >= 2.11.0 or ansible >= 2.9.0)
%endif

%if 0%{?rhel} >= 9
BuildRequires:  ansible-core
%global ansible_collection_build ansible-galaxy collection build .
%global ansible_collection_install ansible-galaxy collection install -n -p %{buildroot}%{_datadir}/ansible/collections %{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif

%if %{defined fedora}
BuildRequires:  ansible-packaging
BuildRequires:  ansible-packaging-tests
# There's ansible-lint errors that need to be addressed
# BuildRequires: python3-ansible-lint
%endif

%description
A collection containing roles for Performance Co-Pilot (PCP) and related
software such as Grafana and Valkey.

The collection is made up of several Ansible roles, including:

%{collection_namespace}.%{collection_name}.pcp
A role for core PCP capabilities, configuring live performance analysis
with a large base set of metrics from the kernel and system services, as
well as data recording and rule inference.

%{collection_namespace}.%{collection_name}.keyserver
A role for configuring a local key server (Valkey/Redis), suitable for
use with a Performance Co-Pilot archive repository (for single or many
hosts) and fast, scalable querying of metrics.

%{collection_namespace}.%{collection_name}.grafana
A role for configuring a local Grafana server, providing web frontend
visuals for Performance Co-Pilot metrics, both live and historically.
Data sources for Vector (live), Valkey (historical) and interactive
bpftrace (eBPF) scripts can be configured by this role.  The PCP REST
API service (from the core pcp role) should be configured in order to
use this role.

%{collection_namespace}.%{collection_name}.bpftrace
A role that extends the core PCP role, providing metrics from bpftrace
scripts using Linux eBPF facilities.  Configuring authentication of a
local user capable of running bpftrace scripts via the PCP agent is a
key task of this role.

%{collection_namespace}.%{collection_name}.elasticsearch
A role that extends the core PCP role, providing metrics from a live
ElasticSearch instance for PCP analysis or exporting of PCP metric
values (and metadata) to ElasticSearch for the indexing and querying
of performance data.

%prep
%autosetup -p1
%if 0%{?rhel}
rm -vr roles/repository tests/*repository* tests/*/*repository* docs/repository
%endif
sed -i \
    -e 's/^name: .*/name: %{collection_name}/g' \
    -e 's/^namespace: .*/namespace: %{collection_namespace}/g' \
    galaxy.yml
find . -name \*.yml -o -name \*.md | while read file; do
    sed -i \
        -e 's/performancecopilot.metrics/%{collection_namespace}.%{collection_name}/g' \
    $file
done

%build
# NOTE: Even though ansible-core is in 8.6, it is only available
# at *runtime*, not at *buildtime* - so we can't have
# ansible-core as a build_dep on RHEL8
%if %{defined rhel} && 0%{?rhel} <= 8
tar -cf %{_tmppath}/%{collection_namespace}-%{collection_name}-%{version}.tar.gz .
%else
%ansible_collection_build
%endif

%install
%if %{defined rhel} && 0%{?rhel} <= 8
mkdir -p %{buildroot}%{ansible_collection_files}/%{collection_name}
cd %{buildroot}%{ansible_collection_files}/%{collection_name}
tar -xf %{_tmppath}/%{collection_namespace}-%{collection_name}-%{version}.tar.gz
%else
%ansible_collection_install
%endif

%check
# There's outstanding ansible-lint failures that need to be addressed.
# %%if %%{defined fedora}
%if 0
ansible-lint `find roles -name \*.yml`
%endif

%files
%doc README.md
%license LICENSE
%{ansible_collection_files}

%changelog
* Fri Aug 1 2025 Sam Feifer <sfeifer@redhat.com> 2.4.2-1
- Latest upstream release

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 19 2024 Sam Feife <sfeifer@redhat.com> 2.4.1-1
- Latest upstream release to resolve build issues

* Tue Oct 15 2024 Nathan Scott <nathans@redhat.com> 2.4.0-1
- Latest upstream release

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Nathan Scott <nathans@redhat.com> 2.3.0-1
- Latest upstream release

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Nathan Scott <nathans@redhat.com> 2.2.9-1
- Latest upstream release

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Nathan Scott <nathans@redhat.com> 2.2.8-1
- Latest upstream release

* Sat Nov 19 2022 Maxwell G <gotmax@e.email> - 2.2.7-2
- BuildRequire ansible-packaging on Fedora
- Resolves: rhbz#2126889
- Fix inverted conditionals and build/install the collection using ansible-galaxy
- Keep ansible-lint disabled for now
- Remove unnecessary macros
- Exclude files with galaxy.yml build_ignore

* Fri Oct 28 2022 Nathan Scott <nathans@redhat.com> 2.2.7-1
- Latest upstream release

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 21 2022 Nathan Scott <nathans@redhat.com> 2.2.5-1
- Latest upstream release

* Tue Feb 15 2022 Nathan Scott <nathans@redhat.com> 2.2.4-3
- RHEL8.6+, RHEL9+, Fedora - add "ansible-core or ansible" dep

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Nathan Scott <nathans@redhat.com> 2.2.4-1
- Small fixes for bpftrace, mssql roles and tests
- RHEL9 - add "Requires: ansible-core"
- Latest upstream release

* Fri Nov 12 2021 Nathan Scott <nathans@redhat.com> 2.2.2-1
- Correct the URL listed for this package (BZ 2001902)
- Latest upstream release

* Thu Aug 26 2021 Nathan Scott <nathans@redhat.com> 2.2.1-1
- Latest upstream release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Nathan Scott <nathans@redhat.com> 2.1.4-1
- Latest upstream release

* Thu Jun 03 2021 Nathan Scott <nathans@redhat.com> 2.1.3-1
- Latest upstream release

* Fri Feb 05 2021 Nathan Scott <nathans@redhat.com> 2.1.2-1
- Add RHEL macros to the spec alongside Fedora
- Latest upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Nathan Scott <nathans@redhat.com> 2.0.3-1
- Updated for new version with changed namespace
- Ansible collection macros now used in the spec
- Added ansible-lint checking in %%check section

* Fri Oct 23 2020 Nathan Scott <nathans@redhat.com> 1.0.0-1
- Initial RPM spec build
