# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global majorver1 8
%global majorver2 6
%global majorver %{majorver1}.%{majorver2}
%global	vers %{majorver}.12

%global pkgname tcl

Name: mingw-%{pkgname}
Version: 8.6.15
Release: 3%{?dist}
Summary: MinGW Windows Tool Command Language, pronounced tickle

License: TCL
URL: http://tcl.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/tcl/%{pkgname}-core%{version}-src.tar.gz
BuildArch: noarch

BuildRequires: make
BuildRequires: autoconf
BuildRequires: file
BuildRequires: m4
BuildRequires: net-tools
BuildRequires: tcl
BuildRequires: mingw32-binutils
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc
BuildRequires: mingw32-zlib

BuildRequires: mingw64-binutils
BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc
BuildRequires: mingw64-zlib

Patch0: tcl-8.6.15-autopath.patch
Patch1: tcl-8.6.15-conf.patch
Patch2: tcl-8.6.13-tcltests-path-fix.patch
Patch3: tcl-8.6.13-configure-c99.patch
Patch4: tcl-mingw.patch
Patch5: tcl-nativetclsh.patch
Patch6: tcl-mingw-w64-compatibility.patch
Patch7: tcl-nativezlib.patch


%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.


%package -n mingw32-%{pkgname}
Summary: MinGW Windows Tool Command Language, pronounced tickle

%description -n mingw32-%{pkgname}
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

%package -n mingw64-%{pkgname}
Summary: MinGW Windows Tool Command Language, pronounced tickle

%description -n mingw64-%{pkgname}
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pkgname}%{version}
chmod -x generic/tclThreadAlloc.c

%build
pushd win
autoconf
%mingw_configure --disable-threads --enable-shared
%mingw_make_build TCL_LIBRARY=%{mingw32_datadir}/%{pkgname}%{majorver}
popd


%install
make install -C win/build_win32 INSTALL_ROOT=%{buildroot} TCL_LIBRARY=%{mingw32_datadir}/%{pkgname}%{majorver}
make install -C win/build_win64 INSTALL_ROOT=%{buildroot} TCL_LIBRARY=%{mingw64_datadir}/%{pkgname}%{majorver}

mv %{buildroot}%{mingw32_bindir}/tclsh%{majorver1}.%{majorver2} %{buildroot}%{mingw32_bindir}/tclsh%{majorver1}%{majorver2}.exe
mv %{buildroot}%{mingw64_bindir}/tclsh%{majorver1}.%{majorver2} %{buildroot}%{mingw64_bindir}/tclsh%{majorver1}%{majorver2}.exe
ln -s tclsh%{majorver1}%{majorver2}.exe %{buildroot}%{mingw32_bindir}/tclsh.exe
ln -s tclsh%{majorver1}%{majorver2}.exe %{buildroot}%{mingw64_bindir}/tclsh.exe

# for linking with -lib%{pkgname}
ln -s lib%{pkgname}%{majorver1}%{majorver2}.dll.a %{buildroot}%{mingw32_libdir}/lib%{pkgname}.dll.a
ln -s lib%{pkgname}%{majorver1}%{majorver2}.dll.a %{buildroot}%{mingw64_libdir}/lib%{pkgname}.dll.a

ln -s ../share/%{pkgname}%{majorver} %{buildroot}/%{mingw32_libdir}/%{pkgname}%{majorver}
ln -s ../share/%{pkgname}%{majorver} %{buildroot}/%{mingw64_libdir}/%{pkgname}%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.5 for now
ln -s %{mingw32_libdir}/%{pkgname}Config.sh %{buildroot}/%{mingw32_libdir}/%{pkgname}%{majorver}/%{pkgname}Config.sh
ln -s %{mingw32_libdir}/%{pkgname}Config.sh %{buildroot}/%{mingw64_libdir}/%{pkgname}%{majorver}/%{pkgname}Config.sh

