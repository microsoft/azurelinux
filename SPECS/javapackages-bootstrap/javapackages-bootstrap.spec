# Exclude automatically generated requires on java interpreter which is not
# owned by any package
%global         __requires_exclude ^/usr/lib/jvm/java

# Don't run OSGi dependency generators on private (bundled) JARs
%global         __requires_exclude_from \\.jar$
%global         __provides_exclude_from \\.jar$

%global mavenHomePath %{_datadir}/%{name}
%global metadataPath %{mavenHomePath}/maven-metadata
%global artifactsPath %{_javadir}
%global launchersPath %{_libexecdir}/%{name}

Name:           javapackages-bootstrap
Version:        1.14.0
Release:        1%{?dist}
Summary:        A means of bootstrapping Java Packages Tools
# For detailed info see the file javapackages-bootstrap-PACKAGE-LICENSING
License:        ASL 2.0 and ASL 1.1 and (ASL 2.0 or EPL-2.0) and (EPL-2.0 or GPLv2 with exceptions) and MIT and (BSD with advertising) and BSD-3-Clause and EPL-1.0 and EPL-2.0 and CDDL-1.0 and xpp and CC0 and Public Domain
URL:            https://github.com/fedora-java/javapackages-bootstrap
BuildArch:      noarch

Source0:        https://github.com/fedora-java/javapackages-bootstrap/releases/download/%{version}/javapackages-bootstrap-%{version}.tar.xz

# License breakdown
Source1:        javapackages-bootstrap-PACKAGE-LICENSING
Source2:        ignore.upstream.patch.txt

Source1002:     apache-pom.tar.xz
Source1001:     ant.tar.xz
Source1003:     apiguardian.tar.xz
Source1004:     asm.tar.xz
Source1005:     assertj-core.tar.xz
Source1006:     bnd.tar.xz
Source1007:     build-helper-maven-plugin.tar.xz
Source1008:     byte-buddy.tar.xz
Source1009:     cdi.tar.xz
Source1010:     cglib.tar.xz
Source1011:     common-annotations-api.tar.xz
Source1012:     commons-beanutils.tar.xz
Source1013:     commons-cli.tar.xz
Source1014:     commons-codec.tar.xz
Source1015:     commons-collections.tar.xz
Source1016:     commons-compress-1.21.tar.xz
Source1017:     commons-io.tar.xz
Source1018:     commons-jxpath.tar.xz
Source1019:     commons-lang.tar.xz
Source1020:     commons-logging.tar.xz
Source1021:     commons-parent-pom.tar.xz
Source1022:     cup.tar.xz
Source1023:     easymock.tar.xz
Source1024:     felix-parent-pom.tar.xz
Source1025:     felix-utils.tar.xz
Source1026:     fusesource-pom.tar.xz
Source1027:     guava.tar.xz
Source1028:     guice.tar.xz
Source1029:     hamcrest.tar.xz
Source1030:     httpcomponents-client.tar.xz
Source1031:     httpcomponents-core.tar.xz
Source1032:     httpcomponents-parent-pom.tar.xz
Source1033:     injection-api.tar.xz
Source1034:     jansi.tar.xz
Source1035:     jcommander.tar.xz
Source1036:     jdom.tar.xz
Source1037:     jdom2.tar.xz
Source1038:     jflex.tar.xz
Source1039:     jsoup.tar.xz
Source1040:     jsr-305.tar.xz
Source1041:     junit4.tar.xz
Source1042:     junit5.tar.xz
Source1043:     maven-antrun-plugin.tar.xz
Source1044:     maven-archiver.tar.xz
Source1045:     maven-artifact-transfer.tar.xz
Source1046:     maven-assembly-plugin.tar.xz
Source1047:     maven-bundle-plugin.tar.xz
Source1048:     maven-common-artifact-filters.tar.xz
Source1049:     maven-compiler-plugin.tar.xz
Source1050:     maven-dependency-analyzer.tar.xz
Source1051:     maven-dependency-plugin.tar.xz
Source1052:     maven-dependency-tree.tar.xz
Source1053:     maven-enforcer.tar.xz
Source1054:     maven-file-management.tar.xz
Source1055:     maven-filtering.tar.xz
Source1056:     maven-jar-plugin.tar.xz
Source1057:     maven-parent-pom.tar.xz
Source1058:     maven-plugin-testing.tar.xz
Source1059:     maven-plugin-tools.tar.xz
Source1060:     maven-remote-resources-plugin.tar.xz
Source1061:     maven-resolver.tar.xz
Source1062:     maven-resources-plugin.tar.xz
Source1063:     maven-resources.tar.xz
Source1064:     maven-shared-incremental.tar.xz
Source1065:     maven-shared-io.tar.xz
Source1066:     maven-shared-utils.tar.xz
Source1067:     maven-source-plugin.tar.xz
Source1068:     maven-surefire.tar.xz
Source1069:     maven-verifier.tar.xz
Source1070:     maven-wagon.tar.xz
Source1071:     maven.tar.xz
Source1072:     mockito.tar.xz
Source1073:     modello.tar.xz
Source1074:     mojo-parent-pom.tar.xz
Source1075:     munge-maven-plugin.tar.xz
Source1076:     objenesis.tar.xz
Source1077:     opentest4j.tar.xz
Source1078:     osgi-annotation.tar.xz
Source1079:     osgi-cmpn.tar.xz
Source1080:     osgi-core.tar.xz
Source1081:     oss-parent-pom.tar.xz
Source1082:     plexus-archiver.tar.xz
Source1083:     plexus-cipher.tar.xz
Source1084:     plexus-classworlds.tar.xz
Source1085:     plexus-compiler.tar.xz
Source1086:     plexus-components-pom.tar.xz
Source1087:     plexus-containers.tar.xz
Source1088:     plexus-interpolation.tar.xz
Source1089:     plexus-io.tar.xz
Source1090:     plexus-languages.tar.xz
Source1091:     plexus-pom.tar.xz
Source1092:     plexus-resources.tar.xz
Source1093:     plexus-sec-dispatcher.tar.xz
Source1094:     plexus-utils.tar.xz
Source1095:     qdox.tar.xz
Source1096:     servlet-api.tar.xz
Source1097:     sisu-build-api.tar.xz
Source1098:     sisu-inject.tar.xz
Source1099:     sisu-mojos.tar.xz
Source1100:     sisu-plexus.tar.xz
Source1101:     slf4j.tar.xz
Source1102:     testng.tar.xz
Source1103:     univocity-parsers.tar.xz
Source1104:     velocity-engine.tar.xz
Source1105:     xbean.tar.xz
Source1106:     xmlunit.tar.xz
Source1107:     xmvn.tar.xz
Source1108:     xz-java.tar.xz

