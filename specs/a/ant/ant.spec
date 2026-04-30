## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 33;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%bcond_with bootstrap

%if %{without bootstrap}
%bcond_with ant_minimal
%else
%bcond_without ant_minimal
%endif

%global ant_home %{_datadir}/ant

Name:           ant
Version:        1.10.15
Release:        %autorelease
Summary:        Java build tool
Summary(it):    Tool per la compilazione di programmi java
Summary(fr):    Outil de compilation pour java
License:        Apache-2.0
URL:            https://ant.apache.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/ant/source/apache-ant-%{version}-src.tar.bz2
Source2:        apache-ant-1.8.ant.conf
# manpage
Source3:        ant.asciidoc

Patch:          %{name}-build.xml.patch

BuildRequires:  rubygem-asciidoctor

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  javapackages-local-openjdk25
BuildRequires:  ant-openjdk25 
BuildRequires:  ant-junit
%endif

%if %{without ant_minimal}
BuildRequires:  mvn(antlr:antlr)
BuildRequires:  mvn(bcel:bcel)
BuildRequires:  mvn(bsf:bsf)
BuildRequires:  mvn(com.jcraft:jsch)
BuildRequires:  mvn(commons-net:commons-net)
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(jakarta.mail:jakarta.mail-api)
BuildRequires:  mvn(jdepend:jdepend)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-logging::api:)
BuildRequires:  mvn(org.tukaani:xz)
BuildRequires:  mvn(oro:oro)
BuildRequires:  mvn(regexp:regexp)
BuildRequires:  mvn(xalan:xalan)
BuildRequires:  mvn(xml-resolver:xml-resolver)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.hamcrest:hamcrest-library)

BuildRequires:  junit5
%endif

Requires:       %{name}-lib = %{version}-%{release}
Requires:       %{name}-jdk-binding
Suggests:       %{name}-openjdk25 = %{version}-%{release}

# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:1.10.15-21

%description
Apache Ant is a Java library and command-line tool whose mission is to
drive processes described in build files as targets and extension
points dependent upon each other.  The main known usage of Ant is the
build of Java applications.  Ant supplies a number of built-in tasks
allowing to compile, assemble, test and run Java applications.  Ant
can also be used effectively to build non Java applications, for
instance C or C++ applications.  More generally, Ant can be used to
pilot any type of process which can be described in terms of targets
and tasks.

%description -l fr
Ant est un outil de compilation multi-plateformes pour java. Il est
utilisé par les projets apache-jakarta et apache-xml.

%description -l it
Ant e' un tool indipendente dalla piattaforma creato per faciltare la
compilazione di programmi java.
Allo stato attuale viene utilizzato dai progetti apache jakarta ed
apache xml.

%package lib
Summary:        Core part of %{name}

%description lib
Core part of Apache Ant that can be used as a library.

%package junit
Summary:        Optional junit tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description junit
Optional junit tasks for %{name}.

%description junit -l fr
Taches junit optionelles pour %{name}.

%if %{without ant_minimal}

%package jmf
Summary:        Optional jmf tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description jmf
Optional jmf tasks for %{name}.

%description jmf -l fr
Taches jmf optionelles pour %{name}.

%package swing
Summary:        Optional swing tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description swing
Optional swing tasks for %{name}.

%description swing -l fr
Taches swing optionelles pour %{name}.

%package antlr
Summary:        Optional antlr tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description antlr
Optional antlr tasks for %{name}.

%description antlr -l fr
Taches antlr optionelles pour %{name}.

%package apache-bsf
Summary:        Optional apache bsf tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description apache-bsf
Optional apache bsf tasks for %{name}.

%description apache-bsf -l fr
Taches apache bsf optionelles pour %{name}.

%package apache-resolver
Summary:        Optional apache resolver tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description apache-resolver
Optional apache resolver tasks for %{name}.

%description apache-resolver -l fr
Taches apache resolver optionelles pour %{name}.

%package commons-logging
Summary:        Optional commons logging tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description commons-logging
Optional commons logging tasks for %{name}.

%description commons-logging -l fr
Taches commons logging optionelles pour %{name}.

%package commons-net
Summary:        Optional commons net tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description commons-net
Optional commons net tasks for %{name}.

%description commons-net -l fr
Taches commons net optionelles pour %{name}.

%package apache-bcel
Summary:        Optional apache bcel tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description apache-bcel
Optional apache bcel tasks for %{name}.

%description apache-bcel -l fr
Taches apache bcel optionelles pour %{name}.

%package apache-oro
Summary:        Optional apache oro tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description apache-oro
Optional apache oro tasks for %{name}.

%description apache-oro -l fr
Taches apache oro optionelles pour %{name}.

%package apache-regexp
Summary:        Optional apache regexp tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description apache-regexp
Optional apache regexp tasks for %{name}.

%description apache-regexp -l fr
Taches apache regexp optionelles pour %{name}.

%package apache-xalan2
Summary:        Optional apache xalan2 tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description apache-xalan2
Optional apache xalan2 tasks for %{name}.

%description apache-xalan2 -l fr
Taches apache xalan2 optionelles pour %{name}.

%package imageio
Summary:        Optional imageio tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description imageio
Optional imageio tasks for %{name}.

%package jakartamail
Summary:        Optional jakartamail tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description jakartamail
Optional jakartamail tasks for %{name}.

%description jakartamail -l fr
Taches jakartamail optionelles pour %{name}.

%package jdepend
Summary:        Optional jdepend tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description jdepend
Optional jdepend tasks for %{name}.

%description jdepend -l fr
Taches jdepend optionelles pour %{name}.

%package jsch
Summary:        Optional jsch tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description jsch
Optional jsch tasks for %{name}.

%description jsch -l fr
Taches jsch optionelles pour %{name}.

%package junit5
Summary:        Optional junit5 tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description junit5
Optional junit5 tasks for %{name}.

%description junit5 -l fr
Taches junit5 optionelles pour %{name}.

%package testutil
Summary:        Test utility classes for %{name}
Requires:       %{name} = %{version}-%{release}

%description testutil
Test utility tasks for %{name}.

%package xz
Summary:        Optional xz tasks for %{name}
Requires:       %{name} = %{version}-%{release}

%description xz
Optional xz tasks for %{name}.

%package manual
Summary:        Manual for %{name}
# ant-manual contains file tutorial-tasks-filesets-properties.zip
# which in turn contains src/Find.java and src/FindTest.java both
# licensed under ASL 1.1. See rhbz#1055629
License:        Apache-2.0 AND Apache-1.1

