# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
%global forgeurl https://pagure.io/fonts-rpm-macros
Epoch: 1
Version: 2.0.5
%forgemeta

#https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/51
%global _spectemplatedir %{_datadir}/rpmdevtools/fedora
%global _docdir_fmt     %{name}
%global ftcgtemplatedir %{_datadir}/fontconfig/templates

# Master definition that will be written to macro files
%global _fontbasedir            %{_datadir}/fonts
%global _fontconfig_masterdir   %{_sysconfdir}/fonts
%global _fontconfig_confdir     %{_sysconfdir}/fonts/conf.d
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail

BuildArch: noarch

Name:      fonts-rpm-macros
Release: 24%{?dist}
Summary:   Build-stage rpm automation for fonts packages

License:   GPL-3.0-or-later
URL:       https://docs.fedoraproject.org/en-US/packaging-guidelines/FontsPolicy/
Source:    %{forgesource}
Patch0:    %{name}-omit-foundry-in-family.patch
Patch1:    %{name}-drop-yaml.patch
Patch2:    %{name}-epoch-in-req.patch
Patch3:    %{name}-fail-on-missing-files.patch
Patch4:    %{name}-spec-template-license-update.patch

Requires:  fonts-srpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:  fonts-filesystem  = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:  fontpackages-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: fontpackages-devel < %{?epoch:%{epoch}:}%{version}-%{release}
# Tooling dropped for now as no one was willing to maintain it
Obsoletes: fontpackages-tools < %{?epoch:%{epoch}:}%{version}-%{release}

Requires:  fontconfig
Requires:  libappstream-glib
Requires:  uchardet

# For the experimental generator
%if 0%{?fedora} || 0%{?rhel} < 10
Requires:  python3-ruamel-yaml
%endif
Requires:  python3-lxml

%description
This package provides build-stage rpm automation to simplify the creation of
fonts packages.

It does not need to be included in the default build root: fonts-srpm-macros
will pull it in for fonts packages only.

%package -n fonts-srpm-macros
Summary:   Source-stage rpm automation for fonts packages
Requires:  redhat-rpm-config
# macros.forge and forge.lua were split into a separate package.
# redhat-rpm-config pulls in forge-srpm-macros but better to explicitly Require
# it.
%if (0%{?fedora} >= 40 || 0%{?rhel} >= 10)
Requires:  forge-srpm-macros
%endif

%description -n fonts-srpm-macros
This package provides SRPM-stage rpm automation to simplify the creation of
fonts packages.

It limits itself to the automation subset required to create fonts SRPM
packages and needs to be included in the default build root.

The rest of the automation is provided by the fonts-rpm-macros package, that
fonts-srpm-macros will pull in for fonts packages only.

%package -n fonts-filesystem
Summary:   Directories used by font packages
License:   MIT

Provides:  fontpackages-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: fontpackages-filesystem < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n fonts-filesystem
This package contains the basic directory layout used by font packages,
including the correct permissions for the directories.

%package -n fonts-rpm-templates
Summary:   Example fonts packages rpm spec templates
License:   MIT

Requires:    fonts-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Supplements: fonts-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n fonts-rpm-templates
This package contains documented rpm spec templates showcasing how to use the
macros provided by fonts-rpm-macros to create fonts packages.

