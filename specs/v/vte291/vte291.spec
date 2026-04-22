## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global apiver 2.91

%global fmt_version 11.0.0
%global fribidi_version 1.0.0
%global glib2_version 2.72.0
%global gnutls_version 3.2.7
%global gtk3_version 3.24.22
%global gtk4_version 4.14.0
%global icu_uc_version 4.8
%global libsystemd_version 220
%global pango_version 1.22.0
%global pcre2_version 10.21
%global simdutf_version 7.2.1

%if 0%{?rhel}
%bcond bundled_fast_float 1
%else
%bcond bundled_fast_float 0
%endif

Name:           vte291
Version:        0.82.3
Release:        %autorelease
Summary:        GTK terminal emulator library

# libvte-2.91.so is generated from LGPLv2+ and MIT sources
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND X11 AND CC-BY-4.0

URL:            https://wiki.gnome.org/Apps/Terminal/VTE
Source0:        https://download.gnome.org/sources/vte/0.82/vte-%{version}.tar.xz

BuildRequires:  pkgconfig(fmt) >= %{fmt_version}
BuildRequires:  pkgconfig(fribidi) >= %{fribidi_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnutls) >= %{gnutls_version}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(icu-uc) >= %{icu_uc_version}
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libpcre2-8) >= %{pcre2_version}
BuildRequires:  pkgconfig(libsystemd) >= %{libsystemd_version}
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  pkgconfig(simdutf) >= %{simdutf_version}
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  gobject-introspection-devel
BuildRequires:  gperf
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros
BuildRequires:  vala

%if %{without bundled_fast_float}
BuildRequires:  fast_float-devel
%endif

Requires:       fribidi >= %{fribidi_version}
Requires:       glib2 >= %{glib2_version}
Requires:       gnutls%{?_isa} >= %{gnutls_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}
Requires:       libicu%{?_isa} >= %{icu_uc_version}
Requires:       pango >= %{pango_version}
Requires:       pcre2%{?_isa} >= %{pcre2_version}
Requires:       systemd-libs%{?_isa} >= %{libsystemd_version}
Requires:       vte-profile

%if %{with bundled_fast_float}
Provides:       bundled(fast_float)
%endif

%description
VTE is a library implementing a terminal emulator widget for GTK+. VTE
is mainly used in gnome-terminal, but can also be used to embed a
console/terminal in games, editors, IDEs, etc.

%package        gtk4
Summary:        GTK4 terminal emulator library

# libvte-2.91.so is generated from LGPLv2+ and MIT sources
License:        LGPL-3.0-or-later AND MIT AND X11

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gtk4
VTE is a library implementing a terminal emulator widget for GTK 4. VTE
is mainly used in gnome-terminal, but can also be used to embed a
console/terminal in games, editors, IDEs, etc.

%package        devel
Summary:        Development files for GTK+ 3 %{name}

# vte-2.91 is generated from GPLv3+ sources, while the public headers are
# LGPLv3+
License:        GPL-3.0-or-later AND LGPL-3.0-or-later

Requires:       %{name}%{?_isa} = %{version}-%{release}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends:     gi-docgen-fonts

%description devel
The %{name}-devel package contains libraries and header files for
developing GTK+ 3 applications that use %{name}.

%package        gtk4-devel
Summary:        Development files for GTK 4 %{name}

# vte-2.91 is generated from GPLv3+ sources, while the public headers are
# LGPLv3+
License:        GPL-3.0-or-later AND LGPL-3.0-or-later

Requires:       %{name}-gtk4%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends:     gi-docgen-fonts

%description gtk4-devel
The %{name}-gtk4-devel package contains libraries and header files for
developing GTK 4 applications that use %{name}.

# vte-profile is deliberately not noarch to avoid having to obsolete a noarch
# subpackage in the future when we get rid of the vte3 / vte291 split. Yum is
# notoriously bad when handling noarch obsoletes and insists on installing both
# of the multilib packages (i686 + x86_64) as the replacement.
%package -n     vte-profile
Summary:        Profile script for VTE terminal emulator library
License:        GPL-3.0-or-later
# vte.sh was previously part of the vte3 package
Conflicts:      vte3 < 0.36.1-3

%description -n vte-profile
The vte-profile package contains a profile.d script for the VTE terminal
emulator library.

%prep
%autosetup -p1 -n vte-%{version}
%if 0%{?flatpak}
# Install user units where systemd macros expect them
sed -i -e "/^vte_systemduserunitdir =/s|vte_prefix|'/usr'|" meson.build
%endif

