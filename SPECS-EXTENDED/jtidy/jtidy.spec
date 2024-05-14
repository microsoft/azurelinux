Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package jtidy
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


%define with()          %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
%define without()       %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}
%define bcond_with()    %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
%define bcond_without() %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}
%define _without_maven 1
%define section free
%bcond_with             maven
Name:           jtidy
Version:        8.0
Release:        32%{?dist}
Summary:        HTML syntax checker and pretty printer
License:        BSD
Group:          Development/Libraries/Java
URL:            https://jtidy.sourceforge.net/
# svn export -r813 https://svn.sourceforge.net/svnroot/jtidy/trunk/jtidy/ jtidy
# # bnc#501764
# rm jtidy/src/config/clover.license
Source0:        %{_distro_sources_url}/jtidy-r813.tar.bz2
Source1:        %{name}.jtidy.script
Source2:        build.xml
Source3:        maven-build.properties
Source4:        maven-build.xml
BuildRequires:  ant >= 1.6
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
Requires:       xerces-j2
Requires:       xml-commons-apis
BuildArch:      noarch

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%package javadoc
Summary:        HTML syntax checker and pretty printer
Group:          Development/Libraries/Java

%description javadoc
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%package scripts
Summary:        HTML syntax checker and pretty printer
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}
Requires:       javapackages-tools

%description scripts
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%prep
%setup -q -n %{name}
cp -p %{SOURCE2} %{SOURCE3} %{SOURCE4} .

sed -i 's/charset="ISO-8859-1"/charset="UTF-8"/' maven-build.xml

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
if [ `uname -m` = "ppc64" -o `uname -m` = "ppc64le" ];then
export ANT_OPTS="-Xss2m"
else
export ANT_OPTS="-Xss1m"
fi
export CLASSPATH=$(build-classpath junit slf4j xerces-j2 xml-commons-jaxp-1.3-apis):`pwd`/target/classes:`pwd`/target/test-classes
export OPT_JAR_LIST="junit ant/ant-junit"
%{ant} \
    -Dbuild.sysclasspath=only \
    -Dmaven.mode.offline=true \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    -Dmaven.test.skip=true \
    -Dmaven.test.error.ignore=true \
    package javadoc

%install

# jar
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/jtidy-8.0-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a net.sf.jtidy:%{name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -aL target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

# shell script
install -d -m 0755 %{buildroot}%{_bindir}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# ant.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/ant.d
cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
jtidy xerces-j2 xml-commons-jaxp-1.3-apis
EOF

%files
%defattr(0644,root,root,0755)
%license LICENSE.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif
%config(noreplace) %{_sysconfdir}/ant.d/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0-32
- Updating naming for 3.0 version of Azure Linux.

* Fri Apr 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0-31
- Updating source URL.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0-30
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 8.0-29.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Oct 29 2018 Fridrich Strba <fstrba@suse.com>
- Fix javadoc build
- Package maven artifact
* Fri Sep  8 2017 fstrba@suse.com
- Modified file:
  * maven-build.xml
    + Specify java source and target level 1.6 in order to allow
    building with jdk9
* Thu Dec  5 2013 dvaleev@suse.com
- increase stack size for ppc64le
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Wed Dec 12 2012 dvaleev@suse.com
- increase stack size for ppc64
* Fri Jun 15 2012 mvyskocil@suse.cz
- disable javadoc (workaround for jdk7 build)
* Wed May 20 2009 mvyskocil@suse.cz
- 'fixed bnc#501764: removed clover.license from source tarball'
* Thu May  7 2009 mvyskocil@suse.cz
- Initial packaging of 8.0 in SUSE (from jpp 5.0)
