Summary:        A shared storage lock manager
Name:           sanlock
Version:        3.8.5
Release:        1%{?dist}
License:        GPLv2 AND GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pagure.io/sanlock/
Source0:        https://releases.pagure.org/sanlock/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libaio-devel
BuildRequires:  libblkid-devel
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  systemd-units

Requires:           %{name}-lib = %{version}-%{release}
Requires(post):     systemd-sysv
Requires(post):     systemd-units
Requires(postun):   systemd-units
Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd
Requires(preun):    systemd-units

%description
The sanlock daemon manages leases for applications on hosts using shared storage.

%prep
%autosetup

%build
%{set_build_flags}
# upstream does not require configure
# upstream does not support _smp_mflags
make -C wdmd
make -C src
make -C python PY_VERSION=3
make -C reset

%install
make -C src \
        install LIBDIR=%{_libdir} \
        DESTDIR=%{buildroot}
make -C wdmd \
        install LIBDIR=%{_libdir} \
        DESTDIR=%{buildroot}
make -C python \
        install LIBDIR=%{_libdir} \
        DESTDIR=%{buildroot} \
        PY_VERSION=3
make -C reset \
        install LIBDIR=%{_libdir} \
        DESTDIR=%{buildroot}


install -D -m 0644 init.d/sanlock.service.native %{buildroot}/%{_unitdir}/sanlock.service
install -D -m 0755 init.d/wdmd %{buildroot}%{_libdir}/systemd/systemd-wdmd
install -D -m 0644 init.d/wdmd.service.native %{buildroot}/%{_unitdir}/wdmd.service
install -D -m 0644 init.d/sanlk-resetd.service %{buildroot}/%{_unitdir}/sanlk-resetd.service

install -D -m 0644 src/logrotate.sanlock \
    %{buildroot}%{_sysconfdir}/logrotate.d/sanlock

install -D -m 0644 src/sanlock.conf \
    %{buildroot}%{_sysconfdir}/sanlock/sanlock.conf

install -D -m 0644 init.d/wdmd.sysconfig \
    %{buildroot}%{_sysconfdir}/sysconfig/wdmd

install -Dd -m 0755 %{buildroot}%{_sysconfdir}/wdmd.d
install -Dd -m 0775 %{buildroot}/%{_localstatedir}/run/sanlock
install -Dd -m 0775 %{buildroot}/%{_localstatedir}/run/sanlk-resetd

%pre
getent group sanlock > /dev/null || %{_sbindir}/groupadd \
    -g 179 sanlock
getent passwd sanlock > /dev/null || %{_sbindir}/useradd \
    -u 179 -c "sanlock" -s /sbin/nologin -r \
    -g 179 -d %{_var}/run/sanlock sanlock
%{_sbindir}/usermod -a -G disk sanlock

%post
%systemd_post wdmd.service sanlock.service

%preun
%systemd_preun wdmd.service sanlock.service

%postun
%systemd_postun wdmd.service sanlock.service

%package        lib
Summary:        A shared storage lock manager library

%description    lib
The %{name}-lib package contains the runtime libraries for sanlock,
a shared storage lock manager.
Hosts connected to a common SAN can use this to synchronize their
access to the shared disks.

%ldconfig_scriptlets lib

%package        -n python3-sanlock
%{?python_provide:%python_provide python3-sanlock}
Summary:        Python bindings for the sanlock library

Requires:       %{name}-lib = %{version}-%{release}

%description    -n python3-sanlock
The %{name}-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the sanlock library.

%package        devel
Summary:        Development files for %{name}

Requires:       %{name}-lib = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n     sanlk-reset
Summary:        Host reset daemon and client using sanlock

Requires:       sanlock = %{version}-%{release}
Requires:       sanlock-lib = %{version}-%{release}

%description -n sanlk-reset
The sanlk-reset package contains the reset daemon and client.
A cooperating host running the daemon can be reset by a host
running the client, so long as both maintain access to a
common sanlock lockspace.

%files
%license README.license
%doc init.d/sanlock
%doc init.d/sanlock.service
%doc init.d/wdmd.service
%{_libdir}/systemd/systemd-wdmd
%{_unitdir}/sanlock.service
%{_unitdir}/wdmd.service
%{_sbindir}/sanlock
%{_sbindir}/wdmd
%dir %{_sysconfdir}/wdmd.d
%dir %{_sysconfdir}/sanlock
%dir %attr(-,sanlock,sanlock) %{_localstatedir}/run/sanlock
%{_mandir}/man8/wdmd*
%{_mandir}/man8/sanlock*
%config(noreplace) %{_sysconfdir}/logrotate.d/sanlock
%config(noreplace) %{_sysconfdir}/sanlock/sanlock.conf
%config(noreplace) %{_sysconfdir}/sysconfig/wdmd

%files devel
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

%files lib
%{_libdir}/libsanlock.so.*
%{_libdir}/libsanlock_client.so.*
%{_libdir}/libwdmd.so.*

%files -n python3-sanlock
%{python3_sitearch}/sanlock_python-*.egg-info
%{python3_sitearch}/sanlock*.so

%files -n sanlk-reset
%{_sbindir}/sanlk-reset
%{_sbindir}/sanlk-resetd
%{_unitdir}/sanlk-resetd.service
%dir %attr(-,root,root) %{_localstatedir}/run/sanlk-resetd
%{_mandir}/man8/sanlk-reset*

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8.5-1
- Auto-upgrade to 3.8.5 - Azure Linux 3.0 - package upgrades

* Tue Dec 28 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 3.8.4-1
- Update to version 3.8.4.

* Mon Jul 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Added %%license macro.
- Switched to using the offical upstream sources and %%autosetup.
- License verified.

* Sat May 02 2020 Nir Soffer <nsoffer@redhat.com> - 3.8.1-1
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
