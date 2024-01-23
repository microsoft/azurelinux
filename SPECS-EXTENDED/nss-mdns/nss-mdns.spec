Vendor:         Microsoft Corporation
Distribution:   Mariner

Name: nss-mdns
Version: 0.15.1
Release: 11%{?dist}
Summary: glibc plugin for .local name resolution

License: LGPLv2+
URL: https://github.com/lathiat/nss-mdns
Source0: https://github.com/lathiat/nss-mdns/releases/download/v%{version}/nss-mdns-%{version}.tar.gz

# https://github.com/lathiat/nss-mdns/pull/84
Patch1:  nss-mdns-local-heuristic.patch
Patch2:  nss-mdns-local-heuristic-unit.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: pkgconfig(check)
Requires: avahi
Requires: authselect

%description
nss-mdns is a plugin for the GNU Name Service Switch (NSS) functionality of
the GNU C Library (glibc) providing host name resolution via Multicast DNS
(aka Zeroconf, aka Apple Rendezvous, aka Apple Bonjour), effectively allowing
name resolution by common Unix/Linux programs in the ad-hoc mDNS domain .local.

nss-mdns provides client functionality only, which means that you have to
run a mDNS responder daemon separately from nss-mdns if you want to register
the local host name via mDNS (e.g. Avahi).


%prep
%autosetup -p1

%build
%configure --libdir=/%{_lib}
%make_build

%check
make check || (cat ./test-suite.log; false)

%install
rm -rf $RPM_BUILD_ROOT
%make_install


%post
%{?ldconfig}

%posttrans
authselect enable-feature with-mdns4 &> /dev/null || :

%preun
authselect disable-feature with-mdns4 &> /dev/null || :

%ldconfig_postun


%files
%license LICENSE
%doc README.md NEWS.md ACKNOWLEDGEMENTS.md
/%{_lib}/*.so.*


%changelog
* Mon Jan 22 2024 Alexander Dobrzhansky <cptlangley@gmail.com> - 0.15.1-11     
- First version of nss-mdns for CBL-Mariner. Spec file imported from Fedora.

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 06 2022 Petr Menšík <pemensik@redhat.com> - 0.15.1-7
- Attempt to solve local heuristic (#2148500)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 16 2022 Pavel Březina - 0.15.1-5
- Require authselect since it is used in scriptlets to auto-enable nss-mdns

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Pavel Březina - 0.15.1-3
- Rely only on authselect for nsswitch.conf changes (#2023745)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 12 2021 Adam Goode <adam@spicenitz.org> - 0.15.1-1
- New upstream release, fixes broken 0.15 release

* Tue May 11 2021 Adam Goode <adam@spicenitz.org> - 0.15-1
- New upstream release

* Fri Mar 26 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.14.1-11
- Move 'myhostname' before 'mdns4_minimal' (#1943199)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep  2 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.14.1-9
- Place 'mdns4_minimal' in /etc/nsswitch.conf after 'files' in /etc/nsswitch.conf,
  so that it ends up before 'resolve' (#1867830)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 17 2020 Pavel Březina <pbrezina@redhat.com> - 0.14.1-7
- Do not remove mdns from nsswitch.conf during upgrade

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Adam Goode <adam@spicenitz.org> - 0.14.1-5
- Properly work with or without authselect (BZ #1577243)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Adam Goode <adam@spicenitz.org> - 0.14.1-1
- New upstream release
- Modernize the spec file

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 30 2008 Stepan Kasal <skasal@redhat.com> - 0.10-6
- use sed instead of perl in %%post and %%preun (#462996),
  fixing two bugs in the scriptlets:
  1) the backup file shall be nsswitch.conf.bak, not nsswitch.confbak
  2) the first element after host: shall be subject to removal, too
- consequently, removed the Requires(..): perl
- removed the reqires for things that are granted
- a better BuildRoot

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-5
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.10-4
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.10-3
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 - Lennart Poettering <lpoetter@redhat.com> - 0.10-2
- Fix up post/preun/postun dependencies, add "avahi" to the dependencies,
  include dist tag in Release field, use _lib directory instead of literal /lib.

* Fri Jun 22 2007 - Lennart Poettering <lpoetter@redhat.com> - 0.10-1
- Update to 0.10, replace perl script by simpler and more robust versions,
  stolen from the Debian package

* Thu Jul 13 2006 - Bastien Nocera <hadess@hadess.net> - 0.8-2
- Make use of Ezio's perl scripts to enable and disable mdns4 lookups
  automatically, patch from Pancrazio `Ezio' de Mauro <pdemauro@redhat.com>

* Tue May 02 2006 - Bastien Nocera <hadess@hadess.net> - 0.8-1
- Update to 0.8, disable legacy lookups so that all lookups are made through
  the Avahi daemon

* Mon Apr 24 2006 - Bastien Nocera <hadess@hadess.net> - 0.7-2
- Fix building on 64-bit platforms

* Tue Dec 13 2005 - Bastien Nocera <hadess@hadess.net> - 0.7-1
- Update to 0.7, fix some rpmlint errors

* Thu Nov 10 2005 - Bastien Nocera <hadess@hadess.net> - 0.6-1
- Update to 0.6

* Tue Dec 07 2004 - Bastien Nocera <hadess@hadess.net> 0.1-1
- Initial package, automatically adds and remove mdns4 as a hosts service
