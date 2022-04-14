Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: sac
Version: 1.3
Release: 33%{?dist}
Summary: Java standard interface for CSS parser
License: W3C
#Original source: http://www.w3.org/2002/06/%{name}java-%{version}.zip
#unzip, find . -name "*.jar" -exec rm {} \;
#to simplify the licensing
Source0: %{name}java-%{version}-jarsdeleted.zip
Source1: %{name}-build.xml
Source2: %{name}-MANIFEST.MF
Source3: https://repo1.maven.org/maven2/org/w3c/css/sac/1.3/sac-1.3.pom
URL: http://www.w3.org/Style/CSS/SAC/

BuildRequires: ant
BuildRequires: javapackages-local

BuildArch: noarch

%description
SAC is a standard interface for CSS parsers, intended to work with CSS1, CSS2,
CSS3 and other CSS derived languages.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
install -m 644 %{SOURCE1} build.xml
find . -name "*.jar" -exec rm -f {} \;

%build
ant jar javadoc

# inject OSGi manifest
jar ufm build/lib/sac.jar %{SOURCE2}

%install
%mvn_artifact %{SOURCE3} build/lib/sac.jar
%mvn_file ":sac" sac
%mvn_install -J build/api

%files -f .mfiles
%license COPYRIGHT.html

%files javadoc -f .mfiles-javadoc
%license COPYRIGHT.html

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3-33
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-27
- Elimitate race condition when injecting JAR manifest
- Resolves: rhbz#1495242

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Mat Booth <mat.booth@redhat.com> - 1.3-25
- Spec file modernisation to fix FTBFS

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 23 2016 Sopot Cela <scela@redhat.com> - 1.3-23
- Changed broken Source3: URL

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 10 2014 David Tardon <dtardon@redhat.com> - 1.3-20
- Resolves: rhbz#1107270 fix FTBFS

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Caolán McNamara <caolanm@redhat.com> - 1.3-18
- Resolves: rhbz#1068513 switch to java-headless (build)requires

* Wed Aug 21 2013 Mat Booth <fedora@matbooth.co.uk> - 1.3-17
- Update for newer guidelines, rhbz #993211

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Caolán McNamara <caolanm@redhat.com> - 1.3-14
- repack zip to drop jars

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Caolán McNamara <caolanm@redhat.com> - 1.3-11
- Resolves: rhbz#715875 FTBFS

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 1.3-9
- Drop gcj.
- Adapt to current guidelines.

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 1.3-8
- add COPYING to all subpackages

* Mon May 31 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.3-7
- Fix spelling of my surname in %%changelog.

* Wed Mar 24 2010 Alexander Kurtakov <akurtako@redhat.com> 1.3-6
- Add maven pom and metadata.

* Fri Jul 24 2009 Caolán McNamara <caolanm@redhat.com> - 1.3-5
- make javadoc no-arch when building as arch-dependant aot

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 6 2009 Alexander Kurtakov <akurtako@redhat.com> 1.3-3.3
- Add osgi manifest (needed by eclipse-birt).

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3-3.2
- drop repotag

* Fri May 09 2008 Caolán McNamara <caolanm@redhat.com> 1.3-3jpp.1
- update for guidelines

* Sat May 03 2008 Caolán McNamara <caolanm@redhat.com> 1.3-3jpp
- import from jpackage

* Fri Sep 03 2004 Fernando Nasser <fnasser@redhat.com> 1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 1.3-2jpp
- update for JPackage 1.5

* Thu Jul 11 2002 Ville Skyttä <ville.skytta@iki.fi> 1.3-1jpp
- Update to 1.3.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Add Distribution tag, fix URL, tweak Summary and description.

* Wed Feb 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-1jpp 
- first jpp release
