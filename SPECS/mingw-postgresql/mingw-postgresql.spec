# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-postgresql
Version:        16.9
Release:        1%{?dist}
Summary:        MinGW Windows PostgreSQL library

License:        PostgreSQL
URL:            http://www.postgresql.org/
Source0:        https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source1:        https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.sha256

# Allow linking to MinGW TCL DLL
Patch0:         postgresql-10.0-mingw.patch
# https://www.postgresql.org/message-id/2a6c418e-373b-8466-fcb8-ce729aab255f@gmail.com
Patch1:         postgresql-11.2-import-name.patch
# https://www.postgresql.org/message-id/2a6c418e-373b-8466-fcb8-ce729aab255f@gmail.com
Patch2:         postgresql-11.2-static-libraries.patch
# Use winpthreads directly instead of internal reimplementation
# It causes multiple definition errors if linked together with something that pulls in winpthreads
#Patch3:         postgresql_pthread.patch
# Keep/add some libraries in SHLIB_LINK as eventually passed to the pkgconfig Libs.private:
# - libz, libpathcch, required by libcrypto
# - libiconv, required by libintl
Patch4:         postgresql_libs.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gettext
#BuildRequires:  mingw32-icu
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-libxslt
BuildRequires:  mingw32-openssl
BuildRequires:  mingw32-tcl
BuildRequires:  mingw32-readline
BuildRequires:  mingw32-winpthreads
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gettext
#BuildRequires:  mingw64-icu
BuildRequires:  mingw64-libxml2
BuildRequires:  mingw64-libxslt
BuildRequires:  mingw64-openssl
BuildRequires:  mingw64-readline
BuildRequires:  mingw64-tcl
BuildRequires:  mingw64-winpthreads
BuildRequires:  mingw64-zlib

BuildRequires:  bison flex gettext make pkgconfig tcl


%description
MinGW Windows copy of PostgreSQL. PostgreSQL is an advanced Object-Relational
database management system (DBMS).


# Win32
%package -n mingw32-postgresql
Summary:        MinGW Windows PostgreSQL library

%description -n mingw32-postgresql
MinGW Windows copy of PostgreSQL. PostgreSQL is an advanced Object-Relational
database management system (DBMS).

%package -n mingw32-postgresql-static
Summary:        Static libraries for MinGW PostgreSQL
Requires:       mingw32-postgresql = %{version}-%{release}

%description -n mingw32-postgresql-static
%{summary}

# Win64
%package -n mingw64-postgresql
Summary:        MinGW Windows PostgreSQL library

%description -n mingw64-postgresql
MinGW Windows copy of PostgreSQL. PostgreSQL is an advanced Object-Relational
database management system (DBMS).

%package -n mingw64-postgresql-static
Summary:        Static libraries for MinGW PostgreSQL
Requires:       mingw64-postgresql = %{version}-%{release}

%description -n mingw64-postgresql-static
%{summary}


%{?mingw_debug_package}


%prep
%autosetup -p1 -n postgresql-%{version}


%build
MINGW32_CONFIGURE_ARGS=--with-tclconfig=%{mingw32_libdir} \
MINGW64_CONFIGURE_ARGS=--with-tclconfig=%{mingw64_libdir} \
%mingw_configure \
    --with-openssl \
    --enable-thread-safety \
    --enable-integer-datetimes \
    --enable-nls \
    --without-icu \
    --with-ldap \
    --with-libxml \
    --with-libxslt \
    --with-tcl
# Make DLL definition file visible during each arch build
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/libpq/libpqdll.def ./build_win32/src/interfaces/libpq/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/libpq/libpqdll.def ./build_win64/src/interfaces/libpq/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/ecpglib/libecpgdll.def ./build_win32/src/interfaces/ecpg/ecpglib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/ecpglib/libecpgdll.def ./build_win64/src/interfaces/ecpg/ecpglib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/pgtypeslib/libpgtypesdll.def ./build_win32/src/interfaces/ecpg/pgtypeslib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/pgtypeslib/libpgtypesdll.def ./build_win64/src/interfaces/ecpg/pgtypeslib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/compatlib/libecpg_compatdll.def ./build_win32/src/interfaces/ecpg/compatlib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/compatlib/libecpg_compatdll.def ./build_win64/src/interfaces/ecpg/compatlib/
%mingw_make_build


%install
%mingw_make_install

