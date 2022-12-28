Summary:        Library to render text and graphic overlays onto video images
Name:           libucil
Version:        0.9.10
Release:        22%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.unicap-imaging.org/
Source0:        %{_mariner_sources_url}/%{name}-%{version}.tar.gz
# check return value of theora_encode_init() (#627890)
Patch0:         libucil-0.9.8-bz627890.patch
# fix some memory leaks
Patch1:         libucil-0.9.10-leaks.patch
# fix some compile-time warnings
Patch2:         libucil-0.9.10-warnings.patch
# asoundlib.h is alsa/asoundlib.h meanwhile
Patch3:         libucil-0.9.10-include-alsa.patch
BuildRequires:  %{_bindir}/perl
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk-doc >= 1.4
BuildRequires:  intltool
BuildRequires:  libogg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtheora-devel
BuildRequires:  libtool
BuildRequires:  libunicap-devel
BuildRequires:  libvorbis-devel
BuildRequires:  pango-devel
BuildRequires:  perl(XML::Parser)

%description
Unicap provides a uniform interface to video capture devices. It allows
applications to use any supported video capture device via a single API.
The related ucil library provides easy to use functions to render text
and graphic overlays onto video images.

%package devel
Summary:        Development files for the ucil library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libunicap-devel
Requires:       pkgconfig

%description devel
The libucil-devel package includes header files and libraries necessary
for developing programs which use the ucil library. It contains the API
documentation of the library, too.

%prep
%autosetup -p1
# fixes for gtk-doc 1.26
sed -i -e '/^DOC_SOURCE_DIR/s/--source-dir=//g' doc/libucil/Makefile.am
mkdir -p m4
gtkdocize --copy
autoreconf -fiv

%build
%configure --disable-rpath --disable-gtk-doc
%make_build

%install
%make_install

# Don't install any static .a and libtool .la files
rm -f %{buildroot}%{_libdir}/%{name}.{a,la}

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS ChangeLog README
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/unicap/*.h
%exclude %{_datadir}/gtk-doc/html/%{name}

%changelog
* Wed Dec 28 2022 Muhammad Falak <mwani@microsoft.com> - 0.9.10-22
- Configure with 'disable-gtk-doc'
- Switch to `%autosetup`
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.10-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.10-4
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Kamil Dudka <kdudka@redhat.com> 0.9.10-2
- fix some memory leaks and compile-time warnings

* Mon Oct 04 2010 Robert Scheck <robert@fedoraproject.org> 0.9.10-1
- Upgrade to 0.9.10

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> 0.9.8-6
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-5
- upstream patch for #632439
- check return value of theora_encode_init() (#627890)

* Wed Aug 25 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-4
- fix SIGSEGV in ucil_theora_encode_thread (#627161)

* Wed Jun 02 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-3
- fix SIGSEGV in ucil_alsa_fill_audio_buffer (#572966)
- fix SIGSEGV in ucil_theora_encode_thread (#595863)

* Fri Mar 12 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-2
- build the package in %%build

* Sun Feb 21 2010 Robert Scheck <robert@fedoraproject.org> 0.9.8-1
- Upgrade to 0.9.8 (#530702, #567109, #567110, #567111)
- Splitting of unicap into libunicap, libucil and libunicapgtk

* Sat Oct 24 2009 Robert Scheck <robert@fedoraproject.org> 0.9.7-1
- Upgrade to 0.9.7 (#530702)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Dan Horak <dan[at]danny.cz> 0.9.5-2
- don't require libraw1394 on s390/s390x

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.9.5-1
- Upgrade to 0.9.5

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.9.3-2
- Rebuild against gcc 4.4 and rpm 4.6

* Mon Oct 13 2008 Robert Scheck <robert@fedoraproject.org> 0.9.3-1
- Upgrade to 0.9.3 (#466825, thanks to Hans de Goede)
- Enabled libv4l support for the new gspca kernel driver

* Sat Aug 09 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-4
- Rebuild to get missing dependencies back (#443015, #458527)

* Tue Aug 05 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-3
- Filter the unicap plugins which overlap with libv4l libraries

* Tue Jul 22 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-2
- Rebuild for libraw1394 2.0.0

* Mon May 19 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-1
- Upgrade to 0.2.23
- Corrected packaging of cpi/*.so files (thanks to Arne Caspari)

* Sat May 17 2008 Robert Scheck <robert@fedoraproject.org> 0.2.22-1
- Upgrade to 0.2.22 (#446021)

* Sat Feb 16 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-3
- Added patch to correct libdir paths (thanks to Ralf Corsepius)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-2
- Changes to match with Fedora Packaging Guidelines (#431381)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-1
- Upgrade to 0.2.19
- Initial spec file for Fedora and Red Hat Enterprise Linux
