%global pypi_name sphinxcontrib-jsmath

Summary:        Sphinx extension for math in HTML via JavaScript
Name:           python-%{pypi_name}
Version:        1.0.1
Release:        16%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://sphinx-doc.org/
Source0:        %{pypi_source}
Patch0:         test_jsmath_path_fix.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%if %{with_check}
BuildRequires:  python%{python3_pkgversion}-atomicwrites
BuildRequires:  python%{python3_pkgversion}-attrs
BuildRequires:  python%{python3_pkgversion}-docutils
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-pluggy
BuildRequires:  python%{python3_pkgversion}-pygments
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-six
%endif

%description
sphinxcontrib-jsmath is a sphinx extension which renders display math in HTML
via JavaScript.

%package -n     python%{python3_pkgversion}-%{pypi_name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{pypi_name}
sphinxcontrib-jsmath is a sphinx extension which renders display math in HTML
via JavaScript.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install more-itertools Sphinx
python3 -m pytest

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/
%{python3_sitelib}/sphinxcontrib_jsmath-%{version}-py%{python3_version}-*.pth
%{python3_sitelib}/sphinxcontrib_jsmath-%{version}-py%{python3_version}.egg-info/

%changelog
* Mon Jun 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-16
- Fixing ptests.

* Fri Apr 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-15
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- Cleaning-up spec. License verified.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.0.1-12
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.0.1-11
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-8
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-7
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 01 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-1
- Initial package
