Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache-commons-net
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


%global base_name    net
%global short_name   commons-%{base_name}
%bcond_with tests
Name:           apache-%{short_name}
Version:        3.6
Release:        3%{?dist}
Summary:        Internet protocol suite Java library
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/%{base_name}/
Source0:        https://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
This is an Internet protocol suite Java library originally developed by
ORO, Inc.  This version supports Finger, Whois, TFTP, Telnet, POP3, FTP,
NNTP, SMTP, and some miscellaneous protocols like Time and Echo as well
as BSD R command support. The purpose of the library is to provide
fundamental protocol access, not higher-level abstractions.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE1} build.xml
%pom_remove_parent .

%build
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# pom
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar
ln -sf %{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}.pom
%add_maven_depmap %{short_name}.pom %{short_name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc README.md RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt
%{_javadir}/%{name}.jar

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.6-2.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Jan  9 2020 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom, since we don't build with
  maven
* Sat Mar  2 2019 Fridrich Strba <fstrba@suse.com>
- Rename to apache-commons-net
- Upgrade to version 3.6
- Generate and customize the ant build file
* Fri Sep  8 2017 fstrba@suse.com
- Specify java source and target 1.6 in order to allow building
  with jdk9
* Fri Jun  9 2017 tchvatal@suse.com
- Require java 1.6 or newer to build
* Fri May 19 2017 tchvatal@suse.com
- Fix build with new javapackages-tools
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Tue Jul  8 2014 tchvatal@suse.com
- Fix sle build properly.
* Wed Apr 30 2014 darin@darins.net
- Update project_xml patch for strict fuzz
- Suppress bytecode check on SLES
- remove java-javadoc build requirement
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Sep  6 2013 mvyskocil@suse.com
- use add_maven_depmap
* Thu Nov 29 2012 mvyskocil@suse.com
- buildrequire saxon8 (bnc#780666)
- remove self-obsolete commons-net
* Wed Nov 28 2012 mvyskocil@suse.com
- require saxon9 for build
- don't build with java5 target
* Tue Jun 26 2012 mvyskocil@suse.cz
- remove openjdk6 dependency
* Mon Mar 12 2012 mvyskocil@suse.cz
- fix bnc#749895 - ant FTP action fails on the date with leap year
* Tue Apr 28 2009 mvyskocil@suse.cz
- Initial SUSE packaging (version 1.4.1 from jpp5)
