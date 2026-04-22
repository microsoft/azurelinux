## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Remove bad dependencies added by perl-generators
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(at|extra|file\\)$

%global pkgconfdir %{_sysconfdir}/dpkg
%global pkgdatadir %{_datadir}/dpkg

Name:           dpkg
Version:        1.23.5
Release:        %autorelease
Summary:        Package maintenance system for Debian Linux
# The entire source code is GPLv2+ with exception of the following
# lib/dpkg/md5.c, lib/dpkg/md5.h - Public domain
# lib/dpkg/showpkg.c, dselect/methods/multicd, lib/dpkg/utils.c, lib/dpkg/showpkg.c - GPLv2
# dselect/methods/ftp - GPL no version info
# scripts/Dpkg/Gettext.pm - BSD
# lib/compat/obstack.h, lib/compat/gettext.h,lib/compat/obstack.c - LGPLv2+
# Automatically converted from old format: GPLv2 and GPLv2+ and LGPLv2+ and Public Domain and BSD - review is highly recommended.
License:        GPL-2.0-only AND GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-Public-Domain AND LicenseRef-Callaway-BSD
URL:            https://tracker.debian.org/pkg/dpkg
Source0:        http://ftp.debian.org/debian/pool/main/d/dpkg/%{name}_%{version}.tar.xz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bzip2-devel
BuildRequires:  dotconf-devel
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  libmd-devel
BuildRequires:  libselinux-devel
BuildRequires:  libtool
BuildRequires:  libzstd-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  perl-devel >= 5.36.0
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl-podlators
BuildRequires:  po4a >= 0.59
BuildRequires:  xz-devel
BuildRequires:  zlib-ng-devel

# Need by make check
BuildRequires: fakeroot
BuildRequires: gnupg2
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(IO::String)
BuildRequires: perl(IPC::Cmd)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Tie::Handle)
BuildRequires: perl(Time::Piece)

Requires:      tar

%description
This package provides the low-level infrastructure for handling the
installation and removal of Debian software packages.

This package contains the tools (including dpkg-source) required to unpack,
build and upload Debian source packages.

This package also contains the programs dpkg which used to handle the
installation and removal of packages on a Debian system.

This package also contains dselect, an interface for managing the installation
and removal of packages on the system.

dpkg and dselect will certainly be non-functional on a rpm-based system because
packages dependencies will likely be unmet.

%package devel
Summary:    Debian package management static library
Provides:   dpkg-static = %{version}-%{release}

%description devel
This package provides the header files and static library necessary to develop
software using dpkg, the same library used internally by dpkg.

Note though, that the API is to be considered volatile, and might change at any
time, use at your own risk.

%package dev
Summary:    Debian package development tools
BuildArch:  noarch

Requires:   binutils
Requires:   bzip2
Requires:   dpkg-perl = %{version}-%{release}
Requires:   gcc
Requires:   lzma
Requires:   make
Requires:   patch
Requires:   xz
Requires:   zstd

%description dev
This package provides the development tools (including dpkg-source) required to
unpack, build and upload Debian source packages.

Most Debian source packages will require additional tools to build; for example,
most packages need make and the C compiler gcc.

%package perl
Summary:    Dpkg perl modules
BuildArch:  noarch

Requires:   dpkg = %{version}-%{release}
Requires:   perl-TimeDate
Requires:   perl(Digest::MD5)
Requires:   perl(Digest::SHA)
Requires:   perl(Digest::SHA1)

