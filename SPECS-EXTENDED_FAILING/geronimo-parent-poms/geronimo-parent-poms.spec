Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           geronimo-parent-poms
Version:        1.6
Release:        30%{?dist}
Summary:        Parent POM files for geronimo-specs
License:        ASL 2.0
URL:            http://geronimo.apache.org/
BuildArch:      noarch

# Following the parent chain all the way up ...
Source0:        http://svn.apache.org/repos/asf/geronimo/specs/tags/specs-parent-%{version}/pom.xml
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

# Dependencies and plugins from the POM files
Provides:       geronimo-specs = %{version}-%{release}

%description
The Project Object Model files for the geronimo-specs modules.

%prep
%setup -c -T
cp -p %{SOURCE0} .
cp -p %{SOURCE1} LICENSE
%pom_remove_parent
# IDEA plugin is not really useful in Fedora
%pom_remove_plugin :maven-idea-plugin
%mvn_alias : org.apache.geronimo.specs:specs

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-22
- Add missing build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-18
- Rebuild to regenerate Maven auto-requires

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-17
- Update to current packaging guidelines

* Mon Dec 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-16
- Convert tabs to spaces

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-15
- Remove maven-idea-plugin

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.6-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 1.6-12
- Build with xmvn

* Thu Aug 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-11
- Install LICENSE file
- Add missing R: jpackage-utils
- Update to current packaging guidelines

* Mon Aug  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-10
- Remove pom.xml from SCM

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Tomas Radej <tradej@redhat.com> - 1.6-8
- Removed maven-pmd-plugin R

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep  7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.6-6
- Remove genesis poms from package (split into separate package)
- Use new macro for depmaps

* Thu May  5 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.6-5
- Add compatibility depmap for geronimo.specs:specs-parent
- Fixes according to new guidelines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  3 2010 Mary Ellen Foster <mefoster at gmail.com> 1.6-3
- Fix tabs and spaces in srpm
- Remove config flag from mavendepmapfragdir
- Add jpackage-utils to the BuildRequires

* Tue Jan 19 2010 Mary Ellen Foster <mefoster at gmail.com> 1.6-2
- Don't include the apache root pom; it's already in maven2-common-poms
- Double check the dependencies to include only what's in the POMs
- Add initial Provides for the genesis stuff
- Fix changelog

* Mon Jan 18 2010 Mary Ellen Foster <mefoster at gmail.com> 1.6-1
- Initial package
