Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           luksmeta
Version:        9
Release:        8%{?dist}
Summary:        Utility for storing small metadata in the LUKSv1 header

License:        LGPLv2+
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

Patch01: luksmeta-9-tests.patch
Patch02: luksmeta-9-relax-layout-assumptions.patch
Patch03: Define-log-callback-function-to-use-with-libcryptset.patch

BuildRequires:  gcc
BuildRequires:  asciidoc
BuildRequires:  pkgconfig
BuildRequires:  cryptsetup-devel
Requires: lib%{name}%{?_isa} = %{version}-%{release}

%description
LUKSMeta is a command line utility for storing small portions of metadata in
the LUKSv1 header for use before unlocking the volume.

%package -n lib%{name}
Summary:        Library for storing small metadata in the LUKSv1 header

%description -n lib%{name}
LUKSMeta is a C library for storing small portions of metadata in the LUKSv1
header for use before unlocking the volume.

%package -n lib%{name}-devel
Summary:        Development files for libluksmeta
Requires:       lib%{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n lib%{name}-devel
This package contains development files for the LUKSMeta library.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
rm -rf %{buildroot}/%{_libdir}/libluksmeta.la

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets -n lib%{name}

%files
%{_bindir}/luksmeta
%{_mandir}/man8/luksmeta.8*

%files -n lib%{name}
%license COPYING
%{_libdir}/libluksmeta.so.*

%files -n lib%{name}-devel
%{_includedir}/luksmeta.h
%{_libdir}/libluksmeta.so
%{_libdir}/pkgconfig/luksmeta.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 9-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 31 2019 Sergio Correia <scorreia@redhat.com> - 9-6
- Define log callback function to use with libcryptsetup
  Logs from libcryptsetup now go to stderr and this prevents issues like
  the one reported in https://bugzilla.redhat.com/show_bug.cgi?id=1770395

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Daniel Kopecek <dkopecek@redhat.com> - 9-4
- Add patch to fix tests on newer kernels 

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 09 2018 Nathaniel McCallum <npmccallum@redhat.com> - 9-2
- Add (upstream) patch to fix tests on LUKSv2-default cryptsetup

* Thu Aug 09 2018 Nathaniel McCallum <npmccallum@redhat.com> - 9-1
- New upstream release
- Add asciidoc build require to generate man pages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 8-2
- Rebuild for cryptsetup-2.0.0

* Fri Sep 29 2017 Nathaniel McCallum <npmccallum@redhat.com> - 8-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Nathaniel McCallum <npmccallum@redhat.com> - 7-1
- New upstream release

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 6-1
- New upstream release

* Thu Jun 01 2017 Nathaniel McCallum <npmccallum@redhat.com> - 5-1
- New upstream release

* Tue May 30 2017 Nathaniel McCallum <npmccallum@redhat.com> - 4-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 25 2016 Nathaniel McCallum <npmccallum@redhat.com> - 3-1
- New upstream release

* Thu Aug 25 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2-1
- First release
