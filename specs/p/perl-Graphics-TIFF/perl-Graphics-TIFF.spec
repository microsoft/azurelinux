# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional tests
%{bcond_without perl_Graphics_TIFF_enables_optional_test}

Name:           perl-Graphics-TIFF
Version:        21
Release: 7%{?dist}
Summary:        Perl extension for the LibTIFF library
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Graphics-TIFF
Source0:        https://cpan.metacpan.org/authors/id/R/RA/RATCLIFFE/Graphics-TIFF-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.5
BuildRequires:  perl(Config)
BuildRequires:  perl(English)
BuildRequires:  perl(ExtUtils::Depends)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::PkgConfig)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  pkgconfig(libtiff-4) >= 4.0.3
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More)
%if %{with perl_Graphics_TIFF_enables_optional_test}
# Optional tests:
# ImageMagick for convert executed by t/1.t
BuildRequires:  ImageMagick
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(Image::Magick)
BuildRequires:  perl(Test::Requires)
%endif

%description
The Graphics::TIFF module allows a Perl developer to access TIFF images using
LibTIFF library in a Perlish and object-oriented way.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Graphics_TIFF_enables_optional_test}
# Optional tests:
# ImageMagick for convert executed by t/1.t
Requires:       ImageMagick
Requires:       perl(Image::Magick)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p 1 -n Graphics-TIFF-%{version}
# Delete author tests skipped by default
for F in t/91_critic.t t/92_tiffinfo.t t/93_tiff2pdf.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{\Q'"$F"'\E}' MANIFEST
done
%if !%{with perl_Graphics_TIFF_enables_optional_test}
for F in t/1.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{\Q'"$F"'\E}' MANIFEST
done
%endif
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
%if %{with perl_Graphics_TIFF_enables_optional_test}
cp -a examples %{buildroot}/%{_libexecdir}/%{name}
chmod +x %{buildroot}/%{_libexecdir}/%{name}/examples/*
%endif
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes examples README
%dir %{perl_vendorarch}/auto/Graphics
%{perl_vendorarch}/auto/Graphics/TIFF
%dir %{perl_vendorarch}/Graphics
%{perl_vendorarch}/Graphics/TIFF.pm
%{_mandir}/man3/Graphics::TIFF.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 21-5
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 21-2
- Perl 5.40 rebuild

* Mon May 06 2024 Petr Pisar <ppisar@redhat.com> - 21-1
- 21 version bump

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20-2
- Perl 5.38 rebuild

* Wed Jun 07 2023 Petr Pisar <ppisar@redhat.com> - 20-1
- 20 version bump

* Thu May 18 2023 Petr Pisar <ppisar@redhat.com> - 19-5
- Handle position tags and adapt tests to changes in ImageMagick-7.1.1.8
  (bug #2208278)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Petr Pisar <ppisar@redhat.com> - 19-3
- Convert a License tag to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 08 2022 Petr Pisar <ppisar@redhat.com> - 19-1
- 19 version bump

* Tue Jun 07 2022 Petr Pisar <ppisar@redhat.com> - 18-4
- Adjust to libtiff-4.4.0 (CPAN RT#143153)

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 18-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 01 2021 Petr Pisar <ppisar@redhat.com> - 18-1
- Version 18 bump (bug #2019091)

* Tue Oct 12 2021 Petr Pisar <ppisar@redhat.com> - 17-1
- Version 17 bump (bug #2012875)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Petr Pisar <ppisar@redhat.com> - 16-1
- 16 version bump

* Thu Jun 03 2021 Petr Pisar <ppisar@redhat.com> - 15-1
- 15 version bump
- Make tests subpackage noarch

* Tue Jun 01 2021 Petr Pisar <ppisar@redhat.com> - 14-1
- 14 version bump

* Thu May 27 2021 Petr Pisar <ppisar@redhat.com> - 13-1
- 13 version bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 12-2
- Perl 5.34 rebuild

* Fri Apr 30 2021 Petr Pisar <ppisar@redhat.com> - 12-1
- 12 version bump

* Tue Apr 27 2021 Petr Pisar <ppisar@redhat.com> - 11-1
- 11 version bump

* Tue Apr 27 2021 Petr Pisar <ppisar@redhat.com> - 10-2
- Adjust tests to libtiff-4.3.0 (CPAN RT#135330)

* Mon Apr 12 2021 Petr Pisar <ppisar@redhat.com> - 10-1
- 10 version bump

* Thu Feb 11 2021 Petr Pisar <ppisar@redhat.com> - 9-1
- Version 9 bump

* Wed Feb 10 2021 Petr Pisar <ppisar@redhat.com> - 8-2
- Make tests subpackage architecture specific

* Tue Feb 09 2021 Petr Pisar <ppisar@redhat.com> - 8-1
- Version 8 bump
- Package tests and make them parallel-safe

* Mon Feb 08 2021 Petr Pisar <ppisar@redhat.com> - 7-3
- Adapt tests to libtiff-4.2.0 (CPAN RT#134344)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 29 2020 Petr Pisar <ppisar@redhat.com> - 7-1
- Version 7 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 10 2017 Petr Pisar <ppisar@redhat.com> - 6-1
- Version 6 bump

* Tue Aug 01 2017 Petr Pisar <ppisar@redhat.com> - 5-1
- Version 5 bump

* Fri Jul 28 2017 Petr Pisar <ppisar@redhat.com> 4-1
- Specfile autogenerated by cpanspec 1.78.
