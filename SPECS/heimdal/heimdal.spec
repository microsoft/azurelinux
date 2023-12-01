%global _hardened_build 1
%global libdir %{_libdir}/heimdal
%global bindir %{_libdir}/heimdal
# Use systemd unit files on RHEL 7 and above.
%if ! (0%{?rhel} && 0%{?rhel} < 7)
  %global _with_systemd 1
%endif
# This macro was added in Fedora 20. Use the old version if it's undefined
# on older Fedoras and RHELs prior to RHEL 8.
# https://fedoraproject.org/wiki/Changes/UnversionedDocdirs
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
Summary:        A Kerberos 5 implementation without export restrictions
Name:           heimdal
Version:        7.7.1
Release:        3%{?dist}
License:        BSD AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.heimdal.software/
Source0:        https://github.com/%{name}/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Source3:        %{name}.sysconfig
Source4:        %{name}.sh
Source5:        %{name}.csh
Source9:        krb5.conf.sample
Source10:       %{name}.logrotate
Source11:       %{name}-bashrc
Source20:       %{name}-kdc.init
Source21:       %{name}-ipropd-master.init
Source22:       %{name}-ipropd-slave.init
Source23:       %{name}-kadmind.init
Source24:       %{name}-kpasswdd.init
Source25:       %{name}-kdc.conf
Source26:       %{name}-kdc.service
Source27:       %{name}-ipropd-master.service
Source28:       %{name}-ipropd-slave.service
Source29:       %{name}-kadmind.service
Source30:       %{name}-kpasswdd.service
Source31:       %{name}-ipropd-slave-wrapper
# klist, kswitch, and kvno are symlinks to "heimtools", and this utility needs
# to know how to interpret the "heimdal-" prefixes.
Patch1:         heimdal-1.6.0-c25f45a-rename-commands.patch
Patch2:         heimdal-configure.patch
Patch3:         CVE-2022-45142.patch
Patch4:         CVE-2022-42898.patch
Patch5:         0001-lib-krb5-krb5_pac_parse-mem-leak-if-pac_header_size-.patch
Patch6:         0002-kdc-Check-generate_pac-return-code.patch
Patch7:         0003-kdc-avoid-re-encoding-KDC-REQ-BODY.patch
BuildRequires:  bison
#libcom_err-devel is in
#BuildRequires:  libcom_err-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  e2fsprogs-libs
BuildRequires:  flex
BuildRequires:  gettext
BuildRequires:  groff
BuildRequires:  libcap-ng-devel
BuildRequires:  libedit-devel
BuildRequires:  libtool
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
#BuildRequires:  openldap-devel
#Required for tests/ldap
#BuildRequires:  openldap-servers
BuildRequires:  pam-devel
BuildRequires:  perl-JSON
#BuildRequires:  doxygen
#BuildRequires:  graphviz
BuildRequires:  python3-devel
BuildRequires:  sqlite-devel
BuildRequires:  systemd-devel
BuildRequires:  texinfo
#%if 0%{?_with_systemd}
#BuildRequires: systemd-units
#%endif
# Bundled libtommath (https://bugzilla.redhat.com/1118462)
Provides:       bundled(libtommath) = 0.42.0
%if (0%{?rhel} && 0%{?rhel} < 7)
BuildRequires:  db4-devel
%else
BuildRequires:  libdb-devel
%endif

%description
Kerberos 5 is a network authentication and single sign-on system.
Heimdal is a free Kerberos 5 implementation without export restrictions
written from the spec (rfc1510 and successors) including advanced features
like thread safety, IPv6, master-slave replication of Kerberos Key
Distribution Center server and support for ticket delegation (S4U2Self,
S4U2Proxy).
This package can coexist with MIT Kerberos 5 packages. Hesiod is disabled
by default since it is deemed too big a security risk by the packager.

%package    workstation
Summary:        Heimdal kerberos programs for use on workstations

%description workstation
This package contains Heimdal Kerberos 5 programs and utilities for
use on workstations (kinit, klist, kdestroy, kpasswd)

%package server
Summary:        Heimdal kerberos server
Requires:       logrotate
Provides:       heimdal-kdc = %{version}-%{release}
Obsoletes:      heimdal-kdc < 1.5
%if 0%{?_with_systemd}
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd
%else
Requires(post): chkconfig
Requires(postun): initscripts
Requires(preun): chkconfig
Requires(preun): initscripts
%endif

