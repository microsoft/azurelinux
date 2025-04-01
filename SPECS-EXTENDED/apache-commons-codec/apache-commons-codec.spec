%bcond_with bootstrap

Name:           apache-commons-codec
Version:        1.17.1
Release:        2%{?dist}
Summary:        Implementations of common encoders and decoders
License:        Apache-2.0
URL:            https://commons.apache.org/codec/
BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/commons/codec/source/commons-codec-%{version}-src.tar.gz
# Data in DoubleMetaphoneTest.java originally has an inadmissible license.
# The author gives MIT in e-mail communication.
Source1:        aspell-mail.txt

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.hamcrest:hamcrest)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-engine)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
%endif

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders. Examples include Base64, Hex,
Phonetic and URLs.

%{?javadoc_package}

%prep
%autosetup -n commons-codec-%{version}-src
cp %{SOURCE1} aspell-mail.txt
sed -i 's/\r//' RELEASE-NOTES*.txt LICENSE.txt NOTICE.txt

%mvn_file : commons-codec %{name}
%mvn_alias : commons-codec:commons-codec

%build
%mvn_build -- -Dcommons.osgi.symbolicName=org.apache.commons.codec

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt aspell-mail.txt
%doc RELEASE-NOTES*

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Marian Koncek <mkoncek@redhat.com> - 1.17.1-1
- Update to upstream version 1.17.1

* Tue Apr 02 2024 Marian Koncek <mkoncek@redhat.com> - 1.16.1-1
- Update to upstream version 1.16.1

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.16.0-7
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 1.16.0-6
- bump of release for for java-21-openjdk as system jdk

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.16.0-3
- Rebuild to regenerate auto-Requires on java

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.16.0-2
- Rebuild

* Thu Aug 17 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.16.0-1
- Update to upstream version 1.16.0

* Thu Aug 10 2023 Marian Koncek <mkoncek@redhat.com> - 1.15-10
- Use implicit maven toolchains

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.15-6
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.15-3
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Marian Koncek <mkoncek@redhat.com> - 1.15-1
- Update to upstream version 1.15

* Fri Sep 04 2020 Mat Booth <mat.booth@redhat.com> - 1.15-1
- Update to latest upstream release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.13-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14-2
- Build with OpenJDK 8

* Wed Jan 22 2020 Marian Koncek <mkoncek@redhat.com> - 1.14-1
- Update to upstream version 1.14

* Thu Dec 12 2019 Mat Booth <mat.booth@redhat.com> - 1.13-1
- Update to upstream version 1.13

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13-2
- Mass rebuild for javapackages-tools 201902

* Mon Jul 29 2019 Marian Koncek <mkoncek@redhat.com> - 1.13-1
- Update to upstream version 1.13

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.12-2
- Mass rebuild for javapackages-tools 201901

* Mon May 13 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.12-1
- Update to upstream version 1.12

* Thu Feb 07 2019 Mat Booth <mat.booth@redhat.com> - 1.11-6
- Rebuild to regenerate OSGi metadata

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-2
- Cleanup spec file

* Fri Nov 24 2017 Mat Booth <mat.booth@redhat.com> - 1.11-1
- Update to latest upstream version

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 17 2014 Mat Booth <mat.booth@redhat.com> - 1.10-1
- Update to upstream version 1.10

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-5
- Remove legacy Obsoletes/Provides for jakarta-commons

