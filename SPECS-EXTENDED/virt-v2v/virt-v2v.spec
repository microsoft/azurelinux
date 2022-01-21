Vendor:         Microsoft Corporation
Distribution:   Mariner
# If there are patches which touch autotools files, set this to 1.
%global patches_touch_autotools %{nil}

# The source directory.
%global source_directory 1.42-stable

Name:          virt-v2v
Version:       1.42.0
Release:       7%{?dist}
Summary:       Convert a virtual machine to run on KVM

License:       GPLv2+
URL:           https://github.com/libguestfs/virt-v2v

Source0:       http://download.libguestfs.org/virt-v2v/%{source_directory}/%{name}-%{version}.tar.gz

# libguestfs hasn't been built on i686 for a while since there is no
# kernel built for this architecture any longer and libguestfs rather
# fundamentally depends on the kernel.  Therefore we must exclude this
# arch.  Note there is no bug filed for this because we do not ever
# expect that libguestfs or virt-v2v will be available on i686 so
# there is nothing that needs fixing.
ExcludeArch:   %{ix86}

%if 0%{patches_touch_autotools}
BuildRequires: autoconf, automake, libtool
%endif

BuildRequires: /usr/bin/pod2man
BuildRequires: gcc
BuildRequires: ocaml >= 4.01
BuildRequires: libguestfs-devel >= 1.40

BuildRequires: augeas-devel
BuildRequires: bash-completion
BuildRequires: file-devel
BuildRequires: gettext-devel
BuildRequires: jansson-devel
BuildRequires: libosinfo-devel
BuildRequires: libvirt-devel
BuildRequires: libvirt-daemon-qemu
BuildRequires: libvirt-daemon-kvm
BuildRequires: libxml2-devel
BuildRequires: pcre-devel
BuildRequires: perl(Sys::Guestfs)
BuildRequires: po4a
BuildRequires: /usr/bin/virsh

BuildRequires: ocaml-findlib-devel
BuildRequires: ocaml-libguestfs-devel
BuildRequires: ocaml-fileutils-devel
BuildRequires: ocaml-gettext-devel
BuildRequires: ocaml-ounit-devel

BuildRequires: nbdkit-python-plugin

Requires:      libguestfs%{?_isa} >= 1.40
Requires:      libguestfs-tools-c >= 1.40

Requires:      gawk
Requires:      gzip
Requires:      unzip
Requires:      curl
Requires:      /usr/bin/virsh

Recommends:    nbdkit
Recommends:    nbdkit-curl-plugin
Recommends:    nbdkit-python-plugin
Recommends:    nbdkit-ssh-plugin
Recommends:    nbdkit-vddk-plugin

# For rhsrvany.exe, used to install firstboot scripts in Windows guests.
Requires:      mingw32-srvany >= 1.0-13


%description
Virt-v2v converts a single guest from a foreign hypervisor to run on
KVM.  It can read Linux and Windows guests running on VMware, Xen,
Hyper-V and some other hypervisors, and convert them to KVM managed by
libvirt, OpenStack, oVirt, Red Hat Virtualisation (RHV) or several
other targets.  It can modify the guest to make it bootable on KVM and
install virtio drivers so it will run quickly.


%package bash-completion
Summary:       Bash tab-completion for %{name}
BuildArch:     noarch
Requires:      bash-completion >= 2.0
Requires:      %{name} = %{version}-%{release}


%description bash-completion
Install this package if you want intelligent bash tab-completion
for %{name}.


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
%autosetup -p1
%if 0%{patches_touch_autotools}
autoreconf -i
%endif


%build
%configure
make %{?_smp_mflags}


%install
%make_install

# Delete libtool crap.
find $RPM_BUILD_ROOT -name '*.la' -delete

# Virt-tools data directory.  This contains a symlink to rhsrvany.exe
# which is satisfied by the dependency on mingw32-srvany.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/virt-tools
pushd $RPM_BUILD_ROOT%{_datadir}/virt-tools
ln -sf /usr/i686-w64-mingw32/sys-root/mingw/bin/rhsrvany.exe
popd

