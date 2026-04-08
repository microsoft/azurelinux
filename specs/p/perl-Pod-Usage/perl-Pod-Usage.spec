# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Pod-Usage
# Compete with perl.spec's epoch
Epoch:          4
Version:        2.05
Release:        520%{?dist}
Summary:        Print a usage message from embedded POD documentation
# License clarification CPAN RT#102529
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Pod-Usage
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Usage-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# scripts/pod2usage.PL uses Config
BuildRequires:  perl(Config)
# scripts/pod2usage.PL uses Cwd
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# scripts/pod2usage.PL uses File::Basename
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
# Getopt::Long not used, scripts/pod2usage not called
# Pod::Usage executes perldoc from perl-Pod-Perldoc by default
BuildRequires:  perl-Pod-Perldoc
BuildRequires:  perl(Pod::Text) >= 4
# Tests:
BuildRequires:  perl(blib)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Pod::Perldoc) >= 3.28
BuildRequires:  perl(Pod::Text)
BuildRequires:  perl(Test::More) >= 0.6
BuildRequires:  perl(vars)
# Optional tests:
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful
Requires:       perl(File::Spec) >= 0.82
# Pod::Usage executes perldoc from perl-Pod-Perldoc by default
Requires:       perl-Pod-Perldoc
Requires:       perl(Pod::Text) >= 4

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude|%{__requires_exclude}|}^perl\\(File::Spec\\)$
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
pod2usage will print a usage message for the invoking script (using its
embedded POD documentation) and then exit the script with the desired exit
status. The usage message printed may have any one of three levels of
"verboseness": If the verbose level is 0, then only a synopsis is printed.
If the verbose level is 1, then the synopsis is printed along with a
description (if present) of the command line options and arguments. If the
verbose level is 2, then the entire manual page is printed.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Pod::Text)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Pod-Usage-%{version}

# Help generators to recognize Perl scripts
for F in `find t -name *.t -o -name *.pl`; do
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
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
perl -i -pe 's{-Mblib}{}' %{buildroot}%{_libexecdir}/%{name}/t/pod/*
perl -i -pe 's{ \@blib,}{}' %{buildroot}%{_libexecdir}/%{name}/t/pod/pod2usage2.t
mkdir -p %{buildroot}%{_libexecdir}/%{name}/lib/Pod
mkdir -p %{buildroot}%{_libexecdir}/%{name}/scripts
ln -s %{perl_vendorlib}/Pod/Usage.pm %{buildroot}%{_libexecdir}/%{name}/lib/Pod/
ln -s %{_bindir}/pod2usage %{buildroot}%{_libexecdir}/%{name}/scripts/pod2usage.PL
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -r -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.05-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.05-519
- Increase release to favour standalone package

* Mon Mar 31 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.05-1
- 2.05 bump (rhbz#2355944)

* Thu Mar 27 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.04-1
- 2.04 bump (rhbz#2354901)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.03-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.03-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.03-510
- Increase release to favour standalone package

* Wed May 15 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.03-504
- Filter provides from sub-package tests

* Wed Feb 07 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.03-503
- Package tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.03-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.03-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.03-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.03-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.03-2
- Perl 5.36 rebuild

* Sun May 22 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.03-1
- 2.03 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.01-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.01-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.01-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 14 2020 Petr Pisar <ppisar@redhat.com> - 4:2.01-1
- 2.01 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.70-2
- Perl 5.32 rebuild

* Mon Mar 16 2020 Petr Pisar <ppisar@redhat.com> - 4:1.70-1
- 1.70 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.69-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.69-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.69-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.69-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.69-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.69-416
- Increase release to favour standalone package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.69-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.69-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.69-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 24 2016 Petr Pisar <ppisar@redhat.com> - 4:1.69-1
- 1.69 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.68-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Petr Pisar <ppisar@redhat.com> - 4:1.68-1
- 1.68 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:1.67-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.67-2
- Perl 5.22 rebuild

* Mon Mar 02 2015 Petr Pisar <ppisar@redhat.com> - 4:1.67-1
- 1.67 bump

* Mon Feb 23 2015 Petr Pisar <ppisar@redhat.com> - 4:1.66-1
- 1.66 bump

* Mon Feb 16 2015 Petr Pisar <ppisar@redhat.com> - 4:1.65-1
- 1.65 bump

* Thu Nov 13 2014 Petr Pisar <ppisar@redhat.com> - 4:1.64-3
- Compete with perl.spec's epoch (bug #1163490)

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.64-2
- Perl 5.20 rebuild

* Tue Jul 01 2014 Petr Pisar <ppisar@redhat.com> - 1.64-1
- 1.64 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.63-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.63-3
- Link minimal build-root packages against libperl.so explicitly

* Tue Jun 25 2013 Petr Pisar <ppisar@redhat.com> - 1.63-2
- Correct dependencies

* Tue Jun 04 2013 Petr Pisar <ppisar@redhat.com> - 1.63-1
- 1.63 bump

* Tue May 21 2013 Petr Pisar <ppisar@redhat.com> - 1.62-1
- 1.62 bump

* Wed Feb 06 2013 Petr Pisar <ppisar@redhat.com> - 1.61-1
- 1.61 bump

* Mon Feb 04 2013 Petr Pisar <ppisar@redhat.com> 1.60-1
- Specfile autogenerated by cpanspec 1.78.
