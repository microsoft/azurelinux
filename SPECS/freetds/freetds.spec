%define bits	%{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32}
Summary:        Implementation of the TDS (Tabular DataStream) protocol
Name:           freetds
Version:        1.3.20
Release:        1%{?dist}
License:        LGPLv2+ AND GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.freetds.org/
Source0:        ftp://ftp.freetds.org/pub/freetds/stable/freetds-%{version}.tar.bz2
Source1:        freetds-tds_sysdep_public.h
BuildRequires:  docbook-style-dsssl
BuildRequires:  doxygen
BuildRequires:  gnutls-devel
BuildRequires:  krb5-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libtool
BuildRequires:  readline-devel
BuildRequires:  unixODBC-devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.

%package libs
Summary:        Libraries for %{name}
Requires:       %{name} = %{version}-%{release}

%description libs
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.
This package contains the libraries for %{name}.

%package devel
Summary:        Header files and development libraries for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%package doc
Summary:        Development documentation for %{name}
BuildArch:      noarch

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}, you will need to install
%{name}-doc.

%prep
%setup -q

#  correct perl path
sed -i '1 s,#!.*/perl,#!perl,' samples/*.pl

chmod -x samples/*.sh


%build

[ -f configure ] || NOCONFIGURE=yes ./autogen.sh

%configure \
	--disable-dependency-tracking \
	--disable-rpath \
	--disable-static \
	--with-tdsver="auto" \
	--with-unixodbc="%{_prefix}" \
	--enable-msdblib \
	--enable-sybase-compat \
	--with-gnutls \
	--enable-krb5

#  disable-rpath in configure does not work...
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_RIE|' libtool


make %{?_smp_mflags} DOCBOOK_DSL="`rpm -ql docbook-style-dsssl | grep -F html/docbook.dsl`"


%install

make install DESTDIR=%{buildroot}

find %{buildroot} -type f -name "*.la" -delete -print
chmod -x %{buildroot}%{_sysconfdir}/*

mv -f %{buildroot}%{_includedir}/tds_sysdep_public.h \
	%{buildroot}%{_includedir}/tds_sysdep_public_%{bits}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/tds_sysdep_public.h

rm -f samples/Makefile* samples/*.in samples/README

mv -f samples/unixodbc.freetds.driver.template \
	samples/unixodbc.freetds.driver.template-%{bits}

mkdir samples-odbc
mv -f samples/*odbc* samples-odbc

#  deinstall it for our own way...
mv -f %{buildroot}%{_docdir}/%{name} docdir
find docdir -type f -print0 | xargs -0 chmod -x


%ldconfig_scriptlets libs


%files
%{_bindir}/*
%license COPYING.txt
%doc AUTHORS.md BUGS.md NEWS.md README.md TODO.md doc/*.html
%doc docdir/userguide docdir/images
%{_mandir}/man1/*

%files libs
%license COPYING_LIB.txt
%{_libdir}/*.so.*
%{_libdir}/libtdsodbc.so
%doc samples-odbc
%config(noreplace) %{_sysconfdir}/*.conf
%{_mandir}/man5/*

%files devel
%doc samples
%{_libdir}/*.so
%exclude %{_libdir}/libtdsodbc.so
%{_includedir}/*

%files doc
%doc docdir/reference

%changelog
* Thu Dec 21 2023 Muhammad Falak <mwani@microsoft.com> - 1.3.20-1
- Upgrade version to 1.3.20

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.1.20-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Sep 16 2022 Osama Esmail <osamaesmail@microsoft.com> - 1.1.20-4
- Moved from SPECS-EXTENDED to SPECS
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.20-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov  7 2019 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.1.20-1
- update to 1.1.20

* Tue Jul  9 2019 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.1.11-1
- Upgrade to 1.1.11 (#1728191)

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.00.38-8
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.00.38-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 11 2017 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.00.38-1
- Update to 1.00.38
- split freetds-libs package (for multiarch support)
- change default tds vesrion to auto
- move odbc plugin from devel to libs package (#1449881)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.95.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.95.81-2
- Rebuild for readline 7.x

* Wed Feb 10 2016 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.95.81-1
- update to 0.95.81
- use proper rpm macros to determine 64 bit arches

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.95.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.95.19-1
- Upgrade to 0.95.19

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-16.git0a42888
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-15.git0a42888
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-14.git0a42888
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tomáš Mráz <tmraz@redhat.com> - 0.91-13.git0a42888
- Rebuild for new libgcrypt

* Fri Jan 10 2014 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-12.git0a42888
- add ppc64le to the list of 64bit arches (#1051199)

* Tue Dec  3 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-11.git0a42888
- update to the latest git source for 0_91 branch
- fix format-security issue (#1037071)

* Thu Aug 22 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-10.git748aa26
- update to the latest git source for 0_91 branch
- fix #999696

* Wed Aug  7 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-9.gitb760a89
- update to the latest git source for 0_91 branch
- fix #992295, #993762

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8.gitf3ae29d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-7.gitf3ae29d
- add aarch64 to the list of 64bit arches (#966129)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6.gitf3ae29d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-5.gitf3ae29d
- update to the latest git source for 0_91 branch
- fix #870483

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-3
- Enable Kerberos support (#797276)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-1
- Upgrade to 0.91
- Drop shared-libtds support

* Wed Mar  9 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.3.20110306dev
- update to the latest stable snapshot 0.82.1.dev.20110306
- make build with shared-libtds conditional
- disable shared-libtds patch by default (seems noone uses it for now)

* Mon Feb 14 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.2.20100810dev
- fix again shared-libtds patch to provide increased library version

* Thu Feb 10 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.1.20100810dev
- update to the latest stable snapshot 0.82.1.dev.20100810
- fix shared-libtds patch to provide properly library names

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-5
- add upstream patch cspublic.BLK_VERSION_150.patch (#492393)

* Tue Feb 24 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-4
- fix autoconf data for libtool2 (patch by Tom Lane <tgl@redhat.com>)

* Fri Jan 30 2009 Karsten Hopp <karsten@redhat.com> 0.82-3
- add s390x to 64 bit archs

* Sun Jan 11 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-3
- Use gnutls for SSL (#479148)

* Tue Jun 17 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-2
- Continue to provide an internal libtds library as public
  (patch from Hans de Goede, #451021). This shared library is needed
  for some existing applications (libgda etc.), which still use it directly.

* Mon Jun  9 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-1
- Upgrade to 0.82

* Tue Feb 26 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-11
- fix "64 or 32 bit" test (#434975)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.64-10
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-9
- drop "Obsoletes:" from -doc subpackage to avoid extra complexity.

* Fri Jan 25 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-8
- resolve multiarch conflicts (#341181):
  - split references to separate freetds-doc subpackage
  - add arch-specific suffixes for arch-specific filenames in -devel
  - add wrapper for tds_sysdep_public.h
- add readline support (#430196)

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.64-7
- Rebuild for selinux ppc32 issue.

* Thu Aug 16 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change License tag to "LGPLv2+ and GPLv2+"

* Fri Jun 15 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-6 
- bump release to provide update path over Livna

* Wed Jun 13 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-5
- spec file cleanups
- allowed for Fedora (no patent issues exist), clarification by
  James K. Lowden <jklowden [AT] freetds.org>
- approved for Fedora (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Wed Aug  2 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- approved for Livna (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Tue Aug  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- add patch to fix sed scripts in the doc/ Makefile
- avoid using rpath in binaries
- cleanup in samples/ dir

* Thu Jul 27 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-3
- rebuild userguide too.
- move reference docs to -devel

* Mon Jul 24 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-2
- Properly clear extra executable bit in source
- Regenerate docs using doxygen

* Thu Jul 20 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-1
- Upgrade to 0.64
- Some spec file and distro cleanups

* Tue Sep 20 2005 V.C.G.Yeah <VCGYeah@iname.com> - 0.63-1
- Upgrade to 0.63
- spec file cleanups
- build static libs conditional

* Thu Sep  2 2004 V.C.G.Yeah <VCGYeah@iname.com> - 0.62.4-1Y
- Updated to release 0.62.4.
- Leave includes in system default include dir (needed for php-mssql build)

* Mon May 17 2004 Dag Wieers <dag@wieers.com> - 0.62.3-1
- Updated to release 0.62.3.

* Wed Feb 04 2004 Dag Wieers <dag@wieers.com> - 0.61.2-0
- Added --enable-msdblib configure option. (Dean Mumby)
- Updated to release 0.61.2.

* Fri Jun 13 2003 Dag Wieers <dag@wieers.com> - 0.61-0
- Initial package. (using DAR)
