Name:           bcel
Version:        6.8.1
Release:        3%{?dist}
Summary:        Byte Code Engineering Library
License:        Apache-2.0
URL:            http://commons.apache.org/proper/commons-bcel/
BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch

Source0:        http://archive.apache.org/dist/commons/bcel/source/bcel-%{version}-src.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

%description
The Byte Code Engineering Library (formerly known as JavaClass) is
intended to give users a convenient possibility to analyze, create, and
manipulate (binary) Java class files (those ending with .class). Classes
are represented by objects which contain all the symbolic information of
the given class: methods, fields and byte code instructions, in
particular.  Such objects can be read from an existing file, be
transformed by a program (e.g. a class loader at run-time) and dumped to
a file again. An even more interesting application is the creation of
classes from scratch at run-time. The Byte Code Engineering Library
(BCEL) may be also useful if you want to learn about the Java Virtual
Machine (JVM) and the format of Java .class files.  BCEL is already
being used successfully in several projects such as compilers,
optimizers, obsfuscators and analysis tools, the most popular probably
being the Xalan XSLT processor at Apache.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{name}-%{version}-src

%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :spotbugs-maven-plugin
%pom_remove_plugin :jacoco-maven-plugin

%mvn_alias : bcel: apache:
%mvn_file : %{name}

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 6.8.1-2
- Rebuilt for java-21-openjdk as system jdk

* Thu Feb 01 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.1-1
- Update to upstream version 6.8.1

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Marian Koncek <mkoncek@redhat.com> - 6.8.0-1
- Update to upstream version 6.8.0

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.7.0-3
- Convert License tag to SPDX format

* Fri Aug 18 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.7.0-2
- Add missing build-requires

* Fri Aug 18 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.7.0-1
- Update to upstream version 6.7.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.5.0-3
- Fix arbitrary bytecode produced via out-of-bounds writing
- Resolves: CVE-2022-42920

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 24 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.5.0-1
- Update to upstream version 6.5.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 6.4.1-9
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.4.1-6
- Remove dependency on jna

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:6.4.1-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.4.1-2
- Mass rebuild for javapackages-tools 201902

* Wed Oct 16 2019 Marian Koncek <mkoncek@redhat.com> - 6.4.1-1
- Update to upstream version 6.4.1

* Fri Oct 04 2019 Fabio Valentini <decathorpe@gmail.com> - 0:6.4.1-1
- Update to version 6.4.1.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-2
- Mass rebuild for javapackages-tools 201901

* Mon May 06 2019 Marian Koncek <mkoncek@redhat.com> - 0:6.3.1-1
- Update to upstream version 6.3.1
- Fixes: RHBZ #1692150

* Tue Feb 05 2019 Marian Koncek <mkoncek@redhat.com> - 0:6.3-1
- Update to upstream version 6.3
- Fixes: RHBZ #1670025

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Michael Simacek <msimacek@redhat.com> - 0:6.2-1
- Update to upstream version 6.2

* Fri Sep 22 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:6.1-2
- Conditionally build without jna

* Tue Sep 19 2017 Michael Simacek <msimacek@redhat.com> - 0:6.1-1
- Update to upstream version 6.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.0-0.7.20140406svn1592769
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.0-0.6.20140406svn1592769
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.0-0.5.20140406svn1592769
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:6.0-0.4.20140406svn1592769
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:6.0-0.3.20140406svn1592769
- Add alias for apache:bcel

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:6.0-0.2.20140406svn1592769
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Michael Simacek <msimacek@redhat.com> - 0:6.0-0.1.20140406svn1592769
- Update to upstream snapshot compatible with Java 8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:5.2-16
- Complete spec file rewrite
- Build with Maven instead of Ant
- Remove manual subpackage

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Tom Callaway <spot@fedoraproject.org> - 0:5.2-14
- Package NOTICE.txt

