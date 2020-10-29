Summary:        Basic system utilities
Name:           coreutils
Version:        8.30
Release:        6%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/coreutils
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
# make this package to own serial console profile since it utilizes stty tool
Source1:        serial-console.sh
Patch0:         http://www.linuxfromscratch.org/patches/downloads/coreutils/coreutils-8.30-i18n-1.patch
Patch1:         http://www.linuxfromscratch.org/patches/downloads/coreutils/coreutils-8.10-uname-1.patch
# Upstream community agreed to not fix this
Patch2:         CVE-2016-2781.nopatch
Requires:       gmp
Provides:       sh-utils
Conflicts:      toybox
%description
The Coreutils package contains utilities for showing and setting
the basic system

%package lang
Summary: Additional language files for coreutils
Group: System Environment/Base
Requires: coreutils >= %{version}
%description lang
These are the additional language files of coreutils.

%prep
%autosetup -p1

%build
autoreconf -fi
export FORCE_UNSAFE_CONFIGURE=1 &&  ./configure \
    --prefix=%{_prefix} \
    --enable-no-install-program=kill,uptime \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/man8
mv -v %{buildroot}%{_bindir}/{cat,chgrp,chmod,chown,cp,date,dd,df,echo} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{false,ln,ls,mkdir,mknod,mv,pwd,rm} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{rmdir,stty,sync,true,uname,test,[} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
sed -i s/\"1\"/\"8\"/1 %{buildroot}%{_mandir}/man8/chroot.8
mv -v %{buildroot}%{_bindir}/{head,sleep,nice} %{buildroot}/bin
rm -rf %{buildroot}%{_infodir}
install -vdm755 %{buildroot}/etc/profile.d
install -m 0644 %{SOURCE1} %{buildroot}/etc/profile.d/
%find_lang %{name}

%check
sed -i '/tests\/misc\/sort.pl/d' Makefile
sed -i 's/test-getlogin$(EXEEXT)//' gnulib-tests/Makefile
sed -i 's/PET/-05/g' tests/misc/date-debug.sh
sed -i 's/2>err\/merge-/2>\&1 > err\/merge-/g' tests/misc/sort-merge-fdlimit.sh
sed -i 's/)\" = \"10x0/| head -n 1)\" = \"10x0/g' tests/split/r-chunk.sh
sed  -i '/mb.sh/d' Makefile
#make NON_ROOT_USERNAME=nobody check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
/bin/*
%{_sysconfdir}/profile.d/serial-console.sh
%{_libexecdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Thu Oct 29 2020 Nicolas Ontiveros <niontive@microsoft.com> 8.30-6
- No patch CVE-2016-2781
* Mon Jun 15 2020 Andrew Phelps <anphel@microsoft.com> 8.30-5
- Add patch for uname processor type
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 8.30-4
- Added %%license line automatically
* Tue Dec 03 2019 Andrew Phelps <anphel@microsoft.com> 8.30-3
- Run autoconf to remake build system files
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 8.30-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Fri Sep 07 2018 Alexey Makhalov <amakhalov@vmware.com> 8.30-1
- Version update to support glibc-2.28
* Tue Aug 28 2018 Alexey Makhalov <amakhalov@vmware.com> 8.27-4
- Add serial-console profile.d script
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 8.27-3
- Added conflicts toybox
* Wed Aug 09 2017 Rongrong Qiu <rqiu@vmware.com> 8.27-2
- Fix make check for bug 1900253
* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 8.27-1
- Upgraded to version 8.27
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.25-2
- GA - Bump release of all rpms
* Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 8.25-1
- Updated to version 8.25
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 8.24-1
- Updated to version 8.24
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 8.22-1
- Initial build. First version
