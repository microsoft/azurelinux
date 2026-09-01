# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           maven-reporting-api
Version:        4.0.0
Release:        4%{?dist}
Epoch:          1
Summary:        API to manage report generation
License:        Apache-2.0
URL:            https://maven.apache.org/shared/maven-reporting-api
VCS:            git:https://github.com/apache/maven-reporting-api.git

Source0:        https://archive.apache.org/dist/maven/reporting/%{name}-%{version}-source-release.zip
# Source file signature
Source1:        https://archive.apache.org/dist/maven/reporting/%{name}-%{version}-source-release.zip.asc
# Apache Maven public key
Source2:        https://downloads.apache.org/maven/KEYS

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  gnupg2
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)

%{?javadoc_package}

%description
API to manage report generation.  Maven-reporting-api is included in the
Maven 2.x core distribution, but was moved to shared components to
achieve report decoupling from the Maven 3 core.

%prep
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}
%autosetup

# Fix end of line encoding
sed -i.orig 's/\r//' README.md
touch -r README.md.orig README.md
rm README.md.orig

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1:4.0.0-4
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Jerry James  <loganjerry@gmail.com> - 1:4.0.0-2
- Fix end of line encodings

* Tue Jan 28 2025 Jerry James <loganjerry@gmail.com> - 1:4.0.0-1
- Version 4.0.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Feb 28 2024 Jerry James <loganjerry@gmail.com> - 1:3.1.1-6
- Build for JDK 8 at a minimum (rhbz#2266673)

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1:3.1.1-6
- Rebuilt for java-21-openjdk as system jdk

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Jerry James <loganjerry@gmail.com> - 1:3.1.1-1
- Version 3.1.1
- Convert License tag to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1:3.1.0-2
- Rebuilt for Drop i686 JDKs

* Mon Feb  7 2022 Jerry James <loganjerry@gmail.com> - 1:3.1.0-1
- Version 3.1.0
- Verify the sources
- Retire alias for old name, not used by anything in Fedora

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1:3.0-24
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:3.0-19
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 12 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.0-13
- Remove legacy obsoletes and provides

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.0-8
- Fix build-requires on parent POM

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.0-6
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.0-5
- Fix unowned directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.0-3
- Build with xmvn
- Resolves: rhbz#912437

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:3.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Tomas Radej <tradej@redhat.com> - 1:3.0-1
- Initial version

