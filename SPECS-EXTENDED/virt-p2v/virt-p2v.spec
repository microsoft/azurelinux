Vendor:         Microsoft Corporation
Distribution:   Mariner

# So far there are no ELF binaries in this package, so the list
# of files in the debuginfo package will be empty, triggering
# an RPM failure.
%global debug_package %{nil}

Summary:       Convert a physical machine to run on KVM
Name:          virt-p2v
Version:       1.42.0
Release:       6%{?dist}
License:       GPLv2+ and LGPLv2+

# virt-p2v works only on x86_64 at the moment.  It requires porting
# to properly detect the hardware on other architectures, and furthermore
# virt-v2v requires porting too.
ExclusiveArch: x86_64

# Source and patches.
URL:           http://libguestfs.org/
Source0:       http://download.libguestfs.org/%{name}/%{name}-%{version}.tar.gz

# Basic build requirements.
BuildRequires: gcc
BuildRequires: perl(Pod::Simple)
BuildRequires: perl(Pod::Man)
BuildRequires: perl(List::MoreUtils)
BuildRequires: /usr/bin/pod2text
BuildRequires: libxml2-devel
BuildRequires: pcre-devel
BuildRequires: bash-completion
BuildRequires: xz
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: m4

# Test suite requirements.
BuildRequires: /usr/bin/qemu-nbd

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_exceptions
Provides:      bundled(gnulib)


Requires:      gawk
Requires:      gzip

# virt-p2v-make-disk runs virt-builder:
Requires:      libguestfs-tools-c

# virt-p2v-make-kickstart runs strip:
Requires:      binutils


# Migrate from the old virt-p2v-maker:
Provides: virt-p2v-maker = %{version}-%{release}
Obsoletes: virt-p2v-maker < 1.41.5

# The bash completion for p2v were shipped with the others of libguestfs:
Obsoletes: libguestfs-bash-completion < 1.41.5


%description
Virt-p2v converts (virtualizes) physical machines so they can be run
as virtual machines under KVM.

This package contains the tools needed to make a virt-p2v boot CD or
USB key which is booted on the physical machine to perform the
conversion.  You also need virt-v2v installed somewhere else to
complete the conversion.

To convert virtual machines from other hypervisors, see virt-v2v.


%prep
%setup -q
%autopatch -p1


%build
%configure \
  --with-extra="fedora=%{fedora},release=%{release}" \
  --disable-gnulib-tests

make V=1 %{?_smp_mflags}


%check

if ! make check; then
    cat test-suite.log
    false
fi


%install
make DESTDIR=$RPM_BUILD_ROOT install

# Delete the development man pages.
rm $RPM_BUILD_ROOT%{_mandir}/man1/p2v-building.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/p2v-hacking.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/p2v-release-notes.1*

%files
%doc README
%license COPYING COPYING.LIB
%{_bindir}/virt-p2v-make-disk
%{_bindir}/virt-p2v-make-kickstart
%{_bindir}/virt-p2v-make-kiwi
%{_datadir}/bash-completion/completions/virt-*
%{_datadir}/virt-p2v
%{_libdir}/virt-p2v
%{_mandir}/man1/virt-p2v-make-disk.1*
%{_mandir}/man1/virt-p2v-make-kickstart.1*
%{_mandir}/man1/virt-p2v-make-kiwi.1*
%{_mandir}/man1/virt-p2v.1*


%changelog
* Tue Sep 26 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.42.0-6
- Removing 'exit' calls from the '%%check' section.

* Fri Jan 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.42.0-5
- Removing in-spec verification of source tarballs.
- License verified.

* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 1.42.0-4
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.42.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.0-1
- New upstream release 1.42.0.
- Use gpgverify macro instead of explicit gpgv2 command.
- Move .sig file to sources instead of dist-git.

* Tue Sep 10 2019 Pino Toscano <ptoscano@redhat.com> - 1:1.41.0-1
- Initial build, split off src:libguestfs.
