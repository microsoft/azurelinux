Summary: SELinux Translation Daemon
Name: mcstrans
Version: 2.9
Release: 2%{?dist}
License: GPL+
Url: https://github.com/SELinuxProject/selinux/wiki
Source: https://github.com/SELinuxProject/selinux/releases/download/20190315/mcstrans-2.9.tar.gz
Source2: secolor.conf.8
BuildRequires: gcc
BuildRequires: libselinux-devel >= %{version}
BuildRequires: libcap-devel pcre-devel libsepol-devel
BuildRequires: systemd
Requires: pcre
%{?systemd_requires}
Provides: setransd
Provides: libsetrans
Obsoletes: libsetrans

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

mcstrans provides an translation daemon to translate SELinux categories
from internal representations to user defined representation.

%prep
%autosetup -p 1 -n mcstrans-%{version}

%build
%set_build_flags

make LIBDIR="%{_libdir}" %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}%{_usr}/share/mcstrans
mkdir -p %{buildroot}%{_sysconfdir}/selinux/mls/setrans.d

make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" SBINDIR="%{_sbindir}" SYSTEMDDIR="/lib/systemd" install
rm -f %{buildroot}%{_libdir}/*.a
cp -r share/* %{buildroot}%{_usr}/share/mcstrans/
# Systemd
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/mcstrans
install -m644 %{SOURCE2} %{buildroot}%{_mandir}/man8/

%post
%systemd_post mcstrans.service

%preun
%systemd_preun mcstrans.service

%postun
%systemd_postun mcstrans.service

%files
%{_mandir}/man8/mcs.8.gz
%{_mandir}/man8/mcstransd.8.gz
%{_mandir}/man8/setrans.conf.8.gz
%{_mandir}/ru/man8/mcs.8.gz
%{_mandir}/ru/man8/mcstransd.8.gz
%{_mandir}/ru/man8/setrans.conf.8.gz
%{_mandir}/man8/secolor.conf.8.gz
/usr/sbin/mcstransd
%{_unitdir}/mcstrans.service
%dir %{_sysconfdir}/selinux/mls/setrans.d

%dir %{_usr}/share/mcstrans

%defattr(0644,root,root,0755)
%dir %{_usr}/share/mcstrans/util
%dir %{_usr}/share/mcstrans/examples
%{_usr}/share/mcstrans/examples/*

%defattr(0755,root,root,0755)
%{_usr}/share/mcstrans/util/*

%changelog
* Thu Aug 27 2020 Daniel Burgener <daburgen@microsoft.com> - 2.9-2
- Initial import from Fedora 31
