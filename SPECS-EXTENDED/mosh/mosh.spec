Name:		mosh
Version:	1.4.0
Release:	6%{?dist}
Summary:	Mobile shell that supports roaming and intelligent local echo
Vendor:     Microsoft Corporation
Distribution: Mariner

License:	GPLv3+
URL:		https://mosh.mit.edu/
Source0:	https://github.com/mobile-shell/mosh/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:	libutempter-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-diagnostics
BuildRequires:	perl-generators
BuildRequires:	protobuf-compiler
BuildRequires:	protobuf-devel
BuildRequires:	zlib-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
Requires:	openssh-clients
Requires:	openssl
Requires:	perl-IO-Socket-IP

%description
Mosh is a remote terminal application that supports:
  - intermittent network connectivity,
  - roaming to different IP address without dropping the connection, and
  - intelligent local echo and line editing to reduce the effects
    of "network lag" on high-latency connections.


%prep
%setup -q


%build
%configure --disable-silent-rules
%make_build


%install
%make_install


%files
%doc README.md ChangeLog
%license COPYING
%{_bindir}/mosh
%{_bindir}/mosh-client
%{_bindir}/mosh-server
%{_mandir}/man1/mosh.1.gz
%{_mandir}/man1/mosh-client.1.gz
%{_mandir}/man1/mosh-server.1.gz


%changelog
* Sun Aug 11 2024 Chris Co <chrco@microsoft.com> - 1.4.0-6
- Initial CBL-Mariner import from Fedora 40 (license: MIT)
- License verified

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Alex Chernyakhovsky <achernya@mit.edu> - 1.4.0-1
- Update to mosh 1.4.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 05 2022 Michal Josef Špaček <mspacek@redhat.com> - 1.3.2-14
- Remove dependency to obsolete IO::Socket::INET6

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 1.3.2-12
- Rebuilt for protobuf 3.19.0

* Tue Oct 26 2021 Adrian Reber <adrian@lisas.de> - 1.3.2-11
- Rebuilt for protobuf 3.18.1

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.3.2-10
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 08:32:44 CET 2021 Adrian Reber <adrian@lisas.de> - 1.3.2-7
- Rebuilt for protobuf 3.14

* Thu Sep 24 2020 Adrian Reber <adrian@lisas.de> - 1.3.2-6
- Rebuilt for protobuf 3.13

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de> - 1.3.2-4
- Rebuilt for protobuf 3.12

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 1.3.2-2
- Rebuild for protobuf 3.11

* Sun Sep 22 2019 Alex Chernyakhovsky <achernya@mit.edu> - 1.3.2-1
- Update to mosh 1.3.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.0-9
- Rebuild for protobuf 3.6

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.0-6
- Rebuild for protobuf 3.5

* Mon Nov 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.0-5
- Rebuild for protobuf 3.4

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Orion Poplawski <orion@cora.nwra.com> - 1.3.0-2
- Rebuild for protobuf 3.3.1

* Sun Mar 26 2017 Alex Chernyakhovsky <achernya@mit.edu> - 1.3.0-1
- Update to mosh 1.3.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2.6-3
- Rebuild for protobuf 3.2.0

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.6-2
- Rebuild for protobuf 3.1.0

* Wed Aug 10 2016 Alex Chernyakhovsky <achernya@mit.edu> - 1.2.6-1
- Update to mosh 1.2.6

* Mon Feb 08 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.5-3
- Let package honor RPM_OPT_FLAGS (Fix F24FTBFS).
- Add %%license.
- Make building verbose.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug  6 2015 Alex Chernyakhovsky <achernya@mit.edu> - 1.2.5-1
- Update to mosh 1.2.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Alex Chernyakhovsky <achernya@mit.edu> - 1.2.4-6
- Rebuild for protobuf version bump.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.2.4-2
- Perl 5.18 rebuild

* Wed Mar 27 2013 Alexander Chernyakhovsky <achernya@mit.edu> - 1.2.4-1
- Update to mosh 1.2.4

* Sun Mar 10 2013 Alexander Chernyakhovsky <achernya@mit.edu> - 1.2.3-3
- Rebuilt for Protobuf API change from 2.4.1 to 2.5.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Alexander Chernyakhovsky <achernya@mit.edu> - 1.2.3-1
- Update to mosh 1.2.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Alexander Chernyakhovsky <achernya@mit.edu> - 1.2.2-1
- Update to mosh 1.2.2

* Sat Apr 28 2012 Alexander Chernyakhovsky <achernya@mit.edu> - 1.2-2
- Add -g and -O2 CFLAGS

* Fri Apr 27 2012 Alexander Chernyakhovsky <achernya@mit.edu> - 1.2-1
- Update to mosh 1.2.

* Mon Mar 26 2012 Alexander Chernyakhovsky <achernya@mit.edu> - 1.1.1-1
- Update to mosh 1.1.1.

* Wed Mar 21 2012 Alexander Chernyakhovsky <achernya@mit.edu> - 1.1-1
- Initial packaging for mosh.
