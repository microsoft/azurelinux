Vendor:         Microsoft Corporation
Distribution:   Mariner
%global base_name exec
%global short_name commons-%{base_name}

Name:           apache-commons-exec
Version:        1.3
Release:        14%{?dist}
Summary:        Java library to reliably execute external processes from within the JVM
License:        ASL 2.0
URL:            http://commons.apache.org/exec/
BuildArch:      noarch

Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)

# Tests execute /usr/bin/ping
BuildRequires:  iputils

%description
Commons Exec is a library for dealing with external process execution and
environment management in Java.


%package javadoc
Summary:        Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{short_name}-%{version}-src

# Fix wrong end-of-line encoding
for file in LICENSE.txt NOTICE.txt RELEASE-NOTES.txt STATUS; do
  sed -i.orig "s/\r//" $file && \
  touch -r $file.orig $file && \
  rm $file.orig
done

# Shell scripts used for unit tests must be executable (see
# http://commons.apache.org/exec/faq.html#environment-testing)
chmod a+x src/test/scripts/*.sh

# Skip Exec57Test (it is unstable), see rhbz#1202260
find -name Exec57Test.java -delete

%mvn_file :%{short_name} %{short_name} %{name}


%build
%mvn_build -- -Dcommons.osgi.symbolicName=org.apache.commons.exec

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc STATUS RELEASE-NOTES.txt


%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 08 2019 Mat Booth <mat.booth@redhat.com> - 1.3-11
- Rebuild to regenerate OSGi metadata

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-5
- Regenerate build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-2
- Skip running unstable Exec57Test
- Resolves: rhbz#1202260

* Tue Dec 02 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3-1
- Update to 1.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Feb 03 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2-1
- Update to 1.2
- Adapt to current guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Mat Booth <fedora@matbooth.co.uk> - 1.1-10
- Add missing BRs

* Mon Jul 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-9
- Install NOTICE file with javadoc package
- Resolves: rhbz#984417

* Mon Feb 18 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.1-4
- Build with maven 3.
- Adapt to current guidelines.

* Mon Mar 07 2011 Tom Callaway <spot@fedoraproject.org> - 1.1-3
- fix maven fragment

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Mohamed El Morabity <melmorabity@fedorapeople.org> - 1.1-1
- Update to 1.1

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-4
- BR iputils. Needed by tests.

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-3
- Change maven plugin names to the new ones.

* Wed Feb  3 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 1.0.1-2
- Add missing %%post/%%postun Requires
- Use macro %%{_mavendepmapfragdir} instead of %%{_datadir}/maven2/pom
- Unown directories %%{_mavenpomdir} and %%{_mavendepmapfragdir}

* Mon Jan 18 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 1.0.1-1
- Initial RPM release
