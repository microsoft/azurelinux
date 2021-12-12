Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           xmlrpc
Version:        3.1.3
Release:        26%{?dist}
Summary:        Java XML-RPC implementation
License:        ASL 2.0
URL:            https://ws.apache.org/xmlrpc/
BuildArch:      noarch

Source0:        https://archive.apache.org/dist/ws/xmlrpc/sources/apache-xmlrpc-%{version}-src.tar.bz2

# Fix build against modern servlet API by implementing missing interfaces
Patch0: 0001-Javax-Servlet-API.patch
# Add OSGi metadata so that xmlrpc can be used in OSGi runtimes
Patch1: 0002-Add-OSGi-metadata.patch
# CVE-2016-5003 - Disallow deserialization of <ex:serializable> tags by default
Patch2: 0003-disallow-deserialization-of-ex-serializable-tags.patch
# CVE-2016-5002 - isallow loading of external DTD
Patch3: 0004-disallow-loading-external-dtd.patch
# Jakarta Commons HttpClient is obsolete and should not be used, one of the other
# provider implementations should by used instead by clients of xmlrpc
Patch4: 0005-Remove-dep-on-ancient-commons-httpclient.patch
# CVE-2019-17570 - Deserialization of server-side exception from faultCause in XMLRPC error response
Patch5: 0006-Fix-for-CVE-2019-17570.patch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.ws.commons.util:ws-commons-util)


%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package common
Summary: Common classes for XML-RPC client and server implementations

%description common
%{summary}.

%package client
Summary: XML-RPC client implementation

%description client
%{summary}.

%package server
Summary: XML-RPC server implementation

%description server
%{summary}.

%prep
%setup -q -n apache-%{name}-%{version}-src

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

sed -i 's/\r//' LICENSE.txt

%pom_disable_module dist
%pom_remove_dep jaxme:jaxmeapi common
%pom_add_dep junit:junit:3.8.1:test

%mvn_file :{*} @1
%mvn_package :*-common %{name}

%build
# ignore test failure because server part needs network
%mvn_build -s -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files common -f .mfiles-%{name}
%license LICENSE.txt NOTICE.txt

%files client -f .mfiles-%{name}-client

%files server -f .mfiles-%{name}-server

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 3.1.3-26
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:3.1.3-25
- Initial CBL-Mariner import from Fedora 30 (license: MIT).

* Wed Apr 01 2020 Mat Booth <mat.booth@redhat.com> - 1:3.1.3-24
- Add patch for CVE-2019-17570

* Tue Mar 31 2020 Mat Booth <mat.booth@redhat.com> - 1:3.1.3-23
- Modernise spec file and remove dep on ancient Jakarta Commons httpclient implementation

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 18 2018 Michael Simacek <msimacek@redhat.com> - 1:3.1.3-20
- Disallow deserialization of <ex:serializable> tags by default
- Resolves CVE-2016-5003
- Disallow loading of external DTD
- Resolves CVE-2016-5002

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Troy Dawson <tdawson@redhat.com> - 1:3.1.3-17
- Add junit to pom deps. Was originally supplied by ws-commons-util (#1460767)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:3.1.3-15
- Rebuild for readline 7.x

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 1:3.1.3-12
- introduce license macro

* Thu Jul 10 2014 Sami Wagiaalla <swagiaal@redhat.com> - 1:3.1.3-11
- Add OSGi info for xmlrpc-server jar.
- export o.a.xmlrpc from xmlrpc-client jar.

* Mon Jun 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-10
- Use servlet 3.1.0 API

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.1.3-8
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-6
- Update to current packaging guidelines

* Fri May 17 2013 Alexander Kurtakov <akurtako@redhat.com> 1:3.1.3-5
- Remove javax.xml.bind from osgi imports - it's part of the JVM now.
- Drop the ws-jaxme dependency for the same reason.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:3.1.3-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Oct 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> 3.1.3-2
- xmlrpc v2 had an Epoch so we need one here. Add it back

* Fri Sep 14 2012 Alexander Kurtakov <akurtako@redhat.com> 3.1.3-1
- First release of version 3.x package
