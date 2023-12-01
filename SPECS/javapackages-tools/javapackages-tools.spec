# Don't generate requires on jpackage-utils and java-headless for
# provided pseudo-artifacts: com.sun:tools and sun.jdk:jconsole.
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}/maven-metadata/javapackages-metadata.xml$
# Disable automatic bytecode compilation for files in java-utils
# https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%global _python_bytecompile_extra 0
%global python_interpreter %{__python3}
%global rpmmacrodir %{_rpmconfigdir}/macros.d
Summary:        Macros and scripts for Java packaging support
Name:           javapackages-tools
Version:        6.0.0
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/fedora-java/javapackages
Source0:        https://github.com/fedora-java/javapackages/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         remove-epoch-from-java-requires.patch
Patch1:         remove-headless-from-java-requires.patch
# Bringing back deprecated macro because the newer alternatives
#  %mvn_artifact and %mvn_install require packages that are not yet supported
Patch2:         undeprecate_add_maven_depmap.patch
BuildRequires:  asciidoc
BuildRequires:  coreutils
BuildRequires:  msopenjdk-11
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-lxml
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  which
BuildRequires:  xmlto
%if %{with_check}
BuildRequires:  python3-pip
%endif
Requires:       coreutils
Requires:       findutils
# default JRE
Requires:       msopenjdk-11
Requires:       javapackages-filesystem = %{version}-%{release}
Requires:       which
Provides:       jpackage-utils = %{version}-%{release}
# These could be generated automatically, but then we would need to
# depend on javapackages-local for dependency generator.
Provides:       mvn(com.sun:tools) = SYSTEM
Provides:       mvn(sun.jdk:jconsole) = SYSTEM
BuildArch:      noarch

%description
This package provides macros and scripts to support Java packaging.

%package -n javapackages-filesystem
Summary:        Java packages filesystem layout
Provides:       eclipse-filesystem = %{version}-%{release}

%description -n javapackages-filesystem
This package provides some basic directories into which Java packages
install their content.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local-bootstrap = %{version}-%{release}
Requires:       xmvn-minimal
Requires:       xmvn-mojo
Requires:       xmvn-tools
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       maven-compiler-plugin
Requires:       maven-jar-plugin
Requires:       maven-resources-plugin
Requires:       maven-surefire-plugin
 
%description -n maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%package -n ivy-local-bootstrap
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local-bootstrap = %{version}-%{release}

%description -n ivy-local-bootstrap
This package implements local mode for Apache Ivy, which allows
artifact resolution using XMvn resolver.

%package -n python3-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       python3-lxml
Requires:       python3-six

%description -n python3-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n javapackages-local-bootstrap
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       msopenjdk-11
Requires:       python3
Requires:       python3-javapackages = %{version}-%{release}

%description -n javapackages-local-bootstrap
This package provides non-essential macros and scripts to support Java packaging.
It is a lightweight version with minimal runtime requirements.

%package -n javapackages-generators
Summary:        RPM dependency generators for Java packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       python3-javapackages = %{version}-%{release}
Requires:       %{python_interpreter}
 
%description -n javapackages-generators
RPM dependency generators to support Java packaging.

%prep
%autosetup -p1 -n javapackages-%{version}

%build
%define jdk_home $(find %{_libdir}/jvm -name "msopenjdk*")
%define jre_home %{jdk_home}/jre

%configure --pyinterpreter=%{python_interpreter} \
    --default_jdk=%{jdk_home} --default_jre=%{jre_home} \
    --rpmmacrodir=%{rpmmacrodir}
./build

%install
./install

sed -e 's/.[17]$/&*/' -i files-*

rm -rf %{buildroot}%{_bindir}/gradle-local
rm -rf %{buildroot}%{_datadir}/gradle-local
rm -rf %{buildroot}%{_mandir}/man7/gradle_build.7

%check
pip3 install -r test-requirements.txt
./check

%files -f files-tools

%files -n javapackages-filesystem -f files-filesystem

