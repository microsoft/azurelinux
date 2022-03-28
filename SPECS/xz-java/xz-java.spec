#
# spec file for package xz-java
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2013 Peter Conrad
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

Summary:        Pure Java implementation of XZ compression
Name:           xz-java
Version:        1.8
Release:        5%{?dist}
License:        Public Domain
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://tukaani.org/xz/java.html
Source:         http://tukaani.org/xz/xz-java-%{version}.zip
Patch0:         xz-java-source-version.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  unzip
BuildArch:      noarch
Provides:       java-xz
Obsoletes:      java-xz

%description
This is an implementation of XZ data compression in pure Java.
Single-threaded streamed compression and decompression and random access
decompression have been implemented.

%package javadoc
Summary:        API documentation of Java XZ compression library
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation of xz-java.

%prep
%setup -q -c -n %{name}
%patch0 -p1

%build
sed -i 's/linkoffline="[^"]*"//;/extdoc_/d' build.xml
ant  -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 clean jar doc maven

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 build/maven/xz-%{version}.jar  %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir} && ln -s %{name}.jar xz.jar)
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 build/maven/xz-%{version}.pom %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/doc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license COPYING
%doc NEWS README THANKS
%{_javadir}/xz.jar

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.8-5
- Move to SPECS
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.8-3.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Feb 13 2019 Klaus Kämpf <kkaempf@suse.com>
- add provides/obsoletes for xz-java (boo#1125298)
* Sat Jan 26 2019 Jan Engelhardt <jengelh@inai.de>
- Trim future goals from description.
* Wed Jan  9 2019 Fridrich Strba <fstrba@suse.com>
- Modified patch:
  * java-3d_source_version.patch -> xz-java-source-version.patch
    + change name to correspond to reality
* Sat Oct 27 2018 Fridrich Strba <fstrba@suse.com>
- renamed package to xz-java
* Tue Oct 23 2018 Fridrich Strba <fstrba@suse.com>
- Update to 1.8
- Modified patch:
  * java-3d_source_version.patch
  - Rediff to changed context
* Mon Oct 22 2018 Fridrich Strba <fstrba@suse.com>
- Generate the maven pom files and install them
* Sat May  3 2014 ecsos@opensuse.org
- update to 1.5
* Mon Nov 11 2013 robertherb@arcor.de.de
- Update to 1.4
- renamed package to java-xz
* Sat Aug 31 2013 conrad@quisquis.de
- Fixed Source header
* Sat Aug 31 2013 conrad@quisquis.de
- Upgrade to 1.3
* Fri Apr  5 2013 conrad@quisquis.de
- Fixed fedora build deps
- Fixed license string
* Thu Mar 28 2013 conrad@quisquis.de
- Disabled external links in javadoc
* Thu Mar 28 2013 conrad@quisquis.de
- Disabled download_files service - upstream server hangs
* Thu Mar 28 2013 conrad@quisquis.de
- Initial project creation
