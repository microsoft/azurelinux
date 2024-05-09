#
# spec file for package jsr-305
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
%global svn_revision 51
%global svn_date 20130910
Summary:        Correctness annotations for Java code
Name:           jsr-305
Version:        0.1+%{svn_date}
Release:        8%{?dist}
# The majority of code is BSD-licensed, but some Java sources
# are licensed under CC-BY license, see: $ grep -r Creative .
License:        BSD AND CC-BY
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://code.google.com/archive/p/jsr-305
# There has been no official release yet.  This is a snapshot of the Subversion
# repository as of 10 Sep 2013.  Use the following commands to generate the
# tarball:
#   svn export -r %{svn_revision} https://%{name}.googlecode.com/svn/trunk %{name}
#   tar -czvf %{name}-%{svn_date}svn.tgz %{name}
# Source0:      https://storage.googleapis.com/google-code-archive-source/v2/code.google.com/jsr-305/source-archive.zip
Source0:        %{_distro_sources_url}/jsr-305-%{svn_date}svn.tgz
Source1:        jsr-305-ri-build.xml
# File containing URL to CC-BY license text
Source2:        NOTICE-CC-BY.txt
BuildRequires:  ant
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
Provides:       mvn(com.google.code.findbugs:jsr305) = %{version}-%{release}
BuildArch:      noarch

%package javadoc
Summary:        Javadoc documentation for %{name}
Group:          Documentation/HTML

%description
This package contains reference implementations, test cases, and other
documents for Java Specification Request 305: Annotations for Software Defect
Detection.

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}
cp -a %{SOURCE1} ri/build.xml
cp %{SOURCE2} NOTICE-CC-BY
dos2unix sampleUses/pom.xml

# do not build sampleUses module - it causes Javadoc generation to fail
%pom_disable_module sampleUses

for module in ri tcl sampleUses proposedAnnotations; do
  %pom_remove_parent ${module}
done

%build
export OPT_JAR_LIST=:
export CLASSPATH=
pushd ri
%{ant} -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 \
       -Dversion=%{version} -Djava.javadoc=%{_javadocdir}/java
popd

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 ri/jsr-305-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}.jar %{buildroot}%{_javadir}/jsr305.jar

# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 ri/pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a com.google.code.findbugs:jsr305

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr ri/javadoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license ri/LICENSE NOTICE-CC-BY
%{_javadir}/jsr305.jar

%files javadoc
%license ri/LICENSE NOTICE-CC-BY
%{_javadocdir}/%{name}

%changelog
* Wed Feb 28 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.1+20130910-8
- build with msopenjdk-17 

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1+20130910-8
- Updating naming for 3.0 version of Azure Linux.


* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.1+20130910-7
- Fixing maven provides

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1+20130910-6
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1+20130910-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.1+20130910-4.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to parent from all pom files

* Wed Mar 13 2019 Fridrich Strba <fstrba@suse.com>
- Fix a broken link

* Wed Feb  6 2019 Fridrich Strba <fstrba@suse.com>
- Cleanup of spec file
- Do not distribute sampleUses as documentation
- Fix javadoc group

* Wed Oct 31 2018 Fridrich Strba <fstrba@suse.com>
- Package also the parent pom

* Thu Oct 25 2018 Fridrich Strba <fstrba@suse.com>
- Update to newer snapshot (svn revision 51)
- Add com.google.code.findbugs:jsr305 alias to the maven provides

* Tue Sep 19 2017 fstrba@suse.com
- Fix build with jdk9: specify java target and source 1.6

* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
- removed "section free" tag
- spec cleaned using spec-cleaner

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Fri Jun 27 2014 tchvatal@suse.com
- Remove java-javadoc dep as it is not needed to sort out SLE11

* Tue Sep 10 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
- don't install versioned jars and javadocs

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Thu Jan 26 2012 mvyskocil@suse.cz
- remove non working url from spec

* Fri Dec  9 2011 coolo@suse.com
- fix license to be in spdx.org format

* Mon Nov 15 2010 mvyskocil@suse.cz
- fix bnc#653551 - No license indicators in jsr-305 package
  * add license file with BSD license text
    as written on https://code.google.com/p/jsr-305/

* Wed Jun  3 2009 mvyskocil@suse.cz
- Initial SUSE packaging based on jpp 5.0
