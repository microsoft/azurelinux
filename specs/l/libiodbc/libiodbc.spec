# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global giturl https://github.com/openlink/iODBC

## admin gui build currently busted, FIXME?
#define _enable_gui --enable-gui

Summary: iODBC Driver Manager
Name: libiodbc
Version: 3.52.16
Release: 4%{?dist}
License: LGPL-2.0-only OR BSD-3-Clause
URL: http://www.iodbc.org/
VCS: git:%{giturl}.git
Source0: %{giturl}/archive/v%{version}/%{name}-%{version}.tar.gz

## upstream patches

## downstream patches
Patch100: libiodbc-3.52.12-multilib.patch
# Fix LTO type mismatches
# https://github.com/openlink/iODBC/issues/107
# https://github.com/openlink/iODBC/issues/108
Patch101: libiodbc-3.52.16-lto.patch
# Fix FTBFS due to a type mismatch in unicode.c
Patch102: libiodbc-3.52.16-unicode.patch

%{?_enable_gui:BuildRequires: gtk2-devel}
BuildRequires: gcc
# Needed for autogen.sh
BuildRequires: libtool
BuildRequires: make

%description
The iODBC Driver Manager is a free implementation of the SAG CLI and
ODBC compliant driver manager which allows developers to write ODBC
compliant applications that can connect to various databases using
appropriate backend drivers.

%package devel
Summary: Header files and libraries for iODBC development
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains the header files and libraries needed to develop
programs that use the driver manager.

%package admin
Summary: Gui administrator for iODBC development
Requires: %{name}%{?_isa} = %{version}-%{release}
%description admin
This package contains a Gui administrator program for maintaining
DSN information in odbc.ini and odbcinst.ini files.


%prep
%autosetup -p1 -n iODBC-%{version}

# fix header permissions
chmod -x include/*.h


%build
# github tarball does not ship configure
./autogen.sh
# The code is not ready for C23 mode
export CFLAGS='%{build_cflags} -std=gnu17'
# --disable-libodbc to minimize conflicts with unixODBC
%configure \
  --enable-odbc3 \
  --with-iodbc-inidir=%{_sysconfdir} \
  --with-layout=RedHat \
  --enable-pthreads \
  --disable-libodbc \
  --disable-static \
  --includedir=%{_includedir}/libiodbc \
  %{?_enable_gui} %{!?_enable_gui:--disable-gui}

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(.*g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build


%install
%make_install

# unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la
rm -rfv %{buildroot}%{_datadir}/libiodbc/samples


%files 
%doc AUTHORS ChangeLog README
%doc etc/odbc*.ini.sample
%license LICENSE*
%{_bindir}/iodbctest
%{_bindir}/iodbctestw
%{_libdir}/libiodbc.so.2*
%{_libdir}/libiodbcinst.so.2*
%{_mandir}/man1/iodbctest.1*
%{_mandir}/man1/iodbctestw.1*

%files devel
%{_bindir}/iodbc-config
%{_includedir}/libiodbc/
%{_libdir}/libiodbc.so
%{_libdir}/libiodbcinst.so
%{_mandir}/man1/iodbc-config.1*
%{_libdir}/pkgconfig/libiodbc.pc

%if 0%{?_enable_gui:1}
%files admin
%{_bindir}/iodbcadm-gtk
%{_libdir}/libdrvproxy.so*
%{_libdir}/libiodbcadm.so*
%{_mandir}/man1/iodbcadm-gtk.1*
%endif


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Jerry James <loganjerry@gmail.com> - 3.52.16-1
- Version 3.52.16
- Reevaluate License field
- Add patch to fix LTO type mismatches
- Add patch to fix FTBFS due to a type mismatch in unicode.c
- Build in C17 mode; the code is not ready for C23
- Avoid rpaths instead of removing them afterwards
- Minor spec file cleanups

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 3.52.15-8
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Rex Dieter <rdieter@fedoraproject.org> - 3.52.15-1
- 3.52.15

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 3.52.13-3
- Ignore annobin symbols in configure test

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep  7 2019 Orion Poplawski <orion@nwra.com> - 3.52.13-1
- Update to 3.52.13

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 3.52.12-7
- use %%make_build %%autosetup %%make_install %%ldconfig_scriptlets
- pull in some upstream fixes

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 3.52.12-1
- 3.52.12 (#1100433), .spec cosmetics, update URL/Source

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.52.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 20 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.7-1
- libiodbc-3.52.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 06 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-4
- -devel: install headers to /usr/include/libiodbc/ to better avoid
  conflicts and need for bogus unixODBC-devel dep

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-3
- capitalize Name,Summary,Version tags
- -devel: capitalize Summary
- fix spurious permissions on header files
- refresh upstream source
- -admin,-devel: add %%defattr(...)

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-2
- iodbc-config multilib patch

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-1
- first try, based on upstream src.rpm

