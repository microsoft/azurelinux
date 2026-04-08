# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global antlr_version 3.5.3
%global javascript_runtime_version 3.1
%global baserelease 16

# This package needs itself to build.  Use this to bootstrap on a new system.
%bcond bootstrap 0

# Component versions to use when bootstrapping
%global antlr2_version 2.7.7
%global bootstrap_version 3.5
%global ST4ver1 4.0.7
%global ST4ver2 4.0.8
%global stringtemplatever 3.2.1

%global giturl  https://github.com/antlr/antlr3

Summary:        ANother Tool for Language Recognition
Name:           antlr3
Epoch:          1
Version:        %{antlr_version}
Release:        %{baserelease}%{?dist}
# Sources are BSD-3-Clause with the following exceptions:
# BSD-3-Clause OR GPL-1.0-or-later OR Artistic-1.0-Perl:
#   runtime/Perl5/Build.PL, runtime/Perl5/lib/ANTLR/Runtime.pm
# Apache-2.0: antlr-ant/main/antlr3-task/antlr3-src/org/apache/tools/ant/antlr/ANTLR3.java
# MIT: runtime/CSharp2/Sources/Antlr3.Runtime/Antlr.Runtime.JavaExtensions/Check.cs
# FSFAP: runtime/C/INSTALL
# LicenseRef-Fedora-Public-Domain: runtime/Python/xmlrunner.py
# LicenseRef-Unicode-legacy-source-code (not allowed in Fedora):
#    runtime/C/include/antlr3convertutf.h
#    runtime/C/src/antlr3convertutf.c
#    runtime/Cpp/include/antlr3convertutf.hpp
# Unknown: runtime/CSharp2/LICENSE.TXT and runtime/Delphi/LICENSE.TXT add a
#   copyleft clause to BSD-3-Clause.  SPDX has no name for it.  We don't ship
#   anything derived from C# or Delphi files in the binary RPM.
License:        BSD-3-Clause
SourceLicense:  %{license} AND (BSD-3-Clause OR GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0 AND MIT AND FSFAP AND LicenseRef-Fedora-Public-Domain
URL:            https://www.antlr3.org/
VCS:            git:%{giturl}.git

Source0:        %{giturl}/archive/%{antlr_version}/%{name}-%{antlr_version}.tar.gz
Source1:        http://www.antlr3.org/download/antlr-javascript-runtime-%{javascript_runtime_version}.zip
%if %{with bootstrap}
# Get prebuilt versions to bootstrap
Source2:        https://repo1.maven.org/maven2/org/antlr/ST4/%{ST4ver1}/ST4-%{ST4ver1}.jar
Source3:        https://repo1.maven.org/maven2/org/antlr/ST4/%{ST4ver1}/ST4-%{ST4ver1}.pom
Source4:        https://repo1.maven.org/maven2/org/antlr/ST4/%{ST4ver2}/ST4-%{ST4ver2}.jar
Source5:        https://repo1.maven.org/maven2/org/antlr/ST4/%{ST4ver2}/ST4-%{ST4ver2}.pom
Source6:        https://repo1.maven.org/maven2/org/antlr/antlr/%{bootstrap_version}/antlr-%{bootstrap_version}.jar
Source7:        https://repo1.maven.org/maven2/org/antlr/antlr/%{bootstrap_version}/antlr-%{bootstrap_version}.pom
Source8:        https://repo1.maven.org/maven2/org/antlr/antlr-master/%{bootstrap_version}/antlr-master-%{bootstrap_version}.pom
Source9:        https://repo1.maven.org/maven2/org/antlr/antlr-runtime/%{bootstrap_version}/antlr-runtime-%{bootstrap_version}.jar
Source10:       https://repo1.maven.org/maven2/org/antlr/antlr-runtime/%{bootstrap_version}/antlr-runtime-%{bootstrap_version}.pom
Source11:       https://repo1.maven.org/maven2/org/antlr/antlr3-maven-plugin/%{bootstrap_version}/antlr3-maven-plugin-%{bootstrap_version}.jar
Source12:       https://repo1.maven.org/maven2/org/antlr/antlr3-maven-plugin/%{bootstrap_version}/antlr3-maven-plugin-%{bootstrap_version}.pom
Source13:       https://repo1.maven.org/maven2/org/antlr/stringtemplate/%{stringtemplatever}/stringtemplate-%{stringtemplatever}.jar
Source14:       https://repo1.maven.org/maven2/org/antlr/stringtemplate/%{stringtemplatever}/stringtemplate-%{stringtemplatever}.pom
Source15:       https://repo1.maven.org/maven2/antlr/antlr/%{antlr2_version}/antlr-%{antlr2_version}.jar
Source16:       https://repo1.maven.org/maven2/antlr/antlr/%{antlr2_version}/antlr-%{antlr2_version}.pom
%endif

Patch:          0001-java8-fix.patch
# Generate OSGi metadata
Patch:          osgi-manifest.patch
# Increase the default conversion timeout to avoid build failures when complex
# grammars are processed on slow architectures.  Patch from Debian.
Patch:          0002-conversion-timeout.patch
# Fix problems with the C template.  Patch from Debian.
Patch:          0003-fix-c-template.patch
# Keep Token.EOF_TOKEN for backwards compatibility.  Patch from Debian.
Patch:          0004-eof-token.patch
# Make parsers reproducible.  Patch from Debian.
Patch:          0005-reproducible-parsers.patch
# Fix for C++20
Patch:          0006-antlr3memory.hpp-fix-for-C-20-mode.patch
# Compile for target 1.8 to fix build with JDK 11
Patch:          0007-update-java-target.patch
# Fix source for tighter gcc template checks
Patch:          0008-unconst-cyclicdfa-gcc-14.patch

BuildRequires:  ant-openjdk25 
BuildRequires:  make
BuildRequires:  maven-local-openjdk25
%if %{without bootstrap}
BuildRequires:  mvn(org.antlr:antlr)
BuildRequires:  mvn(org.antlr:antlr3-maven-plugin)
BuildRequires:  mvn(org.antlr:ST4)
BuildRequires:  mvn(org.antlr:stringtemplate)
%endif
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api)

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# This can be removed when F48 reaches EOL
# The C/C++ backend contains files with the not-allowed
# LicenseRef-Unicode-legacy-source-code license
Obsoletes:      %{name}-C < 3.5.3-16
Obsoletes:      %{name}-C-devel < 3.5.3-16
Obsoletes:      %{name}-C++-devel < 3.5.3-16
Obsoletes:      %{name}-C-docs < 3.5.3-16
Provides:       %{name}-C = %{version}-%{release}
Provides:       %{name}-C-devel = %{version}-%{release}
Provides:       %{name}-C++-devel = %{version}-%{release}
Provides:       %{name}-C-docs = %{version}-%{release}

