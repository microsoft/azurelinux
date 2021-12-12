Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           ortp
Version:        0.23.0
Release:        6%{?dist}
Summary:        A C library implementing the RTP protocol (RFC3550)

License:        LGPLv2+ and VSL
URL:            https://gitlab.linphone.org/BC/public/ortp
# version 0.23.0 no longer exists at linphone.org
# we are reverting to it so linphone-3.6.1 runs until we can get
# recent linphone built.
Source:         https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
#Patch1:		ortp-libsrtp-1.5-fix.patch
#Patch2:		ortp-logging-warning.patch
# ortp-0.23.0 was calling crypto_get_random, which was a private API
# and has been removed.  This patch reads /dev/urandom instead.
Patch3:		ortp-random.patch
# Support libsrtp2
Patch4:		ortp-libsrtp2.patch
# Fix warning on strncpy: see rtcp_APP_get_name() in rtcpparse.c
Patch5:		ortp-gcc10.patch
BuildRequires:  doxygen
BuildRequires:  graphviz

BuildRequires:  libtool perl-Carp
BuildRequires:  libsrtp-devel
BuildRequires:  openssl-devel

%description
oRTP is a C library that implements RTP (RFC3550).

%package        devel
Summary:        Development libraries for ortp
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libsrtp-devel

Requires:       libzrtpcpp-devel


%description    devel
Libraries and headers required to develop software with ortp.

%prep
%setup0 -q

#patch1 -p1 -b .srtp-15
#patch2 -p1 -b .warn
%patch3 -p1 -b .rand
%patch4 -p1 -b .srtp2
%patch5 -p1 -b .gcc10

autoreconf -i -f

%{__perl} -pi.dot  -e 's/^(HAVE_DOT\s+=)\s+NO$/\1 YES/;s/^(CALL_GRAPH\s+=)\s+NO$/\1 YES/;s/^(CALLER_GRAPH\s+=)\s+NO$/\1 YES/' ortp.doxygen.in

%build
%configure --disable-static \
           --enable-ipv6 \
           --enable-ssl-hmac


make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;
rm doc/html/html.tar
rm -r %{buildroot}%{_datadir}/doc/%{name}-%{version}

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog TODO NEWS README
%license COPYING
%{_libdir}/libortp.so.9*

%files devel
%doc doc/html 
%{_includedir}/%{name}
%{_libdir}/libortp.so
%{_libdir}/pkgconfig/ortp.pc

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 0.23.0-6
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:0.23.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb  3 2020 Stuart Gathman <stuart@gathman.org> - 2:0.23.0-4
- Fix gcc-10 warn on use of strncpy with no NULL expected.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan  7 2020 Tom Callaway <spot@fedoraproject.org> - 2:0.23.0-2
- rebuild against new libsrtp

* Mon Nov 25 2019 Stuart Gathman <stuart@gathman.org> - 2:0.23.0-1
- Revert to 0.23.0 because 0.24.2 is incompatible even though it has
- the same ABI version.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Stuart Gathman <stuart@gathman.org> - 1:0.24.2-1
- Update to 0.24.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 15 2018 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.23.0-9
- built without zrtp

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Tom Callaway <spot@fedoraproject.org> - 1:0.23.0-1
- update to 0.23.0

* Fri Nov 14 2014 Tom Callaway <spot@fedoraproject.org> - 1:0.22.0-5
- rebuild for new libsrtp

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul  7 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.22.0-0
- ortp-0.22.0

* Sat Mar 23 2013 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.20.0-5
- autoreconf in %%prep (#926292)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.20.0-2
- ortp-0.20.0
- BR: libzrtpcpp-devel for F17+

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.18.0-1
- ortp-0.18.0
- drop patches for issues fixed in upstream (retval and unused vars)

* Tue Sep 27 2011 Dan Horák <dan[at]danny.cz> - 1:0.16.5-2
- fix another gcc warning and move all fixes to one patch

* Fri Sep  2 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.16.5-1
- ortp-0.16.5
- add BR: libsrtp-devel openssl-devel

* Tue Mar 15 2011 Karsten Hopp <karsten@redhat.com> 0.16.1-3.1
- fix build error (unused variable)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep  2 2010 Dan Horák <dan[at]danny.cz> - 1:0.16.1-2
- fix "ignoring return value" warning

* Mon Nov 30 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1:0.16.1-1
- Updated to 0.16.1, removed old patch
- removed autotool calls, and using install -p

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.5.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.4.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.14.2-0.3.20080211
- fix license tag
- epoch bump to fix pre-release versioning

* Thu Feb 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.2-0.20080211.2%{?dist}
- Update to 0.14.2 snapshot

* Tue Feb  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.2
- Apply patch to remove -Werror from the build (for PPC).

* Fri Feb  1 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.1
- Update to 0.14.1 (using CVS snapshot until official release is available).

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.13.1-4
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-2
- Fix URL

* Mon Apr 23 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-1
- Update to 0.13.1
- BR doxygen and graphviz for building documentation

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.0-1
- Update to 0.13.0
- ortp-devel BR pkgconfig
- Add ldconfig scriptlets

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.12.0-1
- Update to 0.12.0

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-2
- Bring back -Werror patch (needed for building on PPC)

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-1
- Update to 0.11.0
- Remove ortp-0.8.1-Werror.patch

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-3
- Bump release and rebuild

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-2
- Rebuild for Fedora Extras 5

* Tue Jan  3 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-1
- Upstream update

* Thu Dec 22 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-2
- Added ortp.pc to -devel

* Sat Dec  3 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-1
- Upstream update

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-6
- Fix a typo in Requires on -devel

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-5
- Add missing Requires on -devel

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-4
- Split from linphone
