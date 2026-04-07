# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Verify tarball signature with GPGv2.
%global verify_tarball_signature 1

# So far there are no ELF binaries in this package, so the list
# of files in the debuginfo package will be empty, triggering
# an RPM failure.
%global debug_package %{nil}

Summary:       Convert a physical machine to run on KVM
Name:          virt-p2v
Epoch:         1
Version:       1.42.4
Release:       3%{?dist}
License:       GPL-2.0-or-later AND LGPL-2.0-or-later

# virt-p2v works only on x86_64 at the moment.  It requires porting
# to properly detect the hardware on other architectures, and furthermore
# virt-v2v requires porting too.
ExclusiveArch: x86_64

# Source and patches.
URL:           http://libguestfs.org/
Source0:       http://download.libguestfs.org/%{name}/%{name}-%{version}.tar.gz
%if 0%{verify_tarball_signature}
Source1:       http://download.libguestfs.org/%{name}/%{name}-%{version}.tar.gz.sig
%endif

# Keyring used to verify tarball signature.
%if 0%{verify_tarball_signature}
Source2:       libguestfs.keyring
%endif

# Basic build requirements.
BuildRequires: make
BuildRequires: gcc
BuildRequires: perl(Pod::Simple)
BuildRequires: perl(Pod::Man)
BuildRequires: perl(List::MoreUtils)
BuildRequires: /usr/bin/pod2text
BuildRequires: libxml2-devel
BuildRequires: pcre2-devel
BuildRequires: bash-completion-devel
BuildRequires: xz
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: m4
%if 0%{verify_tarball_signature}
BuildRequires: gnupg2
%endif

# Test suite requirements.
BuildRequires: nbdkit

Requires:      gawk
Requires:      gzip

# virt-p2v-make-disk runs virt-builder:
Requires:      guestfs-tools

# virt-p2v-make-kickstart runs strip:
Requires:      binutils


%description
Virt-p2v converts (virtualizes) physical machines so they can be run
as virtual machines under KVM.

This package contains the tools needed to make a virt-p2v boot CD or
USB key which is booted on the physical machine to perform the
conversion.  You also need virt-v2v installed somewhere else to
complete the conversion.

To convert virtual machines from other hypervisors, see virt-v2v.


%prep
%if 0%{verify_tarball_signature}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%autosetup -p1


%build
%configure \
  --with-extra="fedora=%{fedora},release=%{release}"

%make_build


%check
if ! make check; then
    cat test-suite.log
    exit 1
fi


%install
%make_install

# Delete the development man pages.
rm $RPM_BUILD_ROOT%{_mandir}/man1/p2v-building.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/p2v-hacking.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/p2v-release-notes.1*


%files
%doc README
%license COPYING
%{_bindir}/virt-p2v-make-disk
%{_bindir}/virt-p2v-make-kickstart
%{_bindir}/virt-p2v-make-kiwi
%{bash_completions_dir}/virt-*
%{_datadir}/virt-p2v
%{_libdir}/virt-p2v
%{_mandir}/man1/virt-p2v-make-disk.1*
%{_mandir}/man1/virt-p2v-make-kickstart.1*
%{_mandir}/man1/virt-p2v-make-kiwi.1*
%{_mandir}/man1/virt-p2v.1*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.4-1
- New upstream version 1.42.4

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 25 2024 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.3-6
- Use %%{bash_completions_dir} macro
- BR bash-completion-devel (new in Rawhide)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.3-3
- Migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 11 2022 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.3-1
- New upstream release 1.42.3

* Wed Aug 03 2022 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.2-1
- New upstream release 1.42.2
- Uses PCRE2 instead of PCRE.
- Remove Obsolete/Provides etc used for upgrades from Fedora 31.
- libguestfs-tools-c was renamed to guestfs-tools in Fedora 34.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 10 2022 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.1-1
- New upstream release 1.42.1
- gnulib removed upstream.
- Some specfile modernization.

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.0-1
- New upstream release 1.42.0.
- Use gpgverify macro instead of explicit gpgv2 command.
- Move .sig file to sources instead of dist-git.

* Tue Sep 10 2019 Pino Toscano <ptoscano@redhat.com> - 1:1.41.0-1
- Initial build, split off src:libguestfs.
