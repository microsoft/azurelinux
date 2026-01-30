# Exclude automatically generated requires on java interpreter which is not
# owned by any package
%global         __requires_exclude ^/usr/lib/jvm/java

# Don't run OSGi dependency generators on private (bundled) JARs
%global         __requires_exclude_from \\.jar$
%global         __provides_exclude_from \\.jar$

# Generated list of bundled packages
%global         __local_generator_provides cat %{_builddir}/%{buildsubdir}/bundled-provides.txt
%global         __local_generator_path ^%{metadataPath}/.*$

%global         debug_package %{nil}

%global mavenHomePath %{_datadir}/%{name}
%global metadataPath %{mavenHomePath}/maven-metadata
%global artifactsPath %{_javadir}
%global launchersPath %{_libexecdir}/%{name}

Name:           javapackages-bootstrap
Version:        1.14.0
Release:        4%{?dist}
Summary:        A means of bootstrapping Java Packages Tools
# For detailed info see the file javapackages-bootstrap-PACKAGE-LICENSING
License:        ASL 2.0 and ASL 1.1 and (ASL 2.0 or EPL-2.0) and (EPL-2.0 or GPLv2 with exceptions) and MIT and (BSD with advertising) and BSD-3-Clause and EPL-1.0 and EPL-2.0 and CDDL-1.0 and xpp and CC0 and Public Domain
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/fedora-java/javapackages-bootstrap
BuildArch:      noarch

Source0:        https://github.com/fedora-java/javapackages-bootstrap/releases/download/%{version}/javapackages-bootstrap-%{version}.tar.xz

# License breakdown
Source1:        javapackages-bootstrap-PACKAGE-LICENSING
Source2:        ignore.upstream.patch.txt

