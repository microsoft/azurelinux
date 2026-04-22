# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Test-CheckManifest
Version:        1.43
Release: 8%{?dist}
Summary:        Check if your Manifest matches your distro
License:        Artistic-2.0
URL:            https://metacpan.org/release/Test-CheckManifest
Source0:        https://cpan.metacpan.org/authors/id/R/RE/RENEEB/Test-CheckManifest-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{__perl}
BuildRequires:  %{__make}

BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd) >= 3.75
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

BuildRequires:  perl(CPAN::Meta::YAML)
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08


%description
This package checks whether the Manifest file matches the distro or not. To
match a distro the Manifest has to name all files that come along with the
distribution.

%prep
# Unpackage tarball in a subdirectory, otherwise the testsuite will fail.
%setup -q -c -n %{name}-%{version}
%setup -q -T -D -n %{name}-%{version} -a0

%if ("%{version}" == "1.42") || ("%{version}" == "1.43")
cd Test-CheckManifest-%{version}
# Bogus deps
sed -i -e '/Data::Dumper/d' META.json META.yml Makefile.PL
cd ..
%endif

%build
cd Test-CheckManifest-%{version}
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
cd ..

%install
cd Test-CheckManifest-%{version}
%{make_install}

%{_fixperms} $RPM_BUILD_ROOT/*
cd ..

%check
cd Test-CheckManifest-%{version}
%{__make} test
cd ..

%files
%doc Test-CheckManifest-%{version}/Changes Test-CheckManifest-%{version}/README
%license Test-CheckManifest-%{version}/LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 06 2023 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.43-1
- Update to 1.43.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.42-13
- Modernize spec.
- Convert license to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-11
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-8
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-2
- Perl 5.30 rebuild

* Tue Mar 05 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.42-1
- Update to 1.42.
- Add BR: perl(File::Path), perl(IO::File).

* Thu Feb 21 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.41-1
- Update to 1.41.

* Sun Feb 17 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.39-1
- Update to 1.39.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.33-1
- Update to 1.33.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-2
- Perl 5.26 rebuild

* Mon Apr 24 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.31-1
- Update to 1.31.
- Add BR: perl(CPAN::Meta::YAML).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-4
- Remove %%defattr.
- Modernize spec.
- Add %%license.
- Add more BR:s.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-2
- Perl 5.22 rebuild

* Thu Jan 08 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-1
- Upstream update.

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.28-1
- Upstream update.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.26-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.26-1
- Upstream update.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.25-2
- Perl 5.16 rebuild

* Sun Feb 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.25-1
- Upstream update.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.24-2
- Perl mass rebuild

* Sun Apr 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.24-1
- Upstream update.

* Tue Mar 29 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.23-1
- Upstream update.
- Add LICENSE file.
- Spec cleanup.

* Tue Mar 01 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.22-2
- Extend %%description upon reviewer's request.

* Sat Feb 05 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.22-1
- Initial Fedora package.
