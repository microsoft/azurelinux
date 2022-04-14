Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          xapian-core
Version:       1.4.14
Release:       2%{?dist}
Summary:       The Xapian Probabilistic Information Retrieval Library
License:       GPLv2+
URL:           http://www.xapian.org/
Source0:       http://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.xz

BuildRequires: gcc gcc-c++
BuildRequires: libuuid-devel
BuildRequires: zlib-devel
%if ! 0%{?_module_build}
%ifarch %{valgrind_arches}
BuildRequires: valgrind-devel
%endif
%endif
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}


%description
Xapian is an Open Source Probabilistic Information Retrieval Library. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications

%package libs
Summary:       Xapian search engine libraries

%description libs
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
libraries for applications using Xapian functionality

%package devel
Summary:       Files needed for building packages which use Xapian
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
Requires:      libuuid-devel

%description devel
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for building packages which use Xapian

%prep
%autosetup -p1

%build
# Disable SSE on x86, but leave it intact for x86_64
%ifarch x86_64
%configure --disable-static
%else
%configure --disable-static --disable-sse
%endif

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{make_build}

%install
%{make_install}

# Remove libtool archives
find $RPM_BUILD_ROOT -name '*.la' -delete

# Remove the dev docs, we pick them up below
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%ldconfig_scriptlets libs

%files
%doc AUTHORS NEWS README
%{_bindir}/xapian*
%{_bindir}/quest
%{_bindir}/copydatabase
%{_bindir}/simpleindex
%{_bindir}/simplesearch
%{_bindir}/simpleexpand
%{_datadir}/xapian-core/
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian*
%{_mandir}/man1/quest.1*
%{_mandir}/man1/copydatabase.1*

%files libs
%license COPYING
%{_libdir}/libxapian.so.*

%files devel
%doc HACKING PLATFORMS docs/*html docs/apidoc
%{_bindir}/xapian-config
%{_includedir}/xapian
%{_includedir}/xapian.h
%{_libdir}/libxapian.so
%{_libdir}/cmake/xapian
%{_libdir}/pkgconfig/xapian-core.pc
%{_datadir}/aclocal/xapian.m4
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian-config.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.14-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 10 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.14-1
- Update to 1.4.14

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Peter Robinson <pbrobinson@gmail.com> - 1.4.13-2
- Upstream fix for pruning under a positional check (rhbz 1766219)

* Thu Oct 17 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.13-1
- Update to 1.4.13

* Tue Aug 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.12-1
- Update to 1.4.12

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.11-1
- Update to 1.4.11

* Mon Feb 11 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.10-1
- Update to 1.4.10

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.9-1
- Update to 1.4.9

* Tue Aug 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.7-1
- Update to 1.4.7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul  3 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-1
- Update to 1.4.6
- CVE-2018-0499 fix (rhbz 1597583 1597585 1597586)

* Fri Mar  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.5-4
- Add gcc BR, spec cleanups

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 1.4.5-3
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.5-1
- Update to 1.4.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.4-1
- Update to 1.4.4

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Apr 21 2017 Karsten Hopp <karsten@redhat.com> - 1.4.3-3
- use new _module_build macro to limit dependencies for Modularity

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb  4 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.3-1
- Update to 1.4.3

* Thu Nov 24 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-1
- Update to 1.4.1

* Tue Jul  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.23-1
- Update to 1.2.23

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.22-1
- Update to 1.2.22
- Use %%license

* Fri Nov 27 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.21-3
- Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.21-1
- Update to 1.2.21

* Wed Apr 15 2015 Petr Pisar <ppisar@redhat.com> - 1.2.20-2
- Rebuild owing to C++ ABI change in GCC-5 (bug #1195353)

* Sat Mar 21 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.20-1
- Update to 1.2.20

* Wed Feb 25 2015 Than Ngo <than@redhat.com> 1.2.19-3
- rebuilt against new gcc5

* Sat Feb 07 2015 Rex Dieter <rdieter@fedoraproject.org> 1.2.19-2
- rebuild (gcc)

* Tue Nov 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.19-1
- Update to 1.2.19

* Mon Sep  1 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.18-1
- Update to 1.2.18

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.17-1
- Update to 1.2.17

* Sun Jan 12 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.16-1
- Update to 1.2.16

* Fri Aug 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.15-1
- Update to 1.2.15

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.14
- Update to 1.2.14

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12

* Sun Apr 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for c++ ABI breakage

* Sat Jan 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4

* Mon Aug 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Thu Aug  5 2010 Adel Gadllah <adel.gadllah@gmail.com> - 1.2.2-5
- Reenable SSE on x86_64

* Thu Aug  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-4
- Disable SSE instructions by default

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-3
- And remove non spec cut-n-paste issue

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-2
- Add cmake stuff

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Fri May  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-4
- Move license to libs package, a few other spc cleanups

* Fri May  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-3
- Add the libtool archive (temporarily) to fix build of bindings

* Sat May  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-2
- Upload new source 

* Sat May  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
