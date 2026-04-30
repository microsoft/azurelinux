## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The canonical copy of this spec file is upstream at:
# https://github.com/coreos/rpm-ostree/blob/main/packaging/rpm-ostree.spec

Summary: Hybrid image/package system
Name: rpm-ostree
Version: 2026.1
Release: %{autorelease}
License: LGPL-2.0-or-later
URL: https://github.com/coreos/rpm-ostree
# This tarball is generated via "cd packaging && make -f Makefile.dist-packaging dist-snapshot"
# in the upstream git.  It also contains vendored Rust sources.
Source0: https://github.com/coreos/rpm-ostree/releases/download/v%{version}/rpm-ostree-%{version}.tar.xz

Patch0: 0001-rpmostreed-transaction-types-fix-override-reset.patch

# See https://github.com/coreos/fedora-coreos-tracker/issues/1716
# ostree not on i686 for RHEL 10
# https://github.com/containers/composefs/pull/229#issuecomment-1838735764
%if 0%{?fedora} || 0%{?rhel} >= 10
ExcludeArch:    %{ix86}
%endif

BuildRequires: make
%if 0%{?rhel}
BuildRequires: rust-toolset
%else
BuildRequires: rust-packaging
BuildRequires: cargo
BuildRequires: rust
%endif

# Enable ASAN + UBSAN
%bcond_with sanitizers
# Embedded unit tests
%bcond_with bin_unit_tests

# Don't add the ostree-container binaries; this version
# conditional needs to be kept in sync with the bootc one.
%if 0%{?rhel} >= 10 || 0%{?fedora} > 41
    %bcond_with ostree_ext
%else
    %bcond_without ostree_ext
%endif

# This is copied from the libdnf spec
%if 0%{?rhel} && ! 0%{?centos}
%bcond_without rhsm
%else
%bcond_with rhsm
%endif

# RHEL (8,9) doesn't ship zchunk today.  Keep this in sync
# with libdnf: https://gitlab.com/redhat/centos-stream/rpms/libdnf/-/blob/762f631e36d1e42c63a794882269d26c156b68c1/libdnf.spec#L45
%if 0%{?rhel}
%bcond_with zchunk
%else
%bcond_without zchunk
%endif

# For the autofiles bits below
BuildRequires: python3-devel
# We always run autogen.sh
BuildRequires: autoconf automake libtool git
# For docs
BuildRequires: chrpath
BuildRequires: gtk-doc
BuildRequires: /usr/bin/g-ir-scanner
# Core requirements
# One way to check this: `objdump -p /path/to/rpm-ostree | grep LIBOSTREE` and pick the highest (though that might miss e.g. new struct members)
BuildRequires: pkgconfig(ostree-1) >= 2021.5
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(rpm) >= 4.14.0
BuildRequires: pkgconfig(libarchive)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: libcap-devel
BuildRequires: libattr-devel
# Needed by the ostree-ext crate
BuildRequires: libzstd-devel

# We currently interact directly with librepo (libdnf below also pulls it in,
# but duplicating to be clear)
BuildRequires: pkgconfig(librepo)

# Needed by curl-rust
BuildRequires: pkgconfig(libcurl)

BuildRequires: cmake
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(check)

# We use some libsolv types directly too (libdnf below also pulls it in,
# but duplicating to be clear)
BuildRequires: pkgconfig(libsolv)

# These are build deps which aren't strictly required in Koji/Brew builds, but
# are required for git builds. Since they're few and tiny, we just add it here
# to keep it part of `dnf builddep`.
BuildRequires: jq

#########################################################################
#                         libdnf build deps                             #
#                                                                       #
# Copy/pasted from libdnf/libdnf.spec. Removed the irrelevant bits like #
# valgrind, rhsm, swig, python, and sanitizer stuff.                    #
#########################################################################


%global libsolv_version 0.7.21
%global libmodulemd_version 2.13.0
%global librepo_version 1.18.0

BuildRequires:  cmake >= 3.5.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libsolv-devel >= %{libsolv_version}
BuildRequires:  pkgconfig(librepo) >= %{librepo_version}
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.46.0
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  rpm-devel >= 4.15.0
%if %{with rhsm}
BuildRequires:  pkgconfig(librhsm) >= 0.0.3
%endif
%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= 0.9.11
%endif
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
BuildRequires:  pkgconfig(smartcols)
BuildRequires:  gettext

Requires:       libmodulemd%{?_isa} >= %{libmodulemd_version}
Requires:       libsolv%{?_isa} >= %{libsolv_version}
Requires:       librepo%{?_isa} >= %{librepo_version}
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 11
Requires:       rpm-libs%{?_isa} >= 5.99.90
%endif

#########################################################################
#                     end of libdnf build deps                          #
#########################################################################

# For now...see https://github.com/projectatomic/rpm-ostree/pull/637
# and https://github.com/fedora-infra/fedmsg-atomic-composer/pull/17
# etc.  We'll drop this dependency at some point in the future when
# rpm-ostree wraps more of ostree (such as `ostree admin unlock` etc.)
Requires: ostree
Requires: bubblewrap
# We have been building with fuse but changed to fuse3  on:
# https://src.fedoraproject.org/rpms/rpm-ostree/c/3c602a23787fd2df873c0b18df3133c9fec4b66a
# However our code is just calling fuse's fusermount.
# We are updating our spec and code based on the discusion on:
# https://github.com/coreos/rpm-ostree/pull/5047
%if %{defined rhel} && 0%{?rhel} < 10
Requires: fuse
%else
Requires: fuse3
%endif

