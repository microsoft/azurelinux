Summary:        Wrapper for the libev high-performance event loop library
Name:           perl-EV
Version:        4.34
Release:        1%{?dist}
# Note: The source archive includes a libev/ folder which contents are licensed
#       as "BSD or GPLv2+". However, those are removed at build-time and
#       perl-EV is instead built against the system-provided libev.
License:        GPL-1.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/EV
Source0:        https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/EV-%{version}.tar.gz
Patch0:         perl-EV-4.03-Don-t-ask-questions-at-build-time.patch
Patch1:         perl-EV-4.30-Don-t-check-bundled-libev.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(common::sense)
BuildRequires:  gdbm-devel
BuildRequires:  libev-source >= 4.33
BuildRequires:  perl(AnyEvent) => 2.6
BuildRequires:  perl(Canary::Stability)

# We remove the upstream bundled libev, but still build against statically
# linked files from the libev-source package.
Provides:       bundled(libev)

%{?perl_default_filter}

%description
This module provides an interface to libev
(<http://software.schmorp.de/pkg/libev.html>). While the included documentation
is comprehensive, one might also consult the documentation of libev itself
(<http://cvs.schmorp.de/libev/ev.html>) for more subtle details on watcher
semantics or some discussion on the available backends, or how to force a
specific backend with "LIBEV_FLAGS", or just about in any case because it has
much more detailed information.

%prep
%setup -q -n EV-%{version}

%patch -P0 -p1
%patch -P1 -p0

# remove all traces of the bundled libev
rm -fr ./libev

# use the sources from the system libev
mkdir -p ./libev
cp -r /usr/share/libev-source/* ./libev/

%build
PERL_CANARY_STABILITY_NOPROMPT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

%check
%make_build test

%files
%license COPYING
%doc Changes README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/EV*.3pm*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 4.34-1
- Update to version 4.34
- License verified

* Thu Jan 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.33-8
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.33-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.33-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 15 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 4.33-4
- Replace "make pure_install" with %%{make_install}
- Replace calls to make with %%{make_build}

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.33-2
- Perl 5.32 rebuild

* Sun Mar 22 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 4.33-1
- Update to 4.33

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 12 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 4.31-1
- Update to 4.31

* Sun Nov 24 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 4.30-1
- Update to 4.30
- Replace calls to %%{__perl} with /usr/bin/perl
- Patch Makefile.PLL to not check for bundled EV library

* Tue Jul 30 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 4.27-1
- Update to 4.27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.25-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 23 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 4.25-1
- Update to 4.25

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.22-10
- Perl 5.28 rebuild

* Thu Mar  1 2018 Florian Weimer <fweimer@redhat.com> - 4.22-9
- Rebuild with new redhat-rpm-config/perl build flags

* Mon Feb 26 2018 Carl George <carl@george.computer> - 4.22-8
- Add BuildRequires for gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.22-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.22-2
- Perl 5.24 rebuild

* Wed Mar 23 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 4.22-1
- Update to 4.22

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 18 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 4.21-1
- Update to 4.21

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.18-5
- Perl 5.22 rebuild

* Tue Sep 30 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 4.18-4
- Bump to rebuild against libev-source 4.19

* Sun Sep 14 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.18-3
- Bump to rebuild against libev-source 4.18

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.18-2
- Perl 5.20 rebuild

* Sat Sep 06 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.18-1
- Update to 4.18

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.17-3
- Perl 5.20 rebuild

* Wed Sep 03 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.17-2
- Downgrade requirement of libev-source to 4.15
- Truncate RPM Changelog to the 4.xx

* Sun Aug 31 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.17-1
- Update to 4.17

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.11-7
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 4.11-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 28 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 4.11-1
- Update to 4.11

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 4.03-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Petr Pisar <ppisar@redhat.com> - 4.03-7
- Build-require exact or higher version of libev-source (bug #759021)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.03-6
- Perl mass rebuild

* Tue Apr 12 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-5
- Add the correct Obsoletes/Provides to avoid broken deps from the -devel
  subpackage removal.

* Thu Apr 07 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-4
- Readded the header file to the main package, as per guidelines:
      -> http://fedoraproject.org/wiki/Packaging/Perl#.h_files_in_module_packages

* Tue Mar 08 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-3
- Some more fixes as part of the review process:
  - Fix the license tag to be only the license of perl-EV, and add a note about
    the included libev sources.
- Removed manual cleaning of the buildroot since it has been useless since
  Fedora 10 and even EPEL (>=6) doesn't need it now.

* Wed Feb 23 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-2
- Fixes asked during the review process:
  - Filter the private shared EV.so out of the automatic Provides
  - Put the header files in a -devel package
- Removed the Buildroot line since it's useless for newer versions of Fedora
  and this package can only go in Fedora >= 15 due to its libev dependency)

* Mon Jan 24 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-1
- Update to 4.03.
- Use the system libev instead of the bundled one.
