# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Groupings
%global build_petitboot 1

# musl is not available in EPEL.
%if 0%{?fedora}
# musl-gcc does not work on ppc64le (2022-03-22)
%ifnarch ppc64le
%global build_musl 1
%else
%global build_musl 0
%endif
%else
%global build_musl 0
%endif

# uclibc does not work. Except on EPEL9 where somehow it does.
# DISABLED AS OF 2022-03-19 - spot@fedoraproject.org
%ifnarch ppc %{power64} s390 s390x aarch64
%global build_uclibc 0
%else
%global build_uclibc 0
%endif

# We really only need this on EPEL where musl does not exist
# OR on ppc64le on Fedora.
%if 0%{?rhel}
%global build_glibc_static 1
%else
%ifarch ppc64le
%global build_glibc_static 1
%endif
%endif

# Default
# This logic changes if uclibc ever actually works again.
%if 0%{?fedora}
%ifnarch ppc64le
%global default_type musl
%else
%global default_type glibc
%endif
%else
%global default_type glibc
%endif

%global print_configs 0

# Some architectures like the hardened flags, others do not.
# If uclibc ever comes back, make variables for it.
%ifarch x86_64 aarch64
%global hcflags %{_hardening_cflags} -fstack-clash-protection
%global hldflags %{_hardening_ldflags} -Wl,-z,relro,-z,now
%endif

Name:		busybox
Version:	1.37.0
Release:	3%{?dist}
Epoch:		1
Summary:	Statically linked binary providing simplified versions of system commands
License:	GPL-2.0-only
URL:		http://www.busybox.net
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source2:	busybox-petitboot.config
Source3:	busybox-shared.config
Source4:	busybox-glibc-static.config
Source5:	busybox-uclibc-static.config
Source6:	busybox-musl-static.config
# musl kernel headers
Source10:	https://github.com/sabotage-linux/kernel-headers/archive/refs/tags/v4.19.88-1.tar.gz
Patch0:		busybox-1.31.1-stime-fix.patch
# Linux no longer supports CBQ UAPI as of
# https://github.com/torvalds/linux/commit/33241dca486264193ed68167c8eeae1fb197f3df
# I just changed networking/tc.c to print an unsupported message if you try to set options for cbq
# ... there is probably a better fix.
# Technically, the bundled headers from sabotage-linux still have the CBQ vars, but they're really old at this point.
# Felt safer to just disable CBQ, as that is what iproute did:
# https://github.com/iproute2/iproute2/commit/07ba0af3fee132eddc1c2eab643ff4910181c993
Patch1:		busybox-1.36.1-no-cbq.patch
# sha1_process_block64_shaNI is only valid on x86
# most of the calls are wrapped in an arch conditional, but they missed one.
Patch2:		busybox-1.37.0-fix-conditional-for-sha1_process_block64_shaNI.patch
BuildRequires:	gcc
BuildRequires:	libselinux-devel >= 1.27.7-2
BuildRequires:	libsepol-devel
BuildRequires:	libselinux-static
BuildRequires:	libsepol-static
BuildRequires:	glibc-static
%if 0%{?build_musl}
BuildRequires:	musl-libc-static, musl-devel, musl-gcc
%endif
%if 0%{?build_uclibc}
BuildRequires:	uClibc-static
%endif
BuildRequires:	make
# $DEITY help you if you need busybox for ia32 in 2022.
# This also seems of limited use on s390x, since it is missing the necessary kernel headers to support init
ExcludeArch:    i686 s390x

# Using header from Fedora, beacuse sabotage-linux/kernel-headers is not available for riscv64
%ifarch riscv64
BuildRequires:	kernel-headers
%endif

# libbb/hash_md5_sha.c
# https://bugzilla.redhat.com/1024549
Provides:	bundled(md5-drepper2)

%description
Busybox is a single binary which includes versions of a large number
of system commands, including a shell. This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.

%if 0%{?build_petitboot}
%package petitboot
Summary:	Version of busybox configured for use with petitboot

%description petitboot
Busybox is a single binary which includes versions of a large number
of system commands, including a shell. The version contained in this
package is a minimal configuration intended for use with the Petitboot
bootloader used on PlayStation 3. The busybox package provides a binary
better suited to normal use.
%endif