# For container functionality
# https://github.com/coreos/rpm-ostree/issues/3286
Requires: skopeo
Requires: bootc
%if %{without ostree_ext}
Requires: ostree-cli(ostree-container)
%endif

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
rpm-ostree is a hybrid image/package system.  It supports
"composing" packages on a build server into an OSTree repository,
which can then be replicated by client systems with atomic upgrades.
Additionally, unlike many "pure" image systems, with rpm-ostree
each client system can layer on additional packages, providing
a "best of both worlds" approach.

%package libs
Summary: Shared library for rpm-ostree

%description libs
The %{name}-libs package includes the shared library for %{name}.

%package devel
Summary: Development headers for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package includes the header files for %{name}-libs.

%prep
%autosetup -Sgit -n %{name}-%{version} -p1
%if 0%{?__isa_bits} == 32
sed -ie 's,^lto = true,lto = false,' Cargo.toml
%endif

%build
env NOCONFIGURE=1 ./autogen.sh
# Since we're hybrid C++/Rust we need to propagate this manually;
# the %%configure macro today assumes (reasonably) that one is building
# C/C++ and sets C{,XX}FLAGS
%if 0%{?build_rustflags:1}
export RUSTFLAGS="%{build_rustflags}"
%endif
%configure --disable-silent-rules --enable-gtk-doc %{?rpmdb_default} %{?with_sanitizers:--enable-sanitizers}  %{?with_bin_unit_tests:--enable-bin-unit-tests} \
  %{?with_rhsm:--enable-featuresrs=rhsm}

%make_build
%if 0%{?fedora} || 0%{?rhel} >= 10
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest
# https://pagure.io/fedora-rust/rust-packaging/issue/33
sed -i -e '/https:\/\//d' cargo-vendor.txt
%endif

%install
%make_install INSTALL="install -p -c"
%if %{without ostree_ext}
rm -vrf $RPM_BUILD_ROOT/usr/libexec/libostree/ext
%endif
find $RPM_BUILD_ROOT -name '*.la' -delete

# I try to do continuous delivery via rpmdistro-gitoverlay while
# reusing the existing spec files.  Currently RPM only supports
# mandatory file entries.  What this is doing is making each file
# entry optional - if it exists it will be picked up.  That
# way the same spec file works more easily across multiple versions where e.g. an
# older version might not have a systemd unit file.
cat > autofiles.py <<EOF
import os,sys,glob
os.chdir(os.environ['RPM_BUILD_ROOT'])
for line in sys.argv[1:]:
    if line == '':
        break
    if line[0] != '/':
        sys.stdout.write(line + '\n')
    else:
        files = glob.glob(line[1:])
        if len(files) > 0:
            sys.stderr.write('{0} matched {1} files\n'.format(line, len(files)))
            sys.stdout.write(line + '\n')
        else:
            sys.stderr.write('{0} did not match any files\n'.format(line))
EOF
PYTHON='%{python3}'
if ! test -x '%{python3}'; then
    PYTHON=python2
fi
$PYTHON autofiles.py > files \
  '%{_bindir}/*' \
  '%{_libdir}/%{name}' \
  '%{_mandir}/man*/*' \
  '%{_datadir}/dbus-1/system.d/*' \
  '%{_sysconfdir}/rpm-ostreed.conf' \
  '%{_prefix}/lib/systemd/system/*' \
  '%{_prefix}/lib/kernel/install.d/*' \
  '%{_libexecdir}/rpm-ostree*' \
%if %{with ostree_ext}
  '%{_libexecdir}/libostree/ext/*' \
%endif
  '%{_datadir}/polkit-1/actions/*.policy' \
  '%{_datadir}/dbus-1/system-services/*' \
  '%{_datadir}/bash-completion/completions/*'

$PYTHON autofiles.py > files.lib \
  '%{_libdir}/*.so.*' \
  '%{_libdir}/girepository-1.0/*.typelib'

$PYTHON autofiles.py > files.devel \
  '%{_libdir}/lib*.so' \
  '%{_includedir}/*' \
  '%{_datadir}/dbus-1/interfaces/org.projectatomic.rpmostree1.xml' \
  '%{_libdir}/pkgconfig/*' \
  '%{_datadir}/gtk-doc/html/*' \
  '%{_datadir}/gir-1.0/*-1.0.gir'

# Setup rpm-ostree-countme.timer according to presets
%post
%systemd_post rpm-ostree-countme.timer
# Only enable on rpm-ostree based systems and manually force unit enablement to
# explicitly ignore presets for this security fix
if [ -e /run/ostree-booted ]; then
    ln -snf /usr/lib/systemd/system/rpm-ostree-fix-shadow-mode.service  /usr/lib/systemd/system/multi-user.target.wants/
fi

%preun
%systemd_preun rpm-ostree-countme.timer

%postun
%systemd_postun_with_restart rpm-ostree-countme.timer

%files -f files
%doc COPYING.GPL COPYING.LGPL LICENSE README.md

%files libs -f files.lib
%if 0%{?fedora} || 0%{?rhel} >= 10
%license LICENSE.dependencies
%license cargo-vendor.txt
%endif

%files devel -f files.devel

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2026.1-2
- test: add initial lock files

* Tue Feb 17 2026 Joseph Marrero Corchado <jmarrero@redhat.com> - 2026.1-1
- Release 2026.1

* Mon Nov 03 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.12-1
- Release 2025.12

* Thu Sep 11 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.11-1
- Rebase to 2025.11

* Wed Aug 27 2025 Jonathan Lebon <jonathan@jlebon.com> - 2025.10-2
- spec: backport patch for `rpm-ostree compose rootfs --lockfile`

* Wed Jul 30 2025 Colin Walters <walters@verbum.org> - 2025.10-1
- Update to 2025.10

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.9-1
- Release v2025.9

* Tue Jun 03 2025 Colin Walters <walters@verbum.org> - 2025.8-2
- Cherry pick glibc patch

* Wed May 07 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.8-1
- Release 2025.8

