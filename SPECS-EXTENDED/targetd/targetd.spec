Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           targetd
License:        GPLv3
Summary:        Service to make storage remotely configurable
Version:        0.9.0
Release:        2%{?dist}
URL:            https://github.com/open-iscsi/targetd
Source:         https://github.com/open-iscsi/targetd/archive/v%{version}/targetd-%{version}.tar.gz
Source1:        targetd.service
BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-devel
Requires:       python3-PyYAML python3-setproctitle python3-rtslib target-restore
Requires:       nfs-utils, btrfs-progs, python3-blockdev, libblockdev-lvm

%description
targetd turns the machine into a remotely-configurable storage appliance.
It supports an HTTP/jsonrpc-2.0 interface to let a remote
administrator allocate volumes from an LVM volume group, and export
those volumes over iSCSI.

%prep
%setup -q

%build
%py3_build

%install
mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_mandir}/man5/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/target/
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/targetd.service
install -m 644 targetd.yaml %{buildroot}%{_sysconfdir}/target/targetd.yaml
install -m 644 targetd.8 %{buildroot}%{_mandir}/man8/
install -m 644 targetd.yaml.5 %{buildroot}%{_mandir}/man5/
%py3_install

%post
%systemd_post targetd.service

%preun
%systemd_preun targetd.service

%postun
%systemd_postun_with_restart targetd.service

%files
%{_bindir}/targetd
%{_unitdir}/targetd.service
%{python3_sitelib}/targetd/
%{python3_sitelib}/targetd/backends/
%{python3_sitelib}/*.egg-info
%license LICENSE
%doc README.md API.md client
%{_mandir}/man8/targetd.8*
%{_mandir}/man5/targetd.yaml.5*
%config(noreplace) %{_sysconfdir}/target/targetd.yaml

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Sep 10 2020 Tony Asleson <tasleson@redhat.com> - 0.9.0-1
- New upstream release

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Tony Asleson <tasleson@redhat.com> - 0.8.12-1
- New upstream release

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8.11-2
- Rebuilt for Python 3.9

* Tue Feb 25 2020 Tony Asleson <tasleson@redhat.com> - 0.8.11-1
- New upstream release
- Add man page for targetd.yaml.8

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Tony Asleson <tasleson@redhat.com> - 0.8.9-1
* Revive package and update to latest upstream release.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.6-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 3 2017 Tony Asleson <tasleson@redhat.com> 0.8.6-2
- Add and correct dependencies

* Thu Apr 27 2017 Tony Asleson <tasleson@redhat.com> 0.8.6-1
- New upstream version, bug fixes

* Thu Feb 16 2017 Tony Asleson <tasleson@redhat.com> 0.8.5-1
- New upstream version which has python3 support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 12 2015 Andy Grover <agrover@redhat.com> 0.8.3-1
- New upstream version

* Tue Jun 23 2015 Andy Grover <agrover@redhat.com> 0.8.2-1
- New upstream version

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 Andy Grover <agrover@redhat.com> 0.8.1-1
- New upstream version

* Tue Feb 10 2015 Andy Grover <agrover@redhat.com> 0.8-1
- New upstream version

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Andy Grover <agrover@redhat.com> 0.7.2-1
- New upstream version

* Mon Feb 10 2014 Andy Grover <agrover@redhat.com> 0.7.1-1
- New upstream version

* Mon Nov 25 2013 Andy Grover <agrover@redhat.com> 0.7-2
- Fix service file for new ktarget service name
- Add python-rtslib to requires

* Fri Nov 8 2013 Andy Grover <agrover@redhat.com> 0.7-1
- New upstream version
- Use systemd spec macros

* Thu Aug 8 2013 Andy Grover <agrover@redhat.com> 0.6.1-1
- Update to latest version, make needed changes
- Drop patches:
  * require-password.patch
  * use-std-ssl.patch
- Change requires from python-lvm to lvm2-python-libs

* Mon Aug  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.3.1-7
- Add systemd to BuildReq to fix FTBFS

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 16 2013 Andy Grover <agrover@redhat.com> - 0.3.1-5
- Update require-password.patch
- Change target.yaml to not include a commented-out default password

* Tue Apr 16 2013 Andy Grover <agrover@redhat.com> - 0.3.1-4
- Remove dependency on python-tlslite

* Mon Apr 15 2013 Andy Grover <agrover@redhat.com> - 0.3.1-3
- Add patch
  * use-std-ssl.patch
  * require-password.patch

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Andy Grover <agrover@redhat.com> - 0.3.1-1
- New upstream version

* Mon Sep 24 2012 Andy Grover <agrover@redhat.com> - 0.3-1
- New upstream version

* Fri Sep 7 2012 Andy Grover <agrover@redhat.com> - 0.2.4-1
- New upstream version

* Tue Aug 28 2012 Andy Grover <agrover@redhat.com> - 0.2.3-1
- New upstream version
- Add new dependency python-tlslite

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Andy Grover <agrover@redhat.com> - 0.2.2-2
- Add proper pkg requires

* Mon Jun 25 2012 Andy Grover <agrover@redhat.com> - 0.2.2-1
- Initial packaging
