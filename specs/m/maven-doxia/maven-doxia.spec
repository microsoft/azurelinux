# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           maven-doxia
Epoch:          0
Version:        2.0.0
Release: 4%{?dist}
Summary:        Content generation framework
License:        Apache-2.0

URL:            https://maven.apache.org/doxia/
VCS:            git:https://github.com/apache/maven-doxia.git
Source0:        https://repo1.maven.org/maven2/org/apache/maven/doxia/doxia/%{version}/doxia-%{version}-source-release.zip
Source1:        https://repo1.maven.org/maven2/org/apache/maven/doxia/doxia/%{version}/doxia-%{version}-source-release.zip.asc
Source2:        https://downloads.apache.org/maven/KEYS

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  gnupg2
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-abbreviation)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-autolink)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-definition)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-escaped-character)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-footnotes)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-gfm-strikethrough)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-tables)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-typographic)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-wikilink)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-ext-yaml-front-matter)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-util-ast)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-util-data)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-util-misc)
BuildRequires:  mvn(com.vladsch.flexmark:flexmark-util-sequence)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-text)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-surefire-plugin)
BuildRequires:  mvn(org.apiguardian:apiguardian-api)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-testing)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.jetbrains:annotations)
BuildRequires:  mvn(org.junit:junit-bom:pom:)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(org.xmlunit:xmlunit-core)
BuildRequires:  mvn(org.xmlunit:xmlunit-matchers)

# This can be removed when F45 reaches EOL
Obsoletes:      %{name}-logging-api < 1.13.0
Provides:       %{name}-logging-api = %{version}-%{release}
Obsoletes:      %{name}-module-confluence < 1.13.0
Provides:       %{name}-module-confluence = %{version}-%{release}
Obsoletes:      %{name}-module-docbook-simple < 1.13.0
Provides:       %{name}-module-docbook-simple = %{version}-%{release}
Obsoletes:      %{name}-module-fo < 1.13.0
Provides:       %{name}-module-fo = %{version}-%{release}
Obsoletes:      %{name}-module-latex < 1.13.0
Provides:       %{name}-module-latex = %{version}-%{release}
Obsoletes:      %{name}-module-rtf < 1.13.0
Provides:       %{name}-module-rtf = %{version}-%{release}
Obsoletes:      %{name}-module-twiki < 1.13.0
Provides:       %{name}-module-twiki = %{version}-%{release}
Obsoletes:      %{name}-module-xhtml < 1.13.0
Provides:       %{name}-module-xhtml = %{version}-%{release}
Obsoletes:      %{name}-tests < 1.13.0
Provides:       %{name}-tests = %{version}-%{release}

%global _desc %{expand:
Doxia is a content generation framework which aims to provide its users
with powerful techniques for generating static and dynamic content.
Doxia can be used to generate static sites in addition to being
incorporated into dynamic content generation systems like blogs, wikis
and content management systems.}

%description %_desc

%package        core
Summary:        Core classes and interfaces for %{name}
Requires:       %{name}-sink-api = %{version}-%{release}

%description    core %_desc

This package contains the core classes and interfaces for %{name}.

%package        modules
Summary:        Doxia modules for several markup languages
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-sink-api = %{version}-%{release}

%description    modules %_desc

This package provides doxia modules for several markup languages.

%package        module-apt
Summary:        Almost Plain Text module for %{name}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-sink-api = %{version}-%{release}

%description    module-apt %_desc

This package contains a doxia module for Almost Plain Text (APT) source
documents.  APT format is supported both as source and target formats.

%package        module-fml
Summary:        FML module for %{name}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-sink-api = %{version}-%{release}

%description    module-fml %_desc

This package contains a doxia module for FML source documents.  FML
format is only supported as a source format.

%package        module-markdown
Summary:        Markdown module for %{name}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-module-xhtml5 = %{version}-%{release}
Requires:       %{name}-sink-api = %{version}-%{release}

%description    module-markdown %_desc

This package contains a doxia module for Markdown source documents.

%package        module-xdoc
Summary:        Xdoc module for %{name}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-sink-api = %{version}-%{release}

%description    module-xdoc %_desc

This package contains a doxia module for Xdoc source documents.  Xdoc
format is supported both as source and target formats.

%package        module-xhtml5
Summary:        XHTML5 module for %{name}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-sink-api = %{version}-%{release}

%description    module-xhtml5 %_desc

This package contains a doxia module for XHTML5 source documents.
XHTML5 format is supported both as source and target formats.

%package        sink-api
Summary:        Sink API for %{name}

%description    sink-api %_desc

This package contains the sink API for %{name}.  The supported output
document formats are accessed via this API.

%package        test-docs
Summary:        Test documents for %{name}

%description    test-docs %_desc
This package contains several test documents to check syntax structures
under Doxia.

