%define _userunitdir %{_libdir}/systemd/user
Summary:        Library for loading and sharing PKCS#11 modules
Name:           p11-kit
Version:        0.25.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://p11-glue.freedesktop.org/p11-kit.html
Source0:        https://github.com/p11-glue/p11-kit/releases/download/%{version}/p11-kit-%{version}.tar.xz
Source1:        trust-extract-compat
Source2:        p11-kit-client.service
BuildRequires:  gcc
BuildRequires:  gtk-doc
BuildRequires:  libffi-devel
BuildRequires:  libtasn1-devel >= 2.3
BuildRequires:  systemd-bootstrap-devel

%description
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they're discoverable.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package trust
Summary:        System trust module from %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires(post): chkconfig
Requires(postun): chkconfig
Conflicts:      nss < 3.14.3-9

%description trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.

%package server
Summary:        Server and client commands for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description server
The %{name}-server package contains command line tools that enables
exporting PKCS#11 modules through a Unix domain socket.  Note that this
feature is still experimental.

# solution taken from icedtea-web.spec
%define multilib_arches ppc64 sparc64 x86_64 ppc64le
%ifarch %{multilib_arches}
%define alt_ckbi  libnssckbi.so.%{_arch}
%else
%define alt_ckbi  libnssckbi.so
%endif
Vendor:         Microsoft Corporation
Distribution:   Mariner

%prep
%setup -q

%build
# These paths are the source paths that  come from the plan here:
# https://fedoraproject.org/wiki/Features/SharedSystemCertificates:SubTasks
%configure --disable-static --enable-doc --with-trust-paths=%{_sysconfdir}/pki/ca-trust/source:%{_datadir}/pki/ca-trust-source --disable-silent-rules LIBS='-lpthread'
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/pkcs11/modules
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name "*.la" -delete -print
install -p -m 755 %{SOURCE1} %{buildroot}%{_libexecdir}/p11-kit/
# Install the example conf with %%doc instead
rm %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf.example
mkdir -p %{buildroot}%{_userunitdir}
install -p -m 644 %{SOURCE2} %{buildroot}%{_userunitdir}

%check
make check


%post -p /sbin/ldconfig
%post trust
%{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
        %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so 30

%postun -p /sbin/ldconfig
%postun trust
if [ $1 -eq 0 ] ; then
        # package removal
        %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so
fi

%files
%license COPYING
%doc AUTHORS NEWS README
%doc p11-kit/pkcs11.conf.example
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libexecdir}/p11-kit
%{_bindir}/p11-kit
%{_libdir}/libp11-kit.so.*
%{_libdir}/p11-kit-proxy.so
%{_libexecdir}/p11-kit/p11-kit-remote
%{_mandir}/man1/trust.1.gz
%{_mandir}/man8/p11-kit.8.gz
%{_mandir}/man5/pkcs11.conf.5.gz

%files devel
%{_includedir}/p11-kit-1/
%{_libdir}/libp11-kit.so
%{_libdir}/pkgconfig/p11-kit-1.pc
%doc %{_datadir}/gtk-doc/

%files trust
%{_bindir}/trust
%dir %{_libdir}/pkcs11
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/pkcs11/p11-kit-trust.so
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libexecdir}/p11-kit/trust-extract-compat

%files server
%{_libdir}/pkcs11/p11-kit-client.so
%{_userunitdir}/p11-kit-client.service
%{_libexecdir}/p11-kit/p11-kit-server
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.25.0-1
- Auto-upgrade to 0.25.0 - Azure Linux 3.0 - package upgrades

* Thu Feb 24 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 0.24.1-1
- Upgrading to v0.24.1

* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.23.22-3
- Replacing 'systemd-devel' BR with 'systemd-bootstrap-devel'
  to remove cyclic dependencies in other packages.

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 0.23.22-2
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Dec 28 2020 Nicolas Ontiveros <niontive@microsoft.com> - 0.23.22-1
- Upgrade to version 0.23.22 to fix CVE-2020-29361, CVE-2020-29362, and CVE-2020-29363
- Update source URL

* Wed May 27 2020 Paul Monson <paulmon@microsoft.com> - 0.23.16.1-2
- Initial CBL-Mariner import from Fedora 29 (license: MIT).
- License verified.

* Thu May 23 2019 Daiki Ueno <dueno@redhat.com> - 0.23.16.1-1
- Update to upstream 0.23.16.1 release

* Mon Feb 18 2019 Daiki Ueno <dueno@redhat.com> - 0.23.15-2
- trust: Ignore unreadable content in anchors

* Mon Jan 21 2019 Daiki Ueno <dueno@redhat.com> - 0.23.15-1
- Update to upstream 0.23.15 release

