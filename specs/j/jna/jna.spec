## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Allow conditionally building without the reflections library
%if %{defined rhel}
%bcond_with reflections
%else
%bcond_without reflections
%endif

Name:           jna
Version:        5.17.0
Release:        %autorelease
Summary:        Pure Java access to native libraries
# Most of code is dual-licensed under either LGPL 2.1+ only or Apache
# License 2.0.  WeakIdentityHashMap.java was taken from Apache CXF,
# which is pure Apache License 2.0.
License:        Apache-2.0 OR LGPL-2.1-or-later

URL:            https://github.com/java-native-access/jna/
# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.zst
Source1:        package-list
Source2:        generate-tarball.sh

Patch0:         0001-Adapt-build.patch
# This patch is Fedora-specific for now until we get the huge
# JNI library location mess sorted upstream
Patch1:         0002-Load-system-library.patch
# The X11 tests currently segfault; overall I think the X11 JNA stuff is just a
# Really Bad Idea, for relying on AWT internals, using the X11 API at all,
# and using a complex API like X11 through JNA just increases the potential
# for problems.
Patch2:         0003-Tests-headless.patch
# Adds --allow-script-in-comments arg to javadoc to avoid error
Patch3:         0004-Fix-javadoc-build.patch
# Avoid generating duplicate manifest entry
# See https://bugzilla.redhat.com/show_bug.cgi?id=1469022
Patch4:         0005-Fix-duplicate-manifest-entry.patch
# We don't want newly added warnings to break our build
Patch5:         0006-Remove-Werror.patch

Patch6:         0007-Support-openjdk-17.patch

ExclusiveArch:  %{java_arches}

# We manually require libffi because find-requires doesn't work
# inside jars.
Requires:       libffi
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  javapackages-local-openjdk25
BuildRequires:  libffi-devel
BuildRequires:  ant-openjdk25 
BuildRequires:  ant-junit
BuildRequires:  junit
BuildRequires:  libX11-devel
BuildRequires:  libXt-devel
BuildRequires:  objectweb-asm
BuildRequires:  hamcrest
%if %{with reflections}
BuildRequires:  reflections
%endif

# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 5.15.0-4

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

%prep
%autosetup -p1
cp %{SOURCE1} .

chmod -Rf a+rX,u+w,g-w,o-w .
sed -i 's|@LIBDIR@|%{_libdir}/%{name}|' src/com/sun/jna/Native.java

# TEMPLATE has to be changed to %%version in the pom files
# in order to generate correct provides
sed -i 's/TEMPLATE/%{version}/' \
 pom-jna-jpms.xml \
 pom-jna-platform.xml \
 pom-jna.xml \
 pom-jna-platform-jpms.xml \
;

# clean LICENSE.txt
sed -i 's/\r//' LICENSE

chmod -c 0644 LICENSE OTHERS CHANGES.md

%if %{with reflections}
sed s,'<include name="junit.jar"/>,&<include name="reflections.jar"/>,' -i build.xml
build-jar-repository -s -p lib junit reflections
%else
build-jar-repository -s -p lib junit
rm test/com/sun/jna/StructureFieldOrderInspector.java
rm test/com/sun/jna/StructureFieldOrderInspectorTest.java
%endif
ln -s $(xmvn-resolve ant:ant:1.10.5) lib/ant.jar
ln -s $(xmvn-resolve org.ow2.asm:asm) lib/asm-8.0.1.jar
ln -s $(xmvn-resolve org.hamcrest:hamcrest-all) lib/hamcrest-core-1.3.jar
ln -s $(xmvn-resolve org.reflections:reflections) lib/test/reflections.jar

cp lib/native/aix-ppc64.jar lib/clover.jar

%build
# We pass -Ddynlink.native which comes from our patch because
# upstream doesn't want to default to dynamic linking.
# -Drelease removes the .SNAPSHOT suffix from maven artifact names
#ant -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true native compile javadoc jar contrib-jars
ant -Drelease -Dcompatibility=1.8 -Dplatform.compatibility=1.8\
 -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true -DCC=%{__cc} native dist
# remove compiled contribs
find contrib -name build -exec rm -rf {} \; || :

