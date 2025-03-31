%define __requires_exclude system.bundle

Name:          xerces-j2
Version:       2.12.2
Release:       12%{?dist}
Summary:       Java XML parser
# Most of the source is ASL 2.0
# W3C licensed files:
# src/org/apache/xerces/dom3/as
# src/org/w3c/dom/html/HTMLDOMImplementation.java
License:       Apache-2.0 AND W3C
URL:           http://xerces.apache.org/xerces2-j/

%global cvs_version %(tr . _ <<< %{version})

Source0:       http://mirror.ox.ac.uk/sites/rsync.apache.org/xerces/j/source/Xerces-J-src.%{version}.tar.gz
Source11:      %{name}-version.1
Source12:      %{name}-constants.1

# Custom javac ant task used by the build
Source3:       https://svn.apache.org/repos/asf/xerces/java/tags/Xerces-J_%{cvs_version}/tools/src/XJavac.java

# Custom doclet tags used in javadocs
Source5:       https://svn.apache.org/repos/asf/xerces/java/tags/Xerces-J_%{cvs_version}/tools/src/ExperimentalTaglet.java
Source6:       https://svn.apache.org/repos/asf/xerces/java/tags/Xerces-J_%{cvs_version}/tools/src/InternalTaglet.java

Source7:       %{name}-pom.xml

# Patch the build so that it doesn't try to use bundled xml-commons source
Patch0:        %{name}-build.patch

# Patch the manifest so that it includes OSGi stuff
Patch1:        %{name}-manifest.patch

BuildArch:     noarch
#ExclusiveArch: %{java_arches} noarch

BuildRequires: javapackages-local
BuildRequires: ant
BuildRequires: apache-parent
BuildRequires: xml-commons-apis >= 1.4.01
BuildRequires: xml-commons-resolver >= 1.2
BuildRequires: java-devel

Requires:      xml-commons-apis >= 1.4.01
Requires:      xml-commons-resolver >= 1.2
# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:      javapackages-tools

Provides:      jaxp_parser_impl = 1.4
Provides:      %{name}-scripts = %{version}-%{release}

%description
Welcome to the future! Xerces2 is the next generation of high performance,
fully compliant XML parsers in the Apache Xerces family. This new version of
Xerces introduces the Xerces Native Interface (XNI), a complete framework for
building parser components and configurations that is extremely modular and
easy to program.

The Apache Xerces2 parser is the reference implementation of XNI but other
parser components, configurations, and parsers can be written using the Xerces
Native Interface. For complete design and implementation documents, refer to
the XNI Manual.

Xerces2 is a fully conforming XML Schema processor. For more information,
refer to the XML Schema page.

Xerces2 also provides a complete implementation of the Document Object Model
Level 3 Core and Load/Save W3C Recommendations and provides a complete
implementation of the XML Inclusions (XInclude) W3C Recommendation. It also
provides support for OASIS XML Catalogs v1.1.

Xerces2 is able to parse documents written according to the XML 1.1
Recommendation, except that it does not yet provide an option to enable
normalization checking as described in section 2.13 of this specification. It
also handles name spaces according to the XML Namespaces 1.1 Recommendation,
and will correctly serialize XML 1.1 documents if the DOM level 3 load/save
APIs are in use.

%package        javadoc
Summary:        Javadocs for %{name}

%description    javadoc
This package contains the API documentation for %{name}.

%package        demo
Summary:        Demonstrations and samples for %{name}
Requires:       %{name} = %{version}-%{release}

%description    demo
%{summary}.

%prep
%setup -q -n xerces-%{cvs_version}
%patch 0 -p0
%patch 1 -p0

# Copy the custom ant task into place
mkdir -p tools/org/apache/xerces/util
mkdir -p tools/bin
cp -a %{SOURCE3} %{SOURCE5} %{SOURCE6} tools/org/apache/xerces/util

# Make sure upstream hasn't sneaked in any jars we don't know about
find . \( -name '*.class' -o -name '*.jar' \) -delete

sed -i 's/\r//' LICENSE README NOTICE

# Disable javadoc linting
sed -i -e "s|additionalparam='|additionalparam='-Xdoclint:none |" build.xml

# legacy aliases for compatability
%mvn_alias : xerces:xerces xerces:xmlParserAPIs apache:xerces-j2
%mvn_file : %{name} jaxp_parser_impl

%build
pushd tools

# Build custom ant tasks
%javac -classpath $(build-classpath ant) org/apache/xerces/util/XJavac.java
%jar cf bin/xjavac.jar org/apache/xerces/util/XJavac.class

%jar cmf /dev/null serializer.jar
ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
ln -sf $(build-classpath xml-commons-resolver) resolver.jar
popd

