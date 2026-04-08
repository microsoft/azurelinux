# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without httpclient
%bcond_without oro
%bcond_without vfs
%bcond_without sftp

%global jarname ivy

Name:           apache-%{jarname}
Version:        2.5.3
Release:        1%{?dist}
Summary:        Java-based dependency manager
License:        Apache-2.0
URL:            https://ant.apache.org/ivy
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/ant/%{jarname}/%{version}/%{name}-%{version}-src.tar.gz
Source1:        https://archive.apache.org/dist/ant/%{jarname}/%{version}/%{name}-%{version}-src.tar.gz.asc
Source2:        https://archive.apache.org/dist/ant/KEYS

# Non-upstreamable.  Add /etc/ivy/ivysettings.xml at the end list of
# settings files Ivy tries to load.  This file will be used only as
# last resort, when no other setting files exist.
Source3:         00-global-settings.patch

BuildRequires:  gnupg2
BuildRequires:  ant-openjdk21
BuildRequires:  ivy-local
BuildRequires:  dos2unix
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.bouncycastle:bcpg-jdk18on)
BuildRequires:  mvn(org.bouncycastle:bcprov-jdk18on)

%if %{with httpclient}
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
%endif

%if %{with oro}
BuildRequires:  mvn(oro:oro)
%endif

%if %{with vfs}
BuildRequires:  mvn(org.apache.commons:commons-vfs2)
%endif

%if %{with sftp}
BuildRequires:  mvn(com.jcraft:jsch)
BuildRequires:  mvn(com.jcraft:jsch.agentproxy.connector-factory)
BuildRequires:  mvn(com.jcraft:jsch.agentproxy.jsch)
%endif

Provides:       ivy = %{version}-%{release}

Source4: IMPROVEMENT-use-Apache-Commons-Compress-for-pack200-.patch
Source5: remove-Pack200Packing-java.patch
%description
Apache Ivy is a tool for managing (recording, tracking, resolving and
reporting) project dependencies.  It is designed as process agnostic and is
not tied to any methodology or structure. while available as a standalone
tool, Apache Ivy works particularly well with Apache Ant providing a number
of powerful Ant tasks ranging from dependency resolution to dependency
reporting and publication.

