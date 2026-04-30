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
%global apiver 1.16

# “Let mm-common-get copy some files to untracked/”, i.e., replace scripts from
# the tarball with those from mm-common. This is (potentially) required if
# building an autotools-generated tarball with meson, or vice versa.
%bcond maintainer_mode 1

Name:           cairomm%{apiver}
Summary:        C++ API for the cairo graphics library
Version:        1.18.0
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
Patch:          https://gitlab.freedesktop.org/cairo/cairomm/-/commit/43580ed75bde0b7d6ad442c90a22f80b50ce844d.patch

BuildRequires:  gnupg2

BuildRequires:  gcc-c++
BuildRequires:  meson

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(sigc++-3.0)
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

%description
This library provides a C++ interface to cairo.

The API/ABI version series is %{apiver}.


%package        devel
Summary:        Development files for cairomm%{apiver}
Requires:       cairomm%{apiver}%{?_isa} = %{version}-%{release}

%description    devel
The cairomm%{apiver}-devel package contains libraries and header files for
developing applications that use cairomm%{apiver}.

The API/ABI version series is %{apiver}.


%package        doc
Summary:        Documentation for cairomm%{apiver}

# We unbundle Doxygen-inserted JavaScript assets from the HTML documentation
# as much as possible, as prescribed in
# https://src.fedoraproject.org/rpms/doxygen/blob/f42/f/README.rpm-packaging.
#
# Some files originating in Doxygen are still bundled or are generated from
# templates specifically for this package; where these have explicitly
# documented licenses, they are MIT.
License:        %{license} AND MIT

BuildArch:      noarch

%{?doxygen_js_requires}

%description    doc
Documentation for cairomm%{apiver} can be viewed through the devhelp
documentation browser.

The API/ABI version series is %{apiver}.


%prep
%{gpgverify} \
    --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -n cairomm-%{version} -p1

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
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.18.0-13
- test: add initial lock files

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.18.0-11
- Ship Doxygen HTML with full JS, unbundled; drop PDF

* Fri Apr 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.18.0-9
- Backport FSF address removal and related corrections

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.18.0-7
- Add a SourceLicense field

* Fri Nov 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.18.0-6
- Invoke %%meson in %%conf rather than in %%build

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 28 2023 Kalev Lember <klember@redhat.com> - 1.18.0-1
- Update to 1.18.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.2-9
- Use new (rpm 4.17.1+) bcond style

* Thu Jun 15 2023 Björn Persson <Bjorn@Rombobjörn.se> - 1.16.2-8
- Removed superfluous processing of the OpenPGP key.

* Mon Jan 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.2-7
- Revert "Work around missing dependency on texlive-wasy"

* Thu Jan 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.2-6
- Work around missing dependency on texlive-wasy

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.2-4
- Trivially simplify a files list

* Mon Dec 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.2-3
- Indicate dirs. in files list with trailing slashes

* Thu Sep 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.2-2
- Explicit perl BR no longer needed with mm-common >= 1.0.4

* Thu Sep 22 2022 Kalev Lember <klember@redhat.com> - 1.16.2-1
- Update to 1.16.2

* Wed Aug 03 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-17
- Update License field to SPDX

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-14
- Tweak a spec file comment

* Fri Oct 01 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-13
- Re-enable Doxygen HTML, stripping JS, for devhelp

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-12
- Rename PDF documentation file

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-11
- Drop the HTML reference manual altogether

* Sun Sep 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-10
- Mention search/search.js

* Sun Sep 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-9
- In -doc, unbundle js-jquery and fix License

* Sun Sep 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-8
- Use _docdir macro

* Sun Sep 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-7
- Reduce macro indirection in the spec file

* Tue Aug 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-6
- Rebuild for Boost 1.76

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.1-1
- Update to 1.16.1

* Sat Feb 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.0-3
- Verify source with new strong signatures from upstream

* Wed Feb 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.0-2
- Working (but weak, dependent on SHA1) source signature verification
- Tidy up BR’s, including dropping make

* Wed Feb 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.16.0-1
- New multi-version cairomm1.16 package to provide the version 1.16 API/ABI;
  based on the spec file from cairomm-1.14.2-5

## END: Generated by rpmautospec
