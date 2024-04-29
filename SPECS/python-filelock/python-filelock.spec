%global srcname filelock
Summary:        A platform independent file lock
Name:           python-filelock
Version:        3.13.4
Release:        1%{?dist}
License:        Unlicense
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/toxdev/filelock
Source0:        https://github.com/toxdev/%{srcname}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%package doc
Summary:        Documentation for %{srcname}, %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx-theme-alabaster

%description doc
%{summary}

%package -n python%{python3_pkgversion}-%{srcname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-hatchling
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx-theme-alabaster

%description -n python%{python3_pkgversion}-%{srcname}
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

pushd docs
PYTHONPATH=../src sphinx-build ./ html --color -b html -d doctrees
rm html/.buildinfo
popd

%install
%pyproject_install
%pyproject_save_files -l %{srcname}

%check
%if %{with tests}
%pytest
%else
%pyproject_check_import
%endif

%files doc
%license LICENSE
%doc docs/build/html

%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%doc README.md

%changelog
* Fri Apr 26 2024 Osama Esmail <osamaesmail@microsoft.com> - 3.13.4-1
- Lot of redoing to use pyproject
- Upgrading version for 3.0
- Using literal package name so autoupgrader can do its thing.
- Updating package folder name in %%autosetup

* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.12-13
- Updating source URL.

* Sun Feb 13 2022 Jon Slobodzian <joslobo@microsoft.com> - 3.0.12-12
- Add python-devel

* Wed Nov 17 2021 Andrew Phelps <anphel@microsoft.com> - 3.0.12-11
- Use make with single processor to mitigate intermittent build failures

* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 3.0.12-10
- Remove python2 support
- License verified

* Mon Dec 07 2020 Steve Laughman <steve.laughman@microsoft.com> - 3.0.12-9
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.12-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.12-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.12-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Scott K Logan <logans@cottsay.net> - 3.0.12-2
- Add explicit conflict between unlike python2/3 subpackages (rhbz#1708871)
- Make the -doc subpackage dependency weaker

* Sun May 19 2019 Scott K Logan <logans@cottsay.net> - 3.0.12-1
- Update to 3.0.12 (rhbz#1711583)
- Switch to Python 3 sphinx

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 16 2018 Scott K Logan <logans@cottsay.net> - 3.0.10-1
- Update to 3.0.10

* Tue Oct 30 2018 Scott K Logan <logans@cottsay.net> - 3.0.9-1
- Update to 3.0.9
- Add spec conditionals for python version targeting (rhbz#1632320)
- Fix theme package dependency (s/sphinx_rtd_theme/sphinx-theme-alabaster/)

* Fri Sep 14 2018 Scott K Logan <logans@cottsay.net> - 3.0.8-1
- Update to 3.0.8 (rhbz#1459712)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.8-6
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.8-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 04 2017 Scott K Logan <logans@cottsay.net> - 2.0.8-1
- Update to version 2.0.8

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.6-2
- Rebuild for Python 3.6

* Sun May 01 2016 Scott K Logan <logans@cottsay.net> - 2.0.6-1
- Initial package
