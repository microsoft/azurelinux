# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global prever b1

%global py2support 0

Name:           python-coverage
Summary:        Code coverage testing module for Python
Version:        7.10.2
Release:        3%{?dist}
# There is a jquery file in tests/ that is MIT OR GPL-2.0-only
# but it does not end up in the binary package
License:        Apache-2.0
URL:            http://nedbatchelder.com/code/modules/coverage.html
Source0:        https://pypi.python.org/packages/source/c/coverage/coverage-%{version}%{?prever}.tar.gz
BuildRequires:  gcc

%description
Coverage.py is a Python module that measures code coverage during Python 
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.

%{?python_extras_subpkg:%python_extras_subpkg -n python%{python3_pkgversion}-coverage -i %{python3_sitearch}/coverage*.egg-info toml}

%if %{py2support}

%package -n python2-coverage
Summary:        Code coverage testing module for Python 2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# As the "coverage" executable requires the setuptools at runtime (#556290),
# so the "python3-coverage" executable requires python3-setuptools:
Requires:       python2-setuptools
%{?python_provide:%python_provide python2-coverage}
Provides:       bundled(js-jquery) = 1.11.1
Provides:       bundled(js-jquery-debounce) = 1.1
Provides:       bundled(js-jquery-hotkeys) = 0.8
Provides:       bundled(js-jquery-isonscreen) = 1.2.0
Provides:       bundled(js-jquery-tablesorter)

%description -n python2-coverage
Coverage.py is a Python 2 module that measures code coverage during Python
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.

%endif

%package -n python%{python3_pkgversion}-coverage
Summary:        Code coverage testing module for Python 3
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# As the "coverage" executable requires the setuptools at runtime (#556290),
# so the "python3-coverage" executable requires python3-setuptools:
Requires:       python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-coverage}
Provides:       bundled(js-jquery) = 1.11.1
Provides:       bundled(js-jquery-debounce) = 1.1
Provides:       bundled(js-jquery-hotkeys) = 0.8
Provides:       bundled(js-jquery-isonscreen) = 1.2.0
Provides:       bundled(js-jquery-tablesorter)
Conflicts:      python2-coverage < 4.5.4-2

%description -n python%{python3_pkgversion}-coverage
Coverage.py is a Python 3 module that measures code coverage during Python
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.

%prep
%setup -q -n coverage-%{version}%{?prever}

find . -type f -exec chmod 0644 \{\} \;
sed -i 's/\r//g' README.rst

%build
%if %{py2support}
%py2_build
%endif
%py3_build

%install
%if %{py2support}
%py2_install
rm %{buildroot}/%{_bindir}/coverage
%endif

%py3_install
rm %{buildroot}/%{_bindir}/coverage

# make compat symlinks
pushd %{buildroot}%{_bindir}
%if %{py2support}
ln -s coverage-%{python2_version} coverage-2
%endif
ln -s coverage-%{python3_version} coverage-3
ln -s coverage-%{python3_version} coverage
popd

%if %{py2support}
%files -n python2-coverage
%license LICENSE.txt NOTICE.txt
%doc README.rst
%{_bindir}/coverage2
%{_bindir}/coverage-2*
%{python2_sitearch}/coverage/
%{python2_sitearch}/coverage*.egg-info/
%endif

%files -n python%{python3_pkgversion}-coverage
%license LICENSE.txt NOTICE.txt
%doc README.rst
%{_bindir}/coverage
%{_bindir}/coverage3
%{_bindir}/coverage-3*
%{python3_sitearch}/coverage/
%{python3_sitearch}/coverage*.egg-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.10.2-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.10.2-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug  4 2025 Tom Callaway <spot@fedoraproject.org> - 7.10.2-1
- update to 7.10.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 7.3.2-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 7.3.2-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct  3 2023 Tom Callaway <spot@fedoraproject.org> - 7.3.2-1
- update to 7.3.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 7.2.7-2
- Rebuilt for Python 3.12

* Mon Jun  5 2023 Tom Callaway <spot@fedoraproject.org> - 7.2.7-1
- update to 7.2.7

* Fri May 26 2023 Tom Callaway <spot@fedoraproject.org> - 7.2.6-1
- update to 7.2.6

* Mon May  1 2023 Tom Callaway <spot@fedoraproject.org> - 7.2.5-1
- update to 7.2.5

* Fri Apr 28 2023 Tom Callaway <spot@fedoraproject.org> - 7.2.4-1
- update to 7.2.4

* Mon Feb 27 2023 Tom Callaway <spot@fedoraproject.org> - 7.2.1-1
- update to 7.2.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Tom Callaway <spot@fedoraproject.org> - 7.0.5-1
- update to 7.0.5
- correct License tag

