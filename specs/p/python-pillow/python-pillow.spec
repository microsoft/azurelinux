# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global py3_incdir %(RPM_BUILD_ROOT= %{python3} -Ic 'import sysconfig; print(sysconfig.get_path("include"))')

%global srcname pillow

# Dependencies are missing to build the documentation
%bcond_with doc

%if 0%{?rhel} || 0%{?flatpak}
%bcond_with mingw
%else
%bcond_without mingw
%endif
%if 0%{?rhel}
%bcond_with qt
%else
%bcond_without qt
%endif

Name:           python-%{srcname}
Version:        11.3.0
Release:        7%{?dist}
Summary:        Python image processing library

# License: see http://www.pythonware.com/products/pil/license.htm
License:        MIT
URL:            http://python-pillow.github.io/
Source0:        https://github.com/python-pillow/Pillow/archive/%{version}/Pillow-%{version}.tar.gz

# MinGW build fixes
Patch0:         pillow_mingw.patch
# Backport fix for CVE-2026-25990
Patch1:         https://github.com/python-pillow/Pillow/commit/9000313cc5d4a31bdcdd6d7f0781101abab553aa.patch

BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  ghostscript
BuildRequires:  lcms2-devel
BuildRequires:  libimagequant-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libraqm-devel
BuildRequires:  libtiff-devel
BuildRequires:  libwebp-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  tk-devel
BuildRequires:  zlib-devel

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest

%if %{with doc}
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx-copybutton
BuildRequires:  python%{python3_pkgversion}-sphinx_rtd_theme
BuildRequires:  python%{python3_pkgversion}-sphinx-removed-in
%endif


%if %{with mingw}
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-python3
BuildRequires:  mingw32-python3-setuptools
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-freetype
BuildRequires:  mingw32-lcms2
BuildRequires:  mingw32-libimagequant
BuildRequires:  mingw32-libjpeg
BuildRequires:  mingw32-libtiff
BuildRequires:  mingw32-libwebp
BuildRequires:  mingw32-openjpeg2
BuildRequires:  mingw32-tk
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-python3
BuildRequires:  mingw64-python3-setuptools
BuildRequires:  mingw64-dlfcn
BuildRequires:  mingw64-freetype
BuildRequires:  mingw64-lcms2
BuildRequires:  mingw64-libimagequant
BuildRequires:  mingw64-libjpeg
BuildRequires:  mingw64-libtiff
BuildRequires:  mingw64-libwebp
BuildRequires:  mingw64-openjpeg2
BuildRequires:  mingw64-tk
BuildRequires:  mingw64-zlib
%endif

# For EpsImagePlugin.py
Requires:       ghostscript

%global __provides_exclude_from ^%{python3_sitearch}/PIL/.*\\.so$

%description
Python image processing library, fork of the Python Imaging Library (PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are four subpackages: tk (tk interface), qt (PIL image wrapper for Qt),
devel (development) and doc (documentation).


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Python 3 image processing library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Provides:       python%{python3_pkgversion}-imaging = %{version}-%{release}
# For MicImagePlugin.py, FpxImagePlugin.py
Requires:       python%{python3_pkgversion}-olefile

%description -n python%{python3_pkgversion}-%{srcname}
Python image processing library, fork of the Python Imaging Library (PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are four subpackages: tk (tk interface), qt (PIL image wrapper for Qt),
devel (development) and doc (documentation).


%package -n python%{python3_pkgversion}-%{srcname}-devel
Summary:        Development files for %{srcname}
Requires:       python%{python3_pkgversion}-devel, libjpeg-devel, zlib-devel
Requires:       python%{python3_pkgversion}-%{srcname}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}-devel}
Provides:       python%{python3_pkgversion}-imaging-devel = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}-devel
Development files for %{srcname}.


%package -n python%{python3_pkgversion}-%{srcname}-doc
Summary:        Documentation for %{srcname}
BuildArch:      noarch
Requires:       python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}-doc}
Provides:       python%{python3_pkgversion}-imaging-doc = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}-doc
Documentation for %{srcname}.


