Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jarjar
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define section free
Name:           jarjar
Version:        1.4
Release:        5%{?dist}
Summary:        Tool to repackage Java libraries
License:        ASL 2.0
Group:          Development/Libraries/Java
Url:            https://github.com/google/jarjar
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/%{name}/%{name}-src-%{version}.zip
Source1:        jarjar.pom
Source2:        jarjar-util.pom
Patch0:         do-not-embed-asm.patch
Patch1:         jarjar-1.4-asm5.patch
BuildRequires:  ant >= 1.6
BuildRequires:  ant-junit >= 1.6
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
BuildRequires:  objectweb-asm >= 5
BuildRequires:  unzip
Requires:       gnu-regexp
Requires:       objectweb-anttask
Requires:       objectweb-asm >= 5
Requires(post): javapackages-tools
Requires(postun): javapackages-tools
BuildArch:      noarch
%if 0
BuildRequires:  maven2
%endif

%description
Jar Jar Links is a utility that makes it easy to repackage Java
libraries and embed them into your own distribution. This is useful for
two reasons: You can easily ship a single jar file with no external
dependencies. You can avoid problems where your library depends on a
specific version of a library, which may conflict with the dependencies
of another library.

%package maven2-plugin
Summary:        Maven2 plugin for %{name}
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Utilities
Requires:       %{name} = %{version}-%{release}
Requires:       maven2

%description maven2-plugin

%{summary}.

%package javadoc
Summary:        Tool to repackage Java libraries
Group:          Development/Libraries/Java

%description javadoc
Jar Jar Links is a utility that repackages Java libraries and embeds
them into a distribution of its own. This is useful for two reasons:
You can easily ship a single jar file with no external dependencies.
You can avoid problems where your library depends on a specific
version of a library, which may conflict with the dependencies of
another library.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
# remove all binary libs
rm -f lib/*.jar
# maven plugin
find . -name JarJarMojo.java -delete

%build
export JAVA_HOME="%{java_home}"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")
pushd lib
ln -sf $(build-classpath objectweb-asm/asm) asm-4.0.jar
ln -sf $(build-classpath objectweb-asm/asm-commons) asm-commons-4.0.jar
ln -sf $(build-classpath ant) ant.jar
popd
export OPT_JAR_LIST="ant/ant-junit junit"
ant \
    -Dcompile.source=8 -Dcompile.target=8 \
    jar jar-util javadoc mojo test

%install
# jars
mkdir -p %{buildroot}%{_javadir}
install -m 644 dist/%{name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}.jar
install -m 644 dist/%{name}-util-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-util.jar
%if 0
install -m 644 dist/%{name}-plugin-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-maven2-plugin.jar
%endif

# poms
mkdir -p %{buildroot}/%{_mavenpomdir}
install -pD -T -m 644 %{SOURCE1} \
  %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
install -pD -T -m 644 %{SOURCE2} \
  %{buildroot}%{_mavenpomdir}/JPP-%{name}-util.pom

# depmaps
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "jarjar:%{name},com.tonicsystems:%{name},com.googlecode.jarjar:%{name},org.gradle.jarjar:%{name}"
%add_maven_depmap JPP-%{name}-util.pom %{name}-util.jar -a "jarjar:%{name}-util,com.tonicsystems:%{name}-util"

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/javadoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files
%license COPYING
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-util.jar
%{_mavenpomdir}/*
%{_datadir}/maven-metadata/%{name}.xml*

%if 0
%files maven2-plugin
%{_javadir}/%{name}-maven2-plugin-%{version}.jar
%{_javadir}/%{name}-maven2-plugin.jar
%endif

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Wed Jan 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4-5
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.4-3.9
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Dec 11 2018 Fridrich Strba <fstrba@suse.com>
- Build against objectweb-asm >= 5 in order to avoid getting stuck
  with a particular asmN package.
* Tue Nov 20 2018 Fridrich Strba <fstrba@suse.com>
- Additional aliases for the jarjar:jarjar artifact
- Added patch:
  * jarjar-1.4-asm5.patch
    + use asm5 api
* Thu Jul 26 2018 jengelh@inai.de
- Use noun phrasing in summaries; trim bias from descriptions.
- Remove one idempotent %%if..%%endif pair.
* Wed Jun 13 2018 fstrba@suse.com
- Upgrade to upstream version 1.4
- Added patch:
  * do-not-embed-asm.patch
    + modify upstream build so that it does not embed the asm
    inside the jarjar jar files
- Require asm5 for build since we want to be able to support java 8
  bytecode
- Build with java source and target 8
* Mon Sep 18 2017 fstrba@suse.com
- Fix build with jdk9: specify java source and target 1.6
- Clean spec file and fix a warning with duplicate waste
* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Tue Sep 10 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Apr 23 2009 mvyskocil@suse.cz
- Initial packaging for SUSE. Version 0.9 (jpp5)