* Fri Jan 11 2019 Nils Philippsen <nils@tiptoe.de> - 0.23.14-2
- use spaces instead of tabs consistently
- prefer fixed closures to libffi closures (#1656245, patch by Daiki Ueno)

* Mon Sep 10 2018 Daiki Ueno <dueno@redhat.com> - 0.23.14-1
- Update to upstream 0.23.14 release

* Wed Aug 15 2018 Daiki Ueno <dueno@redhat.com> - 0.23.13-3
- Forcibly link with libpthread to avoid regressions (rhbz#1615038)

* Wed Aug 15 2018 Daiki Ueno <dueno@redhat.com> - 0.23.13-2
- Fix invalid memory access on proxy cleanup

* Fri Aug 10 2018 Daiki Ueno <dueno@redhat.com> - 0.23.13-1
- Update to upstream 0.23.13 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 30 2018 Daiki Ueno <dueno@redhat.com> - 0.23.12-1
- Update to upstream 0.23.11 release

* Wed Feb 28 2018 Daiki Ueno <dueno@redhat.com> - 0.23.10-1
- Update to upstream 0.23.10 release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 05 2017 Daiki Ueno <dueno@redhat.com> - 0.23.9-2
- server: Make it possible to eval envvar settings

* Wed Oct 04 2017 Daiki Ueno <dueno@redhat.com> - 0.23.9-1
- Update to upstream 0.23.9

* Fri Aug 25 2017 Kai Engert <kaie@redhat.com> - 0.23.8-2
- Fix a regression caused by a recent nss.rpm change, add a %%ghost file
  for %%{_libdir}/libnssckbi.so that p11-kit-trust scripts install.

* Tue Aug 15 2017 Daiki Ueno <dueno@redhat.com> - 0.23.8-1
- Update to 0.23.8 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun  2 2017 Daiki Ueno <dueno@redhat.com> - 0.23.7-1
- Update to 0.23.7 release

* Thu May 18 2017 Daiki Ueno <dueno@redhat.com> - 0.23.5-3
- Update p11-kit-modifiable.patch to simplify the logic

* Thu May 18 2017 Daiki Ueno <dueno@redhat.com> - 0.23.5-2
- Make "trust anchor --remove" work again

* Thu Mar  2 2017 Daiki Ueno <dueno@redhat.com> - 0.23.5-1
- Update to 0.23.5 release
- Rename -tools subpackage to -server and remove systemd unit files

* Fri Feb 24 2017 Daiki Ueno <dueno@redhat.com> - 0.23.4-3
- Move p11-kit command back to main package

* Fri Feb 24 2017 Daiki Ueno <dueno@redhat.com> - 0.23.4-2
- Split out command line tools to -tools subpackage, to avoid a
  multilib issue with the main package.  Suggested by Yanko Kaneti.

* Wed Feb 22 2017 Daiki Ueno <dueno@redhat.com> - 0.23.4-1
- Update to 0.23.4 release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan  6 2017 Daiki Ueno <dueno@redhat.com> - 0.23.3-2
- Use internal hash implementation instead of NSS (#1390598)

* Tue Dec 20 2016 Daiki Ueno <dueno@redhat.com> - 0.23.3-1
- Update to 0.23.3 release
- Adjust executables location from %%libdir to %%libexecdir

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Martin Preisler <mpreisle@redhat.com> - 0.23.2-1
- Update to stable 0.23.2 release

* Tue Jun 30 2015 Martin Preisler <mpreisle@redhat.com> - 0.23.1-4
- In proxy module don't call C_Finalize on a forked process [#1217915]
- Do not deinitialize libffi's wrapper functions [#1217915]

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.23.1-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Feb 20 2015 Stef Walter <stefw@redhat.com> - 0.23.1-1
- Update to 0.23.1 release

* Thu Oct 09 2014 Stef Walter <stefw@redhat.com> - 0.22.1-1
- Update to 0.22.1 release
- Use SubjectKeyIdentifier as a CKA_ID if possible rhbz#1148895

* Sat Oct 04 2014 Stef Walter <stefw@redhat.com> 0.22.0-1
- Update to 0.22.0 release

* Wed Sep 17 2014 Stef Walter <stefw@redhat.com> 0.21.3-1
- Update to 0.21.3 release
- Includes definitions for trust extensions rhbz#1136817

* Fri Sep 05 2014 Stef Walter <stefw@redhat.com> 0.21.2-1
- Update to 0.21.2 release
- Fix problems with erroneous messages printed rhbz#1133857

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 07 2014 Stef Walter <stefw@redhat.com> - 0.21.1-1
- Update to 0.21.1 release

* Wed Jul 30 2014 Tom Callaway <spot@fedoraproject.org> - 0.20.3-3
- fix license handling

* Fri Jul 04 2014 Stef Walter <stefw@redhat.com> - 0.20.3-2
- Update to stable 0.20.3 release

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.20.2-2
- Own the %%{_libdir}/pkcs11 dir in -trust.

* Tue Jan 14 2014 Stef Walter <stefw@redhat.com> - 0.20.2-1
- Update to upstream stable 0.20.2 release
- Fix regression involving blacklisted anchors [#1041328]
- Support ppc64le in build [#1052707]

* Mon Sep 09 2013 Stef Walter <stefw@redhat.com> - 0.20.1-1
- Update to upstream stable 0.20.1 release
- Extract compat trust data after we've changes
- Skip compat extraction if running as non-root
- Better failure messages when removing anchors

* Thu Aug 29 2013 Stef Walter <stefw@redhat.com> - 0.19.4-1
- Update to new upstream 0.19.4 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Stef Walter <stefw@redhat.com> - 0.19.3-1
- Update to new upstream 0.19.3 release (#967822)

* Wed Jun 05 2013 Stef Walter <stefw@redhat.com> - 0.18.3-1
- Update to new upstream stable release
- Fix intermittent firefox cert validation issues (#960230)
- Include the manual pages in the package

* Tue May 14 2013 Stef Walter <stefw@redhat.com> - 0.18.2-1
- Update to new upstream stable release
- Reduce the libtasn1 dependency minimum version

* Thu May 02 2013 Stef Walter <stefw@redhat.com> - 0.18.1-1
- Update to new upstream stable release
- 'p11-kit extract-trust' lives in libdir

* Thu Apr 04 2013 Stef Walter <stefw@redhat.com> - 0.18.0-1
- Update to new upstream stable release
- Various logging tweaks (#928914, #928750)
- Make the 'p11-kit extract-trust' explicitly reject
  additional arguments

* Thu Mar 28 2013 Stef Walter <stefw@redhat.com> - 0.17.5-1
- Make 'p11-kit extract-trust' call update-ca-trust
- Work around 32-bit oveflow of certificate dates
- Build fixes

* Tue Mar 26 2013 Stef Walter <stefw@redhat.com> - 0.17.4-2
- Pull in patch from upstream to fix build on ppc (#927394)

* Wed Mar 20 2013 Stef Walter <stefw@redhat.com> - 0.17.4-1
- Update to upstream version 0.17.4

* Mon Mar 18 2013 Stef Walter <stefw@redhat.com> - 0.17.3-1
- Update to upstream version 0.17.3
- Put the trust input paths in the right order

* Tue Mar 12 2013 Stef Walter <stefw@redhat.com> - 0.16.4-1
- Update to upstream version 0.16.4

* Fri Mar 08 2013 Stef Walter <stefw@redhat.com> - 0.16.3-1
- Update to upstream version 0.16.3
- Split out system trust module into its own package.
- p11-kit-trust provides an alternative to an nss module

* Tue Mar 05 2013 Stef Walter <stefw@redhat.com> - 0.16.1-1
- Update to upstream version 0.16.1
- Setup source directories as appropriate for Shared System Certificates feature

* Tue Mar 05 2013 Stef Walter <stefw@redhat.com> - 0.16.0-1
- Update to upstream version 0.16.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Kalev Lember <kalevlember@gmail.com> - 0.14-1
- Update to 0.14

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.13-1
- Update to 0.13

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 0.12-1
- Update to 0.12
- Run self tests in %%check

* Sat Feb 11 2012 Kalev Lember <kalevlember@gmail.com> - 0.11-1
- Update to 0.11

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 0.9-1
- Update to 0.9

* Wed Oct 26 2011 Kalev Lember <kalevlember@gmail.com> - 0.8-1
- Update to 0.8

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.6-1
- Update to 0.6

* Sun Sep 04 2011 Kalev Lember <kalevlember@gmail.com> - 0.5-1
- Update to 0.5

* Sun Aug 21 2011 Kalev Lember <kalevlember@gmail.com> - 0.4-1
- Update to 0.4
- Install the example config file to documentation directory

* Wed Aug 17 2011 Kalev Lember <kalevlember@gmail.com> - 0.3-2
- Tighten -devel subpackage deps (#725905)

* Fri Jul 29 2011 Kalev Lember <kalevlember@gmail.com> - 0.3-1
- Update to 0.3
- Upstream rewrote the ASL 2.0 bits, which makes the whole package
  BSD-licensed

* Tue Jul 12 2011 Kalev Lember <kalevlember@gmail.com> - 0.2-1
- Initial RPM release
