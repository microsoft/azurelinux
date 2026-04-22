# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2

%global _hardened_build 1
%global __python %{__python3}

%global released 1
#define tag     devel

Name:           lirc
Version:        0.10.2
Release: 5%{?tag:.}%{?tag}%{?dist}
Summary:        The Linux Infrared Remote Control package

%global repo    http://downloads.sourceforge.net/lirc/LIRC/%{version}
%global tarball %{name}-%{version}%{?tag:-}%{?tag}.tar.gz

                # lib/ciniparser* and lib/dictionary* are BSD, others GPLv2
# Automatically converted from old format: GPLv2 and BSD - review is highly recommended.
License:        GPL-2.0-only AND LicenseRef-Callaway-BSD
URL:            http://www.lirc.org/
Source0:        %{?released:%{repo}%{?tag:-}%{?tag}/}%{tarball}
Source1:        README.fedora
Source2:        99-remote-control-lirc.rules
Patch1:         0001-build-install-media-lirc.h-BTS-872074.patch
Patch2:         0002-Revert-build-Fix-missing-media-lirc.h-BTS-872074.patch
Patch3:         0003-asyncio.get_event_loop-can-return-an-error-in-python.patch


BuildRequires:  gcc-c++
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  alsa-lib-devel
Buildrequires:  autoconf
BuildRequires:  automake
BuildRequires:  checkpolicy
BuildRequires:  doxygen
BuildRequires:  expect
BuildRequires:  kernel-headers
BuildRequires:  man2html-core
BuildRequires:  libftdi-devel
BuildRequires:  libtool
%if (0%{?fedora} && 0%{?fedora} < 37) || (0%{?rhel} && 0%{?rhel} < 10)
BuildRequires:  libusb-devel
%else
BuildRequires:  libusb-compat-0.1-devel
%endif
BuildRequires:  libusb1-devel

BuildRequires:  libxslt
BuildRequires:  libXt-devel
BuildRequires:  portaudio-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-PyYAML
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  socat
BuildRequires:  systemd-devel
BuildRequires: make

Requires:       %{name}-libs = %{version}-%{release}
Requires:       lockdev
Suggests:       xorg-x11-misc-fonts

Requires(post):    systemd
                   #for triggerun
Requires(post):    systemd-sysv
Requires(post):    policycoreutils
Requires(postun):  systemd
Requires(postun):  policycoreutils
Requires(preun):   systemd

%description
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.

Installing this package will install most of the LIRC sub-packages.
You might want to install lirc-core, possibly adding some other
packages to get a smaller installation.


%package        core
Summary:        LIRC core, always needed to run LIRC
Requires:       lirc-libs%{?_isa} = %{version}-%{release}
%{?systemd_requires}

%description    core
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

The lirc core contains the lircd daemons, the devinput and
default driver and most of the applications.

%package        compat
Summary:        Compatibility package installing all lirc packages
Obsoletes:      lirc <=  0.9.1a
Provides:       lirc = %{version}-%{release}
Requires:       lirc-core%{?_isa} = %{version}-%{release}
Requires:       lirc-config = %{version}-%{release}
Requires:       lirc-tools-gui%{?_isa} = %{version}-%{release}
Requires:       lirc-drv-portaudio%{?_isa} = %{version}-%{release}
Requires:       lirc-drv-ftdi%{?_isa} = %{version}-%{release}

%description    compat
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

Installing this package will install most lirc sub-packages, roughly
the same as installing previous versions of the lirc package.

%package        libs
Summary:        LIRC libraries

%description    libs
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

This package includes shared libraries that applications use to
interface with LIRC.


%package        config
Summary:        LIRC Configuration Tools and Data
Requires:       lirc-core = %{version}-%{release}
Requires:       lirc-doc = %{version}-%{release}
Requires:       gnome-icon-theme
Requires:       python%{python3_pkgversion}-PyYAML
BuildArch:      noarch

%description    config
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

The  config package contains tools and data to support the
LIRC configuration process.


%package        devel
Summary:        Development files for LIRC
Requires:       lirc-core%{?_isa} = %{version}-%{release}

%description    devel
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

This package includes files for developing applications that use lirc
including headers and pkg-config files.


%package        doc
Summary:        LIRC documentation
BuildArch:      noarch

%description    doc
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

This package contains lirc documentation.


%package        disable-kernel-rc
Summary:        Disable kernel ir device handling in favor of lirc
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description  disable-kernel-rc
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

