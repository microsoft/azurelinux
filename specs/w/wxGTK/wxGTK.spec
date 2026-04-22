# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/wxGTK.azl.macros}

%global srcname wxWidgets
%global wxbasename wxBase
%global gtk3dir bld_gtk3
%global sover 0
%bcond_without tests

Name:           wxGTK
Version:        3.2.8
Release: 3%{?dist}
Summary:        GTK port of the wxWidgets GUI library
License:        LGPL-2.0-or-later WITH WxWindows-exception-3.1
URL:            https://www.wxwidgets.org/

Source0:        https://github.com/%{srcname}/%{srcname}/releases/download/v%{version}/%{srcname}-%{version}.tar.bz2
Source10:       wx-config
Source9999: wxGTK.azl.macros
# https://bugzilla.redhat.com/show_bug.cgi?id=1225148
# remove abort when ABI check fails
# Backport from wxGTK
Patch0:         %{name}-3.1.6-abicheck.patch
Patch1:         tests-no-deprecated-copy-dtor.patch

BuildRequires: make
BuildRequires:  gcc-c++
BuildRequires:  gtk3-devel
BuildRequires:  autoconf
BuildRequires:  webkit2gtk4.1-devel
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  expat-devel
BuildRequires:  SDL2-devel
BuildRequires:  libGLU-devel
BuildRequires:  libSM-devel
BuildRequires:  gstreamer1-plugins-bad-free-devel
BuildRequires:  gettext
BuildRequires:  cppunit-devel
BuildRequires:  libmspack-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libsecret-devel
BuildRequires:  libcurl-devel
# For Tests
%if %{with tests}
BuildRequires:  glibc-langpack-en
BuildRequires:  mesa-libEGL
BuildRequires:  xclock
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  python3-httpbin
BuildRequires:  vulkan-loader
%endif

# Can be removed in Fedora 42
Provides:       wxGTK3 = %version-%{release}
Obsoletes:      wxGTK3 < %version-%{release}
Obsoletes:      compat-wxGTK3-gtk2 < %version-%{release}
Obsoletes:      compat-wxGTK3-gtk2-devel < %version-%{release}
Obsoletes:      compat-wxGTK3-gtk2-gl < %version-%{release}
Obsoletes:      compat-wxGTK3-gtk2-media < %version-%{release}
Obsoletes:      wxBase3 < %version-%{release}
Obsoletes:      wxBase3-devel < %version-%{release}
Obsoletes:      wxGTK3-devel < %version-%{release}
Obsoletes:      wxGTK3-docs < %version-%{release}
Obsoletes:      wxGTK3-gl < %version-%{release}
Obsoletes:      wxGTK3-i18n < %version-%{release}
Obsoletes:      wxGTK3-media < %version-%{release}
Obsoletes:      wxGTK3-webview < %version-%{release}

Provides:       %{srcname} = %{version}-%{release}
Provides:       bundled(scintilla) = 3.7.2
Requires:       %{wxbasename}%{?_isa} = %{version}-%{release}
Requires:       %{name}-i18n = %{version}-%{release}

%description
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package -n     %{wxbasename}-devel
Summary:        Development files for the wxBase3 library
Requires:       %{wxbasename}%{?_isa} = %{version}-%{release}
Requires(post): /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

%description -n %{wxbasename}-devel
This package include files needed to link with the wxBase3 library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        devel
Summary:        Development files for the wxGTK library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-gl = %{version}-%{release}
Requires:       %{name}-media = %{version}-%{release}
Requires:       %{name}-webview = %{version}-%{release}
Requires:       %{wxbasename} = %{version}-%{release}
Requires:       %{wxbasename}-devel%{?_isa} = %{version}-%{release}
Requires:       gtk3-devel
Requires:       libGLU-devel
Provides:       %{srcname}-devel = %{version}-%{release}

%description devel
This package include files needed to link with the wxGTK library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        gl
Summary:        OpenGL add-on for the wxWidgets library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gl
OpenGL (a 3D graphics API) add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        i18n
Summary:        i18n message catalogs for the wxWidgets library
BuildArch:      noarch

