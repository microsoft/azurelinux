Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global macros_dir %{_rpmconfigdir}/macros.d

%global macrosfile macros.ghc-srpm

Name:           ghc-srpm-macros
Version:        1.9.1
Release:        3%{?dist}
Summary:        RPM macros for building Haskell source packages

License:        GPL-2.0-or-later
Url:            https://src.fedoraproject.org/rpms/ghc-srpm-macros
BuildArch:      noarch

Source0:        %{macrosfile}

%description
Macros used when generating Haskell source RPM packages.


%prep
%{nil}


%build
echo no build stage needed


%install
install -p -D -m 0644 %{SOURCE0} %{buildroot}/%{macros_dir}/%{macrosfile}


%files
%{macros_dir}/%{macrosfile}


%changelog
* Tue Jan 07 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.9.1-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Mon Mar 18 2024 Jens Petersen <petersen@redhat.com> - 1.9.1-1
- %%haskell_setup -q replaces %%haskell_setup_quick
- %%haskell_setup -p and -h options disable prof and doc

* Thu Mar  7 2024 Jens Petersen <petersen@redhat.com> - 1.9-1
- improve haskell_setup to undefine the old macros
- add haskell_setup_quick for test builds

* Wed Mar 06 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1.8-1
- Add riscv64

* Thu Feb 29 2024 Jens Petersen <petersen@redhat.com> - 1.7-1
- add ghc_profiling and haskell_setup macros: will replace with_ghc_prof

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Jens Petersen <petersen@redhat.com> - 1.6.1-3
- migrate to SPDX license tag

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jan 30 2023 Jens Petersen <petersen@redhat.com> - 1.6.1-1
- restore ghc_devel_prof for existing ghc spec files

* Sat Jan 21 2023 Jens Petersen <petersen@redhat.com> - 1.6.0-1
- drop long unused ghc_arches_with_ghci
- update (unused) ghc_arches
- replace unused ghc_devel_prof with with_ghc_prof (moved from ghc-rpm-macros)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct  1 2019 Jens Petersen <petersen@redhat.com> - 1.5.0-1
- define ghc_devel_prof to handle prof/devel BRs across releases

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Mar  7 2016 Michal Toman <mtoman@fedoraproject.org> - 1.4.2-4
- add MIPS to ghc_arches_with_ghci (#1294874)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 27 2015 Jens Petersen <petersen@redhat.com> - 1.4.2-1
- reenable ghci on aarch64 (#1203951)

* Thu Mar 19 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.1-1
- disable ghci on aarch64 due to dynlinked runtime problems (see #1195231)

* Tue Feb 17 2015 Jens Petersen <petersen@redhat.com> - 1.4-1
- ghc-7.8 shared libraries allow ghci to work on all arch's

* Fri Jun 27 2014 Jens Petersen <petersen@redhat.com> - 1.3-2
- add pkg git as URL (#1093541)
- downgrade license tag to GPLv2+ in line with rpm (redhat-rpm-config is GPL+)
- sync with current ghc-rpm-macros: add ghc_arches for backwards compatibility

* Fri May  2 2014 Jens Petersen <petersen@redhat.com> - 1.3-1
- separate from ghc-rpm-macros