mkdir -p %{buildroot}/%{mingw32_includedir}/%{pkgname}-private/{generic,win}
mkdir -p %{buildroot}/%{mingw64_includedir}/%{pkgname}-private/{generic,win}
find generic win -name "*.h" -exec cp -p '{}' %{buildroot}/%{mingw32_includedir}/%{pkgname}-private/'{}' ';'
find generic win -name "*.h" -exec cp -p '{}' %{buildroot}/%{mingw64_includedir}/%{pkgname}-private/'{}' ';'
( cd %{buildroot}/%{mingw32_includedir}
	for i in *.h ; do
		[ -f %{buildroot}/%{mingw32_includedir}/%{pkgname}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{mingw32_includedir}/%{pkgname}-private/generic ;
	done
) || true
( cd %{buildroot}/%{mingw64_includedir}
	for i in *.h ; do
		[ -f %{buildroot}/%{mingw64_includedir}/%{pkgname}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{mingw64_includedir}/%{pkgname}-private/generic ;
	done
) || true

# fix executable bits
chmod a-x %{buildroot}/%{mingw32_datadir}/%{pkgname}%{majorver}/encoding/*.enc
chmod a-x %{buildroot}/%{mingw64_datadir}/%{pkgname}%{majorver}/encoding/*.enc
chmod a-x %{buildroot}/%{mingw32_libdir}/*/pkgIndex.tcl
chmod a-x %{buildroot}/%{mingw64_libdir}/*/pkgIndex.tcl

# remove buildroot traces
sed -i -e "s|$PWD/win|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{mingw32_libdir}/%{pkgname}Config.sh
sed -i -e "s|$PWD/win|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{mingw64_libdir}/%{pkgname}Config.sh
rm -rf %{buildroot}/%{mingw32_datadir}/%{pkgname}%{majorver}/tclAppInit.c
rm -rf %{buildroot}/%{mingw64_datadir}/%{pkgname}%{majorver}/tclAppInit.c
rm -rf %{buildroot}/%{mingw32_datadir}/%{pkgname}%{majorver}/ldAix
rm -rf %{buildroot}/%{mingw64_datadir}/%{pkgname}%{majorver}/ldAix

# move windows packages to where tcl85.dll will find them
mv %{buildroot}/%{mingw32_libdir}/dde* %{buildroot}/%{mingw32_libdir}/%{pkgname}%{majorver}/
mv %{buildroot}/%{mingw64_libdir}/dde* %{buildroot}/%{mingw64_libdir}/%{pkgname}%{majorver}/
mv %{buildroot}/%{mingw32_libdir}/reg* %{buildroot}/%{mingw32_libdir}/%{pkgname}%{majorver}/
mv %{buildroot}/%{mingw64_libdir}/reg* %{buildroot}/%{mingw64_libdir}/%{pkgname}%{majorver}/

# remove local zlib
rm -f %{buildroot}/%{mingw32_bindir}/zlib1.dll
rm -f %{buildroot}/%{mingw64_bindir}/zlib1.dll


%files -n mingw32-%{pkgname}
%{mingw32_bindir}/%{pkgname}sh.exe
%{mingw32_bindir}/%{pkgname}sh%{majorver1}%{majorver2}.exe
%{mingw32_bindir}/%{pkgname}%{majorver1}%{majorver2}.dll
%{mingw32_libdir}/lib%{pkgname}%{majorver1}%{majorver2}.dll.a
%{mingw32_libdir}/lib%{pkgname}stub%{majorver1}%{majorver2}.a
%{mingw32_libdir}/lib%{pkgname}.dll.a
%{mingw32_libdir}/%{pkgname}Config.sh
%{mingw32_datadir}/%{pkgname}%{majorver}
%exclude %{mingw32_datadir}/%{pkgname}%{majorver}/dde1.4/tcldde14.dll.debug
%exclude %{mingw32_datadir}/%{pkgname}%{majorver}/reg1.3/tclreg13.dll.debug
%{mingw32_datadir}/%{pkgname}%{majorver1}
%{mingw32_includedir}/*
%{mingw32_libdir}/%{pkgname}%{majorver}
%doc changes
%doc license.terms

%files -n mingw64-%{pkgname}
%{mingw64_bindir}/%{pkgname}sh.exe
%{mingw64_bindir}/%{pkgname}sh%{majorver1}%{majorver2}.exe
%{mingw64_bindir}/%{pkgname}%{majorver1}%{majorver2}.dll
%{mingw64_libdir}/lib%{pkgname}%{majorver1}%{majorver2}.dll.a
%{mingw64_libdir}/lib%{pkgname}stub%{majorver1}%{majorver2}.a
%{mingw64_libdir}/lib%{pkgname}.dll.a
%{mingw64_libdir}/%{pkgname}Config.sh
%{mingw64_datadir}/%{pkgname}%{majorver}
%exclude %{mingw64_datadir}/%{pkgname}%{majorver}/dde1.4/tcldde14.dll.debug
%exclude %{mingw64_datadir}/%{pkgname}%{majorver}/reg1.3/tclreg13.dll.debug
%{mingw64_datadir}/%{pkgname}%{majorver1}
%{mingw64_includedir}/*
%{mingw64_libdir}/%{pkgname}%{majorver}
%doc changes
%doc license.terms


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 18 2024 Sandro Mani <manisandro@gmail.com> - 8.6.15-1
- Update to 8.6.15

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 04 2024 Sandro Mani <manisandro@gmail.com> - 8.6.14-1
- Update to 8.6.14

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 31 2023 Sandro Mani <manisandro@gmail.com> - 8.6.13-1
- Update to 8.6.13

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 8.6.12-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Sandro Mani <manisandro@gmail.com> - 8.6.12-1
- Update to 8.6.12

* Fri Jul 30 2021 Sandro Mani <manisandro@gmail.com> - 8.6.10-1
- Update to 8.6.10

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.8-1
- update to 8.6.8

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 10 2017 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.7-1
- update to 8.6.7

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 08 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.6-1
- update to 8.6.6

* Fri Jul 01 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.5-1
- update to 8.6.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May  4 2015 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.4-1
- update to 8.6.4

* Thu Dec  4 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.3-1
- update to 8.6.3

* Wed Oct  1 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.2-1
- update to 8.6.2

* Fri Jun 13 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.6.1-1
- update to 8.6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar  6 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.15-1
- update to 8.5.15

* Tue Sep 17 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.14-2
- rename EXCEPTION_REGISTRATION to avoid define clash with new mingw headers

* Tue Sep  3 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.14-1
- update to 8.5.14

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.5.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 8.5.13-3
- %%{mingw32_libdir}/tcl8.5 and %%{mingw64_libdir}/tcl8.5 are symlinks, not folders
- Fixes FTBFS against latest RPM

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec  4 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.13-1
- update to 8.5.13

* Fri Aug  3 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.11-6
- enable 64bit compile

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.5.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 8.5.11-4
- Prevent a file conflict with files from the debuginfo package

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 8.5.11-3
- Renamed the source package to mingw-tcl (#801032)
- Modernize the spec file
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 8.5.11-2
- Rebuild against the mingw-w64 toolchain
- Added a patch to fix compatibility with the mingw-w64 toolcain

* Mon Jan 16 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.11-1
- update 8.5.11

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 10 2011 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.9-4
- put the reg and dde libraries where tcl85.dll searches for it
 
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.9-2
- put the tcl library where tclsh.exe searches for it

* Mon Dec  6 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.9-1
- update to 8.5.9

* Thu Aug  5 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.8-1
- update to 8.5.8

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.5.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.7-6
- add debuginfo packages

* Sat May 23 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.7-5
- rebuilt

* Sat May 23 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.7-4
- use native shell to install tz data

* Sat May 23 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.7-3
- fix BRs

* Fri May 22 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.7-2
- remove check section

* Thu May 21 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.7-1
- update to 8.5.7
- simplify dir ownership

* Thu May 21 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 8.5.6-1
- copy from native