# Guarantee we don't accidentally use subprojects if a new subproject is added.
%if %{with bundled_fast_float}
rm -rf subprojects/fmt/
rm -rf subprojects/simdutf/
%else
rm -rf subprojects/
%endif

%build
%meson --buildtype=plain -Ddocs=true -Dgtk3=true -Dgtk4=true
%meson_build

%install
%meson_install
rm %{buildroot}/%{_datadir}/applications/org.gnome.Vte.App.Gtk3.desktop
rm %{buildroot}/%{_datadir}/applications/org.gnome.Vte.App.Gtk4.desktop

%find_lang vte-%{apiver}

%files -f vte-%{apiver}.lang
%license COPYING.LGPL3
%license COPYING.XTERM
%doc README.md
%{_libdir}/libvte-%{apiver}.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Vte-2.91.typelib
%{_userunitdir}/vte-spawn-.scope.d
%{_datadir}/xdg-terminals/org.gnome.Vte.App.Gtk3.desktop
%{_datadir}/xdg-terminals/org.gnome.Vte.App.Gtk4.desktop

%files gtk4
%{_libdir}/libvte-%{apiver}-gtk4.so.0*
%{_libdir}/girepository-1.0/Vte-3.91.typelib

%files devel
%license COPYING.GPL3
%{_bindir}/vte-%{apiver}
%{_includedir}/vte-%{apiver}/
%{_libdir}/libvte-%{apiver}.so
%{_libdir}/pkgconfig/vte-%{apiver}.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Vte-2.91.gir
%{_datadir}/glade/
%doc %{_docdir}/vte-2.91/
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/vte-2.91.deps
%{_datadir}/vala/vapi/vte-2.91.vapi

%files gtk4-devel
%{_bindir}/vte-%{apiver}-gtk4
%{_includedir}/vte-%{apiver}-gtk4/
%{_libdir}/libvte-%{apiver}-gtk4.so
%{_libdir}/pkgconfig/vte-%{apiver}-gtk4.pc
%{_datadir}/gir-1.0/Vte-3.91.gir
%doc %{_docdir}/vte-2.91-gtk4/
%{_datadir}/vala/vapi/vte-2.91-gtk4.deps
%{_datadir}/vala/vapi/vte-2.91-gtk4.vapi

%files -n vte-profile
%license COPYING.GPL3
%{_libexecdir}/vte-urlencode-cwd
%{_sysconfdir}/profile.d/vte.csh
%{_sysconfdir}/profile.d/vte.sh

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 0.82.3-2
- Latest state for vte291

* Thu Jan 22 2026 Barry Dunn <badunn@redhat.com> - 0.82.3-1
- Update to 0.82.3

* Wed Dec 10 2025 Adrian Vovk <adrianvovk@gmail.com> - 0.82.2-1
- Update to 0.82.2

* Mon Oct 13 2025 Petr Schindler <pschindl@redhat.com> - 0.82.1-1
- Update to 0.82.1

* Tue Sep 16 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 0.82.0-2
- Fix fast_float bcond condition

* Tue Sep 16 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 0.82.0-1
- Update to 0.82.0

* Wed Sep 03 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 0.81.90-3
- Add a bunch of patches!

* Mon Aug 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.81.90-2
- Ensure correct fonts are installed for HTML docs

* Mon Aug 25 2025 Fabio Valentini <decathorpe@gmail.com> - 0.81.90-1
- Update to version 0.81.90

* Tue Aug 05 2025 František Zatloukal <fzatlouk@redhat.com> - 0.81.0-5
- Rebuilt for icu 77.1

* Mon Jul 28 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.81.0-4
- Update std::from_chars patch

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.81.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Milan Crha <mcrha@redhat.com> - 0.81.0-2
- Add simdutf dependency

* Wed Jul 09 2025 Milan Crha <mcrha@redhat.com> - 0.81.0-1
- Update to 0.81.0

* Fri Jun 06 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 0.80.2-3
- Delete demo desktop files

* Mon May 26 2025 nmontero <nmontero@redhat.com> - 0.80.2-1
- Update to 0.80.2

* Mon Apr 14 2025 nmontero <nmontero@redhat.com> - 0.80.1-1
- Update to 0.80.1

* Mon Mar 17 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.80.0-2
- Avoid fast_float dependency

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 0.80.0-1
- Update to 0.80.0

* Wed Mar 05 2025 nmontero <nmontero@redhat.com> - 0.79.91-1
- Update to 0.79.91

* Wed Feb 19 2025 nmontero <nmontero@redhat.com> - 0.79.90-1
- Update to 0.79.90

