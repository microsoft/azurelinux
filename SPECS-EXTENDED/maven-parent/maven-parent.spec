Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:           maven-parent
Version:        41
Release:        7%{?dist}
Summary:        Apache Maven parent POM
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://maven.apache.org
Source0:        https://repo1.maven.org/maven2/org/apache/maven/%{name}/%{version}/%{name}-%{version}-source-release.zip#/%{name}-%{version}.zip
BuildRequires:  apache-parent
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  unzip
Requires:       apache-parent
BuildArch:      noarch


%description
Apache Maven parent POM file used by other Maven projects.

%prep
%setup -q
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :apache-rat-plugin

%build

%install
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom

%files -f .mfiles
%doc LICENSE NOTICE

%changelog
* Fri Feb 14 2025 Archana Shettigar <v-shettigara@microsoft.com> - 41-7
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
- Use javapackages-bootstrap to avoid build cycle.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 41-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 41-5
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 41-4
- bump of release for for java-21-openjdk as system jdk

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 04 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 41-1
- Update to upstream version 41

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 40-2
- Rebuild

* Wed Aug 16 2023 Marian Koncek <mkoncek@redhat.com> - 40-1
- Update to upstream version 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 31 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 39-2
- Rebuild with no changes

* Thu Mar 23 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 39-1
- Update to upstream version 39

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 06 2022 Marian Koncek <mkoncek@redhat.com> - 37-1
- Update to upstream version 37

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 21 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 35-1
- Update to upstream version 35

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 34-10
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 34-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 34-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 34-7
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 34-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Jun 22 2020 Marian Koncek <mkoncek@redhat.com> - 34-1
- Update to upstream version 34

* Fri Mar 27 2020 Severin Gehwolf <sgehwolf@redhat.com> - 34-3
- Remove javadoc taglet configuration which is not longer available

* Wed Mar 25 2020 Severin Gehwolf <sgehwolf@redhat.com> - 34-2
- Remove explicit requirement on maven-plugin-tools-javadoc

* Mon Mar 02 2020 Fabio Valentini <decathorpe@gmail.com> - 34-1
- Update to version 34.
- Switch to HTTPS URL for source downloads.
- Remove upstream patch that's part of this release.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 33-3
- Mass rebuild for javapackages-tools 201902

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 33-2
- Mass rebuild for javapackages-tools 201901

* Fri May 17 2019 Fabio Valentini <decathorpe@gmail.com> - 33-1
- Update to upstream version 33
- Obsolete maven-shared and maven-plugins-pom.

* Tue May 14 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 33-1
- Update to upstream version 33

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 27-1
- Update to upstream version 27

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 26-1
- Update to upstream version 26

* Thu Oct 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 25-1
- Update to upstream version 25

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 24-2
- Rebuild to regenerate Maven auto-requires

* Wed Apr  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 24-1
- Update to upstream version 24

* Mon Mar 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 23-1
- Update to upstream version 23

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 20-6
- Rebuild to regenerate Maven provides

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 20-4
- Build with xmvn

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 20-4
- Add missing BR/R: apache-parent
- Update to current packaging guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 20-1
- Initial version of the package
