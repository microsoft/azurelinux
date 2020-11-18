%define _prefix /var/opt/apache-%{name}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib
Summary:        Apache Ant
Name:           ant
Version:        1.10.9
Release:        2%{?dist}
License:        ASL 2.0 AND BSD AND W3C
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://ant.apache.org
Source0:        https://archive.apache.org/dist/ant/source/apache-%{name}-%{version}-src.tar.gz
Source1:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/hamcrest/hamcrest-1.3.tgz
Source2:        https://dl.bintray.com/vmware/photon_sources/1.0/maven-ant-tasks-2.1.3.tar.gz
BuildRequires:  openjdk8
BuildRequires:  openjre8
Requires:       openjre8
Provides:       %{name}-lib = %{version}-%{release}
Provides:       mvn(ant:ant) = %{version}-%{release}
Provides:       mvn(ant:ant-launcher) = %{version}-%{release}
Provides:       mvn(apache:ant) = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant) = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-bootstrap) = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-launcher) = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-nodeps) = %{version}-%{release}
Provides:       %{name}-antlr = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-antlr) = %{version}-%{release}
Provides:       %{name}-jmf = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-jmf) = %{version}-%{release}
Provides:       %{name}-swing = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-swing) = %{version}-%{release}
Provides:       %{name}-apache-bsf = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-apache-bsf) = %{version}-%{release}
Provides:       %{name}-apache-resolver = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-apache-resolver) = %{version}-%{release}
Provides:       %{name}-commons-logging = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-commons-logging) = %{version}-%{release}
Provides:       %{name}-commons-net = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-commons-net) = %{version}-%{release}
Provides:       %{name}-jai = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-jai) = %{version}-%{release}
Provides:       %{name}-apache-bcel = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-apache-bcel) = %{version}-%{release}
Provides:       %{name}-apache-log4j = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-apache-log4j) = %{version}-%{release}
Provides:       %{name}-apache-oro = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-apache-oro) = %{version}-%{release}
Provides:       %{name}-apache-regexp = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-apache-regexp) = %{version}-%{release}
Provides:       %{name}-apache-xalan2 = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-apache-xalan2) = %{version}-%{release}
Provides:       %{name}-imageio = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-imageio) = %{version}-%{release}
Provides:       %{name}-javamail = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-javamail) = %{version}-%{release}
Provides:       %{name}-jdepend = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-jdepend) = %{version}-%{release}
Provides:       %{name}-jsch = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-jsch) = %{version}-%{release}
Provides:       %{name}-junit = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-junit) = %{version}-%{release}
Provides:       %{name}-testutil = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-testutil) = %{version}-%{release}
Provides:       %{name}-xz = %{version}-%{release}
Provides:       mvn(org.apache.ant:ant-xz) = %{version}-%{release}
BuildArch:      noarch

%description
The Ant package contains binaries for a build system

%package -n ant-scripts
Summary:        Additional scripts for ant
Requires:       %{name} = %{version}
Requires:       python2

%description -n ant-scripts
Apache Ant is a Java-based build tool.

This package contains additional perl and python scripts for Apache
Ant.

%prep
%setup -q -n apache-%{name}-%{version}
tar xf %{SOURCE1} --no-same-owner
tar xf %{SOURCE2} --no-same-owner

%clean
rm -rf %{buildroot}


%build
ANT_DIST_DIR=%{buildroot}%{_prefix}
cp -v ./hamcrest-1.3/hamcrest-core-1.3.jar ./lib/optional
export JAVA_HOME=$(find %{_lib}/jvm -name "OpenJDK*")
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")
mkdir -p -m 700 $ANT_DIST_DIR
./bootstrap.sh && ./build.sh -Ddist.dir=$ANT_DIST_DIR

%install
cp %{_builddir}/apache-%{name}-%{version}/maven-ant-tasks-2.1.3/maven-ant-tasks-2.1.3.jar %{buildroot}/%{_libdir}/
mkdir -p %{buildroot}%{_datadir}/java/ant

