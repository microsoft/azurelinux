Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           jbigkit
Version:        2.1
Release:        19%{?dist}
Summary:        JBIG1 lossless image compression tools

License:        GPLv2+
URL:            https://www.cl.cam.ac.uk/~mgk25/jbigkit/
Source0:        https://www.cl.cam.ac.uk/~mgk25/download/jbigkit-%{version}.tar.gz
Patch0:         jbigkit-2.1-shlib.patch
Patch1:         jbigkit-2.0-warnings.patch
Patch2:         jbigkit-ldflags.patch
# patch for coverity issues - backported from upstream
Patch3:         jbigkit-covscan.patch

# gcc is no longer in buildroot by default
# gcc needed for libjbig library and several filters - jbigtopbm, pbmtojbig e.g.
BuildRequires: gcc

Requires:       jbigkit-libs%{?_isa} = %{version}-%{release}

%package libs
Summary:        JBIG1 lossless image compression library

%package devel
Summary:        JBIG1 lossless image compression library -- development files
Requires:       jbigkit-libs%{?_isa} = %{version}-%{release}

%description libs
JBIG-KIT provides a portable library of compression and decompression
functions with a documented interface that you can include very easily
into your image or document processing software. In addition, JBIG-KIT
provides ready-to-use compression and decompression programs with a
simple command line interface (similar to the converters found in netpbm).

JBIG-KIT implements the specification:
    ISO/IEC 11544:1993 and ITU-T Recommendation T.82(1993):
     Information technology — Coded representation of picture and audio
     information — Progressive bi-level image compression 

which is commonly referred to as the “JBIG1 standard”

%description devel
The jbigkit-devel package contains files needed for development using 
the JBIG-KIT image compression library.

%description
The jbigkit package contains tools for converting between PBM and JBIG1
formats.


%prep
%setup -q -n jbigkit-2.1
%patch 0 -p1 -b .shlib
%patch 1 -p1 -b .warnings
# jbigkit: Partial Fedora build flags injection (bug #1548546)
%patch 2 -p1 -b .ldflags
# covscan issues - backported from upstream
%patch 3 -p1 -b .covscan

%build
# get the correct redhat build flags
%set_build_flags
%make_build

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

install -p -m0755 libjbig/libjbig.so.%{version} $RPM_BUILD_ROOT/%{_libdir}
install -p -m0755 libjbig/libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_libdir}
ln -sf libjbig.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libjbig.so
ln -sf libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libjbig85.so

install -p -m0644 libjbig/jbig.h $RPM_BUILD_ROOT%{_includedir}
install -p -m0644 libjbig/jbig85.h $RPM_BUILD_ROOT%{_includedir}
install -p -m0644 libjbig/jbig_ar.h $RPM_BUILD_ROOT%{_includedir}

install -p -m0755 pbmtools/???to??? $RPM_BUILD_ROOT%{_bindir}
install -p -m0755 pbmtools/???to???85 $RPM_BUILD_ROOT%{_bindir}
install -p -m0644 pbmtools/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%check
make test

%ldconfig_scriptlets libs

%files
%{_bindir}/???to*
%{_mandir}/man1/*
%license COPYING

%files libs
%{_libdir}/libjbig*.so.%{version}
%doc ANNOUNCE TODO CHANGES
%license COPYING

%files devel
%{_libdir}/libjbig*.so
%{_includedir}/jbig*.h

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 25 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2.1-15
- fixed typo found by coverity

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2.1-13
- ship license in correct tag

* Tue Feb 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2.1-12
- 1548546 - jbigkit: Partial Fedora build flags injection

* Fri Feb 09 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2.1-10
- remove old stuff

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Sep  7 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.1-3
- Build with $RPM_OPT_FLAGS again

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Fridolin Pokorny <fpokorny@redhat.com> - 2.1-1
- Update to 2.1
- Removed jbigkit-CVE-2013-6369.patch (accepted by upstream)
- Updated jbigkit-2.0-warnings.patch to fix only fread() checks
- Updated jbigkit-2.0-shlib.patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0-10
- CVE-2013-6369 (#1085362)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-7
- Fix a number of compiler warnings per feedback from Ubuntu security team (#840608)

* Mon Apr 16 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-6
- Don't install up-to-date license file, use the upstream one. (#807760)

* Wed Mar 28 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-5
- Moving from rpmfusion-free to Fedora because it will be free of known patents
  in all countries from 2012-04-04 onwards
- Changed license from GPL to GPLv2+ and included up-to-date license file

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0-3
- rebuild for new F11 features

* Fri Sep 05 2008 David Woodhouse <dwmw2@infradead.org> 2.0-2
- Add missing jbig_ar.h

* Wed Sep 03 2008 David Woodhouse <dwmw2@infradead.org> 2.0-1
- Update to 2.0

* Sun Aug 03 2008 Thorsten Leemhuis <fedora@leemhuis.info> - 1.6-3
- rebuild

* Sun Oct  1 2006 David Woodhouse <dwmw2@infradead.org> 1.6-2
- Review fixes

* Tue Sep 12 2006 David Woodhouse <dwmw2@infradead.org> 1.6-1
- Initial version
