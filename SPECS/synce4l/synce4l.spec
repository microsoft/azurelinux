# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		synce4l
Version:	1.1.0
Release:	5%{?dist}
Summary:	SyncE implementation for Linux

License:	GPL-2.0-or-later
URL:		https://github.com/intel/synce4l
Source0:	https://github.com/intel/synce4l/archive/%{version}/synce4l-%{version}.tar.gz
Source1:	synce4l.service

# Fix compiler warnings to avoid build failures with -Werror
Patch1:		synce4l-ccwarns.patch

BuildRequires:	gcc make systemd
BuildRequires:	libnl3-devel

%{?systemd_requires}

%description
synce4l is a software implementation of Synchronous Ethernet (SyncE) according
to ITU-T Recommendation G.8264. The design goal is to provide logic to
supported hardware by processing Ethernet Synchronization Messaging Channel
(ESMC) and control Ethernet Equipment Clock (EEC) on Network Card Interface
(NIC).

%prep
%autosetup

sed \
	-e 's|^\(logging_level	*\)[0-7]|\16|' \
	-e 's|^\(use_syslog	*\)[01]|\11|' \
	-e 's|^\(verbose	*\)[01]|\10|' \
	-e 's|^\(smc_socket_path	*\)/tmp|\1/run|' \
	< configs/synce4l_dpll.cfg > synce4l.conf
touch -r configs/synce4l_dpll.cfg synce4l.conf

%build
%{make_build} \
	EXTRA_CFLAGS="$RPM_OPT_FLAGS" \
	EXTRA_LDFLAGS="$RPM_LD_FLAGS"

%install
# make_install doesn't work here
%makeinstall

mkdir -p $RPM_BUILD_ROOT{%{_sysconfdir},%{_unitdir},%{_mandir}/man5}
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 -p synce4l.conf $RPM_BUILD_ROOT%{_sysconfdir}

echo '.so man8/synce4l.8' > $RPM_BUILD_ROOT%{_mandir}/man5/synce4l.conf.5

%check
./synce4l -h 2>&1 | grep 'usage:.*synce4l'

%post
%systemd_post synce4l.service

%preun
%systemd_preun synce4l.service

%postun
%systemd_postun_with_restart synce4l.service

%files
%license COPYING
%doc README.md
%config(noreplace) %{_sysconfdir}/synce4l.conf
%{_unitdir}/synce4l.service
%{_sbindir}/synce4l
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 05 2024 Miroslav Lichvar <mlichvar@redhat.com> 1.1.0-2
- move smc_socket_path in default config to /run

* Tue May 28 2024 Miroslav Lichvar <mlichvar@redhat.com> 1.1.0-1
- update to 1.1.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 06 2023 Miroslav Lichvar <mlichvar@redhat.com> 1.0.0-1
- update to 1.0.0
- switch default config to use kernel DPLL API

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Miroslav Lichvar <mlichvar@redhat.com> 0.9.1-1
- update to 0.9.1

* Mon Jun 19 2023 Miroslav Lichvar <mlichvar@redhat.com> 0.9.0-1
- update to 0.9.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-4.20221114gitca51d5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Miroslav Lichvar <mlichvar@redhat.com> 0-3.20221114gitca51d5
- update to 20221114gitca51d5 (#2141038)

* Thu Nov 10 2022 Miroslav Lichvar <mlichvar@redhat.com> 0-2.20221108git079577
- fix compiler warning (#2141038)
- add simple test (#2141038)

* Tue Nov 08 2022 Miroslav Lichvar <mlichvar@redhat.com> 0-1.20221108git079577
- make initial release
