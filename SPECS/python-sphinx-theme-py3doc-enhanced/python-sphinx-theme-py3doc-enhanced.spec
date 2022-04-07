%global pypi_name sphinx_py3doc_enhanced_theme
%global srcname sphinx-py3doc-enhanced-theme
%global pkgname sphinx-theme-py3doc-enhanced
%global desc Theme based on the theme of https://docs.python.org/3/ with some responsive\
enhancements.
Summary:        Theme based on the theme of https://docs.python.org/3/
Name:           python-%{pkgname}
Version:        2.4.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/sphinx_py3doc_enhanced_theme
Source0:        https://pypi.io/packages/source/s/%{pypi_name}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description
%{desc}

%package -n     python%{python3_pkgversion}-%{pkgname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-xml
Provides:       python%{python3_pkgversion}-%{pypi_name} = %{version}-%{release}
BuildArch:      noarch

%description -n python%{python3_pkgversion}-%{pkgname}
%{desc}

%prep
%setup -q -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{pypi_name}/

%changelog
* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.0-1
- Updating to version 2.4.0.

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 2.3.2-20
- License verified

* Sun Oct 18 2020 Steve Laughman <steve.laughman@microsoft.com> - 2.3.2-19
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.3.2-17
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.2-15
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.2-14
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.3.2-11
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.3.2-9
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.3.2-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.2-4
- Rebuild for Python 3.6

* Sat Sep 03 2016 Julien Enselme <jujens@jujens.eu> - 2.3.2-3
- Change package name to python-sphinx-theme-py3doc-enhanced
- Add provides for python-sphinx_py3doc_enhanced_theme

* Mon Aug 22 2016 Julien Enselme <jujens@jujens.eu> - 2.3.2-2
- Use %%desc macro for description

* Wed Aug 17 2016 Julien Enselme <jujens@jujens.eu> - 2.3.2-1
- Initial packaging
