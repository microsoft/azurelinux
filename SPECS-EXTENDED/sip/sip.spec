Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond_without python3

%if %{with python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%endif
%{!?__python2:%global __python2 /usr/bin/python2}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}

%global PYINCLUDE %{_includedir}/python%{python3_version}


%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

# see also https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/JQQ66XJSIT2FGTK2YQY7AXMEH5IXMPUX/
%undefine _strict_symbol_defs_build

Summary: SIP - Python/C++ Bindings Generator
Name: sip
Version: 4.19.21
Release: 2%{?dist}

# sipgen/parser.{c.h} is GPLv3+ with exceptions (bison)
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)
Url: https://www.riverbankcomputing.com/software/sip/intro 
Source0: https://www.riverbankcomputing.com/static/Downloads/sip/%{version}/sip-%{version}%{?snap:.%{snap}}.tar.gz

Source10: sip-wrapper.sh

## upstream patches

## upstreamable patches
# make install should not strip (by default), kills -debuginfo
Patch50: sip-4.18-no_strip.patch
# try not to rpath the world (I *think* this may not be required anymore, since sip-4.19 -- rex)
Patch51: sip-4.18-no_rpath.patch
# set sip_bin properly for python3 build (needswork to be upstreamable)
# no longer needed?  keep for a little while before dropping completely -- rex
#Patch52: sip-4.19.3-python3_sip_bin.patch
# Avoid hardcoding sip.so (needed for wxpython's siplib.so)
Patch53: sip-4.19.18-no_hardcode_sip_so.patch

# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
Source1: macros.sip
%global _sip_api_major 12
%global _sip_api_minor 7
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

BuildRequires: gcc-c++
BuildRequires: sed

Obsoletes: sip-macros < %{version}-%{release}
Provides:  sip-macros = %{version}-%{release}

# upgrade path when no_namespace variants are dropped
%if ! 0%{?no_namespace}
Obsoletes: python2-sip < %{version}-%{release}
Obsoletes: python3-sip < %{version}-%{release}
%endif

%global _description\
SIP is a tool for generating bindings for C++ classes so that they can be\
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,\
because it is specifically designed for C++ and Python, is able to generate\
tighter bindings. SIP is so called because it is a small SWIG.\
\
SIP was originally designed to generate Python bindings for KDE and so has\
explicit support for the signal slot mechanism used by the Qt/KDE class\
libraries. However, SIP can be used to generate Python bindings for any C++\
class library.

%description %_description

%if %{with python2}
%if 0%{?no_namespace}
%package -n python2-sip
Summary: %summary
Provides: sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
Provides: python2-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-sip}
%description -n python2-sip %_description
%endif

%package -n python2-sip-devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: sip = %{version}-%{release}
#Requires: python2-sip%{?_isa} = %{version}-%{release}
BuildRequires: python2-devel
Requires:      python2-devel
# Remove before F30
Provides: sip-devel = %{version}-%{release}
Provides: sip-devel%{?_isa} = %{version}-%{release}
Obsoletes: sip-devel < %{version}-%{release}
%description -n python2-sip-devel
%{summary}.

%package -n python2-pyqt4-sip
Summary: %summary
Provides: python2-pyqt4-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-pyqt4-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-pyqt4-sip}
%description -n python2-pyqt4-sip %_description

%package -n python2-pyqt5-sip
Summary: %summary
Provides: python2-pyqt5-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-pyqt5-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-pyqt5-sip}
%description -n python2-pyqt5-sip %_description

%package -n python2-wx-siplib
Summary: %summary
Provides: python2-wx-siplib-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-wx-siplib-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-wx-siplib}
%description -n python2-wx-siplib %_description
%endif

%if %{with python3}
%if 0%{?no_namespace}
%package -n python%{python3_pkgversion}-sip
Summary: SIP - Python 3/C++ Bindings Generator
Provides: python%{python3_pkgversion}-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-sip
This is the Python 3 build of SIP.

%_description
%endif

%package -n python%{python3_pkgversion}-sip-devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: sip = %{version}-%{release}
#Requires: python3-sip%{?_isa} = %{version}-%{release}
BuildRequires: python%{python3_pkgversion}-devel
Requires:      python%{python3_pkgversion}-devel
%description -n python%{python3_pkgversion}-sip-devel
%{summary}.

