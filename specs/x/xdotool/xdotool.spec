# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           xdotool
Version:        3.20211022.1
Epoch:          1
Release:        9%{?dist}
Summary:        Fake keyboard/mouse input
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/jordansissel/xdotool
Source0:        https://github.com/jordansissel/xdotool/releases/download/v%{version}/xdotool-%{version}.tar.gz

Patch0:         0001-Use-XTEST-instead-of-XWarpPointer-with-a-single-scre.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: libXtst-devel, libX11-devel, libXinerama-devel, libXi-devel, perl-podlators, libxkbcommon-devel

%description
This tool lets you programmatically (or manually) simulate keyboard input
and mouse activity, move and re-size windows, etc.

%package -n libxdo
Summary: Keyboard input simulation library

%description -n libxdo
This library contains functions to simulate keyboard and mouse input

%package -n libxdo-devel
Summary:        Development files for libxdo
Requires:       libxdo = %{epoch}:%{version}-%{release}

%description -n libxdo-devel
The libxdo-devel package contains libraries and header files for
developing applications that use libxdo

%prep
%setup -q
%patch 0 -p1

%build
%set_build_flags
%make_build WITHOUT_RPATH_FIX=1

%install
%make_install PREFIX=%{_prefix} INSTALLMAN=%{_mandir} INSTALLLIB=%{_libdir}

#fix permissions
chmod 0644 examples/ffsp.sh

%ldconfig_scriptlets -n libxdo

%files -n libxdo
%doc CHANGELIST COPYRIGHT README.md
%{_libdir}/*.so.3*

%files -n libxdo-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libxdo.pc

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%doc examples

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20211022.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20211022.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1:3.20211022.1-7
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20211022.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20211022.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 16 2023 Olivier Fourdan <ofourdan@redhat.com> - 1:3.20211022.1-4
- Use XTEST instead of XWarpPointer with a single screen
  https://github.com/jordansissel/xdotool/pull/435

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20211022.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20211022.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 05 2022 Orion Poplawski <orion@nwra.com> - 1:3.20111022.1-1
- Update to 3.20111022.1
- Use set_build_flags and make macros

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20160805.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20160805.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jul 31 2021 Sven Lankes <sven@lank.es> - 1:3.20160805.1-4
- remove "rpath" fix to fix FTBFS
- fixes RHBZ #1988049

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20160805.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20160805.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 25 2020 Till Maas <opensource@till.name> - 3.20160805.1-1
- Update to latest release

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20150503.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Oliver Haessler <oliver@redhat.com> - 3.20150503.1-1
- new upstream release
- add BuildRequire for libxkbcommon-devel

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20110530.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20110530.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20110530.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20110530.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Feb 24 2013 Sven Lankes <sven@lank.es> - 1:2.20110530.1-6
- fix FTBFS, fixes rhbz #914583

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20110530.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1:2.20110530.1-4
- Add libXi-devel dependency

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20110530.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20110530.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Sven Lankes <sven@lank.es> - 1:2.20110530.1-1
- new upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.20101012.3049-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 11 2010 Sven Lankes <sven@lank.es> - 1:2.20101012.3049-1
- new upstream release

* Sun Jul 11 2010 Sven Lankes <sven@lank.es> - 1:2.20100623.2949-1
- remove upstreamed patch
- new upstream release

* Sun Mar 28 2010 Sven Lankes <sven@lank.es> - 1:2.20100602.2915-1
- new upstream release
- add patch from Bruce Jerrick to not segfault when called with unknown command (bz #602946)

* Sun Mar 28 2010 Sven Lankes <sven@lank.es> - 1:1.20100318.2737-1
- new upstream release

* Sun Feb 07 2010 Sven Lankes <sven@lank.es> - 0.20100118.2605-2
- fix requires for libxdo-devel

* Fri Feb 05 2010 Sven Lankes <sven@lank.es> - 0.20100118.2605-1
- New upstream release
- remove BuildRoot from spec
- add subpackages for libxdo
- ship manpage
- bump Epoch as upstream changed the versioning
- use make install (with a makefile-patch) instead of manual install in spec

* Thu Sep 17 2009 Sven Lankes <sven@lank.es> - 20090815-1
- New upstream release (fixes #521765)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090330-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 20090330-2
- New upstream release

* Thu May  7 2009 Ville Skyttä <ville.skytta at iki.fi> - 20090126-2
- Build with $RPM_OPT_FLAGS.

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 20090126-1
- New upstream release

* Mon Mar 02 2009 Caolán McNamara <caolanm@redhat.com> - 20071230-4
- add BuildRequires libX11-devel to build

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071230-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 28 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 20071230-2
- Add patch to fix prefix
- Add CFLAGS to %%build

* Tue May 06 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 20071230-1
- Initial build

