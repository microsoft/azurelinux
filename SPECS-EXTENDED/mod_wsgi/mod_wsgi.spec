%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%bcond_with python2
%else
%bcond_with python3
%bcond_without python2
%endif

Name:           mod_wsgi
Version:        5.0.2
Release:        1%{?dist}
Summary:        A WSGI interface for Python web applications in Apache
License:        Apache-2.0 AND CC-BY-3.0
URL:            https://modwsgi.readthedocs.io/
Source0:        https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}.tar.gz#/mod_wsgi-%{version}.tar.gz
Source1:        wsgi.conf
Source2:        wsgi-python3.conf
Patch1:         mod_wsgi-4.5.20-exports.patch

BuildRequires:  httpd-devel
BuildRequires:  gcc
BuildRequires:  make

# Suppress auto-provides for module DSO
%global __provides_exclude_from %{_httpd_moddir}/.*\\.so$

%global _description\
The mod_wsgi adapter is an Apache module that provides a WSGI compliant\
interface for hosting Python based web applications within Apache. The\
adapter is written completely in C code against the Apache C runtime and\
for hosting WSGI applications within Apache has a lower overhead than using\
existing WSGI adapters for mod_python or CGI.\


%description %_description

%if %{with python2}
%package -n python2-%{name}
Summary: %summary
Requires:       httpd-mmn = %{_httpd_mmn}
BuildRequires:  python2-devel, python2-setuptools
%{?python_provide:%python_provide python2-%{name}}
%if 0%{?rhel} && 0%{?rhel} <= 7
Provides: mod_wsgi = %{version}-%{release}
Provides: mod_wsgi%{?_isa} = %{version}-%{release}
Obsoletes: mod_wsgi < %{version}-%{release}
%endif

%description -n python2-%{name} %_description

%endif

%if %{with python3}
%package -n python3-%{name}
Summary:        %summary
Requires:       httpd-mmn = %{_httpd_mmn}
BuildRequires:  python3-devel, python3-sphinx, python3-sphinx_rtd_theme
BuildRequires:  python3-setuptools
%if !%{with python2}
Provides: mod_wsgi = %{version}-%{release}
Provides: mod_wsgi%{?_isa} = %{version}-%{release}
Obsoletes: mod_wsgi < %{version}-%{release}
%endif

%description -n python3-%{name} %_description

%endif

%prep
%autosetup -p1 -n %{name}-%{version}

: Python2=%{with python2} Python3=%{with python3}

%build
%if %{with python3}
%make_build -C docs html
%endif

export LDFLAGS="$RPM_LD_FLAGS -L%{_libdir}"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"

%if %{with python3}
mkdir py3build/
# this always produces an error (because of trying to copy py3build
# into itself) but we don't mind, so || :
cp -R * py3build/ || :
pushd py3build
%configure --enable-shared --with-apxs=%{_httpd_apxs} --with-python=%{python3}
%make_build
%py3_build
popd
%endif

%if %{with python2}
%configure --enable-shared --with-apxs=%{_httpd_apxs} --with-python=%{python2}
%make_build
%py2_build
%endif

%install
# first install python3 variant and rename the so file
%if %{with python3}
pushd py3build
%make_install LIBEXECDIR=%{_httpd_moddir}
mv  $RPM_BUILD_ROOT%{_httpd_moddir}/mod_wsgi{,_python3}.so

install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
# httpd >= 2.4.x
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-wsgi-python3.conf

%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/mod_wsgi-express{,-3}
popd

%endif

# second install python2 variant
%if %{with python2}
%make_install LIBEXECDIR=%{_httpd_moddir}

install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
# httpd >= 2.4.x
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-wsgi.conf

%py2_install
mv $RPM_BUILD_ROOT%{_bindir}/mod_wsgi-express{,-2}
ln -s %{_bindir}/mod_wsgi-express-2 $RPM_BUILD_ROOT%{_bindir}/mod_wsgi-express
%endif

