# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global giturl  https://github.com/antlr/stringtemplate4

Name:           stringtemplate4
Version:        4.3.4
Release: 10%{?dist}
Summary:        A Java template engine
License:        BSD-3-Clause
URL:            http://www.stringtemplate.org/
VCS:            git:%{giturl}.git
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         %{giturl}/archive/ST4-%{version}/%{name}-%{version}.tar.gz
# Adapt to JDK 11
Patch:          %{name}-java11.patch
# Adapt tests to JDK 21
Patch:          %{name}-java21.patch

BuildRequires:  maven-local-openjdk21
BuildRequires:  mesa-dri-drivers
BuildRequires:  mutter
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.antlr:antlr-runtime) >= 3.5.2
BuildRequires:  mvn(org.antlr:antlr3-maven-plugin) >= 3.5.2
BuildRequires:  xwayland-run

%description
StringTemplate is a java template engine (with ports for
C# and Python) for generating source code, web pages,
emails, or any other formatted text output. StringTemplate
is particularly good at multi-targeted code generators,
multiple site skins, and internationalization/localization.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%autosetup -p1 -n %{name}-ST4-%{version}

%conf
# sonatype-oss-parent is deprecated in Fedora
%pom_remove_parent

%build
xwfb-run -c mutter -- %mvn_build

%install
%mvn_install

%files -f .mfiles
%doc CHANGES.txt README.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Jul 30 2025 jiri vanek <jvanek@redhat.com> - 4.3.4-9
- Rrevert to jdk21

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 4.3.4-8
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jerry James <loganjerry@gmail.com> - 4.3.4-4
- Migrate from xvfb-run to xwfb-run
- Fix the VCS field
- Minor spec file simplifications

* Wed Feb 28 2024 Jerry James <loganjerry@gmail.com> - 4.3.4-4
- Adapt expected test output to JDK 21 (rhbz#2266689)

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 4.3.4-4
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jan 23 2023 Jerry James <loganjerry@gmail.com> - 4.3.4-1
- Version 4.3.4

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Jerry James <loganjerry@gmail.com> - 4.3.3-3
- Convert License tag to SPDX

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 4.3.3-2
- Rebuilt for Drop i686 JDKs

* Wed Apr 13 2022 Jerry James <loganjerry@gmail.com> - 4.3.3-1
- Version 4.3.3

* Fri Apr  8 2022 Jerry James <loganjerry@gmail.com> - 4.3.2-1
- Version 4.3.2

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.3.1-9
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov  6 2021 Jerry James <loganjerry@gmail.com> - 4.3.1-7
- Update the -java11 patch to fix tests too

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 24 2020 Jerry James <loganjerry@gmail.com> - 4.3.1-4
- Remove dependency on deprecated sonatype-oss-parent

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 4.3.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jun 23 2020 Jerry James <loganjerry@gmail.com> - 4.3.1-1
- Version 4.3.1
- Add -java11 patch to adapt to JDK 11

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jerry James <loganjerry@gmail.com> - 4.3-1
- Version 4.3

* Mon Nov 11 2019 Jerry James <loganjerry@gmail.com> - 4.2-1
- Version 4.2

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.8-1
- Update to upstream version 4.0.8

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.4-8
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.0.4-7
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.4-4
- Fix file permissions

* Thu Jul 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.0.4-3
- Fix build. stringtemplate4 now needs itself to build so add it to
  classpath

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.0.4-1
- Initial version of the package

