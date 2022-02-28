Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package junitperf
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define section free

Name:           junitperf
Version:        1.9.1
Release:        27%{?dist}
Summary:        JUnit extension for performance and scalability testing
License:        BSD
Group:          Development/Libraries/Java
Url:            https://github.com/clarkware/junitperf
Source0:        https://github.com/clarkware/junitperf/archive/refs/tags/1.9.1.zip#/%{name}-%{version}.zip
Patch0:         junitperf-1.9.1-javadoc.patch
Requires:       junit >= 3.2
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-devel
BuildRequires:  javapackages-tools
BuildRequires:  junit >= 3.2
BuildRequires:  unzip
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
JUnitPerf is a collection of JUnit test decorators used to measure the
performance and scalability of functionality contained within existing
JUnit tests.



%package javadoc
Summary:        JUnit extension for performance and scalability testing
Group:          Development/Libraries/Java

%description javadoc
JUnitPerf is a collection of JUnit test decorators used to measure the
performance and scalability of functionality contained within existing
JUnit tests.



%package demo
Summary:        JUnit extension for performance and scalability testing
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description demo
JUnitPerf is a collection of JUnit test decorators used to measure the
performance and scalability of functionality contained within existing
JUnit tests.



%prep
%setup -q
%patch0 -p1
# remove all binary libs
find . -name "*.jar" | xargs -t rm

%build
export CLASSPATH=
export OPT_JAR_LIST="junit ant/ant-junit"
# performance tests sometimes failed on build farm, so lets disable them to avoid unpredictable build fails
#ant -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 -Dbuild.sysclasspath=first jar test javadoc
ant -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 -Dbuild.sysclasspath=first jar javadoc

%install
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 0644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
# demo
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples $RPM_BUILD_ROOT%{_datadir}/%{name}

%files
%defattr(0644,root,root,0755)
%doc LICENSE README docs/JUnitPerf.html
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.1-27
- Removing the explicit %%clean stage.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.1-26
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Sep  8 2017 fstrba@suse.com
- Specify java source and target levels 1.6 in order to allow build
  with jdk9
- Added patch:
  * junitperf-1.9.1-javadoc.patch
    + Fix javadoc errors which are fatal with jdk9
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Jun 12 2009 mvyskocil@suse.cz
- Disabled junit testing, because performance testing fails on build farm with
  many virtual machinses
* Tue May 12 2009 mvyskocil@suse.cz
- Initial packaging of junitperf 1.9.1 from jpp 5.0
