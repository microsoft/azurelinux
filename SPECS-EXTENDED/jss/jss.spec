Vendor:         Microsoft Corporation
Distribution:   Mariner
################################################################################
Name:           jss
################################################################################

Summary:        Java Security Services (JSS)
URL:            http://www.dogtagpki.org/wiki/JSS
License:        MPLv1.1 or GPLv2+ or LGPLv2+

Version:        4.8.1
Release:        4%{?dist}
#global         _phase -a1

# To generate the source tarball:
# $ git clone https://github.com/dogtagpki/jss.git
# $ cd jss
# $ git tag v4.5.<z>
# $ git push origin v4.5.<z>
# Then go to https://github.com/dogtagpki/jss/releases and download the source
# tarball.
Source:         https://github.com/dogtagpki/%{name}/archive/v%{version}%{?_phase}/%{name}-%{version}%{?_phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > jss-VERSION-RELEASE.patch
# Patch: jss-VERSION-RELEASE.patch

################################################################################
# Build Dependencies
################################################################################

# autosetup
BuildRequires:  git
BuildRequires:  make
BuildRequires:  cmake >= 3.14
BuildRequires:  zip
BuildRequires:  unzip

BuildRequires:  gcc-c++
BuildRequires:  nspr-devel >= 4.13.1
BuildRequires:  nss-devel >= 3.44
BuildRequires:  nss-tools >= 3.44
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  slf4j
BuildRequires:  glassfish-jaxb-api
%if 0%{?rhel} && 0%{?rhel} <= 7
# no slf4j-jdk14
%else
BuildRequires:  slf4j-jdk14
%endif
BuildRequires:  apache-commons-lang3

BuildRequires:  junit

Requires:       nss >= 3.44
Requires:       java
Requires:       jpackage-utils
Requires:       slf4j
Requires:       glassfish-jaxb-api
%if 0%{?rhel} && 0%{?rhel} <= 7
# no slf4j-jdk14
%else
Requires:       slf4j-jdk14
%endif
Requires:       apache-commons-lang3

Conflicts:      ldapjdk < 4.20
Conflicts:      idm-console-framework < 1.2
Conflicts:      tomcatjss < 7.6.0
Conflicts:      pki-base < 10.10.0

%description
Java Security Services (JSS) is a java native interface which provides a bridge
for java-based applications to use native Network Security Services (NSS).
This only works with gcj. Other JREs require that JCE providers be signed.

################################################################################
%package javadoc
################################################################################

Summary:        Java Security Services (JSS) Javadocs
Requires:       jss = %{version}-%{release}

%description javadoc
This package contains the API documentation for JSS.

################################################################################
%prep

%autosetup -n %{name}-%{version}%{?_phase} -p 1 -S git

################################################################################
%build

%set_build_flags


# Enable compiler optimizations
export BUILD_OPT=1

# Generate symbolic info for debuggers
CFLAGS="-g $RPM_OPT_FLAGS"
export CFLAGS

# Check if we're in FIPS mode
modutil -dbdir /etc/pki/nssdb -chkfips true | grep -q enabled && export FIPS_ENABLED=1

# Disable looking for JAVA_AWT_LIBRARY to fix build.
sed -i -E "/.*JNI REQUIRED.*/i set(JAVA_AWT_LIBRARY NotNeeded)" CMakeLists.txt

# The Makefile is not thread-safe.
%cmake \
    -DJAVA_HOME=%{java_home} \
    -DJAVA_LIB_INSTALL_DIR=%{_jnidir} \
    -B %{_vpath_builddir}

cd %{_vpath_builddir}
%{__make} all
%{__make} javadoc

################################################################################
%install

# There is no install target so we'll do it by hand

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_jnidir}
install -m 644 %{_vpath_builddir}/jss4.jar ${RPM_BUILD_ROOT}%{_jnidir}/jss4.jar

# We have to use the name libjss4.so because this is dynamically
# loaded by the jar file.
install -d -m 0755 $RPM_BUILD_ROOT%{_libdir}/jss
install -m 0755 %{_vpath_builddir}/libjss4.so ${RPM_BUILD_ROOT}%{_libdir}/jss/
pushd  ${RPM_BUILD_ROOT}%{_libdir}/jss
    ln -fs %{_jnidir}/jss4.jar jss4.jar
