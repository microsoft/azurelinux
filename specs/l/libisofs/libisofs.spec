# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname libisofs

Summary:        Library to create ISO 9660 disk images
Name:           libisofs
Version:        1.5.6
Release: 9%{?dist}
# libisofs/make_isohybrid_mbr.c is LGPL-2.0-or-later, rest is GPL-2.0-or-later
License:        GPL-2.0-or-later AND LGPL-2.0-or-later
URL:            https://libburnia-project.org/
Source0:        https://files.libburnia-project.org/releases/%{pkgname}-%{version}.tar.gz
Source1:        https://files.libburnia-project.org/releases/%{pkgname}-%{version}.tar.gz.sig
Source2:        https://keys.openpgp.org/vks/v1/by-fingerprint/44BC9FD0D688EB007C4DD029E9CBDFC0ABC0A854
Patch0:         libisofs-0.6.16-multilib.patch
Patch1:         libisofs-1.5.4-rpath.patch
BuildRequires:  gnupg2
BuildRequires:  gcc, make, libacl-devel, zlib-devel
%if 0%{?rhel} && "%{name}" != "%{pkgname}"
BuildRequires:  autoconf, automake, libtool
%endif

%description
Libisofs is a library to create an ISO-9660 filesystem and supports
extensions like RockRidge or Joliet. It is also a full featured
ISO-9660 editor, allowing you to modify an ISO image or multisession
disc, including file addition or removal, change of file names and
attributes etc. It supports the extension AAIP which allows to store
ACLs and xattr in ISO-9660 filesystems as well. As it is linked with
zlib, it supports zisofs compression, too.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if 0%{!?_without_doc:1}
%package doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
BuildRequires:  doxygen, graphviz

%description doc
Libisofs is a library to create an ISO-9660 filesystem and supports
extensions like RockRidge or Joliet. This package contains the API
documentation for developing applications that use %{name}.
%endif

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1 -b .multilib
%patch -P1 -p1 -b .rpath

# Rename from libisofs to libisofs1 for EPEL
%if 0%{?rhel} && "%{name}" != "%{pkgname}"
sed -e 's@libisofs_libisofs@libisofs_libisofs1@g' \
    -e 's@libisofs/libisofs.la@libisofs/libisofs1.la@g' \
    -e 's@(includedir)/libisofs@(includedir)/libisofs1@g' \
    -e 's@libisofs-1.pc@libisofs1-1.pc@g' -i Makefile.am
sed -e 's@libisofs-1.pc@libisofs1-1.pc@g' -i configure.ac
sed -e 's@isofs@isofs1@g' libisofs-1.pc.in > libisofs1-1.pc.in

libtoolize --force
autoreconf --force --install
%endif

%build
%configure --disable-static
%make_build
%{!?_without_doc:doxygen doc/doxygen.conf}

%install
%make_install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

# Clean up for later usage in documentation
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS COPYRIGHT README
%{_libdir}/%{name}*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}*.pc

