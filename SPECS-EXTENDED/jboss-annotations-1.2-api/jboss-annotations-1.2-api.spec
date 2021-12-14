Vendor:         Microsoft Corporation
Distribution:   Mariner
%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:          jboss-annotations-1.2-api
Version:       1.0.2
Release:       3%{?dist}
Summary:       Common Annotations 1.2 API
License:       CDDL or GPLv2 with exceptions
URL:           https://github.com/jboss/jboss-annotations-api_spec
Source0:       https://github.com/jboss/jboss-annotations-api_spec/archive/jboss-annotations-api_1.2_spec-%{namedversion}.tar.gz
Source1:       cddl.txt

BuildRequires: maven-local
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.jboss:jboss-parent:pom:)

BuildArch:     noarch

%description
This package contains Common Annotations 1.2 API.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc	
This package contains the API documentation for %{name}.

%prep
%setup -q -n jboss-annotations-api_spec-jboss-annotations-api_1.2_spec-%{namedversion}

cp %{SOURCE1} .

%pom_remove_plugin :maven-source-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README
%license cddl.txt LICENSE

%files javadoc -f .mfiles-javadoc
%license cddl.txt LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 17 2019 Fabio Valentini <decathorpe@gmail.com> - 1.0.2-1
- Update to version 1.0.2.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 01 2016 gil cattaneo <puntogil@libero.it> 1.0.0-1
- update to 1.0.0.Final
- fix BR list and use BR mvn()-like
- introduce license macro
- remove some rpmlint problems
- remove duplicate files

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.6.Alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.Alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.4.Alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.3.Alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Marek Goldmann <mgoldman@redhat.com> - 1.0.0-0.2.Alpha1
- Added CDDL license

* Wed Jun 05 2013 Marek Goldmann <mgoldman@redhat.com> - 1.0.0-0.1.Alpha1
- Initial packaging


