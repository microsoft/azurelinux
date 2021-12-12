# Utilize xdg-user-dirs
%{bcond_with perl_File_BaseDir_enables_xdg_user_dirs}
Name:           perl-File-BaseDir
Version:        0.08
Release:        9%{?dist}
Summary:        Use the Freedesktop.org base directory specification
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/File-BaseDir
Source0:        https://cpan.metacpan.org/authors/id/K/KI/KIMRYAN/File-BaseDir-%{version}.tar.gz#/perl-File-BaseDir-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::Build::Compat) >= 0.02
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IPC::System::Simple)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Optional run-time:
%if %{with perl_File_BaseDir_enables_xdg_user_dirs}
BuildRequires:  xdg-user-dirs
%endif
# Tests
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(File::Which)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module can be used to find directories and files as specified by the
Freedesktop.org Base Directory Specification. This specifications gives a
mechanism to locate directories for configuration, application data and
cache data. It is suggested that desktop applications for e.g. the Gnome,
KDE or Xfce platforms follow this layout. However, the same layout can just
as well be used for non-GUI applications.

%if %{with perl_File_BaseDir_enables_xdg_user_dirs}
%package -n perl-File-UserDirs
Summary:        Find extra media and documents Freedesktop.org directories
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# This package does not make sense without xdg-user-dirs
Requires:       xdg-user-dirs
Conflicts:      %{name} < 0.06-2

%description -n perl-File-UserDirs
File::UserDirs Perl module can be used to find directories as informally
specified by the Freedesktop.org xdg-user-dirs software. This gives
a mechanism to locate extra directories for media and documents files.
%endif


%prep
%setup -q -n File-BaseDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/File/UserDirs.pm
%{_mandir}/man3/*
%exclude %{_mandir}/man3/File::UserDirs.3pm.gz

%if %{with perl_File_BaseDir_enables_xdg_user_dirs}
%files -n perl-File-UserDirs
%doc Changes README
%dir %{perl_vendorlib}/File
%{perl_vendorlib}/File/UserDirs.pm
%{_mandir}/man3/File::UserDirs.3pm.gz
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.08-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Oct 22 2020 Joe Schmitt <joschmit@micrsoft.com> - 0.08-8
- Disable perl_File_BaseDir_enables_xdg_user_dirs by default.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-2
- Perl 5.28 rebuild

* Tue Mar 13 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-1
- 0.08 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-2
- Perl 5.22 rebuild

* Tue Apr 21 2015 Petr Pisar <ppisar@redhat.com> - 0.07-1
- 0.07 bump

* Tue Apr 21 2015 Petr Pisar <ppisar@redhat.com> - 0.06-2
- Sub-package File::UserDirs

* Tue Apr 07 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-1
- 0.06 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.03-18
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.03-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.03-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.03-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-7
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.03-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.03-2
- rebuild for new perl

* Thu Nov 22 2007 Patrice Dumas <pertusus@free.fr> 0.03-1
- update to 0.03 (#396071)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.02-1.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.02-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Oct 11 2006 Patrice Dumas <pertusus@free.fr> 0.02-1
- Specfile autogenerated by cpanspec 1.69.
