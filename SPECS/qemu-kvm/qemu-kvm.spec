Summary:        QEMU is a machine emulator and virtualizer
Name:           qemu-kvm
Version:        4.2.0
Release:        44%{?dist}
License:        GPLv2 AND GPLv2+ AND CC-BY AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.qemu.org/
Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
Source1:        65-kvm.rules
# https://git.qemu.org/?p=qemu.git;a=commit;h=8ffb7265af64ec81748335ec8f20e7ab542c3850
Patch0:         CVE-2020-11102.patch
# This vulnerability is in libslirp source code. And qemu is exposed to it when configured with libslirp.
# Since Mariner does not have libslirp, it is not applicable.
Patch1:         CVE-2020-1711.patch
Patch2:         CVE-2020-7211.patch
Patch3:         CVE-2019-20175.patch
Patch4:         CVE-2020-13659.patch
Patch5:         CVE-2020-16092.patch
Patch6:         CVE-2020-15863.patch
Patch7:         CVE-2020-10702.patch
Patch8:         CVE-2020-10761.patch
# CVE-2020-13253 backported to 4.2.0. Original version: https://github.com/qemu/qemu/commit/790762e5487114341cccc5bffcec4cb3c022c3cd
Patch9:         CVE-2020-13253.patch
Patch10:        CVE-2020-13754.patch
Patch11:        CVE-2020-13800.patch
Patch12:        CVE-2020-14364.patch
Patch13:        CVE-2020-13791.patch
# CVE-2018-19665 patch never merged upstream, link: https://lists.gnu.org/archive/html/qemu-devel/2018-11/msg03570.html
Patch14:        CVE-2018-19665.patch
Patch15:        CVE-2020-13361.patch
Patch16:        CVE-2020-11869.patch
Patch17:        CVE-2020-14415.patch
Patch18:        CVE-2020-15859.patch
Patch19:        CVE-2020-13362.patch
Patch20:        CVE-2020-25742.patch
Patch21:        CVE-2020-25743.patch
Patch22:        CVE-2020-15469.patch
Patch23:        CVE-2020-24352.patch
Patch24:        CVE-2018-12617.patch
Patch25:        CVE-2020-25723.patch
Patch26:        CVE-2020-27821.patch
Patch27:        CVE-2020-17380.patch
Patch28:        CVE-2021-20203.patch
Patch29:        CVE-2021-20255.patch
Patch30:        CVE-2021-3416.patch
Patch31:        CVE-2021-3392.patch
Patch32:        CVE-2021-3409.patch
Patch33:        CVE-2021-20181.patch
Patch34:        CVE-2021-20221.patch
Patch35:        CVE-2021-3527.patch
Patch36:        CVE-2021-3546.patch
Patch37:        CVE-2021-3682.patch
Patch38:        CVE-2021-3713.patch
Patch39:        CVE-2021-3545.patch
Patch40:        CVE-2021-3930.patch
Patch41:        CVE-2021-3607.patch
Patch42:        CVE-2021-3608.patch
Patch43:        CVE-2021-20257.patch
Patch44:        CVE-2021-3748.patch
Patch45:        CVE-2021-3638.patch
Patch46:        CVE-2021-3750.patch
Patch47:        CVE-2021-4206.patch
Patch48:        0001-removed-tulip.c-from-build-process-due-to-CVE-2022-2962.patch
# Range 1001+ reserved for nopatch files
Patch1001:      CVE-2020-7039.nopatch
# CVE-2020-12829 affects the sm501 video driver, which is only used for powerpc and SuperH emulation
# CONFIG_SM501 is selected by CONFIG_SAM460EX and CONFIG_R2D (from ppc-softmmu and sh4 targets respectively). We are not affected because we only build natively.
# This is resolved in qemu >= 5.0
Patch1002:      CVE-2020-12829.nopatch
Patch1003:      CVE-2020-27661.nopatch
# CVE 2020-35506 affects the SCSI ESP driver (esp.c), which is only compiled when CONFIG_ESP is set.
# Our configuration does not enable CONFIG_ESP/compile esp.c, so Mariner is not vulnerable.
Patch1004:      CVE-2020-35506.nopatch
# CVE-2021-4145 is a NULL-pointer dereference of the `self` pointer in `mirror_wait_on_conflicts()`.
# This function in v4.2.0 only checks the `self` pointer with another op, which will not cause a NULL-pointer dereference.
# The Code path for CVE-2021-4145 does not occur in the current version (v4.2.0) shipped with `Mariner-1.0`.
Patch1005:      CVE-2021-4145.nopatch
# CVE-2021-3947 is a stack-buffer-overflow in the NVME component. The current version (v4.2.0) does not ship it.
Patch1006:      CVE-2021-3947.nopatch
# CVE-2022-1050 only affects installations of QEMU with RDMA support. We don't have that enabled.
Patch1007:      CVE-2022-1050.nopatch
# CVE-2021-20295 only affects RedHat's particular release of QEMU
Patch1008:      CVE-2021-20295.nopatch
Patch1009:      CVE-2022-35414.patch
# CVE-2022-0358 is in the tools component.
# Version (v4.2.0) does not ship tools component code.
# CVE and provided patch not applicable hence adding nopatch.
Patch1010:      CVE-2022-0358.nopatch

