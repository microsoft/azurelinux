Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.3.1
Release:        3%{?dist}
License:        LGPLv2+
URL:            https://www.open-scap.org
Source0:        https://github.com/OpenSCAP/openscap/releases/download/%{version}/%{name}-%{version}.tar.gz
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cmake
BuildRequires:  swig libxml2-devel libxslt-devel perl-XML-Parser
BuildRequires:  rpm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pcre-devel
BuildRequires:  libacl-devel
BuildRequires:  libselinux-devel libcap-devel
BuildRequires:  util-linux-devel
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  popt-devel
BuildRequires:  python2-devel
Requires:       curl
Requires:       popt
%description
SCAP is a multi-purpose framework of specifications that supports automated configuration, vulnerability and patch checking, technical control compliance activities, and security measurement.
OpenSCAP has received a NIST certification for its support of SCAP 1.2.

%package devel
Summary: Development Libraries for openscap
Group: Development/Libraries
Requires: openscap = %{version}-%{release}
Requires: libxml2-devel
%description devel
Header files for doing development with openscap.

%package perl
Summary: openscap perl scripts
Requires: perl
Requires: openscap = %{version}-%{release}
%description perl
Perl scripts.

%package python
Summary: openscap python
Group: Development/Libraries
Requires: openscap = %{version}-%{release}
BuildRequires:  python2-devel
%description python
Python bindings.


%prep
%setup -q
mkdir build

%build
cd build
%cmake -DENABLE_PERL=ON \
       -DENABLE_SCE=ON \
       ..
make %{?_smp_flags}

%install
cd build
%make_install
#make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

#%check
#make check need BuildRequires per-XML-XPATH and bzip2
#no per-XML-XPATH so disable make check
#make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/*
%exclude /usr/src/debug
%exclude %{_libdir}/debug
%{_bindir}/*
#%{_libexecdir}/*
%{_mandir}/man8/*
%{_datadir}/openscap/*
%{_libdir}/libopenscap_sce.so.*
%{_libdir}/libopenscap.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libopenscap_sce.so
%{_libdir}/libopenscap.so
%{_libdir}/pkgconfig/*

%files perl
%defattr(-,root,root)
%{_libdir}/perl5/*
%{_datadir}/perl5/vendor_perl/openscap_pm.pm

%files python
%defattr(-,root,root)
%{_libdir}/python2.7/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.1-3
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.3.1-2
-   Renaming XML-Parser to perl-XML-Parser
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.3.1-1
-   Update to 1.3.1. Remove probe directory. License fixed.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.17-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.2.17-1
-   Update to 1.2.17
*   Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.14-3
-   Disable make check which need per-XML-XPATH for bug 1900358
*   Fri May 5 2017 Alexey Makhalov <amakhalov@vmware.com> 1.2.14-2
-   Remove BuildRequires XML-XPath.
*   Mon Mar 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.14-1
-   Update to latest version.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-2
-   BuildRequires curl-devel.
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-1
-   Initial build. First version
