## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
Name:           slf4j2
Version:        2.0.17
Release:        %autorelease
Summary:        Simple Logging Facade for Java
# the log4j-over-slf4j and jcl-over-slf4j submodules are ASL 2.0, rest is MIT
License:        MIT AND Apache-2.0
URL:            https://www.slf4j.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/qos-ch/slf4j/archive/v_%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.0.16-4

%description
The Simple Logging Facade for Java or (SLF4J) is intended to serve
as a simple facade for various logging APIs allowing to the end-user
to plug in the desired implementation at deployment time. SLF4J also
allows for a gradual migration path away from
Jakarta Commons Logging (JCL).

Logging API implementations can either choose to implement the
SLF4J interfaces directly, e.g. NLOG4J or SimpleLogger. Alternatively,
it is possible (and rather easy) to write SLF4J adapters for the given
API implementation, e.g. Log4jLoggerAdapter or JDK14LoggerAdapter..

%package jdk14
Summary:        SLF4J JDK14 Binding

%description jdk14
SLF4J JDK14 Binding.

%package jdk-platform-logging
Summary:        SLF4J Platform Logging Binding

%description jdk-platform-logging
SLF4J Platform Logging Binding.

%package -n jcl-over-%{name}
Summary:        JCL 1.1.1 implemented over SLF4J

%description -n jcl-over-%{name}
JCL 1.1.1 implemented over SLF4J.

%package -n jul-to-%{name}
Summary:        JUL to SLF4J bridge

%description -n jul-to-%{name}
JUL to SLF4J bridge.

%package -n log4j-over-%{name}
Summary:        Log4j implemented over SLF4J

%description -n log4j-over-%{name}
Log4j implemented over SLF4J.

%package migrator
Summary:        SLF4J Migrator

%description migrator
SLF4J Migrator.

%prep
%autosetup -p1 -C
find -name '*.jar' -delete
install -p -m 0644 %{SOURCE1} LICENSE-2.0.txt

%pom_disable_module integration
%pom_disable_module osgi-over-slf4j
%pom_disable_module slf4j-ext
%pom_disable_module slf4j-log4j12
%pom_disable_module slf4j-reload4j

# dos2unix
find -name '*.css' -o -name '*.js' -o -name '*.txt' -exec sed -i 's/\r//' {} +

# Remove wagon-ssh build extension
%pom_xpath_remove pom:extensions parent

%mvn_package :::sources: __noinstall
%mvn_package :slf4j-bom __noinstall
%mvn_package :slf4j-parent __noinstall
%mvn_package :slf4j-site __noinstall
%mvn_package :slf4j-api
%mvn_package :slf4j-simple
%mvn_package :slf4j-nop

%mvn_compat_version : 2.0.17

%build
%mvn_build -j -f -s -j -- -Drequired.jdk.version=1.8

%install
# Compat symlinks
%mvn_file ':slf4j-{*}' %{name}/slf4j-@1 %{name}/@1

%mvn_install

%files -f .mfiles
%license LICENSE.txt LICENSE-2.0.txt

%files jdk14 -f .mfiles-slf4j-jdk14

%files jdk-platform-logging -f .mfiles-slf4j-jdk-platform-logging

%files -n jcl-over-%{name} -f .mfiles-jcl-over-slf4j

%files -n jul-to-%{name} -f .mfiles-jul-to-slf4j

%files -n log4j-over-%{name} -f .mfiles-log4j-over-slf4j

%files migrator -f .mfiles-slf4j-migrator

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.0.17-6
- test: add initial lock files

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.17-4
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.17-3
- Switch javapackages test plan to f43 ref

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.17-2
- Switch to javapackages tests from CentOS Stream GitLab

* Thu Mar 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.17-1
- Update to upstream version 2.0.17

* Mon Mar 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.16-3
- Remove javadoc subpackage

* Fri Feb 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.16-2
- Disable javadocs

* Fri Feb 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.16-1
- Update to upstream version 2.0.16

* Fri Feb 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.36-1
- Rename to slf4j2

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Marian Koncek <mkoncek@redhat.com> - 1.7.36-1
- Update to upstream version 1.7.36

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.7.32-12
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 1.7.32-11
- bump of release for for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.32-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.32-9
- Rebuild to regenerate auto-Requires on java

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.32-8
- Convert License tag to SPDX format