* Tue Apr 29 2025 Jonathan Lebon <jonathan@jlebon.com> - 2025.7-3
- Backport "core: Ignore replaced files in rpmdb write transaction"

* Thu Apr 03 2025 Jonathan Lebon <jonathan@jlebon.com> - 2025.7-2
- Backport sysusers fix for FCOS

* Tue Apr 01 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.7-1
- Release 2025.7

* Mon Mar 17 2025 Timothée Ravier <tim@siosm.fr> - 2025.6-6
- Update backport for PR #5334 (Emulate new %%sysusers RPM scriplet)

* Wed Mar 12 2025 Adam Williamson <awilliam@redhat.com> - 2025.6-5
- Backport PR #5334 to fix ostree build with sysusers changes

* Sat Mar 08 2025 Dusty Mabe <dusty@dustymabe.com> - 2025.6-4
- Adjust libdnf CMake patch so it will apply

* Fri Mar 07 2025 Dusty Mabe <dusty@dustymabe.com> - 2025.6-3
- Fix libdnf use of CMake

* Fri Mar 07 2025 Dusty Mabe <dusty@dustymabe.com> - 2025.6-2
- Fast track support for deploying digests in OCI path

* Mon Mar 03 2025 Colin Walters <walters@verbum.org> - 2025.6-1
- Update to 2025.6

* Mon Feb 10 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.5-1
- Release 2025.5

* Thu Jan 30 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.4-1
- Release 2025.4

* Tue Jan 28 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.3-3
- spec: use autorelease on rawhide

* Tue Jan 28 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.3-2
- spec: remove kernel_install conditional temporarily

* Mon Jan 27 2025 Colin Walters <walters@verbum.org> - 2025.3-1
- Update to 2025.3, add a bcond for kernel-install

* Fri Jan 24 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.2-2
- spec: Sync with upstream

* Thu Jan 23 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.2-1
- Release 2025.2

* Thu Jan 16 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.1-2
- spec: package /lib/kernel/install.d/05-rpmostree.install

* Thu Jan 16 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.1-1
- Rebase to rpm-ostree 2025.1

* Wed Jan 15 2025 Colin Walters <walters@verbum.org> - 2024.9-5
- Drop unused patch

* Wed Jan 15 2025 Colin Walters <walters@verbum.org> - 2024.9-4
- Fast track https://github.com/coreos/rpm-ostree/pull/5224

* Tue Dec 10 2024 Colin Walters <walters@verbum.org> - 2024.9-3
- Flip bcond for ostree_ext off

* Tue Dec 10 2024 Colin Walters <walters@verbum.org> - 2024.9-2
- Add a bcond for ostree_ext

* Tue Nov 19 2024 Joseph Marrero Corchado <jmarrero@redhat.com> - 2024.9-1
- Release 2024.9

* Tue Nov 05 2024 Colin Walters <walters@verbum.org> - 2024.8-4
- spec: Add Requires: bootc

* Mon Oct 07 2024 Colin Walters <walters@verbum.org> - 2024.8-3
- Backport patch for https://gitlab.com/fedora/bootc/tracker/-/issues/29

* Thu Sep 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2024.8-2
- Add libzstd-devel BuildRequires

* Wed Sep 04 2024 Colin Walters <walters@verbum.org> - 2024.8-1
- Release 2024.8

* Fri Aug 09 2024 Joseph Marrero <jmarrero@redhat.com> - 2024.7-1
- Release 2024.7

* Tue Jul 30 2024 Peter Robinson <pbrobinson@gmail.com> - 2024.6-4
- cleanup .gitignore

* Tue Jul 30 2024 Peter Robinson <pbrobinson@gmail.com> - 2024.6-3
- Require fuse3 as ostree now uses it

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 21 2024 Joseph Marrero <jmarrero@redhat.com> - 2024.6-1
- Release 2024.6

* Tue Apr 16 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2024.5-2
- Update Rust macro usage

* Tue Apr 16 2024 Joseph Marrero Corchado <jmarrero@redhat.com> - 2024.5-1
- Rebase to 2024.5

* Tue Apr 09 2024 Timothée Ravier <tim@siosm.fr> - 2024.4-5
- Backport fix for /etc/[g]shadow permissions

* Tue Apr 02 2024 Timothée Ravier <tim@siosm.fr> - 2024.4-4
- Cleanup unused patch

* Thu Mar 21 2024 Colin Walters <walters@verbum.org> - 2024.4-3
- Backport patch to fix https://github.com/coreos/rpm-ostree/issues/4879

* Fri Mar 15 2024 Colin Walters <walters@verbum.org> - 2024.4-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2024.4

* Fri Mar 15 2024 Colin Walters <walters@verbum.org> - 2024.4-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2024.4

* Sun Feb 25 2024 Joseph Marrero <jmarrero@redhat.com> - 2024.3-2
- Backport: https://github.com/coreos/rpm-
  ostree/commit/fe586621e5014d14f92b913338171a02ed29e6cc

* Tue Feb 20 2024 Joseph Marrero <jmarrero@redhat.com> - 2024.3-1
- Release 2024.3

* Thu Jan 25 2024 Joseph Marrero <jmarrero@redhat.com> - 2024.2-1
- Release 2024.2

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Colin Walters <walters@verbum.org> - 2024.1-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2024.1

* Mon Dec 18 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.12-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.12

* Wed Nov 29 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.11-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.11

* Wed Nov 15 2023 Timothée Ravier <tim@siosm.fr> - 2023.10-4
- Setup rpm-ostree-countme.timer according to presets

* Thu Oct 26 2023 Colin Walters <walters@verbum.org> - 2023.10-3
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.10

* Wed Oct 04 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.8-3
- Update python3 macros and dependency.

* Wed Sep 27 2023 Colin Walters <walters@verbum.org> - 2023.8-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.8

