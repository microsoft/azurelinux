# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

################################################################################
Name:           jss
################################################################################

%global         vendor_id dogtag
%global         product_id %{vendor_id}-jss

# Upstream version number:
%global         major_version 5
%global         minor_version 8
%global         update_version 0

# Downstream release number:
# - development/stabilization (unsupported): 0.<n> where n >= 1
# - GA/update (supported): <n> where n >= 1
%global         release_number 1

# Development phase:
# - development (unsupported): alpha<n> where n >= 1
# - stabilization (unsupported): beta<n> where n >= 1
# - GA/update (supported): <none>
#global         phase

%if 0%{?rhel} && 0%{?rhel} >= 10
%global enable_nss_version_pqc_def_flag -DENABLE_NSS_VERSION_PQC_DEF=ON
%endif

%undefine       timestamp
%undefine       commit_id

Summary:        Java Security Services (JSS)
URL:            https://github.com/dogtagpki/jss
License:        (MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later) AND Apache-2.0
Version:        %{major_version}.%{minor_version}.%{update_version}
Release:        %{release_number}%{?phase:.}%{?phase}%{?timestamp:.}%{?timestamp}%{?commit_id:.}%{?commit_id}%{?dist}

# To generate the source tarball:
# $ git clone https://github.com/dogtagpki/jss.git
# $ cd jss
# $ git tag v4.5.<z>
# $ git push origin v4.5.<z>
# Then go to https://github.com/dogtagpki/jss/releases and download the source
# tarball.
Source:         https://github.com/dogtagpki/jss/archive/v%{version}%{?phase:-}%{?phase}/jss-%{version}%{?phase:-}%{?phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > jss-VERSION-RELEASE.patch
# Patch: jss-VERSION-RELEASE.patch

%if 0%{?java_arches:1}
ExclusiveArch: %{java_arches}
%else
ExcludeArch: i686
%endif

################################################################################
# Java
################################################################################

# use Java 17 on Fedora 39 or older and RHEL 9 or older
# otherwise, use Java 21

# maven-local is a subpackage of javapackages-tools

%if 0%{?fedora} && 0%{?fedora} >= 43

%define java_devel java-25-openjdk-devel
%define java_headless java-25-openjdk-headless
%define java_home %{_jvmdir}/jre-25-openjdk
%define maven_local maven-local-openjdk25

%else

%define java_devel java-21-openjdk-devel
%define java_headless java-21-openjdk-headless
%define java_home %{_jvmdir}/jre-21-openjdk
%define maven_local maven-local

%endif

################################################################################
# Build Options
################################################################################

# By default the javadoc package will be built unless --without javadoc
# option is specified.

%bcond_without javadoc

# By default the tests package will be built and the tests will executed
# unless --without tests option is specified.

%bcond_without tests

################################################################################
# Build Dependencies
################################################################################

BuildRequires:  make
BuildRequires:  cmake >= 3.14
BuildRequires:  zip
BuildRequires:  unzip

BuildRequires:  gcc-c++
BuildRequires:  nss-devel >= 3.101
BuildRequires:  nss-tools >= 3.101

BuildRequires:  %{java_devel}
BuildRequires:  %{maven_local}
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-jdk14)

%description
Java Security Services (JSS) is a java native interface which provides a bridge
for java-based applications to use native Network Security Services (NSS).
This only works with gcj. Other JREs require that JCE providers be signed.

################################################################################
%package -n %{product_id}
################################################################################

Summary:        Java Security Services (JSS)

Requires:       nss >= 3.101

Requires:       %{java_headless}
Requires:       mvn(org.apache.commons:commons-lang3)
Requires:       mvn(org.slf4j:slf4j-api)
Requires:       mvn(org.slf4j:slf4j-jdk14)

Obsoletes:      jss < %{version}-%{release}
Provides:       jss = %{version}-%{release}
Provides:       jss = %{major_version}.%{minor_version}
Provides:       %{product_id} = %{major_version}.%{minor_version}

Conflicts:      ldapjdk < 4.20
Conflicts:      idm-console-framework < 1.2
Conflicts:      pki-base < 10.10.0

%description -n %{product_id}
Java Security Services (JSS) is a java native interface which provides a bridge
for java-based applications to use native Network Security Services (NSS).
This only works with gcj. Other JREs require that JCE providers be signed.

################################################################################
%package -n %{product_id}-tomcat
################################################################################

Summary:        Java Security Services (JSS) Connector for Tomcat

# Tomcat
BuildRequires:  mvn(org.apache.tomcat:tomcat-catalina) >= 10.1.36
BuildRequires:  mvn(org.apache.tomcat:tomcat-coyote) >= 10.1.36
BuildRequires:  mvn(org.apache.tomcat:tomcat-juli) >= 10.1.36

Requires:       %{product_id} = %{version}-%{release}
Requires:       mvn(org.apache.tomcat:tomcat-catalina) >= 10.1.36
Requires:       mvn(org.apache.tomcat:tomcat-coyote) >= 10.1.36 
Requires:       mvn(org.apache.tomcat:tomcat-juli) >= 10.1.36

