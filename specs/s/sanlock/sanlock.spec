# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           sanlock
Version:        3.9.5
Release: 6%{?dist}
Summary:        A shared storage lock manager
License:	GPL-2.0-only AND GPL-2.0-or-later AND LGPL-2.0-or-later
URL:            https://pagure.io/sanlock/
BuildRequires:  gcc
BuildRequires:  libaio-devel
BuildRequires:  libblkid-devel
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  systemd-units
BuildRequires:  python3-setuptools
Requires:       %{name}-lib = %{version}-%{release}
Requires(post): systemd-units
Requires(post): systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
Source0:        https://releases.pagure.org/sanlock/%{name}-%{version}.tar.gz

# Patch0: 0001-foo.patch

%description
The sanlock daemon manages leases for applications on hosts using shared storage.

%prep
%setup -q
# %patch0 -p1

%build
%set_build_flags
# upstream does not require configure
# upstream does not support _smp_mflags
CFLAGS=$RPM_OPT_FLAGS make -C wdmd
CFLAGS=$RPM_OPT_FLAGS make -C src
CFLAGS=$RPM_OPT_FLAGS make -C python PY_VERSION=3

%install
rm -rf $RPM_BUILD_ROOT
make -C src \
        install LIBDIR=%{_libdir} BINDIR=%{_sbindir} \
        DESTDIR=$RPM_BUILD_ROOT
make -C wdmd \
        install LIBDIR=%{_libdir} BINDIR=%{_sbindir} \
        DESTDIR=$RPM_BUILD_ROOT
make -C python \
        install LIBDIR=%{_libdir} BINDIR=%{_sbindir} \
        DESTDIR=$RPM_BUILD_ROOT \
        PY_VERSION=3


install -D -m 0644 init.d/sanlock.service.native $RPM_BUILD_ROOT/%{_unitdir}/sanlock.service
install -D -m 0755 init.d/systemd-wdmd $RPM_BUILD_ROOT/usr/lib/systemd/systemd-wdmd
install -D -m 0644 init.d/wdmd.service $RPM_BUILD_ROOT/%{_unitdir}/wdmd.service

install -p -D -m 0644 src/sanlock.sysusers $RPM_BUILD_ROOT/%{_sysusersdir}/sanlock.conf

install -D -m 0644 src/logrotate.sanlock \
    $RPM_BUILD_ROOT/etc/logrotate.d/sanlock

install -D -m 0644 src/sanlock.conf \
    $RPM_BUILD_ROOT/etc/sanlock/sanlock.conf

install -D -m 0644 init.d/wdmd.sysconfig \
    $RPM_BUILD_ROOT/etc/sysconfig/wdmd

install -Dd -m 0755 $RPM_BUILD_ROOT/etc/wdmd.d

%if 0%{?fedora} < 42
%pre
# As libvirt does, install a sysusers file, but also directly
# create the user and group to avoid rpm installation errors
# (sysusers rpm macros seem to be insufficient to avoid problems.)
getent group sanlock > /dev/null || /usr/sbin/groupadd \
    -g 179 sanlock
getent passwd sanlock > /dev/null || /usr/sbin/useradd \
    -u 179 -c "sanlock" -s /sbin/nologin -r \
    -g 179 -d /run/sanlock sanlock
/usr/sbin/usermod -a -G disk sanlock
%endif

%post
%systemd_post wdmd.service sanlock.service

%preun
%systemd_preun wdmd.service sanlock.service

%postun
%systemd_postun wdmd.service sanlock.service

%files
/usr/lib/systemd/systemd-wdmd
%{_unitdir}/sanlock.service
%{_unitdir}/wdmd.service
%{_sbindir}/sanlock
%{_sbindir}/wdmd
%dir %{_sysconfdir}/wdmd.d
%dir %{_sysconfdir}/sanlock
%{_mandir}/man8/wdmd*
%{_mandir}/man8/sanlock*
%config(noreplace) %{_sysconfdir}/logrotate.d/sanlock
%config(noreplace) %{_sysconfdir}/sanlock/sanlock.conf
%config(noreplace) %{_sysconfdir}/sysconfig/wdmd
%{_sysusersdir}/sanlock.conf

