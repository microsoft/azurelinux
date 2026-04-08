# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:             adobe-mappings-cmap
Summary:          CMap resources for Adobe's character collections
Version:          20231115
Release:          3%{?dist}
License:          BSD-3-Clause

URL:              https://www.adobe.com/
Source:           https://github.com/adobe-type-tools/cmap-resources/archive/%{version}.tar.gz#/cmap-resources-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    git
BuildRequires: make

# The cmap-resources package duplicated this one (albeit with different
# installation paths). It was retired for F36. Provide an upgrade path.
%global crversion %(echo '%{version}' | \
    awk '{print substr($0,1,4)"."substr($0,5,2)"."substr($0,7)}')
Provides:         cmap-resources = %{crversion}-6.%{release}
Obsoletes:        cmap-resources < 2019.07.30-6
Provides:         cmap-resources-cns1-6 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-cns1-6 < 2019.07.30-6
Provides:         cmap-resources-cns1-7 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-cns1-7 < 2019.07.30-6
Provides:         cmap-resources-gb1-5 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-gb1-5 < 2019.07.30-6
Provides:         cmap-resources-japan1-7 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-japan1-7 < 2019.07.30-6
Provides:         cmap-resources-korea1-2 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-korea1-2 < 2019.07.30-6
Provides:         cmap-resources-identity-0 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-identity-0 < 2019.07.30-6
Provides:         cmap-resources-kr-9 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-kr-9 < 2019.07.30-6

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

Provides:         cmap-resources-japan2-0 = %{crversion}-6.%{release}
Obsoletes:        cmap-resources-japan2-0 < 2019.07.30-6

%description deprecated
This sub-package contains currently deprecated CMap resources that some
applications might still require to function properly.

%package devel
Summary:          RPM macros for Adobe's CMap resources for character collections
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-deprecated = %{version}-%{release}

%description devel
This package is useful for development purposes only. It installs RPM
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
%license LICENSE.md

# Necessary directories ownership (to remove them correctly when uninstalling):
%dir %{_datadir}/adobe
%dir %{_datadir}/adobe/resources
%dir %{_datadir}/adobe/resources/mapping

%{_datadir}/adobe/resources/mapping/CNS1
%{_datadir}/adobe/resources/mapping/GB1
%{_datadir}/adobe/resources/mapping/Identity
%{_datadir}/adobe/resources/mapping/Japan1
%{_datadir}/adobe/resources/mapping/Korea1
%{_datadir}/adobe/resources/mapping/KR
%{_datadir}/adobe/resources/mapping/Manga1

%files deprecated
%{_datadir}/adobe/resources/mapping/deprecated

%files devel
%{_rpmconfigdir}/macros.d/macros.%{name}

# =============================================================================

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20231115-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20231115-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 17 2024 Zdenek Dohnal <zdohnal@redhat.com> - 20231115-1
- 20231115 (fedora#2239976)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230622-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230622-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230622-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 Richard Lescak <rlescak@redhat.com> - 20230622-1
- rebase to version 20230622 (#2216272)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230118-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Richard Lescak <rlescak@redhat.com> - 20230118-2
- SPDX migration

* Thu Jan 19 2023 Richard Lescak <rlescak@redhat.com> - 20230118-1
- Rebase to version 20230118 (#2162105)

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20190730-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20190730-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20190730-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20190730-2
- Add Provides/Obsoletes to support “cmap-resources” retirement

* Wed Oct 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20190730-1
- Update to 20190730 (close RHBZ#2013684)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20171205-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 20171205-8
- remove mention of Fedora from desc

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
