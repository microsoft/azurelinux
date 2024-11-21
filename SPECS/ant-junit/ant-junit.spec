#
# spec file for package ant-junit
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

%define ant_junit_requires_eq()  %(LC_ALL="C" echo '%*' | xargs -r rpm -q --qf 'Requires: %%{name} = %%{version}\\n' | sed -e 's/ (none):/ /' -e 's/ 0:/ /' | grep -v "is not")
%global ant_home %{_datadir}/ant
##### WARNING: please do not edit this auto generated spec file. Use the ant.spec! #####
%bcond_with bootstrap
%bcond_without junit
%bcond_with junit5
%bcond_with antlr

Summary:        Optional junit tasks for ant
Name:           ant-junit
Version:        1.10.14
Release:        1%{?dist}
License:        ASL 2.0 AND W3C
Group:          Development/Tools/Building
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://ant.apache.org/
Source0:        https://www.apache.org/dist/ant/source/apache-ant-%{version}-src.tar.gz
Source1:        apache-ant-1.8.ant.conf
Source10:       ant-bootstrap.pom.in
Patch0:         apache-ant-no-test-jar.patch
Patch1:         apache-ant-class-path-in-manifest.patch
Patch2:         apache-ant-bootstrap.patch
#PATCH-FEATURE-OPENSUSE bmwiedemann -- have fixed build dates
Patch3:         reproducible-build-date.patch
# PATCH-FEATURE-OPENSUSE reproducible-build-manifest.patch -- have fixed "Created-by" in manifest
Patch5:         reproducible-build-manifest.patch
Patch6:         apache-ant-xml-apis.patch
BuildRequires:  antlr-bootstrap
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  unzip
BuildRequires:  xml-commons-apis-bootstrap
#!BuildIgnore:  xml-commons-apis
BuildArch:      noarch
# Needed for maven conversions
%if !%{with bootstrap}
BuildRequires:  javapackages-local-bootstrap
%endif
%if %{with junit} || %{with antlr} || %{with junit5}
BuildRequires:  ant = %{version}
BuildRequires:  hamcrest
BuildRequires:  junit
#!BuildIgnore:  antlr
%endif
%if %{with antlr}
BuildRequires:  xerces-j2
BuildRequires:  xz-java
%endif
%if %{with junit5}
BuildRequires:  apiguardian
BuildRequires:  junit5
%endif
%if %{with bootstrap}
Requires:       java-devel >= 1.8
Requires:       javapackages-tools
Requires:       xerces-j2
Requires:       xml-apis
Requires:       xml-resolver
Obsoletes:      apache-ant < %{version}
Provides:       apache-ant = %{version}
Obsoletes:      ant-nodeps < %{version}
Provides:       ant-nodeps = %{version}
Obsoletes:      ant-trax < %{version}
Provides:       ant-trax = %{version}
%endif
%if %{with antlr}
Requires:       antlr
%ant_junit_requires_eq    ant
Obsoletes:      ant-javadoc
%endif
%if %{with junit}
Requires:       junit4
%ant_junit_requires_eq    ant
%endif
%if %{with junit5}
Requires:       junit5
%ant_junit_requires_eq    ant
%endif
%if %{with junit}
%description
Apache Ant is a Java-based build tool.

This package contains optional JUnit tasks for Apache Ant.
%elif %{with junit5}
%description
Apache Ant is a Java-based build tool.

This package contains optional JUnit5 tasks for Apache Ant.
%else
%description
Apache Ant is a Java-based build tool. In theory, it is kind of like
Make. Build description files are written in XML.
%endif

%if %{with bootstrap}
%package -n ant-jmf
Summary:        Optional jmf tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
Requires:       ant = %{version}

%description -n ant-jmf
Apache Ant is a Java-based build tool.

This package contains optional jmf tasks for Apache Ant.

%package -n ant-swing
Summary:        Optional swing tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
Requires:       ant = %{version}

%description -n ant-swing
Apache Ant is a Java-based build tool.

This package contains optional swing tasks for Apache Ant.

%package -n ant-scripts
Summary:        Additional scripts for ant
License:        Apache-2.0
Group:          Development/Tools/Building
Requires:       ant = %{version}
Requires:       perl
Requires:       python3

%description -n ant-scripts
Apache Ant is a Java-based build tool.

This package contains additional perl and python scripts for Apache
Ant.

%endif #if bootstrap

%if %{with antlr}
%package -n ant-apache-bsf
Summary:        Optional apache bsf tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  bsf
Requires:       bsf
%ant_junit_requires_eq    ant

%description -n ant-apache-bsf
Apache Ant is a Java-based build tool.

This package contains optional apache bsf tasks for Apache Ant.

%package -n ant-apache-resolver
Summary:        Optional apache resolver tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  xml-resolver
Requires:       xml-resolver
%ant_junit_requires_eq    ant

%description -n ant-apache-resolver
Apache Ant is a Java-based build tool.

This package contains optional apache resolver tasks for Apache Ant.

%package -n ant-commons-logging
Summary:        Optional commons logging tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  apache-commons-logging
Requires:       apache-commons-logging
%ant_junit_requires_eq    ant

%description -n ant-commons-logging
Apache Ant is a Java-based build tool.

This package contains optional commons logging tasks for Apache Ant.

%package -n ant-commons-net
Summary:        Optional commons net tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  apache-commons-net
Requires:       apache-commons-net
%ant_junit_requires_eq    ant

%description -n ant-commons-net
Apache Ant is a Java-based build tool.

This package contains optional commons net tasks for Apache Ant.

%package -n ant-apache-bcel
Summary:        Optional apache bcel tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  bcel
Requires:       bcel
%ant_junit_requires_eq    ant
Provides:       ant-jakarta-bcel = %{version}
Obsoletes:      ant-jakarta-bcel < %{version}

%description -n ant-apache-bcel
Apache Ant is a Java-based build tool.

This package contains optional apache bcel tasks for Apache Ant.

%package -n ant-apache-oro
Summary:        Optional apache oro tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  oro
Requires:       oro
%ant_junit_requires_eq    ant
Provides:       ant-jakarta-oro = %{version}
Obsoletes:      ant-jakarta-oro < %{version}

%description -n ant-apache-oro
Apache Ant is a Java-based build tool.

This package contains optional apache oro tasks for Apache Ant.

%package -n ant-apache-regexp
Summary:        Optional apache regexp tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  regexp
Requires:       regexp
%ant_junit_requires_eq    ant
Provides:       ant-jakarta-regexp = %{version}
Obsoletes:      ant-jakarta-regexp < %{version}

%description -n ant-apache-regexp
Apache Ant is a Java-based build tool.