%package -n python%{python3_pkgversion}-pyqt4-sip
Summary: SIP - Python 3/C++ Bindings Generator for pyqt4
BuildRequires: python%{python3_pkgversion}-devel
Provides: python%{python3_pkgversion}-pyqt4-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-pyqt4-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-pyqt4-sip
This is the Python 3 build of pyqt4-SIP.

%package -n python%{python3_pkgversion}-pyqt5-sip
Summary: SIP - Python 3/C++ Bindings Generator for pyqt5
BuildRequires: python%{python3_pkgversion}-devel
Provides: python%{python3_pkgversion}-pyqt5-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-pyqt5-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-pyqt5-sip
This is the Python 3 build of pyqt5-SIP.

%package -n python%{python3_pkgversion}-wx-siplib
Summary: SIP - Python 3/C++ Bindings Generator for wx
BuildRequires: python%{python3_pkgversion}-devel
Provides: python%{python3_pkgversion}-wx-siplib-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-wx-siplib-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-wx-siplib
This is the Python 3 build of wx-siplib.

%_description

%endif


%prep

%setup -q -n %{name}-%{version}%{?snap:.%{snap}}

%patch 50 -p1 -b .no_strip
%patch 51 -p1 -b .no_rpath
%patch 53 -p1 -b .no_sip_so


%build
%if %{with python2}
%if 0%{?no_namespace}
mkdir %{_target_platform}-python2
pushd %{_target_platform}-python2
%{__python2} ../configure.py \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd
%endif

mkdir %{_target_platform}-python2-pyqt4
pushd %{_target_platform}-python2-pyqt4
%{__python2} ../configure.py \
  --sip-module=PyQt4.sip \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd

mkdir %{_target_platform}-python2-pyqt5
pushd %{_target_platform}-python2-pyqt5
%{__python2} ../configure.py \
  --sip-module=PyQt5.sip \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd

sed -i -e 's|target = sip|target = siplib|g' siplib/siplib.sbf
mkdir %{_target_platform}-python2-wx
pushd %{_target_platform}-python2-wx
%{__python2} ../configure.py \
  --sip-module=wx.siplib \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd
%endif
sed -i -e 's|target = siplib|target = sip|g' siplib/siplib.sbf

%if %{with python3}
%if 0%{?no_namespace}
mkdir %{_target_platform}-python3
pushd %{_target_platform}-python3
%{__python3} ../configure.py \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd
%endif

mkdir %{_target_platform}-python3-pyqt4
pushd %{_target_platform}-python3-pyqt4
%{__python3} ../configure.py \
  --sip-module=PyQt4.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd

mkdir %{_target_platform}-python3-pyqt5
pushd %{_target_platform}-python3-pyqt5
%{__python3} ../configure.py \
  --sip-module=PyQt5.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd

sed -i -e 's|target = sip|target = siplib|g' siplib/siplib.sbf
mkdir %{_target_platform}-python3-wx
pushd %{_target_platform}-python3-wx
%{__python3} ../configure.py \
  --sip-module=wx.siplib \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%make_build
popd
sed -i -e 's|target = siplib|target = sip|g' siplib/siplib.sbf

%endif


%install
# Perform the Python 3 installation first, to avoid stomping over the Python 2
# /usr/bin/sip:
%if %{with python3}
%if 0%{?no_namespace}
%make_install -C %{_target_platform}-python3
%endif
%make_install -C %{_target_platform}-python3-pyqt4
%make_install -C %{_target_platform}-python3-pyqt5
%make_install -C %{_target_platform}-python3-wx
mv %{buildroot}%{python3_sitearch}/wx/sip.pyi %{buildroot}%{python3_sitearch}/wx/siplib.pyi
ln -s sip %{buildroot}%{_bindir}/python3-sip

## toplevel __pycache__ creation is ... inconsistent
## rawhide makes one, f23 local builds do not, so let's *make* it consistent
mkdir -p %{buildroot}%{python3_sitearch}/__pycache__/exclude_rpm_hack
%endif

# Python 2 installation:
%if %{with python2}
%if 0%{?no_namespace}
%make_install -C %{_target_platform}-python2
%endif
%make_install -C %{_target_platform}-python2-pyqt4
%make_install -C %{_target_platform}-python2-pyqt5
%make_install -C %{_target_platform}-python2-wx
mv %{buildroot}%{python2_sitearch}/wx/sip.pyi %{buildroot}%{python2_sitearch}/wx/siplib.pyi
%endif

