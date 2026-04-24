# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# work around flakey gcc warnings
%{!?with_Werror: %global with_Werror 0}
%{!?with_sqlite: %global with_sqlite 0%{?fedora} >= 17 || 0%{?rhel} >= 7}
# prefer prebuilt docs
%{!?with_docs: %global with_docs 0}
%{!?with_htmldocs: %global with_htmldocs 0}
%{!?with_monitor: %global with_monitor 1}
# crash is not available
%ifarch ppc ppc64 %{sparc} %{mips} %{riscv}
%{!?with_crash: %global with_crash 0}
%else
%{!?with_crash: %global with_crash 1}
%endif
%{!?with_rpm: %global with_rpm 1}
%{!?elfutils_version: %global elfutils_version 0.179}
%{!?with_boost: %global with_boost 1}
%ifarch x86_64 ppc ppc64 ppc64le aarch64
%{!?with_dyninst: %global with_dyninst 0%{?fedora} >= 18 || 0%{?rhel} >= 7}
%else
%{!?with_dyninst: %global with_dyninst 0}
%endif
%{!?with_bpf: %global with_bpf 0%{?fedora} >= 22 || 0%{?rhel} >= 8}
%{!?with_systemd: %global with_systemd 0%{?fedora} >= 19 || 0%{?rhel} >= 7}
%{!?with_emacsvim: %global with_emacsvim 0%{?fedora} >= 19 || 0%{?rhel} >= 7}
%ifarch %{ix86}
%{!?with_java: %global with_java 0}
%else
%{!?with_java: %global with_java 0%{?fedora} >= 19 || 0%{?rhel} >= 7}
%endif
%{!?with_debuginfod: %global with_debuginfod 0%{?fedora} >= 25 || 0%{?rhel} >= 7}
%{!?with_virthost: %global with_virthost 0%{?fedora} >= 19 || 0%{?rhel} >= 7}
%{!?with_virtguest: %global with_virtguest 1}
%{!?with_dracut: %global with_dracut 0%{?fedora} >= 19 || 0%{?rhel} >= 6}
%ifarch x86_64
%{!?with_mokutil: %global with_mokutil 0%{?fedora} >= 18 || 0%{?rhel} >= 7}
%{!?with_openssl: %global with_openssl 0%{?fedora} >= 18 || 0%{?rhel} >= 7}
%else
%{!?with_mokutil: %global with_mokutil 0}
%{!?with_openssl: %global with_openssl 0}
%endif
%{!?with_pyparsing: %global with_pyparsing 0%{?fedora} >= 18 || 0%{?rhel} >= 7}
%{!?with_python3: %global with_python3 0%{?fedora} >= 23 || 0%{?rhel} > 7}
%{!?with_python2_probes: %global with_python2_probes (0%{?fedora} <= 28 && 0%{?rhel} <= 7)}
%{!?with_python3_probes: %global with_python3_probes (0%{?fedora} >= 23 || 0%{?rhel} > 7)}
%{!?with_httpd: %global with_httpd 0}
%{!?with_specific_python: %global with_specific_python 0%{?fedora} >= 31}
%{!?with_sysusers: %global with_sysusers 0%{?fedora} >= 32 || 0%{?rhel} >= 9}
# NB: can't turn this on by default on any distro version whose builder system
# may run kernels different than the distro version itself.
%{!?with_check: %global with_check 0}


# Virt is supported on these arches, even on el7, but it's not in core EL7
%if 0%{?rhel} && 0%{?rhel} <= 7
%ifarch ppc64le aarch64
%global with_virthost 0
%endif
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 6
   %define initdir %{_initddir}
%else
   # RHEL5 doesn't know _initddir
   %define initdir %{_initrddir}
%endif

%if %{with_virtguest}
   %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
      %define udevrulesdir /usr/lib/udev/rules.d
   %else
      %if 0%{?rhel} >= 6
         %define udevrulesdir /lib/udev/rules.d
      %endif
   %endif
%endif

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
   %define dracutstap %{_prefix}/lib/dracut/modules.d/99stap
%else
   %define dracutstap %{_prefix}/share/dracut/modules.d/99stap
%endif

%if 0%{?rhel} == 6 || 0%{?rhel} == 7
    %define dracutbindir /sbin
%else
    %define dracutbindir %{_bindir}
%endif

%{!?_rpmmacrodir: %define _rpmmacrodir %{_rpmconfigdir}/macros.d}

# To avoid testsuite/*/*.stp has shebang which doesn't start with '/'
%define __brp_mangle_shebangs_exclude_from .stp$

%define _systemtap_runtime_preinstall \
# See systemd-sysusers(8) sysusers.d(5)\
\
g     stapusr  156\
g     stapsys  157\
g     stapdev  158\
g     stapunpriv 159\
u     stapunpriv 159      "systemtap unprivileged user"   /var/lib/stapunpriv   /sbin/nologin\
m     stapunpriv stapunpriv

%define _systemtap_server_preinstall \
# See systemd-sysusers(8) sysusers.d(5)\
\
g     stap-server  -\
u     stap-server  -      "systemtap compiler server"   /var/lib/stap-server   /sbin/nologin\
m     stap-server stap-server


%define _systemtap_testsuite_preinstall \
# See systemd-sysusers(8) sysusers.d(5)\
\
u     stapusr  -          "systemtap testsuite user"    /   /sbin/nologin\
u     stapsys  -          "systemtap testsuite user"    /   /sbin/nologin\
u     stapdev  -          "systemtap testsuite user"    /   /sbin/nologin\
m     stapusr  stapusr\
m     stapsys  stapusr\
m     stapsys  stapsys\
m     stapdev  stapusr\
m     stapdev  stapdev

%define _systemtap_server_preinstall_tmpfiles \
# See systemd-tmpfiles(8) tmpfiles.d(5)\
d /var/lib/stap-server 0750 stap-server stap-server -\
d /var/lib/stap-server/.systemtap 0700 stap-server stap-server -\
d /var/log/stap-server 0755 stap-server stap-server -\
f /var/log/stap-server/log 0644 stap-server stap-server -

Name: systemtap
# PRERELEASE
Version: 5.4
Release: 2%{?release_override}%{?dist}
# for version, see also configure.ac


# Packaging abstract:
#
# systemtap              empty req:-client req:-devel
# systemtap-server       /usr/bin/stap-server*, req:-devel
# systemtap-devel        /usr/bin/stap, runtime, tapset, req:kernel-devel
# systemtap-runtime      /usr/bin/staprun, /usr/bin/stapsh, /usr/bin/stapdyn
# systemtap-client       /usr/bin/stap, samples, docs, tapset(bonus), req:-runtime
# systemtap-initscript   /etc/init.d/systemtap, dracut module, req:systemtap
# systemtap-sdt-devel    /usr/include/sys/sdt.h
# systemtap-sdt-dtrace   /usr/bin/dtrace
# systemtap-testsuite    /usr/share/systemtap/testsuite*, req:systemtap, req:sdt-devel
# systemtap-runtime-java libHelperSDT.so, HelperSDT.jar, stapbm, req:-runtime
# systemtap-runtime-virthost  /usr/bin/stapvirt, req:libvirt req:libxml2
# systemtap-runtime-virtguest udev rules, init scripts/systemd service, req:-runtime
# systemtap-runtime-python2 HelperSDT python2 module, req:-runtime
# systemtap-runtime-python3 HelperSDT python3 module, req:-runtime
# systemtap-jupyter      /usr/bin/stap-jupyter-* interactive-notebook req:systemtap
#
# Typical scenarios:
#
# stap-client:           systemtap-client
# stap-server:           systemtap-server
# local user:            systemtap
#
# Unusual scenarios:
#
# intermediary stap-client for --remote:       systemtap-client (-runtime unused)
# intermediary stap-server for --use-server:   systemtap-server (-devel unused)

