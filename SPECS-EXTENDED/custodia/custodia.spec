Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# Enable python3 build by default
%bcond_without python3

# Disable python2 build by default
%bcond_with python2


%{!?python3_pkgversion:%global python3_pkgversion 3}

Name:           custodia
Version:        0.6.0
Release:        13%{?dist}
Summary:        A service to manage, retrieve and store secrets for other processes

License:        GPLv3+
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source2:        custodia.conf
Source3:        custodia@.service
Source4:        custodia@.socket
Source5:        custodia.tmpfiles.conf

Patch1:         nonfatal_deprecation.patch
Patch2:         0001-Replace-use-of-pytest-get_marker.patch

BuildArch:      noarch

BuildRequires:      systemd

%if 0%{?with_python2}
BuildRequires:      python2-devel
BuildRequires:      python2-jwcrypto >= 0.4.2
BuildRequires:      python2-requests
BuildRequires:      python2-setuptools >= 18
BuildRequires:      python2-coverage
BuildRequires:      python2-pytest
BuildRequires:      python2-docutils
BuildRequires:      python2-configparser
BuildRequires:      python2-systemd
BuildRequires:      tox >= 2.3.1
%endif

%if 0%{?with_python3}
BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      python%{python3_pkgversion}-jwcrypto >= 0.4.2
BuildRequires:      python%{python3_pkgversion}-requests
BuildRequires:      python%{python3_pkgversion}-setuptools > 18
BuildRequires:      python%{python3_pkgversion}-coverage
BuildRequires:      python%{python3_pkgversion}-pytest
BuildRequires:      python%{python3_pkgversion}-docutils
BuildRequires:      python%{python3_pkgversion}-systemd
%endif

%if 0%{?with_python3}
Requires:           python%{python3_pkgversion}-custodia = %{version}-%{release}
%else
Requires:           python2-custodia = %{version}-%{release}
%endif

Requires(preun):    systemd-units
Requires(postun):   systemd-units
Requires(post):     systemd-units


%global overview                                                           \
Custodia is a Secrets Service Provider, it stores or proxies access to     \
keys, password, and secret material in general. Custodia is built to       \
use the HTTP protocol and a RESTful API as an IPC mechanism over a local   \
Unix Socket. It can also be exposed to a network via a Reverse Proxy       \
service assuming proper authentication and header validation is            \
implemented in the Proxy.                                                  \
                                                                           \
Custodia is modular, the configuration file controls how authentication,   \
authorization, storage and API plugins are combined and exposed.


%description
A service to manage, retrieve and store secrets for other processes

%{overview}

%if 0%{?with_python2}
%package -n python2-custodia
Summary:    Sub-package with python2 custodia modules
%{?python_provide:%python_provide python2-%{name}}
Requires:   python2-configparser
Requires:   python2-jwcrypto >= 0.4.2
Requires:   python2-requests
Requires:   python2-setuptools
Requires:   python2-systemd
Conflicts:  python2-custodia-extra < %{version}

%description -n python2-custodia
Sub-package with python custodia modules

%{overview}
%endif

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-custodia
Summary:    Sub-package with python3 custodia modules
%{?python_provide:%python_provide python3-%{name}}
Requires:   python%{python3_pkgversion}-jwcrypto >= 0.4.2
Requires:   python%{python3_pkgversion}-requests
Requires:   python%{python3_pkgversion}-setuptools
Requires:   python%{python3_pkgversion}-systemd
Conflicts:  python%{python3_pkgversion}-custodia-extra < %{version}

%description -n python%{python3_pkgversion}-custodia
Sub-package with python custodia modules

%{overview}

%endif  # with_python3


%prep
%autosetup -p1


%build
%if 0%{?with_python2}
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif


%check
# don't download packages
export PIP_INDEX_URL=https://host.invalid./
# Don't try to download dnspython3. The package is provided by python%{python3_pkgversion}-dns
export PIP_NO_DEPS=yes
# Ignore all install packages to enforce installation of sdist. Otherwise tox
# may pick up this package from global site-packages instead of source dist.
export PIP_IGNORE_INSTALLED=yes

