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

%global so_version 1
%global apiver 1.0

# “Let mm-common-get copy some files to untracked/”, i.e., replace scripts from
# the tarball with those from mm-common. This is (potentially) required if
# building an autotools-generated tarball with meson, or vice versa.
%bcond maintainer_mode 1

Name:           cairomm
Summary:        C++ API for the cairo graphics library
Version:        1.14.5
Release:        %autorelease

URL:            https://www.cairographics.org
License:        LGPL-2.0-or-later
# The following files under other allowable licenses belong to the build system
# and do not contribute to the licenses of the binary RPMs.
#
# FSFAP:
#   build/ax_boost_base.m4
#   build/ax_boost_test_exec_monitor.m4
#   build/ax_boost_unit_test_framework.m4
# GPL-2.0-or-later:
#   MSVC_NMake/gendef/gendef.cc
#   untracked/docs/tagfile-to-devhelp2.xsl
# LGPL-2.1-or-later:
#   Makefile.am
#   cairomm/Makefile.am
#   configure.ac
#   docs/Makefile.am
# MIT:
#   untracked/docs/reference/html/dynsections.js
#   untracked/docs/reference/html/jquery.js
#   untracked/docs/reference/html/menu.js
#   untracked/docs/reference/html/menudata.js
SourceLicense:  %{shrink:
                %{license} AND
                FSFAP AND
                GPL-2.0-or-later AND
                LGPL-2.1-or-later AND
                MIT
                }

%global src_base https://www.cairographics.org/releases
Source0:        %{src_base}/cairomm-%{version}.tar.xz
# No keyring with authorized GPG signing keys is published
# (https://gitlab.freedesktop.org/freedesktop/freedesktop/-/issues/331), but we
# are able to verify the signature using the key for Kjell Ahlstedt from
# https://gitlab.freedesktop.org/freedesktop/freedesktop/-/issues/290.
Source1:        %{src_base}/cairomm-%{version}.tar.xz.asc
Source2:        https://gitlab.freedesktop.org/freedesktop/freedesktop/uploads/0ac64e9582659f70a719d59fb02cd037/gpg_key.pub

# Fix outdated FSF mailing address in COPYING
# https://gitlab.freedesktop.org/cairo/cairomm/-/merge_requests/29
# (Merged upstream, so we are comfortable patching the license file.)
Patch:          https://gitlab.freedesktop.org/cairo/cairomm/-/merge_requests/29.patch
# Change license info to mention Lesser GPL 2.1 instead of Library GPL 2
#
# The GNU Library General Public License has been superseded by
# the GNU Lesser General Public License.
# https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html
#
# Remove obsolete FSF (Free Software Foundation) address.
# Committed to master branch:
# https://gitlab.freedesktop.org/cairo/cairomm/-/commit/43580ed75bde0b7d6ad442c90a22f80b50ce844d
# Cherry-picked to cairomm-1-14 branch:
# https://gitlab.freedesktop.org/cairo/cairomm/-/commit/2b73bbba0f88f1995ce4b1c2a0cf73299bdd654b
Patch:          https://gitlab.freedesktop.org/cairo/cairomm/-/commit/2b73bbba0f88f1995ce4b1c2a0cf73299bdd654b.patch
# MSVC_NMake/gendef/gendef.cc: License info: library -> program
#
# Was incorrectly corrected in the previous commit.
# https://gitlab.freedesktop.org/cairo/cairomm/-/commit/871393804b0bdec39e365a59ceaed7aaee774355
Patch:          https://gitlab.freedesktop.org/cairo/cairomm/-/commit/871393804b0bdec39e365a59ceaed7aaee774355.patch

BuildRequires:  gnupg2

BuildRequires:  gcc-c++
BuildRequires:  meson

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(sigc++-2.0)
BuildRequires:  pkgconfig(fontconfig)

