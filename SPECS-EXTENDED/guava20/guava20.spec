Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package guava20
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


%global guava_compat_version 20.0,19.0,18.0,17.0,16.0.1,16.0,15.0,14.0.1,14.0,13.0.1,13.0,12.0.1,12.0,11.0.2,11.0.1,11.0,10.0.1,10.0
%global guava_alias com.google.collections:google-collections,com.google.guava:guava-jdk5
Name:           guava20
Version:        20.0
Release:        5%{?dist}
Summary:        Google Core Libraries for Java
# Most of the code is under ASL 2.0
# Few classes are under CC0, grep for creativecommons
License:        Apache-2.0 AND CC0-1.0
Group:          Development/Libraries/Java
URL:            https://github.com/google/guava
Source0:        https://github.com/google/guava/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        osgi-manifest.txt
Patch0:         0001-Avoid-presizing-arrays.patch
Patch1:         guava20-java8compat.patch
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsr-305
BuildRequires:  junit
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
Requires:       %{name} = %{version}
Requires:       jsr-305
Requires:       junit

%description testlib
guava-testlib provides additional functionality for conveninent unit testing

%prep
%setup -q -n guava-%{version}
cat %{SOURCE1} | sed 's#@BNDVRSN@#%{version}.0#g' >manifest.txt

%patch0 -p1
%patch1 -p1

find . -name '*.jar' -delete

%pom_disable_module guava-gwt
%pom_remove_plugin -r :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_dep jdk:srczip guava
%pom_remove_dep :caliper guava-tests

# javadoc generation fails due to strict doclint in JDK 1.8.0_45
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml

%pom_remove_dep -r :animal-sniffer-annotations
%pom_remove_dep -r :error_prone_annotations
%pom_remove_dep -r :j2objc-annotations

annotations=$(
    grep -F -hr -e com.google.j2objc.annotations \
        -e com.google.errorprone.annotation -e org.codehaus.mojo.animal_sniffer \
    | sort -u \
    | sed 's/.*\.\([^.]*\);/\1/' \
    | paste -sd\|
)
# guava started using quite a few annotation libraries for code quality, which
# we don't have. This ugly regex is supposed to remove their usage from the code
find -name '*.java' | xargs sed -ri \
    "s/^import .*\.($annotations);//;s/@($annotations)"'\>\s*(\((("[^"]*")|([^)]*))\))?//'

for mod in guava  guava-gwt  guava-testlib  guava-tests; do
  %pom_remove_parent ${mod}
  %pom_xpath_inject "pom:project" "
    <groupId>com.google.guava</groupId>
    <version>%{version}</version>" ${mod}
done

%build
mkdir -p guava/build/classes
javac -d guava/build/classes \
  -cp $(build-classpath jsr-305) \
  -source 6 -target 6 -encoding utf8 \
  $(find guava/src/ -name \*.java | xargs)
jar cfm guava/build/guava-%{version}.jar manifest.txt -C guava/build/classes .

mkdir -p guava-testlib/build/classes
javac \
  -d guava-testlib/build/classes \
  -cp $(build-classpath jsr-305 junit):guava/build/classes \
  -source 6 -target 6 -encoding utf8 \
  $(find guava-testlib/src/ -name \*.java | xargs)
jar cf guava-testlib/build/guava-testlib-%{version}.jar -C guava-testlib/build/classes .

mkdir -p build/apidoc
javadoc \
  -d build/apidoc \
  -Xdoclint:none \
  -classpath $(build-classpath jsr-305 junit):guava/build/classes \
  -source 6 -encoding utf8 -notimestamp \
  $(find {guava,guava-testlib}/src/ -name \*.java | xargs)

%install
# jars
install -dm 755 %{buildroot}%{_javadir}/%{name}
install -m 0644 guava/build/guava-%{version}.jar %{buildroot}%{_javadir}/%{name}/guava.jar
install -m 0644 guava-testlib/build/guava-testlib-%{version}.jar %{buildroot}%{_javadir}/%{name}/guava-testlib.jar

# poms
install -dm 755 %{buildroot}%{_mavenpomdir}/%{name}
install -m 0644 guava/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/guava.pom
%add_maven_depmap %{name}/guava.pom %{name}/guava.jar -v %{guava_compat_version} -a %{guava_alias}

install -m 0644 guava-testlib/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/guava-testlib.pom
%add_maven_depmap %{name}/guava-testlib.pom %{name}/guava-testlib.jar -v %{guava_compat_version} -f testlib

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -a build/apidoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc CONTRIBUTORS README*
%license COPYING

%files javadoc
%license COPYING
%{_javadocdir}/%{name}

%files testlib -f .mfiles-testlib

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20.0-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 20.0-4.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Set javadoc Xdoclint:none.

* Mon Mar 23 2020 Fridrich Strba <fstrba@suse.com>
- Add bundle manifest to the guava jar so that it might be usable
  from eclipse
* Fri Oct  4 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to parents from all installed pom files
* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the parent pom, since we are not building using
  Maven.
* Thu Oct 25 2018 Fridrich Strba <fstrba@suse.com>
- Initial packaging of guava20 20.0
