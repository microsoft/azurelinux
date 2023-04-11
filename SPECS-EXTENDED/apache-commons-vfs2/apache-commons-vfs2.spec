%global base_name vfs2
%global short_name commons-%{base_name}
Summary:        Commons Virtual File System
Name:           apache-%{short_name}
Version:        2.2
Release:        3%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/vfs/
Source0:        https://archive.apache.org/dist/commons/vfs/source/%{short_name}-distribution-%{version}-src.tar.gz
Source1:        build.xml
Source2:        common.xml
Source3:        commons-vfs2-build.xml
Source4:        commons-vfs2-examples-build.xml
Patch0:         0001_exlcude_abstractclass_from_test.patch
Patch1:         0002_remove_ftpFile_providers.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-collections4
BuildRequires:  apache-commons-compress
BuildRequires:  apache-commons-httpclient
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-lang3
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-net > 2
BuildRequires:  fdupes
BuildRequires:  httpcomponents-core
BuildRequires:  javapackages-local-bootstrap
Requires:       apache-commons-logging
BuildArch:      noarch

%description
Commons VFS provides a single API for accessing various
different file systems. It presents a uniform view of the
files from various different sources, such as the files on
local disk, on an HTTP server, or inside a Zip archive.
Some of the features of Commons VFS are:
* A single consistent API for accessing files of different
 types.
* Support for numerous file system types.
* Caching of file information. Caches information in-JVM,
 and optionally can cache remote file information on the
 local file system.
* Event delivery.
* Support for logical file systems made up of files from
 various different file systems.
* Utilities for integrating Commons VFS into applications,
 such as a VFS-aware ClassLoader and URLStreamHandlerFactory.
* A set of VFS-enabled Ant tasks.

%package ant
Summary:        Development files for Commons VFS
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}

%description ant
This package enables support for the Commons VFS ant tasks.

%package examples
Summary:        Commons VFS Examples
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description examples
VFS is a Virtual File System library - Examples.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n commons-vfs-%{version}
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} commons-vfs2/build.xml
cp %{SOURCE4} commons-vfs2-examples/build.xml
%patch0 -p1 -b .build.xml
%patch1 -p1 -b .provider.xml

%pom_remove_plugin :apache-rat-plugin

# Convert from dos to unix line ending
for file in LICENSE.txt NOTICE.txt README.txt RELEASE-NOTES.txt; do
 sed -i.orig 's|\r||g' $file
 touch -r $file.orig $file
 rm $file.orig
done

# Disable unwanted module
%pom_disable_module commons-vfs2-distribution

# Fix ant gId
%pom_change_dep -r :ant org.apache.ant:
# Upadate bouncycastle aId
%pom_change_dep -r :bcprov-jdk16 :bcprov-jdk15on

# Remove unwanted dependency jackrabbit-{standalone,webdav}
%pom_remove_dep -r org.apache.jackrabbit:

rm -rf commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/webdav

# Use old version of sshd-core
%pom_remove_dep -r :sshd-core

# hadoop has been retired
%pom_remove_dep -r org.apache.hadoop
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/hdfs

# not really needed
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :findbugs-maven-plugin

%pom_remove_dep -r :jsch
rm -rf commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/sftp
rm commons-vfs2-examples/src/main/java/org/apache/commons/vfs2/libcheck/SftpCheck.java
rm commons-vfs2/src/test/java/com/jcraft/jsch/TestIdentityRepositoryFactory.java
rm commons-vfs2/src/test/java/org/apache/commons/vfs2/util/DelegatingFileSystemOptionsBuilderTest.java

%pom_remove_dep -r :ftpserver-core
rm -rf commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/ftps
rm -rf commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/ftp

%pom_remove_parent commons-vfs2 commons-vfs2-examples

%build
mkdir -p lib
build-jar-repository -s lib ant commons-httpclient commons-logging commons-compress commons-collections4 commons-net commons-lang3 commons-io httpcomponents-core commons-codec

%{ant} \
  -Dtest.skip=true \
  package javadoc

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 %{short_name}/target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar
ln -sf %{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
install -pm 0644 %{short_name}-examples/target/%{short_name}-examples-%{version}.jar %{buildroot}%{_javadir}/%{short_name}-examples.jar
ln -sf %{short_name}-examples.jar %{buildroot}%{_javadir}/%{name}-examples.jar
# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 %{short_name}/pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}.pom
%add_maven_depmap %{short_name}.pom %{short_name}.jar
install -pm 0644 %{short_name}-examples/pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}-examples.pom
%add_maven_depmap %{short_name}-examples.pom %{short_name}-examples.jar -f examples
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/%{short_name}-examples
cp -pr %{short_name}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
cp -pr %{short_name}-examples/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/%{short_name}-examples/
%fdupes -s %{buildroot}%{_javadocdir}

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant commons-logging commons-vfs" > commons-vfs
install -p -m 644 commons-vfs %{buildroot}%{_sysconfdir}/ant.d/commons-vfs

%check
# Few tests cases have dependency on httpcomponents-client, which fails to install
# due to dependencies on mvn artifacts, commenting out those test cases
rm commons-vfs2/src/test/java/org/apache/commons/vfs2/util/NHttpFileServer.java
rm commons-vfs2/src/test/java/org/apache/commons/vfs2/provider/url/test/UrlProviderHttpTestCase.java
rm commons-vfs2/src/test/java/org/apache/commons/vfs2/provider/http/test/HttpProviderTestCase.java

%{ant} test

%files -f .mfiles
%doc README.txt RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt
%{_javadir}/%{name}.jar

%files examples -f .mfiles-examples
%{_javadir}/%{name}-examples.jar

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%files ant
%config %{_sysconfdir}/ant.d/commons-vfs

%changelog
* Tue Nov 15 2022 Sumedh Sharma <sumsharma@microsoft.com> - 2.2-3
- Disable hadoop/ftp/ssh fs layer builds.
- Enable check section. Disable tests having dependency on hadoop/ftp/ssh vfs.
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.2-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Mon Mar  4 2019 Fridrich Strba <fstrba@suse.com>
- Intial packaging of apache-commons-vfs2 2.2
- Generate and customize ant build system
