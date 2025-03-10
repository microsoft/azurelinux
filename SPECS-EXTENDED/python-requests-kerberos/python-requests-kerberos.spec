Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           python-requests-kerberos
Version:        0.14.0
Release:        6%{?dist}
Summary:        A Kerberos authentication handler for python-requests
License:        ISC
URL:            https://github.com/requests/requests-kerberos
# Upstream considers Github not PyPI to be the authoritative source tarballs:
# https://github.com/requests/requests-kerberos/pull/78
Source:         %{url}/archive/v%{version}/requests-kerberos-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(pytest)   
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3-requests

%global _description %{expand:
Requests is an HTTP library, written in Python, for human beings. This library
adds optional Kerberos/GSSAPI authentication support and supports mutual
authentication.}

%description %_description

%package -n python3-requests-kerberos
Summary:        %{summary}


%description -n python3-requests-kerberos %_description

%prep
%autosetup -n requests-kerberos-%{version}
# avoid unnecessary coverage dependency
sed -i '/pytest-cov/d' requirements-test.txt

%generate_buildrequires
%pyproject_buildrequires requirements-test.txt

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files requests_kerberos


%check
pip install pyspnego
%pytest -v tests


%files -n python3-requests-kerberos -f %{pyproject_files}
%doc README.rst AUTHORS HISTORY.rst

%changelog
* Thu Feb 12 2025 Sumit Jena <v-sumitjena@microsoft.com> - 0.14.0-6
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Thu Apr 28 2022 Muhammad Falak <mwani@microsoft.com> - 0.12.0-11
- Use `py.test` instead of `py.test-3` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12.0-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-8
- Subpackage python2-requests-kerberos has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Dan Callaghan <dcallagh@redhat.com> 0.12.0-1
- Upstream release 0.12.0:
  https://github.com/requests/requests-kerberos/blob/v0.12.0/HISTORY.rst#0120-2017-12-20

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 12 2016 Dan Callaghan <dcallagh@redhat.com> - 0.10.0-1
- upstream bug fix release 0.10.0:
  https://github.com/requests/requests-kerberos/blob/v0.10.0/HISTORY.rst#0100-2016-05-18

* Fri Jul 01 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-5
- add Obsoletes for python -> python2 rename

* Fri Jul 01 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-4
- build for Python 2 and 3 (RHBZ#1334415)
- use %%license
- run tests in %%check

* Thu Feb 11 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-3
- really fix requirements for kerberos module (#1305986)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-1
- upstream release 0.8.0 (#1296743)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dan Callaghan <dcallagh@redhat.com> - 0.7.0-2
- relaxed version in kerberos module requirement, to work with
  python-kerberos 1.1 (#1215565)

* Tue May 05 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0 (#1164464)

* Fri Nov 07 2014 Dan Callaghan <dcallagh@redhat.com> - 0.6-1
- fix for mutual authentication handling (RHBZ#1160545, CVE-2014-8650)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Dan Callaghan <dcallagh@redhat.com> - 0.5-1
- upstream bug fix release 0.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Dan Callaghan <dcallagh@redhat.com> - 0.3-1
- upstream bug fix release 0.3

* Mon May 27 2013 Dan Callaghan <dcallagh@redhat.com> - 0.2-2
- require requests >= 1.0

* Tue May 14 2013 Dan Callaghan <dcallagh@redhat.com> - 0.2-1
- initial version
