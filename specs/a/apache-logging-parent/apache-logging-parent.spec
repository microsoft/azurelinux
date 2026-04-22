# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           apache-logging-parent
Summary:        Parent pom for Apache Logging Services projects
Version:        9
Release: 11%{?dist}
License:        Apache-2.0

URL:            https://logging.apache.org/
Source0:        https://repo1.maven.org/maven2/org/apache/logging/logging-parent/%{version}/logging-parent-%{version}-source-release.zip
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache:apache:pom:)

%description
Parent pom for Apache Logging Services projects.


%prep
%setup -q -n logging-parent-logging-parent-%{version}
cp -p %SOURCE1 LICENSE

%pom_remove_plugin com.diffplug.spotless:spotless-maven-plugin

%build
%mvn_build


%install
%mvn_install


%files -f .mfiles
%license LICENSE


%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 9-10
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 9-6
- Do not obsolete jboss-parent

* Thu Feb 01 2024 Marian Koncek <mkoncek@redhat.com> - 9-5
- Add ExclusiveArch field

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Chris Kelley <ckelley@redhat.com> - 9-1
- Unretire package; update to version 9.

* Mon Jul 29 2019 Fabio Valentini <decathorpe@gmail.com> - 2-1
- Update to version 2.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Michael Simacek <msimacek@redhat.com> - 1-1
- Initial packaging

