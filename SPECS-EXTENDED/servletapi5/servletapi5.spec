Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package servletapi5
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
Name:           servletapi5
Version:        5.0.18
Release:        290%{?dist}
Summary:        Java servlet and JSP implementation classes
License:        ASL 1.1
Group:          Development/Libraries/Java
Url:            https://jakarta.apache.org/tomcat/
Source0:        %{_distro_sources_url}/%{full_name}-5-src.tar.gz
#!BuildIgnore:  xml-commons xml-commons-resolver xerces-j2 xml-commons-apis
#!BuildIgnore:  xml-commons-jaxp-1.3-apis
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  javapackages-tools
BuildRequires:  xml-commons-apis-bootstrap
Requires(post): update-alternatives
Provides:       servlet = %{version}
Provides:       servlet24 = %{version}
Provides:       servlet5 = %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
This subproject contains the source code for the implementation classes
of the Java Servlet and JSP APIs (packages javax.servlet).

%prep
%setup -q -c -T -a 0 -n %{full_name}-5-src

%build
# Fix us a license file first
cp -f jakarta-tomcat-%{version}-src/jakarta-servletapi-5/jsr154/LICENSE .
cd jakarta-tomcat-%{version}-src/jakarta-servletapi-5
find . -type f -name "*.jar" -exec rm -f {} \;
pushd .
cd jsr154
ant jar examples -Dservletapi.build=build -Dservletapi.dist=dist -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6
popd
pushd .
cd jsr152
ant jar examples -Dservletapi.build=build -Dservletapi.dist=dist -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6
popd

%install
cd jakarta-tomcat-%{version}-src/jakarta-servletapi-5
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 jsr152/dist/lib/jsp-api.jar %{buildroot}%{_javadir}/jspapi-%{version}.jar
install -m 644 jsr154/dist/lib/servlet-api.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# alternatives
mkdir -p %{buildroot}%{_sysconfdir}/alternatives/
ln -sf %{_sysconfdir}/alternatives/servlet.jar %{buildroot}%{_javadir}/servlet.jar

%post
update-alternatives --install %{_javadir}/servlet.jar servlet %{_javadir}/%{name}-%{version}.jar 50

%postun
if [ "$1" = "0" ]; then
    update-alternatives --remove servlet %{_javadir}/%{name}-%{version}.jar
fi

%files
%defattr(-,root,root)
%license LICENSE
%{_javadir}/*
%{_javadir}/servlet.jar
%ghost %{_sysconfdir}/alternatives/servlet.jar

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0.18-290
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 5.0.18-289
- Update Source0
- License verified.

* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0.18-288
- Adding BR on "javapackages-tools" to provide missing "%%{_javadir}" macro.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0.18-287
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Oct  3 2017 fstrba@suse.com
- Removed patch:
  * java150_build.patch
  - Don't hardcode the source and target levels, specify them on
    command line instead
- Don't build with java-1_5_0-gcj-compat, since it is bound to go
- Specify source and target level 1.6 in order to allow building
  with jdk9
* Mon Jul 21 2014 tchvatal@suse.com
- Cleanup with spec-cleaner.
- Fix update-alternatives code
* Fri Aug 23 2013 mvyskocil@suse.com
- drop javadoc package
* Mon Nov  8 2010 mvyskocil@suse.cz
- Build ignore xml-commons-1.3-jaxp-apis
* Mon Jul 28 2008 coolo@suse.de
- yet another package to ignore
* Mon Jul 28 2008 coolo@suse.de
- build without openjdk to avoid cycle
* Mon Sep 25 2006 dbornkessel@suse.de
- java150 fixes: added target="1.4" and source="1.4"
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Sep 28 2005 dmueller@suse.de
- add norootforbuild
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 5.0.18 (JPackage 1.5)
