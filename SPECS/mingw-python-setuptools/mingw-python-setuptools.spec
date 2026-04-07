# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pypi_name setuptools

Name:          mingw-python-%{pypi_name}
Summary:       MinGW Windows Python %{pypi_name} library
Version:       78.1.1
Release:       2%{?dist}
BuildArch:     noarch

License:       MIT
URL:           https://pypi.python.org/pypi/%{pypi_name}
Source0:       %{pypi_source %{pypi_name} %{version}}

# Adapt is_mingw check to only check get_platform, as sys.platform will be 'linux' when cross-compiling
Patch0:        mingw-python-setuptools_is_mingw.patch
# Don't append -s to linker commandline
Patch1:        mingw-python-setuptools_nostrip.patch
# Don't override shared_lib_extension with SHLIB_SUFFIX config value
# The value set by Mingw32CCompiler class is already correct, no need to override
Patch2:        mingw-python-setuptools-shlib-suffix.patch

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-python3

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-python3


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

# Remove bundled exes
rm -f setuptools/*.exe

# Strip shebangs on python modules
find setuptools -name \*.py | xargs sed -i -e '1 {/^#!\//d}'


%build
%{mingw32_py3_build_host}
%{mingw64_py3_build_host}
%{mingw32_py3_build}
%{mingw64_py3_build}


%install
%{mingw32_py3_install_host}
%{mingw64_py3_install_host}
%{mingw32_py3_install}
%{mingw64_py3_install}

find %{buildroot}%{mingw32_python3_sitearch}/ -name '*.exe' | xargs rm -f
find %{buildroot}%{mingw64_python3_sitearch}/ -name '*.exe' | xargs rm -f


%files -n mingw32-python3-%{pypi_name}
%license LICENSE
%{_prefix}/%{mingw32_target}/lib/python%{mingw32_python3_version}/site-packages/%{pypi_name}/
%{_prefix}/%{mingw32_target}/lib/python%{mingw32_python3_version}/site-packages/pkg_resources/
%{_prefix}/%{mingw32_target}/lib/python%{mingw32_python3_version}/site-packages/_distutils_hack/
%{_prefix}/%{mingw32_target}/lib/python%{mingw32_python3_version}/site-packages/distutils-precedence.pth
%{_prefix}/%{mingw32_target}/lib/python%{mingw32_python3_version}/site-packages/%{pypi_name}-%{version}-py%{mingw32_python3_version}.egg-info/
%{mingw32_python3_sitearch}/%{pypi_name}/
%{mingw32_python3_sitearch}/pkg_resources/
%{mingw32_python3_sitearch}/_distutils_hack/
%{mingw32_python3_sitearch}/distutils-precedence.pth
%{mingw32_python3_sitearch}/%{pypi_name}-%{version}-py%{mingw32_python3_version}.egg-info/

%files -n mingw64-python3-%{pypi_name}
%license LICENSE
%{_prefix}/%{mingw64_target}/lib/python%{mingw64_python3_version}/site-packages/%{pypi_name}/
%{_prefix}/%{mingw64_target}/lib/python%{mingw64_python3_version}/site-packages/pkg_resources/
%{_prefix}/%{mingw64_target}/lib/python%{mingw64_python3_version}/site-packages/_distutils_hack/
%{_prefix}/%{mingw64_target}/lib/python%{mingw64_python3_version}/site-packages/distutils-precedence.pth
%{_prefix}/%{mingw64_target}/lib/python%{mingw64_python3_version}/site-packages/%{pypi_name}-%{version}-py%{mingw64_python3_version}.egg-info/
%{mingw64_python3_sitearch}/%{pypi_name}/
%{mingw64_python3_sitearch}/pkg_resources/
%{mingw64_python3_sitearch}/_distutils_hack/
%{mingw64_python3_sitearch}/distutils-precedence.pth
%{mingw64_python3_sitearch}/%{pypi_name}-%{version}-py%{mingw64_python3_version}.egg-info/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 78.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 29 2025 Sandro Mani <manisandro@gmail.com> - 78.1.1-1
- Update to 78.1.1

* Fri Mar 28 2025 Sandro Mani <manisandro@gmail.com> - 78.1.0-1
- Update to 78.1.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 74.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Sandro Mani <manisandro@gmail.com> - 74.1.3-4
- Add mingw-python-setuptools-shlib-suffix.patch

* Sun Dec 08 2024 Sandro Mani <manisandro@gmail.com> - 74.1.3-3
- Add mingw-python-setuptools_nostrip.patch

* Fri Nov 29 2024 Sandro Mani <manisandro@gmail.com> - 74.1.3-2
- Add mingw-python-setuptools_is_mingw.patch

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 74.1.3-1
- Update to 74.1.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 69.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 17 2024 Sandro Mani <manisandro@gmail.com> - 69.2.0-1
- Update to 69.2.0

* Wed Feb 07 2024 Sandro Mani <manisandro@gmail.com> - 69.0.3-1
- Update to 69.0.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 68.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 68.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 28 2023 Sandro Mani <manisandro@gmail.com> - 68.2.2-1
- Update to 68.2.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 67.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 25 2023 Sandro Mani <manisandro@gmail.com> - 67.7.2-1
- Update to 67.7.2

* Sat Apr 22 2023 Sandro Mani <manisandro@gmail.com> - 67.7.1-1
- Update to 67.7.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 65.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Sandro Mani <manisandro@gmail.com> - 65.5.1-1
- Update to 65.5.1

* Mon Oct 31 2022 Sandro Mani <manisandro@gmail.com> - 65.5.0-1
- Update to 65.5.0

* Tue Oct 11 2022 Sandro Mani <manisandro@gmail.com> - 65.4.1-2
- Add mingw-python-setuptools_linkpython.patch

* Mon Oct 10 2022 Sandro Mani <manisandro@gmail.com> - 65.4.1-1
- Update to 65.4.1

* Thu Aug 04 2022 Sandro Mani <manisandro@gmail.com> - 59.6.0-6
- Add host build

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 59.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 59.6.0-4
- Rebuild for new python dependency generator (take two)

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 59.6.0-3
- Rebuild for new python dependency generator

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 59.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Sandro Mani <manisandro@gmail.com> - 59.6.0-1
- Update to 59.6.0

* Sat Nov 13 2021 Sandro Mani <manisandro@gmail.com> - 58.5.3-1
- Update to 58.5.3

* Sat Oct 23 2021 Sandro Mani <manisandro@gmail.com> - 58.3.0-1
- Update to 58.3.0

* Wed Aug 04 2021 Sandro Mani <manisandro@gmail.com> - 57.4.0-1
- Update to 57.4.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 57.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Sandro Mani <manisandro@gmail.com> - 57.1.0-1
- Update to 57.1.0

* Mon Jun 21 2021 Sandro Mani <manisandro@gmail.com> - 57.0.0-1
- Update to 57.0.0

* Fri Jun 11 2021 Sandro Mani <manisandro@gmail.com> - 56.2.0-2
- Rebuild (python-3.10)

* Wed May 19 2021 Sandro Mani <manisandro@gmail.com> - 56.2.0-1
- Update to 56.2.0

* Wed Apr 14 2021 Sandro Mani <manisandro@gmail.com> - 56.0.0-1
- Update to 56.0.0

* Thu Mar 18 2021 Sandro Mani <manisandro@gmail.com> - 54.1.2-1
- Update to 54.1.2

* Mon Feb 15 2021 Sandro Mani <manisandro@gmail.com> - 53.0.0-2
- Add mingw-python-setuptools_no-msvc.patch

* Thu Feb 04 2021 Sandro Mani <manisandro@gmail.com> - 53.0.0-1
- Update to 53.0.0

* Thu Jan 28 2021 Sandro Mani <manisandro@gmail.com> - 52.0.0-1
- Update to 52.0.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 51.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Sandro Mani <manisandro@gmail.com> - 51.1.2-1
- Update to 51.1.2

* Wed Dec 30 2020 Sandro Mani <manisandro@gmail.com> - 51.1.1-1
- Update to 51.1.1

* Sun Nov 08 2020 Sandro Mani <manisandro@gmail.com> - 50.3.2-2
- Switch to py3_build/py3_install macros

* Wed Oct 28 2020 Sandro Mani <manisandro@gmail.com> - 50.3.2-1
- Update to 50.3.2

* Fri Sep 11 2020 Sandro Mani <manisandro@gmail.com> - 50.1.0-1
- Update to 50.1.0

* Thu Aug 27 2020 Sandro Mani <manisandro@gmail.com> - 49.6.0-1
- Update to 49.6.0

* Thu Jul 30 2020 Sandro Mani <manisandro@gmail.com> - 49.1.3-1
- Update to 49.1.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 47.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Sandro Mani <manisandro@gmail.com> - 47.3.1-1
- Update to 47.3.1

* Fri Jun 12 2020 Sandro Mani <manisandro@gmail.com> - 47.1.1-1
- Update to 47.1.1

* Sat May 30 2020 Sandro Mani <manisandro@gmail.com> - 46.4.0-2
- Rebuild (python-3.9)

* Mon May 18 2020 Sandro Mani <manisandro@gmail.com> - 46.4.0-1
- Update to 46.4.0

* Thu May 14 2020 Sandro Mani <manisandro@gmail.com> - 46.2.0-1
- Update to 46.2.0

* Thu Apr 02 2020 Sandro Mani <manisandro@gmail.com> - 46.1.2-1
- Update to 46.1.2

* Fri Mar 13 2020 Sandro Mani <manisandro@gmail.com> - 46.0.0-1
- Update to 46.0.0

* Mon Mar 02 2020 Sandro Mani <manisandro@gmail.com> - 45.2.0-1
- Update to 45.2.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 41.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Sandro Mani <manisandro@gmail.com> - 41.6.0-1
- Update to 41.6.0

* Thu Sep 26 2019 Sandro Mani <manisandro@gmail.com> - 41.2.0-1
- Update to 41.2.0

* Mon Aug 05 2019 Sandro Mani <manisandro@gmail.com> - 41.0.1-3
- Drop python2 build

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 41.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 01 2019 Sandro Mani <manisandro@gmail.com> - 41.0.1-1
- Update to 41.0.1
- Add python3 subpackages

* Wed Feb 06 2019 Sandro Mani <manisandro@gmail.com> - 40.8.0-1
- Update to 40.8.0

* Tue Feb 05 2019 Sandro Mani <manisandro@gmail.com> - 40.7.3-1
- Update to 40.7.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 40.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Sandro Mani <manisandro@gmail.com> - 40.7.1-1
- Update to 40.7.1

* Tue Sep 25 2018 Sandro Mani <manisandro@gmail.com> - 40.4.3-1
- Update to 40.4.3

* Thu Sep 20 2018 Sandro Mani <manisandro@gmail.com> - 40.4.1-1
- Update to 40.4.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 39.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Sandro Mani <manisandro@gmail.com> - 39.2.0-1
- Update to 39.2.0

* Wed Mar 21 2018 Sandro Mani <manisandro@gmail.com> - 39.0.1-1
- Update to 39.0.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 38.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Sandro Mani <manisandro@gmail.com> - 38.4.0-1
- Update to 38.4.0

* Wed Jan 03 2018 Sandro Mani <manisandro@gmail.com> - 38.2.5-1
- Update to 38.2.5

* Thu Nov 23 2017 Sandro Mani <manisandro@gmail.com> - 37.0.0-1
- Update to 37.0.0

* Tue Sep 05 2017 Sandro Mani <manisandro@gmail.com> - 36.2.0-2
- Remove bundled exes
- Remove shebangs on python modules
- Delete exes underneath site-packages

* Thu Aug 31 2017 Sandro Mani <manisandro@gmail.com> - 36.2.0-1
- Initial package
