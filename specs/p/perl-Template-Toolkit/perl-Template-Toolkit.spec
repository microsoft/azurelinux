# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Template-Toolkit
Version:        3.102
Release: 5%{?dist}
Summary:        Template processing system
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            http://www.template-toolkit.org/
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/Template-Toolkit-%{version}.tar.gz
# No 225 version available
Source1:        http://tt2.org/download/TT_v224_html_docs.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(AppConfig)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Run-time:
# Not used for tests - perl(Apache::Util)
BuildRequires:  perl(base)
BuildRequires:  perl(CGI) >= 4.11
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(HTML::Entities)
# Prefer Image::Info over Image::Size
BuildRequires:  perl(Image::Info)
BuildRequires:  perl(locale)
BuildRequires:  perl(overload)
BuildRequires:  perl(Pod::POM)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Text::Wrap)
# Tests:
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Tie::StdArray)
BuildRequires:  perl(Tie::StdHash)
BuildRequires:  perl(utf8)
# Apache::Util pulls in mod_perl and httpd, for cmd-line tools using
# Template-Toolkit this is a lot of unnecessary and often unwanted packages
# The code checks for the existence of either Apache::Util or HTML::Entities,
# and the latter is much lighter weight from a dependency footprint.
# https://bugzilla.redhat.com/show_bug.cgi?id=1802358
# Requires:     perl(Apache::Util)
Requires:       perl(Encode)
Requires:       perl(File::Temp)
Requires:       perl(HTML::Entities)
# Prefer Image::Info over Image::Size
Requires:       perl(Image::Info)
Requires:       perl(Math::Trig)
Provides:       perl-Template-Toolkit-examples = %{version}-%{release}
Obsoletes:      perl-Template-Toolkit-examples < 2.22-1

%global __provides_exclude ^perl\\(bytes\\)
%{?perl_default_filter}


%description
The Template Toolkit is a collection of modules which implement a
fast, flexible, powerful and extensible template processing system.
It was originally designed and remains primarily useful for generating
dynamic web content, but it can be used equally well for processing
any other kind of text based documents: HTML, XML, POD, PostScript,
LaTeX, and so on.


%prep
%setup -q -n Template-Toolkit-%{version} -a 1
find lib -type f | xargs chmod -c -x
find TT_v*_html_docs -depth -name .svn -type d -exec rm -rf {} \;
find TT_v*_html_docs -type f -exec chmod -x {} +;

# Convert file to UTF-8
iconv -f iso-8859-1 -t utf-8 -o Changes{.utf8,}
mv Changes{.utf8,}


%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor \
  TT_DBI=n TT_ACCEPT=y NO_PERLLOCAL=1 NO_PACKLIST=1
%make_build OPTIMIZE="%{optflags}"


%install
%make_install \
  TT_PREFIX=%{buildroot}%{_datadir}/tt2
chmod -R u+w %{buildroot}/*
# Nuke buildroot where it hides
sed -i "s|%{buildroot}||g" %{buildroot}%{perl_vendorarch}/Template/Config.pm


%check
make test


%files
%doc Changes README.md TODO TT_v*_html_docs/*
%{_bindir}/tpage
%{_bindir}/ttree
%{perl_vendorarch}/Template.pm
%{perl_vendorarch}/auto/Template
%{perl_vendorarch}/Template
%{_mandir}/man1/tpage.1*
%{_mandir}/man1/ttree.1*
%{_mandir}/man3/Template*.3*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.102-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.102-3
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 30 2024 Xavier Bachelot <xavier@bachelot.org> - 3.102-1
- Update to 3.102 (RHBZ#2295396)
- Convert License to SPDX
- Clean up specfile

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.101-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.101-7
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.101-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.101-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.101-3
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep  1 2022 Tom Callaway <spot@fedoraproject.org> - 3.101-1
- update to 3.101

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.010-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.010-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Tom Callaway <spot@fedoraproject.org> - 3.010-1
- update to 3.010

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.009-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Tom Callaway <spot@fedoraproject.org> - 3.009-1
- update to 3.009

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.008-3
- Perl 5.32 rebuild

* Mon Jun 15 2020 Tom Callaway <spot@fedoraproject.org> - 3.008-2
- drop Requires on Apache::Util (bz1802358)

* Mon Mar 30 2020 Tom Callaway <spot@fedoraproject.org> - 3.008-1
- update to 3.008

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Tom Callaway <spot@fedoraproject.org> - 3.007-1
- update to 3.007

* Fri Jan 17 2020 Tom Callaway <spot@fedoraproject.org> - 3.006-1
- update to 3.006

* Wed Jan 15 2020 Tom Callaway <spot@fedoraproject.org> - 3.005-1
- update to 3.005

* Mon Jan 13 2020 Tom Callaway <spot@fedoraproject.org> - 3.004-1
- update to 3.004

* Tue Jan  7 2020 Tom Callaway <spot@fedoraproject.org> - 3.003-1
- update to 3.003

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-2
- Perl 5.30 rebuild

* Wed May 22 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-1
- 2.29 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-1
- 2.28 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.27-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.27-3
- Rebuild due to bug in RPM (RHBZ #1468476)

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.27-2
- Perl 5.26 rebuild

* Tue Apr 18 2017 Tom Callaway <spot@fedoraproject.org> - 2.27-1
- update to 2.27

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-2
- Perl 5.22 rebuild

* Fri Mar 27 2015 Tom Callaway <spot@fedoraproject.org> - 2.26-1
- update to 2.26

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 2.25-1
- 2.25 bump

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 2.24-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Petr Pisar <ppisar@redhat.com> - 2.24-2
- Remove executable bit from documentation

* Thu Aug 23 2012 Tom Callaway <spot@fedoraproject.org> - 2.24-1
- update to 2.24

* Tue Aug 21 2012 Petr Pisar <ppisar@redhat.com> - 2.22-14
- Correct dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 2.22-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Iain Arnell <iarnell@gmail.com> 2.22-10
- update filtering for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.22-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.22-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.22-6
- Mass rebuild with perl-5.12.0

* Tue Feb  9 2010 Stepan Kasal <skasal@redhat.com> - 2.22-5
- delete the buildroot before install

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.22-4
- use filtering macros

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.22-3
- drop build requirements for TeX; LaTeX support has been removed in 2.14a
- fix the Obsoletes tag

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.22-2
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-1
- update to 2.22
- obsolete examples package, upstream got rid of them

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-1
- update to 2.20

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.19-3
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-2
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-1
- 2.19
- license tag fix
- rebuild for BuildID

* Wed Feb 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-1
- go to 2.18

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.15-2
- bump for fc6

* Mon May 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.15-1
- bump to 2.15
- gd test is gone, don't need to patch anything

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-8
- really resolve bug 173756

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-7
- use proper TT_PREFIX setting everywhere, resolve bug 173756

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-6
- bump for FC-5

* Mon Jul 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-5
- don't need Tie::DBI as a BuildRequires, since we're not running 
  the tests

* Mon Jul 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-4
- put examples in their own subpackage

* Sat Jul  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.14-3
- Filter false positive provides.
- Include template library, switch to %%{_datadir}/tt2.
- Tune build dependencies for full test suite coverage.
- Fix and enable GD tests.
- Include more documentation.
- Fine tune dir ownerships and file permissions.

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.14-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.14-1
- Initial package for Fedora Extras
