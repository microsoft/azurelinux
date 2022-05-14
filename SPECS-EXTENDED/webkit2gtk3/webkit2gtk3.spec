Vendor:         Microsoft Corporation
Distribution:   Mariner
## START: Set by rpmautospec
## (rpmautospec version 0.2.5)
%define autorelease(e:s:pb:) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{?dist}
## END: Set by rpmautospec

## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global add_to_license_files() \
        mkdir -p _license_files ; \
        cp -p %1 _license_files/$(echo '%1' | sed -e 's!/!.!g')

# Build documentation by default (use `rpmbuild --without docs` to override it).
# This is used by Coverity. Coverity injects custom compiler warnings, but
# any warning during WebKit docs build is fatal!
%bcond_without docs

Name:           webkit2gtk3
Version:        2.36.1
Release:        %autorelease
Summary:        GTK Web content engine library

License:        LGPLv2
URL:            https://www.webkitgtk.org/
Source0:        webkitgtk-%{version}.tar.xz

BuildRequires:  bison
BuildRequires:  ccache
BuildRequires:  bubblewrap
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  gnupg2
BuildRequires:  gperf
BuildRequires:  gtk-doc
BuildRequires:  hyphen-devel
BuildRequires:  libatomic
BuildRequires:  ninja-build
BuildRequires:  perl(English)
BuildRequires:  perl-local-lib
BuildRequires:  perl-generators
BuildRequires:  perl-Module-Build
BuildRequires:  perl-File-Find-Rule
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(Switch)
BuildRequires:  python3
BuildRequires:  ruby
BuildRequires:  rubygems
BuildRequires:  rubygem-json
BuildRequires:  xdg-dbus-proxy

BuildRequires:  pkgconfig(atspi-2)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enchant-2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtasn1)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwoff2dec)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wpe-1.0)
BuildRequires:  pkgconfig(wpebackend-fdo-1.0)
BuildRequires:  pkgconfig(xt)

# These are hard requirements of WebKit's bubblewrap sandbox.
Requires:       bubblewrap
Requires:       xdg-dbus-proxy

# If Geoclue is not running, the geolocation API will not work.
Recommends:     geoclue2

# Needed for various GStreamer elements.
#Requires:     gstreamer-plugins-bad-free
Requires:     gstreamer-plugins-good

# If no xdg-desktop-portal backend is installed, many features will be broken
# inside the sandbox. In particular, the -gtk backend has to be installed for
# desktop settings access, including font settings.
Recommends:     xdg-desktop-portal-gtk

# This package was renamed, so obsolete the old webkitgtk4 package. This is
# still here because some Fedora packages still depend on the webkitgtk4 name.
Obsoletes:      webkitgtk4 < %{version}-%{release}
Provides:       webkitgtk4 = %{version}-%{release}

# We're supposed to specify versions here, but these libraries don't do
# normal releases. Accordingly, they're not suitable to be system libs.
Provides:       bundled(angle)
Provides:       bundled(xdgmime)

# Require the jsc subpackage
Requires:       %{name}-jsc%{?_isa} = %{version}-%{release}

# Filter out provides for private libraries
%global __provides_exclude_from ^%{_libdir}/webkit2gtk-4\\.0/.*\\.so$

%description
WebKitGTK is the port of the portable web rendering engine WebKit to the
GTK platform.

This package contains WebKit2 based WebKitGTK for GTK 3.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-jsc%{?_isa} = %{version}-%{release}
Requires:       %{name}-jsc-devel%{?_isa} = %{version}-%{release}
Obsoletes:      webkitgtk4-devel < %{version}-%{release}
Provides:       webkitgtk4-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%if %{with docs}
%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Obsoletes:      webkitgtk4-doc < %{version}-%{release}
Provides:       webkitgtk4-doc = %{version}-%{release}

%description    doc
This package contains developer documentation for %{name}.
%endif

%package        jsc
Summary:        JavaScript engine from %{name}
Obsoletes:      webkitgtk4-jsc < %{version}-%{release}
Provides:       webkitgtk4-jsc = %{version}-%{release}

%description    jsc
This package contains JavaScript engine from %{name}.

