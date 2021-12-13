Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          disruptor
Version:       3.3.6
Release:       9%{?dist}
Summary:       Concurrent Programming Framework
License:       ASL 2.0
URL:           http://lmax-exchange.github.io/disruptor/
Source0:       https://github.com/LMAX-Exchange/disruptor/archive/%{version}/%{name}-%{version}.tar.gz
Source1:       http://repo1.maven.org/maven2/com/lmax/%{name}/%{version}/%{name}-%{version}.pom
# see http://www.jmock.org/threading-synchroniser.html
Patch0:        disruptor-3.3.2-jmock.patch

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.hamcrest:hamcrest-library)

%if %{with_check}
BuildRequires: mvn(org.jmock:jmock-junit4)
BuildRequires: mvn(org.jmock:jmock-legacy)
%endif

%if 0
# Unavailable performance test deps
BuildRequires: mvn(org.hdrhistogram:HdrHistogram:1.2.1)
%endif

BuildArch:     noarch

%description
A High Performance Inter-Thread Messaging Library.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
# Cleanup
find . -name "*.class" -print -delete
find . -name "*.jar" -type f -print -delete

%patch0 -p1

cp -p %{SOURCE1} pom.xml

# Add OSGi support
%pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
%pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 . '
<extensions>true</extensions>
<configuration>
  <instructions>
    <Bundle-DocURL>%{url}</Bundle-DocURL>
    <Bundle-Name>${project.name}</Bundle-Name>
    <Bundle-Vendor>LMAX Disruptor Development Team</Bundle-Vendor>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

# fail to compile cause: incompatible hamcrest apis
rm -r src/test/java/com/lmax/disruptor/RingBufferTest.java \
 src/test/java/com/lmax/disruptor/RingBufferEventMatcher.java
# Failed to stop thread: Thread[com.lmax.disruptor.BatchEventProcessor@1d057a39,5,main]
rm -r src/test/java/com/lmax/disruptor/dsl/DisruptorTest.java
# Test fails due to incompatible jmock version
#rm -f src/test/java/com/lmax/disruptor/EventPollerTest.java

%mvn_file :%{name} %{name}

%build

%mvn_build --skip-tests -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%check
mvn test

%files -f .mfiles
%doc README.md
%license LICENCE.txt

%files javadoc -f .mfiles-javadoc
%license LICENCE.txt

%changelog
* Wed Aug 18 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.6-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Moving tests to the '%%check' section.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 11 2016 gil cattaneo <puntogil@libero.it> 3.3.6-1
- update to 3.3.6

* Thu Jun 23 2016 gil cattaneo <puntogil@libero.it> 3.3.4-1
- update to 3.3.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 gil cattaneo <puntogil@libero.it> 3.3.2-2
- build fix for jmock 2.8.1

* Wed Jun  3 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.2-1
- Update to upstream version 3.3.2

* Sun Feb 01 2015 gil cattaneo <puntogil@libero.it> 3.2.1-3
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 gil cattaneo <puntogil@libero.it> 3.2.1-1
- update to 3.2.1

* Wed Aug 14 2013 gil cattaneo <puntogil@libero.it> 3.2.0-1
- initial rpm
