Name:           perl-File-Slurp
Version:        9999.29
Release:        3%{?dist}
Summary:        Efficient Reading/Writing of Complete Files
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/File-Slurp
Source0:        https://cpan.metacpan.org/modules/by-module/File/File-Slurp-%{version}.tar.gz#/perl-File-Slurp-%{version}.tar.gz

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

BuildRequires:  %{__perl}
BuildRequires:  %{__make}

BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(re)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

# Tests
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec) >= 3.01
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)

%description
This module provides subs that allow you to read or write entire files with
one simple call. They are designed to be simple to use, have flexible ways
to pass in or get the file contents and to be very efficient. There is also
a sub to read in all the files in a directory other than . and ..

These slurp/spew subs work for files, pipes and sockets, and stdio, 
pseudo-files, and DATA.

%prep
%setup -q -n File-Slurp-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%{__make} %{?_smp_mflags}

%install
%{__make} pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
# For license text(s), see the perl package.
%doc Changes README.md
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 9999.29-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9999.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.29-1
- Update to 9999.29.

* Wed Sep 18 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.28-1
- Update to 9999.28.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9999.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 9999.27-2
- Perl 5.30 rebuild

* Thu Apr 11 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.27-1
- Update to 9999.27.

* Sat Feb 16 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.26-1
- Update to 9999.26.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9999.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 21 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.25-1
- Update to 9999.25.

* Mon Nov 05 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.24-1
- Update to 9999.24.

* Mon Oct 22 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.23-1
- Update to 9999.23.

* Sat Oct 13 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.21-1
- Update to 9999.21.
- Rework BRs.
- Drop xt-test.
- Spec file cosmetics.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9999.19-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 9999.19-20
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9999.19-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9999.19-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 9999.19-17
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9999.19-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 9999.19-15
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9999.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.19-13
- Remove %%defattr.
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 9999.19-11
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 9999.19-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 9999.19-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 9999.19-4
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 9999.19-2
- Perl mass rebuild

* Wed Jun 08 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.19-1
- Upstream update.

* Sun May 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.18-1
- Upstream update.

* Thu Apr 28 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.16-1
- Upstream update.

* Tue Mar 29 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.15-1
- Upstream update.
- Add perl_default_filter.
- Fix encoding of "Changes".
- Spec cleanup.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 9999.13-9
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 9999.13-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 9999.13-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 09 2008 Ralf Corsépius <rc040203@freenet.de> - 9999.13-4
- Re-activate tests.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.13-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.13-2
- disable tests, due to wacky Fedora builders

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.13-1
- go to 9999.13 to fix build failures against perl 5.10.0

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.12-4
- rebuild for new perl

* Sun Sep 02 2007 Ralf Corsépius <rc040203@freenet.de> - 9999.12-3
- Update license tag.
- BR: perl(ExtUtils::MakeMaker).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.12-2
- Mass rebuild.

* Sat Mar 18 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.12-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.11-2
- Rebuild for perl-5.8.8.

* Wed Feb 01 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.11-1
- Upstream update.
- BR perl(Test::Pod), perl(Test::Pod::Coverage).
