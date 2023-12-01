Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           netcf
Version:        0.2.8
Release:        16%{?dist}
Summary:        Cross-platform network configuration library

License:        LGPLv2+
URL:            https://fedorahosted.org/netcf/
Source0:        https://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.gz

# Patches
# One patch per line, in this format:
# Patch001: file1.patch
# Patch002: file2.patch
# ...
#
# The patches will automatically be put into the build source tree
# during the %prep stage (using git, which is now required for an rpm
# build)
#
Patch001: netcf-call-aug_load-at-most-once-per-second.patch
Patch002: netcf-optimize-aug_match-query-for-all-ifcfg-files-related.patch
Patch003: netcf-linux-include-bond-element-for-bonds-with-no-slaves.patch
Patch004: netcf-Properly-classify-bond-devices-with-no-slaves.patch

# Default to skipping autoreconf.  Distros can change just this one
# line (or provide a command-line override) if they backport any
# patches that touch configure.ac or Makefile.am.
%{!?enable_autotools:%define enable_autotools 0}

# git is used to build a source tree with patches applied (see the
# %prep section)
BuildRequires:  gcc
BuildRequires: git

# Fedora 20 / RHEL-7 are where netcf first uses systemd. Although earlier
# Fedora has systemd, netcf still used sysvinit there.

    %define with_systemd 1




%if %{with_systemd}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: /usr/bin/pod2man
%endif

BuildRequires:  readline-devel augeas-devel >= 0.5.2
BuildRequires:  libxml2-devel libxslt-devel

# force the --with-libnl1 option on F17/RHEL6 and earlier

%define with_libnl1 0

# require libnl3 on F18/RHEL7 and later

BuildRequires:  libnl3-devel




Requires:       %{name}-libs = %{version}-%{release}

Provides: bundled(gnulib)

%description
Netcf is a library used to modify the network configuration of a
system. Network configurations are expressed in a platform-independent
XML format, which netcf translates into changes to the system's
'native' network configuration files.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        libs
Summary:        Libraries for %{name}

# bridge-utils is needed because /sbin/ifup calls brctl
# if you create a bridge device
Requires:       bridge-utils

%description    libs
The libraries for %{name}.

%prep
%setup -q

# Patches have to be stored in a temporary file because RPM has
# a limit on the length of the result of any macro expansion;
# if the string is longer, it's silently cropped
%{lua:
    tmp = os.tmpname();
    f = io.open(tmp, "w+");
    count = 0;
    for i, p in ipairs(patches) do
        f:write(p.."\n");
        count = count + 1;
    end;
    f:close();
    print("PATCHCOUNT="..count.."\n")
    print("PATCHLIST="..tmp.."\n")
}

git init -q
git config user.name rpm-build
git config user.email rpm-build
git config gc.auto 0
git add .
git commit -q -a --author 'rpm-build <rpm-build>' \
           -m '%{name}-%{version} base'

COUNT=$(grep '\.patch$' $PATCHLIST | wc -l)
if [ $COUNT -ne $PATCHCOUNT ]; then
    echo "Found $COUNT patches in $PATCHLIST, expected $PATCHCOUNT"
    exit 1
fi
if [ $COUNT -gt 0 ]; then
    xargs git am <$PATCHLIST || exit 1
fi
echo "Applied $COUNT patches"
rm -f $PATCHLIST


%build
%if %{with_libnl1}
%define _with_libnl1 --with-libnl1
%endif
%if %{with_systemd}
    %define sysinit --with-sysinit=systemd
%else
    %define sysinit --with-sysinit=initscripts
%endif


%if 0%{?enable_autotools}
 autoreconf -if
%endif

%configure --with-driver=redhat \
           --disable-static \
           %{?_with_libnl1} \
           %{sysinit}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT SYSTEMD_UNIT_DIR=%{_unitdir} \
     INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -delete

%preun libs

