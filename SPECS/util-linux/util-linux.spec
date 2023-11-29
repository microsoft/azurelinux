Summary:        Utilities for file systems, consoles, partitions, and messages
Name:           util-linux
Version:        2.39.2
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://git.kernel.org/pub/scm/utils/util-linux/util-linux.git/about/
Source0:        https://mirrors.edge.kernel.org/pub/linux/utils/%{name}/v2.37/%{name}-%{version}.tar.xz
Source1:        runuser
Source2:        runuser-l
Source3:        su
Source4:        su-l
BuildRequires:  audit-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libselinux-devel
BuildRequires:  ncurses-devel
BuildRequires:  pam-devel
Requires:       %{name}-libs = %{version}-%{release}
Requires:       audit-libs
Conflicts:      toybox
Provides:       %{name}-ng = %{version}-%{release}
Provides:       hardlink = 1.3-9
Provides:       uuidd = %{version}-%{release}
%if %{with_check}
BuildRequires:  ncurses-term
%endif

%description
Utilities for handling file systems, consoles, partitions,
and messages.

%package lang
Summary:        Additional language files for util-linux
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description lang
These are the additional language files of util-linux.

%package devel
Summary:        Header and library files for util-linux
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Provides:       libmount-devel = %{version}-%{release}
Provides:       libblkid = %{version}-%{release}
Provides:       libblkid-devel = %{version}-%{release}
Provides:       libuuid-devel = %{version}-%{release}
Provides:       libuuid-devel%{?_isa} = %{version}-%{release}
Provides:       libsmartcols = %{version}-%{release}
Provides:       libsmartcols-devel = %{version}-%{release}

%description devel
These are the header and library files of util-linux.

%package libs
Summary:        library files for util-linux
Group:          Development/Libraries

%description libs
These are library files of util-linux.

%prep
%autosetup -p1
sed -i -e 's@etc/adjtime@var/lib/hwclock/adjtime@g' $(grep -rl '%{_sysconfdir}/adjtime' .)

%build
autoreconf -fi
./configure \
    --enable-hardlink \
    --disable-nologin \
    --disable-chfn-chsh \
    --disable-login \
    --disable-silent-rules \
    --disable-static \
    --disable-use-tty-group \
    --without-python \
    --with-selinux \
    --with-audit
make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}%{_sharedstatedir}/hwclock
make DESTDIR=%{buildroot} install
chmod 644 %{buildroot}%{_docdir}/util-linux/getopt*.tcsh
find %{buildroot} -type f -name "*.la" -delete -print

# Install 'uuidd' directories, which are not created by 'make'.
install -d %{buildroot}%{_prefix}%{_var}/run/uuidd
install -d %{buildroot}%{_sharedstatedir}/libuuid

%find_lang %{name}

install -vdm755 %{buildroot}%{_sysconfdir}/pam.d
install -vm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/

