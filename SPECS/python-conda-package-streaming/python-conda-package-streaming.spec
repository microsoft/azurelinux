%global srcname conda-package-streaming
%global pkgname conda_package_streaming

# We have a circular dep on conda for tests
%bcond_with bootstrap

Distribution:   Azure Linux
Name:           python-%{srcname}
Vendor:         Microsoft Corporation
Version:        0.11.0
Release:        2%{?dist}
Summary:        Extract metadata from remote conda packages without downloading whole file

License:        BSD-3-Clause
URL:            https://github.com/conda/conda-package-streaming
Source0:        https://github.com/conda/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global common_description %{expand:Download conda metadata from packages without transferring entire file. Get
metadata from local .tar.bz2 packages without reading entire files.

Uses enhanced pip lazy_wheel to fetch a file out of .conda with no more than
3 range requests, but usually 2.

Uses tar = tarfile.open(fileobj=...) to stream remote .tar.bz2. Closes the
HTTP request once desired files have been seen.}

%description
%{common_description}


%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
Requires:       python3-requests
Requires:       python3-zstandard
# For tests
%if %{without bootstrap}
# Need conda executable for tests
BuildRequires:  conda
%endif

%description -n python3-%{srcname}
%{common_description}


%prep
%autosetup -n %{srcname}-%{version}
# do not run coverage in pytest, drop unneeded and unpackaged boto3-stubs dev dep
sed -i -e '/cov/d' -e '/boto3-stubs/d' pyproject.toml requirements.txt
%if %{with bootstrap}
sed -i -e '/"conda"/d' -e '/conda-package-handling/d' pyproject.toml
%endif

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pkgname}

%check
pip3 install pytest pytest-cov pytest-mock boto3 boto3-stubs[essential] bottle zstandard archspec
%if %{without bootstrap}
# To set CONDA_EXE
. /etc/profile.d/conda.sh
export CONDA_EXE
# The deselected tests require a populated conda package cache which we can't really provide
%pytest -v tests \
  --deselect=tests/test_transmute.py::test_transmute \
  --deselect=tests/test_transmute.py::test_transmute_backwards \
  --deselect=tests/test_url.py::test_lazy_wheel
%else
# Minimal non-conda required test
%pytest -v tests/test_degraded.py
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license %{python3_sitelib}/conda_package_streaming-%{version}.dist-info/LICENSE


%changelog
* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 18 2024 Orion Poplawski <orion@nwra.com> - 0.11.0-1
- Update to 0.11.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Orion Poplawski <orion@nwra.com> - 0.10.0-3
- Drop bootstrap

* Sun Jun 16 2024 Python Maint <python-maint@redhat.com> - 0.10.0-3
- Bootstrap for Python 3.13

* Fri Jun 14 2024 Orion Poplawski <orion@nwra.com> - 0.10.0-2
- Bootstrap build with Python 3.13

* Thu Jun 06 2024 Orion Poplawski <orion@nwra.com> - 0.10.0-1
- Update to 0.10.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Aug 26 2023 Orion Poplawski <orion@nwra.com> - 0.9.0-1
- Update to 0.9.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 20 2023 Python Maint <python-maint@redhat.com> - 0.7.0-6
- Rebuilt for Python 3.12

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 0.7.0-5
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Orion Poplawski <orion@nwra.com> - 0.7.0-3
- Use test extras for build requires
- Add bootstrap conditional

* Wed Dec 07 2022 Orion Poplawski <orion@nwra.com> - 0.7.0-2
- Use macro for description
- Use %%pytest macro
- Fix license
- Add comments about deselected tests

* Sat Dec 03 2022 Orion Poplawski <orion@nwra.com> - 0.7.0-1
- Initial Fedora package
