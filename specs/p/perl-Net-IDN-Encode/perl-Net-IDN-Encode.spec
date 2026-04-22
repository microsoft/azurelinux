# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Net-IDN-Encode
Summary:        Internationalizing Domain Names in Applications (IDNA)
Version:        2.500
Release: 27%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Net-IDN-Encode
Source0:        https://cpan.metacpan.org/authors/id/C/CF/CFAERBER/Net-IDN-Encode-%{version}.tar.gz
# Make Unicode property generator compatible with perl 5.30-RC1,
# CPAN RT#129588, <https://github.com/cfaerber/Net-IDN-Encode/pull/8>
Patch0:         Net-IDN-Encode-2.500-Make-generated-arrays-available-at-compile-time.patch
# Adapt to perl-5.38.0 and stricter GCC, bug #2241714, CPAN RT#149108,
# proposed to an upstream.
Patch1:         Net-IDN-Encode-2.500-use_uvchr_to_utf8_flags_instead_of_uvuni_to_utf8_flags.patch

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  glibc-common
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.5
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(integer)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(open)
# An optional dependency, via Unicode::UCD
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Unicode::Normalize)
BuildRequires:  perl(Unicode::UCD)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)

# This isn't picked up automatically by rpmbuild
Requires:       perl(XSLoader)

%{?perl_default_filter}

%description
This module provides an easy-to-use interface for encoding and decoding
Internationalized Domain Names (IDNs).


%prep
%autosetup -p1 -n Net-IDN-Encode-%{version}

# Remove incorrect executable bits
chmod -x lib/Net/IDN/Encode.pm \
         lib/Net/IDN/Standards.pod

# Convert files to UTF-8
for FILE in LICENSE README; do
  iconv -f ISO_8859-1 -t UTF8 $FILE > $FILE.utf8
  mv $FILE.utf8 $FILE
done


%build
# Makefile.PL is broken, use Build.PL
perl Build.PL installdirs=vendor optimize="%{optflags}"
./Build


%install
./Build install destdir=%{buildroot} create_packlist=0
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*


%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
./Build test


%files
%doc Changes eg README
%license LICENSE
%dir %{perl_vendorarch}/auto/Net
%{perl_vendorarch}/auto/Net/IDN
%dir %{perl_vendorarch}/Net
%{perl_vendorarch}/Net/IDN
%{_mandir}/man3/Net::IDN::*.3pm*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.500-25
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.500-22
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Petr Pisar <ppisar@redhat.com> - 2.500-19
- Adapt to perl-5.38.0 and stricter GCC (bug #2241714)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.500-17
- Perl 5.38 rebuild

* Tue May 09 2023 Michal Josef Špaček <mspacek@redhat.com> - 2.500-16
- Fix patch warning
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.500-13
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.500-10
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.500-7
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.500-4
- Perl 5.30 rebuild

* Fri May 17 2019 Petr Pisar <ppisar@redhat.com> - 2.500-3
- Make Unicode property generator compatible with perl 5.30-RC1
  (CPAN RT#129588)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.500-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 14 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 2.500-1
- Update to 2.500

* Sun Sep 23 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 2.401-1
- Update to 2.401

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.400-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.400-8
- Perl 5.28 rebuild

* Fri Mar 02 2018 Petr Pisar <ppisar@redhat.com> - 2.400-7
- Adapt to removing GCC from a build root (bug #1547165)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.400-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.400-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.400-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.400-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.400-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 08 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.400-1
- Update to 2.400

* Sun Dec 11 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.303-1
- Update to 2.303

* Sun Dec 04 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.301-1
- Update to 2.301

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.300-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.300-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 Petr Šabata <contyk@redhat.com> - 2.300-2
- Prevent FTBFS by correcting the build time dependency list

* Thu Jul 23 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.300-1
- Update to 2.300
- Use %%license tag

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.202-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.202-2
- Perl 5.22 rebuild

* Sat Apr 25 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.202-1
- Update to 2.202

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.201-2
- Perl 5.20 rebuild

* Sun Aug 31 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 2.201-1
- Update to 2.201

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.003-8
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.003-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 2.003-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 2.003-2
- Add missing build requirements.
- Add a requirement left out by rpmbuild.
- Remove the incorrect executable bits.
- Make sure all files are UTF-8 encoded.

* Wed Jan 02 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 2.003-1
- Initial package for Fedora, with help from cpanspec.
