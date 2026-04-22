# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global candidate rc1

Name:    tpm2-tools
Version: 5.7
Release: 5%{?candidate:.%{candidate}}%{?dist}
Summary: A bunch of TPM testing toolS build upon tpm2-tss

License: BSD-3-Clause
URL:     https://github.com/tpm2-software/tpm2-tools
Source0: https://github.com/tpm2-software/tpm2-tools/releases/download/%{version}%{?candidate:-%{candidate}}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.gz

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: autoconf-archive
%if ! 0%{?rhel}
BuildRequires: pandoc
%endif
BuildRequires: pkgconfig(cmocka)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(openssl)
# tpm2-tss-devel provides tss2-mu/sys/esys package config
BuildRequires: pkgconfig(tss2-mu) >= 3.1.0
BuildRequires: pkgconfig(tss2-sys) >= 3.1.0
BuildRequires: pkgconfig(tss2-esys) >= 3.1.0
BuildRequires: pkgconfig(uuid)

# tpm2-tools is heavily depending on TPM2.0-TSS project, matched tss is required
Requires: tpm2-tss%{?_isa} >= 3.1.0

%description
tpm2-tools is a batch of tools for tpm2.0. It is based on tpm2-tss.

%prep
%autosetup -p1 -n %{name}-%{version}%{?candidate:-%{candidate}}

%build
%configure --prefix=/usr --disable-static --disable-silent-rules
%make_build

%install
%make_install

%files
%license docs/LICENSE
%doc docs/README.md docs/CHANGELOG.md
%{_bindir}/tpm2
%{_bindir}/tpm2_*
%{_bindir}/tss2
%{_bindir}/tss2_*
%{_datadir}/bash-completion/completions/tpm2*
%{_datadir}/bash-completion/completions/tss2*
%{_mandir}/man1/tpm2_*.1.gz
%{_mandir}/man1/tpm2.1.gz
%{_mandir}/man1/tss2_*.1.gz

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Apr 28 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 5.7-1
- Update to 5.7

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 12 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 5.6-1
- Update to 5.6

* Tue Sep 26 2023 Štěpán Horáček <shoracek@redhat.com> - 5.5-5
- Migrate license to SPDX

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 17 2023 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 5.5-3
- Disable compiler optimization to fix LTO + FORTIFY_SOURCE=3 issue
  Resolves rhbz#2171376

* Tue Feb 21 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.5-2
- Disable manpage regeneration in RHEL/ELN builds