%description server
This package contains the master Heimdal kerberos Key Distribution
Center (KDC), admin interface server (admind) and master-slave
synchronisation daemons. Install this package if you intend to
set up Kerberos server.

%package libs
Summary:        Heimdal kerberos shared libraries
#Requires(post): info
#Requires(preun): info

%description libs
This package contains shared libraries required by several of the other
Heimdal packages.

%package devel
Summary:        Header and other development files for Heimdal kerberos
Provides:       %{name}-static = %{version}-%{release}

%description devel
Contains files needed to compile and link software using the Heimdal
kerberos headers/libraries.

%package path
Summary:        Heimdal kerberos PATH manipulation
Requires:       %{name}-libs
# For /etc/profile.d
#Requires: setup

%description path
This package prepends the Heimdal binary directory to the beginning of
PATH.

%prep
%autosetup -p1
%py3_shebang_fix .

./autogen.sh

%build
%ifarch i386
%global build_fix "-march=i686"
%else
%global build_fix ""
%endif
autoreconf -ivf
%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name} \
        --libdir=%{libdir} \
        --enable-static \
        --enable-shared \
        --enable-pthread-support \
        --without-x \
        --without-hesiod \
        --with-ipv6 \
        --enable-kcm \
        --enable-pk-init \
        --with-openldap=%{_prefix} \
        --with-sqlite3=%{_prefix} \
        --with-libedit=%{_prefix} \
        LIBS="-ltermcap" \
        CFLAGS="-fPIC %{optflags} %{build_fix}"
%make_build -j1 -C include krb5-types.h
%make_build -j1
%make_build -j1 -C doc html

# po/localefiles is not in the tarball, which causes install to fail
touch po/localefiles
%make_build -C po mo

%check
# Several intermittent test failures here, so make this non-fatal:
# (timeout to debug hard to reproduce stuck build)
timeout 20m %make_build check || :

%install
%make_install
# install the init files
%if 0%{?_with_systemd}
  # install systemd service files
  mkdir -p %{buildroot}%{_unitdir}
  pushd %{buildroot}%{_unitdir}
    install -p -D -m 644 %{SOURCE26} heimdal-kdc.service
    install -p -D -m 644 %{SOURCE27} heimdal-ipropd-master.service
    install -p -D -m 644 %{SOURCE28} heimdal-ipropd-slave.service
    install -p -D -m 644 %{SOURCE29} heimdal-kadmind.service
    install -p -D -m 644 %{SOURCE30} heimdal-kpasswdd.service
  popd
  install -p -D -m 755 %{SOURCE31} %{buildroot}%{_libexecdir}/ipropd-slave-wrapper
%else
  # install legacy SysV init scripts
  mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
  pushd %{buildroot}%{_sysconfdir}/rc.d/init.d
    install -p -D -m 755 %{SOURCE20} heimdal-kdc
    install -p -D -m 755 %{SOURCE21} heimdal-ipropd-master
    install -p -D -m 755 %{SOURCE22} heimdal-ipropd-slave
    install -p -D -m 755 %{SOURCE23} heimdal-kadmind
    install -p -D -m 755 %{SOURCE24} heimdal-kpasswdd
  popd
%endif
install -p -D -m 644 %{SOURCE3}  %{buildroot}%{_sysconfdir}/sysconfig/heimdal
install -p -D -m 644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/profile.d/heimdal.sh
install -p -D -m 644 %{SOURCE5}  %{buildroot}%{_sysconfdir}/profile.d/heimdal.csh
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/heimdal
mkdir -p %{buildroot}%{_localstatedir}/heimdal/
install -p -D -m 755 %{SOURCE25}  %{buildroot}%{_sysconfdir}/heimdal-kdc.conf
ln -s %{_sysconfdir}/heimdal-kdc.conf %{buildroot}%{_localstatedir}/heimdal/kdc.conf
echo "# see man heimdal-kadmind(8)" > %{buildroot}%{_sysconfdir}/heimdal-kadmind.acl
ln -s %{_sysconfdir}/heimdal-kadmind.acl %{buildroot}%{_localstatedir}/heimdal/kadmind.acl
touch    %{buildroot}%{_sysconfdir}/heimdal-slaves
ln -s %{_sysconfdir}/heimdal-slaves %{buildroot}%{_localstatedir}/heimdal/slaves
install -d -m 700 %{buildroot}%{_localstatedir}/log/heimdal
install -d -m 755 %{buildroot}/%{_pkgdocdir}
install -p -D -m 644 LICENSE    %{buildroot}/%{_pkgdocdir}/LICENSE
install -p -D -m 644 %{SOURCE9} %{buildroot}/%{_pkgdocdir}/krb5.conf.sample
install -p -D -m 644 %{SOURCE11} %{buildroot}/%{_pkgdocdir}/bashrc
# we don't need pkgconfig file and info/dir
rm -rf %{buildroot}%{libdir}/pkgconfig
rm -rf %{buildroot}%{_infodir}/dir
# NOTICE: no support for X11
rm -f %{buildroot}%{_mandir}/man1/kx.1*
rm -f %{buildroot}%{_mandir}/man1/rxtelnet.1*
rm -f %{buildroot}%{_mandir}/man1/rxterm.1*
rm -f %{buildroot}%{_mandir}/man1/tenletxr.1*
rm -f %{buildroot}%{_mandir}/man1/xnlock.1*
rm -f %{buildroot}%{_mandir}/man8/kxd.8*
# Remove CAT files, they are not needed
rm -rf %{buildroot}%{_mandir}/cat*
# Remove libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
cat >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf << EOF
%{_libdir}/%{name}
EOF

