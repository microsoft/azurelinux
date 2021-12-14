Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname keycloak-httpd-client-install
%global summary Tools to configure Apache HTTPD as Keycloak client





  %bcond_with python2
  %bcond_without python3


Name:           %{srcname}
Version:        1.1
Release:        6%{?dist}
Summary:        %{summary}

%global git_tag RELEASE_%(r=%{version}; echo $r | tr '.' '_')

License:        GPLv3
URL:            https://github.com/jdennis/keycloak-httpd-client-install
Source0:        https://github.com/jdennis/keycloak-httpd-client-install/archive/%{git_tag}.tar.gz

BuildArch:      noarch

%if %{with python2}
BuildRequires:  python2-devel
%endif # with_python2

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

Requires:       %{_bindir}/keycloak-httpd-client-install

%description
Keycloak is a federated Identity Provider (IdP). Apache HTTPD supports
a variety of authentication modules which can be configured to utilize
a Keycloak IdP to perform authentication. This package contains
libraries and tools which can automate and simplify configuring an
Apache HTTPD authentication module and registering as a client of a
Keycloak IdP.

%if %{with python2}
%package -n python2-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python2-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python2-requests
Requires:       python2-requests-oauthlib
Requires:       python2-jinja2
Requires:       %{_bindir}/keycloak-httpd-client-install

%description -n python2-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.
%endif # with_python2

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python3-requests
Requires:       python3-requests-oauthlib
Requires:       python3-jinja2

%description -n python3-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%endif

%prep
%autosetup -n %{srcname}-%{git_tag} -p1

%build
%if %{with python2}
%py2_build
%endif # with_python2

%if 0%{?with_python3}
%py3_build
%endif

%install
%if %{with python2}
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%py2_install
%endif # with_python2

%if 0%{?with_python3}
# py3_install won't overwrite files if they have a timestamp greater-than
# or equal to the py2 installed files. If both the py2 and py3 builds execute
# quickly the files end up with the same timestamps thus leaving the py2
# version in the py3 install. Therefore remove any files susceptible to this.
%if %{with python2}
rm %{buildroot}%{_bindir}/keycloak-httpd-client-install
%endif # with_python2
%py3_install
%endif

install -d -m 755 %{buildroot}/%{_mandir}/man8
install -c -m 644 doc/keycloak-httpd-client-install.8 %{buildroot}/%{_mandir}/man8

%files
%license LICENSE.txt
%doc README.md doc/ChangeLog
%{_datadir}/%{srcname}/

%if %{with python2}
# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python2-%{srcname}
%{python2_sitelib}/*

%if ! 0%{?with_python3}
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*
%endif
%endif # with_python2

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{python3_sitelib}/*
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
