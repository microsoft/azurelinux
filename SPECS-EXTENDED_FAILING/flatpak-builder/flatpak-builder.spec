Vendor:         Microsoft Corporation
Distribution:   Mariner
%global glib2_version 2.44
%global ostree_version 2017.14
%global flatpak_version 0.99.1

Name:           flatpak-builder
Version:        1.0.10
Release:        2%{?dist}
Summary:        Tool to build flatpaks from source

# src/builder-utils.c has portions derived from GPLv2+ code,
# the rest is LGPLv2+
License:        LGPLv2+ and GPLv2+
URL:            http://flatpak.org/
Source0:        https://github.com/flatpak/flatpak-builder/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  gettext
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  flatpak >= %{flatpak_version}
BuildRequires:  libcap-devel
BuildRequires:  elfutils-devel
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(ostree-1) >= %{ostree_version}
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  /usr/bin/xmlto
BuildRequires:  /usr/bin/xsltproc

Requires:       flatpak%{?_isa} >= %{flatpak_version}
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       ostree-libs%{?_isa} >= %{ostree_version}
Requires:       /usr/bin/bzip2
%if ! 0%{?rhel} > 7
# No bzr in latest RHEL
Recommends:     /usr/bin/bzr
%endif
Requires:       /usr/bin/eu-strip
Requires:       /usr/bin/git
Requires:       /usr/bin/lzip
Requires:       /usr/bin/patch
Requires:       /usr/bin/rofiles-fuse
Requires:       /usr/bin/strip
Recommends:     /usr/bin/svn
Requires:       /bin/tar
Requires:       /usr/bin/unzip

%description
Flatpak-builder is a tool for building flatpaks from sources.

See http://flatpak.org/ for more information.


%prep
%autosetup -p1


%build
%configure \
    --enable-docbook-docs

%make_build V=1


%install
%make_install


%files
%license COPYING
%doc %{_pkgdocdir}
%{_bindir}/flatpak-builder
%{_mandir}/man1/flatpak-builder.1*
%{_mandir}/man5/flatpak-manifest.5*


%changelog
* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.10-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Fri Mar 20 2020 Kalev Lember <klember@redhat.com> - 1.0.10-1
- Update to 1.0.10

* Tue Feb 25 2020 David King <amigadave@amigadave.com> - 1.0.9-3
- Use elfutils instead of libdwarf

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 14 2019 David King <amigadave@amigadave.com> - 1.0.9-1
- Update to 1.0.9

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Kalev Lember <klember@redhat.com> - 1.0.7-1
- Update to 1.0.7

* Fri Feb 08 2019 Kalev Lember <klember@redhat.com> - 1.0.5-1
- Update to 1.0.5

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 David King <amigadave@amigadave.com> - 1.0.3-2
- Add dependency on lzip

* Mon Jan 28 2019 David King <amigadave@amigadave.com> - 1.0.3-1
- Update to 1.0.3

* Tue Jan 15 2019 Kalev Lember <klember@redhat.com> - 1.0.2-1
- Update to 1.0.2
- Change bzr requires to recommends

* Tue Oct 16 2018 Kalev Lember <klember@redhat.com> - 1.0.1-2
- Change svn requires to recommends (#1639355)

* Thu Oct 04 2018 Kalev Lember <klember@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Mon Aug 20 2018 David King <amigadave@amigadave.com> - 1.0.0-1
- Update to 1.0.0

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 0.99.3-4
- Update license to "LGPLv2+ and GPLv2+"

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.99.3-3
- Rebuild with fixed binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Kalev Lember <klember@redhat.com> - 0.99.3-1
- Update to 0.99.3

* Wed Jun 27 2018 Kalev Lember <klember@redhat.com> - 0.99.2-1
- Update to 0.99.2

* Mon Jun 25 2018 David King <amigadave@amigadave.com> - 0.99.1-1
- Update to 0.99.1

* Fri Apr 27 2018 David King <amigadave@amigadave.com> - 0.10.10-2
- Add some extra dependencies

* Thu Apr 26 2018 Kalev Lember <klember@redhat.com> - 0.10.10-1
- Update to 0.10.10

* Mon Feb 19 2018 David King <amigadave@amigadave.com> - 0.10.9-1
- Update to 0.10.9

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Kalev Lember <klember@redhat.com> - 0.10.6-1
- Update to 0.10.6

* Tue Nov 28 2017 David King <amigadave@amigadave.com> - 0.10.5-1
- Update to 0.10.5

* Mon Nov 06 2017 Kalev Lember <klember@redhat.com> - 0.10.4-1
- Update to 0.10.4

* Tue Oct 31 2017 David King <amigadave@amigadave.com> - 0.10.3-1
- Update to 0.10.3

* Mon Oct 30 2017 David King <amigadave@amigadave.com> - 0.10.2-1
- Update to 0.10.2

* Fri Oct 27 2017 Kalev Lember <klember@redhat.com> - 0.10.1-1
- Update to 0.10.1

* Thu Oct 26 2017 Kalev Lember <klember@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Mon Oct 09 2017 Kalev Lember <klember@redhat.com> - 0.9.99-1
- Update to 0.9.99

* Mon Sep 25 2017 Kalev Lember <klember@redhat.com> - 0.9.98-1
- Update to 0.9.98

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 0.9.11-1
- Update to 0.9.11

* Mon Sep 04 2017 Kalev Lember <klember@redhat.com> - 0.9.9-1
- Initial flatpak-builder package