# Delete the v2v test harness (except for the man page).
rm -r $RPM_BUILD_ROOT%{_libdir}/ocaml/v2v_test_harness
rm -r $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/dllv2v_test_harness*

# Find locale files.
%find_lang %{name}


%check
# All tests fail at the moment because of bugs in libvirt blockdev.
# # Tests fail on both armv7 and ppc64le in Fedora 31 because the kernel
# # cannot boot on qemu.
# %ifnarch %{arm} ppc64le

# # On x86_64 this single test fails with: "virt-v2v: warning: the
# # target hypervisor does not support a x86_64 KVM guest".  Missing
# # BuildRequires?
# %ifarch x86_64
# truncate -s 0 tests/test-v2v-o-libvirt.sh
# %endif

# # This test fails in mock.
# truncate -s 0 tests/test-v2v-oa-option.sh

# # Make sure we can see the debug messages (RHBZ#1230160).
# export LIBGUESTFS_DEBUG=1
# export LIBGUESTFS_TRACE=1

# make %{?_smp_mflags} check || {
#     cat tests/test-suite.log
#     exit 1
#   }

# %endif


%files -f %{name}.lang
%license COPYING
#doc README
%{_bindir}/virt-v2v
%{_bindir}/virt-v2v-copy-to-local
%{_mandir}/man1/virt-v2v.1*
%{_mandir}/man1/virt-v2v-copy-to-local.1*
%{_mandir}/man1/virt-v2v-hacking.1*
%{_mandir}/man1/virt-v2v-input-vmware.1*
%{_mandir}/man1/virt-v2v-input-xen.1*
%{_mandir}/man1/virt-v2v-output-local.1*
%{_mandir}/man1/virt-v2v-output-openstack.1*
%{_mandir}/man1/virt-v2v-output-rhv.1*
%{_mandir}/man1/virt-v2v-release-notes-1.42.1*
%{_mandir}/man1/virt-v2v-support.1*
%{_mandir}/man1/virt-v2v-test-harness.1*
%{_datadir}/virt-tools


%files bash-completion
%license COPYING
%{_datadir}/bash-completion/completions/virt-v2v
%{_datadir}/bash-completion/completions/virt-v2v-copy-to-local


%files man-pages-ja
%license COPYING
%lang(ja) %{_mandir}/ja/man1/*.1*


%files man-pages-uk
%license COPYING
%lang(uk) %{_mandir}/uk/man1/*.1*


%changelog
* Fri Jan 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.42.0-7
- Removing in-spec verification of source tarballs.
- License verified.

* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 1.42.0-6
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.42.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed May 06 2020 Richard W.M. Jones <rjones@redhat.com> - 1.42.0-4
- Re-add Epoch.  Forgotten when we split this package from libguestfs.

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.42.0-2
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Thu Apr 16 2020 Richard W.M. Jones <rjones@redhat.com> - 1.42.0-1
- New upstream stable version 1.42.0.

* Sat Apr 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-11
- Update all OCaml dependencies for RPM 4.16.

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-10
- OCaml 4.10.0 final.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.41.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-8
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-7
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-6
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-5
- OCaml 4.10.0+beta1 rebuild.
- Use nbdkit-python-plugin (now all Python 3 in Rawhide).

* Wed Nov 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-4
- Use license instead of doc for COPYING file.
- Include license in all subpackages.
- Use gpgverify macro.
- Don't own bash-completion directory because we Require the
  bash-completion package which owns it already.

* Tue Nov 26 2019 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-2
- Fix permissions on .sig file.
- Disable -oa preallocated test since it fails in reviewers mock environment.

* Fri Nov 15 2019 Richard W.M. Jones <rjones@redhat.com> - 1.41.8-1
- Initial release of separate virt-v2v program, was part of libguestfs.
