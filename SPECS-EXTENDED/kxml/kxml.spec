Vendor:         Microsoft Corporation
Distribution:   Mariner
# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           kxml
Version:        2.3.0
Release:        22%{?dist}
Summary:        Small XML pull parser
License:        MIT
URL:            http://kxml.sourceforge.net/
# ./create-tarball %%{version}
Source0:        %{name}-%{version}-clean.tar.gz
Source1:        http://repo1.maven.org/maven2/net/sf/kxml/kxml2/%{version}/kxml2-%{version}.pom
Source2:        http://repo1.maven.org/maven2/net/sf/kxml/kxml2-min/%{version}/kxml2-min-%{version}.pom
Source3:        %{name}-%{version}-OSGI-MANIFEST.MF

Patch0:         0001-Unbundle-xpp3-classes.patch

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  xpp3 >= 1.1.3.1
Requires:       xpp3 >= 1.1.3.1

BuildArch:      noarch

%description
kXML is a small XML pull parser, specially designed for constrained
environments such as Applets, Personal Java or MIDP devices.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0 -p1

%build
export OPT_JAR_LIST=xpp3
ant

jar ufm dist/%{name}2-%{version}.jar %{SOURCE3}

%mvn_artifact %{SOURCE1} dist/%{name}2-%{version}.jar
%mvn_artifact %{SOURCE2} dist/%{name}2-min-%{version}.jar

# Compat symlinks
%mvn_file :kxml2 kxml/kxml2 kxml
%mvn_file :kxml2-min kxml/kxml2-min kxml-min

%install
%mvn_install -J www/kxml2/javadoc

%files -f .mfiles
%license license.txt

%files javadoc -f .mfiles-javadoc
%license license.txt

%changelog
* Wed Nov 03 2021 Muhammad Falak <mwani@microsft.com> - 2.3.0-22
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.0-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-15
- Elimitate race condition when injecting JAR manifest
- Resolves: rhbz#1495232

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Mat Booth <mat.booth@redhat.com> - 2.3.0-13
- Install with xmvn

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 23 2016 Severin Gehwolf <sgehwolf@redhat.com> - 2.3.0-11
- Fix OSGi metadata after RHBZ#1299774.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-9
- Unbundle xpp3 classes
- Resolves: rhbz#1299774

* Tue Jun 16 2015 Jie Kang <jkang@redhat.com> - 2.3.0-8
- Add OSGi metadata.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-6
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.0-5
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Michal Srb <msrb@redhat.com> - 2.3.0-4
- Install POM+depmap for net.sf.kxml:kxml2-min

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Michal Srb <msrb@redhat.com> - 2.3.0-2
- Clean up tarball
- Drop group tag
- Fix R

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-1
- Update to upstream version 2.3.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.2-11
- Fix license tag
- Add missing Requires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-9
- Adapt to current guidelines.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 9 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> 2.2.2-7
- Fix pom dependency from xmlpull to xpp3

* Wed Dec 8 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-6
- Remove versioned jar and javadoc.
- Fix pom name.

* Thu Sep 3 2009 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-5
- Fix Summary and description.
- Fix line length.
- Use pom from the URL.

* Thu Sep 3 2009 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-4
- Adapt for Fedora.

* Mon Dec 08 2008 Will Tatam <will.tatam@red61.com> 2.2.2-3
- Auto rebuild for JPackage 5 in mock

* Wed May 07 2008 Ralph Apel <r.apel@r-apel.de> 0:2.2.2-2jpp
- Add xpp3 (B)R

* Wed May 07 2008 Ralph Apel <r.apel@r-apel.de> 0:2.2.2-1jpp
- 2.2.2

* Thu Aug 26 2004 Fernando Nasser <fnasser@redhat.com> 0:2.1.8-4jpp
- Pro-forma rebuild with Ant 1.6.2

* Mon Jan 26 2004 David Walluck <david@anti-microsoft.org> 0:2.1.8-3jpp
- remove fractal reference

* Sun Jan 25 2004 David Walluck <david@anti-microsoft.org> 0:2.1.8-2jpp
- fix license

* Sun Jan 25 2004 David Walluck <david@anti-microsoft.org> 0:2.1.8-1jpp
- release
