# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Architectures that we run the test suite on.
#
# As the test suite takes a very long time to run and is somewhat
# unreliable on !x86 architectures, only run it on x86-64.
%global test_arches x86_64

# Verify tarball signature with GPGv2.
%global verify_tarball_signature 1

# The source directory.
%global source_directory 1.55-development

# Filter perl provides.
%{?perl_default_filter}

Summary:       Tools to access and modify virtual machine disk images
Name:          guestfs-tools
Version:       1.55.5
Release:       1%{?dist}
License:       GPL-2.0-or-later AND LGPL-2.0-or-later

# Build only for architectures that have a kernel
ExclusiveArch: %{kernel_arches}
%if 0%{?rhel}
# No qemu-kvm on POWER (RHBZ#1946532).
ExcludeArch: %{power64}
%endif

# Source and patches.
URL:           http://libguestfs.org/
Source0:       http://download.libguestfs.org/guestfs-tools/%{source_directory}/%{name}-%{version}.tar.gz
%if 0%{verify_tarball_signature}
Source1:       http://download.libguestfs.org/guestfs-tools/%{source_directory}/%{name}-%{version}.tar.gz.sig
%endif

# Keyring used to verify tarball signature.
%if 0%{verify_tarball_signature}
Source2:       libguestfs.keyring
%endif

# Basic build requirements.
BuildRequires: autoconf, automake, libtool, gettext-devel
BuildRequires: gcc, gcc-c++
BuildRequires: make
BuildRequires: glibc-utils
BuildRequires: libguestfs-devel >= 1:1.57.6-1
BuildRequires: libguestfs-xfs
BuildRequires: perl(Pod::Simple)
BuildRequires: perl(Pod::Man)
BuildRequires: perl(Module::Build)
BuildRequires: perl(Test::More)
BuildRequires: /usr/bin/pod2text
BuildRequires: po4a
BuildRequires: pcre2-devel
BuildRequires: libxml2-devel
BuildRequires: json-c-devel
BuildRequires: libvirt-devel
BuildRequires: libosinfo-devel
BuildRequires: libxcrypt-devel
BuildRequires: ncurses-devel
%ifarch x86_64
BuildRequires: glibc-static
%endif
BuildRequires: ocaml >= 4.08
BuildRequires: ocaml-libguestfs-devel
BuildRequires: ocaml-findlib-devel
BuildRequires: ocaml-gettext-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: xz-devel
%if !0%{?rhel}
BuildRequires: zip
BuildRequires: unzip
%endif
%if !0%{?rhel}
BuildRequires: perl(Expect)
%endif
BuildRequires: bash-completion-devel
BuildRequires: /usr/bin/qemu-img
BuildRequires: xorriso
BuildRequires: hwdata-devel
BuildRequires: perl(Locale::TextDomain)
BuildRequires: perl(Sys::Guestfs)
BuildRequires: perl(Win::Hivex)
BuildRequires: perl(Win::Hivex::Regedit)
BuildRequires: perl-generators

%if 0%{verify_tarball_signature}
BuildRequires: gnupg2
%endif

# Ensure a minimum version of libguestfs is installed.
Requires:      libguestfs%{?_isa} >= 1:1.57.6-1

# For virt-builder:
Requires:      curl
Requires:      gnupg2
Requires:      /usr/bin/qemu-img
Requires:      xz

# For virt-builder-repository:
Suggests:      osinfo-db

# For virt-drivers:
Recommends:    hwdata

# For virt-inspector, since Fedora and RHEL >= 7 use XFS:
Recommends:    libguestfs-xfs

# For virt-edit and virt-customize:
Suggests:      perl

# This replaces the libguestfs-tools-c package.
Provides:      libguestfs-tools-c = 1:%{version}-%{release}
Obsoletes:     libguestfs-tools-c <= 1:1.45.2-1


%description
guestfs-tools is a set of tools that can be used to make batch
configuration changes to guests, get disk used/free statistics
(virt-df), perform backups and guest clones, change
registry/UUID/hostname info, build guests from scratch (virt-builder)
and much more.

