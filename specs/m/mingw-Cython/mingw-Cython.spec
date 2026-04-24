# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# Disable debugsource packages
%undefine _debugsource_packages

%global pypi_name cython
%global mod_name Cython

Name:          mingw-%{mod_name}
Summary:       MinGW Windows Python %{mod_name} library
Version:       3.1.2
Release: 3%{?dist}

License:       Apache-2.0
URL:           http://www.cython.org
Source:        %{pypi_source}

BuildRequires: gcc

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-dlfcn
BuildRequires: mingw32-gcc
BuildRequires: mingw32-python3
BuildRequires: mingw32-python3-build

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-dlfcn
BuildRequires: mingw64-gcc
BuildRequires: mingw64-python3
BuildRequires: mingw64-python3-build


%description
MinGW Windows Python %{mod_name} library.


%package -n mingw32-python3-%{mod_name}
Summary:       MinGW Windows Python3 %{mod_name} library

%description -n mingw32-python3-%{mod_name}
MinGW Windows Python3 %{mod_name} library.


%package -n mingw64-python3-%{mod_name}
Summary:       MinGW Windows Python3 %{mod_name} library

%description -n mingw64-python3-%{mod_name}
MinGW Windows Python3 %{mod_name} library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%build
%mingw32_py3_build_host_wheel
%mingw64_py3_build_host_wheel
%mingw32_py3_build_wheel
%mingw64_py3_build_wheel


%install
%mingw32_py3_install_host_wheel
%mingw64_py3_install_host_wheel
%mingw32_py3_install_wheel
%mingw64_py3_install_wheel


%files -n mingw32-python3-%{mod_name}
%license LICENSE.txt
%{mingw32_bindir}/cygdb
%{mingw32_bindir}/cython
%{mingw32_bindir}/cythonize
%{mingw32_python3_sitearch}/cython.py
%{mingw32_python3_sitearch}/__pycache__/cython*.pyc
%{mingw32_python3_sitearch}/pyximport/
%{mingw32_python3_sitearch}/%{mod_name}/
%{mingw32_python3_sitearch}/cython-%{version}.dist-info/
%{_prefix}/%{mingw32_target}/bin/cygdb
%{_prefix}/%{mingw32_target}/bin/cython
%{_prefix}/%{mingw32_target}/bin/cythonize
%{mingw32_python3_hostsitearch}/cython.py
%{mingw32_python3_hostsitearch}/__pycache__/cython*.pyc
%{mingw32_python3_hostsitearch}/pyximport/
%{mingw32_python3_hostsitearch}/%{mod_name}/
%{mingw32_python3_hostsitearch}/cython-%{version}.dist-info/

%files -n mingw64-python3-%{mod_name}
%license LICENSE.txt
%{mingw64_bindir}/cygdb
%{mingw64_bindir}/cython
%{mingw64_bindir}/cythonize
%{mingw64_python3_sitearch}/cython.py
%{mingw64_python3_sitearch}/__pycache__/cython*.pyc
%{mingw64_python3_sitearch}/pyximport/
%{mingw64_python3_sitearch}/%{mod_name}/
%{mingw64_python3_sitearch}/cython-%{version}.dist-info/
%{_prefix}/%{mingw64_target}/bin/cygdb
%{_prefix}/%{mingw64_target}/bin/cython
%{_prefix}/%{mingw64_target}/bin/cythonize
%{mingw64_python3_hostsitearch}/cython.py
%{mingw64_python3_hostsitearch}/__pycache__/cython*.pyc
%{mingw64_python3_hostsitearch}/pyximport/
%{mingw64_python3_hostsitearch}/%{mod_name}/
%{mingw64_python3_hostsitearch}/cython-%{version}.dist-info/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Sandro Mani <manisandro@gmail.com> - 3.1.2-1
- Update to 3.1.2

* Fri Mar 28 2025 Sandro Mani <manisandro@gmail.com> - 3.0.12-1
- Update to 3.0.12

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 08 2024 Sandro Mani <manisandro@gmail.com> - 3.0.11-1
- Update to 3.0.11

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 08 2024 Sandro Mani <manisandro@gmail.com> - 3.0.10-1
- Update to 3.0.10

* Fri Mar 22 2024 Sandro Mani <manisandro@gmail.com> - 3.0.9-1
- Update to 3.0.9

* Thu Jan 25 2024 Sandro Mani <manisandro@gmail.com> - 3.0.8-1
- Update to 3.0.8

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Sandro Mani <manisandro@gmail.com> - 3.0.6-1
- Update to 3.0.6

* Wed Nov 01 2023 Sandro Mani <manisandro@gmail.com> - 3.0.5-1
- Update to 3.0.5

* Tue Sep 12 2023 Sandro Mani <manisandro@gmail.com> - 3.0.2-1
- Update to 3.0.2

* Tue Aug 15 2023 Sandro Mani <manisandro@gmail.com> - 3.0.0-1
- Update to 3.0.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Sandro Mani <manisandro@gmail.com> - 0.29.36-1
- Update to 0.29.36

