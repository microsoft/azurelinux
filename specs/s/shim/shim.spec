# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# this is to make us only expand %%{dist} if we're on a modularity build.
# it's 2 macros make vim's \c not put a brace at the end of the changelog.
%global _dist %{expand:%{?_module_build:%%{?dist}}}


Name:		shim
Version:	15.8
Release: 4%{?dist}
Summary:	First-stage UEFI bootloader
License:	BSD-3-Clause
URL:		https://github.com/rhboot/shim/
BuildRequires:	efi-filesystem
BuildRequires:	efi-srpm-macros >= 5-1

ExclusiveArch:	%{efi}
# but we don't build a .i686 package, just a shim-ia32.x86_64 package
ExcludeArch:	%{ix86}
# but we don't build a .arm package, just a shim-arm.aarch64 package
ExcludeArch:	%{arm}

Source0:	shim.rpmmacros
Source1:	shim.conf

# keep these two lists of sources synched up arch-wise.  That is 0 and 10
# match, 1 and 11 match, ...
Source10:	BOOTAA64.CSV
Source20:	shimaa64.efi
Source11:	BOOTIA32.CSV
Source21:	shimia32.efi
Source12:	BOOTX64.CSV
Source22:	shimx64.efi
#Source13:	BOOTARM.CSV
#Source23:	shimarm.efi

%include %{SOURCE0}

BuildRequires:	pesign >= 0.112-20.fc27
# We need this because %%{efi} won't expand before choosing where to make
# the src.rpm in koji, and we could be on a non-efi architecture, in which
# case we won't have a valid expansion here...  To be solved in the future
# (shim 16+) by making the unsigned packages all provide "shim-unsigned", so
# we can just BuildRequires that.
%ifarch x86_64
BuildRequires: %{unsignedx64} = 15.8
BuildRequires: %{unsignedia32} = 15.8
%endif
%ifarch aarch64
BuildRequires: %{unsignedaa64} = 15.8
#BuildRequires: %% {unsignedarm} = %% {shimverarm}
%endif

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments. This package contains the version signed by
the UEFI signing service.

%define_pkg -a %{efi_arch} -p 1
%if %{efi_has_alt_arch}
%define_pkg -a %{efi_alt_arch}
%endif

%prep
cd %{_builddir}
rm -rf shim-%{version}
mkdir shim-%{version}

test -e %{shimdirx64}/$(basename %{shimefix64}) && cp -vf %{shimdirx64}/$(basename %{shimefix64}) %{shimefix64} ||:
test -e %{shimdiria32}/$(basename %{shimefiia32}) && cp -vf %{shimdiria32}/$(basename %{shimefiia32}) %{shimefiia32} ||:
test -e %{shimdiraa64}/$(basename %{shimefiaa64}) && cp -vf %{shimdiraa64}/$(basename %{shimefiaa64}) %{shimefiaa64} ||:
%build

cd shim-%{version}
%if %{efi_has_alt_arch}
%define_build -a %{efi_alt_arch} -A %{efi_alt_arch_upper} -i %{shimefialt} -b no -c %{is_alt_signed} -d %{shimdiralt}
%endif
%define_build -a %{efi_arch} -A %{efi_arch_upper} -i %{shimefi} -b no -c %{is_signed} -d %{shimdir}

%install
rm -rf $RPM_BUILD_ROOT
cd shim-%{version}
install -D -d -m 0755 $RPM_BUILD_ROOT/boot/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_root}/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_efi}/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_dir}/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_boot}/

%do_install -a %{efi_arch} -A %{efi_arch_upper} -b %{bootcsv}
%if %{efi_has_alt_arch}
%do_install -a %{efi_alt_arch} -A %{efi_alt_arch_upper} -b %{bootcsvalt}
%endif

%if %{provide_legacy_shim}
install -m 0700 %{shimefi} $RPM_BUILD_ROOT%{efi_esp_dir}/shim.efi
%endif
install -D -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/dnf/protected.d/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/dnf/protected.d/

( cd $RPM_BUILD_ROOT ; find .%{efi_esp_root} -type f ) \
  | sed -e 's/\./\^/' -e 's,^\\\./,.*/,' -e 's,$,$,' > %{__brp_mangle_shebangs_exclude_from_file}

%define_files -a %{efi_arch} -A %{efi_arch_upper}
%if %{provide_legacy_shim}
%{efi_esp_dir}/shim.efi
%endif
%{_sysconfdir}/dnf/protected.d/shim.conf

%if %{efi_has_alt_arch}
%define_files -a %{efi_alt_arch} -A %{efi_alt_arch_upper}
%{_sysconfdir}/dnf/protected.d/shim.conf
%endif

