#
# spec file for package junit
#
# Copyright (c) 2020 SUSE LLC
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

Summary:        Java regression test package
Name:           junit
Version:        4.13
Release:        4%{?dist}
License:        EPL-1.0
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.junit.org/
Source0:        https://github.com/junit-team/junit/archive/r%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  hamcrest >= 1.3
BuildRequires:  java-devel >= 1.6
BuildRequires:  javapackages-local-bootstrap
Requires:       mvn(org.hamcrest:hamcrest-core)
Provides:       %{name}-demo = %{version}-%{release}
Obsoletes:      %{name}-demo < %{version}-%{release}
Provides:       %{name}4-demo = %{version}-%{release}
Obsoletes:      %{name}4-demo < %{version}-%{release}
Provides:       %{name}4 = %{version}-%{release}
Obsoletes:      %{name}4 < %{version}-%{release}
BuildArch:      noarch

%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck.
It is used by the developer who implements unit tests in Java.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML
Provides:       %{name}4-javadoc = %{version}-%{release}
Obsoletes:      %{name}4-javadoc < %{version}-%{release}

%description javadoc
Javadoc for %{name}.

%package manual
Summary:        Manual for %{name}
Group:          Documentation/Other
Provides:       %{name}4-manual = %{version}-%{release}
Obsoletes:      %{name}4-manual < %{version}-%{release}

%description manual
Documentation for %{name}.

%prep
%setup -q -n %{name}4-r%{version}
cp %{SOURCE1} .

find . -type f -name "*.jar" -or -name "*.class" | xargs -t rm -rf

ln -s $(build-classpath hamcrest/all) lib/hamcrest-core-1.3.jar

%build
export CLASSPATH=$(build-classpath hamcrest/all)
ant jars javadoc -Dversion-status=

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{name}%{version}/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# compat symlink
ln -sf %{_javadir}/%{name}.jar %{buildroot}%{_javadir}/%{name}4.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr %{name}%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%check
cat > test.java <<EOF
import org.junit.Assert;
class test {

    public static void main(String[] args) {
        Assert.fail("Hello world from junit");
    }

}
EOF
javac -cp %{buildroot}/%{_javadir}/%{name}.jar test.java
java -cp %{buildroot}/%{_javadir}/%{name}.jar: test 2>&1 | \
   grep 'Exception in thread "main" java.lang.AssertionError: Hello world from junit'

%files -f .mfiles
%license LICENSE-junit.txt
%doc CODING_STYLE.txt README.md acknowledgements.txt
%{_javadir}/%{name}4.jar

%files javadoc
%license LICENSE-junit.txt
%{_javadocdir}/%{name}

%files manual
%license LICENSE-junit.txt
%doc doc/*

%changelog
* Fri Apr 01 2022 Henry Li <lihl@microsoft.com> - 4.13-4
- Remove target to upload docs to sourceforge from build.xml

* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 4.13-3
- Move to SPECS
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.13-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.13-1.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Apr  7 2020 Fridrich Strba <fstrba@suse.com>
- Upgrade to 4.13
- Removed patches:
  * junit-jdk10.patch
  * junit-jdk11.patch
    + not needed with this version
* Mon Feb  4 2019 Fridrich Strba <fstrba@suse.com>
- Add OSGi manifest to the jar file
- Package the manual
- BuildRequire and Require hamcrest-core, since the package does
  strictly depend on hamcrest-core only.
* Mon Jan 21 2019 Jan Engelhardt <jengelh@inai.de>
- Trim repeated metadata from description.
* Wed Dec 26 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to 4.12
- Removed patches:
  * junit-jdk8.patch
  * junit-jdk9.patch
  * junit-no-hamcrest-src.patch
    + Integrated directly in the added build.xml file
* Wed Jul 11 2018 fstrba@suse.com
- Added patch:
  * junit-jdk11.patch
    + Fix build with jdk11
    + Don't override removed SecurityManager methods
* Mon Dec 18 2017 fstrba@suse.com
- Run fdupes on documentation
* Mon Dec 18 2017 dimstar@opensuse.org
- Harden and fix the test suite:
  + org.framework.junit is deprecated since junit 4.0
  + Ensure we fail check when junit no longer returns what we
    expect it to (error code checking is useless, since Assert
    returns !0, like any other failure to start the test).
* Mon Dec 18 2017 fstrba@suse.com
- Added patch:
  * junit-jdk10.patch
    + Remove a function getInCheck from NoExitSecurityManager,
    since it does not exist in the extended class in jdk10 and is
    deprecated in previous versions
* Fri Sep  8 2017 fstrba@suse.com
- Added patch:
  * junit-jdk9.patch
    + Build with java source and target levels 1.6 in order to
    allow building with jdk9
* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
* Tue Jul 28 2015 tchvatal@suse.com
- Add patch to build with jdk8:
  * junit-jdk8.patch
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Oct 25 2013 mvyskocil@suse.com
- Update to 4.11
  * Matchers: Upgrade to Hamcrest 1.3
    no longer included junit jar
  * Parameterized Tests
  * Specify Test execution order
  * New maven artifact 'junit:junit' w/o builtin hamcrest
  * Number of improvements into Rules
- Drop jdk7-testfailure.patch, fixed upstream
- Add junit-no-hamcrest-src.patch, don't bundle hamcrest into junit.jar
- Use SourceUrl for release tarball and pom
- Don't inject OSGI manifest, it breaks junit.jar
- Provide/obsolete package junit4
* Fri Aug 23 2013 mvyskocil@suse.com
- disable javadoc build
* Thu Sep 11 2008 mvyskocil@suse.cz
- Use gcc-java for build
- Update 3.8.2 (a new build.xml)
- Removed a java14compat
- Removed javadoc postin/postun
- Add a cpl-v10.html
* Thu Mar 29 2007 ro@suse.de
- added unzip to buildreq
* Tue Sep 26 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jul 28 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 3.8.1 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 3.8.1 (JPackage 1.5)
