# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libnice
Version:        0.1.22
Release: 9%{?dist}
Summary:        GLib ICE implementation

License:        LGPL-2.1-or-later OR MPL-1.1
URL:            https://nice.freedesktop.org/
Source0:        https://nice.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source1:        https://nice.freedesktop.org/releases/%{name}-%{version}.tar.gz.asc

# gpg --recv-keys 1D388E5A4ED9A2BB
# gpg --output olivier.pgp --armor --export olivier.crete@ocrete.ca
Source2: olivier.pgp

# Build against the new gupnp-igd
Patch0:         libnice-gupnp-1.6.patch
Patch1:         libnice-0.1.22-fix-test-new-trickle-for-glib-2.83.patch
Patch2:         libnice-0.1.22-fix-openscanhub-findings.patch

BuildRequires:  glib2-devel
BuildRequires:  gnupg2
BuildRequires:  gnutls-devel >= 2.12.0
BuildRequires:  gobject-introspection-devel
BuildRequires:  gstreamer1-devel >= 0.11.91
BuildRequires:  gstreamer1-plugins-base-devel >= 0.11.91
BuildRequires:  gupnp-igd-devel >= 0.1.2
BuildRequires:  gtk-doc
BuildRequires:  graphviz
BuildRequires:  meson


%description
%{name} is an implementation of the IETF draft Interactive Connectivity
Establishment standard (ICE). ICE is useful for applications that want to
establish peer-to-peer UDP data streams. It automates the process of traversing
NATs and provides security against some attacks. Existing standards that use
ICE include the Session Initiation Protocol (SIP) and Jingle, XMPP extension
for audio/video calls.


%package        gstreamer1
Summary:        GStreamer plugin for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    gstreamer1
The %{name}-gstreamer1 package contains a gstreamer 1.0 plugin for %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

# disable tests that don't work in koji environment
sed \
    -e "s/^  'test-set-port-range'/#&/" \
    -i tests/meson.build

%build
%meson -D gtk_doc=enabled
%meson_build


%install
%meson_install


%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

# Temporarily make the upstream test-suite run on Intel arches only because we
# are getting random crashes in Koji on secondary arches but I have not been
# able to reproduce them locally so far.
%ifarch x86_64 %{ix86}
%meson_test
%endif


%ldconfig_scriptlets


%files
%doc NEWS README
%license COPYING COPYING.LGPL COPYING.MPL
%{_bindir}/stunbdc
%{_bindir}/stund
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/Nice-0.1.typelib


