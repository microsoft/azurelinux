Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global pkgconfdir      %{_sysconfdir}/dpkg
%global pkgdatadir      %{_datadir}/dpkg

Name:           dpkg
Version:        1.20.10
Release:        1%{?dist}
Summary:        Package maintenance system for Debian Linux
# The entire source code is GPLv2+ with exception of the following
# lib/dpkg/md5.c, lib/dpkg/md5.h - Public domain
# lib/dpkg/showpkg.c, dselect/methods/multicd, lib/dpkg/utils.c, lib/dpkg/showpkg.c - GPLv2
# dselect/methods/ftp - GPL no version info
# scripts/Dpkg/Gettext.pm - BSD
# lib/compat/obstack.h, lib/compat/gettext.h,lib/compat/obstack.c - LGPLv2+
License:        GPLv2 and GPLv2+ and LGPLv2+ and Public Domain and BSD
URL:            https://tracker.debian.org/pkg/dpkg
Source0:        https://ftp.debian.org/debian/pool/main/d/dpkg/%{name}_%{version}.tar.xz
# https://lists.debian.org/debian-dpkg/2017/08/msg00002.html
# The problem is that your compiler gives a different triplet than the
# one used by dpkg itself
# Finally trying to correct triplet for Fedora
Patch1:         cputable_ppc64le.patch
Patch2:         ostable_armv7hl.patch


BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  zlib-devel bzip2-devel libselinux-devel gettext ncurses-devel
BuildRequires:  autoconf automake gettext-devel libtool
BuildRequires:  doxygen xz-devel
BuildRequires:  po4a >= 0.59
BuildRequires:  dotconf-devel
# for /usr/bin/perl
BuildRequires: perl-interpreter
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl-Time-Piece
BuildRequires: perl(Digest)
# for /usr/bin/pod2man
BuildRequires: perl-podlators
# Needed for --clamp-mtime in dpkg-source -b.
Requires:      tar >= 1.28
# Need by make check
BuildRequires: perl(Test::More)
BuildRequires: perl(IPC::Cmd)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(IO::String)
BuildRequires: perl(Tie::Handle)
# ./t/dpkg_buildpackage.t ........ skipped: requires command fakeroot
BuildRequires: fakeroot

Requires(post): coreutils


%description
This package provides the low-level infrastructure for handling the
installation and removal of Debian software packages.

This package contains the tools (including dpkg-source) required
to unpack, build and upload Debian source packages.

This package also contains the programs dpkg which used to handle the
installation and removal of packages on a Debian system.

This package also contains dselect, an interface for managing the
installation and removal of packages on the system.

dpkg and dselect will certainly be non-functional on a rpm-based system
because packages dependencies will likely be unmet.


%package devel
Summary: Debian package management static library
Provides: dpkg-static = %{version}-%{release}

%description devel
This package provides the header files and static library necessary to
develop software using dpkg, the same library used internally by dpkg.

Note though, that the API is to be considered volatile, and might change
at any time, use at your own risk.


%package dev
Summary:  Debian package development tools
Requires: dpkg-perl = %{version}-%{release}
Requires: patch
Requires: make
Requires: binutils
Requires: bzip2
Requires: lzma
Requires: xz
# dpkg-architecture -qDEB_HOST_GNU_TYPE relies on cc -dumpmachine
Requires:  gcc
Obsoletes: dpkg-devel < 1.16
BuildArch: noarch

%description dev
This package provides the development tools (including dpkg-source)
required to unpack, build and upload Debian source packages.
 .
Most Debian source packages will require additional tools to build;
for example, most packages need make and the C compiler gcc.

%package perl
Summary: Dpkg perl modules
Requires: dpkg = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires: perl-TimeDate
Requires: perl-Time-Piece
Requires: perl(Digest::MD5)
Requires: perl(Digest::SHA)
Requires: perl(Digest::SHA1)
BuildArch: noarch

