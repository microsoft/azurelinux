%global srcname pyroute2

Summary:        Pure Python netlink library
Name:           python-%{srcname}
Version:        0.6.5
Release:        2%{?dist}
License:        GPLv2+
URL:            https://github.com/svinota/%{srcname}
Source0:        %{srcname}-%{version}.tar.gz
Source1:        %{srcname}.core-%{version}.tar.gz
Source2:        %{srcname}.nslink-%{version}.tar.gz
Source3:        %{srcname}.nftables-%{version}.tar.gz
Source4:        %{srcname}.ethtool-%{version}.tar.gz
Source5:        %{srcname}.ipset-%{version}.tar.gz
Source6:        %{srcname}.ipdb-%{version}.tar.gz
Source7:        %{srcname}.ndb-%{version}.tar.gz
BuildArch:      noarch

%description
PyRoute2 provides several levels of API to work with Netlink
protocols, such as Generic Netlink, RTNL, TaskStats, NFNetlink,
IPQ.

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
 
%description -n python3-%{srcname}
PyRoute2 provides several levels of API to work with Netlink
protocols, such as Generic Netlink, RTNL, TaskStats, NFNetlink,
IPQ.

%prep
%setup -q -n %{srcname}-%{version}
cd ..
tar xzvf %{Source1}
tar xzvf %{Source2}
tar xzvf %{Source3}
tar xzvf %{Source4}
tar xzvf %{Source5}
tar xzvf %{Source6}
tar xzvf %{Source7}

%build
%py3_build
cd ../pyroute2.core-%{version}
%py3_build
cd ../pyroute2.nslink-%{version}
%py3_build
cd ../pyroute2.nftables-%{version}
%py3_build
cd ../pyroute2.ethtool-%{version}
%py3_build
cd ../pyroute2.ipset-%{version}
%py3_build
cd ../pyroute2.ipdb-%{version}
%py3_build
cd ../pyroute2.ndb-%{version}
%py3_build

%install
%py3_install
cd ../pyroute2.core-%{version}
%py3_install
cd ../pyroute2.nslink-%{version}
%py3_install
cd ../pyroute2.nftables-%{version}
%py3_install
cd ../pyroute2.ethtool-%{version}
%py3_install
cd ../pyroute2.ipset-%{version}
%py3_install
cd ../pyroute2.ipdb-%{version}
%py3_install
cd ../pyroute2.ndb-%{version}
%py3_install

%files -n python3-%{srcname}
%{_bindir}/ss2
%{_bindir}/%{srcname}-cli
%doc README* LICENSE.GPL.v2 LICENSE.Apache.v2
%{python3_sitelib}/%{srcname}*
%{python3_sitelib}/pr2modules


%changelog
* Tue Feb 08 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.6.5-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

* Tue Feb 01 2022 Alfredo Moralejo <amoralej@rechat.com> - 0.6.5-1
- Update to 0.6.5

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.5.14-2
- Rebuilt for Python 3.10

* Fri Feb 19 2021 Yatin Karel <ykarel@redhat.com> - 0.5.14-1
- Update to 0.5.14

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5.6-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Yatin Karel <ykarel@redhat.com> - 0.5.6-1
- Update to 0.5.6

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-6
- Subpackage python2-pyroute2 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Alfredo Moralejo <amoralej@redhat.com> - 0.5.3-3
- Fix build in CentOS7.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 07 2018 Slawek Kaplonski <skaplons@redhat.com> 0.5.3-1
- Update to 0.5.3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.2-2
- Rebuilt for Python 3.7

* Thu Jun 21 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 0.5.2-1
- Upstream 0.5.2 (includes previous deprecated async arg patch)

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.21-3
- Rebuilt for Python 3.7

* Fri Mar 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.4.21-2
- Conditionalize the Python 2 subpackage
- Don't build the Python 2 subpackage on EL > 7

* Fri Feb 9 2018 amoralej <amoralej@redhat.com> - 0.4.21-1
- Upstream 0.4.21

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 29 2017 hguemar <hguemar@benihime.seireitei> - 0.4.19-1
- Upstream 0.4.19

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun  1 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 0.4.15-1
- Upstream 0.4.15
- req: #365 -- full and short nla notation fixed, critical
- iproute: #364 -- new method, brport()
- ipdb: -- support bridge port options

* Tue Mar  7 2017 Antoni S. Puimedon <antonisp@celebdor.com> 0.4.13-1
- upgrade to 0.4.13
- ipset hash:mac support
- ipset: hash:mac support
- ipset: list:set support
- ifinfmsg: allow absolute/relative paths in the net_ns_fd NLA
- ipdb: #322 -- IPv6 updates on interfaces in DOWN state
- rtnl: #284 -- support vlan_flags
- ipdb: #307 -- fix IPv6 routes management
- ipdb: #311 -- vlan interfaces address loading
- iprsocket: #305 -- support NETLINK_LISTEN_ALL_NSID

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.10-2
- Rebuild for Python 3.6

* Fri Oct 14 2016 Peter V. Saveliev <peter@svinota.eu> 0.4.10-1
- devlink fd leak fix

* Thu Oct  6 2016 Peter V. Saveliev <peter@svinota.eu> 0.4.9-1
- critical fd leak fix
- initial NETLINK_SOCK_DIAG support

* Tue Sep 27 2016 Peter V. Saveliev <peter@svinota.eu> 0.4.8-1
- uplift to 0.4.x

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.19-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr  5 2016 Peter V. Saveliev <peter@svinota.eu> 0.3.19-1
- separate Python2 and Python3 packages
- MPLS lwtunnel support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.15-2

- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Fri Nov 20 2015 Peter V. Saveliev <peter@svinota.eu> 0.3.15-1
- critical NetNS fd leak fix

* Tue Sep  1 2015 Peter V. Saveliev <peter@svinota.eu> 0.3.14-1
- bogus rpm dates in the changelog are fixed
- both licenses added

* Tue Sep  1 2015 Peter V. Saveliev <peter@svinota.eu> 0.3.13-1
- BPF filters support
- MPLS routes support
- MIPS platform support
- multiple improvements on iwutil
- memory consumption improvements

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan  8 2015 Peter V. Saveliev <peter@svinota.eu> 0.3.4-1
- Network namespaces support
- Veth, tuntap
- Route metrics

* Fri Dec  5 2014 Peter V. Saveliev <peter@svinota.eu> 0.3.3-1
- Fix-ups, 0.3.3
- Bugfixes for Python 2.6

* Tue Nov 18 2014 Peter V. Saveliev <peter@svinota.eu> 0.3.2-1
- Update to 0.3.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Jiri Pirko <jpirko@redhat.com> - 0.2.7-1
- Update to 0.2.7

* Thu Aug 22 2013 Peter V. Saveliev <peet@redhat.com> 0.1.11-1
- IPRSocket threadless objects
- rtnl: tc filters improvements

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Peter V. Saveliev <peet@redhat.com> 0.1.10-1
- fd and threads leaks fixed
- shutdown sequence fixed (release() calls)
- ipdb: interface removal
- ipdb: fail on transaction sync timeout

* Tue Jun 11 2013 Peter V. Saveliev <peet@redhat.com> 0.1.9-2
- fedpkg import fix

* Tue Jun 11 2013 Peter V. Saveliev <peet@redhat.com> 0.1.9-1
- several races fixed
- Python 2.6 compatibility issues fixed

* Wed Jun 05 2013 Peter V. Saveliev <peet@redhat.com> 0.1.8-1
- initial RH build
