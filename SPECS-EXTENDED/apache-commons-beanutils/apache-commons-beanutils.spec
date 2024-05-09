%define base_name	beanutils
%define short_name	commons-%{base_name}
Summary:        Utility methods for accessing and modifying the properties of JavaBeans
Name:           apache-commons-beanutils
Version:        1.9.4
Release:        5%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://commons.apache.org/beanutils
Source0:        https://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         jdk11.patch
Patch1:         apache-commons-beanutils-fix-build-version.patch
BuildRequires:  ant
BuildRequires:  commons-collections
BuildRequires:  commons-logging
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  xml-commons-apis
Requires:       commons-collections >= 2.0
Requires:       commons-logging >= 1.0
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch

%description
The scope of this package is to create a package of Java utility
methods for accessing and modifying the properties of arbitrary
JavaBeans.  No dependencies outside of the JDK are required, so the use
of this package is very lightweight.

%package javadoc
Summary:        Javadoc for jakarta-commons-beanutils

%description javadoc
The scope of the Jakarta Commons BeanUtils Package is to create a
package of Java utility methods for accessing and modifying the
properties of arbitrary JavaBeans.  No dependencies outside of the JDK
are required, so the use of this package is very lightweight.

This package contains the javadoc documentation for the Jakarta Commons
BeanUtils Package.

%prep
%autosetup -p1 -n %{short_name}-%{version}-src
sed -i 's/\r//' *.txt
# bug in ant build
touch README.txt

%pom_remove_parent

%build
export CLASSPATH=%(build-classpath commons-collections commons-logging)
ant -Dbuild.sysclasspath=first dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

pushd %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{name}.jar
for jar in *.jar; do
    ln -sf ${jar} `echo $jar| sed "s|apache-||g"`
done
popd # come back from javadir

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom
%add_maven_depmap %{name}-%{version}.pom %{name}-%{version}.jar -a "%{short_name}:%{short_name}-core,%{short_name}:%{short_name}-bean-collections"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files
%defattr(0644,root,root,0755)
%license LICENSE.txt
%doc NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Mon Nov 07 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.9.4-5
- Update Source url to https.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.4-4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Oct  7 2019 Fridrich Strba <fstrba@suse.com>
- Add aliases to account for the ephemeral commons-beanutils-core
  and commons-beanutils-bean-collections split.

* Thu Oct  3 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to parent pom, since it is not needed when not
  building with maven

* Wed Aug 21 2019 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Update to 1.9.4
  * BEANUTILS-520: BeanUtils mitigate CVE-2014-0114
- Security fix: [bsc#1146657, CVE-2019-10086]
  * PropertyUtilsBean (and consequently BeanUtilsBean) now disallows class
    level property access by default, thus protecting against CVE-2014-0114.
- Fix build version in build.xml
  * Added apache-commons-beanutils-fix-build-version.patch

* Tue Oct 23 2018 Fridrich Strba <fstrba@suse.com>
- Cleanup the maven pom files installation

* Fri Sep 21 2018 Tomáš Chvátal <tchvatal@suse.com>
- Fix the Source URLs to use mirrors properly

* Thu Sep 20 2018 pmonrealgonzalez@suse.com
- Updated to 1.9.3
  * This is a bug fix release, which also improves the tests for
    building on Java 8.
  * Note that Java 8 and later no longer support indexed bean
    properties on java.util.List, only on arrays like String[].
    (BEANUTILS-492). This affects PropertyUtils.getPropertyType()
    and PropertyUtils.getPropertyDescriptor(); their javadoc have
    therefore been updated to reflect this change in the JDK.
  * Changes in this version include:
  - Fixed Bugs:
  * BEANUTILS-477: Changed log level in FluentPropertyBeanIntrospector
  * BEANUTILS-492: Fixed exception when setting indexed properties
    on DynaBeans.
  * BEANUTILS-470: Precision lost when converting BigDecimal.
  * BEANUTILS-465: Indexed List Setters fixed.
  - Changes:
  * BEANUTILS-433: Update dependency from JUnit 3.8.1 to 4.12.
  * BEANUTILS-469: Update commons-logging from 1.1.1 to 1.2.
  * BEANUTILS-474: FluentPropertyBeanIntrospector does not use the
    same naming algorithm as DefaultBeanIntrospector.
  * BEANUTILS-490: Update Java requirement from Java 5 to 6.
  * BEANUTILS-482: Update commons-collections from 3.2.1 to 3.2.2
    (CVE-2015-4852).
  * BEANUTILS-490: Update java requirement to Java 6.
  * BEANUTILS-492: IndexedPropertyDescriptor tests now pass on Java 8.
  * BEANUTILS-495: DateConverterTestBase fails on M/d/yy in Java 9.
  * BEANUTILS-496: testGetDescriptorInvalidBoolean fails on Java 9.
  - Historical list of changes:
    https://commons.apache.org/proper/commons-beanutils/changes-report.html
- Refreshed patch jdk9.patch for this version update

* Tue May 15 2018 fstrba@suse.com
- Modified patch:
  * jdk9.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
- Run fdupes on documentation

* Thu Sep 14 2017 fstrba@suse.com
- Added patch:
  * jdk9.patch
  - Specify java source and target level 1.6 in order to allow
    building with jdk9

* Thu Dec  4 2014 p.drouand@gmail.com
- Remove java-devel dependency; not needed anymore

* Tue Jul  8 2014 tchvatal@suse.com
- Cleanup bit with spec-cleaner

* Mon Jul  7 2014 dmacvicar@suse.de
- update to 1.9.2
- CVE-2014-3540:
  'class' property is exposed, potentially leading to RCE (bnc#885963)
- for full changelog, see
  * https://commons.apache.org/proper/commons-beanutils/javadocs/v1.9.0/RELEASE-NOTES.txt
  * https://commons.apache.org/proper/commons-beanutils/javadocs/v1.9.1/RELEASE-NOTES.txt
  * https://commons.apache.org/proper/commons-beanutils/javadocs/v1.9.2/RELEASE-NOTES.txt

* Mon Apr  2 2012 mvyskocil@suse.cz
- update to 1.8.3 and rename to apache- to follow the upstream
- fixes in this release
  * memory leak in jdk5/jdk6 BEANUTILS-291, BEANUTILS-366
  * BEANUTILS-373 MethodUtils is not thread safe because WeakFastHashMap which
    uses WeakHashMap is not thread-safe
  * [BEANUTILS-371] Add constructors which have useColumnLabel parameter to
    ResultSetDynaClass and RowSetDynaClass
  * and a lot of other like NPE in BeanUtilsBean.setProperty()

* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.

* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.7.0 from JPackage.org

* Mon Feb 21 2005 skh@suse.de
- update to version 1.7.0
- don't use icecream

* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage

* Sun Sep  5 2004 skh@suse.de
- Initial package created with version 1.6.1 (JPackage 1.5)