%description manual
Documentation for %{name}.

%description manual -l it
Documentazione di %{name}.

%description manual -l fr
Documentation pour %{name}.

%endif

# -----------------------------------------------------------------------------

%prep
%autosetup -p1 -C

# clean jar files
find . -name "*.jar" | xargs -t rm

# failing testcases. TODO see why
rm src/tests/junit/org/apache/tools/ant/types/selectors/SignedSelectorTest.java \
   src/tests/junit/org/apache/tools/ant/taskdefs/condition/IsFileSelectedTest.java \
   src/tests/junit/org/apache/tools/ant/taskdefs/condition/IsSignedTest.java \
   src/tests/junit/org/apache/tools/ant/taskdefs/optional/image/ImageIOTest.java \
   src/tests/junit/org/apache/tools/ant/taskdefs/JarTest.java \
   src/tests/junit/org/apache/tools/mail/MailMessageTest.java

# Test relies on internal JUnit 5 API that was changed
rm src/tests/junit/org/apache/tools/ant/taskdefs/optional/junitlauncher/LegacyXmlResultFormatterTest.java

# Log4jListener is deprecated by upstream: Apache Log4j (1) is not
# developed any more. Last release is 1.2.17 from 26 May 2012 and
# contains vulnerability issues.
rm src/main/org/apache/tools/ant/listener/Log4jListener.java

#install jars
%if %{with bootstrap}
ln -s %{_datadir}/javapackages-bootstrap/junit.jar lib/optional/junit.jar
ln -s %{_datadir}/javapackages-bootstrap/hamcrest-core.jar lib/optional/hamcrest-core.jar
%else
%if %{with ant_minimal}
build-jar-repository -s -p lib/optional junit hamcrest/core hamcrest/library
%else
build-jar-repository -s -p lib/optional antlr bcel commons-lang3 jakarta-mail/jakarta.mail-api jakarta-activation/jakarta.activation-api jdepend junit oro regexp bsf commons-logging commons-net jsch xalan-j2 xml-commons-resolver xalan-j2-serializer hamcrest/core hamcrest/library xz-java junit5 opentest4j
%endif
%endif

# fix hardcoded paths in ant script and conf
cp -p %{SOURCE2} %{name}.conf
sed -e 's:/etc/ant.conf:%{_sysconfdir}/ant.conf:g' \
    -e 's:/etc/ant.d:%{_sysconfdir}/ant.d:g' \
    -e 's:/usr/share/ant:%{_datadir}/ant:g' \
    -e 's:/usr/bin/build-classpath:%{_bindir}/build-classpath:g' \
    -e 's:/usr/share/java-utils/java-functions:%{_javadir}-utils/java-functions:g' \
    -i src/script/ant %{name}.conf

# Remove unnecessary JARs from the classpath
sed -i 's/jaxp_parser_impl//;s/xml-commons-apis//' src/script/ant

# Fix file-not-utf8 rpmlint warning
iconv KEYS -f iso-8859-1 -t utf-8 >KEYS.utf8
mv KEYS.utf8 KEYS
iconv LICENSE -f iso-8859-1 -t utf-8 >LICENSE.utf8
mv LICENSE.utf8 LICENSE

# We want a hard dep on antlr
%pom_xpath_remove pom:optional src/etc/poms/ant-antlr/pom.xml

# fix javamail dependency coordinates (remove once javamail is updated)
%pom_change_dep com.sun.mail:jakarta.mail jakarta.mail:jakarta.mail-api src/etc/poms/ant-jakartamail/pom.xml

%pom_change_dep commons-logging:commons-logging-api org.apache.commons:commons-logging::api: src/etc/poms/ant-commons-logging/pom.xml

%build
%if %{with ant_minimal}
%{ant} jars
%else
%{ant} jars test-jar
%endif

# typeset the manpage
asciidoctor -b manpage -D man %{SOURCE3}

# remove empty jai and netrexx jars. Due to missing dependencies they contain only manifests.
rm build/lib/ant-jai.jar build/lib/ant-netrexx.jar
# log4j logging is deprecated
rm build/lib/ant-apache-log4j.jar
# dropped in favor of jakartamail
rm build/lib/ant-javamail.jar

%install
# ANT_HOME and subdirs
mkdir -p %{buildroot}%{ant_home}/{lib,etc,bin}

%mvn_alias :ant org.apache.ant:ant-nodeps apache:ant ant:ant
%mvn_alias :ant-launcher ant:ant-launcher

%mvn_file ':{ant,ant-bootstrap,ant-launcher}' %{name}/@1 @1

%if %{with ant_minimal}
mv build/lib build/lib0
mkdir build/lib/
mv build/lib0/ant.jar build/lib/
mv build/lib0/ant-bootstrap.jar build/lib/
mv build/lib0/ant-launcher.jar build/lib/
mv build/lib0/ant-junit.jar build/lib/
mv build/lib0/ant-junit4.jar build/lib/
%endif

