# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname flit-core
%global pypi_name flit_core

Name:           mingw-python-%{pkgname}
Summary:        MinGW Python %{pypi_name} library
Version:        3.12.0
Release:        2%{?dist}
BuildArch:      noarch

License:        BSD-2-Clause
Url:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %{pypi_source}


BuildRequires:  mingw32-filesystem >= 102
BuildRequires:  mingw32-python3

BuildRequires:  mingw64-filesystem >= 102
BuildRequires:  mingw64-python3


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
# See https://flit.pypa.io/en/stable/bootstrap.html
# It is a pure python module, one wheel is sufficient for all
# %%mingw32_python3_version is the same as %%mingw64_python3_version
/usr/bin/python%{mingw32_python3_version} -m flit_core.wheel


%install
mkdir -p %{buildroot}%{mingw32_python3_sitearch}
mkdir -p %{buildroot}%{mingw32_python3_hostsitearch}
mkdir -p %{buildroot}%{mingw64_python3_sitearch}
mkdir -p %{buildroot}%{mingw64_python3_hostsitearch}

%mingw32_python3 bootstrap_install.py --installdir %{buildroot}%{mingw32_python3_sitearch} dist/flit_core-*.whl
%mingw32_python3_host bootstrap_install.py --installdir %{buildroot}%{mingw32_python3_hostsitearch} dist/flit_core-*.whl
%mingw64_python3 bootstrap_install.py --installdir %{buildroot}%{mingw64_python3_sitearch} dist/flit_core-*.whl
%mingw64_python3_host bootstrap_install.py --installdir %{buildroot}%{mingw64_python3_hostsitearch} dist/flit_core-*.whl


%files -n mingw32-python3-%{pkgname}
%{mingw32_python3_sitearch}/%{pypi_name}/
%{mingw32_python3_sitearch}/%{pypi_name}-%{version}.dist-info/
%{mingw32_python3_hostsitearch}/%{pypi_name}/
%{mingw32_python3_hostsitearch}/%{pypi_name}-%{version}.dist-info/

%files -n mingw64-python3-%{pkgname}
%{mingw64_python3_sitearch}/%{pypi_name}/
%{mingw64_python3_sitearch}/%{pypi_name}-%{version}.dist-info/
%{mingw64_python3_hostsitearch}/%{pypi_name}/
%{mingw64_python3_hostsitearch}/%{pypi_name}-%{version}.dist-info/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 28 2025 Sandro Mani <manisandro@gmail.com> - 3.12.0-1
- Update to 3.12.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 03 2024 Sandro Mani <manisandro@gmail.com> - 3.10.1-1
- Update to 3.10.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Sandro Mani <manisandro@gmail.com> - 3.9.0-1
- Update to 3.9.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 Sandro Mani <manisandro@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Oct 19 2022 Sandro Mani <manisandro@gmail.com> - 3.7.1-2
- Use flit bootstrapping logic

* Thu Oct 13 2022 Sandro Mani <manisandro@gmail.com> - 3.7.1-1
- Initial package
