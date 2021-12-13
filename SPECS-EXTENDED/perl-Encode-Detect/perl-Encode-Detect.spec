Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: perl-Encode-Detect
Version: 1.01
Release: 33%{?dist}
Summary: Encode::Encoding subclass that detects the encoding of data

License: MPLv1.1 or GPLv2+ or LGPLv2+
URL: https://metacpan.org/release/Encode-Detect
Source0: https://cpan.metacpan.org/authors/id/J/JG/JGMYERS/Encode-Detect-%{version}.tar.gz#/perl-Encode-Detect-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::CBuilder)
BuildRequires: perl(Module::Build)
BuildRequires: perl(Test::More)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: perl(Encode::Encoding)

%description
This Perl module is an Encode::Encoding subclass that uses
Encode::Detect::Detector to determine the charset of the input data and then
decodes it using the encoder of the detected charset.

%prep
%setup -q -n Encode-Detect-%{version}
cat <<EOF >%{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(base)/d'
EOF
%define __perl_requires %{_builddir}/Encode-Detect-%{version}/%{name}-req
%{__chmod} +x %{__perl_requires}

%build
%{__perl} Build.PL installdirs=vendor optimize="${RPM_OPT_FLAGS}"
./Build

%check
./Build test

%install
%{__rm} -rf "${RPM_BUILD_ROOT}"
./Build install destdir="${RPM_BUILD_ROOT}" create_packlist=0
find "${RPM_BUILD_ROOT}" -type f -name "*.bs" -size 0 -exec %{__rm} -f {} \;
find "${RPM_BUILD_ROOT}" -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} "${RPM_BUILD_ROOT}"/*

%files
%doc Changes LICENSE
%{perl_vendorarch}/auto/Encode
%{perl_vendorarch}/Encode
%{_mandir}/man3/Encode::Detect.3*
%{_mandir}/man3/Encode::Detect::Detector.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.01-33
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-30
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-27
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-23
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-21
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-18
- Perl 5.22 rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.01-17
- Rebuilt for GCC 5 C++11 ABI change

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-16
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.01-12
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 1.01-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.01-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.01-2
- rebuild against perl 5.10.1

* Thu Nov 12 2009 Warren Togami <wtogami@redhat.com> - 1.01-1
- 1.01 (no changes of consequence, only match latest upstream version)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 20 2008 James Ralston <ralston@pobox.com> - 1.00-4
- remove test before rm -rf $RPM_BUILD_ROOT; rpm will prevent badness

* Wed Dec 19 2007 James Ralston <ralston@pobox.com> - 1.00-3
- the "Build test" step requires perl(Test::More) and perl(Data::Dump)

* Thu Oct 11 2007 James Ralston <ralston@pobox.com> - 1.00-2
- adjust static Requires
- filter erroneous auto-generated Requires in %%prep

* Wed Oct 10 2007 James Ralston <ralston@pobox.com> - 1.00-1
- specfile autogenerated by cpanspec 1.73.