%package shared
Summary:	A shared (non-static) version of busybox

%description shared
Busybox is a single binary which includes versions of a large number
of system commands, including a shell. The version contained in this
package is build against shared libraries, most notably glibc.

%prep
%setup -q -a 10
%patch -P0 -p1 -b .stime
%patch -P1 -p1 -b .cbq
%patch -P2 -p1 -b .shani-fix

%build
# Fix architecture name maps
arch=`uname -m | sed -e 's/i.86/i386/' -e 's/armv7l/arm/' -e 's/armv5tel/arm/'`

## TODO: CC="gcc %{optflags}" ?

## STATIC BUILDS

%ifarch riscv64
mkdir linux-header-stock
rpm -ql kernel-headers | xargs -i cp -v --parents {} ./linux-header-stock || :
%endif

# 1. Musl
%if 0%{?build_musl}
# We use musl-libc. It has broader architecture support and is still small.
cp %{SOURCE6} .config
%ifarch s390x
sed -i -e "s/CONFIG_KBD_MODE=y/# CONFIG_KBD_MODE is not set/" -e "s/CONFIG_LOADFONT=y/# CONFIG_LOADFONT is not set/" -e "s/CONFIG_SETFONT=y/# CONFIG_SETFONT is not set/" -e "s/CONFIG_OPENVT=y/# CONFIG_OPENVT is not set/" -e "s/CONFIG_SHOWKEY=y/# CONFIG_SHOWKEY is not set/" .config
%endif
# set all new options to defaults
yes "" | make oldconfig && \
%if 0%{?print_configs}
cat .config && \
%endif
%ifarch riscv64
make V=1 \
CC="musl-gcc -static" \
EXTRA_CFLAGS="-g -Ilinux-header-stock/usr/include %{?hcflags}" \
CFLAGS_busybox="-L%{_prefix}/$arch-linux-musl %{?hldflags}"
%else
make V=1 \
CC="musl-gcc -static" \
EXTRA_CFLAGS="-g -Ikernel-headers-4.19.88-1/$arch/include %{?hcflags}" \
CFLAGS_busybox="-L%{_prefix}/$arch-linux-musl %{?hldflags}"
%endif
cp busybox_unstripped busybox.musl.static
cp docs/busybox.1 docs/busybox.musl.static.1
%endif

make clean

# 2. uclibc
%if 0%{?build_uclibc}
# We use uclibc. It has smaller architecture support, but is more feature rich than musl.
# uclibc can't be built on ppc64,s390,ia64
cp %{SOURCE5} .config
# set all new options to defaults
yes "" | make oldconfig && \
%if 0%{?print_configs}
cat .config && \
%endif
make V=1 \
EXTRA_CFLAGS="-fstack-protector-strong -fstack-clash-protection -g -isystem %{_includedir}/uClibc" \
CFLAGS_busybox="-Wl,-z,relro,-z,now -nostartfiles -L%{_libdir}/uClibc %{_libdir}/uClibc/crt*.o"

cp busybox_unstripped busybox.uclibc.static
cp docs/busybox.1 docs/busybox.uclibc.static.1
%endif

make clean

# 3. glibc (static)
%if 0%{?build_glibc_static}
cp %{SOURCE4} .config
# set all new options to defaults
yes "" | make oldconfig && \
%if 0%{?print_configs}
cat .config && \
%endif
make V=1 \
EXTRA_CFLAGS="%{?hcflags} -g" \
CFLAGS_busybox="%{?hldflags}"

cp busybox_unstripped busybox.glibc.static
cp docs/busybox.1 docs/busybox.glibc.static.1
%endif

#    grep -v \
#        -e ^CONFIG_FEATURE_HAVE_RPC \
#        -e ^CONFIG_FEATURE_MOUNT_NFS \
#        -e ^CONFIG_FEATURE_INETD_RPC \
#        .config1 >.config && \
#    echo "# CONFIG_FEATURE_HAVE_RPC is not set" >>.config && \
#    echo "# CONFIG_FEATURE_MOUNT_NFS is not set" >>.config && \
#    echo "# CONFIG_FEATURE_INETD_RPC is not set" >>.config && \

%if 0%{?build_petitboot}

make clean

