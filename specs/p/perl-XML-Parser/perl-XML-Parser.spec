# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-XML-Parser
Version:        2.47
Release: 9%{?dist}
Summary:        Perl module for parsing XML documents

License:        Artistic-2.0
Url:            https://metacpan.org/release/XML-Parser
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-%{version}.tar.gz

# Build
BuildRequires:  coreutils
BuildRequires:  expat-devel
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(Devel::CheckLib) >= 1.16
BuildRequires:  perl(English)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(lib)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
# LWPExternEnt.pl script is loaded by Parser.pm
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::file)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(if)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
Requires:       perl(IO::File)
Requires:       perl(IO::Handle)
Requires:       perl(LWP::UserAgent)
Requires:       perl(URI)
Requires:       perl(URI::file)

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(XML::Parser\\)$

%description
This module provides ways to parse XML documents. It is built on top
of XML::Parser::Expat, which is a lower level interface to James
Clark's expat library. Each call to one of the parsing methods creates
a new instance of XML::Parser::Expat which is then used to parse the
document. Expat options may be provided when the XML::Parser object is
created. These options are then passed on to the Expat object on each
parse call. They can also be given as extra arguments to the parse
methods, in which case they override options given at XML::Parser
creation time.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n XML-Parser-%{version} 
chmod 644 samples/{canonical,xml*}
perl -MConfig -pi -e 's|^#!/usr/local/bin/perl\b|$Config{startperl}|' samples/{canonical,xml*}

# Remove bundled library
rm -r inc
perl -i -ne 'print $_ unless m{^inc/}' MANIFEST

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -delete
%{_fixperms} $RPM_BUILD_ROOT/*

for file in samples/REC-xml-19980210.xml; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
  perl -i -pe "s/encoding='ISO-8859-1'/encoding='UTF-8'/" "$file"
done

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t samples %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
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
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc README Changes samples/
%license LICENSE
%{perl_vendorarch}/XML/
%{perl_vendorarch}/auto/XML/
%{_mandir}/man3/XML::Parser*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.47-7
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.47-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.47-1
- 2.47 bump (rhbz#2256150)

* Wed Sep 20 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-16
- Package tests

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-14
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-11
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-8
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Petr Pisar <ppisar@redhat.com> - 2.46-5
- Modernize a spec file

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-4
- Perl 5.32 rebuild

* Tue Mar 10 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-3
- Specify all dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 24 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-1
- 2.46 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-16
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Petr Pisar <ppisar@redhat.com> - 2.44-14
- Fix a buffer overwrite in parse_stream() with wide characters on the standard
  input (bug #1473368)

* Mon Jul 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-13
- Specify all dependencies

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-11
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-2
- Perl 5.22 rebuild

* Tue Feb 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-1
- 2.44 bump

* Thu Dec 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.43-1
- 2.43 bump
- Updated BRs; Removed bundled Devel::CheckLib

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.41-14
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.41-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.41-8
- Update dependencies and summary
- Remove pre-RPM-4.9 filters
- Remove deleting empty directories
- Update REC-xml-19980210.xml to match new encoding

* Mon Aug 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.41-7
- Specify all dependencies.
- Remove perl(LWP) and perl(URI) from Requires. 
- Update source link. 

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.41-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 2.41-3
- update filtering for rpm 4.9

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.41-2
- Perl mass rebuild

* Fri Jun  3 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.41-1
- update 2.41
- clean spec from rm, clean, deffattr

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 2.40-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.40-1
- update 

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.36-9
- Mass rebuild with perl-5.12.0

* Tue Feb  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.36-8
- rebuild with expat-2.0.1-10 which should fix tests part #549216, #555457

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.36-7
- rebuild against perl 5.10.1

* Mon Aug 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.36-6
- rebuild against perl without DEBUGGING defined

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.36-3
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.36-2
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.36-1
- bump to 2.36

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.34-11
- rebuild for new perl

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.34-10
- Add dist tag to release field
- Fix previous changelog

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 2.34-9
- Remove BR: perl
- fix utf-8 rpmlint warning

* Tue Aug 28 2007 Robin Norwood <rnorwood@redhat.com> - 2.34-8
- Update license tag
- Add README Changes samples/ to %%doc section

* Thu Aug  9 2007 Joe Orton <jorton@redhat.com> - 2.34-7
- BuildRequire perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.34-6.1.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.34-6.1.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.34-6.1.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 2.34-6-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.34-6
- #155619
- Bring up to date with current Fedora.Extras perl spec template.

* Sun Aug 08 2004 Alan Cox <alan@redhat.com> 2.34-5
- runtime requires expat

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Warren Togami <wtogami@redhat.com> 2.34-3
- #110597 BR expat-devel

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 2.34-1
- update to 2.34

* Mon Jan 26 2004 Jeremy Katz <katzj@redhat.com> 2.31-17
- more rebuilding

* Mon Jan 19 2004 Chip Turner <cturner@redhat.com> 2.31-16
- rebuild for newer perl

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when
  package is removed

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 
