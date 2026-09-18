# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:             ipset
Version:          7.24
Release:          2%{?dist}
Summary:          Manage Linux IP sets

License:          GPL-2.0-only
URL:              http://ipset.netfilter.org/
Source0:          %{url}/%{name}-%{version}.tar.bz2
Source1:          %{name}.service
Source2:          %{name}.start-stop
Source3:          %{name}-config

BuildRequires:    libmnl-devel
BuildRequires:    automake
BuildRequires:    autoconf
BuildRequires:    make
BuildRequires:    libtool
BuildRequires:    libtool-ltdl-devel

# An explicit requirement is needed here, to avoid cases where a user would
# explicitly update only one of the two (e.g 'yum update ipset')
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description
IP sets are a framework inside the Linux kernel since version 2.4.x, which can
be administered by the ipset utility. Depending on the type, currently an IP
set may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
addresses in a way, which ensures lightning speed when matching an entry
against a set.

If you want to:
 - store multiple IP addresses or port numbers and match against the collection
   by iptables at one swoop;
 - dynamically update iptables rules against IP addresses or ports without
   performance penalty;
 - express complex IP address and ports based rulesets with one single iptables
   rule and benefit from the speed of IP sets
then ipset may be the proper tool for you.


%package libs
Summary:       Shared library providing the IP sets functionality

%description libs
This package contains the libraries which provide the IP sets funcionality.


%package devel
Summary:       Development files for %{name}
Requires:      %{name}-libs%{?_isa} == %{version}-%{release}
Requires:      kernel-headers

%description devel
This package contains the files required to develop software using the %{name}
libraries.


%package service
Summary:          %{name} service for %{name}s
Requires:         %{name} = %{version}-%{release}
BuildRequires:    systemd
Requires:         iptables-services
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildArch:        noarch

%description service
This package provides the service %{name} that is split
out of the base package since it is not active by default.


%prep
%autosetup -p1


%build
./autogen.sh
%configure --enable-static=no --with-kmod=no

# Just to make absolutely sure we are not building the bundled kernel module
# I have to do it after the configure run unfortunately
rm -fr kernel

# Prevent libtool from defining rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f '{}' \;

# install systemd unit file
install -d -m 755 %{buildroot}/%{_unitdir}
install -c -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}

# install supporting script
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -c -m 755 %{SOURCE2} %{buildroot}%{_libexecdir}/%{name}

# install ipset-config
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -c -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-config

# Create directory for configuration
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# Turn absolute symlink into a relative one
ln -sf %{name} %{buildroot}/%{_sbindir}/%{name}-translate


%preun
if [[ $1 -eq 0 && -n $(lsmod | grep "^xt_set ") ]]; then
    rmmod xt_set 2>/dev/null
    [[ $? -ne 0 ]] && echo Current iptables configuration requires ipsets && exit 1
fi


%ldconfig_scriptlets libs


%post service
%systemd_post %{name}.service
if [[ -f /etc/ipset/ipset ]] && [[ ! -f /etc/sysconfig/ipset ]]; then
	mv /etc/ipset/ipset /etc/sysconfig/ipset
	ln -s /etc/sysconfig/ipset /etc/ipset/ipset
	echo "Warning: ipset save location has moved to /etc/sysconfig"
fi
[[ -f /etc/sysconfig/iptables-config ]] && . /etc/sysconfig/iptables-config
[[ -f /etc/sysconfig/ip6tables-config ]] && . /etc/sysconfig/ip6tables-config
if [[ ${IPTABLES_SAVE_ON_STOP} == yes ]] || \
   [[ ${IP6TABLES_SAVE_ON_STOP} == yes ]]; then
	echo "Warning: ipset no longer saves automatically when iptables does"
	echo "         must enable explicitly in /etc/sysconfig/ipset-config"
fi

%preun service
if [[ $1 -eq 0 && -n $(lsmod | grep "^xt_set ") ]]; then
    rmmod xt_set 2>/dev/null
    [[ $? -ne 0 ]] && echo Current iptables configuration requires ipsets && exit 1
fi
%systemd_preun %{name}.service

%postun service
%systemd_postun_with_restart %{name}.service


%files
%doc ChangeLog
%license COPYING
%{_mandir}/man8/%{name}*.8.*
%{_sbindir}/%{name}
%{_sbindir}/%{name}-translate

%files libs
%license COPYING
%{_libdir}/lib%{name}.so.13*

%files devel
%{_includedir}/lib%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_mandir}/man3/libipset.3.*

%files service
%{_unitdir}/%{name}.service
%dir %{_libexecdir}/%{name}
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/ipset-config
%ghost %config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/ipset
%attr(0755,root,root) %{_libexecdir}/%{name}/%{name}.start-stop


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 20 2025 Phil Sutter <psutter@redhat.com> - 7.24-1
- new version

* Wed May 07 2025 Phil Sutter <psutter@redhat.com> - 7.23-1
- new version

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 01 2024 Phil Sutter <psutter@redhat.com> - 7.22-1
- Turn absolute ipset-translate symlink into a relative one
- Rebase onto v7.22 plus fixes

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 12 2024 Nicolas Chauvet <kwizart@gmail.com> - 7.21-1
- Update to 7.21

