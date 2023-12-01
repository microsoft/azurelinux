%define _unpackaged_files_terminate_build 0
%define        with_boost     1
%define        with_crash     1
%define        with_docs      0
%define        with_grapher   0
%define        with_pie       1
%define        with_rpm       0
%define        with_sqlite    1
Summary:        Programmable system-wide instrumentation system
Name:           systemtap
Version:        4.5
Release:        3%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/System
URL:            https://sourceware.org/systemtap/
Source0:        https://sourceware.org/systemtap/ftp/releases/%{name}-%{version}.tar.gz
BuildRequires:  elfutils-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  glibc-devel
BuildRequires:  libgcc
BuildRequires:  libstdc++-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libxml2-devel
BuildRequires:  nspr-devel
BuildRequires:  nss
BuildRequires:  nss-devel
BuildRequires:  perl
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  shadow-utils
BuildRequires:  sqlite-devel
%if %with_boost
BuildRequires:  boost-devel
%endif
%if %{with_crash}
BuildRequires:  crash-devel
BuildRequires:  zlib-devel
Requires:       crash
%endif
%if %{with_rpm}
BuildRequires:  rpm-devel
%endif
Requires:       elfutils
Requires:       gcc
Requires:       kernel-devel
Requires:       make
Requires:       %{name}-runtime = %{version}-%{release}
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system.  The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.

%package initscript
Summary:        Systemtap Initscript
Group:          System/Tools
Requires:       %{name}-runtime = %{version}-%{release}
Requires:       initscripts

%description initscript
Initscript for Systemtap scripts.

%package python
Summary:        Python interface for systemtap
Group:          System/Tools
Requires:       python3

%description python
This packages has the python interface to systemtap

%package runtime
Summary:        Instrumentation System Runtime
Group:          System/Tools
Requires:       kernel-devel

%description runtime
SystemTap runtime is the runtime component of an instrumentation system for systems running Linux.

%package sdt-devel
Summary:        Static probe support tools
Group:          System/Tools
Requires:       %{name} = %{version}-%{release}

%description sdt-devel
Support tools to allow applications to use static probes.

%package server
Summary:        Instrumentation System Server
Group:          System/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-runtime = %{version}-%{release}
Requires:       coreutils
Requires:       gzip
Requires:       nss
Requires:       unzip

%description server
SystemTap server is the server component of an instrumentation system for systems running Linux.

%prep
%setup -q
sed -i "s#"kernel"#"linux"#g" stap-prep
sed -i "s#"devel"#"dev"#g" stap-prep

%build
%configure \
%if %{with_crash}
	--enable-crash \
%else
	--disable-crash \
%endif
	--disable-docs \
%if %{with_sqlite}
	--enable-sqlite \
%else
	--disable-sqlite \
%endif
%if %{with_rpm}
	--with-rpm \
%else
	--without-rpm \
%endif
%if %{with_pie}
	--enable-pie \
%else
	--disable-pie \
%endif
	--disable-grapher \
    --disable-virt \
	--without-python2-probes \
	--with-python3 \
	--disable-silent-rules

make

%install
[ %{buildroot} != / ] && rm -rf ""
%makeinstall

mv %{buildroot}%{_datadir}/systemtap/examples examples

find examples -type f -name '*.stp' -print0 | xargs -0 sed -i -r -e '1s@^#!.+stap@#!%{_bindir}/stap@'

chmod 755 %{buildroot}%{_bindir}/staprun

install -c -m 755 stap-prep %{buildroot}%{_bindir}/stap-prep

mkdir -p %{buildroot}%{_sysconfdir}//rc.d/init.d/
install -m 755 initscript/systemtap %{buildroot}%{_sysconfdir}/rc.d/init.d/
mkdir -p %{buildroot}%{_sysconfdir}/systemtap
mkdir -p %{buildroot}%{_sysconfdir}/systemtap/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/systemtap/script.d
install -m 644 initscript/config.systemtap %{buildroot}%{_sysconfdir}/systemtap/config
mkdir -p %{buildroot}%{_localstatedir}/cache/systemtap
mkdir -p %{buildroot}%{_localstatedir}/run/systemtap

