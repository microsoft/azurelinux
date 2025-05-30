Name: po4a
Version: 0.60
Release: 2%{?dist}
Summary: A tool maintaining translations anywhere
License: GPL+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://po4a.org/

Source0: https://github.com/mquinson/po4a/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: %{_bindir}/xsltproc
BuildRequires: coreutils
BuildRequires: docbook-style-xsl
BuildRequires: findutils
BuildRequires: grep
# Requires a pod2man which supports --utf8
# Seemingly added in perl-5.10.1
BuildRequires: perl-interpreter >= 4:5.10.1
BuildRequires: perl-generators
BuildRequires: perl(lib)
BuildRequires: perl(Encode)
BuildRequires: perl(ExtUtils::Install)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Spec)
BuildRequires: perl(File::stat)
BuildRequires: perl(Module::Build)
BuildRequires: perl(Pod::Man)

# Run-time:
BuildRequires: %{_bindir}/nsgmls
BuildRequires: gettext
BuildRequires: perl(Carp)
BuildRequires: perl(Config)
BuildRequires: perl(Cwd)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(Encode::Guess)
BuildRequires: perl(Exporter)
BuildRequires: perl(Fcntl)
BuildRequires: perl(File::Temp)
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Getopt::Std)
BuildRequires: perl(IO::File)
BuildRequires: perl(Pod::Parser)
BuildRequires: perl(Pod::Usage)
BuildRequires: perl(POSIX)
BuildRequires: perl(SGMLS) >= 1.03ii
BuildRequires: perl(strict)
BuildRequires: perl(subs)
BuildRequires: perl(Time::Local)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)
BuildRequires: perl(I18N::Langinfo)
BuildRequires: perl(Locale::gettext) >= 1.01
BuildRequires: perl(Term::ReadKey)
BuildRequires: perl(Text::WrapI18N)
BuildRequires: perl(Unicode::GCString)

# Required by the tests:
BuildRequires: perl(Test::More)
BuildRequires: perl(YAML::Tiny)


Requires: %{_bindir}/nsgmls
Requires: %{_bindir}/xsltproc
Requires: gettext
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Optional, but package is quite useless without
Requires: perl(Locale::gettext) >= 1.01
# Optional run-time:
Requires: perl(I18N::Langinfo)
Requires: perl(Term::ReadKey)
Requires: perl(Text::WrapI18N)
Requires: perl(Unicode::GCString)

%description
The po4a (po for anything) project goal is to ease translations (and
more interestingly, the maintenance of translations) using gettext
tools on areas where they were not expected like documentation.

%prep
%setup -q

chmod +x scripts/*

# Fix bang path /usr/bin/env perl -> %{_bindir}/perl (RHBZ#987035).
%{__perl} -p -i -e 's,#!\s*/usr/bin/env perl,#!%{_bindir}/perl,' \
  $(find . -type f -executable |
    xargs grep -l "/usr/bin/env perl")

%build
export PO4AFLAGS="-v -v -v"
LANG=C.utf8
%{__perl} ./Build.PL installdirs=vendor
./Build

%install
LANG=C.utf8
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'