mkdir -p %{buildroot}%{bindir}/bin
mkdir -p %{buildroot}%{_mandir}/%{name}/man{1,5,8}

# rename clashes with other pkgs from <app> to heimdal-<app>
for prog in kadmin kadmind kdestroy kinit klist kpasswd krb5-config ktutil su pagsh compile_et
do
   if [ -e %{buildroot}%{_bindir}/${prog} ]; then
     mv %{buildroot}%{_bindir}/{,%{name}-}${prog}
     ln -s %{_bindir}/%{name}-${prog} %{buildroot}%{bindir}/bin/${prog}
   elif [ -e %{buildroot}%{_sbindir}/${prog} ]; then
     mv %{buildroot}%{_sbindir}/{,%{name}-}${prog}
     ln -s %{_sbindir}/%{name}-${prog} %{buildroot}%{bindir}/bin/${prog}
   elif [ -e %{buildroot}%{_libexecdir}/${prog} ]; then
     mv %{buildroot}%{_libexecdir}/{,%{name}-}${prog}
   fi

   if [ -e %{buildroot}%{_mandir}/man1/${prog}.1 ]; then
     mv %{buildroot}%{_mandir}/man1/{,%{name}-}${prog}.1
   elif [ -e %{buildroot}%{_mandir}/man8/${prog}.8 ]; then
     mv %{buildroot}%{_mandir}/man8/{,%{name}-}${prog}.8
   fi
done

# If we have the prefixed name in one pkg we want it in all.
mv %{buildroot}%{_bindir}/{,%{name}-}kswitch
ln -s %{_bindir}/%{name}-kswitch %{buildroot}%{bindir}/bin/kswitch
mv %{buildroot}%{_mandir}/man1/{,%{name}-}kswitch.1

ln -s %{name}-kinit %{buildroot}%{_bindir}/kauth

mv %{buildroot}%{_mandir}/man5/{,%{name}-}krb5.conf.5

rm %{buildroot}%{_mandir}/man5/qop.5
ln -s mech.5.gz %{buildroot}%{_mandir}/man5/qop.5.gz

%find_lang %{name} --all-name

%post server
%if 0%{?_with_systemd}
  %systemd_post heimdal-kdc.service
  %systemd_post heimdal-ipropd-master.service
  %systemd_post heimdal-ipropd-slave.service
  %systemd_post heimdal-kadmind.service
  %systemd_post heimdal-kpasswdd.service
%else
  /sbin/chkconfig --add heimdal-kdc
  /sbin/chkconfig --add heimdal-ipropd-master
  /sbin/chkconfig --add heimdal-ipropd-slave
  /sbin/chkconfig --add heimdal-kadmind
  /sbin/chkconfig --add heimdal-kpasswdd
%endif

%preun server
%if 0%{?_with_systemd}
  %systemd_preun heimdal-kdc.service
  %systemd_preun heimdal-ipropd-master.service
  %systemd_preun heimdal-ipropd-slave.service
  %systemd_preun heimdal-kadmind.service
  %systemd_preun heimdal-kpasswdd.service
