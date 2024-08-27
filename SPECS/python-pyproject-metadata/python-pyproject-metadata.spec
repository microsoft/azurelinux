%global pkgname pyproject-metadata

# Building the documentation requires the furo Sphinx theme.  But building furo
# requires sphinx_theme_builder, which requires this package.  Avoid a
# dependency loop with this conditional.
%bcond_with doc

Name:           python-%{pkgname}
Version:        0.8.0
Release:        1%{?dist}
Summary:        PEP 621 metadata parsing

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/pypa/python-%{pkgname}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  %{py3_dist docutils}

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

%global _desc %{expand:
Dataclass for PEP 621 metadata with support for core metadata generation.

This project does not implement the parsing of pyproject.toml containing
PEP 621 metadata.  Instead, given a Python data structure representing
PEP 621 metadata (already parsed), it will validate this input and
generate a PEP 643-compliant metadata file (e.g. PKG-INFO).}

%description %_desc

%package     -n python3-%{pkgname}
Summary:        PEP 621 metadata parsing

# This can be removed when F40 reaches EOL
Obsoletes:      python3-pep621 < 0.5
Provides:       python3-pep621 = %{version}-%{release}

%description -n python3-%{pkgname} %_desc

%if %{with doc}
%package        doc
Summary:        Documentation for python3-%{pkgname}

# This can be removed when F40 reaches EOL
Obsoletes:      python3-pep621-doc < 0.5
Provides:       python3-pep621-doc = %{version}-%{release}

%description    doc
Documentation for python3-%{pkgname}.
%endif

%prep
%autosetup -p1 -n %{pkgname}-%{version}
# No need to BuildRequire pytest-cov to run pytest
sed -i /pytest-cov/d pyproject.toml

%generate_buildrequires
%if %{with doc}
%pyproject_buildrequires -x test,docs
%else
%pyproject_buildrequires -x test
%endif

%build
%pyproject_wheel
rst2html --no-datestamp CHANGELOG.rst CHANGELOG.html

%if %{with doc}
# Build the documentation
PYTHONPATH=$PWD/build/lib
mkdir html
sphinx-build -b html docs html
rm -rf html/{.buildinfo,.doctrees}
%endif

%install
%pyproject_install
%pyproject_save_files pyproject_metadata

%check
# Freezing package versions to keep the tests stable.
pip3 install iniconfig==2.0.0
%pytest

%files -n python3-%{pkgname} -f %{pyproject_files}
%doc CHANGELOG.html README.md
%license LICENSE

%if %{with doc}
%files doc
%doc html
%endif

%changelog
* Tue Aug 27 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.0-1
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- License Verified
- Upgraded to version 0.8.0.
- Switched to using original upstream source.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Drop an unused build requirement on pytest-cov

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.7.1-2
- Rebuilt for Python 3.12

* Thu Feb 23 2023 Jerry James <loganjerry@gmail.com> - 0.7.1-1
- Dynamically generate BuildRequires

* Mon Jan 30 2023 Jerry James <loganjerry@gmail.com> - 0.7.1-1
- Version 0.7.1
- Drop packaging workaround, resolved upstream

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Jerry James <loganjerry@gmail.com> - 0.7.0-2
- Work around FTI due to version of packaging (rhbz#2161981)

* Tue Jan 17 2023 Jerry James <loganjerry@gmail.com> - 0.7.0-1
- Version 0.7.0

* Tue Jul 26 2022 Jerry James <loganjerry@gmail.com> - 0.6.1-1
- Initial RPM, obsoleting python-pep621