%if 0%{!?_without_doc:1}
%files doc
%doc doc/html/
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 20 2023 Robert Scheck <robert@fedoraproject.org> 1.5.6-1
- Upgrade to 1.5.6 (#2216133)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 08 2021 Robert Scheck <robert@fedoraproject.org> 1.5.4-1
- Upgrade to 1.5.4 (#1926007)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 27 2019 Robert Scheck <robert@fedoraproject.org> 1.5.2-1
- Upgrade to 1.5.2 (#1765955)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 08 2018 Robert Scheck <robert@fedoraproject.org> 1.5.0-1
- Upgrade to 1.5.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 01 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.4.8-2
- Cleanup spec file conditionals

* Fri Sep 15 2017 Robert Scheck <robert@fedoraproject.org> 1.4.8-1
- Upgrade to 1.4.8 (#1491483)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Sep 18 2016 Robert Scheck <robert@fedoraproject.org> 1.4.6-1
- Upgrade to 1.4.6 (#1377003)

* Tue Jul 05 2016 Robert Scheck <robert@fedoraproject.org> 1.4.4-1
- Upgrade to 1.4.4 (#1352346)

* Sat Apr 30 2016 Robert Scheck <robert@fedoraproject.org> 1.4.2-3
- Move large documentation into -doc subpackage (#744416)
- Reworked spec file to build libisofs1 for RHEL >= 6 (#744416)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 24 2015 Robert Scheck <robert@fedoraproject.org> 1.4.2-1
- Upgrade to 1.4.2 (#1287354)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Robert Scheck <robert@fedoraproject.org> 1.4.0-1
- Upgrade to 1.4.0 (#1222526)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 29 2014 Robert Scheck <robert@fedoraproject.org> 1.3.8-1
- Upgrade to 1.3.8 (#1114299)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Robert Scheck <robert@fedoraproject.org> 1.3.6-1
- Upgrade to 1.3.6 (#1072839)

* Sat Dec 14 2013 Robert Scheck <robert@fedoraproject.org> 1.3.4-1
- Upgrade to 1.3.4 (#1043071)

* Sun Aug 25 2013 Robert Scheck <robert@fedoraproject.org> 1.3.2-1
- Upgrade to 1.3.2 (#994921)

* Sat Aug 03 2013 Robert Scheck <robert@fedoraproject.org> 1.3.0-1
- Upgrade to 1.3.0 (#965234, #976945)
- Run autoreconf to recognize aarch64 (#925783)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 1.2.8-2
- Don't ship api docs twice (they were included in both
  the main and the devel package, by accident (need to save
  space on the f19 live images)

* Tue Mar 19 2013 Robert Scheck <robert@fedoraproject.org> 1.2.8-1
- Upgrade to 1.2.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 12 2013 Robert Scheck <robert@fedoraproject.org> 1.2.6-1
- Upgrade to 1.2.6 (#893694)

* Wed Aug 29 2012 Honza Horak <hhorak@redhat.com> 1.2.4-2
- Changed license from GPLv2 to GPLv2+ to correspond with source
- Added license LGPLv2+ due to make_isohybrid_mbr.c

* Fri Aug 10 2012 Robert Scheck <robert@fedoraproject.org> 1.2.4-1
- Upgrade to 1.2.4 (#842079)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 13 2012 Robert Scheck <robert@fedoraproject.org> 1.2.2-1
- Upgrade to 1.2.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Robert Scheck <robert@fedoraproject.org> 1.1.6-1
- Upgrade to 1.1.6

* Sun Sep 18 2011 Robert Scheck <robert@fedoraproject.org> 1.1.4-1
- Upgrade to 1.1.4

* Sun Jul 10 2011 Robert Scheck <robert@fedoraproject.org> 1.1.2-1
- Upgrade to 1.1.2

* Tue May 17 2011 Robert Scheck <robert@fedoraproject.org> 1.0.8-1
- Upgrade to 1.0.8

* Sun Apr 10 2011 Robert Scheck <robert@fedoraproject.org> 1.0.6-1
- Upgrade to 1.0.6

* Tue Mar 15 2011 Robert Scheck <robert@fedoraproject.org> 1.0.4-1
- Upgrade to 1.0.4

* Mon Feb 28 2011 Robert Scheck <robert@fedoraproject.org> 1.0.2-1
- Upgrade to 1.0.2

* Thu Feb 17 2011 Honza Horak <hhorak@redhat.com> - 1.0.0-1
- Update to upstream 1.0.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Robert Scheck <robert@fedoraproject.org> 0.6.40-1
- Upgrade to 0.6.40

* Sun Oct 31 2010 Robert Scheck <robert@fedoraproject.org> 0.6.38-1
- Upgrade to 0.6.38

* Sun Jul 04 2010 Robert Scheck <robert@fedoraproject.org> 0.6.34-1
- Upgrade to 0.6.34

* Fri May 14 2010 Robert Scheck <robert@fedoraproject.org> 0.6.32-1
- Upgrade to 0.6.32

* Sat Apr 17 2010 Robert Scheck <robert@fedoraproject.org> 0.6.30-1
- Upgrade to 0.6.30

* Tue Feb 16 2010 Robert Scheck <robert@fedoraproject.org> 0.6.28-1
- Upgrade to 0.6.28

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Robert Scheck <robert@fedoraproject.org> 0.6.20-1
- Upgrade to 0.6.20

* Tue Mar 17 2009 Robert Scheck <robert@fedoraproject.org> 0.6.16-1
- Upgrade to 0.6.16
- Several spec file cleanups and solved the multilib issues

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Denis Leroy <denis@poolshark.org> - 0.6.12-1
- Update to 0.6.12 upstream version

* Wed Aug  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.6-2
- fix license tag

* Wed Jun 11 2008 Denis Leroy <denis@poolshark.org> - 0.6.6-1
- Update to upstream 0.6.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.8-3
- Autorebuild for GCC 4.3

* Wed Oct 10 2007 Jesse Keating <jkeating@redhat.com> - 0.2.8-2
- Rebuild for BuildID

* Fri Aug 10 2007 Denis Leroy <denis@poolshark.org> - 0.2.8-1
- Update to 0.2.8
- Fixed Source URL

* Mon Jan 08 2007 Jesse Keating <jkeating@redhat.com> - 0.2.4-2
- Move html docs to -devel
- Change urls to new upstream location

* Wed Jan 03 2007 Jesse Keating <jkeating@redhat.com> - 0.2.4-1
- New upstream release to fix some issues

* Tue Jan 02 2007 Jesse Keating <jkeating@redhat.com> - 0.2.3-2
- Fix some issues brought up during review

* Tue Jan 02 2007 Jesse Keating <jkeating@redhat.com> - 0.2.3-1
- Initial release split off of libburn package.
- Disable docs for now, will be fixed in future upstream release
