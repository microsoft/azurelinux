Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           jdepend
Version:        2.10
Release:        1%{?dist}
Summary:        Java Design Quality Metrics
License:        MIT
URL:            https://github.com/clarkware/jdepend
#BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch
 
Source0:        https://github.com/clarkware/jdepend/archive/refs/tags/2.10.tar.gz#/jdepend-2.10.tar.gz
 
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch
BuildRequires:  ant 
# TODO Remove in Fedora 46

 
%description
JDepend traverses a set of Java class and source file directories and
generates design quality metrics for each Java package. JDepend allows
you to automatically measure the quality of a design in terms of its
extensibility, reusability, and maintainability to effectively manage
and control package dependencies.

%package demo
Summary:        Demonstration and sample files for jdepend
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}

%description demo
JDepend traverses a set of Java class and source file directories and
generates design quality metrics for each Java package. JDepend allows
you to automatically measure the quality of a design in terms of its
extensibility, reusability, and maintainability to effectively manage
and control package dependencies.

This package contains demonstration and sample files for JDepend.
 
%prep
%autosetup -p1 
# remove all binary libs
find . -name "*.jar" -delete
# fix strange permissions
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
 
%build
ant jar
 
%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{name}-%{version}.jar \
    %{buildroot}%{_javadir}/%{name}-%{version}.jar

# provide unversioned symlink for convenience
(cd %{buildroot}%{_javadir} && ln -sf %{name}-%{version}.jar %{name}.jar)

# demo files
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr sample %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE.md
%doc README.md CHANGELOG.md docs
%{_javadir}/jdepend*.jar

%files demo
%{_datadir}/%{name}

%changelog
* Mon Nov 17 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 2.10-1
- Upgrade to version 2.10 (license: MIT).
- License verified
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.1-96
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.9.1-95.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Nov 27 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom file
* Fri Sep  8 2017 fstrba@suse.com
- Removed patch:
  * jdepend-target15.patch
- Added patch:
  * jdepend-target16.patch
    + Specify java source and target levels 1.6 in order to allow
    building with jdk9
* Fri Jun  9 2017 tchvatal@suse.com
- Drop javadoc so we build with gcj properly
* Fri Aug 29 2008 mvyskocil@suse.cz
- source=1.5 -target=1.5
- bzipped source code
- removed the gcj support
- removed a javadoc scripplets
* Fri Mar 14 2008 mvyskocil@suse.cz
- merged with jpackage 1.7:
- update to version 2.9.1
- removed a java14compat patch
- added a gcj build support
- added post(un) scripts for javadoc subpackage
* Thu Mar 29 2007 ro@suse.de
- added unzip to buildreq
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jul 28 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 2.6 from JPackage.org
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 2.6 (JPackage 1.5)
