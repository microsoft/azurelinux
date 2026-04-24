# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} == 7
%bcond_with    python3
%bcond_without python2
%else
%bcond_with    python2
%bcond_without python3
%endif

%global library openshift

%if 0%{?rhel} == 7
%global py3 python%{python3_pkgversion}
%global py3dev python%{python3_pkgversion}
%endif
%if 0%{?rhel} == 8
%global py3 python3
%global py3dev python36
%endif
%if 0%{?rhel} >= 9
%global py3 python3
%global py3dev python3
%endif
%if 0%{?fedora}
%global py3 python3
%global py3dev python3
%endif

Name:       python-%{library}
Version:    0.13.2
Release: 12%{?dist}
Summary:    Python client for the OpenShift API
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:    Apache-2.0
URL:        https://github.com/openshift/openshift-restclient-python
Source0:    https://github.com/openshift/openshift-restclient-python/archive/v%{version}.tar.gz
BuildArch:  noarch
Epoch:      1

%if 0%{?with_python2}
%package -n python2-%{library}
Summary:    Python client for the OpenShift API
%{?python_provide:%python_provide python2-%{library}}

BuildRequires: python2-devel
%if 0%{?rhel} != 7
BuildRequires: python2-kubernetes
%endif
BuildRequires: python-pytest
BuildRequires: python-setuptools
BuildRequires: git

Requires: python2
Requires: python2-dictdiffer
Requires: python2-kubernetes >= 9.0.0
Requires: python2-string_utils
Requires: python-requests
Requires: python2-ruamel-yaml
Requires: python-six
Requires: python-jinja2

%description -n python2-%{library}
Python client for the kubernetes API.
%endif

%if 0%{?with_python3}
%package -n %{py3}-%{library}
Summary: Python client for the OpenShift API
BuildRequires: %{py3dev}-devel
BuildRequires: %{py3dev}-rpm-macros
%if 0%{?rhel} != 7
BuildRequires: %{py3}-kubernetes >= 8.0.0
%endif
BuildRequires: %{py3}-pytest
BuildRequires: %{py3}-setuptools
BuildRequires: git

Requires: %{py3}
Requires: %{py3}-dictdiffer
Requires: %{py3}-kubernetes
Requires: %{py3}-string_utils
Requires: %{py3}-requests
Requires: %{py3}-ruamel-yaml
Requires: %{py3}-six
Requires: %{py3}-jinja2

%description -n %{py3}-%{library}
Python client for the OpenShift API
%endif

#recommonmark not available for docs in EPEL
%if 0%{?fedora}
%package doc
Summary: Documentation for %{name}.
%if 0%{?with_python3}
BuildRequires: %{py3}-sphinx
BuildRequires: %{py3}-recommonmark
%else
BuildRequires: python2-sphinx
BuildRequires: python2-recommonmark
%endif
%description doc
%{summary}
%endif

%description
Python client for the OpenShift API

%prep
%autosetup -n openshift-restclient-python-%{version} -S git
#there is no include in RHEL7 setuptools find_packages
#the requirements are also done in an non-backwards compatible way
%if 0%{?rhel}
sed -i -e "s/find_packages(include='openshift.*')/['openshift', 'openshift.dynamic', 'openshift.helper']/g" setup.py
sed -i -e "49d" setup.py
%endif

#work around https://bugzilla.redhat.com/show_bug.cgi?id=1759100 in Fedora 31
sed -i 's/~/>/g' requirements.txt

%build
%if 0%{?with_python2}
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?fedora} >= 30
sphinx-build-3 doc/source/ html
%{__rm} -rf html/.buildinfo
%{__rm} -rf html/.doctrees
%endif

%if 0%{?fedora} > 28 && 0%{?fedora} < 30
sphinx-build doc/source/ html
%{__rm} -rf html/.buildinfo
%{__rm} -rf html/.doctrees
%endif

