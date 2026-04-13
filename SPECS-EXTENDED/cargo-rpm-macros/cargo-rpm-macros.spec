Vendor:         Microsoft Corporation
Distribution:   Azure Linux	
%bcond_without check
 
Name:           cargo-rpm-macros
Version:        28.4
Release:        1%{?dist}
Summary:        RPM macros and generators for building Rust packages with cargo
License:        MIT
 
URL:            https://codeberg.org/rust2rpm/cargo-rpm-macros
Source:         %{url}/archive/v%{version}.tar.gz
 
# temporary patch for compatibility with RHEL / ELN:
# The %%cargo_prep macro in RHEL / ELN accepts a -V flag. Using the same spec
# file for both Fedora and ELN would cause spec file parsing errors because
# the -V flag is not known in Fedora.
Patch:          0001-Temporarily-accept-cargo_prep-V-flag-for-spec-compat.patch
 
BuildArch:      noarch
 
%if %{with check}
BuildRequires:  python3-pytest
%endif
 
# obsolete + provide rust-packaging (removed in Fedora 38)
Obsoletes:      rust-packaging < 24
Provides:       rust-packaging = %{version}-%{release}

Requires:       cargo
Requires:       gawk
Requires:       grep
  
%description
%{summary}.

%prep
%autosetup -n cargo-rpm-macros -p1
 
%build
# nothing to do
 
%install
install -D -p -m 0644 -t %{buildroot}/%{_rpmmacrodir} macros.d/macros.cargo
install -D -p -m 0644 -t %{buildroot}/%{_rpmmacrodir} macros.d/macros.cargo-buildsys
install -D -p -m 0644 -t %{buildroot}/%{_rpmmacrodir} macros.d/macros.rust
install -D -p -m 0644 -t %{buildroot}/%{_fileattrsdir} fileattrs/cargo.attr
install -D -p -m 0644 -t %{buildroot}/%{_fileattrsdir} fileattrs/cargo_vendor.attr
 
%if %{with check}
%check
export MACRO_DIR=%{buildroot}%{_rpmmacrodir}
# Skip Fedora-specific assertions that hardcode /usr/bin paths and full rust_arches.
pytest -vv \
	-k 'not test_cargo_prep and not test_cargo_prep_vendor and not test_cargo_prep_no_replacement and not test_cargo_install and not test_rust_arches'
%endif
 
%files
%license LICENSE
%{_rpmmacrodir}/macros.cargo
%{_rpmmacrodir}/macros.cargo-buildsys
%{_rpmmacrodir}/macros.rust
%{_fileattrsdir}/cargo.attr
%{_fileattrsdir}/cargo_vendor.attr

%changelog
* Sat Dec 20 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 26.4-1
- Initial CBL-Mariner import from Fedora 43 (license: MIT).
- License verified
