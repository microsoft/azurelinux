#
# spec file for package ant-contrib
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
#

Summary:        Collection of tasks for Ant
Name:           ant-contrib
Version:        1.0b3
Release:        20%{?dist}
License:        ASL 2.0 AND ASL 1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://ant-contrib.sourceforge.net/
Source0:        https://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}-src.tar.bz2
# Upstream POM file
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/1.0b3/%{name}-1.0b3.pom
# ASL 2.0 Licence text
# Upstream bug at https://sourceforge.net/tracker/?func=detail&aid=3590371&group_id=36177&atid=416920
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt
Patch0:         ant-contrib-pom.patch
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
Requires:       ant
Requires:       java-headless
BuildArch:      noarch

# Temp: Do not build with x86_64 due to docker build issue
ExclusiveArch:  aarch64

%description
The Ant-Contrib project is a collection of tasks (and at one point
maybe types and other tools) for Apache Ant.

%package        manual
Summary:        Manual for %{name}

%description    manual
Documentation for %{name} tasks.

%package        javadoc
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description    javadoc
Api documentation for %{name}.

%prep
%setup -q -n %{name}
cp %{SOURCE1} %{name}-1.0b3.pom
cp %{SOURCE2} LICENSE-2.0.txt

%patch0 -p1

find . -name '*.jar' -or -name '*.class' -exec rm -rf {} +

# needs porting to latest ivy
rm -fr src/java/net/sf/antcontrib/net/URLImportTask.java

%build
ant -Ddist.dir="." -Dproject.version=%{version} dist

%install
# jars
install -Dpm 644 target/%{name}.jar %{buildroot}%{_javadir}/ant/%{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/docs/api/* %{buildroot}%{_javadocdir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant/ant-contrib" > %{buildroot}%{_sysconfdir}/ant.d/ant-contrib

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{name}-1.0b3.pom %{buildroot}/%{_mavenpomdir}/JPP.ant-%{name}.pom

echo "call add_maven_depmap JPP.ant-%{name}.pom ant/%{name}.jar"
%add_maven_depmap JPP.ant-%{name}.pom ant/%{name}.jar

%files
%defattr(0644,root,root,0755)
%license LICENSE-2.0.txt target/docs/LICENSE.txt
%config %{_sysconfdir}/ant.d/%{name}
%{_javadir}/ant/%{name}.jar
%{_mavenpomdir}/JPP.ant-%{name}.pom
%{_datadir}/maven-metadata/%{name}.xml

%files manual
%doc target/docs/manual/tasks/*

%files javadoc
%license LICENSE-2.0.txt target/docs/LICENSE.txt
%doc %{_javadocdir}/%{name}

%changelog
* Wed Nov 17 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0b3-20
- License verified.

* Fri Nov 20 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0b3-19
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Simplify buildrequires and runtime requires.
- Remove junit integration.
- Remove fdupes dependency.
- Set %%license.

* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Run fdupes on the documentation

* Wed Sep  6 2017 fstrba@suse.com
- Added patch:
  * ant-contrib-sourcetarget.patch
  - build with java source and target 1.6
  - fixes the build with java 9

* Fri May 19 2017 tchvatal@suse.com
- Fix build with new javapackages-tools

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Thu Mar 12 2015 archie@dellroad.org
- Add back patch enabling the <antcontrib:for> task (boo#922324)
  * ant-contrib-1.0b3-enable-for-task.patch

* Mon Jul  7 2014 tchvatal@suse.com
- Clean up a bit with spec-cleaner

* Fri Nov 15 2013 mvyskocil@suse.com
- don't require ant-junit for build, junit is sufficient
  * reducing of cycles

* Wed Nov  6 2013 mvyskocil@suse.com
- upgrade to 1.0b3
  * no upstream changelog available
- removed patches:
  * ant-contrib-1.0b2-enable-for-task.patch
    there is no for task in beta3
  * ant-contrib-ant-1.7.0.patch
    no longer needed
  * ant-contrib-build_xml.patch
    fixed upstream
  * ant-contrib-BuildFileTest_java.patch
    no longer needed
- added patches:
  * ant-contrib-antservertest.patch
  * ant-contrib-pom.patch
  * local-ivy.patch
- add pom file
- add ant.d configuration

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Thu Aug 22 2013 mvyskocil@suse.com
- disable javadoc build

* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile

* Fri Oct  8 2010 mvyskocil@suse.cz
- fix bnc#644661 - ant-contrib does not export the antcontrib:for task

* Thu Apr 30 2009 mrueckert@suse.de
- rename ant_version to ant_minimal_version
- use requires_eq for the ant package

* Thu Apr 30 2009 ro@suse.de
- bump ant-version to 1.7.1

* Thu Sep 11 2008 mvyskocil@suse.cz
- Use a gcc-java to build

* Fri Aug  8 2008 mvyskocil@suse.cz
- Make junit testing optional and disable it by default  to break a build cycle
  ant-antlr - bsf - jython - mysql-connector-java - ant-contrib ant-contrib

* Thu Jul 10 2008 mvyskocil@suse.cz
- Removed summary tags from description of subpackages.
- Remove the ant-1.7.0 archive to reduce a size of source package and
  use only one necessary file BuildFileTest.java

* Wed Jul  2 2008 mvyskocil@suse.cz
- First release based on jpackage.org 1.7 (1.0.b2)
  - adjusted for ant 1.7.0
