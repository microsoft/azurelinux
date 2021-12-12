Vendor:         Microsoft Corporation
Distribution:   Mariner
%global modname isort

Name:               python-%{modname}
Version:            4.3.21
Release:            8%{?dist}
Summary:            Python utility / library to sort Python imports

License:            MIT
URL:                https://github.com/timothycrosley/%{modname}
Source0:            %{url}/archive/%{version}-2/%{modname}-%{version}-2.tar.gz
BuildArch:          noarch

%description
%{summary}.

%package -n python%{python3_pkgversion}-%{modname}
Summary:            %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}
BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      python%{python3_pkgversion}-setuptools
BuildRequires:      python%{python3_pkgversion}-mock
BuildRequires:      python%{python3_pkgversion}-pytest
# Explicitly conflict with the python2 package that used to ship
# /usr/bin/isort. Drop the conflict in F32.
Conflicts:          python2-%{modname} < 4.3.4-7

%description -n python%{python3_pkgversion}-%{modname}
%{summary}.

Python %{python3_pkgversion} version.

%prep
%autosetup -n %{modname}-%{version}-2

# Drop shebang
sed -i -e '1{\@^#!.*@d}' %{modname}/main.py
chmod -x LICENSE

%build
%py3_build

%install
%py3_install
mv %{buildroot}%{_bindir}/%{modname}{,-%{python3_version}}
ln -s %{modname}-%{python3_version} %{buildroot}%{_bindir}/%{modname}-%{python3_pkgversion}
ln -s %{modname}-3 %{buildroot}%{_bindir}/%{modname}

# Re-enable once pylama is in Fedora.
#%check
#%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{modname}
%doc README.rst *.md
%license LICENSE
%{_bindir}/%{modname}
%{_bindir}/%{modname}-%{python3_pkgversion}
%{_bindir}/%{modname}-%{python3_version}
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-*.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.3.21-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.3.21-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 4.3.21-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.21-3
- ACTUALLY fix it.

* Fri Jun 28 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.21-2
- Fix Source URL for  1725224.

* Wed Jun 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.21-1
- 4.3.21-2

* Wed May 15 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.20-1
- 4.3.20

* Mon May 13 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.19-1
- 4.3.19

* Thu May 02 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.18-1
- 4.3.18

* Mon Apr 08 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.17-1
- 4.3.17

* Mon Mar 25 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.16-1
- 4.3.16

* Mon Mar 11 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.15-1
- 4.3.15

* Fri Mar 08 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.13-1
- 4.3.13

* Wed Mar 06 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.12-1
- 4.3.12

* Wed Mar 06 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.11-1
- 4.3.11

* Mon Mar 04 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.10-1
- 4.3.10

* Tue Feb 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.9-1
- 4.3.9

* Mon Feb 25 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.6-1
- 4.3.6

* Mon Feb 11 2019 Kalev Lember <klember@redhat.com> - 4.3.4-8
- Explicitly conflict with the python2 package that used to ship /usr/bin/isort

* Fri Feb 08 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.3.4-7
- Drop python2 support.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 4.3.4-4
- Rebuilt for Python 3.7

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 4.3.4-3
- Rebuilt for Python 3.7

* Tue May 22 2018 Avram Lubkin <aviso@rockhopper.net> - 4.3.4-2
- Add futures as a dependency for Python 2 package

* Mon Feb 12 2018 Gwyn Ciesla <limburgher@gmail.com> - 4.3.4-1
- 4.3.4.

* Thu Feb 08 2018 Gwyn Ciesla <limburgher@gmail.com> - 4.3.3-1
- 4.3.3.

* Sat Feb 03 2018 Gwyn Ciesla <limburgher@gmail.com> - 4.3.1-1
- 4.3.1.

* Fri Feb 02 2018 Gwyn Ciesla <limburgher@gmail.com> - 4.3.0-1
- 4.3.0.

* Fri Jan 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.2.15-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Gwyn Ciesla <limburgher@gmail.com> - 4.2.15-1
- 4.2.15, BZ 1460466.

* Tue Jun 06 2017 Gwyn Ciesla <limburgher@gmail.com> - 4.2.14-1
- 4.2.14, BZ 1459144.

* Mon Jun 05 2017 Gwyn Ciesla <limburgher@gmail.com> - 4.2.13-1
- 4.2.13, BZ 1458494.

* Fri Jun 02 2017 Gwyn Ciesla <limburgher@gmail.com> - 4.2.12-1
- 4.2.12, BZ 1458262.

* Thu Jun 01 2017 Gwyn Ciesla <limburgher@gmail.com> - 4.2.8-1
- 4.2.8, BZ 1457715.

* Thu Mar 9 2017 Orion Poplawski <orion@cora.nwra.com> - 4.2.5-8
- Enable EPEL7 build

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Stratakis Charalampos <cstratak@redhat.com> - 4.2.5-6
- Rebuild for Python 3.6

* Wed Aug 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.2.5-5
- Modernize spec

* Tue Aug 09 2016 Jon Ciesla <limburgher@gmail.com> - 4.2.5-4
- Fix python binary versioning again.

* Tue Aug 09 2016 Jon Ciesla <limburgher@gmail.com> - 4.2.5-3
- Fix python binary versioning again.

* Mon Aug 08 2016 Jon Ciesla <limburgher@gmail.com> - 4.2.5-2
- Switch to github.
- Fix python binary versioning.
- Run tests.

* Fri Jul 29 2016 Jon Ciesla <limburgher@gmail.com> - 4.2.5-1
- Initial package.