# 4. Petitboot

# 4a. Musl
%if 0%{?build_musl}
cp %{SOURCE2} .config
%ifarch s390x
sed -i -e "s/CONFIG_KBD_MODE=y/# CONFIG_KBD_MODE is not set/" -e "s/CONFIG_LOADFONT=y/# CONFIG_LOADFONT is not set/" -e "s/CONFIG_SETFONT=y/# CONFIG_SETFONT is not set/" -e "s/CONFIG_OPENVT=y/# CONFIG_OPENVT is not set/" -e "s/CONFIG_SHOWKEY=y/# CONFIG_SHOWKEY is not set/" .config
%endif
# set all new options to defaults
yes "" | make oldconfig
%if 0%{?print_configs}
cat .config && \
%endif
sed -i -e "s/CONFIG_FEATURE_VI_REGEX_SEARCH=y/CONFIG_FEATURE_VI_REGEX_SEARCH=n/" -e "s/CONFIG_EXTRA_COMPAT=y/CONFIG_EXTRA_COMPAT=n/" -e "s/CONFIG_FEATURE_INETD_RPC=y/CONFIG_FEATURE_INETD_RPC=n/" -e "s/CONFIG_FEATURE_UTMP=y/CONFIG_FEATURE_UTMP=n/" .config && \
%ifarch riscv64
make V=1 \
CC="musl-gcc -static" \
EXTRA_CFLAGS="-g -Ilinux-header-stock/usr/include %{?hcflags}" \
CFLAGS_busybox="-L%{_prefix}/$arch-linux-musl %{?hldflags}"
%else
make V=1 \
CC="musl-gcc -static" \
EXTRA_CFLAGS="-g -Ikernel-headers-4.19.88-1/$arch/include %{?hcflags}" \
CFLAGS_busybox="-L%{_prefix}/$arch-linux-musl %{?hldflags}"
%endif

cp busybox_unstripped busybox.musl.petitboot
cp docs/busybox.1 docs/busybox.musl.petitboot.1
%endif

make clean

#4b. Uclibc
%if 0%{?build_uclibc}
cp %{SOURCE2} .config
# set all new options to defaults
yes "" | make oldconfig
%if 0%{?print_configs}
cat .config && \
%endif
sed -i -e "s/CONFIG_UNICODE_PRESERVE_BROKEN=y/CONFIG_UNICODE_PRESERVE_BROKEN=n/" .config && \
make V=1 \
EXTRA_CFLAGS="-g -isystem %{_includedir}/uClibc" \
CFLAGS_busybox="%{_hardening_ldflags} -Wl,-z,relro,-z,now -static -nostartfiles -L%{_libdir}/uClibc %{_libdir}/uClibc/crt1.o %{_libdir}/uClibc/crti.o %{_libdir}/uClibc/crtn.o"; \
LDFLAGS="--static"

cp busybox_unstripped busybox.uclibc.petitboot
cp docs/busybox.1 docs/busybox.uclibc.petitboot.1
%endif

make clean

#4c. Glibc static
%if 0%{?build_glibc_static}
cp %{SOURCE2} .config
# set all new options to defaults
yes "" | make oldconfig
%if 0%{?print_configs}
cat .config && \
%endif
make V=1 \
EXTRA_CFLAGS="-g %{?hcflags}" \
LDFLAGS="%{?hldflags}"

cp busybox_unstripped busybox.glibc.petitboot
cp docs/busybox.1 docs/busybox.glibc.petitboot.1
%endif

%endif

make clean

## Shared
# 5. Glibc

# copy new configuration file
cp %{SOURCE3} .config
# set all new options to defaults
yes "" | make oldconfig
# Use optflags
%if 0%{?print_configs}
cat .config
%endif
make V=1 EXTRA_CFLAGS="%{optflags}" CFLAGS_busybox="%{build_ldflags}"
cp busybox_unstripped busybox.shared
cp docs/busybox.1 docs/busybox.shared.1

