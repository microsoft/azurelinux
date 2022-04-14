Vendor:         Microsoft Corporation
Distribution:   Mariner
%global artifactId javax.servlet.jsp
%global jspspec 2.3

Name:       glassfish-jsp
Version:    2.3.4
Release:    4%{?dist}
Summary:    Glassfish J2EE JSP API implementation
# Classes in package "org.apache.jasper" are Apache licensed
License:    (CDDL-1.1 or GPLv2 with exceptions) and ASL 2.0
URL:        https://github.com/javaee/javaee-jsp-api

Source0:    https://github.com/javaee/javaee-jsp-api/archive/%{artifactId}-%{version}.tar.gz
Source1:    http://www.apache.org/licenses/LICENSE-2.0.txt

# JSP can do byte-code compilation at runtime, if we enable the Eclipse compiler support
Patch0:     %{name}-build-eclipse-compilers.patch
# Fix compilation errors due to unimplemented interfaces in newer servlet APIs
Patch1:     %{name}-port-to-servlet-3.1.patch

BuildArch:  noarch

BuildRequires:  maven-local
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(javax.servlet.jsp:javax.servlet.jsp-api)
BuildRequires:  mvn(net.java:jvnet-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.eclipse.jdt:core)
BuildRequires:  mvn(org.glassfish:javax.el)

Provides:   jsp = %{jspspec}
Provides:   jsp%{jspspec}
Provides:   javax.servlet.jsp

%description
This project provides a container independent implementation of JSP
specification %{jspspec}.

%package javadoc
Summary: API documentation for %{name}

%description javadoc
%{summary}.

%prep
%setup -q -n javaee-jsp-api-%{artifactId}-%{version}

cp -p %{SOURCE1} LICENSE-ASL-2.0.txt

pushd impl
%patch0 -p1
%patch1 -p1

%pom_add_dep org.eclipse.jdt:core::provided

%mvn_alias : "org.eclipse.jetty.orbit:org.apache.jasper.glassfish"

# compat symlink
%mvn_file : %{name}/javax.servlet.jsp %{name}

# Plugins not needed for RPM builds:
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-source-plugin
popd

%build
pushd impl
%mvn_build
popd

%install
pushd impl
%mvn_install
popd

# Install j2ee api symlinks
install -d -m 755 %{buildroot}%{_javadir}/javax.servlet.jsp/
pushd %{buildroot}%{_javadir}/javax.servlet.jsp/
for jar in ../%{name}/*jar; do
    ln -sf $jar .
done
# Copy jsp-api so that deps can be included as well
build-jar-repository -p . glassfish-jsp-api
xmvn-subst -R %{buildroot} -s .
popd

%files -f impl/.mfiles
%{_javadir}/javax.servlet.jsp
%license LICENSE-ASL-2.0.txt LICENSE

%files javadoc -f impl/.mfiles-javadoc
%license LICENSE-ASL-2.0.txt LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Mat Booth <mat.booth@redhat.com> - 2.3.4-2
- Add extra license and patch comments

* Tue Dec 17 2019 Mat Booth <mat.booth@redhat.com> - 2.3.4-1
- Update to version 2.3.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-0.15.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-0.14.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-0.13.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-0.12.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Michael Simacek <msimacek@redhat.com> - 2.3.3-0.11.b02
- Specify CDDL license version
- Include correct license file for CDDL

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-0.10.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.3-0.9.b02
- Drop javax.servlet:jsp-api alias (it's for API, not impl)

* Fri Feb 24 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.3-0.8.b02
- Fix xmvn-subst invocation

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.3-0.7.b02
- Simplify J2EE symlink installation

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-0.6.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.3-0.5.b02
- Add missing build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-0.4.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-0.3.b02
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.3-0.2.b02
- Remove maven-javadoc-plugin execution

* Mon Jan 19 2015 Michael Simacek <msimacek@redhat.com> - 2.3.3-0.1.b02
- Update to upstream version 2.3.3-b02

* Mon Jun 9 2014 Alexander Kurtakov <akurtako@redhat.com> 2.3.2-5
- Rebuild to regen osgi metadata.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.2-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.2-2
- Regenerate BR

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.2-1
- Update to upstream version 2.3.2
- Port to servlet 3.1
- Drop group tag

* Mon Aug 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.6-11
- Add javax.servlet.jsp directory and provides

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Michal Srb <msrb@redhat.com> - 2.2.6-9
- Add compat symlink

* Fri Jun 07 2013 Michal Srb <msrb@redhat.com> - 2.2.6-8
- Build with XMvn
- Fix URL for CDDL license

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.6-7
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#917623

* Tue Feb 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.6-6
- Change scope of Eclipse JDT dependency from compile to provided
- Fix eclipse patch

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.6-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Sep  4 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.6-3
- Fix license tag
- Install license files

* Thu Aug 30 2012 Krzysztof Daniel <kdaniel@redhat.com> 2.2.6-2
- Build Eclipse compiler adapters.

* Wed Aug 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.6-1
- Update to upstream version 2.2.6

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-1
- Update to upstream version 2.2.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-2
- Add explicit BR/R on java and jpackage-utils
- Fix whitespace

* Wed Mar 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-1
- Initial version of the package
