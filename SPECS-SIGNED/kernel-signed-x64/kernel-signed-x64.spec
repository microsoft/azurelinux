%global debug_package %{nil}
Summary:        Signed Linux Kernel for x86_64 systems
Name:           kernel-signed-x64
Version:        5.4.51
Release:        2%{?dist}
License:        GPLv2
URL:            https://github.com/microsoft/WSL2-Linux-Kernel
Group:          System Environment/Kernel
Vendor:         Microsoft Corporation
Distribution:   Mariner

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
Source1:        vmlinuz-%{version}-%{release}

ExclusiveArch:  x86_64

BuildRequires:  cpio

Conflicts:      kernel

%define uname_r %{version}-%{release}

%description
This package contains the Linux kernel package with kernel signed with the production key

%prep

%build
rpm2cpio %{SOURCE0} | cpio -idmv

%install
install -vdm 700 %{buildroot}/boot
install -vdm 755 %{buildroot}/lib/modules/%{uname_r}
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel

cp -rp ./boot/* %{buildroot}/boot
cp -rp ./lib/* %{buildroot}/lib
cp -rp ./var/* %{buildroot}/%{_localstatedir}
cp %{SOURCE1} %{buildroot}/boot/vmlinuz-%{version}-%{release}

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
     if [ `ls /boot/linux-*.cfg 1> /dev/null 2>&1` ]
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
/lib/modules/%{uname_r}/*
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}

%changelog
*   Tue Sep 01 2020 Chris Co <chrco@microsoft.com> 5.4.51-2
-   Update release number
*   Wed Aug 19 2020 Chris Co <chrco@microsoft.com> 5.4.51-1
-   Update source to 5.4.51
*   Wed Aug 19 2020 Chris Co <chrco@microsoft.com> 5.4.42-12
-   Update release number
*   Tue Aug 18 2020 Chris Co <chrco@microsoft.com> 5.4.42-11
-   Original version for CBL-Mariner.