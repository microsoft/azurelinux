# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MooseX-Types-Common 
Summary:        A library of commonly used type constraints 
Version:        0.001015
Release: 3%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl 
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/MooseX-Types-Common-%{version}.tar.gz
URL:            https://metacpan.org/release/MooseX-Types-Common
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8
BuildRequires:  perl(Config)
BuildRequires:  perl(Module::Build::Tiny)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(if)
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(MooseX::Types::Moose)
# With MooseX::Types >= 0.42
BuildRequires:  perl(namespace::autoclean)
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(open)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Warnings) >= 0.005
BuildRequires:  perl(utf8)
# With MooseX::Types >= 0.42
Requires:       perl(namespace::autoclean)

%{?perl_default_filter}

%description
A set of commonly-used type constraints that do not ship with Moose
by default.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(URI::URL)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n MooseX-Types-Common-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
PERL_MM_FALLBACK_SILENCE_WARNING=1 perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=$RPM_BUILD_ROOT --create_packlist=0
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset AUTHOR_TESTING
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset AUTHOR_TESTING
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
./Build test

%files
%doc README Changes
%license LICENSE
%{perl_vendorlib}/MooseX*
%{_mandir}/man3/MooseX*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.001015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Apr 20 2025 Emmanuel Seyman <emmanuel@seyman.fr> - 0.001015-1
- Update to 0.001015

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 06 2024 Miroslav Suchý <msuchy@redhat.com> - 0.001014-27
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.001014-20
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Petr Pisar <ppisar@redhat.com> - 0.001014-18
- Package the tests

* Thu Jan 06 2022 Petr Pisar <ppisar@redhat.com> - 0.001014-17
- Specify all dependencies

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.001014-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.001014-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.001014-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.001014-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.001014-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.001014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 22 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.001014-1
- Update to 0.001014

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 23 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.001013-4
- Add perl(open) as a BuildRequires (#1234735)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001013-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-2
- Perl 5.22 rebuild

* Sun Mar 29 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.001013-1
- Update to 0.001013

* Thu Nov 13 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.001012-1
- Update to 0.001012
- Tighten file listing
- Drop obsoletes for test sub-package
- Use %%license tag


* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.001008-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.001008-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.001008-2
- Perl 5.16 rebuild

* Sun Jun 17 2012 Iain Arnell <iarnell@gmail.com> 0.001008-1
- update to latest upstream version
- BR inc::Module::Install instead of EU::MM

* Sun Feb 26 2012 Iain Arnell <iarnell@gmail.com> 0.001007-1
- update to latest upstream version
- drop Test::Exception build requirement again

* Thu Feb 23 2012 Iain Arnell <iarnell@gmail.com> 0.001006-1
- update to latest upstream version

* Tue Feb 21 2012 Iain Arnell <iarnell@gmail.com> 0.001005-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.001004-2
- drop tests subpackage; move tests to main package documentation

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.001004-1
- update to latest upstream version
- remove unnecessary explicit requires

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.001003-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- BR Capture::Tiny for improved test coverage

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.001002-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.001002-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.001002-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.001002-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.001002)
- added a new req on perl(Moose) (version 0.39)
- added a new req on perl(MooseX::Types) (version 0.04)

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.001001-1
- submission

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.001001-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
