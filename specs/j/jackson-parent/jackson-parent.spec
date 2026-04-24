# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          jackson-parent
Version:       2.18.1
Release: 5%{?dist}
Summary:       Parent pom for all Jackson components
License:       Apache-2.0

URL:           https://github.com/FasterXML/jackson-parent
Source0:       %{url}/archive/%{name}-%{version}.tar.gz
# jackson-parent package don't include the license file
# reported @ https://github.com/FasterXML/jackson-parent/issues/1
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.fasterxml:oss-parent:pom:)

BuildArch:      noarch
%if 0%{?fedora} || 0%{?rhel} >= 10
ExclusiveArch:  %{java_arches} noarch
%endif

%description
Project for parent pom for all Jackson components.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp -p %{SOURCE1} LICENSE
sed -i 's/\r//' LICENSE

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.18.1-4
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 28 2024 Packit <hello@packit.dev> - 2.18.1-1
- Update to version 2.18.1
- Resolves: rhbz#2322288

* Fri Sep 27 2024 Packit <hello@packit.dev> - 2.18-1
- Update to version 2.18
- Resolves: rhbz#2315058

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 12 2024 Packit <hello@packit.dev> - 2.17-1
- [maven-release-plugin] prepare release jackson-parent-2.17 (Tatu Saloranta)
- Prepare for 2.17 release (Tatu Saloranta)
- Fix version in pom (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2269107

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.16-4
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 23 2023 Chris Kelley <ckelley@redhat.com> - 2.16-1
- [maven-release-plugin] prepare release jackson-parent-2.16 (Tatu Saloranta)
- Prepare for 2.16 release (Tatu Saloranta)
- Update `oss-parent` dep to 56 (Tatu Saloranta)
- Back to snapshot (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Chris Kelley <ckelley@redhat.com> - 2.15-1
- Update to version 2.15

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Chris Kelley <ckelley@redhat.com> - 2.14-1
- Update to version 2.14
- Update to use SPDX licence

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.11-8
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.11-7
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.11-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon May 25 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11-1
- Update to version 2.11.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Fabio Valentini <decathorpe@gmail.com> - 2.10-1
- Update to version 2.10.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Mat Booth <mat.booth@redhat.com> - 2.9.1.2-1
- Update to latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Mat Booth <mat.booth@redhat.com> - 2.9.1-1
- Update to latest upstream release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 22 2016 gil cattaneo <puntogil@libero.it> 2.7-1.1
- update to 2.7-1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 28 2015 gil cattaneo <puntogil@libero.it> 2.6.2-1
- update to 2.6.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5-1
- update to 2.5

* Wed Jul 02 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- initial rpm
