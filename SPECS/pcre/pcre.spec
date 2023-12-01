Summary:        Grep for perl compatible regular expressions
Name:           pcre
Version:        8.45
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.pcre.org
Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
Requires:       libgcc
Requires:       libstdc++
Requires:       pcre-libs = %{version}-%{release}
Requires:       readline

%description
The PCRE package contains Perl Compatible Regular Expression libraries. These are useful for implementing regular expression pattern matching using the same syntax and semantics as Perl 5.

%package        devel
Summary:        Headers and static lib for pcre development
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description    devel
Install this package if you want do compile applications using the pcre
library.

%package        libs
Summary:        Libraries for pcre
Group:          System Environment/Libraries

%description libs
This package contains minimal set of shared pcre libraries.

%prep
%autosetup

%build
%configure \
%ifarch s390 s390x sparc64 sparcv9 riscv64
    --disable-jit                     \
%else
    --enable-jit                      \
%endif
    --docdir=%{_docdir}/pcre-%{version} \
    --enable-unicode-properties       \
    --enable-pcre16                   \
    --enable-pcre32                   \
    --enable-pcregrep-libz            \
    --enable-pcregrep-libbz2          \
    --enable-pcretest-libreadline     \
    --with-match-limit-recursion=16000
%make_build

%install
%make_install
mv -v %{buildroot}%{_libdir}/libpcre.so.* %{buildroot}/lib &&
ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libpcre.so) %{buildroot}%{_libdir}/libpcre.so
ln -sfv $(readlink %{buildroot}%{_libdir}/libpcre.so) %{buildroot}%{_libdir}/libpcre.so.0
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/pcregrep
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.1*
%{_mandir}/man1/pcretest.1*
%{_libdir}/*.so.*
%exclude %{_libdir}/libpcre.so.*

%files devel
%defattr(-, root, root)
%{_bindir}/*
%exclude %{_bindir}/pcregrep
%exclude %{_bindir}/pcretest
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files libs
%defattr(-, root, root)
%{_libdir}/libpcre.so.*

%changelog
* Tue Mar 08 2022 Matt DeVuyst <mattdev@microsoft.com> - 8.45-2
- Enable JIT feature on supported architectures (as Fedora does).

* Thu Feb 10 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 8.45-1
- Upgrading to v8.45
- Correcting source URL.

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 8.44-3
- Remove *.la files from devel subpackage
- Build static libraries, add compatibility provides for static subpackage
- Remove manual pkgconfig provides

* Mon Apr 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 8.44-2
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Thu Oct 29 2020 Joe Schmitt <joschmit@microsoft.com> - 8.44-1
- Update to version 8.44 to fix CVE-2020-14155.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.42-4
- Added %%license line automatically

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> - 8.42-3
- Update URL.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 8.42-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 8.42-1
- Update to version 8.42

* Wed Dec 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 8.41-1
- Update to version 8.41

* Wed Jul 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 8.40-4
- Added fix for CVE-2017-11164 by adding stack recursion limit

* Wed May 24 2017 Divya Thaluru <dthaluru@vmware.com> - 8.40-3
- Added fixes for CVE-2017-7244, CVE-2017-7245, CVE-2017-7246, CVE-2017-7186

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 8.40-2
- Added -libs subpackage

* Mon Apr 03 2017 Robert Qi <qij@vmware.com> - 8.40-1
- Update to 8.40

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 8.39-2
- Modified %%check

* Fri Sep 9 2016 Xiaolin Li <xiaolinl@vmware.com> - 8.39-1
- Update to version 8.39

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 8.38-3
- GA - Bump release of all rpms

* Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  8.38-2
- Add upstream fixes patch

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> - 8.38-1
- Updated to version 8.38

* Mon Nov 30 2015 Sharath George <sharathg@vmware.com> - 8.36-2
- Add symlink for libpcre.so.1

* Thu Nov 06 2014 Sharath George <sharathg@vmware.com> - 8.36-1
- Initial version
