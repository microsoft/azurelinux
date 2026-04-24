# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         min_qt_version 5.12
%global         min_kf_version 5.66

# uncomment to enable bootstrap mode
#global bootstrap 1

%if !0%{?bootstrap}
%global tests 1
%endif

Name:           kio-fuse
Version:        5.1.0
Release: 10%{?dist}
Summary:        KIO FUSE

License:        GPL-3.0-or-later
URL:            https://invent.kde.org/system/kio-fuse
Source0:        https://download.kde.org/stable/%{name}/%{name}-%{version}.tar.xz
Source1:        https://download.kde.org/stable/%{name}/%{name}-%{version}.tar.xz.sig
Source2:        gpgkey-21EC3FD75D26B39E820BE6FBD27C2C1AF21D8BAD.gpg

## upstream fixes
# Data loss on remote mount when using rmdir in terminal
# https://bugs.kde.org/show_bug.cgi?id=482902
Patch0:         kio-fuse-5.1.0-use-KIO__rmdir-for-unlinking-directories.patch

BuildRequires:  cmake
BuildRequires:  gnupg2
BuildRequires:  gcc-c++
BuildRequires:  systemd
BuildRequires:  kf6-rpm-macros
BuildRequires:  extra-cmake-modules  >= %{min_kf_version}

BuildRequires:  pkgconfig(fuse3)

BuildRequires:  cmake(Qt6Core)       >= %{min_qt_version}
BuildRequires:  cmake(Qt6Test)       >= %{min_qt_version}

BuildRequires:  cmake(KF6KIO)        >= %{min_kf_version}
BuildRequires:  cmake(KF6CoreAddons) >= %{min_kf_version}

%if 0%{?tests}
BuildRequires:  dbus-x11
BuildRequires:  kio-extras
BuildRequires:  fuse3
%endif

Requires:       systemd
Requires:       dbus-common

%description
KioFuse works by acting as a bridge between KDE's KIO filesystem design and
FUSE.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1


%build
%cmake_kf6 -DBUILD_TESTING:BOOL=%{?tests:ON}%{!?tests:OFF} \
	-DQT_MAJOR_VERSION=6

%cmake_build


%install
%cmake_install


%check
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
dbus-launch --exit-with-session \
%ctest --timeout 30 ||:
%endif


%files
%license LICENSES/GPL-3.0-or-later.txt
%doc README.md DESIGN.md
%{_libexecdir}/kio-fuse
%{_userunitdir}/kio-fuse.service
%{_kf6_datadir}/dbus-1/services/org.kde.KIOFuse.service
%{_tmpfilesdir}/%{name}-tmpfiles.conf


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 5.1.0-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 12 2024 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.1.0-5
- added patch to fix #2274653

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 31 2023 Marie Loise Nolden <loise@kde.org> - 5.1.0-2
- use Qt6/KF6

* Tue Dec 12 2023 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.1.0-1
- version 5.1.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.0.1-1
- version 5.0.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.0.0-4
- pull in upstream crash fix
- move BR: make inside '%%if %%{tests}' (only explicitly used there)

* Sat Jan  9 16:34:01 MSK 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.0.0-3
- ignore exit status of `make test`

* Sat Jan  9 16:15:31 MSK 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.0.0-2
- cleaned up build dependicies & tests enabled

* Fri Jan  1 15:55:51 MSK 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.0.0-1
- version 5.0.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.95.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 4.95.0-1
- first spec for version 4.95.0