%description perl
This package provides the perl modules used by the scripts
in dpkg-dev. They cover a wide range of functionality. Among them
there are the following public modules:
.
 - Dpkg: core variables
 - Dpkg::Arch: architecture handling functions
 - Dpkg::Build::Info: build information functions
 - Dpkg::BuildFlags: set, modify and query compilation build flags
 - Dpkg::BuildOptions: parse and manipulate DEB_BUILD_OPTIONS
 - Dpkg::BuildProfile: parse and manipulate build profiles
 - Dpkg::Changelog: parse changelogs
 - Dpkg::Changelog::Entry: represents a changelog entry
 - Dpkg::Changelog::Parse: generic changelog parser for dpkg-parsechangelog
 - Dpkg::Checksums: generate and parse checksums
 - Dpkg::Compression: simple database of available compression methods
 - Dpkg::Compression::Process: wrapper around compression tools
 - Dpkg::Compression::FileHandle: transparently (de)compress files
 - Dpkg::Conf: parse dpkg configuration files
 - Dpkg::Control: parse and manipulate Debian control information
   (.dsc, .changes, Packages/Sources entries, etc.)
 - Dpkg::Control::Changelog: represent fields output by dpkg-parsechangelog
 - Dpkg::Control::Fields: manage (list of known) control fields
 - Dpkg::Control::Hash: parse and manipulate a block of RFC822-like fields
 - Dpkg::Control::Info: parse files like debian/control
 - Dpkg::Control::Tests: parse files like debian/tests/control
 - Dpkg::Deps: parse and manipulate dependencies
 - Dpkg::Exit: push, pop and run exit handlers
 - Dpkg::Gettext: wrapper around Locale::gettext
 - Dpkg::IPC: spawn sub-processes and feed/retrieve data
 - Dpkg::Index: collections of Dpkg::Control (Packages/Sources files for
   example)
 - Dpkg::Interface::Storable: base object serializer
 - Dpkg::Path: common path handling functions
 - Dpkg::Source::Package: extract Debian source packages
 - Dpkg::Substvars: substitute variables in strings
 - Dpkg::Vendor: identify current distribution vendor
 - Dpkg::Version: parse and manipulate Debian package versions
.
All the packages listed in Suggests or Recommends are used by some of the
modules.

%package -n dselect
Summary:  Debian package management front-end
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description -n dselect
dselect is a high-level interface for managing the installation and
removal of Debian software packages.
Many users find dselect intimidating and new users may prefer to use apt-based
user interfaces.

%prep
%autosetup -p1

# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(Dselect::Ftp)/d' -e '/perl(extra)/d' -e '/perl(file)/d' -e '/perl(in)/d'
EOF

%define __perl_requires %{_builddir}/dpkg-%{version}/dpkg-req
chmod +x %{__perl_requires}

%build
autoreconf
%configure --disable-linker-optimisations \
        --with-admindir=%{_localstatedir}/lib/dpkg \
        --with-libselinux \
        --without-libmd \
        --with-libz \
        --with-liblzma \
        --with-libbz2

# todo add this
#--with-devlibdir=\$${prefix}/lib/$(DEB_HOST_MULTIARCH) \
#If Fedora is not using multiarch then this probably would not make
#sense there.
%make_build


%install
%make_install

mkdir -p %{buildroot}/%{pkgconfdir}/origins

# Prepare "vendor" files for dpkg-vendor
cat <<EOF > %{buildroot}/%{pkgconfdir}/origins/fedora
Vendor: Fedora
Vendor-URL: https://www.fedoraproject.org/
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
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install -pm0644 debian/dpkg.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

# from dpkg.postinst
# Create the database files if they don't already exist
create_database() {
    admindir=${DPKG_ADMINDIR:-%{buildroot}/var/lib/dpkg}

    for file in diversions statoverride status; do
    if [ ! -f "$admindir/$file" ]; then
        touch "$admindir/$file"
    fi
    done
}

# Create log file and set default permissions if possible
create_logfile() {
    logfile=%{buildroot}/var/log/dpkg.log
    mkdir -p %{buildroot}/var/log/
    touch $logfile
    chmod 644 $logfile
    #chown root:root $logfile 2>/dev/null || chown 0:0 $logfile
}
create_database
create_logfile

