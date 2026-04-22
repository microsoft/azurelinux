# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname wxpython4
%global srcname wxPython
%bcond_without tests
%global sum New implementation of wxPython, a GUI toolkit for Python
%global desc \
wxPython4 is a is a new implementation of wxPython focused on improving speed,\
maintainability and extensibility. Just like "Classic" wxPython it wraps the\
wxWidgets C++ toolkit and provides access to the user interface portions of the\
wx API, enabling Python applications to have a GUI on Windows, Macs or Unix\
systems with a native look and feel and requiring very little (if any) platform\
specific code.

Name:           python-wxpython4
Version:        4.2.4
Release: 2%{?dist}
Summary:        %{sum}
# wxPython is licensed under the wxWidgets license.  The only exception is
# the pubsub code in wx/lib/pubsub which is BSD licensed.  Note: wxPython
# includes a bundled copy of wxWidgets in ext/wxWidgets which has a few
# bits of code that use other licenses.  This source is not used in the
# Fedora build, except for the interface headers in ext/wxWidgets/interface
# and the doxygen build scripts.
License:        LGPL-2.0-or-later WITH WxWindows-exception-3.1 AND BSD-2-Clause
URL:            https://www.wxpython.org/
Source0:        https://files.pythonhosted.org/packages/source/w/%{srcname}/wxpython-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  waf
BuildRequires:  wxGTK-devel
# For tests
%if %{with tests}
BuildRequires:  glibc-langpack-en
BuildRequires:  mesa-dri-drivers
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  python3-numpy
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-forked
BuildRequires:  python3-pytest-timeout
BuildRequires:  python3-pytest-xdist
BuildRequires:  vulkan-loader
%endif

%description %{desc}

%package -n python3-%{pkgname}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{pkgname}}
BuildRequires:  python3-cython
BuildRequires:  python3-devel
BuildRequires:  python3-pillow
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3dist(sip) >= 6.8.5
Requires:       python3-pillow
Requires:       python3-six

%description -n python3-%{pkgname} %{desc}

%package -n python3-%{pkgname}-media
Summary:        %{sum} (media module)
%{?python_provide:%python_provide python3-%{pkgname}-media}
Requires:       python3-%{pkgname}%{?_isa} = %{version}-%{release}

%description -n python3-%{pkgname}-media %{desc}
This package provides the wx.media module.

%package -n python3-%{pkgname}-webview
Summary:        %{sum} (webview module)
%{?python_provide:%python_provide python3-%{pkgname}-webview}
Requires:       python3-%{pkgname}%{?_isa} = %{version}-%{release}

%description -n python3-%{pkgname}-webview %{desc}
This package provides the wx.html2 module.

%package        doc
Summary:        Documentation and samples for wxPython
BuildArch:      noarch

%description doc
Documentation, samples and demo application for wxPython.


%prep
%autosetup -n %{srcname}-%{version} -p1

