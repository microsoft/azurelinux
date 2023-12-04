%global srcname pycosat
%global sum Python bindings to picosat (a SAT solver)
%global pkgdesc \
PicoSAT is a popular SAT solver written by Armin Biere in pure C. This \
package provides efficient Python bindings to picosat on the C level, i.e. \
when importing pycosat, the picosat solver becomes part of the Python process \
itself.
Summary:        %{sum}
Name:           python-%{srcname}
Version:        0.6.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ContinuumIO/pycosat
Source0:        https://github.com/ContinuumIO/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  picosat-devel

%description
%{pkgdesc}

%package -n python%{python3_pkgversion}-%{srcname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Summary:        %{sum}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python%{python3_pkgversion}-%{srcname}
%{pkgdesc}

%prep
%setup -q -n %{srcname}-%{version}
sed -i -e s/distutils.core/setuptools/ setup.py
rm picosat.*

# upstream only applies proper flags when build is invoked with --inplace
sed -i "s/if '--inplace' in sys.argv:/if True:/" setup.py

%build
%py3_build

%install
%py3_install

%check
pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    pytest>=5.4.0 \
    pytest-cov>=2.7.1
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc CHANGELOG README.rst
%{python3_sitearch}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.6.4-1
- Auto-upgrade to 0.6.4 - Azure Linux 3.0 - package upgrades

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 0.6.3-15
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Orion Poplawski <orion@nwra.com> - 0.6.3-12
- Add BR on python-setuptools

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.6.3-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.3-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.3-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 7 2018 Orion Poplawski <orion@nwra.com> - 0.6.3-5
- Drop Python 2 package for Fedora 30+ (bugz #1634962)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.3-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 5 2018 Orion Poplawski <orion@cora.nwra.com> - 0.6.3-1
- Update to 0.6.3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr 19 2016 Orion Poplawski <orion@cora.nwra.com> - 0.6.1-7
- Build python3 packages for EPEL7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Jerry James <loganjerry@gmail.com> - 0.6.1-5
- Rebuild for picosat 965

* Sun Jan 3 2016 Orion Poplawski <orion@cora.nwra.com> - 0.6.1-4
- Fix PYTHONPATH in %%check

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Sep 22 2015 Orion Poplawski <orion@cora.nwra.com> - 0.6.1-2
- Quiet setup

* Mon Sep 21 2015 Orion Poplawski <orion@cora.nwra.com> - 0.6.1-1
- Initial package
