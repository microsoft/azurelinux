Name:           perl-HTML-Parser
Summary:        Perl module for parsing HTML
Version:        3.82
Release:        1%{?dist}
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTML-Parser-%{version}.tar.gz#/perl-HTML-Parser-%{version}.tar.gz
URL:            https://metacpan.org/release/HTML-Parser
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(HTML::Tagset) >= 3
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(URI)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(SelectSaver)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
Requires:       perl(HTML::Tagset) >= 3
Requires:       perl(HTTP::Headers)
Requires:       perl(IO::File)
Requires:       perl(URI)

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(HTML::Tagset\\)$

%description
The HTML-Parser module for perl to parse and extract information from
HTML documents, including the HTML::Entities, HTML::HeadParser,
HTML::LinkExtor, HTML::PullParser, and HTML::TokeParser modules.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
 
%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTML-Parser-%{version}
chmod -c a-x eg/*

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 \
                 NO_PERLLOCAL=1
%make_build

%install
%make_install
file=%{buildroot}%{_mandir}/man3/HTML::Entities.3pm
iconv -f iso-8859-1 -t utf-8 <"$file" > "${file}_" && \
    touch -r ${file} ${file}_ && \
    mv -f "${file}_" "$file"
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes README TODO eg/
%{perl_vendorarch}/HTML/
%{perl_vendorarch}/auto/HTML/
%{_mandir}/man3/HTML::*.3pm*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue Mar 26 2024 Sam Meluch <sammeluch@microsoft.com> - 3.82-1
- Upgrade to version 3.82
- Add tests package
* Tue Jul 26 2022 Henry Li <lihl@microsoft.com> - 3.72-23
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.72-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 3.72-21
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-18
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-17
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Petr Pisar <ppisar@redhat.com> - 3.72-14
- Remove tests subpackage

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-13
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-12
- Perl 5.28 rebuild

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-11
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-7
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-1
- 3.72 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.71-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-10
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-9
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-8
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-7
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.71-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Petr Šabata <contyk@redhat.com> - 3.71-2
- Fix the dependency list
- Fix bogus dates in the changelog

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 3.71-2
- Perl 5.18 rebuild

* Mon May 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-1
- 3.71 bump

* Tue Apr 02 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.70-1
- 3.70 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.69-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Petr Šabata <contyk@redhat.com> - 3.69-9
- Fix the dep list
- Modernize the spec a bit

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.69-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.69-7
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 3.69-6
- Perl 5.16 rebuild

* Mon Apr 16 2012 Petr Pisar <ppisar@redhat.com> - 3.69-5
- Exclude HTTP::Headers build-dependency at Perl bootstrap (bug #810223)

* Mon Apr 16 2012 Petr Pisar <ppisar@redhat.com> - 3.69-4
- Revert "Exclude HTTP::Headers dependency at Perl bootstrap"

* Wed Jan 18 2012 Petr Pisar <ppisar@redhat.com> - 3.69-3
- Exclude HTTP::Headers dependency at Perl bootstrap

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Petr Sabata <contyk@redhat.com> - 3.69-1
- 3.69 bump
- Drop Buildroot and defattr, cleanup

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.68-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.68-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 07 2010 Petr Sabata <psabata@redhat.com> - 3.68-1
- Update to the latest upstream release, v3.68

* Wed Sep 01 2010 Petr Sabata <psabata@redhat.com> - 3.67-1
- Update to the latest upstream release, v3.67

* Mon Jul 12 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.66-1
- update

* Fri Jul 09 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.65-1
- and re-add real-name macro back, maintainertool can't handle it

- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (3.65)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- altered br on perl(HTML::Tagset) (3.03, => 3)
- added a new br on perl(Test::More) (version 0)
- added a new br on perl(XSLoader) (version 0)
- altered req on perl(HTML::Tagset) (3.03 => 3)
- added a new req on perl(XSLoader) (version 0)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.64-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 3.64-2
- rebuild against perl 5.10.1

* Mon Nov  2 2009 Stepan Kasal <skasal@redhat.com> - 3.64-1
- new upstream version

* Fri Oct 23 2009 Warren Togami <wtogami@redhat.com> - 3.63-2
- 3.63 CVE-2009-3627

* Thu Sep 17 2009 Warren Togami <wtogami@redhat.com> - 3.62-1
- 3.62

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> - 3.60-1
- update to latest for mojomojo
- filter bad provides (Parser.so)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 16 2008 Marcela Mašláňová <mmaslano@redhat.com> - 3.59-1
- update to the latest version for Padre editor

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.56-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.56-4
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.56-3
- rebuild for new perl

* Wed Aug 29 2007 Robin Norwood <rnorwood@redhat.com> - 3.56-2
- Fix license tag
- update BuildRequires

* Sat Feb  3 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.56-1
- Update to 3.56.
- Brought specfile closer to the Fedora's Perl template.
- Converted specfile to UTF-8 (changelog entries).
- Added examples and doc files.

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 3.55-1.fc6
- Upgrade to 3.55

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.54-1.fc6.1
- rebuild

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 3.54-1
- upgrade to 3.54

* Wed Mar 22 2006 Jason Vas Dias <jvdias@redhat.com> - 3.51-1
- upgrade to 3.51

* Mon Feb 20 2006 Jason Vas Dias <jvdias@redhat.com> - 3.50-1
- upgrade to 3.50

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.48-1.1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.48-1.1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 3.48-1
- rebuild for new perl-5.8.8

* Mon Dec 19 2005 Jason Vas Dias<jvdias@redhat.com> - 3.48-1
- upgrade to 3.48

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 3.46

* Fri Apr  1 2005 Michael Schwendt <mschwendt@users.sf.net> - 3.45-1
- Update to 3.45 plus heavy spec cleanup.

* Wed Mar 30 2005 Warren Togami <wtogami@redhat.com>
- remove brp-compress

* Thu Nov 25 2004 Miloslav Trmac <mitr@redhat.com> - 3.35-7
- Convert man page to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 17 2004 Chip Turner <cturner@redhat.com> 3.35-2
- rebuild for fc1 update

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 3.35-1
- update to 3.35

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when package is removed

* Mon Jun  3 2002 Chip Turner <cturner@redhat.com>
- fix for Makefile.PL sometimes prompting for input

* Wed Mar 27 2002 Chip Turner <cturner@redhat.com>
- update to 3.26, move to vendor_perl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul 19 2001 Crutcher Dunnavant <crutcher@redhat.com> 3.25-2
- imported from mandrake. tweaked man path.

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 3.25-1mdk
- 3.25.

* Wed Jun 20 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.18-3mdk
- Fixed distribution tag.
- Updated Requires.
- Added an option to %%makeinstall.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.18-2mdk
- Rebuild against the latest perl.

* Tue Feb 27 2001 François Pons <fpons@mandrakesoft.com> 3.18-1mdk
- 3.18.

* Tue Jan 30 2001 François Pons <fpons@mandrakesoft.com> 3.15-1mdk
- 3.15.

* Tue Dec 05 2000 François Pons <fpons@mandrakesoft.com> 3.14-1mdk
- 3.14.

* Thu Oct 12 2000 François Pons <fpons@mandrakesoft.com> 3.13-1mdk
- 3.13.

* Tue Aug 29 2000 François Pons <fpons@mandrakesoft.com> 3.11-1mdk
- 3.11.

* Thu Aug 03 2000 François Pons <fpons@mandrakesoft.com> 3.10-2mdk
- macroszifications.
- add doc.

* Tue Jul 18 2000 François Pons <fpons@mandrakesoft.com> 3.10-1mdk
- removed perllocal.pod from files.
- 3.10.

* Tue Jun 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.08-1mdk
- update to 3.08

* Wed May 17 2000 David BAUDENS <baudens@mandrakesoft.com> 3.05-4mdk
- Fix build for i486
- Use %%{_tmppath} for BuildRoot

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 3.05-3mdk
- rebuild, new group, cleanup

* Tue Feb 29 2000 Jean-Michel Dault <jmdault@netrevolution.com> 3.0.5-1mdk
- upgrade to 3.05

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
-updated to 3.02

* Sun Aug 29 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- bzip2'd sources
- updated to 2.23

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated. 