BuildRequires:  alsa-lib-devel
BuildRequires:  glib-devel
BuildRequires:  pixman-devel
BuildRequires:  python3-devel
BuildRequires:  zlib-devel
Requires:       alsa-lib
Requires:       cyrus-sasl
Requires:       pixman

%description
QEMU is a generic and open source machine & userspace emulator and virtualizer.

%global debug_package %{nil}

%package -n qemu-img
Summary:        QEMU command line tool for manipulating disk images
Group:          Development/Tools
Requires:       glib
Requires:       libstdc++
Requires:       pixman

%description -n qemu-img
This package provides a command line tool for manipulating disk images.

%prep
%autosetup -n qemu-%{version} -p1

# Remove invalid flag exposed by binutils 2.36.1
sed -i "/LDFLAGS_NOPIE/d" configure

%build

%ifarch aarch64
   QEMU_ARCH=aarch64-softmmu
%else
   QEMU_ARCH=x86_64-softmmu
%endif

./configure \
 --prefix="%{_prefix}" \
 --libdir="%{_libdir}" \
 --audio-drv-list=alsa \
%ifarch aarch64
 --extra-cflags="%{optflags} -fPIC" \
%endif
 --target-list=$QEMU_ARCH &&
unset QEMU_ARCH &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/udev
install -d %{buildroot}%{_libdir}/udev/rules.d
install -D -m0644 %{SOURCE1} %{buildroot}%{_libdir}/udev/rules.d

chgrp kvm  %{buildroot}%{_libexecdir}/qemu-bridge-helper &&
chmod 4750 %{buildroot}%{_libexecdir}/qemu-bridge-helper

ln -sv qemu-system-`uname -m` %{buildroot}%{_bindir}/qemu
chmod 755 %{buildroot}%{_bindir}/qemu

%check
testsPassed=true
make check-unit
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-qtest
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-speed
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-qapi-schema
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-block
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-tcg
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-softfloat
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-acceptance
if [ $? -ne 0 ]; then
    testsPassed=false
fi
if [ "$testsPassed" = false ] ; then
    echo 'One (or more) tests failed. Check log for further details'
    (exit 1)
