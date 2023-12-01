%global use_alternatives 1
%global lspp 1
# {_exec_prefix}/lib/cups is correct, even on x86_64.
# It is not used for shared objects but for executables.
# It's more of a libexec-style ({_libexecdir}) usage,
# but we use lib for compatibility with 3rd party drivers (at upstream request).
%global cups_serverbin %{_libdir}/cups
%global VERSION %{version}
# Openprinting version
%global OP_VER op2
%bcond_with missing_dependencies
Summary:        CUPS printing system
Name:           cups
Version:        2.3.3%{OP_VER}
Release:        5%{?dist}
License:        ASL 2.0 with exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.cups.org/
# Apple stopped uploading the new versions into github, use OpenPrinting fork
Source0:        https://github.com/OpenPrinting/cups/releases/download/v%{VERSION}/cups-%{VERSION}-source.tar.gz
# Pixmap for desktop file
Source1:        cupsprinter.png
# cups_serverbin macro definition for use during builds
Source2:        macros.cups
# selinux and audit enablement for CUPS - needs work and CUPS upstream wants
# to have these features implemented their way in the future
Patch100:       cups-lspp.patch
# PAM enablement, very old patch, not even git can track when or why
# the patch was added.
Patch1:         cups-system-auth.patch
# cups-config from devel package conflicted on multilib arches,
# fixed hack with pkg-config calling for gnutls' libdir variable
Patch2:         cups-multilib.patch
# if someone makes a change to banner files, then there will <banner>.rpmnew
# with next update of cups-filters - this patch makes sure the banner file
# changed by user is used and .rpmnew or .rpmsave is ignored
# Note: This could be rewrite with use a kind of #define and send to upstream
Patch3:         cups-banners.patch
# don't export ssl libs to cups-config - can't find the reason.
Patch4:         cups-no-export-ssllibs.patch
# enables old uri usb:/dev/usb/lp0 - leave it here for users of old printers
Patch5:         cups-direct-usb.patch
# when system workload is high, timeout for cups-driverd can be reached -
# increase the timeout
Patch6:         cups-driverd-timeout.patch
# usb backend didn't get any notification about out-of-paper because of kernel
Patch7:         cups-usb-paperout.patch
# uri compatibility with old Fedoras
Patch8:         cups-uri-compat.patch
# use IP_FREEBIND, because cupsd cannot bind to not yet existing IP address
# by default
Patch9:         cups-freebind.patch
# add support of multifile
Patch10:        cups-ipp-multifile.patch
# prolongs web ui timeout
Patch11:        cups-web-devices-timeout.patch
# failover backend for implementing failover functionality
# TODO: move it to the cups-filters upstream
Patch12:        cups-failover-backend.patch
# add device id for dymo printer
Patch13:        cups-dymo-deviceid.patch
#### UPSTREAM PATCHES (starts with 1000) ####
##### Patches removed because IMHO they aren't no longer needed
##### but still I'll leave them in git in case their removal
##### breaks something.
BuildRequires:  automake
# gcc and gcc-c++ is no longer in buildroot by default
# gcc for most of files
BuildRequires:  gcc
# gcc-c++ for ppdc and cups-driverd
BuildRequires:  gcc-c++
BuildRequires:  krb5-devel
BuildRequires:  libacl-devel
# make is used for compilation
BuildRequires:  make
BuildRequires:  openldap-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconf-pkg-config
# Make sure we get postscriptdriver tags.
#BuildRequires: python3-cups
BuildRequires:  systemd-devel
# needed for systemd rpm macros according FPG
BuildRequires:  systemd-rpm-macros
# needed for decompressing functions when reading from gzipped ppds
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(avahi-client)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libusb-1.0)
%if %{lspp}
BuildRequires:  audit-libs-devel
BuildRequires:  libselinux-devel
%endif
Requires:       %{name}-client = %{version}-%{release}
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
# We ship udev rules which use setfacl.
Requires:       acl
Requires:       dbus
Requires:       systemd
Requires(post): grep
Requires(post): sed
Requires(post): systemd
Requires(postun): systemd
# Requires working PrivateTmp (bug #807672)
Requires(pre):  systemd
Requires(preun): systemd
# avahi is needed for mDNS discovery and sharing queues
Recommends:     avahi
# getaddrinfo from glibc needs nss-mdns or systemd-resolved for resolving
# mdns .local addresses. Don't require a specific package for now and let
# the user to decide what to use
# just recommend nss-mdns for Fedora for now to have working default, but
# don't hardwire it for resolved users
Recommends:     nss-mdns
# Make sure we have some filters for converting to raster format.
%if 0%{with missing_dependencies}
Requires:       cups-filters
%endif

%description
CUPS printing system provides a portable printing layer for
UNIX® operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.

%package        client
Summary:        CUPS printing system - client programs
License:        ASL 2.0 with exceptions
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       lpr
%if %{use_alternatives}
Requires:       %{_sbindir}/alternatives
Provides:       %{_bindir}/lpq
Provides:       %{_bindir}/lpr
Provides:       %{_bindir}/lp
Provides:       %{_bindir}/cancel
Provides:       %{_bindir}/lprm
Provides:       %{_bindir}/lpstat
%endif

%description client
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This package contains command-line client
programs.

%package        devel
Summary:        CUPS printing system - development environment
License:        ASL 2.0 with exceptions
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       gnutls-devel
Requires:       krb5-devel
Requires:       zlib-devel

%description devel
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.

%package        libs
Summary:        CUPS printing system - libraries
License:        ASL 2.0 with exceptions and zlib

%description libs
CUPS printing system provides a portable printing layer for
UNIX® operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.
The cups-libs package provides libraries used by applications to use CUPS
natively, without needing the lp/lpr commands.

%package        filesystem
Summary:        CUPS printing system - directory layout
License:        ASL 2.0 with exceptions
BuildArch:      noarch

%description filesystem
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This package provides some directories which are
required by other packages that add CUPS drivers (i.e. filters, backends etc.).

%package        lpd
Summary:        CUPS printing system - lpd emulation
License:        ASL 2.0 with exceptions
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       lpd

%description lpd
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This is the package that provides standard
lpd emulation.

%package        ipptool
Summary:        CUPS printing system - tool for performing IPP requests
License:        ASL 2.0 with exceptions
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# ippfind needs avahi for printer discovery
Requires:       avahi
# mdns address resolver (nss-mdns or systemd-resolved) is needed too,
# but don't require a specific package for now and let the user to choose
# what to use
# just recommend nss-mdns for Fedora for now to have working default, but
# don't hardwire it for resolved users
Recommends:     nss-mdns

%description ipptool
Sends IPP requests to the specified URI and tests and/or displays the results.

%package        printerapp
Summary:        CUPS printing system - tools for printer application
License:        ASL 2.0 with exceptions
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# ippeveprinter needs avahi for registering and sharing printer
Requires:       avahi
# mdns address resolver (nss-mdns or systemd-resolved) is needed too,
# but don't require a specific package for now and let the user to choose
# what to use
# just recommend nss-mdns for Fedora for now to have working default, but
# don't hardwire it for resolved users
Recommends:     nss-mdns

%description printerapp
Provides IPP everywhere printer application ippeveprinter and tools for printing
PostScript and HP PCL document formats - ippevepcl and ippeveps. The printer
application enables older printers for IPP everywhere standard - so if older printer
is installed with a printer application, its print queue acts as IPP everywhere printer
to CUPS daemon. This solution will substitute printer drivers and raw queues in the future.

%prep
%setup -q -n cups-%{VERSION}
# Use the system pam configuration.
%patch1 -p1 -b .system-auth
# Prevent multilib conflict in cups-config script.
%patch2 -p1 -b .multilib
# Ignore rpm save/new files in the banners directory.
%patch3 -p1 -b .banners
# Don't export SSLLIBS to cups-config.
%patch4 -p1 -b .no-export-ssllibs
# Allow file-based usb device URIs.
%patch5 -p1 -b .direct-usb
# Increase driverd timeout to 70s to accommodate foomatic (bug #744715).
%patch6 -p1 -b .driverd-timeout
# Support for errno==ENOSPACE-based USB paper-out reporting.
%patch7 -p1 -b .usb-paperout
# Allow the usb backend to understand old-style URI formats.
%patch8 -p1 -b .uri-compat
# Use IP_FREEBIND socket option when binding listening sockets (bug #970809).
%patch9 -p1 -b .freebind
# Fixes for jobs with multiple files and multiple formats.
%patch10 -p1 -b .ipp-multifile
# Increase web interface get-devices timeout to 10s (bug #996664).
%patch11 -p1 -b .web-devices-timeout
# Add failover backend (bug #1689209)
%patch12 -p1 -b .failover
# Added IEEE 1284 Device ID for a Dymo device (bug #747866).
%patch13 -p1 -b .dymo-deviceid

# UPSTREAM PATCHES


# LSPP support.
%patch100 -p1 -b .lspp


# Log to the system journal by default (bug #1078781, bug #1519331).
sed -i -e 's,^ErrorLog .*$,ErrorLog syslog,' conf/cups-files.conf.in
sed -i -e 's,^AccessLog .*$,AccessLog syslog,' conf/cups-files.conf.in
sed -i -e 's,^PageLog .*,PageLog syslog,' conf/cups-files.conf.in

# Let's look at the compilation command lines.
perl -pi -e "s,^.SILENT:,," Makedefs.in

# remove this once we don't have any patches changing configure stuff
aclocal -I config-scripts
autoconf -f -I config-scripts

%build
# cups can use different compiler if it is installed, so set to GCC for to be sure
export CC=%{__cc}
export CXX=%{__cxx}
# add Mariner specific flags to DSOFLAGS
export DSOFLAGS="$DSOFLAGS -L../cgi-bin -L../filter -L../ppdc -L../scheduler -Wl,-z,relro -Wl,-z,now -specs=%{_libdir}/rpm/mariner/default-hardened-ld -Wl,-z,relro,-z,now -fPIE -pie"
export CFLAGS="%{optflags} -fstack-protector-all -DLDAP_DEPRECATED=1"
# --enable-debug to avoid stripping binaries
%configure --with-docdir=%{_datadir}/%{name}/www --enable-debug \
%if %{lspp}
	--enable-lspp \
%endif
  --with-exe-file-perm=0755 \
	--with-cupsd-file-perm=0755 \
	--with-log-file-perm=0600 \
	--enable-relro \
	--with-dbusdir=%{_sysconfdir}/dbus-1 \
	--with-php=%{_bindir}/php-cgi \
	--enable-avahi \
	--enable-threads \
	--enable-gnutls \
	--enable-webif \
	--with-xinetd=no \
	--with-access-log-level=actions \
	--enable-page-logging \
	--with-rundir=%{_rundir}/cups \
	--enable-sync-on-close \
	localedir=%{_datadir}/locale

# If we got this far, all prerequisite libraries must be here.
%make_build

%install
# %%make_install macro results into permission error during install phase,
# because it sets INSTALL env to 'install -p'.
# use the old make invocation for now, fix this upstream when upstream will
# have a time for github issues
make install DESTDIR=%{buildroot}

rm -rf	%{buildroot}%{_initddir} \
	%{buildroot}%{_sysconfdir}/init.d \
	%{buildroot}%{_sysconfdir}/rc?.d
mkdir -p %{buildroot}%{_unitdir}

find %{buildroot}%{_datadir}/cups/model -name "*.ppd" |xargs gzip -n9f

%if %{use_alternatives}
pushd %{buildroot}%{_bindir}
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i $i.cups
done
cd %{buildroot}%{_sbindir}
mv lpc lpc.cups
cd %{buildroot}%{_mandir}/man1
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i.1 $i-cups.1
done
cd %{buildroot}%{_mandir}/man8
mv lpc.8 lpc-cups.8
popd
%endif

mkdir -p %{buildroot}%{_datadir}/pixmaps %{buildroot}%{_sysconfdir}/X11/sysconfig %{buildroot}%{_sysconfdir}/X11/applnk/System
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps

# Ship an rpm macro for where to put driver executables.
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d

# Ship a printers.conf file, and a client.conf file.  That way, they get
# their SELinux file contexts set correctly.
touch %{buildroot}%{_sysconfdir}/cups/printers.conf
touch %{buildroot}%{_sysconfdir}/cups/classes.conf
touch %{buildroot}%{_sysconfdir}/cups/client.conf
touch %{buildroot}%{_sysconfdir}/cups/subscriptions.conf
touch %{buildroot}%{_sysconfdir}/cups/lpoptions

# LSB 3.2 printer driver directory
mkdir -p %{buildroot}%{_datadir}/ppd

