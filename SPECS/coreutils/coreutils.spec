Summary:        Basic system utilities
Name:           coreutils
Version:        8.32
Release:        7%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.gnu.org/software/coreutils
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
# make this package to own serial console profile since it utilizes stty tool
Source1:        serial-console.sh
# The following two patches are sourced from RedHat via Photon
Patch0:         coreutils-8.32-i18n-1.patch
Patch1:         coreutils-8.10-uname-1.patch
Patch2:         skip_test_if_run_as_root.patch
Patch3:         fix_test_env_signal_handler.patch
Patch4:         coreutils-fix-get-sys_getdents-aarch64.patch
BuildRequires:  libselinux-devel
BuildRequires:  libselinux-utils
Requires:       gmp
Requires:       libselinux
Conflicts:      toybox
Provides:       sh-utils
%if %{with_check}
BuildRequires:  perl
BuildRequires:  perl(File::Find)
%endif

%description
The Coreutils package contains utilities for showing and setting
the basic system

%package lang
Summary:        Additional language files for coreutils
Group:          System Environment/Base
Requires:       coreutils >= %{version}

%description lang
These are the additional language files of coreutils.

%prep
%autosetup -N
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%ifarch aarch64
%patch4 -p1
%endif

%build
autoreconf -fi
export FORCE_UNSAFE_CONFIGURE=1 &&  ./configure \
    --prefix=%{_prefix} \
    --enable-install-program=arch \
    --enable-no-install-program=kill,uptime \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/man8
mv -v %{buildroot}%{_bindir}/{arch,cat,chgrp,chmod,chown,cp,date,dd,df,echo} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{false,ln,ls,mkdir,mknod,mv,pwd,rm} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{rmdir,stty,sync,true,uname,test,[} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
sed -i s/\"1\"/\"8\"/1 %{buildroot}%{_mandir}/man8/chroot.8
mv -v %{buildroot}%{_bindir}/{head,sleep,nice} %{buildroot}/bin
rm -rf %{buildroot}%{_infodir}
install -vdm755 %{buildroot}%{_sysconfdir}/profile.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/
%find_lang %{name}

%check
sed -i '/tests\/misc\/sort.pl/d' Makefile
sed -i 's/test-getlogin$(EXEEXT)//' gnulib-tests/Makefile
sed -i 's/PET/-05/g' tests/misc/date-debug.sh
sed -i 's/2>err\/merge-/2>\&1 > err\/merge-/g' tests/misc/sort-merge-fdlimit.sh
sed -i 's/)\" = \"10x0/| head -n 1)\" = \"10x0/g' tests/split/r-chunk.sh
sed  -i '/mb.sh/d' Makefile
# remove capability test which incorrectly determines xattr support and then fails
sed -i '/tests\/cp\/capability.sh/d' Makefile
LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 make -k check

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
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 8.32-7
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Nov 23 2022 Chris PeBenito <chpebeni@microsoft.com> - 8.32-6
- Force rebuild to address missing SELinux features.

* Mon Jul 11 2022 Olivia Crain <oliviacrain@microsoft.com> - 8.32-5
- Add upstream patch to fix race in env-signal-handler test
- Ensure SRPMs built on any architecture include all patches
- Remove nopatch files from spec

* Wed Jun 29 2022 Olivia Crain <oliviacrain@microsoft.com> - 8.32-4
- Configure build to output `arch` binary (equivalent to `uname -m`)

* Wed Mar 23 2022 Chris PeBenito <chpebeni@microsoft.com> 8.32-3
- Add missing BuildRequires needed to correctly enable SELinux support.

* Mon Mar 14 2022 Bala <balakumaran.kannan@microsoft.com> - 8.32-2
- BR perl related packages for PTest
- Add patch to skip some tests when run as root user

* Fri Oct 08 2021 Andrew Phelps <anphel@microsoft.com> 8.32-1
- Update to version 8.32
- Add patch to fix aarch64 build issue
- License verified

* Tue Jun 15 2021 Daniel Burgener <daburgen@microsoft.com> 8.30-10
- Fix issue with undocumented libselinux requirement

* Tue Feb 16 2021 Daniel Burgener <daburgen@microsoft.com> 8.30-9
- Enable SELinux support

* Fri Jan 22 2021 Andrew Phelps <anphel@microsoft.com> 8.30-8
- Fix check test

* Tue Nov 10 2020 Thomas Crain <thcrain@microsoft.com> 8.30-7
- Nopatch CVE-2013-0222, CVE-2013-0223
- Remove references to Linux From Scratch
- Change Source0 to HTTPS url

* Thu Oct 29 2020 Nicolas Ontiveros <niontive@microsoft.com> 8.30-6
- No patch CVE-2016-2781
- No patch CVE-2013-0221

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
