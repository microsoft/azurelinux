%global __provides_exclude_from ^(%{python2_sitearch}/.*\\.so|%{python3_sitearch}/.*\\.so)$

Summary:        iSCSI daemon and utility programs
Name:           iscsi-initiator-utils
Version:        2.1.9
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.open-iscsi.com/
Source0:        https://github.com/open-iscsi/open-iscsi/archive/%{git_commit}.tar.gz#/open-iscsi-%{version}.tar.gz
Source4:        04-iscsi
Source5:        iscsi-tmpfiles.conf

Patch0001:      0001-unit-file-tweaks.patch
Patch0002:      0002-idmb_rec_write-check-for-tpgt-first.patch
Patch0003:      0003-idbm_rec_write-seperate-old-and-new-style-writes.patch
Patch0004:      0004-idbw_rec_write-pick-tpgt-from-existing-record.patch
Patch0005:      0005-update-initscripts-and-docs.patch
Patch0006:      0006-use-var-for-config.patch
Patch0007:      0007-use-red-hat-for-name.patch
Patch0008:      0008-libiscsi.patch
Patch0009:      0009-Add-macros-to-release-GIL-lock.patch
Patch0010:      0010-libiscsi-introduce-sessions-API.patch
Patch0011:      0011-libiscsi-fix-discovery-request-timeout-regression.patch
Patch0012:      0012-libiscsi-format-security-build-errors.patch
Patch0013:      0013-libiscsi-fix-build-to-use-libopeniscsiusr.patch
Patch0014:      0014-libiscsi-fix-build-against-latest-upstream-again.patch
Patch0015:      0015-remove-the-offload-boot-supported-ifdef.patch
Patch0016:      0016-Revert-iscsiadm-return-error-when-login-fails.patch
Patch0017:      0017-dont-install-scripts.patch
Patch0018:      0018-use-var-lib-iscsi-in-libopeniscsiusr.patch
Patch0019:      0019-Coverity-scan-fixes.patch
Patch0020:      0020-fix-upstream-build-breakage-of-iscsiuio-LDFLAGS.patch
Patch0021:      0021-use-Red-Hat-version-string-to-match-RPM-package-vers.patch
Patch0022:      0022-iscsi_if.h-replace-zero-length-array-with-flexible-a.patch
Patch0023:      0023-stop-using-Werror-for-now.patch
Patch0024:      0024-minor-service-file-updates.patch
Patch0025:      0025-Remove-dependences-from-iscsi-init.service.patch
Patch0026:      0026-fix-libpath.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  doxygen
BuildRequires:  flex
BuildRequires:  isns-utils-devel
BuildRequires:  kmod-devel
BuildRequires:  libmount-devel
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-units

Requires:       %{name}-iscsiuio >= %{version}-%{release}
Requires:       isns-utils
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

# Old NetworkManager expects the dispatcher scripts in a different place
Conflicts:      NetworkManager < 1.20

%description
The iscsi package provides the server daemon for the iSCSI protocol,
as well as the utility programs used to manage it. iSCSI is a protocol
for distributed disk access using SCSI commands sent over Internet
Protocol networks.

%package iscsiuio
Summary:        Userspace configuration daemon required for some iSCSI hardware
License:        BSD
Requires:       %{name} = %{version}-%{release}

%description iscsiuio
The iscsiuio configuration daemon provides network configuration help
for some iSCSI offload hardware.

%package devel
Summary:        Development files for %{name}
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n python3-%{name}
%{?python_provide:%python_provide python3-%{name}}
Summary:        Python %{python3_version} bindings to %{name}
License:        GPLv2+
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  make
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
The %{name}-python3 package contains Python %{python3_version} bindings to the
libiscsi interface for interacting with %{name}

%prep
%autosetup -p1 -n open-iscsi-%{open_iscsi_version}.%{open_iscsi_build}

# change exec_prefix, there's no easy way to override
sed -i -e 's|^exec_prefix = /$|exec_prefix = %{_exec_prefix}|' Makefile

%build
# avoid undefined references linking failures
%undefine _ld_as_needed

# configure sub-packages from here
# letting the top level Makefile do it will lose setting from rpm
cd iscsiuio
autoreconf --install
%configure
cd ..

make OPTFLAGS="%{optflags} %{?__global_ldflags}"
pushd libiscsi
%py3_build
popd


