%global debug_package %{nil}
%define uname_r %{version}-%{release}
Summary:        Signed Linux Kernel for x86_64 systems
Name:           kernel-signed-x64
Version:        5.10.28.1
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        kernel-%{version}-%{release}.x86_64.rpm
Source1:        vmlinuz-%{uname_r}
BuildRequires:  cpio
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils
Conflicts:      kernel
ExclusiveArch:  x86_64

%description
This package contains the Linux kernel package with kernel signed with the production key

%prep

%build
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./boot/vmlinuz-%{uname_r}

%install
install -vdm 700 %{buildroot}/boot
install -vdm 755 %{buildroot}/lib/modules/%{uname_r}
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel

cp -rp ./boot/. %{buildroot}/boot
cp -rp ./lib/. %{buildroot}/lib
cp -rp ./var/. %{buildroot}/%{_localstatedir}

%triggerin -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/initrd.img-%{uname_r}
echo "initrd of kernel %{uname_r} removed" >&2

%postun
if [ ! -e /boot/mariner.cfg ]
then
     ls /boot/linux-*.cfg 1> /dev/null 2>&1
     if [ $? -eq 0 ]
     then
          list=`ls -tu /boot/linux-*.cfg | head -n1`
          test -n "$list" && ln -sf "$list" /boot/mariner.cfg
     fi
fi

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/mariner.cfg

%files
/boot/*
/boot/.vmlinuz-%{uname_r}.hmac
/lib/modules/%{uname_r}/*
/lib/modules/%{uname_r}/.vmlinuz.hmac
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}

%changelog
* Thu Apr 15 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.28.1-2
- Update to kernel release 5.10.28.1-2

* Thu Apr 08 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-1
- Update source to 5.10.28.1
- Update uname_r define to match the new value derived from the source

* Fri Mar 26 2021 Daniel Mihai <dmihai@microsoft.com> - 5.10.21.1-4
- Update to kernel release 5.10.21.1-4

* Thu Mar 18 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-3
- Fix file copy

* Wed Mar 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.10.21.1-2
- Update to kernel release 5.10.21.1-2

* Thu Mar 11 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-1
- Update source to 5.10.21.1

* Fri Mar 05 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-4
- Update release number to match kernel spec
- Use uname_r macro instead of version-release for kernel version

* Thu Mar 04 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.13.1-3
- Update to kernel release 5.10.13.1-3

* Mon Feb 22 2021 Thomas Crain <thcrain@microsoft.com> - 5.10.13.1-2
- Update to kernel release 5.10.13.1-2

* Thu Feb 18 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-1
- Update source to 5.10.13.1

* Tue Feb 16 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-5
- Update to kernel release 5.4.91-5.

* Tue Feb 09 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-4
- Update to kernel release 5.4.91-4.

* Thu Jan 28 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-3
- Add hmac files for FIPS

* Wed Jan 27 2021 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.91-2
- Update release number to match kernel spec

* Wed Jan 20 2021 Chris Co <chrco@microsoft.com> - 5.4.91-1
- Update source to 5.4.91

* Tue Jan 12 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.4.83-4
- Update release number to match kernel spec

* Sat Jan 09 2021 Andrew Phelps <anphel@microsoft.com> - 5.4.83-3
- Update to kernel release 5.4.83-3

* Mon Dec 28 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.83-2
- Update to kernel release 5.4.83-2

* Tue Dec 15 2020 Henry Beberman <henry.beberman@microsoft.com> - 5.4.83-1
- Update source to 5.4.83

* Fri Dec 04 2020 Chris Co <chrco@microsoft.com> - 5.4.81-1
- Update source to 5.4.81

* Wed Nov 25 2020 Chris Co <chrco@microsoft.com> - 5.4.72-5
- Update release number to match kernel spec

* Mon Nov 23 2020 Chris Co <chrco@microsoft.com> - 5.4.72-4
- Update release number to match kernel spec

* Mon Nov 16 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.72-3
- Update release number

* Tue Nov 10 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.72-2
- Update release number

* Mon Oct 26 2020 Chris Co <chrco@microsoft.com> - 5.4.72-1
- Update source to 5.4.72
- Lint spec

* Fri Oct 16 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.51-11
- Update release number

* Fri Oct 02 2020 Chris Co <chrco@microsoft.com> - 5.4.51-10
- Update release number to match kernel spec

* Fri Oct 02 2020 Chris Co <chrco@microsoft.com> - 5.4.51-9
- Update release number

* Wed Sep 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 5.4.51-8
- Update postun script to deal with removal in case of another installed kernel.

* Fri Sep 25 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.51-7
- Update release number

* Wed Sep 23 2020 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.51-6
- Update release number

* Thu Sep 03 2020 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.51-5
- Update release number

* Thu Sep 03 2020 Chris Co <chrco@microsoft.com> - 5.4.51-4
- Update release number

* Thu Sep 03 2020 Chris Co <chrco@microsoft.com> - 5.4.51-3
- Add missing requires

* Tue Sep 01 2020 Chris Co <chrco@microsoft.com> - 5.4.51-2
- Update release number

* Wed Aug 19 2020 Chris Co <chrco@microsoft.com> - 5.4.51-1
- Update source to 5.4.51

* Wed Aug 19 2020 Chris Co <chrco@microsoft.com> - 5.4.42-12
- Update release number

* Tue Aug 18 2020 Chris Co <chrco@microsoft.com> - 5.4.42-11
- Original version for CBL-Mariner.
