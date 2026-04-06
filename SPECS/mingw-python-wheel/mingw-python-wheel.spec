# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pypi_name wheel

Name:          mingw-python-%{pypi_name}
Summary:       MinGW Windows Python %{pypi_name} library
Version:       0.46.3
Release:       1%{?dist}
BuildArch:     noarch

License:       MIT AND (Apache-2.0 OR BSD-2-Clause)
URL:           https://pypi.python.org/pypi/%{pypi_name}
Source0:       %{pypi_source %{pypi_name} %{version}}

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-python3
BuildRequires: mingw32-python3-setuptools

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-python3
BuildRequires: mingw64-python3-setuptools

# Don't scan */bin/wheel for requires, it would generate a Requires: pythonX.Y
%global __requires_exclude_from ^.*/bin/wheel$

%description
MinGW Windows Python %{pypi_name} library.


%package -n mingw32-python3-%{pypi_name}
Summary:       MinGW Windows Python3 %{pypi_name} library

%description -n mingw32-python3-%{pypi_name}
MinGW Windows Python3 %{pypi_name} library.


%package -n mingw64-python3-%{pypi_name}
Summary:       MinGW Windows Python3 %{pypi_name} library

%description -n mingw64-python3-%{pypi_name}
MinGW Windows Python3 %{pypi_name} library.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%build
%mingw32_py3_build
%mingw64_py3_build
%mingw32_py3_build_host
%mingw64_py3_build_host


%install
%mingw32_py3_install
%mingw64_py3_install
%mingw32_py3_install_host
%mingw64_py3_install_host


%files -n mingw32-python3-%{pypi_name}
%license LICENSE.txt
%{mingw32_bindir}/wheel
%{mingw32_python3_sitearch}/%{pypi_name}/
%{mingw32_python3_sitearch}/%{pypi_name}-%{version}-py%{mingw32_python3_version}.egg-info/
%{_prefix}/%{mingw32_target}/bin/wheel
%{mingw32_python3_hostsitearch}/%{pypi_name}/
%{mingw32_python3_hostsitearch}/%{pypi_name}-%{version}-py%{mingw32_python3_version}.egg-info/

%files -n mingw64-python3-%{pypi_name}
%license LICENSE.txt
%{mingw64_bindir}/wheel
%{mingw64_python3_sitearch}/%{pypi_name}/
%{mingw64_python3_sitearch}/%{pypi_name}-%{version}-py%{mingw64_python3_version}.egg-info/
%{_prefix}/%{mingw64_target}/bin/wheel
%{mingw64_python3_hostsitearch}/%{pypi_name}/
%{mingw64_python3_hostsitearch}/%{pypi_name}-%{version}-py%{mingw64_python3_version}.egg-info/


%changelog
* Thu Jan 22 2026 Sandro Mani <manisandro@gmail.com> - 0.46.3-1
- Update to 0.46.3

* Thu Jan 22 2026 Sandro Mani <manisandro@gmail.com> - 0.46.2-1
- Update to 0.46.2

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 15 2025 Sandro Mani <manisandro@gmail.com> - 0.46.1-1
- Update to 0.46.1

* Fri Apr 04 2025 Sandro Mani <manisandro@gmail.com> - 0.46.0-1
- Update to 0.46.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.45.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 27 2024 Sandro Mani <manisandro@gmail.com> - 0.45.1-1
- Update to 0.45.1

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 0.45.0-1
- Update to 0.45.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Apr 14 2024 Sandro Mani <manisandro@gmail.com> - 0.43.0-1
- Update to 0.43.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 12 2023 Sandro Mani <manisandro@gmail.com> - 0.41.2-1
- Update to 0.41.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 28 2023 Sandro Mani <manisandro@gmail.com> - 0.40.0-1
- Update to 0.40.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Sandro Mani <manisandro@gmail.com> - 0.38.4-1
- Update to 0.38.4

* Wed Oct 19 2022 Sandro Mani <manisandro@gmail.com> - 0.37.1-2
- Fix license
- Add host build
- Filter requires on */bin/wheel

* Tue Sep 27 2022 Sandro Mani <manisandro@gmail.com> - 0.37.1-1
- Initial build
