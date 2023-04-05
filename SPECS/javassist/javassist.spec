#
# spec file for package javassist
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2000-2005, JPackage Project
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
%define tar_version rel_3_23_1_ga
Summary:        Java Programming Assistant: bytecode manipulation
Name:           javassist
Version:        3.23.1
Release:        7%{?dist}
License:        LGPL-2.1-or-later OR MPL-1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://www.javassist.org/
Source0:        https://github.com/jboss-javassist/javassist/archive/%{tar_version}.tar.gz
Patch0:         javassist-java8-compat.patch
Patch1:         javassist-osgi.patch
BuildRequires:  ant >= 1.6
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
Javassist (Java Programming Assistant) makes Java bytecode manipulation
simple. It is a class library for editing bytecodes in Java; it enables
Java programs to define a new class at runtime and to modify a class
file when the JVM loads it. Unlike other similar bytecode editors,
Javassist provides two levels of API: source level and bytecode level.
If the users use the source-level API, they can edit a class file
without knowledge of the specifications of the Java bytecode. The whole
API is designed with only the vocabulary of the Java language. You can
even specify inserted bytecode in the form of source text; Javassist
compiles it on the fly. On the other hand, the bytecode-level API
allows the users to directly edit a class file as other editors.

%package demo
Summary:        Samples for javassist
Group:          Documentation/Other
Requires:       javassist = %{version}-%{release}

%description demo
Samples for javassist.

%{summary}.

%package javadoc
Summary:        Javadoc for javassist
Group:          Documentation/HTML

%description javadoc
Javadoc for javassist.

%{summary}.

%package manual
Summary:        Tutorial for javassist
Group:          Documentation/Other

%description manual
Tutorial for javassist.

%{summary}.

%prep
%setup -q -n %{name}-%{tar_version}
%if %{?pkg_vcmp:%pkg_vcmp java-devel < 9}%{!?pkg_vcmp:1}
%patch0 -p1
%endif
%patch1 -p1
for j in $(find . -name "*.jar"); do
        mv $j $j.no
done

%build
ant -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 dist

%install
# jars
mkdir -p %{buildroot}/%{_javadir}
cp -p %{name}.jar \
  %{buildroot}/%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}/%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a javassist:javassist

# demo
mkdir -p %{buildroot}/%{_datadir}/%{name}-%{version}
cp -pr sample/* %{buildroot}/%{_datadir}/%{name}-%{version}

# javadoc
mkdir -p %{buildroot}/%{_javadocdir}/%{name}
cp -pr html/* %{buildroot}/%{_javadocdir}/%{name}

%fdupes -s %{buildroot}/%{_javadocdir}/%{name}/jquery/

# manual
mkdir -p %{buildroot}/%{_docdir}/%{name}-%{version}/tutorial
cp -pr tutorial/* %{buildroot}/%{_docdir}/%{name}-%{version}/tutorial
cp -p License.html %{buildroot}/%{_docdir}/%{name}-%{version}

%files
%defattr(0644,root,root,0755)
%dir %{_docdir}/%{name}-%{version}
%license %{_docdir}/%{name}-%{version}/License.html
%{_javadir}/*.jar
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/tutorial

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.23.1-7
- Moved from extended to core
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.23.1-6
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 3.23.1-5.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Mar 25 2020 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * javassist-osgi.patch
    + Add OSGi manifest to the javassist.jar

* Mon Apr 15 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * javassist-java8-compat.patch
  - Allow building on systems that do not have java 9 or higher

* Thu Oct 18 2018 Fridrich Strba <fstrba@suse.com>
- Install and package the maven pom and metadata files

* Mon Oct 15 2018 Fridrich Strba <fstrba@suse.com>
- BuildRequire at least Java 9. This version uses APIs introduced
  in Java 9

* Sun Oct  7 2018 Jan Engelhardt <jengelh@inai.de>
- Replace old $RPM_* shell vars by macros.

* Fri Oct  5 2018 pmonrealgonzalez@suse.com
- Version update to 3.23.1:
  * 3.23.1 Github PR #171
  * 3.23   Fix leaking file handlers in ClassPool and removed
    ClassPath.close(). Github issue #165
  * 3.22   Java 9 supports.
    JIRA JASSIST-261.
- Dropped patch fixed upstream:
    javassist-rel_3_21_0_ga-javadoc.patch

* Fri Sep  8 2017 fstrba@suse.com
- Specify java target and source version 1.6 in order to allow
  building with jdk9
- Added patch:
  * javassist-rel_3_21_0_ga-javadoc.patch
  - fix javadoc errors that are fatal with jdk9

* Fri Jun  9 2017 tchvatal@suse.com
- Version update to 3.21.0:
  * various compiler settings
  * Require java >= 1.6

* Sat Jan 24 2015 p.drouand@gmail.com
- Update to version 3.19.0
  * Including a number of bug fixes and Java 8 supports.
- Clean up specfile
- Remove redundant %%clean section
- Build for java API 1.5
- Remove unzip requirement
- Update home page and download source Urls

* Wed Sep  3 2014 ro@suse.de
- fix group entries for subpackages

* Tue Sep  2 2014 ro@suse.de
- sanitize release line in specfile

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Thu Mar  7 2013 cfarrell@suse.com
- license update: LGPL-2.1+ or MPL-1.1
  This is a dual license so the operator is ^or^ not ^and^

* Tue Mar  5 2013 coolo@suse.com
- update license to new format

* Fri Apr 27 2012 mvyskocil@suse.cz
- format spec file for Factory

* Thu Dec  9 2010 mc@suse.de
- initial release