Summary: Programmable system-wide instrumentation system
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Source: ftp://sourceware.org/pub/systemtap/releases/systemtap-%{version}.tar.gz

# Build*
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: cpio
BuildRequires: gettext-devel
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(avahi-client)
%if %{with_debuginfod}
BuildRequires: pkgconfig(libdebuginfod)
BuildRequires: pkgconfig(json-c)
%endif
%if %{with_dyninst}
BuildRequires: dyninst-devel >= 10.0
BuildRequires: pkgconfig(libselinux)
%endif
%if %{with_sqlite}
BuildRequires: sqlite-devel > 3.7
%endif
%if %{with_monitor}
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(ncurses)
%endif
%if %{with_systemd}
BuildRequires: systemd
%endif
# Needed for libstd++ < 4.0, without <tr1/memory>
BuildRequires: boost-devel
%if %{with_crash}
BuildRequires: crash-devel zlib-devel
%endif
%if %{with_rpm}
BuildRequires: rpm-devel
%endif
BuildRequires: elfutils-devel >= %{elfutils_version}
%if %{with_docs}
BuildRequires: /usr/bin/latex /usr/bin/dvips /usr/bin/ps2pdf
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires: tex(fullpage.sty) tex(fancybox.sty) tex(bchr7t.tfm) tex(graphicx.sty)
%endif
%if %{with_htmldocs}
# On F10, xmlto's pdf support was broken off into a sub-package,
# called 'xmlto-tex'.  To avoid a specific F10 BuildReq, we'll do a
# file-based buildreq on '/usr/share/xmlto/format/fo/pdf'.
BuildRequires: xmlto /usr/share/xmlto/format/fo/pdf
%endif
%endif
%if %{with_emacsvim}
# for _emacs_sitelispdir macros etc.
BuildRequires: emacs-common
%endif
%if %{with_java}
BuildRequires: java-devel
%endif
%if %{with_virthost}
# BuildRequires: libvirt-devel >= 1.0.2
BuildRequires: pkgconfig(libvirt)
BuildRequires: pkgconfig(libxml-2.0)
%endif
BuildRequires: readline-devel
%if %{with_python2_probes}
BuildRequires: python2-devel
%if 0%{?fedora} >= 1
BuildRequires: python2-setuptools
%else
BuildRequires: python-setuptools
%endif
%endif
%if %{with_python3}
BuildRequires: python3
%endif
%if %{with_python3_probes}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif

%if %{with_httpd}
BuildRequires: libmicrohttpd-devel
BuildRequires: libuuid-devel
%endif
%if %{with_sysusers}
BuildRequires: systemd-rpm-macros
%endif
%if %{with_check}
BuildRequires: kernel-devel
# and some of the same Requires: as below
BuildRequires: dejagnu gcc make
%endif



# Install requirements
Requires: systemtap-client = %{version}-%{release}
Requires: systemtap-devel = %{version}-%{release}

%description
SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system.  The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.

# ------------------------------------------------------------------------

%package server
Summary: Instrumentation System Server
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap-devel = %{version}-%{release}
Conflicts: systemtap-devel < %{version}-%{release}
Conflicts: systemtap-runtime < %{version}-%{release}
Conflicts: systemtap-client < %{version}-%{release}
Requires: nss coreutils
Requires: zip unzip
Requires(pre): shadow-utils
BuildRequires: nss-devel avahi-devel
%if %{with_openssl}
Requires: openssl
%endif
%if %{with_systemd}
Requires: systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description server
This is the remote script compilation server component of systemtap.
It announces itself to nearby clients with avahi (if available), and
compiles systemtap scripts to kernel objects on their demand.


%package devel
Summary: Programmable system-wide instrumentation system - development headers, tools
License: GPL-2.0-or-later AND GPL-2.0-only AND BSD-3-Clause AND LGPL-2.1-only AND BSD-2-Clause
URL: https://sourceware.org/systemtap/

%if 0%{?rhel} >= 8 || 0%{?fedora} >= 20
Recommends: (kernel-debug-devel if kernel-debug)
Recommends: (kernel-devel if kernel)
%else
Requires: kernel-devel-uname-r
%endif

Requires: gcc make
# for compiling --runtime=dyninst sripts, need elfutils headers, bz1930973
Requires: elfutils-devel >= %{elfutils_version}

Conflicts: systemtap-client < %{version}-%{release}
Conflicts: systemtap-server < %{version}-%{release}
Conflicts: systemtap-runtime < %{version}-%{release}
# Suggest: kernel-debuginfo

%description devel
This package contains the components needed to compile a systemtap
script from source form into executable (.ko) forms.  It may be
installed on a self-contained developer workstation (along with the
systemtap-client and systemtap-runtime packages), or on a dedicated
remote server (alongside the systemtap-server package).  It includes
a copy of the standard tapset library and the runtime library C files.


%package runtime
Summary: Programmable system-wide instrumentation system - runtime
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires(pre): shadow-utils
Conflicts: systemtap-devel < %{version}-%{release}
Conflicts: systemtap-server < %{version}-%{release}
Conflicts: systemtap-client < %{version}-%{release}

%description runtime
SystemTap runtime contains the components needed to execute
a systemtap script that was already compiled into a module
using a local or remote systemtap-devel installation.


%package client
Summary: Programmable system-wide instrumentation system - client
License: GPL-2.0-or-later AND GPL-2.0-only AND BSD-3-Clause AND LGPL-2.1-only AND GFDL-1.2-or-later AND BSD-2-Clause
URL: https://sourceware.org/systemtap/
Requires: zip unzip
Requires: systemtap-runtime = %{version}-%{release}
Requires: coreutils grep sed unzip zip
Requires: openssh-clients
Conflicts: systemtap-devel < %{version}-%{release}
Conflicts: systemtap-server < %{version}-%{release}
Conflicts: systemtap-runtime < %{version}-%{release}
%if %{with_mokutil}
Requires: mokutil
%endif

%description client
This package contains/requires only the components needed to
use systemtap scripts by compiling them using a local or a remote
systemtap-server service, then run them using a local or
remote systemtap-runtime.  It includes script samples and
documentation, and a copy of the tapset library for reference.
It does NOT include all the components for running a systemtap
script in a self-contained fashion; for that, use the -devel
subpackage instead.

%package initscript
Summary: Systemtap Initscripts
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap = %{version}-%{release}
%if %{with_systemd}
Requires: systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description initscript
This package includes a SysVinit script to launch selected systemtap
scripts at system startup, along with a dracut module for early
boot-time probing if supported.


%package sdt-devel
Summary: Static probe support header files
License: GPL-2.0-or-later AND CC0-1.0
URL: https://sourceware.org/systemtap/
%if 0%{?rhel} && 0%{?rhel} <= 10
# for RHEL buildability compatibility, pull in sdt-dtrace at all times
Requires: systemtap-sdt-dtrace = %{version}-%{release}
%endif

%description sdt-devel
This package includes the <sys/sdt.h> header file used for static
instrumentation compiled into userspace programs.


%package sdt-dtrace
Summary: Static probe support dtrace tool
License: GPL-2.0-or-later AND CC0-1.0
URL: https://sourceware.org/systemtap/
Provides: dtrace = %{version}-%{release}
%if %{with_pyparsing}
%if %{with_python3}
Requires: python3-pyparsing
%else
%if 0%{?rhel} >= 7
Requires: pyparsing
%else
Requires: python2-pyparsing
%endif
%endif
%endif

%description sdt-dtrace
This package includes the dtrace-compatibility preprocessor
to process related .d files into tracing-macro-laden .h headers.