* Wed Jul 30 2014 Mat Booth <mat.booth@redhat.com> - 1.9-4
- Fix incorrect parent BR causing FTBFS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-1
- Update to upstream version 1.9
- Update to current packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 Tomas Radej <tradej@redhat.com> - 1.8-4
- Fixed license tag (MIT is only in test that doesn't make it into binary RPM)

* Tue Jun 25 2013 Tomas Radej <tradej@redhat.com> - 1.8-2
- Clarified licensing of DoubleMetaphoneTest.java

* Fri May 03 2013 Mat Booth <fedora@matbooth.co.uk> - 1.8-1
- Update to 1.8, rhbz #957598

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-5
- Remove unneeded BR: maven-idea-plugin

* Mon Feb 18 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.7-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-2
- Add Provides/Obsoletes for jakarta-commons-codec

* Thu Oct 25 2012 Mat Booth <fedora@matbooth.co.uk> - 1.7-1
- Update to 1.7.
- Can finally remove the provides/obsoletes on the old jakarta name.

* Mon Sep 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-5
- Restore apache-commons-codec.jar symlink, resolves #857947

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-4
- Enable tests
- Install NOTICE with javadoc package
- Fix file permissions
- Remove versioned symlinks

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 akurtakov <akurtakov@rh.akurtakov> 1.6-1
- Update to latest upstream (1.6).

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.4-13
- Build with maven 3.
- Adapt to current guidelines.

* Thu Feb 10 2011 mbooth <fedora@matbooth.co.uk> 1.4-12
- Drop versioned jars and javadocs.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May 21 2010 Mat Booth <fedora@matbooth.co.uk> 1.4-10
- Correct dep-map names #594717.

* Fri May 21 2010 Alexander Kurtakov <akurtako@redhat.com> 1.4-9
- Obsolete/Provide commons-codec.

* Fri May 14 2010 Mat Booth <fedora@matbooth.co.uk> - 1.4-8
- Obsolete jakarta javadoc package.
- Keep legacy depmap around.

* Thu May 13 2010 Mat Booth <fedora@matbooth.co.uk> - 1.4-7
- Use global instead of define.
- Drop really old obsoletes/provides on short_name.
- Fix requires.

* Tue May 11 2010 Mat Booth <fedora@matbooth.co.uk> - 1.4-6
- Rename package (jakarta-commons-codec->apache-commons-codec).

* Tue Dec 8 2009 Mat Booth <fedora@matbooth.co.uk> - 1.4-5
- Enable OSGi automatic depsolving (from Alphonse Van Assche).

* Sun Nov 8 2009 Mat Booth <fedora@matbooth.co.uk> - 1.4-4
- Fix javadoc package requires

* Sat Nov 7 2009 Mat Booth <fedora@matbooth.co.uk> - 1.4-3
- Correct Obsoletes/Provides according to naming guidelines

* Sat Nov 7 2009 Mat Booth <fedora@matbooth.co.uk> - 1.4-2
- Add all maven related build reqs
- Require Java 1.6 because tests fail on GCJ

* Sat Nov 7 2009 Mat Booth <fedora@matbooth.co.uk> - 1.4-1
- Update to 1.4
- Rewrite spec file to build using upstream-preferred maven instead of ant
- Drop patch to add OSGi manifest (done automatically in the maven build)
- Install pom and add to maven dep-map
- Re-enable all tests

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-11.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 24 2008 Andrew Overholt <overholt@redhat.com> 1.3-9.4
- Update OSGi manifest.

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3-9.3
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.3-9jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 06 2007 Andrew Overholt <overholt@redhat.com> 1.3-8jpp.2
- Add OSGi manifest.

* Wed Mar 21 2007 Matt Wringe <mwringe@redhat.com> 0:1.3-8jpp.1
- Update to latest jpp version
- Fix rpmlint issues

* Wed Mar 21 2007 Matt Wringe <mwringe@redhat.com> 0:1.3-8jpp
- Fix some rpmlint warnings
- Update copyright year

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> 0:1.3-7jpp.2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Matt Wringe <mwringe at redhat.com> 0:1.3-7jpp.1
- Merge with upstream version.

* Tue Sep 26 2006 Matt Wringe <mwringe at redhat.com> 0:1.3-7jpp
- Add missing java-javadoc requires and buildrequires.

* Mon Sep 25 2006 Matt Wringe <mwringe at redhat.com> 0:1.3-6jpp.1
- Merge with upstream version.

* Mon Sep 25 2006 Matt Wringe <mwringe at redhat.com> 0:1.3-6jpp
- Update jakarta-commons-codec-1.3-buildscript.patch to build
  offline.

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> 0:1.3-5jpp.1
- Merge with upstream version
 - Add missing javadoc requires

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.3-4jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> 0:1.3-4jpp_1fc
- Merged with upstream version
- Now is natively compiled

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> 0:1.3-4jpp
- Added conditional native compiling

* Tue Apr 04 2006 Ralph Apel <r.apel@r-apel.de> 0:1.3-3jpp
- First JPP-1.7 release

* Wed Sep 08 2004 Fernando Nasser <fnasser@redhat.com> 0:1.3-2jpp
- Do not stop on test failure

* Tue Sep 07 2004 Fernando Nasser <fnasser@redhat.com> 0:1.3-1jpp
- Upgrade to 1.3
- Rebuilt with Ant 1.6.2

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.2-1jpp
- 1.2
- use perl instead of patch

* Wed May 28 2003 Ville Skyttä <jpackage-discuss at zarb.org> - 0:1.1-1jpp
- First JPackage release.
