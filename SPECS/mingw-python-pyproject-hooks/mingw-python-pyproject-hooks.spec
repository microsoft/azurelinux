# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package is required by python-build to build wheels.
# To bootstrap, we copy the files to appropriate locations manually and create a minimal dist-info metadata.
# Note that as a pure Python package, the wheel contains no pre-built binary stuff.
%bcond_with     bootstrap

%{?mingw_package_header}

%global pkgname pyproject-hooks
%global pypi_name pyproject_hooks

Name:           mingw-python-%{pkgname}
Summary:        MinGW Python %{pypi_name} library
Version:        1.2.0
Release:        3%{?dist}
BuildArch:      noarch

License:        MIT
Url:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %{pypi_source}


BuildRequires:  mingw32-filesystem >= 102
BuildRequires:  mingw32-python3
%if %{without bootstrap}
BuildRequires:  mingw32-python3-flit-core
BuildRequires:  mingw32-python3-build
%endif

BuildRequires:  mingw64-filesystem >= 102
BuildRequires:  mingw64-python3
%if %{without bootstrap}
BuildRequires:  mingw64-python3-flit-core
BuildRequires:  mingw64-python3-build
%endif


%description
MinGW Python %{pypi_name} library.


%package -n mingw32-python3-%{pkgname}
Summary:       MinGW Python 3 %{pypi_name} library

%description -n mingw32-python3-%{pkgname}
MinGW Python 3 %{pypi_name} library.


%package -n mingw64-python3-%{pkgname}
Summary:       MinGW Python 3 %{pypi_name} library

%description -n mingw64-python3-%{pkgname}
MinGW Python 3 %{pypi_name} library.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%build
%if %{with bootstrap}
%global distinfo %{pypi_name}-%{version}+rpmbootstrap.dist-info
mkdir %{distinfo}
cat > %{distinfo}/METADATA << EOF
Metadata-Version: 2.2
Name: %{pypi_name}
Version: 1.2.0
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
cp -a src/pyproject_hooks %{distinfo} %{buildroot}%{mingw32_python3_sitearch}/
cp -a src/pyproject_hooks %{distinfo} %{buildroot}%{mingw64_python3_sitearch}/
mkdir -p %{buildroot}%{mingw32_python3_hostsitearch}
mkdir -p %{buildroot}%{mingw64_python3_hostsitearch}
cp -a src/pyproject_hooks %{distinfo} %{buildroot}%{mingw32_python3_hostsitearch}/
cp -a src/pyproject_hooks %{distinfo} %{buildroot}%{mingw64_python3_hostsitearch}/
%else
%mingw32_py3_install_wheel
%mingw64_py3_install_wheel
%mingw32_py3_install_host_wheel
%mingw64_py3_install_host_wheel
%endif


%files -n mingw32-python3-%{pkgname}
%license LICENSE
%{mingw32_python3_sitearch}/%{pypi_name}/
%{mingw32_python3_sitearch}/%{distinfo}
%{mingw32_python3_hostsitearch}/%{pypi_name}/
%{mingw32_python3_hostsitearch}/%{distinfo}

%files -n mingw64-python3-%{pkgname}
%license LICENSE
%{mingw64_python3_sitearch}/%{pypi_name}/
%{mingw64_python3_sitearch}/%{distinfo}
%{mingw64_python3_hostsitearch}/%{pypi_name}/
%{mingw64_python3_hostsitearch}/%{distinfo}


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 03 2024 Sandro Mani <manisandro@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Sandro Mani <manisandro@gmail.com> - 1.0.0-1
- Full build

* Tue Jan 24 2023 Sandro Mani <manisandro@gmail.com> - 1.0.0-0.1
- Bootstrap build
