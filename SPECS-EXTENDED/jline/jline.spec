Summary:        Java library for reading and editing user input in console applications
Name:           jline
Version:        2.14.6
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://github.com/jline/jline2
Source0:        https://github.com/jline/jline2/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
Patch0:         jline-java8compat.patch
Patch1:         jline-jansi2.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  jansi
BuildRequires:  javapackages-local-bootstrap
Requires:       jansi
BuildArch:      noarch

%description
JLine is a java library for reading and editing user input in console
applications. It features tab-completion, command history, password
masking, customizable keybindings, and pass-through handlers to use to
chain to other console applications.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -p1 -n jline2-%{name}-%{version}
%pom_change_dep org.fusesource.jansi:jansi org.fusesource.jansi:jansi:1.12
cp %{SOURCE1} build.xml
mkdir -p lib

# Remove maven-shade-plugin usage
%pom_remove_plugin "org.apache.maven.plugins:maven-shade-plugin"
# Remove animal sniffer plugin in order to reduce deps
%pom_remove_plugin "org.codehaus.mojo:animal-sniffer-maven-plugin"

# Remove unavailable and unneeded deps
%pom_xpath_remove "pom:build/pom:extensions"
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-javadoc-plugin

%pom_remove_parent

%build
build-jar-repository -s lib jansi
%{ant} package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Tue Jan 17 2023 Sumedh Sharma <sumsharma@microsoft.com> - 2.14.6-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Converting the 'Release' tag to the '[number].[distribution]' format.
- License verified

* Mon May 16 2022 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * jline-jansi2.patch
    + fix jline build against jansi 2.4.x
- Remove dependency on jansi-native and hawtjni-runtime

* Sun Mar 20 2022 Fridrich Strba <fstrba@suse.com>
- Build with source and target levels 8

* Fri Sep 27 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * jline-java8compat.patch
    + build binaries compatible with Java 8

* Thu Jun 27 2019 Fridrich Strba <fstrba@suse.com>
- Work around a problem with dependency resolution, where variables
  are not resolved

* Tue Mar  5 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 2.14.6
  * NOT backward compatible with jline 1.x
  * Depend on jansi 2.9+
  * #277: Allow setting max history-size. 'FileHistory' allows
    delayed init (to allow setMaxSize to take effect) and
  'ConsoleReader' exposes ability to read inputrc settings.
  * Ability to control terminal encoding
  * Backward history searching
  * Handle EOF / Ctrl-D on unsupported terminals
  * Distinguish carriage return from newline
  * Correcting Manifest to make jline work as a bundle in OSGi
  * Handle TERM=dumb as an UnsupportedTerminal
  * Updated license headers to be consistent BSD version
  * Added support for vi keymap. Most major vi features should work.
  * The "jline.esc.timeout" configuration option (in your
    $HOME/.jline.rc) controls the number of millisesconds that
  jline will wait after seeing an ESC key to see if another
  character arrives.
  * The JVM shutdown hook that restores the terminal settings when
    the JVM exits (jline.shutdownhook) is now turned on by default.
- Generate and customize the ant build file in order to be able
  to build without maven.

* Wed Sep 27 2017 fstrba@suse.com
- Don't require java-1_5_0-gcj-compat, but build with any
  java-devel provider
- Specify java source and target level 1.6: fixes build with
  jdk9

* Fri Jun  9 2017 tchvatal@suse.com
- Reduce depgraph and drop maven fragment to allow bootstrap

* Fri May 19 2017 mpluskal@suse.com
- Update dependencies

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Mon Aug 26 2013 mvyskocil@suse.com
- use new add_maven_depmap from javapackages-utils

* Thu Apr 25 2013 mvyskocil@suse.com
- add findutils dependency (bnc#816314)

* Thu Sep  2 2010 mvyskocil@suse.cz
- ignore antlr(-java) to reduce build cycles

* Wed Nov 18 2009 mvyskocil@suse.cz
- Build using gcj - needed by rhino 1.7R2 - bnc#554532

* Thu May  7 2009 mvyskocil@suse.cz
- Initial SUSE packaging 0.9.94 from jpp 5.0
