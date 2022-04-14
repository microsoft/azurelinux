Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname jaxb-dtd-parser

Name:          glassfish-dtd-parser
Version:       1.4
Release:       3%{?dist}
Summary:       Library for parsing XML DTDs
License:       CDDL-1.1 and GPLv2 with exceptions

# NOTE: The new upstream repository under the Eclipse EE4J umbrella is here:
# https://github.com/eclipse-ee4j/jaxb-dtd-parser
URL:           https://github.com/javaee/%{srcname}
Source0:       %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: maven-local
BuildRequires: mvn(net.java:jvnet-parent:pom:)

%description
Library for parsing XML DTDs.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{srcname}-%{version}

# builds fail if this file is present
rm dtd-parser/src/module-info.java

%build
pushd dtd-parser
%mvn_file :dtd-parser %{name}
%mvn_build
popd

%install
pushd dtd-parser
%mvn_install
popd

%files -f dtd-parser/.mfiles
%license LICENSE

%files javadoc -f dtd-parser/.mfiles-javadoc
%license LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Fabio Valentini <decathorpe@gmail.com> - 1.4-1
- Update to version 1.4.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.20.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.19.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.18.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.17.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Michael Simacek <msimacek@redhat.com> - 1.2-0.16.20120120svn
- Fix license tag syntax

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.15.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.14.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.13.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.12.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 1.2-0.11.20120120svn
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.10.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.2-0.9.20120120svn
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.2-0.8.20120120svn
- rebuilt rhbz#992383
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.7.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.6.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-0.5.20120120svn
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2-0.3.20120120svn
- Fixed the release number

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2-0.2.20120120svn
- Updated license reference

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2-0.1.20120120svn
- Initial packaging
