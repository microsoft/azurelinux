Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-archiver
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


%bcond_with tests
%bcond_with snappy
Name:           plexus-archiver
Version:        4.2.1
Release:        2%{?dist}
Summary:        Plexus Archiver Component
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://codehaus-plexus.github.io/plexus-archiver
Source0:        https://github.com/codehaus-plexus/plexus-archiver/archive/plexus-archiver-%{version}.tar.gz
Source1:        %{name}-build.xml
Patch0:         0001-Remove-support-for-snappy.patch
Patch1:         logger-level.patch
BuildRequires:  ant
BuildRequires:  apache-commons-compress
BuildRequires:  apache-commons-io
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsr-305
BuildRequires:  plexus-containers-container-default >= 2.1
BuildRequires:  plexus-io >= 3.2
BuildRequires:  plexus-utils >= 3.3
BuildRequires:  xz-java
Requires:       mvn(org.apache.commons:commons-compress)
Requires:       mvn(org.codehaus.plexus:plexus-io)
Requires:       mvn(org.codehaus.plexus:plexus-utils)
Requires:       mvn(org.tukaani:xz)
BuildArch:      noarch
%if %{with snappy}
BuildRequires:  mvn(org.iq80.snappy:snappy)
%endif
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  guava20
BuildRequires:  plexus-classworlds
BuildRequires:  xbean
BuildRequires:  xz-java
%endif

%description
Plexus contains end-to-end developer tools for writing applications.
At the core is the container, which can be embedded or for an
application server. There are many reusable components for hibernate,
form processing, jndi, i18n, velocity, etc. Plexus also includes an
application server which is like a J2EE application server.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
cp %{SOURCE1} build.xml

%if %{without snappy}
%patch0 -p1
%pom_remove_dep org.iq80.snappy:snappy
rm -rf src/main/java/org/codehaus/plexus/archiver/snappy
rm -rf src/test/java/org/codehaus/plexus/archiver/snappy
rm -f src/main/java/org/codehaus/plexus/archiver/tar/SnappyTarFile.java
rm -f src/main/java/org/codehaus/plexus/archiver/tar/PlexusIoTarSnappyFileResourceCollection.java
rm -r src/test/java/org/codehaus/plexus/archiver/tar/TarSnappyUnArchiverTest.java
%endif
%patch1 -p1

%pom_remove_plugin :maven-enforcer-plugin

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>" .

%build
mkdir -p lib
build-jar-repository -s lib plexus-containers/plexus-container-default jsr-305 commons-compress commons-io plexus/utils plexus/io
%if %{with tests}
build-jar-repository -s lib plexus/classworlds guava20/guava-20.0 xbean/xbean-reflect xz-java
%endif
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/plexus
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/plexus/archiver.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/plexus
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/plexus/archiver.pom
%add_maven_depmap plexus/archiver.pom plexus/archiver.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE

%files javadoc
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.2.1-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 4.2.1
- Modified patch:
  * 0001-Remove-support-for-snappy.patch
    + rediff to changed context
* Mon Apr  1 2019 Jan Engelhardt <jengelh@inai.de>
- Describe package, not the project vision.
* Fri Mar  8 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-archiver 3.6.0
- Generate and customize ant build file
- Make running of tests optional
- Added patches:
  * 0001-Remove-support-for-snappy.patch
    + When built without snappy support and trying to use Snappy,
    throw UnsupportedOperationException
  * logger-level.patch
    + Cast the result of getContainer() call, because the
    getLoggerManager() method is not a method of the
    PlexusContainer interface, but of the DefaultPlexusContainer
    implementation