This package contains optional apache regexp tasks for Apache Ant.

%package -n ant-apache-xalan2
Summary:        Optional apache xalan2 tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  regexp
BuildRequires:  xalan-j2
Requires:       regexp
%ant_junit_requires_eq    ant

%description -n ant-apache-xalan2
Optional apache xalan2 tasks for %{name}.

%package -n ant-imageio
Summary:        Optional imageio tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
%ant_junit_requires_eq    ant

%description -n ant-imageio
Apache Ant is a Java-based build tool.

This package contains optional imageio tasks for Apache Ant.

%package -n ant-javamail
Summary:        Optional javamail tasks for ant
License:        CDDL-1.0
Group:          Development/Tools/Building
BuildRequires:  javamail >= 1.2-5jpp
Requires:       javamail >= 1.2-5jpp
%ant_junit_requires_eq    ant

%description -n ant-javamail
Apache Ant is a Java-based build tool.

This package contains optional javamail tasks for Apache Ant.

%package -n ant-jdepend
Summary:        Optional jdepend tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  jdepend
Requires:       jdepend
%ant_junit_requires_eq    ant

%description -n ant-jdepend
Apache Ant is a Java-based build tool.

This package contains optional jdepend tasks for Apache Ant.

%package -n ant-jsch
Summary:        Optional jsch tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
BuildRequires:  jsch
Requires:       jsch
%ant_junit_requires_eq    ant

%description -n ant-jsch
Apache Ant is a Java-based build tool.

This package contains optional jsch tasks for Apache Ant.

%package -n ant-xz
Summary:        Opional xz tasks for ant
License:        Apache-2.0
Group:          Development/Tools/Building
Requires:       xz-java
%ant_junit_requires_eq    ant

%description -n ant-xz
Apache Ant is a Java-based build tool.

This package contains optional xz tasks for Apache Ant.

%package -n ant-testutil
Summary:        Test utility classes for ant
License:        Apache-2.0
Group:          Development/Tools/Building
Requires:       junit4
%ant_junit_requires_eq    ant

%description -n ant-testutil
Test utility tasks for %{name}.

%package -n ant-manual
Summary:        Manual for ant
License:        Apache-2.0
Group:          Development/Tools/Building

%description -n ant-manual
Apache Ant is a Java-based build tool.

This package contains the manual for Apache Ant.

%endif

%prep
%setup -q -n apache-ant-%{version}
#Fixup version
find -name build.xml -o -name pom.xml | xargs sed -i -e s/-SNAPSHOT//
find -name \*.jar -print -delete

# When bootstrapping, we don't have junit
%if %{with bootstrap}
%patch 0 -p1
%endif
%patch 1
%patch 2 -p1
%patch 3 -p1
%patch 5 -p1
%patch 6 -p1

# clean jar files
find . -name "*.jar" -print -delete

# Log4jListener is deprecated by upstream: Apache Log4j (1) is not
# developed any more. Last release is 1.2.17 from 26 May 2012 and
# contains vulnerability issues.
rm src/main/org/apache/tools/ant/listener/Log4jListener.java

# failing testcases. TODO see why
%if %{with antlr} || %{with junit}
rm  src/tests/junit/org/apache/tools/mail/MailMessageTest.java \
    src/tests/junit/org/apache/tools/ant/taskdefs/ExecuteWatchdogTest.java \
    src/tests/junit/org/apache/tools/ant/taskdefs/JavaTest.java \
    src/tests/junit/org/apache/tools/ant/taskdefs/TestProcess.java
%endif

#install jars
%if %{with junit} || %{with junit5}
build-jar-repository -s -p lib/optional junit4
%endif
%if %{with junit5}
build-jar-repository -s -p lib/optional junit5 opentest4j
%endif
%if %{with antlr}
# we need to build junit in antlr, but we remove it later
build-jar-repository -s -p lib/optional xerces-j2 xml-commons-apis-bootstrap antlr-bootstrap bcel javamail/mailapi jdepend junit4 oro regexp bsf commons-logging commons-net jsch xalan-j2 xalan-j2-serializer xml-resolver xz-java
%endif

# Fix file-not-utf8 rpmlint warning
iconv KEYS -f iso-8859-1 -t utf-8 -o KEYS.utf8
mv KEYS.utf8 KEYS
iconv LICENSE -f iso-8859-1 -t utf-8 -o LICENSE.utf8
mv LICENSE.utf8 LICENSE
# -----------------------------------------------------------------------------

%build
export OPT_JAR_LIST=:

%if %{with antlr} || %{with junit} || %{with junit5}
ant -Dbuild.sysclasspath=first jars test-jar

#remove empty jai and netrexx jars. Due to missing dependencies they contain only manifests.
rm -rf build/lib/ant-jai.jar build/lib/ant-netrexx.jar
%endif

%if %{with bootstrap}
export GC_MAXIMUM_HEAP_SIZE="134217728" #128M
export JAVA_HOME="%{java_home}"
sh -x ./build.sh --noconfig jars

%endif
%?strip_all_nondeterminism

# log4j logging is deprecated
rm -f build/lib/ant-apache-log4j.jar

%install
# ANT_HOME and subdirs
mkdir -p %{buildroot}%{ant_home}/{lib,etc}
# jars
install -d -m 755 %{buildroot}%{_javadir}/ant
install -d -m 755 %{buildroot}%{_mavenpomdir}

%if %{without junit} && %{without junit5}
  rm build/lib/ant-junit*.jar
%else
  %if %{without junit}
    rm build/lib/ant-junit.jar
    rm build/lib/ant-junit4.jar
  %else
    # empty in this scenario
    rm build/lib/ant-junitlauncher.jar
  %endif
  # remove all others
  for i in build/lib/ant-*.jar ; do
    case $i in
     */ant-junit*)
       ;;
     *)
       rm -v $i
       ;;
    esac
  done
%endif

