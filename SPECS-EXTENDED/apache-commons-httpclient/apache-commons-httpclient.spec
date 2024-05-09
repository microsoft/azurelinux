Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache-commons-httpclient
#
# Copyright (c) 2020 SUSE LLC
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


%define short_name commons-httpclient
Name:           apache-commons-httpclient
Version:        3.1
Release:        14%{?dist}
Summary:        Feature rich package for accessing resources via HTTP
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://hc.apache.org/httpclient-3.x/
Source0:        https://www.apache.org/dist/httpcomponents/commons-httpclient/source/%{short_name}-%{version}-src.tar.gz
Source1:        https://repo.maven.apache.org/maven2/%{short_name}/%{short_name}/%{version}/%{short_name}-%{version}.pom
Patch0:         %{name}-disablecryptotests.patch
# Add OSGi MANIFEST.MF bits
Patch1:         %{name}-addosgimanifest.patch
Patch2:         %{name}-encoding.patch
#PATCH-FIX-UPSTREAM: bnc#803332
#https://issues.apache.org/jira/secure/attachment/12560251/CVE-2012-5783-2.patch
Patch3:         %{short_name}-CVE-2012-5783-2.patch
#PATCH-FIX-UPSTREAM bsc#1178171 CVE-2014-3577 MITM security vulnerability
Patch4:         apache-commons-httpclient-CVE-2014-3577.patch
#PATCH-FIX-UPSTREAM bsc#945190 CVE-2015-5262 Missing HTTPS connection timeout
Patch5:         apache-commons-httpclient-CVE-2015-5262.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  commons-codec
BuildRequires:  commons-logging >= 1.0.3
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
Requires:       commons-codec
Requires:       commons-logging >= 1.0.3
Provides:       %{short_name} = %{version}
Provides:       jakarta-%{short_name} = %{version}
Obsoletes:      jakarta-%{short_name} < %{version}
Provides:       jakarta-%{short_name}3 = %{version}
Obsoletes:      jakarta-%{short_name}3 < %{version}
BuildArch:      noarch

%description
Although the java.net  package provides basic functionality for
accessing resources via HTTP, it doesn't provide the full flexibility
or functionality needed by many applications. The Apache Commons
HttpClient component provides a package implementing the client side
of the most recent HTTP standards and recommendations.

The HttpClient component may be of interest to anyone building
HTTP-aware client applications such as web browsers, web service
clients, or systems that leverage or extend the HTTP protocol for
distributed communication.

%package        javadoc
Summary:        Developer documentation for %{name}
Group:          Development/Libraries/Java

%description    javadoc
Developer documentation for %{name} in JavaDoc
format.

%{summary}.

%package        demo
Summary:        Demonstration files for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description    demo
Demonstration files for %{name}. NOTE: It is
possible that some demonstration files are specially prepared for SUN
Java runtime environment. If they fail with IBM or BEA Java, the
package itself does not need to be broken.

%{summary}.

%package        manual
Summary:        Manual for %{name}
Group:          Development/Libraries/Java

%description    manual
Manual for %{name}

%{summary}.

