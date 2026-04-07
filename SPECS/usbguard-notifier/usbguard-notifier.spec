# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           usbguard-notifier
Version:        0.1.1
Release:        2%{?dist}
Summary:        A tool for detecting usbguard policy and device presence changes

License:        GPL-2.0-or-later
URL:            https://github.com/Cropi/%{name}
Source0:        https://github.com/Cropi/usbguard-notifier/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Patch0:         remove-catch.patch

Requires: systemd

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: autoconf automake libtool make
BuildRequires: usbguard-devel
BuildRequires: librsvg2-devel
BuildRequires: libnotify-devel
BuildRequires: asciidoc
BuildRequires: systemd-rpm-macros

%description
USBGuard Notifier software framework detects usbguard policy modifications
as well as device presence changes and displays them as pop-up notifications.

%prep
%setup -q
%patch -P 0 -p1

%build
mkdir -p ./m4
autoreconf -i -f -v --no-recursive ./

export CXXFLAGS="$RPM_OPT_FLAGS"

%configure \
    --disable-silent-rules \
    --enable-debug-build

%set_build_flags
make %{?_smp_mflags}


%install
make install INSTALL='install -p' DESTDIR=%{buildroot}

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_bindir}/usbguard-notifier
%{_bindir}/usbguard-notifier-cli
%{_mandir}/man1/usbguard-notifier.1.gz
%{_mandir}/man1/usbguard-notifier-cli.1.gz
%{_userunitdir}/usbguard-notifier.service


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Apr 24 2025 Attila Lakatos <alakatos@redhat.com> - 0.1.1-1
- Rebase to 0.1.1
- Remove catch dependency
  resolves: rhbz#2270438

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Attila Lakatos <alakatos@redhat.com> - 0.1.0-1
- Rebase to 0.1.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Attila Lakatos <alakatos@redhat.com> - 0.0.6-5
- Merge notifications when inserting a usb device
  resolves: rhbz#1972505

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Radovan Sroka <rsroka@redhat.com> - 0.0.6-3
- Rebuild with the usbguard 1.0.0 - soname bump

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 29 2020 Attila Lakatos <alakatos@redhat.com> 0.0.6-1
- Rebase to 0.0.6

* Fri Feb 21 2020 Attila Lakatos <alakatos@redhat.com> 0.0.5-1
- Initial package
