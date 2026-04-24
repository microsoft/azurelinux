# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       perl-srpm-macros    
Version:    1
Release: 61%{?dist}
Summary:    RPM macros for building Perl source package from source repository
License:    GPL-3.0-or-later
Source0:    macros.perl-srpm
BuildArch:  noarch

%description
These RPM macros are used for building Perl source packages from source
repositories. They influence build-requires set into the source package.

%install
install -m 644 -D "%{SOURCE0}" \
    '%{buildroot}%{_rpmconfigdir}/macros.d/macros.perl-srpm'

%files
%{_rpmconfigdir}/macros.d/macros.perl-srpm

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1-59
- Disable perl_bootstrap for perl 5.42 rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1-58
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1-55
- Disable perl_bootstrap for perl 5.40 rebuild

* Mon Apr 29 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1-54
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.50
- Disable perl_bootstrap for perl 5.38 rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.49
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 04 2022 Michal Josef Špaček <mspacek@redhat.com> - 1-47
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1-45
- Disable perl_bootstrap for perl 5.36 rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1-44
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1-41
- Disable perl_bootstrap for perl 5.34 rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1-40
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1-37
- Disable perl_bootstrap for perl 5.32 rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1-36
- Disable perl_bootstrap for perl 5.32 rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1-35
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.32
- Define %%__perl, because in rpm 4.15 those are no longer defined

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1-31
- Disable perl_bootstrap for perl 5.30 rebuild

* Wed Apr 24 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1-30
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1-27
- Disable perl_bootstrap for perl 5.28 rebuild

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1-26
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1-23
- Disable perl_bootstrap for perl 5.26 rebuild

* Fri Jun 02 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1-22
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1-20
- Disable perl_bootstrap for perl 5.24 rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1-19
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.16
- Disable perl_bootstrap for perl 5.22 rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-14
- Disable perl_bootstrap for perl 5.20 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-13
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 1-11
- Move macro files into %%{_rpmconfigdir}/macros.d

* Tue Aug 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-10
- Disable perl_bootstrap for perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1-8
- Perl 5.18 rebuild

* Thu Feb 28 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1-7
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1-4
- Disable perl_bootstrap for perl 5.16 rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1-3
- Perl 5.16 rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1-2
- Enable perl_bootstrap for perl 5.16 rebuild

* Tue May 15 2012 Petr Pisar <ppisar@redhat.com> - 1-1
- Introduce Perl SRPM macros as a standalone package


