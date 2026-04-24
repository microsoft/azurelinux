# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%?mingw_package_header

Summary:        MinGW Windows Internationalized Domain Name 2008 support library
Name:           mingw-libidn2
Version:        2.3.8
Release: 3%{?dist}
License:        (GPL-2.0-or-later OR LGPL-3.0-or-later) AND GPL-3.0-or-later
URL:            https://www.gnu.org/software/libidn/#libidn2

Source0:        https://ftp.gnu.org/gnu/libidn/libidn2-%{version}.tar.gz
Source1:        https://ftp.gnu.org/gnu/libidn/libidn2-%{version}.tar.gz.sig
Source2:        https://keys.openpgp.org/vks/v1/by-fingerprint/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils

BuildRequires:  gnupg2
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig

# mingw32-gcc and mingw64-gcc are not available on s390x builders
%if 0%{?rhel}
ExclusiveArch:  %{ix86} x86_64 %{arm}
%endif

%description
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

# Win32
%package -n mingw32-libidn2
Summary:        MinGW Windows IDN 2008 library the win32 target
Requires:       pkgconfig

%description -n mingw32-libidn2
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package -n mingw32-libidn2-static
Summary:        Static version of the MinGW Windows IDN 2008 library
Requires:       mingw32-libidn2 = %{version}-%{release}

%description -n mingw32-libidn2-static
Static version of the MinGW Windows IDN 2008 library.

# Win64
%package -n mingw64-libidn2
Summary:        MinGW Windows IDN 2008 library the win64 target
Requires:       pkgconfig

%description -n mingw64-libidn2
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package -n mingw64-libidn2-static
Summary:        Static version of the MinGW Windows IDN 2008 library
Requires:       mingw64-libidn2 = %{version}-%{release}

%description -n mingw64-libidn2-static
Static version of the MinGW Windows IDN 2008 library.

%?mingw_debug_package

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q -n libidn2-%{version}

%build
%mingw_configure --disable-nls --enable-static --enable-shared
%mingw_make %{?_smp_mflags}

%install
%mingw_make DESTDIR=$RPM_BUILD_ROOT install

# Remove documentation which duplicates native Fedora package.
rm -r $RPM_BUILD_ROOT%{mingw32_infodir}
rm -r $RPM_BUILD_ROOT%{mingw64_infodir}
rm -r $RPM_BUILD_ROOT%{mingw32_mandir}/man*
rm -r $RPM_BUILD_ROOT%{mingw64_mandir}/man*

# The .def file isn't interesting for other libraries/applications
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/libidn2-*.def
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/libidn2-*.def

# The executables are not useful in this build
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/lookup.exe
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/register.exe

rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/lookup.exe
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/register.exe

# Drop all .la files
find $RPM_BUILD_ROOT -name "*.la" -delete

# Win32
%files -n mingw32-libidn2
%license COPYING COPYING.LESSERv3 COPYING.unicode COPYINGv2
%{mingw32_bindir}/idn2.exe
%{mingw32_bindir}/libidn2-0.dll
%{mingw32_libdir}/libidn2.dll.a
%{mingw32_libdir}/pkgconfig/libidn2.pc
%{mingw32_includedir}/idn2.h

%files -n mingw32-libidn2-static
%{mingw32_libdir}/libidn2.a

# Win64
%files -n mingw64-libidn2
%license COPYING COPYING.LESSERv3 COPYING.unicode COPYINGv2
%{mingw64_bindir}/idn2.exe
%{mingw64_bindir}/libidn2-0.dll
%{mingw64_libdir}/libidn2.dll.a
%{mingw64_libdir}/pkgconfig/libidn2.pc
%{mingw64_includedir}/idn2.h

%files -n mingw64-libidn2-static
%{mingw64_libdir}/libidn2.a

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Mar 09 2025 Robert Scheck <robert@fedoraproject.org> 2.3.8-1
- Upgrade to 2.3.8 (#2350925)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Robert Scheck <robert@fedoraproject.org> 2.3.7-1
- Upgrade to 2.3.7 (#2260624)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 24 2022 Robert Scheck <robert@fedoraproject.org> 2.3.4-1
- Upgrade to 2.3.4 (#2137125)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Robert Scheck <robert@fedoraproject.org> 2.3.3-1
- Upgrade to 2.3.3 (#2106162)

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.3.2-4
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Robert Scheck <robert@fedoraproject.org> 2.3.2-1
- Upgrade to 2.3.2 (#1983907)

* Wed May 12 2021 Robert Scheck <robert@fedoraproject.org> 2.3.1-1
- Upgrade to 2.3.1 (#1960007)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 16 2019 Robert Scheck <robert@fedoraproject.org> - 2.3.0-1
- New upstream release (#1764345, #1773229)

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 2.2.0-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Tue Aug 13 2019 Fabiano Fidêncio <fidencio@redhat.com> - 2.2.0-1
- Update the sources accordingly to its native counter part, rhbz#1740792

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.1.1a-1
- New upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 30 2017 Robert Scheck <robert@fedoraproject.org> - 2.0.4-1
- New upstream release (#1486881, #1486882)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr  4 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.0.0-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 21 2016 Nikos Mavrogiannopoulos - 0.11-1
- Initial RPM release.
