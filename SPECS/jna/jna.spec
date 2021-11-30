#
# spec file for package jna
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2000-2009, JPackage Project
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#

#need to disable debuginfo till we bring in x11 deps
%define debug_package %{nil}
Summary:        Java Native Access
Name:           jna
Version:        5.5.0
Release:        2%{?dist}
License:        ASL 2.0 AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/java-native-access/jna
Source0:        https://github.com/java-native-access/jna/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         jna_remove_clover_and_win32_native_jar.patch
BuildRequires:  ant
BuildRequires:  dos2unix
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  libffi
BuildRequires:  libffi-devel
BuildRequires:  openjdk8
#BuildRequires:  openjre8
BuildRequires:  openjdk-11-hotspot
BuildRequires:  javapackages-tools
#Requires:       openjre8
Requires:       openjdk-11-hotspot

%description
JNA provides Java programs easy access to native shared libraries
(DLLs on Windows) without writing anything but Java code. JNA's
design aims to provide native access in a natural way with a
minimum of effort. No boilerplate or generated code is required.
While some attention is paid to performance, correctness and ease
of use take priority.

%package        contrib
Summary:        Contrib for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    contrib
This package contains the contributed examples for %{name}.

%package        javadoc
Summary:        Javadocs for %{name}
BuildArch:      noarch

%description    javadoc
This package contains the javadocs for %{name}.

%prep
%setup -q
# Cleanup the dist tarball
find . -name '*jar' | xargs rm
rm -rf dist
dos2unix OTHERS

%patch0 -p1

sed -i 's|@LIBDIR@|%{_libdir}/%{name}|' src/com/sun/jna/Native.java

%clean
rm -rf %{buildroot}


%build
build-jar-repository -s -p lib ant
ant \
    jar \
    native \
    platform-jar \
    -Dbuild-native=true -Drelease \
    -Dcompatibility=1.6 -Dplatform.compatibility=1.6 \
    -Ddynlink.native=true \
    -Dcflags_extra.native=-DNO_JAWT \
    -Dtests.exclude-patterns="**/*.java" \
    jar \
    native \
    platform-jar \
    javadoc

%install
# NOTE: JNA has highly custom code to look for native jars in this
# directory.  Since this roughly matches the jpackage guidelines,
# we'll leave it unchanged.
install -d -m 755 %{buildroot}%{_libdir}/%{name}
install -m 755 build/native*/libjnidispatch*.so %{buildroot}%{_libdir}/%{name}/

install -d -m 755 %{buildroot}%{_jnidir}/%{name}
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -p -m 644 build/jna-min.jar %{buildroot}%{_jnidir}/%{name}.jar
ln -sf ../%{name}.jar %{buildroot}%{_jnidir}/%{name}/%{name}.jar
ln -sf %{_jnidir}/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar
install -p -m 644 ./contrib/platform/dist/jna-platform.jar %{buildroot}%{_javadir}/%{name}-platform.jar
ln -sf ../%{name}-platform.jar %{buildroot}%{_javadir}/%{name}/%{name}-platform.jar

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 pom-jna.xml %{buildroot}/%{_mavenpomdir}/%{name}.pom
install -p -m 644 pom-jna-platform.xml %{buildroot}/%{_mavenpomdir}/%{name}-platform.pom
%add_maven_depmap %{name}.pom %{name}.jar
%add_maven_depmap %{name}-platform.pom %{name}-platform.jar -a net.java.dev.jna:platform -f contrib

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}

%check
#ignore a unicode name test which fails in chroot checks
sed -i 's/testLoadLibraryWithUnicodeName/ignore_testLoadLibraryWithUnicodeName/' test/com/sun/jna/LibraryLoadTest.java
ant

%files -f .mfiles
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libjnidispatch.so
%{_jnidir}/%{name}
%{_javadir}/%{name}.jar
%license LICENSE
%doc CHANGES.md OTHERS README.md TODO

%files contrib -f .mfiles-contrib
%{_javadir}/%{name}

%files javadoc
%{_javadocdir}/jna
%license LICENSE

%changelog
* Wed Nov 17 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.5.0-2
- License verified.

* Fri Nov 20 2020 Joe Schmitt <joschmit@microsoft.com> - 5.5.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Disable JAWT to avoid X11 header dependencies.
- Remove unneeded patches.