%install
%if 0%{?with_python2}
%py2_install
%endif
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?rhel} != 7
export PYTHONPATH="$(pwd)"
%if 0%{?with_python2}
py.test test/unit -c /dev/null -v -r s
%endif
%if 0%{?with_python3}
py.test test/unit -c /dev/null -v -r s
%endif
%endif

%if 0%{?with_python2}
%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{library}
%{python2_sitelib}/%{library}-*.egg-info
%exclude %{python2_sitelib}/scripts
%endif

%if 0%{?with_python3}
%files -n %{py3}-%{library}
%license LICENSE
%{python3_sitelib}/%{library}
%{python3_sitelib}/%{library}-*.egg-info
%exclude %{python3_sitelib}/scripts
%endif

%if 0%{?fedora}
%files doc
%license LICENSE
%doc html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:0.13.2-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:0.13.2-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1:0.13.2-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1:0.13.2-6
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1:0.13.2-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 28 2023 Jason Montleon <jmontleo@redhat.com> - 1:0.13.2-1
- Update to 0.13.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1:0.13.1-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1:0.13.1-2
- Rebuilt for Python 3.11

* Mon Feb 07 2022 Jason Montleon <jmontleo@redhat.com> 1:0.13.1-1
- Update to 0.13.1

* Fri Feb 04 2022 Jason Montleon <jmontleo@redhat.com> 1:0.13.0-1
- Update to 0.13.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 20 2021 Jason Montleon <jmontleo@redhat.com> 1:0.12.1-1
- Update to 0.12.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.11.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:0.11.2-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Jason Montleon <jmontleo@redhat.com> - 1:0.11.2.1
- Rebuilt for Python 3.9

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:0.11.0-4
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> 1:0.11.0-3
- Add missing changelog entries

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> 1:0.11.0-2
- Fix el8 builds

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> 1:0.11.0-1
- Update to 0.11.0

* Fri Mar 13 2020 Jason Montleon <jmontleo@redhat.com> 1:0.10.3-1
- Update to 0.10.3

* Wed Feb 19 2020 Jason Montleon <jmontleo@redhat.com> 1:0.10.2-1
- Update to 0.10.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Jason Montleon <jmontleo@redhat.com> 0.10.1-3
- work around BZ 1759100

* Tue Dec 17 2019 Jason Montleon <jmontleo@redhat.com> 0.10.1-2
- remove exclude possibly causing problems

* Tue Dec 17 2019 Jason Montleon <jmontleo@redhat.com> 0.10.1-1
- Update to upstream 0.10.1

* Fri Nov 08 2019 Jason Montleon <jmontleo@redhat.com> 0.10.0-1
- Update to upstream 0.10.0

* Fri Oct 18 2019 Jason Montleon <jmontleo@redhat.com> 0.9.2-1
- Update to upstream 0.9.2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.8.8-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.8.8-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 25 2019 Jason Montleon <jmontleo@redhat.com> 0.8.8-1
- Update to upstream 0.8.8

* Wed Apr 24 2019 Jason Montleon <jmontleo@redhat.com> 0.8.7-1
- Update to upstream 0.8.7

* Mon Feb 18 2019 Jason Montleon <jmontleo@redhat.com> 0.8.6-1
- Update to upstream 0.8.6

* Sat Feb 2 2019 Jason Montleon <jmontleo@redhat.com> 0.8.4-3
- Disable checks for EPEL builds
- Remove kubernetes BuildRequire for EPEL builds, requires websocket-client
- websocket-client is in extras, required by EPEL, but not available in buildroot?

* Tue Jan 29 2019 Jason Montleon <jmontleo@redhat.com> 0.8.4-2
- Fix orphaned library directories
- Add unit tets to %%check
- Remove some unnecessary sed statements for EL7

* Tue Jan 29 2019 Jason Montleon <jmontleo@redhat.com> 0.8.4-1
- Update to 0.8.4

* Thu Dec 20 2018 Daniel Mellado <dmellado@redhat.com> 0.8.1-2
- Ensure .doctrees directory is also cleaned up
- Remove unnecessary provides name setting