%files -n javapackages-generators -f files-generators

%files -n javapackages-local-bootstrap -f files-local

%files -n ivy-local-bootstrap -f files-ivy

%files -n maven-local

%files -n python3-javapackages -f files-python
%license LICENSE

%changelog
* Fri Mar 31 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 6.0.0-2
- Added maven-local subpackage

* Thu Feb 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 6.0.0-1
- Update source to v6.0.0
- Update remove-headless-from-java-requires.patch
- Add undeprecate_add_maven_depmap.patch to support legacy macros
    while we wait for maven to be fixed (so that the new macros can be used)
- Add javapackages-generators 

* Wed Jan 05 2022 Olivia Crain <oliviacrain@microsoft.com> - 5.3.0-14
- Add patch to replace generated dependency on "java-headless" with "java"
- Amend epoch patch to fix expected test results
- Remove obsoletes statements that don't apply to Mariner
- Install test requirements with pip during check section

* Thu Dec 02 2021 Andrew Phelps <anphel@microsoft.com> - 5.3.0-13
- Update to build with JDK 11
- License verified

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 5.3.0-12
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Wed Dec 09 2020 Joe Schmitt <joschmit@microsoft.com> - 5.3.0-11
- Add remove-epoch-from-java-requires.patch to remove epoch from java versions during dependency generation.

* Fri Nov 20 2020 Joe Schmitt <joschmit@microsoft.com> - 5.3.0-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Dynamically calculate jdk and jre paths.
- Remove meta packages.
- Simplify spec macro and bcond usage.
- Create bootstrap packages for ivy-local and javapackages-local with minimal runtime requirements.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.3.0-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 5.3.0-7
- Rebuilt for Python 3.8

* Sun Aug 11 2019 Fabio Valentini <decathorpe@gmail.com> - 5.3.0-6
- Disable gradle support by default.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-3
- Make it possible to build SRPM without python-devel installed

* Thu Oct  4 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-2
- Make javapackages-local require Python interpreter executable path

* Mon Aug 06 2018 Michael Simacek <msimacek@redhat.com> - 5.3.0-1
- Update to upstream version 5.3.0

* Thu Aug  2 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-6
- Switch auto-requires generator to javapackages-filesystem

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 5.2.0-4
- Rebuilt for Python 3.7

* Mon Jun 25 2018 Michael Simacek <msimacek@redhat.com> - 5.2.0-3
- Disable bytecode compilation outside of site-packages

* Wed Jun 20 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-2
- Fix running tests on Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.2.0-2
- Rebuilt for Python 3.7

* Tue Jun  5 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-1
- Update to upstream version 5.2.0

* Tue May 15 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.1.0-1
- Update to upstream version 5.1.0
- Introduce javapackages-filesystem package

* Wed May 02 2018 Michael Simacek <msimacek@redhat.com> - 5.0.0-13
- Backport abrt-java-connector changes

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.0.0-12
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Merlin Mathesius <mmathesi@redhat.com> - 5.0.0-10
- Cleanup spec file conditionals

* Sat Sep 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-9
- Conditionally allow building without asciidoc

* Thu Sep  7 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-8
- Allow manpages to be either compressed or not

* Thu Aug 17 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-7
- Fix traceback on corrupt zipfile
- Resolves: rhbz#1481005

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-5
- Conditionalize use of XMvn Javadoc MOJO

* Mon Jul 03 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-4
- Fix default JRE path

* Mon Jul 03 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-3
- Don't use xmvn javadoc for now

* Wed Jun 21 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-2
- Re-add dist-tag

* Wed Jun 21 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-2
- Remove xmvn version requirement

* Wed Jun 21 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-1
- Update to upstream version 5.0.0

* Tue Mar 14 2017 Michael Simacek <msimacek@redhat.com> - 4.7.0-16
- Force locale in test to fix failures

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-14
- Fix build without gradle

* Tue Jan 31 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-13
- Allow to conditionally build without gradle

