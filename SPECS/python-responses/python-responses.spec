%global srcname responses

Summary:        Reusable django app for collecting and visualizing network topology
Name:           python-%{srcname}
Version:        0.10.15
Release:        4%{?dist}
License:        ASL 2.0
URL:            https://github.com/getsentry/responses
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-requests
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-mock
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
A utility library for mocking out the requests Python library.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%if %{undefined __pythondist_requires}
Requires:       python%{python3_pkgversion}-requests
Requires:       python%{python3_pkgversion}-six
%endif

%description -n python%{python3_pkgversion}-%{srcname}
A utility library for mocking out the requests Python library.

%prep
%setup -q -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

# skipping tests due to missing dependencies: python-pytest-localserver
%check
pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    pytest>=5.4.0 \
    pytest-localserver
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/__pycache__/%{srcname}.*.pyc

%changelog
* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 0.10.15-4
- Initial CBL-Mariner version imported from Fedora 34 (license: MIT)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 14 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.15-1
- Version update

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.14-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.14-1
- Version update

* Wed Mar 04 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.12-1
- Version update

* Sat Feb 29 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.11-1
- Version update

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.10.5-1
- Upgrade to 0.10.5 (#1684241).
- https://github.com/getsentry/responses/blob/0.10.5/CHANGES

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-5
- Enable python dependency generator

* Fri Dec 28 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-4
- Subpackage python2-responses has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-2
- Rebuilt for Python 3.7

* Mon Apr 09 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.9.0-1
- Version update
- Explicitly require pythonX-setuptools regardless of environment

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.1-7
- Escape macros in %%changelog

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 02 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.1-2
- Fixed python packages prefix for el <= 7

* Mon Jan 25 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.1-1
- LICENSE file added in upstream update
- Commented %%check section due test file missing in pypi release. See https://github.com/getsentry/responses/issues/98

* Sat Jan 23 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.0-1
- Package review submission
