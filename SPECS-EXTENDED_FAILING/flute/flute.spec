Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: flute
Version: 1.3.0
Release: 24%{?dist}
Summary: Java CSS parser using SAC
# The entire source code is W3C except ParseException.java which is LGPLv2+
License: W3C and LGPLv2+
Source0: http://downloads.sourceforge.net/jfreereport/%{name}-%{version}-OOo31.zip
URL: http://www.w3.org/Style/CSS/SAC/
BuildRequires: ant, java-devel, jpackage-utils, sac
Requires: java, jpackage-utils sac
BuildArch: noarch

%description
A Cascading Style Sheets parser using the Simple API for CSS, for Java.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
find . -name "*.jar" -exec rm -f {} \;
mkdir -p lib
build-jar-repository -s -p lib sac

%build
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%license COPYRIGHT.html
%{_javadir}/*.jar

%files javadoc
%license COPYRIGHT.html
%{_javadocdir}/%{name}

%changelog
* Wed Jan 05 2022 Thomas Crain <thcrain@microsoft.com> - 1.3.0-24
- Rename java-headless dependency to java
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-22.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-21.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-20.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-19.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-18.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-17.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-16.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-15.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-14.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-13.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Caolán McNamara <caolanm@redhat.com> 1.3.0-12.OOo31
- Resolves: rhbz#1068074 Switch to java-headless (build)requires

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-11.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-10.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-9.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-8.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Caolán McNamara <caolanm@redhat.com> 1.3.0-7.OOo31
- Related: rhbz#749103 drop gcj aot

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6.OOo31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 1.3.0-5.OOo31
- add COPYRIGHT to all subpackages, sync with GCJGuidelines packaging
  guidelines

* Sun Jun 13 2010 Caolán McNamara <caolanm@redhat.com> - 1.3.0-4.OOo31
- rpmlint warnings

* Wed Jan 06 2010 Caolán McNamara <caolanm@redhat.com> - 1.3.0-3.OOo31
- ParseException.java is under LGPLv2+

* Fri Jul 24 2009 Caolán McNamara <caolanm@redhat.com> - 1.3.0-2.OOo31
- make javadoc no-arch when building as arch-dependant aot

* Sun May 03 2009 Caolán McNamara <caolanm@redhat.com> - 1.3.0-1.OOo31
- post-release tuned for OpenOffice.org report-designer

* Mon Mar 09 2009 Caolán McNamara <caolanm@redhat.com> - 1.3-5.20061107jfree
- better adherence to versioning guidelines

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 07 2007 Caolán McNamara <caolanm@redhat.com> 1.3-4
- initial import from jpackage

* Mon Aug 23 2004 Ralph Apel <r.apel at r-apel.de> 1.3-3jpp
- update for JPackage 1.5

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 1.3-2jpp
- update for JPackage 1.5

* Thu Jul 11 2002 Ville Skyttä <ville.skytta at iki.fi> 1.3-1jpp
- Update to 1.3.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Add Distribution tag, fix URL, tweak Summary and description.

* Wed Feb 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-1jpp
- first jpp release