* Tue Aug 29 2023 Colin Walters <walters@verbum.org> - 2023.6-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.5-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.5

* Tue Jun 13 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.4-5
- Switch License tags to SPDX

* Thu May 25 2023 Adam Williamson <awilliam@redhat.com> - 2023.4-4
- Backport libdnf patches to work with rpm-4.19

* Fri May 19 2023 Petr Pisar <ppisar@redhat.com> - 2023.4-3
- Rebuild against rpm-4.19 (https://fedoraproject.org/wiki/Changes/RPM-4.19)

* Thu May 18 2023 Colin Walters <walters@verbum.org> - 2023.4-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.4

* Mon Apr 24 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.3-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.3

* Tue Mar 07 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.2-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.2

* Thu Feb 16 2023 Colin Walters <walters@verbum.org> - 2023.1-4
- Cherry pick
  https://github.com/coreos/rpm-ostree/pull/4308/commits/476afb1d08513cb74cd1d28490c5e028c70f67c2

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 2023.1-3
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jonathan Lebon <jonathan@jlebon.com> - 2023.1-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2023.1

* Tue Dec 20 2022 Colin Walters <walters@verbum.org> - 2022.19-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.19

* Tue Dec 13 2022 Colin Walters <walters@verbum.org> - 2022.18-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.18

* Mon Dec 12 2022 Colin Walters <walters@verbum.org> - 2022.17-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.17

* Mon Nov 28 2022 Colin Walters <walters@verbum.org> - 2022.16-2
- Cherry pick https://github.com/coreos/rpm-ostree/pull/4166

* Fri Nov 18 2022 Jonathan Lebon <jonathan@jlebon.com> - 2022.16-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.16

* Wed Nov 02 2022 Jonathan Lebon <jonathan@jlebon.com> - 2022.15-3
- Backport semanage bug workaround
  https://github.com/coreos/rpm-ostree/pull/4122

* Tue Nov 01 2022 Colin Walters <walters@verbum.org> - 2022.15-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.15

* Thu Oct 13 2022 Joseph Marrero <jmarrero@fedoraproject.org> - 2022.14-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.14

* Sat Aug 27 2022 Colin Walters <walters@verbum.org> - 2022.13-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.13

* Sun Aug 07 2022 Colin Walters <walters@verbum.org> - 2022.12-4
- Cherry pick patch to work around filesystem package

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Colin Walters <walters@verbum.org> - 2022.12-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.12

* Mon Jul 11 2022 Colin Walters <walters@verbum.org> - 2022.11-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.11

* Thu Jun 16 2022 Colin Walters <walters@verbum.org> - 2022.10-3
- Backport https://github.com/coreos/rpm-ostree/pull/3771

* Tue Jun 14 2022 Colin Walters <walters@verbum.org> - 2022.10-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.10

* Fri May 13 2022 Jonathan Lebon <jonathan@jlebon.com> - 2022.9-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.9

* Wed Apr 20 2022 Colin Walters <walters@verbum.org> - 2022.8-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.8

* Mon Apr 11 2022 Colin Walters <walters@verbum.org> - 2022.7-2
- Rebase to 2022.7

* Fri Apr 08 2022 Colin Walters <walters@verbum.org> - 2022.6-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.6

* Thu Mar 24 2022 Jonathan Lebon <jonathan@jlebon.com> - 2022.5.80.gb7f91619
- Git snapshot for https://github.com/coreos/rpm-ostree/pull/3535

* Thu Mar 03 2022 Jonathan Lebon <jonathan@jlebon.com> - 2022.5-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.5

* Tue Mar 01 2022 Joseph Marrero <jmarrero@fedoraproject.org> - 2022.4-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.4

* Mon Feb 28 2022 Joseph Marrero <jmarrero@fedoraproject.org> - 2022.3-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.3

* Thu Feb 03 2022 Joseph Marrero <jmarrero@fedoraproject.org> - 2022.2-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.2

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Colin Walters <walters@verbum.org> - 2022.1-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2022.1

* Wed Nov 17 2021 Colin Walters <walters@verbum.org> - 2021.14-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.14

* Wed Nov 03 2021 Luca BRUNO <lucab@lucabruno.net> - 2021.13-2
- Backport patch to fix F35 rebases through DBus
  https://github.com/coreos/rpm-ostree/pull/3199

* Tue Nov 02 2021 Luca BRUNO <lucab@lucabruno.net> - 2021.13-1
- New upstream version
  https://github.com/coreos/rpm-ostree/releases/tag/v2021.13

* Thu Oct 14 2021 Colin Walters <walters@verbum.org> - 2021.12-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.12

* Thu Sep 30 2021 Colin Walters <walters@verbum.org> - 2021.11-3
- Backport patch for openshift/os extensions + multiarch

* Fri Sep 24 2021 Colin Walters <walters@verbum.org> - 2021.11-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.11

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2021.10-3
- Rebuilt with OpenSSL 3.0.0

* Fri Aug 27 2021 Colin Walters <walters@verbum.org> - 2021.10-2
- Backport
  https://github.com/coreos/rpm-ostree/pull/3095/commits/1d445170b97e8eaad6979b68f1c3ce3481c801ea

* Thu Aug 26 2021 Jonathan Lebon <jonathan@jlebon.com> - 2021.10-1
- New release v2021.10
  https://github.com/coreos/rpm-ostree/releases/tag/v2021.10

* Thu Aug 19 2021 Colin Walters <walters@verbum.org> - 2021.9-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.9

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jonathan Lebon <jonathan@jlebon.com> - 2021.7-1
- New release v2021.7
  https://github.com/coreos/rpm-ostree/releases/tag/v2021.7

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 2021.6-3
- Rebuild for versioned symbols in json-c

* Tue Jun 22 2021 Colin Walters <walters@verbum.org>
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.6

* Thu Jun 17 2021 Luca BRUNO <lucab@lucabruno.net> - 2021.5-2
- Backport _dbpath fixes, see
  https://github.com/coreos/rpm-ostree/issues/2904

* Wed May 12 2021 Luca BRUNO <lucab@lucabruno.net> - 2021.5-1
- New upstream version
  https://github.com/coreos/rpm-ostree/releases/tag/v2021.5

* Sun May 09 2021 Jeff Law <jlaw@tachyum.com> - 2021.4-4
- Re-enable LTO

* Wed Apr 28 2021 Colin Walters <walters@verbum.org> - 2021.4-3
- Backport another patch for https://pagure.io/fedora-infrastructure/issue/9909

* Tue Apr 27 2021 Colin Walters <walters@verbum.org> - 2021.4-2
- Backport patch for https://pagure.io/fedora-infrastructure/issue/9909

* Mon Apr 12 2021 Jonathan Lebon <jonathan@jlebon.com> - 2021.4-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.4

* Wed Mar 17 2021 Colin Walters <walters@verbum.org> - 2021.3-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.3

* Wed Feb 17 2021 Colin Walters <walters@verbum.org> - 2021.2-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.2

* Wed Feb 10 2021 Colin Walters <walters@verbum.org> - 2021.1-4
- Backport patches from https://github.com/coreos/rpm-ostree/pull/2553

* Tue Jan 26 2021 Jonathan Lebon <jonathan@jlebon.com> - 2021.1-3
- Backport https://github.com/coreos/rpm-ostree/pull/2490 for rawhide

* Tue Jan 19 15:08:59 UTC 2021 Colin Walters <walters@verbum.org> - 2021.1-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2021.1

* Fri Dec 11 19:13:03 UTC 2020 Colin Walters <walters@verbum.org> - 2020.10-3
- https://github.com/coreos/rpm-ostree/releases/tag/v2020.10

* Fri Dec 11 13:42:33 UTC 2020 Colin Walters <walters@verbum.org> - 2020.9-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2020.9

* Sat Nov 14 14:51:20 UTC 2020 Colin Walters <walters@verbum.org> - 2020.8-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2020.8

* Mon Nov 02 2020 Luca BRUNO <lucab@lucabruno.net> - 2020.7-1
- New upstream version
  https://github.com/coreos/rpm-ostree/releases/tag/v2020.7

* Mon Nov 02 2020 Jeff Law <law@redhat.com> - 2020.6-2
- Fix invalid use of volatile caught by gcc-11

* Fri Oct 30 16:48:43 UTC 2020 Colin Walters <walters@verbum.org> - 2020.6-1
- https://github.com/coreos/rpm-ostree/releases/tag/v2020.6

* Wed Oct 28 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.5-2
- sysroot: Fix usage of sd_journal_send on 32 bit (gh#2276)

* Tue Sep 15 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.5-1
- New upstream version
  https://github.com/coreos/rpm-ostree/releases/tag/v2020.5

* Mon Aug 17 2020 Colin Walters <walters@verbum.org> - 2020.4.15.g8b0bcd7b-2
- Update to latest upstream git for
  https://bugzilla.redhat.com/show_bug.cgi?id=1865397

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.4-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.4-1
- New upstream version
  https://github.com/coreos/rpm-ostree/releases/tag/v2020.4

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <aw@redhat.com> - 2020.3-2
- Disable LTO

* Fri Jun 19 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.3-1
- New upstream version
  https://github.com/coreos/rpm-ostree/releases/tag/v2020.3

* Fri May 15 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.2-3
- Backport https://github.com/coreos/rpm-ostree/pull/2096
  See https://github.com/coreos/fedora-coreos-tracker/issues/481

* Fri May 15 2020 Colin Walters <walters@verbum.org> - 2020.2-2
- https://github.com/coreos/rpm-ostree/releases/tag/v2020.2

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 2020.1.80.g3ec5e287-2
- Rebuild (json-c)

* Mon Apr 20 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.1.80.g3ec5e287-1
- git master snapshot for using strict mode and lockfile-repos in FCOS:
  https://github.com/coreos/rpm-ostree/pull/1858
  https://github.com/coreos/rpm-ostree/pull/2058
  https://github.com/coreos/fedora-coreos-tracker/issues/454

* Fri Mar 13 2020 Colin Walters <walters@verbum.org> - 2020.1.21.ge9011530-2
- Backport https://github.com/coreos/rpm-ostree/pull/2015
  See https://github.com/coreos/fedora-coreos-tracker/issues/343

* Thu Feb 27 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.1.21.ge9011530-1
- git master snapshot for using base initramfs kargs in RHCOS:
  https://github.com/coreos/rpm-ostree/pull/1998
  https://github.com/coreos/rpm-ostree/pull/1997
  https://bugzilla.redhat.com/show_bug.cgi?id=1806588

* Wed Feb 05 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.1-1
- New upstream version

* Tue Feb 04 2020 Jonathan Lebon <jonathan@jlebon.com> - 2019.7.31.g70c38563-1
- git master snapshot for Silverblue rawhide compose fixes
  https://pagure.io/releng/failed-composes/issue/717
  https://pagure.io/releng/failed-composes/issue/929
  https://github.com/rpm-software-management/libdnf/pull/885

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Jonathan Lebon <jonathan@jlebon.com> - 2019.7-2
- Backport patch for Silverblue composes:
  https://pagure.io/releng/failed-composes/issue/717

* Thu Dec 19 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.7-1
- New upstream version

* Sat Dec 14 2019 Jeff Law <law@redhat.com> - 2019.6.24.gfec61ce5-2
- Fix missing #includes for gcc-10

* Thu Oct 31 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.6.27.g3b8a1ec6-1
- git master snapshot for dracut cpio cap_mknod fix:
  https://github.com/coreos/rpm-ostree/pull/1946

* Thu Oct 31 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.6.24.gfec61ce5-1
- git master snapshot for HMAC path fix for FIPS:
  https://github.com/coreos/rpm-ostree/pull/1934

* Wed Sep 25 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.6-1
- New upstream version

* Thu Aug 22 2019 Colin Walters <walters@verbum.org> - 2019.5.7.gcac5aa41-3
- New upstream git snapshot, mainly for backporting the arch-includes conditionals
  to aid Fedora CoreOS on s390x.

* Wed Jul 31 2019 Stephen Gallagher <sgallagh@redhat.com> - 2019.5-2
- Fix libmodulemd dependencies

* Thu Jul 25 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.5-1
- New upstream version

* Fri Jul 19 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4.39.g8d90d03d-1
- git master snapshot for --parent and lockfile overrides
  https://github.com/projectatomic/rpm-ostree/pull/1871
  https://github.com/projectatomic/rpm-ostree/pull/1867

* Fri Jul 12 2019 Colin Walters <walters@verbum.org> - 2019.4.28.g44395673-3
- Update rpmostree-rust.h in sources

* Fri Jul 12 2019 Colin Walters <walters@verbum.org> - 2019.4.28.g44395673-2
- Update with git snapshot for zstd support

* Wed Jul 10 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4.27.gb381e029-1
- git master snapshot for add-commit-metadata
  https://github.com/projectatomic/rpm-ostree/pull/1865/

* Fri Jun 14 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4.15.gbbc9aa9f-1
- git master snapshot for OSTree layers
  https://github.com/projectatomic/rpm-ostree/pull/1830/

* Mon Jun 10 22:13:22 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2019.4.10.gc1cc0827-3
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:05 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2019.4.10.gc1cc0827-2
- Rebuild for RPM 4.15

* Thu Jun 06 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4.10.gc1cc0827-1
- git master snapshot for lockfile
  https://github.com/projectatomic/rpm-ostree/pull/1745/

* Tue May 28 2019 Dusty Mabe <dusty@dustymabe.com> - 2019.4-3
- Add back in ppc64le and ppc64

* Thu May 23 2019 Dusty Mabe <dusty@dustymabe.com> - 2019.4-2
- Backport patch for db diff --format=json

* Tue May 21 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4-1
- New upstream version

* Mon May 06 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.3.5.g0da9f997-2
- Add temporary hack to avoid UTF-8 for Bodhi
  https://pagure.io/releng/issue/8330

* Tue Apr 09 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.3.5.g0da9f997-1
- git master snapshot to test coreos-continuous tag

* Wed Mar 27 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.3-1
- New upstream version

* Thu Feb 14 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.2-1
- New upstream version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.1-1
- New upstream version

* Fri Dec 14 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.10-1
- New upstream version

* Tue Dec 04 2018 Jonathan Lebon <jonathan@jlebon.com>
- Simplify Rust conditionals

* Fri Nov 02 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.9-3
- Backport patch for https://pagure.io/dusty/failed-composes/issue/956

* Tue Oct 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2018.9-2
- Rebuild for libsolv 0.7

* Sun Oct 28 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.9-1
- New upstream version

* Tue Sep 11 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.8-1
- New upstream version

* Thu Aug 09 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.7-1
- New upstream version

* Wed Aug 01 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.6.42.gda27b94b-1
- git master snapshot for https://bugzilla.redhat.com/show_bug.cgi?id=1565647

* Mon Jul 30 2018 Colin Walters <walters@verbum.org> - 2018.6-4
- Backport patch for https://bugzilla.redhat.com/show_bug.cgi?id=1607223
  from https://github.com/projectatomic/rpm-ostree/pull/1469
- Also https://github.com/projectatomic/rpm-ostree/pull/1461

* Mon Jul 16 2018 Colin Walters <walters@verbum.org> - 2018.6-3
- Make build python3-only compatible for distributions that want that

* Fri Jun 29 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.6-2
- Rebuild for yummy Rusty bitsy

* Fri Jun 29 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.6-1
- New upstream version

* Tue May 15 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.5-1
- New upstream version

* Mon Mar 26 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.4-1
- New upstream version

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2018.3-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Mar 07 2018 Jonathan Lebon <jlebon@redhat.com> - 2018.3-3
- Add BR on gcc-c++

* Thu Mar 01 2018 Dusty Mabe <dusty@dustymabe.com> - 2018.3-2
- backport treating FUSE as netfs
- See https://github.com/projectatomic/rpm-ostree/pull/1285

* Sun Feb 18 2018 Jonathan Lebon <jlebon@redhat.com> - 2018.3-1
- New upstream version (minor bugfix release)

* Fri Feb 16 2018 Jonathan Lebon <jlebon@redhat.com> - 2018.2-1
- New upstream version

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Dusty Mabe <dusty@dustymabe.com> - 2018.1-2
- Revert the ostree:// formatting in the output.
- See https://github.com/projectatomic/rpm-ostree/pull/1136#issuecomment-358122137

* Mon Jan 15 2018 Colin Walters <walters@verbum.org> - 2018.1-1
- https://github.com/projectatomic/rpm-ostree/releases/tag/v2018.1

* Tue Dec 05 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.11-1
- New upstream version

* Wed Nov 22 2017 Colin Walters <walters@verbum.org> - 2017.10-3
- Backport patch for NFS issues
- https://pagure.io/atomic-wg/issue/387

* Sun Nov 12 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.10-2
- Backport fix for --repo handling
  https://github.com/projectatomic/rpm-ostree/pull/1101

* Thu Nov 02 2017 Colin Walters <walters@verbum.org> - 2017.10-1
- https://github.com/projectatomic/rpm-ostree/releases/tag/v2017.10

* Mon Sep 25 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.9-1
- New upstream version

* Mon Aug 21 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.8-2
- Patch to allow metadata_expire=0
  https://github.com/projectatomic/rpm-ostree/issues/930

* Fri Aug 18 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.8-1
- New upstream version

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 2017.7-7
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 2017.7-6
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.7-3
- Tweak new pkg name to rpm-ostree-libs to be more consistent with the main
  package name and ostree's ostree-libs.

* Fri Jul 21 2017 Colin Walters <walters@verbum.org> - 2017.7-2
- Enable introspection, rename shared lib to librpmostree
  Due to an oversight, we were not actually building with introspection.
  Fix that.  And while we are here, split out a shared library package,
  so that e.g. containers can do `from gi.repository import RpmOstree`
  without dragging in the systemd service, etc. (RHBZ#1473701)

* Mon Jul 10 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.7-1
- New upstream version

* Sat Jun 24 2017 Colin Walters <walters@verbum.org>
- Update to git snapshot to help debug compose failure

* Wed May 31 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.6-3
- Make sure we don't auto-provide libdnf (RHBZ#1457089)

* Fri May 26 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.6-2
- Bump libostree dep

* Fri May 26 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.6-1
- New upstream version

* Fri Apr 28 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.5-2
- Bump libostree dep and rebuild in override

* Fri Apr 28 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.5-1
- New upstream version

* Fri Apr 14 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.4-2
- Backport patch to allow unprivileged `rpm-ostree status`

* Thu Apr 13 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.4-1
- New upstream version.

* Fri Apr 07 2017 Colin Walters <walters@verbum.org> - 2017.3-4
- Backport patch to add API devices for running on CentOS 7
  https://github.com/projectatomic/rpm-ostree/issues/727

* Thu Mar 16 2017 Colin Walters <walters@verbum.org> - 2017.3-3
- Add patch to fix f26 altfiles

* Fri Mar 10 2017 Colin Walters <walters@verbum.org> - 2017.3-2
- Backport patch for running in koji

* Mon Mar 06 2017 Colin Walters <walters@verbum.org> - 2017.3-1
- New upstream version
  Fixes: CVE-2017-2623
  Resolves: #1422157

* Fri Mar 03 2017 Colin Walters <walters@verbum.org> - 2017.2-5
- Add patch to bump requires for ostree

* Mon Feb 27 2017 Colin Walters <walters@verbum.org> - 2017.2-4
- Add requires on ostree

* Sat Feb 18 2017 Colin Walters <walters@verbum.org> - 2017.2-3
- Add patch for gperf 3.1 compatibility
  Resolves: #1424268

* Wed Feb 15 2017 Colin Walters <walters@verbum.org> - 2017.2-2
- New upstream version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Colin Walters <walters@verbum.org> - 2017.1-3
- Back out netns usage for now for https://pagure.io/releng/issue/6602

* Sun Jan 22 2017 Colin Walters <walters@verbum.org> - 2017.1-2
- New upstream version

* Mon Dec 12 2016 walters@redhat.com - 2016.13-1
- New upstream version

* Sat Nov 26 2016 walters@redhat.com - 2016.12-4
- Backport patch to fix install-langs

* Tue Nov 15 2016 walters@redhat.com - 2016.11-2
- New upstream version

* Mon Oct 24 2016 walters@verbum.org - 2016.11-1
- New upstream version

* Fri Oct 07 2016 walters@redhat.com - 2016.10-1
- New upstream version

* Thu Sep 08 2016 walters@redhat.com - 2016.9-1
- New upstream version

* Thu Sep 08 2016 walters@redhat.com - 2016.8-1
- New upstream version

* Thu Sep 01 2016 walters@redhat.com - 2016.7-4
- Add requires on fuse https://github.com/projectatomic/rpm-ostree/issues/443

* Wed Aug 31 2016 Colin Walters <walters@verbum.org> - 2016.7-3
- Backport patch for running inside mock

* Sat Aug 13 2016 walters@redhat.com - 2016.6-3
- New upstream version

* Sat Aug 13 2016 Colin Walters <walters@verbum.org> - 2016.6-2
- Backport patches from master to fix non-containerized composes

* Thu Aug 11 2016 walters@redhat.com - 2016.6-1
- New upstream version

* Mon Jul 25 2016 Colin Walters <walters@verbum.org> - 2016.5-1
- New upstream version

* Fri Jul 08 2016 walters@verbum.org - 2016.4-2
- Require bubblewrap

* Fri Jul 08 2016 walters@redhat.com - 2016.4-1
- New upstream version

* Thu Jul 07 2016 Colin Walters <walters@verbum.org> - 2016.3.5.g4219a96-1
- Backport fixes from https://github.com/projectatomic/rpm-ostree/commits/2016.3-fixes

* Wed Jun 15 2016 Colin Walters <walters@verbum.org> - 2016.3.3.g17fb980-2
- Backport fixes from https://github.com/projectatomic/rpm-ostree/commits/2016.3-fixes

* Fri May 20 2016 Colin Walters <walters@redhat.com> - 2016.3-2
- New upstream version

* Thu Mar 31 2016 Colin Walters <walters@redhat.com> - 2016.1-3
- Backport patch to fix Fedora composes writing data into source file:/// URIs

* Thu Mar 24 2016 Colin Walters <walters@redhat.com> - 2016.1-2
- New upstream version

* Tue Feb 23 2016 Colin Walters <walters@redhat.com> - 2015.11.43.ga2c052b-2
- New git snapshot, just getting some new code out there
- We are now bundling a copy of libhif, as otherwise coordinated releases with
  PackageKit/dnf would be required, and we are not ready for that yet.

* Wed Feb 10 2016 Matthew Barnes <mbarnes@redhat.com> - 2015.11-3
- Fix URL: https://github.com/projectatomic/rpm-ostree

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2015.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Colin Walters <walters@redhat.com> - 2015.11-1
- New upstream version

* Sat Nov 21 2015 Colin Walters <walters@redhat.com> - 2015.10-1
- New upstream version

* Mon Nov 09 2015 Colin Walters <walters@redhat.com> - 2015.9-4
- Fix files list for -devel, which should in turn fix Anaconda
  builds which pull in rpm-ostree, but should not have devel bits.

* Sat Oct 31 2015 Colin Walters <walters@redhat.com> - 2015.9-3
- Add patch that should fix bodhis use of --workdir-tmpfs

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 2015.9-2
- Rebuilt for librpm soname bump

* Wed Aug 26 2015 Colin Walters <walters@redhat.com> - 2015.9-2
- New upstream version

* Tue Aug 04 2015 Colin Walters <walters@redhat.com> - 2015.8-1
- New upstream version

* Mon Jul 27 2015 Colin Walters <walters@redhat.com> - 2015.7-5
- rebuilt

* Mon Jul 20 2015 Colin Walters <walters@redhat.com> - 2015.7-4
- Rebuild for CentOS update to libhif

* Tue Jun 16 2015 Colin Walters <walters@redhat.com> - 2015.7-3
- Rebuild to pick up hif_source_set_required()

* Mon Jun 15 2015 Colin Walters <walters@redhat.com> - 2015.7-2
- New upstream version

* Tue Jun 09 2015 Colin Walters <walters@redhat.com> - 2015.6-2
- New upstream version

* Tue May 12 2015 Colin Walters <walters@redhat.com> - 2015.5-3
- Add patch to fix rawhide composes

* Mon May 11 2015 Colin Walters <walters@redhat.com> - 2015.5-2
- New upstream release
  Adds shared library and -devel subpackage

* Fri Apr 10 2015 Colin Walters <walters@redhat.com> - 2015.4-2
- New upstream release
  Port to libhif, drops dependency on yum.

* Thu Apr 09 2015 Colin Walters <walters@redhat.com> - 2015.3-8
- Cherry pick f21 patch to disable read only /etc with yum which
  breaks when run inside docker

* Wed Apr 08 2015 Colin Walters <walters@redhat.com> - 2015.3-7
- Add patch to use yum-deprecated
  Resolves: #1209695

* Fri Feb 27 2015 Colin Walters <walters@redhat.com> - 2015.3-5
- Drop /usr/bin/atomic, now provided by the "atomic" package

* Fri Feb 06 2015 Dennis Gilmore <dennis@ausil.us> - 2015.3-4
- add git to BuildRequires

* Thu Feb 05 2015 Colin Walters <walters@redhat.com> - 2015.3-3
- Adapt to Hawkey 0.5.3 API break

* Thu Feb 05 2015 Dennis Gilmore <dennis@ausil.us> - 2015.3-3
- rebuild for libhawkey soname bump

* Fri Jan 23 2015 Colin Walters <walters@redhat.com> - 2015.3-2
- New upstream release

* Thu Jan 08 2015 Colin Walters <walters@redhat.com> - 2015.2-1
- New upstream release

* Wed Dec 17 2014 Colin Walters <walters@redhat.com> - 2014.114-2
- New upstream release

* Tue Nov 25 2014 Colin Walters <walters@redhat.com> - 2014.113-1
- New upstream release

* Mon Nov 24 2014 Colin Walters <walters@redhat.com> - 2014.112-1
- New upstream release

* Mon Nov 17 2014 Colin Walters <walters@redhat.com> - 2014.111-1
- New upstream release

* Fri Nov 14 2014 Colin Walters <walters@redhat.com> - 2014.110-1
- New upstream release

* Fri Oct 24 2014 Colin Walters <walters@redhat.com> - 2014.109-1
- New upstream release

* Sat Oct 04 2014 Colin Walters <walters@redhat.com> - 2014.107-2
- New upstream release

* Mon Sep 08 2014 Colin Walters <walters@redhat.com> - 2014.106-3
- New upstream release
- Bump requirement on ostree

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.105-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Colin Walters <walters@verbum.org> - 2014.105-2
- New upstream release

* Sun Jul 13 2014 Colin Walters <walters@verbum.org>
- New upstream release

* Sat Jun 21 2014 Colin Walters <walters@verbum.org>
- New upstream release
- Bump OSTree requirements
- Enable hawkey package diff, we have new enough versions
  of libsolv/hawkey
- Enable /usr/bin/atomic symbolic link

* Tue Jun 10 2014 Colin Walters <walters@verbum.org>
- New upstream git snapshot

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Colin Walters <walters@verbum.org>
- New upstream release

* Fri May 23 2014 Colin Walters <walters@verbum.org>
- Previous autobuilder code is split off into rpm-ostree-toolbox

* Sun Apr 13 2014 Colin Walters <walters@verbum.org>
- New upstream release

* Tue Apr 08 2014 Colin Walters <walters@verbum.org>
- Drop requires on yum to allow minimal images without it

* Mon Mar 31 2014 Colin Walters <walters@verbum.org>
- New upstream release

* Sat Mar 22 2014 Colin Walters <walters@verbum.org> - 2014.6.3.g5707fa7-2
- Bump ostree version requirement

* Sat Mar 22 2014 Colin Walters <walters@verbum.org> - 2014.6.3.g5707fa7-1
- New git snapshot, add rpm-ostree-sign to file list

* Sat Mar 22 2014 Colin Walters <walters@verbum.org> - 2014.6-1
- New upstream version

* Fri Mar 07 2014 Colin Walters <walters@verbum.org> - 2014.5-1
- Initial package

## END: Generated by rpmautospec