%package testsuite
Summary: Instrumentation System Testsuite
License: GPL-2.0-or-later AND GPL-2.0-only AND GPL-3.0-or-later AND MIT
URL: https://sourceware.org/systemtap/
Requires: systemtap = %{version}-%{release}
Requires: systemtap-sdt-devel = %{version}-%{release}
Requires: systemtap-server = %{version}-%{release}
Requires: dejagnu which elfutils grep nc wget
%if %{with_debuginfod}
Requires: elfutils-debuginfod
%endif
# work around fedora ci gating kvetching about i686<->x86-64 conflicts
%ifarch x86_64
Conflicts: systemtap-testsuite = %{version}-%{release}.i686
%endif
%ifarch i686
Conflicts: systemtap-testsuite = %{version}-%{release}.x86_64
%endif
Requires: gcc gcc-c++ make glibc-devel
# testsuite/systemtap.base/ptrace.exp needs strace
Requires: strace
# testsuite/systemtap.base/ipaddr.exp needs nc. Unfortunately, the rpm
# that provides nc has changed over time (from 'nc' to
# 'nmap-ncat'). So, we'll do a file-based require.
Requires: /usr/bin/nc
%ifnarch ia64 ppc64le aarch64
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
# no prelink
%else
Requires: prelink
%endif
%endif
# testsuite/systemtap.server/client.exp needs avahi
Requires: avahi
%if %{with_crash}
# testsuite/systemtap.base/crash.exp needs crash
Requires: crash
%endif
%if %{with_java}
Requires: systemtap-runtime-java = %{version}-%{release}
%endif
%if %{with_python2_probes}
Requires: systemtap-runtime-python2 = %{version}-%{release}
%endif
%if %{with_python3_probes}
Requires: systemtap-runtime-python3 = %{version}-%{release}
%endif
%ifarch x86_64
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 20
# fweimer, personal correspondence
Recommends: glibc-devel(x86-32)
%else
Requires: /usr/lib/libc.so
%endif
# ... and /usr/lib/libgcc_s.so.*
# ... and /usr/lib/libstdc++.so.*
%endif
%if 0%{?fedora} >= 18
Requires: stress
%endif
# The following "meta" files for the systemtap examples run "perf":
#   testsuite/systemtap.examples/hw_watch_addr.meta
#   testsuite/systemtap.examples/memory/hw_watch_sym.meta
Requires: perf

%description testsuite
This package includes the dejagnu-based systemtap stress self-testing
suite.  This may be used by system administrators to thoroughly check
systemtap on the current system.


%if %{with_java}
%package runtime-java
Summary: Systemtap Java Runtime Support
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap-runtime = %{version}-%{release}
# work around fedora ci gating kvetching about i686<->x86-64 conflicts
%ifarch x86_64
Conflicts: systemtap-runtime = %{version}-%{release}.i686
%endif
%ifarch i686
Conflicts: systemtap-runtime = %{version}-%{release}.x86_64
%endif
Requires: byteman > 2.0
Requires: iproute
Requires: java-devel

%description runtime-java
This package includes support files needed to run systemtap scripts
that probe Java processes running on the OpenJDK runtimes using Byteman.
%endif

%if %{with_python2_probes}
%package runtime-python2
Summary: Systemtap Python 2 Runtime Support
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap-runtime = %{version}-%{release}

%description runtime-python2
This package includes support files needed to run systemtap scripts
that probe python 2 processes.
%endif

%if %{with_python3_probes}
%package runtime-python3
Summary: Systemtap Python 3 Runtime Support
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap-runtime = %{version}-%{release}

%if ! (%{with_python2_probes})
# Provide an clean upgrade path when the python2 package is removed
Obsoletes: %{name}-runtime-python2 < %{version}-%{release}
%endif

%description runtime-python3
This package includes support files needed to run systemtap scripts
that probe python 3 processes.
%endif

%if %{with_python3_probes}
%package exporter
Summary: Systemtap-prometheus interoperation mechanism
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap-runtime = %{version}-%{release}

%description exporter
This package includes files for a systemd service that manages
systemtap sessions and relays prometheus metrics from the sessions
to remote requesters on demand.
%endif

%if %{with_virthost}
%package runtime-virthost
Summary: Systemtap Cross-VM Instrumentation - host
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
# only require libvirt-libs really
#Requires: libvirt >= 1.0.2
Requires: libxml2

%description runtime-virthost
This package includes the components required to run systemtap scripts
inside a libvirt-managed domain from the host without using a network
connection.
%endif

%if %{with_virtguest}
%package runtime-virtguest
Summary: Systemtap Cross-VM Instrumentation - guest
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap-runtime = %{version}-%{release}
%if %{with_systemd}
Requires(post): findutils coreutils
Requires(preun): grep coreutils
Requires(postun): grep coreutils
%else
Requires(post): chkconfig initscripts
Requires(preun): chkconfig initscripts
Requires(postun): initscripts
%endif

%description runtime-virtguest
This package installs the services necessary on a virtual machine for a
systemtap-runtime-virthost machine to execute systemtap scripts.
%endif

%package jupyter
Summary: ISystemtap jupyter kernel and examples
License: GPL-2.0-or-later
URL: https://sourceware.org/systemtap/
Requires: systemtap = %{version}-%{release}

%description jupyter
This package includes files needed to build and run
the interactive systemtap Jupyter kernel, either locally
or within a container.

# ------------------------------------------------------------------------

%prep
%setup -q

%build

# Enable/disable the dyninst pure-userspace backend
%if %{with_dyninst}
%global dyninst_config --with-dyninst
%else
%global dyninst_config --without-dyninst
%endif

# Enable/disable the dyninst pure-userspace backend
%if %{with_Werror}
%global Werror_config --enable-Werror
%else
%global Werror_config --disable-Werror
%endif

# Enable/disable the sqlite coverage testing support
%if %{with_sqlite}
%global sqlite_config --enable-sqlite
%else
%global sqlite_config --disable-sqlite
%endif

%if %{with_debuginfod}
%global debuginfod_config --with-debuginfod
%else
%global debuginfod_config --without-debuginfod
%endif


# Enable/disable the crash extension
%if %{with_crash}
%global crash_config --enable-crash
%else
%global crash_config --disable-crash
%endif

# Enable/disable the code to find and suggest needed rpms
%if %{with_rpm}
%global rpm_config --with-rpm
%else
%global rpm_config --without-rpm
%endif

%if %{with_docs}
%if %{with_htmldocs}
%global docs_config --enable-docs --enable-htmldocs
%else
%global docs_config --enable-docs --disable-htmldocs
%endif
%else
%global docs_config --enable-docs=prebuilt
%endif

%if %{with_java}
%global java_config --with-java=%{_jvmdir}/java
%else
%global java_config --without-java
%endif

%if %{with_python3}
%global python3_config --with-python3
%else
%global python3_config --without-python3
%endif
%if %{with_python2_probes}
%global python2_probes_config --with-python2-probes
%else
%global python2_probes_config --without-python2-probes
%endif
%if %{with_python3_probes}
%global python3_probes_config --with-python3-probes
%else
%global python3_probes_config --without-python3-probes
%endif

%if %{with_virthost}
%global virt_config --enable-virt
%else
%global virt_config --disable-virt
%endif

%if %{with_dracut}
%global dracut_config --with-dracutstap=%{dracutstap} --with-dracutbindir=%{dracutbindir}
%else
%global dracut_config %{nil}
%endif

%if %{with_httpd}
%global httpd_config --enable-httpd
%else
%global httpd_config --disable-httpd
%endif

%if %{with_bpf}
%global bpf_config --with-bpf
%else
%global bpf_config --without-bpf
%endif

# We don't ship compileworthy python code, just oddball samples
%global py_auto_byte_compile 0

%configure %{Werror_config} %{dyninst_config} %{sqlite_config} %{crash_config} %{docs_config} %{rpm_config} %{java_config} %{virt_config} %{dracut_config} %{python3_config} %{python2_probes_config} %{python3_probes_config} %{httpd_config} %{bpf_config} %{debuginfod_config} --disable-silent-rules --with-extra-version="rpm %{version}-%{release}"
make %{?_smp_mflags} V=1


%install
make DESTDIR=$RPM_BUILD_ROOT install