%package        lib
Summary:        A shared storage lock manager library

%description    lib
The %{name}-lib package contains the runtime libraries for sanlock,
a shared storage lock manager.
Hosts connected to a common SAN can use this to synchronize their
access to the shared disks.

%ldconfig_scriptlets lib

%files          lib
%{_libdir}/libsanlock.so.*
%{_libdir}/libsanlock_client.so.*
%{_libdir}/libwdmd.so.*

%package        -n python3-sanlock
%{?python_provide:%python_provide python3-sanlock}
Summary:        Python bindings for the sanlock library
Requires:       %{name}-lib = %{version}-%{release}

%description    -n python3-sanlock
The %{name}-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the sanlock library.

%files          -n python3-sanlock
%{python3_sitearch}/sanlock_python-*.egg-info
%{python3_sitearch}/sanlock*.so

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-lib = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files          devel
%{_libdir}/libwdmd.so
%{_includedir}/wdmd.h
%{_libdir}/libsanlock.so
%{_libdir}/libsanlock_client.so
%{_includedir}/sanlock.h
%{_includedir}/sanlock_rv.h
%{_includedir}/sanlock_admin.h
%{_includedir}/sanlock_resource.h
%{_includedir}/sanlock_direct.h
%{_libdir}/pkgconfig/libsanlock.pc
%{_libdir}/pkgconfig/libsanlock_client.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.9.5-4
- Rebuilt for Python 3.14

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.9.5-3
- Drop %%pre scriptlets to create users and groups

* Mon Jan 27 2025 David Teigland <teigland@redhat.com> - 3.9.5-2
- retry

* Mon Jan 27 2025 David Teigland <teigland@redhat.com> - 3.9.5-1
- new upstream release

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.9.4-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Fri Aug 09 2024 David Teigland <teigland@redhat.com> - 3.9.4-1
- new upstream release, adopt sysusers

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.9.3-3
- Rebuilt for the bin-sbin merge

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.9.3-2
- Rebuilt for Python 3.13

* Wed May 15 2024 David Teigland <teigland@redhat.com> - 3.9.3-1
- new upstream release

* Wed Apr 17 2024 David Teigland <teigland@redhat.com> - 3.9.2-2
- Fix build when %_bindir==%_sbindir

* Tue Apr 16 2024 David Teigland <teigland@redhat.com> - 3.9.2-1
- new upstream release

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 David Teigland <teigland@redhat.com> - 3.9.0-1
- rebase to new upstream release

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.8.5-3
- Rebuilt for Python 3.12

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 18 2022 David Teigland <teigland@redhat.com> - 3.8.5-1
- Update to sanlock-3.8.5

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.8.4-5
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.8.4-2
- Rebuilt for Python 3.10

* Thu Jun 03 2021 David Teigland <teigland@redhat.com> 3.8.4-1
- New upstream release

* Wed Feb 24 2021 David Teigland <teigland@redhat.com> 3.8.3-1
- New upstream release
- Drop sanlk-reset which is not used.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 08 2020 Nir Soffer <nsoffer@redhat.com> - 3.8.1-7
- Enable LTO

* Sun Aug 02 2020 Nir Soffer <nsoffer@redhat.com> - 3.8.1-6
- Removing extra linkeer args, hopefully fix python build

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 08 2020 Jeff Law <law@redhat.com> - 3.8.1-3
- Disable LTO

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.1-2
- Rebuilt for Python 3.9

* Sat May 2 2020 Nir Soffer <nsoffer@redhat.com> - 3.8.1-1
- Update to sanlock-3.8.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Nir Soffer <nsoffer@redhat.com> - 3.8.0-1
- Update to sanlock-3.8.0
- Convert spec to python 3

