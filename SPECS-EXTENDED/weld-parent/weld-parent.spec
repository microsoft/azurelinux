Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:             weld-parent
Version:          39
Release:          4%{?dist}
Summary:          Parent POM for Weld
License:          ASL 2.0
URL:              http://weld.cdi-spec.org
Source0:          https://github.com/weld/parent/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:          %{name}-LICENSE.txt

BuildArch:        noarch

BuildRequires:    maven-local
BuildRequires:    mvn(org.apache.maven.plugins:maven-install-plugin)
BuildRequires:    mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:    mvn(org.codehaus.mojo:build-helper-maven-plugin)

%description
Parent POM for Weld

%prep
%setup -q -n parent-%{version}
cp %{SOURCE1} ./LICENSE.txt

%pom_remove_plugin ":maven-enforcer-plugin"
%pom_remove_plugin ":maven-remote-resources-plugin"
%pom_remove_plugin ":buildnumber-maven-plugin"

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%changelog
* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 39-4
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 39-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 20 2019 Fabio Valentini <decathorpe@gmail.com> - 39-1
- Update to version 39.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 34-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 34-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 34-3
- Remove buildnumber-plugin

* Wed Jun 15 2016 gil cattaneo <puntogil@libero.it> 34-2
- Add missing BRs on maven-source-plugin, buildnumber-maven-plugin

* Mon Jun 06 2016 gil cattaneo <puntogil@libero.it> 34-1
- Upstream release 34

* Tue Mar 01 2016 gil cattaneo <puntogil@libero.it> 31-4
- remove enforcer plugin support
- related to rhbz#1308237,1308238
- use BRs mvn()-like
- introduce license macro

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Marek Goldmann <mgoldman@redhat.com> - 31-1
- Upstream release 31

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 26-2
- Rebuild to regenerate broken POM files
- Related: rhbz#1021484

* Tue Oct 22 2013 Marek Goldmann <mgoldman@redhat.com> - 26-1
- Upstream release 26

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Michal Srb <msrb@redhat.com> - 17-8
- Add ASL 2.0 license text
- Add missing BR: maven-plugin-build-helper, maven-install-plugin

* Tue Feb 19 2013 Marek Goldmann <mgoldman@redhat.com> - 17-7
- Added maven-shared BR

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 17-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Jul 23 2012 Marek Goldmann <mgoldman@redhat.com> - 17-4
- Fixed BR, removed maven plugins from R

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Marek Goldmann <mgoldman@redhat.com> 17-2
- Added build section

* Wed Mar 14 2012 Marek Goldmann <mgoldman@redhat.com> 17-1
- Initial packaging

