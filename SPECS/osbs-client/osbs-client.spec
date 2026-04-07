# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora}
# rhel/epel has no flexmock, pytest-capturelog
%global with_check 0
%endif

%global commit 7980ce59a95e2e2fac64f0d3aeec8cdcef297f4c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# set to 0 to create a normal release
%global dev_release 0

%if 0%{?dev_release}
%global postrelease dev
%global release 23
%else
%global postrelease 0
%global release 6
%endif

%global osbs_obsolete_vr 0.14-2

Name:           osbs-client
Version:        1.15.0
%if "x%{postrelease}" != "x0"
Release:        %{release}.%{postrelease}.git.%{shortcommit}%{?dist}
%else
Release:        %{release}%{?dist}
%endif

Summary:        Python command line client for OpenShift Build Service
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/projectatomic/osbs-client
Source0:        https://github.com/projectatomic/osbs-client/archive/%{commit}/osbs-client-%{commit}.tar.gz

BuildArch:      noarch

Requires:       python3-osbs-client = %{version}-%{release}
Requires:       python3-requests
Requires:       python3-requests-kerberos

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  git-core
BuildRequires:  python3-dateutil
BuildRequires:  python3-pytest
BuildRequires:  python3-flexmock
BuildRequires:  python3-six
BuildRequires:  python3-dockerfile-parse
BuildRequires:  python3-jsonschema
BuildRequires:  python3-pytest-runner
BuildRequires:  python3-requests
BuildRequires:  python3-requests-kerberos
BuildRequires:  python3-PyYAML
%endif # with_check


Provides:       osbs = %{version}-%{release}
Obsoletes:      osbs < %{osbs_obsolete_vr}

%description
It is able to query OpenShift v3 for various stuff related to building images.
It can initiate builds, list builds, get info about builds, get build logs...
This package contains osbs command line client.

%package -n python3-osbs-client
Summary:        Python 3 module for OpenShift Build Service
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
Requires:       python3-dockerfile-parse
Requires:       python3-jsonschema
Requires:       python3-requests
Requires:       python3-requests-kerberos
Requires:       python3-dateutil
Requires:       python3-setuptools
Requires:       python3-six
Requires:       krb5-workstation
Requires:       python3-PyYAML
Requires:       git-core

Provides:       python3-osbs = %{version}-%{release}
Obsoletes:      python3-osbs < %{osbs_obsolete_vr}
%{?python_provide:%python_provide python3-osbs-client}

%description -n python3-osbs-client
It is able to query OpenShift v3 for various stuff related to building images.
It can initiate builds, list builds, get info about builds, get build logs...
This package contains osbs Python 3 bindings.


%prep
%autosetup -n %{name}-%{commit}

# Remove this test, it tries to hit httpbin.org which fails the build in koji
rm -f tests/test_http.py

%build
%py3_build


%install
%py3_install


%if 0%{?with_check}
%check
py.test-3 -vv tests
%endif # with_check


%files
%doc README.md
%{_bindir}/osbs


