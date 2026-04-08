# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global core   org.abego.treelayout
%global giturl https://github.com/abego/treelayout

Name:          treelayout
Version:       1.0.3
Release:       27%{?dist}
Summary:       Efficient and customizable Tree Layout Algorithm in Java
License:       BSD-3-Clause
URL:           http://treelayout.sourceforge.net/
VCS:           git:%{giturl}.git
Source0:       %{giturl}/archive/v%{version}/%{name}-%{version}.tar.gz
# Dummy POM to ease building with RPM
Source1:       pom.xml

BuildArch:     noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires: maven-local-openjdk25
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)

%description
Efficiently create compact, highly customizable tree layouts.  The
software builds tree layouts in linear time; i.e., even trees with many
nodes are built quickly.

%package       demo
Summary:       TreeLayout Core Demo

%description   demo
Demo for "org.abego.treelayout.core".

%package       javadoc
Summary:       Javadoc for %{name}

%description   javadoc
This package contains javadoc for %{name}.

%prep
%autosetup
cp -p %{SOURCE1} .

%conf
# sonatype-oss-parent is deprecated in Fedora
%pom_remove_parent %{core} %{core}.demo %{core}.netbeans %{core}.netbeans.demo

# update the source and target JDK
sed -i 's/1\.5/1.8/g' $(find . -name pom.xml)

# fix non ASCII chars for JDK 8 and earlier
if [ -x %{_bindir}/native2ascii ]; then
  native2ascii -encoding UTF8 \
    %{core}/src/main/java/org/abego/treelayout/package-info.java \
    %{core}/src/main/java/org/abego/treelayout/package-info.java
fi

%mvn_package :%{core}.project __noinstall

%build
%mvn_build -s

%install
%mvn_install

%files -f .mfiles-%{core}.core
%doc %{core}/CHANGES.txt README.md
%license %{core}/src/LICENSE.TXT

%files demo -f .mfiles-%{core}.demo
%doc %{core}.demo/CHANGES.txt
%license %{core}.demo/src/LICENSE.TXT

%files javadoc -f .mfiles-javadoc
%license %{core}/src/LICENSE.TXT

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.0.3-27
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.0.3-23
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Jerry James <loganjerry@gmail.com> - 1.0.3-19
- Convert License tag to SPDX

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.0.3-18
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.0.3-17
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.0.3-12
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon May  4 2020 Jerry James <loganjerry@gmail.com> - 1.0.3-11
- Do not try to invoke native2ascii with JDK 9 or later
- Compile for JDK 8 instead of 5 for compatibility with JDK 11

* Sat Jan 18 2020 Jerry James <loganjerry@gmail.com> - 1.0.3-10
- Brought back into Fedora

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 22 2016 gil cattaneo <puntogil@libero.it> 1.0.3-3
- regenerate build-requires

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 21 2015 gil cattaneo <puntogil@libero.it> 1.0.3-1
- update to 1.0.3

* Wed Oct 21 2015 gil cattaneo <puntogil@libero.it> 1.0.2-3
- use upstream source archive
- remove duplicate file

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 24 2015 gil cattaneo <puntogil@libero.it> 1.0.2-1
- update to 1.0.2

* Sun Oct 06 2013 gil cattaneo <puntogil@libero.it> 1.0.1-1
- initial rpm
