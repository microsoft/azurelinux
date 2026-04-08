# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       perl-SOAP-Lite
Version:    1.27
Release:    27%{?dist}
Summary:    Client and server side SOAP implementation
License:    GPL-1.0-or-later OR Artistic-1.0-Perl
URL:        https://metacpan.org/release/SOAP-Lite
Source0:    https://cpan.metacpan.org/authors/id/P/PH/PHRED/SOAP-Lite-%{version}.tar.gz
# Remove /usr/bin/env from shebang
Patch0:     SOAP-Lite-1.22-Remove-usr-bin-env-from-shebang.patch
BuildArch:  noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
# XXX: BuildRequires:  perl(Apache)
# XXX: BuildRequires:  perl(Apache::Const)
# XXX: BuildRequires:  perl(Apache::Constants)
# XXX: BuildRequires:  perl(Apache::RequestIO)
# XXX: BuildRequires:  perl(Apache::RequestRec)
# XXX: BuildRequires:  perl(Apache2::Const)
# XXX: BuildRequires:  perl(Apache2::RequestIO)
# XXX: BuildRequires:  perl(Apache2::RequestRec)
# XXX: BuildRequires:  perl(Apache2::RequestUtil)
# XXX: BuildRequires:  perl(APR::Table)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Inspector)
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(constant)
# FIXME: Unpackaged BuildRequires:  perl(DIME::Message)
# FIXME: Unpackaged BuildRequires:  perl(DIME::Payload)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
# XXX: BuildRequires:  perl(FCGI)
BuildRequires:  perl(HTTP::Daemon)
# XXX: BuildRequires:  perl(HTTP::Daemon::SSL)
# XXX: BuildRequires:  perl(HTTP::Headers)
# XXX: BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::SessionData)
BuildRequires:  perl(IO::SessionSet)
BuildRequires:  perl(IO::Socket)
# XXX: BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(MIME::Base64)
# XXX: BuildRequires:  perl(MIME::Entity)
BuildRequires:  perl(MIME::Lite)
BuildRequires:  perl(MIME::Parser)
BuildRequires:  perl(Net::POP3)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::Escape)
# XXX: BuildRequires:  perl(URI::_server)
BuildRequires:  perl(vars)
# XXX: BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(XML::Parser::Lite)
# Tests only
# Note many tests are skipped as they require an HTTP server set up
BuildRequires:  perl(B)
BuildRequires:  perl(blib)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(IPC::Open2)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(utf8)
# Optional tests only
# XXX: BuildRequires:  perl(LWP::Protocol::https)
# XXX: BuildRequires:  perl(Test::MockObject)
BuildRequires:  perl(Test::XML)
# We need HTTP::Response in case Test::MockObject gets pulled in somehow
BuildRequires:  perl(HTTP::Response)
# XXX: BuildRequires:  perl(Test::Kwalitee) >= 1.21
# XXX: BuildRequires:  perl(Test::Pod) >= 1.41
# We don't require various webserver transports (Apache*/APR, FCGI);
# this would introduced a huge dependency chain and people will generally want only one
# The server also introduces a huge dependency chain not everyone really wants.
Requires:       perl(Compress::Zlib)
# FIXME: Unpackaged Requires:       perl(DIME::Message)
# FIXME: Unpackaged Requires:       perl(DIME::Payload)
Requires:       perl(Encode)
Requires:       perl(HTTP::Headers)
Requires:       perl(HTTP::Request)
Requires:       perl(LWP::Protocol::http)
Requires:       perl(LWP::Protocol::https)
Requires:       perl(LWP::UserAgent)
Requires:       perl(MIME::Base64)
Requires:       perl(MIME::Entity)
Requires:       perl(URI::_server)
Requires:       perl(XML::Parser)
# Merged back into SOAP-Lite in 1.00
Provides:       perl-SOAP-Transport-TCP = %{version}-%{release}
Obsoletes:      perl-SOAP-Transport-TCP < 0.715-12

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(My::.*\\)
%global __provides_exclude %__provides_exclude|perl\\(LWP::Protocol\\)
%global __requires_exclude %{?_requires_exclude:%__requires_exclude|}perl\\(My::\\)

%description
SOAP::Lite is a collection of Perl modules which provides a simple and
lightweight interface to the Simple Object Access Protocol (SOAP) both on
client and server side.

