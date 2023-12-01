Summary:        Library to enable creation and expansion of ISO-9660 filesystems
Name:           libisoburn
Version:        1.5.4
Release:        3%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://dev.lovelyhq.com/libburnia/libisoburn
Source0:        https://dev.lovelyhq.com/libburnia/libisoburn/archive/release-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         libisoburn-1.0.8-multilib.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  libacl-devel
BuildRequires:  libburn-devel >= %{version}
BuildRequires:  libisofs-devel >= %{version}
BuildRequires:	make
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
%if %{with_check}
BuildRequires:  file
BuildRequires:  which
%endif

%description
Libisoburn is a front-end for libraries libburn and libisofs which
enables creation and expansion of ISO-9660 filesystems on all CD/
DVD/BD media supported by libburn. This includes media like DVD+RW,
which do not support multi-session management on media level and
even plain disk files or block devices. Price for that is thorough
specialization on data files in ISO-9660 filesystem images. And so
libisoburn is not suitable for audio (CD-DA) or any other CD layout
which does not entirely consist of ISO-9660 sessions.

%package devel
Summary:        Development files for libisoburn
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkg-config

%description devel
The libisoburn-devel package contains libraries and header files for
developing applications that use libisoburn.

%package -n xorriso
Summary:        ISO-9660 and Rock Ridge image manipulation tool
Group:          Applications/Archiving
URL:            http://scdbackup.sourceforge.net/xorriso_eng.html
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n xorriso
Xorriso is a program which copies file objects from POSIX compliant
filesystems into Rock Ridge enhanced ISO-9660 filesystems and allows
session-wise manipulation of such filesystems. It can load management
information of existing ISO images and it writes the session results
to optical media or to filesystem objects. Vice versa xorriso is able
to copy file objects out of ISO-9660 filesystems.

Filesystem manipulation capabilities surpass those of mkisofs. Xorriso
is especially suitable for backups, because of its high fidelity of
file attribute recording and its incremental update sessions. Optical
supported media: CD-R, CD-RW, DVD-R, DVD-RW, DVD+R, DVD+R DL, DVD+RW,
DVD-RAM, BD-R and BD-RE.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .multilib

libtoolize --force
autoreconf --force --install

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL='install -p' install

# Don't install any libtool .la files
rm -f %{buildroot}%{_libdir}/%{name}.la

# Clean up for later usage in documentation
rm -rf %{buildroot}%{_defaultdocdir}

# Some file cleanups
rm -f %{buildroot}%{_infodir}/dir

# Don't ship proof of concept for the moment
rm -f %{buildroot}%{_bindir}/xorriso-tcltk

%check
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{buildroot}%{_libdir}"
cd releng
./run_all_auto -x ../xorriso/xorriso || (cat releng_generated_data/log.*; false)

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS COPYRIGHT README ChangeLog
%{_libdir}/%{name}*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}*.pc

%files -n xorriso
%{_bindir}/osirrox
%{_bindir}/xorrecord
%{_bindir}/xorriso
%{_bindir}/xorrisofs
%{_bindir}/xorriso-dd-target
%{_mandir}/man1/xorrecord.1*
%{_mandir}/man1/xorriso*.1*
%{_infodir}/xorrecord.info*
%{_infodir}/xorriso*.info*

%changelog
* Tue Sep 26 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.4-3
- Removing 'exit' calls from the '%%check' section.

* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.4-2
- Fixing a typo in the source URL.

* Mon Mar 14 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.5.4-1
- Upgrade to 1.5.4.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.8-4
- Removing the explicit %%clean stage.
- License verified.

* Mon Jan 04 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.4.8-3
- Add BRs for check section

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.4.8-2
- Initial CBL-Mariner import from Fedora 27 (license: MIT).

* Fri Sep 15 2017 Robert Scheck <robert@fedoraproject.org> - 1.4.8-1
- Upgrade to 1.4.8 (#1491482)

* Thu Aug 24 2017 Robert Scheck <robert@fedoraproject.org> - 1.4.6-7
- Move large documentation into -doc subpackage

* Sun Aug 13 2017 Robert Scheck <robert@fedoraproject.org> - 1.4.6-6
- Added upstream patch to avoid %%check failure due to tput error

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.4.6-2
- Rebuild for readline 7.x

* Sun Sep 18 2016 Robert Scheck <robert@fedoraproject.org> - 1.4.6-1
- Upgrade to 1.4.6 (#1377002)

* Tue Jul 05 2016 Robert Scheck <robert@fedoraproject.org> - 1.4.4-1
- Upgrade to 1.4.4 (#1352345)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 24 2015 Robert Scheck <robert@fedoraproject.org> - 1.4.2-1
- Upgrade to 1.4.2 (#1287353)
- Add symlink handling via alternatives for mkisofs (#1256240)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Robert Scheck <robert@fedoraproject.org> - 1.4.0-1
- Upgrade to 1.4.0 (#1222525)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 29 2014 Robert Scheck <robert@fedoraproject.org> - 1.3.8-1
- Upgrade to 1.3.8 (#1078719)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Robert Scheck <robert@fedoraproject.org> - 1.3.6-1
- Upgrade to 1.3.6 (#1072838)

* Sat Dec 14 2013 Robert Scheck <robert@fedoraproject.org> - 1.3.4-1
- Upgrade to 1.3.4 (#1043070)

* Sun Aug 25 2013 Robert Scheck <robert@fedoraproject.org> - 1.3.2-1
- Upgrade to 1.3.2 (#994920)

* Sat Aug 03 2013 Robert Scheck <robert@fedoraproject.org> - 1.3.0-1
- Upgrade to 1.3.0 (#965233)
- Run autoreconf to recognize aarch64

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Robert Scheck <robert@fedoraproject.org> - 1.2.8-1
- Upgrade to 1.2.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 12 2013 Robert Scheck <robert@fedoraproject.org> - 1.2.6-1
- Upgrade to 1.2.6 (#893693)

* Sat Aug 11 2012 Robert Scheck <robert@fedoraproject.org> - 1.2.4-1
- Upgrade to 1.2.4 (#842078)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 13 2012 Robert Scheck <robert@fedoraproject.org> - 1.2.2-1
- Upgrade to 1.2.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Robert Scheck <robert@fedoraproject.org> - 1.1.8-1
- Upgrade to 1.1.8

* Sun Oct 09 2011 Robert Scheck <robert@fedoraproject.org> - 1.1.6-1
- Upgrade to 1.1.6

* Sun Jul 10 2011 Robert Scheck <robert@fedoraproject.org> - 1.1.2-1
- Upgrade to 1.1.2

* Mon May 02 2011 Robert Scheck <robert@fedoraproject.org> - 1.0.8-2
- Added forgotten documentation files to %%files (#697326 #c1)

* Sun Apr 17 2011 Robert Scheck <robert@fedoraproject.org> - 1.0.8-1
- Upgrade to 1.0.8
- Initial spec file for Fedora and Red Hat Enterprise Linux
