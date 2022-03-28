%global pypi_name tomli
%global distinfo %{pypi_name}-%{version}+rpmbootstrap.dist-info

Vendor:         Microsoft Corporation
Distribution:   Mariner
# This package buildrequires flit_core to build the wheel, but flit_core requires tomli.
# To bootstrap, we copy the files to appropriate locations manually and create a minimal dist-info metadata.
# Note that as a pure Python package, the wheel contains no pre-built binary stuff.
# When bootstrap is enabled, we don't run tests either, just an import check.
%bcond_without     bootstrap

Name:           python-%{pypi_name}
Version:        2.0.1
Release:        2%{?dist}
Summary:        A little TOML parser for Python

License:        MIT
URL:            https://pypi.org/project/%{pypi_name}/
Source0:        https://github.com/hukkin/%{pypi_name}/archive/refs/tags/%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%if %{without bootstrap}
# Upstream test requirements are in tests/requirements.txt,
# but they're mixed together with coverage ones. Tests only need:
BuildRequires:  python3-pytest
BuildRequires:  python3-dateutil
%endif

%global _description %{expand:
Tomli is a Python library for parsing TOML.
Tomli is fully compatible with TOML v1.0.0.}


%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
mkdir %{distinfo}
cat > %{distinfo}/METADATA << EOF
Metadata-Version: 2.2
Name: tomli
Version: %{version}+rpmbootstrap
EOF

%install
mkdir -p %{buildroot}%{python3_sitelib}
cp -a tomli %{distinfo} %{buildroot}%{python3_sitelib}
echo '%{python3_sitelib}/tomli/' > %{pyproject_files}
echo '%{python3_sitelib}/%{distinfo}/' >> %{pyproject_files}

%check
%py3_check_import tomli
%if %{without bootstrap}
# assert the properly built package has no runtime requires
# if it does, we need to change the bootstrap metadata
test -f %{buildroot}%{python3_sitelib}/tomli-%{version}.dist-info/METADATA
! grep '^Requires-Dist:' %{buildroot}%{python3_sitelib}/tomli-%{version}.dist-info/METADATA
%pytest
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md
%license LICENSE

%changelog
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
