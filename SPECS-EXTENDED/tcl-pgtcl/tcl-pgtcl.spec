Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global docs_hash 20131007a

Name:		tcl-pgtcl
Version:	2.1.1
Release:	12%{?dist}
Summary:	A Tcl client library for PostgreSQL

URL:		https://sourceforge.net/projects/pgtclng/
# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License: PostgreSQL

Source0:	https://downloads.sourceforge.net/pgtclng/pgtcl%{version}.tar.gz
# Note that for some reason docs are date-labeled not version-labeled
Source1:	https://downloads.sourceforge.net/pgtclng/pgtcldocs-%{docs_hash}.zip

Patch1:		pgtcl-no-rpath.patch

Provides:	pgtcl = %{version}-%{release}
# pgtcl was originally shipped as a sub-RPM of the PostgreSQL package;
# these Provides/Obsoletes give a migration path.  Note there is no
# intention of changing the version numbers in future.
Provides:	postgresql-tcl = 8.5.0-1
Obsoletes:	postgresql-tcl < 8.5

BuildRequires:  gcc
BuildRequires:	libpq-devel tcl-devel
BuildRequires:	autoconf

Requires:	tcl(abi) >= 8.5

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}


%description
PostgreSQL is an advanced Object-Relational database management system.
The tcl-pgtcl package contains Pgtcl, a Tcl client library for connecting
to a PostgreSQL server.


%prep
%setup -q -n pgtcl%{version}

unzip %{SOURCE1}
PGTCLDOCDIR=`basename %{SOURCE1} .zip`
mv $PGTCLDOCDIR Pgtcl-docs

%patch 1 -p1

autoconf


%build
%configure --libdir=%{tcl_sitearch} --with-tcl=%{_libdir}
make all %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
# we don't really need to ship the .h file
rm -f $RPM_BUILD_ROOT%{_includedir}/libpgtcl.h


%files
%license COPYRIGHT
%{_libdir}/tcl%{tcl_version}/pgtcl%{version}/
%doc Pgtcl-docs/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.1-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Oct 12 2014 Pavel Raiskup <praiskup@redhat.com> - 2.1.1-1
- rebase to recent upstream release (#1144394), per release notes:
  https://sourceforge.net/projects/pgtclng/files/pgtclng/2.1.1/

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Wed May 07 2014 Pavel Raiskup <praiskup@redhat.com> - 2.1.0-1
- rebase to recent upstream relase (#1094731), per release notes:
  https://sourceforge.net/projects/pgtclng/files/pgtclng/2.1.0/
- spec cleanup per fedora-review

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Tom Lane <tgl@redhat.com> 2.0.0-1
- Update to pgtcl 2.0.0
- Update URLs to reference new project site at sourceforge

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Tom Lane <tgl@redhat.com> 1.8.0-1
- Update to pgtcl 1.8.0.
- Relabel license as PostgreSQL now that that's separately recognized by OSI.

* Thu Jan 21 2010 Tom Lane <tgl@redhat.com> 1.6.2-3
- Correct Source: tags and comment to reflect how to get the tarball.

* Tue Nov 24 2009 Tom Lane <tgl@redhat.com> 1.6.2-2
- Fix License tag as per discussion in PyGreSQL package review request.
Related: #452321

* Fri Jun 20 2008 Tom Lane <tgl@redhat.com> 1.6.2-1
- Created package by stripping down postgresql specfile and adjusting
  to meet current packaging guidelines for Tcl extensions.