# sip-wrapper
install %{SOURCE10} %{buildroot}%{_bindir}/sip-pyqt4
install %{SOURCE10} %{buildroot}%{_bindir}/sip-pyqt5
install %{SOURCE10} %{buildroot}%{_bindir}/sip-wx
sed -i -e 's|@SIP_MODULE@|PyQt4.sip|g' %{buildroot}%{_bindir}/sip-pyqt4
sed -i -e 's|@SIP_MODULE@|PyQt5.sip|g' %{buildroot}%{_bindir}/sip-pyqt5
sed -i -e 's|@SIP_MODULE@|wx.siplib|g' %{buildroot}%{_bindir}/sip-wx

mkdir -p %{buildroot}%{_datadir}/sip

# Macros used by -devel subpackages:
install -D -p -m644 %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.sip


%files
%doc README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{_bindir}/sip
# sip-wrappers
%{_bindir}/sip-pyqt4
%{_bindir}/sip-pyqt5
%{_bindir}/sip-wx
# compat symlink
%{_bindir}/python3-sip
%dir %{_datadir}/sip/
%{rpm_macros_dir}/macros.sip

%if %{with python2}
%files -n python2-sip-devel
%{_prefix}/include/python2.7/sip.h
%{python2_sitearch}/sipconfig.py*
%{python2_sitearch}/sipdistutils.py*

%if 0%{?no_namespace}
%files -n python2-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python2_sitearch}/sip.*
%{python2_sitearch}/sip-%{version}.dist-info/
%endif

%files -n python2-pyqt4-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python2_sitearch}/PyQt4/
%{python2_sitearch}/PyQt4_sip-%{version}.dist-info/

%files -n python2-pyqt5-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python2_sitearch}/PyQt5/
%{python2_sitearch}/PyQt5/sip.*
%{python2_sitearch}/PyQt5_sip-%{version}.dist-info/