# Tomcat JSS has been replaced with JSS Connector for Tomcat.
# This will remove installed Tomcat JSS packages.
Obsoletes:      tomcatjss <= 8.5
Conflicts:      tomcatjss <= 8.5
Obsoletes:      %{vendor_id}-tomcatjss <= 8.5
Conflicts:      %{vendor_id}-tomcatjss <= 8.5

%if 0%{?rhel} <= 8
# PKI Servlet Engine has been replaced with Tomcat.
# This will remove installed PKI Servlet Engine packages.
Obsoletes:      pki-servlet-engine <= 9.0
Conflicts:      pki-servlet-engine <= 9.0
%endif

%description -n %{product_id}-tomcat
JSS Connector for Tomcat is a Java Secure Socket Extension (JSSE)
module for Apache Tomcat that uses Java Security Services (JSS),
a Java interface to Network Security Services (NSS).

################################################################################
%package -n %{product_id}-tools
################################################################################

Summary:        Java Security Services (JSS) Tools

Provides:       jss-tools = %{version}-%{release}
Provides:       jss-tools = %{major_version}.%{minor_version}
Provides:       %{product_id}-tools = %{major_version}.%{minor_version}

# Some PKI tools have been moved into jss-tools.
Conflicts:      pki-tools < 11.6
Conflicts:      %{vendor_id}-pki-tools < 11.6

%description -n %{product_id}-tools
This package contains JSS tools.

%if %{with javadoc}
################################################################################
%package -n %{product_id}-javadoc
################################################################################

Summary:        Java Security Services (JSS) Javadocs

Obsoletes:      jss-javadoc < %{version}-%{release}
Provides:       jss-javadoc = %{version}-%{release}
Provides:       jss-javadoc = %{major_version}.%{minor_version}
Provides:       %{product_id}-javadoc = %{major_version}.%{minor_version}

%description -n %{product_id}-javadoc
This package contains the API documentation for JSS.
%endif

%if %{with tests}
################################################################################
%package -n %{product_id}-tests
################################################################################

Summary:        Java Security Services (JSS) Tests

BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.opentest4j:opentest4j)

%description -n %{product_id}-tests
This package provides test suite for JSS.

# with tests
%endif

################################################################################
%prep
################################################################################

%autosetup -n jss-%{version}%{?phase:-}%{?phase} -p 1

# disable native modules since they will be built by CMake
%pom_disable_module native
%pom_disable_module symkey

# do not ship examples
%pom_disable_module examples

# flatten-maven-plugin is not available in RPM
%pom_remove_plugin org.codehaus.mojo:flatten-maven-plugin

# specify Maven artifact locations
%mvn_file org.dogtagpki.jss:jss-tomcat         jss/jss-tomcat
%mvn_file org.dogtagpki.jss:jss-tomcat-10.1     jss/jss-tomcat-10.1

# specify Maven artifact packages
%mvn_package org.dogtagpki.jss:jss-tomcat      jss-tomcat
%mvn_package org.dogtagpki.jss:jss-tomcat-10.1  jss-tomcat

################################################################################
%build
################################################################################

# Set build flags for CMake
# (see /usr/lib/rpm/macros.d/macros.cmake)
%set_build_flags

export JAVA_HOME=%{java_home}

# Enable compiler optimizations
export BUILD_OPT=1

# Generate symbolic info for debuggers
CFLAGS="-g $RPM_OPT_FLAGS"
export CFLAGS

# Check if we're in FIPS mode
modutil -dbdir /etc/pki/nssdb -chkfips true | grep -q enabled && export FIPS_ENABLED=1

# build Java code, run Java tests, and build Javadoc with Maven
%mvn_build %{!?with_tests:-f} %{!?with_javadoc:-j}

# create links to Maven-built classes for CMake
mkdir -p %{_vpath_builddir}/classes/jss
ln -sf ../../../base/target/classes/org %{_vpath_builddir}/classes/jss
%if %{with tests}
mkdir -p %{_vpath_builddir}/classes/tests
ln -sf ../../../base/target/test-classes/org %{_vpath_builddir}/classes/tests
%endif

# create links to Maven-built JAR files for CMake
ln -sf ../base/target/jss.jar %{_vpath_builddir}
%if %{with tests}
ln -sf ../base/target/jss-tests.jar %{_vpath_builddir}
%endif

# create links to Maven-built headers for CMake
mkdir -p %{_vpath_builddir}/include/jss
ln -sf ../../../base/target/include/_jni %{_vpath_builddir}/include/jss/_jni

# mark Maven-built targets so that CMake will not rebuild them
mkdir -p %{_vpath_builddir}/.targets
touch %{_vpath_builddir}/.targets/finished_generate_java
%if %{with tests}
touch %{_vpath_builddir}/.targets/finished_tests_generate_java
%endif
%if %{with javadoc}
touch %{_vpath_builddir}/.targets/finished_generate_javadocs
%endif

