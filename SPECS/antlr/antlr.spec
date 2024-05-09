#
# spec file for package antlr
#
# Copyright (c) 2020 SUSE LLC
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

%global debug_package %{nil}
%bcond_with python2

Summary:        Another Tool for Language Recognition
Name:           antlr
Version:        2.7.7
Release:        125%{?dist}
License:        Public Domain
Group:          Development/Tools/Other
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.antlr.org/
# Upstream source under https://www.antlr2.org/download/antlr-2.7.7.tar.gz. Needs verification.
Source0:        %{_distro_sources_url}/antlr-%{version}.tar.bz2
Source1:        %{name}-build.xml
Source2:        %{name}-script
Source3:        https://repo2.maven.org/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
Source1000:     antlr-rpmlintrc
Patch0:         %{name}-jedit.patch
Patch1:         gcc45fix.diff
Patch2:         fix-docpath.diff
BuildRequires:  ant
BuildRequires:  gcc-c++
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xml-commons-apis
Requires:       %{name}-java
Provides:       %{name}-bootstrap = %{version}
Provides:       %{name}-tool = %{version}-%{release}
Obsoletes:      %{name}-bootstrap < %{version}
Obsoletes:      %{name}-javadoc
%if %{with python2}
BuildRequires:  python2-base
%endif

%description
ANTLR, Another Tool for Language Recognition, (formerly PCCTS) is a
language tool that provides a framework for constructing recognizers,
compilers, and translators from grammatical descriptions containing C++
or Java actions (you can use PCCTS 1.xx to generate C-based parsers).

%package        java
Summary:        ANother Tool for Language Recognition (Manual)
Group:          Development/Tools/Other
Requires:       java >= 1.8
BuildArch:      noarch

%description    java
ANTLR, Another Tool for Language Recognition, (formerly PCCTS) is a
language tool that provides a framework for constructing recognizers,
compilers, and translators from grammatical descriptions containing C++
or Java actions (you can use PCCTS 1.xx to generate C-based parsers).

This package provides the Java runtime for antlr

%package        manual
Summary:        ANother Tool for Language Recognition (Manual)
Group:          Development/Tools/Other
BuildArch:      noarch

%description    manual
ANTLR, Another Tool for Language Recognition, (formerly PCCTS) is a
language tool that provides a framework for constructing recognizers,
compilers, and translators from grammatical descriptions containing C++
or Java actions (you can use PCCTS 1.xx to generate C-based parsers).

This package provides the manual for antlr.

%package        devel
Summary:        ANother Tool for Language Recognition (c++ runtime)
Group:          Development/Tools/Other
Requires:       antlr
Provides:       %{name}-C++ = %{version}-%{release}

%description    devel
ANTLR, Another Tool for Language Recognition, (formerly PCCTS) is a
language tool that provides a framework for constructing recognizers,
compilers, and translators from grammatical descriptions containing C++
or Java actions (you can use PCCTS 1.xx to generate C-based parsers).

This package provides the C++ runtime (libantlr.a) and a headers files
of antlr

%package -n     python2-%{name}
Summary:        ANother Tool for Language Recognition (python runtime)
Group:          Development/Tools/Other
Requires:       antlr
Provides:       python-%{name}
Obsoletes:      python-%{name}

%description -n  python2-%{name}
Python support for generating your Lexers, Parsers and TreeParsers in Python.
This feature extends the benefits of ANTLR's predicated-LL(k) parsing
technology to the Python language and platform.

ANTLR Python support was contributed (and is to be maintained) by Wolfgang
Haefelinger and Marq Kole.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.exe" -exec rm -f {} \;
find . -name "*.dll" -exec rm -f {} \;
find . -name Makefile.in | xargs chmod 0644
%patch 0
cp -p %{SOURCE1} build.xml
#Fix the source so that it compiles with GCC 4.5
%patch 1 -p1
#Ensure that the manuals are installed in the correct openSUSE docpath
%patch 2
# check for license problematic files:
find | grep "\(ShowString.java$\|StreamConverter.java$\)" && exit 42 || :

%build
%global _lto_cflags %{_lto_cflags} -ffat-lto-objects
ant \
    -Dj2se.apidoc=%{_javadocdir}/java \
    -Dant.build.javac.source=8 -Dant.build.javac.target=8 \
    jar
%configure --without-examples
make -j1

%if %{with python2}
%py_compile lib/python/antlr
%endif