%else
  if [ $1 -eq 0 ] ; then
     /sbin/service heimdal-kdc stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-kdc
     /sbin/service heimdal-ipropd-master stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-ipropd-master
     /sbin/service heimdal-ipropd-slave stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-ipropd-slave
     /sbin/service heimdal-kadmind stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-kadmind
     /sbin/service heimdal-kpasswdd stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del >/dev/null
  fi
%endif

%postun server
%if 0%{?_with_systemd}
  %systemd_postun heimdal-kdc.service
  %systemd_postun heimdal-ipropd-master.service
  %systemd_postun heimdal-ipropd-slave.service
  %systemd_postun heimdal-kadmind.service
  %systemd_postun heimdal-kpasswdd.service
%else
  if [ $1 -eq 1 ] ; then
     /sbin/service heimdal-kdc condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-ipropd-master condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-ipropd-slave condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-kadmind condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-kpasswdd condrestart >/dev/null 2>&1 || :
  fi
%endif

%if (0%{?rhel} && 0%{?rhel} < 8)
%post libs
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun libs
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun libs -p /sbin/ldconfig
%endif

%files libs -f %{name}.lang
%license LICENSE
%doc %{_pkgdocdir}
%dir %{bindir}
%dir %{bindir}/bin
%dir %{libdir}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{libdir}/lib*.so*
%{libdir}/windc.so*
%{_infodir}/heimdal.info*
%{_infodir}/hx509.info*
%{_mandir}/man5/%{name}-krb5.conf.5*
%{_mandir}/man5/qop.5*
%{_mandir}/man5/mech.5*
%{_mandir}/man8/kerberos.8*
%{_bindir}/string2key
%{_mandir}/man8/string2key.8*
%{_libexecdir}/kdigest
%{_mandir}/man8/kdigest.8*
%{_bindir}/verify_krb5_conf
%{_mandir}/man8/verify_krb5_conf.8*
%{_libexecdir}/digest-service

