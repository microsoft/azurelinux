%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%global	major 78
Summary:       Mozilla's JavaScript engine.
Name:          mozjs
Version:       78.10.0
Release:       2%{?dist}
Group:         Applications/System
Vendor:        Microsoft Corporation
License:       MPLv2.0 and MPLv1.1 and BSD and GPLv2+ and GPLv3+ and LGPLv2+ and AFL and ASL 2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Source0:       https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
%define sha1   firefox-%{version}=547bac33732774993bd8223de9acfeedcc69a10d
Patch0:        emitter.patch
Patch1:        emitter_test.patch
# Build fixes
Patch2:        init_patch.patch
Patch3:        spidermonkey_checks_disable.patch
Distribution:  Mariner
BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3-libs
BuildRequires: python3-devel
BuildRequires: zlib-devel
BuildRequires: gcc
BuildRequires: llvm
BuildRequires: llvm-devel
BuildRequires: icu-devel
BuildRequires: rust
BuildRequires: autoconf213
Requires:      icu
Requires:      python3
Requires:      python3-libs
Obsoletes:     mozjs60
Obsoletes:     mozjs68
Obsoletes:     js

%description
Mozilla's JavaScript engine includes a just-in-time compiler (JIT) that compiles
JavaScript to machine code, for a significant speed increase.

%package       devel
Summary:       mozjs devel
Group:         Development/Tools
Requires:      %{name} = %{version}-%{release}

%description   devel
This contains development tools and libraries for SpiderMonkey.

%prep
%setup -q -n firefox-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
rm -rf modules/zlib

%build
cd js/src
%configure \
    --with-system-icu \
    --enable-readline \
    --disable-jemalloc \
    --disable-tests \
    --with-system-zlib
make %{?_smp_mflags}

%install
cd js/src
make DESTDIR=%{buildroot} install
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc
# remove non required files
rm %{buildroot}%{_libdir}/libjs_static.ajs
rm -rf %{buildroot}%{_libdir}/debug
rm -rf %{buildroot}/usr/src
find %{buildroot} -name '*.la' -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/js%{major}
%{_bindir}/js%{major}-config
%{_libdir}/libmozjs-%{major}.so

%files devel
%defattr(-,root,root)
%{_includedir}/mozjs-%{major}
%{_libdir}/pkgconfig/mozjs-%{major}.pc

%changelog
*   Wed Sep 22 2021 Jon Slobodzian <joslobo@microsoft.com> 78.10.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2)

*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 78.10.0-1
-   Automatic Version Bump

*   Fri Feb 19 2021 Alexey Makhalov <amakhalov@vmware.com> 78.3.1-2
-   Remove python2 requirements

*   Mon Oct 05 2020 Ankit Jain <ankitja@vmware.com> 78.3.1-1
-   Updated to 78.3.1

*   Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 68.11.0-2
-   Removed autoconf213 dependency and obsoletes js

*   Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 68.11.0-1
-   initial version
