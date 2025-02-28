Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global modname isort

Name:               python-%{modname}
Version:            5.13.2
Release:            6%{?dist}
Summary:            Python utility / library to sort Python imports

License:            MIT
URL:                https://github.com/timothycrosley/%{modname}
Source0:            https://files.pythonhosted.org/packages/87/f9/c1eb8635a24e87ade2efce21e3ce8cd6b8630bb685ddc9cdaca1349b2eb5/%{modname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:          noarch

%description
%{summary}.

%package -n python%{python3_pkgversion}-%{modname}
Summary:            %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}
BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      python%{python3_pkgversion}-setuptools
BuildRequires:      python%{python3_pkgversion}-pytest
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description -n python%{python3_pkgversion}-%{modname}
%{summary}.

Python %{python3_pkgversion} version.

%prep
%autosetup -n %{modname}-%{version}

# Drop shebang
#sed -i -e '1{\@^#!.*@d}' %{modname}/main.py
#chmod -x LICENSE

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
%doc *.md
%license LICENSE
%{_bindir}/%{modname}
%{_bindir}/%{modname}-%{python3_pkgversion}
%{_bindir}/%{modname}-%{python3_version}
%{_bindir}/%{modname}-identify-imports
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-*.egg-info/

%changelog
* Thu Feb 27 2025 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 5.13.2-6
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.13.2-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 5.13.2-1
- 5.13.2

* Tue Dec 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 5.13.1-1
- 5.13.1

* Mon Dec 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 5.13.0-1
- 5.13.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 5.12.0-3
- Rebuilt for Python 3.12

* Wed Mar 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 5.12.0-2
- migrated to SPDX license

* Mon Jan 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 5.12.0-1
- 5.12.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 5.11.4-1
- 5.11.4

* Mon Dec 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 5.11.3-1
- 5.11.3

* Thu Dec 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 5.11.2-1
- 5.11.2

* Tue Dec 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 5.11.1-1
- 5.11.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.10.1-4
- Rebuilt for Python 3.11

* Sat Jun 11 2022 Tom Rix <trix@redhat.com> - 5.10.1-3
- Remove python-mock BuildRequires

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 5.10.1-1
- 5.10.1

* Wed Nov 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 5.10.0-1
- 5.10.0

* Thu Jul 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 5.9.3-1
- 5.9.3

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 5.9.2-1
- 5.9.2

* Mon Jun 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 5.9.1-1
- 5.9.1

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 5.8.0-2
- Rebuilt for Python 3.10

* Mon Mar 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 5.8.0-1
- 5.8.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.7.0-1
- 5.7.0

* Tue Oct 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.6.4-1
- 5.6.4

* Sun Oct 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.6.3-1
- 5.6.3

* Sat Oct 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.6.2-1
- 5.6.2

* Thu Oct 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.6.1-1
- 5.6.1

* Wed Sep 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.5.4-1
- 5.5.4

* Mon Sep 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.5.3-1
- 5.5.3

* Thu Sep 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.5.2-1
- 5.5.2

* Fri Sep 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.5.1-1
- 5.5.1

* Thu Sep 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.5.0-1
- 5.5.0

* Mon Aug 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.4.2-1
- 5.4.2

* Thu Aug 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.4.1-1
- 5.4.1

* Thu Aug 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.4.0-1
- 5.4.0

* Fri Aug 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.3.2-1
- 5.3.2

* Wed Aug 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.3.0-1
- 5.3.0

* Thu Jul 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.2.2-1
- 5.2.2

* Mon Jul 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.2.0-1
- 5.2.0

* Mon Jul 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.1.4-1
- 5.1.4

* Thu Jul 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.1.1-1
- 5.1.1

* Wed Jul 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.1.0-1
- 5.1.0

* Mon Jul 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.0.9-1
- 5.0.9

* Fri Jul 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.0.7-1
- 5.0.7

* Thu Jul 09 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.0.6-1
- 5.0.6

* Wed Jul 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 5.0.5-1
- 5.0.5

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 4.3.21-8
- Rebuilt for Python 3.9

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
