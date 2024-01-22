Summary:           A toolkit for defining and handling authorizations.
Name:              polkit
Version:           123
Release:           1%{?dist}
Group:             Applications/System
Vendor:            Microsoft Corporation
License:           GPLv2+
URL:               https://gitlab.freedesktop.org/polkit/polkit
Source0:           https://gitlab.freedesktop.org/polkit/polkit/-/archive/%{version}/polkit-%{version}.tar.gz
Distribution:      Mariner
BuildRequires:     duktape-devel
BuildRequires:     expat-devel
BuildRequires:     glib-devel
BuildRequires:     gobject-introspection-devel
BuildRequires:     intltool >= 0.40.0
BuildRequires:     meson
BuildRequires:     pam-devel
BuildRequires:     systemd-devel
Requires:          duktape
Requires:          expat
Requires:          glib
Requires:          pam
Requires:          systemd
Requires(pre):     /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):  /usr/sbin/userdel /usr/sbin/groupdel

%description
polkit provides an authorization API intended to be used by privileged programs
(“MECHANISMS”) offering service to unprivileged programs (“SUBJECTS”) often
through some form of inter-process communication mechanism

%package           devel
Summary:           polkit development headers and libraries
Group:             Development/Libraries
Requires:          polkit = %{version}-%{release}

%description       devel
header files and libraries for polkit

%prep
%autosetup -p1

%build
%meson \
    -D man=false \
    -D examples=false \
    -D js_engine=duktape \
    -D session_tracking=libsystemd-login
%meson_build

%install
%meson_install
find %{buildroot} -name '*.la' -delete
install -vdm 755 %{buildroot}/etc/pam.d
cat > %{buildroot}/etc/pam.d/polkit-1 << "EOF"
# Begin /etc/pam.d/polkit-1

auth     include        system-auth
account  include        system-account
password include        system-password
session  include        system-session

# End /etc/pam.d/polkit-1
EOF

%find_lang polkit-1

%check
# Disable check. It requires dbus - not available in chroot/container.

%pre
getent group polkitd > /dev/null || groupadd -fg 27 polkitd &&
getent passwd polkitd > /dev/null || \
    useradd -c "PolicyKit Daemon Owner" -d /etc/polkit-1 -u 27 \
        -g polkitd -s /bin/false polkitd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    systemctl stop polkit
    if getent passwd polkitd >/dev/null; then
        userdel polkitd
    fi
    if getent group polkitd >/dev/null; then
        groupdel polkitd
    fi
fi

%files -f polkit-1.lang
%defattr(-,root,root)
%{_bindir}/pk*
%{_libdir}/lib%{name}-*.so.*
%dir %{_libdir}/polkit-1
%{_libdir}/polkit-1/polkit-agent-helper-1
%{_libdir}/polkit-1/polkitd
%{_libdir}/systemd/system/polkit.service
%{_datadir}/dbus-1/system-services/*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%attr(0750,root,polkitd) %dir %{_datadir}/polkit-1/rules.d
%{_datadir}/polkit-1/policyconfig-1.dtd
%dir %{_sysconfdir}/polkit-1
%attr(0750,root,polkitd) %dir %{_sysconfdir}/polkit-1/rules.d
%{_sysconfdir}/pam.d/polkit-1
%{_datadir}/polkit-1/rules.d/50-default.rules
%{_libdir}/girepository-1.0/Polkit-1.0.typelib
%{_libdir}/girepository-1.0/PolkitAgent-1.0.typelib

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_includedir}/*
%{_datadir}/gettext/its/polkit.its
%{_datadir}/gettext/its/polkit.loc


%changelog
* Tue Jan 02 2024 Reuben Olinsky <reubeno@microsoft.com> - 123-1
- Upgrade to polkit v123
- Switch JS engine to duktape.

* Thu Mar 17 2022 Andrew Phelps <anphel@microsoft.com> - 0.119-3
- Disable documentation

* Mon Feb 07 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.119-2
- Patch for CVE-2021-4034.

* Wed Nov 03 2021 Jon Slobodzian <joslobo@microsoft.com> - 0.119-1
- Bump to polkit 0.119.
- Switching a BR to CBL-Mariner's "mozjs" from "mozjs[version]".
- Disabling tests due to their dependency on "dbus".

* Thu Jun 03 2021 Andrew Phelps <anphel@microsoft.com> - 0.116-5
- Enable check tests (with exception of unsupported "polkitbackend" tests)

* Thu Jun 03 2021 Jon Slobodzian <josloboe@microsoft.com> - 0.116-4
- Patch for CVE 2021-3560.  Fix changelog formatting.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.116-3
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 0.116-2
- Renaming Linux-PAM to pam

* Thu Apr 16 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.116-1
- Update to version 0.116.
- License verified.
- Use mozjs60 instead of js for requires and BR.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.113-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 10 2019 Dweep Advani <dadvani@vmware.com> 0.113-4
- Fix for CVE-2018-19788

* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 0.113-3
- Added pre and postun requires for shadow tools

* Thu Oct 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.113-2
- Enable PAM and systemd.

* Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.113-1
- Upgrade to 0.113-1

* Fri May 22 2015 Alexey Makhalov <amakhalov@vmware.com> 0.112-1
- initial version