%install
mkdir -p %{buildroot}%{_sbindir}
install -m 755 busybox.*.static %{buildroot}%{_sbindir}
mv %{buildroot}%{_sbindir}/busybox.%{default_type}.static %{buildroot}%{_sbindir}/busybox
ln -s ./busybox %{buildroot}%{_sbindir}/busybox.%{default_type}.static
%if 0%{?build_petitboot}
install -m 755 busybox.*.petitboot %{buildroot}%{_sbindir}
mv %{buildroot}%{_sbindir}/busybox.%{default_type}.petitboot %{buildroot}%{_sbindir}/busybox.petitboot
ln -s ./busybox.petitboot %{buildroot}%{_sbindir}/busybox.%{default_type}.petitboot
%endif
install -m 755 busybox.shared %{buildroot}%{_sbindir}/busybox.shared
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 docs/busybox.*.static.1 %{buildroot}%{_mandir}/man1/
mv %{buildroot}%{_mandir}/man1/busybox.%{default_type}.static.1 %{buildroot}%{_mandir}/man1/busybox.static.1
ln -s ./busybox.static.1 %{buildroot}%{_mandir}/man1/busybox.%{default_type}.static.1
%if 0%{?build_petitboot}
install -m 644 docs/busybox.*.petitboot.1 %{buildroot}%{_mandir}/man1/
mv %{buildroot}%{_mandir}/man1/busybox.%{default_type}.petitboot.1 %{buildroot}%{_mandir}/man1/busybox.petitboot.1
ln -s ./busybox.petitboot.1 %{buildroot}%{_mandir}/man1/busybox.%{default_type}.petitboot.1
%endif
install -m 644 docs/busybox.shared.1 %{buildroot}%{_mandir}/man1/busybox.shared.1

# Create symlink for udhcpc so cloud-init can use it. rhbz#2247055
ln -s ./busybox %{buildroot}%{_sbindir}/udhcpc

%files
%doc LICENSE README
%{_sbindir}/busybox
%{_sbindir}/busybox*.static
%{_sbindir}/udhcpc
%{_mandir}/man1/busybox*.static.1.gz

%if 0%{?build_petitboot}
%files petitboot
%doc LICENSE README
%{_sbindir}/busybox*.petitboot
%{_mandir}/man1/busybox*.petitboot.1.gz
%endif

%files shared
%doc LICENSE README
%{_sbindir}/busybox.shared
%{_mandir}/man1/busybox.shared.1.gz

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.37.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 27 2024 Tom Callaway <spot@fedoraproject.org> - 1:1.37.0-1
- update to 1.37.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.36.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Tom Callaway <spot@fedoraproject.org> - 1:1.36.1-7
- disable CBQ in networking/tc.c to fix build against current kernel-headers

* Wed Jan 24 2024 Major Hayden <major@redhat.com> - 1:1.36.1-6
- Add symlink for udhcpc so cloud-init can use it rhbz#2247055

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.36.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.36.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.36.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat May 27 2023 Nianqing Yao <imbearchild@outlook.com> - 1:1.36.1-2
- fix build on riscv64

* Fri May 26 2023 Tom Callaway <spot@fedoraproject.org> - 1:1.36.1-1
- update to 1.36.1

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Tom Callaway <spot@fedoraproject.org> - 1:1.36.0-1
- update to 1.36.0
- fix musl builds to be properly static (bz2079295)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.35.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 22 2022 Tom Callaway <spot@fedoraproject.org> - 1:1.35.0-4
- do not even try to do i686 builds
- more disabled features for s390x
- use glibc instead of musl for ppc64le

* Thu Mar  3 2022 Tom Callaway <spot@fedoraproject.org> - 1:1.35.0-3
- rework spec to support musl
- disable uClibc (it does not work, patches welcome)
- use glibc on epel (where musl does not exist yet)
- add shared subpackage

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.35.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 29 2021 Tom Callaway <spot@fedoraproject.org> - 1:1.35.0-1
- update to 1.35.0
- use modern macros and install into %%{_sbindir}

* Thu Sep 30 2021 Tom Callaway <spot@fedoraproject.org> - 1:1.34.1-1
- update to 1.34.1

* Thu Aug 19 2021 Tom Callaway <spot@fedoraproject.org> - 1:1.34.0-1
- update to 1.34.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May  6 2021 Tom Callaway <spot@fedoraproject.org> - 1:1.33.1-1
- update to 1.33.1

