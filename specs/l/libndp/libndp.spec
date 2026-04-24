# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: libndp
Version: 1.9
Release: 5%{?dist}
Summary: Library for Neighbor Discovery Protocol
License: LGPL-2.1-or-later
URL: http://www.libndp.org/
Source: http://www.libndp.org/files/libndp-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires: make
%description
This package contains a library which provides a wrapper
for IPv6 Neighbor Discovery Protocol.  It also provides a tool
named ndptool for sending and receiving NDP messages.

%package devel
Summary: Libraries and header files for libndp development
Requires: libndp = %{version}-%{release}

%description devel
The libndp-devel package contains the header files and libraries
necessary for developing programs using libndp.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -delete

%ldconfig_scriptlets

%files
%doc COPYING
%{_libdir}/*so.*
%{_bindir}/ndptool
%{_mandir}/man8/ndptool.8*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Jiri Pirko <jiri@nvidia.com> - 1.9-1
- 1.9 release
- ndptool: add support for PREF64 option
- libndp: add support for PREF64 option
- libndp: valid route information option length
- SubmittingPatches: update mailing list

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 Eric Garver <eric@garver.life> - 1.8-7
- migrated to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Jiri Pirko <jiri@nvidia.com> - 1.8-1
- 1.8 release
- libndp,ndptool: use poll() instead of select()
- libndp: avoid static buffer for debug string in ndp_sock_recv()
- ndptool: avoid static buffer for string in ndptool
- libndp: use thread local variables for static return arguments
- ndptool: don't use static variable for local context in msgrcv_handler_func()
- ndptool: fix printing dnssl lifetime in ndptool
- ndptool: fix potential memory leak caused by strdup
- ndptool: add -D dest support
- libndp: fix nd_msg typo when setting target address
- libndp: close sockfd after using to avoid handle leak
- ndptool: fix target parameter typo
- ndptool: add -T target support

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 08 2018 Jiri Pirko <jiri@mellanox.com> - 1.7-1
- 1.7 release
- libndp: apply filter to raw socket to only accept ND messages
- libndp: move ndp_sock_{open,close}() after msg parsing functions
- ndptool: Fix compilation on musl libc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 17 2016 Jiri Pirko <jiri@mellanox.com> - 1.6-1
- Update to 1.6
- libndb: reject redirect and router advertisements from non-link-local
- libndp: validate the IPv6 hop limit
- libndp: revert API change for ndp_msg_send() and add ndp_msg_send_with_flags()
- libndp: fix type of field "na" in "struct ndp_msgna"
- ndptool: add option to send messages types
- libndp: add option flags to send messages
- Add SubmittingPatches howto

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 02 2015 Jiri Pirko <jpirko@redhat.com> - 1.5-1
- Update to 1.5
- ndptool: use conventional signal handlers instead of signalfd

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Jiri Pirko <jpirko@redhat.com> - 1.4-1
- Update to 1.4
- libndp: fix buffer overflow in ndp_msg_opt_dnssl_domain()

* Thu Jun 26 2014 Jiri Pirko <jpirko@redhat.com> - 1.3-1
- Update to 1.3
- Add missing <stdarg.h> include for va_list

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Jiri Pirko <jpirko@redhat.com> - 1.2-2
- libndp: fix [cppcheck] Undefined behavior: Variable 'buf' is used as parameter and destination in s[n]printf() [1044084] [1091720]

* Tue Oct 15 2013 Jiri Pirko <jpirko@redhat.com> - 1.2-1
- Update to 1.2
- libndp: silently ignore packets with optlen 0
- libndp: fix processing for larger options
- libndp: do not fail on receiving non-ndp packets

* Fri Oct 04 2013 Jiri Pirko <jpirko@redhat.com> - 1.1-1
- Update to 1.1

* Fri Sep 13 2013 Dan Williams <dcbw@redhat.com> - 1.0-2
- Fix .pc file includes path
- Fix ndptool -v argument

* Thu Aug 08 2013 Jiri Pirko <jpirko@redhat.com> - 1.0-1
- Update to 1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4.20130723git873037a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Dan Williams <dcbw@redhat.com> - 0.1-3.20130723git873037a
- Update to git 873037a

* Fri Jun 07 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-2.20130607git39e1f53
- Update to git 39e1f53

* Sat May 04 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-1.20130504gitca3c399
- Initial build.
