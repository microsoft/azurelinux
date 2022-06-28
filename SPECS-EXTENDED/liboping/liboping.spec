Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           liboping
Version:        1.10.0
Release:        14%{?dist}
Summary:        A C library to generate ICMP echo requests

License:        GPLv2
URL:            https://noping.cc/
Source0:        https://noping.cc/files/%{name}-%{version}.tar.bz2
# Disable -Werror to avoid https://github.com/octo/liboping/issues/38
Patch0:         liboping-1.10.0-no-werror.patch
Patch1:         liboping-1.10-fix-format-ncurses63.patch

BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  ncurses-devel

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Liboping is a C library to generate ICMP echo requests, better known as
"ping packets". It is intended for use in network monitoring applications
or applications that would otherwise need to fork ping(1) frequently.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains files needed to develop and build software against
liboping, a %{summary}.

%prep
%autosetup -p1

%build
%configure --disable-static
make -C src %{?_smp_mflags}
make -C bindings %{?_smp_mflags} perl/Makefile
cd bindings/perl
%{__perl} Makefile.PL INSTALLDIRS=vendor TOP_BUILDDIR=..
%make_build

%install
make -C src install DESTDIR=%{buildroot}
cd bindings/perl
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
LD_LIBRARY_PATH=../../src/.libs make -C bindings/perl test

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog README
%license COPYING
%{_bindir}/oping
%{_bindir}/noping
%{_libdir}/liboping.so.*
%{_mandir}/man8/oping.8*
%{_mandir}/man3/Net::Oping.3pm*
%{perl_vendorarch}/*
%exclude %{_libdir}/liboping.la

%files devel
%{_includedir}/oping.h
%{_libdir}/liboping.so
%{_libdir}/pkgconfig/liboping.pc
%{_mandir}/man3/liboping.3*
%{_mandir}/man3/ping_construct.3*
%{_mandir}/man3/ping_get_error.3*
%{_mandir}/man3/ping_host_add.3*
%{_mandir}/man3/ping_iterator_get.3*
%{_mandir}/man3/ping_iterator_get_context.3*
%{_mandir}/man3/ping_iterator_get_info.3*
%{_mandir}/man3/ping_send.3*
%{_mandir}/man3/ping_setopt.3*

%changelog
* Thu Jun 23 2022 Riken Maharjan <pawelwi@microsoft.com> - 1.10.0-14
- Patch for ncurses6.3 format issue.
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.0-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.10.0-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 1.10.0-8
- Disable -Werror to fix build (see upstream #38)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10.0-6
- Perl 5.28 rebuild

* Mon Jun 18 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.10.0-6
- Update links

* Thu Mar 15 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.10.0-5
- Update BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Fabian Affolter <mail@fabian-affolter.ch> - 1.10.0-1
- Update to latest upstream version 1.10.0 (rhbz#1450029)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.0-3
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.9.0-1
- Update to latest upstream version 1.9.0 (rhbz#1350992)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.0-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.0-2
- Perl 5.22 rebuild

* Fri Nov 21 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.8.0-1
- Update to latest upstream version 1.8.0 (rhbz#1166357)

* Fri Sep 26 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.7.0-1
- Update to latest upstream version 1.7.0 (rhbz#1146892)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 1.6.2-2
- Bulk sad and useless attempt at consistent SPEC file formatting

* Sat Aug 10 2013 Fabian Affolter <mail@fabian-affolter.ch> - 1.6.2-1
- Update to latest upstream version 1.6.2

* Sat Aug 10 2013 Fabian Affolter <mail@fabian-affolter.ch> - 1.6.0-1
- Update to latest upstream version 1.6.0
- Spec file updated

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.5.1-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.5.1-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5.1-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 04 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.5.1-1
- Bump to later version

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.4-2
- Mass rebuild with perl-5.12.0

* Tue Mar 09 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.3.4-1
- Initial packaging
