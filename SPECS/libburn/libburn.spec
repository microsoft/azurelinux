%global pkgname libburn

%global cdrskin cdrskin

Summary:         Library for reading, mastering and writing optical discs
Name:            libburn
Version:         1.5.6
Release:         1%{?dist}
License:         GPLv2+
Group:           System Environment/Libraries
URL:             https://dev.lovelyhq.com/libburnia/libburn
Source0:         https://dev.lovelyhq.com/libburnia/libburn/archive/release-%{version}.tar.gz#//%{pkgname}-%{version}.tar.gz
Patch0:          libburn-0.6.16-multilib.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  intltool
BuildRequires:  gettext

%description
Libburn is a library by which preformatted data get onto optical media:
CD, DVD and BD (Blu-Ray). It also offers a facility for reading data
blocks from its drives without using the normal block device I/O, which
has advantages and disadvantages. It seems appropriate, nevertheless,
to do writing and reading via same channel. On several Linux systems,
the block device driver needs reloading of the drive tray in order to
make available freshly written data. The libburn read function does not
need such a reload. The code of libburn is independent of cdrecord.

%package         devel
Summary:         Development files for %{name}
Group:           Development/Libraries
Requires:        %{name}%{?_isa} = %{version}-%{release}, pkg-config

%description     devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n      %{cdrskin}
Summary:         Limited cdrecord compatibility wrapper to ease migration to %{name}
Group:           Applications/Multimedia
Requires:        %{name}%{?_isa} = %{version}-%{release}

%description -n %{cdrskin}
A limited cdrecord compatibility wrapper which allows to use some %{name}
features from the command line.

%prep
%setup -q -n %{pkgname}
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
%{_includedir}/%{name}
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%files -n %{cdrskin}
%{_bindir}/%{cdrskin}
%{_mandir}/man1/%{cdrskin}.1*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.6-1
- Auto-upgrade to 1.5.6 - Azure Linux 3.0 - package upgrades

* Mon Mar 14 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.5.4-1
- Upgrade to 1.5.4.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.8-3
- Removing the explicit %%clean stage.
- License verified.

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.4.8-2
- Initial CBL-Mariner import from Fedora 27 (license: MIT).

