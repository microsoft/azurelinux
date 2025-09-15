Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package relaxngDatatype
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


Name:           relaxngDatatype
Version:        2011.1
Release:        6%{?dist}
Summary:        RELAX NG Datatype API
License:        BSD-3-Clause
Group:          Development/Languages/Java
URL:            https://sourceforge.net/projects/relaxng
Source0:        https://github.com/java-schema-utilities/relaxng-datatype-java/archive/relaxngDatatype-%{version}.tar.gz
# License is not available in the tarball, this copy fetched from the tarball on the old sourceforge.net site
Source1:        copying.txt
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
Provides:       %{name}-javadoc = %{version}-%{release}
BuildArch:      noarch

%description
RELAX NG is a public space for test cases and other ancillary software
related to the construction of the RELAX NG language and its
implementations.

%prep
%setup -q -n relaxng-datatype-java-relaxngDatatype-%{version}
cp -p %{SOURCE1} .

%pom_remove_parent .

%build
ant \
    -Dbuild.sysclasspath=only \
    -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8

%install
install -Dpm 644 %{name}.jar \
  %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a relaxngDatatype:relaxngDatatype

%files -f .mfiles
%license copying.txt
%{_javadir}/*.jar

%changelog
* Thu Feb 27 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2011.1-6
- Error fix
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2011.1-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Apr 01 2021 Henry Li <lihl@microsoft.com> - 2011.1-4.7
- Remove obsoletes and provides relaxngDataType-javadoc

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 2011.1-4.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the parent pom and remove its reference from the
  pom.xml files, since we are not building using Maven.
- Install unversioned jar/pom files
* Tue Dec 18 2018 Fridrich Strba <fstrba@suse.com>
- Depend on sonatype-oss-parent to satisfy maven dependencies on
  build time.
* Fri Oct 19 2018 Fridrich Strba <fstrba@suse.com>
- Install the provided pom file in order to generate correctly
  the mvn(...) dependencies
* Thu Nov 30 2017 fstrba@suse.com
- Update to version 2011.1
- Removed patch:
  * no-javadoc.patch
    + not needed
* Sun Sep 10 2017 fstrba@suse.com
- Specify java source and target levels 1.6 in order to allow
  building with jdk9
* Fri Jun  9 2017 tchvatal@suse.com
- Obsolete javadoc to bootstrap using gcj
- Add patch no-javadoc.patch
* Fri Jul 11 2014 tchvatal@suse.com
- Do not use versioned javadoc dir.
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Aug  7 2008 mvyskocil@suse.cz
- First release of version 1.0 in Suse (based on spec from jpackage.org 1.7)
