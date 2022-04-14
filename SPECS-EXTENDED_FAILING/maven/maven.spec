#need to disable debuginfo till we bring in x11 deps
%define debug_package %{nil}

Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven
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


%global bundled_slf4j_version 1.7.25
%global homedir %{_datadir}/%{name}%{?maven_version_suffix}
%global confdir %{_sysconfdir}/%{name}%{?maven_version_suffix}
%bcond_with  logback
Name:           maven
Version:        3.6.3
Release:        3%{?dist}
Summary:        Java project management and project comprehension tool
# maven itself is ASL 2.0
# bundled slf4j is MIT
License:        Apache-2.0 AND MIT
Group:          Development/Tools/Building
URL:            https://maven.apache.org/
Source0:        http://archive.apache.org/dist/%{name}/%{name}-3/%{version}/source/apache-%{name}-%{version}-src.tar.gz
Source1:        maven-bash-completion
Source2:        mvn.1
Source10:       apache-%{name}-%{version}-build.tar.xz
Patch1:         0001-Adapt-mvn-script.patch
# Downstream-specific, avoids dependency on logback
# Used only when %%without logback is in effect
Patch2:         0002-Invoke-logback-via-reflection.patch
Patch4:         0004-Use-non-shaded-HTTP-wagon.patch
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-lang3
BuildRequires:  apache-commons-logging
BuildRequires:  atinject
BuildRequires:  cdi-api
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  geronimo-annotation-1_0-api
BuildRequires:  google-guice
BuildRequires:  guava20
BuildRequires:  hawtjni-runtime
BuildRequires:  httpcomponents-client
BuildRequires:  httpcomponents-core
BuildRequires:  jansi
BuildRequires:  jansi-native
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jcl-over-slf4j
BuildRequires:  jdom2
BuildRequires:  maven-resolver-api
BuildRequires:  maven-resolver-connector-basic
BuildRequires:  maven-resolver-impl
BuildRequires:  maven-resolver-spi
BuildRequires:  maven-resolver-transport-wagon
BuildRequires:  maven-resolver-util
BuildRequires:  maven-shared-utils
BuildRequires:  maven-wagon-file
BuildRequires:  maven-wagon-http
BuildRequires:  maven-wagon-http-shared
BuildRequires:  maven-wagon-provider-api
BuildRequires:  modello >= 1.10
BuildRequires:  objectweb-asm
BuildRequires:  plexus-cipher
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-cli
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-interpolation
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-sec-dispatcher
BuildRequires:  plexus-utils
BuildRequires:  qdox
BuildRequires:  sisu-inject
BuildRequires:  sisu-plexus
BuildRequires:  slf4j
BuildRequires:  slf4j-sources
BuildRequires:  unix2dos
BuildRequires:  xbean
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  xmvn-subst
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
Requires:       %{name}-lib = %{version}-%{release}
Requires(post): update-alternatives
Requires(postun): update-alternatives

# maven-lib cannot be noarch because of the position of jansi-native.jar
#BuildArch:      noarch
%if %{with logback}
BuildRequires:  mvn(ch.qos.logback:logback-classic)
%endif

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

%package        lib
Summary:        Core part of Maven
# Require full javapackages-tools since maven-script uses
# /usr/share/java-utils/java-functions
# XMvn does generate auto-requires, but explicit requires are still
# needed because some symlinked JARs are not present in Maven POMs or
# their dependency scope prevents them from being added automatically
# by XMvn.  It would be possible to explicitly specify only
# dependencies which are not generated automatically, but adding
# everything seems to be easier.
Group:          Development/Tools/Building
Requires:       aopalliance
Requires:       apache-commons-cli
Requires:       apache-commons-codec
Requires:       apache-commons-io
Requires:       apache-commons-lang3
Requires:       apache-commons-logging
Requires:       atinject
Requires:       cdi-api
Requires:       cglib
Requires:       geronimo-annotation-1_0-api
Requires:       google-guice
Requires:       guava20
Requires:       hawtjni-runtime
Requires:       httpcomponents-client
Requires:       httpcomponents-core
Requires:       jansi
Requires:       jansi-native
Requires:       javapackages-tools
Requires:       jcl-over-slf4j
Requires:       junit
Requires:       maven-resolver-api
Requires:       maven-resolver-connector-basic
Requires:       maven-resolver-impl
Requires:       maven-resolver-spi
Requires:       maven-resolver-transport-wagon
Requires:       maven-resolver-util
Requires:       maven-shared-utils
Requires:       maven-wagon-file
Requires:       maven-wagon-http
Requires:       maven-wagon-http-shared
Requires:       maven-wagon-provider-api
Requires:       objectweb-asm
Requires:       plexus-cipher
Requires:       plexus-classworlds
Requires:       plexus-containers-component-annotations
Requires:       plexus-interpolation
Requires:       plexus-sec-dispatcher
Requires:       plexus-utils
Requires:       sisu-inject
Requires:       sisu-plexus
Requires:       slf4j
# Maven upstream uses patched version of SLF4J.  They unpack
# slf4j-simple-sources.jar, apply non-upstreamable, Maven-specific
# patch (using a script written in Groovy), compile and package as
# maven-slf4j-provider.jar, together with Maven-specific additions.
Provides:       bundled(slf4j) = %{bundled_slf4j_version}
# This package might be installed on a system, since it used to be
# produced by the binary maven repackaging in some repositories.
# This Obsoletes will allow a clean upgrade.
Obsoletes:      %{name}-jansi
# If XMvn is part of the same RPM transaction then it should be
# installed first to avoid triggering rhbz#1014355.
OrderWithRequires: xmvn-minimal