%package        jsc-devel
Summary:        Development files for JavaScript engine from %{name}
Requires:       %{name}-jsc%{?_isa} = %{version}-%{release}
Obsoletes:      webkitgtk4-jsc-devel < %{version}-%{release}
Provides:       webkitgtk4-jsc-devel = %{version}-%{release}

%description    jsc-devel
The %{name}-jsc-devel package contains libraries, build data, and header
files for developing applications that use JavaScript engine from %{name}.

%prep
#%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n webkitgtk-%{version}

# Remove bundled libraries
rm -rf Source/ThirdParty/gtest/
rm -rf Source/ThirdParty/qunit/

%build
# Increase the DIE limit so our debuginfo packages could be size optimized.
# Decreases the size for x86_64 from ~5G to ~1.1G.
# https://bugzilla.redhat.com/show_bug.cgi?id=1456261
%global _dwz_max_die_limit 250000000
# The _dwz_max_die_limit is being overridden by the arch specific ones from the
# redhat-rpm-config so we need to set the arch specific ones as well - now it
# is only needed for x86_64.
%global _dwz_max_die_limit_x86_64 250000000

# Remove debuginfo to reduce memory consumption:
# https://bugs.webkit.org/show_bug.cgi?id=140176
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/I6IVNA52TXTBRQLKW45CJ5K4RA4WNGMI/
%ifarch %{arm} %{ix86}
%global debug_package %{nil}
%global optflags %(echo %{optflags} | sed 's/-g /-g0 /')
%endif

%cmake \
  -DPORT=GTK \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_MINIBROWSER=ON \
  -DUSE_SOUP2=ON \
  -DUSE_LD_GOLD=ON \
  -DUSE_WPE_RENDERER=ON \
  -DPYTHON_EXECUTABLE=%{_bindir}/python3 \
  -DENABLE_GTKDOC=ON \
  -DENABLE_GAMEPAD=OFF \
  -DUSER_AGENT_BRANDING="Mariner" \
  %{nil}

%cmake_build -j 4

%install
%cmake_install

%find_lang WebKit2GTK-4.0

# Finally, copy over and rename various files for %%license inclusion
%add_to_license_files Source/JavaScriptCore/COPYING.LIB
%add_to_license_files Source/ThirdParty/ANGLE/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/common/third_party/smhasher/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/libXNVCtrl/LICENSE
%add_to_license_files Source/WebCore/LICENSE-APPLE
%add_to_license_files Source/WebCore/LICENSE-LGPL-2
%add_to_license_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CodeMirror/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/Esprima/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/three.js/LICENSE
%add_to_license_files Source/WTF/icu/LICENSE
%add_to_license_files Source/WTF/wtf/dtoa/COPYING
%add_to_license_files Source/WTF/wtf/dtoa/LICENSE