%description perl
This package provides the perl modules used by the scripts in dpkg-dev. They
cover a wide range of functionality. Among them there are the following public
modules:

 - Dpkg: core variables
 - Dpkg::Arch: architecture handling functions
 - Dpkg::BuildFlags: set, modify and query compilation build flags
 - Dpkg::BuildInfo: build information functions
 - Dpkg::BuildOptions: parse and manipulate DEB_BUILD_OPTIONS
 - Dpkg::BuildProfiles: parse and manipulate build profiles
 - Dpkg::Changelog: parse changelogs
 - Dpkg::Changelog::Entry: represents a changelog entry
 - Dpkg::Changelog::Parse: generic changelog parser for dpkg-parsechangelog
 - Dpkg::Checksums: generate and parse checksums
 - Dpkg::Compression: simple database of available compression methods
 - Dpkg::Compression::FileHandle: transparently (de)compress files
 - Dpkg::Compression::Process: wrapper around compression tools
 - Dpkg::Conf: parse dpkg configuration files
 - Dpkg::Control: parse and manipulate Debian control information
   (.dsc, .changes, Packages/Sources entries, etc.)
 - Dpkg::Control::Changelog: represent fields output by dpkg-parsechangelog
 - Dpkg::Control::Fields: manage (list of known) control fields
 - Dpkg::Control::Hash: parse and manipulate a block of RFC822-like fields
 - Dpkg::Control::Info: parse files like debian/control
 - Dpkg::Control::Tests: parse files like debian/tests/control
 - Dpkg::Control::Tests::Entry: represents a debian/tests/control stanza
 - Dpkg::Deps: parse and manipulate dependencies
 - Dpkg::Deps::Simple: represents a single dependency statement
 - Dpkg::Deps::Multiple: base module to represent multiple dependencies
 - Dpkg::Deps::Union: list of unrelated dependencies
 - Dpkg::Deps::AND: list of AND dependencies
 - Dpkg::Deps::OR: list of OR dependencies
 - Dpkg::Deps::KnownFacts: list of installed and virtual packages
 - Dpkg::Exit: push, pop and run exit handlers
 - Dpkg::Gettext: wrapper around Locale::gettext
 - Dpkg::IPC: spawn sub-processes and feed/retrieve data
 - Dpkg::Index: collections of Dpkg::Control (Packages/Sources files for
   example)
 - Dpkg::Interface::Storable: base object serializer
 - Dpkg::Path: common path handling functions
 - Dpkg::Source::Format: manipulate debian/source/format files
 - Dpkg::Source::Package: extract Debian source packages
 - Dpkg::Substvars: substitute variables in strings
 - Dpkg::Vendor: identify current distribution vendor
 - Dpkg::Version: parse and manipulate Debian package versions

All the packages listed in Suggests or Recommends are used by some of the
modules.

%package -n dselect
Summary:  Debian package management front-end
Requires: %{name} = %{version}-%{release}

%description -n dselect
dselect is a high-level interface for managing the installation and removal of
Debian software packages. Many users find dselect intimidating and new users may
prefer to use apt-based user interfaces.

%prep
%autosetup -p1

%build
autoreconf -vif
%configure \
    --disable-linker-optimizations \
    --disable-rpath \
    --disable-update-alternatives \
    --runstatedir=/run \
    --with-admindir=%{_localstatedir}/lib/dpkg \
    --with-libbz2 \
    --with-liblzma \
    --with-libselinux \
    --with-libz-ng \
    --with-libzstd

%make_build

%install
%make_install

mkdir -p %{buildroot}/%{pkgconfdir}/origins

# Prepare "vendor" files for dpkg-vendor
cat <<EOF > %{buildroot}/%{pkgconfdir}/origins/fedora
Vendor: Fedora
Vendor-URL: http://www.fedoraproject.org/
Bugs: https://bugzilla.redhat.com
EOF
%if 0%{?fedora}
ln -sf fedora %{buildroot}/%{pkgconfdir}/origins/default
%endif

# from debian/dpkg.install
install -pm0644 debian/dpkg.cfg %{buildroot}/%{pkgconfdir}
install -pm0644 debian/dselect.cfg %{buildroot}/%{pkgconfdir}
install -pm0644 debian/shlibs.default %{buildroot}/%{pkgconfdir}
install -pm0644 debian/shlibs.override %{buildroot}/%{pkgconfdir}

# debian/dpkg.logrotate
install -D -pm0644 debian/dpkg.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

# from dpkg.postinst
for file in diversions statoverride status; do
    touch %{buildroot}%{_localstatedir}/lib/dpkg/$file
done

# Create log
mkdir -p %{buildroot}%{_localstatedir}/log/
touch %{buildroot}%{_localstatedir}/log/dpkg.log

