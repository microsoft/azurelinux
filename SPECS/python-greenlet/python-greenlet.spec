%global         modname greenlet

%global _description \
The greenlet package is a spin-off of Stackless, a version of CPython\
that supports micro-threads called "tasklets". Tasklets run\
pseudo-concurrently (typically in a single or a few OS-level threads)\
and are synchronized with data exchanges on "channels".

Summary:        Lightweight in-process concurrent programming
Name:           python-%{modname}
Version:        2.0.2
Release:        1%{?dist}
# Most is MIT except for these, which are under the Python Software License:
# - src/greenlet/slp_platformselect.h
# - src/greenlet/platform/ directory
License:        MIT AND Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/python-greenlet/greenlet
Source0:        %{url}/archive/%{version}/%{modname}-%{version}.tar.gz

BuildRequires:  gcc-c++

%description %{_description}

%package -n     python3-%{modname}
%{?python_provide:%python_provide python3-%{modname}}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{modname} %{_description}

Python 3 version.

%package -n     python3-%{modname}-devel
%{?python_provide:%python_provide python3-%{modname}-devel}
Summary:        C development headers for python3-%{modname}

Requires:       python3-%{modname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{modname}-devel
%{summary}.

Python 3 version.

%prep
%autosetup -n %{modname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%check
PYTHONPATH="%{buildroot}%{python3_sitearch}" %{python3} -m unittest discover greenlet.tests

%files -n python3-%{modname}
%license LICENSE LICENSE.PSF
%doc AUTHORS README.rst
%{python3_sitearch}/%{modname}-*.egg-info
%{python3_sitearch}/%{modname}

%files -n python3-greenlet-devel
%{_includedir}/python%{python3_version}*/%{modname}/

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-1
- Auto-upgrade to 2.0.2 - Azure Linux 3.0 - package upgrades

* Thu Mar 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.2-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 30 2021 Kevin Fenzi <kevin@scrye.com> - 1.1.2-1
- Update to 1.1.2. Fixes rhbz#2008848

* Sat Aug 07 2021 Kevin Fenzi <kevin@scrye.com> - 1.1.1-1
- Update to 1.1.1.
- Fixes rhbz#1990901

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.10

* Mon May 10 2021 Nils Philippsen <nils@tiptoe.de> - 1.1.0-1
- Update to 1.1.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 0.4.17-1
- Update to 0.4.17. Fixes bug #1881455

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 06 2020 Orion Poplawski <orion@nwra.com> - 0.4.16-1
- Update to 0.4.16

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.14-8
- Rebuilt for Python 3.9

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.14-7
- Fix Python 3.9 build

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.14-5
- Subpackages python2-greenlet, python2-greenlet-devel have been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.14-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Kevin Fenzi <kevin@scrye.com> - 0.4.14-1
- Update to 0.4.14.
- Drop upstreamed/no longer needed patches.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.13-4
- Add fix for Python 3.7

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.13-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.13-1
- Update to 0.4.13

* Fri Jan 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.12-1
- Update to 0.4.12

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.11-2
- Rebuild for Python 3.6

* Sun Dec 11 2016 Kevin Fenzi <kevin@scrye.com> - 0.4.11-1
- Update to 0.4.11. Fixes bug #1403514

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 25 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9
- Use %license macro
- Follow new RPM Packaging guidelines
- Cleanups in spec

* Fri Aug 21 2015 Kevin Fenzi <kevin@scrye.com> 0.4.7-2
- Re-enable tests on secondary arches. Fixes #1252899
- Applied patch to build on ppc64le. Fixes #1252900

* Fri Jun 26 2015 Kevin Fenzi <kevin@scrye.com> 0.4.7-1
- Update to 0.4.7. Fixes bug #1235896

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 29 2015 Terje Røsten <terje.rosten@ntnu.no> - 0.4.5-1
- 0.4.5
- Add python3 subpackage
- Ship license files
- Some spec clean ups
- Update fixes FTBFS issue (bz#1106779)
- Add comment about issues on ppc64, s390 & s390x

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Orion Poplawski <orion@cora.nwra.com> 0.4.2-1
- Update to 0.4.2

* Mon Aug 05 2013 Kevin Fenzi <kevin@scrye.com> 0.4.1-1
- Update to 0.4.1
- Fix FTBFS bug #993134

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Pádraig Brady <P@draigBrady.com> - 0.4.0-1
- Update to 0.4.0

* Thu Oct 11 2012 Pádraig Brady <P@draigBrady.com> - 0.3.1-11
- Add support for ppc64

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Dan Horák <dan[at]danny.cz> - 0.3.1-8
- disable tests also for s390(x)

* Thu Nov 17 2011 Pádraig Brady <P@draigBrady.com> - 0.3.1-7
- Fix %%check quoting in the previous comment which when
  left with a single percent sign, pulled in "unset DISPLAY\n"
  into the changelog

* Mon Oct 24 2011 Pádraig Brady <P@draigBrady.com> - 0.3.1-6
- cherrypick 25bf29f4d3b7 from upstream (rhbz#746771)
- exclude the %%check from ppc where the tests segfault

* Wed Oct 19 2011 David Malcolm <dmalcolm@redhat.com> - 0.3.1-5
- add a %%check section
- cherrypick 2d5b17472757 from upstream (rhbz#746771)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 14 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-2
- Splitted headers into a -devel package.

* Fri Apr 09 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-1
- Initial package version.
