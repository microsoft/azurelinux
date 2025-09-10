# set upstream name variable
%global srcname pycares

Name:           python3-pycares
Version:        4.5.0
Release:        1%{?dist}
Summary:        Python interface for c-ares

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/saghul/pycares
Source0:        https://github.com/saghul/pycares/archive/refs/tags/v%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  python3-cffi
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  c-ares-devel
BuildRequires:  iana-etc
# for docs
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  python3-sphinxcontrib-jquery
# for tests
BuildRequires:  python3-pytest

%description
pycares is a Python module which provides an interface to
c-ares. c-ares is a C library that performs DNS requests and name
resolutions asynchronously.

%package     -n python3-%{srcname}-doc
Summary:        Documentation for python-pycares
BuildArch:      noarch
Requires:       python3-%{srcname} = %{version}-%{release}

%description -n python3-%{srcname}-doc
pycares is a Python module which provides an interface to
c-ares. c-ares is a C library that performs DNS requests and name
resolutions asynchronously.

This package contains documentation in reST and HTML formats.

%prep
%autosetup -p1 -n %{srcname}-%{version}

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

%check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{python3} -m unittest -v

%files
%license LICENSE
%doc README.rst ChangeLog
# For arch-specific packages: sitearch
%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/%{srcname}-%{version}-py%{python3_version}.egg-info/

%files -n python3-%{srcname}-doc
%doc examples/
%{_pkgdocdir}/

%changelog
* Wed Aug 13 2025 Akhila Guruju <v-guakhila@microsoft.com> - 4.5.0-1
- Upgrade to 4.5.0 by taking reference from Fedora 41 spec (license: MIT).
- License verified.
- Added BR on python3-sphinxcontrib-jquery to fix build.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
