## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 13;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           clevis
Version:        21
Release:        %autorelease
Summary:        Automated decryption framework

License:        GPL-3.0-or-later
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:        clevis.sysusers

Patch0001:      0001-PKCS-11-pin-fix-dracut-for-unconfigured-device.patch
Patch0002:      0002-tpm2-use-first-pcr-algorithm-bank-supported-by.patch
Patch0003:      0003-Include-tpm2_getcap-as-dracut-required-binary.patch

BuildRequires:  git-core
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  asciidoc
BuildRequires:  ninja-build
BuildRequires:  bash-completion
BuildRequires:  bash-completion-devel

BuildRequires:  libjose-devel >= 8
BuildRequires:  libluksmeta-devel >= 8
BuildRequires:  audit-libs-devel
BuildRequires:  libudisks2-devel
BuildRequires:  openssl-devel

BuildRequires:  tpm2-tools >= 4.0.0
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
BuildRequires:  dracut
BuildRequires:  tang >= 6
BuildRequires:  curl
BuildRequires:  luksmeta
BuildRequires:  openssl
BuildRequires:  diffutils
BuildRequires:  cryptsetup
BuildRequires:  jq
BuildRequires:  pcsc-lite
BuildRequires:  opensc


Requires:       tpm2-tools >= 4.0.0
Requires:       coreutils
Requires:       jose >= 8
Requires:       curl
Requires:       jq
Requires(post): systemd
Requires:       clevis-pin-tpm2

%description
Clevis is a framework for automated decryption. It allows you to encrypt
data using sophisticated unlocking policies which enable decryption to
occur automatically.

The clevis package provides basic encryption/decryption policy support.
Users can use this directly; but most commonly, it will be used as a
building block for other packages. For example, see the clevis-luks
and clevis-dracut packages for automatic root volume unlocking of
LUKSv1/LUKSv2 volumes during early boot.

%package luks
Summary:        LUKS integration for clevis
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cryptsetup
Requires:       luksmeta >= 8

%description luks
LUKS integration for clevis. This package allows you to bind a LUKS
volume to a clevis unlocking policy. For automated unlocking, an unlocker
will also be required. See, for example, clevis-dracut and clevis-udisks2.

%package systemd
Summary:        systemd integration for clevis
Requires:       %{name}-luks%{?_isa} = %{version}-%{release}
%if 0%{?fedora} > 27
Requires:       systemd%{?_isa} >= 235-3
%else
%if 0%{?fedora} == 27
Requires:       systemd%{?_isa} >= 234-9
%else
%if 0%{?fedora} == 26
Requires:       systemd%{?_isa} >= 233-7
%else
Requires:       systemd%{?_isa} >= 236
%endif
%endif
%endif

%description systemd
Automatically unlocks LUKS _netdev block devices from /etc/crypttab.

%package dracut
Summary:        Dracut integration for clevis
Requires:       %{name}-systemd%{?_isa} = %{version}-%{release}
Requires:       dracut-network

%description dracut
Automatically unlocks LUKS block devices in early boot.

%package udisks2
Summary:        UDisks2/Storaged integration for clevis
Requires:       %{name}-luks%{?_isa} = %{version}-%{release}

%description udisks2
Automatically unlocks LUKS block devices in desktop environments that
use UDisks2 or storaged (like GNOME).

%package pin-pkcs11
Summary:        PKCS#11 for clevis
Requires:       %{name}-systemd%{?_isa} = %{version}-%{release}
Requires:       %{name}-luks%{?_isa} = %{version}-%{release}
Requires:       %{name}-dracut%{?_isa} = %{version}-%{release}
Requires:       pcsc-lite
Requires:       opensc
Requires:       socat
Requires:       openssl

%description pin-pkcs11
Automatically unlocks LUKS block devices through a PKCS#11 device.

%prep
%autosetup -S git

%build
%meson -Duser=clevis -Dgroup=clevis
%meson_build

%install
%meson_install
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/clevis.conf

%check
desktop-file-validate \
  %{buildroot}/%{_sysconfdir}/xdg/autostart/%{name}-luks-udisks2.desktop
%meson_test