# move DLLs to bin
mv %{buildroot}%{mingw32_libdir}/*.dll %{buildroot}%{mingw32_bindir}
mv %{buildroot}%{mingw64_libdir}/*.dll %{buildroot}%{mingw64_bindir}

# due to Fedora packaging policy, delete executables
rm %{buildroot}%{mingw32_bindir}/*.exe
rm %{buildroot}%{mingw64_bindir}/*.exe
rm -rf %{buildroot}%{mingw32_libdir}/postgresql/
rm -rf %{buildroot}%{mingw64_libdir}/postgresql/

# libpostgres.dll.a is just the import library for postgres.exe, delete it
rm -f %{buildroot}%{mingw32_libdir}/libpostgres.{a,dll.a}
rm -f %{buildroot}%{mingw64_libdir}/libpostgres.{a,dll.a}

# remove server support files
rm -rf %{buildroot}%{mingw32_bindir}/pltcl*
rm -rf %{buildroot}%{mingw64_bindir}/pltcl*
rm -rf %{buildroot}%{mingw32_datadir}
rm -rf %{buildroot}%{mingw64_datadir}


# Win32
%files -n mingw32-postgresql
%license COPYRIGHT
%{mingw32_bindir}/libecpg.dll
%{mingw32_bindir}/libecpg_compat.dll
%{mingw32_bindir}/libpgtypes.dll
%{mingw32_bindir}/libpq.dll
%{mingw32_includedir}/libpq/
%{mingw32_includedir}/postgresql/
%{mingw32_includedir}/ecpg*.h
%{mingw32_includedir}/libpq-events.h
%{mingw32_includedir}/libpq-fe.h
%{mingw32_includedir}/pg*.h
%{mingw32_includedir}/postgres_ext.h
%{mingw32_includedir}/sql*.h
%{mingw32_libdir}/libecpg.dll.a
%{mingw32_libdir}/libecpg_compat.dll.a
%{mingw32_libdir}/libpgtypes.dll.a
%{mingw32_libdir}/libpq.dll.a
%{mingw32_libdir}/pkgconfig/*.pc


%files -n mingw32-postgresql-static
%{mingw32_libdir}/libecpg.a
%{mingw32_libdir}/libecpg_compat.a
%{mingw32_libdir}/libpq.a
%{mingw32_libdir}/libpgcommon.a
%{mingw32_libdir}/libpgcommon_shlib.a
%{mingw32_libdir}/libpgfeutils.a
%{mingw32_libdir}/libpgport.a
%{mingw32_libdir}/libpgport_shlib.a
%{mingw32_libdir}/libpgtypes.a


# Win64
%files -n mingw64-postgresql
%license COPYRIGHT
%{mingw64_bindir}/libecpg.dll
%{mingw64_bindir}/libecpg_compat.dll
%{mingw64_bindir}/libpgtypes.dll
%{mingw64_bindir}/libpq.dll
%{mingw64_includedir}/libpq/
%{mingw64_includedir}/postgresql/
%{mingw64_includedir}/ecpg*.h
%{mingw64_includedir}/libpq-events.h
%{mingw64_includedir}/libpq-fe.h
%{mingw64_includedir}/pg*.h
%{mingw64_includedir}/postgres_ext.h
%{mingw64_includedir}/sql*.h
%{mingw64_libdir}/libecpg.dll.a
%{mingw64_libdir}/libecpg_compat.dll.a
%{mingw64_libdir}/libpgtypes.dll.a
%{mingw64_libdir}/libpq.dll.a
%{mingw64_libdir}/pkgconfig/*.pc


%files -n mingw64-postgresql-static
%{mingw64_libdir}/libecpg.a
%{mingw64_libdir}/libecpg_compat.a
%{mingw64_libdir}/libpq.a
%{mingw64_libdir}/libpgcommon.a
%{mingw64_libdir}/libpgcommon_shlib.a
%{mingw64_libdir}/libpgfeutils.a
%{mingw64_libdir}/libpgport.a
%{mingw64_libdir}/libpgport_shlib.a
%{mingw64_libdir}/libpgtypes.a


%changelog
* Thu Jul 31 2025 Michael Cronenworth <mike@cchtml.com> - 16.9-1
- Update to 16.9

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 16.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 30 2024 Michael Cronenworth <mike@cchtml.com> - 16.3-1
- Update to 16.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 16 2023 Sandro Mani <manisandro@gmail.com> - 15.4-1
- Update to 15.4

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Sandro Mani <manisandro@gmail.com> - 15.3-1
- Update to 15.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 07 2023 Sandro Mani <manisandro@gmail.com> - 15.1-1
- Update to 15.1

* Tue Dec 06 2022 Sandro Mani <manisandro@gmail.com> - 15.0-1
- Update to 15.0

* Fri Nov 18 2022 Sandro Mani <manisandro@gmail.com> - 14.3-1
- Update to 14.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 11.5-12
- Rebuild with mingw-gcc-12

* Tue Feb 22 2022 Sandro Mani <manisandro@gmail.com> - 11.5-11
- Add libpathcch to postgresql_libs.patch
- Modernize spec

* Thu Feb 17 2022 Sandro Mani <manisandro@gmail.com> - 11.5-10
- Rebuild (openssl)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 12 13:45:14 GMT 2020 Sandro Mani <manisandro@gmail.com> - 11.5-6
- Rebuild (mingw-gettext)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Sandro Mani <manisandro@gmail.com> - 11.5-4
- Rebuild (gettext)

* Sun Apr 05 2020 Sandro Mani <manisandro@gmail.com> - 11.5-3
- Use winpthreads directly instead of internal reimplementation
- Add missing libraries to Libs.private of libpq.pc

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 04 2019 Michael Cronenworth <mike@cchtml.com> - 11.5-1
- New upstream release.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Michael Cronenworth <mike@cchtml.com> - 11.2-2
- Add patches to release proper static libraries.

* Sun Feb 17 2019 Michael Cronenworth <mike@cchtml.com> - 11.2-1
- New upstream release.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 05 2018 Michael Cronenworth <mike@cchtml.com> - 10.5-1
- New upstream release.
  https://www.postgresql.org/docs/10/static/release-10-5.html

* Fri Aug 24 2018 Richard W.M. Jones <rjones@redhat.com> - 10.3-3
- Rebuild for new mingw-openssl.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 Michael Cronenworth <mike@cchtml.com> - 10.3-1
- New upstream release.
  https://www.postgresql.org/docs/10/static/release-10-3.html

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Michael Cronenworth <mike@cchtml.com> - 10.1-1
- New upstream release.
  https://www.postgresql.org/docs/10/static/release-10-1.html

* Sat Nov 04 2017 Michael Cronenworth <mike@cchtml.com> - 10.0-1
- New upstream release.
  https://www.postgresql.org/docs/10/static/release-10.html

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> - 9.6.4-2
- Bump and rebuild for an rpm signing issue

* Thu Aug 10 2017 Michael Cronenworth <mike@cchtml.com> - 9.6.4-1
- New upstream release. (CVE-2017-7546 CVE-2017-7547 CVE-2017-7548)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 11 2017 Michael Cronenworth <mike@cchtml.com> - 9.6.3-1
- New upstream release. (CVE-2017-7484 CVE-2017-7485 CVE-2017-7486)

* Sat Apr 01 2017 Michael Cronenworth <mike@cchtml.com> - 9.6.2-1
- New upstream release.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Michael Cronenworth <mike@cchtml.com> - 9.6.1-1
- New upstream release.

* Wed Sep 21 2016 Michael Cronenworth <mike@cchtml.com> - 9.5.4-1
- New upstream release.

* Wed Jun 01 2016 Michael Cronenworth <mike@cchtml.com> - 9.5.3-1
- New upstream release.

* Thu Apr 14 2016 Michael Cronenworth <mike@cchtml.com> - 9.5.2-1
- New upstream release.

* Tue Feb 02 2016 Michael Cronenworth <mike@cchtml.com> - 9.5.0-1
- New upstream release.

* Mon Dec 28 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.5-1
- New upstream release.

* Mon Jul 27 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.4-1
- New upstream release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.2-1
- New upstream release.

* Wed Feb 25 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.1-1
- New upstream release.

* Tue Feb 03 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.0-1
- New upstream release.

* Sat Aug 16 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.5-1
- New upstream release.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.4-1
- New upstream release.

* Thu Mar 06 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.3-1
- New upstream release.

* Tue Jan 07 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.2-1
- New upstream release.

* Mon Oct 28 2013 Michael Cronenworth <mike@cchtml.com> - 9.3.1-1
- Rebase to 9.3 branch.

* Thu Aug 22 2013 Michael Cronenworth <mike@cchtml.com> - 9.2.4-4
- Use upstream patch for Windows error checking

* Thu Aug 15 2013 Michael Cronenworth <mike@cchtml.com> - 9.2.4-3
- Enable NLS, LDAP, TCL, and XML features.
- Patch for Windows error checking (RHBZ# 996529)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Michael Cronenworth <mike@cchtml.com> - 9.2.4-1
- Initial RPM release

