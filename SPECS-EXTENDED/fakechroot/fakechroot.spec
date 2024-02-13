Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           fakechroot
Version:        2.20.1
Release:        4%{?dist}
Summary:        Gives a fake chroot environment
License:        LGPLv2+
URL:            https://github.com/dex4er/fakechroot
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Patch1:         https://github.com/dex4er/fakechroot/commit/b42d1fb9538f680af2f31e864c555414ccba842a.patch
Patch2:         https://github.com/dex4er/fakechroot/pull/85/commits/534e6d555736b97211523970d378dfb0db2608e9.patch
Patch3:         https://github.com/dex4er/fakechroot/pull/85/commits/75d7e6fa191c11a791faff06a0de86eaa7801d05.patch
Patch4:         https://github.com/dex4er/fakechroot/pull/85/commits/693a3597ea7fccfb62f357503ff177bd3e3d5a89.patch
Patch5:         https://github.com/dex4er/fakechroot/pull/86.patch

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  gcc
# Required for manpage
BuildRequires:  /usr/bin/pod2man
BuildRequires:  gdbm-devel
# ldd.fakechroot
Requires:       /usr/bin/objdump

%description
fakechroot runs a command in an environment were is additionally
possible to use the chroot(8) call without root privileges. This is
useful for allowing users to create their own chrooted environment
with possibility to install another packages without need for root
privileges.

%package        libs
Summary:        Libraries of %{name}

%description    libs
This package contains the libraries required by %{name}.

%prep
%autosetup -p1
# For %%doc dependency-clean.
chmod -x scripts/{relocatesymlinks,restoremode,savemode}.sh

%build
autoreconf -vfi

%configure --disable-static --disable-silent-rules --with-libpath="%{_libdir}/fakechroot"

%make_build

%install
%make_install
# Drop libtool files
find %{buildroot}%{_libdir} -name '*.la' -delete -print

%check
%make_build check

%files
%doc scripts/{relocatesymlinks,restoremode,savemode}.sh
%doc NEWS.md README.md THANKS.md
%license COPYING LICENSE
%{_bindir}/%{name}
%{_bindir}/env.%{name}
%{_bindir}/ldd.%{name}
%{_sbindir}/chroot.%{name}
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/chroot.env
%config(noreplace) %{_sysconfdir}/%{name}/debootstrap.env
%config(noreplace) %{_sysconfdir}/%{name}/rinse.env
%{_mandir}/man1/%{name}.1*

%files libs
%{_libdir}/%{name}/

%changelog
* Thu Mar 03 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.20.1-4
- Apply Fedora 36 patches (license: MIT) to fix compilation with GCC 11.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.20.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Sérgio Basto <sergio@serjux.com> - 2.20.1-2
- (#1241555) fakechroot isn't multilib

* Fri Oct 18 2019 Sérgio Basto <sergio@serjux.com> - 2.20.1-1
- Update to 2.20.1 (#1689666)
- Drop upstreamed patch

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.19-4
- Add support for LFS

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 07 2017 Sérgio Basto <sergio@serjux.com> - 2.19-1
- Update fakechroot to 2.19 (#1396855)

* Wed May 18 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.18-1
- Update to 2.18

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Christopher Meng <rpm@cicku.me> - 2.17.2-1
- Update to 2.17.2

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.9-29
- Add BR: /usr/bin/pod2man (Fix FTBFS #913997).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 2.9-23
- Added patch to remove test for specific version of automake.

* Sat Apr 18 2009 Richard W.M. Jones <rjones@redhat.com> - 2.9-22
- FAKECHROOT_CMD_SUBST patch has now been accepted upstream.

* Tue Apr 14 2009 Richard W.M. Jones <rjones@redhat.com> - 2.9-20
- Add fakechroot-scandir.patch to fix builds on Rawhide.

* Tue Apr 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.9-19
- Update to 2.9.
- Removed fakechroot-2.8-initsocketlen.patch (upstream now).
- Removed int->ssize_t readlink type change (upstream testing for type
  now).
- Removed permission fix for scripts/ldd.fake scripts/restoremode.sh
  scripts/savemode.sh (fixed upstream).

* Wed Mar 18 2009 Richard W.M. Jones <rjones@redhat.com> - 2.8-18
- Create a fakeroot-libs subpackage so that the package is multilib aware.

* Thu Jan 15 2009 Rakesh Pandit <rakesh@fedoraproject.org> 2.8-16
- Fixed URL

* Sun Oct  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.8-15
- Fix getpeername/getsockname socklen initialization.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.8-14
- %%check || : does not work anymore.

* Sun Aug  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.8-13
- Update to 2.8.

* Mon Jan  1 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.5-12
- Remove executable bits from scripts in documentation.

* Sun Dec 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.5-11
- Add %%{_libdir}/fakechroot to %%files.
- Fix license (is LGPL, not GPL).
- Add commented %%check (currently broken).
- Add ldd.fake and save/restoremode.sh to %%doc

* Fri Dec 29 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.5-10
- Extend the %%description a bit.

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.5-9
- Don't build static lib.
- Exclude libtool lib.

* Thu Nov 24 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 2.5.

* Sat Sep 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 2.4.

* Sun Jul  3 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9+1.3.

* Sun Feb  6 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.5+1.2.4.

* Sun Jan 25 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.
