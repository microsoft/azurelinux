Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           maven-dependency-plugin
Version:        3.1.1
Release:        6%{?dist}
Summary:        Plugin to manipulate, copy and unpack local and remote artifacts
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/%{name}
BuildArch:      noarch

Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

# port to maven-artifact-transfer 0.11.0
Patch0:         00-maven-artifact-transfer-0.11.0.patch

BuildRequires:  maven-local
BuildRequires:  mvn(classworlds:classworlds)
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-repository-metadata)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.apache.maven.shared:file-management)
BuildRequires:  mvn(org.apache.maven.shared:maven-artifact-transfer) >= 0.11.0
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-dependency-analyzer)
BuildRequires:  mvn(org.apache.maven.shared:maven-dependency-tree)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http-lightweight)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-io)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)


%description

The dependency plugin provides the capability to manipulate
artifacts. It can copy and/or unpack artifacts from local or remote
repositories to a specified location.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
%{summary}.


%prep
%setup -q
%patch0 -p1

%pom_remove_plugin :maven-enforcer-plugin

# We don't want to support legacy Maven versions (older than 3.1)
%pom_remove_dep org.sonatype.aether:

%build
# Tests require legacy Maven
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 03 2019 Fabio Valentini <decathorpe@gmail.com> - 3.1.1-4
- Include backported patch for maven-artifact-transfer 0.11.0 support.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov  5 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-1
- Add missing BR on maven-shared-utils

* Tue Oct 30 2018 Marian Koncek <mkoncek@redhat.com> - 3.1.1-1
- Update to upstream version 3.1.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 14 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.2-1
- Update to upstream version 3.0.2

* Mon Sep 11 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.1-1
- Update to upstream version 3.0.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-1
- Update to upstream version 3.0.0

* Mon Nov 07 2016 Michael Simacek <msimacek@redhat.com> - 3.0.0-0.5.20160823svn1756544
- Regenerate BuildRequires

* Tue Aug 23 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-0.4.20160823svn1756544
- Update to latest upstream snapshot

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.3.20160119svn1722372
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-0.2.20160119svn1722372
- Update to latest upstream snapshot (svn revision 1722372)

* Mon Oct 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-0.1.20151012svn1707940
- Update to upstream 3.0 snapshot (svn revision 1707940)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb  2 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10-1
- Update to upstream version 2.10

* Mon Sep 22 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-1
- Update to upstream version 2.9

* Wed Jun 11 2014 Alexander Kurtakov <akurtako@redhat.com> 2.8-4
- Fix building by dropping useless BRs.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.8-2
- Use Requires: java-headless rebuild (#1067528)

* Tue May 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-1
- Update to upstream version 2.8

* Fri Mar 15 2013 Michal Srb <msrb@redhat.com> - 2.7-1
- Update to upstream version 2.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-1
- Update to upstream version 2.6
- Build with xmvn
- Install license files

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.1-2
- Remove unneeded BR: asm2

* Tue Aug 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.1-1
- Update to upstream version 2.5.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Tomas Radej <tradej@redhat.com> - 2.4-1
- Updated to the upstream version
- Partially removed a test because of a legacy class use
- Removed exception checking as it has already been done

* Fri Jan 13 2012 Alexander Kurtakov <akurtako@redhat.com> 2.3-3
- Add missing BR.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-1
- Update to latest upstream

* Tue Jun 28 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2-2
- BR/R maven-shared-file-management.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2-1
- Update to 2.2 final release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-0.4.svn949573
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-0.3.svn949573
- Fix test case to expect new classworlds

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-0.2.svn949573
- Add missing Requires.

* Thu Jun  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-0.1.svn949573
- Initial package