Patch0:         0001-Bind-to-OpenJDK-11-for-runtime.patch
Patch1:         0001-Remove-usage-of-ArchiveStreamFactory.patch
Patch2:         CVE-2023-37460.patch

Provides:       bundled(ant) = 1.10.9
Provides:       bundled(apache-parent) = 23
Provides:       bundled(apiguardian) = 1.1.1
Provides:       bundled(objectweb-asm) = 9.0
Provides:       bundled(assertj-core) = 3.19.0
Provides:       bundled(aqute-bnd) = 5.2.0
Provides:       bundled(maven-plugin-build-helper) = 3.2.0
Provides:       bundled(byte-buddy) = 1.10.20
Provides:       bundled(cdi-api) = 2.0.2
Provides:       bundled(cglib) = 3.3.0
Provides:       bundled(jakarta-annotations) = 1.3.5
Provides:       bundled(apache-commons-beanutils) = 1.9.4
Provides:       bundled(apache-commons-cli) = 1.4
Provides:       bundled(apache-commons-codec) = 1.15
Provides:       bundled(apache-commons-collections) = 3.2.2
Provides:       bundled(apache-commons-compress) = 1.21
Provides:       bundled(apache-commons-io) = 2.8.0
Provides:       bundled(apache-commons-jxpath) = 1.3
Provides:       bundled(apache-commons-lang3) = 3.11
Provides:       bundled(apache-commons-logging) = 1.2
Provides:       bundled(apache-commons-parent) = 52
Provides:       bundled(java_cup) = 0.11b
Provides:       bundled(easymock) = 4.2
Provides:       bundled(felix-parent) = 7
Provides:       bundled(felix-utils) = 1.11.6
Provides:       bundled(fusesource-pom) = 1.12
Provides:       bundled(guava) = 30.1
Provides:       bundled(google-guice) = 4.2.3
Provides:       bundled(hamcrest) = 2.2
Provides:       bundled(httpcomponents-client) = 4.5.11
Provides:       bundled(httpcomponents-core) = 4.4.13
Provides:       bundled(httpcomponents-project) = 12
Provides:       bundled(atinject) = 1.0.3
Provides:       bundled(jansi) = 1.18
Provides:       bundled(beust-jcommander) = 1.78
Provides:       bundled(jdom) = 1.1.3
Provides:       bundled(jdom2) = 2.0.6
Provides:       bundled(jflex) = 1.7.0
Provides:       bundled(jsoup) = 1.13.1
Provides:       bundled(jsr-305) = 3.0.2
Provides:       bundled(junit) = 4.13.1
Provides:       bundled(junit5) = 5.7.0
Provides:       bundled(maven-antrun-plugin) = 3.0.0
Provides:       bundled(maven-archiver) = 3.5.1
Provides:       bundled(maven-artifact-transfer) = 0.13.1
Provides:       bundled(maven-assembly-plugin) = 3.3.0
Provides:       bundled(maven-plugin-bundle) = 5.1.1
Provides:       bundled(maven-common-artifact-filters) = 3.1.0
Provides:       bundled(maven-compiler-plugin) = 3.8.1
Provides:       bundled(maven-dependency-analyzer) = 1.11.3
Provides:       bundled(maven-dependency-plugin) = 3.1.2
Provides:       bundled(maven-dependency-tree) = 3.0.1
Provides:       bundled(maven-enforcer) = 3.0.0~M2
Provides:       bundled(maven-file-management) = 3.0.0
Provides:       bundled(maven-filtering) = 3.2.0
Provides:       bundled(maven-jar-plugin) = 3.2.0
Provides:       bundled(maven-parent) = 34
Provides:       bundled(maven-plugin-testing) = 3.3.0
Provides:       bundled(maven-plugin-tools) = 3.6.0
Provides:       bundled(maven-remote-resources-plugin) = 1.7.0
Provides:       bundled(maven-resolver) = 1.6.1
Provides:       bundled(maven-resources-plugin) = 3.2.0
Provides:       bundled(maven-resources) = 1.4
Provides:       bundled(maven-shared-incremental) = 1.1
Provides:       bundled(maven-shared-io) = 3.0.0
Provides:       bundled(maven-shared-utils) = 3.3.3
Provides:       bundled(maven-source-plugin) = 3.2.1
Provides:       bundled(maven-surefire) = 3.0.0~M3
Provides:       bundled(maven-verifier) = 1.7.2
Provides:       bundled(maven-wagon) = 3.4.2
Provides:       bundled(maven) = 3.6.3
Provides:       bundled(mockito) = 3.7.13
Provides:       bundled(modello) = 1.11
Provides:       bundled(mojo-parent) = 60
Provides:       bundled(munge-maven-plugin) = 1.0
Provides:       bundled(objenesis) = 3.1
Provides:       bundled(opentest4j) = 1.2.0
Provides:       bundled(osgi-annotation) = 8.0.0
Provides:       bundled(osgi-compendium) = 7.0.0
Provides:       bundled(osgi-core) = 8.0.0
Provides:       bundled(sonatype-oss-parent) = 7
Provides:       bundled(plexus-archiver) = 4.2.2
Provides:       bundled(plexus-cipher) = 1.7
Provides:       bundled(plexus-classworlds) = 2.6.0
Provides:       bundled(plexus-compiler) = 2.8.8
Provides:       bundled(plexus-components-pom) = 6.4
Provides:       bundled(plexus-containers) = 2.1.0
Provides:       bundled(plexus-interpolation) = 1.26
Provides:       bundled(plexus-io) = 3.2.0
Provides:       bundled(plexus-languages) = 1.0.6
Provides:       bundled(plexus-pom) = 7
Provides:       bundled(plexus-resources) = 1.1.0
Provides:       bundled(plexus-sec-dispatcher) = 1.4
Provides:       bundled(plexus-utils) = 3.3.0
Provides:       bundled(qdox) = 2.0.0
Provides:       bundled(jakarta-servlet) = 4.0.3
Provides:       bundled(plexus-build-api) = 0.0.7
Provides:       bundled(sisu) = 0.3.4
Provides:       bundled(sisu-mojos) = 0.3.4
Provides:       bundled(sisu-plexus) = 0.3.4
Provides:       bundled(slf4j) = 1.7.30
Provides:       bundled(testng) = 7.3.0
Provides:       bundled(univocity-parsers) = 2.9.1
Provides:       bundled(velocity) = 1.7
Provides:       bundled(xbean) = 4.18
Provides:       bundled(xmlunit) = 2.8.2
Provides:       bundled(xmvn) = 4.0.0~SNAPSHOT
Provides:       bundled(xz-java) = 1.8

