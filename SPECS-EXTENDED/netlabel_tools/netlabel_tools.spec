Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Tools to manage the Linux NetLabel subsystem
Name: netlabel_tools
Version: 0.30.0
Release: 10%{?dist}
License: GPLv2
URL: https://github.com/netlabel/netlabel_tools
Source: https://github.com/netlabel/netlabel_tools/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0: rhbz1683434.patch

Requires: libnl3
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires:  gcc
BuildRequires: kernel-headers
BuildRequires: libnl3-devel
BuildRequires: doxygen
BuildRequires: systemd
BuildRequires: systemd-devel

%description
NetLabel is a kernel subsystem which implements explicit packet labeling
protocols such as CIPSO for Linux.  Packet labeling is used in secure networks
to mark packets with the security attributes of the data they contain.  This
package provides the necessary user space tools to query and configure the
kernel subsystem.

%prep
%setup -q
%patch0 -p1

%build
%configure
make V=1 %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}/etc"
mkdir -p "%{buildroot}/%{_sbindir}"
mkdir -p "%{buildroot}/%{_unitdir}"
mkdir -p "%{buildroot}/%{_mandir}"
make V=1 DESTDIR="%{buildroot}" install

# NOTE: disable since the tests require messing with the running kernel
#%check
#make V=1 check

%preun
%systemd_preun netlabel.service

%postun
%systemd_postun netlabel.service

%post
%systemd_post netlabel.service

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README
%doc CHANGELOG
%doc SUBMITTING_PATCHES
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0755,root,root) %{_sbindir}/netlabelctl
%attr(0755,root,root) %{_sbindir}/netlabel-config
%attr(0644,root,root) %{_unitdir}/netlabel.service
%attr(0644,root,root) %config(noreplace) /etc/netlabel.rules

%changelog
* Mon Jun 07 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.30.0-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add BR:systemd-devel for the systemd *.pc files

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 02 2019 Paul Moore <paul@paul-moore.com> - 0.30.0-8
- Applied upstream patch to improve netlabel-config error reporting (rhbz #1683434)
- Removed the kernel dependency (rhbz #1733605)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Paul Moore <pmoore@redhat.com> - 0.30.0-0
-New upstream version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 10 2015 Paul Moore <pmoore@redhat.com> - 0.21-0
- New upstream version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Mar 21 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.20-5
- Add patch to support libnl3
- Use %%license
- Cleanup spec

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Paul Moore <pmoore@redhat.com> - 0.20-2
- Build with CFLAGS="${optflags}"

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 3 2013 Paul Moore <pmoore@redhat.com> - 0.20-0
- Version bump to match latest upstream
- Cleanups in the specfile due to changes in the upstream package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 17 2010 Peter Vrabec <pvrabec@redhat.com> - 0.19-8
- fixing return codes (#602291)

* Wed Jun 16 2010 Peter Vrabec <pvrabec@redhat.com> - 0.19-7
- make initscript LSB compliant (#522818)
- show version of netlabelctl and libnetlabel in help (#602577)

* Wed Sep 23 2009 Peter Vrabec <pvrabec@redhat.com> 0.19-6
- make initscript LSB compliant (#522818)

* Wed Sep 23 2009 Peter Vrabec <pvrabec@redhat.com> 0.19-5
- increase rel. number

* Wed Sep 23 2009 Peter Vrabec <pvrabec@redhat.com> 0.19-4
- fix license tag in spec (#524310)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 08 2009 Peter Vrabec <pvrabec@redhat.com> - 0.19-1
- upgrade (#478903)

* Mon Oct 27 2008 Peter Vrabec <pvrabec@redhat.com> - 0.18-1
- upgrade (#439833)

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-8
- fix license tag

* Mon Feb  11 2008 Steve Conklin <sconklin@redhat.com> - 0.17-7
- New patch for bz#431766 to resolve conflicts

* Thu Feb  7 2008 Steve Conklin <sconklin@redhat.com> - 0.17-6
- Various fixes to follow upstream
- Resolves bz#431765 The example configuration file is invalid
- Resolves bz#431766 The netlabelctl command fails to run due to newer libnl package
- Resolves bz#431767 The url listed in the netlabel_tools package is wrong

* Mon Oct 16 2006 James Antill <james@and.org> - 0.17-3
- Add upstream patch.
- s/p1/p0/ for upstream patch.

* Sat Oct 14 2006 Steve Grubb <sgrubb@redhat.com> - 0.17-3
- Add init scripts and default rules

* Sun Oct  1 2006 James Antill <james@and.org> - 0.17-2
- Upgrade to latest upstream.

* Tue Aug 29 2006 James Antill <james@and.org> - 0.16-5
- Fix install calls for mock.

* Tue Aug 29 2006 James Antill <james@and.org> - 0.16-4
- Fix more reviewing problems, building on newer kernel-headers.
- Add URL tag.

* Fri Aug 18 2006 James Antill <james@and.org> - 0.16-3
- Fix minor review problems.
- Added BuildRequires for kernel headers (netlink).

* Fri Aug 18 2006 James Antill <james@and.org> - 0.16-2
- Use root as owner.
- Contribute to fedora extras.

* Thu Aug  3 2006 Paul Moore <paul.moore@hp.com> 0.16-1
- Bumped version number.

* Thu Jul  6 2006 Paul Moore <paul.moore@hp.com> 0.15-1
- Bumped version number.

* Mon Jun 26 2006 Paul Moore <paul.moore@hp.com> 0.14-1
- Bumped version number.
- Changes related to including the version number in the path name.
- Changed the netlabelctl perms from 0750 to 0755.
- Removed the patch. (included in the base with edits)
- Updated the description.

* Fri Jun 23 2006 Steve Grubb <sgrubb@redhat.com> 0.13-1
- Initial build.

