# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora}
%bcond_without mdns
%bcond_without braille
%else
%bcond_with mdns
%bcond_with braille
%endif

# currently we use CUPS PPD compiler which will be removed
# in CUPS 3.0, then we will use PPD compiler from libppd-tools
%bcond_without cups_ppdc

# we build CUPS also with relro
%global _hardened_build 1

Summary: OpenPrinting CUPS filters for CUPS 2.X
Name:    cups-filters
Epoch:   1
Version: 2.0.1
Release: 12%{?dist}

# the CUPS exception text is the same as LLVM exception, so using that name with
# agreement from legal team
# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/message/A7GFSD6M3GYGSI32L2FC5KB22DUAEQI3/
License: Apache-2.0 WITH LLVM-exception

URL:     https://github.com/OpenPrinting/cups-filters
Source0: %{URL}/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1: lftocrlf.ppd
Source2: lftocrlf


# Patches
# https://github.com/OpenPrinting/cups-filters/pull/618
Patch001: 0001-Fix-build-failure-with-GCC-15-and-std-c23.patch
# introducing foomatic-hash, but without rejecting values in foomatic-rip
# https://github.com/OpenPrinting/cups-filters/pull/648
Patch002: 0001-Introduce-foomatic-hash-and-reject-unauthorized-valu.patch
# make sure errors from foomatic-rip are propagated
# https://github.com/OpenPrinting/cups-filters/pull/649
Patch003: foomatic-ripdie-error.patch
# rejecting the unknown values in foomatic-rip
# https://github.com/OpenPrinting/cups-filters/pull/648
Patch004: foomaticrip-reject-unknown-values.patch
# CVE-2025-64524 fix
Patch005: 0001-rastertopclx.c-Fix-infinite-loop-caused-by-crafted-f.patch


# driverless backend/driver was moved into a separate package to
# remove avahi dependency for filters
# remove once C10S is released and F40 is EOL
Conflicts: cups-filters-driverless < 1:2.0.0-3

# autogen.sh
BuildRequires: autoconf
# autogen.sh
BuildRequires: automake
# filter binaries and backends are written in C
BuildRequires: gcc
# autogen.sh
BuildRequires: gettext-devel
# for autosetup
BuildRequires: git-core
# autogen.sh
BuildRequires: libtool
# uses make for compiling
BuildRequires: make
# we use pkgconfig to get a proper devel packages
# proper CFLAGS and LDFLAGS
BuildRequires: pkgconf-pkg-config
# uses CUPS API
BuildRequires: pkgconfig(cups) >= 2.2.2
# uses cupsfilters API
BuildRequires: pkgconfig(libcupsfilters) >= 2.0b3
# uses PPD API
BuildRequires: pkgconfig(libppd) >= 2.0b3
# Make sure we get postscriptdriver tags.
BuildRequires: python3-cups
# for systemd unit for upgrade
BuildRequires: systemd-rpm-macros

%if %{with braille}
Recommends: braille-printer-app
%endif
# needs cups dirs
Requires: cups-filesystem


%description
Contains backends, filters, and other software that was
once part of the core CUPS distribution but is no longer maintained by
Apple Inc. In addition it contains additional filters developed
independently of Apple, especially filters for the PDF-centric printing
workflow introduced by OpenPrinting.


%package driverless
Summary: OpenPrinting driverless backends and drivers for CUPS 2.X
License: Apache-2.0 WITH LLVM-exception

# backends and drivers has been moved from the main package to subpackage
# to remove the avahi/mdns dependency needed for driverless
# remove after F40 is EOL and C10S is released
Conflicts: cups-filters < 1:2.0.0-3

# finding device via driverless depends on running avahi-daemon
Requires: avahi
# ippfind is used in driverless backend, not needed classic PPD based print queue
Requires: cups-ipptool
# cups-browsed needs systemd-resolved or nss-mdns for resolving .local addresses of remote print queues
# let's not require a specific package and let the user decide what he wants to use.
# just recommend nss-mdns for Fedora for now to have working default, but
# don't hardwire it for resolved users
%if %{with mdns}
Recommends: nss-mdns
%endif

# needs cups dirs
Requires: cups-filesystem


%description driverless
Contains backends and drivers for driverless implementation for cups-filters,
which makes driverless printers to be seen when listing printers nearby and gives
a specific generated driver for driverless printer in the local network. They are
tools for backward compatibility with applications which don't handle CUPS temporary
queues.


%prep
%autosetup -S git -N

%if 0%{?fedora} >= 43 || 0%{?rhel} >=9
%autopatch
%else
%autopatch -M 3
%endif


%build
# work-around Rpath
./autogen.sh

%configure --enable-driverless \
           --enable-individual-cups-filters \
           --disable-universal-cups-filter \
           --disable-mutool \
           --disable-rpath \
           --disable-silent-rules \
           --disable-static

%make_build


%install
%make_install

# 2229776 - Add textonly driver back, but as lftocrlf
install -p -m 0755 %{SOURCE2} %{buildroot}%{_cups_serverbin}/filter/lftocrlf
install -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/ppd/cupsfilters/lftocrlf.ppd

%if 0%{?fedora} >= 43 || 0%{?rhel} >=9

mkdir -p %{buildroot}%{_libexecdir}/%{name}

