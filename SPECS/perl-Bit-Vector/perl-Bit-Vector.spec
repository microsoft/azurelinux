# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Bit-Vector
Version:        7.4
Release:        39%{?dist}
Summary:        Efficient bit vector, set of integers and "big int" math library
# Outdated FSF address reported, rt#85827
# Clarified by a private mail from the author:
License:        ( GPL-2.0-or-later OR Artistic-1.0-Perl ) AND LGPL-2.0-or-later
URL:            https://metacpan.org/release/Bit-Vector
Source0:        https://cpan.metacpan.org/authors/id/S/ST/STBEY/Bit-Vector-%{version}.tar.gz
Patch0:         0001-Fix-bool-detection.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Carp::Clan) >= 5.3
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(integer)
BuildRequires:  perl(overload)
BuildRequires:  perl(Storable) >= 2.21
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl(Carp::Clan) >= 5.3
Requires:       perl(Storable) >= 2.21

%{?perl_default_filter}

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Bit::Vector\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Carp::Clan\\)\s*$

%description
Bit::Vector is an efficient C library which allows you to handle bit
vectors, sets (of integers), "big integer arithmetic" and boolean
matrices, all of arbitrary sizes.

The library is efficient (in terms of algorithmic complexity) and
therefore fast (in terms of execution speed) for instance through the
widespread use of divide-and-conquer algorithms.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Bit-Vector-%{version} 
%patch -P0 -p1
chmod -c 644 examples/*.pl
perl -MConfig -pi -e 's|^#!.*perl\b|$Config{startperl}|' \
    examples/{benchmk{1,2,3},primes,SetObject}.pl

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" \
  NO_PERLLOCAL=1 NO_PACKLIST=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -a -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
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
%license Artistic.txt GNU_GPL.txt GNU_LGPL.txt
%doc CHANGES.txt CREDITS.txt README.txt examples/
%{perl_vendorarch}/Bit/
%{perl_vendorarch}/auto/Bit/
%{_mandir}/man3/*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-38
- Perl 5.42 rebuild

* Sat Jan 25 2025 Ralf Corsépius <corsepiu@fedoraproject.org> - 7.4-37
- Add 0001-Fix-bool-detection.patch (F42FTBS, RHBZ#2341020).

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-34
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-30
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-28
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-26
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-23
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-20
- Perl 5.32 rebuild

* Mon Feb 10 2020 Petr Pisar <ppisar@redhat.com> - 7.4-19
- Correct a spelling

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 7.4-18
- Use make_build macro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-12
- Perl 5.28 rebuild

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-11
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-2
- Perl 5.22 rebuild

* Fri Nov 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-1
- 7.4 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 7.3-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 7.3-2
- Perl 5.18 rebuild

* Mon Jun 03 2013 Petr Šabata <contyk@redhat.com> - 7.3-1
- 7.3 bump, 5.18 compatibility changes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 19 2012 Jitka Plesnikova <jplesnik@redhat.com> - 7.2-4
- Use latest version of Bit-Vector-7.2.tar.gz from CPAN

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 7.2-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 7.2-1
- 7.2 bumpity
- Remove command macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  2 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.1-7
- filter *.so library incorectly provided by package
- clean spec file

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.1-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 7.1-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 7.1-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 7.1-2
- rebuild against perl 5.10.1

* Fri Oct  2 2009 Stepan Kasal <skasal@redhat.com> - 7.1-2
- fixed the license tag

* Thu Oct  1 2009 Stepan Kasal <skasal@redhat.com> - 7.1-1
- new upstream release

* Tue Aug  4 2009 Stepan Kasal <skasal@redhat.com> - 6.6-1
- new upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.4-8
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.4-7
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.4-6
- fix license tag, rebuild for new perl

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 6.4-5
- Rebuild for selinux ppc32 issue.

* Fri Jul 06 2007 Robin Norwood <rnorwood@redhat.com> 6.4-4
- Resolves: rhbz#247212
- Fix broken perl_provides script - it was removing both the versioned
  and unversioned Provides: perl(Bit::Vector)

* Sat Jun 30 2007 Steven Pritchard <steve@kspei.com> 6.4-3
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Remove check macro cruft.
- Improve Summary.
- Remove redundant perl build dependency.
- BR ExtUtils::MakeMaker.
- Set OPTIMIZE when we run Makefile.PL, not make.
- BR perl(Carp::Clan) instead of perl-Carp-Clan.
- Remove redundant Carp::Clan dependency.
- Filter unversioned Provides: perl(Bit::Vector)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 6.4-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 6.4-1
- Update to 6.4.
- Bring up to date with current Fedora.Extras perl spec template.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 6.3-1
- update to 6.3

* Wed Jul 16 2003 Elliot Lee <sopwith@redhat.com> 
- Rebuild, remove unpackaged files

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Aug 15 2002 Chip Turner <cturner@redhat.com>
- file list fix for Clan stuff

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 30 2002 cturner@redhat.com
- Specfile autogenerated