%files -n python2-wx-siplib
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python2_sitearch}/wx/
%{python2_sitearch}/wx/siplib.*
%{python2_sitearch}/wx_siplib-%{version}.dist-info/
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-sip-devel
%{PYINCLUDE}/sip.h
%{python3_sitearch}/sipconfig.py*
%{python3_sitearch}/sipdistutils.py*
%{python3_sitearch}/__pycache__/*
%exclude %{python3_sitearch}/__pycache__/exclude_rpm_hack

%if 0%{?no_namespace}
%files -n python%{python3_pkgversion}-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python3_sitearch}/sip.*
%{python3_sitearch}/sip-%{version}.dist-info/
%endif

%files -n python%{python3_pkgversion}-pyqt4-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/sip.*
%{python3_sitearch}/PyQt4_sip-%{version}.dist-info/

%files -n python%{python3_pkgversion}-pyqt5-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/PyQt5/
%{python3_sitearch}/PyQt5/sip.*
%{python3_sitearch}/PyQt5_sip-%{version}.dist-info/

%files -n python%{python3_pkgversion}-wx-siplib
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/wx/
%{python3_sitearch}/wx/siplib.*
%{python3_sitearch}/wx_siplib-%{version}.dist-info/
%endif


%changelog
* Tue Feb 23 2021 Henry Li <lihl@microsoft.com> - 4.19.21-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove conditions that do not apply

* Fri Jan 31 2020 Rex Dieter <rdieter@fedoraproject.org> - 4.19.21-1
- 4.19.21

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.20-1
- 4.19.20, adjust whitespace

* Fri Nov 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.19-4
- disable python2 support on f32+ (#1752802)

* Sun Nov 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.19-3
- revert virtual provides (bad idea)

* Thu Oct 31 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.19.19-2
- Add virtual provides python{2,3}-sip

* Wed Sep 25 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.19-1
- 4.19.19, sip-api(12)=12.7
- Obsoletes: python2-sip python3-sip (when omitted for f31+)

* Mon Sep 16 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.18-7
- drop no_namespace variant for f31+

* Fri Sep 06 2019 Scott Talbert <swt@techie.net> - 4.19.18-6
- Simplify PYINCLUDE conditional and fix for F31

* Wed Aug 28 2019 Gwyn Ciesla <gwync@protonmail.com> 4.19.18-5
- Conditionalize Python 3 include dir.

* Mon Aug 19 2019 Scott Talbert <swt@techie.net> - 4.19.18-4
- Build a namespaced sip module, wx.siplib, for wxpython (#1739469)

* Mon Aug 19 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.19.18-3
- Set paths for flatpak.

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 4.19.18-2
- Rebuilt for Python 3.8

* Sun Aug 04 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.18-1
- 4.19.18

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.17-1
- 4.19.17

* Thu Apr 11 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.16-1
- 4.19.16

* Thu Mar 21 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.19.15-1
- 4.19.15, - sip-api(12)=12.6

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.13-3
- restore non-namespaced python-sip module

* Wed Oct 24 2018 Than Ngo <than@redhat.com> - 4.19.13-2
- Fix python3 subpackages files ownership within __pycache__ (#1619099)

* Wed Oct 03 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.13-1
- 4.19.3
- drop non-namespaced python-sip modules
- FIXME/TODO: add Obsoletes somewhere

* Sun Aug 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-9
- include sip-pyqt4/sip-pyqt5 wrappers

* Fri Aug 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-8
- -devel: move sipconfig/sipdistutils here
- -devel: drop dep on non-private base pkg (which may go away soon anyway)
- -devel: move subpkg defs nearer its basepkg in .spec
- (more) consistently use %%python3_pkgversion
- drop (uneeded) python3_sip_bin.patch

* Tue Aug 14 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-7
- include dist-info (#1524189)

* Tue Aug 14 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-6
- provide python?-pyqt4-sip too
- tighten dir ownership of sip python module dir(s)

* Mon Jul 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-5
- python?-devel: Requires: python?-sip
- add python3-sip compat symlink

* Sun Jul 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-4
- sip-api(12)=12.5

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-2
- *-devel: Requires: sip.
- drop Obsoletes: sip, now that we have a real sip pkg again

* Tue Jul 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-1
- 4.19.12

* Thu Jul 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.12-0.1.dev1807041651
- 4.19.12 snapshot

* Mon Jul 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.11-1
- 4.19.11

* Sun Jul 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.10-1
- 4.19.10

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 4.19.9-0.2.dev1805261119
- Rebuilt for Python 3.7

* Tue May 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.9-0.1.dev1805261119
- 4.19.9.dev1805261119 snapshot
- %build: use --no-dist-info, feature not ready

* Thu Mar 15 2018 Sérgio Basto <sergio@serjux.com> - 4.19.8-3
- Use bcond to handle conditional builds

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.8-2
- BR: gcc-c++, sip-api(12)=12.4

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.8-1
- 4.19.8

* Sat Mar 03 2018 Sérgio Basto <sergio@serjux.com> - 4.19.7-3
- Enable python3 on epel7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.19.7-1
- 4.19.7

* Thu Jan 18 2018 Scott Talbert <swt@techie.net> - 4.19.6-5
- Cherry-pick patch from upstream to fix generator segfault

* Mon Dec 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.6-4
- python2-sip-devel: fix dep on base pkg

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.19.6-3
- Python 2 binary packages renamed to python2-sip and python2-sip-devel
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Mon Dec 11 2017 Merlin Mathesius <mmathesi@redhat.com> - 4.19.6-2
- Cleanup spec file conditionals

* Sat Nov 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.6-1
- sip-4.19.6

* Mon Nov 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.5-1
- sip-4.19.5

* Sat Nov 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.4-1
- sip-4.19.4, sip-api(12)=12.3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.3-2
- python3 sipconfig.py: set proper sip_bin value

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.3-1
- sip-4.19.3, sip-api(12)=12.2

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.2-1
- sip-4.19.2

* Thu Feb 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.19.1-1
- sip-4.19.1, sip-api(12)=12.1 (#1422744)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 31 2016 Rex Dieter <rdieter@math.unl.edu> - 4.19-1
- sip-4.19, sip-api(12)=12.0

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.18.1-2
- Rebuild for Python 3.6

* Tue Jul 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.18.1-1
- sip-4.18.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.18-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.18-2
- backport upstream fix for proper out-of-src-tree builds
- backport upstream fix for Diamond inheritance (#1345953)

* Wed Apr 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.18-1
- sip-4.18, sip-api(11)=11.3

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Rex Dieter <rdieter@fedoraproject.org> 4.17-4
- %%buid: set LFLAGS too

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.17-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Than Ngo <than@redhat.com> - 4.17-2
- rebuild

* Sat Oct 24 2015 Rex Dieter <rdieter@fedoraproject.org> 4.17-1
- sip-4.17, use %%license tag

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 4.16.9-2
- Rebuilt for Python3.5 rebuild

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 4.16.9-1
- sip-4.16.9

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.16.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Rex Dieter <rdieter@fedoraproject.org> 4.16.8-1
- sip-4.16.8, sip-api(11)=11.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.16.7-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.16.7-1
- sip-4.16.7

* Wed Feb 25 2015 Rex Dieter <rdieter@fedoraproject.org> 4.16.6-1
- sip-4.16.6

* Fri Dec 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.5-1
- sip-4.16.5

* Sun Oct 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.4-1
- sip-4.16.4

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.3-1
- sip-4.16.3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.2-1
- sip-4.16.2

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.1-1
- sip-4.16.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16-2
- pull in upstream fix for PyQt-4.11.1 ftbfs

* Wed May 28 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16-1
- sip-4.16, sip-api(11)=11.1

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 4.15.5-2
- rebuild (f21-python)

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.15.5-1
- sip-4.15.5, sip-api(11)=11.0
- -macros: noarch
- s/python/python2/

* Sat Feb 01 2014 Rex Dieter <rdieter@fedoraproject.org> 4.15.4-2
- -macros: use %%_rpmconfigdir/macros.d (where supported)
- .spec cleanup

* Wed Jan 08 2014 Rex Dieter <rdieter@fedoraproject.org> 4.15.4-1
- sip-4.15.4

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 4.15.3-1
- sip-4.15.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.7-1
- sip-4.14.7
- sip-api(10) = 10.0

* Sun Apr 21 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.6-1
- sip-4.14.6

* Tue Mar 26 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.5-1
- sip-4.14.5 (#928340)

* Sun Mar 03 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.4-1
- sip-4.14.4, sip-api 9.2

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-1
- sip-4.14.3

* Sun Dec 09 2012 Rex Dieter <rdieter@fedoraproject.org> 4.14.2-1
- sip-4.14.2

* Sun Oct 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.14.1-1
- sip-4.14.1
- sip-api(9) = 9.1

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.14-1
- sip-4.14
- sip-api(9) = 9.0

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 4.13.3-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 4.13.3-3
- make with_python3 be conditional on fedora

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Rex Dieter <rdieter@fedoraproject.org> 4.13.3-1
- 4.13.3

* Sat Feb 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.13.2-1
- 4.13.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.13.1-1
- 4.13.1

* Wed Oct 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.13-1
- 4.13

* Fri Sep 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.4-3
- License: GPLv2 or GPLv3 and (GPLv3+ with exceptions) (#226419)

* Wed Sep 14 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.4-2
- try not to rpath the world (#737236)

* Wed Aug 10 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.4-1
- 4.12.4

* Wed Jun 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.3-1
- 4.12.3

* Mon May 02 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.2-1
- 4.12.2

* Tue Mar 22 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-5
- Provides: (python3-)sip-api(...)%%{_isa} ...  (ie, make it arch'd)

* Fri Feb 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-4
- no_strip patch, fixes -debuginfo

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-2
- macros.sip: %%_sip_api_minor 1

* Mon Jan 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-1
- sip-4.12.1

* Sat Jan 15 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.12.1-0.1.fa100876a783
- sip-4.12.1 snapshot

* Thu Dec 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.12-2
- rebuild (python3)

* Fri Dec 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.12-1
- sip-4.12

* Mon Nov 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-2
- add missing %%defattr to python3- pkgs (#226419)

* Sat Oct 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-1
- sip-4.11.2

* Wed Sep 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.11.1-1
- sip-4.11.1
- sip-api(8) = 8.0

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 4.10.5-3
- rebuild with python3.2
  https://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 Rex Dieter <rdieter@fedoraproject.org> 4.10.5-1
- sip-4.10.5

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> 4.10.3-1
- sip-4.10.3

* Fri Jun 25 2010 Karsten Hopp <karsten@redhat.com> 4.10.2-3
- bump and rebuild so that s390 will build the python3-sip packages

* Mon Apr 26 2010 David Malcolm <dmalcolm@redhat.com> - 4.10.2-2
- enable "with_python3" in the build
- use py3dir throughout, as provided by python3-devel
- name the python 3 sip binary "python3-sip"
- fix a typo in the name of the data dir: python-3sip -> python3-sip
- split out macros.sip into a new subpackage

* Sat Apr 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- sip-4.10.2

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-2
- _sip_api_minor 1

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- sip-4.10.1

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10-1
- sip-4.10 (final)

* Fri Jan 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10-0.2.20100102
- RFE: Support python3 when building sip (#545124)
- drop old pre v4 changelog

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10-0.1.20100102
- sip-4.10-snapshot-20100102

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- sip-4.9.3

* Fri Nov 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- sip-4.9.2

* Tue Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-3
- move sip binary to -devel 

* Mon Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-2
- Provides: sip-api(%%_sip_api_major) = %%_sip_api
- devel: /etc/rpm/macros.sip helper

* Fri Oct 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-1
- sip-4.9.1

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-0.1.20091014
- sip-4.9.1-snapshot-20091014

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9-1
- sip-4.9
- License: GPLv2 or GPLv3

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.8.2-2
- Convert specfile to UTF-8.

* Tue Jul 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- sip-4.8.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8.1-1
- sip-4.8.1

* Fri Jun 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8-1
- sip-4.8

* Thu May 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8-0.1.20090430
- sip-4.8-snapshot-20090430

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.7.9-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.7.9-1
- sip-4.7.9

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.7.8-1
- sip-4.7.8

* Thu Sep 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.7.7-3
- fix license tag

* Tue Sep 02 2008 Than Ngo <than@redhat.com> 4.7.7-2
- get rid of BR on qt

* Tue Aug 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.7-1
- sip-4.7.7

* Wed May 21 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.6-1
- sip-4.7.6

* Wed May 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.5-1
- sip-4.7.5

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-3
- BR: qt3-devel (f9+)

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-2
- fix 64bit patch

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-1
- sip-4.7.4

* Thu Dec 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.3-1
- sip-4.7.3

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.2-1
- sip-4.7.2
- omit needless scriptlets

* Mon Nov 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.1-2
- License: Python Software Foundation License v2
- fix/cleanup some macro usage
- fix Source, Url. 

* Mon Oct 22 2007 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Mon Oct 01 2007 Than Ngo <than@redhat.com> - 4.6-3
- fix rh#289321, sipconfig.py includes wrong py_lib_dir, thanks to Rex Dieter

* Thu Aug 30 2007 Than Ngo <than@redhat.com> - 4.6-2.fc7
- typo in description

* Thu Apr 12 2007 Than Ngo <than@redhat.com> - 4.6-1.fc7
- 4.6

* Thu Jan 18 2007 Than Ngo <than@redhat.com> - 4.5.2-1
- 4.5.2 

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 4.5-2
- rebuild against python 2.5
- cleanups for python packaging guidelines

* Mon Nov 06 2006 Than Ngo <than@redhat.com> 4.5-1
- 4.5

* Thu Sep 28 2006 Than Ngo <than@redhat.com> 4.4.5-3
- fix #207297, use qt qmake files

* Wed Sep 20 2006 Than Ngo <than@redhat.com> 4.4.5-2
- fix #206633, own %%_datadir/sip

* Wed Jul 19 2006 Than Ngo <than@redhat.com> 4.4.5-1
- update to 4.4.5

* Mon Jul 17 2006 Than Ngo <than@redhat.com> 4.4.3-2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.4.3-1.1
- rebuild

* Thu Apr 27 2006 Than Ngo <than@redhat.com> 4.4.3-1
- update to 4.4.3
- built with %%{optflags}

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.3.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.3.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 12 2005 Than Ngo <than@redhat.com> 4.3.1-1
- update to 4.3.1

* Wed Mar 23 2005 Than Ngo <than@redhat.com> 4.2.1-1
- 4.2.1

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 4.2-1
- 4.2

* Thu Nov 11 2004 Than Ngo <than@redhat.com> 4.1-2
- rebuild against python 2.4

* Fri Sep 24 2004 Than Ngo <than@redhat.com> 4.1-1
- update to 4.1