%description i18n
i18n message catalogs for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        media
Summary:        Multimedia add-on for the wxWidgets library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description media
Multimedia add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        webview
Summary:        WebView add-on for the wxWidgets library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description webview
WebView add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package -n     %{wxbasename}
Summary:        Non-GUI support classes from the wxWidgets library

%description -n %{wxbasename}
Every wxWidgets application must link against this library. It contains
mandatory classes that any wxWidgets code depends on (like wxString) and
portability classes that abstract differences between platforms. wxBase can
be used to develop console mode applications -- it does not require any GUI
libraries or the X Window System.


%package        docs
Summary:        Documentation for the wxGTK library
Requires:       %{name} = %{version}-%{release}
Provides:       %{srcname}-docs = %{version}-%{release}
BuildArch:      noarch

%description docs
This package provides documentation for the %{srcname} library.


%prep
%autosetup -n %{srcname}-%{version} -p1

# patch some installed files to avoid conflicts with 2.8.*
sed -i -e 's|aclocal)|aclocal/wxwin32.m4)|' Makefile.in

# fix plugin dir for 64-bit
sed -i -e 's|/usr/lib\b|/usr/%{_lib}|' wx-config.in configure
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp

# Since we're currently patching configure.in
rm -f configure
./autogen.sh


%build
%global _configure ../configure

mkdir %{gtk3dir}
pushd %{gtk3dir}
%configure \
  --with-gtk=3 \
  --with-opengl \
  --with-sdl \
  --with-libmspack \
  --with-liblzma \
  --enable-intl \
  --disable-rpath \
  --disable-glcanvasegl \
  --enable-ipv6

%make_build
popd

#Docs
WX_SKIP_DOXYGEN_VERSION_CHECK=1 docs/doxygen/regen.sh html
mv docs/doxygen/out/html .

%install
pushd %{gtk3dir}
%make_install
popd

# install our multilib-aware wrapper
##Remove installed
rm %{buildroot}%{_bindir}/wx-config
##Install new and symlink
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_libexecdir}/%{name}/wx-config
sed -i -e 's|=/usr|=%{_prefix}|' %{buildroot}%{_libexecdir}/%{name}/wx-config
ln -s ../..%{_libexecdir}/%{name}/wx-config %{buildroot}%{_bindir}/wx-config-3.2
touch %{buildroot}%{_bindir}/wx-config

#Alternatives setup with wxrc
mv %{buildroot}%{_bindir}/wxrc* %{buildroot}%{_libexecdir}/%{name}
ln -s ../..%{_libexecdir}/%{name}/wxrc-3.2 %{buildroot}%{_bindir}/wxrc-3.2
touch %{buildroot}%{_bindir}/wxrc