cat > %{buildroot}%{_libexecdir}/%{name}/posttrans.sh << EOF
#!/usr/bin/bash

if \$(grep -q -R 'FoomaticRIPCommandLine\|FoomaticRipOptionSetting' %{_sysconfdir}/cups/ppd)
then
  tmpfile=\$(mktemp -p /var/tmp foomatic-scan.XXXXXXXX)

  for ppd in %{_sysconfdir}/cups/ppd/*.ppd
  do
    foomatic-hash --ppd \$ppd \$tmpfile %{_sysconfdir}/foomatic/hashes.d/hashes.upgrade || :
  done

  if test -f %{_sysconfdir}/foomatic/hashes.d/hashes.upgrade
  then
    echo "Foomatic-rip values which can inject code found - review findings in \$tmpfile. Read release notes for instructions." || :
  fi
else
  touch %{_sysconfdir}/foomatic/hashes.d/hashes.new
fi

exit 0
EOF

mkdir -p %{buildroot}%{_unitdir}

cat > %{buildroot}%{_unitdir}/foomaticrip-upgrade.service << EOF
[Unit]
Description=Allowing already installed printers for foomatic-rip
ConditionPathIsDirectory=%{_sysconfdir}/foomatic/hashes.d
ConditionDirectoryNotEmpty=!%{_sysconfdir}/foomatic/hashes.d

[Service]
Type=oneshot
ExecStart=bash -c %{_libexecdir}/%{name}/posttrans.sh

[Install]
WantedBy=multi-user.target
EOF

mkdir -p %{buildroot}%{_unitdir}/cups.service.d

cat > %{buildroot}%{_unitdir}/cups.service.d/10-foomaticrip-upgrade.conf << EOF
[Unit]
After=foomaticrip-upgrade.service
Wants=foomaticrip-upgrade.service
EOF

%endif


# LSB3.2 requires /usr/bin/foomatic-rip,
# create it temporarily as a relative symlink
# we may use symlink to universal filter, but LSB is about guaranteed compatibility set
# among distibutions, so rather have the strict foomatic-rip filter...
ln -sf %{_cups_serverbin}/filter/foomatic-rip %{buildroot}%{_bindir}/foomatic-rip

%if %{with cups_ppdc}
mkdir -p %{buildroot}%{_datadir}/cups/ppdc
mv %{buildroot}%{_datadir}/{ppdc/pcl.h,cups/ppdc/pcl.h}
mv %{buildroot}%{_datadir}/{ppdc/escp.h,cups/ppdc/escp.h}
%endif

# remove license files which are in %%pkgdocdir
rm -f %{buildroot}%{_pkgdocdir}/{COPYING,NOTICE,LICENSE}

# remove INSTALL since it is unnecessary
rm -f %{buildroot}%{_pkgdocdir}/INSTALL

# remove CHANGES-1.x.md, since it is carried by a dependency
rm -f %{buildroot}%{_pkgdocdir}/CHANGES-1.x.md


%check
make check


%post
# remove PPD cache to make bz#2351389 fix work right away
# remove after F43 EOL
if [ $1 -gt 1 ]
then
  rm -f /var/cache/cups/ppds.dat || :
fi

%if 0%{?fedora} >= 43 || 0%{?rhel} >=9
  %systemd_post foomaticrip-upgrade.service
%endif


%preun
%if 0%{?fedora} >= 43 || 0%{?rhel} >=9
  %systemd_preun foomaticrip-upgrade.service
%endif


%postun
%if 0%{?fedora} >= 43 || 0%{?rhel} >=9
  %systemd_postun foomaticrip-upgrade.service
%endif


%posttrans
%if 0%{?fedora} >= 43 || 0%{?rhel} >=9
  %systemd_posttrans_with_reload foomaticrip-upgrade.service
%endif

if [ $1 -gt 1 ]
then
  # since we moved to individual filters, we have to restart cups
  # to load new conversion tables if it is running
  # remove by F43 EOL and C11S release
  if systemctl is-active cups &> /dev/null
  then
    systemctl restart cups || :
  fi

  %if 0%{?fedora} >= 43 || 0%{?rhel} >=9
    systemctl start foomaticrip-upgrade.service || :
  %endif
fi


%files
%license COPYING LICENSE NOTICE
%doc AUTHORS ABOUT-NLS CHANGES.md CONTRIBUTING.md DEVELOPING.md README.md
%{_bindir}/foomatic-hash
%{_bindir}/foomatic-rip
%attr(0744,root,root) %{_cups_serverbin}/backend/beh
# all backends needs to be run only as root because of kerberos
%attr(0744,root,root) %{_cups_serverbin}/backend/parallel
# Serial backend needs to run as root (bug #212577#c4).
%attr(0744,root,root) %{_cups_serverbin}/backend/serial
%attr(0755,root,root) %{_cups_serverbin}/filter/bannertopdf
%attr(0755,root,root) %{_cups_serverbin}/filter/commandtoescpx
%attr(0755,root,root) %{_cups_serverbin}/filter/commandtopclx
%attr(0755,root,root) %{_cups_serverbin}/filter/foomatic-rip
%attr(0755,root,root) %{_cups_serverbin}/filter/gstopdf
%attr(0755,root,root) %{_cups_serverbin}/filter/gstopxl
%attr(0755,root,root) %{_cups_serverbin}/filter/gstoraster
%attr(0755,root,root) %{_cups_serverbin}/filter/imagetopdf
%attr(0755,root,root) %{_cups_serverbin}/filter/imagetops
%attr(0755,root,root) %{_cups_serverbin}/filter/imagetoraster
# 2229776 - Add textonly driver back, but as lftocrlf
%attr(0755,root,root) %{_cups_serverbin}/filter/lftocrlf
%attr(0755,root,root) %{_cups_serverbin}/filter/pclmtoraster
%attr(0755,root,root) %{_cups_serverbin}/filter/pdftopdf
%attr(0755,root,root) %{_cups_serverbin}/filter/pdftops
%attr(0755,root,root) %{_cups_serverbin}/filter/pdftoraster
%attr(0755,root,root) %{_cups_serverbin}/filter/pwgtopclm
%attr(0755,root,root) %{_cups_serverbin}/filter/pwgtopdf
%attr(0755,root,root) %{_cups_serverbin}/filter/pwgtoraster
%attr(0755,root,root) %{_cups_serverbin}/filter/rastertoescpx
%attr(0755,root,root) %{_cups_serverbin}/filter/rastertopclx
%attr(0755,root,root) %{_cups_serverbin}/filter/rastertops
%attr(0755,root,root) %{_cups_serverbin}/filter/texttopdf
%attr(0755,root,root) %{_cups_serverbin}/filter/texttops
%attr(0755,root,root) %{_cups_serverbin}/filter/texttotext
%{_datadir}/cups/drv/cupsfilters.drv
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/cups/mime/cupsfilters-ghostscript.convs
%{_datadir}/cups/mime/cupsfilters-individual.convs
%{_datadir}/cups/mime/cupsfilters-poppler.convs
%dir %{_datadir}/foomatic
%dir %{_datadir}/foomatic/hashes.d
%{_datadir}/ppd/cupsfilters
%if %{with cups_ppdc}
# escp.h and pcl.h are required during runtime, because
# CUPS PPD compiler (ppdc) uses them for generating drivers
# per request from cupsfilters.drv file
%{_datadir}/cups/ppdc/escp.h
%{_datadir}/cups/ppdc/pcl.h
%else
%dir %{_datadir}/ppdc
%{_datadir}/ppdc/escp.h
%{_datadir}/ppdc/pcl.h
%endif
%{_mandir}/man1/foomatic-hash.1.gz
%{_mandir}/man1/foomatic-rip.1.gz
%config(noreplace) %{_sysconfdir}/foomatic
%if 0%{?fedora} >= 43 || 0%{?rhel} >=9
%dir %{_libexecdir}/%{name}
%attr(0744,root,root) %{_libexecdir}/%{name}/posttrans.sh
%ghost %attr(0644,root,root) %{_sysconfdir}/foomatic/hashes.d/hashes.new
%dir %{_unitdir}/cups.service.d
%{_unitdir}/cups.service.d/10-foomaticrip-upgrade.conf
%{_unitdir}/foomaticrip-upgrade.service
%endif

%files driverless
%license COPYING LICENSE NOTICE
%{_bindir}/driverless
%{_bindir}/driverless-fax
%{_cups_serverbin}/backend/driverless
%{_cups_serverbin}/backend/driverless-fax
%{_cups_serverbin}/driver/driverless
%{_cups_serverbin}/driver/driverless-fax
%{_mandir}/man1/driverless.1.gz


%changelog
* Fri Nov 28 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-12
- fix CVE-2025-64524

* Mon Nov 10 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-11
- change return value of foomatic-hash if built without libppd

* Wed Oct 01 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-10
- protect older Fedoras from F43+ changes, fix installability report about hashes.new

* Thu Jul 31 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-9
- Reject unknown values in foomatic-rip in F43+

* Wed Jul 30 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-8
- Introduce foomatic-hash, but not rejecting values in foomatic-rip

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 09 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-6
- CUPS restart has to happen after universal filter is gone for good (in posttrans) (fedora#2370978)

* Mon Jun 02 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-5
- individual filters have to explicitly enabled

* Mon Jun 02 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-4
- disable universal filter for now - some 3rd party drivers did not work with it

* Tue Mar 11 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-3
- textonly driver was missing (fedora#2351389)

* Fri Jan 24 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-2
- fix FTBFS (fedora#2340017)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 15 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.1-1
- 2.0.1

* Fri Jul 19 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-9
- fix missing epochs in conflicts

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 28 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-7
- 2283295 - The directory /usr/share/ppdc/ is not in the RPM database.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-4
- make driverless subpackage require avahi and ipptool - they don't 
  work without them

* Tue Dec 19 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-3
- introduce cups-filters-driverless to strip avahi dependency for filters

* Tue Dec 19 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-2
- use exact foomatic-rip filter to comply with LSB

* Thu Oct 19 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-1
- rebase to 2.0.0

* Mon Aug 07 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~rc2-3
- 2229776 - Add textonly driver back as lftocrlf driver

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0~rc2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~rc2-1
- 2.0rc2

* Wed May 17 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~rc1-2
- 2207970 - CVE-2023-24805 cups-filters: remote code execution in cups-filters, beh CUPS backend

* Thu Apr 27 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~rc1-1
- 2.0rc1

* Wed Mar 01 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~b3-2
- use epoch to ensure clean upgrade path, because I didn't read FPG carefully

* Mon Feb 20 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2.0b3-1
- 2170538 - rebase to 2.0b3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 13 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.16-6
- really build with qpdf-11.1.1 (forgot to wait for qpdf in side tag...)

* Thu Oct 13 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.16-5
- rebuilt with qpdf-11.1.1

* Thu Sep 22 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.16-4
- rebuilt with qpdf-11.1.0

* Thu Sep 22 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.16-3
- build braille subpackage only on Fedora and CentOS Stream > 9

* Wed Sep 21 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.16-2
- disable frequent network interface data update, which slows down the queue creation

* Thu Sep 08 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.16-1
- 1.28.16

* Thu Sep 08 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.15-3
- 2123809 - rpm -Va reports error on /etc/cups/cups-browsed.conf

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Apr 20 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.15-1
- 1.28.15

* Thu Apr 07 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.14-1
- 1.28.14

* Mon Mar 28 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.13-1
- 1.28.13

* Tue Mar 08 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.12-1
- 1.28.12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.11-2
- raise the NVR to get a new build

* Mon Jan 17 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.11-1
- 1.28.11

* Mon Jan 17 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.10-4
- fix typo in braille requires

* Mon Jan 17 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.10-3
- 2040973 - Make Braille printing support optional

* Mon Dec 06 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.10-2
- 1995728 - Enable braille printing

* Tue Sep 14 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.10-1
- 1.28.10

* Tue Jul 27 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.9-5
- rebuilt with poppler-21.07.0

* Tue Jul 27 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.9-4
- remove build requirement on poppler-devel - we need just poppler-cpp-devel

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.9-2
- 1981603 - pdftopdf doesn't handle "page-range=10-2147483647" correctly

* Mon Jun 21 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.9-1
- 1.28.9

* Mon Jun 21 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.8-2
- 1973056 - cups-browsed doesn't renew DBus subscription in time and all printing comes to a halt

* Fri May 14 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.8-1
- 1.28.8

* Wed Apr 28 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.7-7
- 1954524 - cups-browsed doesn't save "*-default" options

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.28.7-6
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 01 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.7-5
- put nss-mdns only for Fedora

* Thu Jan 28 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.7-4
- remove nss-mdns - dont require a specific way how to resolve .local addresses

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.7-2
- unpush fix for 1904405 - M281fdw now often chokes on URF

* Mon Jan 11 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.7-1
- 1.28.7, urftopdf nor pdftoopvp aren't compiled anymore
- 1904405 - HP M281fdw: čžš characters printed as squares with "driverless" driver

* Mon Dec 07 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.6-1
- 1.28.6

* Tue Dec 01 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.5-4
- filters using ijs were removed, removed the dep

* Tue Nov 24 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.5-3
- fix various memory issues within cups-browsed

* Thu Nov 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.5-2
- use make and git-core

* Mon Nov 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.5-1
- 1.28.5, 1881365 - cups-browsed crashing

* Tue Sep 29 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.2-3
- 1891720 - foomatic-rip files up /var/spool/tmp with temporary files

* Thu Sep 17 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.2-2
- 1879147 - driverless cannot generate ppd for dns-sd based uris

* Tue Sep 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.2-1
- 1.28.2

* Thu Sep 03 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.1-2
- revert previous commit - systemd-resolved doesn't work with avahi right now
  because missing link in NetworkManager

* Mon Aug 31 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.1-2
- MDNS resolving should be done by systemd-resolved now

* Thu Aug 27 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.28.1-1
- 1.28.1 - added driverless fax support

* Fri Aug 21 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.5-7
- use configure option instead of downstream, cups-browsed.conf editing, patch
- the exact path in cups-browsed manpage was removed, use the patch removing it instead of downstream one
- use configure option to dont save queues between restarts instead of downstream patch reverting the issue
- memory leaks patch is from upstream too

* Wed Aug 19 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.5-6
- 1867412 - cups-browsed leaks memory

* Thu Aug 06 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.5-5
- require ipptool explicitly
- remove buildrequire on ipptool

* Wed Aug 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.5-4
- use %%make_build and %%make_install according FPG
- own 'new' directories

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.5-2
- 1848575 - [cups, cups-filters] PPD generators creates invalid cupsManualCopies entry

* Mon Jun 08 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.5-1
- 1.27.5

* Tue Apr 14 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.4-1
- 1.27.4

* Wed Apr 08 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.3-3
- memory issues in cups-browsed

* Mon Apr 06 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.3-2
- make nss-mdns and avahi recommended

* Mon Mar 23 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.3-1
- 1.27.3

* Fri Mar 13 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.2-2
- fix leaks in cups-browsed
- add require on nss-mdns

* Mon Mar 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.2-1
- 1.27.2

* Tue Feb 25 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.1-2
- 1806862 - foomatic-rip handles empty files in bad way

* Tue Feb 18 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.1-1
- 1.27.1

* Tue Feb 18 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.0-2
- 1802969 - Service "cups-browsed" is crashing all the time

* Tue Jan 28 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.27.0-1
- 1.27.0
- add post scriptlet for update

* Wed Jan 22 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-13
- fix build with GCC 10 and remove old obsoletes

* Fri Jan 17 2020 Marek Kasik <mkasik@redhat.com> - 1.22.5-11
- Rebuild for poppler-0.84.0

* Wed Jan 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-11
- add buildrequires fro systemd-rpm-macros

* Tue Nov 26 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-10
- 1776271 - Updated cups-browsed in RHEL 7.7 leaks sockets

* Tue Nov 19 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-9
- rebuilt for qpdf-9.1.0

* Tue Oct 22 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-8
- 1756726 - Epson ET 7700 reports pwg support, but pwg does not work

* Wed Oct 09 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-7
- gs 9.27 now uses setfilladjust2

* Tue Sep 17 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-6
- ftbfs with qpdf-9.0.0
- pdftopdf output should not be encrypted

* Wed Sep 11 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-5
- require colord, because it is needed for ICC profiles for filters

* Tue Aug 13 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-4
- 1740122 - foomatic-rip segfaults when env variable PRINTER is not defined

* Wed Aug 07 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-3
- remove unneeded scriptlet

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.5-1
- 1.22.5

* Tue Mar 26 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.3-1
- 1.22.3

* Fri Feb 01 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.0-4
- cups-brf needs to be run as root

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Marek Kasik <mkasik@redhat.com> - 1.22.0-2
- Rebuild for poppler-0.73.0

* Fri Jan 25 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.22.0-1
- 1.22.0

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.21.6-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Tue Jan 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.21.6-1
- 1.21.6

* Thu Dec 13 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.21.5-1
- 1.21.5

* Mon Nov 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.21.2-4
- links in manpages are wrong

* Mon Sep 24 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.21.2-3
- 1632267 - cups-filters needs to obsolete ghostscript-cups and foomatic-filters
- rebuilt for qpdf-8.2.1

* Fri Sep 21 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.21.2-2
- 1628255 - cups-filters: Sticky EOF behavior in glibc breaks descriptor concatenation using dup2 (breaks printing)

* Mon Sep 10 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.21.2-1
- 1.21.2

* Tue Aug 14 2018 Marek Kasik <mkasik@redhat.com> - 1.20.3-7
- Rebuild for poppler-0.67.0

* Tue Jul 24 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.3-6
- correcting license

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.3-4
- rebuilt for new qpdf-8.1.0

* Tue Jun 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.3-3
- hybrid pdftops filter requires poppler and ghostscript for run

* Tue Jun 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.3-2
- cups-browsed needs to have cups.service to run

* Fri Apr 13 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.3-1
- 1.20.3

* Wed Apr 04 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.2-1
- 1.20.2
- fixing discovering of remote CUPS queues and LDAP queues
- dependency on poppler-utils is now only recommended

* Fri Mar 23 2018 Marek Kasik <mkasik@redhat.com> - 1.20.1-4
- Rebuild for poppler-0.63.0

* Wed Mar 07 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.1-3
- Rebuilt for qpdf-8.0.2

* Mon Mar 05 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.1-2
- 1.20.1

* Wed Feb 28 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.0-8
- add explicit soname -> warning about soname change

* Wed Feb 21 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.0-7
- libjpeg is shipped in libjpeg-turbo and pkgconfig in pkgconf-pkg-config

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.0-6
- gcc and gcc-c++ is no longer in buildroot by default

* Wed Feb 14 2018 David Tardon <dtardon@redhat.com> - 1.20.0-5
- rebuild for poppler 0.62.0

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.20.0-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.0-3
- remove old stuff https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/MRWOMRZ6KPCV25EFHJ2O67BCCP3L4Y6N/

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.20.0-1
- Rebase to 1.20.0

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.19.0-2
- Rebuilt for switch to libxcrypt

* Tue Jan 16 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.19.0-1
- Rebase to 1.19.0

* Thu Jan 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.9-5
- adding build dependency on ghostscript because of its package changes

* Tue Jan 02 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.9-4
- 1529680 - set CreateIPPPrintQueues to ALL and LocalRemoteCUPSQueueNaming to RemoteName

* Mon Nov 20 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.9-3
- fixing patch for upstream issue 1413

* Wed Nov 08 2017 David Tardon <dtardon@redhat.com> - 1.17.9-2
- rebuild for poppler 0.61.0

* Wed Oct 18 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.9-1
- rebase to 1.17.9

* Mon Oct 09 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.8-4
- removing Provides ghostscript-cups and foomatic-filters

* Fri Oct 06 2017 David Tardon <dtardon@redhat.com> - 1.17.8-3
- rebuild for poppler 0.60.1

* Fri Oct 06 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.8-2
- upstream 1413 - Propagation of location doesn't work

* Tue Oct 03 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.8-1
- rebase to 1.17.8

* Tue Sep 19 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.7-1
- rebase to 1.17.7

* Fri Sep 08 2017 David Tardon <dtardon@redhat.com> - 1.17.2-2
- rebuild for poppler 0.59.0

* Wed Sep 06 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.17.2-1
- rebase to 1.17.2

* Tue Aug 22 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.16.3-1
- rebase to 1.16.3

* Mon Aug 14 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.16.1-1
- rebase to 1.16.1

* Thu Aug 10 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.16.0-2
- rebuilt for qpdf-libs

* Mon Aug 07 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.16.0-1
- rebase to 1.16.0

* Thu Aug 03 2017 David Tardon <dtardon@redhat.com> - 1.14.1-5
- rebuild for poppler 0.57.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 1.14.1-2
- Rebuilt for Boost 1.64

* Fri Jun 30 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.14.1-1
- rebase to 1.14.1

* Thu Jun 29 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.14.0-3
- update python Requires/BuildRequires accordingly to Fedora Guidelines for Python (python-cups -> python3-cups)

* Wed May 31 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.14.0-2
- removing BuildRequires: mupdf

* Wed May 17 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.14.0-1
- rebase to 1.14.0

* Fri Apr 28 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.13.5-1
- rebase to 1.13.5

* Tue Mar 28 2017 David Tardon <dtardon@redhat.com> - 1.13.4-2
- rebuild for poppler 0.53.0

* Fri Feb 24 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.13.4-1
- rebase to 1.13.4
- 1426567 - Added queues are not marked as remote ones

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1.13.3-3
- Rebuilt for Boost 1.63

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1.13.3-2
- Rebuilt for Boost 1.63

* Thu Jan 19 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.13.3-1
- rebase to 1.13.3

* Mon Jan 02 2017 Zdenek Dohnal <zdohnal@redhat.com> - 1.13.2-1
- rebase to 1.13.2

* Mon Dec 19 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.13.1-1
- rebase to 1.13.1

* Fri Dec 16 2016 David Tardon <dtardon@redhat.com> - 1.13.0-2
- rebuild for poppler 0.50.0

* Mon Dec 12 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.13.0-1
- rebase to 1.13.0

* Fri Dec 02 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.12.0-2
- adding new sources

* Fri Dec 02 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.12.0-1
- rebase to 1.12.0

* Wed Nov 23 2016 David Tardon <dtardon@redhat.com> - 1.11.6-2
- rebuild for poppler 0.49.0

* Fri Nov 11 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.11.6-1
- rebase to 1.11.6

* Mon Oct 31 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.11.5-1
- rebase to 1.11.5

* Fri Oct 21 2016 Marek Kasik <mkasik@redhat.com> - 1.11.4-2
- Rebuild for poppler-0.48.0

* Tue Sep 27 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.11.4-1
- rebase to 1.11.4 

* Tue Sep 20 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.11.3-1
- rebase to 1.11.3

* Tue Aug 30 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.11.2-1
- rebase to 1.11.2, adding cupsfilters-poppler.convs and cupsfilters-mupdf.convs into package

* Wed Aug 03 2016 Jiri Popelka <jpopelka@redhat.com> - 1.10.0-3
- %%{_defaultdocdir}/cups-filters/ -> %%{_pkgdocdir}

* Mon Jul 18 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.10.0-2
- adding new sources cups-filters-1.10.0 

* Mon Jul 18 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.10.0-1
- rebase 1.10.0, include missing ppd.h

* Mon Jul 18 2016 Marek Kasik <mkasik@redhat.com> - 1.9.0-2
- Rebuild for poppler-0.45.0

* Fri Jun 10 2016 Jiri Popelka <jpopelka@redhat.com> - 1.9.0-1
- 1.9.0

* Tue May  3 2016 Marek Kasik <mkasik@redhat.com> - 1.8.3-2
- Rebuild for poppler-0.43.0

* Thu Mar 24 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.8.3-1
- Update to 1.8.3, adding cupsfilters-ghostscript.convs to %%files

* Fri Feb 12 2016 Jiri Popelka <jpopelka@redhat.com> - 1.8.2-1
- 1.8.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Marek Kasik <mkasik@redhat.com> - 1.8.1-2
- Rebuild for poppler-0.40.0

* Fri Jan 22 2016 Jiri Popelka <jpopelka@redhat.com> - 1.8.1-1
- 1.8.1

* Thu Jan 21 2016 Jiri Popelka <jpopelka@redhat.com> - 1.8.0-1
- 1.8.0

* Tue Jan 19 2016 Jiri Popelka <jpopelka@redhat.com> - 1.7.0-1
- 1.7.0

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 1.6.0-2
- Rebuilt for Boost 1.60

* Thu Jan 14 2016 Jiri Popelka <jpopelka@redhat.com> - 1.6.0-1
- 1.6.0

* Fri Dec 18 2015 Jiri Popelka <jpopelka@redhat.com> - 1.5.0-1
- 1.5.0

* Tue Dec 15 2015 Jiri Popelka <jpopelka@redhat.com> - 1.4.0-1
- 1.4.0

* Wed Dec 09 2015 Jiri Popelka <jpopelka@redhat.com> - 1.3.0-1
- 1.3.0

* Fri Nov 27 2015 Jiri Popelka <jpopelka@redhat.com> - 1.2.0-1
- 1.2.0

* Wed Nov 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.0-2
- Rebuild (qpdf-6)

* Tue Oct 27 2015 Jiri Popelka <jpopelka@redhat.com> - 1.1.0-1
- 1.1.0 (version numbering change: minor version = feature, revision = bugfix)

* Sun Sep 13 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.76-1
- 1.0.76

* Tue Sep 08 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.75-1
- 1.0.75

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.0.74-2
- Rebuilt for Boost 1.59

* Wed Aug 26 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.74-1
- 1.0.74

* Wed Aug 19 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.73-1
- 1.0.73 - new implicitclass backend

* Fri Jul 24 2015 David Tardon <dtardon@redhat.com> - 1.0.71-3
- rebuild for Boost 1.58 to fix deps

* Thu Jul 23 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0.71-2
- Add upstream patch for poppler 0.34 support

* Wed Jul 22 2015 Marek Kasik <mkasik@redhat.com> - 1.0.71-2
- Rebuild (poppler-0.34.0)

* Fri Jul 03 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.71-1
- 1.0.71

* Mon Jun 29 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.70-1
- 1.0.70

* Mon Jun 22 2015 Tim Waugh <twaugh@redhat.com> - 1.0.69-3
- Fixes for glib source handling (bug #1228555).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.69-1
- 1.0.69

* Fri Jun  5 2015 Marek Kasik <mkasik@redhat.com> - 1.0.68-2
- Rebuild (poppler-0.33.0)

* Tue Apr 14 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.68-1
- 1.0.68

* Wed Mar 11 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.67-1
- 1.0.67

* Mon Mar 02 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.66-1
- 1.0.66

* Mon Feb 16 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.65-1
- 1.0.65

* Fri Jan 23 2015 Marek Kasik <mkasik@redhat.com> - 1.0.61-3
- Rebuild (poppler-0.30.0)

* Thu Nov 27 2014 Marek Kasik <mkasik@redhat.com> - 1.0.61-2
- Rebuild (poppler-0.28.1)

* Fri Oct 10 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.61-1
- 1.0.61 

* Tue Oct 07 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.60-1
- 1.0.60

* Sun Sep 28 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.59-1
- 1.0.59

* Thu Aug 21 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.58-1
- 1.0.58

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.55-2
- Use %%_defaultdocdir instead of %%doc

* Mon Jul 28 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.55-1
- 1.0.55

* Fri Jun 13 2014 Tim Waugh <twaugh@redhat.com> - 1.0.54-4
- Really fix execmem issue (bug #1079534).

* Wed Jun 11 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.54-3
- Remove (F21) pdf-landscape.patch

* Wed Jun 11 2014 Tim Waugh <twaugh@redhat.com> - 1.0.54-2
- Fix build issue (bug #1106101).
- Don't use grep's -P switch in pstopdf as it needs execmem (bug #1079534).
- Return work-around patch for bug #768811.

* Mon Jun 09 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.54-1
- 1.0.54

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.53-3
- Remove BuildRequires pkgconfig(lcms). pkgconfig(lcms2) is enough.

* Tue May 13 2014 Marek Kasik <mkasik@redhat.com> - 1.0.53-2
- Rebuild (poppler-0.26.0)

* Mon Apr 28 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.53-1
- 1.0.53

* Wed Apr 23 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.52-2
- Remove pdftoopvp and urftopdf in %%install instead of not building them.

* Tue Apr 08 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.52-1
- 1.0.52

* Wed Apr 02 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.51-1
- 1.0.51 (#1083327)

* Thu Mar 27 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.50-1
- 1.0.50

* Mon Mar 24 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.49-1
- 1.0.49

* Wed Mar 12 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.48-1
- 1.0.48

* Tue Mar 11 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.47-2
- Don't ship pdftoopvp (#1027557) and urftopdf (#1002947).

* Tue Mar 11 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.47-1
- 1.0.47: CVE-2013-6473 CVE-2013-6476 CVE-2013-6474 CVE-2013-6475 (#1074840)

* Mon Mar 10 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.46-3
- BuildRequires: pkgconfig(foo) instead of foo-devel

* Tue Mar  4 2014 Tim Waugh <twaugh@redhat.com> - 1.0.46-2
- The texttopdf filter requires a TrueType monospaced font
  (bug #1070729).

* Thu Feb 20 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.46-1
- 1.0.46

* Fri Feb 14 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.45-1
- 1.0.45

* Mon Jan 20 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.44-1
- 1.0.44

* Tue Jan 14 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.43-2
- add /usr/bin/foomatic-rip symlink, due to LSB3.2 (#1052452)

* Fri Dec 20 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.43-1
- 1.0.43: upstream fix for bug #768811 (pdf-landscape)

* Sat Nov 30 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.42-1
- 1.0.42: includes foomatic-rip (obsoletes foomatic-filters package)

* Tue Nov 19 2013 Tim Waugh <twaugh@redhat.com> - 1.0.41-4
- Adjust filter costs so application/vnd.adobe-read-postscript input
  doesn't go via pstotiff (bug #1008166).

* Thu Nov 14 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.41-3
- Fix memory leaks in cups-browsed (bug #1027317).

* Wed Nov  6 2013 Tim Waugh <twaugh@redhat.com> - 1.0.41-2
- Include dbus so that colord support works (bug #1026928).

* Wed Oct 30 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.41-1
- 1.0.41 - PPD-less printing support

* Mon Oct 21 2013 Tim Waugh <twaugh@redhat.com> - 1.0.40-4
- Fix socket leaks in the BrowsePoll code (bug #1021512).

* Wed Oct 16 2013 Tim Waugh <twaugh@redhat.com> - 1.0.40-3
- Ship the gstoraster MIME conversion rule now we provide that filter
  (bug #1019261).

* Fri Oct 11 2013 Tim Waugh <twaugh@redhat.com> - 1.0.40-2
- Fix PDF landscape printing (bug #768811).

* Fri Oct 11 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.40-1
- 1.0.40
- Use new "hybrid" pdftops renderer.

* Thu Oct 03 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.39-1
- 1.0.39
- Removed obsolete patches "pdf-landscape" and "browsepoll-notifications"

* Tue Oct  1 2013 Tim Waugh <twaugh@redhat.com> - 1.0.38-4
- Use IPP notifications for BrowsePoll when possible (bug #975241).

* Tue Oct  1 2013 Tim Waugh <twaugh@redhat.com> - 1.0.38-3
- Fixes for some printf-type format mismatches (bug #1014093).

* Tue Sep 17 2013 Tim Waugh <twaugh@redhat.com> - 1.0.38-2
- Fix landscape printing for PDFs (bug #768811).

* Wed Sep 04 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.38-1
- 1.0.38

* Thu Aug 29 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.37-1
- 1.0.37.

* Tue Aug 27 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.36-5
- Added build dependency - font required for running tests

* Tue Aug 27 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.36-4
- Added checking phase (make check)

* Wed Aug 21 2013 Tim Waugh <twaugh@redhat.com> - 1.0.36-3
- Upstream patch to re-work filter costs (bug #998977). No longer need
  text filter costs patch as paps gets used by default now if
  installed.

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 1.0.36-2
- Rebuild (poppler-0.24.0)

* Tue Aug 13 2013 Tim Waugh <twaugh@redhat.com> - 1.0.36-1
- 1.0.36.

* Tue Aug 13 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-7
- Upstream patch to move in filters from ghostscript.

* Tue Jul 30 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-6
- Set cost for text filters to 200 so that the paps filter gets
  preference for the time being (bug #988909).

* Wed Jul 24 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-5
- Handle page-label when printing n-up as well.

* Tue Jul 23 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-4
- Added support for page-label (bug #987515).

* Thu Jul 11 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.35-3
- Rebuild (qpdf-5.0.0)

* Mon Jul 01 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.35-2
- add cups-browsed(8) and cups-browsed.conf(5)
- don't reverse lookup IP address in URI (#975822)

* Wed Jun 26 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.35-1
- 1.0.35

* Mon Jun 24 2013 Marek Kasik <mkasik@redhat.com> - 1.0.34-9
- Rebuild (poppler-0.22.5)

* Wed Jun 19 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-8
- fix the note we add in cups-browsed.conf

* Wed Jun 12 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-7
- Obsolete cups-php (#971741)

* Wed Jun 05 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-6
- one more cups-browsed leak fixed (#959682)

* Wed Jun 05 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-5
- perl is actually not required by pstopdf, because the calling is in dead code

* Mon Jun 03 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-4
- fix resource leaks and other problems found by Coverity & Valgrind (#959682)

* Wed May 15 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-3
- ship ppdc/pcl.h because of cupsfilters.drv

* Tue May 07 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-2
- pstopdf requires bc (#960315)

* Thu Apr 11 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-1
- 1.0.34

* Fri Apr 05 2013 Fridolin Pokorny <fpokorny@redhat.com> - 1.0.33-1
- 1.0.33
- removed cups-filters-1.0.32-null-info.patch, accepted by upstream

* Thu Apr 04 2013 Fridolin Pokorny <fpokorny@redhat.com> - 1.0.32-2
- fixed segfault when info is NULL

* Thu Apr 04 2013 Fridolin Pokorny <fpokorny@redhat.com> - 1.0.32-1
- 1.0.32

* Fri Mar 29 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.31-3
- add note to cups-browsed.conf

* Thu Mar 28 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.31-2
- check cupsd.conf existence prior to grepping it (#928816)

* Fri Mar 22 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.31-1
- 1.0.31

* Tue Mar 19 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-4
- revert previous change

* Wed Mar 13 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-3
- don't ship banners for now (#919489)

* Tue Mar 12 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-2
- move BrowsePoll from cupsd.conf to cups-browsed.conf in %%post

* Fri Mar 08 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-1
- 1.0.30: CUPS browsing and broadcasting in cups-browsed

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.29-3
- backport upstream buildfix for poppler-0.22.x

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.0.29-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 03 2013 Jiri Popelka <jpopelka@redhat.com> 1.0.29-1
- 1.0.29

* Wed Jan 02 2013 Jiri Popelka <jpopelka@redhat.com> 1.0.28-1
- 1.0.28: cups-browsed daemon and service

* Thu Nov 29 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.25-1
- 1.0.25

* Fri Sep 07 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.24-1
- 1.0.24

* Wed Aug 22 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.23-1
- 1.0.23: old pdftopdf removed

* Tue Aug 21 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.22-1
- 1.0.22: new pdftopdf (uses qpdf instead of poppler)

* Wed Aug 08 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-4
- rebuild

* Thu Aug 02 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-3
- commented multiple licensing breakdown (#832130)
- verbose build output

* Thu Aug 02 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-2
- BuildRequires: poppler-cpp-devel (to build against poppler-0.20)

* Mon Jul 23 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-1
- 1.0.20

* Tue Jul 17 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.19-1
- 1.0.19

* Wed May 30 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.18-1
- initial spec file
