Summary:        administration tool for IP sets
Name:           ipset
Version:        7.15
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/tools
URL:            https://ipset.netfilter.org/
Source0:        https://ipset.netfilter.org/%{name}-%{version}.tar.bz2
# Source1 and Source2 are from Fedora 35 (License: MIT)
# https://src.fedoraproject.org/rpms/ipset/tree/f35
Source1:        %{name}.service
Source2:        %{name}.start-stop
BuildRequires:  libmnl-devel
Requires:       libmnl
Provides:       %{name}-libs = %{version}-%{release}

%description
IP sets are a framework inside the Linux kernel, which can be administered by the ipset utility. Depending on the type, an IP set may store IP addresses, networks, (TCP/UDP) port numbers, MAC addresses, interface names or combinations of them in a way, which ensures lightning speed when matching an entry against a set.

If you want to store multiple IP addresses or port numbers and match against the collection by iptables at one swoop;
dynamically update iptables rules against IP addresses or ports without performance penalty;
express complex IP address and ports based rulesets with one single iptables rule and benefit from the speed of IP sets
then ipset may be the proper tool for you.

%package devel
Summary:        Development files for the ipset library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries and header files for ipset.

%package service
Summary:        %{name} service for %{name}s
BuildRequires:  systemd
Requires:       %{name} = %{version}-%{release}
Requires:       iptables-services
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd
BuildArch:      noarch

%description service
This package provides the service %{name}

%prep
%autosetup

%build
%configure \
    --enable-static=no \
    --with-kmod=no
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

# install systemd unit file
install -d -m 755 %{buildroot}/%{_unitdir}
install -c -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}

# install supporting script
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -c -m 755 %{SOURCE2} %{buildroot}%{_libexecdir}/%{name}

# Create directory for configuration
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

%ldconfig_scriptlets

%post service
%systemd_post %{name}.service

%preun service
if [[ $1 -eq 0 && -n $(lsmod | grep "^xt_set ") ]]; then
    rmmod xt_set 2>/dev/null
    [[ $? -ne 0 ]] && echo Current iptables configuration requires ipsets && exit 1
fi
%systemd_preun %{name}.service

%postun service
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_libdir}/libipset.so.13*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libipset.so
%{_libdir}/pkgconfig/libipset.pc

%files service
%{_unitdir}/%{name}.service
%dir %{_libexecdir}/%{name}
%attr(0755,root,root) %{_libexecdir}/%{name}/%{name}.start-stop
%dir %{_sysconfdir}/%{name}

%changelog
* Thu Jun 15 2023 Andy Zaugg <azaugg@linkedin.com> - 7.15-2
- Fix ipset systemd unit file

* Tue Feb 01 2022 Rachel Menge <rachelmenge@microsoft.com> - 7.15-1
- Update source to 7.15
- Remove check section since testsuite depends on kernel module
  which we do not build

* Thu Sep 30 2021 Olivia Crain <oliviacrain@microsoft.com> - 7.1-3
- Add service subpackage from Fedora 35 (license: MIT)
- Add provides for libs subpackage from main package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 7.1-2
- Added %%license line automatically

* Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> - 7.1-1
- Update to 7.1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 6.38-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 06 2018 Ankit Jain <ankitja@vmware.com> - 6.38-1
- Upgrading version to 6.38

* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> - 6.32-1
- Upgrading version to 6.32

* Wed Aug 3 2016 Xiaolin Li <xiaolinl@vmware.com> - 6.29-1
- Initial build. First version