* Mon Oct 12 2020 Dominique Leuenberger <dimstar@opensuse.org>
- %%{suffix} is an rpm internal macro that extracts a suffix
  (extension) from a filename. With RPM 4.16, it verifies that a
  filename is passed (e.g. %%{suffix:filename.spec}); earlier
  versions returned "", meaning we can just strip it from the
  install command, as we rely on an empty return value.

* Thu Jun  4 2020 Fridrich Strba <fstrba@suse.com>
- Upgrade to 5.5.0
  * Features
    + Add CoreFoundation, IOKit, and DiskArbitration mappings in
    c.s.j.p.mac.
    + c.s.j.p.mac.SystemB now extends c.s.j.p.unix.LibCAPI.
    + Add additional OSGi headers for the JNA bundle to support
    32bit ARM (hardfloat)
    + Include Win32 COM utils (c.s.j.p.win32.com.util and
    c.s.j.p.win32.com.annotation) in OSGI bundle
  * Bug Fixes
    + Fix signature for c.s.j.p.win32.Kernel32#CreateRemoteThread
    and bind VirtualAllocEx, VirtualFreeEx, GetExitCodeThread in
    c.s.j.p.win32.Kernel32
    + Windows needs a wide string in
    c.s.j.p.win32.COM.IShellFolder#ParseDisplayName
    + KEY_ALL_ACCESS value is incorrect in c.s.j.p.win32.WinNT.java
    + Ensure JARs created from the build system don't contain
    invalid Info-ZIP Unicode Path extra info
    + Read correct member of
    WinBase.SYSTEM_INFO.processorArchitecture union
    + Fix passing unions containing integer and floating point
    members as parameters by value
- Modified patch:
  * jna-build.patch
    + rediff to the changed context
    + disable warnings as errors
    + fix build on ppc64 and s390x

* Thu Oct 10 2019 Fridrich Strba <fstrba@suse.com>
- Rename package to jna, since the jna package must be anyway
  archful
- Upgrade to 5.4.0
- Split the package into:
  * jna
    + archful package
    + provides and obsoletes the libjnidispatch package
    + packages the libjnidispatch.so
  * jna-contrib
    + noarch package
    + contains the jna-platform examples
- Removed patches:
  * jna-4.5.1-nojavah.patch
  * jna-getpeer.patch
  * jna-msgsize.patch
    + not needed anymore with this version
- Modified patches:
  * jna-build.patch
  * jna-callback.patch
    + Adapted to changed context
- Added patches:
  * jna-system-libjnidispatch.patch
    + Load the libjnidispatch from system
  * jna-java8compat.patch
    + Add casts to prevent using of java9+ only ByteBuffer
    methods

* Wed Mar 13 2019 Fridrich Strba <fstrba@suse.com>
- Decide whether to apply the jna-4.5.0-nojavah.patch according
  to what java-devel version is used for build

* Wed Oct 24 2018 Fridrich Strba <fstrba@suse.com>
- Install the provided pom*.xml files in order to make maven aware
  about the jna-platform too

* Thu Jul 26 2018 msuchanek@suse.com
- Fix dealing with different java environments
- Fix license warning

* Wed Jun 13 2018 msuchanek@suse.com
- do not apply nojavah on Leap 42.3 - breaks build
- quiet warnings
  + jna-msgsize.patch
  + jna-callback.patch
  + delete jna-no-werror.patch

* Tue Jun 12 2018 fstrba@suse.com
- Upstrem version 4.5.1
- Modified patch:
  * jna-4.5.0-nojavah.patch -> jna-4.5.1-nojavah.patch
    + Rediff to changed context, rework dependency chain and do not
    try to load urls in the no-network build environment
- Added patch:
  * jna-no-werror.patch
    + Disable -Werror to enable build with two new warnings
- Build with compatibility 1.8

* Tue Jan  9 2018 fstrba@suse.com
- Added patch:
  * jna-4.5.0-nojavah.patch
    + Fix build with jdk10
    + Generate relevant header files during javac run

* Tue Jan  2 2018 fstrba@suse.com
- Force build with jdk < 10

* Mon Oct 30 2017 ecsos@opensuse.org
- change version and name from jna-4.1.0.pom to jna-4.5.0.pom
- fix require libjnidispatch-version in jna-package

* Tue Sep 19 2017 fstrba@suse.com
- Upstream version 4.5.0
- Removed patch:
  * reproducible.patch
    + integrated upstream
- Added patch:
  * jna-getpeer.patch
    + upstream workaround to the inaccessibility of the getPeer
    method
    + Fix build with jdk9