%if %{with python2}
%files -n python2-%{name}
%license LICENSE
%doc CREDITS.rst README.rst
%config(noreplace) %{_httpd_modconfdir}/*wsgi.conf
%{_httpd_moddir}/mod_wsgi.so
%{python2_sitearch}/mod_wsgi-*.egg-info
%{python2_sitearch}/mod_wsgi
%{_bindir}/mod_wsgi-express-2
%{_bindir}/mod_wsgi-express
%endif

%if %{with python3}
%files -n python3-%{name}
%license LICENSE
%doc CREDITS.rst README.rst
%config(noreplace) %{_httpd_modconfdir}/*wsgi-python3.conf
%{_httpd_moddir}/mod_wsgi_python3.so
%{python3_sitearch}/mod_wsgi-*.egg-info
%{python3_sitearch}/mod_wsgi
%{_bindir}/mod_wsgi-express-3
%endif

%changelog
* Wed Dec  4 2024 Joe Orton <jorton@redhat.com> - 5.0.2-1
- update to 5.0.2 (#2250905)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Joe Orton <jorton@redhat.com> - 5.0.0-5
- fix LD_RUN_PATH handling

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.0.0-4
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.0.0-3
- Rebuilt for Python 3.13

* Wed Apr 24 2024 Karolina Surma <ksurma@redhat.com> - 5.0.0-2
- Add support for Python 3.13

* Thu Jan 25 2024 Joe Orton <jorton@redhat.com> - 5.0.0-1
- update to 5.0.0 (#2250905)
- remove redundant _httpd_ macro definitions

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Tomas Orsava <torsava@redhat.com> - 4.9.4-5
- Use the modern way of filtering Provides not to interfere with modern Python
  RPM generators

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 4.9.4-4
- Rebuilt for Python 3.12

* Thu Jun 01 2023 Luboš Uhliarik <luhliari@redhat.com> - 4.9.4-3
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 Luboš Uhliarik <luhliari@redhat.com> - 4.9.4-1
- new version 4.9.4

* Wed Aug 31 2022 Luboš Uhliarik <luhliari@redhat.com> - 4.9.3-1
- new version 4.9.3

* Fri Aug 19 2022 Luboš Uhliarik <luhliari@redhat.com> - 4.9.1-4
- Resolves: #2119280 - Core dumped upon file upload >= 1GB

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.9.1-2
- Rebuilt for Python 3.11

* Mon May 02 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.1-1
- Update to 4.9.1
- Fixes: rhbz#2049695

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 Miro Hrončok <mhroncok@redhat.com> - 4.9.0-1
- Update to 4.9.0
- Enable needlessly disabled debuginfo package
- Fixes: rhbz#1960695

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Joe Orton <jorton@redhat.com> - 4.8.0-2
- adjust to use bconds (lbalhar, PR#6)
- adjust to use make_install macro (tstellar, PR#8)

* Thu Jun 17 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.0-1
- update to 4.8.0
- Add experimental Python 3.10 support (#1898158)
- Upstream PR: https://github.com/GrahamDumpleton/mod_wsgi/pull/688

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.7.1-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.7.1-2
- Rebuilt for Python 3.9

* Wed May 13 2020 Joe Orton <jorton@redhat.com> - 4.7.1-1
- update to 4.7.1 (#1721376)

* Thu Feb 13 2020 Tom Stellard <tstellar@redhat.com> - 4.6.8-3
- Use make_build macro instead of just make
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Joe Orton <jorton@redhat.com> - 4.6.8-1
- update to 4.6.8 (#1721376)

* Mon Nov 11 2019 Joe Orton <jorton@redhat.com> - 4.6.6-6
- try again to drop Python 2

* Tue Oct 29 2019 Joe Orton <jorton@redhat.com> - 4.6.6-5
- drop python2 build

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.6-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.6-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Matthias Runge <mrunge@redhat.com> - 4.6.6-1
- update to 4.6.6 (rhbz#1718151)

* Wed May 29 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.5-1
- update to 4.6.5

* Tue Apr 16 2019 Joe Orton <jorton@redhat.com> - 4.6.4-4
- only build docs with Python 3
- fix build on Fedora>30 and RHEL 7

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Adam Williamson <awilliam@redhat.com> - 4.6.4-2
- Run Python 3 build in a subdir, so module isn't linked against both
  libpython 2 and libpython 3 (rhbz#1609491)

* Fri Jul 20 2018 Matthias Runge <mrunge@redhat.com> - 4.6.4-1
- update to 4.6.4 (rhbz#1560329)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.6.2-4
- Rebuilt for Python 3.7

* Fri Apr 20 2018 Joe Orton <jorton@redhat.com> - 4.6.2-3
- use sphinx-build-3 if python2 support is disabled

* Thu Mar 22 2018 Troy Dawson <tdawson@redhat.com> - 4.6.2-2
- Update conditionals.
- Make preperations for non-python2 builds

* Tue Mar 13 2018 Matthias Runge <mrunge@redhat.com> - 4.6.2-1
- update to 4.6.2 (rhbz#1514768)
- add gcc BR

* Wed Feb  7 2018 Joe Orton <jorton@redhat.com> - 4.5.20-4
- restrict module DSO symbol exports

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.5.20-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.5.20-2
- Python 2 binary package renamed to python2-mod_wsgi
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri Oct 20 2017 Joe Orton <jorton@redhat.com> - 4.5.20-1
- update to 4.5.20

* Wed Aug 09 2017 Dan Callaghan <dcallagh@redhat.com> - 4.5.15-5
- include mod_wsgi Python package and mod_wsgi-express script

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.5.15-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Jun 23 2017 Joe Orton <jorton@redhat.com> - 4.5.15-1
- update to 4.5.15 (#1431893)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Jakub Dorňák <jakub.dornak@misli.cz> - 4.5.13-1
- Update to 4.5.13

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.5.9-2
- Rebuild for Python 3.6

* Mon Dec 05 2016 Matthias Runge <mrunge@redhat.com> - 4.5.9-1
- upgrade to 4.5.9 (rhbz#1180445)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 Richard W.M. Jones <rjones@redhat.com> - 4.4.8-1
- Upstream to 4.4.8.
- This version includes the fix for the segfault described in RHBZ#1178851.

* Mon Jan  5 2015 Jakub Dorňák <jdornak@redhat.com> - 4.4.3-1
- update to new upstream version 4.4.3 (#1176914)

* Wed Dec 17 2014 Jan Kaluza <jkaluza@redhat.com> - 4.4.1-1
- update to new upstream version 4.4.1 (#1170994)

* Wed Nov 19 2014 Jan Kaluza <jkaluza@redhat.com> - 4.3.2-1
- update to new upstream version 4.3.2 (#1104526)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Luke Macken <lmacken@redhat.com> - 3.5-1
- Update to 3.5 to fix CVE-2014-0240 (#1101863)
- Remove all of the patches, which have been applied upstream
- Update source URL for new the GitHub upstream

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 3.4-14
- rebuild for Python 3.4

* Mon Apr 28 2014 Matthias Runge <mrunge@redhat.com> - 3.4.13
- do not use conflicts between mod_wsgi packages (rhbz#1087943)

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 3.4-12
- fix _httpd_mmn expansion in absence of httpd-devel

* Fri Jan 10 2014 Matthias Runge <mrunge@redhat.com> - 3.4-11
- added python3 subpackage (thanks to Jakub Dorňák), rhbz#1035876

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  8 2013 Joe Orton <jorton@redhat.com> - 3.4-9
- modernize spec file (thanks to rcollet)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Jan Kaluza <jkaluza@redhat.com> - 3.4-7
- compile with -fno-strict-aliasing to workaround Python
  bug http://www.python.org/dev/peps/pep-3123/

* Thu Nov 22 2012 Joe Orton <jorton@redhat.com> - 3.4-6
- use _httpd_moddir macro

* Thu Nov 22 2012 Joe Orton <jorton@redhat.com> - 3.4-5
- spec file cleanups

* Wed Oct 17 2012 Joe Orton <jorton@redhat.com> - 3.4-4
- enable PR_SET_DUMPABLE in daemon process to enable core dumps

* Wed Oct 17 2012 Joe Orton <jorton@redhat.com> - 3.4-3
- use a NULL c->sbh pointer with httpd 2.4 (possible fix for #867276)
- add logging for unexpected daemon process loss

* Wed Oct 17 2012 Matthias Runge <mrunge@redhat.com> - 3.4-2
- also use RPM_LD_FLAGS for build bz. #867137

* Mon Oct 15 2012 Matthias Runge <mrunge@redhat.com> - 3.4-1
- update to upstream release 3.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Joe Orton <jorton@redhat.com> - 3.3-6
- add possible fix for daemon mode crash (#831701)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 3.3-5
- move wsgi.conf to conf.modules.d

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 3.3-4
- rebuild for httpd 2.4

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 3.3-3
- prepare for httpd 2.4.x

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 James Bowes <jbowes@redhat.com> 3.3-1
- update to 3.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Mar  9 2010 Josh Kayse <joshkayse@fedoraproject.org> - 3.2-1
- update to 3.2

* Sun Mar 07 2010 Josh Kayse <joshkayse@fedoraproject.org> - 3.1-2
- removed conflicts as it violates fedora packaging policy

* Sun Mar 07 2010 Josh Kayse <joshkayse@fedoraproject.org> - 3.1-1
- update to 3.1
- add explicit enable-shared
- add conflicts mod_python < 3.3.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 James Bowes <jbowes@redhat.com> 2.5-1
- Update to 2.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.3-2
- Rebuild for Python 2.6

* Tue Oct 28 2008 Luke Macken <lmacken@redhat.com> 2.3-1
- Update to 2.3

* Mon Sep 29 2008 James Bowes <jbowes@redhat.com> 2.1-2
- Remove requires on httpd-devel

* Wed Jul 02 2008 James Bowes <jbowes@redhat.com> 2.1-1
- Update to 2.1

* Mon Jun 16 2008 Ricky Zhou <ricky@fedoraproject.org> 1.3-4
- Build against the shared python lib.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 James Bowes <jbowes@redhat.com> 1.3-2
- Require httpd

* Sat Jan 05 2008 James Bowes <jbowes@redhat.com> 1.3-1
- Update to 1.3

* Sun Sep 30 2007 James Bowes <jbowes@redhat.com> 1.0-1
- Initial packaging for Fedora