%install
# NOTE: JNA has highly custom code to look for native jars in this
# directory.  Since this roughly matches the jpackage guidelines,
# we'll leave it unchanged.
install -d -m 755 %{buildroot}%{_libdir}/%{name}
install -m 755 build/native*/libjnidispatch*.so %{buildroot}%{_libdir}/%{name}/

%mvn_file :jna jna jna/jna %{_javadir}/jna

%mvn_package :jna-platform contrib
%mvn_alias :jna-platform :platform

%mvn_artifact pom-jna.xml build/jna-min.jar
%mvn_artifact pom-jna-platform.xml contrib/platform/dist/jna-platform.jar

%mvn_install

%files -f .mfiles
%doc OTHERS README.md CHANGES.md TODO
%license LICENSE LGPL2.1 AL2.0
%{_libdir}/%{name}

%files contrib -f .mfiles-contrib

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 5.17.0-6
- Latest state for jna

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 5.17.0-5
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.17.0-3
- Build with OpenJDK 25

* Sat Jul 12 2025 Miroslav Suchý <msuchy@redhat.com> - 5.17.0-2
- Migrate to SPDX license

* Wed Jun 04 2025 Marian Koncek <mkoncek@redhat.com> - 5.17.0-1
- Update to upstream version 5.17.0

* Wed Jun 04 2025 Marian Koncek <mkoncek@redhat.com> - 5.15.0-5
- Drop javadoc subpackage

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.15.0-4
- Switch to javapackages tests from CentOS Stream GitLab

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 24 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.15.0-2
- Rebuild to regenerate auto-requires

* Tue Sep 17 2024 Marian Koncek <mkoncek@redhat.com> - 5.15.0-1
- Update to upstream version 5.15.0

* Tue Sep 17 2024 Marian Koncek <mkoncek@redhat.com> - 5.14.0-10
- Remove double newlines

* Mon Sep 16 2024 Marian Koncek <mkoncek@redhat.com> - 5.14.0-9
- Use %%autosetup

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 5.14.0-4
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Zuzana Miklankova <zmiklank@redhat.com> - 5.14.0-1
- Rebase to version 5.14.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Zuzana Miklankova <zmiklank@redhat.com> - 5.13.0-1
- Rebase to version 5.13.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Zuzana Miklankova <zmiklank@redhat.com> - 5.12.1-1
- Rebase to version 5.12.1

* Mon May 16 2022 Zuzana Miklankova <zmiklank@redhat.com> - 5.11.0-2
- Use correct version in provided pom files

* Mon Mar 28 2022 Zuzana Miklankova <zmiklank@redhat.com> - 5.11.0-1
- Rebase to version 5.11.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 5.10.0-3
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Zuzana Miklankova <zmiklank@redhat.com> - 5.10.0-1
- Rebase to version 5.10.0

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 5.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Wed Dec 1 2021 Zuzana Miklankova <zmiklank@redhat.com> - 5.9.0-3
- Support openjdk-17 with dropping 1.6 compatibility

* Wed Dec 1 2021 Zuzana Miklankova <zmiklank@redhat.com> - 5.9.0-2
- Rebuild with resolved reflections dependecy

* Fri Sep 17 2021 Ondrej Dubaj <odubaj@redhat.com> - 5.9.0-1
- Rebase to version 5.9.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 12 2021 Ondrej Dubaj <odubaj@redhat.com> - 5.6.0-3
- Remove maven-javadoc-plugin dependency

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Ondrej Dubaj <odubaj@redhat.com> - 5.6.0-1
- Rebase to version 5.6.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Fabio Valentini <decathorpe@gmail.com> - 5.4.0-6
- Remove special-cased aarch32 build for java-1.8.0-openjdk.

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 5.4.0-5
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jul 09 2020 Mat Booth <mat.booth@redhat.com> - 5.4.0-4
- Fix conditional build without reflections

* Thu Apr 02 2020 Tom Stellard <tstellar@redhat.com> - 5.4.0-3
- Pass C compiler to ant

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 01 2019 Marian Koncek <mkoncek@redhat.com> - 5.4.0-1
- Update to upstream version 5.4.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Mat Booth <mat.booth@redhat.com> - 4.5.1-9
- Minor correction in license tag

