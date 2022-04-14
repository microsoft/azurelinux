Vendor:         Microsoft Corporation
Distribution:   Mariner
%global tzversion tzdata2017b

Name:             joda-time
Version:          2.9.9
Release:          7%{?dist}
Summary:          Java date and time API

License:          ASL 2.0
URL:              http://www.joda.org/joda-time/
Source0:          https://github.com/JodaOrg/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:          ftp://ftp.iana.org/tz/releases/%{tzversion}.tar.gz
BuildArch:        noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.velocity:velocity)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires:  mvn(org.joda:joda-convert)


%description
Joda-Time provides a quality replacement for the Java date and time classes. The
design allows for multiple calendar systems, while still providing a simple API.
The 'default' calendar is the ISO8601 standard which is used by XML. The
Gregorian, Julian, Buddhist, Coptic, Ethiopic and Islamic systems are also
included, and we welcome further additions. Supporting classes include time
zone, duration, format and parsing.


%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q

sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt
sed -i 's/\r//' RELEASE-NOTES.txt

# all java binaries must be removed from the sources
find . -name '*.jar' -exec rm -f '{}' \;

# replace internal tzdata
rm -f src/main/java/org/joda/time/tz/src/*
tar -xzf %{SOURCE1} -C src/main/java/org/joda/time/tz/src/

# compat filename
%mvn_file : %{name}

# javadoc generation fails due to strict doclint in JDK 8
%pom_remove_plugin :maven-javadoc-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt RELEASE-NOTES.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.9-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-6.tzdata2017b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-5.tzdata2017b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-4.tzdata2017b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-3.tzdata2017b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-2.tzdata2017b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.9-1.tzdata2017b
- Update to upstream version 2.9.9
- Update to tzdata2017b

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-4.tzdata2016c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-3.tzdata2016c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.3-2.tzdata2016c
- Regenerate build-requires

* Wed Mar 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.3-1.tzdata2016c
- Update to upstream version 2.9.3
- Update to tzdata2016c

* Wed Mar 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.2-2.tzdata2016a
- Reintroduce accidentally removed tzdata version to release tag

* Tue Feb 16 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.2-1
- Update to upstream version 2.9.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2.tzdata2015e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov  2 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-1.tzdata2015e
- Update to upstream version 2.9

* Tue Jul 14 2015 Michael Simacek <msimacek@redhat.com> - 2.8.1-1.tzdata2015e
- Update to upstream version 2.8.1
- Update upstream URL
- Update to tzdata2015e

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4.tzdata2013g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3-3.tzdata2013g
- Remove maven-javadoc-plugin execution

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2.tzdata2013g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 16 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-1.tzdata2013g
- Update to latest upstream and tzdata2013g

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2.tzdata2013c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun  5 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-1.tzdata2013c
- Update to latest upstream and tzdata
- Install NOTICE.txt

* Tue Jun  4 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-5.tzdata2012h
- Enable testsuite
- Update to lates packaging guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4.tzdata2012h
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1-3.tzdata2012h
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 1 2012 Chris Spike <spike@fedoraproject.org> 2.1-2.tzdata2012h
- New tzdata (2012h)

* Sat Oct 20 2012 Chris Spike <spike@fedoraproject.org> 2.1-1.tzdata2012g
- Updated to 2.1
- New tzdata (2012g)
- Updated spec file according to latest java packaging guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-8.tzdata2011f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-7.tzdata2011f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 1.6.2-6.tzdata2011f
- Adapt to current guidelines.

* Fri Apr 15 2011 Chris Spike <spike@fedoraproject.org> 1.6.2-5.tzdata2011f
- New tzdata (2011f)
- Fixed build for maven 3
- Cleaned up BRs

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4.tzdata2010n
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Chris Spike <spike@fedoraproject.org> 1.6.2-3.tzdata2010n
- New tzdata (2010n)

* Thu Sep 23 2010 Chris Spike <spike@fedoraproject.org> 1.6.2-2.tzdata2010l
- Ignore test failures (tests fail in koji)

* Thu Sep 23 2010 Chris Spike <spike@fedoraproject.org> 1.6.2-1.tzdata2010l
- New upstream version (1.6.2)
- Removed dependency on main package for -javadoc subpackage
- Replaced summary with latest version
- Switched from ant to maven (no build.xml any more)
- Added patch to remove maven toolchain from pom.xml

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3.tzdata2008i
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2.tzdata2008i
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Conrad Meyer <konrad@tylerc.org> - 1.6-1.tzdata2008i
- New upstream version (1.6).

* Fri Oct 31 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-10.tzdata2008i
- New tzdata.

* Mon Oct 13 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-7.tzdata2008g
- New tzdata (2008g).

* Sat Aug 23 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-7.tzdata2008e
- New version with new tzdata (2008e).

* Sat Jul 19 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-7.tzdata2008d
- New version with new tzdata (2008d).

* Mon Jun 9 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-6.tzdata2008c
- New version with new tzdata (2008c).

* Sun Apr 6 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-5.tzdata2008b
- Don't compile GCJ bits yet as we hit some GCJ bug.

* Sat Apr 5 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-4.tzdata2008b
- Update to tzdata2008b.
- Use unversioned jar.
- Some small things to comply with Java Packaging Guidelines.
- GCJ support.

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-3.tzdata2008a
- Many small changes from bz# 436239 comment 6.
- Change -javadocs to -javadoc in accordance with java packaging
  guidelines draft.

* Sun Mar 16 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-2
- Use system junit via Mamoru Tasaka's patch.

* Mon Mar 3 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-1
- Initial package.