%description    lib
Core part of Apache Maven that can be used as a library.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML
BuildArch:      noarch

%description    javadoc
%{summary}.

%prep
%setup -q -n apache-%{name}-%{version} -a10

%patch1 -p1
%patch4 -p1

# not really used during build, but a precaution
find -name '*.jar' -not -path '*/test/*' -delete
find -name '*.class' -delete
find -name '*.bat' -delete

sed -i 's:\r::' apache-maven/src/conf/settings.xml

# Downloads dependency licenses from the Internet and aggregates them.
# We already ship the licenses in their respective packages.
rm apache-maven/src/main/appended-resources/META-INF/LICENSE.vm

# Disable plugins which are not useful for us
%pom_remove_plugin -r :animal-sniffer-maven-plugin
%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :maven-site-plugin
%pom_remove_plugin -r :buildnumber-maven-plugin
sed -i "
/buildNumber=/ {
  s/=.*/=SUSE %{version}-%{release}/
}
/timestamp=/ d
" `find -name build.properties`
sed -i "s/version=.*/version=%{version}/" `find -name build.properties`
sed -i "s/distributionId=.*/distributionId=apache-maven/" `find -name build.properties`
sed -i "s/distributionShortName=.*/distributionShortName=Maven/" `find -name build.properties`
sed -i "s/distributionName=.*/distributionName=Apache\ Maven/" `find -name build.properties`

%{mvn_package} :apache-maven __noinstall

%if %{without logback}
%pom_remove_dep -r :logback-classic
%patch2 -p1
%endif

%{mvn_alias} :maven-resolver-provider :maven-aether-provider

# xmvn depends on this version, so we want to avoid duplicate apache-commons-lang3 jars in xmvn
%pom_xpath_set pom:project/pom:properties/pom:commonsLangVersion "3.8.1"

%build
mkdir -p lib
build-jar-repository -s lib \
    apache-commons-lang3 \
    atinject \
    commons-cli \
    commons-io \
    guava20/guava-10.0 \
    guice/google-guice-no_aop \
    jdom2/jdom2 \
    maven-resolver/maven-resolver-api \
    maven-resolver/maven-resolver-impl \
    maven-resolver/maven-resolver-spi \
    maven-resolver/maven-resolver-util \
    maven-shared-utils/maven-shared-utils \
    maven-wagon/provider-api \
    objectweb-asm/asm-commons \
    objectweb-asm/asm \
    org.eclipse.sisu.inject \
    org.eclipse.sisu.plexus \
    plexus-classworlds \
    plexus/cli \
    plexus-containers/plexus-component-annotations \
    plexus/interpolation \
    plexus-metadata-generator \
    plexus/plexus-cipher \
    plexus/plexus-sec-dispatcher \
    plexus/utils \
    qdox \
    slf4j/api \
    slf4j/simple \
    xbean/xbean-reflect
ln -s $(build-classpath slf4j/slf4j-simple-sources) lib/
%{ant} \
  -Dtest.skip=true \
  package javadoc

%{mvn_artifact} pom.xml
mkdir -p target/site/apidocs
for i in \
    artifact \
    model \
    plugin-api \
    builder-support \
    model-builder \
    settings \
    settings-builder \
    repository-metadata \
    resolver-provider \
    core \
    slf4j-provider \
    embedder \
    compat; do
  cp -r %{name}-${i}/target/site/apidocs target/site/apidocs/%{name}-${i}
  %{mvn_artifact} %{name}-${i}/pom.xml %{name}-${i}/target/%{name}-${i}-%{version}.jar
done

%install
%mvn_install
%fdupes %{buildroot}%{_javadocdir}

install -d -m 755 %{buildroot}%{homedir}/boot
install -d -m 755 %{buildroot}%{confdir}
install -d -m 755 %{buildroot}%{_datadir}/bash-completion/completions/

