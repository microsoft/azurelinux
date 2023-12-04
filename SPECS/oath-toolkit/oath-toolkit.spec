Summary:        One-time password components
Name:           oath-toolkit
Version:        2.6.9
Release:        1%{?dist}
License:        GPLv3+ and LGPLv2+
URL:            https://www.nongnu.org/oath-toolkit/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz

Patch0:        oath-toolkit-2.6.9-lockfile.patch

BuildRequires: pam-devel
BuildRequires: gtk-doc
BuildRequires: libtool
BuildRequires: xmlsec1-devel
BuildRequires: autoconf
BuildRequires: automake

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
License:          LGPLv2+
# https://fedorahosted.org/fpc/ticket/174
#Provides:         bundled(gnulib)

%description -n liboath
OATH stands for Open AuTHentication, which is the organization that
specify the algorithms. Supported technologies include the event-based
HOTP algorithm (RFC4226) and the time-based TOTP algorithm (RFC6238).

%package -n liboath-devel
Summary:  Development files for liboath
License:  LGPLv2+
Requires: liboath%{?_isa} = %{version}-%{release}

%description -n liboath-devel
Development files for liboath.

%package -n liboath-doc
Summary:   Documentation files for liboath
License:   LGPLv2+
Requires:  liboath = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n liboath-doc
Documentation files for liboath.

%package -n libpskc
Summary:          Library for PSKC handling
License:          LGPLv2+
Requires:         xml-common
# https://fedorahosted.org/fpc/ticket/174
#Provides:         bundled(gnulib)

%description -n libpskc
Library for managing secret key files, the Portable Symmetric Key
Container (PSKC) format described in RFC6030 is supported.

%package -n libpskc-devel
Summary:  Development files for libpskc
License:  LGPLv2+
Requires: libpskc%{?_isa} = %{version}-%{release}

%description -n libpskc-devel
Development files for libpskc.

%package -n libpskc-doc
Summary:   Documentation files for libpskc
License:   LGPLv2+
Requires:  libpskc = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n libpskc-doc
Documentation files for libpskc.

%package -n oathtool
Summary:  A command line tool for generating and validating OTPs
License:  GPLv3+
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

%description -n oathtool
A command line tool for generating and validating OTPs.

%package -n pskctool
Summary:  A command line tool for manipulating PSKC data
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)
Requires: xmlsec1%{?_isa}

%description -n pskctool
A command line tool for manipulating PSKC data.

%package -n pam_oath
Summary:  A PAM module for pluggable login authentication for OATH
Requires: pam

%description -n pam_oath
A PAM module for pluggable login authentication for OATH.

%prep
%setup -q

%build
autoreconf -fi
%configure --with-pam-dir=%{_libdir}/security

# patch must be applied after configure otherwise liboath/oath.h patch will be partly reverted
patch -p1 --input %{PATCH0}

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

%post -p /sbin/ldconfig -n liboath
%post -p /sbin/ldconfig -n libpskc

%postun -p /sbin/ldconfig -n liboath
%postun -p /sbin/ldconfig -n libpskc

%files -n liboath
%license liboath/COPYING
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
%license oathtool/COPYING
%{_bindir}/oathtool
%{_mandir}/man1/oathtool.*

%files -n pskctool
%{_bindir}/pskctool
%{_mandir}/man1/pskctool.*

%files -n pam_oath
%license pam_oath/COPYING
%doc pam_oath/README
%{_libdir}/security/pam_oath.so

%changelog
* Thu Oct 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.9-1
- Auto-upgrade to 2.6.9 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.6.7-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Feb 18 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.6.7-1
- Upgrading to v2.6.7

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 2.6.2-7
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

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