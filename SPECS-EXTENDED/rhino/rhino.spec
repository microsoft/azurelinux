%global debug_package %{nil}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package rhino
#
# Copyright (c) 2025 SUSE LLC and contributors
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


%define scm_version 1_7_15_1
Name:           rhino
Version:        1.7.15.1
Release:        1%{?dist}
Summary:        JavaScript for Java
License:        MPL-2.0
Group:          Development/Libraries/Java
URL:            https://www.mozilla.org/rhino/
Source0:        https://github.com/mozilla/rhino/archive/Rhino%{scm_version}_Release.tar.gz
Source1:        https://repo1.maven.org/maven2/org/mozilla/rhino/%{version}/rhino-%{version}.pom
Source2:        https://repo1.maven.org/maven2/org/mozilla/rhino-engine/%{version}/rhino-engine-%{version}.pom
Source3:        https://repo1.maven.org/maven2/org/mozilla/rhino-runtime/%{version}/rhino-runtime-%{version}.pom
Source10:       %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
Requires:       javapackages-tools

%description
Rhino is an open-source implementation of JavaScript written entirely
in Java. It is typically embedded into Java applications to provide
scripting to end users.

%package engine
Summary:        Rhino Engine
Requires:       %{name} = %{version}

%description engine
Rhino Javascript JSR-223 Script Engine wrapper.

%package runtime
Summary:        Rhino Runtime

%description runtime
Rhino JavaScript runtime jar, excludes tools & JSR-223 Script Engine wrapper.

%package demo
Summary:        Examples for %{name}
Group:          Development/Libraries/Java

%description demo
Examples for %{name}

%prep
%setup -q -n %{name}-Rhino%{scm_version}_Release
cp %{SOURCE10} build.xml

%build
%{ant} jar

pushd examples

export CLASSPATH=../target/%{name}-%{version}.jar
SOURCEPATH=../src
javac -sourcepath ${SOURCEPATH} -source 8 -target 8 *.java
jar --create --verbose \
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 17}%{!?pkg_vcmp:0}
    --date="$(date -u -d @${SOURCE_DATE_EPOCH:-$(date +%%s)} +%%Y-%%m-%%dT%%H:%%M:%%SZ)" \
%endif
    --file=../target/%{name}-examples-%{version}.jar *.class

popd

%install

# jars
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}.jar %{buildroot}%{_javadir}/js.jar
install -pm 0644 target/%{name}-engine-%{version}.jar %{buildroot}%{_javadir}/%{name}-engine.jar
install -pm 0644 target/%{name}-runtime-%{version}.jar %{buildroot}%{_javadir}/%{name}-runtime.jar

# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
cp -a %{SOURCE1} %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a "rhino:js"
cp -a %{SOURCE2} %{buildroot}%{_mavenpomdir}/%{name}-engine.pom
%add_maven_depmap %{name}-engine.pom %{name}-engine.jar -f engine
cp -a %{SOURCE3} %{buildroot}%{_mavenpomdir}/%{name}-runtime.pom
%add_maven_depmap %{name}-runtime.pom %{name}-runtime.jar -f runtime

# scripts
%jpackage_script org.mozilla.javascript.tools.shell.Main "" "" rhino rhino true
%jpackage_script org.mozilla.javascript.tools.debugger.Main "" "" rhino rhino-debugger true
%jpackage_script org.mozilla.javascript.tools.jsc.Main "" "" rhino rhino-jsc true

# examples
install -dm 0755 %{buildroot}%{_datadir}/%{name}
cp -a examples/* %{buildroot}%{_datadir}/%{name}
install -pm 0644 target/%{name}-examples-%{version}.jar %{buildroot}%{_javadir}/%{name}-examples.jar
%fdupes -s %{buildroot}%{_datadir}/%{name}

%files -f .mfiles
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_bindir}/%{name}-debugger
%attr(0755,root,root) %{_bindir}/%{name}-jsc
%{_javadir}/js.jar
%{_javadir}/%{name}-examples.jar
%license LICENSE.txt NOTICE.txt NOTICE-tools.txt
%doc README.md CODE_OF_CONDUCT.md RELEASE-NOTES.md

%files engine -f .mfiles-engine
%license LICENSE.txt
%doc README.md CODE_OF_CONDUCT.md RELEASE-NOTES.md

%files runtime -f .mfiles-runtime
%license LICENSE.txt NOTICE.txt
%doc README.md CODE_OF_CONDUCT.md RELEASE-NOTES.md

%files demo
%{_datadir}/%{name}

%changelog
* Tue Dec 23 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.7.15.1-1
- Upgrade to version 1.7.15.1
- License Verified.

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
