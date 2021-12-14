Vendor:         Microsoft Corporation
Distribution:   Mariner
%global base_name woodstox

Name:           woodstox-core
Summary:        High-performance XML processor
Version:        6.2.3
Release:        2%{?dist}
License:        ASL 2.0 or LGPLv2+ or BSD

URL:            https://github.com/FasterXML/woodstox
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

# Port to latest OSGi APIs
Patch0:         0001-Allow-building-against-OSGi-APIs-newer-than-R4.patch
# Drop requirements on defunct optional dependencies: msv and relaxng
Patch1:         0002-Patch-out-optional-support-for-msv-and-relax-schema-.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.fasterxml:oss-parent:pom:)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.codehaus.woodstox:stax2-api)
BuildRequires:  mvn(org.osgi:osgi.core)

%description
Woodstox is a high-performance validating namespace-aware StAX-compliant
(JSR-173) Open Source XML-processor written in Java.
XML processor means that it handles both input (== parsing)
and output (== writing, serialization)), as well as supporting tasks
such as validation.


%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package contains the API documentation for %{name}.


%prep
%autosetup -p1 -n %{base_name}-%{name}-%{version}

%pom_remove_dep relaxngDatatype:relaxngDatatype
%pom_remove_dep net.java.dev.msv:
rm -rf src/main/java/com/ctc/wstx/msv

# Remove tests for msv and relaxng functionality
rm -rf src/test/java/wstxtest/msv src/test/java/wstxtest/vstream/TestRelaxNG.java src/test/java/stax2/vwstream/W3CSchemaWrite*Test.java \
  src/test/java/failing/{TestRelaxNG,TestW3CSchemaTypes,TestW3CSchemaComplexTypes,TestW3CDefaultValues}.java

# Unnecessary for RPM builds
%pom_remove_plugin :nexus-staging-maven-plugin

# we don't care about Java 9 modules (yet)
%pom_remove_plugin :moditect-maven-plugin

# replace felix-osgi-core with osgi-core
%pom_change_dep -r :org.osgi.core org.osgi:osgi.core

%mvn_alias ":{woodstox-core}" :@1-lgpl :@1-asl :wstx-asl :wstx-lgpl \
    org.codehaus.woodstox:@1 org.codehaus.woodstox:@1-asl \
    org.codehaus.woodstox:@1-lgpl org.codehaus.woodstox:wstx-lgpl \
    org.codehaus.woodstox:wstx-asl

%mvn_file : %{name}{,-asl,-lgpl}


%build
%mvn_build --xmvn-javadoc


%install
%mvn_install


%files -f .mfiles
%doc README.md
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.2.3-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Sat Oct 17 08:41:11 +03 2020 ElXreno <elxreno@gmail.com> - 6.2.3-1
- Update to version 6.2.3

* Wed Oct 14 13:48:17 +03 2020 ElXreno <elxreno@gmail.com> - 6.2.2-1
- Update to version 6.2.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 6.2.1-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jun 23 2020 ElXreno <elxreno@gmail.com> - 6.2.1-3
- Rebuild

* Thu Jun 11 2020 Jiri Vanek <jvanek@redhat.com> - 6.2.1-2
- javadoc geeration  moved to  --xmvn-javadoc

* Sat May 16 2020 Fabio Valentini <decathorpe@gmail.com> - 6.2.1-1
- Update to version 6.2.1.

* Sun May 10 2020 Fabio Valentini <decathorpe@gmail.com> - 6.2.0-1
- Update to version 6.2.0.

* Wed Apr 22 2020 Mat Booth <mat.booth@redhat.com> - 6.1.1-2
- Drop optional support for defunct validation libs (msv and relaxng)

* Mon Mar 02 2020 Fabio Valentini <decathorpe@gmail.com> - 6.1.1-1
- Update to version 6.1.1.

* Thu Feb 13 2020 Fabio Valentini <decathorpe@gmail.com> - 6.0.3-1
- Update to version 6.0.3.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Fabio Valentini <decathorpe@gmail.com> - 6.0.2-1
- Update to version 6.0.2.

* Wed Sep 18 2019 Mat Booth <mat.booth@redhat.com> - 6.0.1-2
- Port to newer OSGi API

* Wed Sep 18 2019 Fabio Valentini <decathorpe@gmail.com> - 6.0.1-1
- Update to version 6.0.1.

* Thu Aug 01 2019 Fabio Valentini <decathorpe@gmail.com> - 5.2.1-1
- Update to version 5.2.1.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Michael Simacek <msimacek@redhat.com> - 5.0.3-1
- Update to upstream version 5.0.3

* Mon Jul 04 2016 Michael Simacek <msimacek@redhat.com> - 5.0.2-1
- Update to upstream version 5.0.2

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.1-1
- Update to upstream version 5.0.1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Michael Simacek <msimacek@redhat.com> - 5.0.0-2
- Fix missing classes and aliases
- Enable tests

* Mon Mar 23 2015 Michael Simacek <msimacek@redhat.com> - 5.0.0-1
- Update to upstream version 5.0.0

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-6
- Remove build-requires on jvnet-parent

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-4
- Add aliases: ":wstx-asl" ":wstx-lgpl"

* Thu Oct  3 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-3
- Fix usage of %%mvn_alias

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-1
- Update to upstream version 4.2.0

* Thu Jun 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-6
- Install NOTICE file with javadoc package
- Update to current packaging guidelines

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4.1.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Jaromir Capik <jcapik@redhat.com> - 4.1.2-1
- Initial version