Source1001:     ant-1.10.14.tar.xz
Source1002:     aopalliance-1.0.tar.xz
Source1003:     apache-pom-30.tar.xz
Source1004:     apiguardian-1.1.2.tar.xz
Source1005:     asm-9.6.tar.xz
Source1006:     assertj-core-3.24.2.tar.xz
Source1007:     bnd-5.2.0.tar.xz
Source1008:     build-helper-maven-plugin-3.4.0.tar.xz
Source1009:     byte-buddy-1.14.10.tar.xz
Source1010:     cdi-2.0.2.tar.xz
Source1011:     cglib-3.3.0.tar.xz
Source1012:     common-annotations-api-1.3.5.tar.xz
Source1013:     commons-beanutils-1.9.4.tar.xz
Source1014:     commons-cli-1.5.0.tar.xz
Source1015:     commons-codec-1.16.0.tar.xz
Source1016:     commons-collections-3.2.2.tar.xz
Source1017:     commons-compress-jpb-1.23.0.tar.xz
Source1018:     commons-io-2.13.0.tar.xz
Source1019:     commons-jxpath-jpb2-1.3.tar.xz
Source1020:     commons-lang-3.13.0.tar.xz
Source1021:     commons-logging-1.2.tar.xz
Source1022:     commons-parent-pom-65.tar.xz
Source1023:     cup-0.11b.tar.xz
Source1024:     disruptor-3.4.4.tar.xz
Source1025:     easymock-4.3.tar.xz
Source1026:     extra-enforcer-rules-1.7.0.tar.xz
Source1027:     felix-parent-pom-7.tar.xz
Source1028:     felix-utils-1.11.8.tar.xz
Source1029:     fusesource-pom-1.12.tar.xz
Source1030:     guava-31.1.tar.xz
Source1031:     guice-5.1.0.tar.xz
Source1032:     hamcrest-2.2.tar.xz
Source1033:     httpcomponents-client-4.5.13.tar.xz
Source1034:     httpcomponents-core-4.4.13.tar.xz
Source1035:     httpcomponents-parent-pom-13.tar.xz
Source1036:     injection-api-1.0.5.tar.xz
Source1037:     jaf-api-2.1.2.tar.xz
Source1038:     jansi-2.4.0.tar.xz
Source1039:     javacc-maven-plugin-3.0.1.tar.xz
Source1040:     javacc-7.0.13.tar.xz
Source1041:     javaparser-3.25.7.tar.xz
Source1042:     jcommander-1.82.tar.xz
Source1043:     jctools-4.0.1.tar.xz
Source1044:     jdom-1.1.3.tar.xz
Source1045:     jdom2-2.0.6.1.tar.xz
Source1046:     jflex-1.7.0.tar.xz
Source1047:     jsoup-1.16.1.tar.xz
Source1048:     jsr-305-3.0.2.tar.xz
Source1049:     junit4-4.13.2.tar.xz
Source1050:     junit5-5.10.0.tar.xz
Source1051:     log4j-2.20.0.tar.xz
Source1052:     mail-api-2.1.2.tar.xz
Source1053:     maven-antrun-plugin-3.1.0.tar.xz
Source1054:     maven-apache-resources-1.5.tar.xz
Source1055:     maven-archiver-3.6.0.tar.xz
Source1056:     maven-artifact-transfer-0.13.1.tar.xz
Source1057:     maven-assembly-plugin-3.6.0.tar.xz
Source1058:     maven-bundle-plugin-5.1.9.tar.xz
Source1059:     maven-common-artifact-filters-3.3.2.tar.xz
Source1060:     maven-compiler-plugin-3.11.0.tar.xz
Source1061:     maven-dependency-analyzer-1.13.2.tar.xz
Source1062:     maven-dependency-plugin-3.6.0.tar.xz
Source1063:     maven-dependency-tree-3.2.1.tar.xz
Source1064:     maven-enforcer-3.3.0.tar.xz
Source1065:     maven-file-management-3.1.0.tar.xz
Source1066:     maven-filtering-3.3.1.tar.xz
Source1067:     maven-jar-plugin-3.3.0.tar.xz
Source1068:     maven-parent-pom-40.tar.xz
Source1069:     maven-plugin-testing-3.3.0.tar.xz
Source1070:     maven-plugin-tools-jpb-3.9.0.tar.xz
Source1071:     maven-remote-resources-plugin-3.1.0.tar.xz
Source1072:     maven-resolver-1.9.15.tar.xz
Source1073:     maven-resources-plugin-3.3.1.tar.xz
Source1074:     maven-shared-incremental-1.1.tar.xz
Source1075:     maven-shared-io-3.0.0.tar.xz
Source1076:     maven-shared-utils-3.4.2.tar.xz
Source1077:     maven-source-plugin-3.3.0.tar.xz
Source1078:     maven-surefire-3.1.2.tar.xz
Source1079:     maven-verifier-2.0.0~M1.tar.xz
Source1080:     maven-wagon-3.5.3.tar.xz
Source1081:     maven-3.9.4.tar.xz
Source1082:     mockito-3.7.13.tar.xz
Source1083:     modello-2.1.1.tar.xz
Source1084:     moditect-1.1.0.tar.xz
Source1085:     modulemaker-maven-plugin-1.9.tar.xz
Source1086:     mojo-parent-pom-76.tar.xz
Source1087:     objenesis-3.3.tar.xz
Source1088:     opentest4j-1.3.0.tar.xz
Source1089:     osgi-annotation-8.1.0.tar.xz
Source1090:     osgi-cmpn-7.0.0.tar.xz
Source1091:     osgi-core-8.0.0.tar.xz
Source1092:     plexus-archiver-jpb-4.8.0.tar.xz
Source1093:     plexus-build-api-0.0.7.tar.xz
Source1094:     plexus-cipher-2.0.tar.xz
Source1095:     plexus-classworlds-2.7.0.tar.xz
Source1096:     plexus-compiler-2.13.0.tar.xz
Source1097:     plexus-components-pom-14.1.tar.xz
Source1098:     plexus-containers-2.1.1.tar.xz
Source1099:     plexus-interpolation-1.26.tar.xz
Source1100:     plexus-io-3.4.1.tar.xz
Source1101:     plexus-languages-1.1.2.tar.xz
Source1102:     plexus-pom-14.tar.xz
Source1103:     plexus-resources-1.2.0.tar.xz
Source1104:     plexus-sec-dispatcher-2.0.tar.xz
Source1105:     plexus-utils.tar-3.5.1.xz
Source1106:     qdox.tar-2.0.3.xz
Source1107:     servlet-api-4.0.3.tar.xz
Source1108:     sisu-inject-0.3.5.tar.xz
Source1109:     sisu-mojos-0.3.5.tar.xz
Source1110:     sisu-plexus-0.3.5.tar.xz
Source1111:     slf4j-1.7.36.tar.xz
Source1112:     testng-7.8.0.tar.xz
Source1113:     univocity-parsers-2.9.1.tar.xz
Source1114:     velocity-engine-2.3.tar.xz
Source1115:     xbean-4.23.tar.xz
Source1116:     xmlunit-2.9.1.tar.xz
Source1118:     xmvn-jpb-4.2.0.tar.xz
Source1119:     xmvn-generator-1.2.1.tar.xz
Source1120:     xz-java-1.9.tar.xz

