Name:		orc
Version:	0.4.39
Release:	2%{?dist}
Summary:	The Oil Run-time Compiler

License:	BSD-2-Clause AND BSD-3-Clause
Vendor:         Microsoft Corporation                              
Distribution:   Azure Linux
URL:		http://cgit.freedesktop.org/gstreamer/orc/
Source0:	https://gstreamer.freedesktop.org/src/orc/%{name}-%{version}.tar.xz

Patch0001:	0001-powerpc-fix-div255w-which-still-used-the-inexact-sub.patch

BuildRequires:	meson >= 0.47.0
BuildRequires:  gcc
BuildRequires:	gtk-doc

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

%package doc
Summary:	Documentation for Orc
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for Orc.

%package devel
Summary:	Development files and libraries for Orc
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-compiler
Requires:	pkgconfig

%description devel
This package contains the files needed to build packages that depend
on orc.

%package compiler
Summary:	Orc compiler
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description compiler
The Orc compiler, to produce optimized code.


%prep
%autosetup -p1

%build
%meson -D default_library=shared
%meson_build

%install
%meson_install

# Remove unneeded files.
find %{buildroot}/%{_libdir} -name \*.a -delete
rm -rf %{buildroot}/%{_libdir}/orc

%check
%meson_test

%ldconfig_scriptlets


%files
%license COPYING
%doc README
%{_libdir}/liborc-0.4.so.0*
%{_libdir}/liborc-test-0.4.so*
%{_bindir}/orc-bugreport

%files doc
%doc %{_datadir}/gtk-doc/html/orc/

%files devel
%doc examples/*.c
%{_includedir}/%{name}-0.4/
%{_libdir}/liborc-0.4.so
%{_libdir}/pkgconfig/orc-0.4.pc
%{_libdir}/pkgconfig/orc-test-0.4.pc

%files compiler
%{_bindir}/orcc


%changelog
* Tue Dec 17 2024 Jyoti kanase <v-jykanase@microsoft.com> - 0.4.39-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Tue Jul 30 2024 Wim Taymans <wtaymans@redhat.com> 0.4.39-1
- Update to 0.4.39
- Add patch for div255w fix on ppc64le

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.38-2
- Move orc-test to main package

* Tue Mar 05 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.38-1
- Update to 0.4.38
- Version the library to catch bumps
- Cleanup spec, use license var

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Wim Taymans <wtaymans@redhat.com> 0.4.33-1
- Update to 0.4.33

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.31-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 18 2021 Vít Ondruch <vondruch@redhat.com> - 0.4.31-6
- Fix ppc64le segfault when used via libvips.
  Resolves: rhbz#1917540

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Wim Taymans <wtaymans@redhat.com> 0.4.31-1
- Update to 0.4.31

* Tue Sep 24 2019 Wim Taymans <wtaymans@redhat.com> 0.4.30-1
- Update to 0.4.30
- Use meson as autogen was removed, add meson buildrequires

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Dan Horák <dan[at]danny.cz> 0.4.29-2
- revert commits changing ppc64/ppc64le support

* Tue Apr 23 2019 Wim Taymans <wtaymans@redhat.com> 0.4.29-1
- Update to 0.4.29
- Add orc-test pkgconfig file

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Wim Taymans <wtaymans@redhat.com> 0.4.28-1
- Update to 0.4.28
- Disable regeneration of docs

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Wim Taymans <wtaymans@redhat.com> 0.4.27-1
- Update to 0.4.27

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 31 2016 Wim Taymans <wtaymans@redhat.com> 0.4.26-1
- Update to 0.4.26

* Mon Mar 07 2016 Wim Taymans <wtaymans@redhat.com> 0.4.25-1
- Update to 0.4.25

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> 0.4.24-1
- Update to 0.4.24

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Wim Taymans <wtaymans@redhat.com> 0.4.23-1
- Update to 0.4.23

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.4.22-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Sep 11 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.4.22-3
- Do not run tests on aarch64

* Thu Sep  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.22-2
- Add upstream patch for selinux issue with tmp files

* Fri Aug 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.22-1
- Update to 0.4.22

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.4.18-1
- Update to 0.4.18.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.17-2
- Fix typo rhbz#817944

* Wed Feb 20 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.17-1
- Update to latest upstream release
- Removed obsolete patches

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Daniel Drake <dsd@laptop.org> - 0.4.16-7
- Fix fallback path when register allocation fails
- Fixes gstreamer-1.0 crash on OLPC XO-1.75

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 07 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-5
- Updated subdir patch.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.16-4
- Rebuilt for glibc bug#747377

* Sun Oct 16 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-3
- Add Fedora specific patch for tempfiles in subdirs

* Sun Oct 16 2011 Daniel Drake <dsd@laptop.org> - 0.4.16-2
- Add upstream patches to fix gstreamer crash on Geode (#746185)

* Mon Oct 03 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-1
- Update to 0.4.16
- Fixing regression introdcued by 0.4.15 (#742534 and #734911)

* Mon Sep 26 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.15-1
- Update to 0.4.15

* Mon Jun 20 2011 Peter Robinson <pbrobinson@gmail.com> - 0.4.14-3
- Add ARM platforms to the make check exclusion

* Sat May 07 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.14-2
- Add orc-bugreport to the main package (#702727)

* Sat Apr 30 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.14-1
- Update to 0.4.14

* Tue Apr 19 2011 Fabian Deutsch <fabiand@fedorpaproject.org> - 0.4.13-1
- Update to 0.4.13, another bug fixing release

* Fri Apr 15 2011 Fabian Deutsch <fabiand@fedorpaproject.org> - 0.4.12-1
- Update to 0.4.12, a bug fixing release

* Wed Feb 23 2011 Karsten Hopp <karsten@redhat.com> 0.4.11-3
- don't run tests on ppc, ppc64

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.11-1
- Update to 0.4.11.
- More bug fixes for CPUs that do not have backends, mmx and sse.

* Fri Oct 08 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.10-1
- Update to 0.4.10.
- Fixes some bugs related to SELinux.

* Mon Sep 06 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9, a pimarily bug fixing release.

* Thu Aug 19 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.7-1
- Updated to 0.4.7.

* Thu Jul 22 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.6-1
- Updated to 0.4.6.
- New orc-bugreport added.

* Tue Jul 13 2010 Dan Horák <dan[at]danny.cz> - 0.4.5-3
- don't run test on s390(x)

* Sun Jun 13 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.5-2
- Added removed testing libraries to package.

* Sun Jun 13 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.5-1
- Updated to 0.4.5.
- Removed testing libraries from package.

* Mon Apr 05 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.4-2
- Docs as noarch.
- Sanitize timestamps of header files.
- orcc in -compiler subpackage.

* Tue Mar 30 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.4-1
- Updated to 0.4.4: Includes bugfixes for x86_64.

* Wed Mar 17 2010 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.3-2
- Running autoreconf to prevent building problems.
- Added missing files to docs.
- Added examples to devel docs.

* Thu Mar 04 2010 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.3-1
- Updated to 0.4.3

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-4
- Removed unused libdir

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-3
- Specfile cleanup
- Removed tools subpackage
- Added docs subpackage

* Sat Oct 03 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-2
- Use orc as pakage name
- spec-file cleanup
- Added devel requirements
- Removed an rpath issue

* Fri Oct 02 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-1
- Initial release

