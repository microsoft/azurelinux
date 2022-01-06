Vendor:         Microsoft Corporation
Distribution:   Mariner
%global short_name httpclient

Name:           jakarta-commons-httpclient
Version:        3.1
Release:        36%{?dist}
Summary: Jakarta Commons HTTPClient implements the client side of HTTP standards
License:        ASL 2.0 and (ASL 2.0 or LGPLv2+)
URL:            http://jakarta.apache.org/commons/httpclient/
Source0:        http://archive.apache.org/dist/httpcomponents/commons-httpclient/source/commons-httpclient-3.1-src.tar.gz
Source1:        http://repo.maven.apache.org/maven2/commons-httpclient/commons-httpclient/%{version}/commons-httpclient-%{version}.pom
Patch0:         %{name}-disablecryptotests.patch
# Add OSGi MANIFEST.MF bits
Patch1:         %{name}-addosgimanifest.patch
Patch2:         %{name}-encoding.patch
# CVE-2012-5783: missing connection hostname check against X.509 certificate name
# https://fisheye6.atlassian.com/changelog/httpcomponents?cs=1422573
Patch3:         %{name}-CVE-2012-5783.patch
Patch4:         %{name}-CVE-2014-3577.patch
Patch5:         %{name}-CVE-2015-5262.patch

BuildArch:      noarch

# FIXME: we need BR maven-local, because we're using macros like mvn_install
# this should be changed to "javapackages-local" when javapackages-tools 4.0.0 is out
BuildRequires:  maven-local
BuildRequires:  ant
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-logging >= 1.0.3
BuildRequires:  junit

Requires:       java
Requires:       apache-commons-logging >= 1.0.3
Requires:       apache-commons-codec
Provides:       deprecated()

%description
The Hyper-Text Transfer Protocol (HTTP) is perhaps the most significant
protocol used on the Internet today. Web services, network-enabled
appliances and the growth of network computing continue to expand the
role of the HTTP protocol beyond user-driven web browsers, and increase
the number of applications that may require HTTP support.
Although the java.net package provides basic support for accessing
resources via HTTP, it doesn't provide the full flexibility or
functionality needed by many applications. The Jakarta Commons HTTP
Client component seeks to fill this void by providing an efficient,
up-to-date, and feature-rich package implementing the client side of the
most recent HTTP standards and recommendations.
Designed for extension while providing robust support for the base HTTP
protocol, the HTTP Client component may be of interest to anyone
building HTTP-aware client applications such as web browsers, web
service clients, or systems that leverage or extend the HTTP protocol
for distributed communication.

%package        javadoc
Summary:        Javadoc for %{name}
Provides:       deprecated()

%description    javadoc
%{summary}.

%package        demo
Summary:        Demos for %{name}
Requires:       %{name} = %{version}-%{release}
Provides:       deprecated()

%description    demo
%{summary}.

%package        manual
Summary:        Manual for %{name}
Requires:       %{name}-javadoc = %{version}-%{release}
Provides:       deprecated()

%description    manual
%{summary}.


