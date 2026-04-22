## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 11;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OTHER LANGUAGE RUNTIMES:
# - A PHP runtime is available as a separate project:
#   https://github.com/antlr/antlr-php-runtime/
# - A dart target is available, should dart ever be added to Fedora.
# - A C# target is available.  It can be built into a DLL successfully with the
#   dotnet package, but we don't seem to be able to create a nupkg with the
#   current tooling, nor is there a well-defined place where a nupkg should be
#   installed.

%global giturl      https://github.com/antlr/antlr4
%global swiftarches x86_64 aarch64
%global swiftdir    %{_prefix}/lib/swift/linux

%ifarch %{swiftarches}
%bcond swift %{undefined rhel}
%else
%bcond swift 0
%endif

Name:           antlr4-project
Version:        4.13.2
Release:        %autorelease
Summary:        Parser generator (ANother Tool for Language Recognition)

License:        BSD-3-Clause
URL:            https://www.antlr.org/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}/antlr4-%{version}.tar.gz
# Fix some javadoc problems
# https://github.com/antlr/antlr4/pull/2960
Patch:          antlr4-javadoc.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  help2man
BuildRequires:  make
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires:  mvn(com.ibm.icu:icu4j)
BuildRequires:  mvn(com.webguys:string-template-maven-plugin)
BuildRequires:  mvn(jakarta.json:jakarta.json-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.abego.treelayout:org.abego.treelayout.core)
BuildRequires:  mvn(org.antlr:ST4)
BuildRequires:  mvn(org.antlr:antlr-runtime)
BuildRequires:  mvn(org.antlr:antlr3-maven-plugin)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
BuildRequires:  mvn(org.twdata.maven:mojo-executor)
BuildRequires:  python3-devel
BuildRequires:  utf8cpp-devel

# https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs
ExclusiveArch:  %{java_arches}

# Subpackages removed in 4.10.  This can be removed when F40 reaches EOL.
Obsoletes:      antlr4-runtime-test-annotations < 4.10
Obsoletes:      antlr4-runtime-test-annotation-processors < 4.10

%global _desc %{expand:
ANTLR (ANother Tool for Language Recognition) is a powerful parser
generator for reading, processing, executing, or translating structured
text or binary files.  It is widely used to build languages, tools, and
frameworks.  From a grammar, ANTLR generates a parser that can build
and walk parse trees.}

%description %_desc

%package     -n antlr4-runtime
Summary:        ANTLR runtime
BuildArch:      noarch

%description -n antlr4-runtime %_desc

This package provides the runtime library used by Java ANTLR parsers.

%package     -n antlr4
Summary:        Parser generator (ANother Tool for Language Recognition)
BuildArch:      noarch
Requires:       antlr4-runtime = %{version}-%{release}
Requires:       java-25-headless
Requires:       javapackages-tools

%description -n antlr4 %_desc

This package provides the ANTLR parser generator.

%package     -n antlr4-javadoc
Summary:        API Documentation for antlr4
BuildArch:      noarch

%description -n antlr4-javadoc %_desc

This package contains API documentation for antlr4.

%package     -n antlr4-maven-plugin
Summary:        ANTLR plugin for Apache Maven
BuildArch:      noarch
Requires:       antlr4 = %{version}-%{release}

%description -n antlr4-maven-plugin %_desc

This package provides a plugin for Apache Maven which can be used to
generate ANTLR parsers during project build.

%package     -n antlr4-doc
Summary:        ANTLR4 documentation
BuildArch:      noarch

%description -n antlr4-doc %_desc

This package contains ANTLR4 documentation.

%package     -n antlr4-cpp-runtime
Summary:        ANTLR runtime for C++

%description -n antlr4-cpp-runtime %_desc

This package provides the runtime library used by C++ ANTLR parsers.

%package     -n antlr4-cpp-runtime-devel
Summary:        Header files for programs that use C++ ANTLR parsers
Requires:       antlr4-cpp-runtime%{?_isa} = %{version}-%{release}

%description -n antlr4-cpp-runtime-devel %_desc

This package provides header files for programs that use C++ ANTLR
parsers.

%ifarch %go_arches
%global goipath github.com/antlr4-go/antlr

%package     -n golang-github-antlr4-antlr-devel
Summary:        ANTLR runtime for Go
BuildArch:      noarch
BuildRequires:  go-rpm-macros

# This can be removed when F44 reaches EOL
Obsoletes:      golang-antlr4-runtime-devel < 4.13
Provides:       golang-antlr4-runtime-devel = %{version}-%{release}