# Everything mentioned in data/cairomm*.pc.in, except the Quartz and Win32
# libraries that do not apply to this platform:
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(cairo-pdf)
BuildRequires:  pkgconfig(cairo-png)
BuildRequires:  pkgconfig(cairo-ps)
BuildRequires:  pkgconfig(cairo-svg)
BuildRequires:  pkgconfig(cairo-xlib)
BuildRequires:  pkgconfig(cairo-xlib-xrender)

%if %{with maintainer_mode}
# mm-common-get
BuildRequires:  mm-common >= 1.0.4
%endif

BuildRequires:  doxygen
# dot
BuildRequires:  graphviz
# xsltproc
BuildRequires:  libxslt
BuildRequires:  pkgconfig(mm-common-libstdc++)

# For tests:
BuildRequires:  boost-devel

# Based on discussion in
# https://src.fedoraproject.org/rpms/pangomm/pull-request/2, cairomm will
# continue to provide API/ABI version 1.0 indefinitely, with the cairomm1.16
# package providing the new 1.16 API/ABI series. This virtual Provides is
# therefore no longer required, as dependent packages requiring the 1.0 API/ABI
# may safely require cairomm and its subpackages.
Provides:       cairomm%{apiver}%{?_isa} = %{version}-%{release}

%description
This library provides a C++ interface to cairo.

The API/ABI version series is %{apiver}.


%package        devel
Summary:        Development files for cairomm
Requires:       cairomm%{?_isa} = %{version}-%{release}

Provides:       cairomm%{apiver}-devel%{?_isa} = %{version}-%{release}

%description    devel
The cairomm-devel package contains libraries and header files for developing
applications that use cairomm.

The API/ABI version series is %{apiver}.


%package        doc
Summary:        Documentation for cairomm

# We unbundle Doxygen-inserted JavaScript assets from the HTML documentation
# as much as possible, as prescribed in
# https://src.fedoraproject.org/rpms/doxygen/blob/f42/f/README.rpm-packaging.
#
# Some files originating in Doxygen are still bundled or are generated from
# templates specifically for this package; where these have explicitly
# documented licenses, they are MIT.
License:        %{license} AND MIT

BuildArch:      noarch

Provides:       cairomm%{apiver}-doc = %{version}-%{release}

%{?doxygen_js_requires}

%description    doc
Documentation for cairomm can be viewed through the devhelp documentation
browser.

The API/ABI version series is %{apiver}.


%prep
%{gpgverify} \
    --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -p1
# Fix stray executable bit:
chmod -v a-x NEWS

# Remove the tag file, which triggers a rebuild of the documentation.
# While we are at it, we might as well rebuild the devhelp XML too.
rm -rf untracked/docs/reference/html
rm untracked/docs/reference/cairomm-%{apiver}.tag \
   untracked/docs/reference/cairomm-%{apiver}.devhelp2


%conf
%meson \
  -Dmaintainer-mode=%{?with_maintainer_mode:true}%{?!with_maintainer_mode:false} \
  -Dbuild-documentation=true \
  -Dbuild-examples=false \
  -Dbuild-tests=true \
  -Dboost-shared=true \
  -Dwarnings=max


%build
%meson_build


%install
%meson_install

install -t %{buildroot}%{_docdir}/cairomm-%{apiver} -m 0644 -p \
    ChangeLog NEWS README.md
cp -rp examples %{buildroot}%{_docdir}/cairomm-%{apiver}/

%{doxygen_unbundle_buildroot}


%check
%meson_test


%files
%license COPYING
%{_libdir}/libcairomm-%{apiver}.so.%{so_version}{,.*}


%files devel
%{_includedir}/cairomm-%{apiver}/
%{_libdir}/libcairomm-%{apiver}.so
%{_libdir}/pkgconfig/cairomm-%{apiver}.pc
%{_libdir}/pkgconfig/cairomm-*-%{apiver}.pc
%{_libdir}/cairomm-%{apiver}/


