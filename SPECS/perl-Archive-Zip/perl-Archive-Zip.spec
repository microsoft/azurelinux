Name:           perl-Archive-Zip
Version:        1.68
Release:        1%{?dist}
Summary:        Perl library for accessing Zip archives
# lib/Archive/Zip/Member.pm:    (GPL+ or Artistic) and BSD
#                               (The _mapPermissionsToUnix() comments are
#                               copied from BSD-licensed unzip)
# other files:                  GPL+ or Artistic
License:        (GPL+ or Artistic) and BSD
URL:            https://metacpan.org/release/Archive-Zip
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://cpan.metacpan.org/authors/id/P/PH/PHRED/Archive-Zip-%{version}.tar.gz
BuildArch:      noarch
# For a Git binary patch
BuildRequires:  git-core
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
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

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Exporter)
Requires:       perl(File::Spec) >= 0.80

Provides:       perl-Archive-Zip = %{version}-%{release}
Provides:       perl(Archive::Zip) = %{version}-%{release}
Provides:       perl(Archive::Zip::Archive) = %{version}-%{release}
Provides:       perl(Archive::Zip::BufferedFileHandle) = %{version}-%{release}
Provides:       perl(Archive::Zip::DirectoryMember) = %{version}-%{release}
Provides:       perl(Archive::Zip::FileMember) = %{version}-%{release}
Provides:       perl(Archive::Zip::Member) = %{version}-%{release}
Provides:       perl(Archive::Zip::MemberRead) = %{version}-%{release}
Provides:       perl(Archive::Zip::MockFileHandle) = %{version}-%{release}
Provides:       perl(Archive::Zip::NewFileMember) = %{version}-%{release}
Provides:       perl(Archive::Zip::StringMember) = %{version}-%{release}
Provides:       perl(Archive::Zip::Tree) = %{version}-%{release}
Provides:       perl(Archive::Zip::ZipFileMember) = %{version}-%{release}

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec\\)$

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


%prep
%autosetup -S git -n Archive-Zip-%{version}
for F in examples/*.pl; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done


%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}


%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*


%files
%license README.md
%doc Changes examples/
%{_bindir}/crc32
%{perl_vendorlib}/Archive/
%{_mandir}/man3/Archive*.3*


%changelog
* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.68-1
- Update to 1.68

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.67-4
- Adding 'BuildRequires: perl-generators'.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.67-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Explicitly provide perl(Archive::*).
- Use README.me as the %%license as it mentions the perl license applies to this package.
- Remove test build requirements.
- Remove double condition on BuildRequires: perl(:VERSION).
- License verified.

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
