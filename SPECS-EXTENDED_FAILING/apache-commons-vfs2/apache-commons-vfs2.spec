Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache-commons-vfs2
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
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


%global base_name vfs2
%global short_name commons-%{base_name}
%bcond_with tests
%bcond_with hadoop
%bcond_without ftp
%bcond_without ssh
Name:           apache-%{short_name}
Version:        2.2
Release:        2%{?dist}
Summary:        Commons Virtual File System
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://commons.apache.org/vfs/
Source0:        http://www.apache.org/dist/commons/vfs/source/%{short_name}-distribution-%{version}-src.tar.gz
Source1:        %{short_name}-%{version}-build.tar.xz
BuildRequires:  ant
BuildRequires:  apache-commons-collections4
BuildRequires:  apache-commons-compress
BuildRequires:  apache-commons-httpclient
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-net > 2
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
Requires:       mvn(commons-logging:commons-logging)
BuildArch:      noarch
%if %{with hadoop}
BuildRequires:  mvn(org.apache.hadoop:hadoop-common)
BuildRequires:  mvn(org.apache.hadoop:hadoop-hdfs)
%endif
%if %{with ssh}
BuildRequires:  jsch
%endif
%if %{with ftp}
%if %{with tests}
BuildRequires:  mvn(org.apache.ftpserver:ftpserver-core)
%endif
%endif

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
%setup -q -n commons-vfs-%{version} -a1

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
%if %{without hadoop}
%pom_remove_dep -r org.apache.hadoop
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/hdfs
%endif

# not really needed
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :findbugs-maven-plugin

%if %{without ssh}
%pom_remove_dep -r :jsch
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/sftp
rm commons-vfs2-examples/src/main/java/org/apache/commons/vfs2/libcheck/SftpCheck.java
%endif

%if %{without ftp}
%pom_remove_dep -r :ftpserver-core
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/ftps
%endif

%pom_remove_parent commons-vfs2 commons-vfs2-examples

%build
mkdir -p lib
build-jar-repository -s lib ant commons-httpclient commons-logging commons-compress commons-collections4 commons-net
%if %{with hadoop}
build-jar-repository -s lib hadoop/common hadoop/hdfs
%endif
%if %{with ssh}
build-jar-repository -s lib jsch
%endif

%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
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
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.2-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Mon Mar  4 2019 Fridrich Strba <fstrba@suse.com>
- Intial packaging of apache-commons-vfs2 2.2
- Generate and customize ant build system
