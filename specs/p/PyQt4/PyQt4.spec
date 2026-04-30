## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 52;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")

## f29+ no longer using separate sipdir for python3
%global py3_sipdir %{_datadir}/sip/PyQt4

%global __provides_exclude_from ^(%{?python3_sitearch:%{python3_sitearch}/.*\\.so|}%{_qt4_plugindir}/.*\\.so)$

%global webkit 1
%global sip_ver 4.19.12

Summary: Python bindings for Qt4
Name:    PyQt4
Version: 4.12.3
Release: %autorelease
License: GPL-3.0-only AND BSD-3-clause
URL:     http://www.riverbankcomputing.com/software/pyqt/
%if 0%{?snap:1}
Source0:  http://www.riverbankcomputing.com/static/Downloads/%{name}/PyQt-x11-gpl-%{version}%{?snap:-snapshot-%{snap}}.tar.gz
%else
Source0:  http://sourceforge.net/projects/pyqt/files/%{name}/PyQt-%{version}/%{name}_gpl_x11-%{version}.tar.gz
%endif
Source2: pyuic4.sh

## upstreamable patches
Patch1: %{name}_gpl_x11-4.12.3-ftbfs.patch

## upstream patches
# fix FTBFS on ARM
Patch60:  qreal_float_support.diff

# Fix Python 3.10 support (rhbz#1895298)
Patch61:  python310-pyobj_ascharbuf.patch

# Fix error: invalid use of undefined type 'struct _frame'
Patch62:  %{name}-4.12.3-pyframe_getback.patch

# rhel patches
Patch300: PyQt-x11-gpl-4.11-webkit.patch

# Fix new function in Python-3.13
Patch301: %{name}-fix_function_for_Python3.13.patch

BuildRequires: make
BuildRequires: chrpath
BuildRequires: findutils
BuildRequires: gcc-c++
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(QtDBus)
BuildRequires: pkgconfig(QtDeclarative)
BuildRequires: pkgconfig(QtDesigner)
BuildRequires: pkgconfig(QtGui)
BuildRequires: pkgconfig(QtHelp)
BuildRequires: pkgconfig(QtMultimedia)
BuildRequires: pkgconfig(QtNetwork)
BuildRequires: pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(QtScript)
BuildRequires: pkgconfig(QtScriptTools)
BuildRequires: pkgconfig(QtSql)
BuildRequires: pkgconfig(QtSvg)
BuildRequires: pkgconfig(QtTest)
BuildRequires: pkgconfig(QtXml)
BuildRequires: pkgconfig(QtXmlPatterns)
BuildRequires: python3-dbus
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pyqt4-sip >= %{sip_ver}
BuildRequires: python3-sip-devel >= %{sip_ver}

%description
These are Python bindings for Qt4.

%package devel
Summary: Files needed to build other bindings based on Qt4
%if 0%{?webkit}
Obsoletes: %{name}-webkit-devel < %{version}-%{release}
Provides: %{name}-webkit-devel = %{version}-%{release}
Obsoletes: PyQt4 < 4.11.4-8
%endif
Provides: python-qt4-devel = %{version}-%{release}
Provides: pyqt4-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Requires: sip-devel
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6

%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt4 classes (e.g. KDE or your own).

%package doc
Summary: PyQt4 developer documentation and examples
BuildArch: noarch
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-doc = %{version}-%{release}

%description doc
%{summary}.

# split-out arch'd subpkg, since (currently) %%_qt4_datadir = %%_qt4_libdir
%package qsci-api
Summary: Qscintilla API file support
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
%py_provides python3-qt4-qsci-api

%description qsci-api
%{summary}.

%if 0%{?webkit}
%package webkit
Summary: Python bindings for Qt4 Webkit
BuildRequires: pkgconfig(QtWebKit)
# when -webkit was split out
Obsoletes: PyQt4 < 4.11.4-8
Provides: pyqt4-webkit = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description webkit
%{summary}.

%package -n python3-%{name}-webkit
Summary: Python3 bindings for Qt4 Webkit
Obsoletes: python3-PyQt4 < 4.11.4-8
%py_provides python3-pyqt4-webkit
Requires:  python3-PyQt4 = %{version}-%{release}

