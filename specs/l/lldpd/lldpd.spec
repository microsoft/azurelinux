# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:     lldpd
Version:  1.0.18
Release: 5%{?dist}
Summary:  ISC-licensed implementation of LLDP
License:  ISC

URL:      https://github.com/lldpd/
Source0:  https://github.com/lldpd/lldpd/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:  %{name}-fedora.service
Source2:  %{name}-tmpfiles
Source3:  %{name}-fedora.sysconfig
Source4:  %{name}-systemd-sysusers.conf
Patch1:   lldpd-configure-c99.patch

BuildRequires: check-devel
BuildRequires: gcc
BuildRequires: libxml2-devel
BuildRequires: libevent-devel
BuildRequires: make
BuildRequires: net-snmp-devel
BuildRequires: readline-devel
BuildRequires: systemd-devel
%{?systemd_requires}

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
  --with-privsep-chroot=%{_rundir}/%{name}/chroot \
  --with-lldpd-ctl-socket=%{_rundir}/%{name}/%{name}.socket \
  --with-systemdsystemunitdir=%{_unitdir} --with-sysusersdir=no

%make_build


%install
%make_install

install -p -D -m644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -D -m644 %{SOURCE3} %{buildroot}/etc/sysconfig/%{name}
install -p -D -m644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf

install -d -D -m 0755 %{buildroot}%{_rundir}/%{name}/chroot
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}
# remove the docs from buildroot
rm -rf %{buildroot}/usr/share/doc/%{name}

# don't include completion conf yet
rm -f %{buildroot}/usr/share/bash-completion/completions/lldpcli
rm -f %{buildroot}/usr/share/zsh/vendor-completions/_lldpcli
rm -f %{buildroot}/usr/share/zsh/site-functions/_lldpcli

# remove static libtool archive
find %{buildroot} -type f -name "*.la" -delete

%ldconfig_scriptlets

%pre
%sysusers_create_compat %{SOURCE4}
exit 0

%post
%systemd_post lldpd.service

%preun
%systemd_preun lldpd.service

%postun
%systemd_postun_with_restart lldpd.service

%files
%license LICENSE
%doc NEWS README.md
%config %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/lldpcli
%{_sbindir}/lldpctl
%{_sbindir}/%{name}
%{_mandir}/man8/lldpcli.8*
%{_mandir}/man8/lldpctl.8*
%{_mandir}/man8/%{name}.8*
%{_libdir}/liblldpctl.so.4*
%dir %{_rundir}/%{name}
%dir %{_rundir}/%{name}/chroot
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%dir %attr(-,lldpd,lldpd) %{_sharedstatedir}/%{name}

%files devel
%{_includedir}/lldp-const.h
%{_includedir}/lldpctl.h
%{_libdir}/liblldpctl.so
%{_libdir}/pkgconfig/lldpctl.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.18-1
- Update to 1.0.18

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Florian Weimer <fweimer@redhat.com> - 1.0.16-4
- Reapply C99 compatibility fix

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May  2 2023 Peter Hjalmarsson <kanelxake@gmail.com> - 1.0.16-2
- Correcting usage of rundir macro
- Fix creation of sysuser

* Tue Apr 11 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.16-1
- Update to 1.0.16
- Modernise spec file
- CVEs: CVE-2020-27827, CVE-2020-27827, CVE-2021-43612

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec  8 2022 Florian Weimer <fweimer@redhat.com> - 1.0.4-11
- Port configure script to C99

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.4-7
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 29 20:35:23 CEST 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.4-5
- Rebuilt for libevent 2.1.12

* Wed Sep 02 2020 Josef Ridky <jridky@redhat.com> - 1.0.4-4
- Rebuilt for new net-snmp release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
