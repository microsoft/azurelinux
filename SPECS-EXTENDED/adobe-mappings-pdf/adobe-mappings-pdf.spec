Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:             adobe-mappings-pdf
Summary:          PDF mapping resources from Adobe
Version:          20180407
Release:          6%{?dist}
License:          BSD

URL:              https://www.adobe.com/
Source:           https://github.com/adobe-type-tools/mapping-resources-pdf/archive/%{version}.tar.gz#/mapping-resources-pdf-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    git

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
This package is useful for Fedora development purposes only. It installs RPM
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
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20180407-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
