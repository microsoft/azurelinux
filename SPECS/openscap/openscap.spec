Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.3.5
Release:        4%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.open-scap.org
Source0:        https://github.com/OpenSCAP/openscap/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:         support_rpm_418.patch
BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libselinux-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  pcre-devel
BuildRequires:  perl-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  popt-devel
BuildRequires:  python3-devel
BuildRequires:  rpm-devel
BuildRequires:  swig
BuildRequires:  util-linux-devel
BuildRequires:  xmlsec1-devel
Requires:       curl
Requires:       popt
Requires:       xmlsec1
Provides:       %{name}-engine-sce = %{version}-%{release}
Provides:       %{name}-scanner = %{version}-%{release}
Provides:       %{name}-utils = %{version}-%{release}

%description
SCAP is a multi-purpose framework of specifications that supports automated configuration, vulnerability and patch checking, technical control compliance activities, and security measurement.
OpenSCAP has received a NIST certification for its support of SCAP 1.2.

%package devel
Summary:        Development Libraries for openscap
Group:          Development/Libraries
Requires:       libxml2-devel
Requires:       openscap = %{version}-%{release}

%description devel
Header files for doing development with openscap.

%package perl
Summary:        openscap perl scripts
Requires:       openscap = %{version}-%{release}
Requires:       perl-interpreter

%description perl
Perl scripts.

%package -n python3-%{name}
Summary:        openscap python
Group:          Development/Libraries
Requires:       openscap = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for %{name}.

%prep
%autosetup -p1
mkdir build

%build
cd build
%cmake -DENABLE_PERL=ON \
       -DENABLE_SCE=ON \
       -DPYTHON_EXECUTABLE:STRING=%{python3} \
       -DPYTHON_VERSION_MAJOR:STRING=$(%{python3} -c "import sys; print(sys.version_info.major)") \
       -DPYTHON_VERSION_MINOR:STRING=$(%{python3} -c "import sys; print(sys.version_info.minor)") \
       ..
%make_build

%install
cd build
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

#%check
#make check need BuildRequires per-XML-XPATH and bzip2
#no per-XML-XPATH so disable make check
#make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/*
%exclude %{_prefix}/src/debug
%exclude %{_libdir}/debug
%{_bindir}/*
%{_mandir}/man8/*
%{_datadir}/openscap/*
%{_libdir}/libopenscap_sce.so.*
%{_libdir}/libopenscap.so.*

%files devel
%defattr(-,root,root)
%{_datadir}/perl5/vendor_perl/openscap_pm.so
%{_includedir}/*
%{_libdir}/libopenscap_sce.so
%{_libdir}/libopenscap.so
%{_libdir}/pkgconfig/*

%files perl
%defattr(-,root,root)
%{_libdir}/perl5/*

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.3.5-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Sun Sep 11 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.3.5-3
- Backport fix to support rpm 4.18.0 versions which moved headers around

* Tue Dec 07 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.5-2
- Using "xmlsec1" instead of "libxmlsec1" as dependency.
- Fixing building Perl binding for new version.

* Tue Nov 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.3.5-1
- Update to version 1.3.5
- License verified

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.3.1-7
- Add provides for scanner subpackage from base package
- Remove openscap-python python2 subpackage
- Add python3-openscap subpackage

* Tue Jan 12 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.3.1-6
- Provide openscap-engine-sce and openscap-utils.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.3.1-5
- Use new perl package names.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.3.1-4
- Explicitly set python verison.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.1-3
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.3.1-2
- Renaming XML-Parser to perl-XML-Parser

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.3.1-1
- Update to 1.3.1. Remove probe directory. License fixed.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.17-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 1.2.17-1
- Update to 1.2.17

* Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> - 1.2.14-3
- Disable make check which need per-XML-XPATH for bug 1900358

* Fri May 5 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.2.14-2
- Remove BuildRequires XML-XPath.

* Mon Mar 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.14-1
- Update to latest version.

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.2.10-2
- BuildRequires curl-devel.

* Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.2.10-1
- Initial build. First version