%description
ANother Tool for Language Recognition, is a language tool that provides a
framework for constructing recognizers, interpreters, compilers, and
translators from grammatical descriptions containing actions in a variety of
target languages.

%package        tool
Summary:        ANother Tool for Language Recognition
License:        BSD-3-Clause AND Apache-2.0
Provides:       %{name} = %{epoch}:%{antlr_version}-%{release}
Obsoletes:      %{name} < %{epoch}:%{antlr_version}-%{release}
Requires:       %{name}-java = %{epoch}:%{antlr_version}-%{release}
# Explicit requires for javapackages-tools since antlr3-script
# uses /usr/share/java-utils/java-functions
Requires:       javapackages-tools

%description    tool
ANother Tool for Language Recognition, is a language tool that provides a
framework for constructing recognizers, interpreters, compilers, and
translators from grammatical descriptions containing actions in a variety of
target languages.

%package        java
Summary:        Java run-time support for ANTLR-generated parsers

%description    java
Java run-time support for ANTLR-generated parsers

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
%{summary}.

%package        javascript
Summary:        Javascript run-time support for ANTLR-generated parsers
Version:        %{javascript_runtime_version}
Release:        %{antlr_version}.%{baserelease}%{?dist}

%description    javascript
Javascript run-time support for ANTLR-generated parsers

%prep
%autosetup -p1 -n antlr3-%{antlr_version} -a 1

%conf
sed -i "s,\${buildNumber},`cat %{_sysconfdir}/fedora-release` `date`," tool/src/main/resources/org/antlr/antlr.properties

# remove pre-built artifacts
find -type f -a -name *.jar -delete
find -type f -a -name *.class -delete

