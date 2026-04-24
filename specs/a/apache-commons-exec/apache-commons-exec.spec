# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_name exec
%global short_name commons-%{base_name}

Name:           apache-commons-exec
Version:        1.5.0
Release: 4%{?dist}
Summary:        Java library to reliably execute external processes from within the JVM
License:        Apache-2.0
URL:            https://commons.apache.org/proper/%{short_name}
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)

# Tests require /usr/bin/ping
BuildRequires:  iputils

%description
Commons Exec is a library for dealing with external process execution and
environment management in Java.


%package javadoc
Summary:        Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%autosetup -n %{short_name}-%{version}-src

# Disable junit-pioneer features since it's not (yet) available in Fedora
%pom_remove_dep org.junit-pioneer:junit-pioneer
find src/test/java/ -name "*.java" -exec sed  -i '/SetSystemProperty/d' {} \;


%build
# - Skip Exec34Test/Exec41Test/Exec60Test ("socket: Operation not permitted" on Koji)
# - Skip Exec57Test (it is unstable), see RHBZ #1202260
# - Skip Exec65Test (calls sudo)
%mvn_build -- \
  -Dcommons.osgi.symbolicName=org.apache.commons.exec \
  -Dcommons.packageId=exec \
  -Dtest=\!org.apache.commons.exec.issues.Exec34Test,\!org.apache.commons.exec.issues.Exec41Test,\!org.apache.commons.exec.issues.Exec57Test,\!org.apache.commons.exec.issues.Exec60Test,\!org.apache.commons.exec.issues.Exec65Test


%install
%mvn_install


%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc RELEASE-NOTES.txt


%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt


%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.5.0-3
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Sun Jan 26 2025 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.3-31
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 31 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-30
- Port to apache-commons-parent 65

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 09 2023 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3-26
- Fix RHBZ #2171437 (FTBFS)

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.3-23
- Rebuilt for Drop i686 JDKs

* Sun Feb 06 2022 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3-22
- Fix build with JDK 17

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.3-21
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Jiri Vanek <jvanek@redhat.com> - 1.3-16
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sat Jul 11 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3-15
- Fix build with JDK-11

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.3-14
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 08 2019 Mat Booth <mat.booth@redhat.com> - 1.3-11
- Rebuild to regenerate OSGi metadata

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-5
- Regenerate build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-2
- Skip running unstable Exec57Test
- Resolves: rhbz#1202260

* Tue Dec 02 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3-1
- Update to 1.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Feb 03 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2-1
- Update to 1.2
- Adapt to current guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Mat Booth <fedora@matbooth.co.uk> - 1.1-10
- Add missing BRs

* Mon Jul 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-9
- Install NOTICE file with javadoc package
- Resolves: rhbz#984417

* Mon Feb 18 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.1-4
- Build with maven 3.
- Adapt to current guidelines.

* Mon Mar 07 2011 Tom Callaway <spot@fedoraproject.org> - 1.1-3
- fix maven fragment

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Mohamed El Morabity <melmorabity@fedorapeople.org> - 1.1-1
- Update to 1.1

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-4
- BR iputils. Needed by tests.

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-3
- Change maven plugin names to the new ones.

* Wed Feb  3 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 1.0.1-2
- Add missing %%post/%%postun Requires
- Use macro %%{_mavendepmapfragdir} instead of %%{_datadir}/maven2/pom
- Unown directories %%{_mavenpomdir} and %%{_mavendepmapfragdir}

* Mon Jan 18 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 1.0.1-1
- Initial RPM release