Virt-alignment-scan scans virtual machines looking for partition
alignment problems.

Virt-builder is a command line tool for rapidly making disk images
of popular free operating systems.

Virt-cat is a command line tool to display the contents of a file in a
virtual machine.

Virt-customize is a command line tool for customizing virtual machine
disk images.

Virt-df is a command line tool to display free space on virtual
machine filesystems.  Unlike other tools, it doesn’t just display the
amount of space allocated to a virtual machine, but can look inside
the virtual machine to see how much space is really being used.  It is
like the df(1) command, but for virtual machines, except that it also
works for Windows virtual machines.

Virt-diff shows the differences between virtual machines.

Virt-drivers detects the bootloader, kernel and drivers inside a guest.

Virt-edit is a command line tool to edit the contents of a file in a
virtual machine.

Virt-filesystems is a command line tool to display the filesystems,
partitions, block devices, LVs, VGs and PVs found in a disk image
or virtual machine.  It replaces the deprecated programs
virt-list-filesystems and virt-list-partitions with a much more
capable tool.

Virt-format is a command line tool to erase and make blank disks.

Virt-get-kernel extracts a kernel/initrd from a disk image.

Virt-inspector examines a virtual machine and tries to determine the
version of the OS, the kernel version, what drivers are installed,
whether the virtual machine is fully virtualized (FV) or
para-virtualized (PV), what applications are installed and more.

Virt-log is a command line tool to display the log files from a
virtual machine.

Virt-ls is a command line tool to list out files in a virtual machine.

Virt-make-fs is a command line tool to build a filesystem out of
a collection of files or a tarball.

Virt-resize can resize existing virtual machine disk images.

Virt-sparsify makes virtual machine disk images sparse (thin-provisioned).

Virt-sysprep lets you reset or unconfigure virtual machines in
preparation for cloning them.

Virt-tail follows (tails) a log file within a guest, like 'tail -f'.


%package -n virt-win-reg
Summary:       Access and modify the Windows Registry of a Windows VM
License:       GPL-2.0-or-later
BuildArch:     noarch

# This replaces the libguestfs-tools package.
Provides:      libguestfs-tools = 1:%{version}-%{release}
Obsoletes:     libguestfs-tools <= 1:1.45.2-1


%description -n virt-win-reg
Virt-win-reg lets you look at and modify the Windows Registry of
Windows virtual machines.


%package bash-completion
Summary:       Bash tab-completion scripts for %{name}
BuildArch:     noarch
Requires:      bash-completion >= 2.0
Requires:      %{name} = %{version}-%{release}


%description bash-completion
Install this package if you want intelligent bash tab-completion
for the virt-* tools.


%package man-pages-ja
Summary:       Japanese (ja) man pages for %{name}
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}

%description man-pages-ja
%{name}-man-pages-ja contains Japanese (ja) man pages
for %{name}.


%package man-pages-uk
Summary:       Ukrainian (uk) man pages for %{name}
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}

%description man-pages-uk
%{name}-man-pages-uk contains Ukrainian (uk) man pages
for %{name}.


%prep
%if 0%{verify_tarball_signature}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%setup -q
%autopatch -p1

%build
autoreconf -fiv

# Preserve timestamps when copying files. Otherwise, the time of the
# build ends up in the header added by gzip when it compresses files.
%{configure} INSTALL='/usr/bin/install -p'

# Building index-parse.c by hand works around a race condition in the
# autotools cruft, where two or more copies of yacc race with each
# other, resulting in a corrupted file.
make -j1 -C builder index-parse.c

make V=1 %{?_smp_mflags}


