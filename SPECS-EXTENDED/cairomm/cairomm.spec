
%global so_version 1
%global apiver 1.0

# “Let mm-common-get copy some files to untracked/”, i.e., replace scripts from
# the tarball with those from mm-common. This is (potentially) required if
# building an autotools-generated tarball with meson, or vice versa.
%bcond maintainer_mode 0

# Doxygen HTML help is not suitable for packaging due to a minified JavaScript
# bundle inserted by Doxygen itself. See discussion at
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555.
#
# We can enable the Doxygen PDF documentation as a substitute.
#
# We still generate the HTML documentation, but strip out all the JavaScript
# that causes policy issues. This degrades it in the browser, but is sufficient
# to keep the Devhelp documentation working.
#%bcond doc_pdf 1

Name:           cairomm
Summary:        C++ API for the cairo graphics library
Version:        1.14.5
Release:        1%{?dist}
vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.cairographics.org
License:        LGPL-2.0-or-later

%global src_base https://www.cairographics.org/releases
Source0:        %{src_base}/cairomm-%{version}.tar.xz
# No keyring with authorized GPG signing keys is published
# (https://gitlab.freedesktop.org/freedesktop/freedesktop/-/issues/331), but we
# are able to verify the signature using the key for Kjell Ahlstedt from
# https://gitlab.freedesktop.org/freedesktop/freedesktop/-/issues/290.
Source1:        %{src_base}/cairomm-%{version}.tar.xz.asc
Source2:        https://gitlab.freedesktop.org/freedesktop/freedesktop/uploads/0ac64e9582659f70a719d59fb02cd037/gpg_key.pub
%global libsigc_version 2.5.1
%global cairo_version 1.10.0
BuildRequires:  gnupg2

BuildRequires:  gcc-c++
BuildRequires:  meson

BuildRequires:  pkgconfig(cairo)
BuildRequires:  libsigc++20-devel >= %{libsigc_version}
Requires:       cairo%{?_isa} >= %{cairo_version}
Requires:       libsigc++20%{?_isa} >= %{libsigc_version}
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


#%package        doc
#Summary:        Documentation for cairomm

#BuildArch:      noarch

#Provides:       cairomm%{apiver}-doc = %{version}-%{release}

#%description    doc
#Documentation for cairomm can be viewed through the devhelp documentation
#browser.

#The API/ABI version series is %{apiver}.


%prep
%{gpgverify} \
    --keyring='%{SOURCE2}' --signature='%{SOURCE1}'  --data='%{SOURCE0}'

%autosetup
# Fix stray executable bit:
chmod -v a-x NEWS

# We must remove the jQuery/jQueryUI bundle with precompiled/minified/bundled
# JavaScript that is in untracked/docs/reference/html/jquery.js, since such
# sources are banned in Fedora. (Note also that the bundled JavaScript had a
# different license.) We also remove the tag file, which triggers a rebuild of
# the documentation. While we are at it, we might as well rebuild the devhelp
# XML too. Note that we will still install the HTML documentation, since the
# devhelp XML requires it, but we will strip out the JavaScript, which will
# degrade the documentation in a web browser.
rm -rf untracked/docs/reference/html
rm untracked/docs/reference/cairomm-%{apiver}.tag \
   untracked/docs/reference/cairomm-%{apiver}.devhelp2



%build
%meson \
  -Dmaintainer-mode=%{?with_maintainer_mode:true}%{?!with_maintainer_mode:false} \
  -Dbuild-documentation=false \
  -Dbuild-examples=false \
  -Dbuild-tests=true \
  -Dboost-shared=true \
  -Dwarnings=max


%meson_build





%install
%meson_install
#install -t %{buildroot}%{_docdir}/cairomm-%{apiver} -m 0644 -p \
#    ChangeLog NEWS README.md
#cp -rp examples %{buildroot}%{_docdir}/cairomm-%{apiver}/

# Strip out bundled and/or pre-minified JavaScript; this degrades the browser
# experience, but the HTML is still usable for devhelp.
#find '%{buildroot}%{_docdir}/cairomm-%{apiver}/reference/html' \
#  -type f \( -name '*.js' -o -name '*.js.*' \) -print -delete



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


#%files doc
#%license COPYING
# Note: JavaScript has been removed from HTML reference manual, degrading the
# browser experience. It is still needed for Devhelp support.
#%doc %{_docdir}/cairomm-%{apiver}/
#%doc %{_datadir}/devhelp/


%changelog
* Thu Nov 2024 Akarsh Chaudhary <v-akarshc@microsoft.com>- 1.14.5-1
- upgrade to version 1.14.5

* Wed Oct 26 2022 Muhammad Falak <mwani@microsoft.com> - 1.12.0-15
- License verified

* Wed Oct 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.0-14
- Bringing back the dependency on 'cairo'.

* Thu Jun 17 2021 Thomas Crain <thcrain@microsoft.com> - 1.12.0-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Use UI-cairo instead of cairo to avoid runtime conflicts

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
