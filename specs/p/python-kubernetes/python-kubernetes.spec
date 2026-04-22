# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?python_enable_dependency_generator}

%if 0%{?rhel} == 8
%global py3 python3
%global py3dev python36
%endif
%if 0%{?rhel} >= 9
%global py3 python3
%global py3dev python3
%endif
%if 0%{?fedora} || 0%{?rhel} >= 9
%global py3 python3
%global py3dev python3
%endif

%global library kubernetes

Name:       python-%{library}
Epoch:      1
Version:    34.1.0
Release: 3%{?dist}
Summary:    Python client for the kubernetes API.
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:    Apache-2.0
URL:        https://pypi.python.org/pypi/kubernetes

Source0:    https://github.com/kubernetes-client/python/archive/v%{version}.tar.gz
Patch1:     0001-Revert-Set-an-upper-limit-on-the-urllib3-dependency.patch
BuildArch:  noarch

%package -n %{py3}-%{library}
Summary:    Kubernetes Python Client
BuildRequires:  git-core
BuildRequires:  %{py3dev}-devel
BuildRequires:  %{py3dev}-rpm-macros
BuildRequires:  %{py3}-setuptools
%if %{undefined __pythondist_requires}
%if 0%{?fedora}
Requires:  %{py3}-adal
%endif
Requires:  %{py3}-certifi
Requires:  %{py3}-six
Requires:  %{py3}-dateutil
Requires:  %{py3}-setuptools
Requires:  %{py3}-urllib3
Requires:  %{py3}-PyYAML
Requires:  %{py3}-google-auth
Requires:  %{py3}-websocket-client
Requires:  %{py3}-oauthlib
Requires:  %{py3}-durationpy
%endif

%description -n %{py3}-%{library}
Python client for the kubernetes API.

%package -n %{py3}-%{library}-tests
Summary:    Tests python-kubernetes library

Requires:  %{py3}-%{library} = 1:%{version}-%{release}

%description -n %{py3}-%{library}-tests
Tests python-kubernetes library

#recommonmark not available for docs in EPEL
%if 0%{?fedora}
%package doc
Summary: Documentation for %{name}.
Provides: %{name}-doc = 1:%{version}-%{release}
BuildRequires: %{py3}-sphinx
BuildRequires: %{py3}-recommonmark
%description doc
%{summary}
%endif

%description
Python client for the kubernetes API.

%prep
%autosetup -n python-%{version} -S git

#This is needed until CentOS 8.1. The dep was
#updated because of a CVE in urllib3 and the
#corresponding package update is in EL 8.1
%if 0%{?rhel} == 8
sed -i 's/1.24.2/1.23/g' requirements.txt
%endif

sed -i 's/^mock.*//g' test-requirements.txt
sed -i 's/^nose.*//g' test-requirements.txt
sed -i 's/^py>.*//g' test-requirements.txt

#BZ1758141 - python autorequires do not handles asterisks properly.
#Fedora is using 0.56.0+ since at least Fedora 31 so this works aorund
#the issue by setting the minimum version above the problem versions.
%if 0%{?fedora} > 30
sed -i 's/websocket-client.*/websocket-client>=0.43.0/g' requirements.txt
%endif

%build
%py3_build

#11.0 adds spinx-markdown-tables as a requirement
#It is not packaged in Fedora
#%if 0%{?fedora}
#sphinx-build doc/source/ html
#%{__rm} -rf html/.buildinfo
#%endif

# Currently recommonmark requires an old version of commonmark,
# commonmark (<=0.5.4) wich doesn't exist in fedora rawhide so
# we disable docs generation until recommonmark is fixed to be
# compatible with recent version.
# generate html docs
# {__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%install
%py3_install
cp -pr kubernetes/test %{buildroot}%{python3_sitelib}/%{library}/
cp -pr kubernetes/e2e_test %{buildroot}%{python3_sitelib}/%{library}/

%check

%if 0%{?fedora}
%files doc
%license LICENSE
#%doc html
%endif

%files -n %{py3}-%{library}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{library}
%{python3_sitelib}/%{library}-*.egg-info
%exclude %{python3_sitelib}/%{library}/test
%exclude %{python3_sitelib}/%{library}/e2e_test

%files -n %{py3}-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{library}/test
%{python3_sitelib}/%{library}/e2e_test

%changelog
* Tue Sep 30 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:34.1.0-2
- Drop urllib3 upper limit so the package can be installed, https://github.com/kubernetes-client/python/issues/2458

