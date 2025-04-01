Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Moo
Version:        2.005005
Release:        8%{?dist}
Summary:        Minimalist Object Orientation (with Moose compatibility)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl

URL:            https://metacpan.org/release/Moo
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Moo-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Method::Modifiers) >= 1.10
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Devel::GlobalDestruction) >= 0.11
BuildRequires:  perl(Exporter)
# Filter::Simple not used at test-time
BuildRequires:  perl(Import::Into) >= 1.002
BuildRequires:  perl(Module::Runtime) >= 0.014
BuildRequires:  perl(mro)
# MRO::Compat not needed with modern perl
BuildRequires:  perl(overload)
BuildRequires:  perl(Role::Tiny) >= 2.002004
BuildRequires:  perl(Scalar::Util) >= 1.00
BuildRequires:  perl(strictures) >= 1.004003
BuildRequires:  perl(Sub::Defer) >= 2.006006
BuildRequires:  perl(Sub::Quote) >= 2.006006
# Text::Balanced not used at test-time
# Optional run-time:
BuildRequires:  perl(Class::XSAccessor) >= 1.18
BuildRequires:  perl(Sub::Util)
# lib/Moo/HandleMoose.pm requires Moose modules. Moo::HandleMoose is used only
# if Moose has been loaded. So this is circular optional dependency definitly
# not suitable for Moo because Moo is reimplementation of Moose:
#   Class::MOP
#   Moose
#   Moose::Meta::Method::Constructor
#   Moose::Util::TypeConstraints
# Tests:
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Class::XSAccessor::Array)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
# MooX::ArrayRef is defined internally via %%INC
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(threads)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Optional tests:
BuildRequires:  perl(CPAN::Meta::Requirements)
Requires:       perl(Carp)
Requires:       perl(Class::Method::Modifiers) >= 1.10
Requires:       perl(Devel::GlobalDestruction) >= 0.11
Requires:       perl(Import::Into) >= 1.002
Requires:       perl(Module::Runtime) >= 0.012
Requires:       perl(mro)
Requires:       perl(Role::Tiny) >= 1.003003

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}perl\\(Moo::_
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}perl\\(Moo::_
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Devel::GlobalDestruction|Import::Into|Module::Runtime|Role::Tiny)\\)$

%description
This module is an extremely light-weight, high-performance Moose
replacement. It also avoids depending on any XS modules to allow simple
deployments. The name Moo is based on the idea that it provides almost -but
not quite- two thirds of Moose.

%prep
%setup -q -n Moo-%{version}

%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
%{make_build} test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Dec 23 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 2.005005-8
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.005005-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.005005-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.005005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.005005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Michal Josef Špaček <mspacek@redhat.com> - 2.005005-3
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.005005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Emmanuel Seyman <emmanuel@seyman.fr> - 2.005005-1
- Update to 2.005005

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.005004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.005004-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.005004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.005004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.005004-2
- Perl 5.34 rebuild

* Sun Apr 04 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 2.005004-1
- Update to 2.005004

* Sun Mar 21 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 2.005003-1
- Update to 2.005003

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.004004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 29 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 2.004004-1
- Update to 2.004004

* Sun Nov 22 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 2.004003-1
- Update to 2.004003

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.004000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.004000-2
- Perl 5.32 rebuild

* Sun Apr 12 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 2.004000-1
- Update to 2.004000

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.003006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 27 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 2.003006-1
- Update to 2.003006
- Replace calls to %%{__perl} with /usr/bin/perl
- Replace calls to "make pure_install" with %%{make_install}
- Replace calls to make with %%{make_build}
- Pass NO_PERLLOCAL=1 to Makefile.PL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.003004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.003004-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.003004-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.003004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.003004-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.003004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.003004-1
- Update to 2.003004

* Sun Nov 19 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.003003-1
- Update to 2.003003

