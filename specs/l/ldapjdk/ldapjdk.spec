# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

################################################################################
Name:             ldapjdk
################################################################################

%global           vendor_id dogtag
%global           product_id %{vendor_id}-ldapjdk

# Upstream version number:
%global           major_version 5
%global           minor_version 6
%global           update_version 0

# Downstream release number:
# - development/stabilization (unsupported): 0.<n> where n >= 1
# - GA/update (supported): <n> where n >= 1
%global           release_number 2

# Development phase:
# - development (unsupported): alpha<n> where n >= 1
# - stabilization (unsupported): beta<n> where n >= 1
# - GA/update (supported): <none>
#global           phase alpha1

%undefine         timestamp
%undefine         commit_id

Summary:          LDAP SDK
URL:              https://github.com/dogtagpki/ldap-sdk
License:          MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later
Version:          %{major_version}.%{minor_version}.%{update_version}
Release:          %{release_number}%{?phase:.}%{?phase}%{?timestamp:.}%{?timestamp}%{?commit_id:.}%{?commit_id}%{?dist}

# To create a tarball from a version tag:
# $ git archive \
#     --format=tar.gz \
#     --prefix ldap-sdk-<version>/ \
#     -o ldap-sdk-<version>.tar.gz \
#     <version tag>
Source: https://github.com/dogtagpki/ldap-sdk/archive/v%{version}%{?phase:-}%{?phase}/ldap-sdk-%{version}%{?phase:-}%{?phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > ldap-sdk-VERSION-RELEASE.patch
# Patch: ldap-sdk-VERSION-RELEASE.patch

BuildArch:        noarch
%if 0%{?java_arches:1}
ExclusiveArch:    %{java_arches} noarch
%endif

################################################################################
# Java
################################################################################

%define java_devel java-25-openjdk-devel
%define java_headless java-25-openjdk-headless
%define java_home %{_jvmdir}/jre-25-openjdk
%define maven_local maven-local-openjdk25

################################################################################
# Build Dependencies
################################################################################

BuildRequires:    ant-openjdk25 
BuildRequires:    %{java_devel}
BuildRequires:    %{maven_local}
BuildRequires:    mvn(org.slf4j:slf4j-api)
BuildRequires:    mvn(org.slf4j:slf4j-jdk14)
BuildRequires:    mvn(org.dogtagpki.jss:jss-base) >= 5.6.0

%description
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

################################################################################
%package -n %{product_id}
################################################################################

Summary:          LDAP SDK

Requires:         %{java_headless}
Requires:         mvn(org.slf4j:slf4j-api)
Requires:         mvn(org.slf4j:slf4j-jdk14)
Requires:         mvn(org.dogtagpki.jss:jss-base) >= 5.6.0

Obsoletes:        ldapjdk < %{version}-%{release}
Provides:         ldapjdk = %{version}-%{release}
Provides:         ldapjdk = %{major_version}.%{minor_version}
Provides:         %{product_id} = %{major_version}.%{minor_version}

%description -n %{product_id}
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

%license docs/ldapjdk/license.txt

################################################################################
%package -n %{product_id}-javadoc
################################################################################

Summary:          Javadoc for LDAP SDK

Obsoletes:        ldapjdk-javadoc < %{version}-%{release}
Provides:         ldapjdk-javadoc = %{version}-%{release}
Provides:         ldapjdk-javadoc = %{major_version}.%{minor_version}
Provides:         %{product_id}-javadoc = %{major_version}.%{minor_version}

%description -n %{product_id}-javadoc
Javadoc for LDAP SDK

################################################################################
%prep
################################################################################

%autosetup -n ldap-sdk-%{version}%{?phase:-}%{?phase} -p 1

# flatten-maven-plugin is not available in RPM
%pom_remove_plugin org.codehaus.mojo:flatten-maven-plugin

