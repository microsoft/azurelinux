Vendor:         Microsoft Corporation
Distribution:   Mariner
# Recent so-version, so we do not bump accidentally.
%global so_ver      4

# Set to 1 when building a bootstrap for a bumped so-name.
%global bootstrap   0

%if 0%{?bootstrap}
%global version_old 4.0.2
%global so_ver_old  4
%endif


Name:           qrencode
Version:        4.0.2
Release:        6%{?dist}
Summary:        Generate QR 2D barcodes

License:        LGPLv2+
URL:            http://fukuchi.org/works/qrencode/
Source0:        http://fukuchi.org/works/qrencode/qrencode-%{version}.tar.bz2
%if 0%{?bootstrap}
Source1:        http://fukuchi.org/works/qrencode/qrencode-%{version_old}.tar.bz2
%endif

BuildRequires:  gcc
BuildRequires:  chrpath
BuildRequires:  libpng-devel
BuildRequires:  SDL-devel
## For ARM 64 support (RHBZ 926414)
BuildRequires:  autoconf >= 2.69

%description
Qrencode is a utility software using libqrencode to encode string data in
a QR Code and save as a PNG image.


%package        devel
Summary:        QR Code encoding library - Development files
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The qrencode-devel package contains libraries and header files for developing
applications that use qrencode.


%package        libs
Summary:        QR Code encoding library - Shared libraries

%description    libs
The qrencode-libs package contains the shared libraries and header files for
applications that use qrencode.


%prep
%autosetup -Tb 0 -p 1

%if 0%{?bootstrap}
mkdir -p bootstrap_ver
pushd bootstrap_ver
tar --strip-components=1 -xf %{SOURCE1}
popd
%endif


%build
## Rebuild configure scripts for ARM 64 support. (RHBZ 926414)
autoconf
%configure --with-tests
%make_build

%if 0%{?bootstrap}
pushd bootstrap_ver
autoconf
%configure --with-tests
%make_build
popd
%endif


%install
%if 0%{?bootstrap}
%make_install -C bootstrap_ver
%{_bindir}/find %{buildroot} -xtype f -not            \
  -name 'lib%{name}.so.%{so_ver_old}*' -delete -print
%{_bindir}/find %{buildroot} -type l -not             \
  -name 'lib%{name}.so.%{so_ver_old}*' -delete -print
%endif

%make_install
rm -f %{buildroot}%{_libdir}/libqrencode.la
chrpath --delete %{buildroot}%{_bindir}/qrencode


%check
pushd ./tests
sh test_all.sh
popd


%files
%{_bindir}/qrencode
%{_mandir}/man1/qrencode.1*


%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc ChangeLog NEWS README TODO
%{_libdir}/libqrencode.so.%{so_ver}*
%if 0%{?bootstrap}
%{_libdir}/libqrencode.so.%{so_ver_old}*
%endif


%files devel
%{_includedir}/qrencode.h
%{_libdir}/libqrencode.so
%{_libdir}/pkgconfig/libqrencode.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.0.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Björn Esser <besser82@fedoraproject.org> - 4.0.2-3
- Disable bootstrap after systemd rebuild

* Tue Jun 25 2019 Björn Esser <besser82@fedoraproject.org> - 4.0.2-2
- Implement bootstrap logic for so-name bumps

* Tue Jun 25 2019 Paul Wouters <pwouters@redhat.com> - 4.0.2-1
- Update to 4.0.2 and cleanup by Vasiliy N. Glazov <vascom2@gmail.com>

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 09 2018 Matthieu Saulnier <fantom@fedoraproject.org> - 3.4.4-7
- Remove French translation in spec file

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.4-4
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Peter Gordon <peter@thecodergeek.com> - 3.4.4-1
- Update to new upstream bug-fix release (3.4.4).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 3.4.2-3
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 11 2013 Peter Gordon <peter@thecodergeek.com> - 3.4.2-1
- Update to new upstream release (3.4.2)
  - Fixes a memory leak, string-splitting, and Micro QR encoding bugs.
- Run autoconf in %%build to add ARM 64 (aarch64) to the configure scripts.
- Resolves:  #926414 (qrencode: Does not support aarch64 in f19 and rawhide)
- Update source/homepage URLs.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jan 25 2013 Matthieu Saulnier <fantom@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1

* Fri Sep 21 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.3.1-4
- Add libs subpackage (fix RHBZ #856808)

* Thu Aug 16 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.3.1-3
- Add French translation in spec file
- Fix incomplete removing Group tags in spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.3.1-1
- update to 3.3.1
- remove "Group" tag in spec file
- fix manfile suffix
- remove patch to fix improper LIBPTHREAD macro in the pkgconfig file:
  - upstream issue

* Sat Feb 25 2012 Peter Gordon <peter@thecodergeek.com> - 3.2.0-3
- Fix applying the LIBPTHREAD patch. (Thanks to Matthieu Saulnier.)

* Thu Feb 23 2012 Peter Gordon <peter@thecodergeek.com> - 3.2.0-2
- Add patch to fix improper LIBPTHREAD macro in the pkgconfig file:
  + fix-LIBPTHREAD-macro.patch
- Resolves: #795582 (qrencode-devel: Malformed pkgconfig file causes build to
  fail ("@LIBPTHREAD@: No such file or directory"))

* Sun Jan 15 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.2.0-1
- update to 3.2.0
- remove BuildRoot tag in spec file
- remove "rm -rf $RPM_BUILD_ROOT" at the beginning of %%install section
- remove %%clean section
- remove %%defattr lines
- add a joker for libqrencode.so.* files

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.1.1-6
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-4
- Fixed the rpath problem.

* Mon Jul 12 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-3
- Fixed some small spec mistakes.

* Mon Jul 12 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-2
- Fixed some small errors.

* Thu Jul 08 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-1
- Initial build.
