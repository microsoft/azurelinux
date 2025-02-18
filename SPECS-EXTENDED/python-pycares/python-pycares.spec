# set upstream name variable
%global srcname pycares


Name:           python-pycares
Version:        4.3.0
Release:        9%{?dist}
Summary:        Python interface for c-ares

License:        MIT
URL:            https://github.com/saghul/pycares
Source0:        https://github.com/saghul/%{srcname}/archive/%{srcname}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  python3-cffi
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  c-ares-devel
# for docs
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
# for tests
#BuildRequires:  python3-pytest

%description
pycares is a Python module which provides an interface to
c-ares. c-ares is a C library that performs DNS requests and name
resolutions asynchronously.



%package     -n python3-%{srcname}
Summary:        Python interface for c-ares
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
pycares is a Python module which provides an interface to
c-ares. c-ares is a C library that performs DNS requests and name
resolutions asynchronously.



%package     -n python-%{srcname}-doc
Summary:        Documentation for python-pycares
BuildArch:      noarch
Requires:       python3-%{srcname} = %{version}-%{release}

%description -n python-%{srcname}-doc
pycares is a Python module which provides an interface to
c-ares. c-ares is a C library that performs DNS requests and name
resolutions asynchronously.

This package contains documentation in reST and HTML formats.



%prep
%autosetup -p1 -n %{srcname}-%{srcname}-%{version}


%build
export PYCARES_USE_SYSTEM_LIB=1
%py3_build

# Build sphinx documentation
pushd docs/
make html
popd # docs


%install
%py3_install

# Install html docs
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -pr docs/_build/html %{buildroot}%{_pkgdocdir}/

# Move sources
mv -f %{buildroot}%{_pkgdocdir}/html/_sources/ %{buildroot}%{_pkgdocdir}/rst/

# Remove buildinfo sphinx documentation
rm -rf %{buildroot}%{_pkgdocdir}/html/.buildinfo

# Fix non-standard modes (775)
chmod 755 %{buildroot}%{python3_sitearch}/%{srcname}/_cares.cpython-*.so


%check
# no tests to run with pytest: Disabling.



%files -n python3-%{srcname}
%license LICENSE
%doc README.rst ChangeLog
# For arch-specific packages: sitearch
%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/%{srcname}-%{version}-py%{python3_version}.egg-info/


%files -n python-%{srcname}-doc
%doc examples/
%{_pkgdocdir}/



%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.3.0-8
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.3.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 4.3.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 11 2022 Matthieu Saulnier <fantom@fedoraproject.org> - 4.3.0-1
- Update to 4.3.0

* Thu Sep 22 2022 Matthieu Saulnier <fantom@fedoraproject.org> - 4.2.2-1
- Update to 4.2.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.1.2-2
- Rebuilt for Python 3.11

* Wed Mar 9 2022 Matthieu Saulnier <fantom@fedoraproject.org> - 4.1.2-1
- Update to 4.1.2
- Fix Requires tag of the doc subpackage

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 30 2021 Matthieu Saulnier <fantom@fedoraproject.org> - 4.0.0-5
- Rebuild for CVE-2021-3672 in c-ares library

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 4.0.0-3
- Set PYCARES_USE_SYSTEM_LIB=1 (fix RHBZ#1965602)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.0-2
- Rebuilt for Python 3.10

* Fri May 14 2021 Matthieu Saulnier <fantom@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0
- Add new BuildRequires (c-ares-devel)

* Tue May 11 2021 Matthieu Saulnier <fantom@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0
- Use pytest to run tests suite
- Re-order BuildRequires tags

* Sun Feb 14 2021 Matthieu Saulnier <fantom@fedoraproject.org> - 3.1.1-6
- Replace glob with %%{python3_version} in %%files section

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Matthieu Saulnier <fantom@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1 upstream release

* Wed Dec 25 2019 Matthieu Saulnier <fantom@fedoraproject.org> - 3.1.0-fix3.1
- Update to 3.1.0-fix3 upstream release
- Remove patch to fix path for the get_version function in docs dir
  - fixed in upstream (commit d0ed707)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 24 2019 Matthieu Saulnier <fantom@fedoraproject.org> - 3.0.0-1
- Bump version to 3.0.0
  - add cffi and sphinx_rtd_theme as buildrequires
  - create patch to fix path for the get_version function in docs dir
- Rebuild for RHBZ#1736524 (FTBFS in Fedora rawhide/f31)
- Removing Python 2 stuff https://fedoraproject.org/wiki/Changes/F31_Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-3
- Rebuilt for Python 3.7

* Wed Apr  4 2018 Matthieu Saulnier <fantom@fedoraproject.org> - 2.3.0-2
- Remove useless code duplication step
- Add missing %%python_provide macro in subpackages
- Cleanup rst doc script in %%install section
- Fix file ownership in doc subpackage

* Mon Apr  2 2018 Matthieu Saulnier <fantom@fedoraproject.org> - 2.3.0-1
- Initial package
