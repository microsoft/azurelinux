%global srcname conda-package-handling
%global pkgname conda_package_handling
Summary:        Create and extract conda packages of various formats
Name:           python-%{srcname}
Version:        1.7.2
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/conda/conda-package-handling
Source0:        https://github.com/conda/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  libarchive-devel

%description
Create and extract conda packages of various formats.

%package -n python%{python3_pkgversion}-%{srcname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-Cython
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-tqdm
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-tqdm
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python%{python3_pkgversion}-%{srcname}
Create and extract conda packages of various formats.

%prep
%autosetup -n %{srcname}-%{version}
sed -i -e s/archive_and_deps/archive/ setup.py

%build
%py3_build

%install
%py3_install

%check
# test_secure_refusal_to_extract_abs_paths is not ready upstream
# https://github.com/conda/conda-package-handling/issues/59
# PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} -v tests -k 'not test_secure_refusal_to_extract_abs_paths'
pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    pytest>=5.4.0 \
    pytest-cov>=2.7.1 \
    pytest-mock
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v tests -k 'not test_secure_refusal_to_extract_abs_paths'


%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc AUTHORS.txt CHANGELOG.md README.md
%{_bindir}/cph
%{python3_sitelib}/%{pkgname}-*.egg-info/
%{python3_sitelib}/%{pkgname}/

%changelog
* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 1.7.2-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Oct 18 2020 Orion Poplawski <orion@nwra.com> - 1.7.2-1
- Update to 1.7.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Orion Poplawski <orion@nwra.com> - 1.7.0-3
- Add BR on python-setuptools

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-2
- Rebuilt for Python 3.9

* Thu May 07 2020 Orion Poplawski <orion@nwra.com> - 1.7.0-1
- Update to 1.7.0

* Thu May 07 2020 Orion Poplawski <orion@nwra.com> - 1.6.1-1
- Update to 1.6.1

* Sun Feb 2 2020 Orion Poplawski <orion@nwra.com> - 1.6.0-3
- Exclude failing test that is not ready upstream

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov  8 2019 Orion Poplawski <orion@nwra.com> - 1.6.0-1
- Update to 1.6.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-2
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Orion Poplawski <orion@nwra.com> - 1.4.1-1
- Update to 1.4.1
- Enable python dependency generator

* Mon Jul 29 2019 Orion Poplawski <orion@nwra.com> - 1.3.11-1
- Update to 1.3.11

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Orion Poplawski <orion@nwra.com> - 1.3.1-1
- Update to 1.3.1

* Sat May 18 2019 Orion Poplawski <orion@nwra.com> - 1.1.1-1
- Initial Fedora package
