%bcond_without bootstrap
Summary:        Tools to manage artifacts and deployment
Name:           maven-wagon
Version:        3.5.3
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://maven.apache.org/wagon
Source0:        https://repo1.maven.org/maven2/org/apache/maven/wagon/wagon/%{version}/wagon-%{version}-source-release.zip
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
Provides:       maven-wagon-file = %{version}-%{release}
Provides:       maven-wagon-http = %{version}-%{release}
Provides:       maven-wagon-http-shared = %{version}-%{release}
Provides:       maven-wagon-provider-api = %{version}-%{release}
Provides:       maven-wagon-providers = %{version}-%{release}
BuildArch:      noarch

%description
Maven Wagon is a transport abstraction that is used in Maven's
artifact and repository handling code. Currently wagon has the
following providers:
* File
* HTTP
* FTP
* SSH/SCP
* WebDAV
* SCM (in progress)

%{?javadoc_package}

%prep
%setup -q -n wagon-%{version}

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_dep :wagon-tck-http wagon-providers/wagon-http

# disable tests, missing dependencies
%pom_disable_module wagon-tcks
%pom_disable_module wagon-ssh-common-test wagon-providers
%pom_disable_module wagon-provider-test
%pom_remove_dep :wagon-provider-test
%pom_remove_dep :wagon-provider-test wagon-providers

# missing dependencies
%pom_disable_module wagon-ftp wagon-providers
%pom_disable_module wagon-http-lightweight wagon-providers
%pom_disable_module wagon-scm wagon-providers
%pom_disable_module wagon-ssh wagon-providers
%pom_disable_module wagon-ssh-common wagon-providers
%pom_disable_module wagon-ssh-external wagon-providers
%pom_disable_module wagon-webdav-jackrabbit wagon-providers

%pom_remove_plugin :maven-shade-plugin wagon-providers/wagon-http

%{mvn_file} ":wagon-{*}" %{name}/@1
%{mvn_package} ":wagon"

%build
# tests are disabled because of missing dependencies
%{mvn_build} -f

# Maven requires Wagon HTTP with classifier "shaded"
%{mvn_alias} :wagon-http :::shaded:

%install
%{mvn_install}

%files -f .mfiles
%license LICENSE NOTICE
%doc DEPENDENCIES

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.3-1
- Auto-upgrade to 3.5.3 - Azure Linux 3.0 - package upgrades

* Fri Mar 24 2023 Riken Maharjan <rmaharjan@microsoft.com> - 3.5.1-4
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- License verified

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 21 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.1-1
- Update to upstream version 3.5.1

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.4.2-6
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-3
- Obsolete removed subpackages

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-2
- Bootstrap build
- Non-bootstrap build

* Tue Feb 02 2021 Fabio Valentini <decathorpe@gmail.com> - 0:3.4.2-1
- Update to version 3.4.2.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:3.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec  4 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-1
- Update to upstream version 3.4.2

* Fri Sep 11 2020 Marian Koncek <mkoncek@redhat.com> - 3.4.1-1
- Update to upstream version 3.4.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:3.4.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Jun 08 2020 Fabio Valentini <decathorpe@gmail.com> - 0:3.4.1-1
- Update to version 3.4.1.

* Sat May 09 2020 Fabio Valentini <decathorpe@gmail.com> - 0:3.4.0-1
- Update to version 3.4.0.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:3.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.4-2
- Build with OpenJDK 8

* Thu Nov 21 2019 Marian Koncek <mkoncek@redhat.com> - 3.3.4-1
- Update to upstream version 3.3.4

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.3-2
- Mass rebuild for javapackages-tools 201902

