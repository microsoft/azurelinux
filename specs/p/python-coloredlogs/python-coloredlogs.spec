# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname coloredlogs

Name:           python-%{srcname}
Version:        15.0.1
Release: 17%{?dist}
Summary:        Colored terminal output for Python's logging module

License:        MIT
URL:            https://%{srcname}.readthedocs.io
Source0:        https://github.com/xolox/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

# Replace pipes.quote with shlex.quote on Python 3
# https://github.com/xolox/python-coloredlogs/pull/120
#
# Fixes:
#
# Relies on the pipes module, removed from the standard library in Python 3.13
# https://github.com/xolox/python-coloredlogs/issues/119
Patch:          https://github.com/xolox/%{name}/pull/120.patch

BuildArch:      noarch

%description
The coloredlogs package enables colored terminal output for Python's logging
module. The ColoredFormatter class inherits from logging.Formatter and uses
ANSI escape sequences to render your logging messages in color. It uses only
standard colors so it should work on any UNIX terminal.


%package doc
Summary:        Documentation for the '%{srcname}' Python module
BuildRequires:  python%{python3_pkgversion}-sphinx

%description doc
HTML documentation for the '%{srcname}' Python module.


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  /usr/bin/script
BuildRequires:  python%{python3_pkgversion}-capturer >= 2.4
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-verboselogs >= 1.7

%if !0%{?rhel} || 0%{?rhel} >= 8
Suggests:       %{name}-doc = %{version}-%{release}
%endif

%description -n python%{python3_pkgversion}-%{srcname}
The coloredlogs package enables colored terminal output for Python's logging
module. The ColoredFormatter class inherits from logging.Formatter and uses
ANSI escape sequences to render your logging messages in color. It uses only
standard colors so it should work on any UNIX terminal.


%prep
%autosetup -p1

# Don't install tests.py
mv %{srcname}/tests.py ./tests.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

sphinx-build-%{python3_version} -nb html -d docs/build/doctrees docs docs/build/html
rm docs/build/html/.buildinfo


%install
%pyproject_install
%pyproject_save_files -l %{srcname}


%check
# Some hacking to get the pth file to get processed outside
# of the build host's site dir. This sitecustomize.py needs
# to be somewhere in the path.
mkdir -p fakesite
echo "import site; site.addsitedir(site.USER_SITE)" > fakesite/sitecustomize.py

PATH=%{buildroot}%{_bindir}:$PATH \
    PYTHONPATH=$PWD/fakesite \
    PYTHONUSERBASE=%{buildroot}%{_prefix} \
    PYTHONUNBUFFERED=1 \
    py.test-%{python3_version} \
    tests.py


%files doc
%license LICENSE.txt
%doc docs/build/html

%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%doc CHANGELOG.rst README.rst
%{python3_sitelib}/%{srcname}.pth
%{_bindir}/%{srcname}


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 15.0.1-16
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 15.0.1-15
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 19 2025 Python Maint <python-maint@redhat.com> - 15.0.1-13
- Rebuilt for Python 3.14

* Fri Jul 18 2025 Scott K Logan <logans@cottsay.net> - 15.0.1-12
- Add missing BuildRequires: /usr/bin/script (rhbz#2341136)
- Switch to pyproject build macros (rhbz#2377563)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 15.0.1-9
- Rebuilt for Python 3.13 (close RHBZ#2291652)
- Applied a simple patch for 'pipes' module removal in Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 15.0.1-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 15.0.1-2
- Rebuilt for Python 3.11

* Wed Apr 27 2022 Scott K Logan <logans@cottsay.net> - 15.0.1-1
- Update to 15.0.1 (rhbz#1906418)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 14.0-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 14.0-2
- Rebuilt for Python 3.9

* Wed Apr 15 2020 Scott K Logan <logans@cottsay.net> - 14.0-1
- Update to 14.0 (rhbz#1803324)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 10.0-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 10.0-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Scott K Logan <logans@cottsay.net> - 10.0-7
- Drop python2 and python3_other
- Deselect plain_text test on Python >= 3.7 (xolox/python-coloredlogs#66)

* Fri Oct 26 2018 Scott K Logan <logans@cottsay.net> - 10.0-6
- Pattern conformance

* Fri Sep 28 2018 Scott K Logan <logans@cottsay.net> - 10.0-5
- Disable python2 for Fedora 30+
- Better conditionals in spec
- Enable tests

* Fri Sep 21 2018 Scott K Logan <logans@cottsay.net> - 10.0-4
- Enable both python34 and python36 for EPEL

* Fri Sep 21 2018 Scott K Logan <logans@cottsay.net> - 10.0-3
- Add missing setuptools BR for EPEL

* Fri Sep 21 2018 Scott K Logan <logans@cottsay.net> - 10.0-2
- Enable python34 builds for EPEL

* Thu Sep 20 2018 Scott K Logan <logans@cottsay.net> - 10.0-1
- Initial package
