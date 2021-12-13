Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:       ibus-rawcode
Version:    1.3.2
Release:    17%{?dist}
Summary:    The Rawcode engine for IBus input platform
License:    GPLv2+
URL:        https://pagure.io/ibus-rawcode
Source0:    https://releases.pagure.org/ibus-sayura/%{name}-%{version}.tar.gz

BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  ibus-devel


Requires: ibus >= 1.5.3

%description
The Rawcode engine for IBus platform.

%prep
%setup -q

%build
%configure --disable-static
# make -C po update-gmo
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{python_sitearch}/_rawcode.la

%find_lang %{name}

%post
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%postun
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_libexecdir}/ibus-engine-rawcode
%{_datadir}/ibus-rawcode
%{_datadir}/ibus/component/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.2-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 09 2017 Pravin Satpute <psatpute@redhat.com> - 1.3.2-9
- Change in upstream hosting from Fedorahosted to pagure.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 04 2013 Pravin Satpute <psatpute@redhat.com> - 1.3.2-3
- Resolves #1013989: ibus write-cache --system 

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Pravin Satpute <psatpute@redhat.com> - 1.3.2-1
- configured with autoconf 2.69

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1.20100707-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Pravin Satpute <psatpute@redhat.com> - 1.3.1.20100707-9
- spec file cleanup

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1.20100707-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 07 2012 Pravin Satpute <psatpute@redhat.com> - 1.3.1.20100707-7
- rebuild for broken dependancies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1.20100707-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011 Pravin Satpute <psatpute@redhat.com> - 1.3.1.20100707-5
- Resolved bug #741189

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1.20100707-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Pravin Satpute <psatpute@redhat.com> - 1.3.1.20100707-3
- rebuild for broken dependancies

* Wed Jul 07 2010 Pravin Satpute <psatpute@redhat.com> - 1.3.1.20100707-1
- upstream new release
- fixed bug 612042

* Fri Jun 11 2010 Pravin Satpute <psatpute@redhat.com> - 1.3.0.20100421-2
- added auxiliary text support, for space hit
- fixed bug 602942

* Wed Apr 21 2010 Pravin Satpute <psatpute@redhat.com> - 1.3.0.20100421-1
- upstream new release
- fixed bug 584233, 584240 

* Mon Feb 08 2010 Adam Jackson <ajax@redhat.com> 1.2.99.20100208-2
- Rebuild for new libibus.so.2 ABI.

* Mon Feb 08 2010 Pravin Satpute <pravin.d.s@gmail.com> - 1.2.99.20100208-1
- updated patches for code enhancements from phuang for ibus-1.2.99
- new upstream release

* Fri Dec 11 2009 Pravin Satpute <psatpute@redhat.com> - @VERSON@-4
- resolved bug 546521

* Tue Nov 17 2009 Pravin Satpute <psatpute@redhat.com> - @VERSON@-3
- resolved bug 531989

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090703-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Pravin Satpute <psatpute@redhat.com> - @VERSON@-1
- upstream release 1.2.0

* Sun Jun 28 2009 Matthias Clasen <mclasen@redhat.com> - 1.0.0.20090303-3
- Rebuild against newer ibus

* Tue Mar 03 2009 Pravin Satpute <pravin.d.s@gmail.com> - 1.0.0.20090303-2
- removed mod_path
- added build requires ibus-devel

* Tue Mar 03 2009 Pravin Satpute <pravin.d.s@gmail.com> - 1.0.0.20090303-1
- The first version.
