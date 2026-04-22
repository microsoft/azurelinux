# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:             adobe-mappings-pdf
Summary:          PDF mapping resources from Adobe
Version:          20190401
Release: 11%{?dist}
License:          BSD-3-Clause

URL:              https://www.adobe.com/
Source:           https://github.com/adobe-type-tools/mapping-resources-pdf/archive/%{version}.tar.gz#/mapping-resources-pdf-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    git
BuildRequires: make

%description
Mapping resources for PDF have a variety of functions, such as mapping CIDs
(Character IDs) to character codes, or mapping character codes to other
character codes.

These mapping resources for PDF should not be confused with CMap resources.
While both types of resources share the same file structure and syntax, they
have very different functions.

These PDF mapping resources are useful for some applications (e.g. Ghostscript)
to function properly.

# === SUBPACKAGES =============================================================

%package devel
Summary:          RPM macros for Adobe's PDF mapping resources
Requires:         %{name} = %{version}-%{release}

%description devel
This package is useful for development purposes only. It installs RPM
macros useful for building packages against %{name},
as well as all the fonts contained in this font set.


# === BUILD INSTRUCTIONS ======================================================

# NOTE: This package provides only resource files, which are already
#       "pre-compiled" to smallest size possible, but they still remain in
#       postscript format as intended. That's why there is no %%build phase.

%prep
%autosetup -n mapping-resources-pdf-%{version} -S git

%install
%make_install prefix=%{_prefix}

# Generate the macro containing the root path to our mappings files:
install -m 0755 -d %{buildroot}%{_rpmconfigdir}/macros.d

cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name} << _EOF
%%adobe_mappings_rootpath     %{_datadir}/adobe/resources/mapping/
_EOF

# === PACKAGING INSTRUCTIONS ==================================================

%files
%doc README.md
%license LICENSE.txt

%dir %{_datadir}/adobe
%dir %{_datadir}/adobe/resources
%dir %{_datadir}/adobe/resources/mapping

%{_datadir}/adobe/resources/mapping/pdf2other
%{_datadir}/adobe/resources/mapping/pdf2unicode

%files devel
%{_rpmconfigdir}/macros.d/macros.%{name}

# =============================================================================

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 21 2023 Richard Lescak <rlescak@redhat.com> - 20190401-4
- SPDX migration

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20190401-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 10 2022 Richard Lescak <rlescak@redhat.com> - 20190401-1
- Rebase to latest version

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 20180407-6
- remove mention of Fedora from desc

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180407-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20180407-1
- Rebase to latest upstream version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170901-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170901-2
- *-devel subpackage added

* Tue Sep 12 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170901-1
- Initial version of specfile