# specify Maven artifact locations
%mvn_file org.dogtagpki.ldap-sdk:ldapjdk     ldapjdk/ldapjdk    ldapjdk
%mvn_file org.dogtagpki.ldap-sdk:ldapbeans   ldapjdk/ldapbeans  ldapbeans
%mvn_file org.dogtagpki.ldap-sdk:ldapfilter  ldapjdk/ldapfilter ldapfilt
%mvn_file org.dogtagpki.ldap-sdk:ldapsp      ldapjdk/ldapsp     ldapsp
%mvn_file org.dogtagpki.ldap-sdk:ldaptools   ldapjdk/ldaptools  ldaptools

################################################################################
%build
################################################################################

export JAVA_HOME=%{java_home}

%mvn_build

################################################################################
%install
################################################################################

%mvn_install

ln -sf %{name}/ldapjdk.pom %{buildroot}%{_mavenpomdir}/JPP-ldapjdk.pom
ln -sf %{name}/ldapsp.pom %{buildroot}%{_mavenpomdir}/JPP-ldapsp.pom
ln -sf %{name}/ldapfilter.pom %{buildroot}%{_mavenpomdir}/JPP-ldapfilter.pom
ln -sf %{name}/ldapbeans.pom %{buildroot}%{_mavenpomdir}/JPP-ldapbeans.pom
ln -sf %{name}/ldaptools.pom %{buildroot}%{_mavenpomdir}/JPP-ldaptools.pom

################################################################################
%files -n %{product_id} -f .mfiles
################################################################################

%{_mavenpomdir}/JPP-ldapjdk.pom
%{_mavenpomdir}/JPP-ldapsp.pom
%{_mavenpomdir}/JPP-ldapfilter.pom
%{_mavenpomdir}/JPP-ldapbeans.pom
%{_mavenpomdir}/JPP-ldaptools.pom

################################################################################
%files -n %{product_id}-javadoc -f .mfiles-javadoc
################################################################################

################################################################################
%changelog
* Fri Nov 28 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 5.6.0-2
- Really rebuilt for java-25-openjdk as system jdk

* Tue Nov 04 2025  Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.6.0-2
- Rebase to LDAP SDK 5.6.0

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 5.6.0-0.1.alpha1.3
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.1.alpha1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.1.alpha1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.5.0-0.1
- Rebase to LDAP SDK 5.6.0-alpha1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 03 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5.5.0-2
- Really rebuilt for java-21-openjdk as system jdk

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 5.5.0-1.1
- Rebuilt for java-21-openjdk as system jdk

* Wed Feb 21 2024 Dogtag PKI Team <devel@lists.dogtagpki.org> 5.5.0-1
- Rebase to LDAP SDK 5.5.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Packit <hello@packit.dev> - 5.4.1-1
- Updating version to v5.4.1 (Chris Kelley)
- Upstream some spec file changes from Fedora to minimise diff (Chris Kelley)
- Introduce Packit configuration for ldapjdk (Chris Kelley)

* Tue Feb 07 2023 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.3.0-1
- Rebase to LDAP SDK 5.3.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 5.2.0-1.1
- Rebuilt for Drop i686 JDKs

* Thu Jun 30 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.2.0-1
- Rebase to LDAP SDK 5.2.0

* Fri Apr 29 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.2.0-0.3.beta2
- Rebase to LDAP SDK 5.2.0-beta2
- Rename packages to dogtag-ldapjdk

* Mon Apr 11 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.2.0-0.2.beta1
- Rebase to LDAP SDK 5.2.0-beta1

* Mon Feb 14 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.1.0-1
- Rebase to LDAP SDK 5.1.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 5.0.0-3
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 30 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-1
- Rebase to LDAP SDK 5.0.0

* Thu Aug 12 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.3.alpha2
- Rebase to LDAP SDK 5.0.0-alpha2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-0.2.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.1.alpha1
- Rebase to LDAP SDK 5.0.0-alpha1
