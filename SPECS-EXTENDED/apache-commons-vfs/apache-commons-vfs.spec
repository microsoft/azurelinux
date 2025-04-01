## START: Set by rpmautospec
## (rpmautospec version 0.6.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%bcond cifs   0
%bcond ftp    0
%bcond hadoop 0
%bcond mina   0

Name:           apache-commons-vfs
Version:        2.9.0
Release:        %autorelease
Summary:        Commons Virtual File System
License:        Apache-2.0
BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch

URL:            https://commons.apache.org/proper/commons-vfs/
VCS:            git:https://github.com/apache/commons-vfs.git
Source0:        https://archive.apache.org/dist/commons/vfs/source/commons-vfs-%{version}-src.tar.gz
Source1:        https://archive.apache.org/dist/commons/vfs/source/commons-vfs-%{version}-src.tar.gz.asc
Source2:        https://downloads.apache.org/commons/KEYS

# Migrate from the old commons-httpclient, which is no longer available in
# Fedora, to the newer httpcomponents httpclient.
Patch:          %{name}-httpclient.patch

BuildRequires:  gnupg2
BuildRequires:  maven-local
BuildRequires:  mvn(com.jcraft:jsch)
BuildRequires:  mvn(com.sun.mail:jakarta.mail)
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(commons-net:commons-net)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.commons:commons-collections4)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore-nio)
BuildRequires:  mvn(org.apache.logging.log4j:log4j-core)
BuildRequires:  mvn(org.apache.logging.log4j:log4j-slf4j-impl)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-surefire-plugin)
BuildRequires:  mvn(org.apache.sshd:sshd-core)
BuildRequires:  mvn(org.bouncycastle:bcprov-jdk16)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%if %{with hadoop}
BuildRequires:  mvn(javax.ws.rs:jsr311-api)
BuildRequires:  mvn(org.apache.hadoop:hadoop-common)
BuildRequires:  mvn(org.apache.hadoop:hadoop-hdfs)
BuildRequires:  mvn(org.apache.hadoop:hadoop-hdfs-client)
%endif
%if %{with ftp}
BuildRequires:  mvn(org.apache.ftpserver:ftpserver-core)
%endif
%if %{with cifs}
BuildRequires:  mvn(jcifs:jcifs)
%endif
%if %{with mina}
BuildRequires:  mvn(org.apache.mina:mina-core)
%endif

Provides:       %{name}2 = %{version}-%{release}

%description
Commons VFS provides a single API for accessing various file systems.
It presents a uniform view of the files from various sources, such as
the files on local disk, on an HTTP server, or inside a Zip archive.

Some of the features of Commons VFS are:
* A single consistent API for accessing files of different types.
* Support for numerous file system types.
* Caching of file information.  Caches information in-JVM, and
  optionally can cache remote file information on the local file
  system (replicator).
* Event delivery.
* Support for logical file systems made up of files from various file
  systems.
* Utilities for integrating Commons VFS into applications, such as a
  VFS-aware ClassLoader and URLStreamHandlerFactory.
* A set of VFS-enabled Ant tasks.

%package       ant
Summary:       Development files for Commons VFS
Requires:      %{name} = %{version}-%{release}
Requires:      ant

%description   ant
This package enables support for the Commons VFS ant tasks.

%package       examples
Summary:       Commons VFS Examples
Requires:      %{name} = %{version}-%{release}

%description   examples
VFS is a Virtual File System library - Examples.

%package       project
Summary:       Commons VFS Parent POM

%description   project
Commons VFS Parent POM.

%javadoc_package

%prep
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}
%autosetup -n commons-vfs-%{version} -p1

# Not needed for RPM builds
%pom_xpath_remove //pom:reporting
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :japicmp-maven-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :maven-pmd-plugin
%pom_remove_plugin :maven-project-info-reports-plugin
%pom_remove_plugin :spotbugs-maven-plugin

# Disable unwanted module
%pom_disable_module commons-vfs2-distribution

# Fix ant gId
%pom_change_dep -r :ant org.apache.ant:

# Remove webdav client (jackrabbit not packaged)
%pom_remove_dep -r org.apache.jackrabbit:
%pom_disable_module commons-vfs2-jackrabbit1
%pom_disable_module commons-vfs2-jackrabbit2

# Remove http3 client.  It needs the old commons-httpclient, which is no
# longer available in Fedora.  We support the http4 client.
%pom_remove_dep -r commons-httpclient:commons-httpclient
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/http
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/https

# Remove http5 client (httpclient5 not packaged)
%pom_remove_dep -r org.apache.httpcomponents.client5:httpclient5
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/http5
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/http5s