fi

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/qemu-system-*
%{_bindir}/elf2dmp
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server
%{_bindir}/qemu-edid
%{_bindir}/qemu-ga
%{_bindir}/qemu-pr-helper
%{_bindir}/qemu
%{_bindir}/virtfs-proxy-helper
%{_libdir}/*
%{_libexecdir}/*
%{_datadir}/*

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd

%changelog
* Thu Sep 29 2022 Aadhar Agarwal <aadagarwal@microsoft.com> - 4.2.0-44
- Disable tulip device emulation from QEMU to address CVE-2022-2962
- Nopatch CVE-2022-2962

* Tue Sep 06 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.2.0-43
- Nopatch CVE-2022-0358.

* Wed Aug 24 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 4.2.0-42
- Patch CVE-2022-35414

* Wed Jul 06 2022 Nick Samson <nisamson@microsoft.com> - 4.2.0-41
- Patch CVE-2021-4206

* Mon Jun 27 2022 Minghe Ren <mingheren@microsoft.com> - 4.2.0-40
- Patch CVE-2021-3750 

* Fri May 06 2022 Nick Samson <nisamson@microsoft.com> - 4.2.0-39
- Patch CVE-2021-20257, CVE-2021-3638, CVE-2021-3748
- Nopatch CVE-2022-1050, CVE-2021-20295

* Wed Mar 16 2022 Muhammad Falak <mwani@microsoft.com> - 4.2.0-38
- Patch CVE-2021-3607 & CVE-2021-3930
- Backport patch to address CVE-2021-3608
- Mark CVE-2021-3947 & CVE-2021-4145 as nopatch

* Thu Nov 18 2021 Cameron Baird <cameronbaird@microsoft.com> - 4.2.0-37
- Patched CVE-2021-3545
- Marked CVE-2020-35506 as nopatch

* Thu Sep 09 2021 Mateusz Malisz <mamalisz@microsoft.com> - 4.2.0-36
- Patched CVE-2021-3713
- Move nopatch files to 1001+ range.
- Reenable autosetup
- Move contents of CVE-2020-12829 to this spec and clear the nopatch file.

* Mon Aug 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.0-35
- Patched CVE-2021-3682.

* Tue Jul 06 2021 Henry Li <lihl@microsoft.com> - 4.2.0-34
- Patch CVE-2021-3546

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.2.0-33
- Mark CVE-2020-27661 as nopatch

* Thu Jun 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-32
- Patch CVE-2021-20221
- Patch CVE-2021-3527

* Mon Jun 07 2021 Henry Beberman <henry.beberman@microsoft.com> - 4.2.0-31
- Patch CVE-2021-20181

* Tue May 11 2021 Andrew Phelps <anphel@microsoft.com> - 4.2.0-30
- Remove LDFLAGS_NOPIE to compile with binutils 2.36.1

* Wed Apr 07 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-29
- Patch CVE-2021-3392 and CVE-2021-3409.

* Tue Mar 30 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-28
- Patch CVE-2021-3416. Added test modules under check section.

* Tue Mar 23 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-27
- Patch CVE-2021-20255

* Fri Mar 19 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-26
- Patch CVE-2021-20203

* Mon Feb 08 2021 Rachel Menge <rachelmenge@microsoft.com> - 4.2.0-25
- Update CVE-2020-17380

* Wed Jan 13 2021 Henry Li <niontive@microsoft.com> - 4.2.0-24
- Update CVE-2020-15469

* Fri Dec 11 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-23
- Patch CVE-2020-27821

* Tue Dec 08 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-22
- Patch CVE-2020-25723

* Tue Nov 17 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-21
- Backport fix for CVE-2018-12617 from 5.0.0

* Mon Nov 16 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-20
- Noatch CVE-2020-12829, only affects SuperH and PowerPC emulation

* Wed Nov 11 2020 Henry Li <lihl@microsoft.com> - 4.2.0-19
- Patch CVE-2020-13361
- Patch CVE-2020-11869
- Patch CVE-2020-14415
- Patch CVE-2020-15859
- Patch CVE-2020-13362
- Patch CVE-2020-25742
- Patch CVE-2020-25743
- Patch CVE-2020-15469
- Patch CVE-2020-24352

* Fri Oct 30 2020 Thomas Crain <thcrain@microsoft.com> - 4.2.0-18
- Patch CVE-2018-19665
- Remove nopatch files for CVE-2016-7161, CVE-2015-7504, CVE-2017-5931,
  CVE-2017-14167, as NIST data for those has been corrected

* Thu Oct 29 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.2.0-17
- Patch CVE-2020-13791.

* Thu Oct 29 2020 Joe Schmitt <joschmit@microsoft.com> - 4.2.0-16
- Patch CVE-2020-13800.
- Patch CVE-2020-14364.

* Wed Oct 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.0-15
- Add patch for CVE-2020-13253.
- Add patch for CVE-2020-13754.
- Adding back regular %%setup as %%autosetup fails on the *.nopatch files.

* Tue Oct 27 2020 Henry Li <lihl@microsoft.com> - 4.2.0-14
- Add patch for CVE-2020-10702
- Add patch for CVE-2020-10761
- Use autosetup

* Tue Sep 29 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-13
- Nopatch CVE-2015-7504, it was fixed in 2.5.0
- Nopatch CVE-2017-5931, it was fixed in 2.9.0
- Nopatch CVE-2017-14167, it was fixed in 2.11.0

* Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-12
- Nopatch CVE-2016-7161, it was fixed in 2.7

* Mon Sep 14 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 4.2.0-11
- Add patch for CVE-2020-15863

* Wed Sep 02 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-10
- Add patch for CVE-2020-16092

* Tue Jun 09 2020 Paul Monson <paulmon@microsoft.com> - 4.2.0-9
- Add patch for CVE-2019-20175
- Add patch for CVE-2020-13659

* Thu May 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.2.0-8
- Fix CVE-2020-1711 and CVE-2020-7211.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.2.0-7
- Added %%license line automatically

* Fri May  1 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.2.0-6
- Renaming qemu to qemu-kvm

* Tue Apr 21 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.2.0-5
- Fix CVE-2020-11102.
- Ignore CVE-2020-7039.
- Update license and URL.
- License verified.

* Mon Mar 30 2020 Chris Co <chrco@microsoft.com> - 4.2.0-4
- Fix changelog to not define a sha1 macro

* Fri Mar 27 2020 Chris Co <chrco@microsoft.com> - 4.2.0-3
- Add elf2dmp and virtfs-proxy-helper binaries to package
- Delete unused sha1

* Tue Mar 24 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.2.0-2
- Add Qemu KVM support

* Wed Jan 8 2020 Paul Monson <paulmon@microsoft.com> - 4.2.0-1
- Original version for CBL-Mariner.
