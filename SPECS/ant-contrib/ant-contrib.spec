Summary:        Collection of tasks for Ant
Name:           ant-contrib
Version:        1.0b3
Release:        19
License:        ASL 2.0 and ASL 1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://ant-contrib.sourceforge.net/
Source0:        https://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}-src.tar.bz2
# Upstream POM file
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/1.0b3/%{name}-1.0b3.pom
# ASL 2.0 Licence text
# Upstream bug at https://sourceforge.net/tracker/?func=detail&aid=3590371&group_id=36177&atid=416920
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt
Patch0:         ant-contrib-pom.patch
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  java-devel
BuildRequires:  ant
Requires:       java-headless
Requires:       ant
BuildArch:      noarch

%description
The Ant-Contrib project is a collection of tasks
(and at one point maybe types and other tools)
for Apache Ant.

%package        javadoc
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description    javadoc
Api documentation for %{name}.

%prep
%setup -q  -n %{name}
cp %{SOURCE1} %{name}-1.0b3.pom
cp %{SOURCE2} LICENSE-2.0.txt

%patch0 -p1

find . -name '*.jar' -or -name '*.class' -exec rm -rf {} +

# sed -i "s|xercesImpl|xerces-j2|g" ivy.xml ||:
# needs porting to latest ivy
rm -fr src/java/net/sf/antcontrib/net/URLImportTask.java

%build
ant -Ddist.dir="." -Dproject.version=%{version} dist

%install
# jars
install -Dpm 644 target/%{name}.jar %{buildroot}%{_javadir}/ant/%{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/docs/api/* %{buildroot}%{_javadocdir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant/ant-contrib" > %{buildroot}%{_sysconfdir}/ant.d/ant-contrib

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{name}-1.0b3.pom %{buildroot}/%{_mavenpomdir}/JPP.ant-%{name}.pom

echo "call add_maven_depmap JPP.ant-%{name}.pom ant/%{name}.jar"
%add_maven_depmap JPP.ant-%{name}.pom ant/%{name}.jar

%files -f .mfiles
%license LICENSE-2.0.txt target/docs/LICENSE.txt
%{_sysconfdir}/ant.d/ant-contrib
%doc target/docs/manual/tasks/*

%files javadoc
%license LICENSE-2.0.txt target/docs/LICENSE.txt
%doc %{_javadocdir}/%{name}

%changelog
* Fri Nov 20 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0b3-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT) and OpenSuSE Tumbleweed (license: MIT).
- Simplify buildrequires and runtime requires.
- Remove junit integration.
- Remove fdupes dependency.
- Set %%license.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.36.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.35.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.34.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.33.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.32.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.31.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.30.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.29.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.28.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 09 2014 Clément David <c.david86@gmail.com> - 1.0-0.27.b3
- Fix incorrect ant.d path.

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.26.b3
- Build using XMvn Ivy resolver

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.25.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.24.b3
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-0.23.b3
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.22.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.21.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 1.0-0.20.b3
- Added ASL 1.1 licence to the licence field

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 1.0-0.19.b3
- Added LICENSE to javadoc (#879349)
- Added ASL 2.0 licence text (#879354)
- Added requires on jpackage-utils in javadoc (#879356)

* Tue Nov 13 2012 Tomas Radej <tradej@redhat.com> - 1.0-0.18.b3
- Used correct upstream pom + patched it

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.17.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.16.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.15.b3
- Update to beta 3.

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.14.b2
- Fix pom installed name.

* Fri Nov 25 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.13.b2
- Adapt to current guidelines.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.12.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.11.b2
- Add maven pom and depmap.

* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.10.b2
- Install ant contrib in ant.d.

* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.9.b2
- Drop gcj_support.
- Install as proper ant plugin.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-0.6.b2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-0.5.b2
- Autorebuild for GCC 4.3

* Sun Aug 03 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.4.b2
- Added dist tag to release.

* Sat Aug 02 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.3.b2
- Removed unneccessary 0 epoch from required packages.
- Fixed dependance on specifically version 3.8.1 of junit.

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.2.b2
- Removed Class-Path from ant-contrib.jar file.
- Renamed patches.

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.1.b2
- Fixed release number to reflect beta status
- Removed Distribution and Vendor tags
- Fixed duplication in postun section
- Removed patch3, and used sed to fix line-endings instead

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-1.b2
- Changed release-version to comply with FE standards
- Consolidated into -manual into main package
- Removed ghosting of the manual symlink
- Removed Epoch
- Run dos2unix over some manual files that have windows line endings
- Changed group for docs to Documentation
- Remove unused Source1
- Set Source0 to valid URL instead of just a file name
- Fix indentation
- Remove {push,pop}d and -c from %%setup
- Changed %%defattr in the %%files section to standard (-,root,root,-)

* Thu Jun 1 2006 Igor Foox <ifoox@redhat.com> - 0:1.0b2-1jpp_1fc
- Update to version 1.0b2
- Added native compilation
- Changed BuildRoot to what Extras expects

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.6-4jpp
- Upgrade to ant-1.6.2
- BuildReq/Req ant = 0:1.6.2
- Relax some other requirements

* Thu Jun 03 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.6-3jpp
- Fix missing buildrequires

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:0.6-2jpp
- Upgrade to Ant 1.6.X

* Wed Mar 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.6-1jpp
- First JPackage release