%if 0%{?with_python2}
tox --sitepackages -e py%{python2_version_nodots} -- --skip-servertests
%endif

%if 0%{?with_python3}
# Test custodia in a virtual environment
%{__python3} -m venv --system-site-packages testenv
testenv/bin/pip install .
testenv/bin/python -m pytest --capture=no --strict --skip-servertests
%endif


%install
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_mandir}/man7
mkdir -p %{buildroot}/%{_defaultdocdir}/custodia
mkdir -p %{buildroot}/%{_defaultdocdir}/custodia/examples
mkdir -p %{buildroot}/%{_sysconfdir}/custodia
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_tmpfilesdir}
mkdir -p %{buildroot}/%{_localstatedir}/lib/custodia
mkdir -p %{buildroot}/%{_localstatedir}/log/custodia
mkdir -p %{buildroot}/%{_localstatedir}/run/custodia

%if 0%{?with_python2}
%py2_install
mv %{buildroot}/%{_bindir}/custodia %{buildroot}/%{_sbindir}/custodia
cp %{buildroot}/%{_sbindir}/custodia %{buildroot}/%{_sbindir}/custodia-2
cp %{buildroot}/%{_bindir}/custodia-cli %{buildroot}/%{_bindir}/custodia-cli-2
%endif

%if 0%{?with_python3}
# overrides /usr/bin/custodia-cli and /usr/sbin/custodia with Python 3 shebang
%py3_install
mv %{buildroot}/%{_bindir}/custodia %{buildroot}/%{_sbindir}/custodia
cp %{buildroot}/%{_sbindir}/custodia %{buildroot}/%{_sbindir}/custodia-3
cp %{buildroot}/%{_bindir}/custodia-cli %{buildroot}/%{_bindir}/custodia-cli-3
%endif

install -m 644 -t "%{buildroot}/%{_mandir}/man7" man/custodia.7
install -m 644 -t "%{buildroot}/%{_defaultdocdir}/custodia" README API.md
install -m 644 -t "%{buildroot}/%{_defaultdocdir}/custodia/examples" custodia.conf
install -m 600 %{SOURCE2} %{buildroot}%{_sysconfdir}/custodia
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/custodia.conf



%pre
getent group custodia >/dev/null || groupadd -r custodia
getent passwd custodia >/dev/null || \
    useradd -r -g custodia -d / -s /usr/sbin/nologin \
    -c "User for custodia" custodia
exit 0


%post
%systemd_post custodia@\*.socket
%systemd_post custodia@\*.service


%preun
%systemd_preun custodia@\*.socket
%systemd_preun custodia@\*.service


%postun
%systemd_postun custodia@\*.socket
%systemd_postun custodia@\*.service


%files
%doc README API.md
%doc %{_defaultdocdir}/custodia/examples/custodia.conf
%license LICENSE
%{_mandir}/man7/custodia*
%{_sbindir}/custodia
%{_bindir}/custodia-cli
%dir %attr(0700,custodia,custodia) %{_sysconfdir}/custodia
%config(noreplace) %attr(600,custodia,custodia) %{_sysconfdir}/custodia/custodia.conf
%attr(644,root,root)  %{_unitdir}/custodia@.socket
%attr(644,root,root)  %{_unitdir}/custodia@.service
%dir %attr(0700,custodia,custodia) %{_localstatedir}/lib/custodia
%dir %attr(0700,custodia,custodia) %{_localstatedir}/log/custodia
%dir %attr(0755,custodia,custodia) %{_localstatedir}/run/custodia
%{_tmpfilesdir}/custodia.conf

%if 0%{?with_python2}
%files -n python2-custodia
%license LICENSE
%{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/%{name}-%{version}-py%{python2_version}-nspkg.pth
%{_sbindir}/custodia-2
%{_bindir}/custodia-cli-2
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-custodia
%license LICENSE
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}-nspkg.pth
%{_sbindir}/custodia-3
%{_bindir}/custodia-cli-3

%endif  # with_python3


%changelog
* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-13
- Making binaries paths compatible with CBL-Mariner's paths.

* Fri Mar 05 2021 Henry Li <lihl@microsoft.com> - 0.6.0-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix distro check to enable python3 build and disable python2 build

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-9
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Simo Sorce <simo@fedoraproject.org> - 0.6.0-7
- Add patch to deal with pytest4 upgrade in future fedora

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-5
- Drop Python 2 package from Fedora 30+

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Christian Heimes <cheimes@redhat.com> - 0.6.0-3
- Don't turn deprecation warnings into fatal errors

* Thu Jun 28 2018 Christian Heimes <cheimes@redhat.com> - 0.6.0-2
- Rebuild for Python 3.7

* Mon Jun 25 2018 Christian Heimes <cheimes@redhat.com> - 0.6.0-1
- New upstream release 0.6.0
- Remove etcd support
- Remove unnecesary conflict with old FreeIPA
- Make Python 2 optional

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-13
- Rebuilt for Python 3.7

* Mon May 07 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-12
- Fix BuildRequires to require the tox command and not the python2 module

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.0-11
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 07 2017 Christian Heimes <cheimes@redhat.com> - 0.5.0-9
- freeipa 4.4.4-2.fc26 and newer are compatible with custodia 0.5
- Fix dependency to python2-jwcrypto >= 0.4.2

* Wed Aug 02 2017 Christian Heimes <cheimes@redhat.com> - 0.5.0-8
- Add PIP_IGNORE_INSTALLED

* Tue Aug 01 2017 Christian Heimes <cheimes@redhat.com> - 0.5.0-7
- Modernize spec

* Tue Aug 01 2017 Christian Heimes <cheimes@redhat.com> - 0.5.0-6
- Require latest python-jwcrypto with Python 3 fix
- Use python2 prefix for all Python 2 dependencies

* Tue Aug 01 2017 Christian Heimes <cheimes@redhat.com> - 0.5.0-5
- Add custodia user and named systemd instances

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Christian Heimes <cheimes@redhat.com> - 0.5.0-3
- Add systemd build requirement for tmpfilesdir and unitdir macros

* Mon Jun 19 2017 Christian Heimes <cheimes@redhat.com> - 0.5.0-2
- Skip etcd store on PPC64
- Add missing pre/post install hooks for systemd service
- Custodia 0.5 is compatible with FreeIPA 4.4.5 and newer
- Drop custodia user from tmpfiles.d conf

* Tue May 16 2017 Simo Sorce <simo@redhat.com> - 0.5.0-1
- New Custodia version
- Drop checks on sha512sum, these checks are already done by dist-git

* Tue Apr 11 2017 Christian Heimes <cheimes@redhat.com> - 0.3.1-3
- Run Python 3 tests with correct Python version

* Fri Apr 07 2017 Christian Heimes <cheimes@redhat.com> - 0.3.1-2
- Add conflict with FreeIPA < 4.5

* Mon Mar 27 2017 Christian Heimes <cheimes@redhat.com> - 0.3.1-1
- Upstream release 0.3.1

* Thu Mar 16 2017 Christian Heimes <cheimes@redhat.com> - 0.3.0-3
- Provide custodia-2 and custodia-3 scripts

* Thu Mar 02 2017 Christian Heimes <cheimes@redhat.com> - 0.3.0-2
- Run Custodia daemon with Python 3
- Resolves: Bug 1426737 - custodia: Provide a Python 3 subpackage

* Wed Mar 01 2017 Christian Heimes <cheimes@redhat.com> - 0.3.0-1
- Update to custodia 0.3.0
- Run tests with global site packages
- Add tmpfiles.d config for /run/custodia

* Wed Feb 22 2017 Christian Heimes <cheimes@redhat.com> - 0.2.0-4
- Add missing runtime requirement on python[23]-systemd.
- Drop unnecesary build dependency on python%%{python3_pkgversion}-configparser.
- Fix tests, don't try to download dnspython3.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-2
- Rebuild for Python 3.6

