Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		xcb-util
Version:	0.4.0
Release:	16%{?dist}
Summary:	Convenience libraries sitting on top of libxcb
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:	gcc
BuildRequires:	pkgconfig(xcb) >= 1.4


%description
The xcb-util module provides a number of libraries which sit on top of
libxcb, the core X protocol library, and some of the extension
libraries. These experimental libraries provide convenience functions
and interfaces which make the raw X protocol more usable. Some of the
libraries also provide client-side code which is not strictly part of
the X protocol but which have traditionally been provided by Xlib.


%package 	devel
Summary:	Development and header files for xcb-util
Requires:	%{name}%{?isa} = %{version}-%{release}

%description	devel
Development files for xcb-util.


%prep
%setup -q


%build
%configure --with-pic --disable-static --disable-silent-rules
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm %{buildroot}%{_libdir}/*.la


%ldconfig_post


%ldconfig_postun


%files
%doc README
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif # licensedir
%{_libdir}/libxcb-util.so.1*


%files devel
%doc NEWS
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h


%changelog
* Fri Jul 12 2024 Hideyuki Nagase <hideyukn@microsoft.com> - 0.4.0-16
- Moved from SPECS-EXTENDED to SPECS.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.0-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 0.4.0-10
- Use ldconfig scriptlet macros

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec  5 2015 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.0-4
- Mark license with %%license.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 22 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.0-2
- Move NEWS to -devel.

* Wed Oct 22 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.0-1
- Update to 0.4.0.
- Modernize spec file.
- Include COPYING.
- Update requirements.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 0.3.9-1
- xcb-util 0.3.9 (#828286)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Adam Jackson <ajax@redhat.com> 0.3.8-1
- xcb-util 0.3.8

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 28 2009 Michal Nowak <mnowak@redhat.com> - 0.3.6-1
- 0.3.6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Adam Jackson <ajax@redhat.com> 0.3.5-1
- xcb-util 0.3.5

* Mon Jul 06 2009 Adam Jackson <ajax@redhat.com> 0.3.4-2
- Explicitly list DSOs so we're notified of version changes.

* Sat Jun 13 2009 Michal Nowak <mnowak@redhat.com> - 0.3.4-1
- 0.3.4; needed for Awesome 3.3

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Michal Nowak <mnowak@redhat.com> - 0.3.3-1
- 0.3.3
- removed patches already in git (and 0.3.3)

* Fri Dec 19 2008 Michal Nowak <mnowak@redhat.com> - 0.3.2-2
- hack the sed lines after %%configure out and hack chrpath in
- make check is running again

* Thu Dec 18 2008 Michal Nowak <mnowak@redhat.com> - 0.3.2-1
- 0.3.2
- remove rpath (x86-64)
- xcb_keysyms: remove xcb_lookup_t
- Revert "keysyms: use xcb_key_lookup_t type for col paramter"
- temporary disabled %%check due to RPATH regression

* Thu Dec  4 2008 Michal Nowak <mnowak@redhat.com> - 0.3.1-2
- patch for exit() in aux library (Peter Harris)
- slight changes in spec file

* Mon Nov 24 2008 Michal Nowak <mnowak@redhat.com> - 0.3.1-1
- 0.3.1
- fix license issue (Jonathan Landis)

* Fri Sep 19 2008 Michal Nowak <mnowak@redhat.com> - 0.3.0-1
- bump to 0.3.0

* Sun Aug 17 2008 Michal Nowak <mnowak@redhat.com> - 0.2.1-2
- new build deps: gperf, pkgconfig, libxcb, m4, xorg-x11-proto-devel
- not installing *.a files anymore
- configure with --with-pic

* Mon Aug 04 2008 Michal Nowak <mnowak@redhat.com> - 0.2.1-1
- initial package

