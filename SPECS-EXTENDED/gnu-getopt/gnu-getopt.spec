Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package gnu-getopt
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


Name:           gnu-getopt
Version:        1.0.14
Release:        3%{?dist}
Summary:        Java getopt Implementation
License:        GPLv2
Group:          Development/Libraries/Java
URL:            http://www.urbanophile.com/arenn/hacking/download.html
Source0:        http://www.urbanophile.com/arenn/hacking/getopt/java-getopt-%{version}.tar.gz
Patch0:         %{name}-java8compat.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
The GNU Java getopt classes support short and long argument parsing in
a manner 100% compatible with the version of GNU getopt in glibc 2.0.6
with a mostly compatible programmer's interface as well. Note that this
is a port, not a new implementation.

%package javadoc
Summary:        Javadoc for gnu.getopt
Group:          Development/Libraries/Java

%description javadoc
The GNU Java getopt classes support short and long argument parsing in
a manner 100% compatible with the version of GNU getopt in glibc 2.0.6
with a mostly compatible programmer's interface as well. Note that this
is a port, not a new implementation.

This package contains the javadoc documentation for the GNU Java getopt
classes.

%prep
%setup -q -c
%patch0
mv gnu/getopt/buildx.xml build.xml

%build
export JAVA_HOME="%{java_home}"
ant jar javadoc

%install
# jars
mkdir -p %{buildroot}%{_javadir}
install -m 644 build/lib/gnu.getopt.jar %{buildroot}%{_javadir}/gnu.getopt-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -s ${jar} ${jar/-%{version}/}; done)
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -a build/api/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files
%defattr(0644,root,root,0755)
%license gnu/getopt/COPYING.LIB
%doc gnu/getopt/README
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Wed Jan 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.14-3
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.14-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Dec 18 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 1.0.14
- Fix url download link
* Thu May 17 2018 fstrba@suse.com
- Modified patch:
  * gnu-getopt-java16compat.patch -> gnu-getopt-java8compat.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
* Thu Sep 14 2017 fstrba@suse.com
- Removed patch:
  * gnu-getopt-java14compat.patch
- Added patch:
  * gnu-getopt-java16compat.patch
    + Build with java source and target 1.6 in order to allow
    building with jdk9
* Sat May 20 2017 tchvatal@suse.com
- Remove unneeded deps
* Tue Oct  7 2014 tchvatal@suse.com
- Clean up with spec-cleaner
* Thu Oct  9 2008 mvyskocil@suse.cz
- update to 1.0.13:
  * added an Spanish, Polish and Italian messages
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.0.10 from JPackage.org
* Fri Feb 18 2005 skh@suse.de
- update to version 1.0.10
- don't use icecream
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Mon Sep  6 2004 skh@suse.de
- Fix rename error.
* Sat Sep  4 2004 skh@suse.de
- Rename to gnu-getopt to not confuse autobuild
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 1.0.9 (JPackage 1.5)