* Wed Feb 12 2025 nmontero <nmontero@redhat.com> - 0.79.90-1
- Update to 0.79.0

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.78.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 0.78.2-2
- Rebuild for ICU 76

* Mon Nov 25 2024 nmontero <nmontero@redhat.com> - 0.78.2-1
- Update to 0.78.2

* Tue Oct 22 2024 nmontero <nmontero@redhat.com> - 0.78.1-1
- Update to 0.78.1

* Mon Sep 16 2024 David King <amigadave@amigadave.com> - 0.78.0-1
- Update to 0.78.0

* Sat Aug 10 2024 Jens Petersen <petersen@redhat.com> - 0.77.91-2
- fix vte.sh error: __vte_shell_precmd: command not found

* Thu Aug 08 2024 David King <amigadave@amigadave.com> - 0.77.91-1
- Update to 0.77.91

* Wed Jul 24 2024 David King <amigadave@amigadave.com> - 0.77.0-1
- Update to 0.77.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.76.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 David King <amigadave@amigadave.com> - 0.76.3-1
- Update to 0.76.3

* Fri Jun 07 2024 David King <amigadave@amigadave.com> - 0.76.2-2
- Use updated notification patches from ptyxis

* Tue May 28 2024 David King <amigadave@amigadave.com> - 0.76.2-1
- Update to 0.76.2

* Fri May 03 2024 David King <amigadave@amigadave.com> - 0.76.1-1
- Update to 0.76.1

* Tue Apr 02 2024 David King <amigadave@amigadave.com> - 0.76.0-1
- Update to 0.76.0

* Mon Feb 12 2024 Tomas Popela <tpopela@redhat.com> - 0.74.2-4
- Build for the SPDX license format change

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 0.74.2-3
- Rebuild for ICU 74

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.74.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 16 2023 Kalev Lember <klember@redhat.com> - 0.74.2-1
- Update to 0.74.2

* Sun Oct 22 2023 Kalev Lember <klember@redhat.com> - 0.74.1-1
- Update to 0.74.1

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 0.74.0-1
- Update to 0.74.0

* Tue Aug 08 2023 Kalev Lember <klember@redhat.com> - 0.73.93-1
- Update to 0.73.93

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.72.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 0.72.2-2
- Rebuilt for ICU 73.2

* Wed Jun 07 2023 Kalev Lember <klember@redhat.com> - 0.72.2-1
- Update to 0.72.2

* Sun Apr 16 2023 David King <amigadave@amigadave.com> - 0.72.1-1
- Update to 0.72.1