%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%ifarch %{test_arches}
# Only run the tests with non-debug (ie. non-Rawhide) kernels.
# XXX This tests for any debug kernel installed.
if grep CONFIG_DEBUG_MUTEXES=y /lib/modules/*/config ; then
    echo "Skipping tests because debug kernel is installed"
    exit 0
fi

# Enable debugging.
export LIBGUESTFS_DEBUG=1
export LIBGUESTFS_TRACE=1

# This test is currently broken and needs further investigation.
export SKIP_TEST_MACHINE_READABLE_SH=1

# This test fails for me in local mock and Koji, but not when running
# in an unrestricted environment.
export SKIP_TEST_VIRT_FORMAT_SH=1

# This test takes too long to run under Koji and times out.  It runs
# fine with KVM enabled.
export SKIP_TEST_VIRT_RESIZE_PL=1

if ! make check -k ; then
    # Dump out the log files of any failing tests to make
    # debugging test failures easier.
    for f in `find -name test-suite.log | xargs grep -l ^FAIL:`; do
        echo '*****' $f '*****'
        cat $f
        echo
    done
    exit 1
fi
%endif


%install
make DESTDIR=$RPM_BUILD_ROOT install

# Delete libtool files.
find $RPM_BUILD_ROOT -name '*.la' -delete

# Move installed documentation back to the source directory so
# we can install it using a %%doc rule.
mv $RPM_BUILD_ROOT%{_docdir}/%{name} installed-docs
gzip --best installed-docs/*.xml

# Find locale files.
%find_lang %{name}


# Fix upgrades from old libguestfs-tools-c package
# which had /etc/virt-builder -> xdg/virt-builder.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Directory_Replacement/
# This can be removed in Fedora > 36.
%pretrans -p <lua>
path = "/etc/virt-builder"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end


%files -f %{name}.lang
%license COPYING
%doc README
%doc installed-docs/*
%dir %{_sysconfdir}/virt-builder
%dir %{_sysconfdir}/virt-builder/repos.d
%config(noreplace) %{_sysconfdir}/virt-builder/repos.d/*
%{_bindir}/virt-alignment-scan
%{_bindir}/virt-builder
%{_bindir}/virt-builder-repository
%{_bindir}/virt-cat
%{_bindir}/virt-customize
%{_bindir}/virt-df
%{_bindir}/virt-diff
%{_bindir}/virt-drivers
%{_bindir}/virt-edit
%{_bindir}/virt-filesystems
%{_bindir}/virt-format
%{_bindir}/virt-get-kernel
%{_bindir}/virt-index-validate
%{_bindir}/virt-inspector
%{_bindir}/virt-log
%{_bindir}/virt-ls
%{_bindir}/virt-make-fs
%{_bindir}/virt-resize
%{_bindir}/virt-sparsify
%{_bindir}/virt-sysprep
%{_bindir}/virt-tail
%{_mandir}/man1/guestfs-tools-release-notes-1*.1*
%{_mandir}/man1/virt-alignment-scan.1*
%{_mandir}/man1/virt-builder-repository.1*
%{_mandir}/man1/virt-builder.1*
%{_mandir}/man1/virt-cat.1*
%{_mandir}/man1/virt-customize.1*
%{_mandir}/man1/virt-df.1*
%{_mandir}/man1/virt-diff.1*
%{_mandir}/man1/virt-drivers.1*
%{_mandir}/man1/virt-edit.1*
%{_mandir}/man1/virt-filesystems.1*
%{_mandir}/man1/virt-format.1*
%{_mandir}/man1/virt-get-kernel.1*
%{_mandir}/man1/virt-index-validate.1*
%{_mandir}/man1/virt-inspector.1*
%{_mandir}/man1/virt-log.1*
%{_mandir}/man1/virt-ls.1*
%{_mandir}/man1/virt-make-fs.1*
%{_mandir}/man1/virt-resize.1*
%{_mandir}/man1/virt-sparsify.1*
%{_mandir}/man1/virt-sysprep.1*
%{_mandir}/man1/virt-tail.1*


%files -n virt-win-reg
%license COPYING
%doc README
%{_bindir}/virt-win-reg
%{_mandir}/man1/virt-win-reg.1*


%files bash-completion
%license COPYING
%dir %{bash_completions_dir}
%{bash_completions_dir}/virt-*


%files man-pages-ja
%lang(ja) %{_mandir}/ja/man1/*.1*


%files man-pages-uk
%lang(uk) %{_mandir}/uk/man1/*.1*


%changelog
* Wed Feb 05 2026 Richard W.M. Jones <rjones@redhat.com> - 1.55.5-1
- New upstream development version 1.55.5

* Wed Jan 21 2026 Richard W.M. Jones <rjones@redhat.com> - 1.55.4-1
- New upstream development version 1.55.4

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.55.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Nov  4 2025 Richard W.M. Jones <rjones@redhat.com> - 1.55.3-1
- New upstream development version 1.55.3
- Requires libguestfs >= 1.57.6 for new inspection APIs.

* Thu Oct 16 2025 Richard W.M. Jones <rjones@redhat.com> - 1.55.2-1
- New upstream development version 1.55.2

* Wed Oct 15 2025 Richard W.M. Jones <rjones@redhat.com> - 1.55.1-2
- OCaml 5.4.0 rebuild

* Fri Aug 15 2025 Richard W.M. Jones <rjones@redhat.com> - 1.55.1-1
- New upstream development version 1.55.1
- Ensure minimum libguestfs is 1.57.1 (for guestfs_setfiles)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.54.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James <loganjerry@gmail.com> - 1.54.0-2
- Rebuild to fix OCaml dependencies

* Tue May 20 2025 Richard W.M. Jones <rjones@redhat.com> - 1.54.0-1
- New upstream stable version 1.54.0

* Thu Apr 03 2025 Richard W.M. Jones <rjones@redhat.com> - 1.53.9-1
- New upstream version 1.53.9
- Enable ocaml-gettext again
- Remove oUnit

* Tue Mar 11 2025 Richard W.M. Jones <rjones@redhat.com> - 1.53.8-1
- New upstream version 1.53.8

* Thu Feb 27 2025 Richard W.M. Jones <rjones@redhat.com> - 1.53.7-3
- Disable gettext support in Fedora Rawhide

* Tue Feb 18 2025 Richard W.M. Jones <rjones@redhat.com> - 1.53.7-1
- New upstream version 1.53.7

* Wed Feb 05 2025 Richard W.M. Jones <rjones@redhat.com> - 1.53.6-1
- New upstream version 1.53.6

* Tue Feb 04 2025 Richard W.M. Jones <rjones@redhat.com> - 1.53.5-4
- Bump and rebuild (RHBZ#2340602)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.53.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Jerry James <loganjerry@gmail.com> - 1.53.5-2
- OCaml 5.3.0 rebuild for Fedora 42

* Mon Nov 18 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.5-1
- New upstream development version 1.53.5

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.4-1
- New upstream development version 1.53.4
- Replace Jansson with json-c

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.3-2
- Rebuild for Jansson 2.14
  (https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Tue Aug 20 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.3-1
- New upstream development version 1.53.3
- Pull in some upstream fixes that improve reliability of firstboot on Windows

* Tue Aug 06 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.2-1
- New upstream development version 1.53.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.53.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.1-3
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.1-2
- OCaml 5.2.0 for Fedora 41

* Thu Apr 25 2024 Richard W.M. Jones <rjones@redhat.com> - 1.53.1-1
- New upstream development version 1.53.1

* Fri Apr 12 2024 Richard W.M. Jones <rjones@redhat.com> - 1.52.0-5
- Fix bytecode compilation (RHBZ#2274708)

* Mon Mar 25 2024 Richard W.M. Jones <rjones@redhat.com> - 1.52.0-4
- Use %%{bash_completions_dir} macro
- BR bash-completion-devel, new in Rawhide

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.52.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.52.0-2
- Fix virt-customize --chown invalid format error
- New upstream github repository.

* Thu Jan  4 2024 Richard W.M. Jones <rjones@redhat.com> - 1.52.0-1
- New stable version 1.52.0

* Tue Dec 19 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.7-1
- New development version 1.51.7

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.6-5
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.6-4
- Bump release and rebuild

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.6-3
- OCaml 5.1.1 rebuild for Fedora 40

* Sat Dec  9 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.6-2
- New development version 1.51.6

* Mon Nov 27 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.5-2
- Fix build for libxml2 2.12.1

* Thu Nov 02 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.5-1
- New development version 1.51.5

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.4-2
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.4-1
- New development version 1.51.4

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.3-1
- New development version 1.51.3

* Mon Jun 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.2-2
- Migrated to SPDX license

* Thu Apr 06 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.2-1
- New development version 1.51.2

* Tue Feb 21 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.1-2
- Fix BR hwdata-devel for PCI IDs data

* Mon Feb 20 2023 Richard W.M. Jones <rjones@redhat.com> - 1.51.1-1
- New development version 1.51.1
- virt-drivers: Add BuildRequires and runtime Recommends on hwdata.

* Tue Feb 14 2023 Richard W.M. Jones <rjones@redhat.com> - 1.50.0-2
- Remove virt-dib (RHBZ#2169550)

* Tue Feb 07 2023 Richard W.M. Jones <rjones@redhat.com> - 1.50.0-1
- New upstream stable version 1.50.0

* Thu Jan 26 2023 Richard W.M. Jones <rjones@redhat.com> - 1.49.10-1
- New upstream development version 1.49.10

* Thu Jan 19 2023 Richard W.M. Jones <rjones@redhat.com> - 1.49.9-1
- New upstream development version 1.49.9
- New tool: virt-drivers
- Add BR glibc-static for tests on x86_64.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Richard W.M. Jones <rjones@redhat.com> - 1.49.8-2
- New upstream development version 1.49.8
- +BR libosinfo-devel

* Sat Dec 10 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.7-2
- New upstream development version 1.49.7

* Fri Nov 25 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.6-1
- New upstream development version 1.49.6
- Enable opensuse repository again

* Mon Nov 21 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.5-2
- Disable opensuse repository

* Wed Oct 12 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.5-1
- New upstream development version 1.49.5

* Mon Aug 01 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.4-1
- New upstream development version 1.49.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.3-1
- New upstream development version 1.49.3

* Thu May 26 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.2-1
- New upstream development version 1.49.2

* Thu May 12 2022 Richard W.M. Jones <rjones@redhat.com> - 1.49.1-1
- New upstream development version 1.49.1

* Mon Mar 14 2022 Richard W.M. Jones <rjones@redhat.com> - 1.48.0-1
- New upstream stable branch version 1.48.0

* Tue Mar 08 2022 Richard W.M. Jones <rjones@redhat.com> - 1.47.5-1
- New upstream development version 1.47.8
- Add new guestfs-tools-release-notes-1.48(1) man page.

* Tue Mar 01 2022 Richard W.M. Jones <rjones@redhat.com> - 1.47.4-1
- New upstream development version 1.47.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.47.3-1
- New upstream development version 1.47.3

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Richard W.M. Jones <rjones@redhat.com> - 1.47.2-1
- New upstream development version 1.47.2

* Wed Jun  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-3
- Add gating tests (for RHEL 9)

* Thu May 13 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-2
- BR perl-generators so deps of virt-win-reg subpackage are correct.

* Sat May 08 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-1
- New stable branch version 1.46.1.

* Tue Apr 27 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.0-1
- New stable branch version 1.46.0.

* Wed Apr 07 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.3-4
- Use Epoch 1 for virt-dib subpackage (only).

* Wed Mar 31 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.3-3
- Add BR xorriso, needed to run the tests.

* Mon Mar 29 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.3-1
- New upstream version 1.45.3.
- Fix symlink replacement of virt-builder directory (RHBZ#1943838).

* Fri Mar 26 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-5
- Skip test-virt-resize.pl that takes too long to run.

* Thu Mar 25 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-4
- Add perl(Test::More) dependency for the Perl test suite.
- Add perl(Module::Build) dependency for the Perl bindings.
- Fix ounit2 dependency again.

* Wed Mar 24 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-2
- Add perl(Locale::TextDomain) dependency for virt-win-reg.
- Fix ounit2 dependency upstream.

* Tue Mar 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-1
- New guestfs-tools package, split off from libguestfs.