# Build everything
export ANT_OPTS="-Xmx512m -Djava.awt.headless=true -Dbuild.sysclasspath=first -Ddisconnected=true"
%ant -Djavac.source=1.8 -Djavac.target=1.8 \
    -Dbuild.compiler=modern \
    clean jars javadocs

%mvn_artifact %{SOURCE7} build/xercesImpl.jar

%install
%mvn_install

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
mkdir -p %{buildroot}%{_javadocdir}/%{name}/impl
mkdir -p %{buildroot}%{_javadocdir}/%{name}/xs
mkdir -p %{buildroot}%{_javadocdir}/%{name}/xni
mkdir -p %{buildroot}%{_javadocdir}/%{name}/other

cp -pr build/docs/javadocs/xerces2/* %{buildroot}%{_javadocdir}/%{name}/impl
cp -pr build/docs/javadocs/xs/* %{buildroot}%{_javadocdir}/%{name}/xs
cp -pr build/docs/javadocs/xni/* %{buildroot}%{_javadocdir}/%{name}/xni
cp -pr build/docs/javadocs/other/* %{buildroot}%{_javadocdir}/%{name}/other

# scripts
%jpackage_script org.apache.xerces.impl.Version "" "" %{name} %{name}-version 1
%jpackage_script org.apache.xerces.impl.Constants "" "" %{name} %{name}-constants 1

# manual pages
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE11} %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE12} %{buildroot}%{_mandir}/man1

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/
install -p -m 644 build/xercesSamples.jar %{buildroot}%{_datadir}/%{name}/%{name}-samples.jar
cp -pr data %{buildroot}%{_datadir}/%{name}

%post
# alternatives support removed in f26
update-alternatives --remove jaxp_parser_impl %{_javadir}/%{name}.jar >/dev/null 2>&1 || :
# it deletes the link, set it up again
ln -sf %{name}.jar %{_javadir}/jaxp_parser_impl.jar

%files -f .mfiles
%doc LICENSE NOTICE README
%{_bindir}/*
%{_mandir}/*/*

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}

%changelog
* Mon Jul 22 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12.2-12
- Fix incorrect permissions of xerces-j2-samples.jar

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12.2-10
- Switch to a newer patch macro syntax

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.12.2-9
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12.2-7
- Convert License tag to SPDX format

* Mon Aug 14 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.12.2-6
- Build with default Java

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Apr 27 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12.2-2
- Workaround build issue with RPM 4.18

* Thu Apr 21 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12.2-1
- Update to upstream version 2.12.2
- Resolves: CVE-2022-23437

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.12.1-7
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12.1-4
- Remove dependency on xalan-j2

* Fri Mar 12 2021 Mat Booth <mat.booth@redhat.com> - 2.12.1-3
- Update OSGi metadata, use import-package instead of require-bundle
  in order to avoid some tricky OSGi breakage on Java 11

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 14 2020 Jerry James <loganjerry@gmail.com> - 2.12.1-1
- Version 2.12.1
- Drop upstreamed getcontentdocument patch
- Drop no longer used taglet sources
- Verify the source tarball
- Compute cvs_version so it doesn't have to be updated in sync with Version
- Build with JDK 11
- Generate the scripts with jpackage_script

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Mat Booth <mat.booth@redhat.com> - 2.12.0-8
- Peg to Java 8 due to use of 'com.sun.tools.doclets.Taglet' that was removed in
  Java 11

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2.12.0-7
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jun 24 2020 Mat Booth <mat.booth@redhat.com> - 2.12.0-6
- Turn off javadoc linting

* Wed Jun 24 2020 Jeff Johnston <jjohnstn@redhat.com> - 2.12.0-5
- Change to build using Java 11
- Fix some impl classes that require getContentDocument() method
- Add a patch-module option for Javadoc generation

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Marian Koncek <mkoncek@redhat.com> - 2.12.0-1
- Update to upstream version 2.12.0

* Fri Aug 03 2018 Michael Simacek <msimacek@redhat.com> - 2.11.0-34
- Fix license tag to include W3C

* Wed Aug 01 2018 Severin Gehwolf <sgehwolf@redhat.com> - 2.11.0-33
- Add requirement on javapackages-tools since scripts use
  java-functions.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.0-30
- Remove unneeded dependency on dejavu-sans-fonts

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 08 2017 Michael Simacek <msimacek@redhat.com> - 2.11.0-28
- Fix missing jaxp_parser_impl symlink after upgrade

* Thu Feb 23 2017 Michael Simacek <msimacek@redhat.com> - 2.11.0-27
- Remove alternatives, there is no other provider
- Specfile cleanup