%description -n golang-github-antlr4-antlr-devel %_desc

This package provides the runtime library used by Go ANTLR parsers.
%endif

%ifarch %nodejs_arches
%package     -n nodejs-antlr4
# The entire project is BSD-3-Clause.
# codepointat.js and fromcodepoint.js are MIT.
License:        BSD-3-Clause AND MIT
Summary:        ANTLR runtime for JavaScript
BuildArch:      noarch
BuildRequires:  nodejs
BuildRequires:  nodejs-packaging
Requires:       nodejs

%description -n nodejs-antlr4 %_desc

This package provides the runtime library used by JavaScript ANTLR
parsers.
%endif

%package     -n python3-antlr4-runtime
Summary:        ANTLR runtime for Python 3
BuildArch:      noarch

%description -n python3-antlr4-runtime %_desc

This package provides the runtime library used by Python 3 ANTLR parsers.

%if %{with swift}
%package     -n swift-antlr4-runtime
Summary:        ANTLR runtime for swift
BuildRequires:  chrpath
BuildRequires:  swift-lang

%description -n swift-antlr4-runtime %_desc

This package provides the runtime library used by swift ANTLR parsers.
%endif

%prep
%autosetup -n antlr4-%{version} -p1

%conf
find -name \*.jar -delete

# sonatype-oss-parent is deprecated in Fedora
%pom_remove_parent

# Xmvn javadoc mojo is in use
%pom_remove_plugin -r :maven-javadoc-plugin

# Missing test deps: org.seleniumhq.selenium:selenium-java
%pom_disable_module runtime-testsuite
%pom_disable_module tool-testsuite

# Missing test dep:
# io.takari.maven.plugins:takari-plugin-testing
%pom_remove_dep -r :takari-plugin-testing

# Adapt to jakarta-json 2.x
%pom_change_dep org.glassfish:javax.json jakarta.json:jakarta.json-api runtime-testsuite

# Missing plugins
# io.takari.maven.plugins:takari-lifecycle-plugin
%pom_remove_plugin -r :takari-lifecycle-plugin
# us.bryon:graphviz-maven-plugin
%pom_remove_plugin :graphviz-maven-plugin runtime/Java

# Don't bundle dependencies
%pom_remove_plugin :maven-shade-plugin tool

%mvn_package :antlr4-master antlr4-runtime

# Use utf8cpp instead of the deprecated wstring_convert
sed -i 's/# \(.*DUSE_UTF8_INSTEAD_OF_CODECVT.*\)/\1/' runtime/Cpp/CMakeLists.txt

%generate_buildrequires
cd runtime/Python3
%pyproject_buildrequires

%build
export JAVA_HOME=%{_jvmdir}/java

# Build for Java
# Due to the missing takari packages, we cannot run the tests
%mvn_build -s -f -- -Dsource=1.8

# Build the C++ runtime
# Disable building tests, because that tries to download googletest from github
cd runtime/Cpp
%cmake \
  -DANTLR_BUILD_CPP_TESTS:BOOL=OFF \
  -DANTLR_BUILD_SHARED:BOOL=ON \
  -DANTLR_BUILD_STATIC:BOOL=OFF \
  -DANTLR4_INSTALL:BOOL=ON \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build
cd -

# Build the Python 3 runtime
cd runtime/Python3
%pyproject_wheel
cd -

%if %{with swift}
# Build the Swift runtime
cd runtime/Swift
# Swift insists on a space between -j and the number, so cannot use _smp_mflags
swift build -c release %{?_smp_build_ncpus:-j %_smp_build_ncpus} \
  -Xlinker --build-id -Xlinker --as-needed -Xlinker -z -Xlinker relro \
  -Xlinker -z -Xlinker now
cd -
%endif

