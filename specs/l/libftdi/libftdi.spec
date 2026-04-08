# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		libftdi
Version:	1.5
Release:	21%{?dist}
Summary:	Library to program and control the FTDI USB controller

# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:	LicenseRef-Callaway-LGPLv2
URL:		https://www.intra2net.com/en/developer/libftdi/
Source0:	https://www.intra2net.com/en/developer/%{name}/download/%{name}1-%{version}.tar.bz2

# http://developer.intra2net.com/git/?p=libftdi;a=commitdiff;h=cdb28383402d248dbc6062f4391b038375c52385;hp=5c2c58e03ea999534e8cb64906c8ae8b15536c30
Patch0:		libftdi-1.5-fix_pkgconfig_path.patch
# http://developer.intra2net.com/mailarchive/html/libftdi/2023/msg00003.html
Patch1:		libftdi-1.5-no-distutils.patch
# http://developer.intra2net.com/mailarchive/html/libftdi/2023/msg00005.html
Patch2:		libftdi-1.5-cmake-deps.patch
# Fix for SWIG 4.3.0
# https://bugzilla.redhat.com/show_bug.cgi?id=2319133
# http://developer.intra2net.com/mailarchive/html/libftdi/2024/msg00024.html
Patch3:		libftdi-1.5-swig-4.3.patch

BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	libconfuse-devel
BuildRequires:	libusbx-devel
BuildRequires:	make
BuildRequires:	python3-devel
BuildRequires:	swig
BuildRequires:	systemd
Requires:	systemd


%description
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%package devel
Summary:	Header files and static libraries for libftdi
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-%{name}%{?_isa} = %{version}-%{release}
Requires:	cmake-filesystem

%description devel
Header files and static libraries for libftdi


%package -n python3-libftdi
%{?python_provide:%python_provide python3-libftdi}
Summary:	Libftdi library Python 3 binding
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python3-libftdi
Libftdi Python 3 Language bindings.


%package c++
Summary:	Libftdi library C++ binding
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description c++
Libftdi library C++ language binding.


%package c++-devel
Summary:	Libftdi library C++ binding development headers and libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-c++ = %{version}-%{release}

%description c++-devel
Libftdi library C++ binding development headers and libraries
for building C++ applications with libftdi.


%prep
%autosetup -p1 -n %{name}1-%{version}

# switch to uaccess control
sed -i -e 's/GROUP="plugdev"/TAG+="uaccess"/g' packages/99-libftdi.rules


%build
%cmake -DSTATICLIBS=off -DFTDIPP=on -DPYTHON_BINDINGS=on -DDOCUMENTATION=on -DEXAMPLES=off
%cmake_build

%install
%cmake_install

install -D -pm 0644 packages/99-libftdi.rules %{buildroot}%{_udevrulesdir}/69-libftdi.rules

rm -f %{buildroot}%{_datadir}/doc/libftdi1/example.conf
rm -f %{buildroot}%{_datadir}/doc/libftdipp1/example.conf


%check
#make check


%files
%license COPYING.LIB
%{_libdir}/libftdi1.so.2*
%{_udevrulesdir}/69-libftdi.rules

