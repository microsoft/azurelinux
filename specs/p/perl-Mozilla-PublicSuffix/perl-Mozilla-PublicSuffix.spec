# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Mozilla-PublicSuffix
Version:        1.0.7
Release:        3%{?dist}
Summary:        Get a domain name's public suffix via the Mozilla Public Suffix List
License:        MIT
URL:            https://metacpan.org/release/Mozilla-PublicSuffix
Source0:        https://cpan.metacpan.org/modules/by-module/Mozilla/Mozilla-PublicSuffix-v%{version}.tar.gz

# https://github.com/rsimoes/Mozilla-PublicSuffix/pull/6
Patch1:         Mozilla-PublicSuffix-unbundle.patch

BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Tiny)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(open)
BuildRequires:  perl(strict)
BuildRequires:  perl(Tie::File)
BuildRequires:  perl(URI)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Exporter)
BuildRequires:  perl(URI::_idna)
BuildRequires:  publicsuffix-list
# Tests
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)

Requires:       publicsuffix-list

%description
This module provides a single function that returns the public suffix of a
domain name by referencing a parsed copy of Mozilla's Public Suffix List.
From the official website at http://publicsuffix.org/

%prep
%setup -q -n Mozilla-PublicSuffix-v%{version}
%autopatch -p1

%build
perl Build.PL installdirs=vendor --config system_publicsuffix_list=/usr/share/publicsuffix/public_suffix_list.dat </dev/null
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 20 2024 Yanko Kaneti <yaneti@declera.com> - 1.0.7-1
- New version and minor tweaks

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.6-2
- Perl 5.36 rebuild

* Thu May 05 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.6-1
- 1.0.6 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.3-2
- Perl 5.34 rebuild

* Thu Mar  4 2021 Yanko Kaneti <yaneti@declera.com> - 1.0.3-1
- New version bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.2-1
- 1.0.2 bump
- Specify all dependencies

* Thu Nov 12 2020 Yanko Kaneti <yaneti@declera.com> - 1.0.1-1
- New version and upstream maintainer.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.0-13
- Perl 5.32 rebuild

* Wed Mar 11 2020 Yanko Kaneti <yaneti@declera.com> - 1.0.0-12
- BR: perl(blib) - split recently

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.0-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.0-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.0-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug  8 2016 Yanko Kaneti <yaneti@declera.com> 1.0.0-1
- Update to v1.0.0. Drop upstreamed patch

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.1.19-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Yanko Kaneti <yaneti@declera.com> 0.1.19-8
- Update test patch two to reflect changes in the list

* Mon Aug  3 2015 Yanko Kaneti <yaneti@declera.com> 0.1.19-7
- Use the new name for the system publicsuffix list
- Update tests for the new non wildard status of .cy
- Use autopatch

* Mon Jun 22 2015 Yanko Kaneti <yaneti@declera.com> 0.1.19-6
- Adjust for the separation of perl(open). Bug 1234362

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.1.19-4
- Perl 5.22 rebuild

* Tue Jan 20 2015 Yanko Kaneti <yaneti@declera.com> 0.1.19-3
- Unbundle the publicsuffix list

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.1.19-2.20140613
- Perl 5.20 rebuild

* Wed Jul 23 2014 Yanko Kaneti <yaneti@declera.com> 0.1.19-1.20140613
- New upstream release - 0.1.19
- Latest public suffix list from publicsuffix.org

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-2.20140311
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Yanko Kaneti <yaneti@declera.com> 0.1.18-1.20140311
- New upstream release - 0.1.18
- Latest public suffix list from publicsuffix.org

* Wed Jan 29 2014 Yanko Kaneti <yaneti@declera.com> 0.1.17-1.20140125
- New upstream release - 0.1.17
- Latest public suffix list from publicsuffix.org

* Mon Jan  6 2014 Yanko Kaneti <yaneti@declera.com> 0.1.16-1.20131212
- Latest public suffix list from publicsuffix.org

* Mon Sep 30 2013 Yanko Kaneti <yaneti@declera.com> 0.1.16-1.20130918
- Update to 0.1.16
- Drop upstreamed patch

* Thu Sep 26 2013 Yanko Kaneti <yaneti@declera.com> 0.1.15-3.20130918
- Latest public suffix list from publicsuffix.org
- Fixup tests in 0.1.15 to match the new list

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.15-3.20130516
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.1.15-2.20130516
- Perl 5.18 rebuild

* Mon May 20 2013 Yanko Kaneti <yaneti@declera.com> 0.1.15-1.20130516
- New upstream bugfix release.

* Thu May 16 2013 Yanko Kaneti <yaneti@declera.com> 0.1.13-2.20130516
- Address review comments (#963197#1)

* Wed May 15 2013 Yanko Kaneti <yaneti@declera.com> 0.1.13-1.20130515
- Specfile autogenerated by cpanspec 1.78 and modified for review
