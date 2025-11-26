Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Epoch:            2
Name:           jtidy
Version:          1.0
Release:          1%{?dist}
Summary:        HTML syntax checker and pretty printer
License:          zlib
URL:            http://jtidy.sourceforge.net/
# svn export -r1125 https://jtidy.svn.sourceforge.net/svnroot/jtidy/trunk/jtidy/ jtidy
# tar caf jtidy.tar.xz jtidy
Source0:        %{name}.tar.xz
Source1:        %{name}.jtidy.script
Patch0:          javac-1.8.patch
%global debug_package %{nil}
BuildRequires:  javapackages-local-bootstrap
BuildRequires:    ant
# Explicit javapackages-tools requires since jtidy script uses
# /usr/share/java-utils/java-functions
Requires:         javapackages-tools

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM interface to the document that is being processed, which
effectively makes you able to use JTidy as a DOM parser for real-world
HTML.

%package javadoc
Summary:          API documentation for %{name}

%description javadoc
This package contains %{summary}.

%prep
%setup -q -n %{name}
%patch -P0 -p1

%build
ant

%install
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-*.jar \
    %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && ln -sf %{name}-%{version}.jar %{name}.jar)
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/javadoc/* %{buildroot}%{_javadocdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
cp -ap %{SOURCE1} %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo jtidy > %{buildroot}%{_sysconfdir}/ant.d/%{name}

%files
%license LICENSE.txt
%{_javadir}/jtidy*.jar
%attr(755, root, root) %{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/ant.d/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}


%changelog
* Fri Nov 21 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.0-1
- Upgrade to version 1.0 (license: MIT).
- License verified

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0-32
- Updating naming for 3.0 version of Azure Linux.

* Fri Apr 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0-31
- Updating source URL.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0-30
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 8.0-29.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Oct 29 2018 Fridrich Strba <fstrba@suse.com>
- Fix javadoc build
- Package maven artifact
* Fri Sep  8 2017 fstrba@suse.com
- Modified file:
  * maven-build.xml
    + Specify java source and target level 1.6 in order to allow
    building with jdk9
* Thu Dec  5 2013 dvaleev@suse.com
- increase stack size for ppc64le
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Wed Dec 12 2012 dvaleev@suse.com
- increase stack size for ppc64
* Fri Jun 15 2012 mvyskocil@suse.cz
- disable javadoc (workaround for jdk7 build)
* Wed May 20 2009 mvyskocil@suse.cz
- 'fixed bnc#501764: removed clover.license from source tarball'
* Thu May  7 2009 mvyskocil@suse.cz
- Initial packaging of 8.0 in SUSE (from jpp 5.0)