* Mon Apr 10 2023 Sandro Mani <manisandro@gmail.com> - 0.29.34-1
- Update to 0.29.34

* Mon Mar 20 2023 Sandro Mani <manisandro@gmail.com> - 0.29.33-2
- Add host build

* Sat Feb 18 2023 Sandro Mani <manisandro@gmail.com> - 0.29.33-1
- Update to 0.29.33

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 19 2022 Sandro Mani <manisandro@gmail.com> - 0.29.32-2
- Switch to python3-build

* Wed Aug 10 2022 Sandro Mani <manisandro@gmail.com> - 0.29.32-1
- Update to 0.29.32

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Sandro Mani <manisandro@gmail.com> - 0.29.30-1
- Update to 0.29.30

* Wed Apr 06 2022 Sandro Mani <manisandro@gmail.com> - 0.29.28-1
- Update to 0.29.28

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 0.29.26-7
- Rebuild with mingw-gcc-12

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 0.29.26-6
- Rebuild for new python dependency generator (take two)

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 0.29.26-5
- Bump release

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 0.29.26-4
- Rebuild for new python dependency generator (take two)

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 0.29.26-3
- Rebuild for new python dependency generator

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Sandro Mani <manisandro@gmail.coM> - 0.29.26-1
- Update to 0.29.26

* Sat Jul 24 2021 Sandro Mani <manisandro@gmail.com> - 0.29.24-1
- Update to 0.29.24

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Sandro Mani <manisandro@gmail.com> - 0.29.22-2
- Rebuild (python-3.10)

* Thu Mar 04 2021 Sandro Mani <manisandro@gmail.com> - 0.29.22-1
- Update to 0.29.22

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Sandro Mani <manisandro@gmail.com> - 0.29.21-2
- Drop BR: mingw-dlfcn

* Thu Jul 23 2020 Sandro Mani <manisandro@gmail.com> - 0.29.21-1
- Update to 0.29.21

* Sat May 30 2020 Sandro Mani <manisandro@gmail.com> - 0.29.19-1
- Update to 0.29.19

* Thu Mar 26 2020 Sandro Mani <manisandro@gmail.com> - 0.29.16-1
- Update to 0.29.16

* Wed Feb 12 2020 Sandro Mani <manisandro@gmail.com> - 0.29.15-1
- Update to 0.29.15

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Sandro Mani <manisandro@gmail.com> - 0.29.14-1
- Update to 0.29.14

* Fri Sep 27 2019 Sandro Mani <manisandro@gmail.com> - 0.29.13-3
- Rebuild (python 3.8)

* Mon Aug 05 2019 Sandro Mani <manisandro@gmail.com> - 0.29.13-2
- Drop python2 build

* Mon Jul 29 2019 Sandro Mani <manisandro@gmail.com> - 0.29.13-1
- Update to 0.29.13

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Sandro Mani <manisandro@gmail.com> - 0.29.12-1
- Update to 0.29.12

* Tue Jul 02 2019 Sandro Mani <manisandro@gmail.com> - 0.29.11-1
- Update to 0.29.11

* Mon Jun 03 2019 Sandro Mani <manisandro@gmail.com> - 0.29.10-1
- Update to 0.29.10

* Mon May 13 2019 Sandro Mani <manisandro@gmail.com> - 0.29.7-1
- Update to 0.29.7

* Wed May 01 2019 Sandro Mani <manisandro@gmail.com> - 0.29.6-2
- Add python3 subpackages

* Mon Mar 11 2019 Sandro Mani <manisandro@gmail.com> - 0.29.6-1
- Update to 0.29.6

* Sun Feb 10 2019 Sandro Mani <manisandro@gmail.com> - 0.29.5-1
- Update to 0.29.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Sandro Mani <manisandro@gmail.com> - 0.29.3-1
- Update to 0.29.3

* Mon Dec 10 2018 Sandro Mani <manisandro@gmail.com> - 0.29.1-1
- Update to 0.29.1

* Sat Aug 11 2018 Sandro Mani <manisandro@gmail.com> - 0.28.5-1
- Update to 0.28.5

* Sun Jul 15 2018 Sandro Mani <manisandro@gmail.com> - 0.28.4-1
- Update to 0.28.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 20 2018 Sandro Mani <manisandro@gmail.com> - 0.28.1-1
- Update to 0.28.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 06 2017 Sandro Mani <manisandro@gmail.com> - 0.27.3-1
- Update to 0.27.3

* Mon Oct 02 2017 Sandro Mani <manisandro@gmail.com> - 0.27.1-1
- Update to 0.27.1

* Sat Sep 09 2017 Sandro Mani <manisandro@gmail.com> - 0.25.2-2
- Rebuild for mingw-filesystem

* Thu Aug 31 2017 Sandro Mani <manisandro@gmail.com> - 0.25.2-1
- Initial package
