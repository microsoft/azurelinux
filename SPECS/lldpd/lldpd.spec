Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without systemd
%global rundir /run/

Name:     lldpd
Version:  1.0.14
Release:  3%{?dist}
Summary:  ISC-licensed implementation of LLDP

License:  ISC
URL:      https://lldpd.github.io/
Source0:  https://github.com/lldpd/lldpd/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:  %{name}-fedora.service
Source2:  %{name}-tmpfiles
Source3:  %{name}-fedora.sysconfig
Source4:  %{name}-el6.init
Source5:  %{name}-el7.service
Patch0:   CVE-2023-41910.patch

BuildRequires: gcc
BuildRequires: readline-devel
BuildRequires: check-devel
BuildRequires: net-snmp-devel
BuildRequires: libxml2-devel
BuildRequires: libevent-devel

%if 0%{?with_systemd}
# For systemd stuff
BuildRequires: systemd
%{?systemd_requires}
%else
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%endif

Requires(pre): shadow-utils

%description
LLDP is an industry standard protocol designed to supplant proprietary
Link-Layer protocols such as EDP or CDP. The goal of LLDP is to provide
an inter-vendor compatible mechanism to deliver Link-Layer notifications
to adjacent network devices.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: %{summary}

%description devel
%{name} development libraries and headers

%prep
%autosetup -p1


%build
%configure --disable-static --with-snmp --disable-silent-rules \
  --with-privsep-user=%{name} --with-privsep-group=%{name} \
  --with-privsep-chroot=%{rundir}%{name}/chroot \
  --with-lldpd-ctl-socket=%{rundir}%{name}/%{name}.socket \
%if 0%{?with_systemd}
  --with-systemdsystemunitdir=%{_unitdir} --with-sysusersdir=no
%endif

make %{?_smp_mflags}


%install
%make_install

%if 0%{?with_systemd}

install -p -D -m644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service



install -p -D -m644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
%else
install -p -D -m755 %{SOURCE4} %{buildroot}%{_initddir}/%{name}
%endif
install -p -D -m644 %{SOURCE3} %{buildroot}/etc/sysconfig/%{name}

install -d -D -m 0755 %{buildroot}%{rundir}%{name}/chroot
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}
# remove the docs from buildroot
rm -rf %{buildroot}/usr/share/doc/%{name}


# don't include completion conf yet
rm -f %{buildroot}/usr/share/bash-completion/completions/lldpcli
rm -f %{buildroot}/usr/share/zsh/vendor-completions/_lldpcli
rm -f %{buildroot}/usr/share/zsh/site-functions/_lldpcli

# remove static libtool archive
rm -f %{buildroot}%{_libdir}/liblldpctl.la

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /usr/sbin/nologin \
    -c "Used by the %{name} daemon" %{name}
exit 0

%post
/sbin/ldconfig
%if 0%{?with_systemd}
%systemd_post %{name}.service
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
/sbin/ldconfig
%if 0%{?with_systemd}
%systemd_postun_with_restart %{name}.service
%else
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%doc NEWS README.md
%license LICENSE
%{_sbindir}/lldpcli
%{_sbindir}/lldpctl
%{_sbindir}/%{name}
%config %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man8/lldpcli.8*
%{_mandir}/man8/lldpctl.8*
%{_mandir}/man8/%{name}.8*
%{_libdir}/liblldpctl.so.4
%{_libdir}/liblldpctl.so.4.*
%dir %{rundir}%{name}
%dir %{rundir}%{name}/chroot
%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%else
%{_initddir}/%{name}
%endif
%dir %attr(-,lldpd,lldpd) %{_sharedstatedir}/%{name}

%files devel
%{_includedir}/lldp-const.h
%{_includedir}/lldpctl.h
%{_libdir}/liblldpctl.so
%{_libdir}/pkgconfig/lldpctl.pc


%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.0.14-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Sep 12 2023 Suresh Thelkar <sthelkar@microsoft.com> - 1.0.14-2
- Backport patch to address CVE-2023-41910

* Tue Aug 16 2022 Muhammad Falak <mwani@microsoft.com> - 1.0.14-1
- Bump version to address CVE-2020-27827

* Thu Jul 28 2022 Henry Li <lihl@microsoft.com> - 1.0.4-4
- License Verified
- Remove usage of macros that do not apply for CBL-Mariner

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 James Hogarth <james.hogarth@gmail.com> - 1.0.4-1
- Updated to new upstream release 1.0.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-5
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 1.0.1-3
- Rebuild for new net-snmp

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018 James Hogarth <james.hogarth@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 21 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.8-1
- Update to 0.9.8

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.7-10
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.7-9
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.7-8
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 06 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-5
- Older fedora needs the older syntax matching EPEL7

* Wed Apr 05 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-4
- EPEL7 systemd needs an older syntax

* Wed Apr 05 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-3
- Use the official release tarball rather than the github snapshot
- Add EPEL6 conditionals

* Wed Apr 05 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-2
- Tweaks to spec requested in review

* Tue Apr 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-1
- Initial package