%find_lang dpkg
%find_lang dpkg-dev
%find_lang dselect

rm %{buildroot}%{_libdir}/libdpkg.la

%check
make TEST_PARALLEL=4 check

%files -f dpkg.lang
%license debian/copyright
%doc README AUTHORS THANKS TODO
%doc debian/changelog debian/README.bug-usertags debian/dpkg.cron.daily
%dir %{pkgconfdir}
%dir %{pkgconfdir}/dpkg.cfg.d
%dir %{pkgconfdir}/origins
%config(noreplace) %{pkgconfdir}/dpkg.cfg
%config(noreplace) %{pkgconfdir}/origins/*
%config(noreplace) %{_sysconfdir}/logrotate.d/dpkg
%config(noreplace) %{_localstatedir}/log/%{name}.log
%dir %{_localstatedir}/lib/dpkg
%config(noreplace) %{_localstatedir}/lib/dpkg/diversions
%config(noreplace) %{_localstatedir}/lib/dpkg/statoverride
%config(noreplace) %{_localstatedir}/lib/dpkg/status
%{_datadir}/doc/dpkg/*
%{_datadir}/dpkg/sh/dpkg-error.sh
%{_bindir}/dpkg
%{_bindir}/dpkg-deb
%{_bindir}/dpkg-maintscript-helper
%{_bindir}/dpkg-query
%{_bindir}/dpkg-split
%{_bindir}/dpkg-trigger
%{_bindir}/dpkg-divert
%{_bindir}/dpkg-statoverride
%{_bindir}/dpkg-realpath
%{_sbindir}/start-stop-daemon
%{_libexecdir}/dpkg/dpkg-db-backup
%{_libexecdir}/dpkg/dpkg-db-keeper
%{_mandir}/man1/dpkg.1.gz
%{_mandir}/man1/dpkg-deb.1.gz
%{_mandir}/man1/dpkg-divert.1.gz
%{_mandir}/man1/dpkg-maintscript-helper.1.gz
%{_mandir}/man1/dpkg-query.1.gz
%{_mandir}/man1/dpkg-realpath.1.gz
%{_mandir}/man1/dpkg-split.1.gz
%{_mandir}/man1/dpkg-statoverride.1.gz
%{_mandir}/man1/dpkg-trigger.1.gz
%{_mandir}/man5/dpkg.cfg.5.gz
%{_mandir}/man8/start-stop-daemon.8.gz
%{_mandir}/*/man1/dpkg.1.gz
%{_mandir}/*/man1/dpkg-deb.1.gz
%{_mandir}/*/man1/dpkg-divert.1.gz
%{_mandir}/*/man1/dpkg-maintscript-helper.1.gz
%{_mandir}/*/man1/dpkg-query.1.gz
%{_mandir}/*/man1/dpkg-realpath.1.gz
%{_mandir}/*/man1/dpkg-split.1.gz
%{_mandir}/*/man1/dpkg-statoverride.1.gz
%{_mandir}/*/man1/dpkg-trigger.1.gz
%{_mandir}/*/man5/dpkg.cfg.5.gz
%{_mandir}/*/man8/start-stop-daemon.8.gz
%dir %{pkgdatadir}
%{pkgdatadir}/abitable
%{pkgdatadir}/cputable
%{pkgdatadir}/ostable
%{pkgdatadir}/tupletable

