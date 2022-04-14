Vendor:         Microsoft Corporation
Distribution:   Mariner
%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:             jboss-jsp-2.2-api
Version:          1.0.1
Release:          22%{?dist}
Summary:          JavaServer(TM) Pages 2.2 API
License:          CDDL or GPLv2 with exceptions
URL:              http://www.jboss.org/

# git clone git://github.com/jboss/jboss-jsp-api_spec.git jboss-jsp-2.2-api
# cd jboss-jsp-2.2-api/ && git archive --format=tar --prefix=jboss-jsp-2.2-api-1.0.1.Final/ jboss-jsp-api_2.2_spec-1.0.1.Final | xz > jboss-jsp-2.2-api-1.0.1.Final.tar.xz
Source0:          %{name}-%{namedversion}.tar.xz

BuildRequires:    maven-local
BuildRequires:    mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:    mvn(org.jboss:jboss-parent:pom:)
BuildRequires:    mvn(org.jboss.spec.javax.el:jboss-el-api_2.2_spec)
BuildRequires:    mvn(org.jboss.spec.javax.servlet:jboss-servlet-api_3.0_spec)

BuildArch:        noarch

%description
JSR-000245: JavaServer(TM) Pages 2.2

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc	
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}

%pom_remove_plugin :maven-source-plugin

%mvn_file : %{name}
%mvn_alias : javax.servlet.jsp:jsp-api

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc README

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 27 2016 gil cattaneo <puntogil@libero.it> 1.0.1-14
- add missing build requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 30 2015 gil cattaneo <puntogil@libero.it> - 1.0.1-12
- Fix FTBFS RHBZ#1239596
- Switch to xmvn
- Use BR mvn()-like
- Fix some rpmlint problem
- Introduce license macro
- Adapt to current guideline

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 27 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.1-10
- Fix FTBFS due to XMvn changes in F21 (#1106884)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0.1-8
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.1-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 22 2012 Anthony Sasadeusz <sasadeu1@umbc.edu> 1.0.1-3
- Corrected license to CDDL or GPLv2 with exceptions.

* Mon Mar 19 2012 Anthony Sasadeusz <sasadeu1@umbc.edu> 1.0.1-2
- Added summary, changed license to GPLv2 with exceptions, expanded description,
- and added LICENSE and README files to javadoc.

* Mon Mar 19 2012 Anthony Sasadeusz <sasadeu1@umbc.edu> 1.0.1-1
- Cleanup and updated to version 1.0.1

* Fri Aug 12 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-1
- Initial packaging

