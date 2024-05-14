Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package servletapi4
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

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define base_name       servletapi
%define full_name       jakarta-%{base_name}
Name:           servletapi4
Version:        4.0.4
Release:        302%{?dist}
Summary:        Java servlet and JSP implementation classes
License:        ASL 1.1
Group:          Development/Libraries/Java
Url:            https://jakarta.apache.org/tomcat/
Source0:        %{_distro_sources_url}/%{full_name}-4-src.tar.gz
Patch160:       java160_build.patch
BuildRequires:  ant
BuildRequires:  ant >= 1.2
BuildRequires:  java-devel >= 1.7.0
BuildRequires:  javapackages-tools
BuildRequires:  xml-commons-apis
Requires(post): %{_sbindir}/update-alternatives
Provides:       servlet = %{version}
Obsoletes:      servlet22 < %{version}
Obsoletes:      servlet4 < %{version}
Provides:       servlet22 = %{version}
Provides:       servlet4 = %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
This subproject contains the source code for the implementation classes
of the Java Servlet and JSP APIs (packages javax.servlet).

%package javadoc
Summary:        Javadoc for servletapi4
Group:          Development/Libraries/Java

%description javadoc
This subproject contains the source code for the implementation classes
of the Java Servlet and JSP APIs (packages javax.servlet). This package
contains the javadoc documentation for the Java Servlet and JSP APIs.

%prep
%setup -q -n %{full_name}-4-src
%patch 160 -p1

%build
ant dist -Dservletapi.build=build -Dservletapi.dist=dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/lib/servlet.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/api/* %{buildroot}%{_javadocdir}/%{name}
# alternatives
mkdir -p %{buildroot}%{_sysconfdir}/alternatives/
ln -sf %{_sysconfdir}/alternatives/servlet.jar %{buildroot}%{_javadir}/servlet.jar

%post
update-alternatives --install %{_javadir}/servlet.jar servlet %{_javadir}/%{name}-%{version}.jar 40

%postun
if [ "$1" = "0" ]; then
	update-alternatives --remove servlet %{_javadir}/%{name}-%{version}.jar
fi

%files
%defattr(-,root,root)
%license LICENSE
%doc README.txt
%{_javadir}/*
%{_javadir}/servlet.jar
%ghost %{_sysconfdir}/alternatives/servlet.jar

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.0.4-302
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 4.0.4-301
- Update Source0
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.0.4-300
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Sep 18 2017 fstrba@suse.com
- Modified patch:
  * java160_build.patch
    + Don't switch off doclint; it is switched off by default
* Sun Sep 10 2017 fstrba@suse.com
- Removed patch:
  * java150_build.patch
- Added patch:
  * java160_build.patch
    + Specify java source and target level 1.6 in order to allow
    building with jdk9
    + Disable doclint, since errors of javadoc in jdk9 are fatal
* Tue Sep 29 2015 dmueller@suse.com
- build against java-1_8_0-openjdk or newer if available
* Mon Jul 21 2014 tchvatal@suse.com
- Cleanup with spec-cleaner
- Fix update-alternatives
* Fri Feb  7 2014 fcrozat@suse.com
- Fix license tag, should be Apache-1.1
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Mon Sep 25 2006 dbornkessel@suse.de
- fixes necessary to compile with Java 1.5.0
  - set source="1.4" and target="1.4" for ant "javac" tasks
  - set source="1.4" for ant "javadoc" tasks
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Sep 29 2005 dmueller@suse.de
- add norootforbuild
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 4.0.4 (JPackage 1.5)
