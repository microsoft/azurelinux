Summary:  Library to create ISO 9660 disk images
Name:     libisofs
Version:  1.5.4
Release:  1%{?dist}
# make_isohybrid_mbr.c is under LGPLv2+, the rest under GPLv2+
License:  GPLv2+ and LGPLv2+
Group:    System Environment/Libraries
URL:      https://dev.lovelyhq.com/libburnia/libisofs
Source0:  https://dev.lovelyhq.com/libburnia/libisofs/archive/release-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:   libisofs-0.6.16-multilib.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  libacl-devel
BuildRequires:  make
BuildRequires:  zlib-devel

%description
Libisofs is a library to create an ISO-9660 filesystem and supports
extensions like RockRidge or Joliet. It is also a full featured
ISO-9660 editor, allowing you to modify an ISO image or multisession
disc, including file addition or removal, change of file names and
attributes etc. It supports the extension AAIP which allows to store
ACLs and xattr in ISO-9660 filesystems as well. As it is linked with
zlib, it supports zisofs compression, too.

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}, pkg-config

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .multilib

libtoolize --force
autoreconf --force --install

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

# Clean up for later usage in documentation
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS COPYRIGHT README
%{_libdir}/%{name}*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}*.pc

%changelog
* Mon Mar 14 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.5.4-1
- Upgrade to 1.5.4.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.8-3
- Removing the explicit %%clean stage.
- License verified.

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.4.8-2
- Initial CBL-Mariner import from Fedora 27 (license: MIT).

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