%prep
%autosetup -p1 -n SOAP-Lite-%{version}
find examples -type f -exec chmod -c ugo-x {} +

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes HACKING README ReleaseNotes.txt examples
%{_bindir}/SOAPsh.pl
%{_bindir}/stubmaker.pl
%{perl_vendorlib}/SOAP
%{perl_vendorlib}/Apache
%{_mandir}/man3/Apache::SOAP.3pm{,.*}
%{_mandir}/man3/SOAP::*.3pm{,.*}
%{_mandir}/man1/SOAPsh.pl.1{,.*}
%{_mandir}/man1/stubmaker.pl.1{,.*}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 24 2024 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.27-24
- Update to more modern perl build/install commands
- Perform deglobbing of files per packaging guidelines

* Thu Feb 22 2024 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.27-23
- Replace deprecated patchN macro (eliminating a build warning)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 09 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.27-19
- Remove obsolete filter-requires.sh script

* Mon Mar 06 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.27-18
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-15
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-9
- Perl 5.32 rebuild

* Tue Mar 17 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-8
- Add perl(blib) for tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-2
- Perl 5.28 rebuild

* Tue May 15 2018 Jan Pazdziora <jpazdziora@redhat.com> - 1.27-1
- 1578182 - Rebase to upstream version 1.27.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 Jan Pazdziora <jpazdziora@redhat.com> - 1.26-1
- 1529819 - Rebase to upstream version 1.26.

* Wed Dec 20 2017 Jan Pazdziora <jpazdziora@redhat.com> - 1.24-1
- 1527723 - Rebase to upstream version 1.24.

* Tue Dec 19 2017 Jan Pazdziora <jpazdziora@redhat.com> - 1.23-1
- 1527521 - Rebase to upstream version 1.23.

* Tue Nov 07 2017 Petr Pisar <ppisar@redhat.com> - 1.22-2
- Remove /usr/bin/env from shebang

* Sat Aug 19 2017 Jan Pazdziora <jpazdziora@redhat.com> - 1.22-1
- 1482299 - Rebase to upstream version 1.22.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Jan Pazdziora <jpazdziora@redhat.com> - 1.20-1
- 1346655 - Rebase to upstream version 1.20.

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 27 2015 Petr Šabata <contyk@redhat.com> - 1.19-1
- 1.19 bump, a properly versioned release

* Wed Aug 26 2015 Petr Šabata <contyk@redhat.com> - 1.18-1
- 1.18 bump

* Fri Jul 31 2015 Petr Šabata <contyk@redhat.com> - 1.17-1
- 1.17 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-2
- Perl 5.22 rebuild

* Wed Mar 25 2015 Petr Šabata <contyk@redhat.com> - 1.14-1
- 1.14 bump
- We now run way more tests than before, yay
- Dep list rewritten once again, I hope nothing breaks

* Tue Jan 06 2015 Petr Šabata <contyk@redhat.com> - 1.13-1
- 1.13 bugfix bump

* Fri Dec 05 2014 Petr Šabata <contyk@redhat.com> - 1.12-1
- 1.12 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Petr Šabata <contyk@redhat.com> - 1.11-1
- 1.11 bump

* Tue Jan 28 2014 Petr Šabata <contyk@redhat.com> - 1.10-1
- 1.10 bump

* Thu Jan 16 2014 Petr Šabata <contyk@redhat.com> - 1.09-1
- 1.09 bugfix bump

* Tue Jan 07 2014 Petr Šabata <contyk@redhat.com> - 1.08-2
- Update the source URL

* Mon Nov 25 2013 Petr Šabata <contyk@redhat.com> - 1.08-1
- 1.08 bump, no code changes

* Thu Nov 14 2013 Petr Šabata <contyk@redhat.com> - 1.06-3
- Properly obsolete/provide SOAP-Transport-TCP

* Tue Nov 12 2013 Petr Šabata <contyk@redhat.com> - 1.06-2
- Add a missing, undetected runtime dependency on LWP::UserAgent