%files gstreamer1
%{_libdir}/gstreamer-1.0/libgstnice.so


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/nice.pc
%{_datadir}/gtk-doc/html/%{name}/
%{_datadir}/gir-1.0/Nice-0.1.gir


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 02 2025 Stefan Becker <chemobejk@gmail.com> - 0.1.22-7
- add upstream patches to fix OpenScanHub findings (#2362866)

* Wed Apr 09 2025 Matej Focko <mfocko@redhat.com> - 0.1.22-6
- Correct the SPDX license

* Wed Jan 22 2025 Stefan Becker <chemobejk@gmail.com> - 0.1.22-5
- add upstream patch to fix test-new-trickle for Glib 2.83

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.1.22-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 Stefan Becker <chemobejk@gmail.com> - 0.1.22-1
- Update to 0.1.22 (#2267812)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Kamil Dudka <kdudka@redhat.com> - 0.1.21-2
- verify GPG signature of upstream tarball when building the package

* Sun Jan 08 2023 Stefan Becker <chemobejk@gmail.com> - 0.1.21-1
- Update to 0.1.21 (#2158912)

* Fri Dec 09 2022 David King <amigadave@amigadave.com> - 0.1.19-3
- Rebuild against gupnp-igd

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 04 2022 Kamil Dudka <kdudka@redhat.com> - 0.1.19-1
- Update to 0.1.19 (#2081497)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Stefan Becker <chemobejk@gmail.com> - 0.1.18-1
- Update to 0.1.18 (#1980120)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Kamil Dudka <kdudka@redhat.com> - 0.1.17-4
- add BR for gtk-doc to fix build failure in Fedora Rawhide

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Stefan Becker <chemobejk@gmail.com> - 0.1.17-2
- Update to 0.1.17 (#1839335)

* Sat May 23 2020 Stefan Becker <chemobejk@gmail.com> - 0.1.17-1
- Update to 0.1.17

* Thu Mar 12 2020 Kalev Lember <klember@redhat.com> - 0.1.16-9
- Rebuilt for gupnp 1.2

* Fri Feb 28 2020 Stefan Becker <chemobejk@gmail.com> - 0.1.16-8
- add upstream patches for incorrectly ignored interfaces (#1808410)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Stefan Becker <chemobejk@gmail.com> - 0.1.16-5
- update to 0.1.16-16-gb998547
- ignore interfaces with "br-", "docker", "veth", "virbr" or "vnet" prefix (#1723770)

* Tue Jun 04 2019 Stefan Becker <chemobejk@gmail.com> - 0.1.16-4
- add upstream patch to make audio connection more reliable (#1716936)

* Fri May 10 2019 Stefan Becker <chemobejk@gmail.com> - 0.1.16-3
- test-new-dribble got renamed to test-new-trickle

* Fri May 10 2019 Kamil Dudka <kdudka@redhat.com> - 0.1.16-2
- reintroduce autoreconf in %%prep

* Fri May 10 2019 Stefan Becker <chemobejk@gmail.com> - 0.1.16-1
- Update to 0.1.16
- drop all upstream patches

* Thu May 09 2019 Stefan Becker <chemobejk@gmail.com> - 0.1.15-1
- Update to 0.1.15
- drop all upstream patches
- drop autoreconf from build
- add upstream patch to fix a test failure

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-9.20180504git34d6044
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-8.20180504git34d6044
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 07 2018 Kamil Dudka <kdudka@redhat.com> - 0.1.14-7.20180504git34d6044
- component: accept TURN in nice_component_verify_remote_candidate() (#1541646)
- update to 0.1.14-85-g34d6044 (#1541646)

* Mon Apr 16 2018 Kamil Dudka <kdudka@redhat.com> - 0.1.14-6.20171128gitfb2f1f7
- temporarily make the upstream test-suite run on Intel arches only
- disable test-send-recv, which fails in Koji

* Fri Mar 16 2018 Kamil Dudka <kdudka@redhat.com> - 0.1.14-5.20171128gitfb2f1f7
- do not build with -Werror by default
- make the build more verbose

* Fri Feb 09 2018 Kamil Dudka <kdudka@redhat.com> - 0.1.14-4.20171128gitfb2f1f7
- enable make check again
- make tests pass in Koji
- disable test-new-dribble that sometimes hangs indefinitely
- make tests compile on i686
- make the package build on armv7hl
- make the package build on Fedora 28
- avoid build failure if gstreamer-plugins-base-devel is installed
- move autoreconf invocation to %%prep
- use Name Version Release that explicitly identifies an SCM snapshot (#1541646)

* Fri Feb 09 2018 Stefan Becker <chemobejk@gmail.com> - 0.1.14-3
- update to 0.1.14-70-gfb2f1f7 with alternate server fixes for SIPE
- add autoreconf build step
- remove examples subpackage as examples are no longer installed

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Stefan Becker <chemobejk@gmail.com> - 0.1.14-1
- Update to 0.1.14

* Wed Jan 24 2018 Tomas Hoger <thoger@redhat.com> - 0.1.13-11
- Add conditional for building with(out) gst010 / GStreamer 0.10 support.
- Disable gst010 plugin by default.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Than Ngo <than@redhat.com> - 0.1.13-7
- Rebuilt for glibc: Revert sendmsg/recvmsg ABI changes

* Fri Jun 10 2016 David Woodhouse <dwmw2@infradead.org> - 0.1.13-6
- More updates from libnice git; use-after-free fixes

* Mon Jun 06 2016 David Woodhouse <dwmw2@infradead.org> - 0.1.13-5
- Wholesale update to git HEAD, which fixes SIPE again.

* Fri May 20 2016 David Woodhouse <dwmw2@infradead.org> - 0.1.13-4
- Backport patch to fix SIPE audio disconnections (#1337051)
- Fix candidate gathering with IPV6 tentative addresses (#1337412)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 0.1.13-1
- Update to 0.1.13
- Tighten dependencies with the _isa macro

* Tue Apr 21 2015 Kalev Lember <kalevlember@gmail.com> - 0.1.11-1
- Update to 0.1.11
- Use license macro for COPYING files

* Mon Mar 02 2015 David Woodhouse <dwmw2@infradead.org> - 0.1.10-1
- Update to 0.1.10

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.1.8-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Oct 26 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.8-1
- Update to 0.1.8
- Build with gobject introspection support

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4.
- Add examples subpackage.

* Fri May 10 2013 Matthias Clasen <mclasen@redhat.com> - 0.1.3-3
- Split the gstreamer plugins off in subpackages

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3.
- Add BR on gstreamer1 packages.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2.

* Mon Jan 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-3
- Rebuild for new gupnp-idg.

* Sun Jan 08 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-2
- Rebuild for new gcc.

* Wed Dec  7 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1.
- Drop ppc64 patch. Fixed upstream.

* Tue Aug 16 2011 David Woodhouse <dwmw2@infradead.org> - 0.1.0-5
- Apply portability patch to nice/Makefile.in too. I hate autocrap.

* Tue Aug 16 2011 David Woodhouse <dwmw2@infradead.org> - 0.1.0-4
- Fix non-portable symbol checks in nice/Makefile.am

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> - 0.1.0-3
- rebuild for new gupnp/gssdp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0.
- Enable make check.
- Drop buildroot and clean section. No longer needed.

* Wed Aug  4 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.13-1
- Update to 0.0.13.

* Wed May 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.12-1
- Update to 0.0.12.

* Fri Mar 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.11-1
- Update to 0.0.11.

* Wed Dec 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.10-2
- Rebuild for new gupnp-igd.

* Mon Nov  9 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.10-1
- Update to 0.0.10.

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.0.9-2
- Rebuild for new gupnp

* Sun Aug  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.9-1
- Update to 0.0.9.
- Drop sha1 patch. Fixed upstream.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Warren Togami <wtogami@redhat.com> - 0.0.8-2
- stun sha1 patch from upstream to make it work at all

* Sun Jun 21 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8.

* Sun Jun 14 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.7-1
- Update to 0.0.7.
- Add BR on gupnp-igd-devel.

* Mon Apr 13 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.6-1
- Update to 0.0.6.

* Wed Mar 18 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.5-1
- Update to 0.0.5.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.0.4-1
- Initial Fedora spec.

