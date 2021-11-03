Summary:        Contains programs for compressing and decompressing files
Name:           bzip2
Version:        1.0.8
Release:        1%{?dist}
License:        BSD
URL:            https://sourceware.org/bzip2/index.html
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://sourceware.org/pub/%{name}/%{name}-%{version}.tar.gz
Provides:       libbz2.so.1()(64bit)
Patch0:         https://www.linuxfromscratch.org/patches/lfs/11.0/bzip2-1.0.8-install_docs-1.patch
Patch1:         cflags-fix.patch
Requires:       bzip2-libs = %{version}-%{release}
Conflicts:      toybox

%description
The Bzip2 package contains programs for compressing and
decompressing files.  Compressing text files with bzip2 yields a much better
compression percentage than with the traditional gzip.

%package        devel
Summary:        Header and development files for bzip2
Requires:       bzip2
Provides:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%package libs
Summary:        Libraries for bzip2
Group:          System Environment/Libraries
%description    libs
This package contains minimal set of shared bzip2 libraries.

%prep
%autosetup -p1
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile

%build
make VERBOSE=1 %{?_smp_mflags} -f Makefile-libbz2_so
make clean
make VERBOSE=1 %{?_smp_mflags}

%install
make PREFIX=%{buildroot}/usr install
install -vdm 0755 %{buildroot}/%{_libdir}
install -vdm 0755 %{buildroot}/bin
cp -av libbz2.so* %{buildroot}/%{_libdir}
install -vdm 755 %{buildroot}%{_libdir}
ln -sv libbz2.so.%{version} %{buildroot}%{_libdir}/libbz2.so
ln -sv libbz2.so.%{version} %{buildroot}%{_libdir}/libbz2.so.1
rm -v %{buildroot}%{_bindir}/{bunzip2,bzcat}
ln -sv bzip2 %{buildroot}/usr/bin/bunzip2
ln -sv bzip2 %{buildroot}/usr/bin/bzcat
find %{buildroot} -name '*.a'  -delete

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/bzcat
%{_bindir}/bunzip2
%{_bindir}/bzless
%{_bindir}/bzgrep
%{_bindir}/bzip2
%{_bindir}/bzdiff
%{_bindir}/bzfgrep
%{_bindir}/bzcmp
%{_bindir}/bzip2recover
%{_bindir}/bzegrep
%{_bindir}/bzmore
%{_mandir}/man1/bzmore.1.gz
%{_mandir}/man1/bzfgrep.1.gz
%{_mandir}/man1/bzegrep.1.gz
%{_mandir}/man1/bzgrep.1.gz
%{_mandir}/man1/bzdiff.1.gz
%{_mandir}/man1/bzcmp.1.gz
%{_mandir}/man1/bzless.1.gz
%{_mandir}/man1/bzip2.1.gz

%files devel
%{_includedir}/bzlib.h
%{_libdir}/libbz2.so
%{_docdir}/*

%files libs
%{_libdir}/libbz2.so.*

%changelog
* Thu Oct 14 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0.8-1
- Upgrade to 1.0.8 to fix CVE-2016-3189

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0.6-16
- Replace incorrect %%{_lib} usage with %%{_libdir}
- Provide bzip2-devel%%{?_isa}

* Fri Jul 31 2020 Leandro Pereira <leperei@microsoft.com> 1.0.6-15
- Don't stomp on CFLAGS.

* Tue May 26 2020 Emre Girgin <mrgirgin@microsoft.com> 1.0.6-14
- Fix CVE-2019-12900. This was erroneously named CVE-2019-1353 before, which is not even related to bzip2.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.6-13
- Added %%license line automatically

* Wed Apr 22 2020 Emre Girgin <mrgirgin@microsoft.com> 1.0.6-12
- Fix CVE-2019-1353.

* Mon Apr 13 2020 Eric Li <eli@microsoft.com> 1.0.6-11
- Update Source0: and delete sha1. Verified License. Fixed URL.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0.6-10
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 1.0.6-9
- Add conflicts toybox.

* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 1.0.6-8
- Fix symlink.

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.6-7
- Added -libs subpackage.

* Fri Oct 21 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.6-6
- Fixing security bug CVE-2016-3189.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.6-5
- GA - Bump release of all rpms.

* Tue Nov 10 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.0.6-4
- Providing libbz2.so.1, miror fix for devel provides.

* Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.6-3
- Adding bzip2 package run time required package for bzip2-devel package.

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.0.6-2
- Update according to UsrMove.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.6-1
- Initial build First version.