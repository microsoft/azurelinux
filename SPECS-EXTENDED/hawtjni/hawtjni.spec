Name:             hawtjni
Version:          1.18
Release:          13%{?dist}
Summary:          Code generator that produces the JNI code
# Maven plugin is under ASL 2.0.
# stdint.h, shipped in JAR as resource, used only with M$ VC++, is under BSD.
# Everything else is under EPL-1.0
License:          ASL 2.0 and EPL-1.0 and BSD

URL:              http://hawtjni.fusesource.org/
Source0:          https://github.com/fusesource/hawtjni/archive/%{name}-project-%{version}.tar.gz

# trivially port from commons-lang to commons-lang3
Patch0:           00-hawtjni-port-to-commons-lang3.patch

BuildArch:        noarch
#ExclusiveArch:  %{java_arches} noarch

BuildRequires:    maven-local
BuildRequires:    mvn(commons-cli:commons-cli)
BuildRequires:    mvn(org.apache.commons:commons-lang3)
BuildRequires:    mvn(org.apache.maven:maven-archiver)
BuildRequires:    mvn(org.apache.maven:maven-artifact)
BuildRequires:    mvn(org.apache.maven:maven-compat)
BuildRequires:    mvn(org.apache.maven:maven-plugin-api)
BuildRequires:    mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:    mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:    mvn(org.apache.xbean:xbean-finder)
BuildRequires:    mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:    mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:    mvn(org.codehaus.plexus:plexus-io)
BuildRequires:    mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:    mvn(org.fusesource:fusesource-pom:pom:)
BuildRequires:    mvn(org.ow2.asm:asm)
BuildRequires:    mvn(org.ow2.asm:asm-commons)

Requires:         autoconf
Requires:         automake
Requires:         libtool
Requires:         make

%description
HawtJNI is a code generator that produces the JNI code needed to
implement java native methods. It is based on the jnigen code generator
that is part of the SWT Tools project which is used to generate all the
JNI code which powers the eclipse platform.

%package javadoc
Summary:          Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%package runtime
Summary:          HawtJNI Runtime

%description runtime
This package provides API that projects using HawtJNI should build
against.

%package -n maven-hawtjni-plugin
Summary:          Use HawtJNI from a maven plugin

%description -n maven-%{name}-plugin
This package allows to use HawtJNI from a maven plugin.

%prep
%setup -q -n %{name}-%{name}-project-%{version}
%patch 0 -p1

%pom_disable_module hawtjni-example
%pom_disable_module hawtjni-maven-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r :maven-eclipse-plugin

%mvn_package ":hawtjni-runtime" runtime

# javadoc generation fails due to strict doclint in JDK 8
%pom_remove_plugin :maven-javadoc-plugin hawtjni-runtime

%build
%mvn_build

%install
%mvn_install

%files runtime -f .mfiles-runtime
%doc readme.md license.txt changelog.md

%files -f .mfiles

%files javadoc -f .mfiles-javadoc
%doc license.txt

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.18-12
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 27 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.18-9
- Disable hawtjni-maven-plugin

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.18-5
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.18-4
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 27 2021 Nicolas De Amicis <deamicis@bluewin.ch> - 1.18-1
- update to version 1.18

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jul 30 2020 Fabio Valentini <decathorpe@gmail.com> - 1.17-6
- Port to commons-lang3.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.17-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Mar 25 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1.17-3
- Add maven-compat to hawtjni-maven-plugin as it is using
  the ArtifactResolver class in the maven-compat.jar

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 05 2019 Fabio Valentini <decathorpe@gmail.com> - 1.17-1
- Update to version 1.17.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  2 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.16-2
- Update license tag

* Mon Feb 26 2018 Michael Simacek <msimacek@redhat.com> - 1.16-1
- Update to upstream version 1.16

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Michael Simacek <msimacek@redhat.com> - 1.15-1
- Update to upstream version 1.15

* Mon Feb 13 2017 Michael Simacek <msimacek@redhat.com> - 1.10-9
- Add Requires on make

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1.10-8
- Regenerate BuildRequires

* Wed Feb  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-7
- Remove unneeded BR on maven-project-info-reports-plugin

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-4
- Remove maven-javadoc-plugin execution

* Fri Nov 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-3
- Spit runtime into subpackage
- Resolves: rhbz#1166607

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-2
- Add requires on autoconf, automake, libtool

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-1
- Update to upstream version 1.10

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-4
- Migrate BuildRequires from junit4 to junit

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-3
- Remove BuildRequires on maven-surefire-provider-junit4

* Thu Mar  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-2
- Update to ASM4
- Resolves: rhbz#1073507

* Wed Sep 18 2013 Marek Goldmann <mgoldman@redhat.com> - 1.9-1
- Upstream release 1.9
- hawtjni: missing barriers in cache initialization, RHBZ#957181

* Tue Aug 06 2013 Marek Goldmann <mgoldman@redhat.com> - 1.8-3
- New guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Marek Goldmann <mgoldman@redhat.com> - 1.8-1
- Upstream release 1.8

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-5
- Remove unneeded BR: maven-idea-plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.6-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-2
- Replace asm2 requires with objectweb-asm
- Resolves: rhbz#902674

* Fri Sep 07 2012 gil cattaneo <puntogil@libero.it> 1.6-1
- Upstream release 1.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-3
- Remove eclipse plugin from BuildRequires

* Thu Jan 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-2
- Replace plexus-maven-plugin with plexus-containers implementation

* Sun Jan 15 2012 Marek Goldmann <mgoldman@redhat.com> 1.5-1
- Upstream release 1.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Marek Goldmann <mgoldman@redhat.com> 1.3-1
- Upstream release 1.3

* Fri Jul 29 2011 Marek Goldmann <mgoldman@redhat.com> 1.2-1
- Upstream release 1.2
- Moved to new depmap macro

* Mon May 30 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-4
- Removed maven-shade-plugin dependency

* Mon May 30 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-3
- Split maven-hawtjni-plugin into new package
- Fixed license
- Fixed summary
- Using xz to compress source code

* Sun May 29 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-2
- Added maven-hawtjni-plugin

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-1
- Initial packaging
