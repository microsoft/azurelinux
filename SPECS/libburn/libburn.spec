# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname libburn

Summary:         Library for reading, mastering and writing optical discs
Name:            libburn
Version:         1.5.6
Release:         8%{?dist}
License:         GPL-2.0-or-later
URL:             https://libburnia-project.org/
Source0:         https://files.libburnia-project.org/releases/%{pkgname}-%{version}.tar.gz
Source1:         https://files.libburnia-project.org/releases/%{pkgname}-%{version}.tar.gz.sig
Source2:         https://keys.openpgp.org/vks/v1/by-fingerprint/44BC9FD0D688EB007C4DD029E9CBDFC0ABC0A854
Patch0:          libburn-0.6.16-multilib.patch
Patch1:          libburn-1.5.4-rpath.patch
Patch2:          https://dev.lovelyhq.com/libburnia/libburn/commit/d537f9dd35282df834a311ead5f113af67d223b3.patch#/libburn-1.5.6-c23.patch
BuildRequires:   gnupg2
BuildRequires:   gcc, make, intltool, gettext
%if 0%{?rhel} && "%{name}" != "%{pkgname}"
BuildRequires:   autoconf, automake, libtool, pkgconfig
%global variant 1
%endif

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
Requires:        %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description     devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if 0%{!?_without_doc:1}
%package doc
Summary:         Documentation files for %{name}
BuildArch:       noarch
BuildRequires:   doxygen, graphviz

%description doc
Libburn is a library by which preformatted data get onto optical media:
CD, DVD and BD (Blu-Ray). This package contains the API documentation
for developing applications that use %{name}.
%endif

%package -n      cdrskin%{?variant}
Summary:         Limited cdrecord compatibility wrapper to ease migration to %{name}
Requires:        %{name}%{?_isa} = %{version}-%{release}
Requires(post):  %{?el8:/usr/sbin/}alternatives, coreutils
Requires(preun): %{?el8:/usr/sbin/}alternatives

%description -n cdrskin%{?variant}
A limited cdrecord compatibility wrapper which allows to use some %{name}
features from the command line.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n %{pkgname}-%{version}

# Rename from libburn to libburn1 for EPEL
%if 0%{?rhel} && "%{name}" != "%{pkgname}"
sed -e 's@libburn_libburn@libburn_libburn1@g' \
    -e 's@libburn/libburn.la@libburn/libburn1.la@g' \
    -e 's@(includedir)/libburn@(includedir)/libburn1@g' \
    -e 's@libburn-1.pc@libburn1-1.pc@g' -i Makefile.am
sed -e 's@libburn-1.pc@libburn1-1.pc@g' -i configure.ac
sed -e 's@burn@burn1@g' libburn-1.pc.in > libburn1-1.pc.in

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

# RHEL ships a cdrskin package already
%if 0%{?rhel} && "%{name}" != "%{pkgname}"
mv -f $RPM_BUILD_ROOT%{_bindir}/cdrskin{,%{?variant}}
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/cdrskin{,%{?variant}}.1
%endif

# Prepare alternatives handling for cdrecord -> cdrskin
touch $RPM_BUILD_ROOT{%{_bindir}/cdrecord,%{_mandir}/man1/cdrecord.1.gz}

%ldconfig_scriptlets

%post -n cdrskin%{?variant}
alternatives --install %{_bindir}/cdrecord cdrecord %{_bindir}/cdrskin%{?variant} 50 \
  --slave %{_mandir}/man1/cdrecord.1.gz cdrecord-cdrecordman %{_mandir}/man1/cdrskin%{?variant}.1.gz

%preun -n cdrskin%{?variant}
if [ $1 -eq 0 ]; then
  alternatives --remove cdrecord %{_bindir}/cdrskin%{?variant}
fi

%files
%license COPYING
%doc AUTHORS COPYRIGHT README
%{_libdir}/%{name}*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%if 0%{!?_without_doc:1}
%files doc
%doc doc/html/
%endif

%files -n cdrskin%{?variant}
%ghost %{_bindir}/cdrecord
%{_bindir}/cdrskin%{?variant}
%ghost %{_mandir}/man1/cdrecord.1*
%{_mandir}/man1/cdrskin%{?variant}.1*

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
- Upgrade to 1.5.6 (#2216132)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 09 2021 Robert Scheck <robert@fedoraproject.org> 1.5.4-2
- Correct alternatives handling for cdrecord man page

* Mon Feb 08 2021 Robert Scheck <robert@fedoraproject.org> 1.5.4-1
- Upgrade to 1.5.4 (#1926008)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 28 2020 Robert Scheck <robert@fedoraproject.org> 1.5.2-4
- Upgrade to 1.5.2.pl01 (#1776514)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 27 2019 Robert Scheck <robert@fedoraproject.org> 1.5.2-1
- Upgrade to 1.5.2 (#1765953)

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