%package        javadoc
# Apache-2.0: the content
# MIT: jquery and jquery-ui
# GPL-2.0-only: script.js, search.js, jquery-ui.overrides.css
License:        Apache-2.0 AND MIT AND GPL-2.0-only WITH Classpath-exception-2.0
Summary:        API documentation for %{name}

%description    javadoc
API documentation for %{name}.

%prep
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}
%autosetup -p1 -n doxia-%{version}

# Convert to Unix line terminators
for f in $(find . -name '*.java' -o -name '*.xml'); do
  sed -i.orig 's/\r//' $f
  touch -r $f.orig $f
  rm -f $f.orig
done

# Plugins not needed for an RPM build
%pom_remove_plugin org.apache.maven.plugins:maven-scm-publish-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-site-plugin
%pom_remove_plugin org.apache.rat:apache-rat-plugin
%pom_remove_plugin org.codehaus.mojo:clirr-maven-plugin
%pom_remove_plugin :maven-install-plugin doxia-modules/doxia-module-markdown

# Needed for the tests
%pom_add_dep org.apiguardian:apiguardian-api:1.1.2:test

# we don't have maven-clean-plugin or maven-site-plugin
%pom_xpath_remove '//pom:goals' doxia-modules/doxia-module-markdown

# requires network
rm doxia-core/src/test/java/org/apache/maven/doxia/util/XmlValidatorTest.java

%build
%mvn_build -s

%install
%mvn_install

%files -f .mfiles-doxia
%doc README.md
%license LICENSE NOTICE
%files core -f .mfiles-doxia-core
%license LICENSE NOTICE
%files module-apt -f .mfiles-doxia-module-apt
%files module-fml -f .mfiles-doxia-module-fml
%files module-markdown -f .mfiles-doxia-module-markdown
%files modules -f .mfiles-doxia-modules
%files module-xdoc -f .mfiles-doxia-module-xdoc
%files module-xhtml5 -f .mfiles-doxia-module-xhtml5
%files sink-api -f .mfiles-doxia-sink-api
%files test-docs -f .mfiles-doxia-test-docs
%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 0:2.0.0-3
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 28 2025 Jerry James <loganjerry@gmail.com> - 0:2.0.0-1
- Version 2.0.0
- Drop all patches
- Drop many modules no longer provided by upstream

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.12.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 0:1.12.0-7
- Rebuilt for java-21-openjdk as system jdk

* Tue Feb 06 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.0-6
- Fix build with plexus-containers 2.2.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 30 2023 Jerry James <loganjerry@gmail.com> - 0:1.12.0-3
- Enable markdown support
- Build for Java 8 at a minimum

* Wed Jul 19 2023 Jerry James <loganjerry@gmail.com> - 0:1.12.0-2
- Enable fop support

* Sat Jun 10 2023 Jerry James <loganjerry@gmail.com> - 0:1.12.0-1
- Version 1.12.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Jerry James <loganjerry@gmail.com> - 0:1.11.1-3
- Convert License tag to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0:1.11.1-2
- Rebuilt for Drop i686 JDKs

* Wed Jun  8 2022 Jerry James <loganjerry@gmail.com> - 0:1.11.1-1
- Version 1.11.1
- Drop old obsoletes
- Verify sources with gpg
- Minor spec file cleanups

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0:1.9.1-7
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:1.9.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu May 07 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.9.1-1
- Update to version 1.9.1.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Fabio Valentini <decathorpe@gmail.com> - 0:1.9-3
- Disable fop support.

* Wed Sep 25 2019 Fabio Valentini <decathorpe@gmail.com> - 0:1.9-2
- Conditionally Obsolete maven-doxia-module-itext.

* Wed Sep 18 2019 Marian Koncek <mkoncek@redhat.com> - 0:1.9-1
- Update to upstream version 1.9
- Obsolete markdown module

* Tue Sep 03 2019 Fabio Valentini <decathorpe@gmail.com> - 0:1.7-12
- Disable itext support.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Michael Simacek <msimacek@redhat.com> - 0:1.7-9
- Disable failing test for now

* Tue Jul 17 2018 Michael Simacek <msimacek@redhat.com> - 0:1.7-8
- Regenerate BuildRequires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-4
- Don't require log4j12 unless built with FOP

* Mon Jul 03 2017 Michael Simacek <msimacek@redhat.com> - 0:1.7-3
- Add missing BR on log4j

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 0:1.7-2
- Add conditional for fop

* Mon May 02 2016 Michael Simacek <msimacek@redhat.com> - 0:1.7-1
- Update to upstream version 1.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 18 2015 Michael Simacek <msimacek@redhat.com> - 0:1.6-4
- Port to fop-2.0
- Cleanup bundled class from sitetools

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6-2
- Rebuild for fop update

* Thu Jul 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6-1
- Update to upstream version 1.6

