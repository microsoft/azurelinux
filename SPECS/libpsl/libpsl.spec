Summary:        libpsl - C library to handle the Public Suffix List
Name:           libpsl
Version:        0.21.1
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Development
URL:            https://github.com/rockdaboot/libpsl
Source0:        https://github.com/rockdaboot/libpsl/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  icu-devel
BuildRequires:  python3
Requires:       icu

%description
libpsl is a C library to handle the Public Suffix List. A "public suffix" is a
domain name under which Internet users can directly register own names.

Browsers and other web clients can use it to

- Avoid privacy-leaking "supercookies";
- Avoid privacy-leaking "super domain" certificates;
- Domain highlighting parts of the domain in a user interface;
- Sorting domain lists by site;

Libpsl...

- has built-in PSL data for fast access;
- allows to load PSL data from files;
- checks if a given domain is a "public suffix";
- provides immediate cookie domain verification;
- finds the longest public part of a given domain;
- finds the shortest private part of a given domain;
- works with international domains (UTF-8 and IDNA2008 Punycode);
- is thread-safe;
- handles IDNA2008 UTS#46;

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%package -n     psl
Summary:        Commandline utility to explore the Public Suffix List
Requires:       %{name} = %{version}-%{release}

%description -n psl
This package contains a commandline utility to explore the Public Suffix List,
for example it checks if domains are public suffixes, checks if cookie-domain
is acceptable for domains and so on.

%prep
%setup -q

%build
%configure --disable-silent-rules \
           --disable-static
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
install -m0755 src/psl-make-dafsa %{buildroot}%{_bindir}/

%check
make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING LICENSE
%{_libdir}/*.so.*

%files -n psl
%defattr(-,root,root)
%doc AUTHORS NEWS
%{_bindir}/psl
%{_bindir}/psl-make-dafsa
%{_mandir}/man1/psl.*
%{_mandir}/man1/psl-make-dafsa.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.21.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jan 12 2022 Henry Li <lihl@microsoft.com> - 0.21.1-1
- Upgrade to version 0.21.1
- Use python3 as BR instead of python2
- Modify the Source0 field

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 0.20.2-6
- Remove libtool archive files from final packaging

* Fri Apr 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20.2-5
- Bumping up release to re-compile against the new version of the 'icu' libraries.
- License verified.
- Removing the 'sha1' macro.
- Updated the '%%license' macro.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.20.2-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.20.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 0.20.2-2
- Added BuildRequires python2

* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 0.20.2-1
- Initial packaging of libpsl
