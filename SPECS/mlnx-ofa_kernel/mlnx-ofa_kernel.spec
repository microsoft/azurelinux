#
# Copyright (c) 2012 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Licensee has the right to choose one of the above licenses.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
#
#
Summary:        Infiniband HCA Driver
Name:           mlnx-ofa_kernel
Version:        23.04
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.mellanox.com/
Source:         https://www.mellanox.com/downloads/ofed/%{name}-%{version}-0.5.3.tgz
%global MLNX_OFED_VERSION 23.04
%global MLNX_OFED_RELEASE 0.5.3
%global WITH_SYSTEMD %(if ( test -d "%{_unitdir}" > /dev/null); then echo -n '1'; else echo -n '0'; fi)
%{!?configure_options: %global configure_options --with-core-mod --with-user_mad-mod --with-user_access-mod --with-addr_trans-mod --with-mlx5-mod --with-mlxfw-mod --with-ipoib-mod}
%global MEMTRACK %(if ( echo %{configure_options} | grep "with-memtrack" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%global MADEYE %(if ( echo %{configure_options} | grep "with-madeye-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%global WINDRIVER %(if (grep -qiE "Wind River" %{_sysconfdir}/issue %{_sysconfdir}/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)
%global POWERKVM %(if (grep -qiE "powerkvm" %{_sysconfdir}/issue %{_sysconfdir}/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)
%global BLUENIX %(if (grep -qiE "Bluenix" %{_sysconfdir}/issue %{_sysconfdir}/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)
%global XENSERVER65 %(if (grep -qiE "XenServer.*6\.5" %{_sysconfdir}/issue %{_sysconfdir}/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)
# MarinerOS 1.0 sets -fPIE in the hardening cflags
# (in the gcc specs file).
# This seems to break only this package and not other kernel packages.
%if "%{_vendor}" == "mariner"
%global _hardened_cflags %{nil}
%endif
%global KVERSION %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-devel))
%global K_SRC %{_libdir}/modules/%{KVERSION}/build
%global moddestdir %{buildroot}%{_libdir}/modules/%{KVERSION}/kernel/
# Select packages to build
# Kernel module packages to be included into kernel-ib
%global build_ipoib %(if ( echo %{configure_options} | grep "with-ipoib-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%global build_oiscsi %(if ( echo %{configure_options} | grep "with-iscsi-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%global build_mlx5 %(if ( echo %{configure_options} | grep "with-mlx5-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%{!?LIB_MOD_DIR: %global LIB_MOD_DIR /lib/modules/%{KVERSION}/updates}
%{!?IB_CONF_DIR: %global IB_CONF_DIR %{_sysconfdir}/infiniband}
%{!?KERNEL_SOURCES: %global KERNEL_SOURCES %{K_SRC}}
%global utils_pname %{name}
%global devel_pname %{name}-devel
%global non_kmp_pname %{name}-modules
BuildRequires:  kernel-devel
BuildRequires:  kmod
Requires:       coreutils
Requires:       grep
Requires:       kernel
Requires:       lsof
Requires:       mlnx-tools >= 5.2.0
Requires:       module-init-tools
Requires:       pciutils
Requires:       procps

%description

InfiniBand "verbs", Access Layer  and ULPs.
Utilities rpm with OFED release %{MLNX_OFED_VERSION}.

%global kernel_source() %{K_SRC}
%global kernel_release() %{KVERSION}
%global flavors_to_build default

%package -n %{non_kmp_pname}
Summary:        Infiniband Driver and ULPs kernel modules
Version:        %{MLNX_OFED_VERSION}
Group:          System Environment/Libraries

%description -n %{non_kmp_pname}
Core, HW and ULPs kernel modules
Non-KMP format kernel modules rpm.

%package -n %{devel_pname}
Summary:        Infiniband Driver and ULPs kernel modules sources
Version:        %{MLNX_OFED_VERSION}
Group:          System Environment/Libraries
Requires:       coreutils
Requires:       pciutils
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description -n %{devel_pname}
Core, HW and ULPs kernel modules sources

%package source
Summary:        Source of the MLNX_OFED main kernel driver
Group:          System Environment/Libraries

%description source
Source of the mlnx-ofa_kernel modules.

You should probably only install this package if you want to view the
sourecs of driver. Use the -devel package if you want to build other
drivers against it.

%global install_mod_dir extra/%{name}

%prep
%autosetup -p1 -n %{name}-%{MLNX_OFED_VERSION}
set -- *
mkdir source
mv "$@" source/
mkdir obj
cp source/COPYING .

%build
export EXTRA_CFLAGS='-DVERSION=\"%{version}\"'
export INSTALL_MOD_DIR=%{install_mod_dir}
export CONF_OPTIONS="%{configure_options}"
for flavor in %{flavors_to_build}; do
    export KSRC=%{kernel_source $flavor}
    export KVERSION=%{kernel_release $KSRC}
    export LIB_MOD_DIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR
    rm -rf obj/$flavor
    cp -a source obj/$flavor
    cd $PWD/obj/$flavor
    find compat -type f -exec touch -t 200012201010 '{}' \; || true
    ./configure --build-dummy-mods --prefix=%{_prefix} --kernel-version $KVERSION --kernel-sources $KSRC --modules-dir $LIB_MOD_DIR $CONF_OPTIONS %{?_smp_mflags}
    make %{?_smp_mflags} kernel
    make build_py_scripts
    cd -
done

%install
export RECORD_PY_FILES=1
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=%{install_mod_dir}
export NAME=%{name}
export VERSION=%{version}
export PREFIX=%{_prefix}
for flavor in %{flavors_to_build}; do
    export KSRC=%{kernel_source $flavor}
    export KVERSION=%{kernel_release $KSRC}
    cd $PWD/obj/$flavor
    make install_modules KERNELRELEASE=$KVERSION
    # install script and configuration files
    make install_scripts
    mkdir -p %{_builddir}/src/$NAME/$flavor
    cp -ar include/ %{_builddir}/src/$NAME/$flavor
    cp -ar config* %{_builddir}/src/$NAME/$flavor
    cp -ar compat*  %{_builddir}/src/$NAME/$flavor
    cp -ar ofed_scripts %{_builddir}/src/$NAME/$flavor

    modsyms=`find . -name Module.symvers -o -name Modules.symvers`
    if [ -n "$modsyms" ]; then
        for modsym in $modsyms
        do
            cat $modsym >> %{_builddir}/src/$NAME/$flavor/Module.symvers
        done
    else
        ./ofed_scripts/create_Module.symvers.sh
        cp ./Module.symvers %{_builddir}/src/$NAME/$flavor/Module.symvers
    fi
    # Cleanup unnecessary kernel-generated module dependency files.
    find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;
    cd -
done

# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} \( -type f -name '*.ko' -o -name '*ko.gz' \) -exec chmod u+x \{\} \;

# copy sources
mkdir -p %{buildroot}/%{_prefix}/src/ofa_kernel-%{version}
mkdir -p %{buildroot}/%{_prefix}/src/ofa_kernel/%{_arch}
cp -a %{_builddir}/%{name}-%{version}/source %{buildroot}/%{_prefix}/src/ofa_kernel-%{version}/source
ln -s ofa_kernel-%{version}/source %{buildroot}/%{_prefix}/src/mlnx-ofa_kernel-%{version}
cp -a %{_builddir}/src/%{name}/* %{buildroot}/%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION}
# Fix path of BACKPORT_INCLUDES
sed -i -e "s@=-I.*backport_includes@=-I/usr/src/ofa_kernel-$VERSION/backport_includes@" %{buildroot}/%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION}/configure.mk.kernel || true
rm -rf %{_builddir}/src

INFO=%{buildroot}%{_sysconfdir}/infiniband/info
/bin/rm -f ${INFO}
mkdir -p %{buildroot}%{_sysconfdir}/infiniband
touch ${INFO}

cat >> ${INFO} << EOFINFO
#!/bin/bash

echo prefix=%{_prefix}
echo Kernel=%{KVERSION}
echo
echo "Configure options: %{configure_options}"
echo
EOFINFO

chmod +x ${INFO} > /dev/null 2>&1

%if "%{WITH_SYSTEMD}" == "1"
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/systemd/system
install -m 0644 %{_builddir}/$NAME-$VERSION/source/ofed_scripts/openibd.service %{buildroot}%{_unitdir}
install -m 0644 %{_builddir}/$NAME-$VERSION/source/ofed_scripts/mlnx_interface_mgr\@.service %{buildroot}%{_sysconfdir}/systemd/system
%endif

install -d %{buildroot}/bin
install -m 0755 %{_builddir}/$NAME-$VERSION/source/ofed_scripts/mlnx_conf_mgr.sh %{buildroot}/bin/
%if "%{WINDRIVER}" == "0" && "%{BLUENIX}" == "0"
install -m 0755 %{_builddir}/$NAME-$VERSION/source/ofed_scripts/mlnx_interface_mgr.sh %{buildroot}/bin/
%else
# Wind River and Mellanox Bluenix are rpm based, however, interfaces management is done in Debian style
install -d %{buildroot}%{_sbindir}
install -m 0755 %{_builddir}/$NAME-$VERSION/source/ofed_scripts/mlnx_interface_mgr_deb.sh %{buildroot}/bin/mlnx_interface_mgr.sh
install -m 0755 %{_builddir}/$NAME-$VERSION/source/ofed_scripts/net-interfaces %{buildroot}%{_sbindir}
%endif

# Install ibroute utilities
# TBD: move these utilities into standalone package
install -d %{buildroot}%{_sbindir}

%if %{build_ipoib}
case $(uname -m) in
    i[3-6]86)
    # Decrease send/receive queue sizes on 32-bit arcitecture
    echo "options ib_ipoib send_queue_size=64 recv_queue_size=128" >> %{buildroot}%{_sysconfdir}/modprobe.d/ib_ipoib.conf
    ;;
esac
%endif

%post -n %{non_kmp_pname}
/sbin/depmod %{KVERSION}
# W/A for OEL6.7/7.x inbox modules get locked in memory
# in dmesg we get: Module mlx4_core locked in memory until next boot
if (grep -qiE "Oracle.*(6.([7-9]|10)| 7)" %{_sysconfdir}/issue %{_sysconfdir}/*release* 2>/dev/null); then
    /sbin/dracut --force
fi

%postun -n %{non_kmp_pname}
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
    /sbin/depmod %{KVERSION}
    # W/A for OEL6.7/7.x inbox modules get locked in memory
    # in dmesg we get: Module mlx4_core locked in memory until next boot
    if (grep -qiE "Oracle.*(6.([7-9]|10)| 7)" %{_sysconfdir}/issue %{_sysconfdir}/*release* 2>/dev/null); then
        /sbin/dracut --force
    fi
fi

%post -n %{utils_pname}
if [ $1 -eq 1 ]; then # 1 : This package is being installed
#############################################################################################################

%if "%{WINDRIVER}" == "1" || "%{BLUENIX}" == "1"
%{_sbindir}/update-rc.d openibd defaults || true
%endif

%if "%{POWERKVM}" == "1"
%{_bindir}/systemctl disable openibd >/dev/null  2>&1 || true
%{_bindir}/systemctl enable openibd >/dev/null  2>&1 || true
%endif

%if "%{WITH_SYSTEMD}" == "1"
%{_bindir}/systemctl daemon-reload >/dev/null 2>&1 || :
cat /proc/sys/kernel/random/boot_id 2>/dev/null | sed -e 's/-//g' > %{_var}/run/openibd.bootid || true
test -s %{_var}/run/openibd.bootid || echo manual > %{_var}/run/openibd.bootid || true
%endif

# Comment core modules loading hack
if [ -e %{_sysconfdir}/modprobe.conf.dist ]; then
    sed -i -r -e 's/^(\s*install ib_core.*)/#MLX# \1/' %{_sysconfdir}/modprobe.conf.dist
    sed -i -r -e 's/^(\s*alias ib.*)/#MLX# \1/' %{_sysconfdir}/modprobe.conf.dist
fi

%if %{build_ipoib}
if [ -e %{_sysconfdir}/modprobe.d/ipv6 ]; then
    sed -i -r -e 's/^(\s*install ipv6.*)/#MLX# \1/' %{_sysconfdir}/modprobe.d/ipv6
fi
%endif

 # Update limits.conf (but not for Containers)
if [ ! -e "/.dockerenv" ] && ! (grep -q docker /proc/self/cgroup 2>/dev/null); then
    if [ -e %{_sysconfdir}/security/limits.conf ]; then
            LIMITS_UPDATED=0
        if ! (grep -qE "soft.*memlock" %{_sysconfdir}/security/limits.conf 2>/dev/null); then
            echo "* soft memlock unlimited" >> %{_sysconfdir}/security/limits.conf
                LIMITS_UPDATED=1
            fi
        if ! (grep -qE "hard.*memlock" %{_sysconfdir}/security/limits.conf 2>/dev/null); then
            echo "* hard memlock unlimited" >> %{_sysconfdir}/security/limits.conf
                LIMITS_UPDATED=1
            fi
            if [ $LIMITS_UPDATED -eq 1 ]; then
            echo "Configured %{_sysconfdir}/security/limits.conf"
            fi
        fi
    fi
fi

# Make IPoIB interfaces be unmanaged on XenServer
if (grep -qi xenserver %{_sysconfdir}/issue %{_sysconfdir}/*-release 2>/dev/null); then
    IPOIB_PNUM=$(lspci -d 15b3: 2>/dev/null | wc -l 2>/dev/null)
    IPOIB_PNUM=$(($IPOIB_PNUM * 2))
    for i in $(seq 1 $IPOIB_PNUM)
    do
        uuid=$(xe pif-list 2>/dev/null | grep -B2 ib${i} | grep uuid | cut -d : -f 2 | sed -e 's/ //g')
        if [ "X${uuid}" != "X" ]; then
            xe pif-forget uuid=${uuid} >/dev/null 2>&1 || true
        fi
    done
fi

fi # 1 : closed
# END of post

%preun -n %{utils_pname}
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
%if "%{WINDRIVER}" == "1" || "%{BLUENIX}" == "1"
%{_sbindir}/update-rc.d -f openibd remove || true
%endif

%if "%{POWERKVM}" == "1"
%{_bindir}/systemctl disable openibd >/dev/null  2>&1 || true
%endif
fi

%postun -n %{utils_pname}
%if "%{WITH_SYSTEMD}" == "1"
%{_bindir}/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

# Uncomment core modules loading hack
if [ -e %{_sysconfdir}/modprobe.conf.dist ]; then
    sed -i -r -e 's/^#MLX# (.*)/\1/' %{_sysconfdir}/modprobe.conf.dist
fi

%if %{build_ipoib}
if [ -e %{_sysconfdir}/modprobe.d/ipv6 ]; then
    sed -i -r -e 's/^#MLX# (.*)/\1/' %{_sysconfdir}/modprobe.d/ipv6
fi
%endif

#end of post uninstall

%post -n %{devel_pname}
if [ -d "%{_prefix}/src/ofa_kernel/default" -a $1 -gt 1 ]; then
    touch %{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION}.missing_link
    # Will run update-alternatives in posttrans
else
    update-alternatives --install \
        %{_prefix}/src/ofa_kernel/default \
        ofa_kernel_headers \
        %{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION} \
        20
fi

%posttrans -n %{devel_pname}
symlink="%{_prefix}/src/ofa_kernel/default"
# Should only be used for upgrading from pre-5.5-0.2.6.0 packages:
# At the time of upgrade there was still a directory, so postpone
# generating the alternative symlink to that point:
for flag_file in %{_prefix}/src/ofa_kernel/*/*.missing_link; do
    dir=${flag_file%.missing_link}
    if [ ! -d "$dir" ]; then
        # Directory is no longer there. Nothing left to handle
        rm -f "$flag_file"
        continue
    fi
    if [ -d "$symlink" ]; then
        echo "%{devel_pname}-%{version}: $symlink is still a non-empty directory. Deleting in preparation for a symlink."
        rm -rf "$symlink"
    fi
    update-alternatives --install \
        "$symlink" \
        ofa_kernel_headers \
        "$dir" \
        20
    rm -f "$flag_file"
done

%postun -n %{devel_pname}
update-alternatives --remove \
    ofa_kernel_headers \
    %{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION} \
%files -n %{utils_pname}
%defattr(-,root,root,-)
%license COPYING
%doc source/ofed_scripts/82-net-setup-link.rules source/ofed_scripts/vf-net-link-name.sh
%dir %{_sysconfdir}/infiniband
%config(noreplace) %{_sysconfdir}/infiniband/openib.conf
%config(noreplace) %{_sysconfdir}/infiniband/mlx5.conf
%{_sysconfdir}/infiniband/info
%{_sysconfdir}/init.d/openibd
%if "%{WITH_SYSTEMD}" == "1"
%{_unitdir}/openibd.service
%{_sysconfdir}/systemd/system/mlnx_interface_mgr@.service
%endif
/lib/udev/sf-rep-netdev-rename
/lib/udev/auxdev-sf-netdev-rename
%{_sbindir}/setup_mr_cache.sh
%{_datadir}/mlnx_ofed/mlnx_bf_assign_ct_cores.sh
%config(noreplace) %{_sysconfdir}/modprobe.d/mlnx.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/mlnx-bf.conf
%{_sbindir}/*
/lib/udev/rules.d/83-mlnx-sf-name.rules
/lib/udev/rules.d/90-ib.rules
/bin/mlnx_interface_mgr.sh
/bin/mlnx_conf_mgr.sh
%if "%{WINDRIVER}" == "1" || "%{BLUENIX}" == "1"
%{_sbindir}/net-interfaces
%endif
%if %{build_ipoib}
%config(noreplace) %{_sysconfdir}/modprobe.d/ib_ipoib.conf
%endif
%if %{build_mlx5}
%{_sbindir}/ibdev2netdev
%endif

%files -n %{non_kmp_pname}
/lib/modules/%{KVERSION}/%{install_mod_dir}

%files -n %{devel_pname}
%defattr(-,root,root,-)
%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION}

%files source
%defattr(-,root,root,-)
%{_prefix}/src/ofa_kernel-%{version}/source
%{_prefix}/src/mlnx-ofa_kernel-%{version}

%changelog
* Fri Jun 30 2023 Juan Camposeco <juanarturoc@microsoft.com> - 23.04-0
- Update ofa_kernel to 23.04
- Remove highest_supported_kernel and not applicable Obsoletes
- Linting formatting

* Thu Mar 23 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.6-2
- Add highest_supported_kernel macro = 5.15.87.1
- Add BuildRequires for kernel-devel <= highest_supported_kernel
- Add Requires for kernel <= highest_supported_kernel

* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.6-1
- Initial CBL-Mariner import from NVIDIA (license: GPLv2).
- Lint spec to conform to Mariner
- Remove unused module signing
- License verified

* Thu Jun 18 2015 Alaa Hleihel <alaa@mellanox.com>
- Renamed kernel-ib package to mlnx-ofa_kernel-modules

* Thu Apr 10 2014 Alaa Hleihel <alaa@mellanox.com>
- Add QoS utils.

* Thu Mar 13 2014 Alaa Hleihel <alaa@mellanox.com>
- Use one spec for KMP and non-KMP OS's.

* Tue Apr 24 2012 Vladimir Sokolovsky <vlad@mellanox.com>
- Remove FC support

* Tue Mar 6 2012 Vladimir Sokolovsky <vlad@mellanox.com>
- Add weak updates support

* Wed Jul 6 2011 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Add KMP support

* Mon Oct 4 2010 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Add mlx4_fc and mlx4_vnic support

* Mon May 10 2010 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Support install macro that removes RPM_BUILD_ROOT

* Thu Feb 4 2010 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added ibdev2netdev script

* Mon Sep 8 2008 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added nfsrdma support

* Wed Aug 13 2008 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added mlx4_en support

* Tue Aug 21 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added %build macro

* Sun Jan 28 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Created spec file for kernel-ib