%files
%license COPYING
%{_datadir}/bash-completion/
%{_bindir}/%{name}-decrypt-tang
%{_bindir}/%{name}-decrypt-tpm2
%{_bindir}/%{name}-decrypt-sss
%{_bindir}/%{name}-decrypt-null
%{_bindir}/%{name}-decrypt
%{_bindir}/%{name}-encrypt-tang
%{_bindir}/%{name}-encrypt-tpm2
%{_bindir}/%{name}-encrypt-sss
%{_bindir}/%{name}-encrypt-null
%{_bindir}/%{name}
%{_mandir}/man1/%{name}-encrypt-tang.1*
%{_mandir}/man1/%{name}-encrypt-tpm2.1*
%{_mandir}/man1/%{name}-encrypt-sss.1*
%{_mandir}/man1/%{name}-decrypt.1*
%{_mandir}/man1/%{name}.1*
%{_sysusersdir}/clevis.conf

%files luks
%{_mandir}/man7/%{name}-luks-unlockers.7*
%{_mandir}/man1/%{name}-luks-unlock.1*
%{_mandir}/man1/%{name}-luks-unbind.1*
%{_mandir}/man1/%{name}-luks-bind.1*
%{_mandir}/man1/%{name}-luks-list.1.*
%{_mandir}/man1/%{name}-luks-edit.1.*
%{_mandir}/man1/%{name}-luks-regen.1.*
%{_mandir}/man1/%{name}-luks-report.1.*
%{_mandir}/man1/%{name}-luks-pass.1.*
%{_bindir}/%{name}-luks-unlock
%{_bindir}/%{name}-luks-unbind
%{_bindir}/%{name}-luks-bind
%{_bindir}/%{name}-luks-common-functions
%{_bindir}/%{name}-luks-list
%{_bindir}/%{name}-luks-edit
%{_bindir}/%{name}-luks-regen
%{_bindir}/%{name}-luks-report
%{_bindir}/%{name}-luks-pass

%files systemd
%{_libexecdir}/%{name}-luks-askpass
%{_libexecdir}/%{name}-luks-unlocker
%{_unitdir}/%{name}-luks-askpass.path
%{_unitdir}/%{name}-luks-askpass.service

%files dracut
%dir %{_prefix}/lib/dracut/modules.d/60%{name}
%{_prefix}/lib/dracut/modules.d/60%{name}/clevis-hook.sh
%{_prefix}/lib/dracut/modules.d/60%{name}/module-setup.sh
%dir %{_prefix}/lib/dracut/modules.d/60%{name}-pin-null
%{_prefix}/lib/dracut/modules.d/60%{name}-pin-null/module-setup.sh
%dir %{_prefix}/lib/dracut/modules.d/60%{name}-pin-sss
%{_prefix}/lib/dracut/modules.d/60%{name}-pin-sss/module-setup.sh
%dir %{_prefix}/lib/dracut/modules.d/60%{name}-pin-tang
%{_prefix}/lib/dracut/modules.d/60%{name}-pin-tang/module-setup.sh
%dir %{_prefix}/lib/dracut/modules.d/60%{name}-pin-tpm2
%{_prefix}/lib/dracut/modules.d/60%{name}-pin-tpm2/module-setup.sh

%files udisks2
%{_sysconfdir}/xdg/autostart/%{name}-luks-udisks2.desktop
%attr(4755, root, root) %{_libexecdir}/%{name}-luks-udisks2

%files pin-pkcs11
%{_libexecdir}/%{name}-luks-pkcs11-askpass
%{_libexecdir}/%{name}-luks-pkcs11-askpin
%{_bindir}/%{name}-decrypt-pkcs11
%{_bindir}/%{name}-encrypt-pkcs11
%{_bindir}/%{name}-pkcs11-afunix-socket-unlock
%{_bindir}/%{name}-pkcs11-common
%{_unitdir}/%{name}-luks-pkcs11-askpass.service
%{_unitdir}/%{name}-luks-pkcs11-askpass.socket
%{_mandir}/man1/%{name}-encrypt-pkcs11.1*
%dir %{_prefix}/lib/dracut/modules.d/60%{name}-pin-pkcs11
%{_prefix}/lib/dracut/modules.d/60%{name}-pin-pkcs11/module-setup.sh
%{_prefix}/lib/dracut/modules.d/60%{name}-pin-pkcs11/%{name}-pkcs11-hook.sh
%{_prefix}/lib/dracut/modules.d/60%{name}-pin-pkcs11/%{name}-pkcs11-prehook.sh