%if ! (%{with_python3})
rm -v $RPM_BUILD_ROOT%{_bindir}/stap-profile-annotate
%endif

%find_lang %{name}
for dir in $(ls -1d $RPM_BUILD_ROOT%{_mandir}/{??,??_??}) ; do
    dir=$(echo $dir | sed -e "s|^$RPM_BUILD_ROOT||")
    lang=$(basename $dir)
    echo "%%lang($lang) $dir/man*/*" >> %{name}.lang
done

%if %{with_sysusers}
mkdir -p %{buildroot}%{_sysusersdir}
echo '%_systemtap_runtime_preinstall' > %{buildroot}%{_sysusersdir}/systemtap-runtime.conf
echo '%_systemtap_server_preinstall' > %{buildroot}%{_sysusersdir}/systemtap-server.conf
echo '%_systemtap_testsuite_preinstall' > %{buildroot}%{_sysusersdir}/systemtap-testsuite.conf
mkdir -p %{buildroot}%{_tmpfilesdir}
echo '%_systemtap_server_preinstall_tmpfiles' > %{buildroot}%{_tmpfilesdir}/systemtap-server.conf
%endif


ln -s %{_datadir}/systemtap/examples

# Fix paths in the example scripts.
find $RPM_BUILD_ROOT%{_datadir}/systemtap/examples -type f -name '*.stp' -print0 | xargs -0 sed -i -r -e '1s@^#!.+stap@#!%{_bindir}/stap@'

# To make rpmlint happy, remove any .gitignore files in the testsuite.
find testsuite -type f -name '.gitignore' -print0 | xargs -0 rm -f

# Because "make install" may install staprun with whatever mode, the
# post-processing programs rpmbuild runs won't be able to read it.
# So, we change permissions so that they can read it.  We'll set the
# permissions back to 04110 in the %files section below.
chmod 755 $RPM_BUILD_ROOT%{_bindir}/staprun

# Copy over the testsuite
cp -rp testsuite $RPM_BUILD_ROOT%{_datadir}/systemtap