%package -n python%{python3_pkgversion}-%{srcname}-tk
Summary:        Tk interface for %{srcname}
Requires:       python%{python3_pkgversion}-tkinter
Requires:       python%{python3_pkgversion}-%{srcname}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}-tk}
Provides:       python%{python3_pkgversion}-imaging-tk = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}-tk
Tk interface for %{srcname}.


%if %{with qt}
%package -n python%{python3_pkgversion}-%{srcname}-qt
Summary:        Qt %{srcname} image wrapper
Requires:       python%{python3_pkgversion}-qt5
Requires:       python%{python3_pkgversion}-%{srcname}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}-qt}
Provides:       python%{python3_pkgversion}-imaging-qt = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}-qt
Qt %{srcname} image wrapper.
%endif


%if %{with mingw}
%package -n mingw32-python3-%{srcname}
Summary:       MinGW Windows Python2 %{srcname} library
BuildArch:     noarch

%description -n mingw32-python3-%{srcname}
MinGW Windows Python2 %{srcname} library.


%package -n mingw64-python3-%{srcname}
Summary:       MinGW Windows Python2 %{srcname} library
BuildArch:     noarch

%description -n mingw64-python3-%{srcname}
MinGW Windows Python2 %{srcname} library.


%{?mingw_debug_package}
%endif


%prep
%autosetup -p1 -n Pillow-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
# Native build
%pyproject_wheel

# MinGW build
%if %{with mingw}
PKG_CONFIG=mingw32-pkg-config %{mingw32_py3_build}
PKG_CONFIG=mingw64-pkg-config %{mingw64_py3_build}
%endif

# Doc build
%if %{with doc}
PYTHONPATH=$(echo $PWD/build/lib.linux-*) make -C docs html BUILDDIR=_build_py3 SPHINXBUILD=sphinx-build-%python3_version
rm -f docs/_build_py3/html/.buildinfo
%endif