Patch0:       CVE-2024-25710.patch
Patch1:       CVE-2026-24400.patch

Provides:     bundled(ant) = 1.10.14
Provides:     bundled(aopalliance) = 1.0
Provides:     bundled(apache-pom) = 30
Provides:     bundled(apiguardian) = 1.1.2
Provides:     bundled(asm) = 9.6
Provides:     bundled(assertj-core) = 3.24.2
Provides:     bundled(bnd) = 5.2.0
Provides:     bundled(build-helper-maven-plugin) = 3.4.0
Provides:     bundled(byte-buddy) = 1.14.10
Provides:     bundled(cdi) = 2.0.2
Provides:     bundled(cglib) = 3.3.0
Provides:     bundled(common-annotations-api) = 1.3.5
Provides:     bundled(commons-beanutils) = 1.9.4
Provides:     bundled(commons-cli) = 1.5.0
Provides:     bundled(commons-codec) = 1.16.0
Provides:     bundled(commons-collections) = 3.2.2
Provides:     bundled(commons-compress) = 1.23.0
Provides:     bundled(commons-io) = 2.13.0
Provides:     bundled(commons-jxpath) = 1.3
Provides:     bundled(commons-lang) = 3.13.0
Provides:     bundled(commons-logging) = 1.2
Provides:     bundled(commons-parent-pom) = 65
Provides:     bundled(cup) = 0.11b
Provides:     bundled(disruptor) = 3.4.4
Provides:     bundled(easymock) = 4.3
Provides:     bundled(extra-enforcer-rules) = 1.7.0
Provides:     bundled(felix-parent-pom) = 7
Provides:     bundled(felix-utils) = 1.11.8
Provides:     bundled(fusesource-pom) = 1.12
Provides:     bundled(guava) = 31.1
Provides:     bundled(guice) = 5.1.0
Provides:     bundled(hamcrest) = 2.2
Provides:     bundled(httpcomponents-client) = 4.5.13
Provides:     bundled(httpcomponents-core) = 4.4.13
Provides:     bundled(httpcomponents-parent-pom) = 13
Provides:     bundled(injection-api) = 1.0.5
Provides:     bundled(jaf-api) = 2.1.2
Provides:     bundled(jansi) = 2.4.0
Provides:     bundled(javacc-maven-plugin) = 3.0.1
Provides:     bundled(javacc) = 7.0.13
Provides:     bundled(javaparser) = 3.25.7
Provides:     bundled(jcommander) = 1.82
Provides:     bundled(jctools) = 4.0.1
Provides:     bundled(jdom) = 1.1.3
Provides:     bundled(jdom2) = 2.0.6.1
Provides:     bundled(jflex) = 1.7.0
Provides:     bundled(jsoup) = 1.16.1
Provides:     bundled(jsr-305-) = 3.0.2
Provides:     bundled(junit4-) = 4.13.2
Provides:     bundled(junit5) = 5.10.0
Provides:     bundled(log4j) = 2.20.0
Provides:     bundled(mail-api) = 2.1.2
Provides:     bundled(maven-antrun-plugin) = 3.1.0
Provides:     bundled(maven-apache-resources) = 1.5
Provides:     bundled(maven-archiver) = 3.6.0
Provides:     bundled(maven-artifact-transfer) = 0.13.1
Provides:     bundled(maven-assembly-plugin) = 3.6.0
Provides:     bundled(maven-bundle-plugin) = 5.1.9
Provides:     bundled(maven-common-artifact-filters) = 3.3.2
Provides:     bundled(maven-compiler-plugin) = 3.11.0
Provides:     bundled(maven-dependency-analyzer) = 1.13.2
Provides:     bundled(maven-dependency-plugin) = 3.6.0
Provides:     bundled(maven-dependency-tree) = 3.2.1
Provides:     bundled(maven-enforcer) = 3.3.0
Provides:     bundled(maven-file-management) = 3.1.0
Provides:     bundled(maven-filtering) = 3.3.1
Provides:     bundled(maven-jar-plugin) = 3.3.0
Provides:     bundled(maven-parent-pom) = 40
Provides:     bundled(maven-plugin-testing) = 3.3.0
Provides:     bundled(maven-plugin-tools) = 3.9.0
Provides:     bundled(maven-remote-resources-plugin) = 3.1.0
Provides:     bundled(maven-resolver) = 1.9.15
Provides:     bundled(maven-resources-plugin) = 3.3.1
Provides:     bundled(maven-shared-incremental) = 1.1
Provides:     bundled(maven-shared-io) = 3.0.0
Provides:     bundled(maven-shared-utils) = 3.4.2
Provides:     bundled(maven-source-plugin) = 3.3.0
Provides:     bundled(maven-surefire) = 3.1.2
Provides:     bundled(maven-verifier) = 2.0.0~M1
Provides:     bundled(maven-wagon) = 3.5.3
Provides:     bundled(maven) = 3.9.4
Provides:     bundled(mockito) = 3.7.13
Provides:     bundled(modello) = 2.1.1
Provides:     bundled(moditect) = 1.1.0
Provides:     bundled(modulemaker-maven-plugin) = 1.9
Provides:     bundled(mojo-parent-pom) = 76
Provides:     bundled(objenesis) = 3.3
Provides:     bundled(opentest4j) = 1.3.0
Provides:     bundled(osgi-annotation) = 8.1.0
Provides:     bundled(osgi-cmpn) = 7.0.0
Provides:     bundled(osgi-core) = 8.0.0
Provides:     bundled(plexus-archiver) = 4.8.0
Provides:     bundled(plexus-build-api) = 0.0.7
Provides:     bundled(plexus-cipher) = 2.0
Provides:     bundled(plexus-classworlds) = 2.7.0
Provides:     bundled(plexus-compiler) = 2.13.0
Provides:     bundled(plexus-components-pom) = 14.1
Provides:     bundled(plexus-containers) = 2.1.1
Provides:     bundled(plexus-interpolation) = 1.26
Provides:     bundled(plexus-io) = 3.4.1
Provides:     bundled(plexus-languages) = 1.1.2
Provides:     bundled(plexus-pom) = 14
Provides:     bundled(plexus-resources) = 1.2.0
Provides:     bundled(plexus-sec-dispatcher) = 2.0
Provides:     bundled(plexus-utils) = 3.5.1
Provides:     bundled(qdox) = 2.0.3
Provides:     bundled(servlet-api) = 4.0.3
Provides:     bundled(sisu-inject) = 0.3.5
Provides:     bundled(sisu-mojos) = 0.3.5
Provides:     bundled(sisu-plexus) = 0.3.5
Provides:     bundled(slf4j) = 1.7.36
Provides:     bundled(testng) = 7.8.0
Provides:     bundled(univocity-parsers) = 2.9.1
Provides:     bundled(velocity-engine) = 2.3
Provides:     bundled(xbean) = 4.23
Provides:     bundled(xmlunit) = 2.9.1
Provides:     bundled(xmvn) = 4.2.0
Provides:     bundled(xmvn-generator) = 1.2.1
Provides:     bundled(xz-java) = 1.9

