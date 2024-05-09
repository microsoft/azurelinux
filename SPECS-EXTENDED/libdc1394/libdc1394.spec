Vendor:         Microsoft Corporation
Distribution:   Azure Linux

#define svn_snapshot .svn459  
#define real_version 2.1.0
%define svn_build %{?svn_snapshot:1}%{!?svn_snapshot:0}

Summary: 1394-based digital camera control library
Name: libdc1394
Version: 2.2.2
Release: 15%{?dist}
License: LGPLv2+
URL: https://sourceforge.net/projects/libdc1394/
Source: https://downloads.sourceforge.net/project/libdc1394/libdc1394-2/%{version}/libdc1394-%{version}.tar.gz
ExcludeArch: s390 s390x

BuildRequires:  gcc
BuildRequires: kernel-headers
BuildRequires: libraw1394-devel libusb1-devel
BuildRequires: doxygen
BuildRequires: perl-interpreter
BuildRequires: libX11-devel libXv-devel
%if %{svn_build}
BuildRequires: libtool
%endif

%description
Libdc1394 is a library that is intended to provide a high level programming
interface for application developers who wish to control IEEE 1394 based
cameras that conform to the 1394-based Digital Camera Specification.

%package devel
Summary: Header files and libraries for %{name}
Requires: %{name} = %{version}-%{release}, libraw1394-devel
Requires: pkgconfig

%description devel
This package contains the header files and libraries
for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package docs
Summary: Development documentation for %{name}

%description docs
This package contains the development documentation for %{name}.

%package tools
Summary: Tools for use with %{name}
Requires: %{name} = %{version}-%{release}

%description tools
This package contains tools that are useful when working and
developing with %{name}.

%prep
%setup -q -n libdc1394-%{version}

%build
%if %{svn_build}
cp /usr/share/libtool/ltmain.sh .
aclocal
autoheader
autoconf
automake --add-missing
%endif
%configure --disable-static --enable-doxygen-html --enable-doxygen-dot
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make doc

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
for p in grab_color_image grab_gray_image grab_partial_image ladybug grab_partial_pvn; do
	%{__install} -p -m 0644 -s examples/.libs/$p %{buildroot}%{_bindir}/dc1394_$p
done
%{__install} -p -m 0644 examples/dc1394_multiview %{buildroot}%{_bindir}/dc1394_multiview
for f in grab_color_image grab_gray_image grab_partial_image; do
	mv %{buildroot}%{_mandir}/man1/$f.1 %{buildroot}%{_mandir}/man1/dc1394_$f.1
done

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libdc1394*.so.*

%files devel
%doc examples/*.h examples/*.c
%{_includedir}/dc1394/
%{_libdir}/libdc1394*.so
%{_libdir}/pkgconfig/%{name}-2.pc
%exclude %{_libdir}/*.la

%files docs
%doc doc/html/*

%files tools
%{_bindir}/dc1394_*
%{_mandir}/man1/dc1394_*.1.gz

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.2-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Stephen Gallagher <sgallagh@redhat.com> - 2.2.2-6
- Add BR on perl to fix FTBFS on F25+

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Tim Niemueller <tim@niemueller.de> - 2.2.2-1
- Upgrade to latest stable release 2.2.2

* Wed Aug  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.2.0-4
- Install docs using %%doc (#993839).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jan 29 2013 Jay Fenlason <fenlason@redhat.com> - 2.2.0-2
- Fix two minor issues detected by rpmdiff: installed binaries not stripped
  and -tools depended on version not version-release

* Tue Dec 11 2012 Jay Fenlason <fenlason@redhat.com> - 2.2.0-1
- New upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 04 2012 Tim Niemueller <tim@niemueller.de> - 2.1.4-2
- Fix improperly installed tools (bz #593873)

* Wed Jan 04 2012 Tim Niemueller <tim@niemueller.de> - 2.1.4-1
- Update to latest stable release 2.1.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> 2.1.2-3
- excludearch s390 s390x where we don't have libraw1394

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Tim Niemueller <tim@niemueller.de> - 2.1.2-1
- Update to latest stable release 2.1.2

* Tue Mar 17 2009 Tim Niemueller <tim@niemueller.de> - 2.1.0-1
- Update to latest stable release 2.1.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 12 2008 Tim Niemueller <tim@niemueller.de> - 2.0.2-1
- Update to latest stable release 2.0.2

* Sat Jan 19 2008 Tim Niemueller <tim@niemueller.de> - 2.0.1-3
- Made autotools calls optional, only called if svn_snapshot is defined
- devel subpackage now requires pkgconfig

* Wed Jan 16 2008 Tim Niemueller <tim@niemueller.de> - 2.0.1-2
- Add docs subpackage to contain development documentation
- Incoroprate multilib tricks
- BuildReqire automake, autoconf, libtool and doxygen
- Removed unused BuildRequires
- Use header file from kernel-headers instead of kernel-devel
- BuildRequire kernel-devel
- Added tools subpackage to contain the resetbus and vloopback tools

* Wed Jan 16 2008 Tim Niemueller <tim@niemueller.de> - 2.0.1-1
- Update to 2.0.1, now patent-free!

* Mon Jan 07 2008 Tim Niemueller <tim@niemueller.de> - 2.0.0-1
- Update to 2.0.0

* Sun Dec 16 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc9
- Update to 2.0.0-rc9

* Wed Nov 28 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc7.3.svn459
- Updated to release 2.0.0-rc7+svn459 (not yet released)

* Fri Nov 02 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc7.1.svn443
- Updated to release 2.0.0-rc7+svn443 (not yet released) for juju support
- Added --without juju to disable juju support (necessary for FC6)

* Fri Feb 02 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc5.1
- Updated to release 2.0.0-rc5.

* Wed Aug 16 2006 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc3.1
- Updated to release 2.0.0-rc3.

* Mon May 08 2006 Dries Verachtert <dries@ulyssis.org> - 2.0.0-0.1.pre7
- Updated to release 2.0.0-0.1.pre7.

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 2.0.0-0.1.pre5.2
- Rebuild for Fedora Core 5.

* Thu Dec  8 2005 Matthias Saou <https://freshrpms.net/> 2.0.0-0.1.pre5
- Update to 2.0.0-pre5.
- Add missing libraw1394-devel dependency to the devel package.

* Tue Aug 30 2005 Dries Verachtert <dries@ulyssis.org> - 2.0.0-0.pre4
- Update to release 2.0.0-0.pre4.

* Thu Aug 25 2005 Dries Verachtert <dries@ulyssis.org> - 1.1.0-1
- Initial package.
