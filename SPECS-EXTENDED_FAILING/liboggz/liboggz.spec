Name:           liboggz
Version:        1.1.1
Release:        19%{?dist}
Summary:        Simple programming interface for Ogg files and streams

License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.xiph.org/oggz/
Source0:        http://downloads.xiph.org/releases/liboggz/%{name}-%{version}.tar.gz
# Always have oggz_off_t == loff_t even on 64-bit platforms
Patch0:		liboggz-1.1.1-multilib.patch

BuildRequires:  gcc
BuildRequires:  libogg-devel >= 1.0
BuildRequires:  doxygen
BuildRequires:  docbook-utils

%description
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

%package devel
Summary:	Files needed for development using liboggz
Requires:       liboggz = %{version}-%{release}
Requires:       libogg-devel >= 1.0
Requires:       pkgconfig

%description devel
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

This package contains the header files and documentation needed for
development using liboggz.

%package doc
Summary:        Documentation for liboggz
Requires:	liboggz = %{version}-%{release}

%description doc
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

This package contains HTML documentation needed for development using
liboggz.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .multilib

%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%check
# Tests disabled for moment because of rpath issue
#make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall docdir=$PWD/__docs_staging INSTALL="%{__install} -p"

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# not particularly interested in the tex docs, the html version has everything
rm -rf __docs_staging/latex

# Multilib fix: ensure generated headers have timestamps
# independent of build time
(cd include/oggz &&
    touch -r oggz_off_t_generated.h.in.multilib \
      $RPM_BUILD_ROOT%{_includedir}/oggz/oggz_off_t_generated.h
)


%ldconfig_scriptlets

                                                                                
%files
%doc AUTHORS ChangeLog COPYING README
# 0 length NEWS file
# %doc NEWS
%{_libdir}/liboggz.so.*
%{_mandir}/man1/*
%{_bindir}/oggz*

%files devel
%{_includedir}/oggz
%{_libdir}/liboggz.so
%{_libdir}/pkgconfig/oggz.pc

%files doc
%doc __docs_staging/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jul 27 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-6
- Make docs install work with unversioned doc dir setups.
- Fix URLs.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 29 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.1.1-1
- Update 1.1.1
- (CVE-2009-3377) CVE-2009-3377 liboggz: unspecified security fixes mentioned in MFSA 2009-63

* Thu Feb 04 2010 Adam Jackson <ajax@redhat.com> 0.9.8-5
- --disable-static, drop the .a files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Michel Salim <salimma@fedoraproject.org> - 0.9.8-2
- Multilib fixes (bugs #342291, #477291)

* Mon Jul  7 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.9.8-1
- Update to 0.9.8

* Wed May 21 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.9.7-1
- Update to 0.9.7

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-2
- Autorebuild for GCC 4.3

* Fri Jan 12 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-1
- new upstream release

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.4-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-2
- rebuilt

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-1
- new upstream release
- removed patch, was applied upstream

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-1
- new upstream release

* Mon Jul 18 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.2-1
- new upstream version
- removed patches
- moved devel docs to versioned location

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-2: rpmlint cleanup

* Fri Jun 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-1: initial package
