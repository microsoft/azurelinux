# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          oath-toolkit
Version:       2.6.12
Release:       3%{?dist}
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:       GPL-3.0-or-later
Summary:       One-time password components
BuildRequires: make
BuildRequires: pam-devel
BuildRequires: gtk-doc
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: xmlsec1-devel
BuildRequires: xmlsec1-openssl-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gnupg2
Source0:       https://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz
Source1:       https://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz.sig
# gpg2 --recv-keys EDA21E94B565716F
# gpg2 --armor --export D73CF638C53C06BE > keyring.asc
Source2:       keyring.asc
URL:           https://www.nongnu.org/oath-toolkit/
Patch0:        oath-toolkit-2.6.12-lockfile.patch

%description
The OATH Toolkit provide components for building one-time password
authentication systems. It contains shared libraries, command line tools and a
PAM module. Supported technologies include the event-based HOTP algorithm
(RFC4226) and the time-based TOTP algorithm (RFC6238). OATH stands for Open
AuTHentication, which is the organization that specify the algorithms. For
managing secret key files, the Portable Symmetric Key Container (PSKC) format
described in RFC6030 is supported.

%package -n liboath
Summary:          Library for OATH handling
License:          LGPL-2.1-or-later
# https://fedorahosted.org/fpc/ticket/174
Provides:         bundled(gnulib)

%description -n liboath
OATH stands for Open AuTHentication, which is the organization that
specify the algorithms. Supported technologies include the event-based
HOTP algorithm (RFC4226) and the time-based TOTP algorithm (RFC6238).

%package -n liboath-devel
Summary:  Development files for liboath
License:  LGPL-2.1-or-later
Requires: liboath%{?_isa} = %{version}-%{release}

%description -n liboath-devel
Development files for liboath.

%package -n liboath-doc
Summary:   Documentation files for liboath
License:   LGPL-2.1-or-later
Requires:  liboath = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n liboath-doc
Documentation files for liboath.

%package -n libpskc
Summary:          Library for PSKC handling
License:          LGPL-2.1-or-later
Requires:         xml-common
# https://fedorahosted.org/fpc/ticket/174
Provides:         bundled(gnulib)

%description -n libpskc
Library for managing secret key files, the Portable Symmetric Key
Container (PSKC) format described in RFC6030 is supported.

%package -n libpskc-devel
Summary:  Development files for libpskc
License:  LGPL-2.1-or-later
Requires: libpskc%{?_isa} = %{version}-%{release}

%description -n libpskc-devel
Development files for libpskc.

%package -n libpskc-doc
Summary:   Documentation files for libpskc
License:   LGPL-2.1-or-later
Requires:  libpskc = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n libpskc-doc
Documentation files for libpskc.

%package -n oathtool
Summary:  A command line tool for generating and validating OTPs
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:  GPL-3.0-or-later
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

%description -n oathtool
A command line tool for generating and validating OTPs.

%package -n pskctool
Summary:  A command line tool for manipulating PSKC data
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)
Requires: xmlsec1-openssl%{?_isa}

%description -n pskctool
A command line tool for manipulating PSKC data.

%package -n pam_oath
Summary:  A PAM module for pluggable login authentication for OATH
Requires: pam

%description -n pam_oath
A PAM module for pluggable login authentication for OATH.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
autoreconf -fi
%configure --with-pam-dir=%{_libdir}/security

# Kill rpaths and link with --as-needed
for d in liboath libpskc pskctool oathtool pam_oath
do
  sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' $d/libtool
  sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' $d/libtool
  sed -i 's| -shared | -Wl,--as-needed\0|g' $d/libtool
done

make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Remove static objects and libtool files
rm -f %{buildroot}%{_libdir}/*.{a,la}
rm -f %{buildroot}%{_libdir}/security/*.la

# Make /etc/liboath directory
mkdir -p -m 0600 %{buildroot}%{_sysconfdir}/liboath

%ldconfig_scriptlets -n liboath

%ldconfig_scriptlets -n libpskc

%files -n liboath
%doc liboath/COPYING
%attr(0600, root, root) %dir %{_sysconfdir}/liboath
%{_libdir}/liboath.so.*

%files -n liboath-devel
%{_includedir}/liboath
%{_libdir}/liboath.so
%{_libdir}/pkgconfig/liboath.pc

%files -n liboath-doc
%{_mandir}/man3/oath*
%{_datadir}/gtk-doc/html/liboath/*

%files -n libpskc
%doc libpskc/README
%{_libdir}/libpskc.so.*
%{_datadir}/xml/pskc

%files -n libpskc-devel
%{_includedir}/pskc
%{_libdir}/libpskc.so
%{_libdir}/pkgconfig/libpskc.pc

%files -n libpskc-doc
%{_mandir}/man3/pskc*
%{_datadir}/gtk-doc/html/libpskc/*

%files -n oathtool
%doc oathtool/COPYING
%{_bindir}/oathtool
%{_mandir}/man1/oathtool.*

%files -n pskctool
%{_bindir}/pskctool
%{_mandir}/man1/pskctool.*

%files -n pam_oath
%doc pam_oath/README pam_oath/COPYING
%{_libdir}/security/pam_oath.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 10 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.12-1
- New version
  Resolves: rhbz#2316447
- Dropped privileges when operating on user files
  Resolves: CVE-2024-47191

* Thu Jul  25 2024 Miroslav Suchý <msuchy@redhat.com> - 2.6.11-6
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 11 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.11-4
- Added gpg2 signature verification

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.11-1
- New version
  Resolves: rhbz#2257841

* Wed Jan  3 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.10-1
- New version
  Resolves: rhbz#2256555

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.9-1
- New version
  Resolves: rhbz#2221430

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May  3 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.7-1
- New version
  Resolves: rhbz#1955967

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.6-1
- New version
  Resolves: rhbz#1918498
- Updated source URL

* Mon Jan  4 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.5-1
- New version
  Resolves: rhbz#1911419

* Thu Nov 12 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.4-1
- New version
  Resolves: rhbz#1896920

* Mon Nov  9 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-1
- New version
  Resolves: rhbz#1895618

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May  4 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.2-5
- Added support for configurable lock file locations and set the default path
  Resolves: rhbz#1178036

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.2-1
- New version
- Fixed FTBFS
  Resolves: rhbz#1605276

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug  4 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.1-1
- New version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.0-1
- New version
- Dropped strdup-null-check patch (upstreamed)

* Fri Jan 30 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-9
- Fixed invalid reads in libpskc due to references to old (freed) xmlDoc
  (by retain-original-xmldoc patch), patch provided by David Woodhouse
  Resolves: rhbz#1129491

* Tue Nov 11 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-8
- Removed RHEL conditionals (not needed any more)

* Fri Nov  7 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-7
- Added check for strdup failure (by strdup-null-check patch)
  Resolves: rhbz#1161360

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-5
- Added support for RHEL (i.e. no PSKC yet on RHEL)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-3
- Added xmlsec1-openssl to requires
  Resolves: rhbz#1066477

* Mon Feb 17 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-2
- Added xmlsec1-openssl-devel to buildrequires

* Thu Feb 13 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-1
- New version
  Resolves: rhbz#1064764

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.0-1
- New version
  Resolves: rhbz#987378

* Wed Jul 10 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2.0-1
- New version
  Resolves: rhbz#982986

* Wed Jun  5 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.2-3
- Fixed requirements according to reviewer comments
- Linked with --as-needed
- Fixed man pages (by man-fix patch)

* Mon Apr  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.2-2
- Added /etc/liboath directory to hold configuration / user lists

* Sun Apr 07 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.2-1
- Initial version
