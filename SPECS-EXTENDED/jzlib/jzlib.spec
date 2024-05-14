Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package jzlib
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           jzlib
Version:        1.1.3
Release:        5%{?dist}
Summary:        Re-implementation of zlib in pure Java
License:        BSD-3-Clause
Group:          Development/Libraries/Java
URL:            https://www.jcraft.com/jzlib/
Source0:        https://github.com/ymnk/jzlib/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}_build.xml
# This patch is sent upstream: https://github.com/ymnk/jzlib/pull/15
Patch0:         jzlib-javadoc-fixes.patch
BuildRequires:  ant >= 1.6
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
The zlib is designed to be a free, general-purpose, legally
unencumbered -- that is, not covered by any patents -- lossless
data-compression library for use on virtually any computer hardware and
operating system. The zlib was written by Jean-loup Gailly
(compression) and Mark Adler (decompression).

%package        demo
Summary:        Examples for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}

%description    demo
%{summary}.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description    javadoc
%{summary}.

%prep
%setup -q
%patch 0
cp %{SOURCE1} build.xml

# bnc#500524
# be sure that we don't distribute GPL derived code marked as BSD
rm misc/mindtermsrc-v121-compression.patch

%build
%{ant} jar javadoc

%install
# jar
install -Dpm 644 target/%{name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}.jar

# pom
install -Dpm 644 pom.xml \
  %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar

# examples
install -dm 755 %{buildroot}%{_datadir}/%{name}-%{version}
cp -pr example/* %{buildroot}%{_datadir}/%{name}-%{version}
%fdupes -s %{buildroot}%{_datadir}/%{name}-%{version}

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -r target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%defattr(0644,root,root,0755)
%license LICENSE.txt

%files demo
%defattr(0644,root,root,0755)
%doc %{_datadir}/%{name}-%{version}

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.3-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.1.3-4.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Sep 23 2019 Fridrich Strba <fstrba@suse.com>
- Build the jar file as an eclipse bundle
- Build and package the javadoc again
- Added patch:
  * jzlib-javadoc-fixes.patch
    + small fixes for javadoc tags
* Sun Nov 25 2018 Fridrich Strba <fstrba@suse.com>
- Install as maven artifact
* Fri Sep  8 2017 fstrba@suse.com
- Specify java source and target level 1.6 in order to allow build
  with jdk9
* Fri Jun  9 2017 tchvatal@suse.com
- Version update to 1.1.3:
  * Various small fixes in from the github project
- Drop javadoc to bootstrap using gcj
* Tue Jul  8 2014 tchvatal@suse.com
- Cleanup with spec-cleaner and fix sle build properly
* Wed Apr 30 2014 darin@darins.net
- suppress bytecode check on SLE
* Wed Feb 19 2014 lchiquitto@suse.com
- Remove old tarball
* Thu Oct  3 2013 mvyskocil@suse.com
- Update to 1.1.2
  * fixed a bug in DeflaterOutputStream#write() with empty data.  9d4616f
  * fixed a bug in processing unwrapped data with InfalterInputStream. d35db2
  * fixed bugs reported in https://github.com/ymnk/jzlib/pull/5 e4aa20
  + comments and filename in GZIPHeader must be in ISO-8859-1 encoding
  + fixing a bug in GZIPHeader#setOS(int os)
  * some refactoring code. e912088 6900f5 614fdf
  * improving the performace of Adler32#update method.  6900f5
  * constructors of Alder32 and CRC32 become public. 30c4cf
  * added ZStream#end() and ZStream#finished().  6b55e3
  * exposed useful constants for jruby.  e17ad1
  * updated pom.xml to delete "souceDirectory"
  No need to specify sourceDirectory if the project follows maven
  standard.
  * updated configurations to use sbt 0.11.1
- Don't build for java5 only
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Sep 10 2009 mvyskocil@suse.cz
- fixed bnc#536215: remove share/jzlib ghost symlink to allow
  smooth transition from older Packman package
* Mon May  4 2009 mvyskocil@suse.cz
- fixed bnc#500524:
  * removed misc/mindtermsrc-v121-compression.patch in %%%%prep
* Tue Apr 28 2009 mvyskocil@suse.cz
- Initial SUSE packaging (version 1.0.7 from jpp5)