%install
make DESTDIR=%{?buildroot} install_programs install_doc install_etc install_libopeniscsiusr
rm %{buildroot}%{_mandir}/man8/iscsi_discovery.8
rm %{buildroot}%{_mandir}/man8/iscsi_fw_login.8
install -pm 755 usr/iscsistart %{buildroot}%{_sbindir}
install -pm 644 doc/iscsistart.8 %{buildroot}%{_mandir}/man8
install -pm 644 doc/iscsi-iname.8 %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -pm 644 iscsiuio/iscsiuiolog %{buildroot}%{_sysconfdir}/logrotate.d

install -d %{buildroot}%{_sharedstatedir}/iscsi
install -d %{buildroot}%{_sharedstatedir}/iscsi/nodes
install -d %{buildroot}%{_sharedstatedir}/iscsi/send_targets
install -d %{buildroot}%{_sharedstatedir}/iscsi/static
install -d %{buildroot}%{_sharedstatedir}/iscsi/isns
install -d %{buildroot}%{_sharedstatedir}/iscsi/slp
install -d %{buildroot}%{_sharedstatedir}/iscsi/ifaces

# for %%ghost
%{__install} -d %{buildroot}%{_rundir}/lock/iscsi
touch %{buildroot}%{_rundir}/lock/iscsi/lock


install -d %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsi.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsi-shutdown.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsi-init.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsid.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsid.socket %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsiuio.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsiuio.socket %{buildroot}%{_unitdir}

install -d %{buildroot}%{_libexecdir}
install -pm 755 etc/systemd/iscsi-mark-root-nodes %{buildroot}%{_libexecdir}

install -d %{buildroot}%{_libdir}/NetworkManager/dispatcher.d
install -pm 755 %{SOURCE4} %{buildroot}%{_libdir}/NetworkManager/dispatcher.d

