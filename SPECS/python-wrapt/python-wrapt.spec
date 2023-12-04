# Created by pyp2rpm-1.1.1
%global sname wrapt
%global with_docs 1
%{!?_licensedir: %global license %%doc}
%global _description\
The aim of the wrapt module is to provide a transparent object proxy\
for Python, which can be used as the basis for the construction of\
function wrappers and decorator functions.
Summary:        A Python module for decorators, wrappers and monkey patching
Name:           python-%{sname}
Version:        1.15.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/GrahamDumpleton/wrapt
Source0:        https://github.com/GrahamDumpleton/%{sname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  python3-devel

%description %{_description}

%if 0%{?with_docs}
%package doc
Summary:        Documentation for the wrapt module
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%description doc
Documentation for the wrapt module
%endif

%package -n python3-wrapt
%{?python_provide:%python_provide python3-wrapt}
Summary:        A Python module for decorators, wrappers and monkey patching

%description -n python3-wrapt
The aim of the wrapt module is to provide a transparent object proxy
for Python, which can be used as the basis for the construction of
function wrappers and decorator functions.

%prep
%setup -q -n %{sname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{sname}.egg-info

%build
%py3_build

%if 0%{?with_docs}
# for docs
pushd docs
sphinx-build -b html -d build/doctrees . build/html
popd
%endif

%install
%py3_install

%if 0%{?with_docs}
%files doc
%doc docs/build/html
%endif

%files -n python3-wrapt
%doc README.rst
%license LICENSE
%{python3_sitearch}/%{sname}
%{python3_sitearch}/%{sname}-%{version}-py?.?.egg-info

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.15.0-1
- Auto-upgrade to 1.15.0 - Azure Linux 3.0 - package upgrades

* Wed Nov 30 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.11.2-7
- Move to Core.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Miro Hrončok <mhroncok@redhat.com> - 1.11.2-4
- Subpackage python2-wrapt has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.11.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 22 2019 Kevin Fenzi <kevin@scrye.com> - 1.11.2-1
- Update to 1.11.2. Fixes bug #1667650

* Thu Feb 07 2019 Javier Peña <jpena@redhat.com> - 1.11.1-1
- Update to upstream 1.11.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.10.11-4
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.10.11-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 17 2017 Kevin Fenzi <kevin@scrye.com> - 1.10.11-1
- Update to 1.10.11. Fixes bug #1480582

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 1.10.10-5
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.10.10-4
- Python 2 binary package renamed to python2-wrapt
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Ralph Bean <rbean@redhat.com> - 1.10.10-1
- new version

* Wed Mar 15 2017 Ralph Bean <rbean@redhat.com> - 1.10.9-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.10.8-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.8-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 15 2016 Kevin Fenzi <kevin@scrye.com> - 1.10.8-1
- Update to 1.10.8. Fixes bug #1325923

* Mon Apr 04 2016 Ralph Bean <rbean@redhat.com> - 1.10.7-1
- new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Jul 06 2015 Ralph Bean <rbean@redhat.com> - 1.10.5-1
- new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 15 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-6
- Don't build docs on epel7 (the rtd theme is problematic).

* Sat Apr 11 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-5
- Add python3 subpackage

* Wed Mar 25 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-4
- Added doc files for doc subpackage

* Wed Mar 25 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-3
- Fixed Docs

* Tue Mar 24 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-2
- Removed cflags and group section fro doc subpackage

* Tue Mar 24 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-1
- Bumped to upstream version 1.10.4
- Add docs

* Wed Mar 11 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.2-1
- Initial package.
