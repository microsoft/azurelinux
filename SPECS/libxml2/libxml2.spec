%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Libxml2
Name:           libxml2
Version:        2.9.14
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/General Libraries
URL:            https://www.xmlsoft.org/
Source0:        https://gitlab.gnome.org/GNOME/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.gz
Patch0:         CVE-2022-2309.patch
Patch1:         CVE-2022-40303.patch
Patch2:         CVE-2022-40304.patch
BuildRequires:  python-xml
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python3-devel
Provides:       pkgconfig(libxml-2.0)

%description
The libxml2 package contains libraries and utilities used for parsing XML files.

%package python
Summary:        The libxml2 python module
Group:          Development/Languages/Python
Requires:       %{name} = %{version}
Requires:       python2
Requires:       python2-libs

%description    python
The libxml2 python module

%package -n     python3-libxml2
Summary:        Python 3 bindings for libxml2.
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       python3

%description -n python3-libxml2
Python3 libxml2.

%package devel
Summary:        Libraries and header files for libxml
Requires:       %{name} = %{version}

%description devel
Static libraries and header files for the support library for libxml

%prep
%autosetup -n %{name}-v%{version}

%build
./autogen.sh

%configure \
    --disable-static \
    --with-history
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
%{_fixperms} %{buildroot}/*

make clean
%configure \
    --disable-static \
    --with-python=%{_bindir}/python3
make %{?_smp_mflags}
make install DESTDIR=%{buildroot}

%check
make PYTHON_SUBDIR="" runtests

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license COPYING
%{_docdir}/*
%{_libdir}/libxml*
%{_libdir}/xml2Conf.sh
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc/*
%{_mandir}/man1/*

%files python
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-libxml2
%defattr(-,root,root)
%{python3_sitelib}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake

%changelog
* Wed Nov 30 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.9.14-3
- Fix CVE-2022-40303

* Wed Aug 24 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.9.14-2
- Fix CVE-2022-2309.

* Mon Jun 13 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.9.14-1
- Updating to version 2.9.14 to fix CVE-2022-29824.

* Wed Mar 09 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.13-1
- Updating to version 2.9.13 to fix CVE-2022-23308.

* Thu May 27 2021 Mateusz Malisz <mamalisz@microsoft.com> - 2.9.12-1
- Update to version 2.9.12 to fix CVE-2021-3517, CVE-2021-3518 and CVE-2021-3537

* Wed Mar 03 2021 Andrew Phelps <anphel@microsoft.com> - 2.9.10-4
- Skip python tests which are known to be broken.

* Mon Oct 26 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.9.10-3
- Patch CVE-2020-24977.

* Wed Sep 09 2020 Thomas Crain <thcrain@microsoft.com> - 2.9.10-2
- Patch CVE-2019-20388 and CVE-2020-7595.

* Wed Jun 03 2020 Joe Schmitt <joschmit@microsoft.com> - 2.9.10-1
- Update to version 2.9.10 to resolve CVE-2018-14404, CVE-2018-14567 and CVE-2019-19956.
- Remove Fix_nullptr_deref_with_XPath_logic_ops.patch after version update.
- License verified.
- Remove SHA1 macro.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.9.8-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.9.8-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Dec 07 2018 Dweep Advani <dadvani@vmware.com> - 2.9.8-2
- Fix CVE-2018-14404 and improve build and install sections

* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> - 2.9.8-1
- Update to version 2.9.8

* Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.9.7-1
- Update to version 2.9.7

* Wed Oct 18 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.9.6-1
- Update to version 2.9.6

* Mon Oct 2 2017 Anish Swaminathan <anishs@vmware.com> - 2.9.4-12
- Remove call to _PyVerify_fd

* Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.9.4-11
- Apply patch for CVE-2017-8872

* Mon Aug 07 2017 Danut Moraru <dmoraru@vmware.com> - 2.9.4-10
- Change expected parsing error for test for upstream bug 781205 introduced by CVE-2017-9049

* Mon Jul 10 2017 Divya Thaluru <dthaluru@vmware.com> - 2.9.4-9
- Apply patch for CVE-2017-9047, CVE-2017-9048, CVE-2017-9049 and CVE-2017-9050

* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.9.4-8
- Move python2 requires to python subpackage.

* Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> - 2.9.4-7
- Modified python3 version in configure

* Thu Apr 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.9.4-6
- Added python3-libxml2 package.

* Tue Jan 3 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.9.4-5
- Fix for CVE-2016-9318

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.9.4-4
- Moved man3 to devel subpackage.

* Thu Oct 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.9.4-3
- Apply patch for CVE-2016-5131

* Mon Oct 03 2016 Chang Lee <changlee@vmware.com> - 2.9.4-2
- Modified check

* Wed Jun 01 2016 Anish Swaminathan <anishs@vmware.com> - 2.9.4-1
- Upgrade to 2.9.4

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.9.3-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.9.3-1
- Upgraded to version 2.9.3

* Thu Jan 28 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.9.2-1
- Downgrade to version 2.9.2
- libxml 2.9.3 has been found to have major functional issues.
- Until these are resolved, please roadmap updating to 2.9.2.

* Wed Dec 2 2015 Xiaolin Li <xiaolinl@vmware.com> - 2.9.3-1
- Update to version 2.9.3

* Thu Jul 2 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> - 2.9.1-3
- Seperate the python module from the main library

* Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> - 2.9.1-2
- Moved 'Provides: pkgconfig(...)' into base package

* Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> - 2.9.1-1
- Initial build.  First version