* Mon Jun 17 2019 Mat Booth <mat.booth@redhat.com> - 4.5.1-8
- Use xmvn-resolve for portable way to get the ant jar

* Sat Jun 08 2019 Mat Booth <mbooth@apache.org> - 4.5.1-7
- Speed up builds on 32bit arm

* Thu Mar 07 2019 Mat Booth <mat.booth@redhat.com> - 4.5.1-6
- Allow conditionally building without the reflections library for tests

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Michael Simacek <msimacek@redhat.com> - 4.5.1-3
- Disable -Werror

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Michael Simacek <msimacek@redhat.com> - 4.5.1-1
- Update to upstream version 4.5.1

* Tue Sep 19 2017 Michael Simacek <msimacek@redhat.com> - 4.5.0-1
- Update to upstream version 4.5.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.0-5
- Fix generation of JAR manifest
- Resolves: rhbz#1472494

* Mon Jul 10 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.0-4
- Fix duplicate manifest bug
- Resolves: rhbz#1469022

* Fri Jul 07 2017 Michael Simacek <msimacek@redhat.com> - 4.4.0-3
- Temporarily add symlink to javadir

* Mon Jul 03 2017 Michael Simacek <msimacek@redhat.com> - 4.4.0-2
- Install with XMvn

* Tue Mar 28 2017 Michael Simacek <msimacek@redhat.com> - 4.4.0-1
- Update to upstream version 4.4.0

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 4.3.0-4
- Use --allow-script-in-comments on all arches

* Wed Feb  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-3
- Add missing build-requires on GCC

* Tue Jan 31 2017 Michael Simacek <msimacek@redhat.com> - 4.3.0-2
- Try to fix javadoc generation

* Mon Jan 16 2017 Michael Simacek <msimacek@redhat.com> - 4.3.0-1
- Update to upstream version 4.3.0
- Cleanup rhel macros, because packages was retired in EPEL

* Thu Mar 24 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.2-1
- Update to upstream version 4.2.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-1
- Update to upstream version 4.2.1

