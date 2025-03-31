# Perform optional tests
%bcond_without perl_Locale_Maketext_Gettext_enables_optional_test

Name:           perl-Locale-Maketext-Gettext
Version:        1.32
Release:        12%{?dist}
Summary:        Joins the gettext and Maketext frameworks
# README.md:            GPL+ or Artistic
# t/02-big-endian.t:    "the same terms as Perl" and "the same license as the commonlib package"
#                       (The "commonlib" text is a few-line excerpt.)
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Locale-Maketext-Gettext
Source0:        https://cpan.metacpan.org/authors/id/I/IM/IMACAT/Locale-Maketext-Gettext-%{version}.tar.gz
# Convert getext parameters to maketext parameters (CPAN RT#97771)
Patch0:         gettexttomakettext.patch
BuildArch:      noarch
BuildRequires:  coreutils
# diffutils for cmp
BuildRequires:  diffutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Locale::Maketext)
# Tests:
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(vars)
%if %{with perl_Locale_Maketext_Gettext_enables_optional_test}
# Optional tests:
# Module::Signature not used
# Socket not used
BuildRequires:  perl(Test::Pod) >= 1.00
%endif

# Filter private modules
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(T_L10N

%description
Locale::Maketext::Gettext joins the GNU gettext and Maketext frameworks. It
is a subclass of Locale::Maketext(3) that follows the way GNU gettext
works. It works seamlessly, both in the sense of GNU gettext and Maketext.
As a result, you enjoy both their advantages, and get rid of both their
problems, too.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n Locale-Maketext-Gettext-%{version}
# Remove unsed tests
for F in t/00-signature.t \
%if !%{with perl_Locale_Maketext_Gettext_enables_optional_test}
    t/99-pod.t \
%endif
; do
    rm "$F"
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
done
# Sym-link identical files
if cmp t/locale/C/LC_MESSAGES/test.mo t/locale/en/LC_MESSAGES/test.mo; then
    rm t/locale/en/LC_MESSAGES/test.mo
    ln -s ../../C/LC_MESSAGES/test.mo t/locale/en/LC_MESSAGES/test.mo
fi

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
%if %{with perl_Locale_Maketext_Gettext_enables_optional_test}
    rm %{buildroot}%{_libexecdir}/%{name}/t/99-pod.t
%endif
mkdir -p %{buildroot}%{_libexecdir}/%{name}/blib/script
ln -s \
    $(realpath --relative-to %{buildroot}%{_libexecdir}/%{name}/blib/script \
        %{buildroot}%{_bindir}/maketext) \
    %{buildroot}%{_libexecdir}/%{name}/blib/script/maketext
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# t/12-cache.t and others write into CWD.
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
%license Artistic
%doc Changes README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*
%{_bindir}/maketext
%{_mandir}/man1/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-6
- Perl 5.36 rebuild

* Wed Jan 26 2022 Petr Pisar <ppisar@redhat.com> - 1.32-5
- Modernize the spec file
- Package the tests

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-2
- Perl 5.34 rebuild

* Thu Mar 11 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-1
- 1.32 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-1
- 1.30 bump

* Tue Sep 10 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-1
- 1.29 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Petr Pisar <ppisar@redhat.com> - 1.28-3
- Remove signature test (bug #1260618)

* Wed Aug 26 2015 Petr Šabata <contyk@redhat.com> - 1.28-2
- Disable the signature tests, failing due to the patch

* Thu Aug 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-1
- 1.28 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-17
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-16
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.27-13
- Perl 5.18 rebuild

* Tue Mar 19 2013 Rüdiger Landmann <rlandman@redhat.com> 1.27-12
- Patch properly this time

* Mon Mar 18 2013 Rüdiger Landmann <rlandman@redhat.com> 1.27-11
- Add patch to convert gettext %1 to maketext [_1]

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.27-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.27-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-4
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-3
- Mass rebuild with perl-5.12.0

* Mon Sep 21 2009 Rüdiger Landmann <rlandman@redhat.com> 1.27-2
- added BuildRequires:  perl(Test::More) and BuildRequires:  perl(Test::Pod)

* Mon Sep 07 2009 Rüdiger Landmann <rlandman@redhat.com> 1.27-1
- Specfile autogenerated by cpanspec 1.78.
