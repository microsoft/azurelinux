%global tarver 2.1-3

Name:           CUnit
Version:        2.1.3
Release:        23%{?dist}
Summary:        Unit testing framework for C
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        LGPLv2+
URL:            http://cunit.sourceforge.net/
#Source0:       https://downloads.sourceforge.net/cunit/%{name}-%{tarver}.tar.bz2
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  automake
BuildRequires:  libtool

%description 
CUnit is a lightweight system for writing, administering,
and running unit tests in C.  It provides C programmers a basic
testing functionality with a flexible variety of user interfaces.

%package devel
Summary:        Header files and libraries for CUnit development
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel 
The %{name}-devel package contains the header files
and libraries for use with CUnit package.

%prep
%setup -q -n %{name}-%{tarver}
find -name *.c -exec chmod -x {} \;

%build
autoreconf -f -i
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f `find %{buildroot} -name *.la`

# work around bad docdir= in doc/Makefile*
mkdir -p %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_prefix}/doc/%{name} %{buildroot}%{_docdir}/%{name}/html

# add some doc files into the buildroot manually (#1001276)
for f in AUTHORS ChangeLog COPYING NEWS README TODO VERSION ; do
    install -p -m0644 -D $f %{buildroot}%{_docdir}/%{name}/${f}
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license %{_defaultdocdir}/%{name}/COPYING
%{_datadir}/%{name}/
%{_libdir}/libcunit.so.*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README
%{_docdir}/%{name}/TODO
%{_docdir}/%{name}/VERSION

%files devel
%{_docdir}/%{name}/html/
%{_includedir}/%{name}/
%{_libdir}/libcunit.so
%{_libdir}/pkgconfig/cunit.pc
%{_mandir}/man3/CUnit.3*

%changelog
* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 2.1.3-23
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun  1 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1.3-9
- Fix HTML documentation installation location.
- Replace CUnit-2.1-3-src.tar.bz2 tarball, which really
  is 2.1-2 in disguise according to configure.in, with 2.1-3 as
  published on 2014-04-24.
- BR libtool
- Run autoreconf instead of autoconf.
- Drop --enable-curses because without BuildRequires ncurses-devel it
  would disable itself automatically (and if it were enabled, test programs
  would need to link with ncurses explicitly).

* Sun Sep 29 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1.3-8
- Add %%_isa to -devel base package dependency.
- Headers get installed by "make install", copying them from the HTML
  doc headers dir is not necessary.
- Configure build with --disable-static.
- Drop unneeded spec stuff (buildroot def, removal, clean, pkgconfig dep).
- Using %%defattr is not needed anymore.
- Deduplicate documentation files in unversioned docdir (#1001276).

* Tue Sep 10 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject.org> - 2.1.3-7
- Fix build with unversioned docdir (#1001276)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject.org> - 2.1.3-5
- Use header files from doc folder as well
- Enable curses

* Sat Apr 20 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject.org> - 2.1.3-4
- Use autoconf for ARM

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 2 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1.3-1
- Updated to 2.1.3 sources re-run with autoreconf.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1.2-6
- Changed Group to System Environment/Libraries.
- Remove executable permission from C files.
- Created two separate patches for Makefile and manpage fixes.
- Removed passing datarootdir from configure.

* Thu Jan 20 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1.2-5
- Renamed Source0 to use Fedora sourceforge.net naming guidelines.
- Removed exit call in library patch.
- Use A.B.C version number.

* Thu Jan 20 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-4
- Updated to license LGPLv2+.
- Changed to use BuildRoot.
- Added comments for inclusion of patches.
- Removed inconsistent macro usage.
- Moved man page, HTML documentation to devel package.
- Added AUTHORS, COPYING, README, TODO to doc in base package.
- Used * in man, library inclusion.

* Sun Dec 26 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-3
- Created patch to fix man page warnings and datarootdir settings.
- Added patch to remove exit calls in library.

* Wed Dec 15 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-2
- Moved libcunit.so.* to main package.
- Added post, postun ldconfig.
- Added smp flags for make build.
- Changed datarootdir to datadir.

* Tue Dec 14 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-1
- First CUnit package.
