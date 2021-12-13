Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package rhino
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

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define scm_version 1_7_7_1
Name:           rhino
Version:        1.7.7.1
Release:        2%{?dist}
Summary:        JavaScript for Java
License:        MPL-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/mozilla/rhino
Source0:        https://github.com/mozilla/rhino/archive/Rhino%{scm_version}_RELEASE.tar.gz
Source1:        https://repo1.maven.org/maven2/org/mozilla/rhino/%{version}/rhino-%{version}.pom
Source2:        rhino.script
Source3:        rhino-debugger.script
Source4:        rhino-idswitch.script
Source5:        rhino-jsc.script
Patch0:         rhino-build.patch
# Add OSGi metadata from Eclipse Orbit project
Patch1:         rhino-addOrbitManifest.patch
BuildRequires:  ant
BuildRequires:  java-devel >= 1.7
BuildRequires:  javapackages-local-bootstrap
Requires:       javapackages-tools
Requires:       jline
BuildArch:      noarch

%description
Rhino is an open-source implementation of JavaScript written entirely
in Java. It is typically embedded into Java applications to provide
scripting to end users.

%package demo
Summary:        Examples for %{name}
Group:          Development/Libraries/Java

%description demo
Examples for %{name}

%prep
%setup -q -n %{name}-Rhino%{scm_version}_RELEASE
%patch0 -b .build
%patch1 -b .fixManifest
cp %{SOURCE1} pom.xml
%pom_remove_parent

# Fix manifest
sed -i -e '/^Class-Path:.*$/d' src/manifest

# Add jpp release info to version
sed -i -e 's|^implementation.version: Rhino .* release .* \${implementation.date}|implementation.version: Rhino %{version} release %{release} \${implementation.date}|' build.properties

%build
%{ant} \
    -Dtarget-jvm=6 -Dsource-level=6 \
    deepclean jar copy-all

pushd examples

export CLASSPATH=../build/%{name}%{version}/js.jar
SOURCEPATH=../build/%{name}%{version}/src
%javac -sourcepath ${SOURCEPATH} -source 6 -target 6 *.java
%jar cvf ../build/%{name}%{version}/%{name}-examples.jar *.class

popd

%install

# man page
mkdir -p %{buildroot}%{_mandir}/man1/
install -m 644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

# jars
mkdir -p %{buildroot}%{_javadir}
cp -a build/%{name}%{version}/js.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}.jar %{buildroot}%{_javadir}/js.jar

# pom
mkdir -p %{buildroot}%{_mavenpomdir}
cp -a pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a "rhino:js"

# scripts
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}
install -m 0755 %{SOURCE3} %{buildroot}%{_bindir}/%{name}-debugger
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/%{name}-idswitch
install -m 0755 %{SOURCE5} %{buildroot}%{_bindir}/%{name}-jsc