BuildRequires:  byaccj
BuildRequires:  msopenjdk-11
BuildRequires:  javapackages-generators
BuildRequires:  java-devel

Requires:       bash
Requires:       coreutils
Requires:       msopenjdk-11
Requires:       procps-ng

%description
In a nutshell, Java Packages Bootstrap (JPB) is a standalone build of all Java
software packages that are required for Java Packages Tools (JPT) to work.

In order to achieve reliable and reproducible builds of Java packages while
meeting Fedora policy that requires everything to be built from source, without
using prebuilt binary artifacts, it is necessary to build the packages in a
well-defined, acyclic order. Dependency cycles between packages are the biggest
obstacle to achieving this goal and JPT is the biggest offender -- it requires
more than a hundred of Java packages, all of which in turn build-require JPT.

JPB comes with a solution to this problem -- it builds everything that JPT needs
to work, without reliance on any Java software other than OpenJDK. JPT can
depend on JPB for everything, without depending on any other Java packages. For
example, JPB contains embedded version of XMvn, removing dependency of JPT on
XMvn, allowing JPT to be used before one builds XMvn package.

%prep
%setup -q

# leave out the first source as it has already been extracted
# leave out licensing breakdown file
# leave ignore patch text file
other_sources=$(echo %{sources} | cut -d' ' -f4-)

