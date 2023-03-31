
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
Version:        0.7.7
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            http://cal10n.qos.ch
Source0:        https://github.com/qos-ch/cal10n/archive/refs/tags/v_%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        build.xml-0.7.7.tar.xz
Patch0:         cal10n-0.7.7-sourcetarget.patch
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
%setup -q
tar -xf %{SOURCE1}
%patch0 -p1
find . -name "*.jar" | xargs rm

# bnc#759912
rm -rf docs cal10n-site
cat > README.SUSE <<EOF

The documentation under Creative Commons Attribution-NonCommercial-ShareAlike
2.5 License is not suitable for Linux distributors, so it has been removed.

You may find the online version at
http://cal10n.qos.ch/manual.html

EOF

%build
for dir in cal10n-api
do
  pushd $dir
  export CLASSPATH=$(build-classpath \
                     junit \
                     ):target/classes:target/test-classes
  ant -Dmaven.mode.offline=true package javadoc \
      -Dmaven.test.skip=true \
      -lib %{_datadir}/java
  popd
done

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{name}
install -m 644 cal10n-api/target/cal10n-api-%{version}.jar \
        %{buildroot}%{_javadir}/%{name}/cal10n-api-%{version}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom
install -pm 644 %{name}-api/pom.xml %{buildroot}%{_mavenpomdir}/%{name}-api.pom
%add_maven_depmap %{name}-api.pom %{name}/cal10n-api-%{version}.jar

# javadoc
pushd cal10n-api
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
rm -rf target/site/api*
popd
%fdupes -s %{buildroot}%{_javadocdir}/%{name}-%{version}

%files
%license LICENSE.txt
%defattr(0644,root,root,0755)
%doc README.SUSE
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}*.jar
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files javadoc
%license LICENSE.txt
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}

%changelog
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