%post systemd
systemctl preset %{name}-luks-askpass.path >/dev/null 2>&1 || :

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 21-13
- test: add initial lock files

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 25 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 21-11
- Drop call to %%sysusers_create_compat and include extra group in sysusers
  config

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Sergio Arroutbi <sarroutb@redhat.com> - 21-9
- Include packages required by clevis-pin-pkcs11

* Fri Nov 22 2024 Sergio Arroutbi <sarroutb@redhat.com> - 21-8
- Include tpm2_getcap as dracut required binary

* Tue Nov 12 2024 Sergio Arroutbi <sarroutb@redhat.com> - 21-7
- tpm2: use first PCR algorithm bank supported

* Thu Oct 17 2024 Sergio Correia <scorreia@redhat.com> - 21-6
- Follow-up fix from the pkcs11 subpackage split

* Thu Oct 17 2024 Sergio Arroutbi <sarroutb@redhat.com> - 21-5
- Split PKCS#11 files into clevis-pin-pkcs11 package

* Fri Oct 11 2024 Orion Poplawski <orion@nwra.com> - 21-4
- Fix ownership of directories in clevis-dracut

* Thu Oct 10 2024 Sergio Correia <scorreia@redhat.com> - 21-3
- Merge #33 `Change pscs-lite/opensc Requires to Recommends`

* Mon Sep 30 2024 Sergio Arroutbi <sarroutb@redhat.com> - 21-2
- Fix dracut unlocking

* Wed Sep 25 2024 Sergio Arroutbi <sarroutb@redhat.com> - 21-1
- Add new sources (release 21)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 03 2024 Sergio Correia <scorreia@redhat.com> - 20-2
- Make clevis-pin-tpm2 the default tpm2 pin
- Also remove cracklib-dicts dependency as it is not required anymore

* Fri Mar 08 2024 Sergio Arroutbi <sarroutb@redhat.com> - 20-1
- Add new sources (release 20)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Sergio Arroutbi <sarroutb@redhat.com> - 19-3
- Migrate to SPDX like licensing

* Tue Feb 28 2023 Sergio Arroutbi <sarroutb@redhat.com> - 19-2
- Include LUKSv2 volumes in description

* Thu Feb 02 2023 Sergio Correia <scorreia@redhat.com> - 19-1
- Update to latest upstream version, v19

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 18-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Sergio Arroutbi <sarroutb@redhat.com> - 18-15
- Backport upstream fixes

* Fri Aug 05 2022 Luca BRUNO <lucab@lucabruno.net> - 18-10
- Simplify sysusers.d fragment by using default 'nologin' shell

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 8 2022 Sergio Arroutbi <sarroutb@redhat.com> - 18-8
- Support a null pin

* Tue Jun 28 2022 Sergio Arroutbi <sarroutb@redhat.com> - 18-7
  Start clevis-luks-askpass.patch service according to global policy

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 29 2021 Sergio Correia <scorreia@redhat.com> - 18-5
  Account for unlocking failures in clevis-luks-askpass
  Resolves: rhbz#1878892

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 18-4
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Sergio Correia <scorreia@redhat.com> - 18-2
- Port to OpenSSL 3
  Backport of upstream commit (ee1dfedb)

* Thu Apr 15 2021 Sergio Correia <scorreia@redhat.com> - 18-1
- Update to new clevis upstream release, v18.

* Wed Apr 14 2021 Sergio Correia <scorreia@redhat.com> - 17-1
- Update to new clevis upstream release, v17.

* Tue Mar 16 2021 Sergio Correia <scorreia@redhat.com> - 16-2
- Fix for -t option in clevis luks bind - backport upstream commit ea0d0c20

* Tue Feb 09 2021 Sergio Correia <scorreia@redhat.com> - 16-1
- Update to new clevis upstream release, v16.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 08:14:40 GMT 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 15-3
- Upstream patch for tpm-tools 5.0 support

* Thu Oct 29 2020 Sergio Correia <scorreia@redhat.com> - 15-2
- Add jq to dependencies

* Wed Oct 28 2020 Sergio Correia <scorreia@redhat.com> - 15-1
- Update to new clevis upstream release, v15.