%{?javadoc_package}

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup
dos2unix src/java/org/apache/ivy/ant/IvyAntSettings.java asciidoc/release-notes.adoc ivy.xml optional.patterns src/java/org/apache/ivy/core/pack/PackagingManager.java src/java/org/apache/ivy/core/pack/PackingRegistry.java src/java/org/apache/ivy/core/settings/IvySettings.java src/java/org/apache/ivy/core/pack/ArchivePacking.java src/java/org/apache/ivy/core/pack/OsgiBundlePacking.java src/java/org/apache/ivy/core/pack/Pack200Packing.java src/java/org/apache/ivy/core/pack/StreamPacking.java src/java/org/apache/ivy/core/pack/ZipPacking.java src/java/org/apache/ivy/util/FileUtil.java test/java/org/apache/ivy/core/retrieve/RetrieveTest.java test/java/org/apache/ivy/core/pack/ZipPackingTest.java version.properties
patch -p1 -l < %{SOURCE3}
patch -p1 -l < %{SOURCE4}
patch -p1 -l < %{SOURCE5}
# Don't hardcode sysconfdir path
sed -i 's:/etc/ivy/:%{_sysconfdir}/ivy/:' src/java/org/apache/ivy/ant/IvyAntSettings.java
# remove BOM
%pom_remove_dep :jsch.agentproxy
# remove test deps
%pom_remove_dep junit:junit
%pom_remove_dep org.hamcrest:hamcrest-core
%pom_remove_dep org.hamcrest:hamcrest-library
%pom_remove_dep org.apache.ant:ant-testutil
%pom_remove_dep org.apache.ant:ant-junit
%pom_remove_dep org.apache.ant:ant-junit4
%pom_remove_dep ant-contrib:ant-contrib
%pom_remove_dep xmlunit:xmlunit
# change jdk15on to jdk18on
%pom_change_dep :bcpg-jdk15on :bcpg-jdk18on
%pom_change_dep :bcprov-jdk15on :bcprov-jdk18on
# optional dep: httpclient
%if %{without httpclient}
# remove all httpclient related dep(s)
%pom_remove_dep :httpclient
# remove file(s) related to httpclient
rm src/java/org/apache/ivy/util/url/HttpClientHandler.java
%endif
# optional dep: oro
%if %{without oro}
# remove all oro related dep(s)
%pom_remove_dep :oro
# remove file(s) related to oro
rm src/java/org/apache/ivy/plugins/matcher/GlobPatternMatcher.java
%endif
# optional dep: vfs
%if %{without vfs}
# remove all vfs related dep(s)
%pom_remove_dep :commons-vfs2
# remove file(s) related to vfs
rm src/java/org/apache/ivy/plugins/repository/vfs/VfsRepository.java
rm src/java/org/apache/ivy/plugins/repository/vfs/VfsResource.java
rm src/java/org/apache/ivy/plugins/repository/vfs/ivy_vfs.xml
rm src/java/org/apache/ivy/plugins/resolver/VfsResolver.java
%endif
# optional dep: sftp
%if %{without sftp}
# remove all sftp related dep(s)
%pom_remove_dep :jsch
%pom_remove_dep :jsch.agentproxy
%pom_remove_dep :jsch.agentproxy.connector-factory
%pom_remove_dep :jsch.agentproxy.jsch
# remove file(s) related to sftp
rm src/java/org/apache/ivy/plugins/repository/sftp/SFTPRepository.java
rm src/java/org/apache/ivy/plugins/repository/sftp/SFTPResource.java
rm src/java/org/apache/ivy/plugins/repository/ssh/AbstractSshBasedRepository.java
rm src/java/org/apache/ivy/plugins/repository/ssh/RemoteScpException.java
rm src/java/org/apache/ivy/plugins/repository/ssh/Scp.java
rm src/java/org/apache/ivy/plugins/repository/ssh/SshCache.java
rm src/java/org/apache/ivy/plugins/repository/ssh/SshRepository.java
rm src/java/org/apache/ivy/plugins/repository/ssh/SshResource.java
rm src/java/org/apache/ivy/plugins/resolver/AbstractSshBasedResolver.java
rm src/java/org/apache/ivy/plugins/resolver/SFTPResolver.java
rm src/java/org/apache/ivy/plugins/resolver/SshResolver.java
%endif
# compatibility
%mvn_file : %{name}/ivy ivy
# remove prebuilt documentation
rm -rf asciidoc
# publish artifacts through xmvn
%pom_xpath_set ivy:publish/@resolver xmvn build.xml

%build
# create custom ant configuration
mkdir -p ~/.ant
cp /etc/ant.conf ~/.ant
sed -i '$a JAVA_HOME=/usr/lib/jvm/java-21-openjdk' ~/.ant/ant.conf

ant -Divy.mode=local \
    -f build-release.xml \
    release-version jar javadoc publish-local

%install
%mvn_install -J build/reports/api
# create ant deps
mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "apache-ivy/ivy" > %{buildroot}%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles
%license LICENSE NOTICE
%doc README.adoc
%{_sysconfdir}/ant.d/%{name}

%changelog
* Mon Jul 28 2025 jiri vanek <jvanek@redhat.com> - 2.5.2-9
- Rebuilt for java-25-openjdk as preffered jdk
- removed useless jdk11
- downgraded back to jdk21

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 28 2024 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.2-6
- Changed jdk15on to jdk18on

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.5.2-4
- Rebuilt for java-21-openjdk as system jdk

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 08 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.2-1
- Update to version 2.5.2

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.1-5
- Replace BR maven-local-openjdk11 w/ java-11-devel
- Use pom_xpath_set macro to publish artifacts

* Thu Jul 13 2023 Jerry James <loganjerry@gmail.com> - 2.5.1-4
- Enable vfs support

