Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Python serial port access library
Name: pyserial
Version: 3.4
Release: 8%{?dist}
Source0: %pypi_source
License: Python
URL: https://pypi.python.org/pypi/pyserial
BuildRequires: python3-devel
BuildArch: noarch

%global _description\
This module encapsulates the access for the serial port. It provides backends\
for standard Python running on Windows, Linux, BSD (possibly any POSIX\
compliant system) and Jython. The module named "serial" automatically selects\
the appropriate backend.

%description %_description


%package -n python3-pyserial
Summary: %{summary}
Conflicts: python2-pyserial < 3.4-6

%description -n python3-pyserial %_description


%prep
export UNZIP="-aa"
%setup -q


%build
%py3_build


%install
%py3_install
mv %{buildroot}/%{_bindir}/miniterm.py %{buildroot}/%{_bindir}/miniterm-3.py
ln -sf %{_bindir}/miniterm-3.py %{buildroot}/%{_bindir}/miniterm-%{python3_version}.py
ln -sf %{_bindir}/miniterm-3.py %{buildroot}/%{_bindir}/miniterm.py


%files -n python3-pyserial
%doc LICENSE.txt CHANGES.rst README.rst examples
%{python3_sitelib}/*
%{_bindir}/miniterm.py
%{_bindir}/miniterm-3.py
%{_bindir}/miniterm-%{python3_version}.py

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4-6
- Subpackage python2-pyserial has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Eric Smith <brouhaha@fedoraproject.org> - 3.4-1
- Update to latest upstream release.
- Update Source0 and URL to use Pypi.

* Tue Jul 17 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-10
- Update Python macros to new packaging standards
  (See https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-8
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.1.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.1-5
- Python 2 binary package renamed to python2-pyserial
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.1.1-2
- Rebuild for Python 3.6

* Mon Aug 1 2016 Paul Komkoff <i@stingr.net> 3.1.1-1
- new upstream version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Michal Cyprian <mcyprian@redhat.com> - 2.7-3
- Resolve python3 dependency problem, make miniterm.py python2 script, add
  python3 version of the script

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 08 2015 Paul Komkoff <i@stingr.net> 2.7-1
- new upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sat Sep 07 2013 Till Maas <opensource@till.name> - 2.6-7
- Add python3 package

* Sat Sep 07 2013 Paul P. Komkoff <i@stingr.net> - 2.6-6
- patched to allow arbitrary speeds bz#982368

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Paul P. Komkoff Jr <i@stingr.net> - 2.6-1
- new upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Paul P. Komkoff Jr <i@stingr.net> - 2.5-1
- new upstream version

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Oct 18 2009 Paul P Komkoff Jr <i@stingr.net> - 2.4-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.2-7
- Rebuild for Python 2.6

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2-6
- fix license tag

* Tue Dec 12 2006 Paul P. Komkoff Jr <i@stingr.net>
- rebuilt

* Mon Nov  6 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-4
- remove "export libdirname"

* Tue Oct 24 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-3
- Minor specfile fixes

* Sat Oct 14 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-2
- Minor specfile fixes

* Tue May  9 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-1
- Fedora Extras submission
