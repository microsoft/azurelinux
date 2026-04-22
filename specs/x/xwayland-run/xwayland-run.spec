# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           xwayland-run
Version:        0.0.4
Release: 13%{?dist}
Summary:        Set of utilities to run headless X/Wayland clients

License:        GPL-2.0-or-later
URL:            https://gitlab.freedesktop.org/ofourdan/xwayland-run
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz

# https://gitlab.freedesktop.org/ofourdan/xwayland-run/-/merge_requests/19
Patch1: 0001-wlheadless-Ignore-os.waitpid-1-0-error.patch

BuildArch:      noarch

BuildRequires:  meson >= 0.60.0
BuildRequires:  git-core
BuildRequires:  python3-devel
Requires:       (weston or cage or kwin-wayland or mutter or gnome-kiosk)
Requires:       xorg-x11-server-Xwayland
Requires:       dbus-daemon
Requires:       xorg-x11-xauth

# Handle preference for boolean dep on compositor
%if 0%{?rhel}
Suggests:       mutter
%else
Suggests:       weston
%endif

# Provide names of the other utilities included
Provides:       wlheadless-run = %{version}-%{release}
Provides:       xwfb-run = %{version}-%{release}

%description
xwayland-run contains a set of small utilities revolving around running
Xwayland and various Wayland compositor headless.


%prep
%autosetup -S git_am


%build
%meson %{?rhel:-Dcompositor=mutter}
%meson_build


%install
%meson_install


%files
%license COPYING
%doc README.md
%{_bindir}/wlheadless-run
%{_bindir}/xwayland-run
%{_bindir}/xwfb-run
%{_datadir}/wlheadless/
%{_mandir}/man1/wlheadless-run.1*
%{_mandir}/man1/xwayland-run.1*
%{_mandir}/man1/xwfb-run.1*
%{python3_sitelib}/wlheadless/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.0.4-12
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.0.4-11
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.0.4-9
- Rebuilt for Python 3.14

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.0.4-6
- Add Suggests for default compositor

* Fri Jul 05 2024 Olivier Fourdan <ofourdan@redhat.com> - 0.0.4-5
- Backport fix for waitpid errors

* Tue Jul 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.0.4-4
- Rework RHEL variant of compositor dependencies

* Mon Jul  1 2024 Olivier Fourdan <ofourdan@redhat.com> - 0.0.4-2
- Require and use mutter as default compositor in RHEL
- Make other compositors very weak dependencies in RHEL

* Fri Jun 28 2024 Olivier Fourdan <ofourdan@redhat.com> - 0.0.4-1
- Update to 0.0.4
- Add required dependency on xorg-x11-xauth

* Fri Jun 28 2024 Niels De Graef <ndegraef@redhat.com> - 0.0.3-3
- Add a dependency on dbus-daemon

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.0.3-2
- Rebuilt for Python 3.13

* Mon Mar 25 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.0.3-1
- Update to 0.0.3
- Drop upstreamed kwin support patch

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 13 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.0.2-3
- Refresh kwin support patch with final version

* Sun Dec 10 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.0.2-2
- Refresh kwin support patch
- Add provides for other included utilities

* Sun Dec 10 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.0.2-1
- Initial package
