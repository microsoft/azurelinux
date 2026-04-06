# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name colour

Name:           python-%{pypi_name}
Version:        0.1.5
Release:        28%{?dist}
Summary:        Python module to convert and manipulate color representations

License:        BSD-2-Clause
URL:            https://github.com/vaab/colour
Source0:        %{pypi_source}
BuildArch:      noarch

%description
Converts and manipulates common color representation (RGB, HSL, web, etc.)

- Damn simple and pythonic way to manipulate color representation
- Full conversion between RGB, HSL, 6-digit hex, 3-digit hex, human color
- One object (Color) or bunch of single purpose function (rgb2hex, hsl2rgb,
  etc.) web format that use the smallest representation between 6-digit 
  (e.g. #fa3b2c), 3-digit (e.g. #fbb), fully spelled color (e.g. white),
  following W3C color naming for compatible CSS or HTML color specifications.
- smooth intuitive color scale generation choosing N color gradients.
- can pick colors for you to identify objects of your application.

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Converts and manipulates common color representation (RGB, HSL, web, etc.)

- Damn simple and pythonic way to manipulate color representation
- Full conversion between RGB, HSL, 6-digit hex, 3-digit hex, human color
- One object (Color) or bunch of single purpose function (rgb2hex, hsl2rgb,
  etc.) web format that use the smallest representation between 6-digit 
  (e.g. #fa3b2c), 3-digit (e.g. #fbb), fully spelled color (e.g. white),
  following W3C color naming for compatible CSS or HTML color specifications.
- smooth intuitive color scale generation choosing N color gradients.
- can pick colors for you to identify objects of your application.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst TODO.rst
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.1.5-28
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.1.5-27
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 David Auer <dreua@posteo.de> - 0.1.5-25
- Update license descriptor

* Thu Jul 17 2025 David Auer <dreua@posteo.de> - 0.1.5-24
- Use pyproject macros
  Closes: rhbz#2377566

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.1.5-23
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.1.5-21
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Python Maint <python-maint@redhat.com> - 0.1.5-19
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.1.5-15
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.1.5-12
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.1.5-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.1.5-1
- Initial package for Fedora
