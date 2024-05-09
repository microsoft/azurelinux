Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package gnu-regexp
#
# Copyright (c) 2019 SUSE LLC
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


Name:           gnu-regexp
Version:        1.1.4
Release:        294%{?dist}
Summary:        Java NFA regular expression engine
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
Group:          Development/Libraries/Java
URL:            https://www.cacas.org/java/gnu/regexp/
Source0:        https://ftp.frugalware.org/pub/other/sources/gnu.regexp/gnu.regexp-%{version}.tar.gz
Source1:        %{name}.build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  gnu-getopt
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
The gnu-regexp package is a pure-Java implementation of a traditional
(non-POSIX) NFA regular expression engine. Its syntax can emulate many
popular development tools, including awk, sed, emacs, perl and grep.
For a relatively complete list of supported and non-supported syntax,
refer to the syntax and usage notes.

%package demo
Summary:        Java NFA regular expression engine (demo and samples)
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}
Requires:       gnu-getopt

%description demo
Demonstrations and samples for Java NFA regular expression engine gnu-regexp.

%package javadoc
Summary:        Java NFA regular expression engine (documentation)
Group:          Development/Libraries/Java

%description javadoc
Javadoc for Java NFA regular expression engine gnu-regexp.

%prep
%setup -q -n gnu.regexp-1.1.4
cp -a %{SOURCE1} build.xml
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=$(build-classpath gnu.getopt)
ant jar javadoc

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -a build/lib/gnu.regexp.jar %{buildroot}%{_javadir}/gnu.regexp-%{version}.jar
(cd %{buildroot}%{_javadir} && ln -sf gnu.regexp-%{version}.jar %{name}-%{version}.jar && \
    for jar in *-%{version}*; do ln -s ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# demo
mkdir -p %{buildroot}%{_datadir}/gnu.regexp/gnu/regexp/util
cp -a build/classes/gnu/regexp/util/*.class \
  %{buildroot}%{_datadir}/gnu.regexp/gnu/regexp/util
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/gnu.regexp
cp -a build/api/* %{buildroot}%{_javadocdir}/gnu.regexp
%fdupes -s %{buildroot}%{_javadocdir}/gnu.regexp

%files
%defattr(0644,root,root,0755)
%doc COPYING COPYING.LIB README TODO docs/*.html
%{_javadir}/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/gnu.regexp

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/gnu.regexp
%{_javadocdir}/gnu.regexp/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4-294
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Nov 18 2020 Joe Schmitt <joschmit@microsoft.com> - 1.1.4-293.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Add understated build requires on javapackages-local-bootstrap.

* Wed Dec 18 2019 Fridrich Strba <fstrba@suse.com>
- Some files are under GPL 2.0+
- Correct link of the tarball in order to be valid
* Thu Jun 14 2018 fstrba@suse.com
- Build with source and target level 8 in order to prepare for the
  removal of 1.6 compatibility.
- Run fdupes on documentation
* Thu Sep 14 2017 fstrba@suse.com
- Build with source and target level 1.6 in order to allow building
  with jdk9
* Sat May 20 2017 tchvatal@suse.com
- Drop obsolete dependency
* Tue Oct  7 2014 tchvatal@suse.com
- Clean up with spec-cleaner
* Wed Jul 17 2013 mls@suse.de
- drop dir attribute from gnu.regexp symlink
* Thu Apr 23 2009 mvyskocil@suse.cz
- add gnu-regexp jars to make build-classpath works as expected
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Oct 25 2005 ro@suse.de
- fix demo package requires
* Mon Oct 17 2005 jsmeix@suse.de
- Current version 1.1.4 from JPackage.org
