%global pypi_name tomli
%global distinfo %{pypi_name}-%{version}+rpmbootstrap.dist-info
%global _description %{expand:
Tomli is a Python library for parsing TOML.
Tomli is fully compatible with TOML v1.0.0.}

Summary:        A little TOML parser for Python
Name:           python-%{pypi_name}
Version:        2.0.1
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.org/project/%{pypi_name}/
Source0:        https://github.com/hukkin/%{pypi_name}/archive/refs/tags/%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-dateutil
%endif

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files tomli

%check
pip3 install more_itertools pluggy pytest
%py3_check_import tomli
# assert the properly built package has no runtime requires
# if it does, we need to change the bootstrap metadata
test -f %{buildroot}%{python3_sitelib}/tomli-%{version}.dist-info/METADATA
! grep '^Requires-Dist:' %{buildroot}%{python3_sitelib}/tomli-%{version}.dist-info/METADATA
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md
%license LICENSE

%changelog
* Mon Apr 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-3
- Removed BR on "python3-pytest" to break a circular dependency. Replaced with build-time pip3 installation.

* Sun Mar 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Mar 03 2022 Petr Viktorin <pviktori@redhat.com> - 2.0.1-1
- Version 2.0.1
  - Removed support for text file objects as load input
  - First argument of load and loads can no longer be passed by keyword
  - Raise an error when dotted keys define values outside the "current table"
  - Prepare for inclusion in stdlib

* Wed Feb 02 2022 Petr Viktorin <pviktori@redhat.com> - 1.2.3-1
- Update to 1.2.3
  - Allow lower case "t" and "z" in datetimes

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 29 2021 Miro Hrončok <mhroncok@redhat.com> - 1.2.2-2
- Allow a bootstrap build without flit_core

* Wed Oct 27 2021 Petr Viktorin <pviktori@redhat.com> - 1.2.2-1
- Update to version 1.2.2

* Wed Aug 18 2021 Petr Viktorin <pviktori@redhat.com> - 1.2.1-1
- Update to version 1.2.1
  - loading text (as opposed to binary) files is deprecated

* Thu Jul 29 2021 Petr Viktorin <pviktori@redhat.com> - 1.1.0-1
- Update to version 1.1.0
  - `load` can now take a binary file object

* Thu Jul 22 2021 Petr Viktorin <pviktori@redhat.com> - 1.0.4-1
- Initial package