%prep
%setup -q -n %{short_name}-%{version}
mkdir lib # duh
rm -rf docs/apidocs docs/*.patch docs/*.orig docs/*.rej

%patch 0

pushd src/conf
sed -i 's/\r//' MANIFEST.MF
%patch 1
popd

%patch 2
%patch 3 -p1
%patch 4 -p1
%patch 5 -p1

# Use javax classes, not com.sun ones
# assume no filename contains spaces
pushd src
    for j in $(find . -name "*.java" -exec grep -l 'com\.sun\.net\.ssl' {} \;); do
        sed -e 's|com\.sun\.net\.ssl|javax.net.ssl|' $j > tempf
        cp tempf $j
    done
    rm tempf
popd

sed -i 's/\r//' RELEASE_NOTES.txt
sed -i 's/\r//' README.txt
sed -i 's/\r//' LICENSE.txt

%build
ant \
  -Dant.build.javac.source=8 -Dant.build.javac.target=8 \
  -Dbuild.sysclasspath=first \
  -Djavadoc.j2sdk.link=%{_javadocdir}/java \
  -Djavadoc.logging.link=%{_javadocdir}/apache-commons-logging \
  -Dtest.failonerror=false \
  -Dlib.dir=%{_javadir} \
  -Djavac.encoding=UTF-8 \
  dist test

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p dist/%{short_name}.jar \
  %{buildroot}%{_javadir}/%{name}.jar
# compat symlink
pushd %{buildroot}%{_javadir}
ln -s %{name}.jar %{name}3.jar
ln -s %{name}.jar %{short_name}3.jar
ln -s %{name}.jar %{short_name}.jar
ln -s %{name}.jar jakarta-%{short_name}.jar
ln -s %{name}.jar jakarta-%{short_name}3.jar
popd

# pom
mkdir -p %{buildroot}%{_mavenpomdir}
cp -p %{SOURCE1} %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a apache:commons-httpclient

# javadoc
mkdir -p %{buildroot}%{_javadocdir}
mv dist/docs/api %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

# demo
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr src/examples src/contrib %{buildroot}%{_datadir}/%{name}
%fdupes -s %{buildroot}%{_datadir}/%{name}

# manual and docs
rm -f dist/docs/{BUILDING,TESTING}.txt
ln -s %{_javadocdir}/%{name} dist/docs/apidocs
%fdupes -s dist/docs

%files
%defattr(0644,root,root,0755)
%license LICENSE.txt
%doc README.txt RELEASE_NOTES.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}3.jar
%{_javadir}/%{short_name}3.jar
%{_javadir}/%{short_name}.jar
%{_javadir}/jakarta-%{short_name}3.jar
%{_javadir}/jakarta-%{short_name}.jar
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc dist/docs/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1-14
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.1-13.2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed commands.

* Tue Oct 27 2020 Pedro Monreal <pmonreal@suse.com>
- Security fix [bsc#945190, CVE-2015-5262]
  * http/conn/ssl/SSLConnectionSocketFactory.java ignores the
    http.socket.timeout configuration setting during an SSL handshake,
    which allows remote attackers to cause a denial of service (HTTPS
    call hang) via unspecified vectors.
- Add apache-commons-httpclient-CVE-2015-5262.patch
* Tue Oct 27 2020 Pedro Monreal <pmonreal@suse.com>
- Security fix [bsc#1178171, CVE-2014-3577]
  * org.apache.http.conn.ssl.AbstractVerifier does not properly
    verify that the server hostname matches a domain name in the
    subject's Common Name (CN) or subjectAltName field of the X.509
    certificate, which allows MITM attackers to spoof SSL servers
    via a "CN=" string in a field in the distinguished name (DN)
    of a certificate.
- Add apache-commons-httpclient-CVE-2014-3577.patch
* Mon Apr  1 2019 Jan Engelhardt <jengelh@inai.de>
- Trim conjecture from description.
* Mon Jan 21 2019 Fridrich Strba <fstrba@suse.com>
- Add maven pom file and clean-up the spec file
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Run fdupes on documentation
* Thu Sep  7 2017 fstrba@suse.com
- Build with java source and target versions 1.6
  * fixes build with jdk9
* Tue Jul  8 2014 tchvatal@suse.com
- Redo the bytcode disabling properly.
- Cleanup with spec-cleaner
* Mon Apr 14 2014 darin@darins.net
- disable bytecode test on SLES
* Fri Oct 25 2013 mvyskocil@suse.com
- really apply CVE-2012-5783 patch
- build with java 6 and higher
* Thu Mar 28 2013 mvyskocil@suse.com
- enhance fix of bnc#803332 / CVE-2012-5783
  * add a check for subjectAltNames for instance
* Thu Feb 14 2013 mvyskocil@suse.com
- fix bnc#803332: no ssl certificate hostname checking (CVE-2012-5783)
  * commons-httpclient-CVE-2012-5783.patch
- add jakarta- compat symlinks
* Sun Feb  3 2013 p.drouand@gmail.com
- Initial release