* Sun Jun 25 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.1-3
- Build with ivy instead of maven

* Sat Apr 29 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.1-2
- migrated to SPDX license

* Wed Feb 22 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.1-1
- Update to version 2.5.1
- Remove alias for jayasoft:ivy

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.5.0-11
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.5.0-10
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.0-8
- Enable ssh support

* Wed Dec 01 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.0-7
- Change BR: maven-local-openjdk11

* Wed Nov 17 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.0-6
- Re-add global settings

* Sat Oct 02 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.0-5
- Enable httpclient and oro

* Fri Oct 01 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.5.0-4
- Fix FTBFS (Resolves: #1987365)
- Rebuild with maven

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 13 2020 Fabio Valentini <decathorpe@gmail.com> - 2.5.0-1
- Update to version 2.5.0.
- Disable running the very very broken test suite.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.4.0-22
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-21
- bumped minimal sources/target to 1.6
- changed javadoc to palceholder. The javadoc build fails, but it looks like it is not affecting thebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Fabio Valentini <decathorpe@gmail.com> - 2.4.0-19
- Drop unnecessary dependencies on parent POMs.

* Wed Aug 14 2019 Fabio Valentini <decathorpe@gmail.com> - 2.4.0-18
- Disable ssh, bouncycastle, and vfs support.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Marian Koncek <mkoncek@redhat.com> - 2.4.0-15
- Enabled tests during build and disabled few failing tests
- Resolves: rhbz#1055418

* Tue Jul 17 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-14
- Allow building without vfs support

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 28 2018 Michael Simacek <msimacek@redhat.com> - 2.4.0-12
- Remove now unneeded patch

* Fri Mar 16 2018 Michael Simacek <msimacek@redhat.com> - 2.4.0-11
- Fix build against ant 1.10.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-8
- Don't hardcode sysconfdir path

* Tue Feb 14 2017 Michael Simacek <msimacek@redhat.com> - 2.4.0-7
- Add conditional for bouncycastle

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.4.0-6
- Add conditional for ssh

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Michal Srb <msrb@redhat.com> - 2.4.0-3
- Update comment

* Mon May 04 2015 Michal Srb <msrb@redhat.com> - 2.4.0-2
- Port to bouncycastle 1.52

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-1
- Update to upstream version 2.4.0

* Fri Sep 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-17
- Add compat symlink for ivy.jar

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-16
- Add alias for jayasoft:ivy

* Thu Jun 26 2014 Michal Srb <msrb@redhat.com> - 2.3.0-15
- Drop workaround for broken apache-ivy

* Thu Jun 26 2014 Michal Srb <msrb@redhat.com> - 2.3.0-14
- Fix /etc/ant.d/apache-ivy (Resolves: rhbz#1113275)

* Mon Jun 23 2014 Michal Srb <msrb@redhat.com> - 2.3.0-13
- Add BR on missing parent POMs

* Mon Jun 09 2014 Michal Srb <msrb@redhat.com> - 2.3.0-12
- Add missing BR: apache-commons-lang

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-10
- Use features of XMvn 2.0.0

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-9
- BuildRequire ivy-local >= 3.5.0-2

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-8
- Build with ivy-local
- Add patch for global settings

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.0-7
- Remove prebuilt documentation in %%prep
- Install NOTICE file with javadoc subpackage

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.0-6
- Restore PGP signing ability
- Remove unneeded R

* Thu Dec 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-5
- Enable VFS resolver

* Wed Dec  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4
- Install POM files, resolves: rhbz#1032258
- Remove explicit requires; auto-requires are in effect now

* Fri Nov  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-3
- Add Maven depmap

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 1 2013 Alexander Kurtakov <akurtako@redhat.com> 2.3.0-1
- Update to latest upstream.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-5
- Fix osgi metadata.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-2
- Fix ant integration.

* Fri Feb 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-1
- Update to 2.2.0.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.0-1
- Initial Fedora packaging
