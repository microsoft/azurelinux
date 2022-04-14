Vendor:         Microsoft Corporation
Distribution:   Mariner
%global namedreltag %nil
%global namedversion %{version}%{?namedreltag}

Name:          jctools
Version:       2.1.2
Release:       7%{?dist}
Summary:       Java Concurrency Tools for the JVM
License:       ASL 2.0
URL:           http://jctools.github.io/JCTools/
Source0:       https://github.com/JCTools/JCTools/archive/v%{namedversion}/%{name}-%{namedversion}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(com.github.javaparser:javaparser-core)
BuildRequires:  mvn(com.google.guava:guava-testlib)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires:  mvn(org.ow2.asm:asm-util)

%if %{with_check}
BuildRequires:  mvn(org.hamcrest:hamcrest-all)
BuildRequires:  mvn(junit:junit)
%endif

BuildArch:     noarch

%description
This project aims to offer some concurrent data structures
currently missing from the JDK:

° SPSC/MPSC/SPMC/MPMC Bounded lock free queues
° SPSC/MPSC Unbounded lock free queues
° Alternative interfaces for queues
° Offheap concurrent ring buffer for ITC/IPC purposes
° Single Writer Map/Set implementations
° Low contention stats counters
° Executor

%package channels
Summary:       JCTools Channel implementations

%description channels
Channel implementations for the
Java Concurrency Tools Library.

%package experimental
Summary:       JCTools Experimental implementations

%description experimental
Experimental implementations for the
Java Concurrency Tools Library.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%package parent
Summary:       JCTools Parent POM

%description parent
JCTools Parent POM.

%prep
%setup -q -n JCTools-%{namedversion}
# Cleanup
find . -name '*.class' -print -delete
find . -name '*.jar' -print -delete

# Remove failure-prone tests (race condition?)
rm jctools-core/src/test/java/org/jctools/queues/MpqSanityTestMpscCompound.java
rm jctools-core/src/test/java/org/jctools/queues/atomic/AtomicMpqSanityTestMpscCompound.java
rm jctools-core/src/test/java/org/jctools/maps/NonBlockingHashMapTest.java

%pom_xpath_set pom:project/pom:version %{namedversion}
%pom_xpath_set -r pom:parent/pom:version %{namedversion} %{name}-{build,core,channels,experimental}

# Remove plugins unnecessary for RPM builds
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :coveralls-maven-plugin
%pom_remove_plugin :jacoco-maven-plugin
%pom_remove_plugin :maven-source-plugin %{name}-core
%pom_remove_plugin :maven-javadoc-plugin %{name}-core

# Unavailable deps
%pom_disable_module %{name}-benchmarks
%pom_disable_module %{name}-concurrency-test

# Modern asm deps
%pom_change_dep ":asm-all" ":asm-util" jctools-{channels,experimental}

# Add OSGi support
for mod in core experimental; do
 %pom_xpath_set "pom:project/pom:packaging" bundle %{name}-${mod}
 %pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 %{name}-${mod} '
 <extensions>true</extensions>
 <executions>
   <execution>
     <id>bundle-manifest</id>
     <phase>process-classes</phase>
     <goals>
       <goal>manifest</goal>
     </goals>
   </execution>
 </executions>
 <configuration>
  <excludeDependencies>true</excludeDependencies>
 </configuration>'
done

# No need to package internal build tools
%mvn_package :jctools-build __noinstall

%build
%mvn_build -s --skip-tests

%install
%mvn_install

%check
mvn test

%files -f .mfiles-%{name}-core
%doc README.md
%license LICENSE

%files channels -f .mfiles-%{name}-channels

%files experimental -f .mfiles-%{name}-experimental

%files javadoc -f .mfiles-javadoc
%license LICENSE

%files parent -f .mfiles-%{name}-parent
%license LICENSE

%changelog
* Wed Aug 18 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.2-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Moving tests to the '%%check' section.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Mat Booth <mat.booth@redhat.com> - 2.1.2-5
- Skip problematic NonBlockingHashMapTest

* Mon Sep 09 2019 Fabio Valentini <decathorpe@gmail.com> - 2.1.2-4
- Disable another failure-prone unreliable test.

* Mon Sep 09 2019 Fabio Valentini <decathorpe@gmail.com> - 2.1.2-3
- Disable failure-prone unreliable test.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 13 2019 Mat Booth <mat.booth@redhat.com> - 2.1.2-1
- Update to latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Sep 17 2017 Mat Booth <mat.booth@redhat.com> - 2.0.2-2
- Drop unneeded dep on guava-testlib

* Mon Aug 14 2017 Tomas Repik <trepik@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 gil cattaneo <puntogil@libero.it> 1.2.1-1
- update to 1.2.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 gil cattaneo <puntogil@libero.it> 1.1-0.1.alpha
- initial rpm