%files -f WebKit2GTK-4.0.lang
%license _license_files/*ThirdParty*
%license _license_files/*WebCore*
%license _license_files/*WebInspectorUI*
%license _license_files/*WTF*
%{_libdir}/libwebkit2gtk-4.0.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/WebKit2-4.0.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-4.0.typelib
%{_libdir}/webkit2gtk-4.0/
%{_libexecdir}/webkit2gtk-4.0/
%exclude %{_libexecdir}/webkit2gtk-4.0/MiniBrowser
%exclude %{_libexecdir}/webkit2gtk-4.0/jsc
%{_bindir}/WebKitWebDriver

%files devel
%{_libexecdir}/webkit2gtk-4.0/MiniBrowser
%{_includedir}/webkitgtk-4.0/
%exclude %{_includedir}/webkitgtk-4.0/JavaScriptCore
%exclude %{_includedir}/webkitgtk-4.0/jsc
%{_libdir}/libwebkit2gtk-4.0.so
%{_libdir}/pkgconfig/webkit2gtk-4.0.pc
%{_libdir}/pkgconfig/webkit2gtk-web-extension-4.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/WebKit2-4.0.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-4.0.gir

%files jsc
%license _license_files/*JavaScriptCore*
%{_libdir}/libjavascriptcoregtk-4.0.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/JavaScriptCore-4.0.typelib

%files jsc-devel
%{_libexecdir}/webkit2gtk-4.0/jsc
%dir %{_includedir}/webkitgtk-4.0
%{_includedir}/webkitgtk-4.0/JavaScriptCore/
%{_includedir}/webkitgtk-4.0/jsc/
%{_libdir}/libjavascriptcoregtk-4.0.so
%{_libdir}/pkgconfig/javascriptcoregtk-4.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/JavaScriptCore-4.0.gir

%if %{with docs}
%files doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/jsc-glib-4.0/
%{_datadir}/gtk-doc/html/webkit2gtk-4.0/
%{_datadir}/gtk-doc/html/webkitdomgtk-4.0/
%endif

%changelog
- Sat May 14 2022 Sriram Nambakam <snambakam@microsoft.com> 2.36.1-1
- Include package in Mariner

* Fri Feb 04 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.2-3
- Fix dependency on gst-plugins-bad

* Thu Feb 03 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.2-2
- Remove debuginfo on i686

* Thu Feb 03 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.2-1
- Update to 2.35.2

* Tue Feb 01 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.1-6
- Tighten GStreamer package deps

* Tue Jan 25 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.1-5
- Fix build on armv7hl

* Mon Jan 24 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.1-4
- Add patch for GCC 12 build fixes, update GPG verification

* Fri Jan 21 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.1-3
- Actually add patch for Safari leaks vulnerability

* Fri Jan 21 2022 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.1-2
- Add patch for Safari leaks vulnerability

* Mon Nov 29 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.35.1-1
- Update to WebKitGTK 2.35.1

* Wed Nov 24 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.2-1
- Upgrade to 2.34.2

* Thu Oct 28 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.1-7
- Revert "Override CMAKE_C_FLAGS_RELEASE and CMAKE_CXX_FLAGS_RELEASE"

* Tue Oct 26 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.1-6
- Override CMAKE_C_FLAGS_RELEASE and CMAKE_CXX_FLAGS_RELEASE

* Tue Oct 26 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.1-5
- Reduce number of architectures that require -g1

* Tue Oct 26 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.1-4
- Revert "Give up and ExcludeArch 32-bit arches"

* Tue Oct 26 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.1-3
- Give up and ExcludeArch 32-bit arches

* Mon Oct 25 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.1-2
- Partially revert removal of old Obsoletes/Provides

* Thu Oct 21 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.1-1
- Update to 2.34.1

* Wed Sep 29 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.0-4
- Improve instructions for generating GPG keyring

* Wed Sep 29 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.0-3
- Remove old obsoletes/provides

* Thu Sep 23 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.0-2
- Improve BuildRequires

* Wed Sep 22 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.34.0-1
- Update to WebKitGTK 2.34.0

* Fri Sep 17 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.33.91-1
- Update to 2.33.91

* Thu Sep 02 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.33.90-1
- Update to 2.33.90

* Wed Aug 18 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.33.3-4
- Use %limit_build to request sufficient RAM

* Tue Aug 17 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.33.3-3
- Really add patch...

* Tue Aug 17 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.33.3-2
- Add patch for https://bugs.webkit.org/show_bug.cgi?id=229152

* Mon Aug 16 2021 Michael Catanzaro <mcatanzaro@redhat.com> 2.33.3-1
- Update to 2.33.3 and enable LTO

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> 2.33.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.33.2-2
- Add missing GStreamer recommends

* Tue Jun 08 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.33.2-1
- Update to 2.33.2

* Mon May 24 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.33.1-3
- Unbreak gamepad support

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 2.33.1-2
- Rebuild for ICU 69

* Fri May 14 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.33.1-1
- Update to 2.33.1

* Mon May 10 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.32.1-1
- Update to 2.32.1

* Wed Mar 31 2021 Jonathan Wakely <jwakely@redhat.com> - 2.32.0-2
- Rebuilt for removed libstdc++ symbols (#1937698)

* Fri Mar 26 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Fri Mar 12 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Tue Mar 02 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.31.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.31.1-3
- Fix multilib conflict in gir files

* Wed Jan 13 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.31.1-2
- Disable gamepad support in RHEL

* Tue Jan 12 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Tue Dec 15 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.4-1
- Update to 2.30.4

* Tue Nov 24 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.3-1
- Update to 2.30.3

* Wed Nov 11 2020 Jeff Law <law@redhat.com> - 2.30.2-2
- Fix bogus volatile caught by gcc-11

* Mon Oct 26 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.2-1
- Update to 2.30.2

* Mon Sep 21 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Fri Sep 11 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.0-1
- Update to 2.30.0. Add patch for libwpe#59.

* Fri Sep 04 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Mon Aug 17 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Wed Jul 29 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.29.4-1
- Update to 2.29.4

* Tue Jul 14 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.29.3-2
- Drop some Requires to Recommends

* Wed Jul 08 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.29.3-1
- Update to 2.29.3

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 2.29.2-2
- Disable LTO

* Wed Jun 24 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.29.2-1
- Update to 2.29.2

* Mon May 18 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.29.1-1
- Update to 2.29.1

* Sat May 16 2020 Pete Walter <pwalter@fedoraproject.org> - 2.28.2-3
- Rebuild for ICU 67

* Fri May 08 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.2-2
- Fix garbage collection on ppc64le and s390x after upgrade to 2.28

* Fri Apr 24 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Fri Apr 17 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.1-4
- Actually reenable WPE renderer.

* Fri Apr 17 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.1-3
- Fix and reenable WPE renderer. Fix popup menus in X11.

* Wed Apr 15 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.1-2
- Disable WPE renderer again.

* Mon Apr 13 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Thu Apr 09 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.0-9
- Reenable WPE renderer, seems to have mysteriously fixed itself.
- Second attempt to fix ppc64le.

* Tue Mar 24 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.0-8
- Fix accelerated compositing mode with bubblewrap sandbox enabled
- Fix JavaScriptCore on ppc64le

* Mon Mar 16 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.0-7
- Disable WPE renderer since it's busted, rhbz#1813993.
- Use perl() syntax to denote perl dependencies.
- Bump revision to maintain upgrade path

* Wed Mar 11 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.0-3
- BuildRequires: perl-English

* Wed Mar 11 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.0-2
- Rebuild with koji hopefully not broken this time?
- Add perl-FindBin BuildRequires

* Wed Mar 11 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Thu Feb 27 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Mon Feb 10 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.27.90-2
- Add GPG verification during prep

* Mon Feb 10 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Mon Feb 10 2020 Eike Rathke <erack@redhat.com> - 2.27.4-3
- Resolves: rhbz#1800249 Fix FTBFS

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Eike Rathke <erack@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Wed Dec 04 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 2.27.3-2
- Fix minor file and directory ownership issues, rhbz#1779754 and rhbz#1779772

* Tue Nov 26 2019 Eike Rathke <erack@redhat.com> - 2.27.3-1
- Resolves: rhbz#1776825 Update to 2.27.3

* Sat Nov 02 2019 Pete Walter <pwalter@fedoraproject.org> - 2.27.2-2
- Rebuild for ICU 65

* Tue Oct 22 2019 Eike Rathke <erack@redhat.com> - 2.27.2-1
- Resolves: rhbz#1764135 Update to 2.27.2

* Fri Oct 04 2019 Eike Rathke <erack@redhat.com> - 2.27.1-1
- Resolves: rhbz#1758590 Update to 2.27.1

* Thu Sep 26 2019 Eike Rathke <erack@redhat.com> - 2.26.1-1
- Resolves: rhbz#1754472 Update to 2.26.1

* Thu Sep 19 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 2.26.0-3
- Enable WPE renderer, resolves rhbz#1753730

* Tue Sep 17 2019 Tomas Popela <tpopela@redhat.com> - 2.26.0-2
- Backport fix for a crash when closing the view and HW acceleration is enabled
- Resolves: rhbz#1750345
- Backport fix for EGL_BAD_ALLOC
- Resolves: rhbz#1751936

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Sep 04 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 2.25.92-2
- Add patch to fix startup in X11 when not using gdm

* Tue Sep 03 2019 Eike Rathke <erack@redhat.com> - 2.25.92-1
- Resolves: rhbz#1748305 Update to 2.25.92

* Fri Aug 02 2019 Eike Rathke <erack@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Fri Jul 26 2019 Tomas Popela <tpopela@redhat.com> - 2.25.3-2
- Follow-up fixes for the GTK2 plugins support removal
- Fixes: rhbz#1733436

* Tue Jul 23 2019 Eike Rathke <erack@redhat.com> - 2.25.3-1
- Update to 2.25.3
- This removes support for GTK 2 based NPAPI plugins (such as Adobe Flash)

* Wed Jul 17 2019 Adam Williamson <awilliam@redhat.com> - 2.25.2-2
- Backport fix for crasher that affects Evolution (bwo#199621)

* Mon Jun 24 2019 Eike Rathke <erack@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Thu Jun 06 2019 Eike Rathke <erack@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Fri May 17 2019 Eike Rathke <erack@redhat.com> - 2.24.2-1
- Update to 2.24.2

* Tue Apr 09 2019 Eike Rathke <erack@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Mar 13 2019 Tomas Popela <tpopela@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Fri Mar 08 2019 Tomas Popela <tpopela@redhat.com> - 2.23.92-1
- Update to 2.23.92
- Switch to python3

* Wed Feb 20 2019 Eike Rathke <erack@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Mon Feb 18 2019 Eike Rathke <erack@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Pete Walter <pwalter@fedoraproject.org> - 2.23.3-2
- Rebuild for ICU 63

* Mon Jan 14 2019 Eike Rathke <erack@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Tue Nov 27 2018 Eike Rathke <erack@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Thu Nov 22 2018 Tomáš Popela <tpopela@redhat.com> - 2.22.4-1
- Update to 2.22.4

* Thu Nov 01 2018 Tomas Popela <tpopela@redhat.com> - 2.22.3-2
- Switch to using pkgconfig build requires
- Switch to enchant-2
- Resolves: rhbz#1631486

* Mon Oct 29 2018 Tomas Popela <tpopela@redhat.com> - 2.22.3-1
- Update to 2.22.3

* Fri Oct 19 2018 Tomas Popela <tpopela@redhat.com> - 2.22.2-3
- Fix WebProcess crash while printing
- Resolves: rhbz#1639754

* Tue Sep 25 2018 Tomas Popela <tpopela@redhat.com> - 2.22.2-2
- Switch to Ninja:
  -7 minutes on the x86_64
  -11 minutes on ppc64le
  -13 minutes on i686
  -13 minutes on s390x
  -10 minutes on armv7hl
  -19 minutes on aarch64

* Sun Sep 23 2018 Tomas Popela <tpopela@redhat.com> - 2.22.2-1
- Update to 2.22.2

* Thu Sep 20 2018 Tomas Popela <tpopela@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.22.0-3
- Rebuilt against fixed atk (#1626575)

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.22.0-2
- Rebuilt for GNOME 3.30.0 megaupdate

* Mon Sep 03 2018 Tomas Popela <tpopela@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Thu Aug 30 2018 Tomas Popela <tpopela@redhat.com> - 2.21.92-2
- Update the JSC build fix patch

* Wed Aug 29 2018 Tomas Popela <tpopela@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Thu Aug 16 2018 Tomas Popela <tpopela@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Fri Jul 20 2018 Tomas Popela <tpopela@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Mon Jul 16 2018 Tomas Popela <tpopela@redhat.com> - 2.21.4-4
- Fix the broken build due to python2 changes

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 2.21.4-2
- Rebuild for ICU 62

* Tue Jun 12 2018 Tomas Popela <tpopela@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Mon May 28 2018 Tomas Popela <tpopela@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Thu May 24 2018 Tomas Popela <tpopela@redhat.com> - 2.21.2-2
- Explicitly specify python2 over python and add python2 to BR

* Mon May 21 2018 Tomas Popela <tpopela@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 2.21.1-2
- Rebuild for ICU 61.1

* Wed Apr 18 2018 Tomas Popela <tpopela@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Tue Apr 10 2018 Tomas Popela <tpopela@redhat.com> - 2.20.1-1
- Update to 2.20.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 2.20.0-2
- Bump webkitgtk4 obsoletes versions

* Mon Mar 12 2018 Tomas Popela <tpopela@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Mar 06 2018 Tomas Popela <tpopela@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Wed Feb 21 2018 Tomas Popela <tpopela@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Tomas Popela <tpopela@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Tue Jan 30 2018 Tomas Popela <tpopela@redhat.com> - 2.19.6-3
- Remove obsoleted ldconfig scriptlets

* Wed Jan 17 2018 Tomas Popela <tpopela@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Thu Jan 11 2018 Tomas Popela <tpopela@redhat.com> - 2.19.5-2
- This package was formerly named webkitgtk4