# We want the manuals in the special doc dir, not the generic doc install dir.
# We build it in place and then move it away so it doesn't get installed
# twice. rpm can specify itself where the (versioned) docs go with the
# %doc directive.
mkdir docs.installed
mv $RPM_BUILD_ROOT%{_datadir}/doc/systemtap/*.pdf docs.installed/
%if %{with_docs}
%if %{with_htmldocs}
mv $RPM_BUILD_ROOT%{_datadir}/doc/systemtap/tapsets docs.installed/
mv $RPM_BUILD_ROOT%{_datadir}/doc/systemtap/SystemTap_Beginners_Guide docs.installed/
%endif
%endif

install -D -m 644 macros.systemtap $RPM_BUILD_ROOT%{_rpmmacrodir}/macros.systemtap

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/stap-server
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/stap-server
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/stap-server/.systemtap
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/stap-server
touch $RPM_BUILD_ROOT%{_localstatedir}/log/stap-server/log
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/systemtap
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/systemtap
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 initscript/logrotate.stap-server $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/stap-server

# If using systemd systemtap.service file, retain the old init script in %{_libexecdir} as a helper.
%if %{with_systemd}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
touch $RPM_BUILD_ROOT%{_unitdir}/systemtap.service
# RHBZ2070857
mkdir -p $RPM_BUILD_ROOT%{_presetdir}
echo 'enable systemtap.service' > $RPM_BUILD_ROOT%{_presetdir}/42-systemtap.preset
install -m 644 initscript/systemtap.service $RPM_BUILD_ROOT%{_unitdir}/systemtap.service
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 755 initscript/systemtap $RPM_BUILD_ROOT%{_sbindir}/systemtap-service
%else
mkdir -p $RPM_BUILD_ROOT%{initdir}
install -m 755 initscript/systemtap $RPM_BUILD_ROOT%{initdir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
ln -sf %{initdir}/systemtap $RPM_BUILD_ROOT%{_sbindir}/systemtap-service
# TODO CHECK CORRECTNESS: symlink %{_sbindir}/systemtap-service to %{initdir}/systemtap
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemtap
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/script.d
install -m 644 initscript/config.systemtap $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/config

%if %{with_systemd}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
touch $RPM_BUILD_ROOT%{_unitdir}/stap-server.service
install -m 644 stap-server.service $RPM_BUILD_ROOT%{_unitdir}/stap-server.service
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 644 stap-server.conf $RPM_BUILD_ROOT%{_tmpfilesdir}/stap-server.conf
%else
install -m 755 initscript/stap-server $RPM_BUILD_ROOT%{initdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/stap-server/conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 initscript/config.stap-server $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/stap-server
%endif

%if %{with_emacsvim}
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitelispdir}
install -p -m 644 emacs/systemtap-mode.el* $RPM_BUILD_ROOT%{_emacs_sitelispdir}
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitestartdir}
install -p -m 644 emacs/systemtap-init.el $RPM_BUILD_ROOT%{_emacs_sitestartdir}/systemtap-init.el
for subdir in ftdetect ftplugin indent syntax
do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/$subdir
    install -p -m 644 vim/$subdir/*.vim $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/$subdir
done
%endif

%if %{with_virtguest}
   mkdir -p $RPM_BUILD_ROOT%{udevrulesdir}
   %if %{with_systemd}
      install -p -m 644 staprun/guest/99-stapsh.rules $RPM_BUILD_ROOT%{udevrulesdir}
      mkdir -p $RPM_BUILD_ROOT%{_unitdir}
      install -p -m 644 staprun/guest/stapsh@.service $RPM_BUILD_ROOT%{_unitdir}
   %else
      install -p -m 644 staprun/guest/99-stapsh-init.rules $RPM_BUILD_ROOT%{udevrulesdir}
      install -p -m 755 staprun/guest/stapshd $RPM_BUILD_ROOT%{initdir}
      mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/systemtap
      install -p -m 755 staprun/guest/stapsh-daemon $RPM_BUILD_ROOT%{_libexecdir}/systemtap
      mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
      # Technically, this is only needed for RHEL5, in which the MODULE_ALIAS is missing, but
      # it does no harm in RHEL6 as well
      install -p -m 755 staprun/guest/virtio_console.modules $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
   %endif
%endif

%if %{with_dracut}
   mkdir -p $RPM_BUILD_ROOT%{dracutstap}
   install -p -m 755 initscript/99stap/module-setup.sh $RPM_BUILD_ROOT%{dracutstap}
   install -p -m 755 initscript/99stap/install $RPM_BUILD_ROOT%{dracutstap}
   install -p -m 755 initscript/99stap/check $RPM_BUILD_ROOT%{dracutstap}
   install -p -m 755 initscript/99stap/start-staprun.sh $RPM_BUILD_ROOT%{dracutstap}
   touch $RPM_BUILD_ROOT%{dracutstap}/params.conf
%endif

%if %{with_specific_python}
# Some files got ambiguous python shebangs, we fix them after everything else is done
%py3_shebang_fix %{buildroot}%{python3_sitearch} %{buildroot}%{_bindir}/*
%endif

%check
%if %{with_check}
make check RUNTESTFLAGS=environment_sanity.exp
%endif


%pre runtime
%if %{with_sysusers}
%if (0%{?fedora} && 0%{?fedora} < 42) || (0%{?rhel} && 0%{?rhel} < 11)
echo '%_systemtap_runtime_preinstall' | systemd-sysusers --replace=%{_sysusersdir}/systemtap-runtime.conf -
exit 0
%endif
%else
getent group stapusr >/dev/null || groupadd -f -g 156 -r stapusr
getent group stapsys >/dev/null || groupadd -f -g 157 -r stapsys
getent group stapdev >/dev/null || groupadd -f -g 158 -r stapdev
getent passwd stapunpriv >/dev/null || \
  useradd -c "Systemtap Unprivileged User" -u 159 -g stapunpriv -d %{_localstatedir}/lib/stapunpriv -r -s /sbin/nologin stapunpriv 2>/dev/null || \
  useradd -c "Systemtap Unprivileged User" -g stapunpriv -d %{_localstatedir}/lib/stapunpriv -r -s /sbin/nologin stapunpriv
exit 0
%endif

%pre server
%if %{with_sysusers}
%if (0%{?fedora} && 0%{?fedora} < 42) || (0%{?rhel} && 0%{?rhel} < 11)
echo '%_systemtap_server_preinstall' | systemd-sysusers --replace=%{_sysusersdir}/systemtap-server.conf -
echo '%_systemtap_server_preinstall_tmpfiles' | systemd-tmpfiles --replace=%{_tmpfilesdir}/systemtap-server.conf -
exit 0
%endif
%else
getent group stap-server >/dev/null || groupadd -f -g 155 -r stap-server
getent passwd stap-server >/dev/null || \
  useradd -c "Systemtap Compile Server" -u 155 -g stap-server -d %{_localstatedir}/lib/stap-server -r -s /sbin/nologin stap-server 2>/dev/null || \
  useradd -c "Systemtap Compile Server" -g stap-server -d %{_localstatedir}/lib/stap-server -r -s /sbin/nologin stap-server
exit 0
%endif

%pre testsuite
%if %{with_sysusers}
%if (0%{?fedora} && 0%{?fedora} < 42) || (0%{?rhel} && 0%{?rhel} < 11)
echo '%_systemtap_testsuite_preinstall' | systemd-sysusers --replace=%{_sysusersdir}/systemtap-testsuite.conf -
exit 0
%endif
%else
getent passwd stapusr >/dev/null || \
    useradd -c "Systemtap 'stapusr' User" -g stapusr -r -s /sbin/nologin stapusr
getent passwd stapsys >/dev/null || \
    useradd -c "Systemtap 'stapsys' User" -g stapsys -G stapusr -r -s /sbin/nologin stapsys
getent passwd stapdev >/dev/null || \
    useradd -c "Systemtap 'stapdev' User" -g stapdev -G stapusr -r -s /sbin/nologin stapdev
exit 0
%endif

%post server

# We have some duplication between the %files listings for the
# ~stap-server directories and the explicit mkdir/chown/chmod bits
# here.  Part of the reason may be that a preexisting stap-server
# account may well be placed somewhere other than
# %{_localstatedir}/lib/stap-server, but we'd like their permissions
# set similarly.

test -e ~stap-server && chmod 750 ~stap-server

if [ ! -f ~stap-server/.systemtap/rc ]; then
  mkdir -p ~stap-server/.systemtap
  chown stap-server:stap-server ~stap-server/.systemtap
  # PR16276: guess at a reasonable number for a default --rlimit-nproc
  numcpu=`/usr/bin/getconf _NPROCESSORS_ONLN`
  if [ -z "$numcpu" -o "$numcpu" -lt 1 ]; then numcpu=1; fi
  nproc=`expr $numcpu \* 30`
  # PR29661 -> 4G
  echo "--rlimit-as=4294967296 --rlimit-cpu=60 --rlimit-nproc=$nproc --rlimit-stack=1024000 --rlimit-fsize=51200000" > ~stap-server/.systemtap/rc
  chown stap-server:stap-server ~stap-server/.systemtap/rc
fi

test -e %{_localstatedir}/log/stap-server/log || {
     touch %{_localstatedir}/log/stap-server/log
     chmod 644 %{_localstatedir}/log/stap-server/log
     chown stap-server:stap-server %{_localstatedir}/log/stap-server/log
}
# Prepare the service
%if %{with_systemd}
     # Note, Fedora policy doesn't allow network services enabled by default
     # /bin/systemctl enable stap-server.service >/dev/null 2>&1 || :
     /bin/systemd-tmpfiles --create %{_tmpfilesdir}/stap-server.conf >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add stap-server
%endif
exit 0

%triggerin client -- systemtap-server
if test -e ~stap-server/.systemtap/ssl/server/stap.cert; then
   # echo Authorizing ssl-peer/trusted-signer certificate for local systemtap-server
   %{_libexecdir}/systemtap/stap-authorize-cert ~stap-server/.systemtap/ssl/server/stap.cert %{_sysconfdir}/systemtap/ssl/client >/dev/null
   %{_libexecdir}/systemtap/stap-authorize-cert ~stap-server/.systemtap/ssl/server/stap.cert %{_sysconfdir}/systemtap/staprun >/dev/null
fi
exit 0
# XXX: corresponding %triggerun?

%preun server
# Check that this is the actual deinstallation of the package, as opposed to
# just removing the old package on upgrade.
if [ $1 = 0 ] ; then
    %if %{with_systemd}
       /bin/systemctl --no-reload disable stap-server.service >/dev/null 2>&1 || :
       /bin/systemctl stop stap-server.service >/dev/null 2>&1 || :
    %else
        /sbin/service stap-server stop >/dev/null 2>&1
        /sbin/chkconfig --del stap-server
    %endif
fi
exit 0

%postun server
# Check whether this is an upgrade of the package.
# If so, restart the service if it's running
if [ "$1" -ge "1" ] ; then
    %if %{with_systemd}
        /bin/systemctl condrestart stap-server.service >/dev/null 2>&1 || :
    %else
        /sbin/service stap-server condrestart >/dev/null 2>&1 || :
    %endif
fi
exit 0

%post initscript
%if %{with_systemd}
    # RHBZ2070857 - use systemd presets instead
    # /bin/systemctl enable systemtap.service >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add systemtap
%endif
exit 0

%preun initscript
# Check that this is the actual deinstallation of the package, as opposed to
# just removing the old package on upgrade.
if [ $1 = 0 ] ; then
    %if %{with_systemd}
        /bin/systemctl --no-reload disable systemtap.service >/dev/null 2>&1 || :
        /bin/systemctl stop systemtap.service >/dev/null 2>&1 || :
    %else
        /sbin/service systemtap stop >/dev/null 2>&1
        /sbin/chkconfig --del systemtap
    %endif
fi
exit 0

%postun initscript
# Check whether this is an upgrade of the package.
# If so, restart the service if it's running
if [ "$1" -ge "1" ] ; then
    %if %{with_systemd}
        /bin/systemctl condrestart systemtap.service >/dev/null 2>&1 || :
    %else
        /sbin/service systemtap condrestart >/dev/null 2>&1 || :
    %endif
fi
exit 0

%post runtime-virtguest
%if %{with_systemd}
   # Start services if there are ports present
   if [ -d /dev/virtio-ports ]; then
      (find /dev/virtio-ports -iname 'org.systemtap.stapsh.[0-9]*' -type l \
         | xargs -n 1 basename \
         | xargs -n 1 -I {} /bin/systemctl start stapsh@{}.service) >/dev/null 2>&1 || :
   fi
%else
   /sbin/chkconfig --add stapshd
   /sbin/chkconfig stapshd on
   /sbin/service stapshd start >/dev/null 2>&1 || :
%endif
exit 0

%preun runtime-virtguest
# Stop service if this is an uninstall rather than an upgrade
if [ $1 = 0 ]; then
   %if %{with_systemd}
      # We need to stop all stapsh services. Because they are instantiated from
      # a template service file, we can't simply call disable. We need to find
      # all the running ones and stop them all individually
      for service in `/bin/systemctl --full | grep stapsh@ | cut -d ' ' -f 1`; do
         /bin/systemctl stop $service >/dev/null 2>&1 || :
      done
   %else
      /sbin/service stapshd stop >/dev/null 2>&1
      /sbin/chkconfig --del stapshd
   %endif
fi
exit 0

%postun runtime-virtguest
# Restart service if this is an upgrade rather than an uninstall
if [ "$1" -ge "1" ]; then
   %if %{with_systemd}
      # We need to restart all stapsh services. Because they are instantiated from
      # a template service file, we can't simply call restart. We need to find
      # all the running ones and restart them all individually
      for service in `/bin/systemctl --full | grep stapsh@ | cut -d ' ' -f 1`; do
         /bin/systemctl condrestart $service >/dev/null 2>&1 || :
      done
   %else
      /sbin/service stapshd condrestart >/dev/null 2>&1
   %endif
fi
exit 0

%if %{with_python3_probes}
%if %{with_systemd}
%preun exporter
if [ $1 = 0 ] ; then
  /bin/systemctl stop stap-exporter.service >/dev/null 2>&1 || :
  /bin/systemctl disable stap-exporter.service >/dev/null 2>&1 || :
fi
exit 0

%postun exporter
# Restart service if this is an upgrade rather than an uninstall
if [ "$1" -ge "1" ]; then
   /bin/systemctl condrestart stap-exporter >/dev/null 2>&1 || :
fi
exit 0
%endif
%endif

%post
# Remove any previously-built uprobes.ko materials
(make -C %{_datadir}/systemtap/runtime/uprobes clean) >/dev/null 2>&1 || true
(/sbin/rmmod uprobes) >/dev/null 2>&1 || true

%preun
# Ditto
(make -C %{_datadir}/systemtap/runtime/uprobes clean) >/dev/null 2>&1 || true
(/sbin/rmmod uprobes) >/dev/null 2>&1 || true

# ------------------------------------------------------------------------

%files
# The main "systemtap" rpm doesn't include any files.

%files server -f systemtap.lang
%{_bindir}/stap-server
%dir %{_libexecdir}/systemtap
%{_libexecdir}/systemtap/stap-serverd
%{_libexecdir}/systemtap/stap-start-server
%{_libexecdir}/systemtap/stap-stop-server
%{_libexecdir}/systemtap/stap-gen-cert
%{_libexecdir}/systemtap/stap-sign-module
%{_libexecdir}/systemtap/stap-authorize-cert
%{_libexecdir}/systemtap/stap-env
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%{_mandir}/man8/stap-server.8*
%if %{with_systemd}
%{_unitdir}/stap-server.service
%{_tmpfilesdir}/stap-server.conf
%{_tmpfilesdir}/systemtap-server.conf
%else
%{initdir}/stap-server
%dir %{_sysconfdir}/stap-server/conf.d
%config(noreplace) %{_sysconfdir}/sysconfig/stap-server
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/stap-server
%dir %{_sysconfdir}/stap-server
%dir %attr(0750,stap-server,stap-server) %{_localstatedir}/lib/stap-server
%dir %attr(0700,stap-server,stap-server) %{_localstatedir}/lib/stap-server/.systemtap
%dir %attr(0755,stap-server,stap-server) %{_localstatedir}/log/stap-server
%ghost %config(noreplace) %attr(0644,stap-server,stap-server) %{_localstatedir}/log/stap-server/log
%ghost %attr(0755,stap-server,stap-server) %{_localstatedir}/run/stap-server
%doc README README.unprivileged AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING
%if %{with_sysusers}
%{_sysusersdir}/systemtap-server.conf
%endif


%files devel -f systemtap.lang
%{_bindir}/stap
%{_bindir}/stap-prep
%if %{with_python3}
%{_bindir}/stap-profile-annotate
%endif
%{_bindir}/stap-report
%dir %{_datadir}/systemtap
%{_datadir}/systemtap/runtime
%{_datadir}/systemtap/tapset
%{_mandir}/man1/stap.1*
%{_mandir}/man1/stap-prep.1*
%{_mandir}/man1/stap-report.1*
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%doc README README.unprivileged AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING
%if %{with_java}
%dir %{_libexecdir}/systemtap
%{_libexecdir}/systemtap/libHelperSDT.so
%endif
%if %{with_emacsvim}
%{_emacs_sitelispdir}/*.el*
%{_emacs_sitestartdir}/systemtap-init.el
%{_datadir}/vim/vimfiles
%endif
# Notice that the stap-resolve-module-function.py file is used by
# *both* the python2 and python3 subrpms.  Both subrpms use that same
# python script to help list python probes.
%if %{with_python3_probes} || %{with_python2_probes}
%{_libexecdir}/systemtap/python/stap-resolve-module-function.py
%dir %{_libexecdir}/systemtap/python
%exclude %{_libexecdir}/systemtap/python/stap-resolve-module-function.py?
%endif


%files runtime -f systemtap.lang
%attr(4110,root,stapusr) %{_bindir}/staprun
%{_bindir}/stapsh
%{_bindir}/stap-merge
%{_bindir}/stap-report
%if %{with_dyninst}
%{_bindir}/stapdyn
%endif
%if %{with_bpf}
%{_bindir}/stapbpf
%endif
%dir %{_libexecdir}/systemtap
%{_libexecdir}/systemtap/stapio
%{_libexecdir}/systemtap/stap-authorize-cert
%if %{with_crash}
%dir %{_libdir}/systemtap
%{_libdir}/systemtap/staplog.so*
%endif
%{_mandir}/man1/stap-report.1*
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%{_mandir}/man8/stapsh.8*
%{_mandir}/man8/staprun.8*
%if %{with_dyninst}
%{_mandir}/man8/stapdyn.8*
%endif
%if %{with_bpf}
%{_mandir}/man8/stapbpf.8*
%endif
%doc README README.security AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING
%if %{with_sysusers}
%{_sysusersdir}/systemtap-runtime.conf
%endif


%files client -f systemtap.lang
%doc README README.unprivileged AUTHORS NEWS
%{_datadir}/systemtap/examples
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc docs.installed/*.pdf
%if %{with_docs}
%if %{with_htmldocs}
%doc docs.installed/tapsets/*.html
%doc docs.installed/SystemTap_Beginners_Guide
%endif
%endif
%{_bindir}/stap
%{_bindir}/stap-prep
%{_bindir}/stap-report
%{_mandir}/man1/stap.1*
%{_mandir}/man1/stap-prep.1*
%{_mandir}/man1/stap-merge.1*
%{_mandir}/man1/stap-report.1*
%{_mandir}/man1/stapref.1*
%{_mandir}/man3/*
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%dir %{_datadir}/systemtap
%{_datadir}/systemtap/tapset



%files initscript
%if %{with_systemd}
%{_presetdir}/42-systemtap.preset
%{_unitdir}/systemtap.service
%{_sbindir}/systemtap-service
%else
%{initdir}/systemtap
%{_sbindir}/systemtap-service
%endif
%dir %{_sysconfdir}/systemtap
%dir %{_sysconfdir}/systemtap/conf.d
%dir %{_sysconfdir}/systemtap/script.d
%config(noreplace) %{_sysconfdir}/systemtap/config
%dir %{_localstatedir}/cache/systemtap
%ghost %{_localstatedir}/run/systemtap
%{_mandir}/man8/systemtap-service.8*
%if %{with_dracut}
   %dir %{dracutstap}
   %{dracutstap}/*
%endif


%files sdt-devel
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%{_rpmmacrodir}/macros.systemtap
%doc README AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING


%files sdt-dtrace
%{_bindir}/dtrace
%doc README AUTHORS NEWS
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man1/dtrace.1*


%files testsuite
%dir %{_datadir}/systemtap
%{_datadir}/systemtap/testsuite
%if %{with_sysusers}
%{_sysusersdir}/systemtap-testsuite.conf
%endif


%if %{with_java}
%files runtime-java
%dir %{_libexecdir}/systemtap
%{_libexecdir}/systemtap/libHelperSDT.so
%{_libexecdir}/systemtap/HelperSDT.jar
%{_libexecdir}/systemtap/stapbm
%endif

%if %{with_python2_probes}
%files runtime-python2
%{python_sitearch}/HelperSDT
%{python_sitearch}/HelperSDT-*.egg-info
%endif
%if %{with_python3_probes}
%files runtime-python3
%{python3_sitearch}/HelperSDT
%{python3_sitearch}/HelperSDT-*.egg-info
%endif

%if %{with_virthost}
%files runtime-virthost
%{_mandir}/man1/stapvirt.1*
%{_bindir}/stapvirt
%endif

%if %{with_virtguest}
%files runtime-virtguest
%if %{with_systemd}
   %{udevrulesdir}/99-stapsh.rules
   %{_unitdir}/stapsh@.service
%else
   %{udevrulesdir}/99-stapsh-init.rules
   %dir %{_libexecdir}/systemtap
   %{_libexecdir}/systemtap/stapsh-daemon
   %{initdir}/stapshd
   %{_sysconfdir}/sysconfig/modules/virtio_console.modules
%endif
%endif

%if %{with_python3_probes}
%files exporter
%{_sysconfdir}/stap-exporter
%{_sysconfdir}/sysconfig/stap-exporter
%{_unitdir}/stap-exporter.service
%{_mandir}/man8/stap-exporter.8*
%{_sbindir}/stap-exporter
%endif

%files jupyter
%{_bindir}/stap-jupyter-container
%{_bindir}/stap-jupyter-install
%{_mandir}/man1/stap-jupyter.1*
%dir %{_datadir}/systemtap
%{_datadir}/systemtap/interactive-notebook

# ------------------------------------------------------------------------

# Future new-release entries should be of the form
# * DDD MMM DD YYYY YOURNAME <YOUREMAIL> - V-R
# - Upstream release, see wiki page below for detailed notes.
#   https://sourceware.org/systemtap/wiki/SystemTapReleases

# PRERELEASE
%changelog
* Fri Oct 31 2025 Frank Ch. Eigler <fche@redhat.com> - 5.4-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases

* Mon Sep 22 2025 Frank Ch. Eigler <fche@redhat.com> - 5.4-17585496g86ab88eb
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Mon Sep 22 2025 Frank Ch. Eigler <fche@redhat.com> - 5.4-17585473g1fe4178d
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.3-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.3-2
- Rebuilt for Python 3.14

* Fri May 02 2025 Frank Ch. Eigler <fche@redhat.com> - 5.3-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases

* Thu Feb 06 2025 Frank Ch. Eigler <fche@redhat.com> - 5.3~pre17373816g7a71d34b.5
- Respin against dyninst 13 redux

* Fri Jan 24 2025 Frank Ch. Eigler <fche@redhat.com> - 5.3~pre17373816g7a71d34b.3
- Respin against dyninst 13, sans dyninst on i686.

* Mon Jan 20 2025 Frank Ch. Eigler <fche@redhat.com> - 5.3-17373816g7a71d34b
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Mon Jan 20 2025 Frank Ch. Eigler <fche@redhat.com> - 5.3-17373794g3efe129d
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Sun Jan 19 2025 Frank Ch. Eigler <fche@redhat.com> - 5.3-17373422g9a48fbea
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Sun Jan 19 2025 Frank Ch. Eigler <fche@redhat.com> - 5.2-17373420g1e894ff0
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 08 2024 Frank Ch. Eigler <fche@redhat.com> - 5.2-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases

* Mon Oct 07 2024 William Cohen <wcohen@redhat.com> - 5.2-17283218gc5774e18
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Tue Oct 01 2024 William Cohen <wcohen@redhat.com> - 5.2-17277956g0b7f6722
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Fri Aug 30 2024 Frank Ch. Eigler <fche@redhat.com> - 5.2-17250223gd07e4284
- Automated weekly rawhide release
- Applied spec changes from upstream git

* Thu Aug 08 2024 Lumír Balhar <lbalhar@redhat.com> - 5.2-pre
- Final split of sdt-dtrace and sdt-devel (rhbz#2296275)
  https://fedoraproject.org/wiki/Changes/Separate_dtrace_package

* Fri Apr 26 2024 Frank Ch. Eigler <fche@redhat.com> - 5.1-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases

* Sat Nov 04 2023 Frank Ch. Eigler <fche@redhat.com> - 5.0-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases
- migrated to SPDX license

* Fri Apr 28 2023 Frank Ch. Eigler <fche@redhat.com> - 4.9-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases

* Thu Nov 03 2022 Serhei Makarov <serhei@serhei.io> - 4.8-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases
  
* Mon May 02 2022 Frank Ch. Eigler <fche@redhat.com> - 4.7-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases

* Mon Nov 15 2021 Serhei Makarov <me@serhei.io> - 4.6-1
- Upstream release, see wiki page below for detailed notes.
  https://sourceware.org/systemtap/wiki/SystemTapReleases

* Fri May 07 2021 Serhei Makarov <me@serhei.io> - 4.5-1
- Upstream release.

* Mon Nov 09 2020 Frank Ch. Eigler <fche@redhat.com> - 4.4-1
- Upstream release.

* Thu Jun 11 2020 Frank Ch. Eigler <fche@redhat.com> - 4.3-1
- Upstream release.

* Mon Nov 18 2019 Sagar Patel <sapatel@redhat.com> - 4.2-1
- Upstream release.

* Tue May 07 2019 Serguei Makarov <smakarov@redhat.com> - 4.1-1
- Upstream release.

* Sat Oct 13 2018 Frank Ch. Eigler <fche@redhat.com> - 4.0-1
- Upstream release.

* Thu Jun 07 2018 Frank Ch. Eigler <fche@redhat.com> - 3.3-1
- Upstream release.

* Wed Oct 18 2017 Frank Ch. Eigler <fche@redhat.com> - 3.2-1
- Upstream release.

* Fri Feb 17 2017 Frank Ch. Eigler <fche@redhat.com> - 3.1-1
- Upstream release.

* Sun Mar 27 2016 Frank Ch. Eigler <fche@redhat.com> - 3.0-1
- Upstream release.

* Thu Oct 08 2015 Frank Ch. Eigler <fche@redhat.com> - 2.9-1
- Upstream release.

* Wed Jun 17 2015 Abegail Jakop <ajakop@redhat.com> - 2.8-1
- Upstream release.

* Wed Feb 18 2015 Frank Ch. Eigler <fche@redhat.com> - 2.7-1
- Upstream release.

* Fri Sep 05 2014 Josh Stone <jistone@redhat.com> - 2.6-1
- Upstream release.

* Mon Jul 07 2014 Josh Stone <jistone@redhat.com>
- Flip with_dyninst to an %%ifarch passlist.

* Wed Apr 30 2014 Jonathan Lebon <jlebon@redhat.com> - 2.5-1
- Upstream release.

* Thu Feb 13 2014 Lukas Berk <lberk@redhat.com>
- Add directory checks for runtime-java sym links

* Mon Jan 06 2014 Jonathan Lebon <jlebon@redhat.com>
- Added dracut module to initscript package

* Wed Nov 06 2013 Frank Ch. Eigler <fche@redhat.com> - 2.4-1
- Upstream release.

* Wed Oct 09 2013 Jonathan Lebon <jlebon@redhat.com>
- Added runtime-virthost and runtime-virtguest packages.

* Thu Jul 25 2013 Frank Ch. Eigler <fche@redhat.com> - 2.3-1
- Upstream release.

* Thu May 16 2013 Frank Ch. Eigler <fche@redhat.com> - 2.2.1-1
- Upstream release.

* Tue May 14 2013 Frank Ch. Eigler <fche@redhat.com> - 2.2-1
- Upstream release.

* Wed Feb 13 2013 Serguei Makarov <smakarov@redhat.com> - 2.1-1
- Upstream release.

* Tue Oct 09 2012 Josh Stone <jistone@redhat.com> - 2.0-1
- Upstream release.

* Fri Jul 13 2012 Peter Robinson <pbrobinson@fedoraproject.org>
- Fix ifarch statement
- use file based requires for glibc-devel on x86_64 so that we work in koji

* Sun Jun 17 2012 Frank Ch. Eigler <fche@redhat.com> - 1.8-1
- Upstream release.

* Wed Feb 01 2012 Frank Ch. Eigler <fche@redhat.com> - 1.7-1
- Upstream release.

* Fri Jan 13 2012 David Smith <dsmith@redhat.com> - 1.6-2
- Fixed /bin/mktemp require.

* Mon Jul 25 2011 Stan Cox <scox@redhat.com> - 1.6-1
- Upstream release.

* Mon May 23 2011 Stan Cox <scox@redhat.com> - 1.5-1
- Upstream release.

* Mon Jan 17 2011 Frank Ch. Eigler <fche@redhat.com> - 1.4-1
- Upstream release.

* Wed Jul 21 2010 Josh Stone <jistone@redhat.com> - 1.3-1
- Upstream release.

* Mon Mar 22 2010 Frank Ch. Eigler <fche@redhat.com> - 1.2-1
- Upstream release.

* Mon Dec 21 2009 David Smith <dsmith@redhat.com> - 1.1-1
- Upstream release.

* Tue Sep 22 2009 Josh Stone <jistone@redhat.com> - 1.0-1
- Upstream release.

* Tue Aug  4 2009 Josh Stone <jistone@redhat.com> - 0.9.9-1
- Upstream release.

* Thu Jun 11 2009 Josh Stone <jistone@redhat.com> - 0.9.8-1
- Upstream release.

* Thu Apr 23 2009 Josh Stone <jistone@redhat.com> - 0.9.7-1
- Upstream release.

* Fri Mar 27 2009 Josh Stone <jistone@redhat.com> - 0.9.5-1
- Upstream release.

* Wed Mar 18 2009 Will Cohen <wcohen@redhat.com> - 0.9-2
- Add location of man pages.

* Tue Feb 17 2009 Frank Ch. Eigler <fche@redhat.com> - 0.9-1
- Upstream release.

* Thu Nov 13 2008 Frank Ch. Eigler <fche@redhat.com> - 0.8-1
- Upstream release.

* Tue Jul 15 2008 Frank Ch. Eigler <fche@redhat.com> - 0.7-1
- Upstream release.

* Fri Feb  1 2008 Frank Ch. Eigler <fche@redhat.com> - 0.6.1-3
- Add zlib-devel to buildreq; missing from crash-devel
- Process testsuite .stp files for #!stap->#!/usr/bin/stap

* Fri Jan 18 2008 Frank Ch. Eigler <fche@redhat.com> - 0.6.1-1
- Add crash-devel buildreq to build staplog.so crash(8) module.
- Many robustness & functionality improvements:

* Wed Dec  5 2007 Will Cohen <wcohen@redhat.com> - 0.6-2
- Correct Source to point to location contain code.

* Thu Aug  9 2007 David Smith <dsmith@redhat.com> - 0.6-1
- Bumped version, added libcap-devel BuildRequires.

* Wed Jul 11 2007 Will Cohen <wcohen@redhat.com> - 0.5.14-2
- Fix Requires and BuildRequires for sqlite.

* Mon Jul  2 2007 Frank Ch. Eigler <fche@redhat.com> - 0.5.14-1
- Many robustness improvements: 1117, 1134, 1305, 1307, 1570, 1806,
  2033, 2116, 2224, 2339, 2341, 2406, 2426, 2438, 2583, 3037,
  3261, 3282, 3331, 3428 3519, 3545, 3625, 3648, 3880, 3888, 3911,
  3952, 3965, 4066, 4071, 4075, 4078, 4081, 4096, 4119, 4122, 4127,
  4146, 4171, 4179, 4183, 4221, 4224, 4254, 4281, 4319, 4323, 4326,
  4329, 4332, 4337, 4415, 4432, 4444, 4445, 4458, 4467, 4470, 4471,
  4518, 4567, 4570, 4579, 4589, 4609, 4664

* Mon Mar 26 2007 Frank Ch. Eigler <fche@redhat.com> - 0.5.13-1
- An emergency / preliminary refresh, mainly for compatibility
  with 2.6.21-pre kernels.

* Mon Jan  1 2007 Frank Ch. Eigler <fche@redhat.com> - 0.5.12-1
- Many changes, see NEWS file.

* Tue Sep 26 2006 David Smith <dsmith@redhat.com> - 0.5.10-1
- Added 'systemtap-runtime' subpackage.

* Wed Jul 19 2006 Roland McGrath <roland@redhat.com> - 0.5.9-1
- PRs 2669, 2913

* Fri Jun 16 2006 Roland McGrath <roland@redhat.com> - 0.5.8-1
- PRs 2627, 2520, 2228, 2645

* Fri May  5 2006 Frank Ch. Eigler <fche@redhat.com> - 0.5.7-1
- PRs 2511 2453 2307 1813 1944 2497 2538 2476 2568 1341 2058 2220 2437
  1326 2014 2599 2427 2438 2465 1930 2149 2610 2293 2634 2506 2433

* Tue Apr  4 2006 Roland McGrath <roland@redhat.com> - 0.5.5-1
- Many changes, affected PRs include: 2068, 2293, 1989, 2334,
  1304, 2390, 2425, 953.

* Wed Feb  1 2006 Frank Ch. Eigler <fche@redhat.com> - 0.5.4-1
- PRs 1916, 2205, 2142, 2060, 1379

* Mon Jan 16 2006 Roland McGrath <roland@redhat.com> - 0.5.3-1
- Many changes, affected PRs include: 2056, 1144, 1379, 2057,
  2060, 1972, 2140, 2148

* Mon Dec 19 2005 Roland McGrath <roland@redhat.com> - 0.5.2-1
- Fixed build with gcc 4.1, various tapset changes.

* Wed Dec  7 2005 Roland McGrath <roland@redhat.com> - 0.5.1-1
- elfutils update, build changes

* Fri Dec 02 2005  Frank Ch. Eigler  <fche@redhat.com> - 0.5-1
- Many fixes and improvements: 1425, 1536, 1505, 1380, 1329, 1828, 1271,
  1339, 1340, 1345, 1837, 1917, 1903, 1336, 1868, 1594, 1564, 1276, 1295

* Mon Oct 31 2005 Roland McGrath <roland@redhat.com> - 0.4.2-1
- Many fixes and improvements: PRs 1344, 1260, 1330, 1295, 1311, 1368,
  1182, 1131, 1332, 1366, 1456, 1271, 1338, 1482, 1477, 1194.

* Wed Sep 14 2005 Roland McGrath <roland@redhat.com> - 0.4.1-1
- Many fixes and improvements since 0.2.2; relevant PRs include:
  1122, 1134, 1155, 1172, 1174, 1175, 1180, 1186, 1187, 1191, 1193, 1195,
  1197, 1205, 1206, 1209, 1213, 1244, 1257, 1258, 1260, 1265, 1268, 1270,
  1289, 1292, 1306, 1335, 1257

* Wed Sep  7 2005 Frank Ch. Eigler <fche@redhat.com>
- Bump version.

* Tue Aug 16 2005 Frank Ch. Eigler <fche@redhat.com>
- Bump version.

* Wed Aug  3 2005 Martin Hunt <hunt@redhat.com> - 0.2.2-1
- Add directory /var/cache/systemtap
- Add stp_check to /usr/libexec/systemtap

* Wed Aug  3 2005 Roland McGrath <roland@redhat.com> - 0.2.1-1
- New version 0.2.1, various fixes.

* Fri Jul 29 2005 Roland McGrath <roland@redhat.com> - 0.2-1
- New version 0.2, requires elfutils 0.111

* Mon Jul 25 2005 Roland McGrath <roland@redhat.com>
- Clean up spec file, build bundled elfutils.

* Thu Jul 21 2005 Martin Hunt <hunt@redhat.com>
- Set Version to use version from autoconf.
- Fix up some of the path names.
- Add Requires and BuildRequires.

* Tue Jul 19 2005 Will Cohen <wcohen@redhat.com>
- Initial creation of RPM.
