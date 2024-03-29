Name:           jakarta-servlet
Version:        5.0.0
Release:        14%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        Server-side API for handling HTTP requests and responses
# most of the project is EPL-2.0 or GPLv2 w/exceptions,
# but some files still have Apache-2.0 license headers:
# https://github.com/eclipse-ee4j/servlet-api/issues/347
License:        (EPL-2.0 or GPLv2 with exceptions) and ASL 2.0
URL:            https://github.com/eclipse-ee4j/servlet-api
BuildArch:      noarch

Source0:        https://github.com/jakartaee/servlet/archive/refs/tags/%{version}-RELEASE.tar.gz#/%{name}-%{version}-RELEASE.tar.gz

BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap

Provides:       glassfish-servlet-api = %{version}-%{release}

%description
Jakarta Servlet defines a server-side API for handling HTTP requests
and responses.

%{?javadoc_package}

%prep
%setup -q -n servlet-%{version}-RELEASE

# remove unnecessary dependency on parent POM
%pom_remove_parent . api

# do not build specification documentation
%pom_disable_module spec

# Copy to old package name
# TODO: Remove when all dependencies are migrated from javax.servlet to jakarta.servlet
cp -pr api/src/main/java/jakarta api/src/main/java/javax
sed -i -e 's/jakarta\./javax./g' $(find api/src/main/java/javax -name *.java)
%pom_xpath_replace pom:instructions/pom:Export-Package \
  '<Export-Package>jakarta.servlet.*,javax.servlet.*;version="4.0.0"</Export-Package>' api

# do not install useless parent POM
%mvn_package jakarta.servlet:servlet-parent __noinstall

# remove unnecessary maven plugins
%pom_remove_plugin -r :formatter-maven-plugin
%pom_remove_plugin -r :impsort-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :maven-javadoc-plugin
%pom_remove_plugin -r :maven-source-plugin

# add maven artifact coordinate aliases for backwards compatibility
%mvn_alias jakarta.servlet:jakarta.servlet-api \
    javax.servlet:javax.servlet-api \
    javax.servlet:servlet-api

# add compat symlink for packages constructing the classpath manually
%mvn_file :{*} %{name}/@1 glassfish-servlet-api

%build
%mvn_build
%install
%mvn_install
%files -f .mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
* Thu Mar 28 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 5.0.0-14
- Initial Azure Linux import from Fedora 39 (license: MIT).
- License verified

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 5.0.0-10
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-7
- Re-add provides on glassfish-servlet-api

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-6
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 20 2020 Mat Booth <mat.booth@redhat.com> - 5.0.0-4
- Correct mvn_file macro invokation

* Wed Aug 19 2020 Fabio Valentini <decathorpe@gmail.com> - 5.0.0-3
- Add compat symlink for packages constructing the classpath manually.

* Wed Aug 19 2020 Mat Booth <mat.booth@redhat.com> - 5.0.0-2
- Also ship the API in the old javax namespace to aid transition

* Thu Aug 13 2020 Fabio Valentini <decathorpe@gmail.com> - 5.0.0-1
- Initial package renamed from glassfish-servlet-api.
