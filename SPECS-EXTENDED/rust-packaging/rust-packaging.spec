%bcond_without check

Name:           rust-packaging
Version:        26.4
Release:        2%{?dist}
Summary:        RPM macros and generators for building Rust packages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pagure.io/fedora-rust/rust-packaging
Source:         %{url}/archive/%{version}/rust-packaging-%{version}.tar.gz

# temporary patch for compatibility with RHEL / ELN:
# The %%cargo_prep macro in RHEL / ELN accepts a -V flag. Using the same spec
# file for both Fedora and ELN would cause spec file parsing errors because
# the -V flag is not known in Fedora.
Patch:          0001-Temporarily-accept-cargo_prep-V-flag-for-spec-compat.patch

BuildArch:      noarch

%if %{with check}
BuildRequires:  python3-pytest
%endif

%description
%{summary}.

%package -n rust-srpm-macros
Summary:        RPM macros for building Rust projects

%description -n rust-srpm-macros
RPM macros for building source packages for Rust projects.

%package -n cargo-rpm-macros
Summary:        RPM macros for building projects with cargo

# obsolete + provide rust-packaging (removed in Fedora 38)
Obsoletes:      rust-packaging < 24
Provides:       rust-packaging = %{version}-%{release}
Requires:       cargo2rpm >= 0.1.8
Requires:       cargo
Requires:       gawk
Requires:       grep
Requires:       azurelinux-rpm-macros

%description -n cargo-rpm-macros
RPM macros for building projects with cargo.

%prep
%autosetup -p1

%build
# nothing to do

%install
install -D -p -m 0644 -t %{buildroot}/%{_rpmmacrodir} macros.d/macros.cargo
install -D -p -m 0644 -t %{buildroot}/%{_rpmmacrodir} macros.d/macros.rust
install -D -p -m 0644 -t %{buildroot}/%{_rpmmacrodir} macros.d/macros.rust-srpm
install -D -p -m 0644 -t %{buildroot}/%{_fileattrsdir} fileattrs/cargo.attr
install -D -p -m 0644 -t %{buildroot}/%{_fileattrsdir} fileattrs/cargo_vendor.attr

%if %{with check}
%check
export MACRO_DIR=%{buildroot}%{_rpmmacrodir}
#pytest -vv
%pytest -k "not (test_cargo_prep or test_cargo_prep_vendor or test_cargo_prep_no_replacement or test_cargo_install)"
%endif

%files -n rust-srpm-macros
%license LICENSE
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.rust-srpm

%files -n cargo-rpm-macros
%license LICENSE
%{_rpmmacrodir}/macros.cargo
%{_rpmmacrodir}/macros.rust
%{_fileattrsdir}/cargo.attr
%{_fileattrsdir}/cargo_vendor.attr

%changelog
* Fri Dec 26 2025 Aditya Singh <v-aditysing@microsoft.com> - 26.4-2
- Initial Azure Linux import from Fedora 43 (license: MIT).
- License verified. 

* Mon Aug 18 2025 Fabio Valentini <decathorpe@gmail.com> - 26.4-1
- Update to version 26.4; Fixes RHBZ#2389206

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 26.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 26.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 21 2024 Fabio Valentini <decathorpe@gmail.com> - 26.3-3
- Adapt tests to slightly different macro expansion in RPM 4.20

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 26.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 17 2024 Fabio Valentini <decathorpe@gmail.com> - 26.3-1
- Update to version 26.3; Fixes RHBZ#2281002

* Tue Mar 05 2024 Fabio Valentini <decathorpe@gmail.com> - 26.2-1
- Update to version 26.2; Fixes RHBZ#2267089

* Wed Feb 21 2024 Fabio Valentini <decathorpe@gmail.com> - 26.1-1
- Update to version 26.1; Fixes RHBZ#2265140

* Wed Jan 31 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 25.2-4
- Disable rust-srpm-macros in EPEL

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 25.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 12 2023 Fabio Valentini <decathorpe@gmail.com> - 25.2-2
- Temporarily accept cargo_prep -V flag for spec compatibiltiy with RHEL

* Sat Sep 30 2023 Fabio Valentini <decathorpe@gmail.com> - 25.2-1
- Update to version 25.2

* Fri Sep 29 2023 Fabio Valentini <decathorpe@gmail.com> - 25.1-1
- Update to version 25.1; Fixes RHBZ#2241437

* Thu Sep 28 2023 Fabio Valentini <decathorpe@gmail.com> - 25.0-1
- Update to version 25.0

* Thu Aug 17 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 24-5
- Correct cargo_registry path

* Thu Aug 17 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 24-4
- Correct cargo and cargo2rpm paths

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 19 2023 Fabio Valentini <decathorpe@gmail.com> - 24-2
- Include upstream patches with minor bug fixes and improvements

* Thu Feb 16 2023 Fabio Valentini <decathorpe@gmail.com> - 24-1
- Update to version 24

* Thu Jan 26 2023 Fabio Valentini <decathorpe@gmail.com> - 23-7
- Backport upstream patches for force-frame-pointers support

* Thu Jan 26 2023 Fabio Valentini <decathorpe@gmail.com> - 23-6
- Drop partially broken patch for force-frame-pointers support

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Fabio Valentini <decathorpe@gmail.com> - 23-4
- Backport upstream patches for various bugs in rust2rpm v23

* Thu Jan 05 2023 Fabio Valentini <decathorpe@gmail.com> - 23-3
- Backport upstream patch for force-frame-pointers support