for source in ${other_sources}
do
  tar -xf "${source}"
done

%patch0 -p1
pushd "downstream/commons-compress"
%patch1 -p1 
popd

pushd "downstream/plexus-archiver"
%patch2 -p1 
popd

for patch_path in patches/*/*
do
  package_name="$(echo ${patch_path} | cut -f2 -d/)"
  patch_name="$(echo ${patch_path} | cut -f3 -d/)"
  
  pushd "downstream/${package_name}"
  # not applying some patches provided by javapackages-bootstrap
  # some upstream patches become not applicable when upgrading any of the sources
  # only apply the patch if patch is not in the ignore.upstream.patch.txt file
  if ! grep -Fxq "patches/${package_name}/${patch_name}" %{SOURCE2}
  then
    patch -p1 < "../../patches/${package_name}/${patch_name}"
  fi  
  popd
done

# removing harmony files from the source as it causes build time error
sed  -i "/<excludeSourceMatching>/a\ \t<excludeSourceMatching>/org/apache/commons/compress/harmony/(pack200|unpack200)/.*</excludeSourceMatching>" project/commons-compress.xml


%build
export LC_ALL=en_US.UTF-8 
export JAVA_HOME=$(find /usr/lib/jvm -name "*openjdk*")
./mbi.sh build -parallel

%install
export JAVA_HOME=$(find /usr/lib/jvm -name "*openjdk*")
./mbi.sh dist \
  -basePackageName=%{name} \
  -installRoot=%{buildroot} \
  -mavenHomePath=%{mavenHomePath} \
  -metadataPath=%{metadataPath} \
  -artifactsPath=%{artifactsPath} \
  -launchersPath=%{launchersPath} \
  -licensesPath=%{_licensedir}/%{name} \

# fix permissions
for f in mvn mvnDebug mvnyjp
do
  chmod +x "%{buildroot}%{mavenHomePath}/bin/${f}"
done

# Use toolchains.xml provided by javapackages-tools
ln -sf %{_datadir}/xmvn/conf/toolchains.xml %{buildroot}%{mavenHomePath}/conf/toolchains.xml

install -d -m 755 %{buildroot}%{_rpmmacrodir}
echo '%%jpb_env PATH=/usr/libexec/javapackages-bootstrap:$PATH' >%{buildroot}%{_rpmmacrodir}/macros.%{name}

# by default it sets JAVA_HOME to /usr/lib/jvm/java-11-openjdk
sed -i 's|/usr/lib/jvm/java-11-openjdk|%{java_home}|' %{buildroot}%{_datadir}/%{name}/bin/mvn
sed -i 's|/usr/lib/jvm/java-11-openjdk|%{java_home}|' %{buildroot}%{launchersPath}/xmvn-install

%check
%{buildroot}%{launchersPath}/xmvn --version

%files
%{mavenHomePath}
%{metadataPath}/*
%{artifactsPath}/*
%{launchersPath}/*
%{_rpmmacrodir}

%license %{_licensedir}/%{name}
%doc README.md
%doc AUTHORS

%changelog
* Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.14.0-1
- Auto-upgrade to 1.14.0 - azl 3.0

* Fri Aug 11 2023 Saul Paredes <saulparedes@microsoft.com> - 1.5.0-4
- Patch plexus-archiver to fix CVE-2023-37460

* Wed Apr 05 2023 Riken Maharjan <rmaharjan@microsoft.com> - 1.5.0-3
- Update commons-compress to 1.21 

* Thu Mar 16 2023 Riken Maharjan <rmaharjan@microsoft.com> - 1.5.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified

* Mon Jul 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-1
- Update to upstream version 1.5.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 18 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-1
- Update to upstream version 1.4.0

* Mon Feb 08 2021 Marian Koncek <mkoncek@redhat.com> - 1.3.0-1
- Update to upstream version 1.3.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 16 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Thu Dec  3 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.0-1
- Update to upstream version 1.1.0

* Wed Nov 25 2020 Marian Koncek <mkoncek@redhat.com> - 1.0.0-1
- Initial commit