%find_lang dpkg
%find_lang dpkg-dev
%find_lang dselect

rm %{buildroot}%{_libdir}/libdpkg.la

# fedora has its own implementation
rm %{buildroot}%{_bindir}/update-alternatives
rm %{buildroot}%{_mandir}/man1/update-alternatives.1
rm -r %{buildroot}%{_mandir}/*/man1/update-alternatives.1
rm -r %{buildroot}%{_sysconfdir}/alternatives/

#mkdir -p %{buildroot}%{_localstatedir}/lib/dpkg/alternatives %{buildroot}%{_localstatedir}/lib/dpkg/info \
# %{buildroot}%{_localstatedir}/lib/dpkg/parts %{buildroot}%{_localstatedir}/lib/dpkg/updates \
# %{buildroot}%{_localstatedir}/lib/dpkg/methods

%if 0%{?rhel}
# https://www.spinics.net/linux/fedora/epel-devel/msg02029.html
# avoid conflicts files with man-pages (who cares about it and pl man pages ?)
rm -rf %{buildroot}%{_mandir}/it/man1/
rm -rf %{buildroot}%{_mandir}/it/man5/
rm -rf %{buildroot}%{_mandir}/pl/man1/
%endif

%check
make VERBOSE=1 TESTSUITEFLAGS=--verbose \
    TEST_PARALLEL=4 check || :
# I've queued patches so that the test suite should be able to pass
# in 1.21.x w/ no dpkg installed.

%files -f dpkg.lang
%doc debian/changelog README AUTHORS THANKS TODO
%doc debian/README.bug-usertags debian/dpkg.cron.daily
%license debian/copyright
%dir %{pkgconfdir}
%dir %{pkgconfdir}/dpkg.cfg.d
%dir %{pkgconfdir}/origins
%config(noreplace) %{pkgconfdir}/dpkg.cfg
%config(noreplace) %{pkgconfdir}/origins/*
%config(noreplace) %{_sysconfdir}/logrotate.d/dpkg
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
%{_sbindir}/dpkg-fsys-usrunmess
%dir %{pkgdatadir}
%{pkgdatadir}/abitable
%{pkgdatadir}/cputable
%{pkgdatadir}/ostable
%{pkgdatadir}/tupletable
%{_mandir}/man1/dpkg.1.gz
%{_mandir}/man1/dpkg-deb.1.gz
%{_mandir}/man1/dpkg-maintscript-helper.1.gz
%{_mandir}/man1/dpkg-query.1.gz
%{_mandir}/man1/dpkg-split.1.gz
%{_mandir}/man1/dpkg-trigger.1.gz
%{_mandir}/man5/dpkg.cfg.5.gz
%{_mandir}/man1/dpkg-divert.1.gz
%{_mandir}/man1/dpkg-statoverride.1.gz
%{_mandir}/man8/start-stop-daemon.8.gz
%{_mandir}/man1/dpkg-realpath.1.gz
%{_mandir}/man8/dpkg-fsys-usrunmess.8.gz
%{_mandir}/*/man1/dpkg.1.gz
%{_mandir}/*/man1/dpkg-deb.1.gz
%{_mandir}/*/man1/dpkg-maintscript-helper.1.gz
%{_mandir}/*/man1/dpkg-query.1.gz
%{_mandir}/*/man1/dpkg-split.1.gz
%{_mandir}/*/man1/dpkg-trigger.1.gz
%{_mandir}/*/man5/dpkg.cfg.5.gz
%{_mandir}/*/man1/dpkg-divert.1.gz
%{_mandir}/*/man1/dpkg-statoverride.1.gz
%{_mandir}/*/man8/start-stop-daemon.8.gz
%{_mandir}/*/man1/dpkg-realpath.1.gz
%{_mandir}/*/man8/dpkg-fsys-usrunmess.8.gz
%{_datadir}/polkit-1/actions/org.dpkg.pkexec.update-alternatives.policy
%{_datadir}/doc/dpkg/*
%{_datadir}/dpkg/sh/dpkg-error.sh
%{_localstatedir}/log/%{name}.log
%{_localstatedir}/lib/dpkg

%files devel
%{_libdir}/libdpkg.a
%{_libdir}/pkgconfig/libdpkg.pc
%{_includedir}/dpkg/*.h
%{_datadir}/aclocal/dpkg-*.m4

%files dev -f dpkg-dev.lang
%doc AUTHORS THANKS debian/README.bug-usertags doc/README.api doc/frontend.txt doc/triggers.txt
%config(noreplace) %{pkgconfdir}/shlibs.default
%config(noreplace) %{pkgconfdir}/shlibs.override

%{_bindir}/dpkg-architecture
%{_bindir}/dpkg-buildpackage
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
%{pkgdatadir}/*.mk
#dpkg-dev.manpages
%{_mandir}/man5/deb-buildinfo.5.gz
%{_mandir}/man5/deb-changelog.5.gz
%{_mandir}/man5/deb-changes.5.gz
%{_mandir}/man5/deb-conffiles.5.gz
%{_mandir}/man5/deb-control.5.gz
%{_mandir}/man5/deb-extra-override.5.gz
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
%{_mandir}/man7/deb-version.7.gz
%{_mandir}/man5/deb.5.gz
%{_mandir}/man5/deb822.5.gz
%{_mandir}/man1/dpkg-architecture.1.gz
%{_mandir}/man1/dpkg-buildflags.1.gz
%{_mandir}/man1/dpkg-buildpackage.1.gz
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
%{_mandir}/man5/dsc.5.gz
%{_mandir}/*/man5/deb-buildinfo.5.gz
%{_mandir}/*/man5/deb-changelog.5.gz
%{_mandir}/*/man5/deb-changes.5.gz
%{_mandir}/*/man5/deb-conffiles.5.gz
%{_mandir}/*/man5/deb-control.5.gz
%{_mandir}/*/man5/deb-extra-override.5.gz
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
%{_mandir}/*/man7/deb-version.7.gz
%{_mandir}/*/man5/deb.5.gz
%{_mandir}/*/man5/deb822.5.gz
%{_mandir}/*/man1/dpkg-architecture.1.gz
%{_mandir}/*/man1/dpkg-buildflags.1.gz
%{_mandir}/*/man1/dpkg-buildpackage.1.gz
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
%{_mandir}/*/man5/dsc.5.gz

