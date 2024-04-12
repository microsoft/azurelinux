#
# spec file for package cal10n
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
Summary:        Compiler assisted localization library (CAL10N)
Name:           cal10n
Version:        0.8.1.10
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            http://cal10n.qos.ch
Source0:        https://code.opensuse.org/adrianSuSE/%{name}/blob/factory/f/%{name}-%{version}.tar.xz
# cal10n-build.tar.gz imported from https://code.opensuse.org/adrianSuSE/cal10n/blob/factory/f/cal10n-build.tar.xz
Source1:        %{name}-build.tar.xz
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  junit
BuildRequires:  xz
Requires:       java
BuildArch:      noarch

%description
Compiler Assisted Localization, abbreviated as CAL10N (pronounced as "calion")
is a java library for writing localized (internationalized) messages.
Features:
    * java compiler verifies message keys used in source code
    * tooling to detect errors in message keys
    * native2ascii tool made superfluous, as you can directly encode bundles
      in the most convenient charset, per locale.
    * good performance (300 nanoseconds per key look-up)
    * automatic reloading of resource bundles upon change

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q -a1
find . -name "*.jar" -exec rm -f {} \;

# We don't want to depend on ant, since it will be
# present when we try to use the task
%pom_change_dep :ant :::provided %{name}-ant-task 

# bnc#759912
rm -rf docs cal10n-site
cat > README.SUSE <<EOF

The documentation under Creative Commons Attribution-NonCommercial-ShareAlike
2.5 License is not suitable for Linux distributors, so it has been removed.

You may find the online version at
http://cal10n.qos.ch/manual.html

EOF

%build
mkdir -p lib
build-jar-repository -s lib \
%if %{with tests}
    ant-antunit \
%endif
    ant/ant
%{ant} \
%if %{without tests}
    -Dtest.skip=true \
%endif
    package javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{name}
install -m 644 %{name}-api/target/%{name}-api-*.jar \
        %{buildroot}%{_javadir}/%{name}/%{name}-api.jar
install -m 644 %{name}-ant-task/target/%{name}-ant-task-*.jar \
        %{buildroot}%{_javadir}/%{name}/%{name}-ant-task.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom
install -pm 644 %{name}-api/pom.xml %{buildroot}%{_mavenpomdir}/%{name}-api.pom
%add_maven_depmap %{name}-api.pom %{name}/%{name}-api.jar
install -pm 644 %{name}-ant-task/pom.xml %{buildroot}%{_mavenpomdir}/%{name}-ant-task.pom
%add_maven_depmap %{name}-ant-task.pom %{name}/%{name}-ant-task.jar

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
for i in api ant-task; do
  install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/${i}
  cp -pr %{name}-${i}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/${i}/
done
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc README.SUSE

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Apr 05 2024 Mitch Zhu <mitchzhu@microsoft.com> - 0.8.1.10-1
- Update to version 0.8.1.10
- Import build, install section, and source file from openSUSE (license: MIT).

* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.7.7-6
- Moved from extended to core
- Updated source URL

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.7-5
- Converting the 'Release' tag to the '[number].[distribution]' format.
- License verified.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 0.7.7-4.9
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Oct 18 2018 Fridrich Strba <fstrba@suse.com>
- Install the maven pom files in order to generate correctly the
  mvn(...) provides.

* Wed May 16 2018 fstrba@suse.com
- Modified patch:
  * cal10n-0.7.7-sourcetarget.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
- Run fdupes on documentation

* Thu Sep  7 2017 fstrba@suse.com
- Added patch:
  * cal10n-0.7.7-sourcetarget.patch
  - Force java source and target levels to 1.6 in order to allow
    building with jdk9

* Thu Dec 25 2014 p.drouand@gmail.com
- Update to version 0.7.7
  + Correctly read escaped ':', '#', '!', '=' characters. The behavior
  is documented in the Properties javadocs (http://tinyurl.com/bprdgnk).
  This fixes CAL-37 (http://jira.qos.ch/browse/CAL-37)
- Update build.xml.tar.bz2, rename it to build.xml-$VERSION and
  recompress it in xz format
- Add a requirement to xz

* Mon Jul  7 2014 tchvatal@suse.com
- Depend on junit not junit4

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Fri May  4 2012 mvyskocil@suse.cz
- fix bnc#759912 - Manual for cal10n 0.7.4 uses CC-BY-SA-NC-2.5 license

* Fri Apr 27 2012 mvyskocil@suse.cz
- format spec for Factory

* Mon Dec 12 2011 dmacvicar@suse.de
- fix build.xml files to build in openSUSE 12.1 and newer.
  MANIFEST contained an absolute path in maven-build.xml
- Fix group for javadoc subpackage
- remove id generation for buildroot (used in Fedora)

* Wed Jul 27 2011 dmacvicar@suse.de
- Un-mavenize. Build with ant