%install
# Native build
%pyproject_install
install -d %{buildroot}/%{py3_incdir}/Imaging
install -m 644 src/libImaging/*.h %{buildroot}/%{py3_incdir}/Imaging

# MinGW build
%if %{with mingw}
(
%{mingw32_py3_install}
%{mingw64_py3_install}

install -d %{buildroot}/%{mingw32_py3_incdir}/Imaging
install -m 644 src/libImaging/*.h %{buildroot}/%{mingw32_py3_incdir}/Imaging

install -d %{buildroot}/%{mingw64_py3_incdir}/Imaging
install -m 644 src/libImaging/*.h %{buildroot}/%{mingw64_py3_incdir}/Imaging

# Remove sample scripts
rm -rf %{buildroot}%{mingw32_bindir}
rm -rf %{buildroot}%{mingw64_bindir}
)
%endif


%if %{with mingw}
%mingw_debug_install_post
%endif


%check
# Check Python 3 modules
ln -s $PWD/Images $(echo $PWD/build/lib.linux-*)/Images
cp -R $PWD/Tests $(echo $PWD/build/lib.linux-*)/Tests
cp -a $PWD/selftest.py $(echo $PWD/build/lib.linux-*)/selftest.py
pushd build/lib.linux-*
PYTHONPATH=$PWD %{__python3} selftest.py
popd
%ifnarch s390x
%pytest -v -k "not test_qt_image_qapplication" || :
%else
%pytest -v -k "not test_qt_image_qapplication" || :
%endif


%files -n python%{python3_pkgversion}-%{srcname}
%doc README.md CHANGES.rst
%license docs/COPYING
%{python3_sitearch}/PIL/
%{python3_sitearch}/pillow-%{version}.dist-info/
# These are in subpackages
%exclude %{python3_sitearch}/PIL/_imagingtk*
%exclude %{python3_sitearch}/PIL/ImageTk*
%exclude %{python3_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python3_sitearch}/PIL/ImageQt*
%exclude %{python3_sitearch}/PIL/__pycache__/ImageTk*
%exclude %{python3_sitearch}/PIL/__pycache__/SpiderImagePlugin*
%exclude %{python3_sitearch}/PIL/__pycache__/ImageQt*

%files -n python%{python3_pkgversion}-%{srcname}-devel
%{py3_incdir}/Imaging/

%if %{with doc}
%files -n python%{python3_pkgversion}-%{srcname}-doc
%doc docs/_build_py3/html
%endif

%files -n python%{python3_pkgversion}-%{srcname}-tk
%{python3_sitearch}/PIL/_imagingtk*
%{python3_sitearch}/PIL/ImageTk*
%{python3_sitearch}/PIL/SpiderImagePlugin*
%{python3_sitearch}/PIL/__pycache__/ImageTk*
%{python3_sitearch}/PIL/__pycache__/SpiderImagePlugin*

%if %{with qt}
%files -n python%{python3_pkgversion}-%{srcname}-qt
%{python3_sitearch}/PIL/ImageQt*
%{python3_sitearch}/PIL/__pycache__/ImageQt*
%endif

%if %{with mingw}
%files -n mingw32-python3-%{srcname}
%license docs/COPYING
%{mingw32_python3_sitearch}/PIL/
%{mingw32_python3_sitearch}/pillow-%{version}-py%{mingw32_python3_version}.egg-info/
%{mingw32_py3_incdir}/Imaging/

%files -n mingw64-python3-%{srcname}
%license docs/COPYING
%{mingw64_python3_sitearch}/PIL/
%{mingw64_python3_sitearch}/pillow-%{version}-py%{mingw64_python3_version}.egg-info/
%{mingw64_py3_incdir}/Imaging/
%endif


%changelog
* Sat Feb 14 2026 Sandro Mani <manisandro@gmail.com> - 11.1.0-7
- Backport fix for CVE-2026-25990

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 11.3.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Sep 09 2025 Sandro Mani <manisandro@gmail.com> - 11.3.0-5
- Rebuild (libimagequant)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 11.3.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Sandro Mani <manisandro@gmail.com> - 11.3.0-2
- Use pyproject macros

* Fri Jul 04 2025 Sandro Mani <manisandro@gmail.com> - 11.3.0-1
- Update to 11.3.0

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 11.2.1-2
- Rebuilt for Python 3.14

* Tue Apr 15 2025 Sandro Mani <manisandro@gmail.com> - 11.2.1-1
- Update to 11.2.1

* Wed Apr 02 2025 Sandro Mani <manisandro@gmail.com> - 11.2.0-1
- Update to 11.2.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Sandro Mani <manisandro@gmail.com> - 11.1.0-1
- Update to 11.1.0

* Tue Oct 15 2024 Sandro Mani <manisandro@gmail.com> - 11.0.0-1
- Update to 11.0.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Sandro Mani <manisandro@gmail.com> - 10.4.0-1
- Update to 10.4.0

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 10.3.0-2
- Rebuilt for Python 3.13

* Tue Apr 02 2024 Sandro Mani <manisandro@gmail.com> - 10.3.0-1
- Update to 10.3.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Sandro Mani <manisandro@gmail.com> - 10.2.0-1
- Update to 10.2.0

* Sun Oct 15 2023 Sandro Mani <manisandro@gmail.com> - 10.1.0-1
- Update to 10.1.0

* Mon Sep 18 2023 Sandro Mani <manisandro@gmail.com> - 10.0.1-1
- Update to 10.0.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Sandro Mani <manisandro@gmail.com> - 10.0.0-1
- Update to 10.0.0

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 9.5.0-2
- Rebuilt for Python 3.12

* Mon Apr 03 2023 Sandro Mani <manisandro@gmail.com> - 9.5.0-1
- Update to 9.5.0

* Sat Mar 04 2023 Sandro Mani <manisandro@gmail.com> - 9.4.0-3
- Rebuild (libimagequant)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Sandro Mani <manisandro@gmail.com> - 9.4.0-1
- Update to 9.4.0

* Mon Oct 31 2022 Sandro Mani <manisandro@gmail.com> - 9.3.0-2
- Rebuild (mingw-python-3.11)

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 9.3.0-1
- Update to 9.3.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 03 2022 Sandro Mani <manisandro@gmail.com> - 9.2.0-1
- Update to 9.2.0

* Wed Jun 22 2022 Charalampos Stratakis <cstratak@redhat.com> - 9.1.1-4
- Fix FTBFS with setuptools >= 62.1
Resolves: rhbz#2097095

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 9.1.1-3
- Rebuilt for Python 3.11

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 9.1.1-2
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 9.1.1-1
- Update to 9.1.1

* Tue Apr 05 2022 Sandro Mani <manisandro@gmail.com> - 9.1.0-1
- Update to 9.1.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 9.0.1-7
- Rebuild with mingw-gcc-12

* Thu Mar 03 2022 Sandro Mani <manisandro@gmail.com> - 9.0.1-6
- Fix name -> srcname

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 9.0.1-5
- Make mingw subpackages noarch

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 9.0.1-4
- Add mingw subpackages

* Thu Feb 03 2022 Sandro Mani <manisandro@gmail.com> - 9.0.1-1
- Update to 9.0.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Sandro Mani <manisandro@gmail.com> - 9.0.0-1
- Update to 9.0.0

* Fri Oct 15 2021 Sandro Mani <manisandro@gmail.com> - 8.4.0-1
- Update to 8.4.0

* Fri Sep 03 2021 Sandro Mani <manisandro@gmail.com> - 8.3.2-1
- Update to 8.3.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Sandro Mani <manisandro@gmail.com> - 8.3.1-1
- Update to 8.3.1

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 8.2.0-3
- Rebuilt for Python 3.10

* Mon May 24 2021 Sandro Mani <manisandro@gmail.com> - 8.2.0-2
- Run full test suite

* Fri Apr 02 2021 Sandro Mani <manisandro@gmail.com> - 8.2.0-1
- Update to 8.2.0

* Sat Mar 06 2021 Sandro Mani <manisandro@gmail.com> - 8.1.2-1
- Update to 8.1.2

* Tue Mar 02 2021 Sandro Mani <manisandro@gmail.com> - 8.1.1-1
- Update to 8.1.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 09 2021 Robert-André Mauchin <zebob.m@gmail.com> - 8.1.0-2
- Add patch to fix the import error occurring with Python 3.10
- Fix: rhbz#1904379

* Sun Jan 03 2021 Sandro Mani <manisandro@gmail.com> - 8.1.0-1
- Update to 8.1.0

* Fri Oct 23 2020 Sandro Mani <manisandro@gmail.com> - 8.0.1-1
- Update to 8.0.1

* Thu Oct 15 2020 Sandro Mani <manisandro@gmail.com> - 8.0.0-1
- Update to 8.0.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Sandro Mani <manisandro@gmail.com> - 7.2.0-1
- Update to 7.2.0

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 7.1.2-2
- Rebuilt for Python 3.9

* Sat Apr 25 2020 Sandro Mani <manisandro@gmail.com> - 7.1.2-1
- Update to 7.1.2

* Tue Apr 21 2020 Charalampos Stratakis <cstratak@redhat.com> - 7.1.1-2
- Fix html docs build failure with Sphinx3 (rhbz#1823884)

* Thu Apr 02 2020 Sandro Mani <manisandro@gmail.com> - 7.1.1-1
- Update to 7.1.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Sandro Mani <manisandro@gmail.com> - 7.0.0-1
- Update to 7.0.0
- Drop python2 packages

* Mon Oct 21 2019 Sandro Mani <manisandro@gmail.com> - 6.2.1-1
- Update to 6.2.1

* Mon Oct 07 2019 Petr Viktorin <pviktori@redhat.com> - 6.2.0-2
- Remove optional build dependency on python2-cffi

* Tue Oct 01 2019 Sandro Mani <manisandro@gmail.com> - 6.2.0-1
- Update to 6.2.0

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-4
- Rebuilt for Python 3.8

* Mon Aug 12 2019 Sandro Mani <manisandro@gmail.com> - 6.1.0-3
- Drop python2-pillow-qt, python2-pillow-tk

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Sandro Mani <manisandro@gmail.com> - 6.1.0-1
- Update to 6.1.0

* Fri May 31 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 6.0.0-2
- Fix broken Python/C interop on s390x

* Tue Apr 02 2019 Sandro Mani <manisandro@gmail.com> - 6.0.0-1
- Update to 6.0.0

* Sun Mar 10 2019 Sandro Mani <manisandro@gmail.com> - 5.4.1-4
- Drop python2-pillow-doc

* Mon Mar 04 2019 Yatin Karel <ykarel@redhat.com> - 5.4.1-3
- Fix python3 conditional

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Sandro Mani <manisandro@gmail.com> - 5.4.1-1
- Update to 5.4.1

* Mon Oct 01 2018 Sandro Mani <manisandro@gmail.com> - 5.3.0-1
- Update to 5.3.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 5.2.0-2
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Sandro Mani <manisandro@gmail.com> - 5.2.0-1
- Update to 5.2.0

* Wed Jun 27 2018 Miro Hrončok <mhroncok@redhat.com> - 5.1.1-3
- Fix the tkinter dependency

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 5.1.1-2
- Rebuilt for Python 3.7

* Wed Apr 25 2018 Sandro Mani <manisandro@gmail.com> - 5.1.1-1
- Update to 5.1.1

* Thu Apr 05 2018 Sandro Mani <manisandro@gmail.com> - 5.1.0-1
- Update to 5.1.0

* Wed Mar 07 2018 Sandro Mani <manisandro@gmail.com> - 5.0.0-3
- Add missing BR: gcc

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Sandro Mani <manisandro@gmail.com> - 5.0.0-1
- Update to 5.0.0

* Tue Oct 03 2017 Sandro Mani <manisandro@gmail.com> - 4.3.0-1
- Update to 4.3.0

* Tue Sep 05 2017 Troy Dawson <tdawson@redhat.com> - 4.2.1-5
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.2.1-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu Jul 06 2017 Sandro Mani <manisandro@gmail.com> - 4.2.1-1
- Update to 4.2.1

* Sat Jul 01 2017 Sandro Mani <manisandro@gmail.com> - 4.2.0-1
- Update to 4.2.0

* Fri Apr 28 2017 Sandro Mani <manisandro@gmail.com> - 4.1.1-1
- Update to 4.1.1

* Wed Apr 05 2017 Sandro Mani <manisandro@gmail.com> - 4.1.0-1
- Update to 4.1.0

* Wed Feb 15 2017 Sandro Mani <manisandro@gmail.com> - 4.0.0-3
- Fix some __pycache__ files in wrong subpackage (#1422606)

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 4.0.0-2
- Rebuild (libwebp)

* Tue Jan 03 2017 Sandro Mani <manisandro@gmail.com> - 4.0.0-1
- Update to 4.0.0

* Mon Dec 12 2016 Miro Hrončok <mhroncok@redhat.com> - 3.4.2-3
- Enable docs build

* Mon Dec 12 2016 Miro Hrončok <mhroncok@redhat.com> - 3.4.2-2
- Rebuild for Python 3.6

* Wed Oct 19 2016 Sandro Mani <manisandro@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Tue Oct 04 2016 Sandro Mani <manisandro@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Oct 03 2016 Sandro Mani <manisandro@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Thu Aug 18 2016 Sandro Mani <manisandro@gmail.com> - 3.3.1-1
- Update  to 3.3.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Jul 02 2016 Sandro Mani <manisandro@gmail.com> - 3.3.0-1
- Update to 3.3.0
- Modernize spec

* Fri Apr 01 2016 Sandro Mani <manisandro@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Wed Feb 10 2016 Sandro Mani <manisandro@gmail.com> - 3.1.1-3
- Fix broken python3-pillow package description

* Sun Feb 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.1.1-2
- Fix provides

* Thu Feb 04 2016 Sandro Mani <manisandro@gmail.com> - 3.1.1-1
- Update to 3.1.1
- Fixes CVE-2016-0740, CVE-2016-0775

* Mon Jan 11 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.0-2
- Fix executable files in doc package bringing in python 2 for the python3 doc
  packages

* Mon Jan 04 2016 Sandro Mani <manisandro@gmail.com> - 3.1.0-1
- Update to 3.1.0

* Tue Dec 29 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.0.0-5
- Build with docs

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.0.0-4
- Rebuilt for libwebp soname bump

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 3.0.0-3
- Rebuilt for Python3.5 rebuild with docs

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 3.0.0-2
- Rebuilt for Python3.5 rebuild without docs

* Fri Oct 02 2015 Sandro Mani <manisandro@gmail.com> - 3.0.0-1
- Update to 3.0.0

* Wed Jul 29 2015 Sandro Mani <manisandro@gmail.com> - 2.9.0-2
- Fix python3-pillow-tk Requires: tkinter -> python3-tkinter (#1248085)

* Thu Jul 02 2015 Sandro Mani <manisandro@gmail.com> - 2.9.0-1
- Update to 2.9.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Sandro Mani <manisandro@gmail.com> - 2.8.2-1
- Update to 2.8.2

* Thu Apr 02 2015 Sandro Mani <manisandro@gmail.com> - 2.8.1-1
- Update to 2.8.1

* Wed Apr 01 2015 Sandro Mani <manisandro@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Mon Jan 12 2015 Sandro Mani <manisandro@gmail.com> - 2.7.0-1
- Update to 2.7.0
- Drop sane subpackage, is in python-sane now
- Fix python3 headers directory
- Drop Obsoletes: python3-pillow on python3-pillow-qt

* Mon Oct 13 2014 Sandro Mani <manisandro@gmail.com> - 2.6.1-1
- Update to 2.6.1

* Thu Oct 02 2014 Sandro Mani <manisandro@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Wed Aug 20 2014 Sandro Mani <manisandro@gmail.com> - 2.5.3-3
- Rebuilding again to resolve transient build error that caused BZ#1131723

* Tue Aug 19 2014 Stephen Gallagher <sgallagh@redhat.com> - 2.5.3-2
- Rebuilding to resolve transient build error that caused BZ#1131723

* Tue Aug 19 2014 Sandro Mani <manisandro@gmail.com> - 2.5.3-1
- Update to 2.5.3 (Fix CVE-2014-3598, a DOS in the Jpeg2KImagePlugin)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Sandro Mani <manisandro@gmail.com> - 2.5.2-1
- Update to 2.5.2 (Fix CVE-2014-3589, a DOS in the IcnsImagePlugin)

* Sat Jul 26 2014 Sandro Mani <manisandro@gmail.com> - 2.5.1-2
- Reenable jpeg2k tests on big endian arches

* Tue Jul 15 2014 Sandro Mani <manisandro@gmail.com> - 2.5.1-1
- Update to 2.5.1

* Wed Jul 02 2014 Sandro Mani <manisandro@gmail.com> - 2.5.0-1
- Update to 2.5.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Sandro Mani <manisandro@gmail.com> - 2.4.0-10
- Rebuild with docs enabled
- Update python-pillow_openjpeg-2.1.0.patch

* Tue May 27 2014 Sandro Mani <manisandro@gmail.com> - 2.4.0-9
- Rebuild against openjpeg-2.1.0

* Fri May 23 2014 Dan Horák <dan[at]danny.cz> - 2.4.0-8
- skip jpeg2k tests on big endian arches (#1100762)

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.0-6
- Set with_docs to 1 to build docs.

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.0-5
- Bootstrap building sphinx docs because of circular dependency with sphinx.

* Fri May  9 2014 Orion Poplawski <orion@cora.nwra.com> - 2.4.0-4
- Rebuild for Python 3.4

* Tue Apr 22 2014 Sandro Mani <manisandro@gmail.com> - 2.4.0-3
- Add patch: Have the tempfile use a suffix with a dot

* Thu Apr 17 2014 Sandro Mani <manisandro@gmail.com> - 2.4.0-2
- Enable Jpeg2000 support
- Enable webp support also on s390* archs, bug #962091 is now fixed
- Add upstream patch for ghostscript detection

* Wed Apr 02 2014 Sandro Mani <manisandro@gmail.com> - 2.4.0-1
- Update to 2.4.0

* Wed Mar 19 2014 Sandro Mani <manisandro@gmail.com> - 2.3.1-1
- Update to 2.3.1 (Fix insecure use of tempfile.mktemp (CVE-2014-1932 CVE-2014-1933))

* Thu Mar 13 2014 Jakub Dorňák <jdornak@redhat.com> - 2.3.0-5
- python-pillow does not provide python3-imaging
  (python3-pillow does)

* Tue Jan 07 2014 Sandro Mani <manisandro@gmail.com> - 2.3.0-4
- Add missing ghostscript Requires and BuildRequires

* Mon Jan 06 2014 Sandro Mani <manisandro@gmail.com> - 2.3.0-3
- Remove python-pillow_help-theme.patch, add python-sphinx-theme-better BR

* Sun Jan 05 2014 Sandro Mani <manisandro@gmail.com> - 2.3.0-2
- Rebuild with docs enabled
- Change lcms BR to lcms2

* Thu Jan 02 2014 Sandro Mani <manisandro@gmail.com> - 2.3.0-1
- Update to 2.3.0
- Build with doc disabled to break circular python-pillow -> python-sphinx -> python pillow dependency

* Wed Oct 23 2013 Sandro Mani <manisandro@gmail.com> - 2.2.1-2
- Backport fix for decoding tiffs with correct byteorder, fixes rhbz#1019656

* Wed Oct 02 2013 Sandro Mani <manisandro@gmail.com> - 2.2.1-1
- Update to 2.2.1
- Really enable webp on ppc, but leave disabled on s390

* Thu Aug 29 2013 Sandro Mani <manisandro@gmail.com> - 2.1.0-4
- Add patch to fix incorrect PyArg_ParseTuple tuple signature, fixes rhbz#962091 and rhbz#988767.
- Renable webp support on bigendian arches

* Wed Aug 28 2013 Sandro Mani <manisandro@gmail.com> - 2.1.0-3
- Add patch to fix memory corruption caused by invalid palette size, see rhbz#1001122

* Tue Jul 30 2013 Karsten Hopp <karsten@redhat.com> 2.1.0-2
- Build without webp support on ppc* archs (#988767)

* Wed Jul 03 2013 Sandro Mani <manisandro@gmail.com> - 2.1.0-1
- Update to 2.1.0
- Run tests in builddir, not installroot
- Build python3-pillow docs with python3
- python-pillow_endian.patch upstreamed

* Mon May 13 2013 Roman Rakus <rrakus@redhat.com> - 2.0.0-10
- Build without webp support on s390* archs
  Resolves: rhbz#962059

* Sat May 11 2013 Roman Rakus <rrakus@redhat.com> - 2.0.0-9.gitd1c6db8
- Conditionaly disable build of python3 parts on RHEL system

* Wed May 08 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-8.gitd1c6db8
- Add patch to fix test failure on big-endian

* Thu Apr 25 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.0-7.gitd1c6db8
- Remove Obsoletes in the python-pillow-qt subpackage. Obsoletes isn't
  appropriate since qt support didn't exist in the previous python-pillow
  package so there's no reason to drag in python-pillow-qt when updating
  python-pillow.

* Fri Apr 19 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-6.gitd1c6db8
- Update to latest git
- python-pillow_quantization.patch now upstream
- python-pillow_endianness.patch now upstream
- Add subpackage for ImageQt module, with correct dependencies
- Add PyQt4 and numpy BR (for generating docs / running tests)

* Mon Apr 08 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-5.git93a488e
- Reenable tests on bigendian, add patches for #928927

* Sun Apr 07 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-4.git93a488e
- Update to latest git
- disable tests on bigendian (PPC*, S390*) until rhbz#928927 is fixed

* Fri Mar 22 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-3.gitde210a2
- python-pillow_tempfile.patch now upstream
- Add python3-imaging provides (bug #924867)

* Fri Mar 22 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-2.git2e88848
- Update to latest git
- Remove python-pillow-disable-test.patch, gcc is now fixed
- Add python-pillow_tempfile.patch to prevent a temporary file from getting packaged

* Tue Mar 19 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-1.git2f4207c
- Update to 2.0.0 git snapshot
- Enable python3 packages
- Add libwebp-devel BR for Pillow 2.0.0

* Wed Mar 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.8-6.20130305git
- Add ARM support

* Tue Mar 12 2013 Karsten Hopp <karsten@redhat.com> 1.7.8-5.20130305git
- add s390* and ppc* to arch detection

* Tue Mar 05 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-4.20130305git7866759
- Update to latest git snapshot
- 0001-Cast-hash-table-values-to-unsigned-long.patch now upstream
- Pillow-1.7.8-selftest.patch now upstream

* Mon Feb 25 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-3.20130210gite09ff61
- Really remove -fno-strict-aliasing
- Place comment on how to retreive source just above the Source0 line

* Mon Feb 18 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-2.20130210gite09ff61
- Rebuild without -fno-strict-aliasing
- Add patch for upstream issue #52

* Sun Feb 10 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-1.20130210gite09ff61
- Initial RPM package