rm -rf wx/py/tests
rm -f docs/sphinx/_downloads/i18nwxapp/i18nwxapp.zip
cp -a wx/lib/pubsub/LICENSE_BSD_Simple.txt license
# Remove env shebangs from various files
sed -i -e '/^#!\//, 1d' demo/*.py{,w}
sed -i -e '/^#!\//, 1d' demo/agw/*.py
sed -i -e '/^#!\//, 1d' docs/sphinx/_downloads/i18nwxapp/*.py
sed -i -e '/^#!\//, 1d' samples/floatcanvas/*.py
sed -i -e '/^#!\//, 1d' samples/mainloop/*.py
sed -i -e '/^#!\//, 1d' samples/ribbon/*.py
sed -i -e '/^#!\//, 1d' wx/py/*.py
sed -i -e '/^#!\//, 1d' wx/tools/*.py
# Fix end of line encodings
sed -i 's/\r$//' docs/sphinx/_downloads/*.py
sed -i 's/\r$//' docs/sphinx/rest_substitutions/snippets/python/contrib/*.py
sed -i 's/\r$//' docs/sphinx/rest_substitutions/snippets/python/converted/*.py
sed -i 's/\r$//' docs/sphinx/_downloads/i18nwxapp/locale/I18Nwxapp.pot
sed -i 's/\r$//' docs/sphinx/make.bat
sed -i 's/\r$//' samples/floatcanvas/BouncingBall.py
# Remove spurious executable perms
chmod -x demo/*.py
chmod -x samples/mainloop/mainloop.py
chmod -x samples/printing/sample-text.txt
# Remove empty files
find docs/sphinx/rest_substitutions/snippets/python/converted -size 0 -delete
# Convert files to UTF-8
for file in demo/TestTable.txt docs/sphinx/_downloads/i18nwxapp/locale/I18Nwxapp.pot; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
DOXYGEN=`which doxygen` WAF=`which waf` %{__python3} -u build.py dox touch etg --nodoc sip build_py --use_syswx --gtk3


%install
%{__python3} build.py install_py --destdir=%{buildroot} --extra_setup=--prefix=%{_prefix}
rm -f %{buildroot}%{_bindir}/*
# Remove locale files (they are provided by wxWidgets)
rm -rf %{buildroot}%{python3_sitearch}/wx/locale

%check
%if %{with tests}
SKIP_TESTS="'not (test_frameRestore or test_newIdRef03)'"
xvfb-run -a %{__python3} build.py test --pytest_timeout=60 --extra_pytest="-k $SKIP_TESTS" --verbose || true
%endif


%files -n python3-%{pkgname}
%license license/*
%{python3_sitearch}/*
%exclude %{python3_sitearch}/wx/*html2*
%exclude %{python3_sitearch}/wx/__pycache__/*html2*
%exclude %{python3_sitearch}/wx/*media*
%exclude %{python3_sitearch}/wx/__pycache__/*media*

%files -n python3-%{pkgname}-media
%{python3_sitearch}/wx/*media*
%{python3_sitearch}/wx/__pycache__/*media*

%files -n python3-%{pkgname}-webview
%{python3_sitearch}/wx/*html2*
%{python3_sitearch}/wx/__pycache__/*html2*

%files doc
%doc docs demo samples
%license license/*


%changelog
* Mon Dec 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 4.2.4-1
- 4.2.4

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.2.3-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.2.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.2.3-2
- Rebuilt for Python 3.14

* Fri Apr 11 2025 Scott Talbert <swt@techie.net> - 4.2.3-1
- Update to new upstream release 4.2.3 (#2358774)

* Sat Feb 22 2025 Scott Talbert <swt@techie.net> - 4.2.2-3
- Fix FTBFS w/ sip 6.10.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 16 2024 Scott Talbert <swt@techie.net> - 4.2.2-1
- Update to new upstream release 4.2.2 (#2311851)

* Wed Jul 31 2024 Scott Talbert <swt@techie.net> - 4.2.1-10
- Update License tag to use SPDX identifiers

* Tue Jul 23 2024 Scott Talbert <swt@techie.net> - 4.2.1-9
- Fix FTBFS w/ sip 6.8.5+

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 4.2.1-7
- Rebuilt for Python 3.13

* Sat Jan 27 2024 Scott Talbert <swt@techie.net> - 4.2.1-6
- Revert back to generating code and apply patches to fix FTBFS

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Scott Talbert <swt@techie.net> - 4.2.1-4
- BR python3-cython to fix FTBFS with Python 3.13 (#2252055)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 4.2.1-2
- Backport patches needed for compatibility with Python 3.12

* Mon Jun 19 2023 Scott Talbert <swt@techie.net> - 4.2.1-1
- Update to new upstream release 4.2.1 (#2208211 #2213374)
- Temporarily use upstream generated cpp files (broken by doxygen)
- Add missing BR for python3-pytest-forked to fix tests

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 4.2.0-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Scott Talbert <swt@techie.net> - 4.2.0-2
- Rebuild due to wxGLCanvas ABI change

* Mon Aug 08 2022 Scott Talbert <swt@techie.net> - 4.2.0-1
- Update to new upstream release 4.2.0 (#1827788)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Scott Talbert <swt@techie.net> - 4.0.7-31
- Update to build with sip 6.6.2+

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 4.0.7-30
- Rebuilt for Python 3.11

* Tue Mar 08 2022 Scott Talbert <swt@techie.net> - 4.0.7-29
- Fix even more Python 3.10 int/float issues (#2060854)

* Wed Feb 16 2022 Scott Talbert <swt@techie.net> - 4.0.7-28
- Fix additional Python 3.10 issues

* Wed Feb 16 2022 Scott Talbert <swt@techie.net> - 4.0.7-27
- Add more test BRs and enable more tests

* Mon Feb 14 2022 Scott Talbert <swt@techie.net> - 4.0.7-26
- Remove hard-coded references to siplib versions

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 28 2021 Scott Talbert <swt@techie.net> - 4.0.7-24
- Fix more Python 3.10 issues with AGW FlatNotebook (#2035790)

* Wed Dec 22 2021 Scott Talbert <swt@techie.net> - 4.0.7-23
- Fix a bunch of Python 3.10 issues

* Mon Oct 11 2021 Scott Talbert <swt@techie.net> - 4.0.7-22
- Fix build with sip 6.2.0

* Wed Aug 04 2021 Scott Talbert <swt@techie.net> - 4.0.7-21
- Remove patch for UnicodeDecodeError due to proper fix in sip

* Tue Aug 03 2021 Scott Talbert <swt@techie.net> - 4.0.7-20
- Fix UnicodeDecodeError on package import due to sip 6 (#1988466)

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-19
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Scott Talbert <swt@techie.net> - 4.0.7-18
- Fix building with sip 6

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.7-17
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 20:38:35 EST 2021 Scott Talbert <swt@techie.net> - 4.0.7-15
- Switch to building with sip 5

* Mon Jan 11 21:38:13 EST 2021 Scott Talbert <swt@techie.net> - 4.0.7-14
- Fix FTBFS with doxygen 1.9.1

* Thu Nov 26 09:38:13 EST 2020 Scott Talbert <swt@techie.net> - 4.0.7-13
- Backport upstream fix for wxPseudoDC.FindObjects crash (#1901912)

* Thu Nov  5 19:46:11 EST 2020 Scott Talbert <swt@techie.net> - 4.0.7-12
- Backport upstream fix for wxCustomDataObject.GetData crash

* Sat Oct 31 2020 Scott Talbert <swt@techie.net> - 4.0.7-11
- Fix crash in wxCustomDataObject.GetData

* Wed Aug 12 2020 Scott Talbert <swt@techie.net> - 4.0.7-10
- Remove BD on python3-pathlib2 (not needed)

* Mon Aug 03 2020 Scott Talbert <swt@techie.net> - 4.0.7-9
- Rebuild with latest wxGTK3 build to fix missing symbol issue (#1862822)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Scott Talbert <swt@techie.net> - 4.0.7-7
- Fix FTBFS with sip 4.19.23

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.7-6
- Rebuilt for Python 3.9

* Mon Feb 10 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.7-5
- Rebuilt to fix an undefined symbol (#1801244)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 11 2020 Scott Talbert <swt@techie.net> - 4.0.7-3
- Build using unbundled copy of waf (#1789646)

* Thu Nov 07 2019 Scott Talbert <swt@techie.net> - 4.0.7-2
- Remove BR on python-PyPDF2 - PDF tests are disabled by default anyway

* Sat Oct 26 2019 Scott Talbert <swt@techie.net> - 4.0.7-1
- Update to new upstream release 4.0.7 (#1765757)

* Mon Sep 16 2019 Scott Talbert <swt@techie.net> - 4.0.6-9
- Remove Python 2 subpackages (#1629793)

* Thu Aug 29 2019 Scott Talbert <swt@techie.net> - 4.0.6-8
- Switch to using private sip module, wx.siplib (#1739469)

* Wed Aug 28 2019 Scott Talbert <swt@techie.net> - 4.0.6-7
- Fix FloatCanvas with Python 3.8 (time.clock removed)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.6-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 25 2019 Scott Talbert <swt@techie.net> - 4.0.6-4
- Stop running tests for Python 2 to release some Py2 dependencies

* Wed Jul 17 2019 Scott Talbert <swt@techie.net> - 4.0.6-3
- Fix FTBFS due to easy_install switch to Python 3

* Fri Jun 28 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.0.6-2
- >= sip-api

* Tue May 21 2019 Scott Talbert <swt@techie.net> - 4.0.6-1
- Update to new upstream release 4.0.6 (#1711733)

* Sat May 18 2019 Scott Talbert <swt@techie.net> - 4.0.4-4
- Fix FTBFS with Python 3.8 (#1710767)

* Sat Apr 06 2019 Scott Talbert <swt@techie.net> - 4.0.4-3
- Fix FTBFS with SIP 4.19.14 (#1696302)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Scott Talbert <swt@techie.net> - 4.0.4-1
- New upstream release 4.0.4

* Tue Nov 20 2018 Scott Talbert <swt@techie.net> - 4.0.1-11
- Fix tests

* Sat Oct 27 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 4.0.1-10
- Rebuilt for sip update

* Mon Jul 16 2018 Scott Talbert <swt@techie.net> - 4.0.1-9
- Replace use of python3-sip binary with sip (fixes FTBFS)
- Use sip-api macros to ensure dependency on correct sip module version

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Scott Talbert <swt@techie.net> - 4.0.1-7
- Re-enable tests but enable pytest-timeout

* Wed Jun 20 2018 Scott Talbert <swt@techie.net> - 4.0.1-6
- Cherry-pick waf 2.0.7 updates to fix Python 3.7 FTBFS (#1593029)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-5
- Rebuilt for Python 3.7

* Mon Feb 19 2018 Scott Talbert <swt@techie.net> - 4.0.1-4
- Add missing BR for gcc-c++

* Thu Feb 15 2018 Scott Talbert <swt@techie.net> - 4.0.1-3
- Second round of review comment fixes

* Tue Feb 13 2018 Scott Talbert <swt@techie.net> - 4.0.1-2
- Address initial review comments
- Fix rpmlint errors
- Fix and enable tests (but they are still not required to pass)

* Wed Feb 07 2018 Scott Talbert <swt@techie.net> - 4.0.1-1
- Initial packaging