* Sun Sep 03 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.003002-4
- Update BuildRequires versions (fixes #1486333)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.003002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.003002-2
- Perl 5.26 rebuild

* Sun Apr 02 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.003002-1
- Update to 2.003002

* Thu Mar 09 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.003001-1
- Update to 2.003001

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.003000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 11 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.003000-1
- Update to 2.003000

* Sun Nov 13 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.002005-1
- Update to 2.002005

* Tue Jun 28 2016 Petr Pisar <ppisar@redhat.com> - 2.002004-1
- 2.002004 bump

* Fri Jun 24 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.002003-1
- Update to 2.002003

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.001001-2
- Perl 5.24 rebuild

* Sat Mar 05 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.001001-1
- Update to 2.001001

* Wed Mar 02 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.001000-1
- Update to 2.001000

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.000002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 31 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000002-1
- Update to 2.000002

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.000001-2
- Perl 5.22 rebuild

* Sun Mar 22 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000001-1
- Update to 2.000001

* Sun Mar 08 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000000-1
- Update to 2.000000

* Sun Jan 25 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 1.007000-1
- Update to 1.007000

* Mon Nov 10 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1.006001-1
- Update to 1.006001

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.006000-2
- Perl 5.20 rebuild

* Fri Aug 22 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.006000-1
- Upstream update.
- Reflect deps having changed.

* Tue Jul 22 2014 Petr Pisar <ppisar@redhat.com> - 1.005000-1
- 1.005000 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Miro Hrončok <mhroncok@redhat.com> - 1.003001-2
- Role::Tiny is now >= 1.003002

* Fri Oct 18 2013 Miro Hrončok <mhroncok@redhat.com> - 1.003001-1
- 1.003001 bump
- Source URL was changed in this release

* Fri Aug 16 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003000-2
- Added perl(Moo::Conflicts) to provides

* Fri Aug 09 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003000-1
- 1.003000 bump
- Update source link
- Specify all dependencies

* Thu Aug 08 2013 Petr Pisar <ppisar@redhat.com> - 1.002000-3
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Iain Arnell <iarnell@gmail.com> 1.002000-1
- update to latest upstream version

* Fri Apr 19 2013 Iain Arnell <iarnell@gmail.com> 1.001000-1
- update to latest upstream version

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 1.000008-1
- update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 05 2013 Iain Arnell <iarnell@gmail.com> 1.000007-1
- update to latest upstream version

* Sat Oct 27 2012 Iain Arnell <iarnell@gmail.com> 1.000005-1
- update to latest upstream version

* Fri Oct 19 2012 Iain Arnell <iarnell@gmail.com> 1.000004-1
- update to latest upstream version

* Sun Sep 09 2012 Iain Arnell <iarnell@gmail.com> 1.000003-1
- update to latest upstream version

* Sun Jul 29 2012 Iain Arnell <iarnell@gmail.com> 1.000001-1
- update to latest upstream version

* Thu Jul 26 2012 Iain Arnell <iarnell@gmail.com> 1.000000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 20 2012 Iain Arnell <iarnell@gmail.com> 1.000000-1
- update to latest upstream version
- explicity require Role::Tiny >= 1.001003

* Tue Jul 17 2012 Iain Arnell <iarnell@gmail.com> 0.091014-1
- update to latest upstream version

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.091007-2
- Perl 5.16 rebuild

* Sat May 19 2012 Iain Arnell <iarnell@gmail.com> 0.091007-1
- update to latest upstream version

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 0.009014-1
- update to latest upstream version

* Fri Jan 06 2012 Iain Arnell <iarnell@gmail.com> 0.009013-1
- update to latest upstream version

* Sun Nov 20 2011 Iain Arnell <iarnell@gmail.com> 0.009012-1
- update to latest upstream version
- filter private requires/provides

* Mon Oct 10 2011 Iain Arnell <iarnell@gmail.com> 0.009011-1
- update to latest upstream version

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 0.009010-1
- Specfile autogenerated by cpanspec 1.79.