* Thu Feb 01 2024 Nicolas Chauvet <kwizart@gmail.com> - 7.20-1
- Update to 7.20

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 23 2023 Nicolas Chauvet <kwizart@gmail.com> - 7.19-1
- Update to 7.19

* Fri Aug 11 2023 Phil Sutter <psutter@redhat.com> - 7.17-7
- Convert license to SPDX format

* Fri Aug 11 2023 Phil Sutter <psutter@redhat.com> - 7.17-6
- Convert license to SPDX format

* Fri Aug 11 2023 Phil Sutter <psutter@redhat.com> - 7.17-5
- Convert license to SPDX format

* Fri Aug 11 2023 Phil Sutter <psutter@redhat.com> - 7.17-4
- Convert license to SPDX format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Nicolas Chauvet <kwizart@gmail.com> - 7.17-1
- Update to 7.17

* Fri Dec 02 2022 Nicolas Chauvet <kwizart@gmail.com> - 7.16-1
- Update to 7.16

* Tue Aug 23 2022 Nicolas Chauvet <kwizart@gmail.com> - 7.15-5
- Backport upstream patches - rhbz#2117654
  ipset-translate does not work with IPv6 sets

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 15 2022 Phil Sutter <psutter@redhat.com> - 7.15-3
- Use the advanced init script from Centos9Stream

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 16 2021 Nicolas Chauvet <kwizart@gmail.com> - 7.15-1
- Update to 7.15

* Wed Jul 28 2021 Nicolas Chauvet <kwizart@gmail.com> - 7.14-1
- Update to 7.14

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.11-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Mar 01 2021 Nicolas Chauvet <kwizart@gmail.com> - 7.11-1
- Update to 7.11

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Nicolas Chauvet <kwizart@gmail.com> - 7.10-1
- Update to 7.10

* Wed Dec 16 2020 Nicolas Chauvet <kwizart@gmail.com> - 7.9-1
- Update to 7.9

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 24 2020 Nicolas Chauvet <kwizart@gmail.com> - 7.6-1
- Update to 7.6

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Nicolas Chauvet <kwizart@gmail.com> - 7.5-1
- Update to 7.5

* Mon Nov 04 2019 Eric Garver <eric@garver.life> - 7.4-1
- Update to 7.4

* Mon Aug 19 2019 Nicolas Chauvet <kwizart@gmail.com> - 7.3-1
- Update to 7.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Nicolas Chauvet <kwizart@gmail.com> - 7.2-1
- Update to 7.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Nicolas Chauvet <kwizart@gmail.com> - 6.38-1
- Update to 6.38
- Clean-up spec

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 12 2018 Eric Garver <egarver@redhat.com> - 6.35-3
- Patch for missing header file (RHBZ#1543596)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Nicolas Chauvet <kwizart@gmail.com> - 6.35-1
- Update to 6.35

* Mon Jul 31 2017 Nicolas Chauvet <kwizart@gmail.com> - 6.32-1
- Update to 6.32

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 07 2017 Nicolas Chauvet <kwizart@gmail.com> - 6.29-3
- Userspace needs kernel-headers - rhbz#1420864

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Apr 18 2016 Thomas Woerner <twoerner@redhat.com> - 6.29-1
- New upstream version 6.29 (RHBZ#1317208)
  - Suppress unnecessary stderr in command loop for resize and list
  - Correction in comment test
  - Support chroot buildroots (reported by Jan Engelhardt)
  - Fix "configure" breakage due to pkg-config related changes
    (reported by Jan Engelhardt)
  - Support older pkg-config packages
  - Add bash completion to the install routine (Mart Frauenlob)
  - Fix misleading error message with comment extension
  - Test added to check 0.0.0.0/0,iface to be matched in hash:net,iface type
  - Fix link with libtool >= 2.4.4 (Olivier Blin)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Thomas Woerner <twoerner@redhat.com> - 6.27-1
- New upstream version 6.27 (RHBZ#1145913)

* Sat Oct 10 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 6.26-1
- Upstream 6.26 (RHBZ#1145913)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep 18 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 6.22-1
- New upstream release.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.21.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.21.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 6.21.1-2
- Remove runtime requirement on the kernel.
  https://lists.fedoraproject.org/pipermail/devel/2014-March/196565.html

* Tue Oct 29 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 6.20.1-1
- New upstream release.

* Tue Aug 27 2013 Quentin Armitage <quentin@armitage.org.uk> 6.19-2
- Add service pkg - adds save and reload functionality on shutdown/startup
- Add requires dependency of ipset on matching ipset-libs

* Thu Aug 15 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 6.19-1
- New upstream release.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.16.1-1
- New upstream release.
- Fix a requirement.

* Wed Sep 26 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.14-1
- New upstream release.
- Fix scriptlets, ldconfig is needed for the libs subpackage, not the main one.

* Mon Jul 30 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.13-1
- New upstream release.
- Split out the library in its own subpackage.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.11-1
- New upstream release.
- Removed our patch, it has been integrated upstream. As such, we also don't
  need to re-run autoreconf any more.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 6.9.1-2
- Some fixes based on Pierre-Yves' review feedback.

* Wed Sep 14 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 6.9.1-1
- Initial packaging.
