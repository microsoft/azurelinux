Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package slf4j-sources
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2000-2009, JPackage Project
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


%global base_name slf4j
Name:           %{base_name}-sources
Version:        1.7.30
Release:        4%{?dist}
Summary:        SLF4J Source JARs
# the log4j-over-slf4j and jcl-over-slf4j submodules are ASL 2.0, rest is MIT
License:        ASL 2.0 and MIT
Group:          Development/Libraries/Java
URL:            https://www.slf4j.org/
Source0:        https://github.com/qos-ch/%{base_name}/archive/v_%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Patch2:         slf4j-commons-lang3.patch
BuildRequires:  javapackages-local
BuildArch:      noarch

%description
SLF4J Source JARs.

%prep
%setup -q -n %{base_name}-v_%{version}
%patch2 -p1
find . -name "*.jar" | xargs rm
cp -p %{SOURCE1} APACHE-LICENSE

# Compat symlinks
%{mvn_file} ':{*}' %{base_name}/@1
%{mvn_package} :::sources:
%pom_disable_module slf4j-log4j12

%build
rm -f */src/main/resources/META-INF/MANIFEST.MF
for i in api ext jcl jdk14 nop simple; do
  mkdir -p %{base_name}-${i}/target
  jar cf %{base_name}-${i}/target/%{base_name}-${i}-%{version}-sources.jar -C %{base_name}-${i}/src/main/java .
  jar uf %{base_name}-${i}/target/%{base_name}-${i}-%{version}-sources.jar -C %{base_name}-${i}/src/main/resources .
#  %{mvn_artifact} org.slf4j:%{base_name}-${i}:jar:sources:%{version} %{base_name}-${i}/target/%{base_name}-${i}-%{version}-sources.jar
done
for i in jcl-over-slf4j jul-to-slf4j log4j-over-slf4j; do
  mkdir -p ${i}/target
  jar cf ${i}/target/${i}-%{version}-sources.jar -C ${i}/src/main/java .
  jar uf ${i}/target/${i}-%{version}-sources.jar -C ${i}/src/main/resources .
#  %{mvn_artifact} org.slf4j:${i}:jar:sources:%{version} ${i}/target/${i}-%{version}-sources.jar
done

%install
install -dm 0755 %{buildroot}%{_javadir}/%{base_name}
for i in api ext jcl jdk14 nop simple; do
  install -pm 0644 %{base_name}-${i}/target/%{base_name}-${i}-%{version}-sources.jar \
    %{buildroot}%{_javadir}/%{base_name}/%{base_name}-${i}-sources.jar
  %add_maven_depmap org.slf4j:%{base_name}-${i}:jar:sources:%{version} %{base_name}/%{base_name}-${i}-sources.jar
done
for i in jcl-over-slf4j jul-to-slf4j log4j-over-slf4j; do
  install -pm 0644 ${i}/target/${i}-%{version}-sources.jar \
    %{buildroot}%{_javadir}/%{base_name}/${i}-sources.jar
  %add_maven_depmap org.slf4j:${i}:jar:sources:%{version} %{base_name}/${i}-sources.jar
done

%files -f .mfiles
%license LICENSE.txt APACHE-LICENSE

%changelog
* Tue Jan 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.30-4
- Removing dependency on "log4j12".
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.30-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sat Apr 11 2020 Fridrich Strba <fstrba@suse.com>
- Don't use %%%%mvn_artifact, but %%%%add_maven_depmap for the
  sources artifacts, so that they don't suck in half of the xmvn*
  stack in order to build
* Wed Feb 26 2020 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 1.7.30
- Removed patch:
  * slf4j-Disallow-EventData-deserialization-by-default.patch
    + not needed any more
* Wed Dec 18 2019 Fridrich Strba <fstrba@suse.com>
- Use the source tarball from github, since the previous one is
  not accessible anymore
- Modified patches:
  * slf4j-Disallow-EventData-deserialization-by-default.patch
    + Adapt to unix line-ends
  * slf4j-commons-lang3.patch
    + Adapt to unix line-ends
    + Do not patch inexisting files
* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to parent from all pom files
- Avoid dependencies without version tag
* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against the compatibility log4j12-mini package
- Depend on mvn(log4j:log4j:1.2.17) provided by the compatibility
  packages
* Tue Mar 19 2019 Fridrich Strba <fstrba@suse.com>
- Fix an unexpanded ${parsedVersion.osgiVersion} variable in the
  manifests.
* Mon Mar 18 2019 Fridrich Strba <fstrba@suse.com>
- Split slf4j package into several sub-packages leaving only
  parent, api, simple and nop in the main package
- Package slf4j source jar files in a separate spec file
* Tue Feb 26 2019 Fridrich Strba <fstrba@suse.com>
- Clean up the maven pom installation
* Mon Oct 22 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to 1.7.25
- Modify the build.xml file tarball to correspond to the right
  version
- Modify slf4j-commons-lang3.patch to the new context
* Mon Oct 15 2018 Fridrich Strba <fstrba@suse.com>
- Install the maven artefacts to have mvn dependencies/provides
  generated automatically
* Fri May 18 2018 pmonrealgonzalez@suse.com
- Security fix:  [bsc#1085970, CVE-2018-8088]
  * Disallow EventData deserialization by default
  * Added slf4j-Disallow-EventData-deserialization-by-default.patch
    refreshed from Fedora [ https://src.fedoraproject.org/rpms/slf4j/
    blob/d7cd96bc7a8e8d8d62c8bc62baa7df02cef56c63/f/
    0001-Disallow-EventData-deserialization-by-default.patch ]
* Wed Oct 11 2017 fstrba@suse.com
- Adeed patch:
  * slf4j-commons-lang3.patch
    + Use apache-commons-lang3 instead of apache-commons-lang
* Sun Sep 10 2017 fstrba@suse.com
- Specify java source and target levels 1.6 in order to allow
  building with jdk9
- Disable doclint to avoid bailing out on formatting errors
- Recompress the build.xml.tar.bz2, so that it is a real tar.bz2
* Fri May 19 2017 tchvatal@suse.com
- Remove some not-needed deps
* Tue Nov 10 2015 dmacvicar@suse.de
- note:
  slf4j-pom_xml.patch was removed (not relevant anymore)
* Fri Oct 23 2015 dmacvicar@suse.de
- remove all unnecessary maven depmap metadata
* Fri Oct 23 2015 dmacvicar@suse.de
- update to version 1.7.12
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Aug 29 2014 coolo@suse.com
- build against log4j-mini to avoid a cycle
* Thu Sep 19 2013 mvyskocil@suse.com
- self-provide osgi(slf4j.api) symbol
* Fri Sep 13 2013 mvyskocil@suse.com
- fix build with apache-commons-lang
* Wed Sep 11 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Apr 27 2012 mvyskocil@suse.cz
- format spec file to be suitable for Factory
* Mon Dec 12 2011 dmacvicar@suse.de
- Fix absolute path in maven-build.xml that prevented
  package task in newer versions of openSUSE
- Fix javadoc group
* Wed Jul 27 2011 dmacvicar@suse.de
- Completely remove all maven build parts. Build with ant
* Mon Jul  4 2011 dmacvicar@suse.de
- add BuildRoot tag
