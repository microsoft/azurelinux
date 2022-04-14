Name:         codemodel
Version:      2.6
Release:      29%{?dist}
Summary:      Java library for code generators
License:      CDDL-1.1 or GPLv2 with exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:          http://codemodel.java.net
# svn export https://svn.java.net/svn/codemodel~svn/tags/codemodel-project-2.6/ codemodel-2.6
# tar -zcvf codemodel-2.6.tar.gz codemodel-2.6
Source0:      %{name}-%{version}.tar.gz
# Remove the dependency on istack-commons (otherwise it will be a
# recursive dependency with the upcoming changes to that package):
Patch0:       %{name}-remove-istack-commons-dependency.patch

BuildArch:     noarch

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(net.java:jvnet-parent:pom:)
BuildRequires: mvn(org.apache.ant:ant)


%description
CodeModel is a Java library for code generators; it provides a way to
generate Java programs in a way much nicer than PrintStream.println().
This project is a spin-off from the JAXB RI for its schema compiler
to generate Java source files.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep

# Unpack and patch the original source:
%setup -q
%patch0 -p1

# Remove bundled jar files:
find . -name '*.jar' -print -delete

%mvn_file :%{name} %{name}
%mvn_file :%{name}-annotation-compiler %{name}-annotation-compiler

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%license LICENSE.html

%files javadoc -f .mfiles-javadoc
%license LICENSE.html

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-29
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Michael Simacek <msimacek@redhat.com> - 2.6-24
- Regenerate BRs

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Michael Simacek <msimacek@redhat.com> - 2.6-22
- Change license to CDDL-1.1 or GPLv2 with exceptions

* Wed Nov 08 2017 Michael Simacek <msimacek@redhat.com> - 2.6-21
- Change license to CDDL-1.1 and GPLv2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 2.6-16
- introduce license macro

* Tue Jun 24 2014 Michael Simacek <msimacek@redhat.com> - 2.6-15
- Chnage jvnet-parent BR to jvnet-parent:pom

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Michael Simacek <msimacek@redhat.com> - 2.6-13
- Change maven-surefire-provider-junit4 dependency to
  maven-surefire-provider-junit

* Thu Mar 20 2014 Michael Simacek <msimacek@redhat.com> - 2.6-12
- Remove BR java-devel

* Thu Mar 13 2014 Michael Simacek <msimacek@redhat.com> - 2.6-11
- Drop manual requires

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 2.6-10
- rebuilt FTBFS in rawhide
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-6
- Add maven-enforcer-plugin as build time dependeny

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-4
- Restore the dependency on jvnet-parent
- Remove the dependency on istack-commons

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-3
- Added build requirement for maven-surefire-provider-junit4

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-2
- Cleanup of the spec file

* Mon Jan 16 2012 Marek Goldmann <mgoldman@redhat.com> 2.6-1
- Initial packaging