- Modified patch:
  * jna-build.patch
    + rediff to the new context

* Tue Sep 19 2017 fstrba@suse.com
- Build with source and target levels 1.6
- Force building with java-devel < 1.9, since the code uses APIs
  removed in jdk9

* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
- drop conditionals for unsupported SUSE versions

* Fri Feb 24 2017 msuchanek@suse.com
- Upstream version 4.2.2
  * adds some symbols needed by Arduino IDE.

* Fri Mar 18 2016 bwiedemann@suse.com
- Add reproducible.patch to fix build-compare

* Sun Nov  8 2015 p.drouand@gmail.com
- Update to version 4.2.1
  * Add support for linux-sparcv9.
  * Added `GetCommState`, `GetCommTimeouts` `SetCommState` and `SetCommTimeouts`
    to `com.sun.jna.platform.win32.Kernel32`. Added `DCB` structure to
    `com.sun.jna.platform.win32.WinBase.
  * Make loading debug flags mutable.
  * Added `host_processor_info` to `com.sun.jna.platform.mac.SystemB`.
  * Added JNA functional overview.
  * Update linux-arm natives omitted in 4.2.
- Update jna-4.1.0-build.patch > jna-build.patch

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Mon Nov  3 2014 cbosdonnat@suse.com
- Updated to 4.1.0. See the changelog on:
  https://github.com/twall/jna/blob/master/CHANGES.md
- Updated jna-3.4.0-build.patch into jna-4.1.0-build.patch
- Added libjnidispatch.rpmlintrc to silence warning about explicit
  library dependency between jna and libjnidistach: rpm doesn't
  detect library dependencies on Java packages, we need to force it.
- Removed libffi patches: now using the libffi package.
  * libffi-aarch64.patch
  * libffi-ppc64le.patch
- Added rpmlint filters:
  * libjnidispatch-rpmlintrc

* Tue Jul  8 2014 tchvatal@suse.com
- Do not depend on ant-trax and run spec-cleaner.

* Mon Dec  9 2013 dvaleev@suse.com
- enable ppc64le
- added patches:
  * libffi-ppc64le.patch

* Wed Sep 11 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Thu Apr 11 2013 schwab@suse.de
- libffi-aarch64.patch: import aarch64 support for libffi

* Wed Dec 12 2012 dvaleev@suse.com
- enable ppc and ppc64 builds

* Wed Nov 14 2012 mvyskocil@suse.com
- fix a build for non-suse distros

* Tue Jun 19 2012 mvyskocil@suse.cz
- fix a build with jdk7
- rename to libjnidispatch to follow packaging policy (provides jna-native)
- jna and jna-javadoc are now noarch subpackages of it
- don't strip a binary during a build

* Thu Feb  9 2012 mvyskocil@suse.cz
- Update to 3.4.0
  * moved object creation out into pure Java code reduce JNI crossing
  * add native peer value accessors for Pointer
  * avoid loading any system-provided JNA via jna.nosys=true
  * override default jnidispatch library name with jna.boot.library
  * throw an error if JNA is not with a library
  * linux/arm and linux/ppc 32-bit support
  * preliminary linux/ppc64 support
  * linux multi-arch support (kohsuke).
  * add to `platform.unix.x11`: `XGrabKey`, `XUngrabKey`, `XSetErrorHandler`.
  * and a lot of bugfixes (see /usr/share/packages/doc/jna/README.md)
- fix bnc#745571 enable build of jna-native as well

* Thu Apr  8 2010 mvyskocil@suse.cz
- update to 3.1.0 (jna-3.1.0-2.jpp6.src.rpm)
  * raw JNI mapping of static Java methods increased performance
  * library option to allow passing/return of Java Objects.
  * handling of uncaught callback exceptions (Issue 63).
  * object oriented interface to X server (see contrib/x11)
  * Memory class more accessible.
  * allow implicit library access to current process on linux (issue 98).
  * open all shared libraries with RTLD_GLOBAL, if applicable. This was the default behavior on OSX and changes the default behavior on linux.
  * allow NIO Buffer as Structure field (with limitations) (Issue 57)
  * add size_t size.
  * Bug Fixes

* Mon Jun  1 2009 mvyskocil@suse.cz
- fixed bnc#507734:  jna declared LGPL but contains GPL files and binaries
  * removed all jars from source archive
  * added gpl to docdir

* Tue May 19 2009 mvyskocil@suse.cz
- 'Initial SUSE packaging from jpackage.org 5.0'
