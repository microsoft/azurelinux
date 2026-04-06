# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkg_name geographiclib

Name:           python-%{pkg_name}
Version:        2.1
Release:        2%{?dist}
Summary:        Python 3 implementation of geographiclib

License:        MIT
URL:            https://github.com/geographiclib/geographiclib-python
BuildArch:      noarch
Source0:        %{pypi_source geographiclib}

BuildRequires:  python3-devel
BuildRequires:  python3-pytest

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-python3
BuildRequires:  mingw32-python3-build

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-python3
BuildRequires:  mingw64-python3-build


%description
A translation of the GeographicLib::Geodesic class to Python.


%package -n python3-%{pkg_name}
Summary:        Python 3 implementation of %{pkg_name}


%description -n python3-%{pkg_name}
A translation of the GeographicLib::Geodesic class to Python.


%package -n mingw32-python3-%{pkg_name}
Summary:        MinGW Windows %{pkg_name} python 3 bindings

%description -n mingw32-python3-%{pkg_name}
MinGW Windows %{pkg_name} python 3 bindings.


%package -n mingw64-python3-%{pkg_name}
Summary:        MinGW Windows %{pkg_name} python 3 bindings

%description -n mingw64-python3-%{pkg_name}
MinGW Windows %{pkg_name} python 3 bindings.



%prep
%autosetup -p1 -n geographiclib-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
# Native build
%pyproject_wheel
# MinGW build
%mingw32_py3_build_wheel
%mingw64_py3_build_wheel


%install
# Native build
%pyproject_install
%pyproject_save_files -l geographiclib
# MinGW build
(
%mingw32_py3_install_wheel
%mingw64_py3_install_wheel
)
%mingw_debug_install_post


%check
%pytest


%files -n python3-%{pkg_name} -f %{pyproject_files}
%doc README.md

%files -n mingw32-python3-%{pkg_name}
%license LICENSE
%{mingw32_python3_sitearch}/%{pkg_name}/
%{mingw32_python3_sitearch}/%{pkg_name}-%{version}.dist-info/

%files -n mingw64-python3-%{pkg_name}
%license LICENSE
%{mingw64_python3_sitearch}/%{pkg_name}/
%{mingw64_python3_sitearch}/%{pkg_name}-%{version}.dist-info/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 22 2025 Sandro Mani <manisandro@gmail.com> - 2.1-1
- Update to 2.1

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Sandro Mani <manisandro@gmail.com> - 2.0-4
- Don't explicitly add %%license to %%files as %%pyproject_save_files -l is used

* Sun Jul 13 2025 Sandro Mani <manisandro@gmail.com> - 2.0-3
- Initial standalone package
