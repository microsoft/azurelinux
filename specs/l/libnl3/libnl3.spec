# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: libnl3
Version: 3.12.0
Release: 3%{?dist}
Summary: Convenience library for kernel netlink sockets
License: LGPL-2.1-only
URL: http://www.infradead.org/~tgr/libnl/

%global version_path libnl%(echo %{version} | tr . _)

%if 0%{?rhel} > 8 || 0%{?fedora} > 43
# Disable python3 build by default
%bcond_with python3
%else
%bcond_without python3
%endif

Source0: https://github.com/thom311/libnl/releases/download/%{version_path}/libnl-%{version}.tar.gz
Source1: https://github.com/thom311/libnl/releases/download/%{version_path}/libnl-doc-%{version}.tar.gz

#Patch1: some.patch


BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: flex
BuildRequires: libtool
BuildRequires: swig


%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation


%package devel
Summary: Libraries and headers for using libnl3
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}
Requires: kernel-headers

%description devel
This package contains various headers for using libnl3


%package cli
Summary: Command line interface utils for libnl3
Requires: %{name} = %{version}-%{release}

%description cli
This package contains various libnl3 utils and additional
libraries on which they depend


%package doc
Summary: API documentation for libnl3
Requires: %{name} = %{version}-%{release}

%description doc
This package contains libnl3 API documentation


%if %{with python3}
%package -n python3-libnl3
Summary: libnl3 binding for Python 3
%{?python_provide:%python_provide python3-libnl3}
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: make
Requires: %{name} = %{version}-%{release}

%description -n python3-libnl3
Python 3 bindings for libnl3
%endif

%prep
%autosetup -p1 -n libnl-%{version}

tar -xzf %SOURCE1

%build
autoreconf -vif
%configure
make %{?_smp_mflags}

%if %{with python3}
pushd ./python/
# build twice, otherwise capi.py is not copied to the build directory.
CFLAGS="$RPM_OPT_FLAGS" %pyproject_wheel
CFLAGS="$RPM_OPT_FLAGS" %pyproject_wheel
popd
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name \*.la -delete

%if %{with python3}
pushd ./python/
%pyproject_install
popd
%endif

%check
make check

%if %{with python3}
pushd ./python/
%{__python3} setup.py check
popd
%endif

%ldconfig_scriptlets
%ldconfig_scriptlets cli

