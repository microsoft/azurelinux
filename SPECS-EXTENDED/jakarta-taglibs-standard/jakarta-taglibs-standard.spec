Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package jakarta-taglibs-standard
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


%define short_name      taglibs-standard
Name:           jakarta-taglibs-standard
Version:        1.1.1
Release:        261%{?dist}
Summary:        Open Source Implementation of the JSP Standard Tag Library
License:        ASL 2.0
Group:          Development/Libraries/Java
Url:            https://tomcat.apache.org/taglibs/
# Need to switch to upstream's source tarball:
# https://archive.apache.org/dist/jakarta/taglibs/standard/source/jakarta-taglibs-standard-1.1.1-src.tar.gz
Source0:        %{_distro_sources_url}/jakarta-taglibs-standard-%{version}-src.tar.bz2
Patch0:         %{name}-%{version}-build.patch
Patch1:         %{name}-java6-compatibility.patch
Patch2:         %{name}-%{version}-remove-enums.patch
Patch3:         jakarta-taglibs-standard-java7.patch
Patch4:         CVE-2015-0254.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  servletapi5
BuildRequires:  xalan-j2
Requires:       servletapi5 >= 5.0.16
Requires:       xalan-j2
BuildArch:      noarch

%description
This package contains releases for the 1.1.x versions of the Standard
Tag Library, Jakarta Taglibs's open source implementation of the JSP
Standard Tag Library (JSTL), version 1.1. JSTL is a standard under the
Java Community Process.

%package        javadoc
Summary:        Javadoc for jakarta-taglibs-standard
Group:          Development/Libraries/Java

%description    javadoc
This package contains the javadoc documentation for Jakarta Taglibs.

%prep
%setup -q -n %{name}-%{version}-src
%patch 0
%patch 1 -b .sav1
%patch 2 -b .sav2
%patch 3 -p1
%patch 4 -p1

cat > build.properties <<EOBP
build.dir=build
dist.dir=dist
servlet24.jar=$(build-classpath servletapi5)
jsp20.jar=$(build-classpath jspapi)
xalan.jar=$(build-classpath xalan-j2)
EOBP

%build
ant \
  -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -f standard/build.xml \
  dist

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p standard/dist/standard/lib/jstl.jar %{buildroot}%{_javadir}/jakarta-taglibs-core-%{version}.jar
cp -p standard/dist/standard/lib/standard.jar %{buildroot}%{_javadir}/jakarta-taglibs-standard-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr standard/dist/standard/javadoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files
%license LICENSE
%doc standard/README_src.txt standard/README_bin.txt standard/dist/doc/doc/standard-doc/*.html
%{_javadir}/*

%files javadoc
%license LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-261
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-260
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-259
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Sep 18 2017 fstrba@suse.com
- Modified patch:
  * jakarta-taglibs-standard-1.1.1-build.patch
    + Don't hardcode java source and target levels
- Specify source and target level 1.6 in order to allow building
  with jdk9
- Clean spec file and fix some rpmlint errors
* Tue Oct  6 2015 tchvatal@suse.com
- Update URL to link to live domain
- Fix bnc#920813 CVE-2015-0254, patch taken from debian:
  * CVE-2015-0254.patch
* Fri Jul 11 2014 tchvatal@suse.com
- Cleanup bit with spec-cleaner.
* Wed Jun 13 2012 mvyskocil@suse.cz
- fix build with java7
- use non-versioned javadocdir
* Tue Aug  5 2008 mvyskocil@suse.cz
- fixed build using openjdk6 (add java6 API and remove enums)
- use bzip2 in source tarball
- use macro name in patches
- use source=1.5 and target=1.5
* Sun Sep 17 2006 ro@suse.de
- fix build with java-1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jul 28 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.1.1 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Sun Sep  5 2004 skh@suse.de
- Initial package created with version 1.1.1 (JPackage 1.5)