BuildRequires:  byaccj
BuildRequires:  msopenjdk-17
BuildRequires:  javapackages-generators
BuildRequires:  java-devel
BuildRequires:  rpm-devel
BuildRequires:  jurand

Requires:       bash
Requires:       coreutils
Requires:       msopenjdk-17
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

pushd "downstream/commons-compress"
%patch -P 0 -p1
popd

pushd "downstream/assertj-core"
%patch -P 1 -p1
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
    #patch -p1 < "../../patches/${package_name}/${patch_name}"
    find . -name '*.java' -exec sed -i 's/\r//' {} +
    sed 's/\r//' "../../patches/${package_name}/${patch_name}" | patch -p1
  fi  
  popd
done


%build
export LC_ALL=en_US.UTF-8 
export JAVA_HOME=$(find /usr/lib/jvm -name "*openjdk*")
echo $JAVA_HOME
./mbi.sh build -parallel

%install
export JAVA_HOME=$(find /usr/lib/jvm -name "*openjdk*")
./mbi.sh dist \
  -javaCmdPath=%{java_home}/bin/java \
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

 
install -D -p -m 644 downstream/xmvn-generator/src/main/lua/xmvn-generator.lua %{buildroot}%{_rpmluadir}/%{name}-generator.lua
install -D -p -m 644 downstream/xmvn-generator/src/main/rpm/macros.xmvngen %{buildroot}%{_rpmmacrodir}/macros.jpbgen
install -D -p -m 644 downstream/xmvn-generator/src/main/rpm/macros.xmvngenhook %{buildroot}%{_sysconfdir}/rpm/macros.jpbgenhook
install -D -p -m 644 downstream/xmvn-generator/src/main/rpm/xmvngen.attr %{buildroot}%{_fileattrsdir}/jpbgen.attr

