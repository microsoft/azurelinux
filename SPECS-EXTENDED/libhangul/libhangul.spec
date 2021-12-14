Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		libhangul
Version:	0.1.0
Release:	22%{?dist}

License:	LGPLv2+
URL:		https://github.com/libhangul/libhangul
# Change Source URL when upstream released tar ball
# Source0:	https://github.com/libhangul/libhangul/archive/libhangul-%{version}.tar.gz
Source0:	https://libhangul.googlecode.com/files/libhangul-%{version}.tar.gz

Summary:	Hangul input library
BuildRequires:	  gettext-devel, automake, libtool


%description
libhangul provides common features for Hangul input method programs.


%package devel
Summary:	Development files for libhangul
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
%description devel
This package contains development files necessary to develop programs
providing Hangul input.


%prep
%setup -q
autoreconf -fi

%build
%configure --disable-static

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm $RPM_BUILD_ROOT%{_libdir}/%{name}.la
%find_lang %{name}


%ldconfig_scriptlets


%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/lib*.so.*
%{_datadir}/%{name}
%{_bindir}/hangul

%files devel
%{_includedir}/hangul-*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.0-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Peng Wu <pwu@redhat.com> - 0.1.0-17
- Fixes URL

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.1.0-10
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Daiki Ueno <dueno@redhat.com> - 0.1.0-6
- pull the latest config.guess and config.sub for ARM64 port

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 Daiki Ueno <dueno@redhat.com> - 0.1.0-4
- follow the URL change of upstream

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Daiki Ueno <dueno@redhat.com> - 0.1.0-1
- update to 0.1.0
- drop buildroot cleanup

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Daiki Ueno <dueno@redhat.com> - 0.0.12-1
- update to 0.0.12
- install %%{_bindir}/hangul and locale files.

* Mon Oct  4 2010 Daiki Ueno <dueno@redhat.com> - 0.0.11-1
- update to 0.0.11

* Thu Dec 10 2009 Jens Petersen <petersen@redhat.com> - 0.0.10-1
- update to 0.0.10
- drop buildroot field and removal

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Jens Petersen <petersen@redhat.com> - 0.0.9-1
- update to 0.0.9 (fixes #501212)
- hanjac and hanja.txt are gone

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 28 2008 Jens Petersen <petersen@redhat.com> - 0.0.8-2
- add hanjac and hanja.bin to filelists

* Tue Oct 28 2008 Jens Petersen <petersen@redhat.com> - 0.0.8-1
- update to 0.0.8 (#468817)

* Wed Aug  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.0.6-5
- fix license tag

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.0.6-4
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.0.6-3
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 0.0.6-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Hu Zheng <zhu@redhat.com> - 0.0.6-1
- New upstream release.

* Mon Feb 19 2007 Akira TAGOH <tagoh@redhat.com> - 0.0.4-2
- Better descriptions.

* Fri Feb 16 2007 Akira TAGOH <tagoh@redhat.com> - 0.0.4-1
- New upstream release.
- cleanup spec.

* Wed Nov 29 2006 Akira TAGOH <tagoh@redhat.com> - 0.0.3-1
- Initial package.

