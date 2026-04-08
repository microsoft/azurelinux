# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jackson-bom
Version:        2.18.2
Release:        4%{?dist}
Summary:        Bill of materials POM for Jackson projects
License:        Apache-2.0

URL:            https://github.com/FasterXML/jackson-bom
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.fasterxml.jackson:jackson-parent:pom:) >= 2.17
BuildRequires:  mvn(junit:junit)

BuildArch:      noarch
%if 0%{?fedora} || 0%{?rhel} >= 10
ExclusiveArch:  %{java_arches} noarch
%endif

%description
A "bill of materials" POM for Jackson dependencies.

%prep
%setup -q -n %{name}-%{name}-%{version}

# Disable plugins not needed during RPM builds
%pom_remove_plugin ":maven-enforcer-plugin" base
%pom_remove_plugin ":nexus-staging-maven-plugin" base

# New EE coords
%pom_change_dep "javax.activation:javax.activation-api" "jakarta.activation:jakarta.activation-api" base

# Remove dep on junit-bom
%pom_remove_dep "org.junit:junit-bom" base

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.18.2-4
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 28 2024 Packit <hello@packit.dev> - 2.18.2-1
- Update to version 2.18.2
- Resolves: rhbz#2322286

* Fri Sep 27 2024 Packit <hello@packit.dev> - 2.18.0-1
- Update to version 2.18.0
- Resolves: rhbz#2315055

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Packit <hello@packit.dev> - 2.17.2-1
- Update to version 2.17.2
- Resolves: rhbz#2296001

* Sun May 05 2024 Packit <hello@packit.dev> - 2.17.1-1
- Update to version 2.17.1
- Resolves: rhbz#2279120

* Fri Mar 15 2024 Chris Kelley <ckelley@redhat.com> - 2.17.0-2
- Fix build issue with introduction of JUnit5

* Tue Mar 12 2024 Packit <hello@packit.dev> - 2.17.0-1
- [maven-release-plugin] prepare release jackson-bom-2.17.0 (Tatu Saloranta)
- Prepare for 2.17.0 release (Tatu Saloranta)
- Update to 2.17 jackson-parent (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- [maven-release-plugin] prepare release jackson-bom-2.17.0-rc1 (Tatu Saloranta)
- Prepare for 2.17.0-rc1 (Tatu Saloranta)
- Add `jackson-jr-extension-javatime` (to be included in 2.17) (Tatu Saloranta)
- Add JDK 21 on ci (Tatu Saloranta)
- Add managed version dependency to JUnit 5 (Tatu Saloranta)
- Prepare for 2.17.0-rc1 release cycle (Tatu Saloranta)
- Update maven properies version (Tatu Saloranta)
- Further update to refer to the very latest released version, 2.16.1 (Tatu Saloranta)
- latest release version in readme (SanviT)
- Start 2.17 branch (Tatu Saloranta)
- Resolves rhbz#2269275

* Sat Mar 09 2024 Packit <hello@packit.dev> - 2.16.2-1
- [maven-release-plugin] prepare release jackson-bom-2.16.2 (Tatu Saloranta)
- Prepare for 2.16.2 release (Tatu Saloranta)
- Resolves rhbz#2268705

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.16.1-3
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Marco Fargetta <mfargett@redhat.com> - 2.16.1-1
- [maven-release-plugin] prepare release jackson-bom-2.16.1 (Tatu Saloranta)
- Prepare for 2.16.1 release (Tatu Saloranta)
- back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 15 2023 Packit <hello@packit.dev> - 2.16.0-1
- [maven-release-plugin] prepare release jackson-bom-2.16.0 (Tatu Saloranta)
- Prepare for 2.16.0 release (Tatu Saloranta)
- Add version of `jackson-module-android-record` (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2249891

* Mon Nov 06 2023 Chris Kelley <ckelley@redhat.com> - 2.15.3-1
- [maven-release-plugin] prepare release jackson-bom-2.15.3 (Tatu Saloranta)
- Prepare for 2.15.3 release (Tatu Saloranta)
- Update `nexus-staging-maven-plugin` dep to 1.6.13 (from 1.6.8) (Tatu Saloranta)
- To 2.15.3-SNAPSHOT (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Chris Kelley <ckelley@redhat.com> - 2.15.2-1
- Update to version 2.15.2

* Tue Apr 25 2023 Chris Kelley <ckelley@redhat.com> - 2.15.0-1
- Update to version 2.15.0

* Tue Jan 31 2023 Chris Kelley <ckelley@redhat.com> - 2.14.2-1
- Update to version 2.14.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Chris Kelley <ckelley@redhat.com> - 2.14.1-1
- Update to version 2.14.1

* Tue Nov 08 2022 Chris Kelley <ckelley@redhat.com> - 2.14.0-1
- Update to version 2.14
- Uptade to use SPDX licence

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-6
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-5
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Fabio Valentini <decathorpe@gmail.com> - 2.11.4-1
- Update to version 2.11.4.

* Wed Oct 14 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.3-1
- Update to version 2.11.3.

* Sat Aug 08 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.2-1
- Update to version 2.11.2.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.11.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Jul 06 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.1-1
- Update to version 2.11.1.

* Mon May 25 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.0-1
- Update to version 2.11.0.

* Fri May 08 2020 Fabio Valentini <decathorpe@gmail.com> - 2.10.4-1
- Update to version 2.10.4.

* Tue Mar 03 2020 Fabio Valentini <decathorpe@gmail.com> - 2.10.3-1
- Update to version 2.10.3.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Fabio Valentini <decathorpe@gmail.com> - 2.10.2-1
- Update to version 2.10.2.

* Wed Nov 13 2019 Fabio Valentini <decathorpe@gmail.com> - 2.10.1-1
- Update to version 2.10.1.

* Thu Oct 3 2019 Alexander Scheel <ascheel@redhat.com> - 2.10.0-1
- Update to latest upstream release

* Thu Sep 12 2019 Alexander Scheel <ascheel@redhat.com> - 2.9.9-1
- Update to latest upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Mat Booth <mat.booth@redhat.com> - 2.9.8-1
- Update to latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-1
- Update to latest upstream release

* Thu Jan 18 2018 Mat Booth <mat.booth@redhat.com> - 2.9.3-1
- Initial packaging

