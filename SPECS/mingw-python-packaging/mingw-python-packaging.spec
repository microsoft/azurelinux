# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package is required by python-build to build wheels.
# To bootstrap, we copy the files to appropriate locations manually and create a minimal dist-info metadata.
# Note that as a pure Python package, the wheel contains no pre-built binary stuff.
%bcond_with     bootstrap

%{?mingw_package_header}

%global pypi_name packaging

Name:           mingw-python-%{pypi_name}
Summary:        MinGW Python packaging core utils
Version:        25.0
Release:        2%{?dist}
BuildArch:      noarch

License:        BSD-2-Clause OR Apache-2.0
Url:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %{pypi_source}


BuildRequires:  mingw32-filesystem >= 102
BuildRequires:  mingw32-python3
%if %{without bootstrap}
BuildRequires:  mingw32-python3-build
BuildRequires:  mingw32-python3-flit-core
%endif

BuildRequires:  mingw64-filesystem >= 102
BuildRequires:  mingw64-python3
%if %{without bootstrap}
BuildRequires:  mingw64-python3-build
BuildRequires:  mingw64-python3-flit-core
%endif


%description
MinGW Python packaging core utils.


%package -n mingw32-python3-%{pypi_name}
Summary:       MinGW Python 3 packaging core utils
%if %{with bootstrap}
Requires:      mingw32-python3-pyparsing
%endif

%description -n mingw32-python3-%{pypi_name}
MinGW Python 3 packaging core utils.


%package -n mingw64-python3-%{pypi_name}
Summary:       MinGW Python 3 packaging core utils
%if %{with bootstrap}
Requires:      mingw64-python3-pyparsing
%endif

%description -n mingw64-python3-%{pypi_name}
MinGW Python 3 packaging core utils.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%build
%if %{with bootstrap}
%global distinfo %{pypi_name}-%{version}+rpmbootstrap.dist-info
mkdir %{distinfo}
cat > %{distinfo}/METADATA << EOF
Metadata-Version: 2.2
Name: %{pypi_name}
Version: 25.0
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
cp -a packaging %{distinfo} %{buildroot}%{mingw32_python3_sitearch}/
cp -a packaging %{distinfo} %{buildroot}%{mingw64_python3_sitearch}/
mkdir -p %{buildroot}%{mingw32_python3_hostsitearch}
mkdir -p %{buildroot}%{mingw64_python3_hostsitearch}
cp -a packaging %{distinfo} %{buildroot}%{mingw32_python3_hostsitearch}/
cp -a packaging %{distinfo} %{buildroot}%{mingw64_python3_hostsitearch}/
%else
%mingw32_py3_install_wheel
%mingw64_py3_install_wheel
%mingw32_py3_install_host_wheel
%mingw64_py3_install_host_wheel
%endif


%files -n mingw32-python3-%{pypi_name}
%license LICENSE.BSD LICENSE.APACHE LICENSE
%{mingw32_python3_sitearch}/%{pypi_name}/
%{mingw32_python3_sitearch}/%{distinfo}
%{mingw32_python3_hostsitearch}/%{pypi_name}/
%{mingw32_python3_hostsitearch}/%{distinfo}

%files -n mingw64-python3-%{pypi_name}
%license LICENSE.BSD LICENSE.APACHE LICENSE
%{mingw64_python3_sitearch}/%{pypi_name}/
%{mingw64_python3_sitearch}/%{distinfo}
%{mingw64_python3_hostsitearch}/%{pypi_name}/
%{mingw64_python3_hostsitearch}/%{distinfo}


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Apr 21 2025 Sandro Mani <manisandro@gmail.com> - 25.0-1
- Update to 25.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Sandro Mani <manisandro@gmail.com> - 24.2-1
- Update to 24.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Sandro Mani <manisandro@gmail.com> - 24.1-1
- Update to 24.1

* Sun Mar 24 2024 Sandro Mani <manisandro@gmail.com> - 24.0-1
- Update to 24.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 07 2023 Sandro Mani <manisandro@gmail.com> - 23.2-1
- Update to 23.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 24 2023 Sandro Mani <manisandro@gmail.com> - 23.1-1
- Update to 23.1

* Sat Feb 11 2023 Sandro Mani <manisandro@gmail.com> - 23.0-1
- Update to 23.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 21.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 31 2022 Sandro Mani <manisandro@gmail.com> - 21.3-7
- Full build

* Mon Oct 10 2022 Sandro Mani <manisandro@gmail.com> - 21.3-6
- Switch to python3-build (bootstrap)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 21.3-4
- Rebuild for new python dependency generator (take two)

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 21.3-3
- Rebuild for new python dependency generator

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Sandro Mani <manisandro@gmail.com> - 21.3-1
- Update to 21.3

* Tue Nov 02 2021 Sandro Mani <manisandro@gmail.com> - 21.2-1
- Update to 21.2

* Mon Sep 20 2021 Sandro Mani <manisandro@gmail.com> - 21.0-2
- Also include LICENSE in %%license
- Require: mingw-python-pyparsing

* Tue Sep 14 2021 Sandro Mani <manisandro@gmail.com> - 21.0-1
- Initial package