%install
### jars ###
install -d -m 0755 %{buildroot}%{_javadir}
cp -a work/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -s -f ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# compat symlink
install -d -m 0755 %{buildroot}%{_datadir}/%{name}-%{version}/
ln -s -f %{_javadir}/%{name}-%{version}.jar %{buildroot}%{_datadir}/%{name}-%{version}/%{name}.jar

### pom ###
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom
%add_maven_depmap %{name}-%{version}.pom %{name}-%{version}.jar -a %{name}:%{name}all -f java

### scripts ###
install -d -m 0755 %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}
install -m 0755 scripts/%{name}-config %{buildroot}%{_bindir}/

### python runtime ###
%if %{with python2}
install -d -m 0755 %{buildroot}%{python_sitearch}/%{name}
cp -a lib/python/antlr/* %{buildroot}%{python_sitearch}/%{name}
%endif

### cpp runtime ###
mkdir -p %{buildroot}%{_libdir}
install -m 0755 lib/cpp/src/lib%{name}.a %{buildroot}%{_libdir}
install -d -m 0755 %{buildroot}%{_includedir}/%{name}
install -m 0644 lib/cpp/%{name}/*hpp %{buildroot}%{_includedir}/%{name}

### doc permissions ###
rm doc/{Makefile,Makefile.in}
find doc -type f | xargs chmod 0644

%files
%license LICENSE.txt
%doc README.txt CHANGES.txt
%dir %{_datadir}/%{name}-%{version}
%{_bindir}/antlr
%{_bindir}/antlr-config

%files java
%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/*jar
%{_javadir}/%{name}*.jar
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%config(noreplace) %{_mavendepmapfragdir}/%{name}-java
%else
%{_datadir}/maven-metadata/%{name}-java.xml
%endif

%files manual
%doc doc

%files devel
%{_libdir}/libantlr.a
%{_includedir}/%{name}

%if %{with python2}
%files -n python2-%{name}
%dir %{_datadir}/%{name}-%{version}
%{python_sitearch}/%{name}
%endif

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.7-125
- Updating naming for 3.0 version of Azure Linux.

* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.7-124
- Fixing source URL.

* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.7.7-123
- Move to SPECS
- License verified
- Note, antlr2 is actually public domain https://www.antlr2.org/license.html

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.7-122
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.7.7-121.3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Build without python2.
- Set debug_package nil.
- Provides antlr-tool and antrl-C++.

* Thu May  7 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Build antlr-manual package without examples files [bsc#1120360]
- Remove not needed files
* Mon Jan  6 2020 Fridrich Strba <fstrba@suse.com>
- Not only provide python-antlr, but also obsolete it
* Wed Jul 31 2019 Martin Liška <mliska@suse.cz>
- Use FAT LTO objects in order to provide proper static library.
* Sun Nov 18 2018 Fridrich Strba <fstrba@suse.com>
- Install as maven artifact using the pom file from maven central
* Thu Sep 13 2018 Tomáš Chvátal <tchvatal@suse.com>
- Do not create compat symlink for python stuff as it was not working
  before anyway
- Rename python package to python2-antlr (provide old symbol)
* Fri Jul 20 2018 tchvatal@suse.com
- Do not use old compat macros for python directories
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
* Fri Jan 12 2018 tchvatal@suse.com
- Add condition about python2 module, the rewrite happened in antlr4
  for python3 support and it is completely different than the antlr2
  * The python module is not used by any package in TW bsc#1068226
* Thu Dec  7 2017 dimstar@opensuse.org
- Fix build with RPM 4.14: a command that exits with error > 0
  aborts the build (and grep not finding a string is retval 1).
* Fri Nov  3 2017 mpluskal@suse.com
- Explicitly require python2 [bsc#1068226, fate#323526]
* Fri Sep 29 2017 fstrba@suse.com
- Require java-devel >= 1.6 to build, because of the source and
  target level
* Wed Sep  6 2017 fstrba@suse.com
- fixes necessary to compile with Java 9
  * set javac source and target to 1.6
* Fri Jun  9 2017 tchvatal@suse.com
- Drop the javadoc so we can be build with java bootstrapping reducing
  the cycle/failures
* Fri May 19 2017 tchvatal@suse.com
- Reduce dependencies a bit
* Thu Dec  4 2014 p.drouand@gmail.com
- Remove java-devel dependency; not needed anymore
* Fri Jul  4 2014 tchvatal@suse.com
- Cleanup with spec-cleaner and fix the sle11 build properly.
* Wed Apr 30 2014 darin@darins.net
- Set buildarch on SLE_11 or the python subpackage is packaged
  as noarch when they need be arch specific.
  https://lists.opensuse.org/opensuse-packaging/2014-04/msg00055.html
* Tue Apr 29 2014 darin@darins.net
- supporess bytecode version check on SLE
- fix perms for SLES
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Jul 11 2013 dmueller@suse.com
- drop antlr-cshap, entirely unused and removes mono dependency
* Wed Oct 31 2012 mvyskocil@suse.com
- examples files are now 0644 to beeing able to fdupes them properly (bnc#784670)
* Thu Jul 21 2011 toddrme2178@gmail.com
- Modify descriptions (fix for RPMLINT warnings)
- Check for duplicate files (fix for RPMLINT warnings)
* Mon Aug 23 2010 mvyskocil@suse.cz
- add missing java requires of antlr-java package
* Thu Aug 19 2010 mvyskocil@suse.cz
- enabled the python (python-antlr) and csharp (antlr-csharp) support
- moved jar files to new antlr-java package, which is required by main antlr
  one. This is to have jar files in noarch package
- do not use default make install, but install files manually with a
  compatibility links to /usr/share/antlr-2.7.7
* Wed Aug 18 2010 tittiatcoke@opensuse.org
- Ensure that the development files are build too. The package is now a build
  requirement for the KDESDK4 package.
- Removed the structure to build just the native version.
* Mon Mar  3 2008 mvyskocil@suse.cz
- updated to 2.7.7
  * updated BaseAST.java to make the doWorkForAll method static. Same
    behaviour, except no ClassCastExceptions when sibling.getFirstChild()
    happens to return an AST that doesn't extend BaseAST.  Oliver Wong contributed
    the patch.
  * updated TokenStreamRewriteEngine.java to reflect bug fixes discovered
    in v3 counterpart.
* Wed Feb 20 2008 adrian@suse.de
- do not PreReq files to fix build env setup for other packages
- remove SL-9.1 traces
* Fri May  4 2007 dbornkessel@suse.de
- added unzip to BuildRequires
* Sat Oct  7 2006 dbornkessel@suse.de
- added check that checks whether deleted files ShowString.java and StreamConverter.java are really not in place
* Thu Oct  5 2006 dbornkessel@suse.de
- deleted
  antlr-2.7.6/examples/java/unicode.IDENTs/ShowString.java
  antlr-2.7.6/examples/java/unicode.IDENTs/StreamConverter.java
  from tar ball due to licensing issues (Bug #207621)
* Mon Sep 25 2006 dbornkessel@suse.de
- fixes necessary to compile with Java 1.5.0
  - set source="1.4" and target="1.4" for ant "javac" tasks
  - set source="1.4" for ant "javadoc" tasks
* Wed Sep 20 2006 dbornkessel@suse.de
- Provide: antlr-bootstrap
  Obsoletes: antlr-bootstrap
* Mon Sep 18 2006 dbornkessel@suse.de
- update to 2.7.6
  - added size, index methods to TokenStreamRewriteEngine.java
  - bug in syn preds for tree parsers.  Submitted by Ole Kniemeyer.
  - all Class.forName yanked out; uses thread context loader
  - option to prevent System.exit termination
  - added recover() method to lexers
  - fixed code gen bug for syn preds in tree parsers.  Thanks to Marc Horowitz.
  - BaseAST was not checking for null text in toString()
  - Scott added java line ouput in code gen
  - Prashant tweaked a few things for ANTLRStudio; a few new classes in ASdebug package
  - Give errors if the user attempts to set k>1 in a TreeWalker
  - Added missing Makefile.in for C++ heteroAST example and enabled it
    in configure.in
  - Many small C++ support code and codegen tweaks fixes to increase
    portability. (Compaq Tru64 UNIX V5.1, VC's)
  - Prevent '\' entering the bitset dump comments, might occur at end of
    line. Some compilers continue the comment to the next line (not sure
    if this is a compiler bug, should look it up)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Oct 25 2005 jsmeix@suse.de
- removed sub-package antlr-jedit because since jedit version 4.2
  /usr/share/jedit/modes/antlr.xml is included in jedit.
* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Tue Jul 19 2005 jsmeix@suse.de
- Current version 2.7.4 from JPackage.org
* Wed Mar  2 2005 skh@suse.de
- added support for C++ output (#67164)
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
- conflict with pccts
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 2.7.4 (JPackage 1.5)
