Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache-ivy
#
# Copyright (c) 2019 SUSE LLC
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


%bcond_without  ssh
%bcond_without  vfs
Name:           apache-ivy
Version:        2.4.0
Release:        7%{?dist}
Summary:        Java-based dependency manager
License:        Apache-2.0
Group:          Development/Tools/Building
URL:            http://ant.apache.org/ivy/
Source0:        %{name}-%{version}-src.tar.gz
Source1:        ivy.1
Source2:        http://repo1.maven.org/maven2/org/apache/ivy/ivy/%{version}/ivy-%{version}.pom
Patch0:         apache-ivy-2.4.0-jdk9.patch
Patch1:         apache-ivy-global-settings.patch
Patch2:         port-to-bc-1.52.patch
BuildRequires:  ant
BuildRequires:  bouncycastle-pg
BuildRequires:  commons-httpclient
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsch
BuildRequires:  oro
Provides:       ivy = %{version}-%{release}
Obsoletes:      ivy < %{version}-%{release}
BuildArch:      noarch
%if %{with vfs}
BuildRequires:  apache-commons-vfs2
%endif
%if %{with ssh}
BuildRequires:  jsch-agent-proxy-connector-factory
BuildRequires:  jsch-agent-proxy-core
BuildRequires:  jsch-agent-proxy-jsch
%endif

%description
Apache Ivy is a tool for managing (recording, tracking, resolving and
reporting) project dependencies.  It is designed as process agnostic and is
not tied to any methodology or structure. while available as a standalone
tool, Apache Ivy works particularly well with Apache Ant providing a number
of powerful Ant tasks ranging from dependency resolution to dependency
reporting and publication.

%package javadoc
Summary:        API Documentation for ivy
Group:          Documentation/HTML

%description javadoc
JavaDoc documentation for %{name}

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

cp %{SOURCE2} pom.xml

%pom_remove_parent .

# Remove prebuilt documentation
rm -rf doc build/doc

# Port from commons-vfs 1.x to 2.x
%if %{with vfs}
sed -i "s/commons.vfs/&2/" {src,test}/java/org/apache/ivy/plugins/repository/vfs/*
%else
sed -i /commons-vfs/d ivy.xml
sed '/vfs.*=.*org.apache.ivy.plugins.resolver.VfsResolver/d' -i \
        src/java/org/apache/ivy/core/settings/typedef.properties
rm -rf src/java/org/apache/ivy/plugins/repository/vfs
rm -rf src/java/org/apache/ivy/plugins/resolver/VfsResolver.java
%endif

%if %{without ssh}
rm -r src/java/org/apache/ivy/plugins/repository/{ssh,sftp}
rm src/java/org/apache/ivy/plugins/resolver/*{Ssh,SFTP}*.java
%endif

%build
# Craft class path
mkdir -p lib
build-jar-repository lib ant ant/ant-nodeps oro jsch commons-httpclient bcprov bcpg
export CLASSPATH=$(build-classpath ant ant/ant-nodeps oro jsch commons-httpclient bcprov bcpg)
%if %{with vfs}
build-jar-repository lib commons-vfs2
export CLASSPATH=${CLASSPATH}:$(build-classpath commons-vfs2)
%endif
%if %{with ssh}
build-jar-repository lib jsch.agentproxy.core \
                         jsch.agentproxy.connector-factory \
                         jsch.agentproxy.jsch
export CLASSPATH=${CLASSPATH}:$(build-classpath jsch.agentproxy.core jsch.agentproxy.connector-factory jsch.agentproxy.jsch)
%endif

# Build
ant -Dtarget.ivy.version=%{version} -Dbundle.version=%{version} /localivy /offline jar javadoc

%install
# Code
install -d %{buildroot}%{_javadir}/%{name}
install -p -m644 build/artifact/jars/ivy.jar %{buildroot}%{_javadir}/ivy.jar
ln -sf ../ivy.jar %{buildroot}%{_javadir}/%{name}/ivy.jar

install -d -m 0755 %{buildroot}/%{_mavenpomdir}/
install -m 0644 pom.xml %{buildroot}/%{_mavenpomdir}/JPP-ivy.pom
# Maven depmap
%add_maven_depmap JPP-ivy.pom ivy.jar

# API Documentation
install -d %{buildroot}%{_javadocdir}/%{name}
cp -rp build/doc/reports/api/. %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

# Command line script
MAIN_CLASS=`sed -rn 's/^Main-Class: (.*)$/\1/gp' META-INF/MANIFEST.MF | tr -d '
'`
%jpackage_script "${MAIN_CLASS}" "" "" ant:ant/ant-nodeps:ivy:oro:jsch:commons-httpclient ivy

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ivy" > %{buildroot}%{_sysconfdir}/ant.d/%{name}

# Man page
install -d %{buildroot}%{_mandir}/man1
install %{SOURCE1} %{buildroot}%{_mandir}/man1/ivy.1

%files -f .mfiles
%license LICENSE NOTICE
%doc README
%config %{_sysconfdir}/ant.d/%{name}
%{_javadir}/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_mandir}/man1/*

%files javadoc
%{_javadocdir}/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.0-7
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.4.0-6.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Dec 10 2019 Fridrich Strba <fstrba@suse.com>
- Specify bundle.version in order to avoid unexpanded macro
* Tue Sep 24 2019 Fridrich Strba <fstrba@suse.com>
- Build the bouncycastle signer plugin since bcpg is now present
- Added patch:
  * port-to-bc-1.52.patch
    + Allow building the signer plugin against bouncycastle >= 1.52
* Tue Jul  2 2019 Fridrich Strba <fstrba@suse.com>
- Add possibility to build with ssh and vfs integration, since
  we have all the dependencies in openSUSE.
* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Remove the reference to parent from pom file, since we are not
  building using maven.
* Thu Feb  7 2019 Fridrich Strba <fstrba@suse.com>
- Add apache-ivy/ivy.jar symlink
* Mon Nov 26 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 2.4.0
- Modified patch:
  * apache-ivy-2.3.0-jdk9.patch -> apache-ivy-2.4.0-jdk9.patch
    + rediff to changed context
- Added patch:
  * apache-ivy-global-settings.patch
    + change global settings
* Tue May 15 2018 fstrba@suse.com
- Modified patch:
  * apache-ivy-2.3.0-jdk9.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
- Run fdupes on documentation
* Thu Sep  7 2017 fstrba@suse.com
- Added patch:
  * apache-ivy-2.3.0-jdk9.patch
    + Use source and target version 1.6 to enable build with jdk9
* Sun May 21 2017 tchvatal@suse.com
- Reduce deps a bit
* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Tue Jul  8 2014 tchvatal@suse.com
- Do not depend on ant-nodeps.
* Wed Nov  6 2013 mvyskocil@suse.com
- Remove jakarta-commons-httpclient3, we do no longer provide it
- Add ant.d config snippet for ivy
- call add_maven_depmap
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Jan 25 2013 archie@dellroad.org
- Upgrade to release 2.3.0
  * improved Ant support with some new Ant tasks and enhancements to existing tasks
  * improved Maven2 compatibility
  * some new resolvers
  * numerous bug fixes as documented in Jira and in the release notes
* Wed Jan  2 2013 archie@dellroad.org
- Define ${target.ivy.version} during build
- Include an ivy(1) command line script and man page
* Mon Jan 16 2012 mvyskocil@suse.cz
- Initial SUSE packaging of apache-ivy 2.2.0
  (without signing support)