%install
# Install for Java; cannot use %%mvn_install as it passes %%name to -n
xmvn-install -R .xmvn-reactor -n antlr4 -d %{buildroot}
jdir=target/site/apidocs
[ -d .xmvn/apidocs ] && jdir=.xmvn/apidocs
mkdir -p %{buildroot}%{_licensedir}
if [ -d "${jdir}" ]; then
   install -dm755 %{buildroot}%{_javadocdir}/antlr4
   cp -pr "${jdir}"/* %{buildroot}%{_javadocdir}/antlr4
   echo '%{_javadocdir}/antlr4' >>.mfiles-javadoc
fi

%jpackage_script org.antlr.v4.Tool "" "" antlr4/antlr4:antlr3-runtime:antlr4/antlr4-runtime:stringtemplate4:treelayout antlr4 true

# Install the C++ runtime
cd runtime/Cpp
%cmake_install
cd -

# Install the Go runtime
%ifarch %go_arches
mkdir -p %{buildroot}%{gopath}/src/%{goipath}
cp -a runtime/Go/antlr/v* %{buildroot}%{gopath}/src/%{goipath}
cat > %{buildroot}%{gopath}/src/%{goipath}/.goipath << EOF
version:%{version}-%{release}
excluderegex:.*example.*
EOF
%endif

# Install the JavaScript runtime
%ifarch %nodejs_arches
mkdir -p %{buildroot}%{nodejs_sitelib}
cp -a runtime/JavaScript/src/antlr4 %{buildroot}%{nodejs_sitelib}
%endif

# Install the Python 3 runtime
cd runtime/Python3
%pyproject_install
%pyproject_save_files -L antlr4
cd -

%if %{with swift}
# Install the Swift runtime
mkdir -p %{buildroot}%{swiftdir}/%{_arch}
cp -p .build/release/libAntlr4Dynamic.so %{buildroot}%{swiftdir}
cp -p .build/release/libAntlr4Static.a %{buildroot}%{swiftdir}
cp -p .build/*/release/Modules/Antlr4.swift{doc,module,sourceinfo} %{buildroot}%{swiftdir}/%{_arch}
cp -p .build/release/description.json %{buildroot}%{swiftdir}/%{_arch}

# Fix the rpath to have $ORIGIN first
oldrunpath=$(chrpath %{buildroot}%{swiftdir}/libAntlr4Dynamic.so | cut -d= -f2 | cut -d: -f1)
chrpath -r "\$ORIGIN:$oldrunpath" %{buildroot}%{swiftdir}/libAntlr4Dynamic.so
%endif

# Create man pages
export PYTHONPATH=%{buildroot}%{python3_sitelib}
mkdir -p %{buildroot}%{_mandir}/man1
cat > antlr4 << EOF
java -cp %{buildroot}%{_javadir}/antlr4/antlr4.jar:%{buildroot}%{_javadir}/antlr4/antlr4-runtime.jar:$(build-classpath antlr3-runtime stringtemplate4 treelayout) org.antlr.v4.Tool
EOF
chmod a+x antlr4
help2man -N --version-string=%{version} -h '' ./antlr4 \
  -n 'Parser generator (ANother Tool for Language Recognition)' \
  > %{buildroot}%{_mandir}/man1/antlr4.1
cd %{buildroot}%{_bindir}
help2man -N --version-string=%{version} ./pygrun \
  -n 'Parser generator (ANother Tool for Language Recognition)' \
  > %{buildroot}%{_mandir}/man1/pygrun.1
cd -

# Clean up bits we do not want
rm -fr %{buildroot}%{_docdir}/libantlr4

%files -n antlr4-runtime -f .mfiles-antlr4-runtime
%doc README.md
%license LICENSE.txt

%files -n antlr4 -f .mfiles-antlr4
%doc CHANGES.txt
%{_bindir}/antlr4
%{_mandir}/man1/antlr4.1*

%files -n antlr4-javadoc -f .mfiles-javadoc
%doc CHANGES.txt
%license LICENSE.txt

%files -n antlr4-maven-plugin -f .mfiles-antlr4-maven-plugin

%files -n antlr4-doc
%doc doc
%license LICENSE.txt

%files -n antlr4-cpp-runtime
%doc runtime/Cpp/README.md
%license LICENSE.txt
%{_libdir}/libantlr4-runtime.so.%{version}

%files -n antlr4-cpp-runtime-devel
%doc runtime/Cpp/cmake/Antlr4Package.md runtime/Cpp/cmake/README.md
%{_includedir}/antlr4-runtime/
%{_libdir}/libantlr4-runtime.so
%{_libdir}/cmake/antlr4-generator/
%{_libdir}/cmake/antlr4-runtime/

%ifarch %go_arches
%files -n golang-github-antlr4-antlr-devel
%license LICENSE.txt
%{gopath}/src/github.com/
%endif

%ifarch %nodejs_arches
%files -n nodejs-antlr4
%doc runtime/JavaScript/README.md
%license LICENSE.txt
%{nodejs_sitelib}/antlr4/
%endif

%files -n python3-antlr4-runtime -f %{pyproject_files}
%doc runtime/Python3/README.txt
%license LICENSE.txt
%{_bindir}/pygrun
%{_mandir}/man1/pygrun.1*