%description -n python3-%{name}-webkit
%{summary}.
%endif

# The bindings are imported as "PyQt4", hence it's reasonable to name the
# Python 3 subpackage "python3-PyQt4", despite the apparent tautology
%package -n python3-%{name}
Summary: Python 3 bindings for Qt4
Requires: python3-dbus
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%{?_sip_api:Requires: python3-pyqt4-sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if 0%{?webkit}
Obsoletes: python3-PyQt4 < 4.11.4-8
%endif
Provides: python3-qt4 = %{version}-%{release}
Provides: python%{python3_version}dist(pyqt4) = %{version}

%description -n python3-%{name}
These are Python 3 bindings for Qt4.

%package -n python3-%{name}-devel
Summary: Python 3 bindings for Qt4
%if 0%{?webkit}
%py_provides python3-%{name}-webkit-devel
%endif
Provides: python3-qt4-devel = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}
Requires: python3-sip-devel
# when split happened, upgrade path
Obsoletes: python3-PyQt4-devel < 4.10.3-6

%description -n python3-%{name}-devel
Files needed to build other Python 3 bindings for C++ classes that inherit
from any of the Qt4 classes (e.g. KDE or your own).


%prep
%setup -q -n PyQt4_gpl_x11-%{version}%{?snap:-snapshot-%{snap}}

# save orig for comparison later
cp -a ./sip/QtGui/opengl_types.sip ./sip/QtGui/opengl_types.sip.orig
%patch -P 1 -p1 -b .ftbfs
%patch -P 60 -p1 -b .arm
%patch -P 61 -p1
%patch -P 62 -p1
%if ! 0%{?webkit}
%patch -P 300 -p1 -b .webkit
%endif
%patch -P 301 -p1 -b .python3.13


%build
QT4DIR=%{_qt4_prefix}
PATH=%{_qt4_bindir}:$PATH ; export PATH

mkdir %{_target_platform}-python3
pushd %{_target_platform}-python3
%{__python3} ../configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=%{_qt4_qmake} \
  --qsci-api-destdir=%{_qt4_datadir}/qsci \
  %{?py3_sipdir:--sipdir=%{py3_sipdir}} \
  --verbose \
  CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LFLAGS="%{__global_ldflags}"
%make_build
popd


%install
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{_target_platform}-python3
%if "%py3_sipdir" == "%{_datadir}/sip/PyQt4"
# copy files to old location for compat purposes temporarily
mkdir -p %{buildroot}%{_datadir}/python3-sip
cp -alf %{buildroot}%{py3_sipdir} \
        %{buildroot}%{_datadir}/python3-sip/PyQt4
%endif
mkdir %{buildroot}%{python3_sitearch}/PyQt4/__pycache__/ ||:

# likewise, remove Python 2 code from the Python 3.1 directory:
rm -rfv %{buildroot}%{python3_sitearch}/PyQt4/uic/port_v2/

# install pyuic4 wrapper
rm -fv %{buildroot}%{_bindir}/pyuic4
install -p -m755 -D %{SOURCE2} \
  %{buildroot}%{_bindir}/pyuic4
sed -i \
  -e "s|@PYTHON3@|%{__python3}|g" \
  %{buildroot}%{_bindir}/pyuic4


%check
# verify opengl_types.sip sanity
diff -u ./sip/QtGui/opengl_types.sip.orig \
        ./sip/QtGui/opengl_types.sip ||:

