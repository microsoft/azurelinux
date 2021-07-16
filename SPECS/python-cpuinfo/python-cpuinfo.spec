%global srcname cpuinfo
%global sum Getting CPU info
Summary:        %{sum}
Name:           python-%{srcname}
Version:        7.0.0
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/workhorsy/py-cpuinfo
Source0:        https://files.pythonhosted.org/packages/source/p/py-%{srcname}/py-%{srcname}-%{version}.tar.gz
# https://github.com/workhorsy/py-cpuinfo/issues/55
# ExclusiveArch:  %%{ix86} x86_64 %%{power64} s390x noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
Py-cpuinfo gets CPU info with pure Python. Py-cpuinfo should work without
any extra programs or libraries, beyond what your OS provides.

These approaches are used for getting info:
    Windows Registry
    /proc/cpuinfo
    sysctl
    dmesg
    isainfo and psrinfo
    Querying x86 CPUID register

%package -n python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}
Summary:        %{sum}

%description -n python3-%{srcname}
Py-cpuinfo gets CPU info with pure Python. Py-cpuinfo should work without
any extra programs or libraries, beyond what your OS provides.

These approaches are used for getting info:
    Windows Registry
    /proc/cpuinfo
    sysctl
    dmesg
    isainfo and psrinfo
    Querying x86 CPUID register

%prep
%setup -q -n py-%{srcname}-%{version}
rm -rf *.egg-info

sed -i -e '/^#!\//, 1d' cpuinfo/cpuinfo.py

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
    python%{python3_version} -m pytest -v tests

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%doc ChangeLog
%{_bindir}/cpuinfo
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/py_%{srcname}-%{version}-py3.*.egg-info

%changelog
* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 7.0.0-4
- Update check section to use pytest
- License verified

* Sun Oct 18 2020 Steve Laughman <steve.laughman@microsoft.com> - 7.0.0-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 06 2020 Parag Nemade <pnemade AT redhat DOT com> - 7.0.0-1
- Update to 7.0.0 version (#1853940)

* Thu Jun 11 2020 Parag Nemade <pnemade AT redhat DOT com> - 6.0.0-1
- Update to 6.0.0 version (#1846323)

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 5.0.0-2
- Drop the versioned binary and restore to original path name

* Sat Mar 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 5.0.0-1
- Update to 5.0.0 version (#1691106)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Parag Nemade <pnemade AT redhat DOT com> - 4.0.0-4
- Remove python2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-2
- Rebuilt for Python 3.7

* Wed Apr 04 2018 Parag Nemade <pnemade AT redhat DOT com> - 4.0.0-1
- Update to 4.0.0 version (#1563228)

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.3.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.3.0-1
- Update to 3.3.0 version

* Thu Apr 20 2017 Than Ngo <than@redhat.com> - 3.2.0-2
- added s390x support
- enable all supported archs

* Thu Apr 20 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.2.0-1
- Update to 3.2.0 version

* Sun Apr 09 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.0.0-1
- Update to 3.0.0 version

* Tue Mar 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.7-3
- One more attempt to fix the ExclusiceArch: tag (Thanks sharckcz)

* Tue Mar 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.7-2
- Resolves:rh#1409636 - python-cpuinfo does not support aarch64, ppc64
  and ppc64le, and s390/s390x 

* Tue Mar 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.7-1
- Update to 0.2.7 version

* Sun Mar 12 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.6-1
- Update to 0.2.6 version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 25 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.2.3-2
- Thanks to Petr Viktorin (rh#1330005) for correcting dependencies

* Sat Apr 23 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.2.3-1
- Update to 0.2.3 release (rh#1311530)
- Added %%license tag

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.8-1
- Update to 0.1.8 release (rh#1292653)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Jul 13 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.6-1
- Update to 0.1.6 release (rh#1242523)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.4-1
- Update to 0.1.4 release
- Resolves:rh#1190549 - cpuinfo failed to run

* Tue Feb 03 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.2-3
- Resolves:rh#1178548, follow dnf way to use py3 binary

* Fri Oct 03 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.2-2
- Clean the spec to follow py3 guidelines

* Wed Oct 01 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.2-1
- Update to 0.1.2 release

* Mon Sep 22 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.0-2
- fix rpmlint messages
- Added upstream LICENSE file not in tarball

* Mon Sep 22 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.0-1
- Initial packaging
