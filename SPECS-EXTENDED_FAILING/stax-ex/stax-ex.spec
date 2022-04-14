Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          stax-ex
Version:       1.7.7
Release:       13%{?dist}
Summary:       StAX API extensions
License:       CDDL or GPLv2
Url:           https://javaee.github.io/metro-stax-ex
# Source0: https://github.com/javaee/metro-stax-ex/archive/refs/tags/stax-ex-1.7.7.tar.gz
Source0:       https://github.com/javaee/metro-stax-ex/archive/refs/tags/%{name}-%{version}.tar.gz

BuildRequires: dos2unix
BuildRequires: maven-local
BuildRequires: mvn(javax.xml.stream:stax-api)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(net.java:jvnet-parent:pom:)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)

BuildArch:     noarch

%description
This project develops a few extensions to complement JSR-173 StAX API in the
following area.

* Enable parser instance reuse (which is important in the
  high-performance environment like JAXB and JAX-WS)
* Improve the support for reading from non-text XML infoset,
  such as FastInfoset.
* Improve the namespace support.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

%pom_remove_dep javax.activation:activation
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin
%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-deploy-plugin

# Convert the license to UTF-8:
mv LICENSE.txt LICENSE.txt.tmp
iconv -f ISO-8859-1 -t UTF-8 LICENSE.txt.tmp > LICENSE.txt
dos2unix LICENSE.txt

%mvn_file :stax-ex %{name}

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.7-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 22 2016 gil cattaneo <puntogil@libero.it> 1.7.7-5
- regenerate build-requires

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 gil cattaneo <puntogil@libero.it> 1.7.7-2
- introduce license macro

* Wed Jan 21 2015 gil cattaneo <puntogil@libero.it> 1.7.7-1
- update to 1.7.7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.7.1-7
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.7.1-6
- rebuilt FTBFS in rawhide
- swith to Xmvn
- adapt to new guideline

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.7.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Oct 30 2012 Marek Goldmann <mgoldman@redhat.com> - 1.7.1-2
- Added maven-enforcer-plugin BR

* Tue Aug 28 2012 gil cattaneo <puntogil@libero.it> 1.7.1-1
- Updated to upstream version 1.7.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 9 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.7-1
- Updated to upstream version 1.7

* Fri Mar 9 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.4-2
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 1.4-1
- Initial packaging