%pom_remove_parent

%pom_disable_module antlr3-maven-archetype
%pom_disable_module gunit
%pom_disable_module gunit-maven-plugin
%pom_disable_module antlr-complete

%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin -r :maven-javadoc-plugin

# workarounds bug in filtering (Mark invalid)
%pom_xpath_remove pom:resource/pom:filtering

%mvn_package :antlr-runtime java
%mvn_package : tool

%mvn_file :antlr antlr3
%mvn_file :antlr-runtime antlr3-runtime
%mvn_file :antlr-maven-plugin antlr3-maven-plugin

%if %{with bootstrap}
# Make the bootstrap JARs and POMs available
mkdir -p .m2/org/antlr/ST4/%{ST4ver1}
cp -p %{SOURCE2} %{SOURCE3} .m2/org/antlr/ST4/%{ST4ver1}
mkdir -p .m2/org/antlr/ST4/%{ST4ver2}
cp -p %{SOURCE4} %{SOURCE5} .m2/org/antlr/ST4/%{ST4ver2}
mkdir -p .m2/org/antlr/antlr/%{bootstrap_version}
cp -p %{SOURCE6} %{SOURCE7} .m2/org/antlr/antlr/%{bootstrap_version}
mkdir -p .m2/org/antlr/antlr-master/%{bootstrap_version}
cp -p %{SOURCE8} .m2/org/antlr/antlr-master/%{bootstrap_version}
mkdir -p .m2/org/antlr/antlr-runtime/%{bootstrap_version}
cp -p %{SOURCE9} %{SOURCE10} .m2/org/antlr/antlr-runtime/%{bootstrap_version}
mkdir -p .m2/org/antlr/antlr3-maven-plugin/%{bootstrap_version}
cp -p %{SOURCE11} %{SOURCE12} .m2/org/antlr/antlr3-maven-plugin/%{bootstrap_version}
mkdir -p .m2/org/antlr/stringtemplate/%{stringtemplatever}
cp -p %{SOURCE13} %{SOURCE14} .m2/org/antlr/stringtemplate/%{stringtemplatever}
mkdir -p .m2/antlr/antlr/%{antlr2_version}
cp -p %{SOURCE15} %{SOURCE16} .m2/antlr/antlr/%{antlr2_version}

# We don't need the parent POM
%pom_remove_parent .m2/org/antlr/ST4/%{ST4ver1}/ST4-%{ST4ver1}.pom
%pom_remove_parent .m2/org/antlr/ST4/%{ST4ver2}/ST4-%{ST4ver2}.pom
%pom_remove_parent .m2/org/antlr/antlr-master/%{bootstrap_version}/antlr-master-%{bootstrap_version}.pom
%endif

%build
%mvn_build -f

# build ant task
pushd antlr-ant/main/antlr3-task/
export CLASSPATH=$(build-classpath ant)
javac -encoding ISO-8859-1 -source 1.8 -target 1.8 \
  antlr3-src/org/apache/tools/ant/antlr/ANTLR3.java
jar cvf ant-antlr3.jar \
  -C antlr3-src org/apache/tools/ant/antlr/antlib.xml \
  -C antlr3-src org/apache/tools/ant/antlr/ANTLR3.class
popd

%install
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/antlr

%mvn_install

# install ant task
install -m 644 antlr-ant/main/antlr3-task/ant-antlr3.jar -D $RPM_BUILD_ROOT%{_javadir}/ant/ant-antlr3.jar
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ant-antlr3 << EOF
ant/ant-antlr3 antlr3
EOF

# install wrapper script
%jpackage_script org.antlr.Tool '' '' 'stringtemplate4/ST4.jar:antlr3.jar:antlr3-runtime.jar' antlr3 true

# install javascript runtime
pushd antlr-javascript-runtime-%{javascript_runtime_version}
install -pm 644 *.js $RPM_BUILD_ROOT%{_datadir}/antlr/
popd

%files tool -f .mfiles-tool
%doc README.txt tool/{LICENSE.txt,CHANGES.txt}
%{_bindir}/antlr3
%{_javadir}/ant/ant-antlr3.jar
%config(noreplace) %{_sysconfdir}/ant.d/ant-antlr3

%files java -f .mfiles-java
%doc tool/LICENSE.txt