%files doc
%license COPYING
# Note: JavaScript has been removed from HTML reference manual, degrading the
# browser experience. It is still needed for Devhelp support.
%doc %{_docdir}/cairomm-%{apiver}/
%doc %{_datadir}/devhelp/


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.14.5-13
- test: add initial lock files

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.5-11
- Ship Doxygen HTML with full JS, unbundled; drop PDF

* Fri Apr 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.5-9
- Backport FSF address removal and related corrections

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.5-7
- Add a SourceLicense field

* Thu Oct 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.5-6
- Invoke %%meson in %%conf rather than in %%build

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 28 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.5-1
- Update to 1.14.5 (close RHBZ#2240942)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.4-9
- Use new (rpm 4.17.1+) bcond style

* Thu Jun 15 2023 Björn Persson <Bjorn@Rombobjörn.se> - 1.14.4-8
- Removed superfluous processing of the OpenPGP key.

* Mon Jan 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.4-7
- Revert "Work around missing dependency on texlive-wasy"

* Thu Jan 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.4-6
- Work around missing dependency on texlive-wasy

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.4-4
- Trivially simplify a files list

* Mon Dec 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.4-3
- Indicate dirs. in files list with trailing slashes

* Thu Sep 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.4-2
- Explicit perl BR no longer needed with mm-common >= 1.0.4

* Wed Sep 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.4-1
- Update to 1.14.4 (close RHBZ#2128740)

* Wed Aug 03 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-24
- Update License field to SPDX

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-21
- Tweak a spec file comment

* Wed Oct 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-20
- Bump release and rebuild (close RHBZ#2015257)

* Fri Oct 01 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-19
- Re-enable Doxygen HTML, stripping JS, for devhelp

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-18
- Rename PDF documentation file

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-17
- No need to remove .la files; meson doesn’t create them

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-16
- Package PDF docs in lieu of HTML

* Sun Sep 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-15
- Mention search/search.js

* Sat Sep 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-14
- In -doc, unbundle js-jquery and fix License

* Sat Sep 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-13
- Reduce macro indirection in spec file

* Tue Aug 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-12
- Rebuild for Boost 1.76

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-9
- Fix release number with rpmautospec

* Sat Feb 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-8
- Verify source with new strong signatures from upstream

* Thu Feb 18 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-7
- Working (but weak, dependent on SHA1) source signature verification
- Added API/ABI version to descriptions

* Wed Feb 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-6
- Fix typo %%{_?isa} for %%{?_isa} in virtual Provides
- Tidy up BR’s, including dropping make

* Mon Feb 15 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-5
- Update comments based on the new plan for the version 1.16 API/ABI

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-4
- Prepare for future upgrade to API/ABI version 1.16 by introducing virtual
  Provides for a name for API/ABI version 1.0: cairomm1.0. This will be the name
  of a future package that continues to provide API/ABI version 1.0 after the
  upgrade.

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-3
- Switch from autotools to meson; enable the tests, since the meson build system
  permits us to use a shared boost library
- Install examples in the -doc subpackage

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-2
- Restore removal of pre-built documentation with its minified JS bundle

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.2-1
- Update to 1.14.2; this adds new APIs, but is ABI-backwards-compatible

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.12.2-1
- Update to 1.12.2

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.12.0-16
- Switch URLs from HTTP to HTTPS
- Rough out code to verify source tarball signatures, and document why we
  cannot yet do so

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.12.0-15
- Spec file style tweaks
- Macro-ize documentation path in description
- Simplified summaries and descriptions
- Use make macros (https://src.fedoraproject.org/rpms/cairomm/pull-request/1)
- Drop obsolete %%ldconfig_scriptlets macro
- Much stricter file globs, including so-version
- Stop requiring the base package from the -doc package
- Migrate top-level text file documentation to the -doc subpackage
- BR mm-common; at minimum, this lets us find tags for libstdc++ documentation;
  require libstdc++-docs from the -doc subpackage, since we are now able to
  find the tag file in configure
- Remove bundled jQuery/jQueryUI from prebuilt documentation, and rebuild the
  documentation ourselves
- Add a note explaining why we cannot run the tests
- Drop explicit/manual lib Requires on cairo/libsigc++20
- Drop version requirements in BRs
- Rebuild autotools-generated files

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.12.0-7
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1.12.0-1
- Update to 1.12.0
- Drop manual requires that are automatically handled by pkgconfig dep gen
- Use license macro for COPYING
- Tighten -devel subpackage deps with the _isa macro
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.10.0-11
- Rebuilt for GCC 5 C++11 ABI change

* Sat Mar 07 2015 Kalev Lember <kalevlember@gmail.com> - 1.10.0-10
- Rebuilt for gcc5 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-4
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.10.0-2
- Rebuild for new libpng

* Fri Jul 29 2011 Kalev Lember <kalevlember@gmail.com> - 1.10.0-1
- Update to 1.10.0
- Have the -doc subpackage depend on the base package
- Modernize the spec file
- Really own /usr/share/devhelp directory

* Mon Feb 21 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.9.8-2
- fix documentation location
- co-own /usr/share/devhelp

* Mon Feb 14 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.9.8-1
- upstream 1.9.8
- fix issues with f15/rawhide (RHBZ #676878)
- drop gtk-doc dependency (RHBZ #604169)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.9.1-1
- New upstream release
- Removed html docs from -devel package
- Seperated requires into one per line
- Fixed devhelp docs

* Tue Nov 17 2009 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.8.4-1
- New upstream release
- Added cairommconfig.h file
- Added doc subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.8.0-1
- Update to 1.8.0
- Added libsigc++20-devel dependency

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Denis Leroy <denis@poolshark.org> - 1.6.2-1
- Update to upstream 1.6.2
- atsui patch upstreamed

* Sun Mar 23 2008 Denis Leroy <denis@poolshark.org> - 1.5.0-1
- Update to 1.5.0
- Added patch from Mamoru Tasaka to fix font type enum (#438600)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.4-2
- Autorebuild for GCC 4.3

* Fri Aug 17 2007 Denis Leroy <denis@poolshark.org> - 1.4.4-1
- Update to upstream version 1.4.4
- Fixed License tag

* Fri Jul 20 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.4.2-1
- New upstream release
- Changed install to preserve timestamps
- Removed mv of docs/reference and include files directly

* Wed Jan 17 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.4-1
- New release

* Sat Oct 14 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.2-1
- New upstream release

* Sun Aug 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-4
- Bumped release for make tag

* Sun Aug 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-3
- Bumped release for mass rebuild

* Sun Aug 20 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-2
- Bumped release for make tag

* Sun Aug 20 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-1
- New upstream release
- Updated summary and description

* Thu Aug  3 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.1.10-1
- First release for cairo 1.2
- Adjusted cairo dependencies for new version
- Docs were in html, moved to reference/html

* Sun Apr  9 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.6.0-1
- New upstream version should fix the upstream issues like AUTHORS and README
- Added pkgconfig to cairomm BuildRequires and cairomm-devel Requires
- Replaced makeinstall
- Fixed devel package description
- Modified includedir syntax
- docs included via the mv in install and in the devel files as html dir

* Sun Mar  5 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-10
- Removed duplicate Group tag in devel
- Disabled docs till they're fixed upstream

* Sun Mar  5 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-9
- Removed requires since BuildRequires is present
- Cleaned up Source tag

* Fri Feb 24 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-7
- Fixed URL and SOURCE tags
- Fixed header include directory

* Fri Feb 24 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-6
- Fixed URL tag

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-5
- Remove epoch 'leftovers'

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-4
- Cleanup for FE

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-3
- Added pre-release alphatag

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-2
- Updated to current cairomm CVS
- Added documentation to devel package

* Fri Feb 03 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-1
- Updated to current cairomm CVS

* Fri Jan 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.4.0-1
- Initial creation from papyrus.spec.in

## END: Generated by rpmautospec