# build native code and run native tests with CMake
./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --prefix-dir=%{_prefix} \
    --include-dir=%{_includedir} \
    --lib-dir=%{_libdir} \
    --sysconf-dir=%{_sysconfdir} \
    --share-dir=%{_datadir} \
    --cmake="%{__cmake} %{?enable_nss_version_pqc_def_flag}" \
    --java-home=%{java_home} \
    --jni-dir=%{_jnidir} \
    --version=%{version} \
    --without-java \
    --without-javadoc \
    %{!?with_tests:--without-tests} \
    dist

################################################################################
%install
################################################################################

# install Java binaries and Javadoc
%mvn_install

# install jss.jar
mkdir -p %{buildroot}%{_javadir}/jss
cp base/target/jss.jar %{buildroot}%{_javadir}/jss/jss.jar

# create links for backward compatibility
mkdir -p %{buildroot}%{_jnidir}
ln -sf ../../..%{_javadir}/jss/jss.jar %{buildroot}%{_jnidir}/jss.jar

mkdir -p %{buildroot}%{_libdir}/jss
ln -sf ../../..%{_javadir}/jss/jss.jar %{buildroot}%{_libdir}/jss/jss.jar

# install native binaries
./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --install-dir=%{buildroot} \
    --without-java \
    install

# install tests binaries
%if %{with tests}
mkdir -p %{buildroot}%{_datadir}/jss/tests/lib
cp base/target/jss-tests.jar %{buildroot}%{_datadir}/jss/tests/lib
%endif

################################################################################
%files -n %{product_id} -f .mfiles
################################################################################

%doc jss.html
%license MPL-1.1.txt gpl.txt lgpl.txt symkey/LICENSE
%{_javadir}/jss/jss.jar
%{_jnidir}/jss.jar
%{_libdir}/jss/jss.jar
%{_libdir}/jss/libjss.so
%{_libdir}/jss/libjss-symkey.so

################################################################################
%files -n %{product_id}-tomcat -f .mfiles-jss-tomcat
################################################################################

################################################################################
%files -n %{product_id}-tools
################################################################################

%{_bindir}/p12tool
%{_bindir}/p7tool
%{_bindir}/sslget

%if %{with javadoc}
################################################################################
%files -n %{product_id}-javadoc -f .mfiles-javadoc
################################################################################
%endif

%if %{with tests}
################################################################################
%files -n %{product_id}-tests
################################################################################

%{_datadir}/jss/tests/

# with tests
%endif

################################################################################
%changelog
* Tue Nov 04 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.8.0-1
- Rebase to JSS 5.8.0-1

* Mon Aug 11 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.8.0-0.5.beta4
- Rebuild for Fedora 43

* Mon Aug 11 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.8.0-0.4.beta4.1
- Rebase to JSS 5.8.0-beta4

* Mon Jul 28 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.8.0-0.3.beta3.1
- Rebase to JSS 5.8.0-beta3

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-0.1.beta1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.8.0.1
- Rebase to JSS 5.8.0-beta1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.1.alpha1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.6.0-1
- Rebase to JSS 5.6.0-alpha1

* Fri Oct 04 2024 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.5.1-1
- Rebase to JSS 5.5.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 29 2024 Adam Williamson <awilliam@redhat.com> - 5.5.0-2
- Really build against java-21

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 5.5.0-1.1
- Rebuilt for java-21-openjdk as system jdk

* Wed Feb 21 2024 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.5.0-1
- Rebase to JSS 5.5.0

* Thu Feb 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5.4.2-1.4
- Fix compatibility with NSS 3.97

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.2-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Packit <hello@packit.dev> - 5.4.2-1
- Updating version to v5.4.2 (Chris Kelley)
- Upstream spec file changes to reduce diffs (Chris Kelley)
- Introduce Packit configuration for jss (Chris Kelley)

* Tue Feb 07 2023 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.3.0-2
- Update version number in JSSConfig.cmake

* Tue Feb 07 2023 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.3.0-1
- Rebase to JSS 5.3.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 29 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.2.0-1
- Rebase to JSS 5.2.0

* Wed Apr 27 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.2.0-0.3.beta2
- Rebase to JSS 5.2.0-beta2
- Rename packages to dogtag-jss

* Mon Apr 11 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.2.0-0.2.beta1
- Rebase to JSS 5.2.0-beta1

* Mon Feb 14 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.1.0-1
- Rebase to JSS 5.1.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 5.1.0-0.3.alpha2
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-0.2.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 26 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.1.0-0.1.alpha2
- Rebase to JSS 5.1.0-alpha2

* Thu Sep 30 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-1
- Rebase to JSS 5.0.0

* Wed Sep 29 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.5.beta1
- Drop BuildRequires and Requires on glassfish-jaxb-api

* Fri Sep 03 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.4.beta1
- Rebase to JSS 5.0.0-beta1

* Thu Aug 12 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.3.alpha2
- Rebase to JSS 5.0.0-alpha2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-0.2.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.1.alpha1
- Rebase to JSS 5.0.0-alpha1