* Wed Nov 23 2022 Fabio Valentini <decathorpe@gmail.com> - 23-2
- Backport upstream patches for various bugs in rust2rpm v23

* Fri Oct 28 2022 Fabio Valentini <decathorpe@gmail.com> - 23-1
- Update to version 23; Fixes RHBZ#2138138

* Wed Oct 05 2022 Fabio Valentini <decathorpe@gmail.com> - 22-4
- Include upstream patch to correctly recognize "wasm64" target

* Mon Aug 08 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 22-3
- Adjust build flags to allow the new implementation using --package-
  metadata

* Tue Jul 26 2022 Fabio Valentini <decathorpe@gmail.com> - 22-2
- Fix generation of specs when there's only an auto-generated patch

* Mon Jul 25 2022 Fabio Valentini <decathorpe@gmail.com> - 22-1
- Update to version 22; Fixes RHBZ#2110233

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Fabio Valentini <decathorpe@gmail.com> - 21-5
- Adapt %%cargo_prep macro to fix builds with Rust 1.62+

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 21-4
- Rebuilt for Python 3.11

* Sat Mar 19 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 21-3
- Backport patch to fix rpmautospec detection

* Tue Feb 22 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 21-2
- Add patches to allow debuginfo level to be set easily again

* Sun Feb 20 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 21-1
- Version 21

* Tue Feb 15 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20-3
- Include linker flags for package note in %%build_rustflags

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20-1
- Version 20

* Mon Nov 22 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 19-2
- Rebuild in a side tag

* Mon Nov 22 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 19-1
- Version 19

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Fabio Valentini <decathorpe@gmail.com> - 18-1
- Update to version 18.

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 17-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 28 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 17-2
- Band-aid clap pre-release version

* Sat Dec 26 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 17-1
- Update to 17

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 15-2
- Rebuilt for Python 3.9

* Fri May 22 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 15-1
- Update to 15

* Sat May 02 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 14-1
- Update to 14

* Mon Feb 03 2020 Josh Stone <jistone@redhat.com> - 13-3
- Use 'cargo install --no-track' with cargo 1.41

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 13-1
- Update to 13

* Fri Dec 13 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 12-2
- Fixup generation of files with no-tilde

* Fri Dec 13 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 12-1
- Update to 12

* Wed Dec 04 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11-1
- Update to 11

* Sat Sep 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-6
- Depend on setuptools in runtime

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 10-5
- Rebuilt for Python 3.8

* Sun Aug 18 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-4
- Ignore Cargo.lock

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-2
- Do not use awk's inplace feature

* Sun Jun 16 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-1
- Update to 10

* Sat Jun 08 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9-3
- Update patches

* Sat Jun 08 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9-2
- Backport patches from upstream

* Sun May 05 09:18:19 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9-1
- Update to 9

* Tue Apr 23 21:18:12 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8-1
- Update to 8

* Tue Apr 23 16:17:30 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7-1
- Update to 7

* Sun Mar 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-28
- Install $PWD/Cargo.toml into $REG_DIR/Cargo.toml

* Sun Mar 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-27
- Restore Cargo.toml.deps into $PWD/Cargo.toml

* Sun Mar 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-26
- Strip out target dependencies too

* Sun Mar 10 2019 Igor Gnatenko <ignatnekobrain@fedoraproject.org> - 6-25
- Do not error on removing files which do not exist

* Sun Mar 10 2019 Igor Gnatenko <ignatnekobrain@fedoraproject.org> - 6-24
- Escape `\n` properly in macro file

* Sun Mar 10 2019 Igor Gnatenko <ignatnekobrain@fedoraproject.org> - 6-23
- Do not pull optional deps into BRs and trivial fixes

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-21
- Use %%version_no_tilde

* Sat Jan 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-20
- Trivial fixes for pre-release versions

* Sat Jan 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-19
- Add support for pre-release versions

* Fri Dec 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-18
- Set CARGO_HOME

* Sat Nov 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-17
- Update patchset

* Sat Nov 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-16
- Make package archful

* Fri Nov 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-15
- Support .rust2rpm.conf

* Wed Oct 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-14
- Fix syntax error

* Tue Oct 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-13
- Support multiple dependencies with same name

* Sat Oct 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-12
- Fix requirements with space

* Fri Oct 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-11
- Trivial fixes to last patchset

* Fri Oct 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-10
- Split features into subpackages

* Sun Sep 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-1
- Update to 6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 5-10
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-9
- Rebuilt for Python 3.7

* Fri Jun 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-8
- Various improvements for %%cargo_* macros

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5-7
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-6
- Pass %%__cargo_common_opts to %%cargo_install

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-5
- Explicitly require rust/cargo

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-3
- Fix syntax error

* Tue Jan 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-2
- Remove Cargo.lock

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-1
- Update to 5

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-7
- Add Obsoletes for rust-rpm-macros

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-6
- Use cp instead of install

* Sat Oct 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-5
- Generate runtime dependencyon cargo for devel subpackages

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-2
- Include license

* Sat Jul 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-1
- Update to 4

* Fri Jun 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-5
- Explicitly set rustdoc path

* Wed Jun 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-4
- Mageia doesn't have C.UTF-8 lang

* Wed Jun 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-3
- Switch cargo_registry to /usr/share/cargo/registry

* Wed Jun 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-2
- Set C.UTF-8 for cargo inspector where python doesn't do locale coercing

* Tue Jun 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-1
- Initial package