%files javascript
%doc tool/LICENSE.txt
%{_datadir}/antlr/

%files javadoc -f .mfiles-javadoc
%doc tool/LICENSE.txt

%changelog
* Fri Feb 20 2026 Jerry James <loganjerry@gmail.com> - 1:3.5.3-16
- Remove the C and C++ backends
- They contain files with a disallowed license

* Tue Sep 23 2025 Jerry James <loganjerry@gmail.com> - 1:3.5.3-15
- Remove build dependency on maven-enforcer-plugin

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1:3.5.3-14
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Jerry James <loganjerry@gmail.com> - 1:3.5.3-11
- Clarify license of the tool subpackage
- Move configuration actions to %%conf

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1:3.5.3-10
- Rebuilt for java-21-openjdk as system jdk

* Thu Feb  1 2024 Avi Kivity <avi@scylladb.com> - 1:3.5.3-9
- Remove const specifiers in templates that are now flagged by gcc 14.

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 11 2023 Jerry James <loganjerry@gmail.com> - 1:3.5.3-5
- Remove unneeded maven 2 dependency

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 11 2022 Jerry James <loganjerry@gmail.com> - 1:3.5.3-3
- Convert License tag to SPDX

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Jerry James <loganjerry@gmail.com> - 1:3.5.3-2
- Remove i686 support (https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs)

* Sun Apr 10 2022 Jerry James <loganjerry@gmail.com> - 1:3.5.3-1
- Version 3.5.3
- Drop ancient obsoletes
- Minor spec file cleanups

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1:3.5.2-35
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Mar 12 2021 Jerry James <loganjerry@gmail.com> - 1:3.5.2-32
- Add bootstrap conditional (bz 1847093)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:3.5.2-29
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jun 03 2020 Fabio Valentini <decathorpe@gmail.com> - 1:3.5.2-28
- Actually apply Patch7.

* Tue May 12 2020 Jerry James <loganjerry@gmail.com> - 1:3.5.2-27
- Add 0007-update-java-target.patch to fix JDK 11 build

