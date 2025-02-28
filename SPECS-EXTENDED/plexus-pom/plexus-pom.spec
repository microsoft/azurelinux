Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:          plexus-pom
Version:       16
Release:       5%{?dist}
Summary:       Root Plexus Projects POM
License:       Apache-2.0
URL:           https://github.com/codehaus-plexus/plexus-pom
Source0:       https://github.com/codehaus-plexus/plexus-pom/archive/plexus-%{version}.tar.gz
Source1:       https://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  javapackages-local-bootstrap
BuildArch:     noarch


%description
The Plexus project provides a full software stack for creating and
executing software projects. This package provides parent POM for
Plexus packages.

%prep
%autosetup -n plexus-pom-plexus-%{version}
cp -p %{SOURCE1} LICENSE

%pom_remove_dep org.junit:junit-bom
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-enforcer-plugin
cp -p %{SOURCE1} LICENSE

%build

%install
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/plexus.pom
%add_maven_depmap %{name}/plexus.pom

%files -f .mfiles
%license LICENSE

%changelog
* Wed Feb 12 2025 Archana Shettigar <v-shettigara@microsoft.com> - 16-5
- Initial Azure Linux import from Fedora 41 (license: MIT).
- Use javapackages-local-bootstrap to avoid build cycle.
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 16-3
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 16-2
- bump of release for for java-21-openjdk as system jdk

* Thu Feb 01 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 16-1
- Update to upstream version 16

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Marian Koncek <mkoncek@redhat.com> - 15-1
- Update to upstream version 15

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 14-2
- Rebuild

* Wed Aug 16 2023 Marian Koncek <mkoncek@redhat.com> - 14-1
- Update to upstream version 14

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 06 2022 Marian Koncek <mkoncek@redhat.com> - 10-1
- Update to upstream version 10

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 24 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 8-1
- Update to upstream version 8

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 7-5
- Rebuilt for java-17-openjdk as system jdk

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 7-2
- Bootstrap build
- Non-bootstrap build

* Mon Feb 01 2021 Fabio Valentini <decathorpe@gmail.com> - 7-1
- Update to version 7.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 26 2021 Marian Koncek <mkoncek@redhat.com> - 7-1
- Update to upstream version 7

* Fri Dec  4 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.5-1
- Update to upstream version 6.5

* Sat Oct 24 2020 Fabio Valentini <decathorpe@gmail.com> - 6.5-1
- Update to version 6.5.

* Fri Sep 11 2020 Marian Koncek <mkoncek@redhat.com> - 6.4-2
- Update to upstream version 6.4

* Sun Aug 16 2020 Fabio Valentini <decathorpe@gmail.com> - 6.4-1
- Update to version 6.4.

* Wed Jul 29 2020 Marian Koncek <mkoncek@redhat.com> - 6.3-1
- Update to upstream version 6.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Fabio Valentini <decathorpe@gmail.com> - 6.3-1
- Update to version 6.3.

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 6.2-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Mar 02 2020 Fabio Valentini <decathorpe@gmail.com> - 6.2-1
- Update to version 6.2.

* Thu Feb 13 2020 Fabio Valentini <decathorpe@gmail.com> - 6.1-1
- Update to version 6.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.1-2
- Mass rebuild for javapackages-tools 201902

* Thu Oct 24 2019 Fabio Valentini <decathorpe@gmail.com> - 5.1-1
- Update to version 5.1.

* Mon Jul 29 2019 Marian Koncek <mkoncek@redhat.com> - 5.1-1
- Update to upstream version 5.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0-3
- Mass rebuild for javapackages-tools 201901

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 11 2018 Marian Koncek <mkoncek@redhat.com> - 5.0-4
- Remove Group tag

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0-1
- Update to upstream version 5.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.3-1
- Update to upstream version 3.3.3

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-10
- Update upstream URL

* Wed Feb 11 2015 gil cattaneo <puntogil@libero.it> 3.3.1-9
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-7
- Rebuild to regenerate Maven auto-requires

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-6
- Rebuild to regenerate provides

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-4
- Build with xmvn

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.3.1-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Dec 08 2012 gil cattaneo <puntogil@libero.it> 3.3.1-1
- Update to 3.3.1

* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.1-3
- Install LICENSE file
- Resolves: rhbz#878825

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 gil cattaneo <puntogil@libero.it> 3.0.1-1
- initial rpm
