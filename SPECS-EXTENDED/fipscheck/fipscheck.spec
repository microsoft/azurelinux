Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:	A library for integrity verification of FIPS validated modules
Name:		fipscheck
Version:	1.5.0
Release:	9%{?dist}
License:	BSD
# This is a Red Hat maintained package which is specific to
# our distribution.
URL:		https://pagure.io/fipscheck
Source0:	https://releases.pagure.org/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:	gcc
BuildRequires:	openssl-devel >= 1.0.0

Requires:      %{name}-lib%{?_isa} = %{version}-%{release}

%description
FIPSCheck is a library for integrity verification of FIPS validated
modules. The package also provides helper binaries for creation and
verification of the HMAC-SHA256 checksum files.

%package lib
Summary:	Library files for %{name}

Requires:	%{_bindir}/fipscheck

%description lib
This package contains the FIPSCheck library.

%package devel
Summary:	Development files for %{name}

Requires:	%{name}-lib%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags}

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    $RPM_BUILD_ROOT%{_bindir}/fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/fipscheck $RPM_BUILD_ROOT%{_libdir}/libfipscheck.so.1.2.1 \
    ln -s libfipscheck.so.1.2.1.hmac $RPM_BUILD_ROOT%{_libdir}/fipscheck/libfipscheck.so.1.hmac \
%{nil}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

mkdir -p $RPM_BUILD_ROOT%{_libdir}/fipscheck

%ldconfig_scriptlets lib

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc ChangeLog README NEWS AUTHORS
%{_bindir}/fipscheck
%{_bindir}/fipshmac
%{_libdir}/fipscheck/fipscheck.hmac
%{_mandir}/man8/*

%files lib
%{_libdir}/libfipscheck.so.*
%dir %{_libdir}/fipscheck
%{_libdir}/fipscheck/libfipscheck.so.*.hmac

%files devel
%{_includedir}/fipscheck.h
%{_libdir}/libfipscheck.so
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.0-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Tomáš Mráz <tmraz@redhat.com> - 1.5.0-1
- handle empty hmac file as checksum mismatch

* Tue Sep 10 2013 Tomáš Mráz <tmraz@redhat.com> - 1.4.1-1
- fix inverted condition in FIPSCHECK_verify_ex()

* Fri Sep  6 2013 Tomáš Mráz <tmraz@redhat.com> - 1.4.0-1
- added new API calls to support setting hmac suffix

* Mon Apr 16 2012 Tomas Mraz <tmraz@redhat.com> - 1.3.1-1
- manual pages added by Paul Wouters

* Tue Sep  7 2010 Tomas Mraz <tmraz@redhat.com> - 1.3.0-1
- look up the hmac files in the _libdir/fipscheck first

* Tue May 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.0-1
- add lib subpackage to avoid multilib on the base package
- add ability to compute hmacs on multiple files at once
- improved debugging with FIPSCHECK_DEBUG

* Thu Mar 19 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.1-1
- move binaries and libraries to /usr

* Wed Mar 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.0-1
- hmac check itself as required by FIPS

* Mon Feb  9 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.4-1
- add some docs to the README, require current openssl in Fedora

* Fri Oct 24 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.3-1
- use OpenSSL in FIPS mode to do the HMAC checksum instead of NSS

* Tue Sep  9 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.2-1
- fix test for prelink

* Mon Sep  8 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.1-1
- put binaries in /bin and libraries in /lib as fipscheck
  will be used by modules in /lib

* Mon Sep  8 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.0-2
- minor fixes for package review

* Wed Sep  3 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.0-1
- Initial spec file
