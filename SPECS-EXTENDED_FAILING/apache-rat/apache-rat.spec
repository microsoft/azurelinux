Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           apache-rat
Summary:        Apache Release Audit Tool (RAT)
Version:        0.13
Release:        3%{?dist}
License:        ASL 2.0

URL:            http://creadur.apache.org/rat/
Source0:        http://www.apache.org/dist/creadur/%{name}-%{version}/%{name}-%{version}-src.tar.bz2

Patch1:         0001-Port-to-current-doxia-sitetools.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-cli:commons-cli)
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-antunit)
BuildRequires:  mvn(org.apache.ant:ant-testutil)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-decoration-model)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven:maven-artifact:2.2.1)
BuildRequires:  mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  mvn(org.apache.maven:maven-model:2.2.1)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven:maven-settings:2.2.1)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.shared:maven-plugin-testing-harness)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.hamcrest:hamcrest-library)
BuildRequires:  mvn(org.mockito:mockito-all)
BuildRequires:  mvn(org.mockito:mockito-core)

%description
Release Audit Tool (RAT) is a tool to improve accuracy and efficiency when
checking releases. It is heuristic in nature: making guesses about possible
problems. It will produce false positives and cannot find every possible
issue with a release. It's reports require interpretation.

RAT was developed in response to a need felt in the Apache Incubator to be
able to review releases for the most common faults less labor intensively.
It is therefore highly tuned to the Apache style of releases.

This package just contains meta-data, you will want either apache-rat-tasks,
or apache-rat-plugin.


%package        api
Summary:        API module for %{name}

%description    api
Shared beans and services.


%package        core
Summary:        Core functionality for %{name}

# explicit requires for javapackages-tools since apache-rat-script
# uses /usr/share/java-utils/java-functions
Requires:       javapackages-tools

%description    core
The core functionality of RAT, shared by the Ant tasks, and the Maven plugin.
It also includes a wrapper script "apache-rat" that should be the equivalent
to running upstream's "java -jar apache-rat.jar".


%package        plugin
Summary:        Maven plugin for %{name}

%description    plugin
Maven plugin for running RAT, the Release Audit Tool.


%package        tasks
Summary:        Ant tasks for %{name}

%description    tasks
Ant tasks for running RAT.


%package        javadoc
Summary:        Javadocs for %{name}

%description    javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q

%patch1 -p1

# apache-rat is a module bundling other RAT modules together and as
# such it is not needed.
%pom_disable_module apache-rat

# maven-antrun-plugin is used for running tests only and tests are
# skipped anyways.  See rhbz#988561
%pom_remove_plugin -r :maven-antrun-plugin

# don't run apache-rat's checks on apache-rat:
# these tests fail and would introduce a circular self-dependency
%pom_remove_plugin -r :apache-rat-plugin

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

# runs non-xmvn maven and downloads stuff
%pom_remove_plugin -r :maven-invoker-plugin

# wagon-ssh is not needed in Fedora.
%pom_xpath_remove pom:extensions

# incompatible with our plexus-container
rm apache-rat-plugin/src/test/java/org/apache/rat/mp/RatCheckMojoTest.java


%build
%mvn_build -s


%install
%mvn_install

# create wrapper script
%jpackage_script org.apache.rat.Report "" "" %{name}/%{name}-core:commons-cli:commons-io:commons-collections:commons-compress:commons-lang:junit apache-rat true

# install ant taksks
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "apache-rat/rat-core apache-rat/rat-tasks" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name}


%files -f .mfiles-%{name}-project
%doc LICENSE NOTICE

%files api -f .mfiles-%{name}-api
%doc README.txt RELEASE-NOTES.txt
%doc LICENSE NOTICE

%files core -f .mfiles-%{name}-core
%{_bindir}/%{name}

%files plugin -f .mfiles-%{name}-plugin

%files tasks -f .mfiles-%{name}-tasks
%{_sysconfdir}/ant.d/%{name}
%doc ant-task-examples.xml

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.13-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jul 29 2019 Fabio Valentini <decathorpe@gmail.com> - 0.13-1
- Update to version 0.13.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Severin Gehwolf <sgehwolf@redhat.com> - 0.12-7
- Add explicit requirement for javapackages-tools.
  See RHBZ#1600426.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12-2
- Port to current doxia sitetools

* Thu Jun 23 2016 Michael Simacek <msimacek@redhat.com> - 0.12-1
- Update to upstream version 0.12
- Enable tests

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11-1
- Update to upstream version 0.11

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-6
- Update to Maven Doxia 1.6

* Fri Jun 13 2014 Michal Srb <msrb@redhat.com> - 0.10-5
- Fix FTBFS (Resolves: #1105955)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-3
- Remove wagon-ssh extension from POM

* Thu Oct  3 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-2
- Add missing BR
- Update to current packaging guidelines

* Tue Sep 3 2013 Orion Poplawski <orion@cora.nwra.com> 0.10-1
- Update to 0.10

* Fri Aug 9 2013 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Update to 0.9

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-10
- Split up depmap fragments (bug 973242)

* Tue Feb 26 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-9
- Drop BR on maven-doxia and maven-doxia-sitetools (bug #915606)

* Tue Feb 12 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-8
- Add apache-rat wrapper script to apache-rat-core (bug #907782)
- Disable tests for now due to Fedora maven bug

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.8-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-6
- Run mvn-rpmbuild package instead of install

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-5
- Install NOTICE files
- Remove defattr

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-2
- Update to maven 3

* Tue Dec 6 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-1
- Update to 0.8 release
- Add BR maven-invoker-plugin

* Thu Apr 28 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-0.7.20100827
- Add needed requires to core

* Thu Mar 3 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-0.6.20100827
- Drop unneeded rm from %%install
- Don't ship BUILD.txt
- Cleanup Requires

* Mon Dec 27 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.5.20100827
- Drop maven settings patch
- Add svn revision to export command
- Set maven.test.failure.ignore=true instead of maven.test.skip
- Use %%{_mavenpomdir}

* Thu Dec 9 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.4.20100827
- Change BR to ant-antunit
- Drop versioned jar and javadoc
- Drop BuildRoot and %%clean

* Mon Nov 1 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.3.20100827
- Add /etc/ant.d/apache-rat

* Fri Oct 29 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.2.20100827
- First real working package

* Wed Aug 11 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.1
- Initial Fedora package