* Tue Aug 15 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.32-7
- Build with default JDK 17

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.7.32-3
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Simon Legner <Simon.Legner@gmail.com> - 1.7.32-1
- Update to upstream version 1.7.32

* Tue Nov 16 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.30-11
- Enable slf4j-migrator and log4j-over-slf4j modules

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.30-9
- Bootstrap build
- Non-bootstrap build

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.7.30-7
- Disable unused log4j12 module.

* Thu Jul 30 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.7.30-6
- Port to commons-lang3.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 0:1.7.30-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Roland Grunberg <rgrunber@redhat.com> - 0:1.7.30-3
- Use source/target of 1.6 to build against Java 11.
- Set javadoc plugin source value to 1.6.

* Fri Mar 20 2020 Mat Booth <mat.booth@redhat.com> - 0:1.7.30-2
- Fix broken OSGi metadata

* Wed Feb 05 2020 Dinesh Prasanth M K <dmoluguw@redhat.com> - 0:1.7.30-1
- Update to upstream version 1.7.30

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.30-2
- Build with OpenJDK 8

* Thu Jan 23 2020 Marian Koncek <mkoncek@redhat.com> - 1.7.30-1
- Update to upstream version 1.7.30

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.28-2
- Mass rebuild for javapackages-tools 201902

* Tue Aug 13 2019 Marian Koncek <mkoncek@redhat.com> - 1.7.28-1
- Update to upstream version 1.7.28

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.26-3
- Mass rebuild for javapackages-tools 201901

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.26-2
- Disable slf4j-ext module

* Thu May 09 2019 Dinesh Prasanth M K <dmoluguw@redhat.com> - 0:1.7.25-7
- Rebuilt for Fedora 31

* Wed Feb 27 2019 Marian Koncek <mkoncek@redhat.com> - 0:1.7.26-1
- Update to upstream version 1.7.26
- Fixes: RHBZ #1678877

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 19 2018 Michael Simacek <msimacek@redhat.com> - 0:1.7.25-4
- Disallow EventData deserialization by default (CVE-2018-8088)
- Resolves rhbz#1549928

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.25-1
- Update to upstream version 1.7.25

* Wed Feb 22 2017 Michael Simacek <msimacek@redhat.com> - 0:1.7.22-4
- Avoid absolute paths

* Thu Feb 16 2017 Michael Simacek <msimacek@redhat.com> - 0:1.7.22-3
- Avoid literal carriage return
- Remove Group tag

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Michael Simacek <msimacek@redhat.com> - 0:1.7.22-1
- Update to upstream version 1.7.22

* Fri Nov 18 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.21-4
- Install source JARs in separate package

* Mon Oct  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.21-3
- Remove build-requires on perl

* Tue May 31 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.21-2
- Fix build issue with maven-jar-plugin 3.0.0

* Wed Apr  6 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.21-1
- Update to upstream version 1.7.21

* Wed Mar 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.20-1
- Update to upstream version 1.7.20

* Thu Mar 24 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.19-1
- Update to upstream version 1.7.19

* Mon Feb 29 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.18-1
- Update to upstream version 1.7.18

* Mon Feb 22 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.17-1
- Update to upstream version 1.7.17

* Tue Feb 16 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.16-1
- Update to upstream version 1.7.16

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.14-1
- Update to upstream version 1.7.14

* Thu Nov 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.13-1
- Update to upstream version 1.7.13

* Mon Aug 03 2015 Michael Simacek <msimacek@redhat.com> - 0:1.7.12-3
- List manual files in %%files section

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.12-1
- Update to upstream version 1.7.12

* Mon Jan 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.10-1
- Update to upstream version 1.7.10

* Fri Oct 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.7-3
- Remove workaround for MSHARED-325

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.7-1
- Update to upstream version 1.7.7

* Thu Mar 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.6-5
- Disable filtering of bundled JavaScript binaries
- Resolves: rhbz#1078536

* Fri Mar 07 2014 Michael Simacek <msimacek@redhat.com> - 0:1.7.6-4
- Merge api, simple and nop back into main package
- Remove parent, migrator and site subpackages