* Thu Feb 16 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 5.5-1
- Update to 5.5

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.5-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 5.5-0.1.rc1
- Update to 5.5-RC1
- Enable LTO (RHBZ#1986628)

* Thu Dec 08 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 5.4-1
- Update to 5.4

* Wed Sep 28 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 5.3-1
- Update to 5.3

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 02 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 5.2-1
- Update to 5.2

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 5.1.1-3
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1
- Fixes CVE-2021-3565 (rhbz 1964428)

* Tue May 25 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 5.1-1
- Update to 5.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 5.0-1
- Update tp tpm2-tools 5.0

* Sat Aug 29 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 4.3.0-1
- Update to 4.3.0

* Mon Aug 10 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 4.2.1-4
- Rebuild for tpm2-tss 3.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 4.2.1-2
- Disable LTO due to latent uninitialized variable exposed by LTO

* Wed May 27 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 4.2.1-1
- Update to 4.2.1

* Tue Apr 14 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 4.2-1
- Update to 4.2

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Yunying Sun <yunying.sun@intel.com> - 4.1-1
- Update to 4.1 release

* Tue Oct 29 2019 Yunying Sun <yunying.sun@intel.com> - 4.0.1-1
- Update to 4.0.1 release

* Tue Sep 10 2019 Peter Robinson <pbrobinson@fedoraproject.org> 4.0-1
- Update to 4.0

* Fri Sep  6 2019 Javier Martinez Canillas <javierm@redhat.com> 4.0-0.4-rc2
- Use a release tarball instead of a source code tarball

* Fri Sep  6 2019 Peter Robinson <pbrobinson@fedoraproject.org> 4.0-0.3-rc2
- Update to 4.0 RC2

* Tue Aug 27 2019 Peter Robinson <pbrobinson@fedoraproject.org> 4.0-0.2-rc1
- Update to 4.0 RC1

* Tue Aug 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 4.0-0.1-rc0
- Update to 4.0 RC0

* Thu Aug  1 2019 Peter Robinson <pbrobinson@fedoraproject.org> 3.2.0-3
- Fix for crash for max PCRs available

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Yunying Sun <yunying.sun@intel.com> - 3.2.0-1
- Update to 3.2.0 release
- Removed patches since all have been included in 3.2.0 release

* Fri May 10 2019 Javier Martinez Canillas <javierm@redhat.com> - 3.1.4-2
- Allow tpm2_makecredential to run without a TPM (jetwhiz)
- Add tpm2_pcrreset and tpm2_checkquote tools (jetwhiz)

* Fri Mar 15 2019 Yunying Sun <yunying.sun@intel.com> - 3.1.4-1
- Update to 3.1.4 release
- Removed the 4 patches since all have been included in 3.1.4 release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 7 2019 Javier Martinez Canillas <javierm@redhat.com> - 3.1.3-3
- Fix broken -T option when passing additional arguments

* Mon Jan 7 2019 Javier Martinez Canillas <javierm@redhat.com> - 3.1.3-2
- Fix broken -T option and a couple of minor fixes
- Add pandoc BuildRequires

* Wed Nov 7 2018 Yunying Sun <yunying.sun@intel.com> - 3.1.3-1
- Update to 3.1.3 release

* Wed Sep 12 2018 Javier Martinez Canillas <javierm@redhat.com> - 3.1.2-1
- Update to 3.1.2 release
- Restore TCTI configuration environment for tools
- Restore tpm2_getcap tool properties output
  Resolves: rhbz#1625647

* Sat Jul 14 2018 Javier Martinez Canillas <javierm@redhat.com> - 3.1.1-3
- Revert backward incompatible change that removes default object attributes

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Yunying Sun <yunying.sun@intel.com> - 3.1.1-1
- Update to 3.1.1 release

* Thu Jul 5 2018 Yunying Sun <yunying.sun@intel.com> - 3.1.0-1
- Update Requires version of tpm2-tss to 2.0.0
- Remove BuildRequires for tcti-abrmd since it is optional
- Remove BuildRequires for tcti-{device,mssim} as it is now dynamically loaded
- Update to 3.1.0 release

* Mon Apr 30 2018 Javier Martinez Canillas <javierm@redhat.com> - 3.0.4-1
- Update URLs to point to the new project location
- Update to 3.0.4 release

* Wed Feb 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 3.0.3-3
- Remove ExclusiveArch: x86_64 directive

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Javier Martinez Canillas <javierm@redhat.com> - 3.0.3-1
- Update to 3.0.3 release

* Mon Dec 18 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0.2-1
- Update to 3.0.2 release

* Tue Dec 12 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0.1-1
- Update to 3.0.1 release (RHBZ#1512743)
- Download the generated tarball provided instead of the source code tarball

* Fri Dec 08 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0-1
- Update to 3.0 release

* Wed Nov 29 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0-0.1.rc1
- Update to 3.0 release candidate 1
- Update URLs to point to the new project location
- Make the package to obsolete version 2.1.1

* Wed Nov 01 2017 Javier Martinez Canillas <javierm@redhat.com> - 2.1.1-1
- Rename remaining tpm2.0-tools prefixes to tpm2-tools
- Remove global pkg_prefix since now the upstream repo and package names match
- Remove downstream patches since now these are in the latest upstream release
- Update to 2.1.1 release (RHBZ#1504438)

* Thu Oct 19 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 2.1.0-7
- Clean up potential memleak (RHBZ#1503959)

* Thu Oct 05 2017 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-6
- Add tpm2-abrmd-devel BuildRequires so tools have abrmd support (RHBZ#1498909)

* Fri Aug 18 2017 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-5
- Remove unneeded source tarballs (RHBZ#1482830)

* Tue Aug 15 2017 Sun Yunying <yunying.sun@intel.com> - 2.1.0-4
- Add patch to fix build error when openssl-devel is installed(RHBZ#1481236)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Sun Yunying <yunying.sun@intel.com> - 2.1.0-2
- Add patch to fix gcc7 complaining about implicit-fallthrough cases

* Fri Jul 28 2017 Sun Yunying <yunying.sun@intel.com> - 2.1.0-1
- Update to latest upstream release 2.1.0

* Fri Jul 28 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-9
- Update Requires dependency so that tpm2-tss update won't break tpm2-tools

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-7
- Only update release version to make fedpkg build works for f26

* Wed Mar 1 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-6
- Update tpm2-tss version to 1.0-3 to fix broken dependency on f26

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-4
- Dependency check failed for Requires again, here to fix this
- Update release version and changelog

* Thu Jan 19 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-3
- Change spec file permission to 644 to avoid rpmlint complain
- Update Requires to fix dependency check error reported in Bodhi
- Remove tpm2-tss-devel version in BuildRequires comment
- Update release version and changelog

* Wed Dec 21 2016 Sun Yunying <yunying.sun@intel.com> - 1.1.0-2
- Remove pkg_version to avoid dupliate use of version
- Remove redundant BuildRequires for autoconf/automake/pkgconfig
- Add comments for BuildRequires of sapi/tcti-device/tcti-socket
- Use ExclusiveArch instead of ExcludeArch
- Requires tpm2-tss version updated to 1.0-2
- Updated release version and changelog

* Fri Dec 2 2016 Sun Yunying <yunying.sun@intel.com> - 1.1.0-1
- Initial version of the package