%if %{with swift}
%files -n swift-antlr4-runtime
%license LICENSE.txt
%{swiftdir}/
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 4.13.2-11
- Latest state for antlr4-project

* Wed Nov 12 2025 Vít Ondruch <vondruch@redhat.com> - 4.13.2-10
- Rebuild for nodejs-packaging

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.13.2-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.13.2-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 4.13.2-7
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Python Maint <python-maint@redhat.com> - 4.13.2-5
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Jerry James <loganjerry@gmail.com> - 4.13.2-3
- Add java-headless dependency to the antlr4 package
- Simplify swift conditionals
- Do configuration actions in %%conf

* Fri Nov 08 2024 Michel Lind <salimma@fedoraproject.org> - 4.13.2-2
- Gate out Swift language support on EL for now

* Sun Aug 04 2024 Jerry James <loganjerry@gmail.com> - 4.13.2-1
- Version 4.13.2

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Jerry James <loganjerry@gmail.com> - 4.13.1-2
- Build with maven-replacer-plugin support

* Thu Jul 11 2024 Jerry James <loganjerry@gmail.com> - 4.13.1-1
- Version 4.13.1
- Drop unneeded static-library patch
- Build javadoc documentation again
- Change name of the golang package

* Wed Jun 26 2024 Jerry James <loganjerry@gmail.com> - 4.10.1-16
- Remove reference to static library from cmake files

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 4.10.1-15
- Rebuilt for Python 3.13

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 4.10.1-14
- Rebuilt for java-21-openjdk as system jdk

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 4.10.1-13
- Rebuild for golang 1.22.0

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug  1 2023 Jerry James <loganjerry@gmail.com> - 4.10.1-10
- Remove maven-clean-plugin BR

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Python Maint <python-maint@redhat.com> - 4.10.1-8
- Rebuilt for Python 3.12

* Mon Feb 27 2023 Jerry James <loganjerry@gmail.com> - 4.10.1-7
- Dynamically generate python BuildRequires

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Jerry James <loganjerry@gmail.com> - 4.10.1-6
- Adapt to jakarta-json 2.x

* Wed Nov  2 2022 Jerry James <loganjerry@gmail.com> - 4.10.1-5
- BR nodejs-packaging to fix FTBFS

* Thu Aug 11 2022 Jerry James <loganjerry@gmail.com> - 4.10.1-4
- Convert License tag to SPDX

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Jerry James <loganjerry@gmail.com> - 4.10.1-3
- Remove i686 support (https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs)

* Tue Jun 21 2022 Jerry James <loganjerry@gmail.com> - 4.10.1-2
- Adapt to changed Provides in javapackages-tools

* Mon Jun 20 2022 Jerry James <loganjerry@gmail.com> - 4.10.1-1
- Version 4.10.1
- Add generated cmake files to antlr4-cpp-runtime-devel (rhbz#2098357)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.9.3-5
- Rebuilt for Python 3.11

* Wed Apr 27 2022 Jerry James <loganjerry@gmail.com> - 4.9.3-4
- Remove . from %%cmake to fix FTBFS (rhbz#2070433)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.9.3-3
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov  7 2021 Jerry James <loganjerry@gmail.com> - 4.9.3-1
- Version 4.9.3
- Drop upstreamed -unicode-properties and -utf8cpp patches

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Jerry James <loganjerry@gmail.com> - 4.9.2-2
- Drop the javadoc subpackage due to xmvn errors
- Fix an invalid RPATH in the swift runtime library

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.9.2-2
- Rebuilt for Python 3.10

* Fri Mar 12 2021 Jerry James <loganjerry@gmail.com> - 4.9.2-1
- Version 4.9.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan  7 2021 Jerry James <loganjerry@gmail.com> - 4.9.1-1
- Version 4.9.1
- Remove the mono runtime, which no longer builds on Fedora

* Mon Nov 30 2020 Jerry James <loganjerry@gmail.com> - 4.9-1
- Version 4.9
- Add the JavaScript runtime
- Add -utf8cpp patch

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Jerry James <loganjerry@gmail.com> - 4.8-4
- Fix cmake and javadoc issues

* Tue Jul 21 2020 Mat Booth <mat.booth@redhat.com> - 4.8-3
- Allow building against JDK 11

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.8-2
- Rebuilt for Python 3.9

* Tue Jan 21 2020 Jerry James <loganjerry@gmail.com> - 4.8-1
- Initial RPM, based on old antlr4.spec

## END: Generated by rpmautospec
