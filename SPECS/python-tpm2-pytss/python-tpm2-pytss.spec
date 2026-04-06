# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name tpm2-pytss
%global _name tpm2_pytss

Name:           python-%{pypi_name}
Version:        2.3.0
Release:        9%{?dist}
Summary:        TPM 2.0 TSS Bindings for Python

License:        BSD-2-Clause
URL:            https://github.com/tpm2-software/tpm2-pytss
Source:         %{pypi_source %{pypi_name}}
# https://github.com/tpm2-software/tpm2-pytss/pull/585
Patch1:         %{name}-2.3.0-secp192.patch
# https://github.com/tpm2-software/tpm2-pytss/pull/589
Patch2:         %{name}-bsd.patch
# https://github.com/tpm2-software/tpm2-pytss/pull/615
Patch3:         %{name}-gcc15.patch
# cryptograpy: add copy dunder for private keys
# cryptography >= 45.0.0 requires the copy dunder for private key implementations.
# https://github.com/tpm2-software/tpm2-pytss/commit/6ab4c74e6fb3da7cd38e97c1f8e92532312f8439
Patch4:         %{name}-copy-dunder.patch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
%if %{undefined rhel}
BuildRequires:  python3-pytest-xdist
%endif
BuildRequires:  tpm2-tss-devel >= 2.0.0
BuildRequires:  gcc
# for tests
BuildRequires:  swtpm
BuildRequires:  tpm2-tools

%global _description %{expand:
TPM2 TSS Python bindings for Enhanced System API (ESYS), Feature API (FAPI),
Marshaling (MU), TCTI Loader (TCTILdr) and RC Decoding (rcdecode) libraries.
It also contains utility methods for wrapping keys to TPM 2.0 data structures
for importation into the TPM, unwrapping keys and exporting them from the TPM,
TPM-less makecredential command and name calculations, TSS2 PEM Key format
support, importing Keys from PEM, DER and SSH formats, conversion from
tpm2-tools based command line strings and loading tpm2-tools context files.
}

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{_name}


%check
%pyproject_check_import
# The test test_tools_decode_tpml_tagged_tpm_property checks TPM2 revision which is not stable
# In upstream this test as well as the tools are removed so I do not have any good way to fix it
%ifarch s390x
# this test does not work for some reason on the s390x as it times out
%global testargs -k "not test_spi_helper_good and not test_tools_decode_tpml_tagged_tpm_property"
%else
%global testargs -k "not test_tools_decode_tpml_tagged_tpm_property"
%endif
%pytest --import-mode=append %{?!rhel:-n 1} %{?testargs}


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.3.0-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.3.0-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.3.0-6
- Patch for cryptography 45; fixes RHBZ#2372172

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.3.0-5
- Rebuilt for Python 3.14

* Wed Feb 05 2025 Jakub Jelen <jjelen@redhat.com> - 2.3.0-4
- Fix build with gcc15 (#2341227)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Jakub Jelen <jjelen@redhat.com> - 2.3.0-1
- New upstream release (#2295581)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.2.1-3
- Rebuilt for Python 3.13

* Mon May 27 2024 Jakub Jelen <jjelen@redhat.com> - 2.2.1-2
- Fix build issue in rawhide (#2283520)

* Tue Mar 05 2024 Jakub Jelen <jjelen@redhat.com> - 2.2.1-1
- New upstream release (#2149103)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 16 2023 Jakub Jelen <jjelen@redhat.com> - 2.1.0-3
- Enable tests on i686 again

* Wed Aug 16 2023 Jakub Jelen <jjelen@redhat.com> - 2.1.0-2
- Enable builds on i686 again
- Fix another test issues

* Mon Aug 07 2023 Jakub Jelen <jjelen@redhat.com> - 2.1.0-1
- New upstream release (#2149103)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.2.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Jakub Jelen <jjelen@redhat.com> - 1.2.0-1
- Official Fedora package (#2135713)

* Tue Apr 12 2022 Traxtopel <traxtopel@gmail.com> - 1.1.0-1
- Initial package.
