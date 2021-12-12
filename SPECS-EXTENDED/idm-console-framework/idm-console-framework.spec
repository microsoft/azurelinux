Vendor:         Microsoft Corporation
Distribution:   Mariner
################################################################################
Name:             idm-console-framework
################################################################################

Summary:          Identity Management Console Framework
URL:              http://www.dogtagpki.org/
License:          LGPLv2

BuildArch:        noarch

Version:          1.2.0
Release:          5%{?dist}
# global           _phase -a1

# To create a tarball from a version tag:
# $ git archive \
#     --format=tar.gz \
#     --prefix idm-console-framework-<version>/ \
#     -o idm-console-framework-<version>.tar.gz \
#     <version tag>
Source: https://github.com/dogtagpki/idm-console-framework/archive/v%{version}%{?_phase}/idm-console-framework-%{version}%{?_phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > idm-console-framework-VERSION-RELEASE.patch
# Patch: idm-console-framework-VERSION-RELEASE.patch

################################################################################
# Build Dependencies
################################################################################

# autosetup
BuildRequires:    git

BuildRequires:    java-devel >= 1.8.0
BuildRequires:    ant >= 1.6.2
BuildRequires:    jss >= 4.5.0-1
BuildRequires:    ldapjdk >= 4.20.0

################################################################################
# Runtime Dependencies
################################################################################

# Urge use of OpenJDK for runtime
Requires:         java >= 1.8.0
Requires:         jss >= 4.5.0-1
Requires:         ldapjdk >= 4.20.0

%description
A Java Management Console framework used for remote server management.

################################################################################
%prep
################################################################################

%autosetup -n idm-console-framework-%{version}%{?_phase} -p 1 -S git

################################################################################
%build
################################################################################

%{ant} \
    -Dlib.dir=%{_libdir} \
    -Dbuilt.dir=`pwd`/built \
    -Dclassdest=%{_javadir}

################################################################################
%install
################################################################################

install -d $RPM_BUILD_ROOT%{_javadir}
install -m644 built/release/jars/idm-console-* $RPM_BUILD_ROOT%{_javadir}

################################################################################
%files
################################################################################

%doc LICENSE
%{_javadir}/idm-console-base.jar
%{_javadir}/idm-console-mcc.jar
%{_javadir}/idm-console-mcc_en.jar
%{_javadir}/idm-console-nmclf.jar
%{_javadir}/idm-console-nmclf_en.jar

################################################################################
%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 10 2018 Dogtag PKI Team <pki-team@redhat.com> 1.2.0-1
- Rebased to IDM Console Framework 1.2.0
