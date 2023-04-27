#
# spec file for package apache-commons-lang3
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
%define base_name lang3
%define short_name commons-%{base_name}
Summary:        Apache Commons Lang Package
Name:           apache-%{short_name}
Version:        3.8.1
Release:        5%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-lang
Source0:        https://archive.apache.org/dist/commons/lang/source/%{short_name}-%{version}-src.tar.gz
Source1:        build.xml
Source2:        default.properties
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.7
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
Provides:       %{short_name} = %{version}-%{release}
BuildArch:      noarch

%description
The standard Java libraries fail to provide enough methods for
manipulation of its core classes. The Commons Lang Component provides
these extra methods.

The Commons Lang Component provides a host of helper utilities for the
java.lang API, notably String manipulation methods, basic numerical
methods, object reflection, creation and serialization, and System
properties. Additionally it contains an inheritable enum type, an
exception structure that supports multiple types of nested-Exceptions
and a series of utilities dedicated to help with building methods, such
as hashCode, toString and equals.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE1} .
cp %{SOURCE2} .
sed -i 's/\r//' *.txt

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.apache.commons</groupId>" .

%build
export OPT_JAR_LIST=`cat %{_sysconfdir}/ant.d/junit`
export CLASSPATH=
ant \
    -Dcompile.source=1.7 -Dcompile.target=1.7 \
    -Dfinal.name=%{short_name} \
     jar javadoc

%install

# jars
install -dm 755 %{buildroot}%{_javadir}
install -m 0644  target/%{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
# pom
install -dm 755 %{buildroot}%{_mavenpomdir}
install -m 0644  pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}/%{name}/

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc RELEASE-NOTES.txt
%{_javadir}/%{short_name}.jar

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.8.1-5
- Moved from extended to core
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.1-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 3.8.1-3.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven

* Mon Feb  4 2019 Fridrich Strba <fstrba@suse.com>
- Clean-up the spec file and install less jar symlinks

* Mon Oct 22 2018 Fridrich Strba <fstrba@suse.com>
- Build commons-lang3-3.8.1 using modified build.xml and
  default.properties from 3.4.
- Removed patch:
  * commons-lang3-3.4-javadoc.patch
  - integrated in the build.xml
- Use source and target version 1.7, since the code contains
  diamond operator.

* Wed May  2 2018 tchvatal@suse.com
- Format with spec-cleaner

* Mon Oct  9 2017 fstrba@suse.com
- Modified patch:
  * commons-lang3-3.4-javadoc.patch
    + Fix build with jdk9
- Allow building with jdk9 too
- Run fdupes on javadoc

* Thu Sep 14 2017 fstrba@suse.com
- Specify java target and source level 1.6
- Force building with jdk < 1.9, since jdk9's javadoc chocks on one
  class file (internal error)

* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local

* Sun Jan 24 2016 p.drouand@gmail.com
- Initial release (version 3.4)
