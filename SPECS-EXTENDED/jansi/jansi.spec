%bcond_with bootstrap

Name:             jansi
Version:          2.4.1
Release:          4%{?dist}
Summary:          Generate and interpret ANSI escape sequences in Java
License:          Apache-2.0
URL:              http://fusesource.github.io/jansi/
ExclusiveArch:    %{java_arches}

# ./generate-tarball.sh
Source0:          %{name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:          generate-tarball.sh

# Change the location of the native artifact to where Fedora wants it
Patch0:           %{name}-jni.patch

BuildRequires:    gcc
%if %{with bootstrap}
BuildRequires:    javapackages-bootstrap
%else
BuildRequires:    maven-local
BuildRequires:    mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:    mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:    mvn(org.fusesource:fusesource-pom:pom:)
BuildRequires:    mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:    mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:    mvn(org.moditect:moditect-maven-plugin)
%endif

%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%package javadoc
BuildArch:        noarch
Summary:          Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -n jansi-jansi-%{version} -p1

# We don't need the Fuse JXR skin
%pom_xpath_remove "pom:build/pom:extensions"

# Plugins not needed for an RPM build
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :spotless-maven-plugin

# We don't want GraalVM support in Fedora
%pom_remove_plugin :exec-maven-plugin
%pom_remove_dep :picocli-codegen

# Set the JNI path
sed -i 's,@LIBDIR@,%{_prefix}/lib,' \
    src/main/java/org/fusesource/jansi/internal/JansiLoader.java

%build
%set_build_flags
CC="${CC:-gcc}"
# Build the native artifact
CFLAGS="$CFLAGS -I. -I%{java_home}/include -I%{java_home}/include/linux -fPIC -fvisibility=hidden"
cd src/main/native
$CC $CFLAGS -c jansi.c
$CC $CFLAGS -c jansi_isatty.c
$CC $CFLAGS -c jansi_structs.c
$CC $CFLAGS -c jansi_ttyname.c
$CC $CFLAGS $LDFLAGS -shared -o libjansi.so *.o -lutil
cd -

# Build the Java artifacts
%mvn_build -- -Dlibrary.jansi.path=$PWD/src/main/native

%install
# Install the native artifact
mkdir -p %{buildroot}%{_prefix}/lib/%{name}
cp -p src/main/native/libjansi.so %{buildroot}%{_prefix}/lib/%{name}

# Install the Java artifacts
%mvn_install

%files -f .mfiles
%license license.txt
%doc readme.md changelog.md
%{_prefix}/lib/%{name}/

%files javadoc -f .mfiles-javadoc
%license license.txt

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.4.1-3
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 2.4.1-2
- bump of release for for java-21-openjdk as system jdk

* Thu Feb 01 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.1-1
- Update to upstream version 2.4.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-10
- Rebuild to regenerate auto-Requires on java

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-9
- Convert License tag to SPDX format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-5
- Ensure CC env variable is set during build

* Thu Jul 14 2022 Marian Koncek <mkoncek@redhat.com> - 2.4.0-4
- Make javadoc subpackage noarch

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.4.0-3
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 01 2021 Marian Koncek <mkoncek@redhat.com> - 2.4.0-1
- Update to upstream version 2.4.0

* Fri Sep 24 2021 Marian Koncek <mkoncek@redhat.com> - 2.3.3-3
- Install native artifact into a fixed location
- Related: rhbz#1994935

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Jerry James <loganjerry@gmail.com> - 2.3.3-1
- Version 2.3.3

* Fri Jun 18 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-5
- Clean tarball from content with questionable licensing
- Resolves: rhbz#1973738

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-4
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Timm Bäder <tbaeder@redhat.com> - 2.1.1-2
- Use standard variables when compiling native artifact

* Tue Dec 15 2020 Jerry James <loganjerry@gmail.com> - 2.1.1-1
- Version 2.1.1
- Remove package name from Summary
- Add patch to change the location of the JNI shared object

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.18-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 08 2019 Fabio Valentini <decathorpe@gmail.com> - 1.18-1
- Update to version 1.18.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 05 2018 Michael Simacek <msimacek@redhat.com> - 1.17.1-1
- Update to upstream version 1.17.1

* Mon Feb 26 2018 Michael Simacek <msimacek@redhat.com> - 1.17-1
- Update to upstream version 1.17

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Michael Simacek <msimacek@redhat.com> - 1.16-1
- Update to upstream version 1.16

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Michael Simacek <msimacek@redhat.com> - 1.11-11
- Remove BR on maven-site-plugin

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8
- Remove maven-javadoc-plugin execution

* Tue Jan 27 2015 Mat Booth <mat.booth@redhat.com> - 1.11-7
- Add/remove BRs to fix FTBFS bug

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-5
- Migrate BuildRequires from junit4 to junit

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-4
- Remove BuildRequires on maven-surefire-provider-junit4

* Wed Sep 11 2013 Marek Goldmann <mgoldman@redhat.com> - 1.11-3
- Using xmvn
- Remove the jboss-native deps with classifiers

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Marek Goldmann <mgoldman@redhat.com> - 1.11-1
- Upstream release 1.11 RHBZ#962761
- CVE-2013-2035 HawtJNI: predictable temporary file name leading to local arbitrary code execution RHBZ#962614

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.9-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Oct 09 2012 Marek Goldmann <mgoldman@redhat.com> - 1.9-1
- Upstream release 1.9, RHBZ#864490

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 04 2012 Tomas Radej <tradej@redhat.com> - 1.6-3
- Removed maven-license-plugin BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Marek Goldmann <mgoldman@redhat.com> 1.6-1
- Upstream release 1.6
- Spec file cleanup

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.5-1
- Initial packaging