%if %{with_systemd}
    %systemd_preun netcf-transaction.service
%else
if [ $1 = 0 ]; then
    /sbin/chkconfig --del netcf-transaction
fi
%endif

%post libs

%if %{with_systemd}
    %systemd_post netcf-transaction.service
    /bin/systemctl --no-reload enable netcf-transaction.service >/dev/null 2>&1 || :
%else
/sbin/chkconfig --add netcf-transaction
%endif

%postun libs

%if %{with_systemd}
    %systemd_postun netcf-transaction.service
%endif

%files
%{_bindir}/ncftool
%{_mandir}/man1/ncftool.1*

%files libs
%{_datadir}/netcf
%{_libdir}/*.so.*
%if %{with_systemd}
%{_unitdir}/netcf-transaction.service
%else
%{_sysconfdir}/rc.d/init.d/netcf-transaction
%endif
%attr(0755, root, root) %{_libexecdir}/netcf-transaction.sh
%doc AUTHORS COPYING NEWS

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/netcf.pc

%changelog
* Wed Jun 16 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.2.8-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Specify "redhat" network driver to enable build

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.8-13
- Rebuild for readline 8.0

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.8-12
- Remove obsolete scriptlets

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.2.8-5
- Rebuild for readline 7.x

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Laine Stump <laine@redhat.com>
 - Improve performance with large number of interfaces
   (Bug 1268384, Bug 1271341)
 - recognize bond devices with no slaves

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Laine Stump <laine@redhat.com> - 0.2.8-1
 - rebase to netcf-0.2.8
 - Fix build on systems with newer libnl3 that doesn't
   #include <linux/if.h>

* Mon Apr 06 2015 Laine Stump <laine@redhat.com> - 0.2.7-1
 - rebase to netcf-0.2.7
 - resolve CVE-2014-8119
 - support multiple IPv4 addresses in interface config (redhat driver)
 - allow static IPv4 config simultaneous with DHCPv4 (redhat driver)
 - recognize IPADDR0/NETMASK0/PREFIX0
 - remove extra quotes from IPV6ADDR_SECONDARIES (redhat+suse drivers)
 - miscellaneous systemd service fixes
 - use git to apply patches in rpm specfile
 - revert the 0.2.6-2 specfile patch mentioned below (now fixed properly)

* Thu Jan  8 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.6-2
- do not write to the console (#1135744)

* Fri Aug 22 2014 Laine Stump <laine@redhat.com> - 0.2.6-1
 - allow interleaved elements in interface XML schema
 - allow <link> element in vlan and bond interfaces

* Wed Aug 20 2014 Laine Stump <laine@redhat.com> - 0.2.5-1
 - report link state/speed in interface status
 - change DHCPv6 to DHCPV6C in ifcfg files
 - max vlan id is 4095, not 4096

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Laine Stump <laine@redhat.com> - 0.2.4-1
 - wait for IFF_UP and IFF_RUNNING after calling ifup
 - don't require IFF_RUNNING for bridge devices
 - avoid memory leak in debian when listing interfaces
 - avoid use of uninitialized data when getting mac address
   (fixes https://bugzilla.redhat.com/show_bug.cgi?id=1046594 )
 - limit interface names to IFNAMSIZ-1 characters in length
 - support systemd for netcf-transaction

* Sat May 03 2014 Cole Robinson <crobinso@redhat.com> - 0.2.3-7
- Fix reading bridge stp value (bz #1031053)

* Thu Apr 24 2014 Tomáš Mráz <tmraz@redhat.com> - 0.2.3-6
- Rebuild for new libgcrypt

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Richard W.M. Jones <rjones@redhat.com> - 0.2.3-3
- Rebuild for libnl soname breakage (RHBZ#901569).

* Fri Jan 18 2013 Daniel P. Berrange <berrange@redhat.com> - 0.2.3-2
- Rebuild for libnl3 soname change

* Fri Dec 21 2012 Laine Stump <laine@redhat.com> - 0.2.3-1
- Rebase to netcf-0.2.3
- eliminate calls to nl_cache_mngt_provide(), to avoid
  non-threadsafe code in libnl (and because it isn't needed
  anyway) (This non-threadsafe code could lead to a segfault)
- portability fixes for FreeBSD
- fix bug when a config file has two config parameters with
  identical names
- add HACKING document
- always bail immediately if get_augeas fails (doing otherwise
  could lead to a segfault)

* Sat Aug 25 2012 Laine Stump <laine@redhat.com> - 0.2.2-1
- Rebase to netcf-0.2.2
- specfile: require libnl3-devel for rpm builds on Fedora 18+ and
  RHEL7+. Likewise, force libnl1 for F17- and RHEL6.x-, even if
  libnl3-devel is installed.

* Fri Aug 10 2012 Laine Stump <laine@redhat.com> - 0.2.1-1
- Rebase to netcf-0.2.1
- update gnulib to fix broken build on systems with nwer glibc (which no
  longer provides gets()).
- add ncftool manpage
- interfaces are only "active" if both UP and RUNNING.
- add "bundled(gnulib)" to specfile to indicate that we use a local
  copy of gnulib sources (used by Fedora/RHEL when determining the scope
  of security bugs).
- Fix ipcalc_netmask, which was trimming off the last digit in
  character representations of full-length netmasks (all 4 octets
  having 3 chars each)
- other minor bugfixes

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Laine Stump <laine@redhat.com> - 0.1.9-1
- Rebase to netcf-0.1.9
- always add <bridge> element to bridge, even if there is no physdev present
- don't log error if interface isn't found in kernel during status report
- allow building with C++
- update gnulib

* Tue Jun 21 2011 Laine Stump <laine@redhat.com> - 0.1.8-1
- Rebase to netcf-0.1.8
- new transactional change APIs: ncf_change_(begin|commit|rollback)
- add stdout/stderr to error text when an external program fails
- make error reporting of failed execs more exact/correct
- Remove unnecessary "Requires" of libxml2 and augeas from pkgconfig file
  to pulling in extra packages when building an application that uses netcf.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 27 2010 Laine Stump <laine@redhat.com> - 0.1.7-1
- New version

* Tue Apr 20 2010 Laine Stump <laine@redhat.com> - 0.1.6-1
- New version
- Remove patch n0001-src-dutil.c-add-missing-includes-for-stat.patch,
  included upstream

* Mon Feb 15 2010 David Lutterkort <lutter@redhat.com> - 0.1.5-2
- patch1: add missing includes for stat in dutil.c

* Mon Nov 30 2009 David Lutterkort <lutter@redhat.com> - 0.1.5-1
- New version

* Thu Nov  5 2009 David Lutterkort <lutter@redhat.com> - 0.1.4-1
- New version

* Tue Oct 27 2009 David Lutterkort <lutter@redhat.com> - 0.1.3-1
- New version

* Fri Sep 25 2009 David Lutterkort <lutter@redhat.com> - 0.1.2-1
- New Version

* Wed Sep 16 2009 David Lutterkort <lutter@redhat.com> - 0.1.1-1
- Remove patch netcf-0.1.0-fix-initialization-of-libxslt.patch,
  included upstream

* Tue Sep 15 2009 Mark McLoughlin <markmc@redhat.com> - 0.1.0-3
- Fix libvirtd segfault caused by libxslt init issue (#523382)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 David Lutterkort <lutter@redhat.com> - 0.1.0-1
- BR on augeas-0.5.2
- Drop explicit requires for augeas-libs

* Wed Apr 15 2009 David Lutterkort <lutter@redhat.com> - 0.0.2-1
- Updates acording to Fedora review

* Fri Feb 27 2009 David Lutterkort <lutter@redhat.com> - 0.0.1-1
- Initial specfile
