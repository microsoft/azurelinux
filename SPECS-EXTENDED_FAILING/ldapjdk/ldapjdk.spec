Vendor:         Microsoft Corporation
Distribution:   Mariner
################################################################################
Name:             ldapjdk
################################################################################

Summary:          LDAP SDK
URL:              http://www.dogtagpki.org/
License:          MPLv1.1 or GPLv2+ or LGPLv2+

BuildArch:        noarch

Version:          4.22.0
Release:          4%{?dist}
# global           _phase -a1

%global spname		ldapsp
%global filtname	ldapfilt
%global beansname	ldapbeans

# To create a tarball from a version tag:
# $ git archive \
#     --format=tar.gz \
#     --prefix ldap-sdk-<version>/ \
#     -o ldap-sdk-<version>.tar.gz \
#     <version tag>
Source: https://github.com/dogtagpki/ldap-sdk/archive/v%{version}%{?_phase}/ldap-sdk-%{version}%{?_phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > ldap-sdk-VERSION-RELEASE.patch
# Patch: ldap-sdk-VERSION-RELEASE.patch

################################################################################
# Build Dependencies
################################################################################

# autosetup
BuildRequires:    git

BuildRequires:    ant
BuildRequires:    java-devel
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:	  jpackage-utils >= 1.5
%else
BuildRequires:    javapackages-local
%endif
BuildRequires:    slf4j
%if 0%{?rhel} && 0%{?rhel} <= 7
# no slf4j-jdk14
%else
BuildRequires:    slf4j-jdk14
%endif
BuildRequires:    jss >= 4.6.0

################################################################################
# Runtime Dependencies
################################################################################

Requires:         jpackage-utils >= 1.5
Requires:         slf4j
%if 0%{?rhel} && 0%{?rhel} <= 7
# no slf4j-jdk14
%else
Requires:         slf4j-jdk14
%endif
Requires:         jss >= 4.6.0


%description
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

%license docs/ldapjdk/license.txt

################################################################################
%package javadoc
################################################################################

Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}

################################################################################
%prep
################################################################################

%autosetup -n ldap-sdk-%{version}%{?_phase} -p 1 -S git

# Remove all bundled jars, we must build against build-system jars
rm -f ./java-sdk/ldapjdk/lib/{jss32_stub,jsse,jnet,jaas,jndi}.jar

################################################################################
%build
################################################################################

# Link to build-system BRs
pwd
%if 0%{?rhel} && 0%{?rhel} <= 7
( cd  java-sdk/ldapjdk/lib && build-jar-repository -s -p . jss4 jsse jaas jndi )
%else
( cd  java-sdk/ldapjdk/lib && build-jar-repository -s -p . jss4 )
ln -s /usr/lib/jvm-exports/java/{jsse,jaas,jndi}.jar java-sdk/ldapjdk/lib
%endif
cd java-sdk
if [ ! -e "$JAVA_HOME" ] ; then export JAVA_HOME="%{java_home}" ; fi
sh -x ant dist

################################################################################
%install
################################################################################

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 java-sdk/dist/packages/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 644 java-sdk/dist/packages/%{spname}.jar $RPM_BUILD_ROOT%{_javadir}/%{spname}.jar
install -m 644 java-sdk/dist/packages/%{filtname}.jar $RPM_BUILD_ROOT%{_javadir}/%{filtname}.jar
install -m 644 java-sdk/dist/packages/%{beansname}.jar $RPM_BUILD_ROOT%{_javadir}/%{beansname}.jar

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}-1.3.0

pushd $RPM_BUILD_ROOT%{_javadir}-1.3.0
	ln -fs ../java/*%{spname}.jar jndi-ldap.jar
popd

mkdir -p %{buildroot}%{_mavenpomdir}
sed -i 's/@VERSION@/%{version}/g' %{name}.pom
install -pm 644 %{name}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "ldapsdk:ldapsdk"

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -r java-sdk/dist/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

################################################################################
%files -f .mfiles
################################################################################

%{_javadir}/%{spname}*.jar
%{_javadir}/%{filtname}*.jar
%{_javadir}/%{beansname}*.jar
%{_javadir}-1.3.0/*.jar

################################################################################
%files javadoc
################################################################################

%dir %{_javadocdir}/%{name}
%{_javadocdir}/%{name}/*

################################################################################
%changelog
* Wed Nov 03 2021 Muhammad Falak <mwani@microsft.com> - 4.22.0-4
- Remove epoch from jpackage-utils

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.22.0-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Aug 13 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.22.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Set 'JAVA_HOME' to macro '%%{java_home}' to fix the build.

* Wed Jun 10 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.22.0-1
- Rebase to match latest upstream version: 4.22.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.21.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 08 2019 Dogtag PKI Team <pki-team@redhat.com> 4.21.0-2
- Bump min required JSS version to 4.6.0

* Thu Aug 08 2019 Dogtag PKI Team <pki-team@redhat.com> 4.21.0-1
- Rebased to LDAP SDK 4.21.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 10 2018 Dogtag PKI Team <pki-team@redhat.com> 4.20.0-1
- Rebased to LDAP SDK 4.20.0

