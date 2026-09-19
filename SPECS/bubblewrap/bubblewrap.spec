Summary:        setuid implementation of a subset of user namespaces.
Name:           bubblewrap
Version:        0.12.0
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/containers/bubblewrap/
Source0:        https://github.com/containers/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
BuildRequires:  libcap-devel
BuildRequires:  meson
BuildRequires:  ninja-build
Requires:       libcap

%description
Bubblewrap could be viewed as setuid implementation of a subset of user namespaces. Emphasis on subset - specifically relevant to the above CVE, bubblewrap does not allow control over iptables.

The original bubblewrap code existed before user namespaces - it inherits code from xdg-app helper which in turn distantly derives from linux-user-chroot.

%prep
%autosetup -p1

%build
%meson \
    -Dman=disabled \
    -Dselinux=disabled
%meson_build

%install
%meson_install

%check
%meson_test

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/bwrap
%{_datadir}/bash-completion/completions/bwrap
%{_datadir}/zsh/site-functions/_bwrap

%changelog
* Mon Sep 14 2026 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.12.0-1
- Auto-upgrade to 0.12.0 - for CVE-2026-87766
- Switch to the Meson build system, as upstream removed Autotools in 0.11.0
- Replace autoconf/automake/libtool build dependencies with meson and ninja-build
- Explicitly disable SELinux support to preserve prior behavior under
  Meson's --auto-features=enabled

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.0-1
- Auto-upgrade to 0.8.0 - Azure Linux 3.0 - package upgrades

* Tue Mar 08 2022 Andrew Phelps <anphel@microsoft.com> - 0.6.1-1
- Upgrade to version 0.6.1
- Disable documentation explicitly

* Mon Jul 19 2021 Thomas Crain <thcrain@microsoft.com> - 0.4.1-1
- Update to latest upstream version
- Lint spec, modernize with macros
- Remove CVE-2019-12439, CVE-2020-5291 patches. Both are patched in this version.

* Thu May 21 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.3.0-5
- Fixed CVE-2019-12439

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.3.0-4
- Added %%license line automatically

* Tue Apr 21 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.3.0-3
- Ignore CVE-2020-5291.
- Update Source0 and URL.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.3.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> - 0.3.0-1
- Updated to version 0.3.0.

* Thu Aug 03 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.1.8-1
- Initial build.  First version
