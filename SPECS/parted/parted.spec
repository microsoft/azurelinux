Summary:        GNU Parted manipulates partition tables
Name:           parted
Version:        3.4
Release:        99%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.gnu.org/software/parted/
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
# Upstream patches since v3.4 release
Patch0: 0001-parted-add-fix-to-fix-in-script-mode.patch
Patch1: 0002-doc-Document-fix-flag.patch
Patch2: 0003-tests-Add-tests-for-fix.patch
Patch3: 0004-tests-Fix-test-t1700-probe-fs.patch
Patch4: 0005-tests-Fix-t9041-undetected-in-use-16th-partition.patch
Patch5: 0006-libparted-Fix-fd-check-in-_flush_cache.patch
Patch6: 0007-libparted-Fix-potential-memory-leak-in-sdmmc_get_pro.patch
Patch7: 0008-fs-Fix-copy-paste-error-in-HFS-journal-code.patch
Patch8: 0009-parted-Fix-end_input-leak-in-do_mkpart.patch
Patch9: 0010-parted-Free-tmp-usage-inside-do_print.patch
Patch10: 0011-parted-Fix-memory-leaks-in-do_resizepart.patch
Patch11: 0012-libparted-Fix-warning-about-buffer-size-in-Atari-lab.patch
Patch12: 0013-libparted-Fix-potential-memory-leak-in-gpt_write.patch
Patch13: 0014-tests-t0400-Work-around-a-mkswap-bug-by-using-dev-ze.patch
Patch14: 0015-tests-t9050-Use-dev-zero-for-temporary-file-and-mksw.patch
Conflicts:      toybox
Provides:       %{name}-devel = %{version}-%{release}

%description
This is useful for creating space for new operating systems,
reorganizing disk usage, copying data on hard disks and disk imaging.
The package contains a library, libparted, as well as well as a
command-line frontend, parted, which can also be used in scripts.

%prep
%setup -q
%patch0 -p1

%build
#Add a header to allow building with glibc-2.28 or later
sed -i '/utsname.h/a#include <sys/sysmacros.h>' libparted/arch/linux.c &&

%configure --without-readline --disable-debug \
	   --disable-nls --disable-device-mapper
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

rm -rf %{buildroot}%{_infodir}/dir

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/parted.info.gz
%{_datadir}/*

%changelog
* Tue Dec 21 2021 Max Brodeur-Urbas <maxbr@microsoft.com> - 3.4-1
- Upgrading to 3.4
- Adding 0001-freelocale-bug-fix.patch.
- License verified.

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 3.2-12
- Remove libtool archive files from final packaging

* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 3.2-11
- Provide parted-devel.

*  Wed Aug 05 2020 Andrew Phelps <anphel@microsoft.com> 3.2-10
-  Remove conflicting 'dir' file from _infodir

*  Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.2-9
-  Added %%license line automatically

*  Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.2-8
-  Initial CBL-Mariner import from Photon (license: Apache2).

*  Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 3.2-7
-  Add conflict toybox.

*  Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.2-6
-  Fix compilation issue against glibc-2.28.

*  Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-5
-  Fix summary and description.

*  Tue Jun 06 2017 ChangLee <changlee@vmware.com> 3.2-4
-  Remove %check.

*  Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.2-3
-  Modified %check.

*  Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
-  GA Bump release of all rpms.

*  Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.2-1
-  Initial version.
