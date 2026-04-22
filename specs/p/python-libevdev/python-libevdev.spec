# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		python-libevdev
Version:	0.12
Release: 7%{?dist}
Summary:	Python bindings to the libevdev evdev device wrapper library

# SPDX
License:	MIT
URL:		https://pypi.python.org/pypi/libevdev/
Source0:	https://gitlab.freedesktop.org/libevdev/python-libevdev/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:	noarch

%description
%{name} provides the Python bindings to the libevdev evdev device
wrapper library. These bindings provide a pythonic API to access evdev
devices and create uinput devices.

%package -n	python3-libevdev
Summary:	Python bindings to the libevdev evdev device wrapper library

BuildRequires:	python3-devel
Requires:	libevdev

%{?python_provide:%python_provide python3-libevdev}

%description -n	python3-libevdev
%{name} provides the Python bindings to the libevdev evdev device
wrapper library. These bindings provide a pythonic API to access evdev
devices and create uinput devices.


%generate_buildrequires
%pyproject_buildrequires


%prep
%autosetup -n %{name}-%{version} -p1


%build
%pyproject_wheel


%install
%pyproject_install


%files -n	python3-libevdev
%license COPYING
%{python3_sitelib}/libevdev/
%{python3_sitelib}/libevdev-%{version}.dist-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.12-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.12-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Peter Hutterer <peter.hutterer@redhat.com> - 0.12-3
- Update python packaging macros (#2377854)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.12-2
- Rebuilt for Python 3.14

* Thu May 29 2025 Peter Hutterer <peter.hutterer@redhat.com> - 0.12-1
- python-libevdev 0.12

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.11-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 05 2023 Peter Hutterer <peter.hutterer@redhat.com>
- SPDX migration: mark license as SPDX compatible

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.11-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.11-2
- Rebuilt for Python 3.11

* Mon May 30 2022 Peter Hutterer <peter.hutterer@redhat.com> - 0.11-1
- python-libevdev 0.11

* Thu Feb 10 2022 Peter Hutterer <peter.hutterer@redhat.com> - 0.10-1
- python-libevdev 0.10

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Peter Hutterer <peter.hutterer@redhat.com> 0.9-1
- python-libevdev 0.9

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.8-1
- python-libevdev 0.8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.7-1
- python-libevdev 0.7

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.6.1-1
- python-libevdev 0.6.1

* Tue Sep 11 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.5-4
- Update URLs for gitlab

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5-2
- Rebuilt for Python 3.7

* Tue Apr 24 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.5-1
- python-libevdev 0.5

* Thu Apr 19 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.4-2
- Fix failure when setting up EV_REP

* Mon Feb 26 2018 Peter Hutterer <peter.hutterer@redhat.com>- 0.4-1
- initial import (#1549003)

