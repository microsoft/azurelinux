Summary:        Library to access the metadata for a Python package
Name:           python-importlib-metadata
Version:        6.8.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://importlib-metadata.readthedocs.io/
Source0:        %{pypi_source importlib_metadata}

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-docutils
BuildRequires:  python3-packaging
BuildRequires:  python3-pluggy
BuildRequires:  python3-pygments
BuildRequires:  python3-six
BuildRequires:  python3-test
BuildRequires:  python3-zipp
BuildRequires:  python3dist(pytest)
%endif

%description
Library to access the metadata for a Python package.
This package supplies third-party access to the functionality
of importlib.metadata including improvements added to subsequent
Python versions.

%package -n     python3-importlib-metadata
Summary:        %{summary}

Requires:       python3-zipp

%description -n python3-importlib-metadata
Library to access the metadata for a Python package.
This package supplies third-party access to the functionality
of importlib.metadata including improvements added to subsequent
Python versions.

%prep
%autosetup -n importlib_metadata-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files importlib_metadata

%check
pip3 install pyfakefs more-itertools
rm -rf .pyproject-builddir
# Ignored file uses pytest_perf not available in Mariner
# test_find_local tries to install setuptools from PyPI
%pytest --ignore exercises.py -k "not test_find_local"

%files -n python3-importlib-metadata -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.8.0-1
- Auto-upgrade to 6.8.0 - Azure Linux 3.0 - package upgrades

* Fri Apr 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.11.3-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.
- Replacing BR on "python3-pyfakefs" with a pip3 install during tests.
- Adding missing dependency on "python3-zipp".

* Mon Mar 14 2022 Lumír Balhar <lbalhar@redhat.com> - 4.11.3-1
- Update to 4.11.3
Resolves: rhbz#2063566

* Mon Feb 28 2022 Lumír Balhar <lbalhar@redhat.com> - 4.11.2-1
- Update to 4.11.2
Resolves: rhbz#2059016

* Tue Feb 15 2022 Lumír Balhar <lbalhar@redhat.com> - 4.11.1-1
- Update to 4.11.1
Resolves: rhbz#2054478

* Fri Feb 11 2022 Lumír Balhar <lbalhar@redhat.com> - 4.11.0-1
- Update to 4.11.0
Resolves: rhbz#2053332

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Lumír Balhar <lbalhar@redhat.com> - 4.10.1-1
- Update to 4.10.1
Resolves: rhbz#2041301

* Mon Jan 03 2022 Lumír Balhar <lbalhar@redhat.com> - 4.10.0-1
- Update to 4.10.0
Resolves: rhbz#2034072

* Sat Dec 18 2021 Lumír Balhar <lbalhar@redhat.com> - 4.8.3-1
- Update to 4.8.3
Resolves: rhbz#2033335

* Tue Nov 09 2021 Lumír Balhar <lbalhar@redhat.com> - 4.8.2-1
- Update to 4.8.2
Resolves: rhbz#2021375

* Mon Aug 30 2021 Lumír Balhar <lbalhar@redhat.com> - 4.8.1-1
- Update to 4.8.1
Resolves: rhbz#1997891

* Mon Aug 16 2021 Lumír Balhar <lbalhar@redhat.com> - 4.6.4-1
- Update to 4.6.4
Resolves: rhbz#1993538

* Mon Aug 02 2021 Lumír Balhar <lbalhar@redhat.com> - 4.6.3-1
- Update to 4.6.3
Resolves: rhbz#1988649

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Lumír Balhar <lbalhar@redhat.com> - 4.6.1-1
- Update to 4.6.1
Resolves: rhbz#1979098

* Wed Jun 30 2021 Lumír Balhar <lbalhar@redhat.com> - 4.6.0-1
- Unretired and updated package

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.18-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.18-1
- Initial package