%files
%license COPYING
%exclude %{_libdir}/libnl-cli*.so.*
%exclude %{_libdir}/libnl*-3.a
%{_libdir}/libnl-*.so.*
%config(noreplace) %{_sysconfdir}/*

%files devel
%license COPYING
%{_includedir}/libnl3/netlink/
%dir %{_includedir}/libnl3/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files cli
%license COPYING
%{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl/
%{_bindir}/*
%{_mandir}/man8/*

%files doc
%license COPYING
%doc libnl-doc-%{version}/*.html
%doc libnl-doc-%{version}/*.css
%doc libnl-doc-%{version}/stylesheets/*
%doc libnl-doc-%{version}/images/*
%doc libnl-doc-%{version}/images/icons/*
%doc libnl-doc-%{version}/images/icons/callouts/*
%doc libnl-doc-%{version}/api/*

%if %{with python3}
%files -n python3-libnl3
%{python3_sitearch}/netlink
%{python3_sitearch}/netlink-*.dist-info
%endif

%changelog
* Thu Dec 4 2025 Thomas Haller <thom311@gmail.com> - 3.12.0-2
- Fix build issue for Python

* Thu Dec 4 2025 Thomas Haller <thom311@gmail.com> - 3.12.0-1
- Update to 3.12.0 release
- Disable python subpackages for Fedora 44+

* Wed Aug  6 2025 Thomas Haller <thaller@redhat.com> - 3.11.0-6
- Update python macros in spec file (rh#2377311)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.11.0-4
- Rebuilt for Python 3.14

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 30 2024 Thomas Haller <thaller@redhat.com> - 3.11.0-1
- Update to 3.11.0 release

* Fri Jul 19 2024 Thomas Haller <thaller@redhat.com> - 3.10.0-1
- Update to 3.10.0 release

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.9.0-4
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec  4 2023 Thomas Haller <thaller@redhat.com> - 3.9.0-1
- Update to 3.9.0 release

* Mon Oct 30 2023 Thomas Haller <thaller@redhat.com> - 3.8.0-2
- Use SPDX license identifier in package

* Tue Aug 29 2023 Thomas Haller <thaller@redhat.com> - 3.8.0-1
- Update to 3.8.0 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.7.0-4
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul  6 2022 Thomas Haller <thaller@redhat.com> - 3.7.0-1
- Update to 3.7.0 release

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.6.0-4
- Rebuilt for Python 3.11

* Fri May 6 2022 Till Maas <opensource@till.name> - 3.6.0-3
- Fix URLs (rh #1541407)
- Cleanup specfile

* Fri May  6 2022 Thomas Haller <thaller@redhat.com> - 3.6.0-2
- route: fix crash parsing multihop route (rh #2081279)

* Fri Apr 15 2022 Thomas Haller <thaller@redhat.com> - 3.6.0-1
- Update to 3.6.0 release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.5.0-7
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep  1 2019 Thomas Haller <thaller@redhat.com> - 3.5.0-1
- Update to 3.5.0 release

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4.0-10
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4.0-7
- Subpackage python2-libnl3 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.4.0-5
- Rebuilt for Python 3.7

* Fri Mar 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 3.4.0-4
- Conditionalize the Python 2 subpackage

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.4.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Oct  9 2017 Thomas Haller <thaller@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Wed Sep 20 2017 Thomas Haller <thaller@redhat.com> - 3.4.0-0.1
- Update to 3.4.0-rc1

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.3.0-4
- Python 2 binary package renamed to python2-libnl3
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May  3 2017 Thomas Haller <thaller@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Mon Mar  6 2017 Thomas Haller <thaller@redhat.com> - 3.3.0-0.1
- Update to 3.3.0-rc1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Thomas Haller <thaller@redhat.com> - 3.2.29-2
- Update with patches from upstream
- check valid input arguments for nla_reserve() (rh#1414305, CVE-2017-0386)
- fix crash during SRIOV parsing
- lazyly read psched settings
- use O_CLOEXEC when creating file descriptors with fopen()

* Fri Dec 30 2016 Thomas Haller <thaller@redhat.com> - 3.2.29-1
- Update to 3.2.29

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2.29-0.3
- Rebuild for Python 3.6

* Fri Dec 16 2016 Thomas Haller <thaller@redhat.com> - 3.2.29-0.2
- macsec: fix endianness for MACSec's 'sci' parameter

* Mon Dec 12 2016 Thomas Haller <thaller@redhat.com> - 3.2.29-0.1
- Update to 3.2.29-rc1

* Fri Aug 26 2016 Thomas Haller <thaller@redhat.com> - 3.2.28-3
- route: fix nl_object_identical() comparing AF_INET addresses (rh #1370526)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.28-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Jul  9 2016 Thomas Haller <thaller@redhat.com> - 3.2.28-1
- Update to 3.2.28

* Thu Jun 30 2016 Thomas Haller <thaller@redhat.com> - 3.2.28-0.1
- Update to 3.2.28-rc1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 16 2015 Thomas Haller <thaller@redhat.com> - 3.2.27-1
- Update to 3.2.27

* Mon Sep 21 2015 Thomas Haller <thaller@redhat.com> - 3.2.27-0.1
- Update to 3.2.27-rc1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-4
- Update to 3.2.26
- cli package brings more commands and installs them to /bin

* Mon Mar  9 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-3
- Update to 3.2.26-rc1
- fix broken symbols from 3.2.26-1
- backport upstream fix for nl_socket_set_fd()

* Sat Mar  7 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-2
- Revert update to 3.2.26-rc1 to previous 3.2.25-6

* Fri Mar  6 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-1
- Update to 3.2.26-rc1

* Tue Feb  3 2015 Thomas Haller <thaller@redhat.com> - 3.2.25-6
- add new packages with language bindings for Python 2 and Python 3 (rh #1167112)

* Tue Dec  9 2014 Thomas Haller <thaller@redhat.com> - 3.2.25-5
- Add support for IPv6 link local address generation

* Fri Oct 10 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.2.25-4
- Add support for IPv6 tokenized interface identifiers

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Thomas Haller <thaller@redhat.com> 3.2.25-2
- Update to 3.2.25

* Fri Jul  4 2014 Thomas Haller <thaller@redhat.com> 3.2.25-1
- Update to 3.2.25-rc1

* Sun Jun  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.2.24-5
- Run autoreconf for new automake, cleanup spec

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Thomas Haller <thaller@redhat.com> - 3.2.24-3
- add nl_has_capability() function
- retry local port on ADDRINUSE (rh #1097175)
- python: fix passing wrong argument in netlink/core.py
- fix return value of nl_rtgen_request()
- fix nl_msec2str()
- fix crash in rtnl_act_msg_parse()
- fix rtnl_route_build_msg() not to guess the route scope if RT_SCOPE_NOWHERE

* Fri Apr  4 2014 Thomas Haller <thaller@redhat.com> - 3.2.24-2
- fix breaking on older kernels due to IFA_FLAGS attribute (rh #1063885)

* Thu Jan 23 2014 Thomas Haller <thaller@redhat.com> - 3.2.24-1
- Update to 3.2.24 (rhbz#963111)

* Mon Sep 23 2013 Paul Wouters <pwouters@redhat.com> - 3.2.22-2
- Update to 3.2.22 (rhbz#963111)
- Add patch for double tree crasher in rtnl_link_set_address_family()

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jan 25 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.21-1
- Update to 3.2.21

* Wed Jan 23 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.20-1
- Update to 3.2.20

* Sun Jan 20 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-2
- Age fix

* Thu Jan 17 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-1
- Update to 3.2.19

* Tue Oct 30 2012 Dan Williams <dcbw@redhat.com> - 3.2.14-1
- Update to 3.2.14

* Mon Sep 17 2012 Dan Williams <dcbw@redhat.com> - 3.2.13-1
- Update to 3.2.13

* Fri Feb 10 2012 Dan Williams <dcbw@redhat.com> - 3.2.7-1
- Update to 3.2.7

* Tue Jan 17 2012 Jiri Pirko <jpirko@redhat.com> - 3.2.6-1
- Initial build