for jar in %{buildroot}/%{_libdir}/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/ant/${jarname}.jar
done
rm -rf %{buildroot}%{_bindir}/*.bat
rm -rf %{buildroot}%{_bindir}/*.cmd

mkdir -p %{buildroot}/bin
for b in %{buildroot}%{_bindir}/*
do
    binaryname=$(basename $b)
    ln -sfv %{_bindir}/${binaryname} %{buildroot}/bin/${binaryname}
done

MAVEN_ANT_TASKS_DIR=%{buildroot}%{_prefix}/maven-ant-tasks

mkdir -p -m 700 $MAVEN_ANT_TASKS_DIR
cp %{_builddir}/apache-%{name}-%{version}/maven-ant-tasks-2.1.3/LICENSE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/apache-%{name}-%{version}/maven-ant-tasks-2.1.3/NOTICE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/apache-%{name}-%{version}/maven-ant-tasks-2.1.3/README.txt $MAVEN_ANT_TASKS_DIR/
chown -R root:root $MAVEN_ANT_TASKS_DIR
chmod 644 $MAVEN_ANT_TASKS_DIR/*

%check
# Disable following tests which are currently failing in chrooted environment -
#   - org.apache.tools.ant.types.selectors.OwnedBySelectorTest
#   - org.apache.tools.ant.types.selectors.PosixGroupSelectorTest
#   - org.apache.tools.mail.MailMessageTest
if [ "$(stat -c %{d}:%i /)" != "$(stat -c %{d}:%i /proc/1/root/.)" ]; then
  rm -f src/tests/junit/org/apache/tools/ant/types/selectors/OwnedBySelectorTest.java \
        src/tests/junit/org/apache/tools/ant/types/selectors/PosixGroupSelectorTest.java \
        src/tests/junit/org/apache/tools/mail/MailMessageTest.java
fi
export JAVA_HOME=`echo %{_lib}/jvm/OpenJDK-*`
bootstrap/bin/ant -v run-tests

%files
%defattr(-,root,root)
%license LICENSE
%dir %{_bindir}
%dir %{_libdir}
%dir %{_datadir}/java/ant
%dir %{_prefix}/maven-ant-tasks
/bin/ant
/bin/antRun
%{_bindir}/ant
%{_bindir}/antRun
%{_libdir}/*
%{_datadir}/java/ant/*.jar
%{_prefix}/maven-ant-tasks/LICENSE
%{_prefix}/maven-ant-tasks/README.txt
%{_prefix}/maven-ant-tasks/NOTICE

%files -n ant-scripts
%defattr(-,root,root)
/bin/antRun.pl
/bin/complete-ant-cmd.pl
/bin/runant.py
/bin/runant.pl
%{_bindir}/antRun.pl
%{_bindir}/complete-ant-cmd.pl
%{_bindir}/runant.py
%{_bindir}/runant.pl

%changelog
* Tue Nov 17 2020 Joe Schmitt <joschmit@microsoft.com> - 1.10.9-1
- Add additional provides.

*   Wed Oct 21 2020 Henry Li <lihl@microsoft.com> - 1.10.9-1
-   Updated to version 1.10.9 to resolve CVE-2020-11979

*   Thu May 21 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.10.8-1
-   Updated to version 1.10.8 to resolve CVE-2020-1945

*   Sat May 09 00:21:39 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.10.5-8
-   Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.10.5-7
-   Renaming apache-ant to ant

*   Wed Apr 29 2020 Nicolas Guibourge <nicolasg@microsoft.com> 1.10.5-6
-   Add path to libjli.so in LD_LIBRARY_PATH

*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.10.5-5
-   Fixed "Source0"-"Source2" and "URL" tags.
-   License verified and "License" tag updated.
-   Removed "%%define sha1".
-   Replaced tabs with spaces.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.10.5-4
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Dec 04 2018 Dweep Advani <dadvani@vmware.com> 1.10.5-3
-   Adding MakeCheck tests

*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.10.5-2
-   Removed dependency on JAVA8_VERSION macro

*   Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 1.10.5-1
-   Updated Apache Ant to 1.10.5

*   Wed Jun 28 2017 Kumar Kaushik <kaushikk@vmware.com> 1.10.1-5
-   Base package does not require python2.

*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.10.1-4
-   Removed dependency on ANT_HOME
-   Moved perl and python scripts to ant-scripts package

*   Mon Jun 05 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-3
-   Fixed the profile.d/apache-ant.sh script to include ant in $PATH

*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-2
-   Renamed openjdk to openjdk8

*   Mon Apr 17 2017 Chang Lee <changlee@vmware.com> 1.10.1-1
-   Updated Apache Ant to 1.10.1

*   Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-6
-   use java rpm macros to determine versions

*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-5
-   Updated JAVA_HOME path to point to latest JDK.

*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-4
-   Updated JAVA_HOME path to point to latest JDK.

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-3
-   GA - Bump release of all rpms

*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.9.6-2
-   Updated JAVA_HOME path to point to latest JDK.

*   Mon Feb 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-1
-   Updated to version 1.9.6

*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.9.4-4
-   Updated JAVA_HOME path to point to latest JDK.

*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.9.4-3
-   Changed path to /var/opt.

*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-2
-   Updated dependencies after repackaging openjdk.

*   Wed Aug 12 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Added maven ant tasks

*   Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Initial build. First version
