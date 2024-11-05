Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%define _enable_gui --enable-gui

Summary: iODBC Driver Manager
Name: libiodbc
Version: 3.52.16
Release: 1%{?dist}
License: LGPLv2 or BSD
URL: http://www.iodbc.org/
Source0: https://github.com/openlink/iODBC/archive/v%{version}/%{name}-%{version}.tar.gz

%{?_enable_gui:BuildRequires: gtk2-devel}
BuildRequires: gcc
BuildRequires: chrpath
# Needed for autogen.sh
BuildRequires: libtool

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
# --disable-libodbc to minimize conflicts with unixODBC
%configure \
  --enable-odbc3 \
  --with-iodbc-inidir=%{_sysconfdir} \
  --enable-pthreads \
  --disable-libodbc \
  --disable-static \
  --includedir=%{_includedir}/libiodbc \
  %{?_enable_gui} %{!?_enable_gui:--disable-gui}

%make_build


%install
%make_install

# nuke rpaths
chrpath --delete %{buildroot}%{_bindir}/iodbctest
chrpath --delete %{buildroot}%{_bindir}/iodbctestw

# unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la
rm -rfv %{buildroot}%{_datadir}/libiodbc/samples


%ldconfig_scriptlets

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
* Mon Nov 04 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 3.52.16-1
- Update to 3.52.16
- License verified.
- Restored gui build

* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.52.13-4
- Updating source URL.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.52.13-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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

