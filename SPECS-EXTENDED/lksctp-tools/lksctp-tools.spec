Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:    lksctp-tools
Summary: User-space access to Linux Kernel SCTP
Version: 1.0.19
Release: 10%{?dist}
License: GPL-2.0-or-later AND LGPL-2.0-only AND MIT
Group:   System Environment/Libraries
URL:     http://lksctp.sourceforge.net

Source0: https://github.com/sctp/lksctp-tools/archive/%{name}-%{version}.tar.gz
Patch0: sctp_test-check-strdup-return-in-append_addr.patch
Patch1: man-add-the-missing-description-for-3-flags-in-sctp_.patch
Patch2: man-update-for-DESCRIPTION-and-SYSCTL-in-sctp.7.patch
Patch3: man-add-some-missing-items-in-STATISTICS-in-sctp.7.patch
Patch4: man-improve-the-description-in-SOCKET-OPTIONS-in-sct.patch
Patch5: man-add-the-missing-options-in-SOCKET-OPTIONS-in-sct.patch
Patch6: man-add-CONTROL-MSGS-and-NOTIFICATIONS-in-sctp.7.patch
Patch7: lib-define-cmsg-array-with-correct-size-in-sendv-and.patch
BuildRequires: libtool, automake, autoconf, make

%description
This is the lksctp-tools package for Linux Kernel SCTP (Stream Control
Transmission Protocol) Reference Implementation.

This package is intended to supplement the Linux Kernel SCTP Reference
Implementation now available in the Linux kernel source tree in
versions 2.5.36 and following.  For more information on LKSCTP see the
package documentation README file, section titled "LKSCTP - Linux
Kernel SCTP."

This package contains the base run-time library and command-line tools.

%package devel
Summary: Development files for lksctp-tools
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for lksctp-tools which include man pages, header files,
static libraries, symlinks to dynamic libraries and some tutorial source code.

%package doc
Summary: Documents pertaining to SCTP
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description doc
Documents pertaining to LKSCTP & SCTP in general (IETF RFC's & Internet
Drafts).

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1

%build
[ ! -x ./configure ] && sh bootstrap
%configure --disable-static
# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
rm -f doc/rfc2960.txt doc/states.txt
%make_install

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

%files
%doc AUTHORS ChangeLog COPYING* README
%{_bindir}/*
%{_libdir}/libsctp.so.1*
%dir %{_libdir}/lksctp-tools/
%{_libdir}/lksctp-tools/libwithsctp.so.1*
%{_mandir}/man7/*

%files devel
%{_includedir}/*
%{_libdir}/libsctp.so
%{_libdir}/pkgconfig/libsctp.pc
%{_libdir}/lksctp-tools/libwithsctp.so
%{_datadir}/lksctp-tools/
%{_mandir}/man3/*

%files doc
%doc doc/*.txt

%changelog
* Mon Jan 27 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.0.19-10
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 26 2024 Xin Long <lxin@redhat.com> - 1.0.19-8
- man doc update and one fix for lib and another for sctp_test

* Fri Jan 26 2024 Xin Long <lxin@redhat.com> - 1.0.19-7
- Use SDPX license IDs

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun  5 2022 Peter Hanecak <hany@hany.sk> - 1.0.19-1
- Updated to 1.0.19
- Patches dropped since changes are now incorporated in the upstream

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Apr 17 2021 Peter Hanecak <hany@hany.sk> - 1.0.18-10
- Added autoconf-2.70 fix from upstream

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Jeff Law <law@redhat.com> - 1.0.18-8
- Use symver attribute for symbol versioning.  Re-enable LTO

* Wed Aug 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.0.18-7
- Drop useless ldconfig scriptlets

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 1.0.18-5
- Disable LTO

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Vit Mojzis <vmojzis@redhat.com> - 1.0.18-3
- Added a patch to fix netinet/sctp.h not to be installed.
- Added some fixes for kernel feature detection.
- Updated to 1.0.18. [1568622]

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.16-1
- Update to 1.0.16
- Spec cleanups

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Daniel Borkmann <dborkman@redhat.com> - 1.0.15-1
- Update to 1.0.15

* Tue Apr 09 2013 Daniel Borkmann <dborkman@redhat.com> - 1.0.14-1
- Update to 1.0.14

* Fri Jan 25 2013 Daniel Borkmann <dborkman@redhat.com> - 1.0.13-1
- Update to 1.0.13

* Mon Jan 21 2013 Jan Safranek <jsafrane@redhat.com> - 1.0.12-1
- Update to 1.0.12

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.0.11-2
- Merge-review cleanup (#226100)

* Tue Dec  1 2009 Jan Safranek <jsafrane@redhat.com> 1.0.11-1
- Update to 1.0.11
- Remove rpath from compiled binaries
- Remove static libraries

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Zdenek Prikryl <zprikryl@redhat.com> 1.0.10-1
- added release tag to Requires of devel and doc packages (#492531)
- Update to 1.0.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 06 2008 Zdenek Prikryl <zprikryl@redhat.com> 1.0.9-1
- Update to 1.0.9

* Wed Jul 16 2008 Zdenek Prikryl <zprikryl@redhat.com> 1.0.8-1
- Update to 1.0.8

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.7-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Karsten Hopp <karsten@redhat.com> 1.0.7-2
- rebuild for buildid

* Wed Aug 08 2007 Karsten Hopp <karsten@redhat.com> 1.0.7-1
- update to 1.0.7
- update license tag

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.0.6-3
- add post/postun requirements
- review fixes

* Tue Sep 19 2006 Karsten Hopp <karsten@redhat.de> 1.0.6-2
- fix fileconflict (#205225)

* Tue Jul 25 2006 Karsten Hopp <karsten@redhat.de> 1.0.6-1
- update to 1.0.6

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> 1.0.5-1
- 1.0.5

* Fri Nov 11 2005 Matthias Saou <http://freshrpms.net/> 1.0.4-1
- Update to 1.0.4.
- Update syntax patch.
- Execute bootstrap if no configure script is found.
- Don't own entire man? directories.
- Own data and lib lksctp-tools directories.
- Move devel libs in _libdir/lksctp-tools/ to devel package.
- Exclude .la files.
- Minor spec file cleanups.

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-5
- build with gcc-4

* Mon Feb 07 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-4
- initialize variable before use
- fix subscript out of range bug (#147286)

* Mon Jan 24 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-3
- build for FC

* Mon Jan 24 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-2.40E.1
- initial RH version based on sourceforge rpm

* Thu Dec 30 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.2-1
- 1.0.2 Release

* Tue May 11 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.1-1
- 1.0.1 Release

* Thu Feb 26 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.0-1
- 1.0.0 Release

* Fri Feb  6 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.9.0-1
- package only .txt doc files

* Wed Feb  4 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.7.5-1
- badly placed & undelivered files
- simplified delivery list

* Tue Jan 27 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.7.5-1
- Integrate comment from project team

* Sat Jan 10 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 2.6.0_test7_0.7.4-1
- Creation