%if %{with_docs}
mkdir docs.installed
mv %{buildroot}%{_datadir}/systemtap/*.pdf docs.installed/
mv %{buildroot}%{_datadir}/systemtap/tapsets docs.installed/
%if %{with_publican}
mv %{buildroot}%{_datadir}/systemtap/SystemTap_Beginners_Guide docs.installed/
%endif
%endif

install -m 755 initscript/stap-server %{buildroot}%{_sysconfdir}/rc.d/init.d/
mkdir -p %{buildroot}%{_sysconfdir}/stap-server
mkdir -p %{buildroot}%{_sysconfdir}/stap-server/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 initscript/config.stap-server %{buildroot}%{_sysconfdir}/sysconfig/stap-server
mkdir -p %{buildroot}%{_localstatedir}/log/stap-server
touch %{buildroot}%{_localstatedir}/log/stap-server/log
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 initscript/logrotate.stap-server %{buildroot}%{_sysconfdir}/logrotate.d/stap-server

%find_lang %{name}

%check
make %{?_smp_mflags} check

%pre
getent group stap-server >/dev/null || groupadd -g 155 -r stap-server || groupadd -r stap-server

%pre runtime
getent group stapdev >/dev/null || groupadd -r stapdev
getent group stapusr >/dev/null || groupadd -r stapusr
exit 0

%pre server
getent passwd stap-server >/dev/null || \
%{_sbindir}/useradd -c "Systemtap Compile Server" -u 155 -g stap-server -d %{_localstatedir}/lib/stap-server -m -r -s /sbin/nologin stap-server || \
%{_sbindir}/useradd -c "Systemtap Compile Server" -g stap-server -d %{_localstatedir}/lib/stap-server -m -r -s /sbin/nologin stap-server
test -e ~stap-server && chmod 755 ~stap-server
exit 0

%post server
if [ $1 -eq 1 ] ; then
  test -e %{_localstatedir}/log/stap-server/log || {
  touch %{_localstatedir}/log/stap-server/log
  chmod 664 %{_localstatedir}/log/stap-server/log
  chown stap-server:stap-server %{_localstatedir}/log/stap-server/log
  }

  if test ! -e ~stap-server/.systemtap/ssl/server/stap.cert; then
	runuser -s /bin/sh - stap-server -c %{_libexecdir}/%{name}/stap-gen-cert >/dev/null

	%{_bindir}/stap-authorize-server-cert ~stap-server/.systemtap/ssl/server/stap.cert
	%{_bindir}/stap-authorize-signing-cert ~stap-server/.systemtap/ssl/server/stap.cert
  fi
  /sbin/chkconfig --add stap-server
  exit 0
fi

%preun server
if [ $1 = 0 ] ; then
	/sbin/service stap-server stop >/dev/null 2>&1
	/sbin/chkconfig --del stap-server
fi
exit 0

%postun server
if [ "$1" -ge "1" ] ; then
	/sbin/service stap-server condrestart >/dev/null 2>&1 || :
fi
exit 0

%post initscript
if [ $1 -eq 1 ] ; then
	/sbin/chkconfig --add systemtap
	exit 0
fi

%preun initscript
if [ $1 = 0 ] ; then
	/sbin/service systemtap stop >/dev/null 2>&1
	/sbin/chkconfig --del systemtap
fi
exit 0

%postun initscript
if [ "$1" -ge "1" ] ; then
	/sbin/service systemtap condrestart >/dev/null 2>&1 || :
fi
exit 0

%post
if [ $1 -eq 1 ] ; then
	(make -C %{_datadir}/systemtap/runtime/linux/uprobes clean) >/dev/null 3>&1 || true
	(/sbin/rmmod uprobes) >/dev/null 2>&1 || true
fi

%preun
if [ $1 -eq 0 ] ; then
	(make -C %{_datadir}/systemtap/runtime/linux/uprobes clean) >/dev/null 3>&1 || true
	(/sbin/rmmod uprobes) >/dev/null 2>&1 || true
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS
%license COPYING
%{_bindir}/stap
%{_bindir}/stap-merge
%{_bindir}/stap-prep
%{_bindir}/stap-report
%{_bindir}/stapsh
%{_bindir}/stapbpf
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/runtime
%{_datadir}/systemtap/runtime/*.h
%{_datadir}/systemtap/runtime/*.c
%{_datadir}/systemtap/runtime/transport
%{_datadir}/systemtap/runtime/unwind
%dir %{_datadir}/systemtap/runtime/linux
%{_datadir}/systemtap/runtime/linux/*.c
%{_datadir}/systemtap/runtime/linux/*.h
%dir %attr(0775,root,stap-server) %{_datadir}/systemtap/runtime/linux/uprobes
%{_datadir}/systemtap/runtime/linux/uprobes/*
%dir %{_datadir}/systemtap/runtime/linux/uprobes2
%{_datadir}/systemtap/runtime/linux/uprobes2/*
%{_datadir}/systemtap/runtime/softfloat/*.h
%{_datadir}/systemtap/tapset
%{_mandir}/man1
%{_mandir}/man3/stap*.3stap*
%{_mandir}/man7/warning::buildid.7stap.gz
%{_mandir}/man7/warning::symbols.7stap*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man8/stapsh.8*
%{_mandir}/man8/systemtap.8*
%{_mandir}/man8/stapbpf.8*
%{_bindir}/dtrace

%files initscript
%defattr(-,root,root)
%{_sysconfdir}/rc.d/init.d/systemtap
%dir %{_sysconfdir}/systemtap
%dir %{_sysconfdir}/systemtap/conf.d
%dir %{_sysconfdir}/systemtap/script.d
%config(noreplace) %{_sysconfdir}/systemtap/config
%dir %{_localstatedir}/cache/systemtap
%dir %{_localstatedir}/run/systemtap

%files python
%defattr(-,root,root)
%{python3_sitelib}/*

%files runtime
%defattr(-,root,root)
%attr(4111,root,root) %{_bindir}/staprun
%{_libexecdir}/systemtap/stap-env
%{_libexecdir}/systemtap/stap-authorize-cert
%if %{with_crash}
%{_libdir}/systemtap/staplog.so*
%endif
%{_mandir}/man8/staprun.8*

%files sdt-devel
%defattr(-,root,root)
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%doc NEWS examples

%files server
%defattr(-,root,root)
%{_bindir}/stap-server
%{_libexecdir}/systemtap/stap-serverd
%{_libexecdir}/systemtap/stap-start-server
%{_libexecdir}/systemtap/stap-stop-server
%{_libexecdir}/systemtap/stap-gen-cert
%{_libexecdir}/systemtap/stap-sign-module
%{_sysconfdir}/rc.d/init.d/stap-server
%config(noreplace) %{_sysconfdir}/logrotate.d/stap-server
%dir %{_sysconfdir}/stap-server
%dir %{_sysconfdir}/stap-server/conf.d
%config(noreplace) %{_sysconfdir}/sysconfig/stap-server
%dir %attr(0755,stap-server,stap-server) %{_localstatedir}/log/stap-server
%ghost %config(noreplace) %attr(0644,stap-server,stap-server) %{_localstatedir}/log/stap-server/log
%{_mandir}/man7/error::*.7stap*
%{_mandir}/man7/warning::debuginfo.7stap*
%{_mandir}/man8/stap-server.8*
%{_mandir}/man8/systemtap-service.8*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.5-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Oct 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.5-2
- Fixing default log location.

* Fri Jan 14 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 4.5-1
- Update to version 4.5.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1-9
- Removing the explicit %%clean stage.

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.1-8
- Don't hardcode python site-packages directory (enables Python 3.9 build)

* Wed Oct 27 2021 Muhammad Falak <mwani@microsft.com> - 4.1-7
- Remove epoch

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> 4.1-6
- Explicitly use python3 during build.
- Use lib macros for paths.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.1-5
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 4.1-4
- Renaming linux to kernel

* Fri Apr 17 2020 Emre Girgin <mrgirgin@microsoft.com> 4.1-3
- Rename shadow to shadow-utils.

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> 4.1-2
- Remove toybox and only use coreutils for requires.

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 4.1-1
- Update to 4.1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 4.0-2
- Added BuildRequires python2-devel

* Tue Dec 04 2018 Keerthana K <keerthanak@vmware.com> 4.0-1
- Updated to version 4.0

* Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 3.3-1
- Updated to version 3.3

* Tue Jan 23 2018 Divya Thaluru <dthaluru@vmware.com>  3.2-1
- Updated to version 3.2

* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  3.1-5
- Fixed the log file directory structure

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1-4
- Remove shadow from requires and use explicit tools for post actions

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1-3
- Requires coreutils or toybox

* Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1-2
- systemtap-sdt-devel requires systemtap

* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.1-1
- Update to version 3.1

* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-4
- add shadow to requires

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.0-3
- Use sqlite-{devel,libs}

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.0-2
- Modified %check

* Fri Jul 22 2016 Divya Thaluru <dthaluru@vmware.com> 3.0-1
- Updated version to 3.0
- Removing patch to enable kernel (fix is present in upstream)

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-5
- GA - Bump release of all rpms

* Mon May 23 2016 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.9-4
- Added the patch to enable kernel building with Kernel 4.4

* Fri May 20 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9-3
- Fixed the stap-prep script to be compatible with Photon

* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-2
- Fix for upgrade issues

* Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9-1
- Updated version to 2.9

* Fri Dec 11 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7-2
- Move dtrace to the main package.

* Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 2.7-1
- Initial build. First version
