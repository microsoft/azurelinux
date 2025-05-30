# Based on https://src.fedoraproject.org/rpms/guava/tree/main

Summary:        Google Core Libraries for Java
Name:           guava
Version:        33.0.0
Release:        1%{?dist}
License:        Apache-2.0 AND CC0-1.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://github.com/google/guava
Source0:        https://github.com/google/guava/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-build.tar.xz
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
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
%setup -q

find . -name '*.jar' -delete

%pom_remove_parent guava-bom

%pom_disable_module guava-gwt
%pom_disable_module guava-tests

# Starting guava v27.0 failureaccess module became a seperate runtime depedency due to android limitations.
# We are going to artificially bake it with guava https://github.com/google/guava/wiki/UseGuavaInYourBuild#what-about-guavas-own-dependencies
%pom_xpath_inject pom:modules "<module>futures/failureaccess</module>"
%pom_xpath_inject pom:parent "<relativePath>../..</relativePath>" futures/failureaccess
%pom_xpath_set pom:parent/pom:version %{version}-jre futures/failureaccess

%pom_remove_plugin -r :animal-sniffer-maven-plugin
# Downloads JDK source for doc generation
%pom_remove_plugin :maven-dependency-plugin guava

%pom_remove_dep :caliper guava-tests

%mvn_package :guava-parent guava
 
# javadoc generation fails due to strict doclint in JDK 1.8.0_45
%pom_remove_plugin -r :maven-javadoc-plugin
 
%pom_remove_plugin -r :build-helper-maven-plugin
 
%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml
 
# Remove error_prone_core artifact
%pom_xpath_remove pom:annotationProcessorPaths

# Clean annotation dependencies. These depdencies are only used for 
# code quality. These modules are not present in mariner (and are not needed)
%pom_remove_dep -r :error_prone_annotations
%pom_xpath_remove  "//*[local-name()='arg'][contains(., '-Xplugin:ErrorProne')]"
%pom_remove_dep -r :j2objc-annotations
%pom_remove_dep -r org.checkerframework:

# Clean annotation usage from code
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

find -type f -name "*.java" -print0 | while IFS= read -r -d '' file; do
    if [ -r "$file" ]; then
        # Remove the imports
        sed -i -r "s/^import .*\.($annotations);//" "$file"
        # Removes multi line (with nested parentheses)
        sed -i -E ':a;N;$!ba;s/@('"$annotations"')\([^()]*(\([^()]*\)[^()]*)*\)//g' "$file"
        sed -i -E ':a;N;$!ba;s/@(com\.google\.errorprone\.annotations\.('"$annotations"'))\([^()]*(\([^()]*\)[^()]*)*\)//g' "$file"
        # Remove single line (with nested parentheses)
        sed -i -E "s/@($annotations)\([^()]*(\([^()]*\)[^()]*)*\)//g" "$file"
        sed -i -E 's/@(com\.google\.errorprone\.annotations\.('"$annotations"'))\([^()]*(\([^()]*\)[^()]*)*\)//g' "$file"
        # Remove inline or no parantheses
        sed -i -E "s/@($annotations)//g" "$file"
        sed -i -E "s/@(com\.google\.errorprone\.annotations\.($annotations))//g" "$file"
    else
        echo "Error: Cannot read file $file"
    fi
done

%pom_remove_dep -r :listenablefuture # Android specific
%pom_remove_dep jdk:srczip guava # Reference/IDE specific

%mvn_package "com.google.guava:failureaccess" guava

%mvn_package "com.google.guava:guava-bom" __noinstall

%build
# Tests fail on Koji due to insufficient memory,
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332971
%mvn_build -s -f
 
%install
%mvn_install

%files -f .mfiles-guava
%doc CONTRIBUTORS README*
%license LICENSE

%files javadoc
%{_javadocdir}/%{name}
%doc CONTRIBUTORS README*
%license LICENSE

%files testlib -f .mfiles-guava-testlib

%changelog
* Mon Feb 05 2024 Karim Eldegwy <karimeldegwy@microsoft.com> - 33.0.0-1
- Auto-upgrade to 33.0.0 - 3.0
- Move from ant to mvn, using Fedora's spec file instead of OpenSUSE

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
