Vendor:         Microsoft Corporation
Distribution:   Mariner
%global modname dbusmock

Name:             python-%{modname}
Version:          0.18.3
Release:          4%{?dist}
Summary:          Mock D-Bus objects

License:          LGPLv3+
URL:              https://pypi.python.org/pypi/python-dbusmock
Source0:          https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
# From https://github.com/martinpitt/python-dbusmock/pull/54
Patch0:           0001-Add-mock-server-for-low-memory-monitor.patch

BuildArch:        noarch
BuildRequires:    git
BuildRequires:    python3-dbus
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-nose
BuildRequires:    python3-gobject
BuildRequires:    dbus-x11
BuildRequires:    upower

%global _description\
With this program/Python library you can easily create mock objects on\
D-Bus. This is useful for writing tests for software which talks to\
D-Bus services such as upower, systemd, ConsoleKit, gnome-session or\
others, and it is hard (or impossible without root privileges) to set\
the state of the real services to what you expect in your tests.

%description %_description

%package -n python3-dbusmock
Summary: %summary (Python3)
Requires:         python3-dbus, python3-gobject, dbus-x11
%description -n python3-dbusmock %_description

%prep
%autosetup -n %{name}-%{version} -S git
rm -rf python-%{modname}.egg-info


%build
%py3_build

%install
%py3_install

%check
# Tests are disabled for now
%{__python3} setup.py test

%files -n python3-dbusmock
%doc README.rst COPYING
%{python3_sitelib}/*%{modname}*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.3-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Bastien Nocera <bnocera@redhat.com> - 0.18.3-2
+ python-dbusmock-0.18.3-2
- Add low-memory-monitor mock

* Thu Nov 14 2019 Bastien Nocera <bnocera@redhat.com> - 0.18.3-1
+ python-dbusmock-0.18.3-1
- Update to 0.18.3
- Enable tests

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.17-11
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.17-10
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Miro Hrončok <mhroncok@redhat.com> - 0.17-8
- Subpackage python2-dbusmock has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.17-5
- Rebuilt for Python 3.7

* Fri Mar 30 2018 Bastien Nocera <bnocera@redhat.com> - 0.17-4
+ python-dbusmock-0.17-4
- Patch from Benjamin Berg to correct the python3 subpackage deps
  and summary

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.17-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Bastien Nocera <bnocera@redhat.com> - 0.17-1
- Update to 0.17
- Update source URL

* Tue Oct 17 2017 Bastien Nocera <bnocera@redhat.com> - 0.16.9-1
+ python--0.16.9-1
- Update to 0.16.9

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.16.7-4
- Python 2 binary package renamed to python2-dbusmock
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Bastien Nocera <bnocera@redhat.com> - 0.16.7-1
+ python-dbusmock-0.16.7-1
- Update to 0.16.7

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.11.1-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 08 2014 Matěj Cepl <mcepl@redhat.com> - 0.11.1-1
- Update to 0.11.1

* Thu Jul 17 2014 Bastien Nocera <bnocera@redhat.com> 0.10.3-2
- Add Python3 sub-package

* Thu Jul 17 2014 Bastien Nocera <bnocera@redhat.com> 0.10.3-1
- Update to 0.10.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 12 2013 Bastien Nocera <bnocera@redhat.com> 0.8.1-1
- Update to 0.8.1

* Fri Nov 08 2013 Bastien Nocera <bnocera@redhat.com> 0.8-1
- Update to 0.8

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Bastien Nocera <bnocera@redhat.com> 0.6.3-1
- Update to 0.6.3

* Thu Jun 13 2013 Bastien Nocera <bnocera@redhat.com> 0.6.2-1
- Update to 0.6.2

* Wed Jun 12 2013 Bastien Nocera <bnocera@redhat.com> 0.6-1
- Update to 0.6.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Bastien Nocera <bnocera@redhat.com> 0.4.0-1
- Update to 0.4.0

* Mon Jan 07 2013 Bastien Nocera <bnocera@redhat.com> 0.3.1-1
- Update to 0.3.1

* Wed Dec 19 2012 Matěj Cepl <mcepl@redhat.com> - 0.3-1
- New upstream release.

* Mon Oct 08 2012 Matěj Cepl <mcepl@redhat.com> - 0.1.1-2
- remove the bundled egg-info following the package review.

* Fri Oct 05 2012 Matěj Cepl <mcepl@redhat.com> - 0.1.1-1
- This version should actually work

* Tue Oct 02 2012 Matěj Cepl <mcepl@redhat.com> 0.0.3-1
- initial package for Fedora
