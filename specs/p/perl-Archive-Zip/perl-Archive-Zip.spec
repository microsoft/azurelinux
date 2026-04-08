# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Archive-Zip
Version:        1.68
Release:        17%{?dist}
Summary:        Perl library for accessing Zip archives
# lib/Archive/Zip/Member.pm:    (GPL-1.0-or-later OR Artistic-1.0-Perl) and Info-ZIP
#                               (The _mapPermissionsToUnix() comments are
#                               copied from Info-ZIP licensed unzip)
# other files:                  GPL-1.0-or-later OR Artistic-1.0-Perl
License:        ( GPL-1.0-or-later OR Artistic-1.0-Perl ) AND Info-ZIP
URL:            https://metacpan.org/release/Archive-Zip
Source0:        https://cpan.metacpan.org/authors/id/P/PH/PHRED/Archive-Zip-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
# For a Git binary patch
BuildRequires:  git-core
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.4
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Seekable)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(File::Spec::Unix)
# IO::Scalar not used
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  unzip
BuildRequires:  zip
Requires:       perl(Exporter)
Requires:       perl(File::Spec) >= 0.80

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec\\)$
# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(common\\)

%description
The Archive::Zip module allows a Perl program to create, manipulate,
read, and write Zip archive files.
Zip archives can be created, or you can read from existing zip files.
Once created, they can be written to files, streams, or strings.
Members can be added, removed, extracted, replaced, rearranged, and
enumerated.  They can also be renamed or have their dates, comments,
or other attributes queried or modified.  Their data can be compressed
or uncompressed as needed.  Members can be created from members in
existing Zip files, or from existing directories, files, or strings.

%package tests
Summary:        Tests for %{name}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       unzip
Requires:       zip

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -S git -n Archive-Zip-%{version}
for F in examples/*.pl; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t examples %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The solution is to
# copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes examples/
%{_bindir}/crc32
%{perl_vendorlib}/Archive/
%{_mandir}/man3/Archive*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 08 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.68-11
- Package tests

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.68-8
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.68-5
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Petr Pisar <ppisar@redhat.com> - 1.68-3
- Remove an unused build-time dependency on Test::MockModule

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.68-2
- Perl 5.32 rebuild

* Fri Mar 13 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.68-1
- 1.68 bump
- Use make_* macros

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.67-1
- 1.67 bump

* Tue Sep 17 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.66-1
- 1.66 bump

* Mon Sep 09 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.65-1
- 1.65 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.64-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.64-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 13 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.64-1
- 1.64 bump

* Thu Aug 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.63-1
- 1.63 bump

* Mon Aug 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.62-1
- 1.62 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Petr Pisar <ppisar@redhat.com> - 1.60-4
- Fix CVE-2018-10860 (a directory and symbolic link traversal) (bug #1596132)

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-1
- 1.60 bump

* Tue Dec 19 2017 Petr Pisar <ppisar@redhat.com> - 1.59-6
- Fix shellbang in examples/selfex.pl documentation (CPAN RT#123913)
- Modernize spec file

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.59-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.59-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Petr Pisar <ppisar@redhat.com> - 1.59-2
- License tag corrected to ((GPL+ or Artistic) and BSD)

* Fri Aug 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.59-1
- 1.59 bump

* Mon Aug 08 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.58-1
- 1.58 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.57-2
- Perl 5.24 rebuild

* Mon Apr 04 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.57-1
- 1.57 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.56-1
- 1.56 bump

* Mon Dec 07 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.55-1
- 1.55 bump

* Fri Sep 25 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.53-1
- 1.53 bump

* Tue Sep 22 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.51-1
- 1.51 bump

* Wed Aug 26 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-1
- 1.50 bump

* Mon Aug 03 2015 Petr Pisar <ppisar@redhat.com> - 1.49-1
- 1.49 bump

* Fri Jun 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.48-1
- 1.48 bump

* Thu Jun 18 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.47-1
- 1.47 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-2
- Perl 5.22 rebuild

* Wed Mar 25 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-1
- 1.46 bump

* Tue Feb 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.45-1
- 1.45 bump

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 1.39-2
- Correct dependencies
- Improve sharpbang fix

* Wed Oct 22 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.39-1
- 1.39 bump

* Wed Sep 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-1
- 1.38 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.37-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.37-1
- 1.37 bump

* Thu Jan 02 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-1
- 1.36 bump

* Tue Dec 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-1
- 1.34 bump

* Fri Nov 22 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-1
- 1.33 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.30-12
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.30-9
- Perl 5.16 rebuild
- Specify all dependencies

* Mon Mar 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.30-8
- 543660 apply patch from rt cpan 54827

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.30-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.30-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.30-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.30-2
- rebuild against perl 5.10.1

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.30-1
- update to 1.30

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 1.23-1
- Update to 1.23.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-5
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-4
- rebuild for new perl

* Thu Aug 23 2007 Robin Norwood <rnorwood@redhat.com> - 1.20-3
- Fix license tag

* Wed Jun 27 2007 Robin Norwood <rnorwood@redhat.com> - 1.20-2
- Resolves: rhbz#226240
- Incorporate changes from Steven Pritchard's package review
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Remove check macro cruft.
- Update build dependencies.
- Package LICENSE.
- BR unzip, zip for better test coverage.

* Tue Jun 05 2007 Robin Norwood <rnorwood@redhat.com> - 1.20-1
- Update to latest CPAN version: 1.20
- Fix broken changelog

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.16-1.2.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias<jvdias@redhat.com> - 1.16-1.2
- rebuilt for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Mon Jul 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Thu Apr 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Aug 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.12-0.fdr.1
- Update to 1.12.

* Tue Jul  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.11-0.fdr.1
- Update to 1.11.
- Bring up to date with current fedora.us Perl spec template.

* Sun Apr 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.10-0.fdr.1
- Update to 1.10.
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).

* Fri Nov 28 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.09-0.fdr.1
- Update to 1.09.

* Wed Oct 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.08-0.fdr.1
- Update to 1.08.

* Tue Oct 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.1
- Update to 1.07.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.06-0.fdr.1
- Update to 1.06.
- Specfile cleanups.

* Sun Jun  8 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.05-0.fdr.1
- First build.
