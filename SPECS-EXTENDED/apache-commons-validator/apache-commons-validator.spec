%define base_name validator
%define short_name commons-%{base_name}
Summary:        Apache Commons Validator
Name:           apache-%{short_name}
Version:        1.5.0
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-validator/
Source0:        https://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         commons-validator-1.5.0-srcencoding.patch
Patch1:         commons-validator-1.5.0-locale.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  commons-beanutils
BuildRequires:  commons-collections
BuildRequires:  commons-digester >= 1.8
BuildRequires:  commons-logging
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
Requires:       commons-beanutils >= 1.5
Requires:       commons-collections
Requires:       commons-digester >= 1.8
Requires:       commons-logging >= 1.0.2
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch
%if %{with_check}
BuildRequires:  junit
%endif

%description
A common issue when receiving data either electronically or from user
input is verifying the integrity of the data. This work is repetitive
and becomes even more complicated when different sets of validation
rules need to be applied to the same set of data based, for example, on
locale. Error messages may also vary by locale. This package attempts
to address some of these issues and speed development and maintenance
of validation rules.

%package javadoc
Summary:        Javadoc for jakarta-commons-validator
Group:          Documentation/HTML
Requires(pre):  coreutils

%description javadoc
A common issue when receiving data either electronically or from user
input is verifying the integrity of the data. This work is repetitive
and becomes even more complicated when different sets of validation
rules need to be applied to the same set of data based on locale for
example. Error messages may also vary by locale. This package attempts
to address some of these issues and speed development and maintenance
of validation rules.

This package contains the javadoc documentation for the Jakarta Commons
Validator Package.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1
%patch1 -p1

sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' RELEASE-NOTES.txt
sed -i 's/\r//' NOTICE.txt

%pom_remove_parent .

%build
export CLASSPATH=$(build-classpath \
                   commons-collections \
                   commons-logging \
                   commons-digester \
                   commons-beanutils \
                   junit)
ant \
    -Dcompile.source=11 -Dcompile.target=11 \
    -Dskip.download=true -Dbuild.sysclasspath=first \
    dist

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -pm 644 dist/%{short_name}-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
# pom
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a org.apache.commons:%{short_name}
# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api*/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}/%{name}/

%check
export CLASSPATH=$(build-classpath \
                   commons-collections \
                   commons-logging \
                   commons-digester \
                   commons-beanutils \
                   junit)
ant \
    -Dcompile.source=11 -Dcompile.target=11 \
    -Dant.build.javac.source=11 -Dant.build.javac.target=11 \
    -Dskip.download=true -Dbuild.sysclasspath=first \
    test


%files -f .mfiles
%license LICENSE.txt
%doc NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/%{short_name}.jar

%files javadoc
%license LICENSE.txt
%doc %{_javadocdir}/%{name}

%changelog
* Mon Nov 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.5.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Enable check section
- License verified

* Thu Apr 28 2022 Dirk Müller <dmueller@suse.com>
- use https urls

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
- Remove special conditions for suse_version 1110

* Fri Dec 21 2018 Fridrich Strba <fstrba@suse.com>
- Build against commons-digester >= 1.8
- Removed patch:
  * commons-validator-1.5.0-digester.patch
    + building against commons-digester >= 1.8, this patch is
    superfluous

* Fri Dec 21 2018 Fridrich Strba <fstrba@suse.com>
- Update to 1.5.0
- Install the maven pom file
- Removed patch:
  * commons-validator-1.3.1-crosslink.patch
    + not needed
- Added patch:
  * commons-validator-1.5.0-digester.patch
    + fix build with older versions of commons-digester
- Modified patches:
  * commons-validator-1.3.1-srcencoding.patch ->
    commons-validator-1.5.0-srcencoding.patch
    + specify encoding utf-8 for javac and javadoc invocation
    instead of escaping characters
  * commons-validator-1.3.1-locale.patch ->
    commons-validator-1.5.0-locale.patch
    + Adapt the patch to the 1.5.0 context
    + Add the sysproperty to the junit task

* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility

* Mon Oct  9 2017 fstrba@suse.com
- Fix build and running of junit tests with Java 9+
- Added patch:
  * commons-validator-1.3.1-locale.patch
    + Made two different test.routines target, one with java <= 1.8
    and one with java 9+, since the locale providers changed
    between java 1.8 and 9. Moreover, the options that Java 9
    needs to run in compatibility mode break build with lower
    versions of Java.

* Thu Sep 14 2017 fstrba@suse.com
- Build with java source and target 1.6
- Use java-devel < 1.9 because with jdk9, some unit tests fail
- Clean spec file

* Tue Jul  8 2014 tchvatal@suse.com
- Cleanup with spec-cleaner and fix build on Factory.

* Mon Apr 14 2014 darin@darins.net
- add requirements for SLES

* Fri Jun 15 2012 mvyskocil@suse.cz
- update to 1.3.1
- rename to apache-commons-validator

* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Thu Jul 28 2005 jsmeix@suse.de
- Current version 1.1.4 from JPackage.org

* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.1.3 from JPackage.org

* Tue Feb 22 2005 skh@suse.de
- Update to version 1.1.3

* Sun Sep  5 2004 skh@suse.de
- Initial package created with version 1.0.2 (Jakarta 1.5)
