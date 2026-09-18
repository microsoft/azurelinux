# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-File-Remove
Version:	1.61
Release:	10%{?dist}
Summary:	Convenience module for removing files and directories
License:	GPL-1.0-or-later OR Artistic-1.0-Perl

URL:		https://metacpan.org/release/File-Remove
Source0:	https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/File-Remove-%{version}.tar.gz

BuildRequires:	%{__perl}
BuildRequires:	%{__make}

BuildRequires:	perl-generators
BuildRequires:	perl(blib)
BuildRequires:	perl(constant)
BuildRequires:	perl(Cwd) >= 3.29
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec) >= 3.29
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::More) >= 0.42
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)

BuildArch:	noarch

%description
%{summary}

%prep
%setup -q -n File-Remove-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} DESTDIR="$RPM_BUILD_ROOT"
%{_fixperms} "$RPM_BUILD_ROOT"/*

%check
%{__make} test

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.61-3
- Convert license to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.61-1
- Upstream update to 1.61.
- Spec file cosmetics.

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov  2 2020 Tom Callaway <spot@fedoraproject.org> 1.60-1
- update to 1.60

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.58-7
- Perl 5.32 rebuild

* Tue Mar 03 2020 Petr Pisar <ppisar@redhat.com> - 1.58-6
- Build-require blib module for tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.58-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.58-1
- Update to 1.58.
- Modernize spec.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.57-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.57-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.57-2
- Perl 5.24 rebuild

* Mon Apr 25 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.57-1
- Update to 1.57

* Wed Mar 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.56-1
- Update to 1.56.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.55-2
- Modernize spec.

* Thu Jan 14 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.55-1
- Upstream update.
- Reflect upstream URL-having changed.
- Update BRs.
- Spec cosmetics.
- Introduce %%license.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-10
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.52-6
- Perl 5.18 rebuild

* Wed Jan 30 2013 Petr Šabata <contyk@redhat.com> - 1.52-5
- Use the Module::Install provided by upstream (#906007)

* Wed Nov 28 2012 Petr Šabata <contyk@redhat.com> - 1.52-4
- Add missing buildtime deps
- Unbundle Module::Install
- Drop command macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.52-2
- Perl 5.16 rebuild

* Tue Mar 20 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.52-1
- Upstream update.
- Remove File-Remove-1.51.diff.
- BR: perl(File::Spec) >= 3.29.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.51-1
- Upstream update.
- Add File-Remove-1.51.diff/Remove File-Remove-1.50.diff.

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 1.50-2
- Perl mass rebuild

* Sun Jul 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.50-1
- Upstream update.
- Add File-Remove-1.50.diff/Remove File-Remove-1.49.diff.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.49-2
- Perl mass rebuild

* Mon Mar 28 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.49-1
- Upstream update.
- Add File-Remove-1.49.diff/Remove File-Remove-1.46.diff.
- Spec file cleanup.

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46-1
- Upstream update.
- Remove xt-tests's deps (Upstream doesn't want us to test their works).
- Work around rpm-/perl-version conflicts.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.42-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.42-7
- Rebuild with perl-5.12.0.

* Sun May 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.42-6
- Let META.yml require perl 5.006 (Fix perl-5.12.0 build breakdown).
- Revert 2010-05-01 changes.

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.42-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.42-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 10 2008 Ralf Corsepius <rc040203@freenet.de> - 1.42-1
- Upstream update.

* Tue Jun 10 2008 Ralf Corsepius <rc040203@freenet.de> - 1.41-1
- Upstream update.

* Thu Mar 13 2008 Ralf Corsepius <rc040203@freenet.de> - 1.40-1
- Upstream update.

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-7
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-6
- Rebuild for perl 5.10 (again), first pass

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-5
- rebuild normally, second pass

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-4.1
- rebuild, first pass, without TMV, tests

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-4
- rebuild for new perl

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 0.39-3
- Really BR: perl(Test::MinimumVersion).

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 0.39-2
- Add BR: perl(Test::MinimumVersion).

* Tue Nov 20 2007 Ralf Corsépius <rc040203@freenet.de> - 0.39-1
- Upstream update.

* Wed Oct 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.38-1
- Upstream update.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.37-2
- Update license tag.

* Tue Jul 10 2007 Ralf Corsépius <rc040203@freenet.de> - 0.37-1
- Upstream update.

* Mon Jul 02 2007 Ralf Corsépius <rc040203@freenet.de> - 0.36-2
- Increment release due to koji suckage.

* Mon Jul 02 2007 Ralf Corsépius <rc040203@freenet.de> - 0.36-1
- Upsteam update.
- BR: perl(ExtUtils::MakeMaker).
- BR: perl(Test::More).

* Mon Nov 27 2006 Ralf Corsépius <rc040203@freenet.de> - 0.34-1
- Upstream update.
- Fix URL in Source0.

* Fri Nov 03 2006 Ralf Corsépius <rc040203@freenet.de> - 0.33-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.31-3
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.31-2
- Rebuild for perl-5.8.8.

* Wed Jan 11 2006 Ralf Corsepius <rc040203@freenet.de> - 0.31-1
- Upstream update.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 0.30-2
- Change %%summary according to Ville's preference.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 0.30-1
- FE submission.
