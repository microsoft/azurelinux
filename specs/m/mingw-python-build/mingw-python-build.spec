# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# python-built requires itself to build wheels.
# To bootstrap, we copy the files to appropriate locations manually and create a minimal dist-info metadata.
# Note that as a pure Python package, the wheel contains no pre-built binary stuff.
%bcond_with     bootstrap

%{?mingw_package_header}

%global pypi_name build

Name:           mingw-python-%{pypi_name}
Summary:        MinGW Python %{pypi_name} library
Version:        1.3.0
Release: 2%{?dist}
BuildArch:      noarch

License:        MIT
Url:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %{pypi_source}
Source1:        macros.mingw32-python3-wheel
Source2:        macros.mingw64-python3-wheel


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


%package -n mingw32-python3-%{pypi_name}
Summary:       MinGW Python 3 %{pypi_name} library
Requires:      mingw32-python3-installer
Requires:      mingw32-python3-setuptools
Requires:      mingw32-python3-wheel
# For %%{_rpmconfigdir}/macros.d/
Requires:      rpm

%description -n mingw32-python3-%{pypi_name}
MinGW Python 3 %{pypi_name} library.


%package -n mingw64-python3-%{pypi_name}
Summary:       MinGW Python 3 %{pypi_name} library
Requires:      mingw64-python3-installer
Requires:      mingw64-python3-setuptools
Requires:      mingw64-python3-wheel
# For %%{_rpmconfigdir}/macros.d/
Requires:      rpm

%description -n mingw64-python3-%{pypi_name}
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
Version: 1.3.0
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
cp -a src/build %{distinfo} %{buildroot}%{mingw32_python3_sitearch}/
cp -a src/build %{distinfo} %{buildroot}%{mingw64_python3_sitearch}/
mkdir -p %{buildroot}%{mingw32_python3_hostsitearch}
mkdir -p %{buildroot}%{mingw64_python3_hostsitearch}
cp -a src/build %{distinfo} %{buildroot}%{mingw32_python3_hostsitearch}/
cp -a src/build %{distinfo} %{buildroot}%{mingw64_python3_hostsitearch}/
%else
%mingw32_py3_install_wheel
%mingw64_py3_install_wheel
%mingw32_py3_install_host_wheel
%mingw64_py3_install_host_wheel
%endif

# Install macros
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.mingw32-python3-wheel
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d/macros.mingw64-python3-wheel


%files -n mingw32-python3-%{pypi_name}
%license LICENSE
%{mingw32_bindir}/pyproject-build
%{mingw32_python3_sitearch}/%{pypi_name}/
%{mingw32_python3_sitearch}/%{distinfo}
%{_prefix}/%{mingw32_target}/bin/pyproject-build
%{mingw32_python3_hostsitearch}/%{pypi_name}/
%{mingw32_python3_hostsitearch}/%{distinfo}
%{_rpmconfigdir}/macros.d/macros.mingw32-python3-wheel

%files -n mingw64-python3-%{pypi_name}
%license LICENSE
%{mingw64_bindir}/pyproject-build
%{mingw64_python3_sitearch}/%{pypi_name}/
%{mingw64_python3_sitearch}/%{distinfo}
%{_prefix}/%{mingw64_target}/bin/pyproject-build
%{mingw64_python3_hostsitearch}/%{pypi_name}/
%{mingw64_python3_hostsitearch}/%{distinfo}
%{_rpmconfigdir}/macros.d/macros.mingw64-python3-wheel


%changelog
* Sun Aug 03 2025 Sandro Mani <manisandro@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 10 2024 Sandro Mani <manisandro@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 02 2024 Sandro Mani <manisandro@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Fri Mar 22 2024 Sandro Mani <manisandro@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Wed Jan 24 2024 Sandro Mani <manisandro@gmail.com> - 1.0.3-1
- Update to 1.0.3

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jan 22 2023 Sandro Mani <manisandro@gmail.com> - 0.10.0-1
- Update to 0.10.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Sandro Mani <manisandro@gmail.com> - 0.9.0-1
- Update to 0.9.0

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 0.8.0-3
- Require rpm for %%{_rpmconfigdir}/macros.d/

* Wed Oct 19 2022 Sandro Mani <manisandro@gmail.com> - 0.8.0-2
- Switch to setuptools based build and drop bootstrap logic

* Thu Oct 13 2022 Sandro Mani <manisandro@gmail.com> - 0.8.0-1
- Initial package