popd

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp %{_vpath_builddir}/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -p jss.html $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -p *.txt $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%check
ctest --output-on-failure

# No ldconfig is required since this library is loaded by Java itself.
################################################################################
%files

%defattr(-,root,root,-)
%doc jss.html
%license MPL-1.1.txt gpl.txt lgpl.txt
%{_libdir}/*
%{_jnidir}/*

################################################################################
%files javadoc

%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}/

################################################################################
%changelog
* Wed Jan 05 2022 Thomas Crain <thcrain@microsoft.com> - 4.8.1-4
- Rename java-headless dependency to java
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.8.1-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Aug 13 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.8.1-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Disabled looking for Java's AWT libraries - not needed and Mariner currently don't have them.
- Moved tests into the '%%check' section to not break build on failing tests.

* Thu Jan 14 2021 Dogtag PKI Team <pki-devel@redhat.com> - 4.8.1-1
- Rebase to upstream stable JSS v4.8.1

* Thu Nov 05 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.8.0-2
- Add Conflicts on older PKI versions due to missing ACL3

* Wed Oct 21 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.8.0-1
- Rebase to upstream stable release JSS v4.8.0

* Fri Sep 11 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.7.3-1
- Rebase to upstream stable release JSS v4.7.3

* Tue Aug 18 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.7.2-1
- Rebase to upstream stable release JSS v4.7.2 ; fixes FTBFS

* Thu Jul 09 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.7.0-1
- Rebase to upstream stable release JSS v4.7.0

* Tue Jun 30 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.7.0-0.4
- Rebase to latest upstream JSS v4.7.0-b4

* Wed Jun 10 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.7.0-0.2
- Rebase to latest upstream JSS 4.7.0
- JSS Provided SSLEngine

* Mon Apr 27 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.4-1
- Rebase to JSS 4.6.4
- Fixes memory leak present since v4.6.2

* Thu Mar 5 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.3-1
- Rebase to JSS 4.6.3
- Fixes base64 encoding of CSRs

* Wed Mar 04 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.2-4
- Fix for PBE errors

* Tue Jan 28 2020 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.2-3
- Rebuild with new NSS to fix rhbz#1794814

* Tue Oct 29 2019 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.2-2
- Fix for rhbz#1766451

* Tue Oct 15 2019 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.2-1
- Rebase to JSS 4.6.2
- Fixes CVE-2019-14823

* Thu Aug 08 2019 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.1-2
- Disable unnecessary tests to fix broken s390x

* Thu Aug 08 2019 Dogtag PKI Team <pki-devel@redhat.com> - 4.6.1-1
- Rebase to JSS 4.6.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Dogtag PKI Team <pki-devel@redhat.com> - 4.5.3-2
- Add AIA OCSP certificate checking patch

* Tue Mar 19 2019 Dogtag PKI Team <pki-devel@redhat.com> - 4.5.3-1
- Rebase to JSS 4.5.3

* Fri Feb 01 2019 Dogtag PKI Team <pki-devel@redhat.com> - 4.5.2-3
- Include nuxwdog patch for netscape.security.util.Utils from PKI

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Dogtag PKI Team <pki-devel@redhat.com> 4.5.2-1
- Rebased to JSS 4.5.2

* Thu Nov 29 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.1-1
- Rebased to JSS 4.5.1
- Red Hat Bugzilla #1582323 - DER encoding error for enumerated types with a value of zero
- Red Hat Bugzilla #1534765 - javadoc for org.mozilla.jss.pkix.cms.SignedData.getSignerInfos() is incorrect

* Fri Aug 10 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.0-1
- Rebased to JSS 4.5.0

* Tue Aug 07 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.0-0.6
- Rebased to JSS 4.5.0-b1

* Tue Aug 07 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.0-0.5
- Red Hat Bugzilla #1612063 - Do not override system crypto policy (support TLS 1.3)

* Fri Jul 20 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.0-0.4
- Rebased to JSS 4.5.0-a4
- Red Hat Bugzilla #1604462 - jss: FTBFS in Fedora rawhide

* Thu Jul 05 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.0-0.3
- Rebased to JSS 4.5.0-a3

* Fri Jun 22 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.0-0.2
- Rebased to JSS 4.5.0-a2

* Fri Jun 15 2018 Dogtag PKI Team <pki-devel@redhat.com> 4.5.0-0.1
- Rebased to JSS 4.5.0-a1
