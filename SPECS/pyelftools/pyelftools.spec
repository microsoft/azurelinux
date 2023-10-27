%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
# main package is archful to run tests everywhere but produces noarch packages
%global         debug_package %{nil}

Name:           pyelftools
Version:        0.29
Release:        1%{?dist}
Summary:        Pure-Python library for parsing and analyzing ELF files
License:        Public Domain AND MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/eliben/pyelftools
Source0:        https://github.com/eliben/pyelftools/archive/v%{version}/%{name}-%{version}.tar.gz
%global _description \
Pure-Python library for parsing and analyzing ELF files\
and DWARF debugging information.
%description   %_description

%package     -n python3-%{name}
Summary:	%{summary}
# https://github.com/eliben/pyelftools/issues/180
Provides:	bundled(python3-construct) = 2.6
BuildRequires:  binutils
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch
%{?python_provide:%python_provide python3-%{name}}
%description -n python3-%{name} %_description

%prep
%setup -q
%ifnarch x86_64
rm test/external_tools/readelf
%endif

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd %{buildroot}%{_bindir}
mv readelf.py pyreadelf-%{python3_version}
ln -s pyreadelf-%{python3_version} pyreadelf-3
ln -s pyreadelf-3 pyreadelf
popd

%check
python3 test/run_all_unittests.py
python3 test/run_examples_test.py
# tests may fail because of differences in output-formatting
# from binutils' readelf.  See:
# https://github.com/eliben/pyelftools/wiki/Hacking-guide#tests
python3 test/run_readelf_tests.py || :

%files -n python3-%{name}
%license LICENSE
%doc CHANGES
%{_bindir}/pyreadelf
%{_bindir}/pyreadelf-%{python3_version}
%{_bindir}/pyreadelf-3
%{python3_sitelib}/elftools
%{python3_sitelib}/pyelftools-*.egg-info

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.29-1
- Auto-upgrade to 0.29 - Azure Linux 3.0 - package upgrades

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.27-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 30 2020 Dominik Mierzejewski <rpm@greysector.net> - 0.27-1
- update to 0.27 (#1891845)
- run readelf tests on all arches

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.26-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Dominik Mierzejewski <rpm@greysector.net> - 0.26-1
- update to 0.26 (#1780153)
- make main package archful to run tests on all arches
  (pythonN-pyelftools subpackages are still noarch)
- run readelf tests on x86_64 only for now
- rename binaries to conform to Python packaging guidelines
- enable python3 subpackage for EPEL7
- declare bundled old construct module instead of needlessly requiring it

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.25-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.25-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Terje Rosten <terje.rosten@ntnu.no> - 0.25-2
- Still support Python 2 on Fedora 31

* Sun May 05 2019 Terje Rosten <terje.rosten@ntnu.no> - 0.25-1
- 0.25
- Use bundled construct as construct 2.9 is incompatible
- Drop Python 2 stuff on el8 and Python 31 or newer

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.24-2
- Rebuilt for Python 3.7

* Sun Jun 17 2018 Terje Rosten <terje.rosten@ntnu.no> - 0.24-1
- 0.24
- some clean up
- remove naked provide for Fedora 29 and later
- switch to Python 3 for pyreadelf for Fedora 29 and later

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.22-0.16.git20130619.a1d9681
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-0.15.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.22-0.14.git20130619.a1d9681
- Python 2 binary package renamed to python2-pyelftools
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-0.13.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-0.12.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-0.11.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.22-0.10.git20130619.a1d9681
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-0.9.git20130619.a1d9681
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-0.8.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-0.7.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-0.6.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-0.5.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-0.4.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.22-0.3.git20130619.a1d9681
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Oct 02 2013 Björn Esser <bjoern.esser@gmail.com> - 0.22-0.2.git20130619.a1d9681
- adaptions for new Python-guidelines

* Fri Aug 16 2013 Björn Esser <bjoern.esser@gmail.com> - 0.22-0.1.git20130619.a1d9681
- update to latest pre-release git snapshot
- add python3-package
- build on all arches to get some conclusion from testsuite,
  but create noarch pkgs

* Sat Jun 08 2013 Terje Rosten <terje.rosten@ntnu.no> - 0.21-2
- Remove bundled construct lib

* Thu May 09 2013 Terje Rosten <terje.rosten@ntnu.no> - 0.21-1
- 0.21
- Run test
- Updated source url
- Drop defattr

* Wed Jun 06 2012 Kushal Das <kushal@fedoraproject.org> 0.20-1
- Intial package (#829676)