* Thu Feb 23 2017 Michael Simacek <msimacek@redhat.com> - 2.11.0-26
- Install with XMvn

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 10 2014 Mat Booth <mat.booth@redhat.com> - 2.11.0-22
- Add patch for CVE-2013-4002, rhbz #1140031
- Fix ownership of javadoc directory

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.0-21
- Workaround regression in %%add_maven_depmap -a parameter handling

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.0-20
- Add alias for apache:xerces-j2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.0-18
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.11.0-17
- Use Requires: java-headless rebuild (#1067528)

* Tue Aug 6 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.11.0-16
- Fix FTBFS.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.11.0-13
- Add reexoport to javax.xml.

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.0-13
- Add manual pages

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Alexander Kurtakov <akurtako@redhat.com> 2.11.0-11
- Really restore dependencies.

* Tue Dec 11 2012 Krzysztof Daniel <kdaniel@redhat.com> 2.11.0-10
- Restored dependencies to system.bundle and javax.xml.

* Tue Sep 25 2012 Krzysztof Daniel <kdaniel@redhat.com> 2.11.0-9
- Remove javax.xml from required bundles. They are provided by JVM.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Krzysztof Daniel <kdaniel@redhat.com> 2.11.0-7
- Updated OSGi MANIFEST.MF to import javax.xml

* Thu Mar 08 2012 Andrew Overholt <overholt@redhat.com> - 2.11.0-6
- Remove system.bundle OSGi requirement from MANIFEST.MF
- Fold -scripts sub-package into main

* Tue Mar 06 2012 Marek Goldmann <mgoldman@redhat.com> - 2.11.0-5
- Use non-versioned jar name, RHBZ#800463
- Cleanup in spec file to follow new guidelines
- Consolidated javadocs packages
- Removed manual subpackage because of stylebook issues, see comment on obsolete

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Mat Booth <fedora@matbooth.co.uk> 2.11.0-2
- Install maven pom and depmap.

* Sat Dec 11 2010 Mat Booth <fedora@matbooth.co.uk> - 2.11.0-1
- Update to latest upstream version.
- Provide JAXP 1.4.
- Fix some minor rpmlint warnings.
- Add dep on xalan-j2.
- Fix javadoc taglets.

* Sat Jun 12 2010 Mat Booth <fedora@matbooth.co.uk> - 2.9.0-4
- Fix broken links in manual and fix javadoc requires.
- Build 1.5 bytecode instead of 1.6, for compatibility.

* Fri Jan 22 2010 Andrew Overholt <overholt@redhat.com> - 2.9.0-3
- Fix unversioned Provides for jaxp_parser_impl (make it 1.3).

* Thu Jan 14 2010 Mat Booth <fedora@matbooth.co.uk> - 2.9.0-2
- Add a build dep on a font package because the JDK is missing a dependency
  to function correctly in headless mode. See RHBZ #478480 and #521523.
- Fix groups.

* Tue Jan 5 2010 Mat Booth <fedora@matbooth.co.uk> - 2.9.0-1
- Update to 2.9.0: This is the version Eclipse expects, previously the OSGi
  manifest was lying about its version :-o
- Enable manual sub-package now xml-stylebook is in Fedora.
- Drop GCJ support.
- Minor changes to spec to make it more conforming to the guidelines.
- Drop the libgcj patch, we don't seem to need it anymore.
- Add the OSGi manifest as part of the build instead of the install.
- Fix packaging bug RHBZ #472646.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7.1-12.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7.1-11.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-10.3
- Add osgi manifest.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.7.1-10.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.7.1-10jpp.1
- Autorebuild for GCC 4.3

* Wed Mar 28 2007 Matt Wringe <mwringe@redhat.com> 0:2.7.1-9jpp.1
- Update with newest jpp version
- Clean up spec file for Fedora Review

* Sun Aug 13 2006 Warren Togami <wtogami@redhat.com> 0:2.7.1-7jpp.2
- fix typo in preun req

* Sat Aug 12 2006 Matt Wringe <mwringe at redhat.com> 0:2.7.1-7jpp.1
- Merge with upstream version

* Sat Aug 12 2006 Matt Wringe <mwringe at redhat.com> 0:2.7.1-7jpp
- Add conditional native compiling
- Add missing requires for javadocs
- Add missing requires for post and preun
- Update version to 7jpp at Fedora's request

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:2.7.1-6jpp_9fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:2.7.1-6jpp_8fc
- rebuild

* Thu Mar 30 2006 Fernando Nasser <fnasser@redhat.com> 0:2.7.1-3jpp
- Add missing BR for xml-stylebook

* Wed Mar 22 2006 Ralph Apel <r.apel at r-apel.de> 0:2.7.1-2jpp
- First JPP-1.7 release
- use tools subdir and give it as java.endorsed.dirs (for java-1.4.2-bea e.g.)

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:2.7.1-6jpp_7fc
- stop scriptlet spew

* Wed Feb 22 2006 Rafael Schloming <rafaels@redhat.com> - 0:2.7.1-6jpp_6fc
- Updated to 2.7.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:2.6.2-6jpp_5fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:2.6.2-6jpp_4fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Archit Shah <ashah@redhat.com> 0:2.6.2-6jpp_3fc
- build xerces without using native code

* Mon Jan  9 2006 Archit Shah <ashah@redhat.com> 0:2.6.2-6jpp_2fc
- rebuilt for new gcj

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:2.6.2-6jpp_1fc
- rebuilt for new gcj

* Tue Dec 13 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Oct 07 2005 Ralph Apel <r.apel at r-apel.de> 0:2.7.1-1jpp
- Upgrade to 2.7.1

* Thu Jul 21 2005 Ralph Apel <r.apel at r-apel.de> 0:2.6.2-7jpp
- Include target jars-dom3
- Create new subpackage dom3

* Mon Jul 18 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-5jpp_2fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm (also BC-compiles samples).

* Wed Jul 13 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-6jpp
- Build with Sun JDK (from <gareth.armstrong at hp.com>).

* Wed Jun 15 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-5jpp_1fc
- Upgrade to 2.6.2-5jpp.

* Tue Jun 14 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-5jpp
- Remove the tools tarball, and build xjavac from source.
- Patch xjavac to fix the classpath under libgcj too.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_8fc
- Remove the tools tarball, and build xjavac from source.
- Replace classpath workaround to xjavac task and use
  xml-commons classes again (#152255).

* Thu May 26 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_7fc
- Rearrange how BC-compiled stuff is built and installed.

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_6fc
- Add alpha to the list of build architectures (#157522).
- Use absolute paths for rebuild-gcj-db.

* Thu May  5 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_5fc
- Add dependencies for %%post and %%postun scriptlets (#156901).

* Fri Apr 29 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_4fc
- BC-compile.

* Thu Apr 28 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_3fc
- Revert xjavac classpath workaround, and patch to use libgcj's
  classes instead of those in xml-commons (#152255).

* Thu Apr 21 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_2fc
- Add classpath workaround to xjavac task (#152255).

* Wed Jan 12 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_1fc
- Reenable building of classes that require javax.swing (#130006).
- Sync with RHAPS.

* Mon Nov 15 2004 Fernando Nasser <fnasser@redhat.com>  0:2.6.2-4jpp_1rh
- Merge with upstream for 2.6.2 upgrade

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:2.6.2-2jpp_5fc
- Build into Fedora.

* Thu Oct 28 2004 Gary Benson <gbenson@redhat.com> 0:2.6.2-2jpp_4fc
- Bootstrap into Fedora.

* Fri Oct 1 2004 Andrew Overholt <overholt@redhat.com> 0:2.6.2-2jpp_4rh
- add coreutils BuildRequires

* Thu Sep 30 2004 Andrew Overholt <overholt@redhat.com> 0:2.6.2-2jpp_3rh
- Remove xml-commons-resolver as a Requires

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> 0:2.6.2-4jpp
- Build with ant-1.6.2
- Dropped jikes requirement, built for 1.4.2

* Wed Jun 23 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-3jpp
- Updated Patch #0 to fix breakage using BEA 1.4.2 SDK, new patch
  from <mwringe@redhat.com> and <vivekl@redhat.com>.

* Mon Jun 21 2004 Vivek Lakshmanan <vivekl@redhat.com> 0:2.6.2-2jpp_2rh
- Added new Source1 URL and added new %%setup to expand it under the
  expanded result of Source0.
- Updated Patch0 to fix version discrepancies.
- Added build requirement for xml-commons-apis
 
* Mon Jun 14 2004 Matt Wringe <mwringe@redhat.com> 0:2.6.2-2jpp_1rh
- Update to 2.6.2
- made patch names comformant

* Mon Mar 29 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-2jpp
- Rebuilt with jikes 1.18 for java 1.3.1_11

* Fri Mar 26 2004 Frank Ch. Eigler <fche@redhat.com> 0:2.6.1-1jpp_2rh
- add RHUG upgrade cleanup

* Tue Mar 23 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-1jpp
- 2.6.2

* Thu Mar 11 2004 Frank Ch. Eigler <fche@redhat.com> 0:2.6.1-1jpp_1rh
- RH vacuuming
- remove jikes dependency
- add nonjikes-cast.patch