%check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"
rm -rf %{buildroot}/lib/systemd/system

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%dir %{_sharedstatedir}/hwclock
%dir %{_prefix}%{_var}/run/uuidd
%dir %{_sharedstatedir}/libuuid
/bin/*
%attr(4755,root,root) /bin/mount
%attr(4755,root,root) /bin/umount
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/*
%{_docdir}/util-linux/getopt*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/runuser
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/runuser-l
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/su
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/su-l

%files lang -f %{name}.lang
%defattr(-,root,root)

%files libs
%defattr(-,root,root)
%{_libdir}/*.so
/lib/libblkid.so.*
/lib/libmount.so.*
/lib/libuuid.so.*
/lib/libsmartcols.so.*
/lib/libfdisk.so.*

%files devel
%defattr(-,root,root)
%license Documentation/licenses/COPYING.LGPL-2.1-or-later libsmartcols/COPYING
%license libblkid/COPYING
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 28 2023 Andrew Phelps <anphel@microsoft.com> - 2.39.2-1
- Upgrade to 2.39.2

* Thu Sep 21 2023 Andrew Phelps <anphel@microsoft.com> - 2.37.4-8
- Add su-l file for PAM

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.37.4-7
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed May 24 2023 Tobias Brick <tobiasb@microsoft.com> - 2.37.4-6
- Add SETUID bit to mount and umount.

* Mon Feb 06 2023 Mitch Zhu <mitchzhu@microsoft.com> - 2.37.4-5
- Add patch to prevent cdrom probe on Azure VMs

* Wed Jul 20 2022 Minghe Ren <mingheren@microsoft.com> - 2.37.4-4
- Modify su to improve security
- Change file permission on mount and umount to improve security

* Fri Jul 01 2022 Andrew Phelps <anphel@microsoft.com> - 2.37.4-3
- Enable su tool and related PAM config

* Mon Jun 13 2022 Rachel Menge <rachelmenge@microsoft.com> - 2.37.4-2
- Add Buildrequires libcap-ng-devel to build setpriv

* Tue Jun 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.37.4-1
- Updating to 2.37.4 to fix CVE-2022-0563.

* Tue May 03 2022 Sriram Nambakam <snambakam@microsoft.com> - 2.37.2-5
- Split libraries into the util-linux-libs package

* Mon Mar 14 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.37.2-4
- Add Debian's PAM configs for runuser tool
- Add build require on pam-devel so we have the pam headers

* Fri Mar 04 2022 Andrew Phelps <anphel@microsoft.com> - 2.37.2-3
- Build with audit support

* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.37.2-2
- Removing epoch

* Tue Oct 12 2021 Andrew Phelps <anphel@microsoft.com> - 2.37.2-1
- Update to version 2.37.2

* Tue Sep 21 2021 Henry Li <lihl@microsoft.com> - 2.36.1-5
- Add libmount, libuuid and libfdisk shared library files to util-linux-devel
- Remove libblkid and libfdisk shared library files from util-linux
- Remove util-linux-libs subpackage

* Tue Aug 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.36.1-4
- Adding 'Provides' for 'uuidd' and fixing it.

* Mon Mar 15 2021 Henry Li <lihl@microsoft.com> - 2.36.1-3
- Provide util-linux-ng
- Add files to util-linux-devel
- Provides libblkid, libsmartcols and libsmartcols-devel from util-linux-devel

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.36.1-2
- Provide libuuid-devel%%{?_isa}

* Tue Jan 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.36.1-1
- Upgrade to version 2.36.1.
- Provide hardlink.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 2.32.1-4
- Provide libmount-devel, libblkid-devel, libuuid-devel in util-linux-devel

* Fri Sep 04 2020 Daniel Burgener <daburgen@microsoft.com> 2.32.1-4
- Enable SELinux support (Merged from Mariner 1.0 branch)

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.23.1-3
- Added %%license line automatically

* Tue Apr 14 2020 Emre Girgin <mrgirgin@microsoft.com> 2.32.1-2
- Rename ncurses-terminfo to ncurses-term.

* Tue Mar 17 2020 Andrew Phelps <anphel@microsoft.com> 2.32.1-1
- Update version to 2.32.1. License verified.

* Thu Feb 27 2020 Henry Beberman <hebeberm@microsoft.com> 2.32-4
- Disable chfn, chsh, login, and su builds. These are provided by shadow.

* Tue Dec 03 2019 Andrew Phelps <anphel@microsoft.com> 2.32-3
- Run autoconf to remake build system files

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.32-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Apr 09 2018 Xiaolin Li <xiaolinl@vmware.com> 2.32-1
- Update to version 2.32, fix CVE-2018-7738

* Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 2.31.1-1
- Upgrade to version 2.31.1.

* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-5
- Added conflicts toybox

* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 2.29.2-4
- Cleanup check

* Mon Jul 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-3
- Fixed rpm check errors.

* Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-2
- Added -libs subpackage to strip docker image.

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-1
- Updated to version 2.29.2.

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.27.1-5
- Moved man3 to devel subpackage.

* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2.27.1-4
- Disable use tty droup

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.27.1-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.27.1-2
- GA - Bump release of all rpms

* Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 2.27.1-1
- Upgrade version.

* Tue Oct 6 2015 Xiaolin Li <xiaolinl@vmware.com> 2.24.1-3
- Disable static, move header files, .so and config files to devel package.

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 2.24.1-2
- Update according to UsrMove.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24.1-1
- Initial build. First version