* Sat Sep 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0:3.3.3-4
- Obsolete maven-wagon-ssh properly (#1752165)

* Thu Aug 29 2019 Fabio Valentini <decathorpe@gmail.com> - 0:3.3.3-3
- Disable SSH functionality.

* Fri Jul 12 2019 Fabio Valentini <decathorpe@gmail.com> - 0:3.3.3-2
- Disable SCM leaf subpackage to fix FTBFS on 32bit architectures.

* Wed Jul 10 2019 Marian Koncek <mkoncek@redhat.com> - 3.3.3-1
- Update to upstream version 3.3.3
- Remove dependency on maven-shade-plugin

* Fri Jun 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.2-3
- Disable ftp and http-lightweight providers

* Thu Jun 27 2019 Fabio Valentini <decathorpe@gmail.com> - 0:3.3.3-1
- Update to version 3.3.3.

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.2-2
- Mass rebuild for javapackages-tools 201901

* Wed Feb 27 2019 Marian Koncek <mkoncek@redhat.com> - 0:3.3.2-1
- Update to upstream version 3.3.2
- Fixes: RHBZ #1674068

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct  8 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.2.0-1
- Update to upstream version 3.2.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Michael Simacek <msimacek@redhat.com> - 0:3.1.0-1
- Update to upstream version 3.1.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.0.0-1
- Update to upstream version 3.0.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 0:2.10-3
- Add conditionals for ssh and scm
- Remove old requires from main package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.10-1
- Update to upstream version 2.10

* Wed Jul 08 2015 Michael Simacek <msimacek@redhat.com> - 0:2.9-4
- Remove unnecessary BuildRequires

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.9-2
- Disable webdav-jackrabbit provides

* Tue Apr 21 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.9-1
- Update to upstream version 2.9

* Wed Nov 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.8-1
- Update to upstream version 2.8

* Wed Sep 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-1
- Update to upstream version 2.7

* Thu Aug 21 2014 Michael Simacek <msimacek@redhat.com> - 0:2.6-10
- Enable webdav-jackrabbit module

* Mon Jun 30 2014 Michael Simacek <msimacek@redhat.com> - 0:2.6-9
- Obsolete main package instead of requiring it

* Fri Jun 27 2014 Michael Simacek <msimacek@redhat.com>
- Require main package from provider-api
- Fix maven-parent BR

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.6-6
- Rebuild to regenerate Maven auto-requires

* Thu Mar 06 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-5
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.6-4
- Add requires on all modules to main package

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 0:2.6-3
- Split into subpackages

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.6-2
- Fix unowned directory

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.6-1
- Update to upstream version 2.6

* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.5-2
- Add shaded alias for wagon-http

* Tue Sep 17 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.5-1
- Update to upstream version 2.5

* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3
- Disable unused wagon-provider-test module
- Resolves: rhbz#1002480

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Michal Srb <msrb@redhat.com> - 0:2.4-1
- Port to jetty 9

* Thu Feb 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-1
- Simplify build-requires

* Thu Feb 14 2013 Michal Srb <msrb@redhat.com> - 0:2.4-1
- Update to latest upstream 2.4
- Remove old depmap and patches
- Build with xmvn

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-6
- Remove BR: ganymed-ssh2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-4
- Fix build against jetty 8 and servlet 3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Jaromir Capik <jcapik@redhat.com> - 0:1.0-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata

* Wed Jul 27 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-1
- Update to 1.0 final.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.22
- Install wagon-providers depmap too.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.21
- Install wagon pom depmap.
- Use maven 3 for build.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.b7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b7.1
- Update to beta 7.
- Adapt to current guidelines.
- Fix pom names.

* Thu Sep 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b6.3
- Use javadoc:aggregate.
- Drop ant build.
- Use global instead of define.

* Fri May 14 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.2
- Create patch for wagon-http-shared pom.xml

* Wed May 12 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.1
- Update to beta 6, build with with_maven 1

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.7
- Remove gcj parts.

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.6
- Update to beta2 - sync with jpackage.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.2.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  1 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0:1.0-0.1.a5.3.5
- include missing dir below _docdir

* Fri Oct 03 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3.4
- added patch to make it compatible with the newer version of jsch

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.1.a5.3.3
- drop repotag
- fix license tag

* Sat Apr 05 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.2
- Rebuild with new version of jsch

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.1
- Merge in the changes neeeded to build without jetty
- Fix rpmlint issues
- Generate new *-build.xml files from pom.xml files as origins of
  *-project files is unknown.
- Remove maven1 project.xml files from sources
- Comment out various section requiring maven or javadocs
  (to be re-enabled at a future time). Note that the ant:ant task
  for maven2 does not currently generate javadocs.

* Tue Apr 04 2006 Ralph Apel <r.apel@r-apel.de> - 0:1.0-0.a5.3jpp
- Require j-c-codec, to build with j-c-httpclient = 3.0

* Thu Dec 22 2005 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a5.2jpp
- Commented out potentially superfluous dependencies.
- Disabled wagon-scm

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a5.1jpp
- First JPackage build
