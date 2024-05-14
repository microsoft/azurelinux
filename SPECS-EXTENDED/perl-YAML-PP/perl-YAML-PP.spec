%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Scalar::Util\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(YAML::PP::Test)\s*$
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

Summary:        YAML 1.2 processor
Name:           perl-YAML-PP
Version:        0.031
Release:        2%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/YAML-PP/
Source0:        https://cpan.metacpan.org/authors/id/T/TI/TINITA/YAML-PP-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.0
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

# Run-time
BuildRequires:  perl(B)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Module::Load)
BuildRequires:  perl(Scalar::Util) >= 1.07
BuildRequires:  perl(Term::ANSIColor) >= 4.02
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Tie::StdArray)
BuildRequires:  perl(Tie::StdHash)
BuildRequires:  perl(base)
BuildRequires:  perl(boolean)
BuildRequires:  perl(constant)
BuildRequires:  perl(overload)

%if 0%{?with_check}
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Tie::IxHash)
BuildRequires:  perl(blib) >= 1.01
BuildRequires:  perl(lib)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B::Deparse)
Requires:       perl(Cpanel::JSON::XS)
Requires:       perl(HTML::Entities)
Requires:       perl(JSON::PP)
Requires:       perl(JSON::XS)
Requires:       perl(Scalar::Util) >= 1.07
Requires:       perl(Term::ANSIColor)
Requires:       perl(Tie::IxHash)
Requires:       perl(YAML::PP::Schema::Include)
Requires:       perl(boolean)
# bin/yamlpp-load can use various YAML implementations on user's request:
Suggests:       perl(YAML)
Suggests:       perl(YAML::PP::LibYAML)
Suggests:       perl(YAML::PP::LibYAML::Parser)
Suggests:       perl(YAML::Syck)
Suggests:       perl(YAML::Tiny)
Suggests:       perl(YAML::XS)

%description
YAML::PP is a modern, modular YAML processor.
It aims to support YAML 1.2 and YAML 1.1. See https://yaml.org/.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n YAML-PP-%{version}

for i in $(find e* -type f); do
    chmod -x "$i"
    perl -i -MConfig -pe 's{\A#!.*perl}{$Config{startperl}}' "$i"
done

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t examples ext %{buildroot}%{_libexecdir}/%{name}
perl -i -pe 's{\$Bin/data/simple-out.yaml}{/tmp/simple-out.yaml}' %{buildroot}%{_libexecdir}/%{name}/t/19.file.t
perl -i -pe 's{\$Bin/data/simple.yaml.copy}{/tmp/simple.yaml.copy}' %{buildroot}%{_libexecdir}/%{name}/t/30.legacy.t

# t/00.compile.t examines ./bin
mkdir -p %{buildroot}%{_libexecdir}/%{name}/bin
for F in yamlpp-events yamlpp-highlight yamlpp-load yamlpp-load-dump yamlpp-parse-emit; do
    ln -s %{_bindir}/"$F" %{buildroot}%{_libexecdir}/%{name}/bin
done

cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
%make_build test

%files
%license LICENSE
%doc Changes CONTRIBUTING.md etc examples README.md
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.031-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Mon Jan 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.031-1
- 0.031 bump

* Mon Nov 08 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.030-1
- 0.030 bump

* Mon Oct 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.029-1
- 0.029 bump

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.027-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.027-2
- Perl 5.34 rebuild

* Mon Apr 12 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.027-1
- 0.027 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.026-1
- 0.026 bump

* Mon Sep 07 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.025-1
- 0.025 bump

* Wed Aug 19 2020 Petr Pisar <ppisar@redhat.com> - 0.024-1
- 0.024 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.023-1
- 0.023 bump

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-2
- Perl 5.32 rebuild

* Wed May 06 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-1
- 0.022 bump

* Mon Mar 02 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.021-1
- 0.021 bump

* Tue Feb 18 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.020-1
- 0.020 bump

* Fri Feb 14 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.019-1
- 0.019 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-1
- Specfile autogenerated by cpanspec 1.78.