* Tue May 21 2019 Nir Soffer <nsoffer@redhat.com> - 3.7.3-1
- Update to sanlock-3.7.3
- Add missing BuildRequires and Requires

* Fri Apr 12 2019 Nir Soffer <nsoffer@redhat.com> - 3.7.1-2
- Cleanup up align and sector constants

* Mon Apr 8 2019 Nir Soffer <nsoffer@redhat.com> - 3.7.1-1
- Update to sanlock 3.7.1
- Fix read_resource_owners (414abfe)

* Wed Mar 20 2019 Nir Soffer <nsoffer@redhat.com> - 3.7.0-1
- remove unneeded with_systemd macro
- update to sanlock 3.7.0

* Sat Feb 2 2019 Nir Soffer <nsoffer@redhat.com> - 3.6.0-8
- fix build on Fedora rawhide

* Thu Jan 24 2019 David Teigland <teigland@redhat.com> - 3.6.0-7
- lockfile ownership

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 3.6.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Mar 14 2018 David Teigland <teigland@redhat.com> - 3.6.0-4
- change makefile flags

* Wed Mar 14 2018 David Teigland <teigland@redhat.com> - 3.6.0-3
- rebuild with set_build_flags

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 12 2017 David Teigland <teigland@redhat.com> - 3.6.0-1
- Update to sanlock-3.6.0, drop fence_sanlock

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.5.0-6
- Add Provides for the old name without %%_isa

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.5.0-5
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.5.0-4
- Python 2 binary package renamed to python2-sanlock
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 01 2017 David Teigland <teigland@redhat.com> - 3.5.0-1
- Update to sanlock-3.5.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun 10 2016 David Teigland <teigland@redhat.com> - 3.4.0-1
- Update to sanlock-3.4.0

* Tue Feb 23 2016 David Teigland <teigland@redhat.com> - 3.3.0-2
- remove exclusive arch

* Mon Feb 22 2016 David Teigland <teigland@redhat.com> - 3.3.0-1
- Update to sanlock-3.3.0

* Tue Dec 01 2015 David Teigland <teigland@redhat.com> - 3.2.4-2
- wdmd: prevent probe while watchdog is used

* Fri Jun 19 2015 David Teigland <teigland@redhat.com> - 3.2.4-1
- Update to sanlock-3.2.4

* Fri May 22 2015 David Teigland <teigland@redhat.com> - 3.2.3-2
- add pkgconfig files

* Wed May 20 2015 David Teigland <teigland@redhat.com> - 3.2.3-1
- Update to sanlock-3.2.3

* Thu Oct 30 2014 David Teigland <teigland@redhat.com> - 3.2.2-2
- checksum endian fix

* Mon Sep 29 2014 David Teigland <teigland@redhat.com> - 3.2.2-1
- Update to sanlock-3.2.2

* Thu Aug 21 2014 David Teigland <teigland@redhat.com> - 3.2.1-1
- Update to sanlock-3.2.1

* Mon Aug 18 2014 David Teigland <teigland@redhat.com> - 3.2.0-1
- Update to sanlock-3.2.0

* Wed Jan 29 2014 David Teigland <teigland@redhat.com> - 3.1.0-2
- version interface

* Tue Jan 07 2014 David Teigland <teigland@redhat.com> - 3.1.0-1
- Update to sanlock-3.1.0

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.0.1-3
- Mass rebuild 2013-12-27

* Thu Aug 01 2013 David Teigland <teigland@redhat.com> - 3.0.1-2
- use /usr/lib instead of /lib

* Wed Jul 31 2013 David Teigland <teigland@redhat.com> - 3.0.1-1
- Update to sanlock-3.0.1

* Wed Jul 24 2013 David Teigland <teigland@redhat.com> - 3.0.0-1
- Update to sanlock-3.0.0

