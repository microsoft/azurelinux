# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-podlators
Epoch:          1
Version:        6.0.2
Release:        520%{?dist}
Summary:        Format POD source into various output formats
# pod/perlpodstyle.pod:     FSFAP
# other files:              GPL-1.0-or-later OR Artistic-1.0-Perl
## Not in the binary package
# t/data/basic.cap:         FSFAP
# t/data/basic.clr:         FSFAP
# t/data/basic.man:         FSFAP
# t/data/basic.ovr:         FSFAP
# t/data/basic.pod:         FSFAP
# t/data/basic.txt:         FSFAP
# t/data/man/*:             FSFAP
# t/data/snippets/man/uppercase-license:    MIT
# t/data/snippets/README:   FSFAP
# t/docs/pod.t:             MIT
# t/docs/pod-spelling.t:    MIT
# t/docs/spdx-license.t:    MIT
# t/docs/synopsis.t:        MIT
# t/docs/urls.t:            MIT
# t/lib/Test/RRA.pm:        MIT
# t/lib/Test/RRA/Config.pm:         MIT
# t/lib/Test/RRA/ModuleVersion.pm:  MIT
# t/style/minimum-version.t:        MIT
# t/style/module-version.t:         MIT
# t/style/strict.t:         MIT
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND FSFAP
URL:            https://metacpan.org/release/podlators
Source0:        https://cpan.metacpan.org/authors/id/R/RR/RRA/podlators-v%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.10
BuildRequires:  perl(Config)
# Cwd run by PL script in scripts directory
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# File::Basename run by PL script in scripts directory
BuildRequires:  perl(File::Basename)
# File::Spec version declared in lib/Pod/Man.pm comment
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
# Getopt::Long not used at tests
BuildRequires:  perl(parent)
BuildRequires:  perl(PerlIO)
BuildRequires:  perl(Pod::Simple) >= 3.26
# Pod::Usage not used at tests
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Term::Cap)
# Tests:
BuildRequires:  perl(autodie)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Optional tests:
# JSON::PP not used
# Perl::Critic::Utils not used
# Perl6::Slurp not used
BuildRequires:  perl(PerlIO::encoding)
# Test::CPAN::Changes not used
# Test::MinimumVersion not used
# Test::Pod not used
# Test::Spelling not used
# Test::Strict not used
# Test::Synopsis not used
Requires:       perl(File::Basename)
# File::Spec version declared in lib/Pod/Man.pm comment
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(PerlIO)
Requires:       perl(Pod::Simple) >= 3.26
Conflicts:      perl < 4:5.16.1-234

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Simple\\)$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::Podlators\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::RRA.*\\)

%description
This package contains Pod::Man and Pod::Text modules which convert POD input
to *roff source output, suitable for man pages, or plain text.  It also
includes several sub-classes of Pod::Text for formatted output to terminals
with various capabilities.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(PerlIO)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n podlators-v%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
for F in `find %{buildroot}%{_libexecdir}/%{name} -name *.t -o -name *.pm`; do
    perl -i -pe "s{'t', 'tmp'}{'/tmp'}" $F
done
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset AUTHOR_TESTING AUTOMATED_TESTING RELEASE_TESTING
cd %{_libexecdir}/%{name} && exec prove -I . -r -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
unset AUTHOR_TESTING AUTOMATED_TESTING RELEASE_TESTING
make test

%files
%license LICENSE
%doc Changes README THANKS TODO
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.0.2-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.0.2-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.0.2-1
- 6.0.2 bump (rhbz#2297800)

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.01-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.01-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.01-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.01-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.01-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.01-1
- 5.01 bump

* Mon Nov 28 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.00-1
- 5.00 bump
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.14-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.14-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.14-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.14-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.14-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.14-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.14-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.14-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Petr Pisar <ppisar@redhat.com> - 1:4.14-1
- 4.14 bump

* Thu Jan 02 2020 Petr Pisar <ppisar@redhat.com> - 1:4.13-1
- 4.13 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Petr Pisar <ppisar@redhat.com> - 1:4.12-1
- 4.12 bump

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.11-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.11-2
- Perl 5.28 rebuild

* Wed May 09 2018 Petr Pisar <ppisar@redhat.com> - 4.11-1
- 4.11 bump
- License changed to (GPL+ or Artistic) and FSFAP

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 Petr Pisar <ppisar@redhat.com> - 4.10-1
- 4.10 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.09-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.09-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 08 2016 Petr Pisar <ppisar@redhat.com> - 4.09-1
- 4.09 bump

* Mon Sep 26 2016 Petr Pisar <ppisar@redhat.com> - 4.08-1
- 4.08 bump

* Tue Sep 20 2016 Petr Pisar <ppisar@redhat.com> - 4.07-366
- License declaration corrected to "(GPL+ or Artistic) and MIT"

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.07-365
- Increase release to favour standalone package

* Mon Mar 21 2016 Petr Pisar <ppisar@redhat.com> - 4.07-1
- 4.07 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Petr Pisar <ppisar@redhat.com> - 4.06-1
- 4.06 bump

* Mon Jan 18 2016 Petr Pisar <ppisar@redhat.com> - 4.05-1
- 4.05 bump

* Mon Jan 04 2016 Petr Pisar <ppisar@redhat.com> - 4.04-1
- 4.04 bump

* Mon Dec 07 2015 Petr Pisar <ppisar@redhat.com> - 4.03-1
- 4.03 bump

* Thu Dec 03 2015 Petr Pisar <ppisar@redhat.com> - 4.02-1
- 4.02 bump

* Wed Dec 02 2015 Petr Pisar <ppisar@redhat.com> - 4.01-1
- 4.01 bump

* Tue Dec 01 2015 Petr Pisar <ppisar@redhat.com> - 4.00-1
- 4.00 bump

* Wed Jul 15 2015 Petr Pisar <ppisar@redhat.com> - 2.5.3-347
- Adapt tests to Term-Cap-1.16

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.3-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.3-4
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.3-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 08 2013 Petr Pisar <ppisar@redhat.com> - 2.5.3-1
- 2.5.3 bump

* Mon Sep 23 2013 Petr Pisar <ppisar@redhat.com> - 2.5.2-1
- 2.5.2 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.5.1-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.5.1-3
- Link minimal build-root packages against libperl.so explicitly

* Tue Jun 25 2013 Petr Pisar <ppisar@redhat.com> - 2.5.1-2
- Specify all dependencies

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 2.5.1-1
- 2.5.1 bump

* Thu Feb 07 2013 Petr Pisar <ppisar@redhat.com> - 2.5.0-2
- Correct dependencies

* Fri Jan 04 2013 Petr Pisar <ppisar@redhat.com> - 2.5.0-1
- 2.5.0 bump
- This version makes pod2* tools failing if POD syntax error is encountered

* Thu Nov 01 2012 Petr Pisar <ppisar@redhat.com> - 2.4.2-3
- Do not export under-specified dependencies

* Wed Oct 31 2012 Petr Pisar <ppisar@redhat.com> - 2.4.2-2
- Conflict perl-podlators with perl before sub-packaging

* Wed Sep 12 2012 Petr Pisar <ppisar@redhat.com> 2.4.2-1
- Specfile autogenerated by cpanspec 1.78.