* Mon Mar 20 2023 David King <amigadave@amigadave.com> - 0.72.0-1
- Update to 0.72.0 (#2179642)

* Thu Mar 09 2023 David King <amigadave@amigadave.com> - 0.71.99-1
- Update to 0.71.99

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 0.71.92-1
- Update to 0.71.92

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.70.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 0.70.2-2
- Rebuild for ICU 72

* Tue Dec 06 2022 David King <amigadave@amigadave.com> - 0.70.2-1
- Update to 0.70.2

* Fri Oct 28 2022 David King <amigadave@amigadave.com> - 0.70.1-1
- Update to 0.70.1

* Mon Sep 26 2022 David King <amigadave@amigadave.com> - 0.70.0-2
- Fix GTK4 ABI padding (#2122922)

* Mon Sep 19 2022 Kalev Lember <klember@redhat.com> - 0.70.0-1
- Update to 0.70.0

* Mon Aug 08 2022 Kalev Lember <klember@redhat.com> - 0.69.92-1
- Update to 0.69.92

* Wed Aug 03 2022 David King <amigadave@amigadave.com> - 0.69.90-1
- Update to 0.69.90
- Enable GTK4 support

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 0.68.0-3
- Rebuilt for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.68.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Mar 27 2022 David King <amigadave@amigadave.com> - 0.68.0-1
- Update to 0.68.0

* Thu Feb 17 2022 David King <amigadave@amigadave.com> - 0.67.90-1
- Update to 0.67.90

* Thu Jan 27 2022 David King <amigadave@amigadave.com> - 0.66.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 David King <amigadave@amigadave.com> - 0.66.2-1
- Update to 0.66.2

* Mon Nov 01 2021 David King <amigadave@amigadave.com> - 0.66.1-1
- Update to 0.66.1

* Fri Oct 01 2021 Kalev Lember <klember@redhat.com> - 0.66.0-2
- Require systemd-libs rather than systemd

* Tue Sep 28 2021 David King <amigadave@amigadave.com> - 0.66.0-1
- Update to 0.66.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.64.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.64.2-2
- Fix the License fields and ship the correct license texts

* Wed Jun 16 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.64.2-1
- Update to 0.64.2

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 0.64.1-3
- Rebuild for ICU 69

* Fri May 07 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.64.1-2
- Add missing _VTE_CXX_NOEXCEPT in downstream patches

* Thu May 06 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.64.1-1
- Update to 0.64.1

* Thu May 06 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.64.0-1
- Update to 0.64.0

* Thu May 06 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.63.91-1
- Update to 0.63.91
- Rebase downstream patches

* Thu Feb 18 2021 Kalev Lember <klember@redhat.com> - 0.62.3-2
- Revert a change that limited select all, as decided by Workstation WG

* Tue Feb 16 2021 Kalev Lember <klember@redhat.com> - 0.62.3-1
- Update to 0.62.3
- Use https URLs for upstream

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.62.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Kalev Lember <klember@redhat.com> - 0.62.2-1
- Update to 0.62.2

* Wed Dec 16 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.62.1-3
- Accommodate 'sudo toolbox' when tracking the active container

* Tue Nov 03 2020 Jeff Law <law@redhat.com> - 0.62.1-2
- Fix bogus volatile caught by gcc-11

* Thu Oct 08 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.62.1-1
- Update to 0.62.1
- Rebase downstream patches

* Thu Sep 24 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.62.0-1
- Update to 0.62.0

* Thu Sep 24 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.61.91-1
- Update to 0.61.91

* Thu Sep 24 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.61.90-1
- Update to 0.61.90
- Rebase downstream patches

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Kalev Lember <klember@redhat.com> - 0.60.3-1
- Update to 0.60.3

* Sat May 16 2020 Pete Walter <pwalter@fedoraproject.org> - 0.60.2-2
- Rebuild for ICU 67

* Mon Apr 27 2020 Kalev Lember <klember@redhat.com> - 0.60.2-1
- Update to 0.60.2

* Mon Apr 06 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.60.1-2
- Improve legibility when using colours from the system theme

* Tue Mar 31 2020 Kalev Lember <klember@redhat.com> - 0.60.1-1
- Update to 0.60.1

* Sat Mar 21 2020 Kalev Lember <klember@redhat.com> - 0.60.0-2
- Move vte-urlencode-cwd to vte-profile subpackage (#1815769)

* Fri Mar 06 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.60.0-1
- Update to 0.60.0

* Mon Mar 02 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.59.92-2
- Replace C1 controls with C0 to emit OSC 777 from PS0 (RH #1783802)

* Mon Mar 02 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.59.92-1
- Update to 0.59.92

* Thu Feb 20 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.59.91-1
- Update to 0.59.91
- Rebase downstream patches

* Wed Feb 19 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.59.0-1
- Update to 0.59.0
- Rebase downstream patches

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.58.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 0.58.3-1
- Update to 0.58.3
- Avoid overriding vte's own -fno-exceptions

* Mon Oct 14 2019 Kalev Lember <klember@redhat.com> - 0.58.2-1
- Update to 0.58.2

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 0.58.1-1
- Update to 0.58.1

* Fri Oct 04 2019 Adam Williamson <awilliam@redhat.com> - 0.58.0-2
- Backport fix for crash due to out of bounds cursor position (#1756567)

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 0.58.0-1
- Update to 0.58.0

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 0.57.90-1
- Update to 0.57.90

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.57.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.57.3-1
- Update to 0.57.3
- Rebase downstream patches

* Wed Jun 19 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.57.0-2
- Support tracking the active container inside the terminal

* Tue Jun 18 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.57.0-1
- Update to 0.57.0
- Switch to the Meson build system
- Rebase downstream patches

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 0.56.3-1
- Update to 0.56.3

* Mon May 06 2019 Kalev Lember <klember@redhat.com> - 0.56.2-1
- Update to 0.56.2

* Tue Apr 09 2019 Kalev Lember <klember@redhat.com> - 0.56.1-1
- Update to 0.56.1

* Tue Apr 02 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.56.0-2
- Add signals proxying an interactive shell's precmd and preexec hooks.

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 0.56.0-1
- Update to 0.56.0

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 0.55.92-1
- Update to 0.55.92

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 0.55.90-2
- Rebuilt against fixed atk (#1626575)

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 0.55.90-1
- Update to 0.55.90

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Kalev Lember <klember@redhat.com> - 0.54.3-1
- Update to 0.54.3

* Fri Oct 26 2018 Kalev Lember <klember@redhat.com> - 0.54.2-1
- Update to 0.54.2

* Mon Oct 08 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-4
- Removal of utmp logging makes the utmp group unnecessary

* Fri Oct 05 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-3
- Tweak the escape sequence emission to unbreak the parsing

* Fri Oct 05 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-2
- Tighten the dependencies a bit

* Fri Oct 05 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-1
- Update to 0.54.1

* Thu Oct 04 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.0-1
- Update to 0.54.0

* Thu Oct 04 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.53.92-1
- Update to 0.53.92

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.53.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Kalev Lember <klember@redhat.com> - 0.53.0-2
- Require systemd, not initscripts for the utmp group (#1592403)

* Mon Jun 04 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.53.0-1
- Update to 0.53.0

* Mon May 21 2018 Kalev Lember <klember@redhat.com> - 0.52.2-1
- Update to 0.52.2

* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 0.52.1-1
- Update to 0.52.1

* Tue Apr 03 2018 Kalev Lember <klember@redhat.com> - 0.52.0-1
- Update to 0.52.0
- Remove ldconfig scriptlets

* Wed Mar 28 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.51.90-1
- Update to 0.51.90

* Wed Mar 28 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.51.3-1
- Update to 0.51.3
- Rebase downstream patches

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.50.2-3
- Switch to %%ldconfig_scriptlets

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 0.50.2-2
- Rebuild

* Wed Nov 01 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.50.2-1
- Update to 0.50.2

* Thu Oct 05 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.50.1-1
- Update to 0.50.1
- Rebase downstream patches

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 0.50.0-1
- Update to 0.50.0
- Rebase downstream patches

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 0.48.3-1
- Update to 0.48.3

* Wed Apr 12 2017 Kalev Lember <klember@redhat.com> - 0.48.2-1
- Update to 0.48.2
- Rebase downstream patches

* Wed Mar 22 2017 Kalev Lember <klember@redhat.com> - 0.48.1-1
- Update to 0.48.1

* Fri Feb 24 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.47.90-1
- Update to 0.47.90
- Rebase downstream patches

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 08 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.46.1-1
- Update to 0.46.1
- Rebase downstream patches

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.46.0-2
- BR vala instead of obsolete vala-tools subpackage

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 0.46.0-1
- Update to 0.46.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 0.45.92-1
- Update to 0.45.92

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 0.45.90-1
- Update to 0.45.90
- Rebase downstream patches

* Fri Jul 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.2-2
- Add a property to configure the scroll speed

* Tue May 10 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.2-1
- Update to 0.44.2
- Rebase downstream patches and undo unintentional ABI break

* Mon Apr 11 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.1-1
- Update to 0.44.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 0.44.0-1
- Update to 0.44.0

* Tue Mar 15 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.92-1
- Update to 0.43.92

* Tue Mar 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.91-1
- Update to 0.43.91
- Remove BuildRequires on pkgconfig(libpcre2-8)

* Tue Mar 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.90-1
- Update to 0.43.90

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.2-1
- Update to 0.43.2

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.1-1
- Update to 0.43.1
- Drop upstreamed patch

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.0-1
- Update to 0.43.0
- Add BuildRequires on pkgconfig(libpcre2-8)
- Disable -Wnonnull

* Thu Jan 28 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.42.3-1
- Update to 0.42.3
- Backport upstream patch to fix disappearing lines (GNOME #761097)

* Wed Oct 14 2015 Kalev Lember <klember@redhat.com> - 0.42.1-1
- Update to 0.42.1

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 0.42.0-1
- Update to 0.42.0
- Use license macro for COPYING

* Mon Sep 14 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.41.90-1
- Update to 0.41.90
- Rebased downstream patches after the migration to C++
- gnome-pty-helper has been removed

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.40.2-1
- Update to 0.40.2

* Tue Mar 24 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.40.0-1
- Update to 0.40.0

* Thu Mar 19 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.39.92-1
- Update to 0.39.92

* Tue Feb 17 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.39.90-1
- Update to 0.39.90
- Add command-notify patches

* Fri Dec 19 2014 Richard Hughes <rhughes@redhat.com> - 0.39.1-1
- Update to 0.39.1

* Mon Dec 01 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.39.0-2
- Backport upstream patch to fix zombie shells (GNOME #740929)

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 0.39.0-1
- Update to 0.39.0

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.2-1
- Update to 0.38.2

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.1-1
- Update to 0.38.1

* Sun Sep 14 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.0-1
- Update to 0.38.0

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.90-1
- Update to 0.37.90

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.2-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 0.37.2-1
- Update to 0.37.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.1-1
- Update to 0.37.1

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-2
- Split out a vte-profile subpackage that can be used with both vte291 / vte3

* Tue May 06 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-1
- Initial Fedora package, based on previous vte3 0.36 packaging

## END: Generated by rpmautospec
