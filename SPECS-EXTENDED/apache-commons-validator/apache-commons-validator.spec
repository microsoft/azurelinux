Vendor:         Microsoft Corporation
Distribution:   Mariner
%global short_name      commons-validator

Name:             apache-%{short_name}
Version:          1.5.0
Release:          11%{?dist}
Summary:          Apache Commons Validator
License:          ASL 2.0
URL:              http://commons.apache.org/validator/
BuildArch:        noarch

Source0:          http://www.apache.org/dist/commons/validator/source/%{short_name}-%{version}-src.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(commons-beanutils:commons-beanutils)
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(commons-digester:commons-digester)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)

%description
A common issue when receiving data either electronically or from user input is
verifying the integrity of the data. This work is repetitive and becomes even
more complicated when different sets of validation rules need to be applied to
the same set of data based on locale for example. Error messages may also vary
by locale. This package attempts to address some of these issues and speed
development and maintenance of validation rules.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' RELEASE-NOTES.txt
sed -i 's/\r//' NOTICE.txt

# Compatibility links
%mvn_alias "%{short_name}:%{short_name}" "org.apache.commons:%{short_name}"
%mvn_file :commons-validator %{short_name} %{name}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.0-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-3
- Regenerate build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan  5 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-1
- Update to upstream version 1.5.0

* Wed Jul 08 2015 Michal Srb <msrb@redhat.com> - 1.4.1-1
- Updated to 1.4.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.0-7
- Use Requires: java-headless rebuild (#1067528)

* Tue Aug 06 2013 Mat Booth <fedora@matbooth.co.uk> - 1.4.0-6
- Update for newer guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4.0-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Nov 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-2
- Install NOTICE file with javadoc package

* Fri Oct 19 2012 Chris Spike <spike@fedoraproject.org> 1.4.0-1
- Updated to 1.4.0
- Switched build tool from ant to maven
- Updated to latest java packaging guidelines
- Dropped oro BR/R

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com>- 1.3.1-8
- Fix tests after junit update

* Sat Jan 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.3.1-7
- Tweak source encoding to fix build with Java 1.7.
- Drop versioned jars and javadoc dir.
- Drop no longer needed javadoc Obsoletes.
- Crosslink with local JDK API docs.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3.1-5
- Change oro to jakarta-oro in BR/R

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Chris Spike <chris.spike@arcor.de> 1.3.1-3
- Moved junit tests to check section

* Sat Oct 2 2010 Chris Spike <chris.spike@arcor.de> 1.3.1-2
- Rename and rebase from jakarta-commons-validator
