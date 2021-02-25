Summary:        DBus for systemd
Name:           dbus
Version:        1.13.6
Release:        6%{?dist}
License:        GPLv2+ OR AFL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://www.freedesktop.org/wiki/Software/dbus
Source0:        http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
BuildRequires:  expat-devel
BuildRequires:  systemd-devel
BuildRequires:  xz-devel
Requires:       expat
Requires:       systemd
Requires:       xz
Provides:       dbus-libs = %{version}-%{release}

%description
The dbus package contains dbus.

%package    devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Requires:       expat-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
./configure --prefix=%{_prefix}                 \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_var}             \
            --docdir=%{_docdir}/dbus-1.11.12  \
            --enable-libaudit=no --enable-selinux=no \
            --with-console-auth-dir=/run/console

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}%{_libdir}
#ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libdbus-1.so) %{buildroot}%{_libdir}/libdbus-1.so
#rm -f %{buildroot}%{_sharedstatedir}/dbus/machine-id
#ln -sv %{buildroot}%{_sysconfdir}/machine-id %{buildroot}%{_sharedstatedir}/dbus

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/dbus-1
%{_bindir}/*
%{_libdir}/libdbus-1.so.*
%{_libdir}/tmpfiles.d/dbus.conf
%exclude %{_libdir}/sysusers.d
%{_unitdir}/*
%{_libexecdir}/*
%{_docdir}/*
%{_datadir}/dbus-1

#%{_sharedstatedir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/xml/dbus-1
%{_libdir}/cmake/DBus1
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.13.6-6
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Nov 03 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.13.6-5
- Systemd supports merged /usr. Update with corresponding file locations and macros.

* Mon Nov 02 2020 Joe Schmitt <joschmit@microsoft.com> - 1.13.6-4
- Provide dbus-libs.

* Sat May 09 00:21:00 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.13.6-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.13.6-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 1.13.6-1
-   Update to 1.13.6

*   Fri Apr 21 2017 Bo Gan <ganb@vmware.com> 1.11.12-1
-   Update to 1.11.12

*   Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.8-8
-   Move all header files to devel subpackage.

*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.8.8-7
-   Change systemd dependency

*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.8.8-6
-   Modified %check

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.8-5
-   GA - Bump release of all rpms

*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.8-4
-   Created devel sub-package

*   Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 1.8.8-3
-   Remove debug files.

*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.8.8-2
-   Update according to UsrMove.

*   Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
-   Initial build. First version