%prep
%forgesetup
%writevars -f rpm/macros.d/macros.fonts-srpm _fontbasedir _fontconfig_masterdir _fontconfig_confdir _fontconfig_templatedir
for template in templates/rpm/*\.spec ; do
  target=$(echo "${template}" | sed "s|^\(.*\)\.spec$|\1-bare.spec|g")
  grep -v '^%%dnl' "${template}" > "${target}"
  touch -r "${template}" "${target}"
done
%patch -P0 -p1
%if 0%{?rhel} >= 10
%patch -P1 -p1
%endif
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%install
install -m 0755 -d    %{buildroot}%{_fontbasedir} \
                      %{buildroot}%{_fontconfig_masterdir} \
                      %{buildroot}%{_fontconfig_confdir} \
                      %{buildroot}%{_fontconfig_templatedir}

install -m 0755 -vd   %{buildroot}%{_spectemplatedir}
install -m 0644 -vp   templates/rpm/*spec \
                      %{buildroot}%{_spectemplatedir}
install -m 0755 -vd   %{buildroot}%{ftcgtemplatedir}
install -m 0644 -vp   templates/fontconfig/*{conf,txt} \
                      %{buildroot}%{ftcgtemplatedir}

install -m 0755 -vd   %{buildroot}%{rpmmacrodir}
install -m 0644 -vp   rpm/macros.d/macros.fonts-* \
                      %{buildroot}%{rpmmacrodir}
install -m 0755 -vd   %{buildroot}%{_rpmluadir}/fedora/srpm
install -m 0644 -vp   rpm/lua/srpm/*lua \
                      %{buildroot}%{_rpmluadir}/fedora/srpm
install -m 0755 -vd   %{buildroot}%{_rpmluadir}/fedora/rpm
install -m 0644 -vp   rpm/lua/rpm/*lua \
                      %{buildroot}%{_rpmluadir}/fedora/rpm

install -m 0755 -vd   %{buildroot}%{_bindir}
install -m 0755 -vp   bin/* %{buildroot}%{_bindir}

%files
%license LICENSE.txt
%{_bindir}/fc-weight
%{_bindir}/gen-fontconf
%{rpmmacrodir}/macros.fonts-rpm*
%{_rpmluadir}/fedora/rpm/*.lua

%files -n fonts-srpm-macros
%license LICENSE.txt
%doc     *.md changelog.txt
%{rpmmacrodir}/macros.fonts-srpm*
%{_rpmluadir}/fedora/srpm/*.lua

%files -n fonts-filesystem
%dir %{_datadir}/fontconfig
%dir %{_fontbasedir}
%dir %{_fontconfig_masterdir}
%dir %{_fontconfig_confdir}
%dir %{_fontconfig_templatedir}

%files -n fonts-rpm-templates
%license LICENSE-templates.txt
%doc     *.md changelog.txt
%{_spectemplatedir}/*.spec
%dir %{ftcgtemplatedir}
%doc %{ftcgtemplatedir}/*conf
%doc %{ftcgtemplatedir}/*txt

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 27 2025 Parag Nemade <pnemade AT redhat DOT com> - 1:2.0.5-22
- Update license to use SPDX license expression in spec file templates
  Resolves: rhbz#2253660

* Mon Jan 20 2025 Akira TAGOH <tagoh@redhat.com> - 1:2.0.5-21
- Do not fail as "fonts not found for appstream file" if fontappstreams is defined.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 13 2024 Akira TAGOH <tagoh@redhat.com> - 1:2.0.5-19
- Add exact binary name in the file list.
- Do not package backup files.

* Tue Aug 13 2024 Akira TAGOH <tagoh@redhat.com> - 1:2.0.5-18
- Fail on missing files in macros
  Resolves: rhbz#2296502

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Akira TAGOH <tagoh@redhat.com> - 1:2.0.5-16
- Add %%{epoch} in Requires line if needed
- Support fontpkgheader macro for meta packages.

* Mon Jun  3 2024 Akira TAGOH <tagoh@redhat.com> - 1:2.0.5-15
- Drop YAML support in gen-fontconf for RHEL10 or later.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Parag Nemade <pnemade AT redhat DOT com> - 1:2.0.5-10
- Update license tag to SPDX format

* Fri Aug 19 2022 Akira TAGOH <tagoh@redhat.com> - 1:2.0.5-9
- Omit foundry name in family name.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 17:00:05 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1:2.0.5-3
- Insert Epoch in Requires/Provides/Obsoletes

* Sat May 23 09:03:10 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1:2.0.5-2
- Revert to 2.0.5

* Tue Apr 28 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 3.0.3-1
🐞 Fix bugs in the 3.0.2 refactoring
- 3.0.2-1
🐞 Workaround Fedora problems created by rpm commit 93604e2
   harder

* Mon Apr 27 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 3.0.1-1
🐞 Workaround Fedora problems created by rpm commit 93604e2

* Fri Apr  3 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.5-1
✅ do not add empty urls to appstream files

* Thu Apr  2 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.4-2
✅ validate fontconfig files by default

* Sat Feb 29 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.3-1
✅ minor rpmlint-oriented fixlets

* Sat Feb 22 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.2-1
✅ improve experimental fontconfig configuration generator

* Thu Feb 20 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.1-3
✅ limit descriptions to 80 columns

* Fri Feb 14 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.1-2
✅ use fonts packaging guidelines as URL
- 2.0.1-1
✅ first 2.x version proposed to Fedora, after FPC approval
   https://meetbot-raw.fedoraproject.org/fedora-meeting-1/2020-02-13/fpc.2020-02-13-17.00.txt

* Mon Nov 11 2019 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.0-1
✅ transform into fonts-rpm-macros
✅ major rpm macro and rpm spec template rework


* Mon Nov 10 2008 Nicolas Mailhot <nim@fedoraproject.org>
- 1.0-1
✅ initial release
