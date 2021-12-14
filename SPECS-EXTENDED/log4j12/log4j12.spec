Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package log4j12
#
# Copyright (c) 2020 SUSE LLC
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


%global flavor bootstrap
%if "%{flavor}" == "bootstrap"
%bcond_without bootstrap
%else
%bcond_with bootstrap
%endif
%define real log4j12
Version:        1.2.17
Release:        4%{?dist}
Summary:        Java logging tool
License:        Apache-2.0
URL:            https://logging.apache.org/log4j/
Source0:        http://www.apache.org/dist/logging/log4j/%{version}/log4j-%{version}.tar.gz
# Converted from src/java/org/apache/log4j/lf5/viewer/images/lf5_small_icon.gif
Source1:        log4j-logfactor5.png
Source2:        log4j-logfactor5.sh
Source3:        log4j-logfactor5.desktop
# Converted from docs/images/logo.jpg
Source4:        log4j-chainsaw.png
Source5:        log4j-chainsaw.sh
Source6:        log4j-chainsaw.desktop
Source7:        log4j.catalog
Patch0:         log4j-logfactor5-userdir.patch
Patch1:         log4j-javadoc-xlink.patch
Patch2:         log4j-mx4j-tools.patch
# PATCH-FIX-OPENSUSE -- Drop javadoc timestamp
Patch3:         log4j-reproducible.patch
# PATCH-FIX-UPSTREAM bsc#1159646 CVE-2019-17571 deserialization of untrusted data in SocketServer
Patch4:         log4j-CVE-2019-17571.patch
# PATCH-FIX-OPENSUSE -- add bundle manifest
Patch5:         log4j12-bundle_manifest.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  openjdk8
BuildRequires:  perl
Requires:       javapackages-tools
Requires:       jaxp_parser_impl
Requires:       xml-apis
Requires(pre):  coreutils
Obsoletes:      log4j < 1.3
Obsoletes:      log4j-mini < 1.3
BuildArch:      noarch
%if %{with bootstrap}
Name:           %{real}-mini
Provides:       %{real} = %{version}-%{release}
%else
Name:           %{real}
BuildRequires:  geronimo-jaf-1_0_2-api
BuildRequires:  geronimo-jms-1_1-api
BuildRequires:  javamail
BuildRequires:  mx4j
#!BuildIgnore:  apache-commons-discovery
#!BuildIgnore:  apache-commons-logging
#!BuildIgnore:  axis
Provides:       %{real}-mini
Obsoletes:      %{real}-mini
#!BuildRequires: %{real}-mini
%endif

%description
Log4j is a tool to help the programmer output log statements to a
variety of output targets.

%if %{without bootstrap}
%package        manual
Summary:        Java logging tool (Manual)
# Manual's api directory is a symlink to javadoc
Requires:       %{name}-javadoc

%description    manual
Documentation manual for Java logging tool log4j.

%package        javadoc
Summary:        Java logging tool (Documentation)

%description    javadoc
Documentation javadoc for Java logging tool log4j.
%endif

%prep
%setup -q -n apache-log4j-%{version}
%patch0
%patch1
%patch2
%patch3 -p1
%patch4 -p1
%if %{without bootstrap}
%patch5 -p1
%endif

