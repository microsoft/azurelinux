Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		ptlib
Summary:	Portable Tools Library
Version:	2.10.11
Release:	6%{?dist}
URL:		http://www.opalvoip.org/
License:	MPLv1.0

Source0:	https://download.gnome.org/sources/%{name}/2.10/%{name}-%{version}.tar.xz
Patch1:		ptlib-2.10.10-mga-bison-parameter.patch
Patch2:		ptlib-gcc5.patch
Patch3:		ptlib-gcc8.patch
Patch4:		ptlib-2.10.11-signed_int_overflow.patch
Patch5:		ptlib-2.10.11-openssl11.patch

BuildRequires:	gcc gcc-c++
BuildRequires:	pkgconfig expat-devel flex bison
BuildRequires:	alsa-lib-devel libv4l-devel
BuildRequires:	openldap-devel SDL-devel openssl-devel
BuildRequires:	boost-devel pulseaudio-libs-devel
BuildRequires:	perl-interpreter

%description
PTLib (Portable Tools Library) is a moderately large class library that 
has it's genesis many years ago as PWLib (portable Windows Library), a 
method to product applications to run on both Microsoft Windows and Unix 
systems. It has also been ported to other systems such as Mac OSX, VxWorks 
and other embedded systems.

It is supplied mainly to support the OPAL project, but that shouldn't stop
you from using it in whatever project you have in mind if you so desire. 

%package devel
Summary:	Development package for ptlib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The ptlib-devel package includes the libraries and header files for ptlib.

%prep
%setup -q 
%patch1 -p1 -b .bison
%patch2 -p1 -b .gcc5
%patch3 -p1 -b .gcc8
%patch4 -p1 -b .signed_int_overflow
%patch5 -p1 -b .openssl11

sed -i 's#bits/atomicity.h#ext/atomicity.h#g' configure*
sed -i 's#bits/atomicity.h#ext/atomicity.h#g' include/ptlib/critsec.h

%build
export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -std=gnu++98"
export STDCXXFLAGS="%{optflags} -std=gnu++98"
%configure --prefix=%{_prefix} --disable-static --enable-plugins --disable-oss --enable-v4l2 --disable-avc --disable-v4l --enable-pulse
make %{?_smp_mflags} V=1

%install
make PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir} install

perl -pi -e 's@PTLIBDIR.*=.*@PTLIBDIR = /usr/share/ptlib@' %{buildroot}%{_datadir}/ptlib/make/ptbuildopts.mak

# hack to fixup things for bug 197318
find %{buildroot}%{_libdir} -name '*.so*' -type f -exec chmod +x {} \;

#Remove static libs
find %{buildroot} -name '*.a' -delete

%ldconfig_scriptlets

%files
%license mpl-1.0.htm
%doc History.txt ReadMe.txt
%attr(755,root,root) %{_libdir}/libpt*.so.*
%dir %{_libdir}/%{name}-%{version}
%dir %{_libdir}/%{name}-%{version}/devices
%dir %{_libdir}/%{name}-%{version}/devices/sound
%dir %{_libdir}/%{name}-%{version}/devices/videoinput
# List these explicitly so we don't get any surprises
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/alsa_pwplugin.so
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/pulse_pwplugin.so
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/v4l2_pwplugin.so

%files devel
%{_libdir}/libpt*.so
%{_includedir}/*
%{_datadir}/ptlib
%{_libdir}/pkgconfig/ptlib.pc
%attr(755,root,root) %{_bindir}/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.10.11-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Robert Scheck <robert@fedoraproject.org> - 2.10.11-3
- Backported upstream change for gcc signed int overflow (#1696458)
- Added patch from openSUSE to build against OpenSSL 1.1 rather 1.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 21 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.11-1
- 2.10.11 stable release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 2.10.10-16
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 2.10.10-15
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.10-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 2.10.10-13
- rebuild for Boost 1.58

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.10.10-11
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 26 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.10-10
- Add patch to fix FTBFS with gcc5

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 2.10.10-9
- Rebuild for boost 1.57.0

* Mon Sep  1 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.10-8
- Add patch to fix build against bison3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 2.10.10-5
- Rebuild for boost 1.55.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 2.10.10-3
- Rebuild for boost 1.54.0

* Thu Mar  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.10-2
- Add patch to fix crash in webcam - RHBZ 907303

* Wed Feb 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.10-1
- New 2.10.10 stable release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.9-1
- New 2.10.9 stable release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-4
* Sat Aug 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.10.7-1
- New 2.10.7 stable release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-3
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.10.2-1
- New 2.10.2 stable release

* Sat Jul 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.10.1-1
- New 2.10.1 stable release

* Wed May  4 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.8.3-5
- Add patch to fix ptlib using internal gcc functions

* Wed Apr 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.8.3-4
- Add initial upstream patch to deal with Network interfaces with names other than eth - RHBZ 682388

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 27 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.8.3-2
- Let rpmbuild strip binaries.

* Thu Dec 23 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 2.8.3-1
- New 2.8.3 stable release

* Mon May 31 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.7-1
- New 2.6.7 stable release

* Tue Sep 22 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.5-1
- New 2.6.5 stable release

* Sat Aug 22 2009 Tomas Mraz <tmraz@redhat.com> - 2.6.4-5
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.4-1
- New 2.6.4 stable release

* Tue May 19 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.2-1
- New stable release for ekiga 3.2.1

* Wed Mar 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.1-1
- New stable release for ekiga 3.2.0

* Tue Mar  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.0-1
- New release for ekiga 3.1.2 beta

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.5.2-4
- rebuild with new openssl

* Tue Jan 13 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.2-3
- Add an extra build dep

* Tue Jan  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.2-2
- remove --enable-opal termpoarily, ironically so opal will compile

* Tue Jan  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.2-1
- New release for ekiga 3.1.0 beta

* Mon Oct 20 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.2-1
- Update to new stable release for ekiga 3.0.1

* Tue Sep 23 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.1-1
- Update to new stable release for ekiga 3, disable v4l1

* Wed Sep 10 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.1-2
- Build fixes from package review

* Sun Jun 8 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.1-1
- Initial version of ptlib
