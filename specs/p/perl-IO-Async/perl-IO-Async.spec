# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-IO-Async
Version:        0.804
Release:        3%{?dist}
Summary:        A collection of modules that implement asynchronous filehandle IO

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-Async
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/IO-Async-%{version}.tar.gz

BuildArch:      noarch
# build requirements
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build)
# runtime requirements
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(Future)
BuildRequires:  perl(Future::IO::ImplBase)
BuildRequires:  perl(Future::Utils) >= 0.18
BuildRequires:  perl(Heap::Elem)
BuildRequires:  perl(Heap::Fibonacci)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Poll)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Metrics::Any)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Sereal::Decoder)
BuildRequires:  perl(Sereal::Encoder)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Struct::Dumb)
BuildRequires:  perl(Test2::IPC)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(threads)
BuildRequires:  perl(warnings)
# test requirements
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Future::IO)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Future::IO::Impl)
BuildRequires:  perl(Test::MemoryGrowth)
BuildRequires:  perl(Test::Metrics::Any)
BuildRequires:  perl(lib)
Requires:       perl(threads)
# All five are optional but preferred
Requires:       perl(Heap::Elem)
Requires:       perl(Heap::Fibonacci)
Requires:       perl(IO::Socket::IP)
Requires:       perl(Sereal::Decoder)
Requires:       perl(Sereal::Encoder)

%{?perl_default_filter}

%description
A collection of modules that implement asynchronous filehandle IO

%prep
%setup -q -n IO-Async-%{version}


%build
/usr/bin/perl Build.PL --installdirs=vendor
./Build


%install
./Build install --destdir=$RPM_BUILD_ROOT --create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*


%check
./Build test


%files
%doc Changes examples
%{perl_vendorlib}/Future/IO/Impl/IOAsync.pm
%{perl_vendorlib}/IO*
%{_mandir}/man3/Future::IO::Impl::IOAsync.3pm.gz
%{_mandir}/man3/IO*.3*


%changelog
* Fri Aug 15 2025 Emmanuel Seyman <emmanuel@seyman.fr> - 0.804-3
- Bump to rebuild (#2385391)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.804-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Apr 27 2025 Emmanuel Seyman <emmanuel@seyman.fr> - 0.804-1
- Update to 0.804

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.803-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.803-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Feb 28 2024 Michal Josef Špaček <mspacek@redhat.com> - 0.803-2
- Fix provided files

* Sun Feb 25 2024 Emmanuel Seyman <emmanuel@seyman.fr> - 0.803-1
- Update to 0.803
- Migrate to SPDX license
- Update BuildRequires
- Add examples folder to the documentation

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.802-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.802-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.802-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun May 14 2023 Emmanuel Seyman <emmanuel@seyman.fr> - 0.802-3
- Add perl(Test::Future::IO::Impl) as a BR (#2196755)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.802-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Aug 21 2022 Emmanuel Seyman <emmanuel@seyman.fr> - 0.802-1
- Update to 0.802

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.801-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.801-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.801-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 19 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 0.801-1
- Update to 0.801

* Sun Nov 14 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 0.800-1
- Update to 0.800
- Drop no-longer-needed patch

* Sun Aug 08 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 0.79-1
- Update to 0.79

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.78-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 0.78-1
- Update to 0.78
- Drop upstreamed patch

* Thu Sep 24 2020 Petr Pisar <ppisar@redhat.com> - 0.77-5
- Adapt tests to getaddrinfo() returning EAI_AGAIN in case of an unavailable
  DNS server (bug #1865207)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.77-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.77-2
- Perl 5.32 rebuild

* Sun May 31 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 0.77-1
- Update to 0.77

* Sun May 10 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 0.76-1
- Update to 0.76

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 01 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.75-1
- Update to 0.75
- Replace calls to %/usr/bin/perl with /usr/bin/perl

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.74-1
- Update to 0.74

* Sun Jun 23 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.73-1
- Update to 0.73

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.72-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.72-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.72-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.72-3
- Perl 5.28 rebuild

* Wed Apr 11 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.72-2
- Patch resolver test to add timeout, thanks to ppisar (#1563208)

* Sun Apr 08 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.72-1
- Update to 0.72

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.71-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 25 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.71-1
- Update to 0.71
- Drop no-longer-needed patch

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.70-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.70-1
- Update to 0.70

* Sun Nov 15 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.69-1
- Update to 0.69

* Sun Aug 16 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.68-1
- Update to 0.68
- Disable resolution test for a missing host

* Tue Aug 11 2015 Petr Šabata <contyk@redhat.com> - 0.67-4
- Prevent FTBFS by correcting the build time dependency list

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.67-2
- Perl 5.22 rebuild

* Sun Jun 07 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.67-1
- Update to 0.67

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.66-2
- Perl 5.22 rebuild

* Sun Feb 22 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.65-1
- Update to 0.65

* Sun Nov 02 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.64-1
- Update to 0.64

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.63-2
- Perl 5.20 rebuild

* Sun Jul 20 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.63-1
- Update to 0.63

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 30 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.62-1
- Update to 0.62

* Sun Oct 20 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.61-1
- Update to 0.61

* Sun Sep 22 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.60-1
- Update to 0.60

* Sun Aug 25 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.59-1
- Update to 0.59

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 16 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.58-1
- Update to 0.58
- Add perl default filter
- Remove no-longer-needed macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.29-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.29-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.29-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.29-3
- Add BR perl(Time::HiRes)

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.29-1
- Update to 0.29
- Add Test::Warn BR

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.28-2
- Mass rebuild with perl-5.12.0

* Mon Apr 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.28-1
- Update to 0.28

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-2
- rebuild against perl 5.10.1

* Mon Aug 31 2009 kwizart < kwizart at gmail.com > - 0.23-1
- Update to 0.23

* Tue Aug 11 2009 kwizart < kwizart at gmail.com > - 0.22-2
- Add Missing BR

* Mon Jul 20 2009 kwizart < kwizart at gmail.com > - 0.22-1
- Update to 0.22

* Thu Jul  9 2009 kwizart < kwizart at gmail.com > - 0.21-1
- Initial spec