* Tue May 12 2020 Avi Kivity <avi@scylladb.com> - 1:3.5.2-27
- Fix for C++20 mode (#1834782)

* Sat Apr 25 2020 Fabio Valentini <decathorpe@gmail.com> - 1:3.5.2-26
- Remove unnecessary dependency on deprecated parent pom.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug  1 2019 Jerry James <loganjerry@gmail.com> - 1:3.5.2-24
- BR ant to fix FTBFS.  Thanks to Fabio Valentini for the hint.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Apr 27 2019 Jerry James <loganjerry@gmail.com> - 1:3.5.2-22
- Add Debian patches

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:3.5.2-20
- Explicit requires for javapackages-tools since antlr3 script uses
  java-functions. See RHBZ#1600426.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Michael Simacek <msimacek@redhat.com> - 1:3.5.2-18
- Remove ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 04 2016 David Geiger <daviddavid> - 1:3.5.2-13
- Fix stringtemplate4 jar classpath in shell script (stringtemplate4/ST4.jar)

* Tue Sep 27 2016 Michael Simacek <msimacek@redhat.com> - 1:3.5.2-12
- Fix Java 8 patch

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.2-11
- Regenerate build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Mat Booth <mat.booth@redhat.com> - 1:3.5.2-10
- Fix OSGi metadata
- Delete some commented out sections

* Wed Jun 17 2015 Mat Booth <mat.booth@redhat.com> - 1:3.5.2-9
- Build and ship the antlr3 ant task
- Add provides/obsoletes for separate ant-antlr3 package

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Michal Srb <msrb@redhat.com> - 1:3.5.2-7
- Fix FTBFS (Resolves: rhbz#1204672)

* Mon Mar 30 2015 Michael Simacek <msimacek@redhat.com> - 1:3.5.2-6
- Fix FTBFS

* Mon Mar 23 2015 Dan Horák <dan[at]danny.cz> - 1:3.5.2-5
- update BR - whole autotools chain is required explicitly

* Fri Oct 31 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1:3.5.2-4
- Avoid timestamp conflicts when updating jar manifest

* Sun Aug 31 2014 Till Maas <opensource@till.name> - 1:3.5.2-3
- Add missing dist tags for subpackages

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 18 2014 Michael Simacek <msimacek@redhat.com> - 3.5.2-1
- Update to upstream version 3.5.2
- Build the C runtime from main tarball
- Make C++-devel subpackage

* Tue Jun 17 2014 Michael Simacek <msimacek@redhat.com> - 3.5-1
- Update to upstream version 3.5

* Tue Jun 17 2014 Michael Simacek <msimacek@redhat.com> - 3.4-18
- Specfile cleanup

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-16
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.4-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Sep 09 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-12
- Fix wrong man page references (see BZ#855619)

* Tue Aug 21 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-11
- Now really compile for Java 1.6 everything

* Sat Aug 18 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-10
- Explicitly compile for Java 1.5, to (maybe?) fix BZ#842572

* Mon Aug 6 2012 Alexander Kurtakov <akurtako@redhat.com> 3.4-9
- Inject org.antlr.runtime OSGi metadata.
- Update BRs to newer versions.

* Tue Jul 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-8
- Add back requires on stringtemplate for java subpackage

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-6
- Fixed missing stringtemplate4 in antlr3 generator classpath
- Cleanup of Requires and BuildRequires on antlr2

* Thu Feb 23 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-5
- Disable python runtime (incompatible with current antlr version)

* Wed Feb 22 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-4
- Fix permissions for egg-info dir (fixes BZ#790499)

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-3
- Use wildcards for installing jars (different results on different releases)

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-2
- Add builnumber plugin to buildrequires
- Tab/space cleanup

* Mon Jan 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-1
- Update antlr version to 3.4
- Move to maven3 build, update macros etc
- Remove gunit for now

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 09 2011 Dan Horák <dan[at]danny.cz> - 3.2-15
- fix build on other arches

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2-13
- Add stringtemplate to Requires of java subpackage
- Use tomcat6 for building
- Use felix-parent and cleanup BRs on maven plugins

* Thu Nov 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2-12
- Move all pom files into java subpackage
- Fix pom filenames (Resolves rhbz#655831)
- Add java subpackage Requires for gunit subpackage

* Wed Oct 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-11
- non-bootstrap build

* Wed Oct 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-10
- fix pom patch
- fix bootstrapping
- fix dependencies

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-9
- recompiling .py files against Python 2.7 (rhbz#623269)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2-7
- Add master and runtime poms (#605267)

* Sat May 01 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-6
- Patch the Python runtime to print just a warning in case of version mismatch
  instead of raising an exception (since there is a good change it will work).

* Thu Apr 22 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-5
- Build the C runtime with --enable-64bit on x86_64 to avoid undeterministic
  segfaults caused by possible invalid conversion of 64bit pointers to int32_t

* Mon Mar 08 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-4
- Patch Java runtime build to include OSGi meta-information in the manifest
  (thanks to Mat Booth)
- Add "antlr3" prefix to all man pages to prevent namespace conflicts with
  standard man pages included in the man-pages package
- Split headers and man pages into a C-devel subpackage
- Fix multiple file ownership of Java runtime and gunit by the tool package

* Tue Mar 02 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-3
- Rebuilt in non-bootstrap mode.

* Sun Jan 31 2010 Milos Jakubicek <xjakub@fi.muni.cz> - 3.2-2
- Build the doxygen documentation for the C target in a C-docs subpackage
- BuildRequires/Requires cleanup across subpackages

* Sat Jan 30 2010 Milos Jakubicek <xjakub@fi.muni.cz> - 3.2-1
- Update to 3.2, bootstrap build.
- Build bindings for C and JavaScript as well as gunit and maven plugin.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-7
- Fix the name of the jar to antlr.jar

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-5
- Add bcel to build path

* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-4
- Add bcel build dep to version jar name

* Mon Nov 10 2008 Colin Walters <walters@redhat.com> - 3.1.1-3
- Add antlr3 script

* Thu Nov  6 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-2
- Fix the install of the jar (remove the version)

* Mon Nov  3 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-1
- Update to version 3.1.1
- Add python runtime subpackage

* Fri Jun 27 2008 Colin Walters <walters@redhat.com> - 3.0.1-2
- Fix some BRs

* Sun Apr 06 2008 Colin Walters <walters@redhat.com> - 3.0.1-1
- First version