sed -i 's/\r//g' LICENSE NOTICE src/site/resources/css/*.css

# remove all the stuff we'll build ourselves
find . \( -name "*.jar" -o -name "*.class" \) -exec rm -f {} \;
rm -rf docs/api

# fix encoding of mailbox files
for i in contribs/JimMoore/mail*;do
    iconv --from=ISO-8859-1 --to=UTF-8 "$i" > new
    mv new "$i"
done

%build
%{ant} \
        -Djavamail.jar=$(build-classpath javamail/mailapi) \
        -Dactivation.jar=$(build-classpath jaf) \
        -Djaxp.jaxp.jar.jar=$(build-classpath jaxp_parser_impl) \
        -Djms.jar=$(build-classpath jms) \
        -Djmx.jar=$(build-classpath mx4j/mx4j) \
        -Djmx-extra.jar=$(build-classpath mx4j/mx4j-tools) \
        -Djndi.jar=$(build-classpath jndi) \
        -Djavac.source=1.6 -Djavac.target=1.6 \
        -Djdk.javadoc=%{_javadocdir}/java \
        jar \
%if %{without bootstrap}
        javadoc
%endif

%install
# jars
mkdir -p %{buildroot}%{_javadir}/%{real}
cp -a dist/lib/log4j-%{version}.jar %{buildroot}%{_javadir}/%{real}/log4j.jar

#pom
install -d -m 755 %{buildroot}%{_mavenpomdir}/%{real}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{real}/log4j.pom
%add_maven_depmap %{real}/log4j.pom %{real}/log4j.jar -v "1.2.17,1.2.16,1.2.15,1.2.14,1.2.13,1.2.12,12"

%if %{without bootstrap}
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -a docs/api/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}
rm -rf docs/api
ln -s %{_javadocdir}/%{name} docs/api
%endif
# scripts
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE2} %{buildroot}%{_bindir}/logfactor5
install -p -m 755 %{SOURCE5} %{buildroot}%{_bindir}/chainsaw
# freedesktop.org menu entries and icons
mkdir -p %{buildroot}%{_datadir}/{applications,pixmaps}
cp -a %{SOURCE1} \
  %{buildroot}%{_datadir}/pixmaps/logfactor5.png
cp -a %{SOURCE3} \
  %{buildroot}%{_datadir}/applications/jpackage-logfactor5.desktop
cp -a %{SOURCE4} \
  %{buildroot}%{_datadir}/pixmaps/chainsaw.png
cp -a %{SOURCE6} \
  %{buildroot}%{_datadir}/applications/jpackage-chainsaw.desktop
# DTD and the SGML catalog (XML catalog handled in scriptlets)
mkdir -p %{buildroot}%{_datadir}/sgml/%{name}
cp -a src/main/resources/org/apache/log4j/xml/log4j.dtd \
  %{buildroot}%{_datadir}/sgml/%{name}
cp -a %{SOURCE7} \
  %{buildroot}%{_datadir}/sgml/%{name}/catalog
# fix perl location
perl -p -i -e 's|/opt/perl5/bin/perl|perl|' \
contribs/KitchingSimon/udpserver.pl

%post
# Note that we're using versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/catalog > /dev/null || :
fi
if [ -x %{_bindir}/xmlcatalog -a -w %{_sysconfdir}/xml/catalog ]; then
  %{_bindir}/xmlcatalog --noout --add system log4j.dtd \
    file://%{_datadir}/sgml/%{name}/log4j.dtd %{_sysconfdir}/xml/catalog \
    > /dev/null || :
fi

%preun
if [ $1 -eq 0 ]; then
  if [ -x %{_bindir}/xmlcatalog -a -w %{_sysconfdir}/xml/catalog ]; then
    %{_bindir}/xmlcatalog --noout --del log4j.dtd \
      %{_sysconfdir}/xml/catalog > /dev/null || :
  fi
fi

%postun
# Note that we're using versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --remove \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/catalog > /dev/null || :
fi

%files -f .mfiles
%license LICENSE
%doc NOTICE
%{_bindir}/*
%{_javadir}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/sgml/%{name}

%if %{without bootstrap}
%files manual
%doc docs/* contribs

%files javadoc
%dir %{_javadocdir}/%{name}
%{_javadocdir}/%{name}/*
%endif

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.17-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.2.17-3.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Switch to bootstrap to avoid build cycle.
- Fix linebreak in sed command.
- Remove distro specific update-desktop-files.
- Change distro specific jndi to equivalent openjdk8.

* Fri Mar 20 2020 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * log4j12-bundle_manifest.patch
    + Add a bundle manifest to the log4j12 package so that it can
    be used by eclipse
* Tue Jan  7 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Security fix: [bsc#1159646, CVE-2019-17571]
  * Remote code execution: Deserialization of untrusted data in SocketServer
  * Backported from CVE-2017-5645 for Log4j 2.8.2
- Add log4j-CVE-2019-17571.patch
* Tue Jan  7 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Remove script jpackage-mini-prepare.sh
* Mon Jan  6 2020 Fridrich Strba <fstrba@suse.com>
- Let both the log4j12 and log4j12-mini packages obsolete the log4j
  and log4j-mini < 1.3 in order to simplify upgrades
* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Rename to log4j12/log4j12-mini as a compatibility packages
- Convert to multibuild
- Clean up with the spec-cleaner
- Install maven pom files even with the mini package
* Tue Jan 22 2019 Fridrich Strba <fstrba@suse.com>
- Build against a generic javamail provider instead of against
  classpathx-mail
* Tue Jan 15 2019 Fridrich Strba <fstrba@suse.com>
- Let log4j provide the log4j-mini and obsolete it too.
- Remove conflicts on each other
* Thu Dec 13 2018 Fridrich Strba <fstrba@suse.com>
- Depend on the generic xml-apis
* Thu Oct 18 2018 Fridrich Strba <fstrba@suse.com>
- Install and package the maven pom and metadata files for the
  non-bootstrap log4j
* Wed Jul 25 2018 fstrba@suse.com
- Require at least java 8 for build
* Wed Jan 10 2018 bwiedemann@suse.com
- Add log4j-reproducible.patch to drop javadoc timestamps to make
  package builds more reproducible (boo#1047218)
* Tue Sep 12 2017 fstrba@suse.com
- Specify java source and target level 1.6 to allow building with
  jdk9
* Mon Mar  2 2015 tchvatal@suse.com
- Version bump to 1.2.17 latest 1.2 series:
  * No short changelog provided - many small changes
- Try to avoid cycle between log4j and apache-common-loggings
- Remove obsoleted patch:
  * log4j-jmx-Agent.patch
- Refresh patch to apply to new source:
  * log4j-mx4j-tools.patch
* Mon Mar  2 2015 tchvatal@suse.com
- Cleanup with a spec-cleaner so I can understand what
  is going around here.
* Thu Sep 12 2013 mvyskocil@suse.com
- log4j and log4j-mini are in conflict
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Tue Jul 16 2013 mls@suse.de
- get rid of wrong dir modifier in filelist
* Thu Dec 10 2009 mvyskocil@suse.cz
- refreshed patches
  * log4j-javadoc-xlink.patch
  * log4j-jmx-Agent.patch
  * log4j-logfactor5-userdir.patch
  * log4j-mx4j-tools.patch
* Wed Jul 16 2008 coolo@suse.de
- even more packages to build ignore
* Fri Jun 27 2008 coolo@suse.de
- avoid build cycle between axis and log4j
* Tue May  6 2008 mvyskocil@suse.cz
- removed a dots in a names of geronimo-* packages
* Tue Apr  8 2008 mvyskocil@suse.cz
- updated to 1.2.5 [bnc#355798]
- merged a spec with jpackage 1.7
  - the ant arguments was splitted to several lines
  - new BuildRequires:
  - classpathx-javamail
  - geronimo-jaf
  - geronimo-jms
  - a new patches to break of a dependendy on Sun's HtmlAdaptorServer
    (replaced by HttpAdaptor from mx4j package)
  - added a gjc build branch
- created an autogenerated -mini specfile used for bootstrap (hint from sbrabec@suse.cz)
  - added an explicit provides of log4j symbol for log4j-mini (automatically by script)
- replaced a name `macro' by `real', because the -mini package has a different name
- disable the javadoc and manual subpackages for -mini build
* Thu Jun  7 2007 sbrabec@suse.cz
- Removed invalid desktop Category "Application" (#254654).
* Fri May 18 2007 dbornkessel@suse.de
- removed mx4j BuildReq to avoid build cycle ... apparently it was not used at compile time
* Tue May  8 2007 dbornkessel@suse.de
- use mx4j instead of jmx
* Wed Feb 15 2006 stbinner@suse.de
- add GenericName to .desktop files
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Nov  8 2005 jsmeix@suse.de
- Current version 1.2.12 from JPackage.org
* Wed Sep 28 2005 dmueller@suse.de
- add norootforbuild
* Thu Nov 25 2004 ro@suse.de
- added suse_update_desktop_file
* Thu Sep 23 2004 mskibbe@suse.de
- change specfile(suse_update_desktop_file)
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires for javadoc subpackage.
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 1.2.8 (JPackage 1.5)