%prep
%setup -q -n commons-httpclient-%{version}
mkdir lib # duh
build-jar-repository -p lib commons-codec commons-logging junit
rm -rf docs/apidocs docs/*.patch docs/*.orig docs/*.rej

%patch0

pushd src/conf
%{__sed} -i 's/\r//' MANIFEST.MF
%patch1
popd

%patch2
%patch3 -p2
%patch4 -p1
%patch5 -p1

# Use javax classes, not com.sun ones
# assume no filename contains spaces
pushd src
    for j in $(find . -name "*.java" -exec grep -l 'com\.sun\.net\.ssl' {} \;); do
        sed -e 's|com\.sun\.net\.ssl|javax.net.ssl|' $j > tempf
        cp tempf $j
    done
    rm tempf
popd

%mvn_alias : apache:commons-httpclient
%mvn_file ":{*}" jakarta-@1 "@1" commons-%{short_name}3

%build
ant \
  -Dbuild.sysclasspath=first \
  -Djavadoc.j2sdk.link=%{_javadocdir}/java \
  -Djavadoc.logging.link=%{_javadocdir}/jakarta-commons-logging \
  -Dtest.failonerror=false \
  -Djavac.encoding=UTF-8 \
  dist test

%install
%mvn_artifact %{SOURCE1} dist/commons-httpclient.jar
%mvn_install -J dist/docs/api

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr src/examples src/contrib $RPM_BUILD_ROOT%{_datadir}/%{name}

# manual and docs
rm -Rf dist/docs/{api,BUILDING.txt,TESTING.txt}
ln -s %{_javadocdir}/%{name} dist/docs/apidocs


%files -f .mfiles
%license LICENSE NOTICE
%doc README RELEASE_NOTES

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%files demo
%{_datadir}/%{name}

%files manual
%doc dist/docs/*


%changelog
* Wed Jan 05 2022 Thomas Crain <thcrain@microsoft.com> - 3.1-36
- Rename java-headless dependency to java
- License verified

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 3.1-35
- Remove epoch

* Tue Aug 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:3.1-34
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removed BR on 'java-javadoc' and 'apache-commons-logging-javadoc',
  which are not present package in CBL-Mariner.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-30
- Mark package as deprecated

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-26
- Use build-jar-repository for locating dependencies

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-23
- Respect configured SO_TIMEOUT during SSL handshake
- Resolves: CVE-2015-5262

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-21
- Remove legacy Obsoletes/Provides

* Mon Aug 18 2014 Michal Srb <msrb@redhat.com> - 1:3.1-20
- Fix MITM security vulnerability
- Resolves: CVE-2014-3577

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-19
- Add alias for apache:commons-httpclient

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Michal Srb <msrb@redhat.com> - 1:3.1-17
- Adapt to current guidelines

* Wed May 21 2014 Michal Srb <msrb@redhat.com> - 1:3.1-16
- Migrate to mfiles

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.1-15
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-12
- Add missing connection hostname check against X.509 certificate name
- Resolves: CVE-2012-5783

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-11
- Add maven POM

* Thu Sep 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-10
- Fix license tag

* Thu Sep 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1-9
- Install LICENSE and NOTICE files
- Add missing R: java, jpackage-utils

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Andy Grimm <agrimm@gmail.com> - 1:3.1-7
- Fix character encoding

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.1-5
- Fix symlinks in javadir

* Tue Jun 28 2011 Alexander Kurtakov <akurtako@redhat.com> 1:3.1-4
- Fix FTBFS.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Alexander Kurtakov <akurtako@redhat.com> 1:3.1-2
- Add missing requires on commons-codec.

* Fri Jul 16 2010 Alexander Kurtakov <akurtako@redhat.com> 1:3.1-1
- Drop gcj_support.
- Fix FTBFS.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 24 2008 Andrew Overholt <overholt@redhat.com> 1:3.1-0.3
- Update OSGi MANIFEST.MF

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.1-0.2
- drop repotag
- fix license tag

* Fri Apr 04 2008 Deepak Bhole <dbhole@redhat.com> - 0:3.1-0jpp.1
- Update to 3.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.0.1-2jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 06 2007 Andrew Overholt <overholt@redhat.com> 1:3.0.1-1jpp.2
- Add OSGi MANIFEST.MF information.

* Fri Mar 16 2007 Permaine Cheung <pcheung@redhat.com> - 1:3.0.1-1jpp.1
- Merge with upstream and more rpmlint cleanup.

* Thu Feb 15 2007 Fernando Nasser <fnasser@redhat.com> - 1:3.0.1-1jpp
- Upgrade to 3.0.1

* Fri Jan 26 2007 Permaine Cheung <pcheung@redhat.com> - 1:3.0-8jpp
- Added versions for provides and obsoletes and rpmlint cleanup.

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> - 1:3.0-7jpp.1
- Added missing requirements.
- Added missing postun section for javadoc.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 1:3.0-6jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Deepak Bhole <dbhole@redhat.com> - 1:3.0-6jpp_1fc
- Added conditional native compilation.
- Disable certain ssl related tests that are known to fail with libgcj.

* Thu Apr 06 2006 Fernando Nasser <fnasser@redhat.com> - 1:3.0-5jpp
- Improve backwards compatibility and force removal of older versioned
  packages

* Thu Apr 06 2006 Fernando Nasser <fnasser@redhat.com> - 1:3.0-4jpp
- Remove duplicate release definition
- Require simply a jaxp 1.3

* Thu Apr 06 2006 Fernando Nasser <fnasser@redhat.com> - 1:3.0-3jpp
- BR xml-commons-jaxp-1.3-apis

* Thu Apr 06 2006 Ralph Apel <r.apel@r-apel.de> - 1:3.0-2jpp
- Fix tarball typo
- assure javax classes are used instead of com.sun. ones

* Wed Apr 05 2006 Ralph Apel <r.apel@r-apel.de> - 1:3.0-1jpp
- 3.0 final, drop main version in name

* Thu Oct 20 2005 Jason Corley <jason.corley@gmail.com> - 1:3.0-0.rc4.1jpp
- 3.0rc4

* Thu May 05 2005 Fernando Nasser <fnasser@redhat.com> - 1:3.0-0.rc2.1jpp
- Update to 3.0 rc2.

* Thu Nov  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 1:2.0.2-1jpp
- Update to 2.0.2.
- Fix Group tag in -manual.

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:2.0-2jpp
- Rebuild with ant-1.6.2

* Mon Feb 16 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:2.0-1jpp
- 2.0 final

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:2.0-0.rc3.1jpp
- 2.0-rc3
- bump epoch

* Tue Oct 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-3.rc2.1jpp
- Update to 2.0rc2.
- Manual subpackage.
- Crosslink with local J2SE javadocs.
- Own unversioned javadoc dir symlink.

* Fri Aug 15 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-3.rc1.1jpp
- Update to 2.0rc1.
- Include "jakarta-"-less jar symlinks for consistency with other packages.
- Exclude example and contrib sources from main package, they're in -demo.

* Wed Jul  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-2.beta2.1jpp
- Update to 2.0 beta 2.
- Demo subpackage.
- Crosslink with local commons-logging javadocs.

* Wed Jun  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-2.beta1.1jpp
- Update to 2.0 beta 1.
- Non-versioned javadoc symlinking.

* Fri Apr  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-1.alpha3.2jpp
- Rebuild for JPackage 1.5.

* Wed Feb 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 2.0-1.alpha3.1jpp
- Update to 2.0 alpha 3.
- Fix Group tags.
- Run standalone unit tests during build.

* Thu Sep 12 2002 Ville Skyttä <ville.skytta at iki.fi> 2.0-0.cvs20020909.1jpp
- Tune the rpm release number tag so rpm2html doesn't barf on it.

* Mon Sep  9 2002 Ville Skyttä <ville.skytta at iki.fi> 2.0-0.20020909alpha1.1jpp
- 2.0alpha1 snapshot 20020909.
- Use sed instead of bash extensions when symlinking jars during build.
- Add distribution tag.
- Require commons-logging instead of log4j.

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-4jpp
- renamed to jakarta-commons-httpclient
- additional sources in individual archives
- versioned dir for javadoc
- no dependencies for javadoc package
- dropped j2ee package
- adapted to new jsse package
- section macro

* Fri Dec 7 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-3jpp
- javadoc into javadoc package

* Sat Nov 3 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-2jpp
- fixed jsse subpackage

* Fri Nov 2 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-1jpp
- first JPackage release
