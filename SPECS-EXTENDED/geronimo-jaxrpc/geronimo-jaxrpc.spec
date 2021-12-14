Vendor:         Microsoft Corporation
Distribution:   Mariner
%global spec_ver 1.1
%global spec_name geronimo-jaxrpc_%{spec_ver}_spec

Name:             geronimo-jaxrpc
Version:          2.1
Release:          27%{?dist}
Summary:          Java EE: Java API for XML Remote Procedure Call v1.1
License:          ASL 2.0 and W3C

URL:              http://geronimo.apache.org/
Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz
BuildArch:        noarch

BuildRequires:    java-devel >= 1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    geronimo-parent-poms
BuildRequires:    maven-resources-plugin
BuildRequires:    saaj_api
BuildRequires:    geronimo-osgi-locator
BuildRequires:    glassfish-servlet-api
BuildRequires:    maven-surefire-provider-junit

Provides:         jaxrpc_api = %{spec_ver}

%description
This package contains the core JAX-RPC APIs for the client programming model.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{spec_name}-%{version}
iconv -f iso8859-1 -t utf-8 LICENSE > LICENSE.conv && mv -f LICENSE.conv LICENSE
sed -i 's/\r//' LICENSE NOTICE
# Use parent pom files instead of unavailable 'genesis-java5-flava'
%pom_set_parent org.apache.geronimo.specs:specs:1.4

%mvn_alias : javax.xml:jaxrpc-api
%mvn_file : %{name} jaxrpc

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Wed Nov 03 2021 Muhammad Falak <mwani@microsft.com> - 2.1-27
- Remove epoch from java-devel

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1-26
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-16
- Remove use of depmap

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-14
- Use Requires: java-headless rebuild (#1067528)

* Thu Aug 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-13
- Update to latest packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-9
- Fix license tag
- Install NOTICE file
- Update to current packaging guidelines

* Fri Aug 10 2012 Andy Grimm <agrimm@gmail.com> - 2.1-8
- Update tomcat requirement to fix FTBFS

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 1 2011 Alexander Kurtakov <akurtako@redhat.com> 2.1-5
- Fix the jaxrpc.jar symlink.

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 2.1-4
- Build with maven 3.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 2 2010 Chris Spike <chris.spike@arcor.de> 2.1-2
- Changed BR from 'servlet' to 'servlet >= 2.5'

* Thu Jul 22 2010 Chris Spike <chris.spike@arcor.de> 2.1-1
- Initial version of the package
