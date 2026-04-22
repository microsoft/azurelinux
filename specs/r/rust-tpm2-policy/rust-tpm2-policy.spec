# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with check
%global debug_package %{nil}

%global crate tpm2-policy

Name:           rust-%{crate}
Version:        0.6.0
Release: 12%{?dist}
Summary:        Specify and send TPM2 policies to satisfy object authorization

# Upstream license specification: EUPL-1.2
License:        EUPL-1.2
URL:            https://crates.io/crates/tpm2-policy
Source:         %{crates_source}
Patch0:         tpm2-policy-fix-metadata.diff

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Specify and send TPM2 policies to satisfy object authorization.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires -a

%build
%cargo_build -a

%install
%cargo_install -a

%if %{with check}
%check
%cargo_test -a
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 12 2024 Miroslav Suchý <msuchy@redhat.com> - 0.6.0-8
- convert license to SPDX

* Tue Jan 30 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.0-7
- Fix build

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 07 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.0-4
- Rebuild for tss-esapi 7.2.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 19 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 0.5.3-1
- Update to 0.5.3

* Wed Nov 03 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 06 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0

* Mon Feb 15 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 0.3.1-3
- Update tss-esapi version requirements

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec  3 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Thu Dec  3 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Thu Aug 13 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Mon Aug 03 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 0.1.0-1
 - Initial package