%files perl
%{perl_vendorlib}/Dpkg*
%{_mandir}/man3/Dpkg*.3*
%{_datadir}/dpkg/*.specs


%files -n dselect -f dselect.lang
#doc dselect/methods/multicd/README.multicd
%config(noreplace) %{pkgconfdir}/dselect.cfg
%{_bindir}/dselect
%{perl_vendorlib}/Dselect
%{_localstatedir}/lib/dpkg/methods
%{_libexecdir}/dpkg/methods
%{_mandir}/man1/dselect.1.gz
%{_mandir}/*/man1/dselect.1.gz
%{_mandir}/man5/dselect.cfg.5.gz
%{_mandir}/*/man5/dselect.cfg.5.gz
%dir %{pkgconfdir}/dselect.cfg.d


%changelog
* Mon Jun 20 2022 Muhammad Falak <mwani@microsoft.com> - 1.20-10-1
- Bump version to 1.20.10 to address CVE-2022-1664
- License verified

* Wed Nov 03 2021 Muhammad Falak <mwani@microsft.com> - 1.20.9-5
- Remove epoch from tar

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.9-4
- Initial CBL-Mariner import from Fedora 35 (license: MIT).

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.20.9-2
- Perl 5.34 rebuild

* Fri May 14 2021 Sérgio Basto <sergio@serjux.com>
- Drop requirement of perl(MIME::Lite)

* Mon May 10 2021 Sérgio Basto <sergio@serjux.com> - 1.20.9-1
- Update to 1.20.9 (#1949336)
- flex is not required anymore, doxygen is only needed if you call make doc
- The dpkg-gettext.pl and controllib.pl are long obsolete, can be removed.
- dpkg has not shipped install-info for a long while now.
- and others reviews

* Sat May 01 2021 Sérgio Basto <sergio@serjux.com> - 1.20.7.1-2
- Fix for fedora-silverblue

* Mon Feb 15 2021 Sérgio Basto <sergio@serjux.com> - 1.20.7.1-1
- Update to 1.20.7.1 (#1811388)
- Remove force C++14 as 1.20.7.1 seems ready for C++17

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Jeff Law <law@redhat.com> - 1.19.7-8
- Force C++14 as this code is not C++17 ready

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.19.7-6
- Perl 5.32 rebuild

* Tue Feb 18 2020 Sérgio Basto <sergio@serjux.com> - 1.19.7-5
- Drop Requires:perl-Digest-SHA3, dpkg-perl only needs MD5, SHA1 and SHA256
  (#1758136) related with (#1628409)
- BR: perl(Digest::MD5) need by make check

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Sérgio Basto <sergio@serjux.com> - 1.19.7-3
- More cleanings

* Thu Nov 14 2019 Sérgio Basto <sergio@serjux.com> - 1.19.7-2
- Enable custom perl_requires
- More clean up of el6 builds

* Thu Nov 14 2019 Sérgio Basto <sergio@serjux.com> - 1.19.7-1
- Upgrade dpkg to 1.19.x 1.19.7
- Won't be possible build on el7
- Remove hacks for tar <= 1.28 on el7 (patch 3)
- Remove hacks buil on el6 (patch 2)
- Remove hack for crapy /usr/lib/rpm/perl.req in EL7 (#1510214)
- Disable our custom dpkg-req

* Sat Oct 05 2019 Sérgio Basto <sergio@serjux.com> - 1.18.25-12
- BR: perl(Digest::MD5) need by make check

* Sat Oct 05 2019 Sérgio Basto <sergio@serjux.com> - 1.18.25-11
- Fix #1758136 related with #1628409 (dpkg-perl only needs MD5, SHA1 and SHA256)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.18.25-9
- Perl 5.30 rebuild

* Thu Feb 28 2019 Sérgio Basto <sergio@serjux.com> - 1.18.25-8
- Requires perl(MIME::Lite) on dpkg-dev (rhbz #1678637)
- Adds check section and performs unit tests but ignores failures

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Sérgio Basto <sergio@serjux.com> - 1.18.25-6
- po4a is now available on ppc64 and we can build dpkg there

* Sun Sep 23 2018 Sérgio Basto <sergio@serjux.com> - 1.18.25-5
- Revert "Bundle a version of tar to make it compatible in EL7"
- Keep BR: perl(Digest)
- Remove --clamp-mtime option on tar of el7.
- Add Requires perl(Digest::MD5) and perl(Digest::SHA*) on dpkg-perl (#1628409)

* Sun Sep 16 2018 Sérgio Basto <sergio@serjux.com> - 1.18.25-4
- Fix conflicts with man pages on el

* Sat Sep  8 2018 Robin Lee <cheeselee@fedoraproject.org> - 1.18.25-3
- Bundle a version of tar to make it compatible in EL7 (BZ#1626465)

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.18.25-2
- Rebuild with fixed binutils

* Sun Jul 29 2018 Sérgio Basto <sergio@serjux.com> - 1.18.25-1
- Update dpkg to 1.18.25
- Security fix: directory traversal via /DEBIAN symlink

* Sun Jul 29 2018 Sérgio Basto <sergio@serjux.com> - 1.18.24-9
- Requires(post): coreutils (#1598872)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
- https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.18.24-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.18.24-6
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 18 2017 Sérgio Basto <sergio@serjux.com> - 1.18.24-4
- Fix minor rpmlint warnings
- Make the dependency of perl-interpreter conditional

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 18 2017 Sérgio Basto <sergio@serjux.com> - 1.18.24-1
- Update dpkg to 1.18.24

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.18.22-3
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 04 2017 Sérgio Basto <sergio@serjux.com> - 1.18.22-1
- Update dpkg to 1.18.22  (#1294258)

* Sat Nov 26 2016 Sérgio Basto <sergio@serjux.com> - 1.18.15-1
- New major release, 1.18.15, adaptations based on files of debian directory in
  debian package.

* Fri Nov 25 2016 Sérgio Basto <sergio@serjux.com> - 1.17.27-1
- New upstream vesion, 1.17.27, fixes CVE-2015-0860
- Add start-stop-daemon because could be useful: https://github.com/gammu/gammu/issues/75 (RH
  system not support start-stop-daemon)
- Drop dpkg-tar-invocation.patch it is already is sources.

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.17.25-8
- Perl 5.24 rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 17 2015 Sérgio Basto <sergio@serjux.com> - 1.17.25-6
- Following debian/libdpkg-perl.install _libexecdir/dpkg/parsechangelog moved
  into dpkg-perl.
- Removed duplicated entries of _datadir/dpkg/*.mk in %%files, following
  debian/dpkg-dev.install now only in dpkg-dev.

* Sat Oct 17 2015 Sérgio Basto <sergio@serjux.com> - 1.17.25-5
- Fix rhbz #1271133
- Spec cleanups.

* Wed Jul 22 2015 Petr Pisar <ppisar@redhat.com> - 1.17.25-4
- Require perl(:MODULE_COMPAT_) symbol by packages that provide Perl modules

* Fri Jul 10 2015 Sérgio Basto <sergio@serjux.com> - 1.17.25-3
- call 'tar --no-recursion -T -' and not 'tar -T - --no-recursion' (#1241508)

* Thu Jul 02 2015 Sérgio Basto <sergio@serjux.com> - 1.17.25-1
- Update to 1.17.25 (Debian stable), adjustments following files
  dpkg-1.17.25/debian/*.install, *.postinst, etc.
- Rebased dpkg-perl-libexecdir.patch and dpkg-perl-libexecdir.epel6.patch
- Removed old defattr tags.
- Added License tag.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Sérgio Basto <sergio@serjux.com> - 1.16.16-5
- Fix build for all versions, previous try wasn't correct and back with
  dpkg-perl-libexecdir.patch .
- Added dpkg-perl-libexecdir.epel6.patch just for fix epel <= 6 .
- Cleaned some trailing whitespaces.
- Use _localstatedir instead /var .

* Sat Apr 25 2015 Sérgio Basto <sergio@serjux.com> - 1.16.16-4
- Revert location of dpkg/parsechangelog .
- Fix build for all versions, including epel-6 .

* Tue Apr 21 2015 Sérgio Basto <sergio@serjux.com> - 1.16.16-3
- Better upstream URL .

* Tue Apr 21 2015 Sérgio Basto <sergio@serjux.com> - 1.16.16-2
- Some fixes and added support for epel-6 .
- Removed Patch0: dpkg-perl-libexecdir.patch .
- move %%{_libdir}/dpkg/parsechangelog to archable package .

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 1.16.16-1
- Security update to 1.16.16

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Sérgio Basto <sergio@serjux.com> - 1.16.15-1
- Update to 1.16.15, fixes: CVE-2014-3864, CVE-2014-3865 , rhbz #1103026

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Sérgio Basto <sergio@serjux.com> - 1.16.14-1
- Update to 1.16.14, fixes CVE-2014-0471, rhbz #1092210 .

* Wed Oct 16 2013 Sérgio Basto <sergio@serjux.com> - 1.16.12-1
- Update to 1.16.12
- added /etc/dpkg/origins/... , by Oron Peled, rhbz #973832
- fix few files listed twice.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.16.10-7
- Perl 5.18 rebuild

* Mon Jul 01 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-6
- add support to logrotate, by Oron Peled, rhbz #979378
- added some new %%doc and debian/copyright, by Oron Peled, rhbz #979378
- rpmlint cleanups, by Oron Peled, rhbz #979378 

* Sun Jun 30 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-5
- rhbz #979378 
  - Obsolete the old dpkg-devel.noarch (replaced by dpkg-dev)
  (Obsoletes: dpkg-devel < 1.16)
  - Readd to dpkg-perl: Requires: dpkg = <version>-<release>
  - Patchset Signed-off-by: Oron Peled
  - [PATCH 1/4] move dpkg.cfg from /etc to /etc/dpkg 
  - [PATCH 2/4] fix some pkgdatadir, pkgconfdir file locations
  - [PATCH 3/4] move "dpkg-dev.mo" files to dpkg-perl
  - [PATCH 4/4] minor fix to dpkg-perl ownerships
- move from dpkg to dpkg-dev, rhbz #979378 
  - dpkg-mergechangelogs and its man-pages
  - dpkg-buildflags and its man-pages
- remove man pages dups, also rhbz #979378
    dpkg-architecture.1.gz
    dpkg-buildflags.1.gz
    dpkg-buildpackage.1.gz
    dpkg-checkbuilddeps.1.gz
    dpkg-distaddfile.1.gz
    dpkg-genchanges.1.gz
    dpkg-gencontrol.1.gz
    dpkg-gensymbols.1.gz
    dpkg-mergechangelogs.1.gz
    dpkg-name.1.gz
    dpkg-parsechangelog.1.gz
    dpkg-scanpackages.1.gz
    dpkg-scansources.1.gz
    dpkg-shlibdeps.1.gz
    dpkg-source.1.gz
    dpkg-vendor.1.gz

* Sun Jun 02 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-4
- provided virtual -static package rhbz #967215

* Tue May 21 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-3
- Copied from dpkg-1.16.10/debian/dpkg.postinst, on post install, runs create_database, create_logfile. 
- Based on dpkg.install and dselect.install
  created some missing directories in /var/lib/dpkg and in /etc/dpkg .
- Drop Requirement dpkg of dpkg-perl.
- Fix a FIXME , all perls moved to dpkg-perl.
- TODO: set logrotates, see debian/dpkg.logrotate.

* Fri May 17 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-2
- apply fix by Oron Peled bug #648384, adds dpkg-perl as noarch

* Thu May 16 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-1
- Add BR perl-podlators for pod2man in F19 development or just BR perl
- Add some other importants BR: doxygen flex xz-devel po4a dotconf-devel
- Fix packages names which are debianized, so packages will be: dpkg-perl
and dpkg-dev (and dpkg-devel for headers of dpkg).
- Some clean ups.
- dpkg-perl must be arched.

* Sat May  4 2013 Oron Peled <oron@actcom.co.il>
- Bump version to Debian/wheezy
- Call autoreconf: make sure we don't reuse Debian packaged
  stuff (config.guess, etc.)
- CVE patches not needed -- is already fixed upstream
- Removed dpkg-change-libdir.patch:
  - Patching Makefile.in is wrong (can patch Makefile.am with autoreconf)
  - Less patch churn for non-critical paths
  - Accept /usr/lib/dpkg/parsechangelog
  - Accept /usr/lib/dpkg/methods

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-6
- Fix CVE-2010-1679
- Fix CVE-2011-0402

* Sun Oct 17 2010 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.15.5.6-5
- Apply minimal fix for rhbz #642160

* Thu Mar 11 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-4
- Fix CVE-2010-0396

* Mon Feb 15 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-3
- review changes

* Sun Feb 14 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-2
- review changes

* Sat Feb 13 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-1
- Upgrade to latest upstream
- review changes

* Tue Nov 10 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.4.1-1
- Upgrade to latest upstream
- review changes

* Tue Dec 30 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.23-3
- more review changes               

* Mon Dec 15 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.23-1
- bump version and make some of the review changes

* Tue Aug 19 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-5
- made changes for review 

* Thu Jul 31 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-4
- Change release to -4 as server refused -3

* Thu Jul 31 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-3
- split the package into dkpg, dpkg-dev & dselect

* Tue Jul 29 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-2
- recode man files to UTF8

* Tue Jul 29 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-1
- Rebuild ans add build requires ncurses-devel

* Thu Jul 19 2007 Patrice Dumas <pertusus@free.fr> - 1.14.5-1
- initial packaging