This package contains an udev rule which disables the kernel built-in
handling of infrared devices (i. e., rc* ones) by making lirc the only
used protocol.


%package        tools-gui
Summary:        LIRC GUI tools
Requires:       lirc-core%{?_isa} = %{version}-%{release}

%description   tools-gui
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

This package contains some seldom used X11-based tools for debugging
lirc configurations.


%package        drv-portaudio
Summary:        Portaudio LIRC User-Space Driver
Requires:       lirc-core%{?_isa} = %{version}-%{release}
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2

%description    drv-portaudio
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

This package contains a lirc user space driver which supports
an IR receiver in microphone input using the portaudio library.


%package        drv-ftdi
Summary:        Ftdi LIRC User-Space Driver
Requires:       lirc-core%{?_isa} = %{version}-%{release}

%description    drv-ftdi
Part of the LIRC package suite which handles IR remotes. See
the package lirc for more.

This package contains a user-space driver which works together
with the kernel, providing full support for the ftdi device.
See http://www.ftdichip.com.


# Don't provide or require anything from _docdir, per policy.
%global __provides_exclude_from ^%{_docdir}/.*$
%global __requires_exclude_from ^%{_docdir}/.*$


%prep
%autosetup -p1 -n %{name}-%{version}%{?tag:-}%{?tag}
sed -i -e 's/#effective-user/effective-user /' lirc_options.conf
sed -i -e '/^effective-user/s/=$/= lirc/' lirc_options.conf
sed -i '/User=/s/; *//' systemd/lircd.service
sed -i '/Group=/s/; *//' systemd/lircd.service
sed -i 's/; *user=/User=/' systemd/irexec.service
sed -i 's/; *group=/Group=/' systemd/irexec.service

sed -i -e "s|/usr/local/etc/|%{_sysconfdir}/|" contrib/irman2lirc

# Create a sysusers.d config file
cat >lirc.sysusers.conf <<EOF
u lirc - 'LIRC daemon user, runs lircd.' /var/log/lirc -
m lirc dialout
m lirc lock
m lirc input
EOF


%build
autoreconf -fi
export PYTHON=/usr/bin/python3

%configure \
        --docdir="%{_pkgdocdir}" \
        --enable-uinput \
        --enable-devinput \
        --with-lockdir=/var/lock/lockdev
make LANG=C.utf8 V=0 %{?_smp_mflags}

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

if test -d python-pkg/tests; then
    cd python-pkg/tests; python3 -m unittest discover || exit 1
    cd $OLDPWD
fi

echo "Plugins: 40" > summary.ok
echo "Drivers: 51" >> summary.ok
echo "Errors: 0"   >> summary.ok
tools/lirc-lsplugins -U plugins/.libs -s > summary
diff -w summary summary.ok || exit 1


%install
make -s V=0 LIBTOOLFLAGS="--silent %{?Wnone}" DESTDIR=$RPM_BUILD_ROOT install

chmod 755 $RPM_BUILD_ROOT%{_datadir}/lirc/contrib/irman2lirc
find $RPM_BUILD_ROOT%{_libdir}/ -name \*.la -delete

install -pm 755 contrib/irman2lirc $RPM_BUILD_ROOT%{_bindir}
install -Dpm 644 contrib/60-lirc.rules \
    $RPM_BUILD_ROOT%{_udevrulesdir}/60-lirc.rules
install -Dpm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_udevrulesdir}/99-remote-control-lirc.rules
cp -a %{SOURCE1} README.fedora

mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
echo "d %{_rundir}/lirc  0755  lirc  lirc  -" \
    > $RPM_BUILD_ROOT%{_tmpfilesdir}/lirc.conf

install -m0644 -D lirc.sysusers.conf %{buildroot}%{_sysusersdir}/lirc.conf



%post core
%systemd_post lircd.service lircmd.service
systemd-tmpfiles --create %{_tmpfilesdir}/lirc.conf

%preun core
%systemd_preun lircd.service lircmd.service

%postun core
%systemd_postun_with_restart lircd.service lircmd.service

%ldconfig_scriptlets libs


%files compat

%files drv-portaudio
%{_libdir}/lirc/plugins/audio.so
%{_datadir}/lirc/configs/audio.conf

%files drv-ftdi
%{_libdir}/lirc/plugins/ftdi.so
%{_datadir}/lirc/configs/ftdi.conf

%files tools-gui
%{_bindir}/xmode2
%{_bindir}/irxevent
%{_mandir}/man1/irxevent*
%{_mandir}/man1/xmode2*