%changelog
* Tue Mar 19 2024 Peter Jones <pjones@redhat.com> - 15.8-3
- Fix fbx64/mmx64 signing.
  Related: rhbz#2189197

* Tue Mar 12 2024 Peter Jones <pjones@redhat.com> - 15.8-2
- Update to shim-15.8
  Resolves: CVE-2023-40546
  Resolves: CVE-2023-40547
  Resolves: CVE-2023-40548
  Resolves: CVE-2023-40549
  Resolves: CVE-2023-40550
  Resolves: CVE-2023-40551
  Resolves: rhbz#2113005
  Resolves: rhbz#2189197
  Resolves: rhbz#2238884
  Resolves: rhbz#2259264

* Thu Jul 07 2022 Robbie Harwood <rharwood@redhat.com> - 15.6-2
- Update aarch64 (only) with relocation fixes
- Resolves: #2101248

* Wed Jun 15 2022 Peter Jones <pjones@redhat.com> - 15.6-1
- Update to shim-15.6
  Resolves: CVE-2022-28737

* Wed May 05 2021 Javier Martinez Canillas <javierm@redhat.com> - 15.4-5
- Bump release to build for F35

* Wed Apr 21 2021 Javier Martinez Canillas <javierm@redhat.com> - 15.4-4
- Fix handling of ignore_db and user_insecure_mode (pjones)
- Fix booting on pre-UEFI Macs (pjones)
- Fix mok variable storage allocation region (glin)
  Resolves: rhbz#1948432
- Fix the package version in the .sbat data (pjones)

* Tue Apr 06 2021 Peter Jones <pjones@redhat.com> - 15.4-3
- Mark signed shim packages as protected in dnf.
  Resolves: rhbz#1874541
- Conflict with older fwupd, but don't require it.
  Resolves: rhbz#1877751

* Tue Apr 06 2021 Peter Jones <pjones@redhat.com> - 15.4-2
- Update to shim 15.4
  - Support for revocations via the ".sbat" section and SBAT EFI variable
  - A new unit test framework and a bunch of unit tests
  - No external gnu-efi dependency
  - Better CI
  Resolves: CVE-2020-14372
  Resolves: CVE-2020-25632
  Resolves: CVE-2020-25647
  Resolves: CVE-2020-27749
  Resolves: CVE-2020-27779
  Resolves: CVE-2021-20225
  Resolves: CVE-2021-20233

* Tue Oct 02 2018 Peter Jones <pjones@redhat.com> - 15-8
- Build a -8 because I can't tag -7 into f30 for pretty meh reasons.

* Tue Oct 02 2018 Peter Jones <pjones@redhat.com> - 15-7
- Rebuild just because I'm dumb.

* Tue Oct 02 2018 Peter Jones <pjones@redhat.com> - 15-6
- Put the legacy shim.efi binary in the right subpackage
  Resolves: rhbz#1631989

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 15-5
- Rework the .spec to use efi-rpm-macros.

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 15-4
- Fix directory permissions to be 0700 on FAT filesystems

* Mon Apr 30 2018 Peter Jones <pjones@redhat.com> - 15-3
- Pick a release value that'll be higher than what's in F28.

* Mon Apr 30 2018 Peter Jones <pjones@redhat.com> - 15-1
- Fix BOOT*.CSV and update release to -1

* Tue Apr 24 2018 Peter Jones <pjones@redhat.com> - 15-0.1
- Update to shim 15.
- more reproduceable build
- better checking for bad linker output
- flicker-free console if there's no error output
- improved http boot support
- better protocol re-installation
- dhcp proxy support
- tpm measurement even when verification is disabled
- more reproducable builds
- measurement of everything verified through shim_verify()
- coverity and scan-build checker make targets
- misc cleanups

* Tue Mar 06 2018 Peter Jones <pjones@redhat.com> - 13-5
- Back off to the thing we had in 13-0.8 until I get new signatures.

* Wed Feb 28 2018 Peter Jones <pjones@redhat.com> - 13-4
- Fix an inverted test that crept in in the signing macro.  (Woops.)

* Wed Feb 28 2018 Peter Jones <pjones@redhat.com> - 13-2
- Pivot the shim-signed package to be here.

* Wed Nov 01 2017 Peter Jones <pjones@redhat.com> - 13-1
- Now with the actual signed 64-bit build of shim 13 for x64 as well.
- Make everything under /boot/efi be mode 0700, since that's what FAT will
  show anyway, so that rpm -V is correct.
  Resolves: rhbz#1508516

* Tue Oct 24 2017 Peter Jones <pjones@redhat.com> - 13-0.8
- Now with signed 32-bit x86 build.
  Related: rhbz#1474861

