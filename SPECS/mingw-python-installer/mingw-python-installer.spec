# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package is required by python-build to build wheels.
# To bootstrap, we copy the files to appropriate locations manually and create a minimal dist-info metadata.
# Note that as a pure Python package, the wheel contains no pre-built binary stuff.
%bcond_with     bootstrap

%{?mingw_package_header}

%global pypi_name installer

Name:          mingw-python-%{pypi_name}
Summary:       MinGW Windows Python %{pypi_name} library
Version:       0.7.0
Release:       7%{?dist}
BuildArch:     noarch

License:       MIT
URL:           https://pypi.python.org/pypi/%{pypi_name}
Source0:       %{pypi_source %{pypi_name} %{version}}

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-python3
%if %{without bootstrap}
BuildRequires: mingw32-python3-build
BuildRequires: mingw32-python3-flit-core
%endif

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-python3
%if %{without bootstrap}
BuildRequires: mingw64-python3-build
BuildRequires: mingw64-python3-flit-core
%endif


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
%if %{with bootstrap}
%global distinfo %{pypi_name}-%{version}+rpmbootstrap.dist-info
mkdir %{distinfo}
cat > %{distinfo}/METADATA << EOF
Metadata-Version: 2.2
Name: %{pypi_name}
Version: 0.7.0
EOF
%else
%global distinfo %{pypi_name}-%{version}.dist-info
%mingw32_py3_build_wheel
%mingw64_py3_build_wheel
%mingw32_py3_build_host_wheel
%mingw64_py3_build_host_wheel
%endif


%install
%if %{with bootstrap}
mkdir -p %{buildroot}%{mingw32_python3_sitearch}
mkdir -p %{buildroot}%{mingw64_python3_sitearch}
cp -a src/installer %{distinfo} %{buildroot}%{mingw32_python3_sitearch}/
cp -a src/installer %{distinfo} %{buildroot}%{mingw64_python3_sitearch}/
mkdir -p %{buildroot}%{mingw32_python3_hostsitearch}
mkdir -p %{buildroot}%{mingw64_python3_hostsitearch}
cp -a src/installer %{distinfo} %{buildroot}%{mingw32_python3_hostsitearch}/
cp -a src/installer %{distinfo} %{buildroot}%{mingw64_python3_hostsitearch}/
%else
%mingw32_py3_install_wheel
%mingw64_py3_install_wheel
%mingw32_py3_install_host_wheel
%mingw64_py3_install_host_wheel
%endif


%files -n mingw32-python3-%{pypi_name}
%license LICENSE
%{mingw32_python3_sitearch}/%{pypi_name}/
%{mingw32_python3_sitearch}/%{distinfo}
%{mingw32_python3_hostsitearch}/%{pypi_name}/
%{mingw32_python3_hostsitearch}/%{distinfo}

%files -n mingw64-python3-%{pypi_name}
%license LICENSE
%{mingw64_python3_sitearch}/%{pypi_name}/
%{mingw64_python3_sitearch}/%{distinfo}
%{mingw64_python3_hostsitearch}/%{pypi_name}/
%{mingw64_python3_hostsitearch}/%{distinfo}


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 03 2023 Sandro Mani <manisandro@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 31 2022 Sandro Mani <manisandro@gmail.com> - 0.5.1-2
- Full build

* Tue Oct 18 2022 Sandro Mani <manisandro@gmail.com> - 0.5.1-1
- Initial build
