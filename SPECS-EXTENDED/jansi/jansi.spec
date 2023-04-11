Summary:        Java library for generating and interpreting ANSI escape sequences
Name:           jansi
Version:        2.4.0
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://fusesource.github.io/jansi/
Source0:        https://github.com/fusesource/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
Patch0:         %{name}-jni.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  javapackages-local-bootstrap

%description
Jansi is a java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it, like Windows, and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}
cp %{SOURCE1} build.xml

%pom_remove_parent

# We don't need the Fuse JXR skin
%pom_xpath_remove "pom:build/pom:extensions"

# Plugins not needed for an RPM build
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :nexus-staging-maven-plugin

# We don't want GraalVM support in Fedora
%pom_remove_plugin :exec-maven-plugin
%pom_remove_dep :picocli-codegen

# Build for JDK 1.8 at a minimum
%pom_xpath_set "//pom:properties/pom:jdkTarget" 1.8

# Remove prebuilt shared objects
rm -fr src/main/resources/org/fusesource/jansi/internal

# Unbundle the JNI headers
rm src/main/native/inc_linux/*.h
ln -s %{java_home}/include/jni.h src/main/native/inc_linux
ln -s %{java_home}/include/linux/jni_md.h src/main/native/inc_linux

# Set the JNI path
sed -i 's,@LIBDIR@,%{_libdir},' \
    src/main/java/org/fusesource/jansi/internal/JansiLoader.java
# Filtering complicated with ant
sed -i 's,\${project.version},%{version},' \
    src/main/resources/org/fusesource/jansi/jansi.properties

%build
%set_build_flags
CC="${CC:-gcc}"
# Build the native artifact
CFLAGS="$CFLAGS -I. -I%{java_home}/include -I%{java_home}/include/linux -fPIC -fvisibility=hidden"
pushd src/main/native
$CC $CFLAGS -c jansi.c
$CC $CFLAGS -c jansi_isatty.c
$CC $CFLAGS -c jansi_structs.c
$CC $CFLAGS -c jansi_ttyname.c
$CC $CFLAGS $LDFLAGS -shared -o libjansi.so *.o -lutil
popd

# Build the Java artifacts
%{ant} jar javadoc

%install
# Install the native artifact
install -dm 0755 %{buildroot}%{_libdir}/%{name}
install -pm 0755 src/main/native/libjansi.so %{buildroot}%{_libdir}/%{name}

# jar
install -dm 0755 %{buildroot}%{_jnidir}/%{name}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_jnidir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
%fdupes -s %{buildroot}%{_javadocdir}
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license license.txt
%doc readme.md changelog.md
%{_libdir}/%{name}

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Tue Jan 17 2023 Sumedh Sharma <sumsharma@microsoft.com> - 2.4.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Converting the 'Release' tag to the '[number].[distribution]' format.
- License verified

* Mon May 16 2022 Fridrich Strba <fstrba@suse.com>
- Upgrade the latest upstream release 2.4.0
  Integrates jansi-native libraries
  Does not depend on jansi-native and hawtjni-runtime
- Make the jansi package archful since it installs a native
  library and jni jar
- Added patch:
  jansi-jni.patch Give a possibility to load the native libjansi.so from
  system

* Wed Mar 23 2022 Fridrich Strba <fstrba@suse.com>
- Build with java source and target levels 8

* Thu Jun 27 2019 Fridrich Strba <fstrba@suse.com>
- Remove the reference to jansi-project parent from jansi pom
- Resolve manually jansi-native-version variable so that ivy
  understands it

* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using Maven.
- Make tests conditional and switched off by default

* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Fix double-shipping of documentation
- Avoid name repetition in summary (potential rpmlint warning

* Mon Feb  4 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of jansi 1.17.1
- Add build.xml file for building with ant