%files -n python3-osbs-client
%doc README.md
%{!?_licensedir:%global license %doc}
%license LICENSE
%{_bindir}/osbs
%{python3_sitelib}/osbs*
%dir %{_datadir}/osbs
%{_datadir}/osbs/*.json


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.15.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.15.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.15.0-3
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.15.0-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.15.0-3
- Rebuilt for Python 3.13

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.15.0-3
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.15.0-2
- Rebuilt for Python 3.11

* Wed Jan 19 2022 Clement Verna <cverna@fedoraproject.org> - 1.15.0-1
- Update to latest upstream

* Wed Aug 25 2021 Clement Verna <cverna@fedoraproject.org> - 1.11.0-1
- Update to latest upstream
- Add upstream patch to fix tests using git

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.0-2
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.0-2
- Rebuilt for Python 3.10

* Thu Mar 04 2021 Clement Verna <cverna@fedoraproject.org> - 1.7.0-1
- Update to latest upstream
- New dependency for python-jsonschema

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.62-1
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Clement Verna <cverna@fedoraproject.org> - 0.62-1
- Update to latest upstream

* Tue Dec 10 2019 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.59.2-1
- rebuilt

* Wed Nov 13 2019 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.59.2-1
- rebuilt

* Wed Nov 13 2019 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.59.2-1
- rebuilt

* Thu Oct 17 2019 Clement Verna <cverna@fedoraproject.org> - 0.59.2-1
- Update to latest upstream

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.54-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.54-1
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Athos Ribeiro <athoscr@fedoraproject.org> - 0.54-1
- Update to latest upstream

* Wed Mar 20 2019 Athos Ribeiro <athoscr@fedoraproject.org> - 0.53-1
- Update to latest upstream
- Re-enable test suite

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Clement Verna <cverna@fedoraproject.org> - 0.52-1
- Update to latest upstream

* Mon Oct 22 2018 Miro Hrončok <mhroncok@redhat.com> - 0.49-1
- Drop Python 2 subpackage and Python versioned executables (#1640583)

* Mon Jul 30 2018 Clement Verna <cverna@fedoraproject.org> - 0.49-1
- New upstrean Release 0.49

* Mon Jul 23 2018 Clement Verna <cverna@fedoraproject.org> - 0.48-2
- Add missing PyYAML dependency

* Wed Jul 18 2018 Clement Verna <cverna@fedoraproject.org> - 0.48-1
- new upstream release 0.48

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.47-2
- Rebuilt for Python 3.7

* Tue May 15 2018 Clement Verna <cverna@fedoraproject.org> - 0.47-1
- new upstream release: 0.47

* Thu Mar 01 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.45-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Clement Verna <cverna@fedoraproject.org> - 0.45-1
- Update to latest upstream

* Thu Aug 24 2017 Adam Miller <maxamillion@gmail.com> - 0.41-1
- Update to latest upstream

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.39.1-3
- Python 2 binary package renamed to python2-osbs-client
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 09 2017 Adam Miller <maxamillion@fedoraproject.org> - 0.39.1-1
- Update to latest upstream

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.33-4
- Rebuild for Python 3.6

* Thu Dec 15 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.33-3
- Update patch for site specific customizations to be in line with upstream
- Add cancel-build patch

* Fri Dec 02 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.33-2
- Patch for koji krb5
- Patch for site specific customizations

* Tue Nov 29 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.33-1
- Update to latest upstream

* Thu Oct 13 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.32-1
- Update to latest upstream

* Thu Sep 22 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.31-3
- Update python-requests patch to handle python3 bytestrings properly

* Thu Sep 22 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.31-2
- Fix python3 requires

* Thu Sep 22 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.31-1
- Update to latest upstream

* Thu Sep 22 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.30-3
- Handle new Requires/BuildRequires for epel/f23 and older as well as f24+

* Wed Sep 21 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.30-2
- Apply patch from puiterwijk to switch to python-requests from pycurl

* Tue Sep 20 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.30-1
- new upstream release: 0.30

* Tue Sep 06 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.29-1
- new upstream release: 0.29

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 23 2016 Martin Milata <mmilata@redhat.com> - 0.24-1
- new upstream release: 0.24

* Wed May 11 2016 Martin Milata <mmilata@redhat.com> - 0.23-1
- new upstream release: 0.23

* Mon Apr 25 2016 Martin Milata <mmilata@redhat.com> - 0.22-1
- new upstream release: 0.22

* Wed Apr 20 2016 Martin Milata <mmilata@redhat.com> - 0.21-1
- new upstream release: 0.21

* Mon Apr 11 2016 Martin Milata <mmilata@redhat.com> - 0.20-1
- new upstream release: 0.20

* Thu Apr 07 2016 Martin Milata <mmilata@redhat.com> - 0.19-1
- new upstream release: 0.19

* Thu Mar 10 2016 Martin Milata <mmilata@redhat.com> - 0.18-1
- new upstream release: 0.18

* Fri Feb 12 2016 Martin Milata <mmilata@redhat.com> - 0.17-2
- new upstream release: 0.17

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Martin Milata <mmilata@redhat.com> - 0.16-1
- new upstream release: 0.16

* Fri Nov 20 2015 Jiri Popelka <jpopelka@redhat.com> - 0.15-4
- use py_build & py_install macros
- use python_provide macro
- do not use py3dir
- ship executables per packaging guidelines

* Fri Nov 13 2015 Jiri Popelka <jpopelka@redhat.com> - 0.15-3
- rebuilt for Python3.5

* Thu Nov 05 2015 Jiri Popelka <jpopelka@redhat.com> - 0.15-2
- build for Python 3
- %%check section

* Mon Oct 19 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.15-1
- new upstream release: 0.15

* Thu Aug 06 2015 bkabrda <bkabrda@redhat.com> - 0.14-2
- renamed to osbs-client

* Wed Jul 01 2015 Martin Milata <mmilata@redhat.com> - 0.14-1
- new upstream release: 0.14

* Fri Jun 12 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.13.1-1
- new fixup upstream release: 0.13.1

* Fri Jun 12 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.13-1
- new upstream release: 0.13

* Wed Jun 10 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.12-1
- new upstream release: 0.12

* Wed Jun 03 2015 Martin Milata <mmilata@redhat.com> - 0.11-1
- new upstream release: 0.11

* Thu May 28 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.10-1
- new upstream release: 0.10

* Thu May 28 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.9-1
- new upstream release: 0.9

* Mon May 25 2015 Jiri Popelka <jpopelka@redhat.com> - 0.8-1
- new upstream release: 0.8

* Fri May 22 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.7-1
- new upstream release: 0.7

* Thu May 21 2015 Jiri Popelka <jpopelka@redhat.com> - 0.6-2
- fix %%license handling

* Thu May 21 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.6-1
- new upstream release: 0.6

* Tue May 19 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.5-1
- new upstream release: 0.5

* Tue May 12 2015 Slavek Kabrda <bkabrda@redhat.com> - 0.4-2
- Introduce python-osbs subpackage
- move /usr/bin/osbs to /usr/bin/osbs2, /usr/bin/osbs is now a symlink
- depend on python[3]-setuptools because of entrypoints usage

* Tue Apr 21 2015 Martin Milata <mmilata@redhat.com> - 0.4-1
- new upstream release

* Wed Apr 15 2015 Martin Milata <mmilata@redhat.com> - 0.3-1
- new upstream release

* Wed Apr 08 2015 Martin Milata <mmilata@redhat.com> - 0.2-2.c1216ba
- update to c1216ba

* Tue Apr 07 2015 Tomas Tomecek <ttomecek@redhat.com> - 0.2-1
- new upstream release

* Tue Mar 24 2015 Jiri Popelka <jpopelka@redhat.com> - 0.1-4
- update to 758648c8

* Thu Mar 19 2015 Jiri Popelka <jpopelka@redhat.com> - 0.1-3
- no need to require also python-requests

* Thu Mar 19 2015 Jiri Popelka <jpopelka@redhat.com> - 0.1-2
- separate executable for python 3

* Wed Mar 18 2015 Jiri Popelka <jpopelka@redhat.com> - 0.1-1
- initial spec