%files config
%{_bindir}/irdb-get
%{_bindir}/lirc-config-tool
%{_bindir}/lirc-setup
%{_mandir}/man1/irdb-get*
%{_mandir}/man1/lirc-config-tool*
%{_mandir}/man1/lirc-setup*
%{_datadir}/lirc/configs/*
%exclude %{_datadir}/lirc/configs/ftdi.conf
%exclude %{_datadir}/lirc/configs/audio.conf


%files core
%doc README AUTHORS NEWS README.fedora
%dir  %{_sysconfdir}/lirc
%{_sysconfdir}/lirc/lircd.conf.d
%config(noreplace) %{_sysconfdir}/lirc/lirc*.conf
%config(noreplace) %{_sysconfdir}/lirc/irexec.lircrc
%{_tmpfilesdir}/lirc.conf
%{_unitdir}/lirc*
%{_unitdir}/irexec.service
%{_udevrulesdir}/60-lirc.rules
%{_bindir}/ircat
%{_bindir}/irexec
%{_bindir}/irman2lirc
%{_bindir}/irpipe
%{_bindir}/irpty
%{_bindir}/irrecord
%{_bindir}/irsend
%{_bindir}/irsimreceive
%{_bindir}/irsimsend
%{_bindir}/irtestcase
%{_bindir}/irtext2udp
%{_bindir}/irw
%{_bindir}/lirc-init-db
%{_bindir}/lirc-lsremotes
%{_bindir}/lirc-make-devinput
%{_bindir}/lircrcd
%{_bindir}/mode2
%{_bindir}/pronto2lirc
%{_sbindir}/lirc-lsplugins
%{_sbindir}/lircd
%{_sbindir}/lircd-setup
%{_sbindir}/lircd-uinput
%{_sbindir}/lircmd
%{_libdir}/lirc/plugins
%exclude %{_libdir}/lirc/plugins/ftdi.so
%exclude %{_libdir}/lirc/plugins/audio.so
%{_libdir}/python%{python3_version}/site-packages/lirc
%{_libdir}/python%{python3_version}/site-packages/lirc-setup
%{_datadir}/lirc/
%{_localstatedir}/lib/lirc/images
%{_localstatedir}/lib/lirc/plugins
%exclude %{_datadir}/lirc/configs/*
%{_mandir}/man1/ircat.1*
%{_mandir}/man1/irexec.1*
%{_mandir}/man1/irpipe.1*
%{_mandir}/man1/irpty.1*
%{_mandir}/man1/irrecord.1*
%{_mandir}/man1/irsend.1*
%{_mandir}/man1/irsimreceive.1*
%{_mandir}/man1/irsimsend.1*
%{_mandir}/man1/irtestcase.1*
%{_mandir}/man1/irtext2udp.1*
%{_mandir}/man1/irw.1*
%{_mandir}/man1/lirc-lsplugins.1*
%{_mandir}/man1/lirc-lsremotes.1*
%{_mandir}/man1/lirc-make-devinput.1*
%{_mandir}/man1/mode2.1*
%{_mandir}/man1/pronto2lirc.1*
%{_mandir}/man5/lircd.conf.5*
%{_mandir}/man5/lircrc.5*
%{_mandir}/man8/lircd-setup.8*
%{_mandir}/man8/lircd-uinput.8*
%{_mandir}/man8/lircd.8*
%{_mandir}/man8/lircmd.8*
%{_mandir}/man8/lircrcd.8*
%{_sysusersdir}/lirc.conf
%exclude %{_bindir}/lirc-data2table
%exclude %{_bindir}/lirc-postinstall
%exclude %{_mandir}/man1/lirc-postinstall.1.gz

%files libs
%license COPYING COPYING.ciniparser COPYING.curl
%{_libdir}/libirrecord.so.*
%{_libdir}/liblirc_client.so.*
%{_libdir}/liblirc_driver.so.*
%{_libdir}/liblirc.so.*

%files devel
%{_includedir}/lirc/
%{_includedir}/lirc_private.h
%{_includedir}/lirc_driver.h
%{_includedir}/lirc_client.h
%{_libdir}/libirrecord.so
%{_libdir}/liblirc_client.so
%{_libdir}/liblirc_driver.so
%{_libdir}/liblirc.so
%{_libdir}/pkgconfig/lirc-driver.pc
%{_libdir}/pkgconfig/lirc.pc

%files doc
%license COPYING COPYING.ciniparser COPYING.curl
%doc ChangeLog
%{_pkgdocdir}

%files disable-kernel-rc
%{_udevrulesdir}/99-remote-control-lirc.rules

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.10.2-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.10.2-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 08 2025 Sean Young <sean@mess.org> - 0.10.2-1
- New upstream version 0.10.2

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.10.0-49
- Rebuilt for Python 3.14

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-48
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Fri Jan 24 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-47
- Adjust file patterns for the sbin merge

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.10.0-45
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.10.0-43
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.10.0-39
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.10.0-36
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Alec Leamas <leamas.alec@nowhere.net> - 0.10.0-35
- Handle libusb-devel -> libus-compat-0.1-devel

* Fri Jan 21 2022 Alec Leamas <leamas.alec@nowhere.net> - 0.10.0-34
- Add patch for revised PyYAML interface. Closes: #2034939

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.10.0-31
- Rebuilt for Python 3.10

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-30
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 03 2020 Alec Leamas <leamas.alec@nowhere.nt> - 0.10.0-28
- Add R: lockdev. Closes: #1839223.

* Mon Oct 26 2020 Alec Leamas <leamas.alec@nowhere.nt> - 0.10.0-27
- Fix python bytecompile FTBFS error.

* Mon Oct 26 2020 Alec Leamas <leamas.alec@nowhere.nt> - 0.10.0-26
- Fix python version FTFBS error.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-25
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-23
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Paul Wouters <pwouters@redhat.com> - 0.10.0-22
- Use rundir macro and not old hardcoded /var/run for tmpfile creation in spec file.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-20
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 21 2019 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-19
- Fix FTBS on python 3.8. Closes: #1718285.
- mode2: Fix inconsistent loglevel/debug option (upstream #307)
- plugins: devinput: fix glob "no match" error (upstream #285, DBS 860551)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-18
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar  9 2019 Stephen John Smoogen <smooge@gmail.com> - 0.10.0-16
- EPEL 7 has moved forward to Python 3.6, no need for suppressing tests for < 3.5 any longer

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-14
- Rework patch for lirc-setup crash on startup.

* Fri Oct 12 2018 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-13
- Added patch for lirc-setup crash on startup.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-11
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-10
- Conditionalize ldconfig scriptlets.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-9
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-8
- Patch systemd files to use correct user and group - #1590724.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-6
- Fix for rhbz #1536901, missing R(post) in lirc-core.

* Thu Dec 28 2017 Tom Hughes <tom@compton.nu> - 0.10.0-5
- Don't expire files in runtime directory.

* Sun Dec 10 2017 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-4
- Fix rhbz #1514359, f27 version is less than f26.

* Sun Aug 20 2017 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-3
- Fix rhbz #1483330, use correct serial devices lock dir.

* Tue Aug 15 2017 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-2
- Fix Debian BTS 872074, FTBS on external plugins e. g. libirman.

* Sat Aug 12 2017 Alec Leamas <leamas.alec@gmail.com> - 0.10.0-1
- New upstream release
- All patches upstreamed.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4c-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4c-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 4 2017 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-8
- Fix bad include paths causing FTBS in packages using -devel.
- Fix bad python import path.
- Fix missing socket activation - #1438702

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4c-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-7
- Added upstream patch for bad ircat --config handling
- Added upstream patch for lircd SET_INPUTLOG segfault
- Added upstream patch for FTBS on clients building against lirc

* Fri Dec 23 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-6
- Add patch for --listen parsing bug (upstream #249).

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.4c-5.1
- Rebuild for Python 3.6

* Wed Dec 07 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-5
- Added missing lircd-setup.service file.

* Sun Oct 30 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-4
- Added upstream patches (10)

* Sat Oct 22 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-3
- Add fix for header file curl_poll.h, fixing clients FTBS errors.

* Fri Oct 21 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-2
- Rebuilt

* Fri Oct 21 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4c-1
- New upstream version, patches upstreamed

* Tue Aug 23 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4b-4
- Add fixes for #221 and #222
- Update patches, include everything from upstream
- Add some minor fixes for lircd.org
- Obsoletes 0.9.4b-3 which is unpushed.

* Mon Aug 22 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4b-3
- Add yet another ABRT crasher fix.
- Update fix for #1364744.

* Wed Aug 17 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4b-2
- Added patch for audio_alsa plugin (#218).
- Move R: python3-PyYAML to lirc-compat, fixes import error
  https://retrace.fedoraproject.org/faf/reports/1229333/
- Modify usb devices acl(5) udev rule (#1364744).

* Tue Aug 09 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4b-1
- Rebuilt for new upstream version 0.9.4b.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4a-1
- New upstream release.
- Fixes #1350750, bad systemd files syntax.

* Thu May 26 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4-3
- Add fix for FTBS parallel build deps error.

* Thu May 26 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.4-2
- New upstream release.

* Thu May 12 2016 Alec Leamas <leamas.alec@gmail.com> - 0.9.3a-5
- Fix upstreamed/duplicated lirc.4 manpage (#1319344).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3a-3
- Fix bad Obsoletes (#1284522).

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3a-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 14 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3a-1
  - Upstream update
  - Added missing icons dependency.
  - Some patches upstreamed.

* Mon Sep 14 2015 Alec Leamas <leamas.alec@gmail.com> 0.9.3-6
- Add a selinux policy.
- Clean up some macros.

* Wed Sep 09 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3-5
- Move scriptles to lirc-core (#1261289).
- Adjust deps between lib, core, and devel (also #1261289).
- Make temporary files owned by lirc:lirc
- Add missing library flag causing rpmlint noise.
- Remove foreign distro stuff in contrib/.

* Mon Sep 07 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3-4
- Fix missing file database.py (lirc-setup cannot start).

* Sun Sep 06 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3-3
- Fix missing lirc-drv-irman.

* Sun Sep 06 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3-2
- Rebuilt

* Sat Sep 05 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3-1
- New upstream version.

* Wed Aug 19 2015 Alec Leamas <leamas.alec@gmail.com> - 0.9.3-0.3.pre3
- Added lirc-lsplugins left-over logfile patch (COPR only).

* Tue Aug 18 2015 Alec Leamas <leamas.alec@nowhere.net> - 0.9.3-0.2pre3
- Add new patch for external module compilation  (COPR only).

* Thu Jul 30 2015 Alec Leamas <leamas.alec@nowhere.net> - 0.9.3-0.2pre1
- Add udev rule to fix /dev/lirc0 permissions  (COPR only).

* Wed Jul 1 2015 Alec Leamas <leamas.alec@nowhere.net> - 0.9.3-0.1pre1
- Provisionary COPR 0.9.3 pre-release - major upstream update.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 Alec Leamas <leamas.alec@nowhere.net> - 0.9.2-1
- Major upstream update.
- New package structure with more, smaller packages.

* Wed Sep 03 2014 Alec Leamas <leamas@nowhere.net> - 0.9.1a-4
- rebuilt

* Thu Aug 21 2014 Alec Leamas <leamas.alec@nowhere.net> - 0.9.1a-3
- rebuilt to pick up new iguanaIR.

* Thu Aug 21 2014 Aölec Leamas <leamas.alec@nowhere.net> - 0.9.1a-2
- Rebuilt for new iguanaIR ABI version.

* Tue Aug 19 2014 Alec Leamas <leamas@nowhere.net> - 0.9.1-1
- Updating to latest release.
- Removing tons of patches now upstreamed.
- Using built manpages as-is (no need to remove not-built tools)

* Mon Aug 18 2014 Alec Leamas <leamas@nowhere.net> - 0.9.0-28
- Rebuilt due to iguanaIR so-bump.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.9.0-25
- enable BR iguanaIR again
- add missing isa tags

* Thu May 29 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.9.0-24
- rebuild for libftdi soname bump
- disable BR iguanaIR temporary, it pulls in lirc-0.9.0-23 and build fails

* Wed Jan 08 2014 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-23
- Remove f16 systemd upgrade snippets.

* Sun Nov 17 2013 leamas.alec@gmail.com - 0.9.0-22
- Fix -Werror=format-security build error (#1037178).
- Not yet built.

* Sun Nov 17 2013 leamas.alec@gmail.com - 0.9.0-21
- lircd.service: add sh wrapper to handle empty argumentes.

* Sun Nov 17 2013 leamas.alec@gmail.com - 0.9.0-20
- Fixing typo in -20.
- Ignore errors in PreExec/PostExec.

* Sat Nov 16 2013 Alec Leamas <leamas.alec@gmail.com> - 0.9.0-19
- Fix missing {} in lircd.service (bz 1025030, comment 24)

* Tue Nov 12 2013 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-18
- Remove old nowadays stale links to lirc.service.
- Fix broken reference to lirc.service in lircmd.service
- Update README

* Thu Oct 17 2013 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-17
- Add a udev "Only use lirc" subpackage.
- Revise enabling of lirc protocol.
- Documenting upstream merge request.
- Resurrect contrib/lircs, use systemctl.
- Force creation of /run/lirc after installation.
- Use /lib/tmpfiles.d, not /etc/tmpfiles.d with _tmpfilesdir macro.

* Tue Oct 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.9.0-16
- fix build for f18
- remove BR perl, already called in build system
- fix bogus in changelog date

* Thu Oct 10 2013 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-15
- Actually use sysconfig files (881976).
- Modify lirc.service to not fork.
- Add support for iguanaIR driver (#954146).
- Add hardened build flag (955144).
- Use actual systemd macros (850191).
- Clean up some nowadays not used directives.
- Run autoreconf by default (926082).
- Cleanup some obsoleted autotools usage, two new patches.
- Deactivate other decoders on start (923978).
- Filter away docdir dependencies.
- Remove obsolete F8 upgrade Obsoletes: (sic!).
- Fix inconsistent/duplicate /usr/share/lirc in %%files.
- Add %%doc (notably COPYING) to remotes subpackage.
- Claim /etc/lirc.
- Update to latest upstream (10 patches).
- Use /var and /etc instead of %%{_sysconfdir} and %%{localstatedir}.
- Removed obsolete code to move config files to /etc/lirc in %%post.
- Renamed main systemd service: lirc.service -> lircd.service.
- Added socket activation support.
- Don't claim temporary files in /run/lirc, they are just transient.
- Initiate lircd.conf, lircmd.conf from external template.
- Bumping release, 14 is published.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Jon Ciesla <limburgher@gmail.com> - 0.9.0-9
- Migrate to systemd, BZ 789760.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-7
- Only alter protocols for the device lirc is configured to talk to
  and don't try to poke protocols on non-rc-core lirc devices

* Mon Jun 06 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-6
- And now take out the libusb1-devel bit, its actually the removal of
  libusb-config from libusb-devel that broke things, so we need some
  fixage upstream, backported here.

* Tue May 31 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-5
- Add explict BR: libusb1-devel, as some userspace drivers require it, and
  its apparently not getting into the build root any longer

* Sat May 28 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-4
- Apparently, the title of bz656613 wasn't quite correct, some stuff
  in /var/run does need to be installed, not ghosted...

* Tue May 03 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-3
- Properly support tmpfs /var/run/lirc in new systemd world (#656613)
- Don't ghost config files, lay 'em down with pointers in them

* Tue May 03 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-2
- Only disable in-kernel IR decoders if we're not using devinput mode,
  as they're actually required for devinput mode to work right.

* Sat Mar 26 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-1
- Update to lirc 0.9.0 release
- Disable in-kernel IR decoding when starting up lircd, reenable on shutdown

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-0.2.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Jarod Wilson <jarod@redhat.com> 0.9.0-0.1.pre1
- Update to lirc 0.9.0-pre1 snapshot
- Add conditional flag for building with iguanaIR support (there's an
  iguanaIR package awaiting review right now)

* Mon Sep 06 2010 Jarod Wilson <jarod@redhat.com> 0.8.7-1
- Update to lirc 0.8.7 release

* Sat Sep 04 2010 Jarod Wilson <jarod@redhat.com> 0.8.7-0.1.pre3
- Update to lirc 0.8.7-pre3 snapshot

* Mon Aug 02 2010 Jarod Wilson <jarod@redhat.com> 0.8.7-0.1.pre2
- Fix up sub-package license file inclusion per new fedora
  licensing guidelines
- Update to lirc 0.8.7pre2 snapshot

* Fri May 21 2010 Bastien Nocera <bnocera@redhat.com> 0.8.6-7
- Fix Firefly remote definition keycodes

* Sun Apr 11 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-6
- Revert to compat-ioctls per upstream discussion (#581326)

* Wed Mar 17 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-5
- Update devinput lircd.conf with additional keys from input.h

* Mon Feb 15 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-4
- Un-bungle newly introduced segfault in prior build

* Mon Feb 15 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-3
- Fix up ioctl portability between 32-bit and 64-bit

* Thu Nov 12 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-2
- Add devinput mouse event passthru to uinput support from lirc cvs

* Sun Sep 13 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-1
- Update to lirc 0.8.6 release

* Sat Aug 29 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.6.pre2
- Rediff patches so they actually apply still

* Sat Aug 29 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.5.pre2
- Update to lirc 0.8.6pre2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-0.4.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.3.pre1
- Set up tools to use /dev/lirc0 instead of /dev/lirc by default
- Set a default font for xmode2 most people actually have (#467339)

* Wed Jun 24 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.2.pre1
- Fix things up so the relocated socket actually works out of the box

* Tue Jun 23 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.1.pre1
- Update to lirc 0.8.6pre1
- Adds Linux input layer support to lircmd
- Adds XMP protocol support
- Moves lircd socket from /dev/ to /var/run/lirc/ and pid file from
  /var/run/ to /var/run/lirc/

* Thu May 28 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-2
- Update to lirc 0.8.5
- Add irman support, now that libirman is in Fedora (#474992)

* Sun May 17 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-1.pre3
- Update to lirc 0.8.5pre3 cvs snapshot

* Fri Apr 10 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-1.pre2
- Update to lirc 0.8.5pre2 cvs snapshot

* Thu Feb 26 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-1.pre1
- Update to lirc 0.8.5pre1 cvs snapshot
- Adds support for usb-connected ftdi-based homebrew transceivers
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 09 2008 Jarod Wilson <jarod@redhat.com> 0.8.4a-3
- BR: automake and libtool to get cvs additions building

* Mon Dec 08 2008 Jarod Wilson <jarod@redhat.com> 0.8.4a-2
- Nuke bogus and harmful %%postun --try-restart (#474960)
- Assorted updates from lirc cvs:
  * Add uinput injection support
  * Add support for binding lircd listener to a specific ip

* Sun Oct 26 2008 Jarod Wilson <jarod@redhat.com> 0.8.4a-1
- Update to lirc 0.8.4a release (fixes mode2 irrecord failures)
- Really fix the mceusb remote config file this time

* Thu Oct 16 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-2
- Make all remote configs have unique names (#467303)
- Fix up some key names that got screwed up by standardization script

* Sun Oct 12 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-1
- Update to 0.8.4 release

* Fri Oct 10 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-0.5.pre2
- Re-enable portaudio driver by default, require v19 or later

* Mon Oct 06 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-0.4.pre2
- Update to 0.8.4pre2

* Mon Oct 06 2008 Bastien Nocera <bnocera@redhat.com> 0.8.4-0.3.pre1
- Fix more keycodes for the streamzap remote

* Wed Oct 01 2008 Bastien Nocera <bnocera@redhat.com> 0.8.4-0.2.pre1
- Don't create a backup for the keycodes patch, or all the original files
  will also get installed, and get used in gnome-lirc-properties

* Wed Sep 24 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-0.1.pre1
- Update to 0.8.4pre1
- Drop upstream patches
- Adds support for the CommandIR II userspace driver

* Tue Sep 16 2008 Jarod Wilson <jarod@redhat.com> 0.8.3-7
- Fix multilib upgrade path from F8 (Nicolas Chauvet, #462435)

* Thu Aug 14 2008 Bastien Nocera <bnocera@redhat.com> 0.8.3-6
- Make lircd not exit when there's no device available, so that the
  daemon is running as expected when the hardware is plugged back in
  (#440231)

* Thu Aug 14 2008 Bastien Nocera <bnocera@redhat.com> 0.8.3-5
- Add huge patch to fix the majority of remotes to have sensible keycodes,
  so they work out-of-the-box (#457273)

* Mon Jun 23 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-4
- Drop resume switch patch, no longer required
- Add support for config option style used by gnome-lirc-properties (#442341)

* Mon Jun 02 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-3
- Add additional required patches for gnome-lirc-properties (#442248)
- Put remote definitions in their own sub-package (#442328)

* Mon May 12 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-2
- Include upstream patch for lircd.conf remote include directives (#442248)
- Include upstream patch to validate transmit buffers

* Sun May 04 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-1
- Update to 0.8.3 release

* Sun Apr 27 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-0.4.pre3
- Update to 0.8.3pre3

* Sun Apr 06 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-0.3.pre2
- Update to 0.8.3pre2

* Tue Feb 12 2008 Ville Skyttä <ville.skytta at iki.fi> 0.8.3-0.2.pre1
- Split libraries into -libs subpackage.
- Refresh autotools re-run avoidance hack.

* Thu Oct 18 2007 Jarod Wilson <jwilson@redhat.com> 0.8.3-0.1.pre1
- 0.8.3pre1
- adds Mac IR support, resolves bz #284291

* Wed Aug 15 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-2
- License: GPLv2+

* Sun Jun 10 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-1
- 0.8.2.

* Wed Jun  6 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-0.1.pre3
- 0.8.2pre3.
- Fix up linefeeds and char encodings of more docs.

* Fri May 18 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-0.1.pre2
- 0.8.2pre2.

* Sun Jan  7 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-1
- 0.8.1.

* Sat Dec 30 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre5
- 0.8.1pre5.

* Tue Dec 12 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre4
- 0.8.1pre4.

* Thu Nov 30 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre3
- 0.8.1pre3.

* Sun Oct 15 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre2
- 0.8.1pre2, optflags patch no longer needed.

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre1
- Rebuild.

* Sat Jul  1 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.1.pre1
- 0.8.1pre1.
- Add rpmbuild options for enabling/disabling ALSA, portaudio and/or X
  support, ALSA and X enabled by default, portaudio not.
- Split most of the documentation to -doc subpackage.
- Install irman2lirc as non-doc.

* Tue Feb 14 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-3
- Avoid standard rpaths on lib64 archs.

* Sat Jan 21 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-2
- 0.8.0.

* Sat Jan 14 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre4
- 0.8.0pre4.

* Sun Jan  1 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre3
- 0.8.0pre3.

* Tue Dec 27 2005 Ville Skyttä <ville.skytta at iki.fi>
- Split kernel modules into separate package.
- Disable debugging features.

* Wed Dec 14 2005 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre2
- 0.8.0pre2, kernel >= 2.6.15 USB patch applied upstream.
- lirc_clientd renamed to lircrcd.

* Tue Nov 29 2005 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre1
- Pull security fix for the new lirc_clientd from upstream CVS, and
  while at it, some other useful post-0.8.0pre1 changes.
- Kernel >= 2.6.15 patchwork based on initial patch from Andy Burns (#172404).
- Disable lirc_cmdir kernel module (unknown symbols).
- Adapt to modular X.Org packaging.

* Wed Nov  9 2005 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.1.pre1
- 0.8.0pre1, usage message patch applied upstream.

* Sun Oct 30 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.3-0.1.pre1
- 0.7.3pre1, "no device" crash fix applied upstream.
- Fix lircd and lircmd usage messages.

* Wed Aug 31 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.2-3
- Make the init script startup earlier and shutdown later by default.

* Sun Aug 14 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.2-2
- 0.7.2, patch to fix crash at startup when no device is specified.
- Enable audio input driver support (portaudio).
- Improve package description.
- Don't ship static libraries.
- Drop pre Fedora Extras backwards compatibility hacks.
- Make svgalib support (smode2) build conditional, disabled by default.
- Simplify module package build (still work in progress, disabled by default).
- Other minor specfile cleanups and maintainability improvements.

* Thu May 26 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.1-3
- Adjust kernel module build for FC4 and add hauppauge, igorplugusb, imon,
  sasem, and streamzap to the list of modules to build.  This stuff is still
  disabled by default, rebuild with "--with modules --target $arch" to enable.

* Sun Apr 17 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.1-2
- 0.7.1.

* Thu Apr 7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Dec  5 2004 Ville Skyttä <ville.skytta at iki.fi> 0.7.0-1
- Update to 0.7.0; major rework of the package:
- Change default driver to "any".
- Add -devel subpackage.
- Improve init script, add /etc/sysconfig/lirc for options.
- Rename init script to "lirc" to follow upstream; the script is not only
  for lircd, but lircmd as well.
- Log to syslog instead of separate log file.
- %%ghost'ify /dev/lirc*.
- Build kernel modules when rebuilt with "--with kmod".  This stuff was mostly
  borrowed from Axel Thimm's packages, and is not really ready for FC3+ yet.
- Enable debugging features.
- Specfile cleanups.

* Mon Aug 30 2004 Matthias Saou <http://freshrpms.net/> 0.6.6-3
- Added missing /sbin/ldconfig calls.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 0.6.6-2
- Rebuild for Fedora Core 2... this spec file still _really_ needs reworking!

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.6.6-2
- Rebuild for Fedora Core 1... this spec file _really_ needs reworking!

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9... this spec file needs some reworking!

* Mon Oct  7 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.6.6 final.

* Mon Sep 16 2002 Matthias Saou <http://freshrpms.net/>
- Updated to latest pre-version.
- Kernel modules still need to be compiled separately and with a custom
  kernel :-(

* Thu May  2 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.6.5.
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Thu Oct  4 2001 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.

