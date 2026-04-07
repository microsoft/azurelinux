# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _docdir_fmt ansible-packaging

Name:           ansible-packaging
Version:        1
Release:        18.1%{?dist}
Summary:        RPM packaging macros and generators for Ansible collections

License:        GPL-3.0-or-later

Source0:        ansible-generator
Source1:        ansible.attr
Source2:        macros.ansible
Source3:        macros.ansible-srpm
Source4:        ansible_collection.py

Source100:      COPYING

# Needed for ansible_collection.py
Requires:       %{py3_dist pyyaml}

# Require ansible-core for building. Collections still have a boolean runtime
# dependency on either ansible 2.9 OR ansible-core.
Requires:       ansible-core

Requires:       ansible-srpm-macros = %{version}-%{release}

# Conflict with anything providing its own copies of these files
%if ! (0%{?rhel} >= 8)
Conflicts:      ansible-core < 2.12.1-3
%endif
Conflicts:      ansible < 2.9.27-3

BuildArch:      noarch

%description
%{summary}.


%package -n ansible-srpm-macros
Summary:        SRPM stage RPM packaging macros for Ansible collections

%description -n ansible-srpm-macros
%{summary}.

%package tests
Summary:        Dependencies for Ansible collection package unit tests
Requires:       %{name} = %{version}-%{release}
Requires:       /usr/bin/ansible-test
# This list is taken from %%{python3_sitelib}/ansible_test/_data/requirements/units.txt
Requires:       %{py3_dist pytest}
Requires:       %{py3_dist pytest-mock}
Requires:       %{py3_dist pytest-xdist}
Requires:       (%{py3_dist pytest-forked} if ansible-core < 2.16~~)
Requires:       %{py3_dist pyyaml}
# mock is included in the list upstream, but is deprecated in Fedora.
# Maintainers should work with upstream to add compat code to support
# both unittest.mock and mock and/or patch it out themselves.
# See https://fedoraproject.org/wiki/Changes/DeprecatePythonMock.
# Requires:     %%{py3_dist mock}

%description tests
This package contains the necessary dependencies to run unit tests for packaged
Ansible collections


%prep
%autosetup -T -c
cp -a %{sources} .


%build
# Nothing to build


%install
install -Dpm0644 -t %{buildroot}%{_fileattrsdir} ansible.attr
install -Dpm0644 -t %{buildroot}%{_rpmmacrodir}  macros.ansible
install -Dpm0644 -t %{buildroot}%{_rpmmacrodir}  macros.ansible-srpm
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} ansible-generator
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} ansible_collection.py

%check
# TODO: Currently, this only tests %%{ansible_collection_url}.

rpm_eval() {
    default_macros_path="$(rpm --showrc | grep 'Macro path' | awk -F ': ' '{print $2}')"
    rpm --macros="${default_macros_path}:%{buildroot}%{_rpmmacrodir}/macros.*" "$@"
}

errors() {
    error="error: %%ansible_collection_url: You must pass the collection namespace as the first arg and the collection name as the second"
    "$@" && exit 1
    "$@" |& grep -q "${error}"
}

echo "Ensure macro fails when only collection_namespace macro is defined"
errors rpm_eval -D 'collection_namespace cc' -E '%%ansible_collection_url'

echo
echo "Ensure macro fails when only collection_name macro is defined"
errors rpm_eval -D 'collection_name cc' -E '%%ansible_collection_url'

echo
echo "Ensure macro fails when second argument is missing"
errors rpm_eval -E '%%ansible_collection_url a'

echo
echo "Ensure macro fails when second argument is missing"
errors rpm_eval -D 'collection_name b' -E '%%ansible_collection_url a'

echo
echo "Ensure macro fails when neither the control macros nor macro arguments are passed"
errors rpm_eval -E '%%ansible_collection_url'


echo
echo
echo "Ensure macro works when both arguments are passed and no control macros are set"
[ "$(rpm_eval -E '%%ansible_collection_url community general')" = \
    "https://galaxy.ansible.com/ui/repo/published/community/general" ]

echo
echo "Ensure macro works with the control macros"
[ "$(rpm_eval -D 'collection_namespace ansible' -D 'collection_name posix' \
    -E '%%ansible_collection_url')" = \
    "https://galaxy.ansible.com/ui/repo/published/ansible/posix" ]

echo
echo "Ensure macro prefers the collection namespace and name passed as an argument over the control macros"
[ "$(rpm_eval -D 'collection_namespace ansible' -D 'collection_name posix' \
    -E '%%ansible_collection_url community general')" = \
    "https://galaxy.ansible.com/ui/repo/published/community/general" ]



%files
%{_fileattrsdir}/ansible.attr
%{_rpmmacrodir}/macros.ansible
%{_rpmconfigdir}/ansible-generator
%{_rpmconfigdir}/ansible_collection.py


%files -n ansible-srpm-macros
%license COPYING
%{_rpmmacrodir}/macros.ansible-srpm

# ansible-core in RHEL 8.6 is built against python38. In c8s and the next RHEL
# 8 minor release, it will be built against python39. The testing dependencies
# are not yet packaged for either python version in EPEL 8.
#
# The ansible-test binary is unshipped in EL 10, so we cannot ship the tests
# subpackage yet.
# https://issues.redhat.com/browse/RHEL-69915
%if %{undefined el8} && %{undefined el10}
%files tests
%endif


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-18.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-17.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Maxwell G <maxwell@gtmx.me> - 1-16.1
- Temporarily disable tests subpackage on EL 10

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 10 2024 Maxwell G <maxwell@gtmx.me> - 1-15
- %%ansible_test_unit: handle test dependencies on other collections

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 05 2023 Maxwell G <maxwell@gtmx.me> - 1-12
- %%ansible_collection_url: handle new URL scheme

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 11 2023 Maxwell G <maxwell@gtmx.me> - 1-10
- %%ansible_collection_install - disable spurious collections path warnings
- ansible-packaging-tests - don't depend on pytest-forked with ansible-core 2.16
- ansible-srpm-macros - include license file in the package

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Sep 24 2022 Maxwell G <gotmax@e.email> - 1-8.1
- Refactor %%ansible_collection_url, %%ansible_collection_install,
  %%ansible_test_unit.
- Specfiles no longer need to define %%collection_namespace or %%collection_name
  for the macros to work.
- Add new %%ansible_collections_dir, %%ansible_roles_dir, and
  %%ansible_collection_filelist macros.
- Prepare to deprecate %%ansible_collection_files
- Undefine %%_package_note_file to stop that file from leaking into collection
  artifacts.

* Mon Aug 01 2022 Maxwell G <gotmax@e.email> - 1-7
- Implement %%ansible_test_unit and add ansible-packaging-tests metapackage.
- Require ansible-core at buildtime

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 17 2022 Maxwell G <gotmax@e.email> - 1-5
- Split macros required for building SRPMs into a separate package.

* Tue Apr 26 2022 Maxwell G <gotmax@e.email> - 1-4
- Restore compatability with f34 and f35.

* Mon Jan 31 2022 Neal Gompa <ngompa@fedoraproject.org> - 1-3
- Drop vestigial support for the legacy ansible package
- Make compatibile with RHEL 8.6+

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 1-1
- Initial packaging split out of ansible-core (#2038591)
