Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           google-gson
Version:        2.8.6
Release:        4%{?dist}
Summary:        Java lib for conversion of Java objects into JSON representation
License:        ASL 2.0
URL:            https://github.com/google/gson
Source0:        https://github.com/google/gson/archive/gson-parent-%{version}.tar.gz
Patch0:         osgi-export-internal.patch
Patch1:         java-eight-build.patch

# This commit added a dependency on templating-maven-plugin,
# we don't want it nor need it, so we revert it
# https://github.com/google/gson/commit/d84e26d
Patch2:         no-templating-maven-plugin.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

%description
Gson is a Java library that can be used to convert a Java object into its
JSON representation. It can also be used to convert a JSON string into an
equivalent Java object. Gson can work with arbitrary Java objects including
pre-existing objects that you do not have source-code of.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n gson-gson-parent-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# remove unnecessary dependency on parent POM
%pom_remove_parent

# presence of these files breaks builds with Java 8
find -name "module-info.java" -print -delete

# Use felix maven-bundle-plugin only for OSGi metadata
%pom_remove_plugin :bnd-maven-plugin gson
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-bundle-plugin']" "<configuration>
    <instructions>
      <_include>bnd.bnd</_include>
    </instructions>
  </configuration>
  <executions>
    <execution>
      <id>create-manifest</id>
      <phase>process-classes</phase>
      <goals><goal>manifest</goal></goals>
    </execution>
  </executions>" gson

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc README.md CHANGELOG.md UserGuide.md

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.8.6-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Fabio Valentini <decathorpe@gmail.com> - 2.8.6-2
- Remove unnecessary dependency on parent POM.

* Fri Nov 01 2019 Fabio Valentini <decathorpe@gmail.com> - 2.8.6-1
- Update to version 2.8.6.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 21 2018 Alexander Kurtakov <akurtako@redhat.com> 2.8.2-1
- Update to upstream 2.8.2 release.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 29 2017 Mat Booth <mat.booth@redhat.com> - 2.8.1-2
- Also export internal packages in OSGi metadata

* Fri Aug 25 2017 Mat Booth <mat.booth@redhat.com> - 2.8.1-1
- Update to latest upstream release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.1-6
- Remove unneeded maven-javadoc-plugin invocation

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 02 2016 Michael Simacek <msimacek@redhat.com> - 2.3.1-4
- Skip default jar plugin execution to fix FTBFS

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Michael Simacek <msimacek@redhat.com> - 2.3.1-1
- Update to upstream version 2.3.1

* Mon Apr 20 2015 Michael Simacek <msimacek@redhat.com> - 2.2.4-8
- Remove test that relies on networking

* Mon Mar 30 2015 Michael Simacek <msimacek@redhat.com> - 2.2.4-7
- Remove dependency on cobertura

* Tue Jun 10 2014 Severin Gehwolf <sgehwolf@redhat.com> - 2.2.4-6
- Move to xmvn style packaging.
- Fix FTBFS. Resolves RHBZ#1106707.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.4-4
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.2.4-3
- Add BR maven-install-plugin, resolves RHBZ#992422.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.4-1
- Update to newer upstream release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.2-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Dec 19 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.2.2-2
- Add BR for surefire junit provider.

* Wed Dec 19 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.2.2-1
- Update to latest upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 2 2012 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-2
- Add missing BR on maven-enforcer-plugin.
- Remove no longer needed parts of the spec.

* Mon Jul 2 2012 Krzysztof Daniel <kdaniel@redhat.com> 2.2.1-1
- Update to latest upstream 2.2.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 13 2011 Jaromir Capik <jcapik@redhat.com> - 1.7.1-3
- Removal of failing testInetAddressSerializationAndDeserialization

* Wed May 11 2011 Jaromir Capik <jcapik@redhat.com> - 1.7.1-2
- Conversion of CR+LF to LF in the license file

* Tue May 10 2011 Jaromir Capik <jcapik@redhat.com> - 1.7.1-1
- Initial version of the package
