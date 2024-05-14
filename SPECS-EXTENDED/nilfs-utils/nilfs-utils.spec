Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global _root_libdir	/%{_lib}
%global _root_sbindir 	/sbin

Name:		nilfs-utils
Version:	2.2.8
Release:	3%{?dist}
Summary:	Utilities for managing NILFS v2 filesystems

License:	GPLv2+
URL:		https://nilfs.sourceforge.net
Source0:	https://nilfs.sourceforge.net/download/%{name}-%{version}.tar.bz2
BuildRequires:	gcc, libuuid-devel, libmount-devel

%description
Userspace utilities for creating and mounting NILFS v2 filesystems.

%package devel
Summary:	NILFS2 filesystem-specific headers
Requires:	nilfs-utils = %{version}-%{release}

%description devel
nilfs-utils-devel contains the header files needed to develop NILFS
filesystem-specific programs.

You should install nilfs-utils-devel if you want to develop NILFS
filesystem-specific programs. If you install nilfs-utils-devel, you'll
also want to install nilfs-utils.

%prep
%setup -q

%build
# geez, make install is trying to run ldconfig on the system
%configure LDCONFIG=/bin/true --disable-static --libdir %{_root_libdir}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_root_libdir}/libnilfs*.la

%ldconfig_scriptlets

%files
%doc COPYING ChangeLog
%config(noreplace) /etc/nilfs_cleanerd.conf
%{_root_sbindir}/mkfs.nilfs2
%{_root_sbindir}/mount.nilfs2
%{_root_sbindir}/nilfs_cleanerd
%{_root_sbindir}/umount.nilfs2
%{_sbindir}/nilfs-tune
%{_sbindir}/nilfs-clean
%{_sbindir}/nilfs-resize
%{_root_libdir}/libnilfscleaner.so.*
%{_root_libdir}/libnilfsgc.so.*
%{_bindir}/chcp
%{_bindir}/dumpseg
%{_bindir}/lscp
%{_bindir}/lssu
%{_bindir}/mkcp
%{_bindir}/rmcp
%{_mandir}/man1/lscp.1.gz
%{_mandir}/man1/lssu.1.gz
%{_mandir}/man5/nilfs_cleanerd.conf.5.gz
%{_mandir}/man8/chcp.8.gz
%{_mandir}/man8/dumpseg.8.gz
%{_mandir}/man8/mkcp.8.gz
%{_mandir}/man8/mkfs.nilfs2.8.gz
%{_mandir}/man8/mount.nilfs2.8.gz
%{_mandir}/man8/nilfs.8.gz
%{_mandir}/man8/nilfs_cleanerd.8.gz
%{_mandir}/man8/rmcp.8.gz
%{_mandir}/man8/umount.nilfs2.8.gz
%{_mandir}/man8/nilfs-tune.8.gz
%{_mandir}/man8/nilfs-clean.8.gz
%{_mandir}/man8/nilfs-resize.8.gz
%{_root_libdir}/libnilfs.so.*

%files devel
%{_root_libdir}/libnilfs.so
%{_root_libdir}/libnilfscleaner.so
%{_root_libdir}/libnilfsgc.so
%{_includedir}/nilfs.h
%{_includedir}/nilfs2_fs.h
%{_includedir}/nilfs_cleaner.h

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.8-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 20 2019 Eric Sandeen <sandeen@redhat.com> 2.2.8-1
- New upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 16 2018 Eric Sandeen <sandeen@redhat.com> 2.2.7-3
- BuildRequires: gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 06 2017 Eric Sandeen <sandeen@redhat.com> 2.2.7-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 11 2016 Eric Sandeen <sandeen@redhat.com> 2.2.6-1
- New upstream release

* Sun Sep 04 2016 Eric Sandeen <sandeen@redhat.com> 2.2.5-1
- New upstream release

* Wed Apr 27 2016 Eric Sandeen <sandeen@redhat.com> 2.2.4-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 17 2015 Eric Sandeen <sandeen@redhat.com> 2.2.3-1
- New upstream release

* Fri Sep 19 2014 Eric Sandeen <sandeen@redhat.com> 2.2.2-1
- New upstream release
- Update URLs in specfile

* Mon Aug 25 2014 Eric Sandeen <sandeen@redhat.com> 2.2.1-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Eric Sandeen <sandeen@redhat.com> 2.2.0-1
- New upstream release

* Thu Jan 30 2014 Eric Sandeen <sandeen@redhat.com> 2.1.6-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Eric Sandeen <sandeen@redhat.com> 2.1.5-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Eric Sandeen <sandeen@redhat.com> 2.1.4-1
- New upstream release

* Mon Jun 04 2012 Eric Sandeen <sandeen@redhat.com> 2.1.2-1
- New upstream release

* Mon Jan 16 2012 Eric Sandeen <sandeen@redhat.com> 2.1.1-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Eric Sandeen <sandeen@redhat.com> 2.1.0-2
- Fix up a couple packaging thinkos

* Mon Nov 28 2011 Eric Sandeen <sandeen@redhat.com> 2.1.0-1
- New upstream release

* Tue May 03 2011 Eric Sandeen <sandeen@redhat.com> 2.0.23-1
- New upstream release

* Tue Apr 19 2011 Eric Sandeen <sandeen@redhat.com> 2.0.22-1
- New upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Eric Sandeen <sandeen@redhat.com> 2.0.21-1
- New upstream release

* Mon Oct 04 2010 Eric Sandeen <sandeen@redhat.com> 2.0.20-1
- New upstream release

* Mon Aug 09 2010 Eric Sandeen <sandeen@redhat.com> 2.0.19-1
- New upstream release

* Mon Apr 12 2010 Eric Sandeen <sandeen@redhat.com> 2.0.18-1
- New upstream release

* Mon Mar 15 2010 Eric Sandeen <sandeen@redhat.com> 2.0.17-1
- New upstream release

* Sat Feb 13 2010 Eric Sandeen <sandeen@redhat.com> 2.0.15-2
- Fix stat header inclusion for FTBFS (#564788)

* Sun Jan 03 2010 Eric Sandeen <sandeen@redhat.com> 2.0.15-1
- New upstream release

* Thu Jul 30 2009 Eric Sandeen <sandeen@redhat.com> 2.0.14-2
- Fix libuuid-devel dep, fix odd chown in make install

* Wed Jul 29 2009 Eric Sandeen <sandeen@redhat.com> 2.0.14-1
- New upstream release

* Wed Jun 10 2009 Eric Sandeen <sandeen@redhat.com> 2.0.12-1
- Initial fedora package

