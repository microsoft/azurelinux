Summary:	A library for generating Enhanced Metafiles
Summary(pl):	Biblioteka do generowania plików w formacie Enhanced Metafile
Name:		libEMF
Version:	1.0.13
Release:	2%{?dist}
License:	LGPLv2+ and GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://libemf.sourceforge.net/
Source0:	https://downloads.sourceforge.net/project/libemf/libemf/%{version}/libemf-%{version}.tar.gz
BuildRequires:	gcc-c++

%description
libEMF is a library for generating Enhanced Metafiles on systems which
don't natively support the ECMA-234 Graphics Device Interface
(GDI). The library is intended to be used as a driver for other
graphics programs such as Grace or gnuplot. Therefore, it implements a
very limited subset of the GDI.

%description -l pl
libEMF to biblioteka do generowania plików w formacie Enhanced
Metafile na systemach nie obsługujących natywnie systemu graficznego
ECMA-234 GDI. Biblioteka ma służyć jako sterownik dla innych programów
graficznych, takich jak Grace czy gnuplot. Z tego powodu ma
zaimplementowany bardzo ograniczony podzbiór GDI.

%package devel
Summary:	libEMF header files
Summary(pl):	Pliki nagłówkowe libEMF
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
libEMF header files.

%description devel -l pl
Pliki nagłówkowe libEMF.

%prep
%setup -q -n libemf-%{version}

%build
%configure \
	--disable-static \
	--enable-editing

make %{?_smp_mflags}

%install
export CPPROG="cp -p"
make install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libEMF.la

%check
make check

%ldconfig_scriptlets

%files
%license COPYING COPYING.LIB
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/printemf
%{_libdir}/libEMF.so.1*

%files devel
%doc doc/html/*
%{_libdir}/libEMF.so
%{_includedir}/libEMF

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.13-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Jun 21 2020 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.13-1
- update to 1.0.13 (#1846926)
- fixes CVE-2020-13999

* Fri May 01 2020 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.12-1
- update to 1.0.12 (#1827949)
- drop obsolete patch
- fixes CVE-2020-11863, CVE-2020-11864, CVE-2020-11865, CVE-2020-11866

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 07 2017 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.9-1
- update to 1.0.9
- use license macro
- tighten file list wildcards
- switch to https for source URL

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 09 2015 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.8-1
- update to 1.0.8
- undo upstream's broken partial renaming to libemf

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.7-8
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.7-7
- Add initial patch for aarch64 support (likely needs more work)

* Thu Mar 06 2014 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.7-4
- fix build on aarch64 (bug #925711)
- drop some obsolete/redundant specfile parts

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.7-1
- Update to latest upstream
- Drop all patches (upstreamed)
- Small packaging cleanups

* Mon Nov  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.6-2
- Fixes for non-x86 64bit architectures

* Mon Sep 03 2012 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.6-1
- updated to 1.0.6
- updated source URL
- dropped obsolete patch hunks and rebased patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.4-4
- Add support for ARM using definitions from WINE

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 25 2009 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.4-1
- updated to 1.0.4
- updated source URL
- dropped obsolete patch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Dan Horak <dan[at]danny.cz> - 1.0.3-9
- add support for s390/s390x

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-7
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-6
- fixed compilation with gcc-4.3

* Mon Dec 03 2007 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-5
- fixed compilation on Alpha platform (patch by Oliver Falk)

* Sat Aug 25 2007 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-4
- rebuild for BuildID
- update license tag

* Sun Nov 19 2006 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-3
- remove executable bit from libemf.h

* Sun Nov 19 2006 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-2
- added license texts
- preserved timestamps during install
- added %%check section

* Sun Nov 19 2006 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-1
- adapted PLD spec
- enhanced amd64 patch