# hadoop has been retired
%if %{without hadoop}
%pom_remove_dep -r org.apache.hadoop
%pom_remove_dep -r javax.ws.rs
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/hdfs
%endif

# ftpserver is not available
%if %{without ftp}
%pom_remove_dep -r :ftpserver-core
rm -r commons-vfs2/src/{main,test}/java/org/apache/commons/vfs2/provider/ftps
%endif

# jcifs not packaged and also export controlled in the US
%if %{without cifs}
%pom_remove_dep :jcifs
%endif

# mina is not available
%if %{without mina}
%pom_remove_dep :mina-core
%endif

# Fix installation directory and symlink
%mvn_file :commons-vfs2 %{name}
%mvn_file :commons-vfs2 %{name}2
%mvn_file :commons-vfs2 commons-vfs
%mvn_file :commons-vfs2 commons-vfs2
%mvn_file :commons-vfs2-examples %{name}-examples
%mvn_file :commons-vfs2-examples %{name}2-examples
%mvn_file :commons-vfs2-examples commons-vfs-examples
%mvn_file :commons-vfs2-examples commons-vfs2-examples

%mvn_alias :commons-vfs2 "org.apache.commons:commons-vfs" "commons-vfs:commons-vfs"
%mvn_alias :commons-vfs2-examples "org.apache.commons:commons-vfs-examples" "commons-vfs:commons-vfs-examples"

%build
%mvn_build -sf

%install
%mvn_install

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant commons-logging commons-vfs" > commons-vfs
install -p -m 644 commons-vfs %{buildroot}%{_sysconfdir}/ant.d/commons-vfs

%files -f .mfiles-commons-vfs2
%doc README.md RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt

%files examples -f .mfiles-commons-vfs2-examples

%files project -f .mfiles-commons-vfs2-project
%license LICENSE.txt NOTICE.txt

%files ant
%config(noreplace) %{_sysconfdir}/ant.d/commons-vfs

%changelog
## START: Generated by rpmautospec
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Jerry James <loganjerry@gmail.com> - 2.9.0-6
- Minor spec file simplifications

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.9.0-5
- Rebuilt for java-21-openjdk as system jdk

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 08 2020 Fabio Valentini <decathorpe@gmail.com> - 2.6.0-1
- Update to version 2.6.0.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 05 2019 Fabio Valentini <decathorpe@gmail.com> - 2.4.1-1
- Update to version 2.4.1.

* Fri Jul 26 2019 Fabio Valentini <decathorpe@gmail.com> - 2.1-16
- Disable ftp support by default.

* Wed Jul 24 2019 Fabio Valentini <decathorpe@gmail.com> - 2.1-15
- Disable hadoop support by default.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.1-10
- Add conditionals for ftp and ssh

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.1-9
- Remove rat-plugin

* Sun Jan 29 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-8
- Fix hadoop build conditionals

* Fri Oct 28 2016 gil cattaneo <puntogil@libero.it> 2.1-7
- enable HDFS support (rhbz#1387108)

* Mon Oct  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-6
- Remove build-requires on perl

* Thu Jul 21 2016 gil cattaneo <puntogil@libero.it> 2.1-5
- add missing BR

* Sat Jun 25 2016 gil cattaneo <puntogil@libero.it> 2.1-4
- disable tests failure

* Thu Jun 02 2016 gil cattaneo <puntogil@libero.it> 2.1-3
- disable hadoop stuff with bcond

* Thu Jun 02 2016 Michael Simacek <msimacek@redhat.com> - 2.1-2
- Remove support for retired hadoop

* Sun May 22 2016 gil cattaneo <puntogil@libero.it> 2.1-1
- update to 2.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 gil cattaneo <puntogil@libero.it> 2.0-15
- introduce license macro

* Wed Jul 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-14
- Fix build-requires on apache-commons-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-12
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 gil cattaneo <puntogil@libero.it> 2.0-10
- used pom_xpath_set macro

* Fri Jun 28 2013 gil cattaneo <puntogil@libero.it> 2.0-9
- swith to pom macros
- packaged in /usr/share/java instead of /usr/share/java/apache-commons-vfs

* Fri Jun 28 2013 Michal Srb <msrb@redhat.com> - 2.0-8
- Fix directory ownership

* Thu Jun 27 2013 Michal Srb <msrb@redhat.com> - 2.0-7
- Build with XMvn
- Do not ignore test failures
- Fix BR

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Aug  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-4
- Rebuild against javamail

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 gil cattaneo <puntogil@libero.it> 2.0-2
- add subpackage ant
- install NOTICE.txt in javadocs subpackage

* Mon May 14 2012 gil cattaneo <puntogil@libero.it> 2.0-1
- initial rpm

## END: Generated by rpmautospec
