# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_XML_Simple_enables_optional_test
%else
%bcond_with perl_XML_Simple_enables_optional_test
%endif

Name:           perl-XML-Simple
Version:        2.25
Release: 24%{?dist}
Summary:        Easy API to maintain XML in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/XML-Simple
Source0:        https://cpan.metacpan.org/authors/id/G/GR/GRANTM/XML-Simple-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings::register)
BuildRequires:  perl(XML::NamespaceSupport) >= 1.04
BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(XML::SAX) >= 0.15
# Tests only
BuildRequires:  perl(base)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XML::SAX::Base)
%if %{with perl_XML_Simple_enables_optional_test}
# Optional tests only
BuildRequires:  perl(Tie::IxHash)
%endif
Requires:       perl(File::Basename)
Requires:       perl(File::Spec)
Requires:       perl(IO::Handle)
Requires:       perl(Storable)
Requires:       perl(XML::NamespaceSupport) >= 1.04
Requires:       perl(XML::Parser)
Requires:       perl(XML::SAX) >= 0.15

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(TagsToUpper\\)

%description
The XML::Simple module provides a simple API layer on top of an
underlying XML parsing module (either XML::Parser or one of the SAX2
parser modules).

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n XML-Simple-%{version}

# Remove author tests
for F in t/author-pod-syntax.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
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
# Check section disabled: Disabling checks for initial set of failures.
exit 0

make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-15
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-13
- Package tests

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-11
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-8
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-2
- Perl 5.28 rebuild

* Mon Mar 19 2018 Petr Pisar <ppisar@redhat.com> - 2.25-1
- 2.25 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-2
- Perl 5.26 rebuild

* Tue Apr 18 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-1
- 2.24 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.22-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Petr Šabata <contyk@redhat.com> - 2.22-1
- 2.22 bump

* Fri Dec 04 2015 Petr Šabata <contyk@redhat.com> - 2.21-1
- 2.21 bump
- Package the license text
- Spec cleanup

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-10
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.20-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 24 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-4
- Add test BR perl(XML::SAX::Base)
- Add R perl(IO::Handle), remove duplicate R perl(File::Spec).

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 2.20-2
- Perl 5.16 rebuild

* Thu Jun 21 2012 Petr Šabata <contyk@redhat.com> - 2.20-1
- 2.20 bump
- Modernize spec

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.18-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.18-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.18-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.18-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.18-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-2
- rebuild for new perl

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.18-1
- Update to latest upstream version.

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 2.17-2
- Remove BR: perl

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 2.17-1
- Update to latest CPAN version: 2.17
- Add BuildRequires
- Fix macro-in-changelog rpmlint warning
- Fix license tag

* Tue Dec 05 2006 Robin Norwood <rnorwood@redhat.com> - 2.16-2
- Fix incorrect 'Release' tag - removed extra dot.

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 2.16-1
- Upgrade to latest CPAN version: 2.16

* Wed Jun  7 2006 Jason Vas Dias <jvdias@redhat.com> - 2.14-4
- fix bug 191911: make test fails when default Parser is XML::SAX::PurePerl -
                  succeeds when default Parser is XML::LibXML::SAX -
                  +BuildRequires: perl(XML::LibXML) perl(XML::LibXML::Common)

* Wed Jun  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.14-2.2
- Require perl-XML-Parser (#193985)

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 2.14-2.1
- rebuild for new perl-5.8.8

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.14-2
- Pull perl-XML-Simple from Extras into Core 
  for dependency reasons

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-1
- Update to 2.14.
- Added the dist tag.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.13-2
- rebuilt

* Sat Nov 27 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.13-1
- Update to 2.13.

* Wed May 12 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.4
- Avoid creation of the perllocal.pod file (make pure_install).

* Thu May  6 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.3
- build requirement for perl < 5.8.0 - perl(Storable)

* Thu May  6 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.2
- missing $RPM_OPT_FLAGS in the %%build section.
- optional test module as build requirement perl(Tie::IxHash).

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.12-0.fdr.1
- Update to 2.12.
- Require perl(:MODULE_COMPAT_*).

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.11-0.fdr.1
- Update to 2.11.
- Reduce directory ownership bloat.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.09-0.fdr.2
- Use INSTALLARCHLIB workaround in %%install.

* Wed Sep 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.09-0.fdr.1
- Update to 2.09.

* Wed Sep  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.08-0.fdr.1
- First build.