%files devel
%doc AUTHORS ChangeLog
%doc %{_datadir}/libftdi/examples
%dir %{_includedir}/libftdi1
%{_bindir}/ftdi_eeprom
%{_bindir}/libftdi1-config
%{_includedir}/libftdi1/*.h
%{_libdir}/libftdi1.so
%{_libdir}/pkgconfig/libftdi1.pc
%{_libdir}/cmake/libftdi1/

%files -n python3-libftdi
%{python3_sitearch}/*

%files c++
%{_libdir}/libftdipp1.so.2*
%{_libdir}/libftdipp1.so.3

%files c++-devel
%{_libdir}/libftdipp1.so
%{_includedir}/libftdi1/*.hpp
%{_libdir}/pkgconfig/libftdipp1.pc


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.5-21
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.5-20
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.5-18
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 16 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-16
- Fix for SWIG 4.3.0 (rhbz#2319133)

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.5-15
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.5-13
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.5-9
- Rebuilt for Python 3.12

* Tue Jun 06 2023 Dan Horák <dan[at]danny.cz> - 1.5-8
- Fix parallel build

* Fri Feb 03 2023 Dan Horák <dan[at]danny.cz> - 1.5-7
- Prepare for distutils removal (rhbz#2154854)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.5-4
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 17 2021 Björn Esser <besser82@fedoraproject.org> - 1.5-2
- Add patch to fix includedir in pkgconfig file

* Sun Aug 15 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5-1
- Update to 1.5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4-9
- Rebuilt for Python 3.10

* Tue May 04 2021 Richard Hughes <rhughes@redhat.com> - 1.4-8
- Install the udev file to a non-deprecated location

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 01 2020 Kamil Dudka <kdudka@redhat.com> - 1.4-6
- make the package build with updated %%cmake macro (#1863999)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Dan Horák <dan[at]danny.cz> - 1.4-1
- Update to 1.4

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3-18
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Richard Shaw <hobbes1069@gmail.com> - 1.3-16
- Rebuild to drop python2 subpackage per RHBZ#1634583.

* Sun Feb 17 2019 Richard Shaw <hobbes1069@gmail.com> - 1.3-1
- Add patch to deal with change in CMake/SWIG behavior.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3-12
- Rebuilt for Python 3.7
- Temporarily disable doxygen docs to workaround FTBFS

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 09 2017 Troy Curtis, Jr <troycurtisjr@gmail.com> - 1.3-10
- Add python3 subpackage.
- Drop patch0 in favor of built-in cmake config methods.
- Don't include bytecompiled files for the example python scripts.

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3-9
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3-8
- Python 2 binary package renamed to python2-libftdi
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 1.3-6
- Rebuilt for Boost 1.64

* Thu May 25 2017 Gwyn Ciesla <limburgher@gmail.com> 1.3-5
- libconfuse rebuild.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1.3-3
- Rebuilt for Boost 1.63

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 14 2016 Jon Ciesla <limburgher@gmail.com> 1.3-1
- 1.3, libconfuse rebuild.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 1.2-7
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.2-6
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.2-4
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Sun Feb  8 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-1
- Update to 1.2
- Use %%license

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.1-5
- Rebuild for boost 1.57.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.1-2
- Rebuild for boost 1.55.0

* Mon Mar 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-1
- Update to 1.1
- Build against libusb1
- Package cleanup
- Run make check

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.20-4
- Rebuild for boost 1.54.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 04 2012 Lucian Langa <cooly@gnome.eu.org> - 0.20-1
- new upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Lucian Langa <cooly@gnome.eu.org> - 0.19-2
- fix bug #678781 - too generic name in man file

* Sat Jun 18 2011 Lucian Langa <cooly@gnome.eu.org> - 0.19-1
- new upstream release

* Tue May 24 2011 Lucian Langa <cooly@gnome.eu.org> - 0.19-1
- new upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Dan Horák <dan[at]danny.cz> - 0.18-4
- fix build with libusb >= 1:0.1.3 (wrapper around libusb1)

* Sun Aug  1 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 01 2010 Lucian Langa <cooly@gnome.eu.org> - 0.18-1
- drop patch0 - fixed upstream
- new upstream release

* Wed Jun 09 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-5
- readd mistakenly dropped parch (fixes multilib issues)

* Wed May 05 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-4
- fix typo in group handling (#581151)

* Thu Mar 11 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-3
- fix incorrect UDEV rule (#563566)

* Sat Jan 16 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-2
- do not package static libfiles (#556068)

* Sun Jan  3 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-1
- add patch to fix typo in python bindings
- drop multilib patch0 fixed upstream
- new upstream release

* Sat Aug 22 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-7
- add group for udev rule (#517773)

* Fri Jul 31 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-6
- rebuilt with modified patch

* Fri Jul 31 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-5
- fix multilib conflict in libftdi-config (#508498)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-3
- added udev rules
- addedd c++, python bindings

* Tue Jun 30 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-2
- fix doxygen conflict (#508498)

* Fri May 08 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-1
- new upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Lucian Langa <cooly@gnome.eu.org> - 0.15-3
- fix tag

* Sun Feb 15 2009 Lucian Langa <cooly@gnome.eu.org> - 0.15-2
- add new BR boost-devel

* Sun Feb 15 2009 Lucian Langa <cooly@gnome.eu.org> - 0.15-1
- fix for bug #485600: pick libusb-devel for -devel subpackage
- new upstream release

* Fri Sep 26 2008 Lucian Langa <cooly@gnome.eu.org> - 0.14-2
- require pkgconfig for devel

* Tue Sep 23 2008 Lucian Langa <cooly@gnome.eu.org> - 0.14-1
- new upstream

* Wed Sep 03 2008 Lucian Langa <cooly@gnome.eu.org> - 0.13-1
- initial specfile