for jar in build/lib/*.jar; do
  # Make sure that installed JARs are not empty
  %jar tf ${jar} | grep -E -q '.*\.class'

  jarname=$(basename $jar .jar)

  # jar aliases
  ln -sf ../../java/%{name}/${jarname}.jar %{buildroot}%{ant_home}/lib/${jarname}.jar

  pom=src/etc/poms/${jarname}/pom.xml

  # bootstrap does not have a pom, generate one
  [ $jarname == ant-bootstrap ] && pom='org.apache.ant:ant-bootstrap:%{version}'

  %mvn_artifact ${pom} ${jar}
done

# ant-parent pom
%mvn_artifact src/etc/poms/pom.xml

%mvn_package :ant lib
%mvn_package :ant-launcher lib
%mvn_package :ant-bootstrap lib
%mvn_package :ant-parent lib
%mvn_package :ant-junit4 junit
# catchall rule for the rest
%mvn_package ':ant-{*}' @1

%mvn_install

# scripts: remove dos and os/2 scripts
rm -f src/script/*.bat
rm -f src/script/*.cmd

# XSLs
%if %{with ant_minimal}
rm src/etc/jdepend-frames.xsl
rm src/etc/jdepend.xsl
rm src/etc/maudit-frames.xsl
%endif
cp -p src/etc/*.xsl %{buildroot}%{ant_home}/etc

# install everything else
mkdir -p %{buildroot}%{_bindir}
cp -p src/script/ant %{buildroot}%{_bindir}/
ln -sf %{_bindir}/ant %{buildroot}%{ant_home}/bin/
cp -p src/script/antRun %{buildroot}%{ant_home}/bin/

# default ant.conf
mkdir -p %{buildroot}%{_sysconfdir}
cp -p %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf

# OPT_JAR_LIST fragments
mkdir -p %{buildroot}%{_sysconfdir}/%{name}.d
echo "junit hamcrest/core ant/ant-junit" > %{buildroot}%{_sysconfdir}/%{name}.d/junit
echo "junit hamcrest/core ant/ant-junit4" > %{buildroot}%{_sysconfdir}/%{name}.d/junit4

# JDK bindings
install -d -m 755 %{buildroot}%{_javaconfdir}/
ln -sf %{_jpbindingdir}/ant.conf %{buildroot}%{_javaconfdir}/ant.conf


echo 'JAVA_HOME=%{_jvmdir}/jre-25-openjdk' > %{buildroot}%{_javaconfdir}/ant-openjdk25.conf
%jp_binding --verbose --variant openjdk25 --ghost ant.conf --target %{_javaconfdir}/ant-openjdk25.conf --provides %{name}-jdk-binding --requires java-25-openjdk-headless --recommends java-25-openjdk-devel
touch %{buildroot}%{_javaconfdir}/ant-unbound.conf
%jp_binding --verbose --variant unbound --ghost ant.conf --target %{_javaconfdir}/ant-unbound.conf --provides %{name}-jdk-binding

%if %{without ant_minimal}

echo "ant/ant-jmf" > %{buildroot}%{_sysconfdir}/%{name}.d/jmf
echo "ant/ant-swing" > %{buildroot}%{_sysconfdir}/%{name}.d/swing
echo "antlr ant/ant-antlr" > %{buildroot}%{_sysconfdir}/%{name}.d/antlr
echo "bsf commons-logging ant/ant-apache-bsf" > %{buildroot}%{_sysconfdir}/%{name}.d/apache-bsf
echo "xml-commons-resolver ant/ant-apache-resolver" > %{buildroot}%{_sysconfdir}/%{name}.d/apache-resolver
echo "apache-commons-logging ant/ant-commons-logging" > %{buildroot}%{_sysconfdir}/%{name}.d/commons-logging
echo "apache-commons-net ant/ant-commons-net" > %{buildroot}%{_sysconfdir}/%{name}.d/commons-net
echo "bcel commons-lang3 ant/ant-apache-bcel" > %{buildroot}%{_sysconfdir}/%{name}.d/apache-bcel
echo "oro ant/ant-apache-oro" > %{buildroot}%{_sysconfdir}/%{name}.d/apache-oro
echo "regexp ant/ant-apache-regexp" > %{buildroot}%{_sysconfdir}/%{name}.d/apache-regexp
echo "xalan-j2 xalan-j2-serializer ant/ant-apache-xalan2" > %{buildroot}%{_sysconfdir}/%{name}.d/apache-xalan2
echo "ant/ant-imageio" > %{buildroot}%{_sysconfdir}/%{name}.d/imageio
echo "jakartamail jaf ant/ant-jakartamail" > %{buildroot}%{_sysconfdir}/%{name}.d/jakartamail
echo "jdepend ant/ant-jdepend" > %{buildroot}%{_sysconfdir}/%{name}.d/jdepend
echo "jsch ant/ant-jsch" > %{buildroot}%{_sysconfdir}/%{name}.d/jsch
echo "junit5 hamcrest/core junit opentest4j ant/ant-junitlauncher" > %{buildroot}%{_sysconfdir}/%{name}.d/junitlauncher
echo "testutil ant/ant-testutil" > %{buildroot}%{_sysconfdir}/%{name}.d/testutil
echo "xz-java ant/ant-xz" > %{buildroot}%{_sysconfdir}/%{name}.d/xz

%endif

# manpage
install -d -m 755 %{buildroot}%{_mandir}/man1/
install -p -m 644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%if %{without ant_minimal}
%check
%{ant} -Doffline=true test
%endif

%files
%doc KEYS README WHATSNEW
%license LICENSE NOTICE
%config %{_javaconfdir}/%{name}*.conf
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %{_bindir}/ant
%dir %{ant_home}/bin
%{ant_home}/bin/ant
%attr(0755,root,root) %{ant_home}/bin/antRun
%{_mandir}/man1/%{name}.*
%dir %{ant_home}/etc
%{ant_home}/etc/ant-update.xsl
%{ant_home}/etc/changelog.xsl
%{ant_home}/etc/coverage-frames.xsl
%{ant_home}/etc/mmetrics-frames.xsl
%{ant_home}/etc/log.xsl
%{ant_home}/etc/tagdiff.xsl
%{ant_home}/etc/common2master.xsl
%{ant_home}/etc/printFailingTests.xsl
%dir %{_sysconfdir}/%{name}.d

%files lib -f .mfiles-lib
%dir %{ant_home}
%dir %{ant_home}/lib
%{ant_home}/lib/%{name}.jar
%{ant_home}/lib/%{name}-launcher.jar
%{ant_home}/lib/%{name}-bootstrap.jar

%files junit -f .mfiles-junit
%{ant_home}/lib/%{name}-junit.jar
%{ant_home}/lib/%{name}-junit4.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/junit
%config(noreplace) %{_sysconfdir}/%{name}.d/junit4
%{ant_home}/etc/junit-frames.xsl
%{ant_home}/etc/junit-noframes.xsl
%{ant_home}/etc/junit-frames-xalan1.xsl
%{ant_home}/etc/junit-frames-saxon.xsl
%{ant_home}/etc/junit-noframes-saxon.xsl

%if %{without ant_minimal}

%files jmf -f .mfiles-jmf
%{ant_home}/lib/%{name}-jmf.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/jmf

%files swing -f .mfiles-swing
%{ant_home}/lib/%{name}-swing.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/swing

%files antlr -f .mfiles-antlr
%{ant_home}/lib/%{name}-antlr.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/antlr

%files apache-bsf -f .mfiles-apache-bsf
%{ant_home}/lib/%{name}-apache-bsf.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/apache-bsf

%files apache-resolver -f .mfiles-apache-resolver
%{ant_home}/lib/%{name}-apache-resolver.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/apache-resolver

%files commons-logging -f .mfiles-commons-logging
%{ant_home}/lib/%{name}-commons-logging.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/commons-logging

%files commons-net -f .mfiles-commons-net
%{ant_home}/lib/%{name}-commons-net.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/commons-net

%files apache-bcel -f .mfiles-apache-bcel
%{ant_home}/lib/%{name}-apache-bcel.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/apache-bcel

%files apache-oro -f .mfiles-apache-oro
%{ant_home}/lib/%{name}-apache-oro.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/apache-oro
%{ant_home}/etc/maudit-frames.xsl

%files apache-regexp -f .mfiles-apache-regexp
%{ant_home}/lib/%{name}-apache-regexp.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/apache-regexp

%files apache-xalan2 -f .mfiles-apache-xalan2
%{ant_home}/lib/%{name}-apache-xalan2.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/apache-xalan2

%files imageio -f .mfiles-imageio
%{ant_home}/lib/%{name}-imageio.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/imageio

%files jakartamail -f .mfiles-jakartamail
%{ant_home}/lib/%{name}-jakartamail.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/jakartamail

%files jdepend -f .mfiles-jdepend
%{ant_home}/lib/%{name}-jdepend.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/jdepend
%{ant_home}/etc/jdepend.xsl
%{ant_home}/etc/jdepend-frames.xsl

%files jsch -f .mfiles-jsch
%{ant_home}/lib/%{name}-jsch.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/jsch

%files junit5 -f .mfiles-junitlauncher
%{ant_home}/lib/%{name}-junitlauncher.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/junitlauncher

%files testutil -f .mfiles-testutil
%{ant_home}/lib/%{name}-testutil.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/testutil

%files xz -f .mfiles-xz
%{ant_home}/lib/%{name}-xz.jar
%config(noreplace) %{_sysconfdir}/%{name}.d/xz

%files manual
%license LICENSE NOTICE
%doc manual/*

%endif

# -----------------------------------------------------------------------------

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.10.15-33
- test: add initial lock files

* Thu Sep 04 2025 Jiri Vanek <jvanek@redhat.com> - 1.10.15-32
- manual bodhi update for jdk25 needed on selected pkgs

* Wed Sep 03 2025 Marian Koncek <mkoncek@redhat.com> - 1.10.15-31
- Switch matrix jlink tests to using Java 25

* Wed Sep 03 2025 Marian Koncek <mkoncek@redhat.com> - 1.10.15-30
- Fix matrix tests

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 1.10.15-29
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.15-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-27
- Suggest OpenJDK binding
- Build with OpenJDK 25
- Update bootstrap JAR paths

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-26
- Switch javapackages test plan to f43 ref

* Fri Apr 04 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-25
- Add OpenJDK 25 to test matrix

* Fri Apr 04 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-24
- Add OpenJDK 25 binding

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-23
- Switch to javapackages tests from CentOS Stream GitLab

* Mon Mar 24 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-22
- Use tests from CentOS Stream GitLab

* Wed Mar 05 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-21
- Remove javadoc subpackage

* Tue Feb 18 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-20
- Use %%jar macro

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.15-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-18
- Drop Obsoletes on ant-javamail

* Wed Dec 04 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-17
- Exclude several subpackages from unbound test plan

* Tue Dec 03 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-16
- Fix ant-manual license field

* Mon Dec 02 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-15
- Use smaller jlink image

* Mon Dec 02 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-14
- Require /plans/matrix/unbound/jlink for gating

* Mon Dec 02 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-13
- Add test plan for ant-unbound

* Mon Dec 02 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-12
- Exclude ant-unbound from openjdk21 tests

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-11
- Drop explicit requires on javapackages-tools

* Fri Nov 22 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-10
- Generate bindings with %%jp_binding macro

* Wed Oct 30 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-9
- Work around iconv clobbering file permissions

* Wed Oct 30 2024 Marian Koncek <mkoncek@redhat.com> - 1.10.15-8
- Replace  with %%{buildroot}

* Wed Oct 30 2024 Marian Koncek <mkoncek@redhat.com> - 1.10.15-7
- Add ant-openjdk21 subpackage

* Wed Oct 30 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-6
- Respect JAVA_HOME set by user

* Wed Oct 30 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-5
- Switch to matrix tests

* Thu Sep 19 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-4
- Require OpenJDK 21 for runtime

* Wed Sep 18 2024 Marian Koncek <mkoncek@redhat.com> - 1.10.15-3
- Use asciidoctor instead of asciidoc for manpage generation

* Tue Sep 03 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-2
- Use %%autosetup -C

* Tue Sep 03 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.15-1
- Update to upstream version 1.10.15
- Resolves: rhbz#2309001

* Mon Aug 26 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-22
- Drop explicit LC_ALL setting

* Tue Jul 30 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-13
- Adjust bootstrap build for javapackages-bootstrap update

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-11
- Run tests in explicit offline mode

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.10.14-10
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 1.10.14-9
- bump of release for for java-21-openjdk as system jdk

* Thu Feb 22 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-8
- Drop explicit build-requires on java-devel

* Tue Feb 13 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-7
- Drop patch removing tools.jar from test classpath

* Fri Feb 09 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-6
- Fix source tarball URL

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 05 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-3
- Update Maven coordinates for commons-logging API

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.14-2
- Rebuild

* Tue Aug 22 2023 Marian Koncek <mkoncek@redhat.com> - 1.10.14-1
- Update to upstream version 1.10.14

* Mon Aug 21 2023 Marian Koncek <mkoncek@redhat.com> - 1.10.13-1
- Update to upstream version 1.10.13

* Fri Aug 18 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.12-11
- Add transitive dependency on commons-lang3 through bcel

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.12-7
- Skip running ImageIOTest test

* Mon Jun 06 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.12-6
- Rebuild to fix incorrect version string
- Resolves: rhbz#1936159

* Fri Jun 03 2022 Marian Koncek <mkoncek@redhat.com> - 1.10.12-5
- Fix integer overflow when parsing SOURCE_DATE_EPOCH

* Fri Apr 22 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.12-4
- Fix FTBFS with JUnit 5.8.x

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.10.12-3
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 09 2021 Marian Koncek <mkoncek@redhat.com> - 1.10.12-1
- Update to upstream version 1.10.12

* Wed Oct 13 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.11-2
- Bump release

* Thu Sep  9 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.10.11-1
- Add Obsoletes for removed apache-log4j subpackage to fix upgrades

* Wed Aug 11 2021 Marian Koncek <mkoncek@redhat.com> - 1.10.11-1
- Update to upstream version 1.10.11

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.9-5
- Disable deprecated log4j logging functionality

* Mon Jun 21 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.9-4
- Remove support for JavaScript

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.9-3
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 16 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.10.9-1
- Update to version 1.10.9.
- Addresses: CVE-2020-11979

* Wed Sep 16 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.10.8-6
- Remove workaround for jarsigner issues / RHBZ#1869017.

* Wed Sep 09 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.10.8-5
- Switch from log4j 1.2 compat package to log4j 1.2 API shim.

* Sun Aug 23 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.10.8-4
- Temporarily disable some jarsigner tests to work around RHBZ#1869017.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:1.10.8-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11
- disabled javadoc, as it fails in jdk11, and ant should not be an FTBFS to soon

* Sat May 16 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.10.8-1
- Update to version 1.10.8.
- Addresses: CVE-2020-1945

* Fri May 08 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.10.7-1
- Update to version 1.10.7.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jul 29 2019 Fabio Valentini <decathorpe@gmail.com> - 0:1.10.6-1
- Update to version 1.10.6.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Apr 27 2019 François Cami <fcami@redhat.com> - - 0:1.10.5-5
- Bump to fix FTBFS

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0:1.10.5-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Mon Aug 20 2018 Mat Booth <mat.booth@redhat.com> - 0:1.10.5-2
- Enable building the optional junit5 module

* Thu Aug 02 2018 Michael Simacek <msimacek@redhat.com> - 0:1.10.5-1
- Update to upstream version 1.10.5

* Thu Aug 02 2018 Michael Simacek <msimacek@redhat.com> - 0:1.10.4-4
- Add a manpage
- Avoid installing antRun auxiliary script in bindir, keep it in ant_home

* Mon Jul 30 2018 Severin Gehwolf <sgehwolf@redhat.com> - 0:1.10.4-3
- Require javapackages-tools for ant script.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Michael Simacek <msimacek@redhat.com> - 0:1.10.4-1
- Update to upstream version 1.10.4
- Resolves: rhbz#1584407

* Wed Apr 18 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.10.3-2
- Remove legacy Obsoletes/Provides

* Wed Mar 28 2018 Michael Simacek <msimacek@redhat.com> - 0:1.10.3-1
- Update to upstream version 1.10.3

* Wed Feb  7 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.10.2-1
- Update to upstream version 1.10.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 04 2017 Michael Simacek <msimacek@redhat.com> - 0:1.10.1-8
- Fix directory ownership

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Michael Simacek <msimacek@redhat.com> - 0:1.10.1-6
- Fix requires
- Use JDK's jaxp instead of xerces

* Tue Mar 21 2017 Michael Simacek <msimacek@redhat.com> - 0:1.10.1-5
- Install with XMvn

* Wed Mar  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.10.1-4
- Fix hardcoded paths in ant script and conf
- Fix requires on xz-java

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.10.1-3
- Don't hardcode path to xargs

* Thu Feb 16 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.10.1-2
- Conditionalize weak dependencies

* Wed Feb 15 2017 Michael Simacek <msimacek@redhat.com> - 0:1.10.1-1
- Update to upstream version 1.10.1

* Fri Feb 10 2017 Michael Simacek <msimacek@redhat.com> - 0:1.10.0-3
- Use log4j12

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Michael Simacek <msimacek@redhat.com> - 0:1.10.0-1
- Update to upstream version 1.10.0

* Mon Dec 12 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.7-1
- Update to upstream version 1.9.7

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.6-2
- Recommend java-devel instead of requiring it

* Thu Jul 02 2015 Michael Simacek <msimacek@redhat.com> - 0:1.9.6-1
- Update to upstream version 1.9.6

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Michael Simacek <msimacek@redhat.com> - 0:1.9.5-1
- Update to upstream version 1.9.5

* Fri Apr 03 2015 Michael Simacek <msimacek@redhat.com> - 0:1.9.4-11
- Move launcher to lib subpackage

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.4-10
- Update description

* Tue Mar 31 2015 Michael Simacek <msimacek@redhat.com> - 0:1.9.4-9
- Split library part into subpackage (rhbz#1119283)

* Wed Mar 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.4-8
- Add alias for ant:ant-launcher

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.4-7
- Add hamcrest to ant-junit classpath

* Mon Jan 26 2015 Michael Simacek <msimacek@redhat.com> - 0:1.9.4-6
- Add hamcrest into classpath

* Tue Jan 13 2015 Mat Booth <mat.booth@redhat.com> - 0:1.9.4-5
- Resolves: rhbz#1180568 - Add rhino to classpath for bsf plug-in

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.4-4
- Add aliases for ant:ant and apache:ant

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 6 2014 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.4-2
- Reenable tests.

* Tue May 6 2014 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.4-1
- Update to upstream 1.9.4.
- Disable tests as they use new junit tas attribute added in this release.

* Fri Feb 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.3-2
- Skip installation perl and python scripts

* Thu Jan  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.3-1
- Update to upstream version 1.9.3

* Thu Sep 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-7
- Install Maven depmaps in appropriate subpackages
- Resolves: rhbz#996062

* Fri Aug 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-6
- Fix antRun script
- Resolves: rhbz#675949

* Thu Aug 08 2013 Michal Srb <msrb@redhat.com> - 0:1.9.2-5
- xerces-j2 and xml-commons-apis should be in classpath (Resolves: rhbz#994556)

* Thu Aug 08 2013 Michal Srb <msrb@redhat.com> - 0:1.9.2-4
- Temporarily add xerces-j2 and xml-commons-apis to classpath, see #994556

* Fri Jul 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-3
- Rebuilt to regenerate depmap files
- Resolves: rhbz#988797

* Thu Jul 25 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.2-2
- Update license after removal of W3C content upstream

* Wed Jul 17 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-1
- Update to upstream version 1.9.2
- Remove usage of %%add_to_maven_depmap

* Tue Jul  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.1-3
- Remove arch-specific patch as ant is noarch now
- Remove bcond macro definitions (provided by rpm itself)
- Remove Group tags
- Update to current packaging guidelines
- Run tests in %%check instead of %%build
- Remove dependencies on xerces-j2 and xml-commons-apis, resolves: rhbz#838711
- Convert %%global build_javadoc to conditional
- Remove bootstrap code, resolves: rhbz#915437
- Fail the build if any of JARs is empty
- Skip running tests that fail on Koji, resolves: rhbz#979496
- Merge scripts into main package, resolves: rhbz#798975

* Mon Jun 03 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-2
- Enable unit tests

* Wed May 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.1-1
- Update to upstream version 1.9.1

* Mon Apr 22 2013 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.0-2
- Drop a pile of old provider/requires/obsoletes that are no longer usable
  and cause only problem if ant is scl-ized.

* Mon Mar 11 2013 Michal Srb <msrb@redhat.com> - 0:1.9.0-1
- Update to upstream version 1.9.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 0:1.8.4-5
- Requires on jpackage-utils in javadoc
- Added LICENSE and NOTICE in manual subpackage

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> 0:1.8.4-4
- Including LICENSE and NOTICE in the javadoc subpackage

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> 0:1.8.4-3
- Fixing the license tag

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.4-1
- Update to new upstream version.

* Wed May 2 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.3-2
- Use apache-commons-* instead of jakarta-commons-*.
- Drop xml-commons-apis-13 BR/R since it's no longer needed.

* Wed Feb 29 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.3-1
- Update to upstream 1.8.3 release.
- Drop old stuff.

* Tue Feb 07 2012 Tomas Radej <tradej@redhat.com> - 0:1.8.2-9
- Added patch

* Tue Feb 07 2012 Tomas Radej <tradej@redhat.com> - 0:1.8.2-8
- Removed checking for classpath duplicates
- Added ant-junit4.jar into %%files and ant.d

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 6 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.2-6
- Make scripts executable.
- Adapt to current guidelines.

* Thu Mar 10 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.2-5
- Fix xalan-j2 subpackage path.

* Tue Feb 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8.2-4
- Change oro to jakarta-oro in BR/R

* Wed Feb  9 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8.2-3
- Add backward compatible maven depmap for nodeps jar
- Revert define->global change (different semantic in rpm 4.9.X)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.2-1
- Update to new upstream version.
- Guidelines fixes.

* Sun Nov 28 2010 Ville Skyttä <ville.skytta@iki.fi> - 0:1.8.1-9
- Install javadocs into unversioned dir (#657879).

* Tue Nov 23 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8.1-8
- Fix pom filename (Resolves rhbz#655787)

* Thu Oct 28 2010 Orion Poplawski <orion@cora.nwra.com> 0:1.8.1-7
- Build and package ant-testutil

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.1-6
- Remove jaf from the classpath.

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.1-5
- Drop gcj support.
- Drop jaf BR/R it is part of Java 5+.

* Fri Oct 1 2010 Orion Poplawski <orion@cora.nwra.com> 0:1.8.1-4
- Move ant-trax Provides/Obsoletes to ant-nodeps

* Thu Aug 26 2010 Orion Poplawski <orion@cora.nwra.com> 0:1.8.1-3
- Remove -SNAPSHOT from version

* Wed Aug 25 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.1-2
- Use global instead of define.
- Fix parent pom install.

* Mon Aug 16 2010 Orion Poplawski <orion@cora.nwra.com> 0:1.8.1-1
- Update to ant 1.8.1
- Update no-test-jar patch
- Update class-path-in-manifest patch
- Drop gnu-classpath patch
- Retire trax subpackage no longer shipped
- Add xalan2 subpackage and support for junitreport task
- Drop old jakarta jar aliases

* Thu Aug 13 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.7.1-12
- Fix compile with commons-net 2.0.

* Fri Aug  7 2009 Orion Poplawski <orion@cora.nwra.com> - 0:1.1.7-11
- Add links to jar files into %%{ant_home} (Bug #179759)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.1-10.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.1-9.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0:1.7.1-8.2
- Rebuild for Python 2.6

* Wed Oct  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0:1.7.1-7.2
- Exclude bogus perl(the) Requires
- Exclude bogus perl(oata), perl(examples) Provides

* Fri Sep 26 2008 Permaine Cheung <pcheung@redhat.com> 0:1.7.1-7.1
- Define with_gcj_support

* Tue Sep 23 2008 Permaine Cheung <pcheung@redhat.com> 0:1.7.1-7
- Update to 1.7.1
- Fix some rpmlint issues

* Tue Jul 15 2008 David Walluck <dwalluck@redhat.com> 0:1.7.1-7
- enable non-bootstrap

* Tue Jul 15 2008 David Walluck <dwalluck@redhat.com> 0:1.7.1-6
- add ant-bootstrap jar if bootstrap is enabled
- enable jmf, swing, trax if bootstrap is enabled
- BuildRequires: jaxp_transform_impl
- BuildRequires: junit for non-bootstrap

* Tue Jul 15 2008 David Walluck <dwalluck@redhat.com> 0:1.7.1-5
- enable ant-nodeps in bootstrap mode

* Tue Jul 15 2008 David Walluck <dwalluck@redhat.com> 0:1.7.1-4
- remove junit for bootstrap

* Tue Jul 15 2008 David Walluck <dwalluck@redhat.com> 0:1.7.1-3
- build as bootstrap

* Tue Jul 15 2008 David Walluck <dwalluck@redhat.com> 0:1.7.1-2
- set rpm_mode=false by default

* Thu Jul 10 2008 David Walluck <dwalluck@redhat.com> 0:1.7.1-1
- 1.7.1
- update maven pom files
- rediff apache-ant-jars.patch
- rediff apache-ant-bz163689.patch
- add apache-ant-gnu-classpath.patch
- set rpm_mode=true in conf since the ant script handles the rest

* Thu Jul 10 2008 David Walluck <dwalluck@redhat.com> 0:1.7.0-3
- add bootstrap mode
- replace some alternatives/virtual requires by explicit requires
- remove javadoc scriptlets
- fix GCJ support
- add workaround for xalan-j2 in %%{_sysconfdir}/%%{name}.d/trax
- version Obsoletes and add Provides
- remove Conflicts
- mark files in %%{_sysconfdir} as %%config(noreplace)

* Tue Jul 03 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.7.0-2.jpp5
- Add poms and depmap frags
- (B)R jpackage-utils >= 0:1.7.5
- BR java-devel = 0:1.5.0
- R java >= 0:1.5.0

* Wed Jun 20 2007 Fernando Nasser <fnasser at redhat.com> - 0:1.7.0-1jpp
- Upgrade to the final 1.7.0

* Thu Sep 21 2006 Will Tatam <will.tatam@red61.com> - 0:1.7.0-0.Beta1.1jpp
- Upgraded to 1.7.0Beta1
- removed the apache-ant-1.6.5-jvm1.5-detect.patch as merged upstream

* Fri Aug 11 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.6.5-2jpp
- Added conditional native compilation
- Added patch to fix jvm version detection
- Add missing requirements
- Synch with Fedora spec

* Wed Nov 09 2005 Fernando Nasser <fnasser at redhat.com> - 0:1.6.5-1jpp
- Upgrade to 1.6.5
- Incorporate the following changes:
  From Gary Benson <gbenson at redhat.com>:
- Allow subpackages not in Fedora to be installed from JPackage
- Add NOTICE file as per Apache License version 2.0
- Own /usr/share/java/ant
  From Vadim Nasardinov <vadimn@redhat.com>
- Removed apache-ant-1.6.2.patch.  Incorporated upstream.
  From David Walluck <david@jpackage.org>
- Add manifest-only package (mainly for eclipse)
- Add conflicts on j2sdk for Mandriva

* Mon Nov  8 2004 Gary Benson <gbenson at redhat.com> - 0:1.6.2-3jpp
- Build OPT_JAR_LIST from files in /etc/ant.d.

* Mon Sep 06 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.6.2-2jpp
- Fix to backward compatibility symbolic links.

* Tue Aug 17 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.6.2-1jpp
- Update to Ant 1.6.2

* Thu Aug 05 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.6.1-2jpp
- Remove incorrect noreplace option for ant.conf; it can't be used anymore
  because the sub-packages update that file.
- Add patch to fix temp directory used for file containing large
  command strings (> 4k)

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.6.1-1jpp
- Extend subpackage builds to update ant.conf

* Tue Mar 23 2004 Randy Watler <rwatler at finali.com> - 0:1.6.1-1jpp
- Update to Ant 1.6.1
- Change ant launch script to source instead of patch
- Move optional components to ant subdirectory: %%{_javadir}/%%{name}
- Remove os/2 scripts and set JAVA_HOME for build

* Wed Feb 11 2004 Randy Watler <rwatler at finali.com> - 0:1.6.0-1jpp
- Update to Ant 1.6.0
- Break out optional/optional-full components
- Revise ant launch scripts and support ~/.ant/ant.conf configuration file
- Use --noconfig flag to bootstrap ant build and override existing jpp config
- Modify ant launcher to use ant.library.dir property to find extra jars
- Port changes made in ant launch script for 1.6.2 back into patches

* Wed Aug 13 2003 Paul Nasrat <pauln at truemesh.com> - 0:1.5.4-2jpp
- remove bogus NoSource entries

* Tue Aug 12 2003 Paul Nasrat <pauln at truemesh.com> - 0:1.5.4-1jpp
- Update to 1.5.4
- JavaCC task fixed using merged upstream patches from ant HEAD

* Mon May  5 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.3-2jpp
- Fix non-versioned javadoc symlinking.

* Tue Apr 22 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.3-1jpp
- Update to 1.5.3.
- Remove runtime java-devel dependency.
- Add Epochs in all Provides and Requires.
- Include non-versioned javadoc symlink.
- Build without dependencies that are partially or completely missing from
  JPackage 1.5 (oldbsf, xalan-j1, stylebook1.0b3).
- Add netcomponents to optional jar list in ant.conf.

* Tue Apr 01 2003 Nicolas Mailhot <Nicolas.Mailhot at JPackage.org> - 1.5.2-13jpp
- ant-optional is optional (silly me)
- jaxp_transform is optional , do not require it
- epoch, correct jpackage-utils requires...

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot at JPackage.org> - 1.5.2-11jpp
- add an optional jar list as per Ville's suggestion

* Thu Mar 20 2003 Nicolas Mailhot <Nicolas.Mailhot at JPackage.org> - 1.5.2-10jpp
- hopefully fix CLASSSPATH_OVERRIDE behaviour

* Tue Mar 18 2003 Nicolas Mailhot <Nicolas.Mailhot at JPackage.org> - 1.5.2-7jpp
- for JPackage-utils 1.5

* Wed Mar 12 2003 Ville Skyttä <ville.skytta@iki.fi> - 1.5.2-5jpp
- Move ANT_HOME to /usr/share/ant.
- Don't special-case the lib dir for RPM layout any more, use ANT_HOME/lib.
- Install XSLs into ANT_HOME/etc.
- Call set_jvm by default in ant.conf.
- Provide ant-optional-clean (versioned) in ant-optional.
- Make ant-optional-full conflict with ant-optional-clean.
- Add version info to ant-optional provision in ant-optional-full.
- Built with Sun 1.4.1_02 javac (to get JDK 1.4 regex).

* Tue Mar 11 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.5.2-4jp
- changed provided /etc/ant.conf so that if usejikes is allready provided
  it didn't set it. Which such modification if you want to disable
  ant to use jikes even if jikes is set in /etc/ant.conf you'll just have
  to do usejikes=false ant build.xml.

* Mon Mar 10 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.5.2-3jp
- rebuilt with IBM SDK 1.3.1 since there was zip corruption when built
  with jikes 1.18 and IBM SDK 1.4.

* Wed Mar 05 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.5.2-2jp
- updated URL and source location

* Wed Mar 05 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.5.2-1jp
- 1.5.2
- remove JDK 1.4 related patchs which are now included in ant 1.5.2
- fix ant-optional-full pre/post install script (now remove correctly all
  ant optional jars)
- Built with jikes 1.18 and IBM SDK 1.4

* Sat Feb  1 2003 Ville Skyttä <ville.skytta@iki.fi> - 1.5.1-8jpp
- Symlink a transformer into ANT_LIB for smoother experience on Java 1.3.
- Requires jaxp_transform_impl.
- Don't remove optional.jar symlinks on optional-full upgrade.
- Include Sun's 1.4 JSSE and JCE jars in runtime path, see
  <http://nagoya.apache.org/bugzilla/show_bug.cgi?id=16242>.
- Use jpackage-utils for setting JAVA_HOME when building.
- Built with Sun 1.4.1_01 javac.

* Mon Jan 20 2003 David Walluck <david@anti-microsoft.org> 1.5.1-7jpp
- oldbsf

* Fri Dec 20 2002 Ville Skyttä <ville.skytta@iki.fi> - 1.5.1-6jpp
- Really get rid of automatic dependencies for the -scripts package.

* Wed Dec 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5.1-5jpp
- scripts subpackages
- file-based manual dependencies, as packages doesn't have the same name on RedHat and Mandrake

* Wed Dec 11 2002 Ville Skyttä <ville.skytta@iki.fi> - 1.5.1-4jpp
- Patched to allow easier use with Jikes and IBM's 1.4.0, see
  <http://nagoya.apache.org/bugzilla/show_bug.cgi?id=15289> for details.

* Mon Oct 07 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5.1-3jpp
- new post script for optional-full since rpm didn't works as
  expected and didn't set correct symlink for ant-optional.jar

* Thu Oct 03 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5.1-2jpp
- really used JDK 1.4.1 to get JDK 1.4.x Regexp

* Thu Oct 03 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5.1-1jpp
- ant 1.5.1

* Fri Jul 12 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5-5jpp
- ant script standard behaviour restored, ie ant/lib jars are taken
  before CLASSPATH. You should define CLASSPATH_OVERRIDE env var to have
  CLASSPATH before ant/lib jars
- applied ant script patch for cygwin (cygwin rpm users around ?)
- remove conflict in ant-optional-full, just put provides

* Fri Jul 12 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5-4jpp
- fix a problem in xerces-j2 build by changing the way CLASSPATH is constructed:
  first add jars found in CLASSPATH, then add xml-commons-apis, jaxp_parser_impl,
  ant, ant-optional and finish with jars found in ant/lib.
- jpackage-utils is no more required (but recommanded :)
- ant-optional-full provides ant-optional
- fix link between manual and api (javadoc)

* Thu Jul 11 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5-3jpp
- add missing symlink between optional-full.jar and optional.jar

* Wed Jul 10 2002 Ville Skyttä <ville.skytta@iki.fi> 1.5-2jpp
- Requires jaxp_parser_impl, no longer jaxp_parser2
  (jaxp_parser_impl already requires xml-commons-apis).
- Use sed instead of bash 2 extension when symlinking.

* Wed Jul 10 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5-1jpp
* ant 1.5

* Tue Jul 09 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.5.Beta3-1jpp
- ant 1.5 beta 3
- added bcel as required

* Tue Jul 09 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.4.1-14jpp
- added regexp to list of dependant packages

* Tue Jul 09 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.4.1-13jpp
- added optional-full which include all ant tasks, even those without
  matching package
- added jdepend 2.2
- remove require oro, since ant could works without it
- ant lib is now in %%{_javadir}/%%{name}, put external jars here

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-12jpp
- hardcoded distribution and vendor tag
- group tag again

* Thu May 2 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-11jpp
- no more jikes specific support in launch script
- source user prefs before configuration in launch script
- distribution tag
- group tag
- provided original script as documentation

* Fri Apr 05 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-10jpp
- used xalan-j1 instead of xalan-j2-compat

* Mon Mar 11 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-9jpp
- jaxp_parser2 support

* Wed Feb 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-8jpp
- netcomponents support

* Sun Jan 27 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-7jpp
- adaptation to new stylebook1.0b3 package
- stylebook is a dependency of optional package
- removed redundant dependencies
- launch script correction

* Fri Jan 25 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-6jpp
- cleaned manifest from class-path references
- section macro

* Thu Jan 17 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-5jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for optional package
- additional sources in individual archives
- upgraded launch script
- no more javadoc cross-linking
- additional requirement for optional package: xml-commons-apis, xalan-j2, xalan-j2-compat, jaf, javamail, & log4j

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-4jpp
- removed conditional build
- removed redundant BuildRequires
- ant-optional.jar in ant-optional package
- javadoc into javadoc package
- new launch script using functions library

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.4.1-3jpp
- readded Requires: oro junit stylebook-1.0b3 bsf rhino antlr to the main package
- corrected changelog release 1jpp-> 2jpp

* Tue Nov 20 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.4.1-2jpp
- conditional build
- removed packager tag
- new jpp extension
- added xalan 2.2.D13 support
- added BuildRequires: xalan-j2 >= 2.2.D13
- removed Requires: oro junit stylebook-1.0b3 bsf rhino antlr

* Mon Oct 15 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4.1-1jpp
- 1.4.1

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4-4jpp
- used original tarball

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4-3jpp
- more macros

* Wed Sep 26 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4-2jpp
- first unified release
- dropped explicit xalan-j2 requirement, as stylebook-1.0b3 already requires it
- added missing xalan-j1 compatibility classes
- s/jPackage/JPackage

* Wed Sep 05 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.4-1mdk
- 1.4
- added xalan-j2 antlr bsf rhino to buildrequires and requires
- launch script cleanup

* Tue Jul 31 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.3-4mdk
- jaxp_parser symlink is now jaxp_parser.jar

* Thu Jul 26 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.3-3mdk
- used alternative jaxp_parser
- updated launch script

* Sat Jun 23 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.3-2mdk
- s/Copyright/License/
- truncated description to 72 columns in spec
- updated launch script

* Mon Jun 11 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.3-1mdk
- 1.3
- new versioning scheme
- compiled with oro, junit and stylebook support
- spec cleanup

* Sat Mar 10 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-9mdk
- vendor tag
- packager tag

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-8mdk
- spec cleanup
- corrected changelog
- changed description

* Sun Feb 04 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-7mdk
- launch script improvments (Christian Zoffoli <czoffoli@linux-mandrake.com>)
- added french in spec
- more macros

* Fri Feb 02 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-6mdk
- corrected launch script

* Thu Feb 01 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 1.2-5mdk
- more macros
- added italian in spec

* Wed Jan 31 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-4mdk
- merged with Henri Gomez <hgomez@users.sourceforge.net> specs:
- changed name to ant
- changed javadir to /usr/share/java
- dropped jdk and jre requirement
- corrected require to jaxp
- added Jikes support
- used our own bash script
- dropped perl script
- dropped ant home directory

* Sun Jan 14 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-3mdk
- changed name to jakarta-ant
- changed group to Development/Java

* Thu Jan 04 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-2mdk
- new spec file
- discarded ugly non-free Sun jaxp library from sources, and used pretty open-source xerces instead

* Wed Dec 20 2000 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-1mdk
- first Mandrake release
- used SRPMS from Henri Gomez <hgomez@users.sourceforge.net>

## END: Generated by rpmautospec
