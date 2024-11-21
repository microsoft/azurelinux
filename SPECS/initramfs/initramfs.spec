Summary:        initramfs
Name:           initramfs
Version:        3.0
Release:        3%{?dist}
License:        Apache License
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
Source0:        fscks.conf
BuildRequires:  grub2-rpm-macros
Requires:       dracut
Provides:       initramfs

%description
This package provides the configuration files for initrd generation.

%install
mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d
install -D -m644 %{SOURCE0} %{buildroot}%{_sysconfdir}/dracut.conf.d/

%define watched_path %{_sbindir} %{_libdir}/udev/rules.d %{_libdir}/systemd/system /lib/modules %{_sysconfdir}/dracut.conf.d
%define watched_pkgs e2fsprogs, systemd, kpartx, device-mapper-multipath, verity-read-only-root, dracut-fips, dracut-megaraid

%define removal_action() rm -rf %{_localstatedir}/lib/rpm-state/initramfs

# How it works:
#
# We would like initramfs generation to happen if a given set of packages
# are changed, including installing/upgrading/uninstalling.
#
# Hence, Two sets of triggers:
#
# package triggers for setting the `regenerate` flag
# upon critical package install/upgrade/uninstall
#
# file transaction triggers which overlaps the set of files in those packages
# so that we have an opportunity to check for the flag and (re)generate
# initrd for all the kernels.
#
# All the flags will be put in /var/lib/rpm-state/initramfs
#
# This ensures the easy removal of the intermediate state,
# postun is essential here, as it guarantees that no intermediate states
# will be left over for the new initramfs rpm, since triggerin/un
# in the new rpm will execute after the postun in the old rpm
#
# The order of the scriptlet is critical. The heavy lifting dracut is
# always done post transaction, as it's always invoked in posttrans/
# transfiletriggerin/transfiletriggerpostun. Whereas the creation of flag
# is in the middle of transaction.
#
# The kernel rpm has triggers for initramfs. This is an optimization, as
# we don't want dracut be invoked for all the kernels if some of the kernel
# rpms is being installed/upgraded/uninstalled. Hence, there is no trigger
# in initramfs watching for linux, but there is file transaction trigger
# watching for /lib/modules. The triggerin in linux.rpm will create flag as
#
# pending/%{uname_r}
#
# which indicates only the corresponding initrd will be (re)generated, and
# the triggerun in linux.rpm will remove the corresponding initrd.

%define pkgs_trigger_action() \
[ -f %{_localstatedir}/lib/rpm-state/initramfs/regenerate ] && exit 0 \
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs \
touch %{_localstatedir}/lib/rpm-state/initramfs/regenerate \
echo "initramfs (re)generation" %* >&2

%define file_trigger_action() \
cat > /dev/null \
if [ -f %{_localstatedir}/lib/rpm-state/initramfs/regenerate ]; then \
    echo "(re)generate initramfs for all kernels," %* >&2 \
    dracut --quiet --force --regenerate-all \
elif [ -d %{_localstatedir}/lib/rpm-state/initramfs/pending ]; then \
    for k in `ls %{_localstatedir}/lib/rpm-state/initramfs/pending/`; do \
        echo "(re)generate initramfs for $k," %* >&2 \
        dracut --quiet --force --fstab --kver $k \
    done; \
fi \
%grub2_post
%removal_action

%posttrans
echo "initramfs" %{version}-%{release} "posttrans" >&2
%removal_action
dracut --quiet --force --regenerate-all
%grub2_post

%postun
echo "initramfs" %{version}-%{release} "postun" >&2
#cleanup the states
%removal_action

%triggerin -- %{watched_pkgs}
[ $1 -gt 1 ] && exit 0
#Upgrading, let the posttrans of new initramfs handles it
%pkgs_trigger_action triggerin $* %{version}-%{release}

%triggerun -- %{watched_pkgs}
[ $1 -eq 0 ] && exit 0
#Uninstalling, let the linux.rpm removes initrd for themselves
%pkgs_trigger_action triggerun $* %{version}-%{release}

%transfiletriggerin -- %{watched_path}
%file_trigger_action transfilertriggerin %{version}-%{release}

%transfiletriggerpostun -- %{watched_path}
%file_trigger_action transfiletriggerpostun %{version}-%{release}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/dracut.conf.d/fscks.conf

%changelog
* Wed Mar 06 2024 Chris Gunn <chrisgun@microsoft.com> - 3.0-3
- Remove /var/lib/initramfs/kernel files.

* Fri Feb 23 2024 Chris Gunn <chrisgun@microsoft.com> - 3.0-2
- Call dracut instead of mkinitrd
- Rename initrd.img-<kver> to initramfs-<kver>.img

* Mon Feb 26 2024 Sean Dougherty <sdougherty@microsoft.com> - 3.0-1
- Version bump for Azure Linux 3.0

* Wed Jan 24 2024 Cameron Baird <cameronbaird@microsoft.com> - 2.0-15
- Deprecate old linuxloader in file_trigger_action macro

* Fri Oct 06 2023 Cameron Baird <cameronbaird@microsoft.com> - 2.0-14
- Ensure grub2-mkconfig is called after the initramfs generation
- Deprecate old linuxloader; no longer copy initrd image to efi partition 

* Wed Jun 28 2023 Cameron Baird <cameronbaird@microsoft.com> - 2.0-13
- Copy the initrd image to /boot/efi to maintain backwards compatibility
    with the old linuxloader. Let the initrd remain in /boot as well. 

* Fri Apr 07 2023 Andy Zaugg <azaugg@linkedin.com> - 2.0-12
- Added fsck.xfs into initrd

* Fri Mar 31 2023 Vince Perri <viperri@microsoft.com> - 2.0-11
- Add dracut-megaraid to package watch list, since it will add dracut modules

* Thu Mar 02 2023 Cameron Baird <cameronbaird@microsoft.com> - 2.0-10
- Create initrd in /boot/efi for kernel-mshv only if it is a kata image

* Mon Dec 12 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0-9
- Create initrd in /boot/efi for kernel-mshv.
- License verified.

* Thu Feb 04 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.0-8
- Add dracut-fips to package watch list, since it will add a dracut module

* Fri Dec 11 2020 Daniel McIlvaney <damcilva@microsoft.com> - 2.0-7
- Add verity-read-only-root to package watch list, since it will add a dracut module

* Thu Oct 01 2020 Chris Co <chrco@microsoft.com> 2.0-6
- Update file-triggered initrd generation to workaround kdump initrd limitations

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Aug 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 2.0-4
- Remove watching ostree

* Thu Jul 27 2017 Bo Gan <ganb@vmware.com> 2.0-3
- Move all states to one directory

* Fri May 26 2017 Bo Gan <ganb@vmware.com> 2.0-2
- Discard stdin before dracut

* Wed Apr 12 2017 Bo Gan <ganb@vmware.com> 2.0-1
- Made initrd generation dynamic, triggers for systemd, e2fs-progs

* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-7
- Expand uname -r to have release number

* Wed Nov 23 2016 Anish Swaminathan <anishs@vmware.com> 1.0-6
- Dracut module change to include systemd initrd target

* Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-5
- Added fsck tools
- Use kernel version and release number in initrd file name

* Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-4
- Added kernel macros

* Thu Jun 30 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-4
- Exapand setup macro and remove the source file.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-3
- GA - Bump release of all rpms

* Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-2
- Update to linux-4.4.8

* Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-1
- Initial version.
