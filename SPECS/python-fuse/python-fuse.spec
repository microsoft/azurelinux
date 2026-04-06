# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname fusepy

Name:    python-fuse
# TODO rename to python-fusepy
Version: 3.0.1
Release: 5%{?dist}
Summary: Python module that provides a simple interface to FUSE and MacFUSE
License: ISC
URL: https://github.com/fusepy/fusepy
Source: %{pypi_source %{srcname}}
BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
fusepy is a Python module that provides a simple interface to FUSE and MacFUSE.
It's just one file and is implemented using ctypes.

%package -n python3-fusepy
Summary: %{summary}
%{?python_provide:%python_provide python3-fuse}
%{?python_provide:%python_provide python3-fusepy}
Provides: python3-fuse = %{version}-%{release}
Obsoletes: python3-fuse < 2.0.4-10
Requires: fuse-libs

%description -n python3-fusepy
fusepy is a Python module that provides a simple interface to FUSE and MacFUSE.
It's just one file and is implemented using ctypes.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-fusepy
%doc README.rst
%{python3_sitelib}/fuse.py
%{python3_sitelib}/fusepy-*egg-info/
%{python3_sitelib}/__pycache__

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.0.1-2
- Rebuilt for Python 3.14

* Wed Jan 29 2025 Juan Orti Alcaine <jortialc@redhat.com> - 3.0.1-1
- Update to new upstream repository
- Update to version 3.0.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.4-30
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.4-26
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.4-23
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.4-20
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 08 2020 Juan Orti Alcaine <jortialc@redhat.com> - 2.0.4-18
- BR: python3-setuptools

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-16
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-14
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-13
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 06 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-10
- Rename python3-fuse to python3-fusepy
- Drop python2-fuse, that is done by fuse-python SRPM

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-8
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-4
- Rebuild for Python 3.6

* Tue Nov 22 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 2.0.4-3
- Add fuse-libs dependency

* Mon Oct 17 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 2.0.4-2
- Remove unused commit and shortcommit variables
- Change Source0 to download %%{srcname}-%%{version}.tar.gz
- Reuse %%{summary} macro

* Sun Sep 4 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 2.0.4-1
- Initial RPM