* Tue Aug 21 2012 Andy Grimm <agrimm@gmail.com> - 0:5.2-13
- This package should not own _mavendepmapfragdir (RHBZ#850005)
- Build with maven, and clean up deprecated spec constructs
- Fix pom file (See http://jira.codehaus.org/browse/MEV-592)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Gerard Ryan <galileo@fedoraproject.org> - 0:5.2-11
- Inject OSGI Manifest.

* Wed Jan 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 0:5.2-10
- Specify explicit source encoding to fix build with Java 7.
- Install jar and javadocs unversioned.
- Crosslink with JDK javadocs.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.2-8
- Use global.
- Drop gcj_support.
- Fix groups.
- Fix build.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.2-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.2-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 04 2008 Permaine Cheung <pcheung at redhat.com> 0:5.2-5.1
- Do not install poms in /usr/share/maven2/default_poms

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:5.2-5
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:5.2-4jpp.2
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Permaine Cheung <pcheung at redhat.com> 0:5.2-3jpp.1
- Merge with upstream

* Mon Jan 07 2008 Permaine Cheung <pcheung at redhat.com> 0:5.2-2jpp.2
- Fixed unowned directory (Bugzilla 246185)

* Fri Nov 16 2007 Ralph Apel <r.apel@r-apel.de> 0:5.2-3jpp
- Install poms unconditionally
- Add pom in ./maven2/default_poms
- Add org.apache.bcel:bcel depmap frag

* Wed Sep 19 2007 Permaine Cheung <pcheung at redhat.com> 0:5.2-2jpp.1
- Update to 5.2 in Fedora

* Mon Sep  4 2007 Jason Corley <jason.corley@gmail.com> 0:5.2-2jpp
- use official 5.2 release tarballs and location
- change vendor and distribution to macros
- add missing requires on and maven-plugin-test, maven-plugins-base, and
  maven-plugin-xdoc 
- macro bracket fixes
- remove demo subpackage (examples are not included in the distribution tarball)
- build in mock

* Wed Jun 27 2007 Ralph Apel <r.apel@r-apel.de> 0:5.2-1jpp
- Upgrade to 5.2
- Drop bootstrap option: not necessary any more
- Add pom and depmap frags

* Fri Feb 09 2007 Ralph Apel <r.apel@r-apel.de> 0:5.1-10jpp
- Fix empty-%%post and empty-%%postun
- Fix no-cleaning-of-buildroot

* Fri Feb 09 2007 Ralph Apel <r.apel@r-apel.de> 0:5.1-9jpp
- Optionally build without maven
- Add bootstrap option

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> 0:5.1-8jpp
- Add missing requires for Javadoc task

* Sun Jul 23 2006 Matt Wringe <mwringe at redhat.com> 0:5.1-7jpp
- Add conditional native compilation
- Change spec file encoding from ISO-8859-1 to UTF-8
- Add missing BR werken.xpath and ant-apache-regexp

* Tue Apr 11 2006 Ralph Apel <r.apel@r-apel.de> 0:5.1-6jpp
- First JPP-1.7 release
- Use tidyed sources from svn
- Add resources to build the manual
- Add examples to -demo subpackage
- Build with maven by default
- Add option to build with straight ant

* Fri Nov 19 2004 David Walluck <david@jpackage.org> 0:5.1-5jpp
- rebuild to fix packager

* Sat Nov 06 2004 David Walluck <david@jpackage.org> 0:5.1-4jpp
- rebuild with javac 1.4.2

* Sat Oct 16 2004 David Walluck <david@jpackage.org> 0:5.1-3jpp
- rebuild for JPackage 1.6

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> 0:5.1-2jpp
- Build with ant-1.6.2

* Sun May 11 2003 David Walluck <david@anti-microsoft.org> 0:5.1-1jpp
- 5.1
- update for JPackage 1.5

* Mon Mar 24 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> - 5.0-6jpp
- For jpackage-utils 1.5

* Tue Feb 25 2003 Ville Skyttä <ville.skytta@iki.fi> - 5.0-5jpp
- Rebuild to get docdir right on modern distros.
- Fix License tag and source file perms.
- Built with IBM's 1.3.1SR3 (doesn't build with Sun's 1.4.1_01).

* Tue Jun 11 2002 Henri Gomez <hgomez@slib.fr> 5.0-4jpp
- use sed instead of bash 2.x extension in link area to make spec compatible
  with distro using bash 1.1x

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 5.0-3jpp 
- vendor, distribution, group tags

* Wed Jan 23 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 5.0-2jpp 
- section macro
- no dependencies for manual and javadoc package

* Tue Jan 22 2002 Henri Gomez <hgomez@slib.fr> 5.0-1jpp
- bcel is now a jakarta apache project
- dependency on jakarta-regexp instead of gnu.regexp 
- created manual package

* Sat Dec 8 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.4.1-2jpp
- javadoc into javadoc package
- Requires: and BuildRequires: gnu.regexp

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 4.4.1-1jpp
- removed packager tag
- new jpp extension
- 4.4.1

* Thu Oct 11 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.4.0-2jpp
- first unified release
- used lower case for name
- used original tarball
- s/jPackage/JPackage

* Mon Aug 27 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.4.0-1mdk
- first Mandrake release