%{_fixperms} $RPM_BUILD_ROOT/*

%find_lang %{name}

%check
LANG=C.utf8
./Build test


%files -f %{name}.lang
%doc README* TODO
%license COPYING
%{_bindir}/po4a*
%{_bindir}/msguntypot
%{perl_vendorlib}/Locale
%{_mandir}/man1/po4a*.1*
%{_mandir}/man1/msguntypot.1*
%{_mandir}/man3/Locale::Po4a::*.3*
#{_mandir}/man5/po4a-build.conf*.5*
#{_mandir}/man7/po4a-runtime.7*
%{_mandir}/man7/po4a.7*
%{_mandir}/*/man1/po4a*.1*
%{_mandir}/*/man1/msguntypot.1*
%{_mandir}/*/man3/Locale::Po4a::*.3*
#{_mandir}/*/man5/po4a-build.conf.5*
#{_mandir}/*/man7/po4a-runtime.7*
%{_mandir}/*/man7/po4a.7*

%changelog
* Mon Jan 11 2021 Joe Schmitt <joschmit@microsoft.com> - 0.60-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove texlive dependency

* Sun Jul 26 2020 Sérgio Basto <sergio@serjux.com> - 0.60-1
- Update po4a to 0.60 (#1857579)

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.59.1-2
- Perl 5.32 rebuild

* Mon May 25 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.59.1-1
- Update to 0.59.1 (#1830920)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 26 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.57-1
- Update to 0.57 (#1765793)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 08 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.56-1
- Update to 0.56 (#1718505)

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.54-4
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.54-2
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Mon Sep 24 2018 Sérgio Basto <sergio@serjux.com> - 0.54-1
- Update po4a to 0.54 (#1582687)
- Fix warning "Output of 'msggrep' might be incorrect" with set LANG=en_US.utf8
- Remove HTML test, which does no longer pass

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.52-4
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 02 2017 Sérgio Basto <sergio@serjux.com> - 0.52-2
- Add to Requires all optional run-time perl modules (#1515239)
- Readd Requires of perl-gettext on epel7 since rhbz #1196539 is fixed but RHEL7.4
  also already ships poa4 except in ppc64 see rhbz #1497544

* Sun Aug 27 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 0.52-1
- Update to 0.52 (#1485710)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Sérgio Basto <sergio@serjux.com> - 0.51-1
- Update to 0.51 (#1436674)

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-5
- Perl 5.26 rebuild
- Fix building on Perl without '.' in @INC

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 Sérgio Basto <sergio@serjux.com> - 0.47-1
- Update to 0.47

* Mon Jul 20 2015 Petr Pisar <ppisar@redhat.com> - 0.45-7
- Specify all dependencies

* Wed Jun 17 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.45-6
- Add po4a-0.45-perl-5.22-hacks.diff
  (Address perl-5.22 FTBFS; RHBZ #1230977).
- Add %%license.

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-5
- Perl 5.22 rebuild

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 0.45-4
- Temporary workaround for epel-7 until have perl-gettext in epel-7

* Sat Jan 17 2015 Sérgio Basto <sergio@serjux.com> - 0.45-3
- fix buildrequires for epel7

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-2
- Perl 5.20 rebuild

* Thu Jul 10 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.45-1
- Upstream update.
- Remove 0001-Remove-defined-anachronism.patch,
  po4a-0.44-use-tempfile-correctly.patch.
- Reflect upstream URL having changed.
- Reflect Source0-URL having changed.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug  8 2013 Richard W.M. Jones <rjones@redhat.com> - 0.44-12
- Fix upstream source URL.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.44-11
- Perl 5.18 rebuild

* Tue Jul 30 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.44-10
- Add BR: /usr/share/texlive/texmf-dist/web2c/texmf.cnf.
- Re-enable t/24-tex.t (Cause for breakdown is texlive packing mess).
- Add BR: perl(Unicode::GCString).
- Move shebang fixing into %%build.
- Fix Source0-URL.
- Spec-file cosmetics.

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 0.44-9
- Fix bang path /usr/bin/env perl -> %%{_bindir}/perl (RHBZ#987035).
- Increase verbosity of po4a when building to help diagnose build errors.
- +BR Pod::Parser.
- Disable 24-tex.t which does not run and does not produce any
  useful diagnostics either.

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.44-2
- Perl 5.18 rebuild

* Wed Apr 17 2013 Richard W.M. Jones <rjones@redhat.com> - 0.44-1
- New upstream version 0.44.
- Fix incorrect use of File::Temp->tempfile (RHBZ#953066).
- Tidy up the spec file.
- po4a-build.conf.5 and po4a-runtime.7 man pages are no longer
  installed in the English version for some (unknown) reason.

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.42-3
- Add 0001-Remove-defined-anachronism.patch.
- Modernize spec.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.42-1
- Upstream update.

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.41-5
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.41-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.41-1
- Upstream update.
- Reflect upstream having changed to Module::Build.
- Remove po4a-0.40.1.diff.

* Fri Oct 15 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.40.1-1
- Upstream update.
- Add po4a-v0.40.1.diff (add missing file t/compare-po.pl)
- Make testsuite working.
- Spec overhaul.
- Eliminate /usr/bin/env perl.
- Require perl >= 5.10.1

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.35-15
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.35-14
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.35-11
- Update to 0.35.

* Tue Jan 13 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.34-10
- Add BuildRequires: perl(Test::More), BuildRequires: docbook-dtds.
- Activate tests.
- Fix Source0:-URL.
- Spec file cosmetics.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.34-9
- Update to 0.34.

* Sun Jun 01 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-8
- Let package own %%{perl_vendorlib}/Locale (BZ 449258).

* Thu May 22 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-7
- Remove || : in %%check due to rpm not accepting it anymore.

* Thu May 22 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-6
- Add: "Requires: perl(:MODULE_COMPAT_...)" (BZ 442548).

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.32-5
- fix license tag

* Mon Aug 20 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.32-4
- Update to 0.32.
- fixes a possible race condition under /tmp (no CVE yet).

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.29-3
- Update to 0.29.

* Sat Feb 18 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

