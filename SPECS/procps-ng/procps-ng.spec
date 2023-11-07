Summary:        Programs for monitoring processes
Name:           procps-ng
Version:        4.0.4
Release:        1%{?dist}
License:        GPLv2 AND LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://gitlab.com/procps-ng/procps
Source0:        https://sourceforge.net/projects/procps-ng/files/Production/%{name}-%{version}.tar.xz
BuildRequires:  ncurses-devel
Requires:       ncurses
Conflicts:      toybox
Provides:       /bin/ps
Provides:       procps = %{version}-%{release}

%description
The Procps package contains programs for monitoring processes.

%package    devel
Summary:        Header and development files for procps-ng
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%package lang
Summary:        Additional language files for procps-ng
Group:          Applications/Databases
Requires:       %{name} = %{version}-%{release}

%description lang
These are the additional language files of procps-ng

%prep
%setup -q -n %{name}-%{version}

%build
./configure \
    --prefix=%{_prefix} \
    --exec-prefix= \
    --libdir=%{_libdir} \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-static \
    --disable-kill \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
install -vdm 755 %{buildroot}/%{_libdir}
install -vdm 755 %{buildroot}/%{_sbindir}
ln -s %{_bindir}/pidof %{buildroot}%{_sbindir}/pidof
find %{buildroot} -type f -name "*.la" -delete -print
%find_lang %{name} --all-name --with-man

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
/bin/ps
/bin/pidwait
/bin/pidof
/bin/free
/bin/w
/bin/pgrep
/bin/uptime
/bin/vmstat
/bin/pmap
/bin/tload
/bin/pwdx
/bin/top
/bin/slabtop
/bin/watch
/bin/pkill
%{_sbindir}/pidof
%{_datadir}/locale/*
%{_docdir}/procps-ng-*/*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/libproc2.so.*
/sbin/sysctl

%files devel
%{_includedir}/libproc2/diskstats.h
%{_includedir}/libproc2/meminfo.h
%{_includedir}/libproc2/misc.h
%{_includedir}/libproc2/pids.h
%{_includedir}/libproc2/slabinfo.h
%{_includedir}/libproc2/stat.h
%{_includedir}/libproc2/vmstat.h
%{_includedir}/libproc2/xtra-procps-debug.h
%{_libdir}/pkgconfig/libproc2.pc
%{_libdir}/libproc2.so
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.0.4-1
- Auto-upgrade to 4.0.4 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.3.17-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Dec 07 2021 Chris Co <chrco@microsoft.com> - 3.3.17-1
- Update to 3.3.17
- License verified

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 3.3.15-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 3.3.15-4
- Provide procps and /bin/ps

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.3.15-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.3.15-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Aug 10 2018 Tapas Kundu <tkundu@vmware.com> 3.3.15-1
- Upgrade version to 3.3.15.
- Fix for CVE-2018-1122 CVE-2018-1123 CVE-2018-1124 CVE-2018-1125
- Fix for CVE-2018-1126

* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 3.3.12-3
- Added conflicts toybox

* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 3.3.12-2
- Add lang package.

* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 3.3.12-1
- Upgrade to 3.3.12

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.11-5
- Moved man3 to devel subpackage.

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.3.11-4
- Modified %check

* Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.11-3
- Added patch to interpret ASCII sequence correctly

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.11-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 3.3.11-1
- Upgrade version

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.3.9-2
- Update according to UsrMove.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3.9-1
- Initial build. First version
