Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: lcov
Version: 2.0
Release: 5%{?dist}

Summary: LTP GCOV extension code coverage tool
License: GPL-2.0-or-later

URL: https://github.com/linux-test-project/lcov/
Source0: https://github.com/linux-test-project/lcov/releases/download/v%{version}/lcov-%{version}.tar.gz

BuildArch: noarch
BuildRequires: perl-generators
BuildRequires: git-core
BuildRequires: make

Requires: /usr/bin/gcov
Requires: /usr/bin/find
Requires: perl(GD::Image)
Requires: perl(JSON::XS)

# lcovutil.pm is a private helper file
%global __requires_exclude ^perl\\(lcovutil\\)$
%global __provides_exclude ^perl.*$

%description
LCOV is an extension of GCOV, a GNU tool which provides information
about what parts of a program are actually executed (i.e. "covered")
while running a particular test case. The extension consists of a set
of PERL scripts which build on the textual GCOV output to implement
HTML output and support for large projects.

%prep
%autosetup

%install
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} \
     CFG_DIR=%{_sysconfdir} LIB_DIR=%{_datadir}/lcov

%files
%{_bindir}/gendesc
%{_bindir}/genhtml
%{_bindir}/geninfo
%{_bindir}/genpng
%{_bindir}/lcov
%{_mandir}/man1/gendesc.1*
%{_mandir}/man1/genhtml.1*
%{_mandir}/man1/geninfo.1*
%{_mandir}/man1/genpng.1*
%{_mandir}/man1/lcov.1*
%{_mandir}/man5/lcovrc.5*
%dir %{_datadir}/lcov
%dir %{_datadir}/lcov/support-scripts
%{_datadir}/lcov/lcovutil.pm
%{_datadir}/lcov/support-scripts/analyzeInfoFiles
%{_datadir}/lcov/support-scripts/criteria
%{_datadir}/lcov/support-scripts/get_signature
%{_datadir}/lcov/support-scripts/getp4version
%{_datadir}/lcov/support-scripts/gitblame
%{_datadir}/lcov/support-scripts/gitdiff
%{_datadir}/lcov/support-scripts/p4annotate
%{_datadir}/lcov/support-scripts/p4udiff
%{_datadir}/lcov/support-scripts/py2lcov
%{_datadir}/lcov/support-scripts/spreadsheet.py
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/lcovrc

%changelog
* Thu Nov 7 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.0-5
- Initial Azure Linux import from Fedora 41 (license: MIT)
- Verified license

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Terje Rosten <terje.rosten@ntnu.no> - 2.0-1
- 2.0
- Use explicit file listing
- Remove upstream patches
- Ship new files

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Daniel P. Berrangé <berrange@redhat.com> - 1.14-1
- Update to 1.14 release (rhbz #1713541)
- Add patches for intermediate gcov format (rhbz #1668843)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 30 2018 Daniel P. Berrangé <berrange@redhat.com> - 1.13-4
- Add dep on find command (rhbz #1573158)

* Wed Mar  7 2018 Daniel P. Berrangé <berrange@redhat.com> - 1.13-3
- Add patch for gcc8 (rhbz #1552042)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Daniel Berrange <berrange@localhost.localdomain> - 1.13-1
- Update to 1.13 release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 10 2016 Daniel P. Berrange <berrange@redhat.com> - 1.12-1
- Update to 1.12 release (rhbz #1199640)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.10-2
- Perl 5.18 rebuild

* Tue Mar 19 2013 Daniel P. Berrange <berrange@redhat.com> - 1.10-1
- Update to 1.10 release
- Fix handling of gcc 4.7 unreachable code (rhbz #829514)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 12 2012 berrange <berrange@redhat.com> - 1.9-2
- Fix compat with gcc 4.7 (rhbz #787502)
- Replace 2 argument open with 3 argument open (rhbz #706040)

* Mon Jan 30 2012 Daniel P. Berrange <berrange@redhat.com> - 1.9-1
- Update to 1.9 release (rhbz #627576)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 25 2009 Roland McGrath <roland@redhat.com> - 1.7-1
- Update to 1.7 release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Roland McGrath <roland@redhat.com> - 1.6-1
- Update to 1.6 release.
- Fix License: tag.

* Mon Feb 20 2006 Roland McGrath <roland@redhat.com> - 1.4-2
- Fix lcov -z to look for .gcda (GCC >= 3.4) suffix as well as .da (old GCC).
- Remove empty %%build from spec.
- Fix URL for source tarball.

* Mon Feb 13 2006 Roland McGrath <roland@redhat.com> - 1.4-1
- Initial build, some spec bits snarfed from upstream.