%files server
%if 0%{?_with_systemd}
%{_unitdir}/*.service
%else
%{_initrddir}/*
%endif
%{_sysconfdir}/logrotate.d/heimdal
%config(noreplace) %{_sysconfdir}/sysconfig/heimdal
%dir %attr(700,root,root) %{_localstatedir}/heimdal
%dir %attr(700,root,root) %{_localstatedir}/log/heimdal
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/heimdal-kdc.conf
%config(noreplace) %{_localstatedir}/heimdal/kdc.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/heimdal-kadmind.acl
%config(noreplace) %{_localstatedir}/heimdal/kadmind.acl
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/heimdal-slaves
%config(noreplace) %{_localstatedir}/heimdal/slaves
%{_libexecdir}/hprop
%{_mandir}/man8/hprop.8*
%{_libexecdir}/hpropd
%{_mandir}/man8/hpropd.8*
%{_mandir}/man8/iprop.8*
%{_sbindir}/iprop-log
%{_mandir}/man8/iprop-log.8*
%{_libexecdir}/ipropd-master
%{_mandir}/man8/ipropd-master.8*
%{_libexecdir}/ipropd-slave
%{_mandir}/man8/ipropd-slave.8*
%if 0%{?_with_systemd}
%{_libexecdir}/ipropd-slave-wrapper
%endif
%{_libexecdir}/%{name}-kadmind
%{_mandir}/man8/%{name}-kadmind.8*
%{_libexecdir}/kdc
%{_mandir}/man8/kdc.8*
%{_libexecdir}/kpasswdd
%{_mandir}/man8/kpasswdd.8*
%{_sbindir}/kstash
%{_mandir}/man8/kstash.8*

%files workstation
%{_bindir}/afslog
%{_mandir}/man1/afslog.1*
%{_bindir}/bsearch
%{_mandir}/man1/bsearch.1*
%{_bindir}/%{name}-pagsh
%{bindir}/bin/pagsh
%{_mandir}/man1/%{name}-pagsh.1*
%{_bindir}/gsstool
%{_bindir}/heimtools
%{_bindir}/hxtool
%{_bindir}/idn-lookup
%{_bindir}/%{name}-kdestroy
%{bindir}/bin/kdestroy
%{_mandir}/man1/%{name}-kdestroy.1*
%{_bindir}/kf
%{_mandir}/man1/kf.1*
%{_bindir}/kgetcred
%{_mandir}/man1/kgetcred.1*
%{_libexecdir}/kimpersonate
%{_mandir}/man8/kimpersonate.8*
%{_bindir}/%{name}-kinit
%{bindir}/bin/kinit
%{_bindir}/kauth
%{_mandir}/man1/%{name}-kinit.1*
%{_bindir}/%{name}-klist
%{bindir}/bin/klist
%{_mandir}/man1/%{name}-klist.1*
%{_bindir}/%{name}-kpasswd
%{bindir}/bin/kpasswd
%{_mandir}/man1/%{name}-kpasswd.1*
%{_bindir}/heimdal-kswitch
%{bindir}/bin/kswitch
%{_mandir}/man1/heimdal-kswitch.1*
%{_bindir}/otp
%{_mandir}/man1/otp.1*
%{_bindir}/otpprint
%{_mandir}/man1/otpprint.1*
%{_bindir}/%{name}-kadmin
%{bindir}/bin/kadmin
%{_mandir}/man1/%{name}-kadmin.1*
%{_libexecdir}/kcm
%{_mandir}/man8/kcm.8*
%{_libexecdir}/kfd
%{_mandir}/man8/kfd.8*
%{_bindir}/%{name}-ktutil
%{bindir}/bin/ktutil
%{_mandir}/man1/%{name}-ktutil.1*
%attr(04550,root,root) %{_bindir}/%{name}-su
%{bindir}/bin/su
%{_mandir}/man1/%{name}-su.1*

%files devel
%dir %{_libexecdir}/%{name}
%{_bindir}/%{name}-krb5-config
%{bindir}/bin/krb5-config
%{_mandir}/man1/%{name}-krb5-config.1*
%{_includedir}/*
%{libdir}/lib*.a
%{libdir}/windc.a
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_libexecdir}/%{name}/asn1_compile
%{_libexecdir}/%{name}/asn1_print
%{_libexecdir}/%{name}/slc

%files path
%{_sysconfdir}/profile.d/%{name}.sh
%{_sysconfdir}/profile.d/%{name}.csh

%changelog
* Thu Aug 24 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 7.7.1-3
- Address CVE-2022-42898
- Introduce 3 more patches that fix bugs: https://github.com/heimdal/heimdal/issues/1011

* Tue Mar 14 2023 Thien Trung Vuong <tvuong@microsoft.com> - 7.7.1-2
- Add patch for CVE-2022-45142

* Tue Dec 06 2022 Henry Beberman <henry.beberman@microsoft.com> - 7.7.1-1
- Upgrade to version 7.7.1
- Remove patches that were backported from upstream
- Fixes CVE-2022-42898, CVE-2022-3437, CVE-2022-41916, CVE-2021-44758,
- CVE-2021-3671, CVE-2022-44640, CVE-2019-14870

* Tue Mar 08 2022 Andrew Phelps <anphel@microsoft.com> - 7.7.0-8
- Add patch to compile with newer autoconf

* Thu Feb 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 7.7.0-7
- Remove python2 patch and build requirement
- Add patch to fix python detection during configuration
- Fix python script shebang lines

* Mon Apr 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 7.7.0-6
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Wed Oct 21 2020 Henry Beberman <henry.beberman@microsoft.com> - 7.7.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 7.7.0-3
- Fix configure tests compromised by LTO

* Sat Dec 21 2019 Alexander Boström <abo@root.snowtree.se> - 7.7.0-2
- Set timeout on make check

* Fri Dec 20 2019 Alexander Boström <abo@root.snowtree.se> - 7.7.0-1
- Update to 7.7.0
- Remove upstreamed patch
- New project URL
- Update buildreqs
- Add locale build fix

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 7.5.0-7
- Rebuilt for libcrypt.so.2 (#1666033)

* Sun Jan 06 2019 Björn Esser <besser82@fedoraproject.org> - 7.5.0-6
- Add patch to explicitly use python2 binary, fixes FTBFS (#1604316)
- Do not run 'make dist', fixes FTBFS (#1604316)
- Make sure 'krb5-types.h' is build, fixes FTBFS (#1604316)
- Remove el5 bits
- Drop unneeded scriptlets for newer distros
- Use %%make_build and %%make_install macros
- Install license file using %%license in libs package

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 7.5.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 7.5.0-2
- Rebuilt for switch to libxcrypt

* Thu Dec 14 2017 Ken Dreyer <ktdreyer@ktdreyer.com> - 7.5.0-1
- Update to 7.5.0 GA release (CVE-2017-17439)

* Mon Oct 23 2017 Alexander Boström <abo@root.snowtree.se> - 7.4.0-5
- Backport fix to prevent wait() loop on non-existant child process

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Ken Dreyer <ktdreyer@ktdreyer.com> - 7.4.0-2
- Make test failures non-fatal

* Tue Jul 11 2017 Ken Dreyer <ktdreyer@ktdreyer.com> - 7.4.0-1
- Update to 7.4.0 GA release (CVE-2017-11103)

* Mon Apr 17 2017 Ken Dreyer <ktdreyer@ktdreyer.com> - 7.3.0-1
- Update to 7.3.0 GA release (CVE-2017-6594)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Ken Dreyer <ktdreyer@ktdreyer.com> - 7.1.0-1
- Update to 7.1.0 GA release
- Drop all remaining xinetd bits

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-0.13.20150115gitc25f45a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 10 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.12.20150115gitc25f45a
- Fix ld.so.conf.d file conflict between 32-bit and 64-bit packages
  (rhbz#1244316)
- Mark ld.so.conf.d as %%config(noreplace)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-0.11.20150115gitc25f45a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.10.20150115gitc25f45a
- Update git snapshot to latest tip of heimdal-1-6-branch
- Remove upstreamed patches
- Add virtual provides for bundled(libtommath) (RHBZ #1118462)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-0.10.20140621gita5adc06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.9.20140621gita5adc06
- Remove OpenSSL BR and go back to using hcrypto with bundled libtommath.
  OpenSSL is not thread safe without callbacks (RHBZ #1118462)

* Tue Jul 01 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.8.20140621gita5adc06
- Patch for parallel build failure in kadm5. Thanks Jakub Čajka.
- Remove comments about X11 binaries (we will never ship those).

* Sun Jun 22 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.7.20140621gita5adc06
- Update git snapshot to latest tip of heimdal-1-6-branch

* Sat Jun 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.6.20140606git966108b
- Update git snapshot to latest tip of heimdal-1-6-branch
- Don't ship xinetd support if the distro has systemd (RHBZ #613001)

* Fri May 30 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.5.20140529gitddde77b
- Update git snapshot to latest tip of heimdal-1-6-branch
- Use /sbin path in %%pre/%%post scripts for EL6 and EL5
- Install login.users(5) normally, since it doesn't conflict with anything
  (RHBZ #613001)
- Don't ship ftpusers(5) (RHBZ #613001)
- Patch heimtools to deal with the commands' "heimdal-" prefixes (RHBZ #613001)
- Use "simple" systemd service type for kdc, kadmind, kpasswdd
- Add "--detach" flag in heimdal-ipropd-slave-wrapper to match the systemd
  forking service type
- Patch kadmind to handle systemd's restrictions on setpgid() (RHBZ #613001)

* Thu May 22 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.4.20140522git229d8c7
- Update git snapshot to latest tip of heimdal-1-6-branch
- Drop upstreamed text-fx patch
- Install Texinfo files (RHBZ #613001)
- Add Provides: heimdal-static to -devel subpackage (RHBZ #613001)
- Drop %%defattr (RHBZ #613001)
- Add text content to kadmind.acl to help users (and remove a zero-length file)
- Install profile.d scripts with non-executable permissions
- Remove .la files
- Patch to remove AC_PROG_LIBTOOL macro
- Reload xinetd when using systemd
- Require logrotate and setup, since we drop config files into directories that
  these packages own.
- Add unowned Heimdal directories in %%files
- Replace "heimdal" with %%{name} in %%files
- Do not BR libcap-ng-devel on EL5

* Tue Apr 29 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.3.20140429gitd60ba47
- Add BR libdb-devel on Fedora (RHBZ #613001)
- Add BR openssl-devel and libcap-ng-devel (RHBZ #613001)
- Only set BuildRoot on el5
- Alphabetize non-conditional BuildRequires
- Remove duplicate BR openldap-devel

* Tue Apr 29 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.2.20140326git7e6b55
- Update git snapshot to latest tip of heimdal-1-6-branch
- Rename Source11 with "heimdal-" prefix
- Use newer macro for UnversionedDocdirs change

* Mon Jan 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-0.1.20140106git46a508
- Package git snapshot from master branch

* Wed Oct 16 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-24.20130903gitb074e0b
- Disable autogen and parallel make on EL5
- Add pregenerated autoconf tarball as Source1
- Add script to pregenerate autoconf files as Source2

* Tue Sep 10 2013 Alexander Boström <abo@kth.se> - 1.5.3-23.20130903gitb074e0b
- Fix build. (Problem with symlinks to kcc.)

* Thu Sep 05 2013 Alexander Boström <abo@kth.se> - 1.5.3-22.20130903gitb074e0b
- Rename rename kcc to heimdal-kcc (conflicts in el5 and fedora)
- Rename kswitch to heimdal-kswitch in el6 too

* Tue Sep 03 2013 Alexander Boström <abo@kth.se> - 1.5.3-21.20130903gitb074e0b
- Update to latest git snapshot of heimdal-1-5-branch
- remove upstreamed patch

* Tue Sep 03 2013 Alexander Boström <abo@kth.se> - 1.5.3-20.20130813gitdcc7c13
- Split ipv6_loopbacks_fix.patch into one backport and one smaller change

* Tue Aug 20 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-19.20130813gitdcc7c13
- Build against libedit instead of readline (avoid GPL entanglements)

* Tue Aug 13 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-18.20130813gitdcc7c13
- Update to latest git snapshot of heimdal-1-5-branch
- remove upstreamed texinfo patches

* Tue Aug 13 2013 Alexander Boström <abo@kth.se> - 1.5.3-17.20130730gitd9b3691
- remove workaround for bogus check-iprop check failure

* Mon Aug 12 2013 Alexander Boström <abo@kth.se> - 1.5.3-16.20130730gitd9b3691
- buildreq groff on el6 and older
- remove most comments from sysconfig file
- systemd: only use /etc/sysconfig/heimdal to specify the iprop master
  host, via a wrapper script
- systemd: use Type=forking
- make systemd the default, check for known sysv systems

* Mon Aug 12 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-15.20130812git29f0a90
- Update to latest git snapshot of heimdal-1-5-branch

* Mon Aug 12 2013 Alexander Boström <abo@kth.se> - 1.5.3-14.20130730gitd9b3691
- do not ghost files in owned directory

* Mon Aug 12 2013 Alexander Boström <abo@kth.se> - 1.5.3-13.20130730gitd9b3691
- use global instead of define

* Mon Aug 12 2013 Alexander Boström <abo@kth.se> - 1.5.3-12.20130730gitd9b3691
- add doc references to unit files

* Mon Aug 12 2013 Alexander Boström <abo@kth.se> - 1.5.3-11.20130730gitd9b3691
- add missing req on xinetd
- remove slash after buildroot macro usage
- preserve timestamps of installed files
- move slaves config file to /etc
- no attributes on symlinks
- only ghost own the slave-stats file

* Fri Aug 09 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-10.20130730gitd9b3691
- add systemd files and _with_systemd conditional
- remove "--detach" from sysconfig comments
- tweak kadmind service description
- add comments about texinfo patches

* Fri Aug 09 2013 Alexander Boström <abo@kth.se> - 1.5.3-9.20130730gitd9b3691
- SysV scriptlets and initscript cleanups
- xinetd services ipv6 enabled

* Thu Aug 08 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-8.20130730gitd9b3691
- Add Debian's texinfo patch to hx509, plus my own hacks for 5.1

* Thu Aug 08 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-7.20130730gitd9b3691
- Add missing groff buildreq on F19 and above
- Tweak Summary

* Thu Aug 08 2013 Alexander Boström <abo@kth.se> - 1.5.3-6
- Add missing buildreqs

* Thu Aug 08 2013 Alexander Boström <abo@kth.se> - 1.5.3-5
- Update to post 1.5.3 snapshot, deprecating a couple of patches
- Add autogen.sh and extra BRs, build fixes.

* Thu Aug 08 2013 Alexander Boström <abo@kth.se> - 1.5.3-4
- No autoreconf
- More robust ?rhel macro usage
- BR libcom_err-devel instead of e2fsprogs-devel (but not on el5)
- el5 build fixes

* Tue Aug 06 2013 Alexander Boström <abo@kth.se> - 1.5.3-3
- Add heimdal-des-key-selection.patch

* Tue Aug 06 2013 Alexander Boström <abo@kth.se> - 1.5.3-2
- Use upstream tarball.
- Remove unused patches.
- Fix heimdal-kdc.conf
- Handle the case of no .mo files

* Tue Aug 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-1
- Update to 1.5.3 (tag from Git)
- Use the find_lang macro to include the translation files
- Add Getopt patch in order to build with Fedora's newer Perl
- Adjust Group to satisfy rpmlint
- Remove macros from comments to satisfy rpmlint

* Mon Jul 29 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.19
- really fix prefix munge patch
- fix texi build

* Wed Jul  3 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.18
- fix prefix munge patch

* Tue Jul  2 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.17
- rename kswitch to heimdal-kswitch (except on el6)

* Tue Jul  2 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.16
- ignore missing otp binaries

* Fri Jun 28 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.15
- fix license, fix macro-in-changelog

* Fri Jun 28 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.14
- enable dns_lookup_realm and dns_lookup_kdc in the sample config file
- changed logrotate conf, postrotate should not be required
- add kdc.conf
- move kadmind.acl to sysconfdir

* Thu Jun 27 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.13
- fix qop man symlink

* Thu Jun 27 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.12
- workstation does not require xinetd
- fix paths in xinetd confs

* Wed Jun 26 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.11
- fix symlinks

* Wed Jun 26 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.10
- provide/obsolete heimdal-kdc

* Wed Apr 10 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.9
- make PATH manipulation an optional subpackage

* Wed Apr 10 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.8
- rename to heimdal-* instead of *.heimdal

* Tue Apr  9 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.7
- split init script into multiple services

* Tue Apr  9 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.6
- move su to the workstation subpkg

* Tue Apr  9 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.5
- Add symlinks in the bin dir.

* Tue Apr  9 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.4
- Reuse /etc/security/access.conf from PAM.

* Tue Apr  9 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.3
- move daemon binaries to regular libexec dir, with executable name suffix

* Mon Apr  8 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.2
- move binaries from /usr/lib64/heimdal/bin to /usr/lib/heimdal/bin

* Mon Apr  8 2013 Alexander Boström <abo@kth.se> - 1.5.2-3.kth.1
- disable tests

* Wed Jul 4 2012 Rok Papež, ARNES <rok.papez@arnes.si> - 1.5.2-3
  - updated to upstream 1.5.2
  - added support for Fedora 17
  - fixed wrong PATH on x86_64
  - fixed IPv6 and multiple interfaces bug in krb5_parse_address:
    https://bugzilla.redhat.com/show_bug.cgi?id=808147
  - added support for .heimdal prefix to kcc

* Tue Oct 4 2011 Rok Papež, ARNES <rok.papez@arnes.si> - 1.5.1-1
  - updated to upstream 1.5.1

* Tue Sep 27 2011 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.5.1.pre20110912git-2
  - FESCo updates: https://fedorahosted.org/fesco/ticket/577
  - Implicit requires removed, rpmbuild can figure them out itself
  - Implicit provides removed, we are NOT compatible with krb5
  - Enable hardened build:
        https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
        https://fedoraproject.org/wiki/User:Kevin/DRAFT_When_to_use_PIE_compiler_flags
  - Merged updates from Orion Poplawski

* Mon Sep 12 2011 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.5.1.pre20110912git-1.arnes
  - Updated to Heimdal 1.5.1.pre20110912git

* Tue Nov 30 2010 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.4.1rc1-1.arnes
  - Updated to Heimdal 1.4.1rc1

* Fri Jul 09 2010 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.3.3-1.arnes
  - Updated to Heimdal 1.3.3

* Wed Apr 21 2010 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.3.2-2.arnes
  - Updated to Heimdal 1.3.2

* Thu Sep 17 2009 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.3.0pre9-1
  - Updated to Heimdal 1.3.0pre9
  - Building on CentOS 5.3 i386 and Fedora 11 x86_64.

* Wed Jun 10 2009 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.2.1-9
  - Fixed build for CentOS 4.7 (thanks to Nitzan Zaifman for bugreport)

* Mon Jun 8 2009 Rok Papež, ARNES <aaa-podpora@arnes.si> - 1.2.1-8
  - Fixed paths for building on CentOS 5.3
  - Rebuilt for CentOS 5.3
  - removed obsolete X11 dependency

* Thu Feb 19 2009 Mitja Mihelic, ARNES <aaa-podpora@arnes.si> - 1.2.1-7
  - added dependency on xinetd for heimdal-workstation

* Tue Jan 20 2009 Rok Papež, ARNES <aaa-podpora@arnes.si>
  - Fixed permissions

* Wed Oct 8 2008 Rok Papež, ARNES <aaa-podpora@arnes.si>
  - New specs for Heimdel 1.2.1, suggestions taken from both PDC and Mandrake specs file.
  - Need to be compatible with MIT Kerberos 5 installation.
  - Let MIT have priority