# move bakefiles to avoid conflicts with 2.8.*
mkdir %{buildroot}%{_datadir}/bakefile/presets/wx32
mv %{buildroot}%{_datadir}/bakefile/presets/*.* %{buildroot}%{_datadir}/bakefile/presets/wx32

%find_lang wxstd-3.2

%check
%if %{with tests}
pushd %{gtk3dir}/tests
make %{?_smp_mflags}
python3 -m httpbin.core &
LD_LIBRARY_PATH=%{buildroot}%{_libdir} TZ=UTC wxUSE_XVFB=1 \
  WX_TEST_WEBREQUEST_URL="http://localhost:5000" xvfb-run -a ./test ~[.] \
%ifarch s390x
  ~wxTextFile::Special ~wxFileName::GetSizeSpecial ~wxFile::Special \
%endif
%ifarch riscv64
  ~wxTextFile::Special ~wxFile::Special ~URLTestCase::GetInputStream ~WebRequest::SSL::Error \
%endif
  ~WebRequest::SSL::Ignore
LD_LIBRARY_PATH=%{buildroot}%{_libdir} wxUSE_XVFB=1 xvfb-run -a \
  ./test_gui ~[.] \
%ifarch i686
  ~ImageTestCase \
%endif
%ifarch ppc64le
  ~VirtListCtrlTestCase \
%endif
%ifarch s390x
  ~WebView \
%endif
%ifarch riscv64
  ~TreeCtrlTestCase ~WebView ~wxImage::Paste \
%endif
  ~wxHtmlPrintout::Pagination
popd
%endif

%post -n %{wxbasename}-devel
if [ -f %{_bindir}/wx-config ] && [ ! -h %{_bindir}/wx-config ] ; then
  rm %{_bindir}/wx-config
fi
/usr/sbin/update-alternatives --install %{_bindir}/wx-config \
  wx-config %{_libexecdir}/%{name}/wx-config 25
/usr/sbin/update-alternatives --install %{_bindir}/wxrc \
  wxrc %{_libexecdir}/%{name}/wxrc 25

%postun -n %{wxbasename}-devel
if [ $1 -eq 0 ] ; then
  /usr/sbin/update-alternatives --remove wx-config %{_libexecdir}/%{name}/wx-config
  /usr/sbin/update-alternatives --remove wxrc %{_libexecdir}/%{name}/wxrc
fi

%files
%doc docs/changes.txt docs/readme.txt
%license docs/gpl.txt docs/lgpl.txt docs/licence.txt docs/licendoc.txt
%license docs/preamble.txt
%{_libdir}/libwx_gtk3u_adv-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_aui-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_core-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_html-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_propgrid-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_qa-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_ribbon-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_richtext-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_stc-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_xrc-*.so.%{sover}*

%files -n %{wxbasename}-devel
%ghost %{_bindir}/wx-config
%ghost %{_bindir}/wxrc
%{_bindir}/wxrc-3.2
%{_bindir}/wx-config-3.2
%{_includedir}/wx-3.2
%{_libdir}/libwx_baseu*.so
%dir %{_libdir}/wx
%dir %{_libdir}/wx/config
%dir %{_libdir}/wx/include
%{_datadir}/aclocal/wxwin32.m4
%{_datadir}/bakefile/presets/wx32
%{_libexecdir}/%{name}

%files devel
%{_libdir}/libwx_gtk3u_*.so
%{_libdir}/wx/config/gtk3-unicode-3.2
%{_libdir}/wx/include/gtk3-unicode-3.2

%files gl
%{_libdir}/libwx_gtk3u_gl-*.so.%{sover}*

%files i18n -f wxstd-3.2.lang

%files media
%{_libdir}/libwx_gtk3u_media-*.so.%{sover}*

%files webview
%{_libdir}/libwx_gtk3u_webview-*.so.%{sover}*
%dir %{_libdir}/wx
%{_libdir}/wx/3.2

%files -n %{wxbasename}
%doc docs/changes.txt docs/readme.txt
%license docs/gpl.txt docs/lgpl.txt docs/licence.txt docs/licendoc.txt
%license docs/preamble.txt
%{_libdir}/libwx_baseu-*.so.*
%{_libdir}/libwx_baseu_net-*.so.%{sover}*
%{_libdir}/libwx_baseu_xml-*.so.%{sover}*

%files docs
%doc html

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 06 2025 Scott Talbert <swt@techie.net> - 3.2.8-1
- Update to new upstream release 3.2.8 (#2363255)

* Wed Apr 09 2025 Scott Talbert <swt@techie.net> - 3.2.7-1
- Update to new upstream release 3.2.7

* Tue Feb 18 2025 Scott Talbert <swt@techie.net> - 3.2.6-3
- Add conditional for disabling tests

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 16 2024 Scott Talbert <swt@techie.net> - 3.2.6-1
- Update to new upstream release 3.2.6

* Wed Sep 11 2024 Scott Talbert <swt@techie.net> - 3.2.5-4
- Add more wxGTK3 Obsoletes

* Wed Jul 31 2024 Scott Talbert <swt@techie.net> - 3.2.5-3
- Update License tag to use SPDX identifiers

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat May 18 2024 Scott Talbert <swt@techie.net> - 3.2.5-1
- Update to new upstream release 3.2.5

* Wed Feb 21 2024 David Abdurachmanov <davidlt@rivosinc.com> - 3.2.4-7
- Skip failing tests on riscv64

* Fri Feb 16 2024 Scott Talbert <swt@techie.net> - 3.2.4-6
- Fix FTBFS with autoconf 2.72 (#2264449)

* Sun Feb 04 2024 Scott Talbert <swt@techie.net> - 3.2.4-5
- Enable wxLZMAInputStream (#2258458)

* Wed Jan 31 2024 Scott Talbert <swt@techie.net> - 3.2.4-4
- Fix FTBFS w/ GCC 14 (#2261535)
- Fix FTBFS w/ WebKitGTK 2.43

* Fri Jan 26 2024 Scott Talbert <swt@techie.net> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 10 2023 Scott Talbert <swt@techie.net> - 3.2.4-2
- Rebuild wxMediaCtrl with gstplayer for Wayland support

* Thu Nov 16 2023 Scott Talbert <swt@techie.net> - 3.2.4-1
- Update to new upstream release 3.2.4

* Wed Oct 11 2023 Scott Talbert <swt@techie.net> - 3.2.3-1
- Update to new upstream release 3.2.3

* Mon Aug 21 2023 Scott Talbert <swt@techie.net> - 3.2.2.1-6
- Rebuild with webkit2gtk4.1 (#2232979)

* Tue Jul 25 2023 Scott Talbert <swt@techie.net> - 3.2.2.1-5
- Make wxGetLinuxDistributionInfo work without lsb_release (#2184391)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Scott Talbert <swt@techie.net> - 3.2.2.1-3
- Remove unused BR on GConf2-devel (unused since before 3.0)

* Fri Jun 16 2023 Scott Talbert <swt@techie.net> - 3.2.2.1-2
- Fix WebView selection test with WebKit 2.40+

* Tue Feb 21 2023 Scott Talbert <swt@techie.net> - 3.2.2.1-1
- Update to new upstream release 3.2.2.1 (#2170238)

* Fri Feb 10 2023 Scott Talbert <swt@techie.net> - 3.2.2-1
- Update to new upstream release 3.2.2 (#2168466)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Florian Weimer <fweimer@redhat.com> - 3.2.1-4
- Port configure script to C99

* Tue Nov 22 2022 Scott Talbert <swt@techie.net> - 3.2.1-3
- Rebuild (again) with wxGLCanvas GLX support (resolves many OpenGL issues)

* Thu Nov 17 2022 Scott Talbert <swt@techie.net> - 3.2.1-2
- Rebuild with wxGLCanvas GLX support (resolves many OpenGL issues)

* Fri Sep 09 2022 Scott Talbert <swt@techie.net> - 3.2.1-1
- Update to new upstream release 3.2.1 (#2125703)

* Mon Jul 25 2022 Scott Talbert <swt@techie.net> - 3.2.0-1
- Update to new upstream release 3.2.0 (#2101974)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 09 2022 Scott Talbert <swt@techie.net> - 3.1.7-1
- Update to new upstream release 3.1.7 (#2094214)

* Mon Apr 04 2022 Scott Talbert <swt@techie.net> - 3.1.6-1
- Update to new upstream release 3.1.6 (#2071576)

* Tue Feb 01 2022 Scott Talbert <swt@techie.net> - 3.1.5-6
- Add some BRs to enable more tests

* Fri Jan 28 2022 Scott Talbert <swt@techie.net> - 3.1.5-5
- Fix FTBFS with GCC 12 (#2047123)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Scott Talbert <swt@techie.net> - 3.1.5-3
- Fix wxGLCanvas::IsDisplaySupported() when using EGL

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 15 2021 Scott Talbert <swt@techie.net> - 3.1.5-1
- Update to new upstream release 3.1.5 (#1948935)

* Thu Mar 04 2021 Scott Talbert <swt@techie.net> - 3.1.4-5
- Fix FTBFS due to glibc non-const SIGSTKSZ

* Wed Mar 03 2021 Peter Hutterer <peter.hutterer@redhat.com> 3.1.4-4
- Require only xclock, not all of xorg-x11-apps (#1934359)

* Sat Feb 06 2021 Scott Talbert <swt@techie.net> - 3.1.4-3
- Properly skip WebView tests to fix FTBFS (#1923643)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 08 2020 Scott Talbert <swt@techie.net> - 3.1.4-1
- Update to new upstream release 3.1.4 (#1859715)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 03 2020 Scott Talbert <swt@techie.net> - 3.1.3-1
- Initial packaging of wxWidgets 3.1.x (dev version) (#1714714)