* Thu Sep 17 2015 Levente Farkas <lfarkas@lfarkas.org> - 4.2.0-1
- Update to 4.2.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.0-8
- Force Java 1.6 source/target (rhbz#842609)
- Fix licensing headers (rhbz#988808)

* Wed Oct 01 2014 Michal Srb <msrb@redhat.com> - 4.1.0-7
- Fix for 32-bit systems (Resolves: rhbz#1148349)
- Fix FTBFS (Resolves: rhbz#1106955)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 10 2014 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-4
- fix updated depmap

* Fri Jan 10 2014 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-3
- Update depmap calls and fix tests compilation issue.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul  6 2013 Levente Farkas <lfarkas@lfarkas.org> - 4.0-1
- Update to 4.0

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.2-2
- Fix ant-trax and ant-nodeps BR on RHEL

* Thu Apr 25 2013 Levente Farkas <lfarkas@lfarkas.org> - 3.5.2-1
- Update to 3.5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Levente Farkas <lfarkas@lfarkas.org> - 3.4.0-4
- fix #833786 by Mary Ellen Foster 

* Wed Mar 14 2012 Juan Hernandez <juan.hernandez@redhat.com> - 3.4.0-3
- Generate correctly the maven dependencies map (#)

* Sun Mar 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.4.0-2
- Don't strip binaries too early, build with $RPM_LD_FLAGS (#802020).

* Wed Mar  7 2012 Levente Farkas <lfarkas@lfarkas.org> - 3.4.0-1
- Update to 3.4.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.2.7-11
- Drop dependency on main package from -javadoc.
- Add license to -javadoc, and OTHERS and TODO to main package docs.
- Install javadocs and jars unversioned.
- Fix release-notes.html permissions.
- Make -javadoc and -contrib noarch where available.

* Fri Dec  3 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-10
- fix pom file name #655810
- disable check everywhere since it seems to always fail in mock

* Fri Nov  5 2010 Dan Horák <dan[at]danny.cz> - 3.2.7-9
- exclude checks on s390(x)

* Tue Oct 12 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-8
- exclude check on ppc

* Fri Oct  8 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-7
- fix excludearch condition

* Wed Oct  6 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-6
- readd excludearch for old release fix #548099

* Fri Oct 01 2010 Dennis Gilmore <dennis@ausil.us> - 3.2.7-5.1
- remove the ExcludeArch it makes no sense

* Sun Aug  1 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-5
- reenable test and clean up contrib files

* Tue Jul 27 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-4
- add Obsoletes for jna-examples

* Sat Jul 24 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-3
- upstream 64bit fixes

* Fri Jul 23 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-2
- Temporary hack for 64bit build

* Thu Jul 22 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-1
- Rebase on upstream 3.2.7

* Wed Jul 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-6
- Add maven depmap

* Thu Apr 22 2010 Colin Walters <walters@verbum.org> - 3.2.4-5
- Add patches to make the build happen with gcj

* Wed Apr 21 2010 Colin Walters <walters@verbum.org> - 3.2.4-4
- Fix the build by removing upstream's hardcoded md5

* Thu Dec 17 2009 Levente Farkas <lfarkas@lfarkas.org> - 3.2.4-3
- add proper ExclusiveArch

* Thu Dec 17 2009 Alexander Kurtakov <akurtako@redhat.com> 3.2.4-2
- Comment rhel ExclusiveArchs - not correct applies on Fedora.

* Sat Nov 14 2009 Levente Farkas <lfarkas@lfarkas.org> - 3.2.4-1
- Rebase on upstream 3.2.4

* Thu Oct 29 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.9-6
- Add examples subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Colin Walters <walters@redhat.com> - 3.0.9-3
- Add patch to allow opening current process

* Sun Nov 30 2008 Colin Walters <walters@redhat.com> - 3.0.9-2
- Fix library mapping, remove upstreamed patches

* Fri Oct 31 2008 Colin Walters <walters@redhat.com> - 3.0.9-1
- Rebase on upstream 3.0.9

* Tue Oct 14 2008 Colin Walters <walters@redhat.com> - 3.0.4-10.svn729
- Add patch to support String[] returns

* Wed Oct 01 2008 Colin Walters <walters@redhat.com> - 3.0.4-9.svn729
- Add new patch to support NativeMapped[] which I want

* Wed Oct 01 2008 Colin Walters <walters@redhat.com> - 3.0.4-8.svn729
- Update to svn r729
- drop upstreamed typemapper patch

* Thu Sep 18 2008 Colin Walters <walters@redhat.com> - 3.0.4-7.svn700
- Add patch to make typemapper always accessible
- Add patch to skip cracktastic X11 test bits which currently fail

* Tue Sep 09 2008 Colin Walters <walters@redhat.com> - 3.0.4-5.svn700
- Update to upstream SVN r700; drop all now upstreamed patches

* Sat Sep 06 2008 Colin Walters <walters@redhat.com> - 3.0.4-3.svn630
- A few more patches for JGIR

* Thu Sep 04 2008 Colin Walters <walters@redhat.com> - 3.0.4-2.svn630
- Add two (sent upstream) patches that I need for JGIR

* Thu Jul 31 2008 Colin Walters <walters@redhat.com> - 3.0.4-1.svn630
- New upstream version, drop upstreamed patch parts
- New patch jna-3.0.4-nomixedjar.patch which ensures that we don't
  include the .so in the .jar

* Fri Apr 04 2008 Colin Walters <walters@redhat.com> - 3.0.2-7
- Add patch to use JPackage-compatible JNI library path
- Do build debuginfo package
- Refactor build patch greatly so it's hopefully upstreamable
- Install .so directly to JNI directory, rather than inside jar
- Clean up Requires/BuildRequires (thanks Mamoru Tasaka)

* Sun Mar 30 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-6
- -javadocs should be -javadoc.
- %%files section cleaned a bit.

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-5
- -javadocs package should be in group "Documentation".

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-4
- License should be LGPLv2+, not GPLv2+.
- Several minor fixes.
- Fix Requires in javadoc package.

* Sun Mar 16 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-3
- Don't use internal libffi.

* Thu Mar 6 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-2
- Don't pull in jars from the web.

* Mon Mar 3 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-1
- Initial package.

## END: Generated by rpmautospec