# Remove unshipped files.
rm -rf %{buildroot}%{_mandir}/cat? %{buildroot}%{_mandir}/*/cat?
rm -f %{buildroot}%{_datadir}/applications/cups.desktop
rm -rf %{buildroot}%{_datadir}/icons
# there are pdf-banners shipped with cups-filters (#919489)
rm -rf %{buildroot}%{_datadir}/cups/banners
rm -f %{buildroot}%{_datadir}/cups/data/testprint

# install /usr/lib/tmpfiles.d/cups.conf (bug #656566, bug #893834)
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/cups.conf <<EOF
# See tmpfiles.d(5) for details

d %{_rundir}/cups 0755 root lp -
d %{_rundir}/cups/certs 0511 lp sys -

d %{_var}/spool/cups/tmp - - - 30d
EOF

# /usr/lib/tmpfiles.d/cups-lp.conf (bug #812641)
cat > %{buildroot}%{_tmpfilesdir}/cups-lp.conf <<EOF
# Legacy parallel port character device nodes, to trigger the
# auto-loading of the kernel module on access.
#
# See tmpfiles.d(5) for details

c /dev/lp0 0660 root lp - 6:0
c /dev/lp1 0660 root lp - 6:1
c /dev/lp2 0660 root lp - 6:2
c /dev/lp3 0660 root lp - 6:3
EOF

# create server.conf into cups.service.d directory. The file is needed
# to automatically start cups.service during startup if enabled
mkdir -p %{buildroot}%{_unitdir}/cups.service.d
cat > %{buildroot}%{_unitdir}/cups.service.d/server.conf <<EOF
[Install]
WantedBy=multi-user.target
EOF

find %{buildroot} -type f -o -type l | sed '
s:.*\('%{_datadir}'/\)\([^/_]\+\)\(.*\.po$\):%lang(\2) \1\2\3:
/^%lang(C)/d
/^\([^%].*\)/d
' > %{name}.lang

%post
%systemd_post %{name}.path %{name}.socket %{name}.service

# Because of moving logs to journal, we need to create placeholder files
# at /var/log/cups for users, whose are going to install CUPS on new OS
# machine with info message

confignames=( "ErrorLog" "AccessLog" "PageLog" )
lognames=( "error_log" "access_log" "page_log" )
message="This CUPS log has been moved into journal by default unless changes have     been made in %{_sysconfdir}/cups/cups-files.conf. Log messages can be got by \"$ journalctl -u  cups -e\""
for ((i=0;i<${#confignames[@]};i++));
do
  found=`%{_bindir}/grep -i "${confignames[i]} syslog" %{_sysconfdir}/cups/cups-files.conf`
  if [ ! -z "$found" ]
  then
    if [ ! -f %{_localstatedir}/log/cups/${lognames[i]} ]
    then
      %{_bindir}/touch %{_localstatedir}/log/cups/${lognames[i]} || :
    fi
    perms=`%{_bindir}/ls -lah %{_localstatedir}/log/cups/${lognames[i]} | %{_bindir}/grep -v -e "\-rw-------" -e "root lp"`
    if [ ! -z "$perms" ]
    then
      # we need to set correct permissions and ownership because of possible
      # security issues
      # we need to have it here, because previous CUPS releases had the bug.
      # Checking permissions and ownership here fixes it.
      %{_bindir}/chown root:lp %{_localstatedir}/log/cups/${lognames[i]} || :
      %{_bindir}/chmod 600 %{_localstatedir}/log/cups/${lognames[i]} || :
    fi
    lastmessage=`%{_bindir}/tail -n 1 %{_localstatedir}/log/cups/${lognames[i]} | %{_bindir}/grep "$message"`
    if [ -z "$lastmessage" ]
    then
      %{_bindir}/echo $message >> %{_localstatedir}/log/cups/${lognames[i]} || :
    fi
  fi
done

%post client
%if %{use_alternatives}
%{_sbindir}/alternatives --install %{_bindir}/lpr print %{_bindir}/lpr.cups 40 \
	 --slave %{_bindir}/lp print-lp %{_bindir}/lp.cups \
	 --slave %{_bindir}/lpq print-lpq %{_bindir}/lpq.cups \
	 --slave %{_bindir}/lprm print-lprm %{_bindir}/lprm.cups \
	 --slave %{_bindir}/lpstat print-lpstat %{_bindir}/lpstat.cups \
	 --slave %{_bindir}/cancel print-cancel %{_bindir}/cancel.cups \
	 --slave %{_sbindir}/lpc print-lpc %{_sbindir}/lpc.cups \
	 --slave %{_mandir}/man1/cancel.1.gz print-cancelman %{_mandir}/man1/cancel-cups.1.gz \
	 --slave %{_mandir}/man1/lp.1.gz print-lpman %{_mandir}/man1/lp-cups.1.gz \
	 --slave %{_mandir}/man8/lpc.8.gz print-lpcman %{_mandir}/man8/lpc-cups.8.gz \
	 --slave %{_mandir}/man1/lpq.1.gz print-lpqman %{_mandir}/man1/lpq-cups.1.gz \
	 --slave %{_mandir}/man1/lpr.1.gz print-lprman %{_mandir}/man1/lpr-cups.1.gz \
	 --slave %{_mandir}/man1/lprm.1.gz print-lprmman %{_mandir}/man1/lprm-cups.1.gz \
	 --slave %{_mandir}/man1/lpstat.1.gz print-lpstatman %{_mandir}/man1/lpstat-cups.1.gz
%endif

%post lpd
%systemd_post cups-lpd.socket

%ldconfig_scriptlets libs

%preun
%systemd_preun %{name}.path %{name}.socket %{name}.service

%preun client
%if %{use_alternatives}
if [ $1 -eq 0 ] ; then
	%{_sbindir}/alternatives --remove print %{_bindir}/lpr.cups
fi
%endif

%preun lpd
%systemd_preun cups-lpd.socket

%postun
# ignore the messages due #1614751 (systemd bug)
%systemd_postun_with_restart %{name}.path %{name}.socket %{name}.service > /dev/null 2>&1

%postun lpd
%systemd_postun_with_restart cups-lpd.socket

%triggerin -- samba-client
ln -sf %{_libexecdir}/samba/cups_backend_smb %{cups_serverbin}/backend/smb || :

%triggerun -- samba-client
[ $2 = 0 ] || exit 0
rm -f %{cups_serverbin}/backend/smb

%files -f %{name}.lang
%doc README.md CREDITS.md CHANGES.md
%{_bindir}/cupstestppd
%{_bindir}/ppd*
%{_sbindir}/*
# client subpackage
%exclude %{_sbindir}/lpc.cups
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-deviced
%{cups_serverbin}/daemon/cups-driverd
%{cups_serverbin}/daemon/cups-exec
%{cups_serverbin}/backend/*
%{cups_serverbin}/cgi-bin
%{cups_serverbin}/filter/*
%{cups_serverbin}/monitor
%{cups_serverbin}/notifier
%{_datadir}/cups/drv/sample.drv
%{_datadir}/cups/examples
%{_datadir}/cups/mime/mime.types
%{_datadir}/cups/mime/mime.convs
%{_datadir}/cups/ppdc/*.defs
%{_datadir}/cups/ppdc/*.h
%dir %{_datadir}/cups/templates
%{_datadir}/cups/templates/*.tmpl
%dir %{_datadir}/cups/templates/de
%{_datadir}/cups/templates/de/*.tmpl
%dir %{_datadir}/cups/templates/es
%{_datadir}/cups/templates/es/*.tmpl
%dir %{_datadir}/cups/templates/fr
%{_datadir}/cups/templates/fr/*.tmpl
%dir %{_datadir}/cups/templates/ja
%{_datadir}/cups/templates/ja/*.tmpl
%dir %{_datadir}/cups/templates/pt_BR
%{_datadir}/cups/templates/pt_BR/*.tmpl
%dir %{_datadir}/cups/templates/ru
%{_datadir}/cups/templates/ru/*.tmpl
%dir %{_datadir}/%{name}/usb
%{_datadir}/%{name}/usb/org.cups.usb-quirks
%dir %{_datadir}/%{name}/www
%{_datadir}/%{name}/www/images
%{_datadir}/%{name}/www/*.css
# 1658673 - html files cannot be docs, because CUPS web ui will not have
# introduction page on Fedora Docker image (because rpms are installed
# without docs there because of space reasons)
%{_datadir}/%{name}/www/index.html
%{_datadir}/%{name}/www/help
%{_datadir}/%{name}/www/robots.txt
%{_datadir}/%{name}/www/de/index.html
%{_datadir}/%{name}/www/es/index.html
%{_datadir}/%{name}/www/ja/index.html
%{_datadir}/%{name}/www/ru/index.html
%{_datadir}/%{name}/www/pt_BR/index.html
%{_datadir}/%{name}/www/apple-touch-icon.png
%dir %{_datadir}/%{name}/www/de
%dir %{_datadir}/%{name}/www/es
%dir %{_datadir}/%{name}/www/ja
%dir %{_datadir}/%{name}/www/pt_BR
%dir %{_datadir}/%{name}/www/ru
%{_datadir}/pixmaps/cupsprinter.png
%dir %attr(1770,root,lp) %{_localstatedir}/spool/cups/tmp
%dir %attr(0710,root,lp) %{_localstatedir}/spool/cups
%dir %attr(0755,lp,sys) %{_localstatedir}/log/cups
%{_mandir}/man[1578]/*
# client subpackage
%exclude %{_mandir}/man1/lp*.1.gz
%exclude %{_mandir}/man1/cancel-cups.1.gz
%exclude %{_mandir}/man8/lpc-cups.8.gz
# devel subpackage
%exclude %{_mandir}/man1/cups-config.1.gz
# ipptool subpackage
%exclude %{_mandir}/man1/ipptool.1.gz
%exclude %{_mandir}/man5/ipptoolfile.5.gz
# lpd subpackage
%exclude %{_mandir}/man8/cups-lpd.8.gz
# printerapp
%exclude %{_mandir}/man1/ippeveprinter.1.gz
%exclude %{_mandir}/man7/ippevepcl.7.gz
%exclude %{_mandir}/man7/ippeveps.7.gz
%dir %attr(0755,root,lp) %{_rundir}/cups
%dir %attr(0511,lp,sys) %{_rundir}/cups/certs
%dir %attr(0755,root,lp) %{_sysconfdir}/cups
%attr(0640,root,lp) %{_sysconfdir}/cups/cupsd.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/cupsd.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/cups-files.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/cups-files.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/client.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) %{_sysconfdir}/cups/classes.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) %{_sysconfdir}/cups/printers.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/snmp.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/snmp.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/subscriptions.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/lpoptions
%dir %attr(0755,root,lp) %{_sysconfdir}/cups/ppd
%dir %attr(0700,root,lp) %{_sysconfdir}/cups/ssl
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/cups.conf
%config(noreplace) %{_sysconfdir}/pam.d/cups
%{_tmpfilesdir}/cups.conf
%{_tmpfilesdir}/cups-lp.conf
%dir %{_unitdir}/%{name}.service.d
%attr(0644, root, root)%{_unitdir}/%{name}.service.d/server.conf
%attr(0644, root, root)%{_unitdir}/%{name}.service
%attr(0644, root, root)%{_unitdir}/%{name}.socket
%attr(0644, root, root)%{_unitdir}/%{name}.path

%files client
%{_bindir}/cancel*
%{_bindir}/lp*
%{_sbindir}/lpc.cups
%{_mandir}/man1/cancel-cups.1.gz
%{_mandir}/man1/lp*.1.gz
%{_mandir}/man8/lpc-cups.8.gz

%files libs
%license LICENSE NOTICE
%{_libdir}/libcups.so.2
%{_libdir}/libcupsimage.so.2

%files filesystem
%dir %{cups_serverbin}
%dir %{cups_serverbin}/backend
%dir %{cups_serverbin}/driver
%dir %{cups_serverbin}/filter
%dir %{_datadir}/cups
%dir %{_datadir}/cups/data
%dir %{_datadir}/cups/drv
%dir %{_datadir}/cups/mime
%dir %{_datadir}/cups/model
%dir %{_datadir}/cups/ppdc
%dir %{_datadir}/ppd

%files devel
%{_bindir}/cups-config
%{_includedir}/cups
%{_libdir}/*.so
%{_mandir}/man1/cups-config.1.gz
%{_rpmconfigdir}/macros.d/macros.cups

%files lpd
%{cups_serverbin}/daemon/cups-lpd
%{_mandir}/man8/cups-lpd.8.gz
%attr(0644, root, root)%{_unitdir}/cups-lpd.socket
%attr(0644, root, root)%{_unitdir}/cups-lpd@.service

%files ipptool
%{_bindir}/ippfind
%{_bindir}/ipptool
%dir %{_datadir}/cups/ipptool
%{_datadir}/cups/ipptool/*
%{_mandir}/man1/ipptool.1.gz
%{_mandir}/man5/ipptoolfile.5.gz

%files printerapp
%{_bindir}/ippeveprinter
%dir %{cups_serverbin}/command
%{cups_serverbin}/command/ippevepcl
%{cups_serverbin}/command/ippeveps
%{_mandir}/man1/ippeveprinter.1.gz
%{_mandir}/man7/ippevepcl.7.gz
%{_mandir}/man7/ippeveps.7.gz

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.3.3op2-5
- License verified
- Lint spec

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.3.3op2-4
- Remove epoch

* Wed Aug 25 2021 Muhammad Falak <mwani@microsoft.com> - 1:2.3.3op2-3
- Temporarily remove dependency on `cups-filters` to enable build

* Thu Mar 18 2021 Henry Li <lihl@microsoft.com> - 1:2.3.3op2-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Disable python3-cups from BuildRequires to circumvent circular dependency
- Pass the Mariner specific flags: default-hardened-ld to DSOFLAGS

* Tue Feb 02 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3op2-1
- 1923828 - cups-2.3.3op2 is available

* Mon Feb 01 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3op1-4
- fix for CVE-2020-10001
- recommend nss-mdns for Fedora to have a working default for now
- 1921881 - [abrt] cups: __strcmp_avx2(): help.cgi killed by SIGSEGV
- 1909980 - cupsd crashes on parsing malformed Brother PPD

* Thu Jan 28 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3op1-3
- remove nss-mdns dependency - let the user decide whether use resolved or nss-mdns
- remove cups dependency on cups-ipptool - actually not needed

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.3op1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3op1-1
- 2.3.3op1

* Fri Nov 27 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-20
- make unit files writeable by root
- remove %%post scriptlet - it is covered by drop-in now
- remove cups-filter-debug.patch
- backport cups-synconclose.patch from upstream

* Thu Nov 26 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-20
- remove downstream autostart patch - use systemd drop-in

* Tue Nov 24 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-20
- fix memory leak during device discovery
- remove logrotate patches and support - journal is now default
- remove eggcups patch - seems to cause no harm
- journal is in Fedora for long time - no need to mention it is Fedora syslog
- fix packaging of printerapp manpages
- wheel is now in system groups by default
- remove old scripts for older migrations
- CREDITS is now in markdown format, so we don't need to convert
- fix requires on nss-mdns for cups-printerapp
- take SNMP OID from upstream
- rename unit files and update their patches

* Thu Nov 12 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-19
- 1897023 - Cups service restart sequence during upgrade incorrect

* Tue Nov 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-18
- 1892426 - Crash:free(): invalid pointer in cups backend

* Thu Nov 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-17
- make is no longer in buildroot

* Mon Nov 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-16
- backport cups-ipptool-mdns-uri.patch from upstream
- backport cups-prioritize-print-color-mode.patch from upstream

* Thu Sep 03 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-14
- revert previous commit - resolved doesn't work with avahi due missing link
  in NetworkManager

* Mon Aug 31 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-14
- MDNS resolving should be done by systemd-resolved now

* Mon Aug 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-14
- CUPS exception isn't in spdx database, use only ASL 2.0

* Wed Aug 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-13
- own 'new' directories

* Tue Aug 04 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-12
- typo in DESTDIR during 'make install'

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.3-11
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-9
- use %%make_build and %%make_install macros

* Mon Jul 20 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-8
- 1848575 - [cups, cups-filters] PPD generators creates invalid cupsManualCopies entry

* Fri Jul 17 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-7
- spec cleanup

* Thu Jun 11 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-6
- fix patch errors in failover patch
- cgi script creates a bad uri in web ui
- ipptool doesn't support mdns uris

* Tue Jun 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-5
- remove os ci tests, we use baseos ci

* Fri May 22 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-4
- fix space errors in failover patch

* Thu May 21 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-3
- use _rundir instead of hardcode /run

* Wed May 20 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-2
- 1838455 - ipp/socket backends connect to turned off device for eternity (contimeout is not applied)

* Tue May 19 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.3-1
- 2.3.3

* Tue Apr 21 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.1-9
- 1826330 - CVE-2020-3898 cups: heap based buffer overflow in libcups's ppdFindOption() in ppd-mark.c

* Wed Apr 08 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.1-8
- 1822154 - cups.service doesn't execute automatically on request

* Mon Apr 06 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.1-7
- make avahi and nss-mdns recommended in main package - so users with older printers
  can install cups without it

* Fri Mar 20 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.1-6
- add requires on nss-mdns, because getaddrinfo needs it for resolving .local addresses

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Tom Stellard <tstellar@redhat.com> - 1:2.3.1-4
- Replace hard-coded gcc and g++ with __cc and __cxx macros

* Wed Jan 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.1-3
- add buildrequires on systemd-rpm-macros

* Thu Jan 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.1-2
- do not ship ipp backend as 755, breaks kerberized printing
- https://github.com/apple/cups/pull/5710

* Mon Dec 16 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.1-1
- 2.3.1

* Fri Nov 29 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.0-2
- 1777921 - cups unit file makes systemd to complain

* Mon Nov 18 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.3.0-1
- 2.3.0 - new printerapp subpackage

* Wed Oct 16 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.12-3
- 1720688 - [abrt] cups: __strlen_avx2(): printers.cgi killed by SIGSEGV
- 1750904 - cups is unable to add ppd with custom/Custom option

* Fri Sep 13 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.12-2
- fix cupsctl usage

* Mon Aug 19 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.12-1
- 2.2.12

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.11-3
- 1708988 - Samsung ML-1676P Laser printer fails to print document

* Wed Apr 17 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.11-2
- 1700664 - Stop advertising the HTTP methods that are supported

* Tue Mar 26 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.11-1
- 2.2.11

* Fri Mar 15 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.10-5
- 1689209 - Add failover backend

* Tue Feb 19 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.10-4
- automake sometimes fails to generate correct macros - so force it

* Tue Feb 05 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.10-3
- 1672715 - cups fails to build if clang is installed

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.10-1
- 2.2.10, libcupsmime, libcupsppdc and libcupscgi libraries were removed

* Fri Dec 14 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-10
- previous commit - fix for previous releases

* Thu Dec 13 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-9
- logs need to have correct permissions

* Wed Dec 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-8
- 1658673 - Main index.html of web interface doesn't get installed when not installing documentation

* Mon Dec 10 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-7
- 1657750 - CVE-2018-4700 cups: Predictable session cookie breaks CSRF protection [fedora-all]

* Fri Nov 09 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-6
- 1622432 - Jobs with multiple files don't complete when backend fails
- 1648396 - 'cupsd[998]: [CGI] Unable to execute ippfind utility: No such file or directory' in journal

* Fri Sep 21 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-5
- fixed coverity issues

* Wed Sep 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-4
- 1618018 - Make cups systemd unit files more upstream-like

* Tue Jul 24 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-3
- correcting license

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.8-1
- 2.2.8, removing several downstream patches, adding some upstream patches

* Tue Jun 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.7-2
- 1589593 - cupsd LogLevel ignored when logging to journald (syslog)
- 1590123 - cups-driverd doesn't recognize static gzipped ppds

* Tue Apr 03 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.7-1
- rebase to 2.2.7 
- substitute default values for invalid job attributes (upstream issues #5229 and #5186)

* Thu Mar 29 2018 Pavel Zhukov <pzhukov@redhat.com> - 1:2.2.6-13
- Use dbus fix instead of general attr delete (upstream)

* Wed Mar 28 2018 Pavel Zhukov <pzhukov@redhat.com> - 1:2.2.6-12
- Fix for CVE-2017-18248

* Wed Feb 28 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-11
- remake of 1499261

* Wed Feb 28 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-10
- mention library names explicitly to warn about soname change

* Tue Feb 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-9
- 1548120 - cups: Partial injection of Fedora build flags

* Mon Feb 26 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-8
- pkgconfig is now shipped in pkgconf-pkg-config package

* Tue Feb 20 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-7
- 1499261 - Move log files into journal

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-6
- gcc and gcc-c++ is not in buildroot by default now

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:2.2.6-4
- Switch to %%ldconfig_scriptlets

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1:2.2.6-3
- Rebuilt for switch to libxcrypt

* Fri Jan 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-2
- 1437345 - Remove cups-resolv_reload.patch

* Fri Nov 03 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.6-1
- rebase to 2.2.6

* Tue Oct 17 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.5-1
- rebase to 2.2.5

* Mon Oct 09 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.4-7
- removing ghostscript-cups dependency - cups-filters ships it

* Wed Oct 04 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.4-6
- 1498091 - Cannot browse CUPS servers in GNOME Control Panel Printers

* Mon Oct 02 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.4-5
- 1484916 - Can not get destinations from CUPS server

* Fri Sep 22 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.4-4
- 1494558 - CUPS may fail to start if NIS groups are used

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.4-1
- rebase to 2.2.4

* Thu Jun 29 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.3-6
- update python dependencies accordingly Fedora Guideline for Python (python-cups -> python3-cups)

* Thu Apr 27 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.3-5
- copying cups-resolv_reload.patch from RHEL

* Wed Apr 05 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.3-4
- fixing issue with #1437065 - makes res_init() call to local resolver and keeps error message, but no hard exit for cupsd

* Tue Apr 04 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.3-3
- disable patch for #1437065 for now until issue with stat is solved

* Thu Mar 30 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.3-2
- 1437065 - CUPS does not recognize changes to /etc/resolv.conf until CUPS restart 

* Wed Mar 29 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.3-1
- rebase to 2.2.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.2-1
- rebase to 2.2.2

* Wed Jan 11 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.1-4
- bug 1405669 - adding group wheel to SystemGroup

* Fri Nov 11 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.1-3
- Unable to print from Windows (7) on a Cups-Server(2.2.1-1) with german umlauts in the filename (bug #1386751)

* Mon Nov 07 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.1-2
- #873123 - (cups-usb-quirks) usb printer doesn't print (usblp0: USB Bidirectional printer dev)

* Tue Oct 04 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.1-1
- rebase to 2.2.1

* Thu Sep 22 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2.0-2
- fixing looping in partial failing service (bug #1366775)

* Thu Sep 15 2016 Jiri Popelka <jpopelka@redhat.com> - 1:2.2.0-1
- 2.2.0

* Fri Aug 12 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2-0.4rc1
- fixing release number 

* Tue Aug 09 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2-0.2rc1
- rebase to cups-2.2rc1

* Wed Aug 03 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2-0.2b2
- bug 1358589 - added information about syslog means systemd journal by default

* Mon Jun 27 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.2-0.1b2
- Rebase to 2.2b2, editing patches and spec (no need for /etc/cups/interfaces)

* Mon Jun 27 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.4-1
- substitution BuildRequires: pkgconfig(libsystemd-*) for BuildRequires: pkgconfig(libsystemd)

* Wed Jun 15 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.4-1
- 2.1.4, 1346668 - Change symlink for smb backend to /usr/libexec/samba/cups_backend_smb

* Mon Feb 08 2016 Jiri Popelka <jpopelka@redhat.com> - 1:2.1.3-1
- 2.1.3

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.1.2-1
- 2.1.2 - interface scripts support is back (until 2.2)

* Tue Dec 01 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.1.1-1
- 2.1.1 - interface scripts no longer supported.

* Mon Nov 02 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.1.0-2
- Change mode of subscriptions.conf from 644 to 640 (bug #1259770).

* Tue Sep 01 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.1.0-1
- 2.1.0

* Thu Aug 13 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.1-0.3rc1
- fix crash in scheduler (#1253135)

* Mon Aug 10 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.1-0.2rc1
- better fix for STR#4687

* Mon Aug 10 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.1-0.1rc1
- 2.1rc1

* Mon Aug 10 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.4-1
- 2.0.4

* Tue Jul 28 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.3-5
- BuildRequires: gnutls-devel -> pkgconfig(gnutls)

* Tue Jul 07 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.3-4
- RPM_BUILD_ROOT -> %%{buildroot}, put braces around lspp and use_alternatives

* Thu Jun 25 2015 Tim Waugh <twaugh@redhat.com> - 1:2.0.3-3
- Fix slow resume of jobs after restart (STR #4646).
- Fix redirection from CGI scripts (bug #1232030, STR #4538).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.3-1
- 2.0.3

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:2.0.2-6
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 16 2015 Tim Waugh <twaugh@redhat.com> - 1:2.0.2-5
- Avoid busy loop in cupsd when connection is closed after request
  sent (bug #1179596).

* Mon Feb 16 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.2-2
- Fixed multilib.patch to check for gnutls instead of openssl.

* Tue Feb 10 2015 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.2-1
- 2.0.2

* Tue Jan 27 2015 Tim Waugh <twaugh@redhat.com> - 1:2.0.1-2
- Fixed systemd notify support (bug #1184453).

* Sat Nov 15 2014 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.1-1
- 2.0.1

* Fri Nov  7 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-12
- Re-introduce SSLOptions configuration directive, disable SSL3 by
  default (STR #4476).
- Enable SSL again via GnuTLS (bug #1161235).

* Thu Nov  6 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-11
- Removed openssl requirements from spec file as it is no longer
  supported upstream (see bug #1161235).

* Thu Nov  6 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-10
- cups-lspp.patch: use cupsdLogJob() when appropriate.
- Fixed some warnings in cups-lspp.patch.
- New systemd journal fields CUPS_DEST and CUPS_PRINTER, as well as
  accurate code location fields.

* Wed Oct 22 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-9
- Upstream fix for cupsd crash on restart when colord not available
- (STR #4496).

* Sat Oct 18 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-7
- Fix for last fix (bug #1153660, bug #1154284).

* Thu Oct 16 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-6
- Start cupsd systemd service after network.target (bug #1153660).

* Wed Oct 15 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-5
- Fix cupsGetPPD3() so it doesn't give the caller an unreadable file
  (bug #1150917, STR #4500).

* Wed Oct 15 2014 Tim Waugh <twaugh@redhat.com> - 1:2.0.0-4
- Can no longer reproduce bug #1010580 so removing final-content-type
  patch as it causes issues for some backends (bug #1149244).

* Fri Oct 03 2014 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.0-3
- comment out unnecessary PageLogFormat from cups-files.conf (#1148995)

* Fri Oct 03 2014 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.0-2
- s/org.cups.cupsd/cups/ cups.service

* Wed Oct 01 2014 Jiri Popelka <jpopelka@redhat.com> - 1:2.0.0-1
- 2.0.0

* Fri Sep 12 2014 Jiri Popelka <jpopelka@redhat.com> - 1:2.0-0.1.rc1
- 2.0rc1

* Mon Sep  1 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.5-7
- Fix icon display in web interface during server restart (STR #4475).

* Mon Sep  1 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.5-6
- More STR #4461 fixes from upstream.

* Tue Aug 26 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.5-5
- Use upstream patch for STR #4461.

* Wed Aug 20 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.5-4
- Removed old one-off trigger now it's no longer needed.
- Run systemd postun script for path and socket unit files as well as
  the main service unit file.
- Upstream patch for STR #4396, pre-requisite for STR #2913 patch.
- Upstream patch for STR #2913 to limit Get-Jobs replies to 500 jobs
  (bug #421671).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.5-2
- Fix conf/log file reading for authenticated users (STR #4461).

* Fri Aug 01 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.5-1
- 1.7.5

* Wed Jul 23 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.4-3
- CVE-2014-5029, CVE-2014-5030, CVE-2014-5031 (#1122601)

* Wed Jul 23 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.4-2
- Fix CGI handling (STR #4454).

* Mon Jul 14 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.4-1
- 1.7.4: CVE-2014-3537

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.3-1
- 1.7.3
- str4386.patch merged upstream in STR #4403

* Fri May  9 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.2-3
- Another attempt at avoiding race condition when sending IPP requests
  (STR #4386, bug #1072952).

* Thu Apr 17 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.2-2
- Make cups.service Type=notify (bug #1088918).

* Mon Apr 14 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.2-1
- 1.7.2

* Fri Apr  4 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.1-11
- Log to the system journal by default (bug #1078781).

* Thu Apr  3 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.1-10
- libcups: avoid race condition when sending IPP requests (STR #4386,
  bug #1072952).

* Wed Apr 02 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.1-9
- New client subpackage containing command line client tools (bug #1002342).
- Removed unneeded Group tags.
- Removed 'Requires: /sbin/chkconfig'.
- Moved 'Provides: lpd' to lpd subpackage.

* Tue Mar 18 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.1-8
- Removed patch for STR #4386 as it does not work and causes problems
  instead (bug #1077239).

* Mon Mar 10 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.1-7
- BuildRequires: pkgconfig(foo) instead of foo-devel

* Thu Mar  6 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.1-6
- Track local default in cupsEnumDests() (STR #4332).
- libcups: avoid race condition when sending IPP requests (STR #4386).
- Prevent feedback loop when fetching error_log over HTTP (STR #4366).

* Wed Mar  5 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.1-5
- Fix for cupsEnumDest() 'removed' callbacks (bug #1054312, STR #4380).

* Mon Feb 17 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.1-4
- Document 'journal' logging target.

* Tue Feb 11 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.1-3
- Prevent dnssd backend exiting too early (bug #1026940, STR #4365).

* Mon Feb 03 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.1-2
- move macros.cups from /etc/rpm/ to /usr/lib/rpm/macros.d

* Wed Jan 08 2014 Jiri Popelka <jpopelka@redhat.com> - 1:1.7.1-1
- 1.7.1

* Wed Jan  8 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-11
- Apply upstream patch to improve cupsUser() (STR #4327).

* Tue Jan  7 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-10
- Removed cups-dbus-utf8.patch as no longer needed (see STR #4314).
- Return jobs in rank order when handling IPP-Get-Jobs (STR #4326).

* Thu Jan  2 2014 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-9
- dbus notifier: call _exit when handling SIGTERM (STR #4314).
- Use '-f' when using rm in %%setup section.
- Fixed avahi-no-threaded patch so it removes a call to
  avahi_threaded_poll_stop() (bug #1044602).

* Fri Dec 13 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-8
- Use string literal for format string in sd_journal_print call.

* Thu Nov 28 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-7
- Prevent USB timeouts causing incorrect print output (bug #1026914).

* Thu Nov 14 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-6
- Avoid stale lockfile in dbus notifier (bug #1026949).

* Thu Nov  7 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-5
- Use upstream patch for stringpool corruption issue (bug #974048).

* Mon Nov  4 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-4
- Adjusted commented out default for SyncOnClose in cups-files.conf.

* Thu Oct 31 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-3
- Set the default for SyncOnClose to Yes.

* Mon Oct 28 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-2
- Use upstream patch to fix job history.

* Thu Oct 24 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7.0-1
- 1.7.0.

* Thu Oct 24 2013 Tim Waugh <twaugh@redhat.com>
- Fix job history logging.

* Mon Oct 21 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.27.rc1
- Allow "journal" log type for log output to system journal.

* Fri Sep 27 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.26.rc1
- Reverted upstream change to FINAL_CONTENT_TYPE in order to fix
  printing to remote CUPS servers (bug #1010580).

* Wed Aug 21 2013 Jaromír Končický <jkoncick@redhat.com>
- Add SyncOnClose option (bug #984883).

* Fri Aug 16 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.25.rc1
- Increase web interface get-devices timeout to 10s (bug #996664).

* Thu Aug 15 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.24.rc1
- Build with full read-only relocations (bug #996740).

* Tue Aug  6 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.23.rc1
- Fixes for jobs with multiple files and multiple formats.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7-0.22.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.21.rc1
- Fixed cups-config, broken by last change (bug #987660).

* Mon Jul 22 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.20.rc1
- Removed stale comment in spec file.
- Link against OpenSSL instead of GnuTLS.

* Mon Jul 22 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.19.rc1
- Fixed avahi-no-threaded patch (was missing part of cupsd.h). Thanks
  to Joseph Wang for spotting it.

* Thu Jul 18 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.18.rc1
- Fixed downoad URL to point to the actual source, not a download
  page.

* Fri Jul 12 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.7-0.17.rc1
- 1.7rc1

* Thu Jul 11 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.16.b1
- Avoid sign-extending CRCs for gz decompression (bug #983486).

* Wed Jul 10 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.15.b1
- Fixed download URL.

* Wed Jul 10 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.7-0.14.b1
- Remove pstops cost factor tweak from conf/mime.convs.in

* Mon Jul  1 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.13.b1
- Don't use D-Bus from two threads (bug #979748).

* Fri Jun 28 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.12.b1
- Fix for DNSSD name resolution.

* Wed Jun 26 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.11.b1
- Default to IPP/1.1 for now (bug #977813).

* Tue Jun 25 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.10.b1
- Added libusb quirk for Canon PIXMA MP540 (bug #967873).

* Mon Jun 24 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.9.b1
- Don't link against libgcrypt needlessly.

* Thu Jun 20 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.7-0.8.b1
- Remove scriptlet for migrating to a systemd unit from a SysV initscript

* Thu Jun 20 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.7.b1
- Use IP_FREEBIND socket option when binding listening sockets (bug #970809).

* Tue Jun 18 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.6.b1
- Added IEEE 1284 Device ID for a Dymo device (bug #747866).

* Thu Jun 13 2013 Tim Waugh <twaugh@redhat.com> 1:1.7-0.5.b1
- Prevent stringpool damage leading to memory leaks (bug #974048).

* Tue Jun  4 2013 Tim Waugh <twaugh@redhat.com> - 1:1.7-0.4.b1
- Return from cupsEnumDests() once all records have been returned.

* Thu May 23 2013 Jiri Popelka <jpopelka@redhat.com>
- don't ship Russian web templates because they're broken (#960571, STR #4310)

* Wed May 15 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.7-0.3.b1
- move cups/ppdc/ to filesystem subpackage

* Mon Apr 29 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.7-0.2.b1
- Do not apply unary exclamation mark to va_list (bug #957737).

* Fri Apr 19 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.7-0.1.b1
- 1.7b1
- use _tmpfilesdir macro

* Wed Apr 10 2013 Tim Waugh <twaugh@redhat.com>
- cups-dbus-utf.patch: now that the scheduler only accepts valid UTF-8
  strings for job-name, there's no need to validate it as UTF-8 in the
  dbus notifier.

* Thu Apr  4 2013 Tim Waugh <twaugh@redhat.com> 1:1.6.2-4
- Use IP address when resolving DNSSD URIs (bug #948288).

* Thu Mar 28 2013 Tim Waugh <twaugh@redhat.com> 1:1.6.2-3
- Check for cupsd.conf existence prior to grepping it (bug #928816).

* Tue Mar 19 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.6.2-2
- revert previous bug #919489 fix (i.e we don't ship banners now)

* Mon Mar 18 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.6.2-1
- 1.6.2

* Wed Mar 13 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.6.1-26
- ship banners again (#919489)

* Tue Mar  5 2013 Tim Waugh <twaugh@redhat.com> 1:1.6.1-25
- Talk about systemd in cups-lpd manpage (part of bug #884641).

* Tue Mar  5 2013 Tim Waugh <twaugh@redhat.com> 1:1.6.1-24
- Documentation fixes from STR #4223 (bug #915981).

* Wed Feb 27 2013 Jiri Popelka <jpopelka@redhat.com> - 1:1.6.1-23
- Removed obsolete browsing directives from cupsd.conf (bug #880826, STR #4157).
- Updated summary and descriptions (#882982).
- Fixed bogus dates in changelog.

* Fri Feb 15 2013 Tim Waugh <twaugh@redhat.com> 1:1.6.1-22
- Applied colorman fix from STR #4232 and STR #4276.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-20
- Add quirk rule for Canon MP210 (#847923).

* Mon Jan 14 2013 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-19
- Fix unowned directories (#894531).

* Thu Jan 10 2013 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-18
- Clean /var/spool/cups/tmp with tmpfiles.d instead of tmpwatch&cron (#893834).

* Wed Dec 19 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-17
- Migrate cups-lpd from xinetd to systemd socket activatable service (#884641).
- Clean up old Requires/Conflicts/Obsoletes/Provides.

* Thu Dec  6 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-16
- Additional fix relating to CVE-2012-5519 to avoid misleading error
  message about actions to take to enable file device URIs.

* Tue Dec  4 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-15
- Small error handling improvements in the configuration migration
  script.

* Mon Dec  3 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-14
- move ipptoolfile(5) to ipptool subpackage

* Mon Dec  3 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-13
- Applied additional upstream patch for CVE-2012-5519 so that the
  RemoteRoot keyword is recognised in the correct configuration file.

* Wed Nov 28 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-12
- Fixed paths in config migration %%post script.
- Set default cups-files.conf filename.

* Mon Nov 26 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-11
- Apply upstream fix for CVE-2012-5519 (STR #4223, bug #875898).
  Migrate configuration keywords as needed.

* Mon Nov 19 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-10
- Re-enable the web interface as it is required for adjusting server
  settings (bug #878090).

* Tue Nov  6 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-9
- Disable the web interface by default (bug #864522).

* Tue Oct 30 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-8
- Ensure attributes are valid UTF-8 in dbus notifier (bug #863387).

* Mon Oct 29 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-7
- Removed broken cups-get-classes patch (bug #870612).

* Mon Oct 22 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-6
- Add quirk rule for Xerox Phaser 3124 (#867392)
- backport more quirk rules (STR #4191)

* Thu Sep 20 2012 Tim Waugh <twaugh@redhat.com> 1:1.6.1-5
- The cups-libs subpackage contains code distributed under the zlib
  license (md5.c). 

* Thu Aug 23 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-4
- quirk handler for port reset done by new USB backend (bug #847923, STR #4155)

* Mon Aug 13 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-3
- fixed usage of parametrized systemd macros (#847405)

* Wed Aug 08 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-2
- Requires: cups-filters

* Wed Aug 08 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.6.1-1
- 1.6.1
 - simplified systemd.patch due to removed CUPS Browsing protocol (STR #3922)
 - removed:
   textonly filter - moved to cups-filters
   pstopdf filter - cups-filters also has pstopdf (different)
   PHP module - moved to cups-filters (STR #3932)
   serial.patch - moved to cups-filters
   getpass.patch - r10140 removed the getpass() use
   snmp-quirks.patch - fixed upstream (r10493)
   avahi patches - merged upstream (STR #3066)
   icc.patch - merged upstream (STR #3808)
 - TODO:
   - do we need cups-build.patch ?
- added filesystem sub-package (#624695)
- use macroized systemd scriptlets

* Thu Jul 26 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.4-1
- 1.5.4

* Tue Jul 24 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.3-5
- Don't enable IP-based systemd socket activation by default (bug #842365).

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.3-3
- Require systemd instead of udev.

* Mon May 28 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.3-2
- Buildrequire libusb1 (STR #3477)

* Tue May 15 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.3-1
- 1.5.3

* Wed May 09 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.2-13
- Add triggers for samba4-client. (#817110)
- No need to define BuildRoot and clean it in clean and install section anymore.
- %%defattr no longer needed in %%files sections.

* Tue Apr 17 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.2-12
- Install /usr/lib/tmpfiles.d/cups-lp.conf to support /dev/lp* devices (#812641)
- Move /etc/tmpfiles.d/cups.conf to /usr/lib/tmpfiles.d/ (#812641)

* Tue Apr 17 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.2-11
- The IPP backend did not always setup username/password authentication
  for printers (bug #810007, STR #3985)
- Detect authentication errors for all requests.
  (bug #810007, upstream commit revision10277)

* Thu Mar 29 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.2-10
- Removed private-shared-object-provides filter lines as they are not
  necessary (see bug #807767 comment #3).

* Thu Mar 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1:1.5.2-9
- Rebuild against fixed rpm (bug #807767)

* Wed Mar 28 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.2-8
- Avoid systemd PrivateTmp bug by explicitly requiring the fixed
  version of systemd (bug #807672).

* Fri Mar 16 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.2-7
- Removed debugging messages from systemd-socket patch.

* Wed Mar 14 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.2-6
- Pulled in bugfixes from Avahi patches on fedorapeople.org.

* Tue Feb 28 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.2-5
- If the translated message is empty return the original message
  (bug #797570, STR #4033).

* Thu Feb 23 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.2-4
- cups-polld: restart polling on error (bug #769292, STR #4031).

* Thu Feb 16 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.2-3
- Removed hard requirement on colord as it is optional.

* Wed Feb 15 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.2-2
- Synthesize notify-printer-uri for job-completed events where the job
  never started processing (bug #784786, STR #4014).
- Removed banners from LSPP patch on Dan Walsh's advice.

* Mon Feb 06 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.5.2-1
- 1.5.2
- Updated FSF address in pstopdf and textonly filters

* Wed Jan 18 2012 Remi Collet <remi@fedoraproject.org> 1:1.5.0-28
- build against php 5.4.0, patch for STR #3999
- add filter to fix private-shared-object-provides
- add %%check for php extension

* Tue Jan 17 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.0-27
- Use PrivateTmp=true in the service file (bug #782495).

* Tue Jan 17 2012 Tim Waugh <twaugh@redhat.com> 1:1.5.0-26
- Replace newline characters with spaces in reported Device IDs
  (bug #782129, STR #4005).
- Don't accept Device URIs of '\0' from SNMP devices
  (bug #770646, STR #4004).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-24
- Fixed textonly filter to work with single copies (bug #738412).

* Fri Dec  9 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-23
- Detangle cups-serverbin-compat.patch from cups-lspp.patch.
- Bind to datagram socket as well in systemd cups.socket unit file, to
  prevent that port being stolen by another service (bug #760070).

* Fri Nov 11 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-22
- Fixed trigger (bug #748841).

* Wed Nov  9 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-21
- Set correct systemd service default on upgrade, once updates are
  applied (bug #748841).

* Fri Nov  4 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-20
- Set the correct PostScript command filter for e.g. foomatic queues
  (STR #3973).

* Mon Oct 31 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-19
- Set correct systemd service default on upgrade (bug #748841).

* Wed Oct 19 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-18
- Make sure to guard against retrying the Avahi connection whilst
  already doing so (Ubuntu #877967).

* Tue Oct 18 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-17
- Use libsystemd-daemon instead of bundling sd-daemon.c.

* Tue Oct 11 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-16
- Use upstream fix for driverd issue (bug #742989).
- Array handling fixes for DNSSDPrinters.
- Array handling fixes for Avahi poll implementation.
- Increase client blocking timeout from 30s to 70s (bug #744715).
- Set BindIPv6Only=ipv6-only in systemd socket unit file as better fix
  for bug #737230.

* Fri Oct  7 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-15
- Fixed Timeouts array comparison function (Ubuntu #860691).

* Wed Oct  5 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-14
- Handle "localhost" resolving to 127.0.0.1 on IPv6-addressed systems
  (bug #737230).

* Tue Oct  4 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-13
- Work around PPDs cache handling issue (bug #742989).

* Tue Oct  4 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-12
- More fixes for systemd socket activation:
  - relax permissions check for domain socket in libcups.
  - initialise addrlen before calling getsockname().

* Mon Oct 03 2011 Richard Hughes <rhughes@redhat.com> 1:1.5.0-11
- Updated colord patch with fixes to DeleteDevice.
- Resolves https://bugzilla.redhat.com/show_bug.cgi?id=741697

* Wed Sep 28 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-10
- Fixed string manipulation in the dbus notifier (STR #3947, bug #741833).

* Thu Sep 22 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-9
- Fixed systemd socket activation support (bug #738709, bug #738710).

* Wed Sep 14 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-8
- Prevent libcups crash in cups-get-classes patch (bug #736698).

* Thu Sep  1 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-7
- Use PathExistsGlob instead of DirectoryNotEmpty in cups.path
  (bug #734435).

* Fri Aug 19 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-6
- Tighten explicit libs sub-package requirement so that it includes
  the correct architecture as well (bug #731421 comment #8).

* Fri Aug 19 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-5
- Avoid GIF reader loop (CVE-2011-2896, STR #3914, bug #727800).

* Wed Aug 17 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-4
- Enable systemd units by default (bug #731421).

* Mon Aug  8 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-3
- Updated avahi support to register sub-types.

* Fri Aug  5 2011 Tim Waugh <twaugh@redhat.com> 1:1.5.0-2
- Ported avahi support from 1.4.

* Tue Jul 26 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.5.0-1
- 1.5.0

* Wed Jul 20 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.16.rc1
- Don't delete job data files when restarted (STR #3880).

* Fri Jul 15 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.15.rc1
- Ship an rpm macro for where to put driver executables.

* Thu Jul  7 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.14.rc1
- Undo last change which had no effect.  We already remove the .SILENT
  target from the Makefile as part of the build.

* Thu Jul  7 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.13.rc1
- Make build log verbose enough to include compiler flags used.

* Tue Jul  5 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.12.rc1
- Removed udev rules file as it is no longer necessary.

* Tue Jul  5 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.11.rc1
- Add support for systemd socket activation (patch from Lennart
  Poettering).

* Wed Jun 29 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.10.rc1
- Don't use portreserve any more.  Better approach is to use systemd
  socket activation (not yet done).

* Wed Jun 29 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.9.rc1
- Ship systemd service unit instead of SysV initscript (bug #690766).

* Wed Jun 29 2011 Tim Waugh <twaugh@redhat.com> 1:1.5-0.8.rc1
- Tag localization files correctly (bug #716421).

* Wed Jun 15 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.5-0.7.rc1
- 1.5rc1

* Sat Jun 04 2011 Richard Hughes <rhughes@redhat.com> 1:1.5-0.6.b2
- Updated colord patch with fixes from Tim Waugh.

* Tue May 31 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.5-0.5.b2
- enable LSPP support again

* Tue May 31 2011 Richard Hughes <rhughes@redhat.com> 1:1.5-0.4.b2
- Updated colord patch against 1.5 upstream and fixes from Tim Waugh.

* Tue May 31 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.5-0.3.b2
- fix lspp.patch to not include "config.h" in cups/cups.h (#709384)

* Thu May 26 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.5-0.2.b2
- 1.5b2

* Tue May 24 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.5-0.1.b1
- 1.5b1
  - removed cups-texttops-rotate-page.patch (#572338 is CANTFIX)
  - removed cups-page-label.patch (#520141 seems to be CANTFIX)

* Wed May 18 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-17
- Package parallel port printer device nodes (bug #678804).

* Tue May 17 2011 Richard Hughes <rhughes@redhat.com> 1:1.4.6-16
- Updated colord patch from upstream review.

* Fri Mar 25 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.6-15
- Polished patches according to results from static analysis of code (bug #690130).

* Thu Mar 10 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-14
- Fixed some typos in colord patch.
- LSPP: only warn when unable to get printer context.

* Mon Mar 07 2011 Richard Hughes <rhughes@redhat.com> 1:1.4.6-13
- Updated colord patch.

* Fri Feb 25 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-12
- Fixed build failure due to php_zend_api macro type.

* Fri Feb 25 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-11
- Fixed dbus notifier support for job-state-changed.

* Thu Feb 10 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.6-10
- Remove testing cups-usb-buffer-size.patch (bug #661814).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.6-8
- Use Till's patch to fix USB-Parallel adapter cable problem (bug #624564).

* Tue Jan 25 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-7
- Some fixes for the AvahiClient callback (bug #672143).

* Tue Jan 18 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-6
- Don't use --enable-pie configure option as it has been removed and
  is now assumed.  See STR #3691.

* Fri Jan 14 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-5
- ICC colord support.

* Wed Jan 12 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-4
- Properly separated serverbin-compat and lspp patches.
- Updated ICC patch (still not yet applied).

* Tue Jan 11 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-3
- Build requires automake for avahi support.

* Mon Jan 10 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.6-2
- Use a smaller buffer when writing to USB devices (bug #661814).
- Handle EAI_NONAME when resolving hostnames (bug #617208).

* Fri Jan 07 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.6-1
- 1.4.6.

* Fri Dec 31 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.5-10
- Some Avahi support fixes from Till Kamppeter.

* Fri Dec 24 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.5-9
- Native Avahi support for announcing printers on the network.

* Wed Dec 22 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.5-8
- Don't crash when job queued for browsed printer that times out
  (bug #660604).

* Mon Dec 13 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.5-7
- Call avc_init() only once to not leak file descriptors (bug #654075).

* Thu Dec  9 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.5-6
- The cups-config man page has been moved to the devel sub-package.
- The php sub-package now explicitly requires the libs package with
  the same version and release (bug #646814).

* Tue Dec  7 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.5-5
- Fixed character encoding in CREDITS.txt.
- Mark D-Bus configuration file as config file.
- Don't mark MIME types and convs files as config files.  Overrides
  can be placed as new *.types/*.convs files in /etc/cups.
- Don't mark banners as config files.  Better is to provide new
  banners.
- Don't mark templates and www files as config files.  A better way to
  provide local overrides is to use a different ServerRoot setting.
  Note that a recent security fix required changed to template files.
- Provide versioned LPRng symbol for rpmlint.

* Mon Dec  6 2010 Tim Waugh <twaugh@redhat.com>
- /usr/sbin/cupsd should be mode 0755 (bug #546004).

* Fri Dec 03 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.5-4
- Changed subsystem lock file name in initscript
  so the service is correctly stopped on reboot or halt (bug #659391).

* Fri Nov 26 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.5-3
- BuildRequires python-cups instead of pycups.

* Fri Nov 26 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.5-2
- Added /etc/tmpfiles.d/cups.conf to enable /var/run/cups directory on tmpfs (#656566).

* Fri Nov 12 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.5-1
- 1.4.5.
- No longer need CVE-2010-2941, str3608

* Thu Nov 11 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-12
- Applied patch to fix cupsd memory corruption vulnerability
  (CVE-2010-2941, bug #652161).
- Don't crash when MIME database could not be loaded (bug #610088).

* Wed Sep 29 2010 jkeating - 1:1.4.4-11
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-10
- Perform locking for gnutls and avoid libgcrypt's broken
  locking (bug #607159).
- Build with --enable-threads again (bug #607159).
- Force the use of gnutls despite thread-safety concerns (bug #607159).

* Wed Sep 15 2010 Tim Waugh <twaugh@redhat.com>
- Fixed serverbin-compat patch to avoid misleading "filter not
  available" messages (bug #633779).

* Mon Aug 23 2010 Tim Waugh <twaugh@redhat.com>
- Fixed SNMP quirks parsing.

* Fri Aug 20 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-9
- Use better upstream fix for STR #3608 (bug #606909).

* Fri Aug 13 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-8
- Specify udevadm trigger action in initscript (bug #623959).

* Tue Aug  3 2010 Tim Waugh <twaugh@redhat.com>
- Merged F-12 change:
  - Use numeric addresses for interfaces unless HostNameLookups are
    turned on (bug #583054).

* Tue Jul 13 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.4-7
- Added restartlog to initscript usage output (bug #612996).

* Mon Jul 12 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.4-6
- Moved LICENSE.txt to libs sub-package.

* Mon Jun 28 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-5
- Avoid empty notify-subscribed-event attributes (bug #606909,
  STR #3608).

* Thu Jun 24 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-4
- Use gnutls again but disable threading (bug #607159).

* Tue Jun 22 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-3
- Rebuilt to keep correct package n-v-r ordering between releases.

* Fri Jun 18 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-2
- Re-enabled SSL support by using OpenSSL instead of gnutls.

* Fri Jun 18 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.4-1
- 1.4.4.  Fixes several security vulnerabilities (bug #605399):
  CVE-2010-0540, CVE-2010-0542, CVE-2010-1748.  No longer need str3503,
  str3399, str3505, str3541, str3425p2 or CVE-2010-0302 patches.

* Thu Jun 10 2010 Tim Waugh <twaugh@redhat.com>
- Removed unapplied gnutls-gcrypt-threads patch.  Fixed typos in
  descriptions for lpd and php sub-packages.

* Wed Jun  9 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-11
- Use upstream method of handling SNMP quirks in PPDs (STR #3551,
  bug #581825).

* Tue Jun 01 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.3-10
- Added back still useful str3425.patch.
  Second part of STR #3425 is still not fixed in 1.4.3

* Tue May 18 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-9
- Adjust texttops output to be in natural orientation (STR #3563).
  This fixes page-label orientation when texttops is used in the
  filter chain (bug #572338).

* Thu May 13 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-8
- Fixed Ricoh Device ID OID (STR #3552).

* Tue May 11 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-7
- Add an SNMP query for Ricoh's device ID OID (STR #3552).

* Fri Apr 16 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-6
- Mark DNS-SD Device IDs that have been guessed at with "FZY:1;".

* Fri Apr 16 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.3-5
- Fixed str3541.patch

* Tue Apr 13 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-4
- Add an SNMP query for HP's device ID OID (STR #3552).

* Tue Apr 13 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-3
- Handle SNMP supply level quirks (bug #581825).

* Wed Mar 31 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.3-2
- Another BrowsePoll fix: handle EAI_NODATA as well (bug #567353).

* Wed Mar 31 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.3-1
- 1.4.3.
- No longer need CVE-2009-3553, str3381, str3390, str3391,
  str3403, str3407, str3413, str3418, str3422, str3425,
  str3428, str3431, str3435, str3436, str3439, str3440,
  str3442, str3448, str3458, str3460, cups-sidechannel-intrs,
  negative-snmp-string-length, cups-media-empty-warning patches.

* Tue Mar 30 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-36
- Fixed lpstat to adhere to -o option (bug #577901, STR #3541).

* Wed Mar 10 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-35
- Fixed (for the third time) patch for STR #3425 to correctly
  remove job info files in /var/spool/cups (bug #571830).

* Fri Mar  5 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-34
- Applied patch for CVE-2010-0302 (incomplete fix for CVE-2009-3553,
  bug #557775).
- Added comments for all sources and patches.

* Tue Mar  2 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-33
- Don't own filesystem locale directories (bug #569403).
- Don't apply gcrypt threading patch (bug #553834).
- Don't treat SIGPIPE as an error (bug #569770).

* Wed Feb 24 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-32
- Fixed cupsGetNamedDest() so it falls back to the real default
  printer when a default from configuration file does not exist (bug #565569, STR #3503).

* Tue Feb 23 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-31
- Update classes.conf when a class member printer is deleted
  (bug #565878, STR #3505).

* Tue Feb 23 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-30
- Re-initialize the resolver if getnameinfo() returns EAI_AGAIN
  (bug #567353).

* Mon Feb 15 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-29
- Improve cups-gnutls-gcrypt-threads.patch (#564841, STR #3461).

* Thu Feb  4 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-28
- Rebuild for postscriptdriver tags.

* Fri Jan 22 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-27
- Make sure we have some filters for converting to raster format.

* Fri Jan 15 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-26
- Reset status after successful ipp job (bug #548219, STR #3460).

* Thu Jan 14 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-24
- Install udev rules in correct place (bug #530378).
- Don't mark initscript as config file.

* Wed Jan 13 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-23
- Use %%{_initddir}, %%{_sysconfdir} and SMP make flags.
- Use mode 0755 for binaries and libraries where appropriate.
- Fix lpd obsoletes tag.

* Thu Dec 24 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-22
- Removed use of prereq and buildprereq.
- Fixed use of '%%' in changelog.
- Versioned explicit obsoletes/provides.
- Use tabs throughout.

* Wed Dec 23 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-21
- Fixed patch for STR #3425 again by adding in back-ported change from
  svn revision 8929 (bug #549899).  No longer need
  delete-active-printer patch.

* Tue Dec 22 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-20
- Fixed ipp authentication for servers requiring authentication for
  IPP-Get-Printer-Attributes (bug #548873, STR #3458).

* Mon Dec 21 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-19
- Ensure proper thread-safety in gnutls's use of libgcrypt
  (bug #544619).

* Sat Dec 19 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-18
- Fixed patch for STR #3425 by adding in back-ported change from svn
  revision 8936 (bug #548904).

* Thu Dec 10 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-17
- Fixed invalid read in cupsAddDest (bug #537460).

* Wed Dec  9 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-15
- Use upstream patch to fix scheduler crash when an active printer was
  deleted (rev 8914).

* Tue Dec  8 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-14
- The scheduler did not use the Get-Job-Attributes policy for a
  printer (STR #3431).
- The scheduler added two job-name attributes to each job object
  (STR #3428).
- The scheduler did not clean out completed jobs when
  PreserveJobHistory was turned off (STR #3425).
- The web interface did not show completed jobs (STR #3436).
- Authenticated printing did not always work when printing directly to
  a remote server (STR #3435).
- Use upstream patch to stop the network backends incorrectly clearing
  the media-empty-warning state (rev 8896).
- Use upstream patch to fix interrupt handling in the side-channel
  APIs (rev 8896).
- Use upstream patch to handle negative SNMP string lengths (rev 8896).
- Use upstream fix for SNMP detection (bug #542857, STR #3413).
- Use the text filter for text/css files (bug #545026, STR #3442).
- Show conflicting option values in web UI (bug #544326, STR #3440).
- Use upstream fix for adjustment of conflicting options
  (bug #533426, STR #3439).
- No longer requires paps.  The texttopaps filter MIME conversion file
  is now provided by the paps package (bug #545036).
- Moved %%{_datadir}/cups/ppdc/*.h to the main package (bug #545348).

* Fri Dec  4 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-13
- The web interface prevented conflicting options from being adjusted
  (bug #533426, STR #3439).

* Thu Dec  3 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-12
- Fixes for SNMP scanning with Lexmark printers (bug #542857, STR #3413).

* Mon Nov 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-10
- Undo last change as it was incorrect.

* Mon Nov 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-9
- Fixed small typos introduced in fix for bug #536741.

* Fri Nov 20 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-8
- Do not translate russian links showing completed jobs
  (bug #539354, STR #3422).

* Thu Nov 19 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-7
- Applied patch to fix CVE-2009-3553 (bug #530111, STR #3200).

* Tue Nov 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-6
- Fixed display of current driver (bug #537182, STR #3418).
- Fixed out-of-memory handling when loading jobs (bug #538054,
  STR #3407).

* Mon Nov 16 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-5
- Fixed typo in admin web template (bug #537884, STR #3403).
- Reset SIGPIPE handler for child processes (bug #537886, STR #3399).

* Mon Nov 16 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-4
- Upstream fix for GNU TLS error handling bug (bug #537883, STR #3381).

* Wed Nov 11 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-3
- Fixed lspp-patch to avoid memory leak (bug #536741).

* Tue Nov 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-2
- Added explicit version dependency on cups-libs to cups-lpd
  (bug #502205).

* Tue Nov 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-1
- 1.4.2.  No longer need str3380, str3332, str3356, str3396 patches.
- Removed postscript.ppd.gz (bug #533371).
- Renumbered patches and sources.

* Tue Nov  3 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-14
- Removed stale patch from STR #2831 which was causing problems with
  number-up (bug #532516).

* Tue Oct 27 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-13
- Fix incorrectly applied patch from #STR3285 (bug #531108).
- Set the PRINTER_IS_SHARED variable for admin.cgi (bug #529634, #STR3390).
- Pass through serial parameters correctly in web interface (bug #529635, #STR3391).
- Fixed German translation (bug #531144, #STR3396).

* Tue Oct 20 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-12
- Fix cups-lpd to create unique temporary data files (bug #529838).

* Mon Oct 19 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-11
- Fixed German translation (bug #529575, STR #3380).

* Thu Oct 15 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-10
- Don't ship pstoraster -- it is now provided by the ghostscript-cups
  package.

* Thu Oct  8 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-9
- Fixed naming of 'Generic PostScript Printer' entry.

* Wed Oct  7 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-8
- Use upstream patch for STR #3356 (bug #526405).

* Fri Oct  2 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-7
- Fixed orientation of page labels when printing text in landscape
  mode (bug #520141, STR #3334).

* Wed Sep 30 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-6
- Don't use cached PPD for raw queue (bug #526405, STR #3356).

* Wed Sep 23 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-5
- Fixed cups.init to be LSB compliant (bug #521641)

* Mon Sep 21 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-4
- Changed cups.init to be LSB compliant (bug #521641), i.e.
  return code "2" (instead of "3") if invalid arguments
  return code "4" if restarting service under nonprivileged user
  return code "5" if cupsd not exist or is not executable
  return code "6" if cupsd.conf not exist

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> 1:1.4.1-3
- Use password-auth common PAM configuration instead of system-auth
  when available.

* Tue Sep 15 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-2
- Fixed 'service cups status' to check for correct subsys name
  (bug #521641).

* Mon Sep 14 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-1
- 1.4.1.

* Fri Sep  4 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.0-2
- Fixed the dnssd backend so that it only reports devices once avahi
  resolution has completed.  This makes it report Device IDs
  (bug #520858).
- Fix locale code for Norwegian (bug #520379).

* Fri Aug 28 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.0-1
- 1.4.0.

* Thu Aug 27 2009 Warren Togami <wtogami@redhat.com> 1:1.4-0.rc1.21
- rebuild

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.20
- Fixed admin.cgi crash when modifying a class (bug #519724,
  STR #3312, patch from Jiri Popelka).

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.19
- Prevent infinite loop in cupsDoIORequest when processing HTTP
  errors (bug #518065, bug #519663, STR #3311).
- Fixed document-format-supported attribute when
  application/octet-stream is enabled (bug #516507, STR #3308, patch
  from Jiri Popelka).
- Fixed buggy JobKillDelay handling fix (STR #3292).
- Prevent infinite loop in ppdc (STR #3293).

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1:1.4-0.rc1.17.1
- rebuilt with new audit

* Fri Aug 21 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.17
- Removed 3-distribution symlink (bug #514244).

* Tue Aug 18 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.16
- Fixed JobKillDelay handling for cancelled jobs (bug #518026, STR
  #3292).
- Use 'exec' to invoke ghostscript in the pstoraster filter.  This
  allows the SIGTERM signal to reach the correct process, as well as
  conserving memory (part of bug #518026).

* Tue Aug 11 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.15
- Avoid empty BrowseLocalProtocols setting (bug #516460, STR #3287).

* Mon Aug 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.14
- Fixed ppds.dat handling of drv files (bug #515027, STR #3279).
- Fixed udev rules file to avoid DEVTYPE warning messages.
- Fixed cupsGetNamedDest() so it does not fall back to the default
  printer when a destination has been named (bug #516439, STR #3285).
- Fixed MIME type rules for image/jpeg and image/x-bitmap
  (bug #516438, STR #3284).
- Clear out cache files on upgrade.
- Require acl.

* Thu Aug  6 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.13
- Ship udev rules to allow libusb to access printer devices.
- Fixed duplex test pages (bug #514898, STR #3277).

* Wed Jul 29 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.12
- Fixed Avahi support in the dnssd backend (bug #513888).
- Fixed incorrect arguments to sigaction() in dnssd backend (STR #3272).
- Cheaply restore compatibility with 1.1.x by having cups_get_sdests()
  perform a CUPS_GET_CLASSES request if it is not sure it is talking
  to CUPS 1.2 or later (bug #512866).
- Prevent ipp backend looping with bad IPP devices (bug #476424,
  STR #3262).
- Fixed Device ID reporting in the usb backend (STR #3266).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4-0.rc1.11.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.11
- Tell udevd to replay printer add events in the initscript.

* Wed Jul 15 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.10
- Applied patch to prevent bad job control files crashing cupsd on
  start-up (STR #3253, bug #509741).
- Correctly handle CUPS-Get-PPDs requests for models with '+' in their
  names (STR #3254, bug #509586).
- Accept incorrect device URIs in the (non-libusb) usb backend for
  compatibility with Fedora 11 before bug #507244 was fixed.
- Applied patch to fix incorrect device URIs (STR #3259, bug #507244).
- Applied patch to fix job-hold-until for remote queues (STR #3258,
  bug #497376).

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 1:1.4-0.rc1.9
- add PHP ABI check
- use php_extdir
- add php configuration file (/etc/php.d/cups.ini)

* Fri Jul 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.8
- Build does not require aspell-devel (bug #510405).

* Wed Jul  1 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.7
- Fixed template problem preventing current printer option defaults
  from being shown in the web interface (bug #506794, STR #3244).

* Wed Jul  1 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.6
- Fixed lpadmin for remote 1.3.x servers (bug #506977, STR #3231).

* Tue Jun 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.5
- Added more debugging output when constructing filter chain.

* Thu Jun 18 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.4
- More complete fix for STR #3229 (bug #506461).

* Wed Jun 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.3
- Don't use RPM_SOURCE_DIR macro.
- Fixed add/modify-printer templates which had extra double-quote
  characters, preventing the Continue button from appearing in certain
  browsers (bug #506461, STR #3229).

* Wed Jun 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.1
- 1.4rc1.  No longer need str3124, CVE-2009-0163, CVE-2009-0164,
  str3197, missing-devices patches.
- Disabled avahi patch for the time being.  More work is needed to
  port this to rc1.
- Removed wbuffer patch as it is not needed (see STR #1968).

* Fri May 15 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.18
- More complete fix for STR #3197 (bug #500859).

* Thu May 14 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.17
- Prevent cupsd crash when handling IPP_TAG_DELETEATTR requests
  (STR #3197, bug #500859).

* Thu May  7 2009 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-0.b2.16
- Avoid stripping binaries before rpmbuild creates the -debuginfo subpackage.

* Sun Apr 26 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.15
- Accept "Host: ::1" (bug #497393).
- Accept Host: fields set to the ServerName value (bug #497301).
- Specify that we want poppler's pdftops (not ghostscript) for the
  pdftops wrapper when calling configure.

* Fri Apr 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.14
- Applied patch to fix CVE-2009-0163 (bug #490596).
- Applied patch to fix CVE-2009-0164 (bug #490597).

* Thu Apr  2 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.13
- Don't verify MD5 sum, file size, or mtime for several config files:
  cupsd.conf, client.conf, classes.conf, printers.conf, snmp.conf,
  subscriptions.conf, lpoptions (bug #486287).

* Mon Mar 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.12
- If cups-polld gets EAI_AGAIN when looking up a hostname,
  re-initialise the resolver (bug #490943).

* Wed Mar 11 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.11
- Bumped cupsddk n-v-r for obsoletes/provides, as cupsddk was rebuilt.

* Tue Mar 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.10
- Applied patch to fix ppd-natural-language attribute in PPD list
  (STR #3124).

* Mon Mar  9 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.9
- Handle https:// device URIs (bug #478677, STR #3122).

* Thu Mar  5 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.8
- Updated to svn8404.

* Wed Feb 25 2009 Tim Waugh <twaugh@redhat.com>
- Added 'Should-Start: portreserve' to the initscript (part of bug #487250).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4-0.b2.7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.7
- Prevent cups-deviced missing devices (STR #3108).
- Actually drop the perl implementation of the dnssd backend and use
  the avahi-aware one.

* Thu Feb 12 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.6
- Beginnings of avahi support.  The dnssd backend should now work, but
  the scheduler will not yet advertise DNS-SD services.
- No longer require avahi-tools as the dnssd backend does not use the
  command line tools any longer.
- Load MIME type rules correctly (bug #426089, STR #3059).

* Wed Jan 28 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.4
- Fixed quotas (STR #3077, STR #3078).

* Tue Jan 27 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.3
- Fixed default BrowseLocalProtocols (bug #481505).

* Tue Dec 16 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.2
- 1.4b2.
- No longer need CVE-2008-5183 patch.

* Sat Dec 13 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.6
- Start cupsd at priority 25: after avahi-daemon but before haldaemon
  (bug #468709).

* Tue Dec  9 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.5
- Applied patch to fix RSS subscription limiting (bug #473901,
  CVE-2008-5183).
- Attempt to unbreak the fix for STR #2831 (bug #474742).

* Sun Nov 30 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.4
- Own more directories (bug #473581).

* Tue Nov 11 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.3
- 1.4b1.
- No longer need ext, includeifexists, foomatic-recommended,
  getnameddest, str2101, str2536 patches.
- Require poppler-utils at runtime and for build.  No longer need
  pdftops.conf.
- Obsolete cupsddk.

* Thu Oct 30 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.9-3
- Fixed LSPP labels (bug #468442).

* Tue Oct 21 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.9-2
- Fixed textonly filter to send FF correctly.

* Fri Oct 10 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.9-1
- 1.3.9, including fixes for CVE-2008-3639 (STR #2918, bug #464710),
  CVE-2008-3640 (STR #2919, bug #464713) and CVE-2008-3641 (STR #2911,
  bug #464716).
- No longer need str2892 or res_init patches.

* Wed Sep 10 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-6
- Backported patch for FatalErrors configuration directive
  (bug #314941, STR #2536).

* Thu Sep  4 2008 Tim Waugh <twaugh@redhat.com>
- Use php-cgi for executing PHP scripts (bug #460898).

* Wed Sep  3 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-5
- The dnssd backend uses avahi-browse so require it (bug #458565).
- New php sub-package (bug #428235).
- cups-polld: reinit the resolver if we haven't yet resolved the
  hostname (bug #354071).

* Mon Aug 11 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-4
- Better password prompting behaviour (bug #215133, STR #2101).

* Tue Aug  5 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-3
- Mark template files config(noreplace) for site-local modifications
  (bug #441719).

* Sun Aug  3 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-2
- Applied patch to fix STR #2892 (bug #453610).

* Mon Jul 28 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-1
- 1.3.8.

* Fri Jul 18 2008 Tim Waugh <twaugh@redhat.com>
- Removed autoconf requirement by applying autoconf-generated changes
  to patches that caused them.  Affected patches: cups-lspp.

* Tue Jul 15 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-13
- CVE-2008-1373 patch is no longer needed (applied upstream).
- Mark HTML files and templates config(noreplace) for site-local
  modifications (bug #441719).
- The cups-devel package requires zlib-devel (bug #455192).

* Tue Jul  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-12
- Fixed bug #447200 again.

* Tue Jul  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-11
- Use portreserve.

* Tue Jun 24 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-10
- Rebuilt for new gnutls.

* Tue Jun 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-9
- Don't overwrite the upstream snmp.conf file.

* Tue Jun 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-8
- Fixed bug #447200 again.

* Tue Jun 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-7
- Backported cupsGetNamedDest from 1.4 (bug #428086).

* Tue Jun  3 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-6
- Applied patch to fix STR #2750 (IPP authentication).

* Fri May 30 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-5
- Better fix for cupsdTimeoutJob LSPP configuration suggested by
  Matt Anderson (bug #447200).

* Thu May 29 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-4
- Fix last fix (bug #447200).

* Wed May 28 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-3
- If cupsdTimeoutJob is called when the originating connection is still
  known, pass that to the function so that copy_banner can get at it if
  necessary (bug #447200).

* Fri May  9 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-2
- Applied patch to fix CVE-2008-1722 (integer overflow in image filter,
  bug #441692, STR #2790).

* Thu Apr  3 2008 Tim Waugh <twaugh@redhat.com>
- Main package requires exactly-matching libs package.

* Wed Apr  2 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-1
- 1.3.7.  No longer need str2715, str2727, or CVE-2008-0047 patches.

* Tue Apr  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-9
- Applied patch to fix CVE-2008-1373 (GIF overflow, bug #438303).
- Applied patch to prevent heap-based buffer overflow in CUPS helper
  program (bug #436153, CVE-2008-0047, STR #2729).

* Tue Apr  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-8
- Ship a few doc files (bug #438598).

* Thu Mar 27 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-7
- Don't ship broken symlink %%{_datadir}/cups/doc (bug #438598).

* Mon Mar 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-6
- Own %%{_datadir}/cups/www (bug #437742).

* Thu Feb 28 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-5
- Apply upstream fix for Adobe JPEG files (bug #166460, STR #2727).

* Tue Feb 26 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-4
- LSB header for initscript (bug #246897).
- Move HTML-related files to main application directory so that the CUPS
  web interface still works even with --excludedocs (bug #375631).

* Tue Feb 26 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-3
- Set MaxLogSize to 0 to prevent log rotation.  Upstream default is 1Mb, but
  we want logrotate to be in charge.

* Sat Feb 23 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-2
- Fix encoding of job-sheets option (bug #433753, STR #2715).

* Wed Feb 20 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-1
- 1.3.6.

* Thu Feb 14 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-6
- Include fixes from svn up to revision 7304.  No longer need str2703 patch.
  Build with --with-dbusdir.
- Try out logrotate again (bug #432730).

* Tue Feb 12 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-5
- Fixed admin.cgi handling of DefaultAuthType (bug #432478, STR #2703).

* Tue Feb  5 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-4
- Fix compilation of SO_PEERCRED support.
- Include fixes from svn up to revision 7287.  No longer need str2650 or
  str2664 patches.

* Fri Feb  1 2008 Tim Waugh <twaugh@redhat.com>
- Updated initscript for LSB exit codes and actions (bug #246897).

* Thu Jan 24 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-3
- Build requires autoconf.

* Mon Jan 21 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-2
- Main package requires libs sub-package of the same release.

* Thu Jan 10 2008 Tim Waugh <twaugh@redhat.com>
- Apply patch to fix busy looping in the backends (bug #426653, STR #2664).

* Wed Jan  9 2008 Tim Waugh <twaugh@redhat.com>
- Apply patch to prevent overlong PPD lines from causing failures except
  in strict mode (bug #405061).  Needed for compatibility with older
  versions of foomatic (e.g. Red Hat Enterprise Linux 3/4).
- Applied upstream patch to fix cupsctl --remote-any (bug #421411, STR #2650).

* Thu Jan  3 2008 Tim Waugh <twaugh@redhat.com>
- Efficiency fix for pstoraster (bug #416871).

* Tue Dec 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.5-1
- 1.3.5.

* Mon Dec 10 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.4-5
- Rebuilt with higher release number.

* Tue Dec 4 2007 Warren Togami <wtogami@redhat.com> 1:1.3.4-3
- rebuild

* Fri Nov 30 2007 Tim Waugh <twaugh@redhat.com>
- CVE-2007-4045 patch is not necessarily because cupsd_client_t objects are
  not moved in array operations, only pointers to them.

* Tue Nov 27 2007 Tim Waugh <twaugh@redhat.com>
- Updated to improved dnssd backend from Till Kamppeter.

* Tue Nov 13 2007 Tim Waugh <twaugh@redhat.com>
- Fixed CVE-2007-4045 patch; has no effect with shipped packages since they
  are linked with gnutls.
- LSPP cupsdSetString/ClearString fixes (bug #378451).

* Wed Nov  7 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.4-2
- Applied patch to fix CVE-2007-4045 (bug #250161).
- Applied patch to fix CVE-2007-4352, CVE-2007-5392 and
  CVE-2007-5393 (bug #345101).

* Thu Nov  1 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.4-1
- 1.3.4 (bug #361681).

* Wed Oct 10 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.3-3
- Use ppdev instead of libieee1284 for parallel port Device ID
  retrieval (bug #311671).  This avoids SELinux audit messages.

* Tue Oct  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.3-2
- Use libieee1284 for parallel port Device ID retrieval (bug #311671).

* Fri Sep 28 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.3-1
- 1.3.3.

* Tue Sep 25 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.2-3
- Don't strip foomatic recommended strings from make/model names.

* Fri Sep 21 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.2-2
- Write printcap when remote printers have timed out (bug #290831).

* Wed Sep 19 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.2-1
- Include Till Kamppeter's dnssd backend.
- 1.3.2.
- No longer need str2512 patches.

* Tue Sep 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.1-3
- Write printcap when a remote queue is deleted (bug #290831).

* Tue Sep 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.1-2
- Avoid writing printcap unnecessarily (bug #290831).

* Mon Sep 17 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.1-1
- 1.3.1.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.0-2
- More specific license tag.

* Mon Aug 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.0-1
- 1.3.0.

* Tue Jul 31 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.rc2.2
- Make cancel man page work properly with alternatives system (bug #249768).
- Don't call aclocal even when we modify m4 files -- CUPS does not use
  automake (bug #250251).

* Tue Jul 31 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.rc2.1
- Better buildroot tag.
- Moved LSPP access check in add_job() to before allocation of the job
  structure (bug #231522).
- 1.3rc2.  No longer need avahi patch.

* Mon Jul 23 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.5
- Use kernel support for USB paper-out detection, when available
  (bug #249213).

* Fri Jul 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.4
- Better error checking in the LSPP patch (bug #231522).

* Fri Jul 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.3
- Change initscript start level to 98, to start after avahi but before
  haldaemon.
- The devel sub-package requires krb5-devel.

* Thu Jul 19 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.2
- Build requires avahi-compat-libdns_sd-devel.  Applied patch to fix
  build against avahi (bug #245824).
- Build requires krb5-devel.

* Wed Jul 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.1
- 1.3b1.  No longer need relro, directed-broadcast, af_unix-auth, or
  str2109 patches.

* Fri Jul 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.12-1
- 1.2.12.  No longer need adminutil or str2408 patches.

* Mon Jul  9 2007 Tim Waugh <twaugh@redhat.com>
- Another small improvement for the textonly filter (bug #244979).

* Thu Jul  5 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-5
- Support for page-ranges and accounting in the textonly filter (bug #244979).

* Wed Jul  4 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-4
- Better paper-out detection patch still (bug #246222).

* Fri Jun 29 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-3
- Applied patch to fix group handling in PPDs (bug #186231, STR #2408).

* Wed Jun 27 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-2
- Fixed _cupsAdminSetServerSettings() sharing/shared handling (bug #238057).

* Mon Jun 25 2007 Tim Waugh <twaugh@redhat.com>
- Fixed permissions on classes.conf in the file manifest (bug #245748).

* Wed Jun 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-1
- 1.2.11.

* Tue Jun 12 2007 Tim Waugh <twaugh@redhat.com>
- Make the initscript use start priority 56 (bug #213828).
- Better paper-out detection patch (bug #241589).

* Wed May  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-10

* Revert paper-out detection for the moment.

* Wed May  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-9
- Applied fix for rotated PDFs (bug #236753, STR #2348).

* Thu Apr 26 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-8
- Initscript fixes (bug #237955).

* Wed Apr 25 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-7
- Until bug #236736 is fixed, work around the kernel usblp driver's
  quirks so that we can detect paper-out conditions.

* Tue Apr 10 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-6
- Fixed 'cancel' man page (bug #234088).
- Added empty subscriptions.conf file to make sure it gets the right
  SELinux file context.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-5
- Send D-BUS QueueChanged signal on printer state changes.

* Tue Apr  3 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-4
- Relay printer-state-message values in the IPP backend (STR #2109).

* Mon Apr  2 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-3
- Don't clear printer-state-reasons after job completion (STR #2323).

* Thu Mar 29 2007 Tim Waugh <twaugh@redhat.com>
- Small improvement for AF_UNIX auth patch.

* Thu Mar 29 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-2
- LSPP: Updated patch for line-wrapped labels (bug #228107).

* Tue Mar 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-1
- 1.2.10.

* Tue Mar 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.9-2
- Added %%{_datadir}/ppd for LSB (bug #232893).

* Fri Mar 16 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.9-1
- 1.2.9.

* Fri Mar  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-5
- Better UNIX domain sockets authentication patch after feedback from
  Uli (bug #230613).

* Thu Mar  8 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-4
- Implemented SCM_CREDENTIALS authentication for UNIX domain sockets
  (bug #230613).

* Fri Mar  2 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-3
- Updated LSPP patch (bug #229673).

* Mon Feb 26 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-2
- Applied fix for STR #2264 (bug #230116).

* Wed Feb 14 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-1
- 1.2.8.

* Tue Feb 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.7-8
- Removed logrotate config file and maxlogsize patch (bug #227369).  Now
  CUPS is in charge of rotating its own logs, and defaults to doing so once
  they get to 1Mb in size.

* Fri Jan 12 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.7-7
- Don't even reload CUPS when rotating logs (bug #215024).

* Fri Dec  8 2006 Tim Waugh <twaugh@redhat.com>
- Requires tmpwatch for the cron.daily script (bug #218901).

* Thu Dec  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-6
- Fixed If-Modified-Since: handling in libcups (bug #217556, STR #2133).
- Fixed extra EOF in pstops output (bug #216154, STR #2111).
- Use upstream patch for STR #2121.

* Mon Nov 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-5
- Better LSPP fix for bug #216855.

* Thu Nov 23 2006 Tim Waugh <twaugh@redhat.com>
- Use translated string for password prompt (STR #2121).

* Wed Nov 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-4
- Another LSPP fix (bug #216669).
- Fixed LSPP SELinux check (bug #216855).
- Increased PPD timeout in copy_model() (bug #216065).

* Tue Nov 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-3
- Run the serial backend as root (bug #212577).

* Thu Nov 16 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-2
- 1.2.7.

* Tue Nov 14 2006 Tim Waugh <twaugh@redhat.com>
- Fixed LogFilePerm.

* Mon Nov 13 2006 Tim Waugh <twaugh@redhat.com>
- Don't use getpass() (bug #215133).

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.6-5
- Reload, don't restart, when logrotating (bug #215023).

* Wed Nov  8 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.6-4
- Fixed pdftops.conf (bug #214611).

* Mon Nov  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.6-3
- 1.2.6.

* Mon Nov  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-7
- One more D-Bus signal fix (bug #212763).

* Fri Nov  3 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-6
- Restore missed JobQueuedRemote D-Bus signal in ipp backend (part of
  bug #212763).

* Thu Nov  2 2006 Tim Waugh <twaugh@redhat.com>
- LSPP patch fix (bug #213498).

* Wed Nov  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-5
- Send QueueChanged D-Bus signal on all job state changes.

* Tue Oct 31 2006 Tim Waugh <twaugh@redhat.com>
- Added filter and PPD for text-only printer (bug #213030).

* Mon Oct 30 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-4
- Fixed support for /dev/ttyUSB devices (bug #212577, STR #2061).
- Fixed parallel backend (bug #213021, STR #2056).

* Thu Oct 26 2006 Tim Waugh <twaugh@redhat.com>
- Ship a real lpoptions file to make sure it is world-readable (bug #203510).

* Mon Oct 23 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-3
- 1.2.5.

* Tue Oct 17 2006 Tim Waugh <twaugh@redhat.com>
- Feature-complete LSPP patch from Matt Anderson (bug #210542).

* Thu Oct  5 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-9
- adminutil.c: when writing 'BrowseAllow @LOCAL', add a comment about what
  to change it to when using directed broadcasts from another subnet
  (bug #204373).

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-8
- LSPP patch didn't get updated properly in 1:1.2.4-6.  Use the right
  patch this time (bug #208676).  LSPP re-enabled.

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-7
- LSPP patch disabled, since it still causes cupsd to crash.

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-6
- Updated LSPP patch from Matt Anderson (bug #208676).

* Tue Oct  3 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-5
- Updated LSPP patch from Matt Anderson (bug #208676).

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.4-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-3
- Add '--help' option to lpr command (bug #206380, STR #1989).

* Fri Sep 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-2
- 1.2.4 (bug #206763).  No longer need str1968 patch.

* Wed Sep 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-5
- Fixed STR #1968 properly (bug #205619).

* Tue Sep 12 2006 Tim Waugh <twaugh@redhat.com>
- No longer need language patch.

* Mon Sep 11 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-4
- Applied upstream patch to fix STR #1968 (bug #205619).

* Thu Sep  7 2006 Tim Waugh <twaugh@redhat.com>
- %%ghost %%config(noreplace) /etc/cups/lpoptions (bug #59022).

* Wed Aug 30 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-3
- Don't overwrite snmp.c.
- No longer need str1893 patch.

* Wed Aug 30 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-2
- 1.2.3.  No longer need str1880 or str1881 patches.

* Tue Aug 29 2006 Tim Waugh <twaugh@redhat.com>
- Removed dest-cache patch.

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-17
- Fixed another LSPP patch problem (bug #203784).
- Updated fix for STR #1881 from upstream.

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-16
- Fixed another LSPP patch problem noted by Erwin Rol.

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-15
- Fixed LSPP patch passing NULL to strcmp (bug #203784).

* Mon Aug 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-14
- Updated LSPP patch (bug #203376).

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.2-13
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Fri Aug 18 2006 Tim Waugh <twaugh@redhat.com>
- Own notifier directory (bug #203085).

* Thu Aug 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-12
- Apply patch to fix STR #1880 (bug #200205).

* Wed Aug 16 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-11
- Use upstream patch to fix STR #1881.

* Fri Aug 11 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-10
- Remove 'Provides: LPRng = 3.8.15-3' (bug #148757).
- Applied patch to fix STR #1893 (bug #201800).

* Thu Aug 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-9
- Try different fix for STR #1795/STR #1881 (bug #201167).

* Sun Aug  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-8
- Apply patch from STR #1881 for remote IPP printing (bug #201167).

* Wed Aug  2 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-7
- Updated LSPP patch from Matt Anderson.
- Ship pstopdf filter for LSPP.

* Fri Jul 28 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-6
- Use replacement snmp.c from STR #1737 (bug #193093).
- Re-enable LSPP; doesn't harm browsing after all.

* Fri Jul 28 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-5
- Disable LSPP for now, since it seems to break browsing somehow.

* Mon Jul 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-4
- Fixed package requirements (bug #199903).

* Fri Jul 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-3
- Apply Matt Anderson's LSPP patch.
- Renumbered patches.

* Thu Jul 20 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-2
- 1.2.2.

* Wed Jul 19 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-21
- Sync with svn5754.  Fixes bug #198987, bug #195532, bug #130118.

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 1:1.2.1-20
- Require a new version of D-Bus and rebuild

* Fri Jul 14 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-19
- Sync with svn5737.  Fixes bug #192015.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.1-18.1
- rebuild

* Fri Jul  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-18
- Ship with an empty classes.conf file.

* Tue Jul  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-17
- Sync with svn5706.
- No longer need localhost, str1740, str1758, str1736, str1776 patches.

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-16
- Bumped paps requirement.
- Don't use texttopaps for application/* MIME types (bug #197214).

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-15
- Require paps and use it for printing text (bug #197214).

* Thu Jun 15 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-14
- Don't export in SSLLIBS to cups-config.

* Thu Jun 15 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-13
- Fixed cupsd network default printer crash (STR #1776).

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1:1.2.1-12
- rebuilt with new gnutls

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-11
- Remove certs directory in %%post, not %%postun.

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-10
- Remove old-style certs directory after upgrade (bug #194581).

* Wed Jun  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-9
- Prevent 'too many open files' error (STR #1736, bug #194368).

* Wed Jun  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-8
- Fix 'Allow from @IF(...)' (STR #1758, bug #187703).

* Wed Jun  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-7
- ServerBin compatibility patch (bug #194005).

* Fri Jun  2 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-6
- Applied upstream patch to fix STR #1740 (bug #192809).

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-5
- Fixed group ownerships again (bug #192880).

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-4
- Fixed 'service cups reload' not to give an error message.

* Thu May 25 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-3
- Fix 'localhost' fallback in httpAddrGetList() (bug #192628, STR #1723).

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-2
- 1.2.1.
- Another STR #1705 fix (bug #192034).
- Fixed devel package multilib conflict (bug #192664).

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-7
- Sync to svn5568.  No longer need rpath patch.
- Added a 'conflicts:' for kdelibs to prevent bug #192548.

* Sat May 20 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-6
- Sync to svn5555.  No longer need str1670 or str1705 patches.

* Fri May 19 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-5
- Sync to svn5545.
- Ship a driver directory.

* Thu May 18 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-4
- Disable back-channel data in the usb backend (STR #1705, bug #192034).
- Fix for 'browsing stops on reload', STR #1670 (bug #191217).

* Wed May 17 2006 Tim Waugh <twaugh@redhat.com>
- Sync to svn5538.
- Added 'restartlog' to initscript, for clearing out error_log.  Useful
  for problem diagnosis.
- Initscript no longer needs to check for printconf-backend.

* Tue May 16 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-3
- Added image library build requirements.
- The devel package requires gnutls-devel (bug #191908).

* Mon May  8 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-2
- 1.2.0.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.4
- Sync to svn5493.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.3
- Sync to svn5491.

* Fri Apr 28 2006 Tim Waugh <twaugh@redhat.com>
- Sync to svn5470.
- No longer need link, CAN-2005-0064, or no-propagate-ipp-port patches.
- Switch to upstream PIE implementation (every single binary is PIE).
- Extend relro to all binaries.
- Better rpath patch.

* Wed Apr 26 2006 Tim Waugh <twaugh@redhat.com>
- No longer need backend, rcp, or ppdsdat patches.
- Use configure switch for LogFilePerm default instead of patch.

* Tue Apr 25 2006 Tim Waugh <twaugh@redhat.com>
- Own /var/run/cups (bug #189561).
- Sync from svn5460 to svn5462.

* Tue Apr 25 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.2
- Patch pdftops to understand 'includeifexists', and use that in the
  pdftops.conf file (bug #189809).

* Mon Apr 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.1
- 1.2rc3.
- Ship an snmp.conf.

* Fri Apr 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.4.rc2.2
- Updated to svn 5446.

* Wed Apr 19 2006 Tim Waugh <twaugh@redhat.com>
- Ignore .rpmnew and .rpmsave banner files.

* Tue Apr 11 2006 Tim Waugh <twaugh@redhat.com>
- Ship a /etc/cups/pdftops.conf file (bug #188583).

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com>
- Build requires libacl-devel.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.4.rc2.1
- 1.2rc2.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.9
- Sync scheduler/* with svn 5383.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.8
- No longer need openssl-devel.
- Build with LDAP_DEPRECATED=1, to pick up declarations of ldap_init() etc.
- Only warn about ACLs once (STR #1532).
- Fix imagetops filter (STR #1533).
- Sync pstops.c with svn 5382.

* Thu Apr  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.7
- Build requires openldap-devel.
- Sync pstops.c with svn 5372.

* Tue Apr  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.6
- Tweak to allow 'usb:/dev/usb/lp0'-style URIs again.

* Sun Apr  2 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.5
- Backported svn 5365:5366 change for mutex-protected stringpool (STR #1530).

* Sat Apr  1 2006 Tim Waugh <twaugh@redhat.com>
- Fixed _cupsStrFree() (STR #1529).

* Fri Mar 31 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.4
- Fixed interaction with CUPS 1.1 servers (STR #1528).

* Wed Mar 29 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.3
- Fix group list of non-root backends (STR #1521, bug #186954).

* Tue Mar 28 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.2
- Fix lpq -h (STR#1515, bug #186686).

* Mon Mar 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.1
- Ship a printers.conf file, and a client.conf file.  That way, they get
  their SELinux file contexts set correctly.

* Mon Mar 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.0
- 1.2rc1.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.6
- Add KDE compatibility symbols _ipp_add_attr/_ipp_free_attr to ipp.h, with
  a comment saying why they shouldn't be used.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.5
- Fix KDE compatibility symbols _ipp_add_attr/_ipp_free_attr.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.4
- Update to svn snapshot.

* Thu Mar 23 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.3
- Update to svn snapshot.  No longer need users or policy patches.

* Fri Mar 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.2
- Rebuilt.

* Tue Mar 14 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.1
- Build requires gnutls-devel.
- Fixed default policy name.
- Fixed 'set-allowed-users' in web UI.

* Mon Mar 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.0
- 1.2b2.
- Use new CUPS_SERVERBIN location (/usr/lib/cups even on 64-bit hosts).

* Fri Mar 10 2006 Tim Waugh <twaugh@redhat.com>
- Fixed some permissions.

* Fri Mar 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b1.1
- Ship /etc/cups/ssl directory.

* Thu Mar  9 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b1.0
- 1.2b1.  No longer need devid patch.

* Wed Mar  8 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5238.2
- Fixed 'device-id' attribute in GET_DEVICES requests (STR #1467).

* Tue Mar  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5238.1
- New svn snapshot.
- No longer need browse or raw patches.

* Wed Mar  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5137.1
- Fixed raw printing.
- Removed (unapplied) session printing patch.
- Fixed browse info.

* Thu Feb 23 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5137.0
- New svn snapshot.

* Fri Feb 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5102.0
- New svn snapshot.
- No longer need enabledisable patch.
- Fixed double-free in scheduler/policy.c (STR #1428).

* Fri Feb 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5083.0
- New svn snapshot.

* Wed Jan 25 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn4964.0
- Use -fPIE not -fpie in PIE patch.
- Fix link patch.
- Patch in PIE instead of using --enable-pie, since that doesn't work.

* Fri Jan 20 2006 Tim Waugh <twaugh@redhat.com>
- 1.2 svn snapshot.
- No longer need doclink, str1023, pdftops, sanity, lpstat, str1068,
  sigchld, gcc34, gcc4, slow, CAN-2004-0888, CAN-2005-2097, finddest,
  str1249, str1284, str1290, str1301, CVE-2005-3625,6,7 patches.
- Removed autodetect-tag patch.

* Tue Jan 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.1.23-30
- Include 'Autodetected' tag for better integration with autodetection tools.

* Tue Jan 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.1.23-29
- Apply dest-cache-v2 patch (bug #175847).

* Wed Jan  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.1.23-28
- Apply patch to fix CVE-2005-3625, CVE-2005-3626, CVE-2005-3627
  (bug #176868).

* Mon Dec 19 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-27
- Link pdftops with -z relro.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 1:1.1.23-26
- rebuild for new dbus

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> 1:1.1.23-25
- rebuilt with new openssl

* Thu Oct 20 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-24
- Build with -fstack-protector-all.

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com> 1:1.1.23-23
- link libcupsimage.so against libcups

* Tue Oct 11 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-22
- Apply patch to fix STR #1301 (bug #169979).

* Thu Oct  6 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-21
- Apply patch to fix STR #1290.

* Wed Oct  5 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-20
- Apply upstream patch for STR #1249.

* Fri Sep 30 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-19
- Use upstream patch for STR #1284.

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Thu Sep 29 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-18
- Raise IPP_MAX_VALUES to 100 (bug #164232).  STR #1284.
- Made FindDest better behaved in some instances (bug #164232).  STR #1283.

* Fri Sep  2 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-17
- Fixed CAN-2005-2097 (bug #164510).

* Thu Jun 16 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-16
- Make DeletePrinterFromClass faster (bug #160620).

* Thu Mar 31 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-15
- Don't require exact dbus version, just minimum.

* Thu Mar 10 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-14
- Fixed up dbus patch so that it compiles.

* Wed Mar  9 2005 John (J5) Palmieri <johnp@redhat.com>
- Fix up dbus patch 

* Mon Mar  7 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.23-13
- Fixed up dbus patch to work with dbus 0.31

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 1:1.1.23-12
- rebuild for openssl-0.9.7e

* Tue Feb 22 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-11
- UTF-8-ify spec file (bug #149293).

* Fri Feb 18 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-10
- Fixed build with GCC 4.

* Thu Feb 10 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-9
- Back to old DBUS API since new DBUS isn't built yet.

* Mon Feb  7 2005 Tim Waugh <twaugh@redhat.com>
- Use upstream patch for STR #1068.
- Apply patch to fix remainder of CAN-2004-0888 (bug #135378).

* Wed Feb  2 2005 Tim Waugh <twaugh@redhat.com>
- Applied patch to prevent occasional cupsd crash on reload (bug #146850).

* Tue Feb  1 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-8
- New DBUS API.

* Tue Feb  1 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-7
- Applied patch to prevent file descriptor confusion (STR #1068).

* Fri Jan 28 2005 Tim Waugh <twaugh@redhat.com>
- Build does not require XFree86-devel (bug #146397).

* Thu Jan 27 2005 Tim Waugh <twaugh@redhat.com>
- Corrected directory modes so that they reflect what cupsd sets them to.

* Mon Jan 24 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-6
- Build against new dbus.

* Fri Jan 21 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-5
- Use tmpwatch to remove unused files in the spool temporary directory
  (bug #110026).

* Thu Jan 20 2005 Tim Waugh <twaugh@redhat.com>
- Use gzip's -n flag for the PPDs.

* Thu Jan 20 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-4
- Mark the initscript noreplace (bug #145629).

* Wed Jan 19 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-3
- Applied patch to fix CAN-2005-0064.

* Thu Jan  6 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-2
- Fixed patch from STR #1023.

* Tue Jan  4 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-1
- 1.1.23.

* Mon Dec 20 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.23-0.rc1.1
- 1.1.23rc1.
- No longer need ioctl, ref-before-use, str1023 or str1024 patches.

* Fri Dec 17 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-6
- Use upstream patches for bug #143086.

* Thu Dec 16 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-5
- Fixed STR #1023 (part of bug #143086).
- Fixed STR #1024 (rest of bug #143086).

* Thu Dec  9 2004 Tim Waugh <twaugh@redhat.com>
- Not all files in the doc directory are pure documentation (bug #67337).

* Thu Dec  9 2004 Tim Waugh <twaugh@redhat.com>
- Fixed ioctl parameter size in usb backend.  Spotted by David A. Marlin.

* Fri Dec  3 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-4
- Convert de and fr .tmpl files into UTF-8 (bug #136177).

* Thu Dec  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-3
- Fix ref-before-use bug in debug output (bug #141585).

* Mon Nov 29 2004 Tim Waugh <twaugh@redhat.com>
- Copied "ext" patch over from xpdf RPM package.

* Mon Nov 22 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-2
- Fixed cups-lpd file mode (bug #137325).
- Convert all man pages to UTF-8 (bug #107118).  Patch from Miloslav Trmac.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com>
- New lpd subpackage, from patch by Matthew Galgoci (bug #137325).

* Tue Nov  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-1
- 1.1.22.
- No longer need ippfail, overread or str970 patches.

* Tue Oct 26 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc2.1
- Make cancel-cups(1) man page point to lp-cups(1) not lp(1) (bug #136973).
- Use upstream patch for STR #953.
- 1.1.22rc2.

* Wed Oct 20 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.7
- Prevent filters generating incorrect PS in locales where "," is the
  decimal separator (bug #136102).  Patch from STR #970.

* Thu Oct 14 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.5
- Fixed another typo in last patch!

* Thu Oct 14 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.4
- Fixed typo in last patch.

* Thu Oct 14 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.3
- Another attempt at fixing bug #135502.

* Wed Oct 13 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.2
- Fail better when receiving corrupt IPP responses (bug #135502).

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.1
- 1.1.22rc1.

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-7
- Set LogFilePerm 0600 in default config file.

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-6
- Apply patch to fix CAN-2004-0923 (bug #134601).

* Mon Oct  4 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-5
- Fixed reload logic (bug #134080).

* Wed Sep 29 2004 Warren Togami <wtogami@redhat.com> 1:1.1.21-4
- Remove .pdf from docs, fix links

* Fri Sep 24 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-3
- Write a pid file (bug #132987).

* Thu Sep 23 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-2
- 1.1.21.

* Thu Sep  9 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc2.2
- Updated DBUS patch (from Colin Walters).

* Tue Aug 24 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc2.1
- 1.1.21rc2.
- No longer need state, reload-timeout or str743 patches.
- httpnBase64 patch no longer applies; alternate method implemented
  upstream.
- Fix single byte overread in usersys.c (spotted by Colin Walters).

* Wed Aug 18 2004 Tim Waugh <twaugh@redhat.com>
- Applied httpnEncode64 patch from Colin Walters.

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com>
- Session printing patch (Colin Walters).  Disabled for now.

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.9
- Shorter reload timeout (Colin Walters).
- Updated DBUS patch from Colin Walters.

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com>
- Updated IPP backend IPP_PORT patch from Colin Walters.

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.8
- Preserve DBUS_SESSION_BUS_ADDRESS in environment (Colin Walters).
- Fixed enabledisable patch.

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.7
- Bumped DBUS version to 0.22.

* Fri Aug  6 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.6
- Patch from Colin Walters to prevent IPP backend using non-standard
  IPP port.

* Sun Aug  1 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.5
- Really bumped DBUS version.

* Fri Jul 30 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.4
- Bumped DBUS version.

* Fri Jul 16 2004 Tim Waugh <twaugh@redhat.com>
- Added version to LPRng obsoletes: tag (bug #128024).

* Thu Jul  8 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.3
- Updated DBUS patch.

* Tue Jun 29 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.2
- Apply patch from STR #743 (bug #114999).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.1
- Fix permissions on logrotate script (bug #126426).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-0.rc1.2
- Build for dbus-0.21.
- Fix SetPrinterState().

* Thu Jun  3 2004 Tim Waugh <twaugh@redhat.com>
- Use configure's --with-optim parameter instead of setting OPTIM at
  make time (bug #125228).

* Thu Jun  3 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-0.rc1.1
- 1.1.21rc1.
- No longer need str716, str718, authtype or encryption patches.

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-15
- Build on ppc and ppc64 again.

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-14
- ExcludeArch ppc, ppc64.
- More D-BUS changes.

* Tue Jun  1 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-13
- Enable optimizations on ia64 again.

* Thu May 27 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-12
- D-BUS changes.

* Wed May 26 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-11
- Build requires make >= 3.80 (bug #124472).

* Wed May 26 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-10
- Finish fix for cupsenable/cupsdisable (bug #102490).
- Fix MaxLogSize setting (bug #123003).

* Tue May 25 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-9
- Apply patches from CVS (authtype) to fix STR #434, STR #611, and as a
  result STR #719.  This fixes several problems including those noted in
  bug #114999.

* Mon May 24 2004 Tim Waugh <twaugh@redhat.com>
- Use upstream patch for exit code fix for bug #110135 [STR 718].

* Wed May 19 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-8
- If cupsd fails to start, make it exit with an appropriate code so that
  initlog notifies the user (bug #110135).

* Thu May 13 2004 Tim Waugh <twaugh@redhat.com>
- Fix cups/util.c:get_num_sdests() to use encryption when it is necessary
  or requested (bug #118982).
- Use upstream patch for the HTTP/1.1 Continue bug (from STR716).

* Tue May 11 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-7
- Fix non-conformance with HTTP/1.1, which caused failures when printing
  to a Xerox Phaser 8200 via IPP (bug #122352).
- Make lppasswd(1) PIE.
- Rotate logs within cupsd (instead of relying on logrotate) if we start
  to approach the filesystem file size limit (bug #123003).

* Tue Apr  6 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-6
- Fix pie patch (bug #120078).

* Fri Apr  2 2004 Tim Waugh <twaugh@redhat.com>
- Fix rcp patch for new system-config-printer name.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb  6 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-4
- Tracked D-BUS API changes.
- Updated D-BUS configuration file.
- Symlinks to avoid conflicting with bash builtins (bug #102490).

* Thu Feb  5 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-3
- Improved PIE patch.
- Fixed compilation with GCC 3.4.

* Thu Jan 29 2004 Tim Waugh <twaugh@redhat.com>
- Don't ship cupsconfig now that nothing uses it.

* Wed Jan  7 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-2
- Try harder to find a translated page for the web interface (bug #107619).
- Added build_as_pie conditional to spec file to facilitate debugging.

* Mon Dec  1 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.20-1
- 1.1.20.
- No longer need idefense, str226 patches.
- Updated sanity patch.
- The devel sub-package requires openssl-devel (bug #110772).

* Wed Nov 26 2003 Thomas Woerner <twoerner@redhat.com> 1:1.1.19-16
- removed -Wl,-rpath from cups-sharedlibs.m4 (replaced old no_rpath patch)

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 1:1.1.19-15
- no rpath in cups-config anymore

* Thu Nov 20 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-14
- Enable PIE for cupsd.

* Fri Nov 14 2003 Tim Waugh <twaugh@redhat.com>
- Don't ignore the file descriptor when ShutdownClient is called: it
  might get closed before we next try to read it (bug #107787).

* Tue Oct 14 2003 Tim Waugh <twaugh@redhat.com>
- Removed busy-loop patch; 1.1.19 has its own fix for this.

* Thu Oct  2 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-13
- Apply patch from STR 226 to make CUPS reload better behaved (bug #101507).

* Wed Sep 10 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-12
- Prevent a libcups busy loop (bug #97958).

* Thu Aug 14 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-11
- Another attempt to fix bug #100984.

* Wed Aug 13 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-10
- Pass correct attributes-natural-language through even in the absence
  of translations for that language (bug #100984).
- Show compilation command lines.

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-9
- Prevent lpstat displaying garbage.

* Mon Jul 21 2003 Tim Waugh <twaugh@redhat.com>
- Mark mime.convs and mime.types as config files (bug #99461).

* Mon Jun 23 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-8
- Start cupsd before nfs server processes (bug #97767).

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-7
- Add some %%if %%use_dbus / %%endif's to make it compile without dbus
  (bug #97397).  Patch from Jos Vos.

* Mon Jun 16 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-6
- Don't busy loop in the client if the IPP port is in use by another
  app (bug #97468).

* Tue Jun 10 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-5
- Mark pam.d/cups as config file not to be replaced (bug #92236).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-3
- Provide a version for LPRng (bug #92145).

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-2
- Obsolete LPRng now.

* Tue May 27 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-1
- 1.1.19.  No longer need optparse patch.

* Sat May 17 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.4
- Ship configuration file for D-BUS.

* Fri May 16 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.3
- Rebuild for dbus-0.11 API changes.
- Fix ownership in file manifest (bug #90840).

* Wed May 14 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.2
- Fix option parsing in lpq (bug #90823).

* Tue May 13 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.1
- 1.1.19rc5.

* Thu May  8 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc4.1
- 1.1.19rc4.  Ported initscript, idefense, ppdsdat, dbus patches.
- No longer need error, sigchld patches.
- Ship cupstestppd.

* Thu Apr 24 2003 Tim Waugh <twaugh@redhat.com>
- Mark banners as config files (bug #89069).

* Sat Apr 12 2003 Havoc Pennington <hp@redhat.com> 1:1.1.18-4
- adjust dbus patch - dbus_bus_get() sends the hello for you, 
  and there were a couple of memleaks
- buildprereq dbus 0.9
- rebuild for new dbus
- hope it works, I'm ssh'd in with no way to test. ;-)

* Thu Apr 10 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-3
- Get on D-BUS.

* Fri Mar 28 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-2
- Fix translation in the init script (bug #87551).

* Wed Mar 26 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-1.1
- Turn off optimization on ia64 until bug #87383 is fixed.

* Wed Mar 26 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-1
- 1.1.18.
- No longer need uninit patch.
- Some parts of the iDefense and pdftops patches seem to have been
  picked up, but not others.

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-13
- Don't set SIGCHLD to SIG_IGN when using wait4 (via pclose) (bug #84101).

* Tue Feb  4 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-12
- Fix cups-lpd (bug #83452).

* Fri Jan 31 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-11
- Build ppds.dat on first install.

* Fri Jan 24 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-10
- Add support for rebuilding ppds.dat without running the scheduler
  proper (for bug #82500).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.1.17-9
- rebuilt

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-8
- Warn against editing queues managed by redhat-config-printer
  (bug #82267).

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-7
- Fix up error reporting in lpd backend.

* Thu Jan  9 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-6
- Add epoch to internal requirements.
- Make 'condrestart' return success exit code when daemon isn't running.

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.1.17-5
- Use pkg-config information to find SSL libraries.

* Thu Dec 19 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-4
- Security fixes.
- Make 'service cups reload' update the configuration first (bug #79953).

* Tue Dec 10 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-3
- Fix cupsd startup hang (bug #79346).

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-2
- Fix parallel backend behaviour when cancelling jobs.

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-1
- 1.1.17.
- No longer need libdir patch.
- Fix logrotate script (bug #76791).

* Wed Nov 20 2002 Tim Waugh <twaugh@redhat.com>
- Build requires XFree86-devel (bug #78362).

* Wed Nov 20 2002 Tim Waugh <twaugh@redhat.com>
- 1.1.16.
- Updated system-auth patch.
- Add ncp backend script.

* Wed Nov 13 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-15
- Set alternatives priority to 40.

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.15-14
- Buildrequire pam-devel.
- Patch default PAM config file to remove directory names from module paths,
  allowing the configuration files to work equally well on multilib systems.
- Patch default PAM config file to use system-auth, require the file at build-
  time because that's what data/Makefile checks for.

* Fri Nov  8 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-13
- Use logrotate for log rotation (bug #76791).
- No longer need cups.desktop, since redhat-config-printer handles it.

* Thu Oct 17 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-12
- Revert to libdir for CUPS_SERVERBIN.

* Thu Oct 17 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-11
- Use %%configure for multilib correctness.
- Use libexec instead of lib for CUPS_SERVERBIN.
- Ship translated man pages.
- Remove unshipped files.
- Fix file list permissions (bug #59021, bug #74738).
- Fix messy initscript output (bug #65857).
- Add 'reload' to initscript (bug #76114).

* Fri Aug 30 2002 Bernhard Rosenkraenzer <bero@redhat.de> 1.1.15-10
- Add generic postscript PPD file (#73061)

* Mon Aug 19 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-9
- Fix prefix in pstoraster (bug #69573).

* Mon Aug 19 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-8
- Disable cups-lpd by default (bug #71712).
- No need for fread patch now that glibc is fixed.

* Thu Aug 15 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-7
- Really add cups-lpd xinetd file (bug #63919).
- Ship pstoraster (bug #69573).
- Prevent fread from trying to read from beyond EOF (fixes a segfault
  with new glibc).

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 1.1.15-6
- rebuilt with gcc-3.2 (we hope)

* Mon Aug  5 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.15-5
- Add cups-lpd xinetd file (#63919)

* Tue Jul 23 2002 Florian La Roche <Florian.LaRoche@redhat.de> 1.1.15-4
- add a "exit 0" to postun script

* Tue Jul  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.15-3
- Add a symlink /usr/share/cups/doc -> /usr/share/doc/cups-devel-1.1.15
  because some applications expect to find the cups docs in
  /usr/share/cups/doc

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.15-1
- 1.1.15-1
- Fix up smb printing trigger (samba-client, not samba-clients)
- Start cupsd earlier, apparently it needs to be running before samba
  starts up for smb printing to work.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-17
- Rebuild in current environment
- [-16 never existed because of build system breakage]

* Wed Apr 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-15
- Fix bug #63387

* Mon Apr 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-14
- Fix dangling symlink created by samba-clients trigger

* Wed Apr 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-13
- Add desktop file and icon for CUPS configuration

* Wed Apr  3 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-12
- Support SMB printing (#62407)
- Add HTML redirections to doc files to work around users mistaking
  /usr/share/doc/cups-1.1.14 for the web frontend (#62405)

* Tue Apr  2 2002 Bill Nottingham <notting@redhat.com> 1.1.14-11
- fix subsys in initscript (#59206)
- don't strip binaries

* Mon Mar 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-10
- Make initscript use killproc instead of killall

* Fri Mar  8 2002 Bill Nottingham <notting@redhat.com> 1.1.14-9
- use alternatives --initscript support

* Mon Mar  4 2002 Bill Nottingham <notting@redhat.com> 1.1.14-8
- use the right path for the lpc man page, duh

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com> 1.1.14-7
- lpc man page is alternative too
- run ldconfig in -libs %%post/%%postun, not main
- remove alternatives in %%preun

* Wed Feb 27 2002 Bill Nottingham <notting@redhat.com> 1.1.14-6
- don't source /etc/sysconfig/network in cups.init, we don't use any
  values from it

* Tue Feb 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-4
- Fix bugs #60220 and #60352

* Thu Feb 21 2002 Tim Powers <timp@redhat.com>
- rebuild against correct version of openssl (0.9.6b)

* Wed Feb 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-2
- Add all man pages to alternatives (#59943)
- Update to real 1.1.14

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-1
- Update to almost-1.1.14

* Mon Feb 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-5
- Move cups-config to cups-devel subpackage
- Make alternatives usage a %%define to simplify builds for earlier
  releases
- Explicitly provide things we're supplying through alternatives
  to shut up kdeutils dependencies

* Tue Feb  5 2002 Tim Powers <timp@redhat.com>
- shut the alternatives stuff up for good

* Fri Feb  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-3
- Fix alternatives stuff
- Don't display error messages in %%post

* Wed Jan 30 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-2
- alternatives stuff

* Tue Jan 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-1
- 1.1.13
- Add patch for koi8-{r,u} and iso8859-8 encodings (#59018)
- Rename init scripts so we can safely "killall cupsd" from there

* Sat Jan 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.12-1
- Initial (conflicting, since alternatives isn't there yet) packaging for
  Red Hat Linux

* Sat Jan 19 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.12

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.10-3
- Compress PPD files
- Fix build with gcc 3.1
- Fix init script

* Tue Sep  4 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.10-2
- Fix URL
- Generate printcap
- s/Copyright/License/g

* Tue Sep  4 2001 Than Ngo <than@redhat.com> 1.1.10-1
- update to 1.1.10-1 for ExtraBinge 7.2

* Tue May 29 2001 Michael Stefaniuc <mstefani@redhat.com>
- update to 1.1.8
- changed cupsd.conf to generate /etc/printcap

* Tue May 15 2001 Than Ngo <than@redhat.com>
- update to 1.1.7, bugfixes

* Thu Dec 14 2000 Than Ngo <than@redhat.com>
- fixed package dependency with lpr and LPRng

* Wed Oct 25 2000 Than Ngo <than@redhat.com>
- remove man/cat

* Tue Oct 24 2000 Than Ngo <than@redhat.com>
- don't start cupsd service in level 0, fixed

* Thu Oct 19 2000 Than Ngo <than@redhat.com>
- update to 1.1.4
- fix CUPS_DOCROOT (Bug #18717)

* Fri Aug 11 2000 Than Ngo <than@redhat.de>
- update to 1.1.2 (Bugfix release)

* Fri Aug 4 2000 Than Ngo <than@redhat.de>
- fix, cupsd read config file under /etc/cups (Bug #15432)
- add missing cups filters

* Wed Aug 2 2000 Tim Powers <timp@redhat.com>
- rebuilt against libpng-1.0.8

* Tue Aug 01 2000 Than Ngo <than@redhat.de>
- fix permission, add missing ldconfig in %%post and %%postun (Bug #14963)

* Sat Jul 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.1 (this has some major bugfixes)
- Fix a typo in initscript (it's $?, not ?$)
- Fix /usr/etc vs. /etc trouble, don't insist on /usr/var (YUCK!)
- Create the spool dir

* Fri Jul 28 2000 Than Ngo <than@redhat.de>
- fix unclean code for building against gcc-2.96
- add missing restart function in startup script

* Fri Jul 28 2000 Tim Powers <timp@redhat.com>
- fixed initscript so that conrestart doesn't return 1 if the test fails

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Wed Jul 19 2000 Than Ngo <than@redhat.de>
- using service to fire them up
- fix Prereq section

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- added defattr to the devel package

* Sun Jul 16 2000 Than Ngo <than@redhat.de>
- add cups config files

* Sat Jul 15 2000 Than Ngo <than@redhat.de>
- update to 1.1 release
- move back to /etc/rc.d/init.d
- fix cupsd.init to work with /etc/init.d and /etc/rc.d/init.d
- split cups

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Thu Jul 06 2000 Tim Powers <timp@redhat.com>
- fixed broken PreReq to now require /etc/init.d

* Tue Jun 27 2000 Tim Powers <timp@redhat.com>
- PreReq initscripts >= 5.20

* Mon Jun 26 2000 Tim Powers <timp@redhat.com>
- started changelog 
- fixed init.d script location
- changed script in init.d quite a bit and made more like the rest of our
  startup scripts 