cp -a apache-maven/src/{bin,conf,lib} %{buildroot}%{homedir}/
chmod +x %{buildroot}%{homedir}/bin/*
unix2dos %{buildroot}%{homedir}/bin/*.cmd %{buildroot}%{homedir}/bin/*.conf
chmod -x %{buildroot}%{homedir}/bin/*.cmd %{buildroot}%{homedir}/bin/*.conf

# Transitive deps of wagon-http, missing because of unshading
build-jar-repository -p %{buildroot}%{homedir}/lib \
    aopalliance \
    objectweb-asm/asm \
    cdi-api/cdi-api \
    cglib/cglib \
    commons-cli \
    commons-codec \
    commons-io \
    apache-commons-lang3 \
    commons-logging \
    guava20/guava-10.0 \
    guice/google-guice-no_aop \
    hamcrest/core \
    hawtjni/hawtjni-runtime \
    httpcomponents/httpclient \
    httpcomponents/httpcore \
    jansi/jansi \
    jansi-native/jansi-linux \
    jansi-native/jansi-native \
    atinject \
    slf4j/jcl-over-slf4j \
    geronimo-annotation-1.0-api \
    junit \
    maven-resolver/maven-resolver-api \
    maven-resolver/maven-resolver-connector-basic \
    maven-resolver/maven-resolver-impl \
    maven-resolver/maven-resolver-spi \
    maven-resolver/maven-resolver-transport-wagon \
    maven-resolver/maven-resolver-util \
    maven-shared-utils/maven-shared-utils \
    maven-wagon/http-shared \
    org.eclipse.sisu.inject \
    org.eclipse.sisu.plexus \
    plexus/plexus-cipher \
    plexus-containers/plexus-component-annotations \
    plexus/interpolation \
    plexus/plexus-sec-dispatcher \
    plexus/utils \
    slf4j/api \
    maven-wagon/file \
    maven-wagon/http \
    maven-wagon/provider-api

cp %{buildroot}%{_javadir}/%{name}/*.jar %{buildroot}%{homedir}/lib/

build-jar-repository -p %{buildroot}%{homedir}/boot \
    plexus-classworlds

xmvn-subst -R %{buildroot} -s %{buildroot}%{homedir}

install -p -m 644 %{SOURCE2} %{buildroot}%{homedir}/bin/
gzip -9 %{buildroot}%{homedir}/bin/mvn.1
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/mvn%{?maven_version_suffix}
mv %{buildroot}%{homedir}/bin/m2.conf %{buildroot}%{_sysconfdir}/m2%{?maven_version_suffix}.conf
ln -sf %{_sysconfdir}/m2%{?maven_version_suffix}.conf %{buildroot}%{homedir}/bin/m2.conf
mv %{buildroot}%{homedir}/conf/settings.xml %{buildroot}%{confdir}/
ln -sf %{confdir}/settings.xml %{buildroot}%{homedir}/conf/settings.xml
mv %{buildroot}%{homedir}/conf/logging %{buildroot}%{confdir}/
ln -sf %{confdir}/logging %{buildroot}%{homedir}/conf

# Ghosts for alternatives
install -d -m 755 %{buildroot}%{_bindir}/
install -d -m 755 %{buildroot}%{_mandir}/man1/
touch %{buildroot}%{_bindir}/{mvn,mvnDebug}
touch %{buildroot}%{_mandir}/man1/{mvn,mvnDebug}.1

%post
update-alternatives --install %{_bindir}/mvn mvn %{homedir}/bin/mvn %{?maven_alternatives_priority}0 \
--slave %{_bindir}/mvnDebug mvnDebug %{homedir}/bin/mvnDebug \
--slave %{_mandir}/man1/mvn.1.gz mvn1 %{homedir}/bin/mvn.1.gz \
--slave %{_mandir}/man1/mvnDebug.1.gz mvnDebug1 %{homedir}/bin/mvn.1.gz \

%postun
if [ $1 -eq 0 ]; then
  update-alternatives --remove mvn %{homedir}/bin/mvn
fi

%files lib -f .mfiles
%doc README.md
%license LICENSE NOTICE
%{homedir}
%dir %{confdir}
%dir %{confdir}/logging
%config(noreplace) %{_sysconfdir}/m2%{?maven_version_suffix}.conf
%config(noreplace) %{confdir}/settings.xml
%config(noreplace) %{confdir}/logging/simplelogger.properties

%files
%ghost %{_bindir}/mvn
%ghost %{_bindir}/mvnDebug
%{_datadir}/bash-completion
%ghost %{_mandir}/man1/mvn.1.gz
%ghost %{_mandir}/man1/mvnDebug.1.gz

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.3-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Dec 04 2020 Joe Schmitt <joschmit@microsoft.com> - 1:3.6.3-2.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Change %%post and %%postun dependency on aaa_base to update-alternatives.
- Turn off debug package.

* Sun Mar  1 2020 Fridrich Strba <fstrba@suse.com>
- Let maven-lib obsolete maven-jansi
* Fri Feb  7 2020 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 3.6.3
- Modified patches:
  * 0002-Invoke-logback-via-reflection.patch
  * 0004-Use-non-shaded-HTTP-wagon.patch
    + Adapt to changed line endings
* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 3.6.2
- Modified patch:
  * 0002-Invoke-logback-via-reflection.patch
    + adapt to changed context
- Removed patch:
  * 0003-Revert-MNG-6335-Update-Mockito-to-2.12.0.patch
    + we don't need this patch, since we are not running tests
    by default
- Added patch:
  * 0004-Use-non-shaded-HTTP-wagon.patch
    + we don't use/distribute shared wagon-http
* Mon Apr  1 2019 Jan Engelhardt <jengelh@inai.de>
- Adjust RPM groups. Avoid bashisms in %%postun.
* Fri Mar 29 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven 3.5.4
- Generate and customize ant build files
