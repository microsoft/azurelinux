#
# spec file for package guava
#
# Copyright (c) 2019 SUSE LLC
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

Summary:        Google Core Libraries for Java
Name:           guava
Version:        25.0
Release:        8%{?dist}
License:        Apache-2.0 AND CC0-1.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://github.com/google/guava
Source0:        https://github.com/google/guava/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-build.tar.xz
Patch0:         %{name}-%{version}-java8compat.patch
Patch1:         CVE-2020-8908.patch
Patch2:         CVE-2023-2976.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsr-305
BuildRequires:  junit
Requires:       mvn(com.google.code.findbugs:jsr305)
Provides:       mvn(com.google.guava:guava) = %{version}-%{release}
BuildArch:      noarch

%description
Guava is a suite of core and expanded libraries that include
utility classes, Google's collections, io classes, and much
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%package testlib
Summary:        The guava-testlib artifact
Group:          Development/Libraries/Java
Requires:       mvn(com.google.code.findbugs:jsr305)
Requires:       mvn(com.google.guava:guava)
Requires:       mvn(junit:junit)

%description testlib
guava-testlib provides additional functionality for conveninent unit testing

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

find . -name '*.jar' -delete

%pom_disable_module guava-gwt
%pom_disable_module guava-tests

%pom_remove_plugin -r :animal-sniffer-maven-plugin
# Downloads JDK source for doc generation
%pom_remove_plugin :maven-dependency-plugin guava

%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml

%pom_remove_dep -r :animal-sniffer-annotations
%pom_remove_dep -r :error_prone_annotations
%pom_remove_dep -r :j2objc-annotations
%pom_remove_dep -r org.checkerframework:

annotations=$(
    find -name '*.java' \
    | xargs grep -F -h \
        -e 'import com.google.j2objc.annotations' \
        -e 'import com.google.errorprone.annotation' \
        -e 'import org.codehaus.mojo.animal_sniffer' \
        -e 'import org.checkerframework' \
    | sort -u \
    | sed 's/.*\.\([^.]*\);/\1/' \
    | paste -sd\|
)
# guava started using quite a few annotation libraries for code quality, which
# we don't have. This ugly regex is supposed to remove their usage from the code
find -name '*.java' | xargs sed -ri \
    "s/^import .*\.($annotations);//;s/@($annotations)"'\>\s*(\((("[^"]*")|([^)]*))\))?//g'

for mod in guava guava-testlib; do
  %pom_remove_parent ${mod}
  %pom_xpath_inject pom:project '
    <groupId>com.google.guava</groupId>
    <version>%{version}</version>' ${mod}
done

%pom_change_dep -r -f ::::: :::::

%build
mkdir -p lib
build-jar-repository -s lib junit jsr-305
%ant -Dtest.skip=true package javadoc

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 %{name}/target/%{name}-%{version}*.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
install -pm 0644 %{name}-testlib/target/%{name}-testlib-%{version}*.jar %{buildroot}%{_javadir}/%{name}/%{name}-testlib.jar

# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 %{name}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar -f %{name}
install -pm 0644 %{name}-testlib/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-testlib.pom
%add_maven_depmap %{name}/%{name}-testlib.pom %{name}/%{name}-testlib.jar -f %{name}-testlib

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -r %{name}/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{name}
cp -r %{name}-testlib/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{name}-testlib
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles-guava
%doc CONTRIBUTORS README*
%license COPYING

%files javadoc
%{_javadocdir}/%{name}
%license COPYING

%files testlib -f .mfiles-guava-testlib

%changelog
* Fri Jun 07 2024 Sindhu Karri <lakarri@microsoft.com> 25.0-8
- Add patch for CVE-2023-2976

* Wed Aug 23 2023 Dallas Delaney <dadelan@microsoft.com> 25.0-7
- Add patch for CVE-2020-8908

* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 25.0-6
- Moved from extended to core
- License verified
- Fixing maven provides

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 25.0-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 25.0-4.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Dec  4 2019 Fridrich Strba <fstrba@suse.com>
- Avoid version-less dependencies that can cause problems with
  some tools

* Fri Nov 22 2019 Fridrich Strba <fstrba@suse.com>
- Build the package with ant in order to prevent build cycles
  * using a generated and customized ant build system

* Thu Oct 10 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * guava-25.0-java8compat.patch
    + Avoid callingoverridden methods with covariant return types
    for java.nio.ByteBuffer and java.nio.CharBuffer, which were
    introduced in Java 9
    + This allows us to produce with Java >= 9 binaries that are
    compatible with Java 8

* Fri Apr 12 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of guava 25.0