echo '
%%__xmvngen_debug 1
%%__xmvngen_libjvm %{java_home}/lib/server/libjvm.so
%%__xmvngen_classpath %{artifactsPath}/%{name}/xmvn-generator.jar:%{artifactsPath}/%{name}/asm.jar:%{artifactsPath}/%{name}/commons-compress.jar
%%__xmvngen_provides_generators org.fedoraproject.xmvn.generator.jpms.JPMSGeneratorFactory
%%__xmvngen_requires_generators %%{nil}
%%__xmvngen_post_install_hooks org.fedoraproject.xmvn.generator.transformer.TransformerHookFactory
%%jpb_env PATH=/usr/libexec/javapackages-bootstrap:$PATH
' >%{buildroot}%{_rpmmacrodir}/macros.jpbgen

# by default it sets JAVA_HOME to /usr/lib/jvm/java-11-openjdk
sed -i 's|/usr/lib/jvm/java-17|%{java_home}|' %{buildroot}%{_datadir}/%{name}/bin/mvn
sed -i 's|/usr/lib/jvm/java-17|%{java_home}|' %{buildroot}%{launchersPath}/xmvn-install

sed -i s/xmvn-generator/%{name}-generator/ %{buildroot}%{_sysconfdir}/rpm/macros.jpbgenhook
sed -i s/xmvn-generator/%{name}-generator/ %{buildroot}%{_fileattrsdir}/jpbgen.attr
sed -i s/_xmvngen_/_jpbgen_/ %{buildroot}%{_fileattrsdir}/jpbgen.attr

%check
%{buildroot}%{launchersPath}/xmvn --version

%files
%{mavenHomePath}
%{metadataPath}/*
%{artifactsPath}/*
%{launchersPath}/*
%{_rpmluadir}/*
%{_rpmmacrodir}/*
%{_fileattrsdir}/*
%{_sysconfdir}/rpm/*

%license %{_licensedir}/%{name}
%doc README.md
%doc AUTHORS

%changelog
* Fri Jan 30 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.14.0-4
- Add patch for CVE-2026-24400

* Fri May 16 2025 Sudipta Pandit <sudpandit@microsoft.com> - 1.14.0-3
- Add backported patch for CVE-2024-25710

* Thu Mar 21 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.14.0-2
- Change JAVA_HOME for xmvn to be msopenjdk location.
- Upgrade to 1.14.0 - azl 3.0
- Changes from Fedora 39 (license: MIT).

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
