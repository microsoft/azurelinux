%global srcname conda-package-streaming
%global pkgname conda_package_streaming
%global common_description %{expand:Download conda metadata from packages without transferring entire file. Get
metadata from local .tar.bz2 packages without reading entire files.
Uses enhanced pip lazy_wheel to fetch a file out of .conda with no more than
3 range requests, but usually 2.
Uses tar = tarfile.open(fileobj=...) to stream remote .tar.bz2. Closes the
HTTP request once desired files have been seen.}
# We have a circular dep on conda for tests

Summary:        Extract metadata from remote conda packages without downloading whole file
Name:           python-%{srcname}
Version:        0.11.0
Release:        3%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/conda/conda-package-streaming
Source0:        https://github.com/conda/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch
%if 0%{?with_check}
BuildRequires:  python3-archspec
BuildRequires:  python3-zstandard
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-mock
%endif

%description
%{common_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
Requires:       python3-requests
Requires:       python3-zstandard


%description -n python3-%{srcname}
%{common_description}

%prep
%autosetup -n %{srcname}-%{version}
# do not run coverage in pytest, drop unneeded and unpackaged boto3-stubs dev dep
sed -i -e '/cov/d' -e '/boto3-stubs/d' pyproject.toml requirements.txt

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pkgname}

%check
pip3 install pytest-cov==6.1.0 boto3==1.37.24 boto3-stubs[essential]==1.37.24 bottle==0.13.2
%pytest -v tests/test_degraded.py 


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Tue Apr 01 2025 Riken Maharjan <rmaharjan@microsoft.com> - 0.11.0-3
- Initial Azure Linux import from Fedora 42 (license: MIT)
- License Verified

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