* Fri Dec 30 2022 Tom Callaway <spot@fedoraproject.org> - 7.0.1-1
- update to 7.0.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Miro Hrončok <mhroncok@redhat.com> - 6.4.2-1
- Update to 6.4.2
- Fix coverage reporting for Python 3.11.0b4+
- Fixes: rhbz#2049354

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.3.3-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 6.3.3-1
- Update to 6.3.3

* Tue Jan 25 2022 Tom Callaway <spot@fedoraproject.org> - 6.3-1
- update to 6.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 05 2021 Orion Poplawski <orion@nwra.com> - 6.2-1
- Update to 6.2

* Mon Oct 04 2021 Charalampos Stratakis <cstratak@redhat.com> - 5.6-0.4b1
- Provide the extra toml package (rhbz#2010422)

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-0.3b1
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 5.6-0.2b1
- Rebuilt for Python 3.10

* Wed Apr 14 2021 Tom Callaway <spot@fedoraproject.org> - 5.6-0.1.b1
- 5.6b1

* Mon Mar  1 2021 Tom Callaway <spot@fedoraproject.org> - 5.5-1
- update to 5.5

* Tue Jan 26 2021 Tom Callaway <spot@fedoraproject.org> - 5.4-1
- update to 5.4

* Wed Dec 30 2020 Tom Callaway <spot@fedoraproject.org> - 5.3.1-1
- update to 5.3.1

* Mon Sep 14 2020 Tom Callaway <spot@fedoraproject.org> - 5.3-1
- update to 5.3

* Thu Aug 13 2020 Tom Callaway <spot@fedoraproject.org> - 5.2.1-1
- update to 5.2.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  9 2020 Tom Callaway <spot@fedoraproject.org> - 5.2-1
- update to 5.2

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 5.1-2
- Rebuilt for Python 3.9

* Mon Apr 13 2020 Tom Callaway <spot@fedoraproject.org> - 5.1-1
- update to 5.1

* Tue Mar 17 2020 Tom Callaway <spot@fedoraproject.org> - 5.0.4-1
- update to 5.0.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Tom Callaway <spot@fedoraproject.org> - 5.0.3-1
- update to 5.0.3

* Mon Jan  6 2020 Tom Callaway <spot@fedoraproject.org> - 5.0.2-1
- update to 5.0.2

* Tue Nov 12 2019 Tom Callaway <spot@fedoraproject.org> - 4.5.4-5
- conditionalize (and disable) python2 support

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.5.4-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 4.5.4-3
- Rebuilt for Python 3.8

* Mon Aug 12 2019 Miro Hrončok <mhroncok@redhat.com> - 4.5.4-2
- Make /usr/bin/coverage Python 3
- Remove /usr/bin/python*-coverage links to cleanse tab completion results
- Drop no longer needed Obsoletes for platform-python-coverage

* Mon Aug  5 2019 Tom Callaway <spot@fedoraproject.org> - 4.5.4-1
- update to 4.5.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Tom Callaway <spot@fedoraproject.org> - 4.5.3-1
- update to 4.5.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 4.5.1-2
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Tom Callaway <spot@fedoraproject.org> - 4.5.1-1
- update to 4.5.1

* Tue Feb  6 2018 Tom Callaway <spot@fedoraproject.org> - 4.5-1
- update to 4.5

* Mon Nov 13 2017 Tom Callaway <spot@fedoraproject.org> - 4.4.2-1
- update to 4.4.2

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.1-6
- Use better Obsoletes for platform-python

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.1-5
- Remove platform-python subpackage
- Cleanup spec

* Tue Aug 08 2017 Miro Hrončok <mhroncok@redhat.com> - 4.4.1-4
- Add platform-python subpackage

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Tom Callaway <spot@fedoraproject.org> - 4.4.1-1
- update to 4.4.1

* Mon May  8 2017 Tom Callaway <spot@fedoraproject.org> - 4.4-1
- update to 4.4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Tom Callaway <spot@fedoraproject.org> - 4.3.3-1
- update to 4.3.3

* Tue Jan 03 2017 Tom Callaway <spot@fedoraproject.org> - 4.3.1-1
- update to 4.3.1

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.2-2
- Rebuild for Python 3.6

* Fri Jul 29 2016 Tom Callaway <spot@fedoraproject.org> - 4.2-1
- 4.2 final

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-0.2.b1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul  5 2016 Tom Callaway <spot@fedoraproject.org> - 4.2-0.1.b1
- update to 4.2b1

* Tue Jun 14 2016 Tom Callaway <spot@fedoraproject.org> - 4.1-1
- update to 4.1

* Wed May 11 2016 Tom Callaway <spot@fedoraproject.org> - 4.1-0.5.b3
- update to 4.1b3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-0.4.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Tom Callaway <spot@fedoraproject.org> - 4.1-0.3.b2
- update to 4.1b2

* Wed Jan 13 2016 Orion Poplawski <orion@cora.nwra.com> - 4.1-0.2.b1
- Fix and install license
- Cleanup and modernize spec
- Note bundled jquery libraries

* Tue Jan 12 2016 Tom Callaway <spot@fedoraproject.org> - 4.1-0.1.b1
- update to 4.1b1

* Mon Nov 30 2015 Tom Callaway <spot@fedoraproject.org> - 4.0.3-1
- update to 4.0.3

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Tom Callaway <spot@fedoraproject.org> - 4.0.2-1
- update to 4.0.2

* Thu Oct 29 2015 Tom Callaway <spot@fedoraproject.org> - 4.0.1-1
- update to 4.0.1

* Mon Sep 28 2015 Tom Callaway <spot@fedoraproject.org> - 4.0-1
- update to 4.0 final

* Wed Sep 23 2015 Robert Kuska <rkuska@redhat.com> - 4.0-0.13.b3
- Rebuilt for Python3.5 rebuild

* Wed Sep  9 2015 Tom Callaway <spot@fedoraproject.org> - 4.0-0.12.b3
- update to 4.0b3

* Fri Aug 28 2015 Tom Callaway <spot@fedoraproject.org> - 4.0-0.11.b2
- update to 4.0b2

* Tue Aug  4 2015 Tom Callaway <spot@fedoraproject.org> - 4.0-0.10.b1
- update to 4.0b1

* Mon Jul 13 2015 Tom Callaway <spot@fedoraproject.org> - 4.0-0.9.a6
- add missing Provides: python2-coverage

* Tue Jul  7 2015 Tom Callaway <spot@fedoraproject.org> - 4.0-0.8.a6
- update to 4.0a6

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.7.a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 04 2015 Ralph Bean <rbean@redhat.com> 4.0-0.6.a5
- No longer run 2to3 on the python3 sources.

* Wed Mar 25 2015 Tom Callaway <spot@fedoraproject.org> 4.0-0.5.a5
- unicode fixup

* Tue Feb 17 2015 Tom Callaway <spot@fedoraproject.org> 4.0-0.4.a5
- update to 4.0a5

* Thu Feb  5 2015 Tom Callaway <spot@fedoraproject.org> 4.0-0.3.a3
- update to 4.0a3

* Tue Jan 20 2015 Tom Callaway <spot@fedoraproject.org> 4.0-0.2.a2
- update to 4.0a2

* Thu Oct  9 2014 Tom Callaway <spot@fedoraproject.org> 4.0-0.1.a
- Update to 4.0a1

* Wed Aug 27 2014 Luke Macken <lmacken@redhat.com> - 3.7.1-1
- Update to 3.7.1 (#1043090)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Orion Poplawski <orion@cora.nwra.com> - 3.7-2
- Rebuild for Python 3.4

* Sun Oct 20 2013 Tom Callaway <spot@fedoraproject.org> - 3.7-1
- update to 3.7
- fix macros for current guidelines
- rename binary (with compat symlinks)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun  7 2013 Tom Callaway <spot@fedoraproject.org> - 3.6-1
- update to 3.6 final

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.3.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Tom Callaway <spot@fedoraproject.org> - 3.6-0.3.b3
- update to 3.6beta3

* Thu Nov 29 2012 Tom Callaway <spot@fedoraproject.org> - 3.6-0.1.b1
- update to 3.6beta1
- patch0 merged into upstream

* Wed Oct 10 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5.3-2
- Patch from upstream for traceback when people use this with python2 and
  python3 in the same directory

* Mon Oct  1 2012 Tom Callaway <spot@fedoraproject.org> - 3.5.3-1
- update to 3.5.3

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.5.2-0.4.b1
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.5.2-0.3.b1
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  2 2012 Tom Callaway <spot@fedoraproject.org> - 3.5.2-0.1.b1
- update to 3.5.2b1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep  2 2011 Tom Callaway <spot@fedoraproject.org> - 3.5.1-0.1.b1
- update to 3.5.1b1

* Mon Jun  6 2011 Tom Callaway <spot@fedoraproject.org> - 3.5-0.1.b1
- update to 3.5b1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010  <David Malcolm <dmalcolm@redhat.com>> - 3.4-2
- rebuild for newer python3

* Thu Oct 21 2010 Luke Macken <lmacken@redhat.com> - 3.4-1
- Update to 3.4 (#631751)

* Fri Sep 03 2010 Luke Macken <lmacken@redhat.com> - 3.3.1-4
- Rebuild against Python 3.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 5 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-2
- Fix license tag, permissions, and filtering extraneous provides

* Wed May 5 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Fri Feb  5 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-3
- add python 3 subpackage (#536948)

* Sun Jan 17 2010 Luke Macken <lmacken@redhat.com> - 3.2-2
- Require python-setuptools (#556290)

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-1
- update to 3.2

* Fri Oct 16 2009 Luke Macken <lmacken@redhat.com> - 3.1-1
- Update to 3.1

* Wed Aug 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.1-1
- update to 3.0.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-2
- fix install invocation

* Wed May 6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-1
- Initial package for Fedora
