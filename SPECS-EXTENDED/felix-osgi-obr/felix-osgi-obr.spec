Vendor:         Microsoft Corporation
Distribution:   Mariner
%global bundle org.osgi.service.obr

Name:           felix-osgi-obr
Version:        1.0.2
Release:        26%{?dist}
Summary:        Felix OSGi OBR Service API
License:        ASL 2.0
URL:            https://felix.apache.org/documentation/subprojects/apache-felix-osgi-bundle-repository.html
BuildArch:      noarch

Source0:        https://www.apache.org/dist/felix/org.osgi.service.obr-%{version}-project.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:felix:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.osgi:osgi.core)

%description
OSGi OBR Service API.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{bundle}-%{version}

# Use latest OSGi implementation
%pom_change_dep :org.osgi.core org.osgi:osgi.core

%mvn_file ":{*}" felix/@1

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-26
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 17 2019 Mat Booth <mat.booth@redhat.com> - 1.0.2-24
- Rebuild against OSGi R7 APIs

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.2-17
- Regenerate build-requires
- Update to current packaging guidelines

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.2-14
- Fix build-requires on felix-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-12
- Use Requires: java-headless rebuild (#1067528)

* Tue Aug 06 2013 Michal Srb <msrb@redhat.com> - 1.0.2-11
- Adapt to current guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.2-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Sep  4 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.2-7
- Install LICENSE and NOTICE with javadoc package
- Build with maven
- Move POM file to _mavenpomdir from _datadir/maven2/poms
- Update to current packaging guidelines
- Add missing R: java, jpackage-utils

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0.2-3
- Fix pom name.
- Adapt to current guidelines.

* Thu Sep 3 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0.2-2
- Fix line length.

* Thu Sep 3 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0.2-1
- Initial package.