* Fri Sep 15 2017 Robert Scheck <robert@fedoraproject.org> 1.4.8-1
- Upgrade to 1.4.8 (#1491478)

* Thu Aug 24 2017 Robert Scheck <robert@fedoraproject.org> 1.4.6-5
- Move large documentation into -doc subpackage (#750009)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Sep 18 2016 Robert Scheck <robert@fedoraproject.org> 1.4.6-1
- Update to upstream 1.4.6 (#1377006)

* Tue Jul 05 2016 Robert Scheck <robert@fedoraproject.org> 1.4.4-1
- Update to upstream 1.4.4 (#1352496)
- Reworked spec file to build libburn1 for RHEL >= 6 (#750009)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Robert Scheck <robert@fedoraproject.org> 1.4.2-2
- Update to upstream 1.4.2.pl01 (#1294947)

* Thu Dec 24 2015 Robert Scheck <robert@fedoraproject.org> 1.4.2-1
- Update to upstream 1.4.2 (#1287345)
- Add symlink handling via alternatives for cdrecord (#1256240)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Robert Scheck <robert@fedoraproject.org> 1.4.0-1
- Update to upstream 1.4.0 (#1222524)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 29 2014 Robert Scheck <robert@fedoraproject.org> 1.3.8-1
- Update to upstream 1.3.8 (#1078717)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Robert Scheck <robert@fedoraproject.org> 1.3.6-1
- Update to upstream 1.3.6 (#1072835)

* Sat Dec 14 2013 Robert Scheck <robert@fedoraproject.org> 1.3.4-1
- Update to upstream 1.3.4 (#1043068)

* Sun Aug 25 2013 Robert Scheck <robert@fedoraproject.org> 1.3.2-1
- Update to upstream 1.3.2 (#994916)

* Sat Aug 03 2013 Robert Scheck <robert@fedoraproject.org> 1.3.0-1
- Update to upstream 1.3.0 (#965231)
- Run autoreconf to recognize aarch64 (#925679)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.8-2
- Run autoreconf to overwrite old scripts => recognize aarch64

* Tue Mar 19 2013 Robert Scheck <robert@fedoraproject.org> 1.2.8-1
- Update to upstream 1.2.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 12 2013 Robert Scheck <robert@fedoraproject.org> 1.2.6-1
- Update to upstream 1.2.6 (#893692)

* Wed Dec 05 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.4-5
- renamed patch - added package name to match naming guidelines

* Tue Dec 04 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.4-4
- current time in doxygen footer caused multilib difference - inserted empty footer instead

* Thu Nov 22 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.4-3
- Minor spec-file cleanup

* Wed Aug 29 2012 Honza Horak <hhorak@redhat.com> 1.2.4-2
- Changed license from GPLv2 to GPLv2+ to correspond with source

* Fri Aug 10 2012 Robert Scheck <robert@fedoraproject.org> 1.2.4-1
- Update to upstream 1.2.4 (#842077)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 13 2012 Robert Scheck <robert@fedoraproject.org> 1.2.2-1
- Update to upstream 1.2.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Robert Scheck <robert@fedoraproject.org> 1.1.8-1
- Update to upstream 1.1.8

* Sat Oct 08 2011 Robert Scheck <robert@fedoraproject.org> 1.1.6-1
- Update to upstream 1.1.6

* Sun Sep 18 2011 Robert Scheck <robert@fedoraproject.org> 1.1.4-1
- Update to upstream 1.1.4

* Sun Jul 10 2011 Robert Scheck <robert@fedoraproject.org> 1.1.0-1
- Update to upstream 1.1.0

* Sun Apr 17 2011 Robert Scheck <robert@fedoraproject.org> 1.0.6-1
- Update to upstream 1.0.6

* Mon Feb 28 2011 Honza Horak <hhorak@redhat.com> - 1.0.2-1
- Update to upstream 1.0.2

* Thu Feb 17 2011 Honza Horak <hhorak@redhat.com> - 1.0.0-1
- Update to upstream 1.0.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 22 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 0.8.0-1
- Update to upstream 0.8.0

* Wed Sep 30 2009 Denis Leroy <denis@poolshark.org> - 0.7.0-1
- Update to upstream 0.7.0
- Fixed binary installation
- Removed rpath

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Denis Leroy <denis@poolshark.org> - 0.6.0-2
- Updating to pl01 tarball from upstream
- Fixed project URL

* Wed Jan 07 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.0-1
- New upstream version

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4.8-2
- fix license tag

* Wed Jun 11 2008 Denis Leroy <denis@poolshark.org> - 0.4.8-1
- Update to upstream 0.4.8

* Thu Feb 14 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-2
- Autorebuild for GCC 4.3

* Thu Dec 13 2007 Denis Leroy <denis@poolshark.org> - 0.4.0-1
- Update to 0.4.0

* Wed Oct 10 2007 Jesse Keating <jkeating@redhat.com> - 0.3.8-2
- Rebuild for BuildID

* Fri Aug 10 2007 Denis Leroy <denis@poolshark.org> - 0.3.8-1
- Update to upstream 0.3.8
- Fixed project URL

* Sun Mar 25 2007 Denis Leroy <denis@poolshark.org> - 0.2.6.3-3
- Fixed unowned include directory (#233860)

* Tue Mar 20 2007 Denis Leroy <denis@poolshark.org> - 0.2.6.3-2
- Moved documentation into devel package, #228372
- Updated source URL to new upstream location

* Tue Jan 02 2007 Jesse Keating <jkeating@redhat.com> - 0.2.6.3-1
- Update to 0.2.6.3
- Remove libisofs stuff as it's packaged seperately now.
- Add a manpage for cdrskin

* Sat Oct 21 2006 Jesse Keating <jkeating@redhat.com> - 0.2-2-2
- Point to a real URL in source, now that we have a tarball

* Fri Oct 20 2006 Jesse Keating <jkeating@redhat.com> - 0.2-2-1
- 0.2.2 release

* Tue Sep 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2-5.20060808svn
- Create doxygen docs

* Fri Sep  8 2006 Jesse Keating <jkeating@redhat.com> - 0.2-4.20060808svn
- rebuild with new snapshot

* Sun Aug 27 2006 Jesse Keating <jkeating@redhat.com> - 0.2-3.20060823svn
- don't install dupe headers in -devel packages
- libisofs requires libburn devel for directory ownership

* Sun Aug 27 2006 Jesse Keating <jkeating@redhat.com> - 0.2-2.20060823svn
- Fix cdrskin require
- Fix tabs
- Added doc files

* Wed Aug 23 2006 Jesse Keating <jkeating@redhat.com> - 0.2-1.20060823svn
- Initial package for review