%files doc
%doc doc/*
%doc examples/

%files qsci-api
# avoid dep on qscintilla-python, own %%_qt4_datadir/qsci/... here for now
%dir %{_qt4_datadir}/qsci/
%dir %{_qt4_datadir}/qsci/api/
%dir %{_qt4_datadir}/qsci/api/python/
%{_qt4_datadir}/qsci/api/python/PyQt4.api

%files -n python3-%{name}
%doc NEWS README
%license LICENSE
%{python3_dbus_dir}/qt.so
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/__init__.py*
%{python3_sitearch}/PyQt4/__pycache__/
%{python3_sitearch}/PyQt4/pyqtconfig.py*
%{python3_sitearch}/PyQt4/phonon.so
%{python3_sitearch}/PyQt4/Qt.so
%{python3_sitearch}/PyQt4/QtCore.so
%{python3_sitearch}/PyQt4/QtDBus.so
%{python3_sitearch}/PyQt4/QtDeclarative.so
%{python3_sitearch}/PyQt4/QtDesigner.so
%{python3_sitearch}/PyQt4/QtGui.so
%{python3_sitearch}/PyQt4/QtHelp.so
%{python3_sitearch}/PyQt4/QtMultimedia.so
%{python3_sitearch}/PyQt4/QtNetwork.so
%{python3_sitearch}/PyQt4/QtOpenGL.so
%{python3_sitearch}/PyQt4/QtScript.so
%{python3_sitearch}/PyQt4/QtScriptTools.so
%{python3_sitearch}/PyQt4/QtSql.so
%{python3_sitearch}/PyQt4/QtSvg.so
%{python3_sitearch}/PyQt4/QtTest.so
%{python3_sitearch}/PyQt4/QtXml.so
%{python3_sitearch}/PyQt4/QtXmlPatterns.so
%{python3_sitearch}/PyQt4/uic/
%{_qt4_plugindir}/designer/*

%if 0%{?webkit}
%files -n python3-%{name}-webkit
%{python3_sitearch}/PyQt4/QtWebKit.so
%endif

%files -n python3-%{name}-devel
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{py3_sipdir}/
# compat location
%dir %{_datadir}/python3-sip/
%{_datadir}/python3-sip/PyQt4/


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 4.12.3-52
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.12.3-51
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.12.3-50
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.12.3-48
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Antonio Trande <sagitter@fedoraproject.org> - 4.12.3-45
- Remove old Python2 comment

* Mon Jul 15 2024 Antonio Trande <sagitter@fedoraproject.org> - 4.12.3-44
- Remove old Python2 macros

* Mon Jul 15 2024 Antonio Trande <sagitter@fedoraproject.org> - 4.12.3-43
- Remove old Python2 provides

* Mon Jul 15 2024 Antonio Trande <sagitter@fedoraproject.org> - 4.12.3-42
- Patched for Python-3.13| SPEC file modernized

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.12.3-41
- Rebuilt for Python 3.13

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 05 2023 Antonio Trande <sagitter@fedoraproject.org> - 4.12.3-38
- Simple untested fix for Python 3.13 (rhbz#2247256)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 4.12.3-36
- Rebuilt for Python 3.12

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Than Ngo <than@redhat.com> - 4.12.3-33
- Fix error: invalid use of undefined type 'struct _frame'

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 4.12.3-32
- Rebuilt for Python 3.11

* Tue May 03 2022 Than Ngo <than@redhat.com> - 4.12.3-31
- Fixed bz#2038921 - PyQt4: FTBFS in Fedora Rawhide

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Rex Dieter <rdieter@gmail.com> - 4.12.3-29
- rebuild (python 3.11)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 4.12.3-26
- Rebuilt for Python 3.10

* Thu Feb 18 2021 Miro Hrončok <miro@hroncok.cz> - 4.12.3-25
- No release in pythonX.Ydist(pyqt4) provide

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Tom Stellard <tstellar@redhat.com> - 4.12.3-23
- Add BuildRequires: make

* Wed Nov 25 2020 Victor Stinner <vstinner@python.org> - 4.12.3-22
- Fix Python 3.10 support

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <miro@hroncok.cz> - 4.12.3-20
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-18
- include designer plugin when python2 is disabled too

* Thu Nov 21 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-17
- BR: pkgconfig(dbus-python) make excludes honor inclusion/exclusion of
  python2/python3 appropriately

* Thu Nov 21 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-16
- fix build when python2 is disabled mostly unconditionally build qsci docs

* Tue Nov 19 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-15
- generate qsci as needed

* Fri Nov 15 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-14
- Release++

* Fri Nov 15 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-13
- drop python2 support for f32+ (#1729577)

* Thu Oct 03 2019 Miro Hrončok <miro@hroncok.cz> - 4.12.3-12
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <miro@hroncok.cz> - 4.12.3-11
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-9
- Provides: Provides: python%%{python?_version}dist(pyqt4) (#1705739)

* Mon May 06 2019 Rex Dieter <rdieter@gmail.com> - 4.12.3-8
- rebuild for python autodeps (#1705739)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 10 2018 Rex Dieter <rdieter@gmail.com> - 4.12.3-6
- drop -assistant subpkg on f30+ (#1633792)

* Wed Oct 10 2018 Rex Dieter <rdieter@gmail.com> - 4.12.3-5
- Revert "fixed #1633792. move assistant, webkit into main"

* Wed Oct 10 2018 Rex Dieter <rdieter@gmail.com> - 4.12.3-4
- Revert "fixed #1633792. move assistant, webkit into main"

* Tue Oct 09 2018 Than Ngo <than@redhat.com> - 4.12.3-3
- fixed #1633792. move assistant, webkit into main

* Tue Oct 09 2018 Than Ngo <than@redhat.com> - 4.12.3-2
- fixed #1633792. move assistant, webkit into main

* Fri Aug 31 2018 Rex Dieter <rdieter@gmail.com> - 4.12.3-1
- 4.12.3

* Fri Aug 24 2018 Rex Dieter <rdieter@gmail.com> - 4.12.2-3
- drop backward-compat py3_sipdir

* Fri Aug 24 2018 Rex Dieter <rdieter@gmail.com> - 4.12.2-2
- drop dep on python?-sip

* Tue Aug 14 2018 Rex Dieter <rdieter@gmail.com> - 4.12.2-1
- 4.12.2

* Sun Jul 15 2018 Rex Dieter <rdieter@gmail.com> - 4.12.1-13
- ensure compat dir exists and is owned

* Sun Jul 15 2018 Rex Dieter <rdieter@gmail.com> - 4.12.1-12
- BR: python3-sip

* Sun Jul 15 2018 Rex Dieter <rdieter@gmail.com> - 4.12.1-11
- update sip-related build deps s/dbus-python/python2-dbus/

* Sun Jul 15 2018 Rex Dieter <rdieter@gmail.com> - 4.12.1-10
- use %%make_build %%license -devel: drop dep on -webkit unified sipdir on
  f29+

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <miro@hroncok.cz> - 4.12.1-8
- Rebuilt for Python 3.7

* Tue Feb 20 2018 Rex Dieter <rdieter@gmail.com> - 4.12.1-7
- BR: gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 27 2017 Merlin Mathesius <mmathesi@redhat.com> - 4.12.1-5
- Cleanup spec file conditionals

* Mon Jul 31 2017 Than Ngo <than@redhat.com> - 4.12.1-4
- fixed bz#1348514 - Arbitrary code execution due to insecure loading of
  Python module from CWD

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 05 2017 Rex Dieter <rdieter@math.unl.edu> - 4.12.1-2
- rebuild (sip)

* Sun Jul 02 2017 Rex Dieter <rdieter@math.unl.edu> - 4.12.1-1
- PyQt4-4.12.1

* Thu Mar 30 2017 Rex Dieter <rdieter@math.unl.edu> - 4.12-5
- rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Rex Dieter <rdieter@math.unl.edu> - 4.12-3
- tighten provides filter

* Fri Jan 27 2017 Rex Dieter <rdieter@math.unl.edu> - 4.12-2
- update provides filtering

* Sun Jan 01 2017 Rex Dieter <rdieter@math.unl.edu> - 4.12-1
- PyQt4-4.12

* Sun Dec 11 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.11.4-23
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.4-22
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Wed Apr 20 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-21
- rebuild (qt)

* Mon Apr 18 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-20
- Provides: python2-qt4/python2-PyQt4 (#1249422)

* Mon Apr 18 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-19
- rebuild (qt)

* Wed Apr 13 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-18
- rebuid (sip)

* Wed Mar 02 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-17
- webkit: add Provides: to match those of main pkg

* Wed Mar 02 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-16
- fix mkdir

* Wed Mar 02 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-15
- rebase -webkit.patch, use safer subdir builds

* Wed Mar 02 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-14
- make new -webkit subpkg depend on main pkg too

* Mon Feb 29 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-13
- fix 'macro in comment'

* Mon Feb 29 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-12
- fix typo, move assistant bits together

* Mon Feb 29 2016 Rex Dieter <rdieter@math.unl.edu>
- 4.11.4-8
- don't remove anything from uic/widget-plugins (see also #1294307)
- -webkit subpkg

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 4.11.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-9
- explicitly set CFLAGS,CXXFLAGS,LFLAGS

* Thu Nov 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 4.11.4-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Than Ngo <than@redhat.com> - 4.11.4-7
- rebuilt

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 4.11.4-6
- Rebuilt for Python3.5 rebuild

* Tue Jun 16 2015 Dennis Gilmore <dennis@ausil.us> - 4.11.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-4
- sync %%%%files changes to python3- subpkgs too

* Sun Jun 14 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-3
- update %%%%files

* Sat Jun 13 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-2
- update %%%%files

* Sat Jun 13 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.4-1
- PyQt4-4.11.4

* Sat Jun 06 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.3-7
- missing \

* Sat Jun 06 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.3-6
- Release++

* Sat Jun 06 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.3-5
- 4.11.3-5
- drop qscintilla conditional
- -python3-devel: include binaries, use pyuic4 wrapper (see also #1193107)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.11.3-4
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 25 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.3-3
- rebuild (sip)

* Wed Feb 25 2015 Rex Dieter <rdieter@math.unl.edu> - 4.11.3-2
- rebuild (sip)

* Tue Nov 11 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.3-1
- PyQt4-4.11.3

* Thu Nov 06 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.2-3
- update %%files per previous commit

* Thu Nov 06 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.2-2
- python2_sitelib should be python2_sitearch (#1161121)

* Mon Sep 15 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.2-1
- Merge branch 'master' into f21

* Mon Sep 15 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-6
- Revert "- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild"

* Fri Aug 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 4.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 06 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-4
- PyQt4-4.11.1

* Fri Jun 06 2014 Dennis Gilmore <dennis@ausil.us> - 4.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-2
- rebuild for new qscintilla (#1104559)

* Mon Jun 02 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-1
- 4.11.1-0.1.9d5a6843b580
- PyQt4-4.11.1 snapshot (fix FTBFS)
- re-enable -assistant subpkg

* Wed May 28 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11-3
- explicitly set python3 sipdir

* Wed May 28 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11-2
- Obsoletes: PyQt4-assistant, use configure-ng.py

* Wed May 28 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11-1
- PyQt-4.11

* Mon May 12 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.4-2
- rebuild (f21-python)

* Sun Mar 16 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.4-1
- 4.10.4-1
- PyQt-4.10.4 (#1076001)
- s/python/python2/

* Sat Mar 15 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-15
- make -devel arch'd again, python3-dbus support

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-14
- add Provides: python-qt4... for new subpkgs

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-13
- own qsci-api dirs here for now

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-12
- typo, missing %%endif

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-11
- doc.noarch,-qsci-api subpkgs

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-10
- no more sitelib/PyQt4

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-9
- simpler approach, avoid symlink and just copy

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-8
- polish/improve uic multilib issues, make -devel noarch (#1076346)

* Mon Feb 17 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-7
- flesh out python(3)-qt4 related provides

* Fri Dec 06 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-6
- rebuild (phonon)

* Thu Nov 21 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-5
- Merge branch 'f20'

* Thu Nov 14 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-4
- respin patch for python3

* Thu Nov 14 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-3
- avoid startswith to make python3 happy

* Thu Nov 14 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-2
- Merge branch 'f20'

* Wed Oct 16 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-1
- 4.10.3

* Mon Oct 07 2013 Than Ngo <than@redhat.com> - 4.10.2-4
- fix typo

* Mon Oct 07 2013 Than Ngo <than@redhat.com> - 4.10.2-3
- fix license tag - add missing buildroot

* Fri Aug 02 2013 Dennis Gilmore <dennis@ausil.us> - 4.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.2-1
- 4.10.2

* Tue May 07 2013 Than Ngo <than@redhat.com> - 4.10.1-8
- add qtassistant macro

* Fri May 03 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.1-7
- fix dbus/mainloop hacks (#957867)

* Thu May 02 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.1-6
- ImportError: cannot import name uic (#958736)

* Sat Apr 27 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.1-5
- prune changelog

* Sat Apr 27 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.1-4
- python3: fix %%%%files

* Sat Apr 27 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.1-3
- Release++

* Sat Apr 27 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.1-2
- 4.10.1-2
- filter private shared objects
- %%{python_sitelib}/dbus/mainloop/qt.so should be in %%python_sitearch
  (#957260)
- .spec cleanup
- -assistant subpkg

* Mon Apr 22 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.1-1
- 4.10.1

* Tue Apr 02 2013 Than Ngo <than@redhat.com> - 4.10-11
- adapt rhel patch

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-10
- typo, not my day

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-9
- avoid bootstrap issues, force qscintilla support...

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-8
- +BR: chrpath

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-7
- too many %%endif

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu>
- update changelog

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu>
- qscintilla feature macro too

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-4
- fix python dep for rhel6

* Fri Mar 22 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-3
- introduce webkit feature macro

* Tue Mar 05 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-2
- api files in %%%%_qt4_datadir

* Mon Mar 04 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10-1
- 4.10

* Wed Feb 13 2013 Dennis Gilmore <dennis@ausil.us> - 4.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Than Ngo <than@redhat.com> - 4.9.6-2
- adapt rhel patch

* Mon Dec 10 2012 Rex Dieter <rdieter@math.unl.edu> - 4.9.6-1
- 4.9.6

* Sun Oct 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.5-3
- rebuild (sip)

* Thu Oct 11 2012 Than Ngo <than@redhat.com> - 4.9.5-2
- update webkit patch

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.5-1
- PyQt-4.9.5

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 4.9.4-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 4.9.4-4
- make with_python3 be conditional on fedora

* Mon Jul 30 2012 Than Ngo <than@redhat.com> - 4.9.4-3
- update webkit patch

* Wed Jul 18 2012 Dennis Gilmore <dennis@ausil.us> - 4.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.4-1
- 4.9.4

* Sun Jun 24 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Fri Jun 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Thu Jun 21 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-5
- PyQt4 opengl-types.sip multilib conflict (#509415)

* Fri May 04 2012 Than Ngo <than@redhat.com> - 4.9.1-4
- rhel/fedora condition

* Fri May 04 2012 Than Ngo <than@redhat.com> - 4.9.1-3
- add rhel/fedora condition

* Sun Mar 04 2012 Peter Robinson <pbrobinson@gmail.com> - 4.9.1-2
- Add upstream patch (via Debian) to fix FTBFS on ARM

* Sat Feb 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-1
- 4.9.1

* Thu Jan 12 2012 Dennis Gilmore <dennis@ausil.us> - 4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9-2
- upstream doItemsLayout patch

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.9-1
- 4.9

* Tue Dec 20 2011 Than Ngo <than@redhat.com> - 4.8.6-4
- Provides: pyqt4

* Wed Dec 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.6-3
- devel: Provides: -webkit-devel

* Fri Nov 18 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.6-2
- Provides: python(3)-qt4

* Wed Oct 26 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.6-1
- 4.8.6

* Mon Oct 17 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.5-3
- put back python3-devel, pkgconfig(python3) isn't provided for some reason

* Mon Oct 17 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.5-2
- pkgconfig-style deps Provides: -webkit s/python3-PyQt4/python3-%%name/

* Wed Aug 10 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.5-1
- 4.8.5

* Sun Jul 24 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.4-5
- rebuild (qt48)

* Thu Jun 16 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.4-4
- rebuild

* Wed Jun 08 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.4-3
- squash more rpaths

* Mon May 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.4-2
- up sip-devel dep

* Mon May 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.4-1
- 4.8.4

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> - 4.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.3-3
- use LIBDIR in addition to exec_prefix/lib for finding libpython

* Mon Jan 24 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.3-2
- PyQt4-x11-gpl-4.8.3

* Sat Jan 15 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.3-1
- 4.8.3 snapshot - Little typo (#668289)

* Sat Jan 08 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-6
- up some min build deps

* Thu Dec 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-5
- use right shlib name, really really this time

* Thu Dec 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-4
- arg, fix misplaced quotes

* Thu Dec 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-3
- drop extraneous import sys (doh)

* Thu Dec 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-2
- update patch to accomodate presence of sys.abiflags

* Sat Dec 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- PyQt4-x11-gpl-4.8.2

* Sat Oct 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8.1-1
- PyQt4-x11-gpl-4.8.1

* Wed Oct 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8-4
- fix pyuic_shbang.patch - drop implicit-linking patch (no longer needed)

* Sun Oct 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8-3
- drop BR: qt-assistant-adp-devel (these deprecated bindings are no longer
  included)

* Sat Oct 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8-2
- typo, missing \ in python3 build section

* Sat Oct 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.8-1
- PyQt-x11-gpl-4.8

* Sat Oct 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.7-3
- backport patch to fix kdebindings/pykde ftbfs - drop sip-devel min
  version a bit to match reality

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> - 4.7.7-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.7-1
- PyQt-x11-gpl-4.7.7

* Mon Sep 13 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.6-2
- backport pyuic fix for python2

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.6-1
- PyQt-x11-gpl-4.7.6

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 4.7.4-6
- rebuild with python3.2

* Wed Jul 28 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-5
- dist-git conversion

* Thu Jul 22 2010 dmalcolm <dmalcolm@fedoraproject.org> - 4.7.4-4
- Rebuilt for
  https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-3
- typo!

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-2
- handle case where rpath is gone (yay)

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-1
- PyQt-x11-gpl-4.7.4

* Sun May 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.3-3
- BR: qt4-webkit-devel

* Tue Apr 27 2010 dmalcolm <dmalcolm@fedoraproject.org> - 4.7.3-2
- add python 3 subpackages (#586196)

* Sat Apr 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.3-1
- PyQt-x11-gpl-4.7.3

* Sun Mar 21 2010 Kevin Kofler <kkofler@fedoraproject.org> - 4.7.2-2
- rebuild against fixed qt to get QtMultimedia detected properly

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.2-1
- PyQt-x11-gpl-4.7.2

* Sun Mar 14 2010 Kevin Kofler <kkofler@fedoraproject.org> - 4.7-6
- fix implicit linking when checking for QtHelp and QtAssistant - remove
  Python 3 code from Python 2.6 directory, fixes FTBFS (#564633)

* Sun Mar 14 2010 Kevin Kofler <kkofler@fedoraproject.org> - 4.7-5
- Sync: Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.7-4 - BR
  qt-assistant-adp-devel Tue Feb 23 2010 Than Ngo <than@redhat.com> - 4.7-3
  - fix multilib conflict because of timestamp

* Sat Mar 13 2010 Kevin Kofler <kkofler@fedoraproject.org> - 4.7-4
- BR qt-assistant-adp-devel

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7-3
- rebuild

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7-2
- PyQt-x11-gpl-4.7 (final)

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7-1
- PyQt-x11-gpl-4.7-snapshot-20091231

* Sat Nov 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-5
- phonon bindings missing (#541685)

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 4.6.2-4
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Wed Nov 25 2009 Than Ngo <than@fedoraproject.org> - 4.6.2-3
- fix conditional for RHEL

* Wed Nov 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-2
- PyQt4-4.6.2 breaks QStringList in QVariant, rebuild with sip-4.9.3
  (#541211)

* Fri Nov 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-1
- PyQt4-4.6.2

* Thu Nov 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-4
- rebuild (for qt-4.6.0-rc1, f13+)

* Mon Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-3
- Requires: sip-api(%%_sip_api_major) >= %%_sip_api

* Sat Oct 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-2
- PyQt4-4.6.1

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-1
- PyQt4-4.6.1-snapshot-20091014 (#529192)

* Tue Jul 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.4-1
- PyQt4-4.5.4

* Fri Jul 24 2009 Jesse Keating <jkeating@fedoraproject.org> - 4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-1
- PyQt4-4.5.2

* Thu Jul 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-2
- fix build with qt-4.5.2 - PyQt4-devel multilib conflict (#509415)

* Tue Jun 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-1
- PyQt-4.5.1

* Fri Jun 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5-4
- use --confirm-license

* Fri Jun 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5-3
- PyQt-4.5

* Thu May 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5-2
- fix generation of sip_ver

* Thu May 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5-1
- PyQt-4.5-snapshot-20090520

* Sun Apr 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-7
- rebuild for phonon bindings (#497680)

* Wed Mar 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-6
- move designer plugins to main/runtime (#487622)

* Mon Feb 23 2009 Jesse Keating <jkeating@fedoraproject.org> - 4.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Than Ngo <than@fedoraproject.org> - 4.4.4-4
- rebuilt

* Sun Feb 15 2009 Than Ngo <than@fedoraproject.org> - 4.4.4-3
- rebuild against qt-4.5rc1

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazquez@fedoraproject.org> - 4.4.4-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-1
- PyQt-4.4.4

* Tue Aug 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-1
- PyQt-4.4.3

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.2-3
- PyQt4 is built without QtWebKit support (#451490)

* Wed May 21 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.2-2
- update sip dep

* Wed May 21 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.2-1
- PyQt-4.4.2

* Thu May 15 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4-3
- License: GPLv3 or GPLv2 with exceptions

* Wed May 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4-2
- changelog

* Wed May 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4-1
- respin (gcc43)

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-2
- respin (gcc43)

* Thu Dec 06 2007 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- PyQt-4.3.3

* Thu Nov 22 2007 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-3
- use %%%%python_sitelib (instead of sitearch) for dbus bits

* Thu Nov 22 2007 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- dbus support (#395741)

* Mon Nov 12 2007 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-1
- PyQt-4.3.1

* Thu Oct 04 2007 Rex Dieter <rdieter@fedoraproject.org> - 4.2-6
- drop ExcludeArch: ppc64 , qt4 bug is (hopefully) fixed.

* Thu Oct 04 2007 Rex Dieter <rdieter@fedoraproject.org> - 4.2-5
- drop ExcludeArch: ppc64, roll the dice

* Thu Oct 04 2007 Rex Dieter <rdieter@fedoraproject.org> - 4.2-4
- import

* Thu Nov 14 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.2-3
- fix build against phonon-4.7+ (kde#306261)

* Thu Nov 21 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.2-2
- simpler phonon_detect.patch

* Thu Nov 14 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.2-1
- arg, forgot the patch, here it is

* Mon Sep 15 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.2-1
- PyQt4-4.11.2

* Fri Aug 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 4.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-5
- rebuild (qt/phonon)

* Sun Jul 06 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-4
- PyQt4-4.11.1

* Fri Jun 06 2014 Dennis Gilmore <dennis@ausil.us> - 4.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-2
- rebuild for new qscintilla (#1104559)

* Mon Jun 02 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11.1-1
- 4.11.1-0.1.9d5a6843b580
- PyQt4-4.11.1 snapshot (fix FTBFS)
- re-enable -assistant subpkg

* Wed May 28 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11-3
- explicitly set python3 sipdir

* Wed May 28 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11-2
- Obsoletes: PyQt4-assistant, use configure-ng.py

* Wed May 28 2014 Rex Dieter <rdieter@math.unl.edu> - 4.11-1
- PyQt-4.11

* Mon May 12 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.4-2
- rebuild (f21-python)

* Sun Mar 16 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.4-1
- 4.10.4-1
- PyQt-4.10.4 (#1076001)
- s/python/python2/

* Sat Mar 15 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-15
- make -devel arch'd again, python3-dbus support

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-14
- add Provides: python-qt4... for new subpkgs

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-13
- own qsci-api dirs here for now

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-12
- typo, missing %%endif

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-11
- doc.noarch,-qsci-api subpkgs

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-10
- no more sitelib/PyQt4

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-9
- simpler approach, avoid symlink and just copy

* Fri Mar 14 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-8
- polish/improve uic multilib issues, make -devel noarch (#1076346)

* Mon Feb 17 2014 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-7
- flesh out python(3)-qt4 related provides

* Fri Dec 06 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-6
- rebuild (phonon)

* Thu Nov 21 2013 Rex Dieter <rdieter@math.unl.edu> - 4.10.3-5
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