%files devel
%{_datadir}/aclocal/dpkg-*.m4
%{_includedir}/dpkg/*.h
%{_libdir}/libdpkg.a
%{_libdir}/pkgconfig/libdpkg.pc
%{_mandir}/man7/libdpkg.7.gz

%files dev -f dpkg-dev.lang
%doc doc/README.feature-removal-schedule doc/README.api doc/spec
%config(noreplace) %{pkgconfdir}/shlibs.default
%config(noreplace) %{pkgconfdir}/shlibs.override
%{_bindir}/dpkg-architecture
%{_bindir}/dpkg-buildapi
%{_bindir}/dpkg-buildpackage
%{_bindir}/dpkg-buildtree
%{_bindir}/dpkg-buildflags
%{_bindir}/dpkg-checkbuilddeps
%{_bindir}/dpkg-distaddfile
%{_bindir}/dpkg-genbuildinfo
%{_bindir}/dpkg-genchanges
%{_bindir}/dpkg-gencontrol
%{_bindir}/dpkg-gensymbols
%{_bindir}/dpkg-mergechangelogs
%{_bindir}/dpkg-name
%{_bindir}/dpkg-parsechangelog
%{_bindir}/dpkg-scanpackages
%{_bindir}/dpkg-scansources
%{_bindir}/dpkg-shlibdeps
%{_bindir}/dpkg-source
%{_bindir}/dpkg-vendor
%{_datadir}/zsh/vendor-completions/_dpkg-parsechangelog
%{_mandir}/man1/dpkg-architecture.1.gz
%{_mandir}/man1/dpkg-buildapi.1.gz
%{_mandir}/man1/dpkg-buildflags.1.gz
%{_mandir}/man1/dpkg-buildpackage.1.gz
%{_mandir}/man1/dpkg-buildtree.1.gz
%{_mandir}/man1/dpkg-checkbuilddeps.1.gz
%{_mandir}/man1/dpkg-distaddfile.1.gz
%{_mandir}/man1/dpkg-genbuildinfo.1.gz
%{_mandir}/man1/dpkg-genchanges.1.gz
%{_mandir}/man1/dpkg-gencontrol.1.gz
%{_mandir}/man1/dpkg-gensymbols.1.gz
%{_mandir}/man1/dpkg-mergechangelogs.1.gz
%{_mandir}/man1/dpkg-name.1.gz
%{_mandir}/man1/dpkg-parsechangelog.1.gz
%{_mandir}/man1/dpkg-scanpackages.1.gz
%{_mandir}/man1/dpkg-scansources.1.gz
%{_mandir}/man1/dpkg-shlibdeps.1.gz
%{_mandir}/man1/dpkg-source.1.gz
%{_mandir}/man1/dpkg-vendor.1.gz
%{_mandir}/man5/deb.5.gz
%{_mandir}/man5/deb822.5.gz
%{_mandir}/man5/deb-buildinfo.5.gz
%{_mandir}/man5/deb-changelog.5.gz
%{_mandir}/man5/deb-changes.5.gz
%{_mandir}/man5/deb-conffiles.5.gz
%{_mandir}/man5/deb-control.5.gz
%{_mandir}/man5/deb-extra-override.5.gz
%{_mandir}/man5/deb-md5sums.5.gz
%{_mandir}/man5/deb-old.5.gz
%{_mandir}/man5/deb-origin.5.gz
%{_mandir}/man5/deb-override.5.gz
%{_mandir}/man5/deb-postinst.5.gz
%{_mandir}/man5/deb-postrm.5.gz
%{_mandir}/man5/deb-preinst.5.gz
%{_mandir}/man5/deb-prerm.5.gz
%{_mandir}/man5/deb-shlibs.5.gz
%{_mandir}/man5/deb-split.5.gz
%{_mandir}/man5/deb-src-control.5.gz
%{_mandir}/man5/deb-src-files.5.gz
%{_mandir}/man5/deb-src-rules.5.gz
%{_mandir}/man5/deb-src-symbols.5.gz
%{_mandir}/man5/deb-substvars.5.gz
%{_mandir}/man5/deb-symbols.5.gz
%{_mandir}/man5/deb-triggers.5.gz
%{_mandir}/man5/dsc.5.gz
%{_mandir}/man7/deb-version.7.gz
%{_mandir}/man7/dpkg-build-api.7.gz
%{_mandir}/*/man1/dpkg-architecture.1.gz
%{_mandir}/*/man1/dpkg-buildapi.1.gz
%{_mandir}/*/man1/dpkg-buildflags.1.gz
%{_mandir}/*/man1/dpkg-buildpackage.1.gz
%{_mandir}/*/man1/dpkg-buildtree.1.gz
%{_mandir}/*/man1/dpkg-checkbuilddeps.1.gz
%{_mandir}/*/man1/dpkg-distaddfile.1.gz
%{_mandir}/*/man1/dpkg-genbuildinfo.1.gz
%{_mandir}/*/man1/dpkg-genchanges.1.gz
%{_mandir}/*/man1/dpkg-gencontrol.1.gz
%{_mandir}/*/man1/dpkg-gensymbols.1.gz
%{_mandir}/*/man1/dpkg-mergechangelogs.1.gz
%{_mandir}/*/man1/dpkg-name.1.gz
%{_mandir}/*/man1/dpkg-parsechangelog.1.gz
%{_mandir}/*/man1/dpkg-scanpackages.1.gz
%{_mandir}/*/man1/dpkg-scansources.1.gz
%{_mandir}/*/man1/dpkg-shlibdeps.1.gz
%{_mandir}/*/man1/dpkg-source.1.gz
%{_mandir}/*/man1/dpkg-vendor.1.gz
%{_mandir}/*/man5/deb.5.gz
%{_mandir}/*/man5/deb822.5.gz
%{_mandir}/*/man5/deb-buildinfo.5.gz
%{_mandir}/*/man5/deb-changelog.5.gz
%{_mandir}/*/man5/deb-changes.5.gz
%{_mandir}/*/man5/deb-conffiles.5.gz
%{_mandir}/*/man5/deb-control.5.gz
%{_mandir}/*/man5/deb-extra-override.5.gz
%{_mandir}/*/man5/deb-md5sums.5.gz
%{_mandir}/*/man5/deb-old.5.gz
%{_mandir}/*/man5/deb-origin.5.gz
%{_mandir}/*/man5/deb-override.5.gz
%{_mandir}/*/man5/deb-postinst.5.gz
%{_mandir}/*/man5/deb-postrm.5.gz
%{_mandir}/*/man5/deb-preinst.5.gz
%{_mandir}/*/man5/deb-prerm.5.gz
%{_mandir}/*/man5/deb-shlibs.5.gz
%{_mandir}/*/man5/deb-split.5.gz
%{_mandir}/*/man5/deb-src-control.5.gz
%{_mandir}/*/man5/deb-src-files.5.gz
%{_mandir}/*/man5/deb-src-rules.5.gz
%{_mandir}/*/man5/deb-src-symbols.5.gz
%{_mandir}/*/man5/deb-substvars.5.gz
%{_mandir}/*/man5/deb-symbols.5.gz
%{_mandir}/*/man5/deb-triggers.5.gz
%{_mandir}/*/man5/dsc.5.gz
%{_mandir}/*/man7/deb-version.7.gz
%{_mandir}/*/man7/dpkg-build-api.7.gz
%{pkgdatadir}/*.mk

%files perl
%{_datadir}/dpkg/*.specs
%{_mandir}/man3/Dpkg*.3*
%{perl_vendorlib}/Dpkg*

%files -n dselect -f dselect.lang
%config(noreplace) %{pkgconfdir}/dselect.cfg
%{_bindir}/dselect
%{perl_vendorlib}/Dselect
%{_libexecdir}/dpkg/methods
%{_localstatedir}/lib/dpkg/methods
%{_mandir}/man1/dselect.1.gz
%{_mandir}/man5/dselect.cfg.5.gz
%{_mandir}/*/man1/dselect.1.gz
%{_mandir}/*/man5/dselect.cfg.5.gz
%dir %{pkgconfdir}/dselect.cfg.d

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1.23.5-4
- Latest state for dpkg

* Tue Feb 17 2026 Simone Caronni <negativo17@gmail.com> - 1.23.5-3
- Remove obsolete conditional

* Tue Feb 17 2026 Simone Caronni <negativo17@gmail.com> - 1.23.5-2
- Trim changelog

* Tue Feb 17 2026 Simone Caronni <negativo17@gmail.com> - 1.23.5-1
- Update to 1.23.5

* Tue Feb 17 2026 Simone Caronni <negativo17@gmail.com> - 1.22.21-1
- Update to 1.22.21

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Simone Caronni <negativo17@gmail.com> - 1.22.20-1
- Update to 1.22.20
## END: Generated by rpmautospec
