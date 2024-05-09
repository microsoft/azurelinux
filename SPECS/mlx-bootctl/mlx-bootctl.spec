#
# Copyright (c) 2017 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    available from the Open Source Initiative, see
#    https://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is
#    available from the Open Source Initiative, see
#    https://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    https://www.opensource.org/licenses/gpl-license.php.
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

%global extended_release 0.g99bc4ab
%global BF_VERSION 3.9.0

# take kernel version or default to uname -r
%global KVERSION %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global K_SRC %{_libdir}/modules/%{KVERSION}/build
%global moddestdir %{buildroot}%{_libdir}/modules/%{KVERSION}/kernel/

Summary:        mlx-bootctl Driver
Name:           mlx-bootctl
# Update extended_release with version updates
Version:        1.5
Release:        1%{?dist}
License:        GPLv2 or BSD or CPL
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://www.mellanox.com/
Source:         https://linux.mellanox.com/public/repo/bluefield/%{BF_VERSION}/extras/SOURCES/%{name}-%{version}.tar.gz
BuildRequires:  kernel-devel
BuildRequires:  kmod

%description
%{name} kernel modules release %extended_release

%global kernel_source() %{K_SRC}
%global kernel_release() %{KVERSION}
%global flavors_to_build default

# set modules dir
%{!?install_mod_dir: %global install_mod_dir extra/%{name}}

%prep
%autosetup -p1
set -- *
mkdir source
mv "$@" source/
cp source/debian/copyright COPYRIGHT
mkdir obj

%build
export EXTRA_CFLAGS='-DVERSION=\"%version\"'
export INSTALL_MOD_DIR=%{install_mod_dir}
export CONF_OPTIONS="%{configure_options}"
for flavor in %{flavors_to_build}; do
	export K_BUILD=%{kernel_source $flavor}
	export KVER=%{kernel_release $K_BUILD}
	export LIB_MOD_DIR=/lib/modules/$KVER/$INSTALL_MOD_DIR
	rm -rf obj/$flavor
	cp -r source obj/$flavor
	cd $PWD/obj/$flavor
	make -C $K_BUILD M=$PWD
	cd -
done

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=%{install_mod_dir}
export PREFIX=%{_prefix}
for flavor in %flavors_to_build; do
	export K_BUILD=%{kernel_source $flavor}
	export KVER=%{kernel_release $K_BUILD}
	cd $PWD/obj/$flavor
	make -C $K_BUILD M=$PWD INSTALL_MOD_PATH=${INSTALL_MOD_PATH} INSTALL_MOD_DIR=${INSTALL_MOD_DIR} modules_install

	# Cleanup unnecessary kernel-generated module dependency files.
	find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;
	cd -
done

# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} \( -type f -name '*.ko' -o -name '*ko.gz' \) -exec %{__chmod} u+x \{\} \;

%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
for module in `find %{buildroot}/ -name '*.ko' -o -name '*.ko.gz'`
do
ko_name=${module##*/}
mod_name=${ko_name/.ko*/}
mod_path=${module/*\/%{name}}
mod_path=${mod_path/\/${ko_name}}
echo "override ${mod_name} * extra/%{name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/zz02-%{name}.conf
done
/sbin/depmod -a %{KVERSION}

%post
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
  /sbin/depmod %{KVERSION}
fi # 1 : closed
# END of post

%postun
/sbin/depmod %{KVERSION}

%files
%defattr(-,root,root,-)
%license COPYRIGHT
/lib/modules/%{KVERSION}/
%{_sysconfdir}/depmod.d/zz02-%{name}.conf

%changelog
* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.5-1
- Initial CBL-Mariner import from NVIDIA (license: GPLv2).
- Lint spec to conform to Mariner
- Remove unused module signing
- License verified

* Fri Sep 1 2017 Vladimir Sokolovsky <vlad@mellanox.com>
- Initial packaging