* Wed Jun 11 2014 Michael Simacek <msimacek@redhat.com> - 0:1.5-7
- Change BR classworlds to plexus-classworlds

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-5
- Build-require pegdown >= 1.4.2-2

* Wed Mar 26 2014 Michal Srb <msrb@redhat.com> - 0:1.5-4
- Disable bad tests which rely on ordering in set

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.5-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-2
- Fix unowned directory

* Tue Dec 10 2013 Michael Simacek <msimacek@redhat.com> - 0:1.5-1
- Update to upstream version 1.5
- Move back RenderingContext.java that was moved to doxia-sitetools which
  doesn't have a release yet

* Thu Dec  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6
- BuildRequire plexus-containers-container-default 1.5.5-14
- Resolves: rhbz#1036584

* Mon Nov 25 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-5
- Rebuild after itext versioned jar fixed

* Thu Nov  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-4
- Port to Commons Collections 1.10

* Wed Nov  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-3
- Enable tests

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Michal Srb <msrb@redhat.com> - 0:1.4-1
- Update to upstream version 1.4
- Enable markdown module
- Remove unneeded patch

* Tue Apr 23 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.3-3
- Remove ant-nodeps BuildRequires

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-2
- Conditionally disable itext module

* Tue Mar 19 2013 Michal Srb <msrb@redhat.com> - 0:1.3-1
- Update to upstream version 1.3
- Remove temporary dependencies on subpackages

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-9
- Remove runtime requirement on POM: httpcomponents-project

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.2-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Dec 20 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-8
- Add httpcomponents-project to doxia-core requires

* Thu Dec 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-7
- Temporarly require all subpackages in the main package

* Wed Dec 19 2012 Michal Srb <msrb@redhat.com>
- Splitted into multiple subpackages (Resolves: #888710)

* Mon Dec 10 2012 Michal Srb <msrb@redhat.com> - 0:1.2-5
- Migrated to plexus-components-component-default (Resolves: #878553)
- Removed custom depmap and its occurrence in spec file
- Fixed various rpmlint warnings

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-3
- Remove plexus-xmlrpc from BR
- Update patches to work without plexus-maven-plugin

* Fri May  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-2
- Add forgotten missing requires

* Fri May  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-1
- Update to latest upstream (1.2)
- Use maven 3 to build
- Remove version limits on BR/R (not valid anymore anyway)
- Remove "assert" patch (no explanation for it's existence)

* Tue Feb 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.4-3
- Change oro to jakarta-oro in BR/R

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.4-1
- Update to 1.1.4
- Migrate from tomca5 to tomca6
- Versionless jars and javadocs
- Remove old skip-plugin patch
- Replace add-default-role-hint patch with remove-plexus-component patch
- Rename few jakarta BRs/Rs to apache names

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.3-1
- New bugfix version
- Fix javadoc generation error
- Use %%{_mavenpomdir} macro
- Update BRs to latest maven plugin names
- Use new plexus-containers components
- Remove/update old patches

* Tue May 25 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.2-3
- Update for transitional maven state.
- Install doxia-modules pom.

* Wed May  5 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.1.2-2
- Add BuildRequirement on fop

* Fri Feb 12 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.1.2-1
- Update to 1.1.2
- Add update_maven_depmap to post and postun
- Temporarily disable javadoc until maven2-plugin-javadoc is rebuilt against
  the new doxia

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.8.a10.4
- BR maven2-plugin-plugin.

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.8.a10.3
- BR maven2-plugin-assembly.

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.8.a10.2
- BR maven-surefire-provider-junit.

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.8.a10.1
- Add tomcat5 BR

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.8.a10
- Add tomcat5-servlet-2.4-api BR

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.7.a10
- Fix plexus-cli BR version

* Mon Aug 31 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.6.a10
- Add itext and plexus-cli BRs

* Wed Aug 26 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.5.a10
- Update to 1.0 alpha 10 courtesy of Deepak Bhole
- Remove gcj support
- Add patch to build against iText 2.x (with back-ported XML classes)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.4.a7.2.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a7.2.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7.2.10
- Fix broken release tag

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7.2.9
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a7.2.8
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a7.2jpp.7
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7.2jpp.6
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a7.3jpp.5
- Build with maven
- ExcludeArch ppc64

* Sat Sep 01 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a7.3jpp.4
- Rebuild without maven (fpr initial ppc build)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a7.3jpp.3
- Added switch to ignore failures for the time being

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a7.3jpp.2
- Build with maven

* Tue Feb 27 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.a7.3jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed %%post and %%postun sections for javadoc.
- Fixed instructios on how to generate source drop.
- Fixed %%Summary.
- Added gcj support option.
- Marked configuration file as %%config(noreplace) in %%files section.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a7.3jpp
- Update for maven2 9jpp

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a7.2jpp
- Fix versions in the depmap

* Wed Mar 15 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a7.1jpp
- Initial build