* Tue Sep 08 2020 Sergio Correia <scorreia@redhat.com> - 14-5
- Suppress output in pre scriptlet when adjusting users/groups
  Resolves: rhbz#1876729

* Tue Sep 08 2020 Sergio Correia <scorreia@redhat.com> - 14-4
- Backport upstream PR#230 - clevis-luks-askpass now exits cleanly
  when receives a SIGTERM
  Resolves: rhbz#1876001

* Sat Sep 05 2020 Sergio Correia <scorreia@redhat.com> - 14-3
- If clevis-luks-askpass is enabled, it may be using a wrong target,
  since that changed in v14. Check and update it, if required.

* Mon Aug 31 2020 Sergio Correia <scorreia@redhat.com> - 14-2
- Update sources file with new v14 release.

* Mon Aug 31 2020 Sergio Correia <scorreia@redhat.com> - 14-1
- Update to new clevis upstream release, v14.

* Sun Aug 02 2020 Benjamin Gilbert <bgilbert@redhat.com> - 13-3
- Downgrade cracklib-dicts to Recommends

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 10 2020 Sergio Correia <scorreia@redhat.com> - 13-1
- Update to new clevis upstream release, v13.

* Thu May 07 2020 Sergio Correia <scorreia@redhat.com> - 12-4
- cracklib-dicts should be also listed as a build dependency, since
  it's required for running some of the tests

* Mon Apr 06 2020 Sergio Correia <scorreia@redhat.com> - 12-3
- Make cracklib-dicts a regular dependency

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Sergio Correia <scorreia@redhat.com> - 12-1
- Update to new clevis upstream release, v12.

* Thu Dec 19 2019 Sergio Correia <scorreia@redhat.com> - 11-11
- Backport upstream PR#70 - Handle case where we try to use a partially
  used luksmeta slot
  Resolves: rhbz#1672371

* Thu Dec 05 2019 Sergio Correia <scorreia@redhat.com> - 11-10
- Disable LUKS2 tests for now, since they fail randomly in Koji
  builders, killing the build

* Wed Dec 04 2019 Sergio Correia <scorreia@redhat.com> - 11-9
- Backport of upstream patches and the following fixes:
  - Rework the logic for reading the existing key
  - fix for different output from 'luksAddKey' command w/cryptsetup v2.0.2 (
  - pins/tang: check that key derivation key is available

* Wed Oct 30 2019 Peter Robinson <pbrobinson@fedoraproject.org> 11-8
- Drop need network patch

* Fri Sep 06 2019 Javier Martinez Canillas <javierm@redhat.com> - 11-7
- Add support for tpm2-tools 4.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec  6 2018 Peter Robinson <pbrobinson@fedoraproject.org> 11-4
- Update patch for work around

* Thu Dec  6 2018 Peter Robinson <pbrobinson@fedoraproject.org> 11-3
- Work around network requirement for early boot

* Fri Nov 09 2018 Javier Martinez Canillas <javierm@redhat.com> - 11-2
- Delete remaining references to the removed http pin
- Install cryptsetup and tpm2_pcrlist in the initramfs
- Add device TCTI library to the initramfs
  Resolves: rhbz#1644876

* Tue Aug 14 2018 Nathaniel McCallum <npmccallum@redhat.com> - 11-1
- Update to v11

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 21 2018 Nathaniel McCallum <npmccallum@redhat.com> - 10-1
- Update to v10

* Tue Feb 13 2018 Nathaniel McCallum <npmccallum@redhat.com> - 9-1
- Update to v9

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 13 2017 Nathaniel McCallum <npmccallum@redhat.com> - 8-1
- Update to v8

* Wed Nov 08 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7-2
- Rebuild for cryptsetup-2.0.0

* Fri Oct 27 2017 Nathaniel McCallum <npmccallum@redhat.com> - 7-1
- Update to v7

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Nathaniel McCallum <npmccallum@redhat.com> - 6-1
- New upstream release
- Specify unprivileged user/group during configuration
- Move clevis user/group creation to base clevis package

* Mon Jun 26 2017 Nathaniel McCallum <npmccallum@redhat.com> - 5-1
- New upstream release
- Run clevis decryption from udisks2 under an unprivileged user

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 4-1
- New upstream release

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 3-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 18 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2-1
- New upstream release

* Mon Nov 14 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1-1
- First release

## END: Generated by rpmautospec
