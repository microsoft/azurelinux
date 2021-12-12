Vendor:         Microsoft Corporation
Distribution:   Mariner
# ghc has been bootstrapped on all Fedora archs except aarch64.
# The ghc interpreter ghci is only supported on a subset of archs.

%global macros_dir %{_rpmconfigdir}/macros.d

Name:           ghc-srpm-macros
Version:        1.5.0
Release:        3%{?dist}
Summary:        RPM macros for building Haskell source packages

License:        GPLv2+
Url:            https://src.fedoraproject.org/rpms/ghc-srpm-macros
BuildArch:      noarch

Source0:        macros.ghc-srpm

%description
Macros used when generating Haskell source RPM packages.


%prep
%{nil}


%build
echo no build stage needed


%install
install -p -D -m 0644 %{SOURCE0} %{buildroot}/%{macros_dir}/macros.ghc-srpm


%files
%{macros_dir}/macros.ghc-srpm


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
