Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:        Web Services Description Language Toolkit for Java
Name:           wsdl4j
Version:        1.6.3
Release:        18%{?dist}
License:        CPL
URL:            http://sourceforge.net/projects/wsdl4j
BuildArch:      noarch

Source0:        http://downloads.sourceforge.net/project/wsdl4j/WSDL4J/%{version}/wsdl4j-src-%{version}.zip
Source1:        %{name}-MANIFEST.MF
Source2:        http://repo1.maven.org/maven2/wsdl4j/wsdl4j/%{version}/wsdl4j-%{version}.pom

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  javapackages-local

Provides:       javax.wsdl

%description
The Web Services Description Language for Java Toolkit (WSDL4J) allows the
creation, representation, and manipulation of WSDL documents describing
services.  This code base will eventually serve as a reference implementation
of the standard created by JSR110.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-1_6_3

%mvn_file ":{*}" @1

%build
ant compile javadocs
# inject OSGi manifests
jar ufm build/lib/%{name}.jar %{SOURCE1}

%install
%mvn_artifact %{SOURCE2} build/lib/%{name}.jar
%mvn_artifact %{name}:qname:%{version} build/lib/qname.jar
%mvn_install -J build/javadocs

install -d -m 755 %{buildroot}%{_javadir}/javax.wsdl/
ln -sf ../%{name}.jar %{buildroot}%{_javadir}/javax.wsdl/
ln -sf ../qname.jar %{buildroot}%{_javadir}/javax.wsdl/

%files -f .mfiles
%license license.html
%{_javadir}/javax.wsdl/

%files javadoc -f .mfiles-javadoc
%license license.html

%changelog
* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 1.6.3-18
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0:1.6.3-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6.3-11
- Elimitate race condition when injecting JAR manifest
- Resolves: rhbz#1495240

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6.3-7
- Update to current packaging guidelines

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.3-4
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.3-3
- Add javax.wsdl provides and directory

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.6.3-1
- Update to latest upstream version rhbz #915252.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.2-6
- Do not include versioned javadoc.

* Fri Jun 15 2012 Gerard Ryan <galileo@fedoraproject.org> - 0:1.6.2-5
- Fix file encoding for wsdl4j-MANIFEST.MF
- Update Bundle-Version in OSGi manifest
- Fix installation of jars in specfile
- Clean up specfile - remove javadoc dir version; remove clean section

* Thu Feb 16 2012 Andy Grimm <agrimm@gmail.com> - 0:1.6.2-4
- add POM file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 4 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.2-1
- Update to 1.6.2.
- Cleanups to comply with current guidelines more.

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.2-8
- Drop gcj support.
- Fix groups.

* Mon May 31 2010 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.2-7.7
- Fix specfile encoding.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-7.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-6.6
- Update OSGi manifest

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-6.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.2-5.5
- Add osgi manifest for eclipse-dtp.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-5.4
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-5jpp.3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.5.2-5jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> 1.5.2-4jpp.2
- Rebuild for ppc32 execmem issue and new build-id
- Add %%{?dist} as per new policy

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> 1.5.2-4jpp.1
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.5.2-3jpp_2fc
- Rebuilt

* Wed Jul 19 2006 Deepak Bhole <dbhole@redhat.com> 0:1.5.2-3jpp_1fc
- Remove name/release/version defines as applicable.

* Tue Jul 18 2006 Deepak Bhole <dbhole@redhat.com> 0:1.5.2-2jpp
- Merge changes from fc.
- Add conditional native compilation.

* Mon Jan 30 2006 Ralph Apel <r.apel at r-apel.de> 0:1.5.2-1jpp
- update to 1.5.2
- move qname*.jar to %%{_javadir}/wsdl4j/qname*.jar
  to make place for qname provided by geronimo-specs

* Thu Jun 02 2005 Fernando Nasser <fnasser@redhat.com> 0:1.5.1-1jpp
- update to 1.5.1

* Fri Mar 11 2005 Ralph Apel <r.apel at r-apel.de> 0:1.5-1jpp
- update to 1.5

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-3jpp
- Build with ant-1.6.2

* Thu Jun 26 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.4-2jpp
- Do not drop qname.jar

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.4-1jpp
- 1.4
- update for JPackage 1.5

* Sat Sep  7 2002 Ville Skyttä <ville.skytta@iki.fi> 1.1-1jpp
- First JPackage release.
