
%global srcname dulwich
%global __provides_exclude_from ^(%{python3_sitearch}/.*\\.so)$

Name:           python-%{srcname}
Version:        0.21.7
Release:        6%{?dist}
Summary:        Python implementation of the Git file formats and protocols

License:        GPL-2.0-or-later OR Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.dulwich.io/
Source0:        %{pypi_source}#/%{name}-%{version}.tar.gz

BuildRequires:  gcc

%description
Dulwich is a pure-Python implementation of the Git file formats and
protocols. The project is named after the village in which Mr. and
Mrs. Git live in the Monty Python sketch.

%package -n python3-%{srcname}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Dulwich is a pure-Python implementation of the Git file formats and
protocols. The project is named after the village in which Mr. and
Mrs. Git live in the Monty Python sketch.

%package -n %{name}-doc
Summary:        The %{name} documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-docutils
BuildRequires:  python3-sphinx-epytext

%description -n %{name}-doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build
PYTHONPATH=${PWD} sphinx-build-3 docs html
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install
# Remove extra copy of text docs
rm -rf %{buildroot}%{python3_sitearch}/docs/tutorial/

#%check
# FIXME test_non_ascii fails cause of unicode issue
#nosetests -e non_ascii -w dulwich/tests -v

%files -n python3-%{srcname}
%doc AUTHORS README.rst
%license COPYING
%{_bindir}/dul-*
%{_bindir}/%{srcname}
%{python3_sitearch}/%{srcname}*
%exclude %{python3_sitearch}/%{srcname}/tests*

%files -n %{name}-doc
%doc AUTHORS README.rst
%license COPYING
%doc html

%changelog
* Fri Jan 17 2025 Akhila Guruju <v-guakhila@microsoft.com> - 0.21.7-6
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.21.7-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Joel Capitao <jcapitao@redhat.com> - 0.21.7-1
- Update to latest upstream release 0.21.7 (closes rhbz#2236973)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.21.5-2
- Rebuilt for Python 3.12

* Mon May 22 2023 Fabian Affolter <mail@fabian-affolter.ch> - 0.21.5-1
- Upgrade to latest upstream release 0.21.5 (closes rhbz#2193005)

* Sun Feb 19 2023 Fabian Affolter <mail@fabian-affolter.ch> - 0.21.3-1
- Upgrade to latest upstream release 0.21.3 (closes rhbz#2170942)

* Wed Jan 25 2023 Fabian Affolter <mail@fabian-affolter.ch> - 0.21.2-1
- Upgrade to latest upstream release 0.21.2 (closes rhbz#2138585)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 13 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.46-1
- Update to latest upstream release 0.20.46 (closes rhbz#2124623)

* Fri Aug 19 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.45-1
- Update to latest upstream release 0.20.45 (closes rhbz#2107737)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.44-1
- Update to latest upstream release 0.20.44 (closes rhbz#2102830)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.20.43-2
- Rebuilt for Python 3.11

* Tue Jun 07 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.43-1
- Update to latest upstream release 0.20.43 (closes rhbz#2089721)

* Thu May 19 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.40-1
- Update to latest upstream release 0.20.40 (closes rhbz#2086840)

* Sun May 15 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.36-1
- Update to latest upstream release 0.20.36 (closes rhbz#2086300)

* Sun Mar 20 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.35-1
- Update to latest upstream release 0.20.35 (closes rhbz#2066021)

* Thu Mar 17 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.34-1
- Update to latest upstream release 0.20.34 (closes rhbz#2064048)

* Sun Mar 06 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.33-1
- Update to latest upstream release 0.20.33 (closes rhbz#2061090)

* Mon Jan 24 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.32-1
- Update to latest upstream release 0.20.31 (closes rhbz#2044558)

* Fri Jan 21 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.31-1
- * Fri Jan 21 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.31-1 -
  Update to latest upstream release 0.20.31 (closes rhbz#2037101)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 27 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.25-2
- Update bug id

* Fri Aug 27 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.25-1
- * Fri Aug 27 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.25-1 -
  Update to latest upstream release 0.20.25 (closes rhbz#1923878)

* Wed Aug 25 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.24-1
- * Wed Aug 25 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.24-1 -
  Update to latest upstream release 0.20.24 (rhbz#1925135)

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.23-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.20.23-2
- Rebuilt for Python 3.10

* Tue May 25 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.23-1
- * Tue May 25 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.23-1 -
  Update to latest upstream version 0.20.23 (#1925135)

* Sat Feb 06 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.18-1
- * Sat Feb 06 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.18-1 -
  Update to latest upstream release 0.20.18 (#1925135)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.15-1
- * Wed Dec 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.15-1 -
  Update to latest upstream release 0.20.15 (#1910183)

* Fri Nov 27 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.14-1
- * Mon Nov 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.14-1 -
  Update to latest upstream release 0.20.14 (#1902106)

* Mon Nov 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.13-2
- Fix name

* Mon Nov 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.13-1
- * Mon Nov 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.13-1 -
  CLI part was fixed by upstream (#1866463) - Update to latest upstream
  release 0.20.13 (#1900385)

* Fri Oct 30 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.11-1
- * Fri Oct 30 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.11-1 -
  Update to latest upstream release 0.20.11 (#1893055)

* Mon Aug 31 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.6-1
- * Mon Aug 31 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.6-1 -
  Update to latest upstream release 0.20.6 (rhbz#1873748)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.5-2
- * Fri Jun 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.5-2 -
  Add python3-setuptools as BR

* Mon Jun 22 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.5-1
- * Mon Jun 22 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.5-1 -
  Update to latest upstream release 0.20.5 (rhbz#1846933)

* Mon Jun 15 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.3-1
- * Mon Jun 15 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.3-1 -
  Update to latest upstream release 0.20.3 (rhbz#1846933)

* Mon Jun 01 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.2-1
- * Mon Jun 01 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.2-1 -
  Update to latest upstream release 0.20.2 (rhbz#1842651)

* Sat May 23 2020 Miro Hrončok <miro@hroncok.cz> - 0.19.16-2
- Rebuilt for Python 3.9

* Sat Apr 18 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.19.16-1
- * Sat Apr 18 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.19.16-1 -
  Update to latest upstream release 0.19.16 (rhbz#1825352)

* Fri Feb 28 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.19.15-3
- RPMAUTOSPEC: unresolvable merge

