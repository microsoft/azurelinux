Summary:        Contains the utilities for the ext2 file system
Name:           e2fsprogs
Version:        1.47.0
Release:        1%{?dist}
License:        GPLv2 AND LGPLv2 AND BSD AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            http://e2fsprogs.sourceforge.net
Source0:        https://prdownloads.sourceforge.net/e2fsprogs/%{name}-%{version}.tar.gz
Requires:       %{name}-libs = %{version}-%{release}
Conflicts:      toybox

%description
The E2fsprogs package contains the utilities for handling the ext2 file system.

%package    libs
Summary:        contains libraries used by other packages

%description    libs
It contains the libraries: libss and libcom_err

%package    devel
Summary:        Header and development files for e2fsprogs
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%package lang
Summary:        Additional language files for e2fsprogs
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description lang
These are the additional language files of e2fsprogs

%prep
%autosetup -p1
sed -i -e 's|^LD_LIBRARY_PATH.*|&:/tools/lib|' tests/test_config

%build
LIBS=-L/tools/lib \
CFLAGS="%{build_cflags} -I/tools/include" \
PKG_CONFIG_PATH=/tools/lib/pkgconfig \
%configure \
    --with-root-prefix='' \
    --enable-elf-shlibs \
    --disable-libblkid \
    --disable-libuuid \
    --disable-uuidd \
    --disable-fsck \
    --disable-silent-rules \
    --enable-symlink-install
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-libs
chmod -v u+w %{buildroot}/%{_libdir}/{libcom_err,libe2p,libext2fs,libss}.a
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
# Multi-threaded runs are flaky.
make -j1 check
test_status=$?

for failed_test in $(find tests -name "*.failed")
do
    cat << EOF
"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
"Log '$failed_test':"
"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
EOF
    cat $failed_test
done

# Last command's status is how we determine if the tests failed or not.
[[ $test_status -eq 0 ]]

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license NOTICE
%config %{_sysconfdir}/e2scrub.conf
%config %{_sysconfdir}/mke2fs.conf
%{_bindir}/compile_et
%{_bindir}/mk_cmds
%{_bindir}/chattr
%{_bindir}/lsattr
%{_libdir}/e2initrd_helper
%{_datadir}/ss/ct_c.awk
%{_datadir}/ss/ct_c.sed
%{_datadir}/et/et_h.awk
%{_datadir}/et/et_c.awk
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_sbindir}/*
%{_libdir}/libext2fs.so.2.4
%{_libdir}/libe2p.so.2.3
%{_libdir}/libe2p.so.2
%{_libdir}/libext2fs.so.2
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.so

%files libs
%{_libdir}/libss.so
%{_libdir}/libss.so.*
%{_libdir}/libcom_err.so*

%files devel
%{_includedir}/ss/ss_err.h
%{_includedir}/ss/ss.h
%{_includedir}/et/com_err.h
%{_includedir}/ext2fs/ext2_io.h
%{_includedir}/ext2fs/ext2_fs.h
%{_includedir}/ext2fs/tdb.h
%{_includedir}/ext2fs/qcow2.h
%{_includedir}/ext2fs/bitops.h
%{_includedir}/ext2fs/ext2_err.h
%{_includedir}/ext2fs/ext2fs.h
%{_includedir}/ext2fs/ext3_extents.h
%{_includedir}/ext2fs/ext2_types.h
%{_includedir}/ext2fs/ext2_ext_attr.h
%{_includedir}/ext2fs/hashmap.h
%{_includedir}/e2p/e2p.h
%{_includedir}/com_err.h
%{_libdir}/libcom_err.a
%{_libdir}/libss.a
%{_libdir}/pkgconfig/ss.pc
%{_libdir}/pkgconfig/ext2fs.pc
%{_libdir}/pkgconfig/com_err.pc
%{_libdir}/pkgconfig/e2p.pc
%{_libdir}/libe2p.a
%{_libdir}/libext2fs.a
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Tue Nov 28 2023 Andrew Phelps <anphel@microsoft.com> - 1.47.0-1
- Upgrade to 1.47.0

* Thu Aug 11 2022 Muhammad Falak <mwani@microsoft.com> - 1.46.5-3
- Switch to `%autosetup` instead of `%setup`
- Patch CVE-2022-1304

* Mon Jul 18 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.46.5-2
- Running package tests in a single thread and printing logs for failures.

* Mon Feb 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.46.5-1
- Bump version to 1.46.5 to enable ptest

* Sat Nov 20 2021 Chris Co <chrco@microsoft.com> - 1.46.4-1
- Update to version 1.46.4

* Wed Jan 13 2021 Daniel McIlvaney <damcilva@microsoft.com> - 1.45.6-1
- Upgrade to version 1.45.6

* Fri Jul 31 2020 Leandro Pereira <leperei@microsoft.com> - 1.44.6-3
- Don't stomp on CFLAGS.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.44.6-2
- Added %%license line automatically

* Thu Mar 19 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.44.6-1
- Update version to 1.44.6. License verified.

* Tue Oct 01 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.44.3-4
- Fix libs file list removing static libraries.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.44.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 1.44.3-2
- Add conflicts toybox.

* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.44.3-1
- Version update to fix compilation issue againts glibc-2.28.

* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 1.43.4-2
- Add lang package.

* Mon Apr 03 2017 Chang Lee <changlee@vmware.com> 1.43.4-1
- Updated to version 1.43.4.

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.42.13-5
- Moved man3 to devel subpackage.

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.42.13-4
- Create libs subpackage for krb5.

* Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.42.13-3
- Use symlinks - save a diskspace.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.42.13-2
- GA - Bump release of all rpms.

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 1.42.13-1
- Updated to version 1.42.13.

* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.42.9-4
- Edit post script.

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.42.9-3
- Handled locale files with macro find_lang.

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.42.9-2
- Update according to UsrMove.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.42.9-1
- Initial build First version.
