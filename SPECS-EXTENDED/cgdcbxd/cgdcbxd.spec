Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1

Name:		cgdcbxd
Version:	1.0.2
Release:	12%{?dist}
Summary:	DCB network priority management daemon	
License:	GPLv2
URL:		https://github.com/jrfastab/cgdcbxd
Source:		https://github.com/jrfastab/cgdcbxd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# The service file was created locally for the fedora project, but will be sent
# upstream shortly
Source1:	%{name}.service
BuildRequires:	libcgroup-devel libmnl-devel libtool systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This is a daemon to manage the priority of network traffic in dcb enabled
environments.  By using the information exchanged over the dcbx protocol on a
LAN, this package will enforce network priority on running applications on your
host using the net_prio cgroup

%prep
%setup -q

%build
./bootstrap.sh
export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS=$RPM_LD_FLAGS
%{configure}
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}
install -D -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/cgdcbxd.service

%files
%doc COPYING
%{_unitdir}/cgdcbxd.service
%{_mandir}/man8/*
%{_sbindir}/*

%post
%systemd_post cgdcbxd.service

%preun
%systemd_preun cgdcbxd.service

%postun
%systemd_postun_with_restart cgdcbxd.service

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 14 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-1
- Update to 1.0.2
- Spec cleanups

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Neil Horman <nhorman@redhat.com> - 1.0.1-5
- Update spec file to use _hardend_build macro

* Fri May 02 2014 Neil Horman <nhorman@redhat.com> - 1.0.1-4
- Fixed build to enable RELRO and PIE

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jun 25 2012 Neil Horman <nhorman@tuxdriver.com> 1.0.1-1 
- Initial build
