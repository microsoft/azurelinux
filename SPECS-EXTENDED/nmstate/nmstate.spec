%?python_enable_dependency_generator
%define srcname nmstate
%define libname libnmstate

Name:           nmstate
Version:        0.3.3
Release:        3%{?dist}
Summary:        Declarative network manager API
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/%{srcname}/%{srcname}
Source0:        %{url}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz.asc
Source2:        nmstate.gpg
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  gnupg2
Requires:       python3-setuptools
Requires:       python3-%{libname} = {version}-%{release}

%description
Nmstate is a library with an accompanying command line tool that manages host
networking settings in a declarative manner and aimed to satisfy enterprise
needs to manage host networking through a northbound declarative API and multi
provider support on the southbound.


%package -n python3-%{libname}
Summary:        nmstate Python 3 API library
Requires:       NetworkManager-libnm >= 1.22.10
# Use Recommends for NetworkManager because only access to NM DBus is required,
# but NM could be running on a different host
Recommends:     NetworkManager
# Avoid automatically generated profiles
Recommends:     NetworkManager-config-server
# Use Suggests for NetworkManager-ovs and NetworkManager-team since it is only
# required for OVS and team support
Suggests:       NetworkManager-ovs
Suggests:       NetworkManager-team

%package -n nmstate-plugin-ovsdb
Summary:        nmstate plugin for OVS database manipulation
Requires:       python3-%{libname} = %{version}-%{release}
# The python-openvswitch rpm pacakge is not in the same repo with nmstate,
# hence state it as Recommends, no requires.
Recommends:     python3dist(ovs)

%description -n python3-%{libname}
This package contains the Python 3 library for Nmstate.

%description -n nmstate-plugin-ovsdb
This package contains the nmstate plugin for OVS database manipulation.

%prep
gpg2 --import --import-options import-export,import-minimal %{SOURCE2} > ./gpgkey-mantainers.gpg
gpgv2 --keyring ./gpgkey-mantainers.gpg %{SOURCE1} %{SOURCE0}
%setup -q

%build
%py3_build

%install
%py3_install

%files
%doc README.md
%doc examples/
%{_mandir}/man8/nmstatectl.8*
%{python3_sitelib}/nmstatectl
%{_bindir}/nmstatectl

%files -n python3-%{libname}
%license LICENSE
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{srcname}-*.egg-info/
%exclude %{python3_sitelib}/%{libname}/plugins/nmstate_plugin_*
%exclude %{python3_sitelib}/%{libname}/plugins/__pycache__/nmstate_plugin_*

%files -n nmstate-plugin-ovsdb
%{python3_sitelib}/%{libname}/plugins/nmstate_plugin_ovsdb*
%{python3_sitelib}/%{libname}/plugins/__pycache__/nmstate_plugin_ovsdb*

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 0.3.3-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jul 02 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Thu Jun 25 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.3.2-3
- NetworkManager required version must match upstream required version.

* Thu Jun 25 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.3.2-2
- Fix required NetworkManager version.

* Tue Jun 16 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.3.2-1
- Update to 0.3.2
- Sync with upstream specfile

* Tue Jun 09 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Fri May 08 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.3.0-1
- Update to 0.3.0
- Sync with upstream specfile
- Update signature verification

* Tue Apr 21 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.10-1
- Update to 0.2.10

* Thu Mar 26 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.9-1
- Update to 0.2.9

* Fri Mar 13 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.8-1
- Update to 0.2.8

* Wed Mar 04 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.7-1
- Update to 0.2.7

* Mon Feb 24 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.6-1
- Update to 0.2.6

* Wed Feb 19 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.5-1
- Update to 0.2.5
- Sync with upstream specfile

* Wed Feb 12 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Wed Feb 05 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Tue Feb 04 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.2-1
- Update to 0.2.2
- Sync with upstream specfile

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.1-2
- Fix changelog

* Tue Jan 14 2020 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Tue Dec 03 2019 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.0-2
- Fix changelog

* Tue Dec 03 2019 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Mon Dec 02 2019 Till Maas <opensource@till.name> - 0.1.1-1
- Update to 0.1.1
- Sync with upstream specfile

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.8-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.8-2
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Gris Ge <fge@redhat.com> - 0.0.8-1
- Upgrade to 0.0.8.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Gris Ge <fge@redhat.com> - 0.0.7-2
- Workaround broken dbus-python packaging:
   https://bugzilla.redhat.com/show_bug.cgi?id=1654774

* Fri Jun 14 2019 Gris Ge <fge@redhat.com> - 0.0.7-1
- Upgrade to 0.0.7

* Sun May 05 2019 Gris Ge <fge@redhat.com> - 0.0.6-1
- Upgrade to 0.0.6

* Fri Apr 12 2019 Gris Ge <fge@redhat.com - 0.0.5-2
- Add missing runtime requirement: python3-dbus

* Tue Mar 12 2019 Gris Ge <fge@redhat.com> - 0.0.5-1
- Upgrade to 0.0.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Till Maas <opensource@till.name> - 0.0.4-2
- Sync with upstream spec
- Use Recommends for NetworkManager
- Add Suggests for NetworkManager-ovs
- package examples as doc

* Thu Jan 24 2019 Gris Ge <fge@redhat.com> - 0.0.4-1
- Upgrade to 0.0.4.

* Mon Jan 21 2019 Gris Ge <fge@redhat.com> - 0.0.3-3
- Add missing runtime dependency for nmstatectl.

* Wed Jan 02 2019 Gris Ge <fge@redhat.com> - 0.0.3-2
- Add source file PGP verification.

* Thu Dec 20 2018 Gris Ge <fge@redhat.com> - 0.0.3-1
- Upgrade to 0.0.3.

* Mon Dec 03 2018 Gris Ge <fge@redhat.com> - 0.0.2-2
- Trival RPM SPEC fix.

* Wed Nov 28 2018 Gris Ge <fge@redhat.com> - 0.0.2-1
- Initial release.