* Fri Mar 07 2014 Michael Simacek <msimacek@redhat.com> - 0:1.7.6-3
- Split into subpackages

* Thu Mar  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.6-2
- Remove wagon-ssh build extension
- Disable slf4j-android module

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.6-2
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.6-1
- Update to upstream version 1.7.6

* Tue Aug 06 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-3
- Install manual to versionless docdir (#993551)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.5-1
- Update to upstream version 1.7.5

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.4-1
- Update to upstream version 1.7.4

* Fri Mar 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.3-1
- Update to upstream version 1.7.3

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.7.2-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.2-7
- Fix install location of manual

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.2-6
- Rebuild to generate maven provides

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.2-5
- Build with xmvn

* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.2-4
- Install Apache license file
- Resolves: rhbz#878996

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.2-3
- Avoid cyclic OSGi dependencies

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.2-2
- Fix license to ASL 2.0 and MIT
- Update to add_maven_depmap macro
- Use generated .mfiles list
- Small packaging cleanups

* Mon Oct 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.2-1
- Update to upstream version 1.7.2

* Mon Sep 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.1-1
- Update to upstream version 1.7.1

* Mon Sep 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.0-1
- Update to upstream version 1.7.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6.6-1
- Update to upstream version 1.6.6
- Convert patches to POM macros

* Fri Jan 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 0:1.6.1-5
- Crosslink with local JDK API docs.

* Fri Jan 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 0:1.6.1-4
- Specify explicit source encoding to fix build with Java 1.7.
- Remove no longer needed javadoc dir upgrade hack.

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.1-3
- Build with maven 3.x.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.1-1
- Update to new upstream version.
- Various guidelines fixes.

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.11-3
- Add maven-site-pugin BR.
- Use new package names.

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.11-2
- Skip installing tests jar that is no longer produced.
- Use javadoc aggregate.
- Use mavenpomdir macro.

* Thu Feb 25 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.11-1
- Update to 1.5.11.
- Drop depmap and component info files.

* Wed Feb 10 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.5.10-5
- Require cal10n

* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-4
- Fix javadoc files.

* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-3
- BR maven-plugin-build-helper.

* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-2
- BR cal10n.

* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-1
- Update to upstream 1.5.10.

* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-5
- Skip tests.

* Wed Sep 2 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-4
- Fix other line lenghts.

* Wed Sep 2 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-3
- Fix permissions.
- Fixed descriptions.
- Fix file lengths.

* Wed Sep 2 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-2
- Adapt for Fedora.

* Wed Jul 29 2009 Yong Yang <yyang@redhat.com> 0:1.5.8-1
- 1.5.8
- Replace slf4j-1.5.6-integration-tests-current-only.patch with
  slf4j-1.5.8-skip-integration-tests.patch because of the failure of "testMatch"

* Fri Jun 12 2009 Ralph Apel <r.apel at r-apel.de> 0:1.5.6-2
- Add -ext jar, depmap and pom
- Save jcl104-over-slf4j as symlink

* Tue Feb 18 2009 David Walluck <dwalluck@redhat.com> 0:1.5.6-1
- 1.5.6
- add repolib
- fix file eol
- fix Release tag

* Fri Jul 18 2008 David Walluck <dwalluck@redhat.com> 0:1.5.2-2
- use excalibur for avalon
- remove javadoc scriptlets
- GCJ fixes
- fix maven directory ownership
- fix -bc --short-circuit by moving some of %%build to %%prep

* Sun Jul 06 2008 Ralph Apel <r.apel at r-apel.de> 0:1.5.2-1.jpp5
- 1.5.2

* Mon Feb 04 2008 Ralph Apel <r.apel at r-apel.de> 0:1.4.2-2jpp
- Fix macro misprint
- Add maven2-plugin BRs

* Wed Jul 18 2007 Ralph Apel <r.apel at r-apel.de> 0:1.4.2-1jpp
- Upgrade to 1.4.2
- Build with maven2
- Add poms and depmap frags
- Add gcj_support option

* Mon Jan 30 2006 Ralph Apel <r.apel at r-apel.de> 0:1.0-0.rc5.1jpp
- First JPackage release.

## END: Generated by rpmautospec