for jar in build/lib/*.jar
do
  jarname=$(basename $jar .jar)
  pomname="${jarname}.pom"

  #Determine where to put it
  case $jarname in
#These go into %%{_javadir}, pom files have different names
  ant | ant-bootstrap | ant-launcher)
%if %{with bootstrap}
  destdir="%{buildroot}%{_javadir}/ant"; destname="ant/";pomname="$jarname.pom"
%else
  continue
%endif
  ;;
  ant-jmf|ant-swing)
%if %{with bootstrap}
  destdir="%{buildroot}%{_javadir}/ant"; destname="ant/";
%else
  continue
%endif
  ;;
#Bootstracp builds an incomplete ant-foo jars, don't ship them
  *)
%if %{with bootstrap}
  continue
%else
#These go into %%{_javadir}/ant
  destdir="%{buildroot}%{_javadir}/ant"; destname="ant/";
%endif
  ;;
  esac

  #instal jar
  install -m 644 ${jar} ${destdir}/${jarname}.jar
  # jar aliases
  ln -sf ../../java/${destname}${jarname}.jar %{buildroot}%{ant_home}/lib/${jarname}.jar

  #bootstrap does not have a pom
  if [ "$jarname" = ant-bootstrap ]; then
    mkdir -p src/etc/poms/${jarname}
    sed -e "s#@VERSION@#%{version}#g" < %{SOURCE10} > src/etc/poms/${jarname}/pom.xml
  fi

  #install pom
  if [ "$jarname" != ant-bootstrap ]; then
    %pom_remove_parent src/etc/poms/${jarname}/pom.xml
  fi
  install -m 644 src/etc/poms/${jarname}/pom.xml %{buildroot}/%{_mavenpomdir}/${pomname}
  if [ "$jarname" = ant-launcher ]; then
    %add_maven_depmap ${pomname} ${destname}${jarname}.jar -a ant:ant-launcher
  elif [ "$jarname" = ant-jmf ]; then
    %add_maven_depmap ${pomname} ${destname}${jarname}.jar -f jmf
  elif [ "$jarname" = ant-swing ]; then
    %add_maven_depmap ${pomname} ${destname}${jarname}.jar -f swing
  elif [ "$jarname" = ant ]; then
    %add_maven_depmap ${pomname} ${destname}${jarname}.jar -a org.apache.ant:ant-nodeps,apache:ant,ant:ant
  elif [ "$jarname" = ant-antlr -o "$jarname" = ant-bootstrap ]; then
    %add_maven_depmap ${pomname} ${destname}${jarname}.jar
  else
%if %{with junit} || %{with junit5}
    %add_maven_depmap ${pomname} ${destname}${jarname}.jar
%else
    %add_maven_depmap ${pomname} ${destname}${jarname}.jar -f ${jarname}
%endif
  fi
done

%if %{with bootstrap}

# scripts: remove dos and os/2 scripts
rm -f src/script/*.bat
rm -f src/script/*.cmd

# XSLs
cp -p src/etc/*.xsl %{buildroot}%{ant_home}%{_sysconfdir}
rm -f  %{buildroot}%{ant_home}%{_sysconfdir}/{maudit-frames,jdepend,jdepend-frames,junit-frames,junit-noframes}.xsl
%endif
%if %{with junit}
cp -p src/etc/{junit-noframes,junit-frames}.xsl %{buildroot}%{ant_home}%{_sysconfdir}
%endif
%if %{with antlr}
cp -p src/etc/{maudit-frames,jdepend,jdepend-frames}.xsl %{buildroot}%{ant_home}%{_sysconfdir}
%endif

%if %{with bootstrap}
# install everything else
mkdir -p %{buildroot}%{_bindir}
cp -p src/script/* %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/%{name}/bin/
ln -sf %{_bindir}/antRun %{buildroot}/%{_datadir}/%{name}/bin/antRun
%endif

mkdir -p %{buildroot}%{_sysconfdir}/ant.d

%if %{with bootstrap}
# default ant.conf
mkdir -p %{buildroot}%{_sysconfdir}
cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/ant.conf

# OPT_JAR_LIST fragments
echo "ant/ant-jmf" > %{buildroot}%{_sysconfdir}/%{name}.d/jmf
echo "ant/ant-swing" > %{buildroot}%{_sysconfdir}/%{name}.d/swing
%endif

%if %{with junit}
echo "junit ant/ant-junit" > %{buildroot}%{_sysconfdir}/ant.d/junit
echo "junit4 ant/ant-junit4" > %{buildroot}%{_sysconfdir}/ant.d/junit4
%endif

%if %{with junit5}
echo "junit5 hamcrest/core junit opentest4j ant/ant-junitlauncher" > %{buildroot}%{_sysconfdir}/ant.d/junitlauncher
%endif

%if %{with antlr}
echo "antlr ant/ant-antlr" > %{buildroot}%{_sysconfdir}/ant.d/antlr
echo "rhino bsf ant/ant-apache-bsf" > %{buildroot}%{_sysconfdir}/ant.d/apache-bsf
echo "xml-resolver ant/ant-apache-resolver" > %{buildroot}%{_sysconfdir}/ant.d/apache-resolver
echo "apache-commons-logging ant/ant-commons-logging" > %{buildroot}%{_sysconfdir}/ant.d/commons-logging
echo "apache-commons-net ant/ant-commons-net" > %{buildroot}%{_sysconfdir}/ant.d/commons-net
echo "bcel ant/ant-apache-bcel" > %{buildroot}%{_sysconfdir}/ant.d/apache-bcel
echo "oro ant/ant-apache-oro" > %{buildroot}%{_sysconfdir}/ant.d/apache-oro
echo "regexp ant/ant-apache-regexp" > %{buildroot}%{_sysconfdir}/ant.d/apache-regexp
echo "xalan-j2 ant/ant-apache-xalan2" > %{buildroot}%{_sysconfdir}/ant.d/apache-xalan2
echo "ant/ant-imageio" > %{buildroot}%{_sysconfdir}/ant.d/imageio
echo "javamail jaf ant/ant-javamail" > %{buildroot}%{_sysconfdir}/ant.d/javamail
echo "jdepend ant/ant-jdepend" > %{buildroot}%{_sysconfdir}/ant.d/jdepend
echo "jsch ant/ant-jsch" > %{buildroot}%{_sysconfdir}/ant.d/jsch
echo "xz-java ant/ant-xz" > %{buildroot}%{_sysconfdir}/ant.d/xz
echo "testutil ant/ant-testutil" > %{buildroot}%{_sysconfdir}/ant.d/testutil
%endif

%if %{with bootstrap}
find %{buildroot}%{_datadir}/ant%{_sysconfdir} -type f -name "*.xsl" \
                                                 -a ! -name ant-update.xsl \
                                                 -a ! -name changelog.xsl \
                                                 -a ! -name coverage-frames.xsl \
                                                 -a ! -name junit-frames-xalan1.xsl \
                                                 -a ! -name log.xsl \
                                                 -a ! -name mmetrics-frames.xsl \
                                                 -a ! -name tagdiff.xsl \
                                                 -print -delete
%endif
# remove *.orig
rm -rf %{buildroot}%{_bindir}/ant.orig

%if %{with bootstrap}
pushd %{buildroot}%{_javadir}
  for i in ant-bootstrap ant-launcher ant; do
    ln -sf ant/${i}.jar ${i}.jar
  done
popd

%files -f .mfiles
%license LICENSE NOTICE
%doc KEYS README WHATSNEW
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %{_bindir}/ant
%attr(0755,root,root) %{_bindir}/antRun
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-launcher.jar
%{_javadir}/%{name}-bootstrap.jar
%dir %{_javadir}/%{name}
%dir %{ant_home}
%dir %{ant_home}%{_sysconfdir}
%{ant_home}/bin
%{ant_home}%{_sysconfdir}/ant-update.xsl
%{ant_home}%{_sysconfdir}/changelog.xsl
%{ant_home}%{_sysconfdir}/coverage-frames.xsl
%{ant_home}%{_sysconfdir}/mmetrics-frames.xsl
%{ant_home}%{_sysconfdir}/log.xsl
%{ant_home}%{_sysconfdir}/tagdiff.xsl
%{ant_home}%{_sysconfdir}/junit-frames-xalan1.xsl
# % {ant_home}/etc/common2master.xsl
# % {ant_home}/etc/printFailingTests.xsl
%dir %{ant_home}/lib
%dir %{_sysconfdir}/%{name}.d
%{ant_home}/lib/ant.jar
%{ant_home}/lib/ant-bootstrap.jar
%{ant_home}/lib/ant-launcher.jar
%dir %{_sysconfdir}/ant.d
%endif

%if %{with antlr}
%files -f .mfiles
%{ant_home}/lib/ant-antlr.jar
%config(noreplace) %{_sysconfdir}/ant.d/antlr
%endif

%if %{with junit}
%files -f .mfiles
%{ant_home}/lib/ant-junit*.jar
%config(noreplace) %{_sysconfdir}/ant.d/junit
%config(noreplace) %{_sysconfdir}/ant.d/junit4
%{ant_home}%{_sysconfdir}/junit-frames.xsl
%{ant_home}%{_sysconfdir}/junit-noframes.xsl
%endif

%if %{with junit5}
%files -f .mfiles
%{ant_home}/lib/ant-junitlauncher.jar
%config(noreplace) %{_sysconfdir}/ant.d/junitlauncher
%endif

### Basic ant subpackages
%if %{with bootstrap}
%files -n ant-jmf -f .mfiles-jmf
%{ant_home}/lib/ant-jmf.jar
%config(noreplace) %{_sysconfdir}/ant.d/jmf

%files -n ant-swing -f .mfiles-swing
%{ant_home}/lib/ant-swing.jar
%config(noreplace) %{_sysconfdir}/ant.d/swing

%files -n ant-scripts
%defattr(0755,root,root,0755)
%{_bindir}/*.pl
%{_bindir}/*.py*
%endif #if bootstrap

%if %{with antlr}
%files -n ant-apache-bsf -f .mfiles-ant-apache-bsf
%{ant_home}/lib/ant-apache-bsf.jar
%config(noreplace) %{_sysconfdir}/ant.d/apache-bsf

%files -n ant-apache-resolver -f .mfiles-ant-apache-resolver
%{ant_home}/lib/ant-apache-resolver.jar
%config(noreplace) %{_sysconfdir}/ant.d/apache-resolver

%files -n ant-commons-logging -f .mfiles-ant-commons-logging
%{ant_home}/lib/ant-commons-logging.jar
%config(noreplace) %{_sysconfdir}/ant.d/commons-logging

%files -n ant-commons-net -f .mfiles-ant-commons-net
%{ant_home}/lib/ant-commons-net.jar
%config(noreplace) %{_sysconfdir}/ant.d/commons-net

%files -n ant-apache-bcel -f .mfiles-ant-apache-bcel
%{ant_home}/lib/ant-apache-bcel.jar
%config(noreplace) %{_sysconfdir}/ant.d/apache-bcel

%files -n ant-apache-oro -f .mfiles-ant-apache-oro
%{ant_home}/lib/ant-apache-oro.jar
%{ant_home}%{_sysconfdir}/maudit-frames.xsl
%config(noreplace) %{_sysconfdir}/ant.d/apache-oro

%files -n ant-apache-regexp -f .mfiles-ant-apache-regexp
%{ant_home}/lib/ant-apache-regexp.jar
%config(noreplace) %{_sysconfdir}/ant.d/apache-regexp

%files -n ant-apache-xalan2 -f .mfiles-ant-apache-xalan2
%{ant_home}/lib/ant-apache-xalan2.jar
%config(noreplace) %{_sysconfdir}/ant.d/apache-xalan2

%files -n ant-imageio -f .mfiles-ant-imageio
%{ant_home}/lib/ant-imageio.jar
%config(noreplace) %{_sysconfdir}/ant.d/imageio

%files -n ant-javamail -f .mfiles-ant-javamail
%{ant_home}/lib/ant-javamail.jar
%config(noreplace) %{_sysconfdir}/ant.d/javamail

%files -n ant-jdepend -f .mfiles-ant-jdepend
%{ant_home}/lib/ant-jdepend.jar
%config(noreplace) %{_sysconfdir}/ant.d/jdepend
%{ant_home}%{_sysconfdir}/jdepend.xsl
%{ant_home}%{_sysconfdir}/jdepend-frames.xsl

%files -n ant-jsch -f .mfiles-ant-jsch
%{ant_home}/lib/ant-jsch.jar
%config(noreplace) %{_sysconfdir}/ant.d/jsch

%files -n ant-xz -f .mfiles-ant-xz
%{ant_home}/lib/ant-xz.jar
%config(noreplace) %{_sysconfdir}/ant.d/xz

%files -n ant-testutil -f .mfiles-ant-testutil
%{ant_home}/lib/ant-testutil.jar
%config(noreplace) %{_sysconfdir}/ant.d/testutil

%files -n ant-manual
%doc manual/*
%endif

%changelog
* Fri Nov 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.10.14-1
- Auto-upgrade to 1.10.14 - Azure Linux 3.0 - package upgrades

* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.10.11-2
- Move to SPECS 
- Minor refactor of specfile

* Thu Jan 20 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.11-1
- Removing dependency on 'log4j' using Fedora 36 spec for guidance (license: MIT).
- Updated version to 1.10.11.
- License verified.

* Thu Dec 09 2021 Thomas Crain <thcrain@microsoft.com> - 1.10.9-3
- Replace usage of removed %%requires_eq macro

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.9-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.10.9-1.1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Update python3-base to python3.

* Thu Oct  1 2020 Pedro Monreal <pmonreal@suse.com>
- Update to 1.10.9

  * Security fix: [bsc#1177180, CVE-2020-11979]
  - Insecure temporary file vulnerability
  * Fixed bugs:
  - The ftp task could throw a NullPointerException if an
    error occured.
  - Propertyset now also sees in-scope local properties.
  - Replaced ReaderInputStream with the version of Apache
    Commons IO due to problems with surrogate pairs.
  - <fixcrlf> will no longer remove the temporary file it
    just created before writing to it.
  - <sshexec> and <scp> didn't deal with wildcard hostnames
    in shs config files properly.
  * Other changes:
  - Ant will no longer log a warning if it doesn't find tools.jar.
  - The <jar> task accepts now a nested <indexjarsmapper>
    element that can be used to perform custom filename
    transformations for the <indexjars> archives.
  - Added a new PropertyEnumerator interface that extensions can
    provide if they are managing properties unknown to the Ant project.
  - Added some special code to support GraalVM JavaScript as
    javax.script scripting engine for JavaScript. In particular we
    relax some security settings of GraalVM so that scripts can access
    Ant objects.
  - Also Ant enables Nashorn compatibility mode by default, you can
    disable that by setting the magic Ant property
    ant.disable.graal.nashorn.compat to true.
  - If the magic property ant.tmpdir hasn't been set and Ant can
    control the permissions of directories it creates it will create an
    owner-owned temporary directory unaccessible to others as default
    tempdir as soon as a temporary file is created for the first time.

* Thu May 14 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Update to 1.10.8
  * Security fix: [CVE-2020-1945, bsc#1171696]
  - A new property ant.tmpdir provides improved control over the
    location Ant uses to create temporary files
  * sshexec failed to write output to a file if the file didn't exist
  * Fixes a regression in javac task involving command line argument files.
  * sshexec, sshsession and scp now support a new sshConfig parameter.
  It specified the SSH configuration file (typically ${user.home}/.ssh/config)
  defining the username and keyfile to be used per host.
  * "legacy-xml" formatter of junitlauncher task wasn't writing out
  exceptions that happen in @BeforeAll method of a test.
  * Fixes a potential ConcurrentModificationException in XMLLogger.
  * Fixes a bug in junitlauncher task in forked mode, where if a listener element
  was used as a sibling element for either the test or testclasses element,
  then the forked mode launch would fail.
  * Fixes an issue in AntStructure where an incorrect DTD was being generated.
  * Fixes an incorrect variable name usage in junit-frames-xalan1.xsl.
  * The runant.py script should now work with Python 3.
  * rmic has been removed from Java 15. The task will now throw an
  exception if you try to use it while running Java 15 or newer.
- Remove ant-python3.patch fixed upstream

* Wed May  6 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Add rhino to the ant-apache-bsf optional tasks [bsc#1134001]

* Wed May  6 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Remove jakarta-commons-* dependencies [bsc#1133997]
  * Use apache-commons-logging and apache-commons-net in optional tasks

* Tue Jan 14 2020 Fridrich Strba <fstrba@suse.com>
- Use xml-commons-apis-bootstrap as jar in classpath instead of
  the common xml-apis jar, since we are forcing build against
  the bootstrap package

* Fri Nov  8 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 1.10.7
- Modified patches:
  * apache-ant-bootstrap.patch
  * apache-ant-no-test-jar.patch
  * apache-ant-xml-apis.patch
  * reproducible-build-manifest.patch
    + rediff
- Fix ant-xz.jar to be non-empty and split it from the ant-antlr
  package

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against the new compatibility packages log4j12/log4j12-mini

* Mon Sep 30 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to parent poms from all artifacts and do not
  distribute the ant-parent, since we don't need it

* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Require directly xerces-j2 and not its virtual provide
  jaxp_parser_impl

* Mon Mar 18 2019 Jan Engelhardt <jengelh@inai.de>
- Make "if" statements in build recipe POSIX sh compatible.

* Fri Feb  8 2019 Fridrich Strba <fstrba@suse.com>
- Create an ant-junit5 package to build junit5 optional tasks
  when they become resolved
- Add a simple pom file for ant-bootstrap.jar

* Fri Feb  8 2019 Fridrich Strba <fstrba@suse.com>
- Add compatibility links ant/ant*.jar for bootstrap build

* Tue Feb  5 2019 Fridrich Strba <fstrba@suse.com>
- BuildRequire hamcrest for ant-junit and ant-antlr, since junit4
  depends strictly on hamcrest-core only.

* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- Build ant against xml-commons-apis-bootstrap and
  xml-commons-resolver-bootstrap in order to break build cycle

* Mon Dec 10 2018 Fridrich Strba <fstrba@suse.com>
- Don't build against a particular xml-apis/xml-resolver provider,
  but against the generic virtual provider. This allows easier
  bootstrapping.
- Added patch:
  * apache-ant-xml-apis.patch
    + look for the xml-apis.jar and xml-resolver.jar when composing
    classpath; they are symlinks provided by several packages.

* Mon Nov 26 2018 Fridrich Strba <fstrba@suse.com>
- Let ant-antlr provide ant-xz too, since it contains the
  corresponding jar.

* Wed Oct 31 2018 Fridrich Strba <fstrba@suse.com>
- Add aliases to some maven artifacts so that packages out there
  resolve then correctly

* Fri Oct 26 2018 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Update to 1.10.5 [bsc#1113136]
  * Same version as in 1.9.13 but with additional features and
    requires Java8 or higher.
  * Dropped patch to build with java8+ already fixed in this version
  - apache-ant-1.9.9-sourcetarget.patch
  * Refreshed patch:
  - apache-ant-class-path-in-manifest.patch

* Sun Oct 21 2018 antoine.belvire@opensuse.org
- Add reproducible-build-manifest.patch: Use less detailed version
  string for manifest's "Created-by" field (boo#1110024).

* Wed Oct 17 2018 Fridrich Strba <fstrba@suse.com>
- Require javapackages-local in order to generate correctly the
  maven requires and provides
- Install maven artifacts

* Fri Aug 24 2018 Jason Sikes <jsikes@suse.de>
- Update to 1.9.13
  * Fixes a regression in the "get" task where redirects
    from a HTTP resource to a HTTPS resource started throwing
    an exception.
    Bugzilla Report 62499
  * the new allowFilesToEscapeDest didn't work when set to false and
    archive entries contained relative paths with so many ".."
    segnments that the resulting path would go beyond the file system
    root.
    Bugzilla Report 62502, bsc#1100053, CVE-2018-10886

* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Modified patch:
  * apache-ant-1.9.9-sourcetarget.patch
  - Build with source/target 8

* Fri Feb 23 2018 ecsos@opensuse.org
- fix build error for Leap 42.3

* Thu Feb 22 2018 tchvatal@suse.com
- Add patch to run scripts with python3 if applicable bsc#1082202:
  * ant-python3.patch

* Thu Feb 22 2018 tchvatal@suse.com
- Update to 1.9.10:
  * Various fixes for java10
  * Small fixes all around
- Remove merged patch reproducible.patch

* Sat Oct 28 2017 jengelh@inai.de
- Simply use find -delete over xargs.
- Make description neutral.

* Tue Oct 24 2017 bwiedemann@suse.com
- Add reproducible-build-date.patch to allow to have fixed build dates
  to make other packages build more reproducibly

* Wed Oct  4 2017 fstrba@suse.com
- Remove dependency on java-1_5_0-gcj-compat-devel and build even
  the bootstrap package with java source and target 1.6

* Fri Sep 29 2017 fstrba@suse.com
- Don't condition the maven defines on release version, but on
  _maven_repository being defined

* Thu Sep 14 2017 fstrba@suse.com
- Allow bootstrapping with something else then
  java-1_5_0-gcj-compat, but still require
  java-1_5_0-gcj-compat-devel
- Added patch:
  * apache-ant-bootstrap.patch
  - Add -sourcepath option to fix build breakages with Eclipse
    Compiler for Java(tm)

* Wed Sep  6 2017 fstrba@suse.com
- Added patch:
  * apache-ant-1.9.9-sourcetarget.patch
    + Change java source and target versions to 1.6 to allow build
    with jdk9
- For non-boostrap builds require java-devel >= 1.6

* Fri Jun  9 2017 tchvatal@suse.com
- Do not generate poms on ant core packages to reduce deps and
  allow bootstrap

* Wed May 31 2017 tchvatal@suse.com
- Fix bootstrap to avoid new cycle bsc#1041966

* Fri May 19 2017 tchvatal@suse.com
- Disable javadoc completely it is on the web in much better form
- Remove if0 conditions
- Remove patch apache-ant-old-gcj-build.patch for sle11 and unused
- Fix build with split javapackages-tools

* Mon May  8 2017 bwiedemann@suse.com
- Version bump to 1.9.9:
  * Read WHATSNEW file for full changelist

* Mon May  8 2017 bwiedemann@suse.de
- Add reproducible.patch to allow reproducible builds of ant itself
  and packages built with ant like jcodings

* Mon Feb 20 2017 tchvatal@suse.com
- Revert the previous change as it broke the build of most java
  software stack

* Mon Feb 13 2017 guoyunhebrave@gmail.com
- Add profile.d scripts to set ANT_HOME

* Fri Jan 15 2016 opensuse@dstoecker.de
- junit4 test did not work (bnc#915686)

* Wed Jul 29 2015 tchvatal@suse.com
- Add xalan-j2-serializer to ant-antlr requirements

* Tue Jul 28 2015 tchvatal@suse.com
- Sync the changes files among the subpkgs
- Version bump to 1.9.6:
  * Read WHATSNEW file for full changelist

* Sun Jun 21 2015 jengelh@inai.de
- Do better quoting to get better error messages when it fails

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Thu Aug 28 2014 coolo@suse.com
- to bootstrap 13.2 we need another split because bsf depends on things
  that depend on junit and as antlr requires bsf, we need a 3rd step ->
  split ant-junit to build in between ant and ant-antlr
  
* Fri Jul  4 2014 tchvatal@suse.com
- Fix building on SLE.
- Added patch:
  * apache-ant-old-gcj-build.patch

* Fri Jul  4 2014 tchvatal@suse.com
- Update to 1.9.4:
  * Read WHATSNEW file for full changelist
  * initial support for Java 1.9
  * <junit> has now a threads attribute allowing to run the tests in
    several threads. Bugzilla Report 55925
  * TarInputStream will now read archives created by tar
    implementations that encode big numbers by not adding a trailing
    NUL.

* Thu May 15 2014 peter.trommler@ohm-hochschule.de
- fix summary (was antlr summary)

* Mon May 12 2014 darin@darins.net
- SLE_11 specific spec files for ant/ant-antlr. These build with
  openjdk, which introduced bootstrap breakage in Factory.
- Update pre_checkin.sh for SLE_11 specific spec's

* Fri May  2 2014 tchvatal@suse.com
- Revert the bootstrap breakage.

* Thu Apr 24 2014 dmueller@suse.com
- remove dependency on gpg-offline (blocks rebuilds and
  tarball integrity is checked by source-validator anyway, plus
  it was commented out)
- remove apache-ant-bz163689.patch (was not applied anywhere)

* Wed Apr 23 2014 darin@darins.net
- Update packaging to build the openjdk and not gcj

* Thu Jan  2 2014 mvyskocil@suse.com
- Update to 1.9.3
- BugFixes:
  * Ant 1.8 exec task changes have slowed exec to a crawl, apache#54128
  * <parallel> swallowed the status code of nested <fail> tasks,
  apache#55539
  * a race condition could make <fixcrlf> tasks of parallel builds to
    interfere with each other, apache#54393
  * <mail>'s mailport still didn't work properly when using smtps,
  apache#49267
  * using attributes belonging to the if and unless namespaces
  made macrodef fail, apache#55885.
  * Apt is not available under JDK 1.8, apache#55922
- drop unused macros
- add gpg verification

* Wed Dec  4 2013 mvyskocil@suse.com
- use requires_eq instead of manual call of rpm -q

* Wed Oct  2 2013 mvyskocil@suse.com
- install compat symlink to /usr/share/ant/bin/antRun to make scala build

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Thu Aug 22 2013 mvyskocil@suse.com
- Update to 1.9.2
- Incompatible changes:
  * ProjectHelper's implementation import and include tasks
  defaults the targetPrefix to ProjectHelper.USE_PROJECT_NAME_AS_TARGET_PREFIX.
  ProjectHelper2 is not affected, apache#54940.
  * FixCRLF used to treat the EOL value ASIS to convert to the system property
  line.separator. Specified was that ASIS would leave the EOL characters alone,
  the task now really leaves the EOL characters alone. This also implies that
  EOL ASIS will not insert a newline even if fixlast is set to true.
  apache#53036
  * The CommandLauncher hierarchy that used to be a set of inner
  classes of Execute has been extracted to the
  org.apache.tools.ant.taskdefs.launcher package.
  * Any FileResource whose represented File has a parent also has a basedir.
  * Removing the Perforce Ant tasks replaced by tasks supplied by Perforce Inc.
  * Setting the default encoding of StringResource to UTF-8 instead of null
- Bugfixes:
  * <javadoc> post-process generated docs to migitiate frame
    injection attack (CVE-2013-1571) apache#55132
  * Parsing of zip64 extra fields has become more lenient
  * TarInputStream should now properly read GNU longlink entries' names.
  apache#55040.
  * <java> and <exec> used to be too restrictive when evaluating
  whether a given set of options is compatible with spawning the new
  process, apache#55112.
  * Corrected XSLTC error in <junitreport>, apache#54641.
  * and many more, see WHATSNEW for details

* Mon Jan  7 2013 mvyskocil@suse.com
- remove xerces-j2-bootstrap depenency (bnc#789163)

* Wed May 30 2012 cfarrell@suse.com
- license update: CDDL-1.0
  SPDX format (note that it should CDDL-1.1 if the (c) owner and license
  steward is Oracle)

* Tue May 15 2012 mvyskocil@suse.cz
- build ignore java-1_7_0-openjdk as well

* Wed Feb  1 2012 mvyskocil@suse.cz
- revert the Recommends to fix a lot of build fails

* Wed Jan 25 2012 mvyskocil@suse.cz
- use new _mavendepmapfragdir macro instead of hardocded path
- change java-devel Requires to Recommends

* Tue Jan  3 2012 dmueller@suse.de
- use dist-lite and dist_javadocs to make javadoc build really
  optional
- fix arm check (ifarch does not work in a noarch spec file)

* Thu Dec 15 2011 mvyskocil@suse.cz
- use dist and javadocs targets to make javadoc build really configurable
- disable javadoc build on arm to speedup the build of java platform

* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile

* Mon Mar 14 2011 mvyskocil@suse.cz
- ignore openjdk for build of core ant

* Wed Mar  9 2011 mvyskocil@suse.cz
- Update to ant 1.8.2
  * performance improvements in directory scanning
  * XSLT task honors classpath again (bugrep 49271)
  * distinction between core tasks and optional tasks is abolished
  * new task augment allows to add attributes or nested elements to previously
    defined references
  * Lexically scoped local properties, i.e. properties that are only defined
    inside a target, sequential block or similar environment. This is very
    useful inside of <macrodef>s where a macro can now define a temporary
    property that will disappear once the task has finished.
  * <import> can now import from any file- or URL-providing resource - this
    includes <javaresource>. This means <import> can read build file snippets
    from JARs or fixed server URLs. There are several other improvements in the
    area of import.
  * Various improvements to the directory scanning code that help with symbolic
    link cycles (as can be found on MacOS X Java installations for example) and
    improve scanning performance. For big directory trees the improvement is
    dramatic.
  * The way developers can extend Ant's property expansion algorithm has been
    rewritten (breaking the older API) to be easier to use and be more
    powerful. The whole local properties mechanism is implemented using that
    API and could be implemented in a separate library without changes in Ant's
    core. Things like the yet-to-be-released props Antlib can now provide often
    required "scripty" fuctions without touching Ant itself. At the same time
    the if and unless attributes have been rewritten to do the expected thing
    if applied to a property expansion (i.e. if="${foo}" will mean "yes, do it"
    if ${foo} expands to true, in Ant 1.7.1 it would mean "no" unless a
    property named "true" existed). This adds "testing conditions" as a new
    use-case to property expansion.
  * A new top-level element <extension-point> assists in writing re-usable
    build files that are meant to be imported. <extension-point> has a name and
    a dependency-list like <target> and can be used like a <target> from the
    command line or a dependency-list but the importing build file can add
    targets to the <extension-point>'s depends list.
  * Ant now requires Java 1.4 or later new task include provides an alternative
  to <import> that should be preferred when you don't want to override any
  targets
  * numerous bug fixes and improvements as documented in
    Bugzilla and in WHATSNEW
- merge the nodeps and trax packages to main one
- build ant-antlr.spec using openjdk
- add ant-apache-xalan2 and ant-testutil
- remove all pom files, as they are included and build from source tarball

* Fri Apr  9 2010 mvyskocil@suse.cz
- fix bnc#595144 - Compiled binary in ant
  remove test.exe from source tarball

* Thu Mar 18 2010 mvyskocil@suse.cz
- fix the compat symlinks

* Wed Mar 17 2010 mvyskocil@suse.cz
- return back the /usr/share/ant/lib compat symlinks
  http://lists.opensuse.org/opensuse-java/2010-03/msg00007.html

* Wed Jun 17 2009 mvyskocil@suse.cz
- do not use Release number in Requires of subpackages

* Sun May  3 2009 ro@suse.de
- do not assume release number for ant and ant-antlr are identical

* Tue Apr 28 2009 mvyskocil@suse.cz
- update to 1.7.1. Upstream changes (full list is in WHATSNEW):
  * String resources only have properties single expanded. If you relied on
  <string> resources being expanded more than once, it no longer happens.
  Bugzilla report 42277.
  * A String resource's encoding attribute was only taken into account when
  set from the resource's OutputStream; the InputStream provided the String's
  binary content according to the platform's default encoding. Behavior has
  been modified to encode outgoing (InputStream) content as well as encoding
  incoming (OutputStream) content.
  * <java> with fork now returns gives -1 instead of 0 as result when
  * failonerror
  is false and some exception (including timeout) occurs. Br 42377.
  * ant-type attribute has been marked as deprecated and a warning has been
  issued if it is encountered in the build file.
  * FileUtils.createTempFile now actually creates the file.
  The TempFile task still does not create the file by default, can be
  instructed to do so however using a new parameter.  Bugzilla report 33969.
- added maven pom files from jpackage project
- synchronized ant.spec with jpackage.org 5.0
- used ant-antlr-prepare.sh for generate of ant-antlr.spec from ant.spec to
  keep them synchronized. Build is branched using value of %%%%bootstrap macro:
  * bootstrap == 1 means build ant, ant-{jmf,nodeps,scripts,swing,trax}
  * bootstrap == 0 means build rest of ant modules + ant-javadoc

* Mon Nov  3 2008 mvyskocil@suse.cz
- [bnc#440645] - ant fails without installed jdk:
  - added a java-devel to Recommends:
  
* Mon Jul 21 2008 ro@suse.de
- use xerces-j2-bootstrap to build (as early as possible)
- add java doc dir to filelist of javadoc subpackage to fix build

* Wed Jul 16 2008 coolo@suse.de
- avoid another build cycle

* Wed May  7 2008 mvyskocil@suse.cz
- build using gcj, to allow a openjdk6 bootstrap
- change a source and a target level to 1.5 in build.xml

* Tue Aug 14 2007 skh@suse.de
- disable junit tests and remove junit from BuildRequires to break
  circular build dependency

* Fri Jul  6 2007 dbornkessel@suse.de
- update to version 1.7.0
  major changes are (for a complete list, consult /usr/share/doc/packages/ant/WHATSNEW):
  Changes that could break older environments:
  - ------------------------------------------
  * Initial support for JDK 6 (JSR 223) scripting.
  <*script*> tasks will now use javax.scripting if BSF is
  not available, or if explicitly requested by using
  a "manager" attribute.
  * The -noproxy option which was in the previous 1.7 alpha and beta
  releases has been removed. It is the default behavior and not needed.
  * Removed launcher classes from nodeps jar.
  * <classconstants> filter reader uses ISO-8859-1 encoding to read
  the java class file. Bugzilla report 33604.
  * Defer reference process. Bugzilla 36955, 34458, 37688.
  This may break build files in which a reference was set in a target which was
  never executed. Historically, Ant would set the reference early on, during parse
  time, so the datatype would be defined. Now it requires the reference to have
  been in a bit of the build file which was actually executed. If you get
  an error about an undefined reference, locate the reference and move it somewhere
  where it is used, or fix the depends attribute of the target in question to
  depend on the target which defines the reference/datatype.
  * <script> and <scriptdef> now set the current thread context.
  * Unrestrict the dbvendor names in the websphere element of the ejbjar task.
  Bugzilla Report 40475.
  * <env> nested element in <java>, <exec> and others is now case-insensitive
  for windows OS. Bugzilla Report 28874.
  * Removed support for xalan1 completely. Users of Xalan1 for Ant builds will
  have to stay at ant 1.6.5 or upgrade to xalan2.
  * Use org.apache.log4j.Logger instead of org.apache.log4j.Category.
  Category has been deprecated for ~2 years and has been removed from
  the log4j code.  Logger was introduced in log4j 1.2 so users of
  log4j 1.1 and log4j 1.0 need to upgrade to a newer version of log4j.
  Bugzilla Report 31951.
  * build.sysclasspath now also affects the bootclasspath handling of
  spawned Java VMs.  If you set build.sysclasspath to anything other
  than "ignore" (or leave it unset, since "ignore" is the default when
  it comes to bootclasspath handling), then the bootclasspath of the
  VM running Ant will be added to the bootclasspath you've specified.
  * The <java fork="false"> now as per default installs a security manager
  using the default permissions. This is now independent of the
  failonerror attribute.  Bugzilla report 33361.
  * <signjar> now notices when the jar and signedjar are equal, and switches
  to the same dependency logic as when signedjar is omitted. This may break
  something that depended upon signing in this situation. However, since
  invoking the JDK jarsigner program with -signedjar set to the source jar
  actually crashes the JVM on our (Java1.5) systems, we don't think any
  build files which actually worked will be affected by the change.
  * <signjar> used to ignore a nested fileset when a jar was also provided as an
  attribute, printing a warning message; now it signs files in the fileset.
  * An improved method of handling timestamp granularity differences between
  client and server was added to the <ftp> task.  FTP servers typically
  have HH:mm timestamps whereas local filesystems have HH:mm:ss timestamps.
  Previously, this required tweaking with the timediffmillis attribute
  which also was used to handle timezone differences.  Now, there is a new
  timestampgranularity attribute.  The default value for get operations is 0
  since the user has the more powerful preservelastmodified attribute to work
  with.  Since this is not available on put operations the default value
  adds a minute to the server timestamp in order to account for this,
  Scripts which previously used timediffmillis to do this compensation may
  need to be rewritten.  timediffmillis has now been deprecated.
  * On Java1.5+, Ant automatically sets the system property
  java.net.useSystemProxies to true, which gives it automatic use of the local
  IE (Windows) or Gnome2 (Unix/Linux) proxy settings. This may break any build
  file that somehow relied on content outside the firewall being unreachable:
  use the -noproxy command-line option to disable this new feature.
  Note that the Java1.5 proxy configuration system still does not
  appear to work reliably on Windows or Linux.
  * Support for the XSL:P XML parser has been removed.
  Bugzilla Report 23455.
  * Visual Age for Java optional tasks removed.
  * Testlet (test) optional task removed.
  * Icontract optional task removed.
  * Metamata (maudit, mmetrics, and mparse tasks) removed.
  * Sitraka (jpcoverage, jpcovmerge, jpcovreport) tasks suppressed.
  * <fixcrlf> used 
 (Mac) line endings on OS X, whose proper line separator
  is 
 (Unix).  Bugzilla report 39585.
  * <scp> now optionally supports the sftp protocol, you may need a
  newer jsch.jar.  Bugzilla Report 39373.
  * Ant launcher program prints errors to stderr, and exits with a 2 exit code
  value if, for any reason, it cannot actually start Ant proper. This will only
  affect programs/scripts that called the launcher and which did not want to
  receive an error if Ant itself would not start
  * All .NET tasks are now deprecated in favor of the new .NET Antlib:
  http://ant.apache.org/antlibs/dotnet/index.html

* Fri Sep 22 2006 dbornkessel@suse.de
- read in properties in /etc/ant.conf
- added source=1.4

* Mon May  8 2006 dbornkessel@suse.de
- only ant-antlr updates

* Thu Feb  2 2006 dbornkessel@suse.de
- fixed rpmlint errors and warnings

* Tue Jan 31 2006 dbornkessel@suse.de
- only ant-antlr updates

* Fri Jan 27 2006 dbornkessel@suse.de
- added four missing xsl files
- removed JAVA_HOME magic

* Tue Jan 24 2006 dbornkessel@suse.de
- Not dependend on xml-commons-apis, which are provided by xerces-j2, which does not
  depend on ant package (in contrast to old dependency on
  xml-commons-apis <-> ant)
- optional task are now again in extra spec file ant-antlr

* Thu Jan 19 2006 dbornkessel@suse.de
- Integrated ant and ant-antlr again in one spec file as there is no
  dependency loop ... jpackage BuildRequires were wrong.
- updated to version 1.6.5

* Mon Dec 19 2005 dbornkessel@suse.de
- added if statement that hinders unwanted creation of a file within a for loop

* Wed Sep 28 2005 dmueller@suse.de
- add norootforbuild

* Fri Mar  4 2005 skh@suse.de
- rely on jpackage-utils' java-functions to set JAVA_HOME correctly

* Sun Sep  5 2004 skh@suse.de
- create and add /usr/share/java/ant to file list for optional
  tasks to put their jars into

* Thu Sep  2 2004 skh@suse.de
- renamed from apache-ant to ant
- switched to JPackage 1.5 version
- updated to version 1.6.2
- split off optional tasks into separate package to solve build
  dependency loop in JPackage