* Tue Nov 12 2013 Petr Šabata <contyk@redhat.com> - 1.06-1
- 1.06 bump
- SOAP::Transport::TCP is back
- UDDI::Lite, XML::Parser::Lite, and XMLRPC::Lite are now split from the package

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 0.716-3
- Perl 5.18 rebuild
- Adjust tests for Perl 5.18 (CPAN RT#84168)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.716-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Petr Šabata <contyk@redhat.com> - 0.716-1
- 0.716 bugfix bump
- Fixing historical bogus dates in changelog

* Mon May 06 2013 Petr Pisar <ppisar@redhat.com> - 0.715-4
- Fix sending a large object (bug #960011)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.715-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 02 2012 Petr Šabata <contyk@redhat.com> - 0.715-2
- Bundle 0.714 IO modules to fix dependency breakage
  (confirmed as unintentional by upstream)

* Thu Jul 19 2012 Petr Šabata <contyk@redhat.com> - 0.715-1
- 0.715 bump
- Drop command macros

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 0.714-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.714-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Petr Sabata <contyk@redhat.com> - 0.714-1
- 0.714 bump

* Wed Aug 17 2011 Petr Sabata <contyk@redhat.com> - 0.713-1
- 0.713 bump
- Drop all patches (included upstream)
- Remove now obsolete defattr

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 0.712-8
- RPM 4.9 dependency filtering added
- Add patch for XML::Parser::Lite from rt#68088; perl5.14 fix

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.712-7
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.712-6
- Perl mass rebuild

* Tue May 31 2011 Petr Sabata <contyk@redhat.com> - 0.712-5
- Filter LWP::Protocol from Provides (#709269)

* Tue May 17 2011 Petr Sabata <psabata@redhat.com> - 0.712-4
- Do not require Apache2::*; this introduces mod_perl/httpd dependencies
  This is optional and needed only when running under mod_perl which provides
  those modules. (#705084)
- Use read() instead of sysread() under mod_perl (#663931), mod_perl patch

* Fri Apr  8 2011 Petr Sabata <psabata@redhat.com> - 0.712-3
- BuildArch: noarch

* Wed Apr  6 2011 Petr Sabata <psabata@redhat.com> - 0.712-2
- Fix Requires typos

* Tue Apr  5 2011 Petr Sabata <psabata@redhat.com> - 0.712-1
- 0.712 bump
- Removing clean section
- Removing 'defined hash' patch (included upstream)
- Fixing BRs/Rs; hopefully I didn't omit anything

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.711-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.711-2
- add R: LWP::UserAgent and clean spec from buildroot

* Thu Jun  3 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.711-1
- update and apply fix from https://rt.cpan.org/Public/Bug/Display.html?id=52015

* Thu May 13 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.710.10-4
- BR: perl(version) (Fix perl-5.12.0 build breakdown).

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.710.10-3
- Mass rebuild with perl-5.12.0

* Mon Jan 18 2010 Stepan Kasal <skasal@redhat.com> - 0.710.10-2
- limit BR perl(FCGI) to Fedora

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 0.710.10-1
- new upstream release
- drop upstreamed patch
- add missing build requires
- use %%filter-* macros

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.710.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.710.08-3
- Filter out perl(LWP::Protocol) Provides, which comes from a file
  not stored in Perl's search path for modules (#472359).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.710.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.710.08-1
- New upstream release
- Enable tests
- Include examples in documentation
- Don't grab in dependencies of exotic transports (for the sake
  of consistency with existing practice of Jabber transport)

* Tue Sep 09 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.710.07-2
- Re-add the nil patch

* Tue Jun 24 2008 Mike McGrath <mmcgrath@redhat.com> - 0.710.07-1
- Upstream released new version

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.68-6
- rebuild for new perl

* Thu Oct 18 2007 Mike McGrath <mmcgrath@redhat.com> - 0.68-5
- Fixed build requires

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.68-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Mar 05 2007 Mike McGrath <mmcgrath@redhat.com> - 0.68-4
- bogus reqs diff

* Sat Jan 06 2007 Mike McGrath <imlinux@gmail.com> - 0.68-3
- Changed the way this package removes bogus reqs for EL4

* Sun Sep 10 2006 Mike McGrath <imlinux@gmail.com> - 0.68-1
- Rebuild

* Tue Jul 18 2006 Mike McGrath <imlinux@gmail.com> - 0.68-1
- New upstream source
- Patch provided for <value><nil/></value> issues

* Mon Mar 20 2006 Mike McGrath <imlinux@gmail.com> - 0.67-2
- Removed perl requirements that do not yet exist in Extras

* Sat Mar 18 2006 Mike McGrath <imlinux@gmail.com> - 0.67-1
- New Owner and new spec file

* Wed Oct 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.60a-3
- Fix build, doc permissions (#169821).

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 0.60a-2
- Review suggestions from José Pedro Oliveira

* Fri Mar 18 2005 Hunter Matthews <thm@duke.edu> 0.60a-1
- Initial packaging.