* Mon Sep 29 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:34.1.0-1
- Update to 34.1.0 (#2371315)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:32.0.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:32.0.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:32.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1:32.0.1-2
- Rebuilt for Python 3.14

* Wed Feb 19 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:32.0.1-1
- Update to 32.0.1 (#2341838)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:31.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Miro Hrončok <mhroncok@redhat.com> - 1:31.0.0-2
- Remove unused tests Requires
- https://fedoraproject.org/wiki/Changes/DeprecateNose
- https://fedoraproject.org/wiki/Changes/DeprecatePythonMock

* Tue Nov 05 2024 Jason Montleon <jmontleo@redhat.com 1:31.0.0-1
- - Update to 31.0.0 (#2313897)

* Sun Sep 22 2024 Jason Montleon <jmontleo@redhat.com 1:30.1.0-5
- Fix fail to install for tests sub-package for EPEL 9.
- BZ #2314125 will fully resolve FTI on EPEL 10.

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1:30.1.0-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:30.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1:30.1.0-2
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:30.1.0-1
- Update to 30.1.0 (#2290809)

* Mon Jan 29 2024 Jason Montleon <jmontleo@redhat.com> - 1:29.0.0-1
- Update to 29.0.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Jason Montleon <jmontleo@redhat.com> - 1:26.1.0-2
- Replace git BuildRequire with git-core which is sufficient
- Remove conditional for python2

* Mon Jul 17 2023 Jason Montleon <jmontleo@redhat.com> - 1:26.1.0-1
- Update to 26.1.0

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1:24.2.0-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:24.2.0-5
 Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 02 2022 Jason Montleon <jmontleo@redhat.com> - 1:24.2.0-4
- Align release / changelog

* Tue Aug 02 2022 Jason Montleon <jmontleo@redhat.com> - 1:24.2.0-1
- Update to 24.2.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:21.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:21.7.0-2
- Rebuilt for Python 3.11

* Sun Jan 30 2022 Jason Montleon <jmontleo@redhat.com> - 1:21.7.0-1
- Update to 21.7.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:18.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 20 2021 Jason Montleon <jmontleo@redhat.com> - 1:18.20.0-1
* Update to 18.20.0

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:11.0.0-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:11.0.0-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:11.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Jason Montleon <jmontleo@redhat.com> - 1:11.0.0-6
- Fix sub-package requirements to account for the epoch

* Fri Dec 11 2020 Jason Montleon <jmontleo@redhat.com> - 1:11.0.0-5
- Revert upadte until https://github.com/kubernetes-client/python/issues/1333 is fixed

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 11.0.0-3
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> - 11.0.0-2
- Fix EPEL 7 and 8 builds

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> - 11.0.0-1
- Update to 11.0.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
- Work around BZ1758141 for BZ1799937

* Fri Nov 08 2019 Jason Montleon <jmontleo@redhat.com> 10.0.1-1
- Update to upstream 10.0.1

* Fri Oct 18 2019 Jason Montleon <jmontleo@redhat.com> 9.0.1-1
- Update to upstream 9.0.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 18 2019 Jason Montleon <jmontleo@redhat.com> 8.0.1-1
- Update to upstream 8.0.1

* Sat Feb 2 2019 Jason Montleon <jmontleo@redhat.com> 8.0.0-8
- add upstream patch to make python-adal optional
- remove python-adal requires for EL7 since it's not available in RHEL base, optional, or extras

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Jason Montleon <jmontleo@redhat.com> 8.0.0-6
- Only apply EL7 requirement patch on EL7 so Fedora dependency generator works correctly

* Thu Jan 17 2019 Jason Montleon <jmontleo@redhat.com> 8.0.0-5
- Keep python 2 enabled for Fedora 29.

* Tue Jan 15 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.0.0-4
- Enable python dependency generator

* Fri Dec 14 2018 Jason Montleon <jmontleo@redhat.com> 8.0.0-3
- Default to python 2 for EPEL 7 and python 3 for Fedora
- Add docs package for Fedora

* Mon Nov 26 2018 Jason Montleon <jmontleo@redhat.com> 8.0.0-2
- Patch setup.py to work with EL7 python-setuptools

* Mon Nov 5 2018 Jason Montleon <jmontleo@redhat.com> 8.0.0-1
- Update to 8.0.0

* Wed Oct 3 2018 Jason Montleon <jmontleo@redhat.com> 7.0.0-3
- Adding missing python3-adal dependency

* Wed Oct 3 2018 Jason Montleon <jmontleo@redhat.com> 7.0.0-2
- Adding missing python-adal dependency

* Wed Oct 3 2018 Jason Montleon <jmontleo@redhat.com> 7.0.0-1
- Update to 7.0.0

* Tue Feb 28 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.3.0b3
- Remove BRs for documentation building as it's not creating html docs.

* Mon Feb 27 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.2.0b3
- Fixed files section of python3-kubernetes-tests to contain python3 tests.

* Mon Feb 27 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.1.0b3
- Initial spec for release 1.0.0b3
