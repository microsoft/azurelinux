Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package jsch
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


Name:           jsch
Version:        0.1.55
Release:        2%{?dist}
Summary:        Pure Java implementation of SSH2
License:        BSD-3-Clause
Group:          Development/Libraries/Java
URL:            https://www.jcraft.com/jsch/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.zip
Source1:        https://repo1.maven.org/maven2/com/jcraft/%{name}/%{version}/%{name}-%{version}.pom
Source2:        plugin.properties
Patch0:         jsch-0.1.54-sourcetarget.patch
Patch1:         jsch-osgi-manifest.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jzlib
BuildRequires:  unzip
BuildRequires:  zip
Requires:       jzlib
BuildArch:      noarch

%description
JSch allows you to connect to an sshd server and use port forwarding,
X11 forwarding, file transfer, etc., and you can integrate its
functionality into your own Java programs.

%package        javadoc
Summary:        Pure Java implementation of SSH2
Group:          Development/Libraries/Java

%description    javadoc
JSch allows you to connect to an sshd server and use port forwarding,
X11 forwarding, file transfer, etc., and you can integrate its
functionality into your own Java programs.

%package        demo
Summary:        Pure Java implementation of SSH2
Group:          Development/Libraries/Java

%description    demo
JSch allows you to connect to an sshd server and use port forwarding,
X11 forwarding, file transfer, etc., and you can integrate its
functionality into your own Java programs.

%prep
%setup -q
%patch 0 -p1
%patch 1 -p1
cp %{SOURCE1} pom.xml
%pom_remove_parent

%build
export CLASSPATH=$(build-classpath jzlib)
ant dist javadoc

%install
# inject the OSGi Manifest
cp %{SOURCE2} plugin.properties
jar uf dist/lib/%{name}-*.jar plugin.properties

# jars
install -Dpm 644 dist/lib/%{name}-*.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr javadoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

# examples
install -dm 755 %{buildroot}%{_datadir}/%{name}
cp -pr examples/* %{buildroot}%{_datadir}/%{name}
%fdupes -s %{buildroot}%{_datadir}/%{name}

%files -f .mfiles
%license LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.55-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.1.55-1.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Apr  7 2020 Fridrich Strba <fstrba@suse.com>
- Version 0.1.55
* Tue Apr  7 2020 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * jsch-osgi-manifest.patch
    + create the osgi manifest during the ant build
    + replaces the MANIFEST.MF file
- Miscellaneous clean-up
* Fri Sep 20 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent from pom file, since we are not
  building with maven
* Fri Sep  8 2017 fstrba@suse.com
- Added patch:
  * jsch-0.1.54-sourcetarget.patch
  - Specify java source and target levels to 1.6, in order to
    allow building with jdk9
* Fri Jun  9 2017 tchvatal@suse.com
- Build with full java, does not compile with gcj
* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
* Sun Feb 12 2017 guoyunhebrave@gmail.com
- Version 0.1.54
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Tue Jun 17 2014 tchvatal@suse.com
- Version bump to 0.1.51
- Cleanup with spec-cleaner
- Add maven and osgi things same as in Fedora.
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Mon May 13 2013 mvyskocil@suse.com
- update to 0.1.50
  * fixes connection errors with "verify: false" when running on
    Java 7u6 (and later).
  * The OpenSSH config file and the key exchange method
    "diffie-hellman-group-exchange-sha256" are now supported
* Tue Oct 16 2012 mvyskocil@suse.com
- update to 0.1.49
  * Putty's private key files support
  * hmax-sha2-256 defined in RFC6668 is supported
  * integration with jsch-agent-proxy
  * and many bugfixes
* Tue Apr 28 2009 mvyskocil@suse.cz
- Initial SUSE packaging of version 0.1.40 (from jpp5)
