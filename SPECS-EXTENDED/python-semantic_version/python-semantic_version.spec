Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name semantic_version

Name:           python-%{pypi_name}
Version:        2.8.4
Release:        4%{?dist}
Summary:        Library implementing the 'SemVer' scheme

License:        BSD
URL:            https://github.com/rbarrois/python-semanticversion
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%global _description \
This small python library provides a few tools to handle semantic versioning\
in Python.

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
#BuildRequires:  python3-django
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{_description}

Python 3 version

%package doc
Summary:        Documentation for python-%{pypi_name}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%description doc
%{summary}.

%prep
%autosetup -n semantic_version-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# documentation builds due to broken symlink
# https://github.com/rbarrois/python-semanticversion/issues/20
rm docs/credits.rst

%build
%py3_build
# generate html docs
sphinx-build-%{python3_version} docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%check
# Seems like it's just stuck in koji
#{__python3} setup.py test

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst ChangeLog
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info/

%files doc
%license LICENSE
%doc html

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.8.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Feb 20 2020 Javier Peña <jpena@redhat.com> - 2.8.4-3
- Add sphinx_rtd_theme as a buld dependency

* Thu Feb 20 2020 Javier Peña <jpena@redhat.com> - 2.8.4-2
- Fix name in autosetup

* Thu Feb 20 2020 Javier Peña <jpena@redhat.com> - 2.8.4-1
- Update to latest upstream version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-13
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.6.0-9
- Drop python2 subpackage

* Tue Jan 08 2019 Petr Viktorin <pviktori@redat.com> - 2.6.0-8
- Remove Fedora build dependency on a compatibility build of Django
- Use python3-sphinx on Fedora

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-6
- Rebuilt for Python 3.7

* Tue May 29 2018 Javier Peña <jpena@redhat.com> - 2.6.0-5
- Fix build due to Django dependency (bz#1556267)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.6.0-1
- Update to 2.6.0
- Make package to comply guidelines

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 24 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 2.5.0-1
- Upstream 2.5.0
- Add python3 subpackage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 03 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.4.2-1
- Upstream 2.4.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 01 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.4.1-1
- Upstream 2.4.1

* Mon Mar 30 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.3.1-1
- Initial package.
