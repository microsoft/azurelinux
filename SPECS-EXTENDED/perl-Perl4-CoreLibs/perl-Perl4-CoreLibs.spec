Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Perl4-CoreLibs
Version:        0.005
Release:        6%{?dist}
Summary:        Libraries historically supplied with Perl 4
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Perl4-CoreLibs
Source0:        https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM/Perl4-CoreLibs-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
# Call in chat2.pl
BuildRequires:  hostname
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Module::Build) >= 0.26
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time:
# File::Find not used at tests
BuildRequires:  perl(IPC::Open2)
BuildRequires:  perl(IPC::Open3)
# Prefer Socket over socket.ph
# Socket not used at tests
BuildRequires:  perl(Sys::Syslog) => 0.19
BuildRequires:  perl(Text::ParseWords) >= 3.25
BuildRequires:  perl(Time::Local)
# warnings::register not used at tests
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(newgetopt.pl)
BuildRequires:  perl(Test::More)
Requires:       hostname
Requires:       perl(File::Find)
Requires:       perl(IPC::Open2)
Requires:       perl(IPC::Open3)
Requires:       perl(Socket)
Requires:       perl(Sys::Syslog) => 0.19
Requires:       perl(Text::ParseWords) >= 3.25
Requires:       perl(Time::Local)
Requires:       perl(warnings::register)
# Dependencies on these Perl 4 files are generated as perl(foo.pl):
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:       perl(abbrev.pl) = %{version}
Provides:       perl(assert.pl) = %{version}
Provides:       perl(bigfloat.pl) = %{version}
Provides:       perl(bigint.pl) = %{version}
Provides:       perl(bigrat.pl) = %{version}
Provides:       perl(cacheout.pl) = %{version}
Provides:       perl(chat2.pl) = %{version}
Provides:       perl(complete.pl) = %{version}
Provides:       perl(ctime.pl) = %{version}
Provides:       perl(dotsh.pl) = %{version}
Provides:       perl(exceptions.pl) = %{version}
Provides:       perl(fastcwd.pl) = %{version}
Provides:       perl(finddepth.pl) = %{version}
Provides:       perl(find.pl) = %{version}
Provides:       perl(flush.pl) = %{version}
Provides:       perl(ftp.pl) = %{version}
Provides:       perl(getcwd.pl) = %{version}
Provides:       perl(getopt.pl) = %{version}
Provides:       perl(getopts.pl) = %{version}
Provides:       perl(hostname.pl) = %{version}
Provides:       perl(importenv.pl) = %{version}
Provides:       perl(look.pl) = %{version}
# newgetopt.pl is distributed by Getopt-Long, CPAN RT#102212
Provides:       perl(open2.pl) = %{version}
Provides:       perl(open3.pl) = %{version}
Provides:       perl(pwd.pl) = %{version}
Provides:       perl(shellwords.pl) = %{version}
Provides:       perl(stat.pl) = %{version}
Provides:       perl(syslog.pl) = %{version}
Provides:       perl(tainted.pl) = %{version}
Provides:       perl(termcap.pl) = %{version}
Provides:       perl(timelocal.pl) = %{version}
Provides:       perl(validate.pl) = %{version}

%description
This is a collection of .pl files that have historically been bundled with the
Perl core and were removed from perl 5.16.  These files should not be used by
new code.  Functionally, most have been directly superseded by modules in the
Perl 5 style. This collection exists to support old Perl programs that
predates satisfactory replacements.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Perl4-CoreLibs-%{version}
# newgetopt.pl is distributed by Getopt-Long, CPAN RT#102212
rm lib/newgetopt.pl
sed -i -e '/^lib\/newgetopt\.pl/d' MANIFEST
%build
perl Build.PL installdirs=vendor
./Build
# Help generators to recognize Perl scripts
for F in $(find t/ -name '*.t'); do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%install
./Build install destdir=%{buildroot} create_packlist=0
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove author tests
rm -f %{buildroot}%{_libexecdir}/%{name}/t/pod*
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)" -r
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue May 13 2025 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 0.005-6
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 14 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.005-1
- 0.005 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 15 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.004-19
- Package tests
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-17
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-14
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-11
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Petr Pisar <ppisar@redhat.com> - 0.004-9
- Adjust tests to pass 4-digit years to Time::Local (CPAN RT#131341)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-7
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Petr Pisar <ppisar@redhat.com> - 0.004-5
- Require perl(newgetopt.pl) for tests

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jul 31 2017 Petr Pisar <ppisar@redhat.com> - 0.004-1
- 0.004 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-2
- Perl 5.22 rebuild

* Thu Feb 19 2015 Petr Pisar <ppisar@redhat.com> 0.003-1
- Specfile autogenerated by cpanspec 1.78.
- Do not build-require File::Find, Socket, and warnings::register which are
  not exercised by tests
- Sort provides by English rules
