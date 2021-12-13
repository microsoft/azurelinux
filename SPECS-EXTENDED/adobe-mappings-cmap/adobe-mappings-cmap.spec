Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:             adobe-mappings-cmap
Summary:          CMap resources for Adobe's character collections
Version:          20171205
Release:          8%{?dist}
License:          BSD

URL:              https://www.adobe.com/
Source:           https://github.com/adobe-type-tools/cmap-resources/archive/%{version}.tar.gz#/cmap-resources-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    git

%description
CMap (Character Map) resources are used to unidirectionally map character codes,
such as Unicode encoding form, to CIDs (Character IDs -- meaning glyphs) of a
CIDFont resource.

These CMap resources are useful for some applications (e.g. Ghostscript) to
correctly display text containing Japanese, (Traditional) Chinese, or Korean
characters.

# === SUBPACKAGES =============================================================

%package deprecated
Summary:          Deprecated CMap resources for Adobe's character collections
Requires:         %{name} = %{version}-%{release}

%description deprecated
This sub-package contains currently deprecated CMap resources that some
applications might still require to function properly.

%package devel
Summary:          RPM macros for Adobe's CMap resources for character collections
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-deprecated = %{version}-%{release}

%description devel
This package is useful for Fedora development purposes only. It installs RPM
macros useful for building packages against %{name},
as well as all the fonts contained in this font set.

# === BUILD INSTRUCTIONS ======================================================

# NOTE: This package provides only resource files, which are already
#       "pre-compiled" to smallest size possible, but they still remain in
#       postscript format as intended. That's why there is no %%build phase.

%prep
%autosetup -n cmap-resources-%{version} -S git

%install
%make_install prefix=%{_prefix}

# Generate the macro containing the root path to our mappings files:
install -m 0755 -d %{buildroot}%{_rpmconfigdir}/macros.d

cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name} << _EOF
%%adobe_mappings_rootpath     %{_datadir}/adobe/resources/mapping/
_EOF

# === PACKAGING INSTRUCTIONS ==================================================

%files
%doc README.md VERSIONS.txt
%license LICENSE.txt

# Necessary directories ownership (to remove them correctly when uninstalling):
%dir %{_datadir}/adobe
%dir %{_datadir}/adobe/resources
%dir %{_datadir}/adobe/resources/mapping

%{_datadir}/adobe/resources/mapping/CNS1
%{_datadir}/adobe/resources/mapping/GB1
%{_datadir}/adobe/resources/mapping/Identity
%{_datadir}/adobe/resources/mapping/Japan1
%{_datadir}/adobe/resources/mapping/Korea1

%files deprecated
%{_datadir}/adobe/resources/mapping/deprecated

%files devel
%{_rpmconfigdir}/macros.d/macros.%{name}

# =============================================================================

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20171205-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20171205-2
- *-devel subpackage added

* Tue Jan 02 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20171205-1
- Rebase to latest upstream version

* Thu Nov 09 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20171024-1
- Rebase to latest upstream version

* Mon Sep 11 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170901-1
- Initial version of specfile
