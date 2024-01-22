Summary:          Library to support IDNA2008 internationalized domain names
Name:             libidn2
Version:          2.3.4
Release:          4%{?dist}
License:          (GPLv2+ or LGPLv3+) and GPLv3+
URL:              https://www.gnu.org/software/libidn/#libidn2

Source0:          https://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
Source1:          https://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz.sig
Source2:          https://keys.openpgp.org/vks/v1/by-fingerprint/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE

BuildRequires:    glibc-devel
BuildRequires:    kernel-devel
BuildRequires:    kernel-headers
BuildRequires:    binutils
BuildRequires:    gnupg2
BuildRequires:    gcc
BuildRequires:    make
BuildRequires:    gettext
BuildRequires:    libunistring-devel
BuildRequires:    texinfo
Provides:         bundled(gnulib)

%description
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package devel
Summary:          Development files for libidn2
Requires:         %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libidn2-devel package contains libraries and header files for
developing applications that use libidn2.

%package -n idn2
Summary:          IDNA2008 internationalized domain names conversion tool
License:          GPL-3.0-or-later
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description -n idn2
The idn2 package contains the idn2 command line tool for testing
IDNA2008 conversions.

%prep
%{!?el7:%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'}
%setup -q

%build
%configure --disable-static
# Avoid (unnecessary) full autoreconf
%make_build AUTOMAKE=true
%make_build AUTOMAKE=true -C doc html

%install
%make_install AUTOMAKE=true

# Clean-up examples for documentation
%make_build -C examples distclean
rm -f examples/Makefile*

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Some file cleanups
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%find_lang %{name}

%check
%make_build -C tests check

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING COPYING.LESSERv3 COPYING.unicode COPYINGv2
%doc AUTHORS NEWS README.md
%{_libdir}/%{name}.so.0*

%files devel
%doc doc/%{name}.html examples
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/idn2.h
%{_mandir}/man3/idn2_*.3*
%{_datadir}/gtk-doc/

%files -n idn2
%{_bindir}/idn2
%{_mandir}/man1/idn2.1*
%{_infodir}/%{name}.info*

%changelog
* Tue Jan 16 17:26:11 EST 2024 Dan Streetman <ddstreet@ieee.org> - 2.3.4-4
- Update to version from Fedora 39/rawhide.
- Next line is present only to avoid tooling failures, and does not indicate the actual package license.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- license verified

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 24 2022 Robert Scheck <robert@fedoraproject.org> 2.3.4-1
- Upgrade to 2.3.4 (#2137124)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Robert Scheck <robert@fedoraproject.org> 2.3.3-1
- Upgrade to 2.3.3 (#2106161)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 31 2021 Robert Scheck <robert@fedoraproject.org> 2.3.2-3
- Disable undesired Makefile rebuilding by automake (#1999520)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Robert Scheck <robert@fedoraproject.org> 2.3.2-1
- Upgrade to 2.3.2 (#1983906)

* Wed May 12 2021 Robert Scheck <robert@fedoraproject.org> 2.3.1-1
- Upgrade to 2.3.1 (#1960005)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Jeff Law <law@redhat.com> - 2.3.0-3
- Touch a couple autoconf related files to prevent undesired rebuilding
  if %%configure changes one or more configure files.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 16 2019 Robert Scheck <robert@fedoraproject.org> 2.3.0-1
- Upgrade to 2.3.0 (#1764345, #1772703)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Robert Scheck <robert@fedoraproject.org> 2.2.0-1
- Upgrade to 2.2.0 (#1713402)

* Sat Feb 09 2019 Robert Scheck <robert@fedoraproject.org> 2.1.1a-1
- Upgrade to 2.1.1a (#1674002 #c1)

* Sat Feb 09 2019 Robert Scheck <robert@fedoraproject.org> 2.1.1-1
- Upgrade to 2.1.1 (#1674002, #1674023)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Robert Scheck <robert@fedoraproject.org> 2.0.5-1
- Upgrade to 2.0.5 (#1577864, #1579825)

* Wed Apr 04 2018 Robert Scheck <robert@fedoraproject.org> 2.0.4-7
- Split RPM scriptlets (#1563832)

* Mon Apr 02 2018 Robert Scheck <robert@fedoraproject.org> 2.0.4-6
- Use splitting suggestions from Nikos Mavrogiannopoulos instead

* Mon Apr  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.4-5
- Split cli utilities out into a sub package
- Spec file cleanups

* Fri Mar 30 2018 Robert Scheck <robert@fedoraproject.org> 2.0.4-4
- Added upstream patch to fix silently transliterated decoded
  domain names (#1556954)

* Sun Feb 18 2018 Robert Scheck <robert@fedoraproject.org> 2.0.4-3
- Added upstream patch to fix STD3 ASCII rules (#1543021)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 30 2017 Robert Scheck <robert@fedoraproject.org> 2.0.4-1
- Upgrade to 2.0.4 (#1486881, #1486882)

* Tue Aug 01 2017 Robert Scheck <robert@fedoraproject.org> 2.0.3-1
- Upgrade to 2.0.3 (#1468608, #1474324)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 30 2017 Robert Scheck <robert@fedoraproject.org> 2.0.2-1
- Upgrade to 2.0.2 (#1444712)

* Thu Apr 06 2017 Robert Scheck <robert@fedoraproject.org> 2.0.0-1
- Upgrade to 2.0.0 (#1439727)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Robert Scheck <robert@fedoraproject.org> 0.16-1
- Upgrade to 0.16 (#1416642)

* Mon Nov 21 2016 Robert Scheck <robert@fedoraproject.org> 0.11-1
- Upgrade to 0.11
- Reflect dual-licensing of library in license tag (#1397021)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 7 2015 Than Ngo <than@redhat.com> 0.10-2
- fix build failure related to missing automake-1.14

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.10-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Oct 12 2014 Robert Scheck <robert@fedoraproject.org> 0.10-1
- Upgrade to 0.10

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Robert Scheck <robert@fedoraproject.org> 0.8-3
- Added provide bundled(gnulib) as it's a copylib (#821769)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 15 2012 Robert Scheck <robert@fedoraproject.org> 0.8-1
- Upgrade to 0.8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 13 2011 Robert Scheck <robert@fedoraproject.org> 0.7-1
- Upgrade to 0.7

* Sat Jun 04 2011 Robert Scheck <robert@fedoraproject.org> 0.6-1
- Upgrade to 0.6

* Wed May 18 2011 Robert Scheck <robert@fedoraproject.org> 0.5-1
- Upgrade to 0.5

* Mon May 16 2011 Robert Scheck <robert@fedoraproject.org> 0.4-1
- Upgrade to 0.4

* Sat May 07 2011 Robert Scheck <robert@fedoraproject.org> 0.3-1
- Upgrade to 0.3
- Initial spec file for Fedora and Red Hat Enterprise Linux