install -d %{buildroot}%{_tmpfilesdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/iscsi.conf

install -d %{buildroot}%{_libdir}
install -pm 755 libiscsi/libiscsi.so.0 %{buildroot}%{_libdir}
ln -s    libiscsi.so.0 %{buildroot}%{_libdir}/libiscsi.so
install -d %{buildroot}%{_includedir}
install -pm 644 libiscsi/libiscsi.h %{buildroot}%{_includedir}

install -d %{buildroot}%{python3_sitearch}
pushd libiscsi
%py3_install
popd


%post
%systemd_post iscsi.service iscsi-init.service iscsi-shutdown.service iscsid.service iscsid.socket

if [ $1 -eq 1 ]; then
  if [ ! -f %{_sysconfdir}/iscsi/initiatorname.iscsi ]; then
    echo "InitiatorName=`%{_sbindir}/iscsi-iname`" > %{_sysconfdir}/iscsi/initiatorname.iscsi
  fi
  # enable socket activation and persistant session startup by default
  /bin/systemctl enable iscsi.service >/dev/null 2>&1 || :
  /bin/systemctl enable iscsid.socket >/dev/null 2>&1 || :
fi

%post iscsiuio
%systemd_post iscsiuio.service iscsiuio.socket

if [ $1 -eq 1 ]; then
  /bin/systemctl enable iscsiuio.socket >/dev/null 2>&1 || :
fi

%preun
%systemd_preun iscsi.service iscsi-shutdown.service iscsid.service iscsiuio.service iscsid.socket iscsiuio.socket

%preun iscsiuio
%systemd_preun iscsiuio.service iscsiuio.socket

%postun
%systemd_postun iscsi.service iscsi-shutdown.service iscsid.service iscsiuio.service iscsid.socket iscsiuio.socket

%postun iscsiuio
%systemd_postun iscsiuio.service iscsiuio.socket

%triggerun -- iscsi-initiator-utils < 6.2.0.873-25
# prior to 6.2.0.873-24 iscsi.service was missing a Wants=remote-fs-pre.target
# this forces remote-fs-pre.target active if needed for a clean shutdown/reboot
# after upgrading this package
if [ $1 -gt 0 ]; then
    %{_bindir}/systemctl -q is-active iscsi.service
    if [ $? -eq 0 ]; then
        %{_bindir}/systemctl -q is-active remote-fs-pre.target
        if [ $? -ne 0 ]; then
            SRC=`%{_bindir}/systemctl show --property FragmentPath remote-fs-pre.target | cut -d= -f2`
            DST=/run/systemd/system/remote-fs-pre.target
            if [ $SRC != $DST ]; then
                cp $SRC $DST
            fi
            sed -i 's/RefuseManualStart=yes/RefuseManualStart=no/' $DST
            %{_bindir}/systemctl daemon-reload >/dev/null 2>&1 || :
            %{_bindir}/systemctl start remote-fs-pre.target >/dev/null 2>&1 || :
        fi
    fi
fi
# added in 6.2.0.873-25
if [ $1 -gt 0 ]; then
    systemctl start iscsi-shutdown.service >/dev/null 2>&1 || :
fi

%files
%license COPYING
%doc README
%dir %{_sharedstatedir}/iscsi
%dir %{_sharedstatedir}/iscsi/nodes
%dir %{_sharedstatedir}/iscsi/isns
%dir %{_sharedstatedir}/iscsi/static
%dir %{_sharedstatedir}/iscsi/slp
%dir %{_sharedstatedir}/iscsi/ifaces
%dir %{_sharedstatedir}/iscsi/send_targets
%ghost %attr(0700, root, root) %{_rundir}/lock/iscsi
%ghost %attr(0600, root, root) %{_rundir}/lock/iscsi/lock
%{_unitdir}/iscsi.service
%{_unitdir}/iscsi-init.service
%{_unitdir}/iscsi-shutdown.service
%{_unitdir}/iscsid.service
%{_unitdir}/iscsid.socket
%{_libexecdir}/iscsi-mark-root-nodes
%{_libdir}/NetworkManager
%{_tmpfilesdir}/iscsi.conf
%dir %{_sysconfdir}/iscsi
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/iscsi/iscsid.conf
%{_sbindir}/iscsi-iname
%{_sbindir}/iscsiadm
%{_sbindir}/iscsid
%{_sbindir}/iscsistart
%{_libdir}/libiscsi.so.0
%{_mandir}/man8/iscsi-iname.8.gz
%{_mandir}/man8/iscsiadm.8.gz
%{_mandir}/man8/iscsid.8.gz
%{_mandir}/man8/iscsistart.8.gz
# until we decide to setup libopeniscsiusr as a subpkg for real
%{_libdir}/libopeniscsiusr.so.*

%files iscsiuio
%{_sbindir}/iscsiuio
%{_unitdir}/iscsiuio.service
%{_unitdir}/iscsiuio.socket
%config(noreplace) %{_sysconfdir}/logrotate.d/iscsiuiolog
%{_mandir}/man8/iscsiuio.8.gz

%files devel
%{_libdir}/libiscsi.so
%{_includedir}/libiscsi.h
%{_includedir}/libopeniscsiusr_node.h
%{_libdir}/libopeniscsiusr.so
%{_includedir}/libopeniscsiusr.h
%{_includedir}/libopeniscsiusr_common.h
%{_includedir}/libopeniscsiusr_iface.h
%{_includedir}/libopeniscsiusr_session.h
%{_libdir}/pkgconfig/libopeniscsiusr.pc

%files -n python3-%{name}
%{python3_sitearch}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 6.2.1.4+20210729.2a8f9d8-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Mar 14 2022 Cameron Baird <cameronbaird@microsoft.com> - 6.2.1.4+20210729.2a8f9d8-2
- Package iscsi-init.service 

* Tue Feb 22 2022 Cameron Baird <cameronbaird@microsoft.com> - 6.2.1.4+20210729.2a8f9d8-1
- Update source to v2.1.4
- Readd BR doxygen
- Move libopeniscsiusr*.h files into devel package
- Remove debuginfo

* Thu Jul 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.2.1.0+20191114.4440e57a59-4
- Changed release to a simple integer.
- Switched versioning to closer follow Fedora's guidelines for snapshots.
- Removed BR on 'doxygen' and Python 2 bits.
- Added the '%%license' macro.
- License verified.

* Wed Mar 03 2021 Henry Li <lihl@microsoft.com> - 6.2.1.0-3.git4440e57
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add fix-libpath.patch to fix installation path to /usr/lib instead of /usr/lib64

* Sun Mar 01 2020 Adam Williamson <awilliam@redhat.com> - 6.2.1.0-2.git4440e57
- Backport upstream d3daa7a2 to fix bz #1774746

* Mon Feb 24 2020 Than Ngo <than@redhat.com> - 6.2.1.0-1.git4440e57
- upstream patch to support gcc -fno-common option

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.1.0-0.git4440e57.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 19 2019 Chris Leech <cleech@redhat.com> - 6.2.1.0-0.git4440e57
- update to upstream v2.1.0

* Thu Aug 22 2019 Lubomir Rintel <lkundrak@v3.sk> - 6.2.0.876-12.gitf3c8e90
- Move the NetworkManager dispatcher script out of /etc

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 6.2.0.876-11.gitf3c8e90
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0.876-10.gitf3c8e90
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Chris Leech <cleech@redhat.com> - 6.2.0.876-9.gitf3c8e90
- FTBFS: %systemd_postun scriptlets need service files as an argument

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6.2.0.876-8.gitf3c8e90
- Remove obsolete scriptlets

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0.876-7.gitf3c8e90
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Miro Hrončok <mhroncok@redhat.com> - 6.2.0.876-6.gitf3c8e90
- Disable python2 build

* Tue Jul 10 2018 Chris Leech <cleech@redhat.com> - 6.2.0.876-5.gitf3c8e90
- iscsiuio: add mutex to protect netlink buffer for pass-through xmit
- iscsid: get gateway information from sysfs when recovering sessions
- enabled MaxOustandingR2T negotiation during login

* Mon Jun 25 2018 Adam Williamson <awilliam@redhat.com> - 6.2.0.876-4.git4ef9261
- Rebuilt for Python 3.7, again

* Mon Jun 25 2018 Adam Williamson <awilliam@redhat.com> - 6.2.0.876-3.git4ef9261
- Link libiscsi against libopeniscsiusr (bz #1594946) (python 3.6 build)

* Wed Jun 20 2018 Miro Hrončok <mhroncok@redhat.com> - 6.2.0.876-2.git4ef9261
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Chris Leech <cleech@redhat.com> - 6.2.0.876-1.git4ef9261
- pull in post 2.0.876 tagged fixes from upstream git
- minimal packaging of libopeniscsiusr (internal use only, no dev package yet)
- Conditionalize the python2 subpackage [Charalampos Stratakis <cstratak@redhat.com>]

* Tue Jun 19 2018 Chris Leech <cleech@redhat.com> - 6.2.0.876-1.git24580ad
- rebase to upstream 2.0.876

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 6.2.0.874-10.git86e8892
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0.874-9.git86e8892
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 6.2.0.874-8.git86e8892
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.2.0.874-7.git86e8892
- Python 2 binary package renamed to python2-iscsi-initiator-utils
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0.874-6.git86e8892
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0.874-5.git86e8892
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 12 2017 Chris Leech <cleech@redhat.com> - 6.2.0.874-4.git86e8892
- rebuild to use shared libisns

* Tue Feb 28 2017 Chris Leech <cleech@redhat.com> - 6.2.0.874-3.git86e8892
- libiscsi: fix discovery command timeout regression
- libiscsi: fix format security build errors

* Thu Feb 16 2017 Chris Leech <cleech@redhat.com> - 6.2.0.874-2.git86e8892
- fix regression with iscsiadm discoverydb commands having a 0 timeout

* Thu Feb 09 2017 Chris Leech <cleech@redhat.com> - 6.2.0.874-1
- update to 2.0.874

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 6.2.0.873-35.git4c1f2d9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.873-34.git4c1f2d9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 19 2016 Chris Leech <cleech@redhat.com> - 6.2.0.873-33.git4c1f2d9
- sync with upstream
- sysfs handling changes to speed up operations over large number of sessions

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0.873-32.git4c9d6f9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Feb  3 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 6.2.0.873-31.git4c9d6f9
- BuildRequires: isns-utils-static for -lisns (bz #1291913)

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 6.2.0.873-30.git4c9d6f9
- Rebuilt for Python3.5 rebuild

* Tue Oct 06 2015 Chris Leech <cleech@redhat.com> - 6.2.0.873-29.git4c9d6f9
- rebase with upstream, change Source0 url to github
- build with external isns-utils

* Mon Oct 05 2015 Chris Leech <cleech@redhat.com> - 6.2.0.873-28.git6aa2c9b
- fixed broken multiple trigger scripts, removed old pre-systemd migration triggers
- added libiscsi session API patch (bz #1262279)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.873-27.git6aa2c9b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Chris Leech <cleech@redhat.com> - 6.2.0.873-26.git6aa2c9b
- rebase to upstream snapshot
- add patch to improve GIL lock performance in libiscsi
- Split Python 2 and Python 3 bindings out into subpackages

* Wed Jan 28 2015 Chris Leech <cleech@redhat.com> - 6.2.0.873-25.gitc9d830b
- split out session logout on shutdown to a separate service
- 985321 roll up libiscsi patches, update python bindings to support python3
- scriptlets were never split out properly for the iscsiuio subpackage
- fix regression in network interface binding
- created iscsi-shutdown.service to ensure that session cleanup happens
- Add --with-slp=no
- segfault from unexpected netlink event during discovery
- inhibit strict aliasing optimizations in iscsiuio, rpmdiff error

* Thu Oct 23 2014 Chris Leech <cleech@redhat.com> - 6.2.0.873-24.gitc9d830b
- sync with upstream v2.0.873-84-gc9d830b
- ignore iscsiadm return in iscsi.service
- make sure systemd order against remote mounts is correct
- add discovery as a valid mode in iscsiadm.8
- make sure to pass --with-security=no to isns configure

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.873-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.873-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Chris Leech <cleech@redhat.com> - 6.2.0.873-21
- boot session handling improvements
- split out iscsiuio into a seperate sub-package
- sync with new upstream additions
- revert change to return code when calling login_portal for sessions
  that already exist, as it impacts users scripting around iscsiadm

* Tue Dec 10 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-17
- fix regression in glob use, inappropriate error code escape
- clean up dead node links from discovery when reusing tpgt

* Mon Nov 25 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-16
- fix iscsiuio socket activation
- have systemd start socket units on iscsiadm use, if not already listening

* Sun Sep 15 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-15
- move /sbin to /usr/sbin
- use rpm macros in install rules

* Fri Sep 13 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-14
- fix iscsiuio hardened build and other compiler flags

* Fri Aug 23 2013 Andy Grover <agrover@redhat.com> - 6.2.0.873-13
- Fix patch 0041 to check session != NULL before calling iscsi_sysfs_read_boot()

* Tue Aug 20 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-12
- fix regression in last build, database records can't be accessed

* Mon Aug 19 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-11
- iscsi boot related fixes
  make sure iscsid gets started if there are any boot sessions running
  add reload target to fix double session problem when restarting from NM
  don't rely on session list passed from initrd, never got fully implemented
  remove patches related to running iscsid from initrd, possible to revisit later

* Sun Aug 18 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-10
- sync with upstream git, minor context fixes after rebase of out-of-tree patches
- iscsiuio is merged upstream, remove old source archive and patches
- spec cleanups to fix rpmlint issues

* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 6.2.0.873-9
- Fix FTBFS, cleanup spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.873-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-7
- Use the systemd tmpfiles service to recreate lockfiles in /var/lock
- 955167 build as a position independent executable
- 894576 fix order of setuid/setgid and drop additional groups

* Tue May 28 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-6
- Don't have iscsiadm scan for autostart record if node db is empty (bug #951951)

* Tue Apr 30 2013 Orion Poplawski <orion@cora.nwra.com> - 6.2.0.873-5
- Fix typo in NM dispatcher script (bug #917058)

* Thu Feb 21 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-4
- build with libkmod support, instead of calling out to modprobe
- enable socket activation by default

* Thu Jan 24 2013 Kalev Lember <kalevlember@gmail.com> - 6.2.0.873-3
- Fix the postun script to not use ldconfig as the interpreter

* Wed Jan 23 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-2
- package iscsi_mark_root_nodes script, it's being referenced by the unit files

* Tue Jan 22 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-1
- rebase to new upstream code
- systemd conversion
- 565245 Fix multilib issues caused by timestamp in doxygen footers

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.872-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Mike Christie <mchristi@redhat.com> 6.2.0.872.18
- 789683 Fix boot slow down when the iscsi service is started
  (regression added in 6.2.0.872.16 when the nm wait was added).

* Mon Feb 6 2012 Mike Christie <mchristi@redhat.com> 6.2.0.872.17
- 786174 Change iscsid/iscsi service startup, so it always starts
  when called.

* Sat Feb 4 2012 Mike Christie <mchristi@redhat.com> 6.2.0.872.16
- 747479 Fix iscsidevs handling of network requirement

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.872-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Mike Christie <mcrhsit@redhat.com> 6.2.0.872.14
- Fix version string to reflect fedora and not rhel.

* Tue Oct 18 2011 Mike Christie <mcrhsit@redhat.com> 6.2.0.872.13
- Update iscsi tools.

* Sat Apr 30 2011 Hans de Goede <hdegoede@redhat.com> - 6.2.0.872-12
- Change iscsi init scripts to check for networking being actually up, rather
  then for NetworkManager being started (#692230)

* Tue Apr 26 2011 Hans de Goede <hdegoede@redhat.com> - 6.2.0.872-11
- Fix iscsid autostarting when upgrading from an older version
  (add iscsid.startup key to iscsid.conf on upgrade)
- Fix printing of [ OK ] when successfully stopping iscsid
- systemd related fixes:
 - Add Should-Start/Stop tgtd to iscsi init script to fix (re)boot from
   hanging when using locally hosted targets
 - %%ghost /var/lock/iscsi and contents (#656605)

* Mon Apr 25 2011 Mike Christie <mchristi@redhat.com> 6.2.0.872-10
- Fix iscsi init scripts check for networking being up (#692230)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.872-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
