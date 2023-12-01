Vendor:         Microsoft Corporation
Distribution:   Mariner

%global project_folder %{name}-%{version}-src
%global archive_folder build

Name:           sblim-cim-client2
Version:        2.2.5
Release:        16%{?dist}
Summary:        Java CIM Client library

License:        EPL
URL:            http://sourceforge.net/projects/sblim/
Source0:        http://downloads.sourceforge.net/project/sblim/%{name}/%{version}/%{name}-%{version}-src.zip
Patch0:         sblim-cim-client2-2.2.5-fix-for-java-11-openjdk.patch

BuildArch:      noarch

BuildRequires:  java-devel >= 1.4
BuildRequires:  jpackage-utils >= 1.5.32
BuildRequires:  ant >= 1.6

Requires:       java >= 1.4
Requires:       jpackage-utils >= 1.5.32

%description
The purpose of this package is to provide a CIM Client Class Library for Java
applications. It complies to the DMTF standard CIM Operations over HTTP and
intends to be compatible with JCP JSR48 once it becomes available. To learn
more about DMTF visit http://www.dmtf.org.
More infos about the Java Community Process and JSR48 can be found at
http://www.jcp.org and http://www.jcp.org/en/jsr/detail?id=48.

%package javadoc
Summary:        Javadoc for %{name}
Requires:       sblim-cim-client2 = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%package manual
Summary:        Manual and sample code for %{name}
Requires:       sblim-cim-client2 = %{version}-%{release}

%description manual
Manual and sample code for %{name}.


%prep
%setup -q -n %{project_folder}
%patch0 -p1 -b .fix-for-java-11-openjdk

dos2unixConversion() {
        fileName=$1
        %{__sed} -i 's/\r//g' "$fileName"
}

dosFiles2unix() {
        fileList=$1
        for fileName in $fileList; do
                dos2unixConversion $fileName
        done
}

dosFiles2unix 'ChangeLog NEWS README COPYING sblim-cim-client2.properties sblim-slp-client2.properties'
dosFiles2unix 'smpl/org/sblim/slp/example/*'
dosFiles2unix 'smpl/org/sblim/cimclient/samples/*'

%build
export ANT_OPTS="-Xmx256m"
ant \
        -Dbuild.compiler=modern \
        -Dcompile.source=1.6 \
        -Dcompile.target=1.6 \
        -DManifest.version=%{version}\
        package java-doc


%install
# --- documentation ---
dstDocDir=$RPM_BUILD_ROOT%{_pkgdocdir}
install -d $dstDocDir
install --mode=644 ChangeLog COPYING README NEWS $dstDocDir
# --- samples (also into _docdir) ---
cp -pr  smpl/org $dstDocDir
# --- config files ---
confDir=$RPM_BUILD_ROOT%{_sysconfdir}/java
install -d $confDir
install --mode=664 sblim-cim-client2.properties sblim-slp-client2.properties $confDir
# --- jar ---
install -d $RPM_BUILD_ROOT%{_javadir}
install %{archive_folder}/lib/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
# --- javadoc ---
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr %{archive_folder}/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%files
%dir %{_pkgdocdir}
%config(noreplace) %{_sysconfdir}/java/sblim-cim-client2.properties
%config(noreplace) %{_sysconfdir}/java/sblim-slp-client2.properties
%license %{_pkgdocdir}/COPYING
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/ChangeLog
%doc %{_pkgdocdir}/NEWS
%{_javadir}/%{name}.jar

%files javadoc
%{_javadocdir}/%{name}

%files manual
%license %{_pkgdocdir}/COPYING
%doc %{_pkgdocdir}/org

%changelog
* Thu Feb 17 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.5-16
- Updating used version of Java.

* Wed Jan 05 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.2.5-15
- Rename java-headless dependency to java
- License verified

* Wed Nov 03 2021 Muhammad Falak <mwani@microsft.com> - 2.2.5-14
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.5-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.5-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Dec 16 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.5-1
- Update to sblim-cim-client2-2.2.5

* Thu Nov 07 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-2
- Remove versioned jars from %%{_javadir}
  Resolves: #1022162

* Mon Sep 16 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-1
- Update to sblim-cim-client2-2.2.4

* Wed Aug 07 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.3-3
- Fix for unversioned doc dir change
  Resolves: #994072

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.3-1
- Update to sblim-cim-client2-2.2.3

* Mon Mar 18 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.2-1
- Update to sblim-cim-client2-2.2.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.1-1
- Update to sblim-cim-client2-2.2.1

* Mon Sep 17 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.0-1
- Update to sblim-cim-client2-2.2.0

* Tue Sep 04 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.12-3
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.12-1
- Update to sblim-cim-client2-2.1.12

* Wed Jan 04 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.11-1
- Update to sblim-cim-client2-2.1.11

* Mon Sep 26 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.10-1
- Update to sblim-cim-client2-2.1.10

* Wed Aug 17 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.9-2
- Rebuild due to the trailing slash bug of rpm

* Wed Jul 20 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.9-1
- Update to sblim-cim-client2-2.1.9

* Wed May 25 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.8-1
- Update to sblim-cim-client2-2.1.8

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.7-1
- Update to sblim-cim-client2-2.1.7

* Wed Jun  2 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.3-1
- Update to sblim-cim-client2-2.1.3

* Tue Oct  6 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.9.2-1
- Initial support