* Wed Oct 04 2017 Peter Jones <pjones@redhat.com> - 13-0.7
- Make /boot/efi/EFI/fedora/shim.efi still exist on aarch64 as well.
  Resolves: rhbz#1497854

* Tue Sep 19 2017 Peter Jones <pjones@redhat.com> - 13-0.6
- Fix binary format issue on Aarch64
  Resolves: rhbz#1489604

* Tue Sep 05 2017 Peter Jones <pjones@redhat.com> - 13-0.5
- Make /boot/efi/EFI/fedora/shim.efi still exist on x86_64, since some
  machines have boot entries that point to it.

* Tue Aug 29 2017 Peter Jones <pjones@redhat.com> - 13-0.4
- Make our provides not get silently ignore by rpmbuild...

* Fri Aug 25 2017 Peter Jones <pjones@redhat.com> - 13-0.3
- x64: use the new fbx64.efi and mm64.efi as fallback.efi and MokManager.efi
- Provide: "shim" in x64 and aa64 builds

* Thu Aug 24 2017 Peter Jones <pjones@redhat.com> - 13-0.2
- Obsolete old shim builds.

* Tue Aug 22 2017 Peter Jones <pjones@redhat.com> - 13-0.1
- Initial (partially unsigned) build for multi-arch support on x64/ia32.

* Thu Mar 23 2017 Petr Šabata <contyk@redhat.com> - 0.8-9
- Re-enable dist tag for module builds

* Tue Feb 17 2015 Peter Jones <pjones@redhat.com> - 0.8-8
- Don't dual-sign shim-%%{efidir}.efi either.
  Resolves: rhbz#1184765

* Tue Feb 17 2015 Peter Jones <pjones@redhat.com> - 0.8-8
- Require dbxtool

* Wed Dec 17 2014 Peter Jones <pjones@redhat.com> - 0.8-7
- Wrong -signed changes got built for aarch64 last time, for dumb reasons.
  Related: rhbz#1170289

* Fri Dec 05 2014 Peter Jones <pjones@redhat.com> - 0.8-6
- Rebuild once more so we can use a different -unsigned version on different
  arches (because we can't tag a newer build into aarch64 without an x86
  update to match.)
  Related: rhbz#1170289

* Wed Dec 03 2014 Peter Jones <pjones@redhat.com> - 0.8-5
- Rebuild for aarch64 path fixes
  Related: rhbz#1170289

* Thu Oct 30 2014 Peter Jones <pjones@redhat.com> - 0.8-2
- Remove the dist tag so people don't complain about what it says.

* Fri Oct 24 2014 Peter Jones <pjones@redhat.com> - 0.8-1
- Update to shim 0.8
  rhbz#1148230
  rhbz#1148231
  rhbz#1148232
- Handle building on aarch64 as well

* Fri Jul 18 2014 Peter Jones <pjones@redhat.com> - 0.7-2
- Don't do multi-signing; too many machines screw up verification.
  Resolves: rhbz#1049749

* Wed Nov 13 2013 Peter Jones <pjones@redhat.com> - 0.7-1
- Update to shim 0.7
  Resolves: rhbz#1023767

* Thu Oct 24 2013 Peter Jones <pjones@redhat.com> - 0.5-1
- Update to shim 0.5

* Thu Jun 20 2013 Peter Jones <pjones@redhat.com> - 0.4-1
- Provide a fallback for uninitialized Boot#### and BootOrder
  Resolves: rhbz#963359
- Move all signing from shim-unsigned to here
- properly compare our generated hash from shim-unsigned with the hash of
  the signed binary (as opposed to doing it manually)

* Fri May 31 2013 Peter Jones <pjones@redhat.com> - 0.2-4.4
- Re-sign to get alignments that match the new specification.
  Resolves: rhbz#963361

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Peter Jones <pjones@redhat.com> - 0.2-3.3
- Add obsoletes and provides for earlier shim-signed packages, to cover
  the package update cases where previous versions were installed.
  Related: rhbz#888026

* Mon Dec 17 2012 Peter Jones <pjones@redhat.com> - 0.2-3.2
- Make the shim-unsigned dep be on the subpackage.

* Sun Dec 16 2012 Peter Jones <pjones@redhat.com> - 0.2-3.1
- Rebuild to provide "shim" package directly instead of just as a Provides:

* Sat Dec 15 2012 Peter Jones <pjones@redhat.com> - 0.2-3
- Also provide shim-fedora.efi, signed only by the fedora signer.
- Fix the fedora signature on the result to actually be correct.
- Update for shim-unsigned 0.2-3

* Mon Dec 03 2012 Peter Jones <pjones@redhat.com> - 0.2-2
- Initial build