* Tue Nov 06 2018 Jason Montleon <jmontleo@redhat.com> 0.8.1-1
- Bump version (fabian@fabianism.us)
- [release-0.8] When searching for resources, prefer non-List matches (#232)
  (openshift-cherrypick-robot@redhat.com)
- Version + dependency bump (fabian@fabianism.us)
- Disable python2 builds for Fedora and python3 for EPEL by default

* Tue Nov 06 2018 Jason Montleon <jmontleo@redhat.com> 0.8.0-1
- Fix tag condition (fabian@fabianism.us)
- Add watch to dynamic client (#221) (fabian@fabianism.us)
- Pin flake8 (fabian@fabianism.us)
- Do not decode response data in Python2 (#225)
  (16732494+wallecan@users.noreply.github.com)
- ResourceContainer does not contain delete method (#227)
  (mosonkonrad@gmail.com)
- Add basic documentation for dynamic client verbs to README (#222)
  (fabian@fabianism.us)
- Add support for *List kinds (#213) (fabian@fabianism.us)
- fix deployment conditional (fabian@fabianism.us)
- Bump version + requirements (fabian@fabianism.us)
- Add validate helper function (#199) (will@thames.id.au)
- DynamicApiError: add a summary method (#211) (pierre-louis@libregerbil.fr)
- Allow less strict kubernetes version requirements (#207) (will@thames.id.au)
- Add behavior-based tests for dynamic client (#208) (fabian@fabianism.us)
- Provide 'append_hash' for ConfigMaps and Secrets (#196) (will@thames.id.au)
- Allow creates on subresources properly (#201) (fabian@fabianism.us)
- Rename async to async_req for compatibility with python3 and kubernetes 7
  (#197) (fabian@fabianism.us)
- Update kube_config to support concurrent clusters (#193)
  (tdecacqu@redhat.com)

* Mon Aug 06 2018 David Zager <david.j.zager@gmail.com> 0.6.2-12
- Fix decode issue (#192) (lostonamountain@gmail.com)
- b64encode expects bytes not string (fridolin@redhat.com)
- Update releasers for 3.11 (david.j.zager@gmail.com)

* Mon Jul 23 2018 David Zager <david.j.zager@gmail.com> 0.6.2-11
- include version update script (fabian@fabianism.us)
- Version bump to 0.6.2 (fabian@fabianism.us)

* Thu Jul 05 2018 David Zager <david.j.zager@gmail.com> 0.6.1-10
- Install openshift.dynamic in RPM (#180) (dzager@redhat.com)

* Thu Jul 05 2018 David Zager <david.j.zager@gmail.com> 0.6.1-9
- Call functions on resource fields if they don't exist as name (#179)
  (will@thames.id.au)
- Release 0.6.1 (fabian@fabianism.us)
- Fix typo in argument passing for patch in dynamic client. (#176)
  (fabian@fabianism.us)
- Prevent duplicate keys when creating resource (#178) (dzager@redhat.com)
- Allow content type specification in resource.patch (#174) (will@thames.id.au)
- release 0.6.0 (fabian@fabianism.us)
- Default singular name to name sans last letter (#173) (fabian@fabianism.us)
- Serialize body more thoroughly, won't always be passed as kwarg (#172)
  (fabian@fabianism.us)
- decode response data for python3 compatibility (#171) (fabian@fabianism.us)
- add dynamic client (#167) (fabian@fabianism.us)
- Fixes a bug when running fix_serialization on Kubernetes ExternalName… (#161)
  (zapur1@users.noreply.github.com)

* Tue Feb 27 2018 David Zager <david.j.zager@gmail.com> 0.5.0-8
- Bug 1546843- RuntimeRawExtension objects will now deserialize
  (fabian@fabianism.us)
- Add compatiblity matrix (fabian@fabianism.us)

* Thu Feb 22 2018 David Zager <david.j.zager@gmail.com> 0.5.0-7
- Update client for release k8s-client 5.0 (david.j.zager@gmail.com)
- Lint fix (chousekn@redhat.com)
- Add 'Bearer' to auth header (chousekn@redhat.com)
- All objects will now be instantiated with the proper configuration
  (fabian@fabianism.us)
- Restore API and model matching (chousekn@redhat.com)

* Thu Feb 08 2018 David Zager <david.j.zager@gmail.com> 0.5.0.a1-6
- Allow beta k8s client (david.j.zager@gmail.com)
- Update client to use k8s client 5 (david.j.zager@gmail.com)

* Fri Jan 19 2018 David Zager <david.j.zager@gmail.com> 0.4.0.a1-5
- Add object to primitives, treat as string for now (fabian@fabianism.us)
- update version to match new scheme (fabian@fabianism.us)
- regen modules (fabian@fabianism.us)
- Don't exclude modules that appear in both k8s and openshift from codegen
  (fabian@fabianism.us)
- Prefer openshift models to kubernetes models (fabian@fabianism.us)
- extra escape characters (fabian@fabianism.us)
- Update deployment condition to enforce python versioning standards
  (fabian@fabianism.us)
- Update releasers (david.j.zager@gmail.com)

* Tue Jan 16 2018 David Zager <david.j.zager@gmail.com> 0.4.0-4
- fix linting (fabian@fabianism.us)
- Fix ansible module generation for 1.8/3.8 (fabian@fabianism.us)
- Remove old OpenShift versions (david.j.zager@gmail.com)
- Update watch test (fabian@fabianism.us)
- fix a few nil value errors (fabian@fabianism.us)
- regen modules (fabian@fabianism.us)
- Fixed some errors around object instantiation in the helpers
  (fabian@fabianism.us)
- Generated code (david.j.zager@gmail.com)
- Essentials for updating client-python to 4.0 (david.j.zager@gmail.com)
- Helper base cleanup (#132) (chousekn@redhat.com)

* Mon Dec 04 2017 Jason Montleon <jmontleo@redhat.com> 0.3.4-3
- prefix test names with the cluster type (openshift/k8s) to prevent collision
  (fabian@fabianism.us)
- after the argspec is fully created, go through all aliases and remove any
  collisions (fabian@fabianism.us)
- Add test for build config (fabian@fabianism.us)
- Update _from conversion to handle all python keywords (fabian@fabianism.us)
- Handle _from -> from and vice versa in ansible helper (fabian@fabianism.us)
- add exclude for new file that won't be packaged (#125) (jmontleo@redhat.com)
- Fix k8s_v1beta1_role_binding 404s (#122) (fabian@fabianism.us)
- Pin pytest version due to broken internal API (fabian@fabianism.us)
- Add custom_objects_spec.json to package data
  (ceridwen@users.noreply.github.com)

* Fri Nov 03 2017 Jason Montleon <jmontleo@redhat.com> 0.3.4-2
- Update version

* Fri Nov 03 2017 Jason Montleon <jmontleo@redhat.com> 0.3.3-8
- Bug 1508969 - Add foreground propagation policy (david.j.zager@gmail.com)
- Document how to use the Dockerfile (david.j.zager@gmail.com)
- Add Dockerfile (david.j.zager@gmail.com)
- add unit test for watch (fabian@fabianism.us)
- Bump version (fabian@fabianism.us)
- Support watching openshift resources (fabian@fabianism.us)

* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 0.3.3-7
- add python-requests rpm dep

* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 0.3.3-6
- Fix module Python interpreter (chousekn@redhat.com)
- Version bump (fabian@fabianism.us)
- fix version regex and api_version formatting to prevent filtering out valid
  APIs (fabian@fabianism.us)

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 0.3.2-5
- ignore requirements.txt in packaging

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 0.3.2-4
-

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 0.3.2-3
- make source name match package name

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 0.3.2-2
- Fix source name

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 0.3.2-1
- new package built with tito

* Wed May 10 2017 Jason Montleon <jmontleo@redhat.com> 1.0.0-0.3
- Initial Build

