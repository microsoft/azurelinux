Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           jtidy
VCS: https://src.suse.de/pool/jtidy?trackingbranch=slfo-1.2#0765e5b9560995812fcac0bb88fd0e409490c8343acc52ef06cfa2af91680a0d
Version:        1.0.4
Release:        1%{?dist}
Summary:        HTML syntax checker and pretty printer
License:        HTMLTIDY
Group:          Development/Libraries/Java
URL:            https://github.com/jtidy/jtidy
Source0:        https://github.com/jtidy/jtidy/archive/refs/tags/jtidy-1.0.4.tar.gz
Source1:        %{name}-build.xml
Source100:      %{name}-rpmlintrc
BuildRequires:  ant >= 1.6
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xerces-j2
BuildRequires:  xml-apis
Requires:       xerces-j2
Requires:       xml-apis
BuildArch:      noarch

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%package javadoc
Summary:        HTML syntax checker and pretty printer
Group:          Development/Libraries/Java

%description javadoc
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%package scripts
Summary:        HTML syntax checker and pretty printer
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}
Requires:       javapackages-tools

%description scripts
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%prep
%setup -q -n %{name}-%{name}-%{version}
cp -p %{SOURCE1} build.xml

%build
mkdir -p lib
build-jar-repository -s lib xerces-j2 xml-apis
%{ant} \
    package javadoc

%install
# jar
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a net.sf.jtidy:%{name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -aL target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}
mv %{buildroot}%{_javadocdir}/%{name}/legal/ADDITIONAL_LICENSE_INFO .
mv %{buildroot}%{_javadocdir}/%{name}/legal/LICENSE .

# shell script
%jpackage_script org.w3c.tidy.Tidy "" "" %{name}:xerces-j2:xml-apis %{name} true

# ant.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/ant.d
cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
jtidy xerces-j2 xml-apis
EOF

%files
%license LICENSE.txt
%license LICENSE
%license ADDITIONAL_LICENSE_INFO
%{_javadir}/%{name}.jar
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%exclude /usr/share/maven-poms/%{name}.pom
%exclude /usr/share/maven-metadata/%{name}.xml

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/*

%changelog
* Fri Nov 21 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.0.4-1
- Upgrade to version 1.0.4 reference:openSUSE (license: MIT).
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
