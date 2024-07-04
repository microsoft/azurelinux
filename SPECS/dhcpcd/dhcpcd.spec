%global debug_package   %{nil}

Summary:        A minimalistic network configuration daemon with DHCPv4, rdisc and DHCPv6 support
Name:           dhcpcd
Version:        10.0.8
Release:        1%{?dist}
License:        BSD-2-Clause AND ISC AND MIT
Url:            http://roy.marples.name/projects/%{name}/
Source0:        https://github.com/NetworkConfiguration/%{name}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}@.service
Source3:        systemd-sysusers.conf
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildRequires:  chrony
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  systemd
BuildRequires:  ypbind

%description
The dhcpcd package provides a minimalistic network configuration daemon
that supports IPv4 and IPv6 configuration including configuration discovery
through NDP, DHCPv4 and DHCPv6 protocols.

%prep
%autosetup -p1 -n %{name}-%{version}

%build 
%configure \
    --dbdir=/var/lib/%{name} --runstatedir=%{_rundir}
%make_build

%check
%make_build test

%install
export BINMODE=755
%make_install
find %{buildroot} -name '*.la' -delete -print
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}@.service
install -d %{buildroot}%{_sharedstatedir}/%{_name}

%pre
%sysusers_create_compat %{SOURCE3}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE	
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/hooks
%{_datadir}/%{name}/hooks/10-wpa_supplicant
%{_datadir}/%{name}/hooks/15-timezone
%{_datadir}/%{name}/hooks/29-lookup-hostname
%{_datadir}/%{name}/hooks/50-yp.conf
%{_libexecdir}/%{name}-hooks
%{_libexecdir}/%{name}-run-hooks
%{_mandir}/man5/%{name}.conf.5.gz
%{_mandir}/man8/%{name}-run-hooks.8.gz
%{_mandir}/man8/%{name}.8.gz
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%defattr(0644,root,dhcpcd,0755)
%{_sharedstatedir}/%{name}

%changelog
* Tue Jun 25 2024 Minghe Ren <mingheren@microsoft.com> 10.0.8-1
- Initial build
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified