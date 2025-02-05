Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache-commons-io
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


%define base_name       io
%define short_name      commons-%{base_name}
%bcond_with tests
Name:           apache-%{short_name}
Version:        2.14.0
Release:        1%{?dist}
Summary:        Utilities to assist with developing IO functionality
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/%{base_name}
Source0:        https://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        https://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz.asc
Source2:        %{name}-build.xml
BuildRequires:  ant >= 1.6
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
Provides:       %{short_name} = %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Commons-IO contains utility classes, stream implementations,
file filters, and endian classes. It is a library of utilities
to assist with developing IO functionality.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description    javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE2} build.xml

%pom_remove_parent

%build
%{ant} \
	-Dcompiler.source=1.8 \
%if %{without tests }
	-Dtest.skip=true \
%endif
    jar javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -p -m 0644 target/%{short_name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{short_name}.jar
ln -sf %{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}.pom
%add_maven_depmap %{short_name}.pom %{short_name}.jar -a "org.apache.commons:commons-io"
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc RELEASE-NOTES.txt
%{_javadir}/%{name}.jar

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Mon Oct 7 2024 Bhagyashri Pathak <bhapathak@microsoft.com> - 2.14.0-1
- Upgrade to 2.14.0 to fix the CVE-2024-47554.
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.8.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2.8.0-1.2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Oct 27 2020 Pedro Monreal <pmonreal@suse.com>
- Update to 2.8.0
  * Lots of added functions, fixes and updates.
  * https://commons.apache.org/proper/commons-io/changes-report.html#a2.8.0
* Wed Jun  3 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Update to upstream version 2.7
  * https://commons.apache.org/proper/commons-io/changes-report.html#a2.7
  * Lots of bugfixes, updates and enhancements
  * Java 8 or later is required
* Wed Mar 27 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Tue Feb 26 2019 Fridrich Strba <fstrba@suse.com>
- Update to upstream version 2.6
  * many bugfixes, features and enhancenments, like
    Automatic-Module-Name entry in manifest
  * requires jdk7 or later
  * see RELEASE-NOTES.txt for details
- Generated a build.xml to be able to build with ant
- Build with tests is now optional
- Removed patch:
  * commons-io-version-property.patch
    + not needed anymore in this version
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Run fdupes on documentation
* Thu Sep 14 2017 fstrba@suse.com
- Fix build with jdk9 by specifying source and target level 1.6
* Sun May 21 2017 tchvatal@suse.com
- Remove unused depedencies
* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Mon Jul  7 2014 tchvatal@suse.com
- Use junit not junit4
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Wed Mar 20 2013 mmeister@suse.com
- Added url as source.
  Please see http://en.opensuse.org/SourceUrls
* Thu Oct 25 2012 mvyskocil@suse.com
- update to the latest upstream version 2.4 (needed by fop 1.1)
  * many bugfixes, features and enhancenments, like
  * XmlStreamReader support for UTF-32
  * requires jdk6 or later
  * see RELEASE-NOTES.txt for details
- rename to apache-commons-io to stay compatible with upstream and fedora
- add commons-io-version-property.patch to fix the version in build.xml
* Mon Aug 25 2008 mvyskocil@suse.cz
- target=1.5
- removed a build gcj support
- removed a javadoc %%post/postun
- fixed a wrong end of line encoding
* Thu Mar 13 2008 mvyskocil@suse.cz
- Initial package created with version 1.3.2 (JPackage 1.7)