* Tue Dec 20 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-12
- Non-bootstrap build

* Tue Dec 20 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-11
- Port to Python 3.6

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.7.0-10
- Rebuild for Python 3.6

* Fri Nov 18 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-9
- Add Requires on which
- Resolves: rhbz#1396395

* Mon Oct  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-8
- Fix generation of versioned OSGi requires

* Tue Sep 06 2016 Michael Simacek <msimacek@redhat.com> - 4.7.0-7
- Remove docs, which were split into java-packaging-howto

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-5
- Remove requires on maven-enforcer-plugin

* Tue Jun 28 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-4
- Require xmvn-minimal instead of full xmvn

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-3
- Drop requires on most of parent POMs

* Thu Mar 31 2016 Michal Srb <msrb@redhat.com> - 4.7.0-2
- Add R: findutils (Resolves: rhbz#1321401, thanks Tatsuyuki Ishi)

* Fri Mar 04 2016 Michal Srb <msrb@redhat.com> - 4.7.0-1
- Update to 4.7.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan  4 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-12
- Move mvn_build and builddep to javapackages-local
- Resolves: rhbz#1290399

* Wed Nov 11 2015 Kalev Lember <klember@redhat.com> - 4.6.0-11
- Disable bootstrap

* Wed Nov 11 2015 Kalev Lember <klember@redhat.com> - 4.6.0-10
- Add bootstrap macro (#1280209)
- Enable bootstrap for Python 3.5 rebuilds

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-8
- Backport %%gradle_build macro from 4.7.0-SNAPSHOT

* Mon Oct 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-7
- Don't generate requires on java-headless
- Resolves: rhbz#1272145

* Tue Jul 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-6
- Use %%license macro

* Fri Jul 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-5
- Add requires on java-devel to javapackages-local

* Tue Jun 30 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-4
- Remove jpackage-utils obsoletes

* Mon Jun 22 2015 Michal Srb <msrb@redhat.com> - 4.6.0-3
- Rebuild to fix provides

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Michal Srb <msrb@redhat.com> - 4.6.0-1
- Update to upstream version 4.6.0

* Thu Apr 23 2015 Michal Srb <msrb@redhat.com> - 4.5.0-3
- Fix "UnboundLocalError: local variable 'pom_requires' referenced before assignment"

* Tue Apr 21 2015 Michael Simacek <msimacek@redhat.com> - 4.5.0-2
- Remove fedora-review-plugin-java subpackage

* Thu Apr 09 2015 Michal Srb <msrb@redhat.com> - 4.5.0-1
- Update to upstream version 4.5.0

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.0-4
- Remove requires on plexus-tools-pom

* Tue Mar 24 2015 Michael Simacek <msimacek@redhat.com> - 4.4.0-3
- Handle non-utf-8 poms in pom_editor

* Mon Feb 16 2015 Michael Simacek <msimacek@redhat.com> - 4.4.0-2
- Write temporary XML file as UTF-8 in pom_editor

* Mon Feb 16 2015 Michal Srb <msrb@redhat.com> - 4.4.0-1
- Update to upstream version 4.4.0

* Fri Feb 13 2015 Michal Srb <msrb@redhat.com> - 4.3.2-6
- Fix TypeError in maven_depmap (see: rhbz#1191657)

* Thu Feb 12 2015 Michael Simacek <msimacek@redhat.com> - 4.3.2-5
- Workaround for XMvn version bump (rhbz#1191657)

* Fri Jan 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-4
- Add gradle-local subpackage
- Allow conditional builds with tests skipped

* Mon Jan 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-3
- Port to lua 5.3.0

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-2
- Replace all dashes with dots in versioned provides and requires

* Mon Jan 05 2015 Michal Srb <msrb@redhat.com> - 4.3.2-1
- Update to upstream version 4.3.2
- Fix TypeError in mvn_artifact

* Tue Dec 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.1-1
- Update to upstream version 4.3.1

* Sun Dec 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-1
- Update to upstream version 4.3.0

* Fri Nov 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-11
- Remove dependency on libxslt

* Fri Nov 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-10
- Scan lib64/ in OSGi dep generators
- Related: rhbz#1166156

* Wed Nov 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-9
- Revert adding namespace support in %%mvn_artifact

* Mon Nov 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-8
- Add namespace support in %%mvn_artifact

* Fri Nov 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-7
- Fix OSGi provides/requires generation in Java libdir
- Resolves: rhbz#1166156

* Wed Nov 12 2014 Michal Srb <msrb@redhat.com> - 4.2.0-6
- Fix cache problem (Resolves: rhbz#1155185)

* Thu Oct 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-5
- Use wrapper script to inject ABRT agent JVM argument
- Fix path to ABRT agent DSO
- Resolves: rhbz#1153652

* Tue Oct 21 2014 Michael Simacek <msimacek@redhat.com> - 4.2.0-4
- Fix pom_editor missing space between xmlns declarations

* Wed Sep 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-3
- Do not generate OSGi R on eclipse-platform

* Thu Sep 18 2014 Michal Srb <msrb@redhat.com> - 4.2.0-2
- Fix mvn_artifact: generate R, if it's not explicitly disabled

* Thu Jul 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-1
- Update to upstream version 4.2.0

* Thu Jul 10 2014 Michal Srb <msrb@redhat.com> - 4.1.0-2
- Backport upstream patch for maven.req

* Mon Jun 23 2014 Michal Srb <msrb@redhat.com> - 4.1.0-1
- Update to upstream version 4.1.0

* Thu Jun 12 2014 Michal Srb <msrb@redhat.com> - 4.0.0-8
- Install man page for pom_change_dep

* Tue Jun 10 2014 Michal Srb <msrb@redhat.com> - 4.0.0-7
- Backport fix for maven.prov

* Tue Jun 10 2014 Michal Srb <msrb@redhat.com> - 4.0.0-6
- Update docs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Michal Srb <msrb@redhat.com> - 4.0.0-4
- Backport patch which adds support for "disableEffectivePom" property

* Thu May 29 2014 Michal Srb <msrb@redhat.com> - 4.0.0-3
- Add BR: javapackages-tools

* Thu May 29 2014 Michal Srb <msrb@redhat.com> - 4.0.0-2
- Backport patches for maven.req
- Remove com.sun:tools and sun.jdk:jconsole provides

* Thu May 29 2014 Michal Srb <msrb@redhat.com> - 4.0.0-1
- Update to 4.0.0

* Wed May 28 2014 Michal Srb <msrb@redhat.com> - 3.5.0-9
- Apply the patch from my previous commit

* Wed May 28 2014 Michal Srb <msrb@redhat.com> - 3.5.0-8
- Generate requires on POM artifacts with "pom" extension

* Wed Apr 30 2014 Michal Srb <msrb@redhat.com> - 3.5.0-7
- Improve support for SCLs

* Wed Apr 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-6
- Add explicit maven-local requires on java-1.8.0-openjdk-devel

* Thu Mar 27 2014 Michael Simacek <msimacek@redhat.com> - 3.5.0-6
- Install documentation

* Mon Feb 24 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.5.0-5
- Backport java-headless patches

* Mon Feb 10 2014 Michal Srb <msrb@redhat.com> - 3.5.0-4
- Add support for installing Maven artifacts with .hpi extension

* Fri Jan 17 2014 Michael Simacek <msimacek@redhat.com> - 3.5.0-3
- Use upstream method of running tests (nosetests)

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-2
- Add version requirements on xmvn and ivy

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-1
- Update to upstream version 3.5.0
- Add ivy-local subpackage

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-3
- Update patch for ZIP files

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-2
- Allow ZIP files in %%{_javadir}

* Thu Dec 05 2013 Michal Srb <msrb@redhat.com> - 3.4.2-1
- Update to upstream bugfix release 3.4.2

* Wed Dec  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.1-3
- Add Requires on objectweb-pom

* Tue Nov 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.1-2
- Do not create parent dirs for pom.properties
- Resolves: rhbz#1031769

* Tue Nov 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.1-1
- Update to upstream bugfix release 3.4.1

* Mon Oct 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-3
- Fix XMvn configuration for native JNI repos
- Resolves: rhbz#1021608

* Mon Oct 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-2
- Require exact version of python-javapackages

* Mon Oct 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-1
- Update to upstream version 3.4.0

* Wed Oct  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-1
- Update to upstream version 3.3.1
- Remove workaround for sisu-guice no_aop

* Tue Oct 01 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.3.0-1
- Update to upstream version 3.3.0

* Wed Sep 25 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-2
- Fix installation of artifacts with classifier

* Tue Sep 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-1
- Update to upstream version 3.2.4

* Tue Sep 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.3-1
- Update to upstream version 3.2.3

* Fri Sep 20 2013 Michal Srb <msrb@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Update to upstream version 3.2.1

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-1
- Update to upstream version 3.1.2

* Thu Sep 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.1-1
- Update to upstream version 3.1.1

* Thu Sep 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.0-1
- Update to upstream version 3.1.0

* Mon Sep 16 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-2
- Add depmap for sun.jdk:jconsole

* Fri Sep 13 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-1
- Update to upstream version 3.0.4

* Wed Sep 11 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-1
- Update to upstream version 3.0.3

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-3
- Fix a typo in temporary depmap

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-2
- Make sure we do not provide google guice mapping

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.2-1
- Update to upstream version 3.0.2
- Add separate python-javapackages subpackage
- Add separate fedora-review-plugin-java subpackage
- Enable part of unit tests

* Tue Sep  3 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.0-0.2
- Fix javadoc directory override

* Tue Sep  3 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.0-0.1
- Update to upstream pre-release version 3.0.0

* Fri Jul 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.1-1
- Update to upstream version 2.0.1
- Fix creation of artifact aliases, resolves: rhbz#988462

* Thu Jul 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-2
- Require maven-resources-plugin by maven-local

* Thu Jul 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-1
- Update to upstream version 2.0.0
- Merge functionality of jpackage-utils
- Provide and obsolete jpackage-utils
- %%add_maven_depmap macro now injects pom.properties to every JAR
- %%add_to_maven_depmap and %%update_maven_depmap macros were removed
- maven2jpp-mapdeps.xsl template has been removed
- Macros related to installation of icons and desktop files were removed
- 14 new manual pages were added
- Documentation specific to JPackage was removed
- Add BuildRequires: asciidoc, xmlto

* Mon Jul  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.15.0-2
- Add R: jvnet-parent

* Wed Jun  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.15.0-1
- Update to upstream version 0.15.0
- Added depmap for tools.jar
- Added support for versioned autorequires
- New plugin metadata from Maven Central

* Tue Jun  4 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.14.1-2
- Add several maven plugins to maven-local requires

* Wed May 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.14.1-1
- Update to upstream version 0.14.1 with disabled debugging

* Tue Apr 09 2013 Michal Srb <msrb@redhat.com> - 0.14.0-1
- Update to upstream version 0.14.0

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.7-2
- Add R: maven-surefire-provider-junit4 to maven-local

* Fri Mar 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.7-1
- Update to upstream version 0.13.7

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-4
- Add geronimo-parent-poms to common POMs

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-3
- Add weld-parent to common POMs

* Wed Mar 20 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.13.6-2
- Fix conditional macro to evaluate properly when fedora is not defined

* Mon Mar 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-1
- Update to upstream version 0.13.6

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.5-1
- Update to upstream version 0.13.5

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.4-1
- Update to upstream version 0.13.4

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.3-1
- Update to upstream version 0.13.3

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.2-1
- Update to upstream version 0.13.2

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.1-1
- Update to upstream version 0.13.1

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.0-1
- Update to upstream version 0.13.0

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.0-0.1.git2f13366
- Upate to upstream pre-release snapshot 2f13366

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.6-1
- Update to upstream version 0.12.6
- Resolves: rhbz#917618 (remove jetty orbit provides)
- Resolves: rhbz#917647 (system.bundle into autogenerated deps)

* Fri Mar  1 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.12.5-1
- Update to upstream version 0.12.5
- Resolves problems with compat package provides and automatic requires

* Wed Feb 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.4-2
- Don't mark RPM macro files as configuration

* Mon Feb 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.4-1
- Update to upstream version 0.12.4
- Resolves: rhbz#913630 (versioned requires between subpackages)

* Fri Feb 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.3-1
- Update to upstream version 0.12.3
- Resolves: rhbz#913694 (No plugin found for prefix 'X')

* Wed Feb 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.2-1
- Update to upstream version 0.12.2
- Resolves: rhbz#913120 (MAVEN_OPTS are not passed to Maven)

* Mon Feb 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.1-1
- Update to upstream version 0.12.1
- Resolves: rhbz#912333 (M2_HOME is not exported)

* Fri Feb 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.0-1
- Update to upstream version 0.12.0
- Implement new pom macros: xpath_replace and xpath_set
- Remove Support-local-depmaps.patch (accepted upstream)

* Fri Feb 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-6
- Support local depmaps

* Thu Feb 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-5
- Add some maven-local Requires for convenience

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-4
- Add missing R: httpcomponents-project

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-3
- Add missing R: jboss-patent

* Wed Feb  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-2
- Don't install mvn-local and mvn-rpmbuild on F18

* Wed Jan 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-1
- Update to upstream version 0.11.2

* Wed Jan 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.1-1
- Update to upstream version 0.11.1

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.0-1
- Update to upstream version 0.11.0
- Add mvn-local and mvn-rpmbuild scripts

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.1-1
- Update to upstream version 0.10.1

* Mon Jan  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.0-1
- Update to upstream version 0.10.0
- Implement %%xmvn_alias, %%xmvn_file and %%xmvn_package macros
- Fix regex in osgi.attr
- Add support for pre- and post-goals in mvn-build script

* Mon Dec 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.1-1
- Update to upstream version 0.9.1
- Resolves: rhbz#885636

* Thu Dec  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.0-1
- Update to latest upstream version
- Enable maven requires generator for xmvn packages
- Enable requires generator for javadoc packages

* Wed Dec  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.3-1
- Update to upstream version 0.8.3
- Fix maven provides generator for new XML valid fragments

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.2-1
- Update to upstream version 0.8.2

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.1-1
- Update to upstream version 0.8.1

* Wed Nov 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.0-1
- Update to upstream version 0.8.0
- Add xmvn macros

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-3
- Add BR: jpackage-utils

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-2
- Add maven-local subpackage

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.5-1
- Fix versioned pom installation by quoting _jpath

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.4-1
- Shorten maven filelist filenames

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.3-1
- Update to upstream version 0.7.3

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.2-1
- Make sure add_maven_depmap fails when python tracebacks

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.1-1
- Fix problem with exception in default add_maven_depmap invocation

* Tue Oct 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.0-1
- Update to latest upstream
- Full support for compat depmap generation
- Generate maven-files-%%{name} with a list of files to package
- Add support for maven repo generation (alpha version)

* Mon Jul 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.6.0-1
- Update to upstream version 0.6.0
- Make maven provides versioned
- Add additional pom_ macros to simplify additional pom editing

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-1
- Update to upstream version 0.5.0 - add support for add_maven_depmap -v

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.1-1
- Update to upstream version 0.4.1
- Fixes #837203

* Wed Jun 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-1
- Update to upstream version 0.4.0

* Tue Mar  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.1-1
- Create maven provides from fragments instead of poms

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-3
- Fix maven_depmap installation

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-2
- Add conflicts with older jpackage-utils

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-1
- Initial version split from jpackage-utils
