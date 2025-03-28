Name:           kernel-srpm-macros
Version:        1.0
# when bumping version and resetting release, don't forget to bump version of kernel-rpm-macros as well
Release:        25%{?dist}
Summary:        RPM macros that list arches the full kernel is built on
# This package only exist in Fedora repositories
# The license is the standard (MIT) specified in
# Fedora Project Contribution Agreement
# and as URL we provide dist-git URL
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://src.fedoraproject.org/rpms/kernel-srpm-macros
BuildArch:      noarch
# We are now the ones shipping kmod.attr
Conflicts:      redhat-rpm-config < 205
# macros.kmp, kmodtool and rpmsort were moved from kernel-rpm-macros
# to kernel-srpm-macros in 1.0-9/185-9
Conflicts:      kernel-rpm-macros < 205

# Macros
Source001:        macros.kernel-srpm
Source002:        macros.kmp

# Dependency generator scripts
Source100:      find-provides.ksyms
Source101:      find-requires.ksyms
Source102:      firmware.prov
Source103:      modalias.prov
Source104:      provided_ksyms.attr
Source105:      required_ksyms.attr
Source106:      modalias.attr

# Dependency generators & their rules
Source200:      kmod.attr

# Misc helper scripts
Source300:      kmodtool
Source301:      rpmsort
Source302:      symset-table

# kabi provides generator
Source400: kabi.attr
Source401: kabi.sh

# BRPs
Source500: brp-kmod-set-exec-bit
Source501: brp-kmod-restore-perms

%global rrcdir /usr/lib/rpm/redhat


%description
This packages contains the rpm macro that list what arches
the full kernel is built on.
The variable to use is kernel_arches.

%package -n kernel-rpm-macros
Version: 205
Summary: Macros and scripts for building kernel module packages
# rpmsort is GPL-2.0-or-later
License:        MIT AND GPL-2.0-or-later
Requires: redhat-rpm-config >= 205

# for brp-kmod-compress
Requires: xz
# for brp-kmod-compress, brp-kmod-set-exec-bit
Requires: findutils
# for find-provides.ksyms, find-requires.ksyms, kmodtool
Requires: sed
# for find-provides.ksyms, find-requires.ksyms
Requires: gawk
Requires: grep
Requires: binutils
# for find-requires.ksyms
Requires: kmod

%description -n kernel-rpm-macros
Macros and scripts for building kernel module packages.

%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .

%build
# nothing to do

%install
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d
install -p -m 0644 -t %{buildroot}/%{_rpmconfigdir}/macros.d macros.kernel-srpm
%if 0%{?rhel} >= 8
  sed -i 's/^%%kernel_arches.*/%%kernel_arches x86_64 s390x ppc64le aarch64/' \
    %{buildroot}/%{_rpmconfigdir}/macros.d/macros.kernel-srpm
%endif

mkdir -p %{buildroot}%{rrcdir}/find-provides.d
mkdir -p %{buildroot}%{_fileattrsdir}
install -p -m 755 -t %{buildroot}%{rrcdir} kmodtool rpmsort symset-table
install -p -m 755 -t %{buildroot}%{rrcdir} find-provides.ksyms find-requires.ksyms
install -p -m 755 -t %{buildroot}%{rrcdir}/find-provides.d firmware.prov modalias.prov
install -p -m 755 -t %{buildroot}%{rrcdir} brp-kmod-restore-perms brp-kmod-set-exec-bit
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.kmp
install -p -m 644 -t %{buildroot}%{_fileattrsdir} kmod.attr

install -p -m 644 -t "%{buildroot}%{_fileattrsdir}" kabi.attr
install -p -m 755 -t "%{buildroot}%{_rpmconfigdir}" kabi.sh

install -p -m 644 -t "%{buildroot}%{_fileattrsdir}" provided_ksyms.attr required_ksyms.attr
install -p -m 644 -t "%{buildroot}%{_fileattrsdir}" modalias.attr

%files
%{_rpmconfigdir}/macros.d/macros.kernel-srpm
%{_fileattrsdir}/kmod.attr

%files -n kernel-rpm-macros
%{_rpmconfigdir}/macros.d/macros.kmp
%{_rpmconfigdir}/kabi.sh
%{_fileattrsdir}/kabi.attr
%{_fileattrsdir}/modalias.attr
%{_fileattrsdir}/provided_ksyms.attr
%{_fileattrsdir}/required_ksyms.attr
%dir %{rrcdir}/find-provides.d
%{rrcdir}/brp-kmod-restore-perms
%{rrcdir}/brp-kmod-set-exec-bit
%{rrcdir}/symset-table
%{rrcdir}/find-provides.ksyms
%{rrcdir}/find-requires.ksyms
%{rrcdir}/find-provides.d/firmware.prov
%{rrcdir}/find-provides.d/modalias.prov
%{rrcdir}/kmodtool
%{rrcdir}/rpmsort

%changelog
* Tue Dec 17 2024 Elaheh Dehghani <edehghani@microsoft.org> - 1.0-25
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1.0-23
- Add riscv64

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-19
- Capture local __crc_* symbols for "Provides: kernel()".
- Add support for XZ compression for the symvers file.
- Fix "Provides: kernel()" generation when both __kcrctab and __kcrctab_gpl
  are present.
- Fix regression for "Provides:" generation in cases when modversions are stored
  in a section that is over 64K in size.
- Speedup and cleanup changes in find-provides.ksyms and find-requires.ksyms.
- Fix regex usage in kmod.attr. (Denys Vlasenko)
- Implement modalias "Provides:" grouping. (Denys Vlasenko)
- Speedup and cleanup changes in modalias.prov and kmod.attr. (Denys Vlasenko)

* Tue Mar 30 2023 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-18
- Avoid triggering debuginfod during elfutils tools usage.

* Tue Jan 31 2023 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-17
- Support storing of __crc_* symbols in sections other than .rodata.
- Work around a change in type of __crc_* symbols for some kmods printed by nm
  on ppc64le and s390x.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 18 2021 Miro Hrončok <mhroncok@redhat.com> - 1.0-13
- Bump kernel-rpm-macros to 205 to provide clear upgrade path

* Thu Nov 18 2021 Miro Hrončok <mhroncok@redhat.com> - 1.0-12
- Correct conflicts to redhat-rpm-macros < 205
- Move Perl scripts back to kernel-rpm-macros to avoid Perl in the default buildroot

* Thu Nov 18 2021 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-11
- Add conflicts of redhat-rpm-macros < 204 as macros.kmp, kmodtool,
  and rpmsort were moved from the latter to the former.
- Remove RHEL-specific kABI bits from find-requires.ksyms and macros.kmp.

* Thu Nov 18 2021 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-10
- Add conflicts of kernel-srpm-macros with kernel-rpm-macros < 185-9
  as macros.kmp, kmodtool, and rpmsort were moved from the latter
  to the former.

* Thu Nov 18 2021 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-9
- Update scripts with RHEL-specific changes.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Michal Domonkos <mdomonko@redhat.com> - 1.0-5
- Adopt kernel-rpm-macros & kmod.attr subpackage from redhat-rpm-config

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.0-3
- Escape percent for %%kernel_arches macro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Troy Dawson <tdawson@redhat.com> - 1.0-1
- Initial build