* Mon Mar 22 2021 Tom Callaway <spot@fedoraproject.org> - 1:1.33.0-3
- apply upstream fix for CVE-2021-28831

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.33.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 30 2020 Tom Callaway <spot@fedoraproject.org> - 1:1.33.0-1
- update to 1.33.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Tom Callaway <spot@fedoraproject.org> - 1:1.32.0-1
- update to 1.32.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Tom Callaway <spot@fedoraproject.org> - 1:1.31.1-1
- update to 1.31.1 (fix FTBFS)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.30.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.30.1-2
- Tweak .config files

* Mon May 13 2019 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.30.1-1
- Update to 1.30.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.28.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.28.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 05 2018 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.28.3-1
- Update to 1.28.3

* Mon Mar 26 2018 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.28.2-1
- Update to 1.28.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.26.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 30 2017 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.26.2-1
- Update to 1.26.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.22.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.22.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.22.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 1:1.22.1-3
- Provides: bundled(md5-drepper2)  (rhbz #1024549)

* Thu Mar 05 2015 Dan Horák <dan[at]danny.cz> - 1:1.22.1-2
- drop unneeded patch (#1182677)

* Tue Dec 16 2014 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.22.1-1
- Update to 1.22.1

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.19.4-13
- uClibc not supported on aarch64

* Fri May 16 2014 Jaromir Capik <jcapik@redhat.com> - 1:1.19.4-12
- Disabled uClibc on ppc64le

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Dan Horák <dan[at]danny.cz> - 1.19.4-10
- disable uClib on s390(x)

* Wed May 15 2013 Karsten Hopp <karsten@redhat.com> 1.19.4-9
- disable uClibc on ppc, too

* Wed May 15 2013 Karsten Hopp <karsten@redhat.com> 1.19.4-8
- include sys/resource.h for RLIMIT_FSIZE (rhbz #961542) on PPC*

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  1 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-5
- Added bboconfig applet - useful for running testsuite

* Fri Apr 13 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-4
- Fixed breakage with newer kernel headers
- Excluded Sun-RPC dependednt features not available in newer static glibc

* Mon Mar 12 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-3
- Tweaked spec file again to generate even more proper debuginfo package

* Wed Mar  7 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-2
- Tweaked spec file to generate proper debuginfo package

* Tue Feb 28 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-1
- update to 1.19.4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.3-1
- update to 1.19.3

* Sat Aug 27 2011 Daniel Drake <dsd@laptop.org> - 1:1.18.2-6
- Fix compilation against uClibc and Linux-3.0 headers

* Fri Aug 26 2011 Daniel Drake <dsd@laptop.org> - 1:1.18.2-5
- Remove Linux 2.4 support from insmod/modprobe/etc.
- Fixes build failures on ARM, where such ancient syscalls are not present

* Sat Jun 11 2011 Peter Robinson <pbrobinson@gmail.com> - 1:1.18.2-4
- Add support for ARM

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.18.2-2
- apply fixes from upstream

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.18.2-1
- update to 1.18.2
- use system uClibc

* Mon Oct  4 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-10
- add compatibility with man-db config file (#639461)

* Wed Sep 29 2010 jkeating - 1:1.15.1-9
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-8
- fix build system so that it works with make 3.82 too

* Wed May  5 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-7
- teach uclibc to use /etc/localtime

* Wed Feb 24 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-6
- tweak installed docs

* Wed Jan 27 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-5
- enable Fedora-specific uname -p behavior (#534081)

* Fri Nov 26 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-4
- make uclibc use 32-bit compat struct utmp (#541587)

* Fri Nov 10 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-3
- re-enable rpm applet (#534092)

* Fri Oct  2 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-2
- add manpage generation (#525658)

* Sun Sep 13 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-1
- Rebase to 1.15.1

* Fri Sep 11 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.14.1-6
- REALLY fix build on s390, ia64

* Fri Sep 11 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.14.1-5
- fix build on s390, ia64

* Wed Sep 02 2009 Chris Lumens <clumens@redhat.com> 1.14.1-4
- Remove busybox-anaconda (#514319).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Ivana Varekova <varekova@redhat.com> - 1:1.14.1-2
- add new options to readlink - patch created by Denys Valsenko

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> - 1:1.14.1-1
- fix ppc problem
- update to 1.14.1

* Sun May 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1:1.13.2-4
- Fixing FTBFS on i586/x86_64/ppc, ppc64 still an issue:
- Updated uClibc to 0.9.30.1, subsequently:
- Removed uClibc-0.9.30 patch (merged upstream).
- Added uClibc-0.9.30.1-getline.patch -- prevents conflicts with getline()
  from stdio.h
- Temporarily disable C99 math to bypass ppc bug, see https://bugs.uclibc.org/show_bug.cgi?id=55

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Ivana Varekova <varekova@redhat.com> - 1:1.13.2-2
- use uClibc instead of glibc for static build - thanks Denys Vlasenko

* Mon Jan 19 2009 Ivana Varekova <varekova@redhat.com> - 1:1.13.2-1
- update to 1.13.2

* Tue Dec  2 2008 Ivana Varekova <varekova@redhat.com> - 1:1.12.1-2
- enable selinux in static version of busybox (#462724)

* Mon Nov 10 2008 Ivana Varekova <varekova@redhat.com> - 1:1.12.1-1
- update to 1.12.1

* Tue Aug 26 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-3
- fix findfs problem - #455998

* Wed Jul 23 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-2
- add findfs to static version of busybox 
  (kexec-tools need it #455998)

* Tue Jun 10 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-1
- update to 1.10.3

* Fri May 16 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.2-1
- update to 1.10.2

* Thu May  9 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.1-1
- update to 1.10.1

* Thu Feb 14 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.1-1
- update to 1.9.1
- fix a problem with netfilter.h - thanks dwmw2

* Fri Feb  8 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.0-2
- fix hwclock on ia64 machines

* Mon Jan  7 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.0-1
- update to 1.9.0

* Mon Dec  3 2007 Ivana Varekova <varekova@redhat.com> - 1:1.8.2-1
- update to 1.8.2

* Wed Nov 21 2007 Ivana Varekova <varekova@redhat.com> - 1:1.8.1-1
- update to 1.8.1

* Tue Nov  6 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.3-1
- update to 1.7.3 
- remove --gc-sections from static build Makefile

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-4
- fix 359371 - problem with grep output

* Wed Oct 31 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-3
- fix another sed problem (forgotten fflush - #356111)

* Mon Oct 29 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-2
- fix sed problem with output (#356111)

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-1
- update to 1.7.2
 
* Tue Sep  4 2007 Ivana Varekova <varekova@redhat.com> - 1:1.6.1-2
- spec file cleanup

* Mon Jul 23 2007 Ivana Varekova <varekova@redhat.com> - 1:1.6.1-1
- update to 1.6.1

* Fri Jun  1 2007 Ivana Varekova <varekova@redhat.com> - 1:1.5.1-2
- add msh shell

* Thu May 24 2007 Ivana Varekova <varekova@redhat.com> - 1:1.5.1-1
- update to 1.5.1

* Sat Apr  7 2007 David Woodhouse <dwmw2@redhat.com> - 1:1.2.2-8
- Add busybox-petitboot subpackage

* Mon Apr  2 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-7
- Resolves: 234769 
  busybox ls does not work without a tty

* Mon Feb 19 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-6
- incorporate package review feedback

* Fri Feb  2 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-5
- fix id_ps patch (thanks Chris MacGregor)

* Tue Jan 30 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-4
- remove debuginfo

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-3
- Resolves: 223620
  id output shows context twice
- fix iptunnel x kernel-headers problem

* Mon Dec 10 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-2
- enable ash 

* Thu Nov 16 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-1
- update to 1.2.2

* Mon Aug 28 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-3
- fix #200470 - dmesg aborts
  backport dmesg upstream changes

* Mon Aug 28 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-2
- fix #202891 - tar problem

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.0-1.1
- rebuild

* Tue Jul  4 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-1
- update to 1.2.0

* Thu Jun  8 2006 Jeremy Katz <katzj@redhat.com> - 1:1.1.3-2
- fix so that busybox.anaconda has sh

* Wed May 31 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.3-1
- update to 1.1.3

* Mon May 29 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.2-3
- fix Makefile typo (#193354)

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.2-1
- update to 1.1.2

* Thu May  4 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.1-2
- add -Z option to id command, rename ps command -Z option (#190534)

* Wed May 03 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.1-1
- update to 1.1.1
- fix CVE-2006-1058 - BusyBox passwd command 
  fails to generate password with salt (#187386)
- add -minimal-toc option
- add RPM_OPT_FLAGS
- remove asm/page.h used sysconf command to get PAGE_SIZE
- add overfl patch to aviod Buffer warning

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.01-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.01-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Oct 13 2005 Daniel Walsh <dwalsh@redhat.com> -  1.01-2
- Add sepol for linking load_policy

* Thu Sep  1 2005 Ivana Varekova <varekova@redhat.com> - 1.01-1
- update to 1.01
 
* Tue May 11 2005 Ivana Varekova <varekova@redhat.com> - 1.00-5
- add debug files to debug_package

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> - 1.00-4
- rebuilt

* Wed Jan 26 2005 Ivana Varekova <varekova@redhat.com> - 1.00-3
- update to 1.00 - fix bug #145681
- rebuild

* Thu Jan 13 2005 Jeremy Katz <katzj@redhat.com> - 1.00.rc1-6
- enable ash as the shell in busybox-anaconda

* Sat Oct  2 2004 Bill Nottingham <notting@redhat.com> - 1.00.rc1-5
- fix segfault in SELinux patch (#134404, #134406)

* Fri Sep 17 2004 Phil Knirsch <pknirsch@redhat.com> - 1.00.rc1-4
- Fixed double free in freecon() call (#132809)

* Fri Sep 10 2004 Daniel Walsh <dwalsh@redhat.com> - 1.00.rc1-3
- Add CONFIG_STATIC=y for static builds

* Wed Aug 25 2004 Jeremy Katz <katzj@redhat.com> - 1.00.rc1-2
- rebuild

* Fri Jun 25 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre10.1
- Add BuildRequires libselinux-devel
- Update to latest from upstream

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-4 
- add mknod to busybox-anaconda

* Wed Apr 21 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-3 
- fix LS_COLOR in anaconda patch

* Tue Mar 23 2004 Jeremy Katz <katzj@redhat.com> 1.00.pre8-2
- add awk to busybox-anaconda

* Sat Mar 20 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre8.1
- Update with latest patch. 
- Turn off LS_COLOR in static patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.2
- Fix is_selinux_enabled calls

* Mon Dec 29 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.1
-Latest update

* Wed Nov 26 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.2
- Add insmod

* Mon Sep 15 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.1
- Upgrade to pre3

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 1.00.2
- Upgrade selinux support

* Wed Jul 23 2003 Dan Walsh <dwalsh@redhat.com> 1.00.1
- Upgrade to 1.00 package

* Wed Jul 16 2003 Elliot Lee <sopwith@redhat.com> 0.60.5-10
- Rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-9
- rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-8
- add dmesg to busybox-anaconda

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-5
- lost nolock for anaconda mount when rediffing, it returns (#81764)

* Mon Jan 6 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-4
- Upstream developers wanted to eliminate the use of floats

* Thu Jan 3 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-3
- Fix free to work on large memory machines.

* Sat Dec 28 2002 Jeremy Katz <katzj@redhat.com> 0.60.5-2
- update Config.h for anaconda build to include more useful utils

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.5-1
- update latest release

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.2-8
- incorporate hammer changes

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 06 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix compilation on mainframe

* Tue Apr  2 2002 Jeremy Katz <katzj@redhat.com>
- fix static busybox (#60701)

* Thu Feb 28 2002 Jeremy Katz <katzj@redhat.com>
- don't include mknod in busybox.anaconda so we get collage mknod

* Fri Feb 22 2002 Jeremy Katz <katzj@redhat.com>
- rebuild in new environment

* Wed Jan 30 2002 Jeremy Katz <katzj@redhat.com>
- update to 0.60.2
- include more pieces for the anaconda version so that collage can go away
- make the mount in busybox.anaconda default to -onolock

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
`- automated rebuild

* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- don't obsolete sash
- fix URL and spelling in desc. to satisfy rpmlint

* Thu Jul 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add missing defattr for anaconda subpackage

* Thu Jun 28 2001 Erik Troan <ewt@redhat.com>
- initial build for Red Hat
