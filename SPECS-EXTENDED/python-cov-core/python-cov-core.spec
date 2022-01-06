%{?python_enable_dependency_generator}
# Created by pyp2rpm-1.0.1
%global pypi_name cov-core
%global summary Plugin core for use by pytest-cov, nose-cov and nose2-cov
%global _description \
This is a lib package for use by pytest-cov, nose-cov and nose2-cov. \
If you're developing a coverage plugin for a test framework then you \
probably want one of those.

Name:           python-%{pypi_name}
Version:        1.15.0
Release:        21%{?dist}
Summary:        %{summary}

License:        MIT
URL:            http://bitbucket.org/memedough/cov-core/overview
# url Source seems to be broken
Source0:        https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
 
%description %{_description}

# Python3
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
%if %{undefined __pythondist_requires}
Requires:       python%{python3_pkgversion}-coverage >= 3.6
%endif

%description -n python%{python3_pkgversion}-%{pypi_name} %{_description}

%if 0%{?with_python3_other}
%package -n python%{python3_other_pkgversion}-%{pypi_name}
Summary: %{summary}
BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{pypi_name}}
%if %{undefined __pythondist_requires}
Requires: python%{python3_other_pkgversion}-coverage >= 3.6
%endif

%description -n python%{python3_other_pkgversion}-%{pypi_name} %{_description}
%endif


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%py3_build
%if 0%{?with_python3_other}
%py3_other_build
%endif


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3_other}
%py3_other_install
%endif
%py3_install


# Python3
%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/cov_core*
%{python3_sitelib}/__pycache__/*

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{python3_other_sitelib}/cov_core*
%{python3_other_sitelib}/__pycache__/*
%endif


%changelog
* Wed Jan 5 2022 Cameron Baird <cameronbaird@microsoft.com>  - 1.15.0-21
- Add to SPECS-EXTENDED from Fedora

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-19
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-17
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-16
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 04 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.15.0-13
- Enable python dependency generator

* Fri Jan 04 2019 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-12
- Remove python2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-10
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.15.0-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 25 2017 Aurelien Bompard <abompard@fedoraproject.org> - 1.15.0-6
- Build the Python3 version in EPEL.
- Use the proper Python namespace.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.15.0-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 bkabrda <bkabrda@redhat.com> - 1.15.0-1
- Updated to 1.15.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Sep 16 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.7-2
- Add BR: python-setuptools.

* Thu Sep 05 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.7-1
- Initial package.
