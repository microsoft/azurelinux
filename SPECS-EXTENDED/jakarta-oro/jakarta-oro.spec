Vendor:         Microsoft Corporation
Distribution:   Mariner
# Copyright (c) 2000-2005, JPackage Project
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

%global base_name oro

Name:           jakarta-oro
Version:        2.0.8
Release:        30%{?dist}
Summary:        Full regular expressions API
License:        ASL 1.1
Source0:        http://archive.apache.org/dist/jakarta/oro/%{name}-%{version}.tar.gz
Source1:        MANIFEST.MF
Source2:        http://repo1.maven.org/maven2/%{base_name}/%{base_name}/%{version}/%{base_name}-%{version}.pom
Patch1:         %{name}-build-xml.patch
URL:            http://jakarta.apache.org/oro

BuildRequires:  javapackages-local
BuildRequires:  ant

BuildArch:      noarch

Provides:       deprecated()

%description
The Jakarta-ORO Java classes are a set of text-processing Java classes
that provide Perl5 compatible regular expressions, AWK-like regular
expressions, glob expressions, and utility classes for performing
substitutions, splits, filtering filenames, etc. This library is the
successor to the OROMatcher, AwkTools, PerlTools, and TextTools
libraries from ORO, Inc. (www.oroinc.com). 

%package javadoc
Summary:        Javadoc for %{name}
Provides:       deprecated()

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# remove all CVS files
for dir in `find . -type d -name CVS`; do rm -rf $dir; done
for file in `find . -type f -name .cvsignore`; do rm -rf $file; done

%patch1
cp %{SOURCE1} .

%build
ant -Dfinal.name=%{base_name} jar javadocs

%install
%mvn_file : %{name} %{base_name}
%mvn_artifact %{SOURCE2} %{base_name}.jar

%mvn_install -J docs/api

%files -f .mfiles
%doc COMPILE ISSUES README TODO CHANGES CONTRIBUTORS STYLE
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.0.8-30
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0:2.0.8-29
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0.8-25
- Mark package as deprecated

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Michael Simacek <msimacek@redhat.com> - 0:2.0.8-21
- Install with XMvn

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0.8-18
- Add build-requires on javapackages-local

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0.8-16
- Remove rpm bug workaround

* Fri Jun 27 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0:2.0.8-16
- Update for latest Java packaging guidelines (#1106816)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0.8-12
- Add maven POM

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 21 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.0.8-9
- Fix merge review comments.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.0.8-7
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-6.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Jeff Johnston <jjohnstn@redhat.com> - 0:2.0.8-5.3
- Add OSGi metadata to Manifest.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.0.8-4.2
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.0.8-4jpp.1
- Autorebuild for GCC 4.3

* Mon Aug 21 2006 Fernando Nasser <fnasser.redhat.com> 2.0.8-3jpp.1
- Merge with upstream

* Mon Aug 21 2006 Fernando Nasser <fnasser.redhat.com> 2.0.8-3jpp
- Add AOT bits
- Fix javadoc unversioned link handling
- Add requires for post/postun javadoc sections added above

* Tue Aug 24 2004 Fernando Nasser <fnasser.redhat.com> 2.0.8-2jpp
- Rebuild with Ant 1.6.2
- Changed name to jakarta-oro
- Add backward compatibility to 'oro' bits

* Fri Jan 02 2004 Henri Gomez <hgomez@users.sourceforge.net> 2.0.8-1jpp
- oro 2.0.8

* Tue Mar 25 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 2.0.7-1jpp
- oro 2.0.7
- for jpackage-utils 1.5

* Wed Jul 10 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.0.6-1jpp
- oro 2.0.6

* Tue Jul 02 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-7jpp
- section macro
- use sed instead of bash 2.x extension in link area to make spec compatible with distro using bash 1.1x

* Fri Jan 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-6jpp 
- versioned dir for javadoc
- no dependencies javadoc package

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-5jpp
- javadoc in javadoc package
- official summary

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 2.0.4-4jpp
- removed packager tag
- new jpp extension

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-3jpp
- more macros

* Wed Sep 26 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-2jpp
- first unified release
- s/jPackage/JPackage

* Sun Aug 26 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-1mdk
- 2.0.4
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- used new source packaging policy

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.0.1-3mdk
- spec cleanup
- changelog correction

* Sun Feb 04 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.0.1-2mdk
- merged with Henri Gomez <hgomez@users.sourceforge.net> specs:
- changed name to oro
-  changed javadir to /usr/share/java
-  dropped jdk & jre requirement
-  added Jikes support
- changed jar name to oro.jar
- corrected doc
- more macros

* Sun Jan 14 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.0.1-1mdk
- first Mandrake release
