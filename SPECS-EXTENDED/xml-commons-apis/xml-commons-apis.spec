Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package xml-commons-apis
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           xml-commons-apis
Version:        1.4.01
Release:        4%{?dist}
Summary:        APIs for DOM, SAX, and JAXP
License:        Apache-2.0 AND W3C AND SUSE-Public-Domain
Group:          Development/Libraries/Java
URL:            http://xml.apache.org/commons/
# From source control because the published tarball doesn't include some docs:
#   svn export http://svn.apache.org/repos/asf/xerces/xml-commons/tags/xml-commons-external-1_4_01/java/external
#   tar cJf xml-commons-external-1.4.01-src.tar.xz external
Source0:        xml-commons-external-1.4.01-src.tar.xz
Source1:        %{name}-MANIFEST.MF
Source2:        %{name}-ext-MANIFEST.MF
Source3:        http://repo1.maven.org/maven2/xml-apis/xml-apis/2.0.2/xml-apis-2.0.2.pom
Source4:        http://repo1.maven.org/maven2/xml-apis/xml-apis-ext/1.3.04/xml-apis-ext-1.3.04.pom
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xz
#!BuildIgnore:  xerces-j2 xml-apis xml-resolver
Provides:       xml-commons-apis-bootstrap = %{version}-%{release}
Provides:       xerces-j2-xml-apis
Provides:       xml-apis = %{version}-%{release}
Provides:       xml-commons-jaxp-1.1-apis
Provides:       xml-commons-jaxp-1.2-apis
Provides:       xml-commons-jaxp-1.3-apis
Provides:       xml-commons-jaxp-1.4-apis
Obsoletes:      xerces-j2-xml-apis
Obsoletes:      xml-commons-jaxp-1.1-apis
Obsoletes:      xml-commons-jaxp-1.2-apis
Obsoletes:      xml-commons-jaxp-1.3-apis
Obsoletes:      xml-commons-jaxp-1.4-apis
BuildArch:      noarch

%description
xml-commons-apis is designed to organize and have common packaging for
the various externally-defined standard interfaces for XML. This
includes the DOM, SAX, and JAXP.

%package manual
Summary:        Manual for %{name}
Group:          Documentation/HTML

%description manual
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
%{summary}.

%prep
%setup -q -n external
# Make sure upstream hasn't sneaked in any jars we don't know about
find "(" -name "*.class" -o -name "*.jar" ")" -delete

# Fix file encodings
iconv -f iso8859-1 -t utf-8 LICENSE.dom-documentation.txt > \
  LICENSE.dom-doc.temp && mv -f LICENSE.dom-doc.temp LICENSE.dom-documentation.txt
iconv -f iso8859-1 -t utf-8 LICENSE.dom-software.txt > \
  LICENSE.dom-sof.temp && mv -f LICENSE.dom-sof.temp LICENSE.dom-software.txt

# remove bogus section from poms
cp %{SOURCE3} %{SOURCE4} .
sed -i '/distributionManagement/,/\/distributionManagement/ {d}' *.pom

%pom_remove_parent xml-apis-ext*.pom

%build
ant -Dant.build.javac.source=6 -Dant.build.javac.target=6 jar javadoc

# inject OSGi manifests
jar ufm build/xml-apis.jar %{SOURCE1}
jar ufm build/xml-apis-ext.jar %{SOURCE2}

%install
# jar
install -d -m 0755 %{buildroot}%{_javadir}
install -pm 644 build/xml-apis.jar %{buildroot}%{_javadir}/xml-commons-apis.jar
pushd %{buildroot}%{_javadir}
  for i in \
    jaxp jaxp11 jaxp12 jaxp13 jaxp14 dom3 xerces-j2-xml-apis \
	xml-commons-jaxp-1.4-apis xml-commons-jaxp-1.3-apis \
	xml-commons-jaxp-1.2-apis xml-commons-jaxp-1.1-apis \
	xml-apis; do
    ln -s xml-commons-apis.jar ${i}.jar
  done
popd
install -pm 644 build/xml-apis-ext.jar %{buildroot}%{_javadir}/xml-commons-apis-ext.jar
pushd %{buildroot}%{_javadir}
  for i in xml-commons-jaxp-1.3-apis-ext xml-commons-jaxp-1.4-apis-ext; do
    ln -s xml-commons-apis-ext.jar ${i}.jar
  done
popd

# pom
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 xml-apis-[0-9]*.pom %{buildroot}%{_mavenpomdir}/xml-commons-apis.pom
%add_maven_depmap xml-commons-apis.pom xml-commons-apis.jar
install -pm 644 xml-apis-ext*.pom %{buildroot}%{_mavenpomdir}/xml-commons-apis-ext.pom
%add_maven_depmap xml-commons-apis-ext.pom xml-commons-apis-ext.jar -a xerces:dom3-xml-apis

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -a build/docs/javadoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

# prevent apis javadoc from being included in doc
rm -rf build/docs/javadoc
%fdupes -s build/docs/

%files -f .mfiles
%license LICENSE LICENSE.dom-documentation.txt LICENSE.dom-software.txt LICENSE.sac.html LICENSE.sax.txt
%doc NOTICE README.dom.txt README-sax README.sax.txt
%{_javadir}/*

%files manual
%doc build/docs/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.01-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 19 2020 Joe Schmitt <joschmit@microsoft.com> - 1.4.01-3.8
- Provide bootstrap version of this package.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.4.01-3.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the apache-parent, since we are not building
  using Maven.
* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore xml-apis and xml-resolver, since this does not
  strictly require them for build
* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore xerces-j2 to break cycle of OSGi requires
* Thu Dec 13 2018 Fridrich Strba <fstrba@suse.com>
- Obsolete the different other xml-apis providers
* Tue Dec 11 2018 Jan Engelhardt <jengelh@inai.de>
- Fix RPM groups. Use improved file deletion.
* Thu Dec  6 2018 Fridrich Strba <fstrba@suse.com>
- Initial package of xml-commons-apis
- Provide different api versions to simplify upgrades
