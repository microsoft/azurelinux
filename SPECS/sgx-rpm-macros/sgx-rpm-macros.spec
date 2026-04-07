# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: sgx-rpm-macros
Version: 1
Release: 3%{?dist}
License: MIT-0
Summary: RPM macros for working with the SGX SDK

Source0: macros.sgx
Source1: MIT-0

BuildArch: noarch

%description
RPM macros for working with the SGX SDK

%build
cp %{SOURCE1} MIT-0

%install
%__install -d %{buildroot}/%{_rpmmacrodir}/
cp %{SOURCE0} %{buildroot}/%{_rpmmacrodir}/

%files
%license MIT-0
%{_rpmmacrodir}/macros.sgx

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 29 2024 Daniel P. Berrangé <berrange@redhat.com> - 1-1
- Initial package (rhbz#2337576)
