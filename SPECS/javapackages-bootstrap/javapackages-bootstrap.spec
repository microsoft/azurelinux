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
Version:        1.5.0
Release:        1%{?dist}
Summary:        A means of bootstrapping Java Packages Tools
# For detailed info see the file javapackages-bootstrap-PACKAGE-LICENSING
License:        ASL 2.0 and ASL 1.1 and (ASL 2.0 or EPL-2.0) and (EPL-2.0 or GPLv2 with exceptions) and MIT and BSD with advertising and BSD and EPL-1.0 and EPL-2.0 and CDDL-1.0 and xpp and CC0 and Public Domain
URL:            https://github.com/fedora-java/javapackages-bootstrap
BuildArch:      noarch

Source0:        https://github.com/fedora-java/javapackages-bootstrap/releases/download/%{version}/javapackages-bootstrap-%{version}.tar.xz

# License breakdown
Source1:        javapackages-bootstrap-PACKAGE-LICENSING

# To obtain the following sources:
# tar -xf ${name}-${version}.tar.xz
# pushd ${name}-${version}
# ./downstream.sh clone
# ./downstream.sh prep
# ./downstream.sh archive
# The results are in the archive directory
Source1002:     %{_mariner_sources_url}/apache-pom.tar.xz
Source1001:     %{_mariner_sources_url}/ant.tar.xz
Source1003:     %{_mariner_sources_url}/apiguardian.tar.xz
Source1004:     %{_mariner_sources_url}/asm.tar.xz
Source1005:     %{_mariner_sources_url}/assertj-core.tar.xz
Source1006:     %{_mariner_sources_url}/bnd.tar.xz
Source1007:     %{_mariner_sources_url}/build-helper-maven-plugin.tar.xz
Source1008:     %{_mariner_sources_url}/byte-buddy.tar.xz
Source1009:     %{_mariner_sources_url}/cdi.tar.xz
Source1010:     %{_mariner_sources_url}/cglib.tar.xz
Source1011:     %{_mariner_sources_url}/common-annotations-api.tar.xz
Source1012:     %{_mariner_sources_url}/commons-beanutils.tar.xz
Source1013:     %{_mariner_sources_url}/commons-cli.tar.xz
Source1014:     %{_mariner_sources_url}/commons-codec.tar.xz
Source1015:     %{_mariner_sources_url}/commons-collections.tar.xz
Source1016:     %{_mariner_sources_url}/commons-compress.tar.xz
Source1017:     %{_mariner_sources_url}/commons-io.tar.xz
Source1018:     %{_mariner_sources_url}/commons-jxpath.tar.xz
Source1019:     %{_mariner_sources_url}/commons-lang.tar.xz
Source1020:     %{_mariner_sources_url}/commons-logging.tar.xz
Source1021:     %{_mariner_sources_url}/commons-parent-pom.tar.xz
Source1022:     %{_mariner_sources_url}/cup.tar.xz
Source1023:     %{_mariner_sources_url}/easymock.tar.xz
Source1024:     %{_mariner_sources_url}/felix-parent-pom.tar.xz
Source1025:     %{_mariner_sources_url}/felix-utils.tar.xz
Source1026:     %{_mariner_sources_url}/fusesource-pom.tar.xz
Source1027:     %{_mariner_sources_url}/guava.tar.xz
Source1028:     %{_mariner_sources_url}/guice.tar.xz
Source1029:     %{_mariner_sources_url}/hamcrest.tar.xz
Source1030:     %{_mariner_sources_url}/httpcomponents-client.tar.xz
Source1031:     %{_mariner_sources_url}/httpcomponents-core.tar.xz
Source1032:     %{_mariner_sources_url}/httpcomponents-parent-pom.tar.xz
Source1033:     %{_mariner_sources_url}/injection-api.tar.xz
Source1034:     %{_mariner_sources_url}/jansi.tar.xz
Source1035:     %{_mariner_sources_url}/jcommander.tar.xz
Source1036:     %{_mariner_sources_url}/jdom.tar.xz
Source1037:     %{_mariner_sources_url}/jdom2.tar.xz
Source1038:     %{_mariner_sources_url}/jflex.tar.xz
Source1039:     %{_mariner_sources_url}/jsoup.tar.xz
Source1040:     %{_mariner_sources_url}/jsr-305.tar.xz
Source1041:     %{_mariner_sources_url}/junit4.tar.xz
Source1042:     %{_mariner_sources_url}/junit5.tar.xz
Source1043:     %{_mariner_sources_url}/maven-antrun-plugin.tar.xz
Source1044:     %{_mariner_sources_url}/maven-archiver.tar.xz
Source1045:     %{_mariner_sources_url}/maven-artifact-transfer.tar.xz
Source1046:     %{_mariner_sources_url}/maven-assembly-plugin.tar.xz
Source1047:     %{_mariner_sources_url}/maven-bundle-plugin.tar.xz
Source1048:     %{_mariner_sources_url}/maven-common-artifact-filters.tar.xz
Source1049:     %{_mariner_sources_url}/maven-compiler-plugin.tar.xz
Source1050:     %{_mariner_sources_url}/maven-dependency-analyzer.tar.xz
Source1051:     %{_mariner_sources_url}/maven-dependency-plugin.tar.xz
Source1052:     %{_mariner_sources_url}/maven-dependency-tree.tar.xz
Source1053:     %{_mariner_sources_url}/maven-enforcer.tar.xz
Source1054:     %{_mariner_sources_url}/maven-file-management.tar.xz
Source1055:     %{_mariner_sources_url}/maven-filtering.tar.xz
Source1056:     %{_mariner_sources_url}/maven-jar-plugin.tar.xz
Source1057:     %{_mariner_sources_url}/maven-parent-pom.tar.xz
Source1058:     %{_mariner_sources_url}/maven-plugin-testing.tar.xz
Source1059:     %{_mariner_sources_url}/maven-plugin-tools.tar.xz
Source1060:     %{_mariner_sources_url}/maven-remote-resources-plugin.tar.xz
Source1061:     %{_mariner_sources_url}/maven-resolver.tar.xz
Source1062:     %{_mariner_sources_url}/maven-resources-plugin.tar.xz
Source1063:     %{_mariner_sources_url}/maven-resources.tar.xz
Source1064:     %{_mariner_sources_url}/maven-shared-incremental.tar.xz
Source1065:     %{_mariner_sources_url}/maven-shared-io.tar.xz
Source1066:     %{_mariner_sources_url}/maven-shared-utils.tar.xz
Source1067:     %{_mariner_sources_url}/maven-source-plugin.tar.xz
Source1068:     %{_mariner_sources_url}/maven-surefire.tar.xz
Source1069:     %{_mariner_sources_url}/maven-verifier.tar.xz
Source1070:     %{_mariner_sources_url}/maven-wagon.tar.xz
Source1071:     %{_mariner_sources_url}/maven.tar.xz
Source1072:     %{_mariner_sources_url}/mockito.tar.xz
Source1073:     %{_mariner_sources_url}/modello.tar.xz
Source1074:     %{_mariner_sources_url}/mojo-parent-pom.tar.xz
Source1075:     %{_mariner_sources_url}/munge-maven-plugin.tar.xz
Source1076:     %{_mariner_sources_url}/objenesis.tar.xz
Source1077:     %{_mariner_sources_url}/opentest4j.tar.xz
Source1078:     %{_mariner_sources_url}/osgi-annotation.tar.xz
Source1079:     %{_mariner_sources_url}/osgi-cmpn.tar.xz
Source1080:     %{_mariner_sources_url}/osgi-core.tar.xz
Source1081:     %{_mariner_sources_url}/oss-parent-pom.tar.xz
Source1082:     %{_mariner_sources_url}/plexus-archiver.tar.xz
Source1083:     %{_mariner_sources_url}/plexus-cipher.tar.xz
Source1084:     %{_mariner_sources_url}/plexus-classworlds.tar.xz
Source1085:     %{_mariner_sources_url}/plexus-compiler.tar.xz
Source1086:     %{_mariner_sources_url}/plexus-components-pom.tar.xz
Source1087:     %{_mariner_sources_url}/plexus-containers.tar.xz
Source1088:     %{_mariner_sources_url}/plexus-interpolation.tar.xz
Source1089:     %{_mariner_sources_url}/plexus-io.tar.xz
Source1090:     %{_mariner_sources_url}/plexus-languages.tar.xz
Source1091:     %{_mariner_sources_url}/plexus-pom.tar.xz
Source1092:     %{_mariner_sources_url}/plexus-resources.tar.xz
Source1093:     %{_mariner_sources_url}/plexus-sec-dispatcher.tar.xz
Source1094:     %{_mariner_sources_url}/plexus-utils.tar.xz
Source1095:     %{_mariner_sources_url}/qdox.tar.xz
Source1096:     %{_mariner_sources_url}/servlet-api.tar.xz
Source1097:     %{_mariner_sources_url}/sisu-build-api.tar.xz
Source1098:     %{_mariner_sources_url}/sisu-inject.tar.xz
Source1099:     %{_mariner_sources_url}/sisu-mojos.tar.xz
Source1100:     %{_mariner_sources_url}/sisu-plexus.tar.xz
Source1101:     %{_mariner_sources_url}/slf4j.tar.xz
Source1102:     %{_mariner_sources_url}/testng.tar.xz
Source1103:     %{_mariner_sources_url}/univocity-parsers.tar.xz
Source1104:     %{_mariner_sources_url}/velocity-engine.tar.xz
Source1105:     %{_mariner_sources_url}/xbean.tar.xz
Source1106:     %{_mariner_sources_url}/xmlunit.tar.xz
Source1107:     %{_mariner_sources_url}/xmvn.tar.xz
Source1108:     %{_mariner_sources_url}/xz-java.tar.xz

Patch0:         0001-Bind-to-OpenJDK-11-for-runtime.patch

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
Provides:       bundled(apache-commons-compress) = 1.20
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
other_sources=$(echo %{sources} | cut -d' ' -f3-)

for source in ${other_sources}
do
  tar -xf "${source}"
done

%patch0 -p1

for patch_path in patches/*/*
do
  package_name="$(echo ${patch_path} | cut -f2 -d/)"
  patch_name="$(echo ${patch_path} | cut -f3 -d/)"
  
  pushd "downstream/${package_name}"
  patch -p1 < "../../patches/${package_name}/${patch_name}"
  popd
done

%build
export LC_ALL=C.utf8
JAVA_HOME=%{java_home} ./mbi.sh build -parallel

%install
JAVA_HOME=%{java_home} ./mbi.sh dist \
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
* Thu Mar 16 2023 Riken Maharjan <rmaharjan@microsoft.com> - 1.5.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