# examples
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a examples/* %{buildroot}%{_datadir}/%{name}
cp -a build/%{name}%{version}/%{name}-examples.jar %{buildroot}%{_javadir}/%{name}-examples.jar

find %{buildroot}%{_datadir}/%{name} -name '*.build' -delete

%files -f .mfiles
%license LICENSE.txt
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_bindir}/%{name}-debugger
%attr(0755,root,root) %{_bindir}/%{name}-idswitch
%attr(0755,root,root) %{_bindir}/%{name}-jsc
%{_javadir}/js.jar
%{_javadir}/%{name}-examples.jar
%{_mandir}/man1/%{name}.1*

%files demo
%{_datadir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.7.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 19 2020 Joe Schmitt <joschmit@microsoft.com> - 1.7.7.1-1.4
- Remove openSUSE specific macro %%ext_man.
- Upgrade to latest version of supported jline.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.7.7.1-1.3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Jul 29 2020 Pedro Monreal Gonzalez <pmonreal@suse.com>
- Update to 1.7.7.1:
  * Release notes:
    https://github.com/mozilla/rhino/blob/master/RELEASE-NOTES.md#rhino-1771
- Rebase patches:
  * rhino-addOrbitManifest.patch
  * rhino-build.patch
- Remove pathes:
  * rhino-1.7R3-crosslink.patch
  * rhino-288467.patch
  * rhino-1.7-gcj.patch
* Sat Mar  2 2019 Fridrich Strba <fstrba@suse.com>
- Build against jline1, a compatibility package
* Tue Feb 12 2019 Fridrich Strba <fstrba@suse.com>
- Do not buildrequire jline, since it is only runtime dependency
- Do not run ant with -v and -d options during the product build
* Sun Nov 18 2018 Fridrich Strba <fstrba@suse.com>
- Actually use the rhino-js.pom file in the source package.
- Add "org.mozilla:rhino" alias, since the later 1.7.x versions
  are distributed as such
* Tue Oct  3 2017 fstrba@suse.com
- Don't require java-1_5_0-gcj-compat-devel, since it is bound to
  go
- Require java-devel >= 1.6
- Specify java source and target level 6 to allow buiding with jdk9
* Fri Sep 15 2017 fstrba@suse.com
- Make build with the new version of java-1_5_0-gcj-compat, where
  javac is not just a simple link to gcj, but a wrapper script that
  runs Eclipse Compiler for Java(tm)
- Make buildable with different versions of OpenJDK
* Fri Jun  9 2017 tchvatal@suse.com
- Drop maven depmap so we can actually bootstrap
* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
- spec cleaned using spec-cleaner
* Fri Feb 10 2017 dimstar@opensuse.org
- Revert back to using gcj: it is going to stay around for a while
  longer and it helps avoiding bootstrap cycles.
* Thu Jan  5 2017 tchvatal@suse.com
- Build with java not gcj as it gets deprecated
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Aug 23 2013 mvyskocil@suse.com
- disable javadoc build
- use add_maven_depmap from new javapackages-tools
- workaround xbean.jar definition problem
* Mon Jan  7 2013 mvyskocil@suse.com
- remove xerces-j2-bootstrap depenency (bnc#789163)
* Mon Jun 18 2012 mvyskocil@suse.cz
- ignore jdk7 as well
* Tue Jan 17 2012 cfarrell@suse.com
- license update: MPL-1.1 or GPL-2.0+
  the code is dual licensed under a choice of MPL-1.1 or GPL-2.0+
* Mon Jan 16 2012 mvyskocil@suse.cz
- update to rhino 1_7R3 (bugfix release)
- fix bnc#739502 - rhino-dojo.patch adds Sun proprietary code to rhino 1.7
* Thu Dec 15 2011 coolo@suse.com
- fix license to be in spdx.org format
* Mon Mar 14 2011 mvyskocil@suse.cz
- ignore openjdk for build
* Mon Nov  8 2010 mvyskocil@suse.cz
- build ignore xml-commons-jaxp-1.3-apis
* Thu Sep  2 2010 mvyskocil@suse.cz
- ignore antlr(-java) to reduce build cycles
* Wed Nov 18 2009 mvyskocil@suse.cz
- fixed bnc#554532 - rhino does not work at all
  * Update to 1_7R2, return back the examples
  * merged with rhino-1.7-1.r2.8.jpp6.src.rpm
* Thu Nov 13 2008 mvyskocil@suse.cz
- fixed bnc#444259 - rhino contains conflicting class in rhino-examples.jar
  - don't build and install a rhino-examples.jar
* Thu Oct 16 2008 mvyskocil@suse.cz
- Use xerces-j2-bootstrap to prevent another build cycle
- Added a xerces-j2 and non-bootstrap xml-commons* packages to BuildIgnore
* Wed Oct  1 2008 adrian@suse.de
- Use xmlbeans-mini, instead of xmlbeans in BuildRequires to
  get rid of all the new build cycles
* Mon Sep  8 2008 mvyskocil@suse.cz
- Removed a src.zip - contains a non-free source codes.
* Fri Sep  5 2008 mvyskocil@suse.cz
- Fixed a build with gcj (to prevent of a build cycles with build of openjdk6)
* Fri Sep  5 2008 mvyskocil@suse.cz
- Update to 1.7 (from jpackage 1.7, due some license issues in source tarball )
- Add a doc from Mozilla's CVS
- Removed a patches:
  - rhino-dojo patch contains part with permissive licnse
  - rhino-build patch is not necessary for java 5+
* Tue Sep  2 2008 mvyskocil@suse.cz
- Initial packaging of rhino 1.6 (based on Jpackage 1.7)
