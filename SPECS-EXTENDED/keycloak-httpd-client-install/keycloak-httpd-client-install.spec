Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname keycloak-httpd-client-install
%global summary Tools to configure Apache HTTPD as Keycloak client


Name:           %{srcname}
Version:        1.3
Release:        2%{?dist}
Summary:        %{summary}

License:        GPL-3.0-or-later
URL:            https://github.com/latchset/keycloak-httpd-client-install
Source0:        https://github.com/latchset/keycloak-httpd-client-install/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  (python3-setuptools if python3-devel >= 3.12)

Requires:       %{_bindir}/keycloak-httpd-client-install

%description
Keycloak is a federated Identity Provider (IdP). Apache HTTPD supports
a variety of authentication modules which can be configured to utilize
a Keycloak IdP to perform authentication. This package contains
libraries and tools which can automate and simplify configuring an
Apache HTTPD authentication module and registering as a client of a
Keycloak IdP.

%package -n python3-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python3-requests
Requires:       python3-requests-oauthlib
Requires:       python3-jinja2
Requires:       python3-lxml

%description -n python3-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%py3_build

%install
%py3_install

install -d -m 755 %{buildroot}/%{_mandir}/man8
install -c -m 644 doc/keycloak-httpd-client-install.8 %{buildroot}/%{_mandir}/man8

%files
%license LICENSE.txt
%doc README.md doc/ChangeLog
%{_datadir}/%{srcname}/

%files -n python3-%{srcname}
%{python3_sitelib}/*
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*

%changelog
* Tue Mar 11 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.3-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Fri Sep 13 2024 Tomas Halman <thalman@redhat.com> - 1.3-1
- Rebase to version 1.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.1-22
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 4 2023 Tomas Halman <thalman@redhat.com> - 1.1-19
- Resolves: rhbz#2115262 keycloak-httpd-client-install missing dependency to python-lxml

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.1-17
- Rebuilt for Python 3.12

* Tue Mar 7 2023 Tomas Halman <thalman@redhat.com> - 1.1-16
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 4 2023 keycloak-httpd-client-install fails to build with Python 3.12 - 1.1.14
- Resolves: rhbz#2155009 - keycloak-httpd-client-install fails to build with
  Python 3.12: ModuleNotFoundError: No module named 'distutils'

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1-12
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1-9
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1-6
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Jakub Hrozek <jhrozek@redhat.com> - 1.1-1
- New upstream release 1.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 29 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8-8
- Remove python2 subpackage from Fedora 30+ (#1627398)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018  <jdennis@redhat.com> - 0.8-6
- Restore use of bcond for python conditionals

* Mon Jul  9 2018  <jdennis@redhat.com> - 0.8-5
- Share same spec file with RHEL

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8-4
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.8-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 10 2018 John Dennis <jdennis@redhat.com> - 0.8-1
- Upgrade to upstream 0,8, includes:
- CVE-2017-15112 unsafe use of -p/--admin-password on command line
- CVE-2017-15111 unsafe /tmp log file in --log-file option in keycloak_cli.py

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar  1 2017 John Dennis <jdennis@redhat.com> - 0.6-1
- Resolves: rhbz#1427720, if --mellon-root is not supplied and defaults to /
  you end up with double slashes in entityId and endpoints
- add --tls-verify option to control python-requests behavor when
  using tls to connect. With this option you can use a self-signed
  cert or point to a CA bundle.
- Fix warnings and checks when using client originate method
  'registration' with 'anonymous' authentication.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan  6 2017 John Dennis <jdennis@redhat.com> - 0.5-1
- Fix default port bug
  Strip the port from the URL if it matches the scheme (e.g. 80 for
  http and 443 for https)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 27 2016 John Dennis <jdennis@redhat.com> - 0.4-1
- new upstream
  See ChangeLog for details

* Fri May 20 2016 John Dennis <jdennis@redhat.com> - 0.3-1
- new upstream
  See ChangeLog for details

* Tue May 17 2016 John Dennis <jdennis@redhat.com> - 0.2-1
- new upstream
- Add keycloak-httpd-client-install.8 man page

* Fri May 13 2016 John Dennis <jdennis@redhat.com> - 0.1-1
- Initial version
